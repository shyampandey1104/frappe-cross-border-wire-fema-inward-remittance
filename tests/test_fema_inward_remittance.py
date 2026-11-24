import unittest
from fema_inward_remittance.engine import InwardRemittanceWire, FEMAInwardRemittanceEngine

class TestFEMAInwardRemittanceEngine(unittest.TestCase):
    def setUp(self):
        self.engine = FEMAInwardRemittanceEngine(exporter_ie_code="07AAA00000")

    def test_wire_processing_and_fx_spread(self):
        wire = InwardRemittanceWire(
            wire_reference_no="SWIFT-UETR-99812401", remitter_name="Acme Corp USA",
            originating_country="US", currency="USD", foreign_amount=50000.0,
            exchange_rate_applied=86.20
        )
        res = self.engine.process_incoming_wire(wire, benchmark_fbil_rate=86.55)
        self.assertEqual(res["realized_inr"], 4310000.0)
        self.assertEqual(res["bank_fx_spread_loss_inr"], 17500.0) # (86.55 - 86.20) * 50k

    def test_fira_allocation(self):
        wire = InwardRemittanceWire(
            wire_reference_no="SWIFT-UETR-99812402", remitter_name="Stripe Payments UK",
            originating_country="GB", currency="GBP", foreign_amount=20000.0,
            exchange_rate_applied=108.50
        )
        self.engine.process_incoming_wire(wire, benchmark_fbil_rate=108.70)
        alloc = self.engine.allocate_fira_and_settle_invoice(
            wire_ref="SWIFT-UETR-99812402", invoice_no="EXP-INV-2026-0041",
            rbi_purpose_code="P0802", fira_no="eFIRA-HDFC-2026-9901"
        )
        self.assertEqual(alloc["status"], "SETTLED_EDPMS_AUDIT_READY")

if __name__ == "__main__":
    unittest.main()
