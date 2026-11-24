from setuptools import setup, find_packages

setup(
    name="frappe-cross-border-wire-fema-inward-remittance",
    version="1.0.0",
    description="Frappe FEMA Cross-Border Wire Engine: SWIFT Inward Remittance, RBI Purpose Codes, e-FIRA Vault & EDPMS Reconciler.",
    author="Shyam Kumar Pandey",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
