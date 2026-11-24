"""FEMA Cross-Border Inward Remittance & RBI Purpose Code Engine."""
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional

@dataclass
class InwardRemittanceWire:
    wire_reference_no: str     # SWIFT MT103 UETR
    remitter_name: str
    originating_country: str
    currency: str              # USD, EUR, GBP
    foreign_amount: float
    exchange_rate_applied: float
    realized_amount_inr: float = 0.0
    rbi_purpose_code: str = "" # e.g. P0802 for Software Exports, P0102 for Goods
    fira_document_id: str = ""
    status: str = "RECEIVED_UNRECONCILED"

class FEMAInwardRemittanceEngine:
    def __init__(self, exporter_ie_code: str):
        self.exporter_ie_code = exporter_ie_code
        self.wires: Dict[str, InwardRemittanceWire] = {}
        self.matched_invoices: Dict[str, str] = {}

    def process_incoming_wire(self, wire: InwardRemittanceWire, benchmark_fbil_rate: float) -> Dict[str, Any]:
        wire.realized_amount_inr = round(wire.foreign_amount * wire.exchange_rate_applied, 2)
        spread_per_unit = round(benchmark_fbil_rate - wire.exchange_rate_applied, 4)
        total_bank_spread_inr = round(spread_per_unit * wire.foreign_amount, 2)
        
        self.wires[wire.wire_reference_no] = wire
        return {
            "wire_reference_no": wire.wire_reference_no,
            "currency": wire.currency,
            "realized_inr": wire.realized_amount_inr,
            "bank_fx_spread_loss_inr": total_bank_spread_inr,
            "requires_purpose_code": bool(not wire.rbi_purpose_code)
        }

    def allocate_fira_and_settle_invoice(self, wire_ref: str, invoice_no: str, rbi_purpose_code: str, fira_no: str) -> Dict[str, Any]:
        if wire_ref not in self.wires:
            raise ValueError(f"Wire {wire_ref} not found.")
        wire = self.wires[wire_ref]
        
        wire.rbi_purpose_code = rbi_purpose_code
        wire.fira_document_id = fira_no
        wire.status = "SETTLED_EDPMS_AUDIT_READY"
        self.matched_invoices[invoice_no] = wire_ref

        return {
            "wire_reference_no": wire_ref,
            "invoice_no": invoice_no,
            "rbi_purpose_code": wire.rbi_purpose_code,
            "fira_number": wire.fira_document_id,
            "status": wire.status
        }
