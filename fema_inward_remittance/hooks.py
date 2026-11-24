# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "fema_inward_remittance"
app_title = "Frappe Cross Border Wire Fema Inward Remittance"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Cross Border Wire Fema Inward Remittance - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/fema_inward_remittance/css/fema_inward_remittance.bundle.css"
app_include_js = "/assets/fema_inward_remittance/js/fema_inward_remittance.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Cross Border Wire Fema Inward Remittance Entry": {
        "validate": "fema_inward_remittance.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "fema_inward_remittance.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "fema_inward_remittance.tasks.hourly_sync"
    ],
    "daily": [
        "fema_inward_remittance.tasks.daily_reconciliation"
    ],
    "weekly": [
        "fema_inward_remittance.tasks.weekly_digest"
    ]
}
