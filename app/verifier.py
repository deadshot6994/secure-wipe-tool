import json
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from tkinter import filedialog

def generate_certificate(paths):
    """Generate or update wipe certificate (JSON + PDF)."""

    # Let user select save location
    cert_base = filedialog.asksaveasfilename(
        title="Save Certificate",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )

    if not cert_base:
        return None  # user cancelled

    cert_json = cert_base
    cert_pdf = cert_base.replace(".json", ".pdf")

    # Load existing JSON if it exists
    data = {"records": []}
    if os.path.exists(cert_json):
        with open(cert_json, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"records": []}

    # New record
    new_record = {
        "wiped_paths": paths,
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }
    data["records"].append(new_record)

    # Save JSON
    with open(cert_json, "w") as f:
        json.dump(data, f, indent=4)

    # Save PDF (append-like: just regenerate with all records)
    c = canvas.Canvas(cert_pdf)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 800, "Secure Wipe Certificate Log")

    y = 770
    for i, rec in enumerate(data["records"], start=1):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, y, f"Record {i}: {rec['timestamp']}")
        y -= 20
        c.setFont("Helvetica", 10)
        for p in rec["wiped_paths"]:
            c.drawString(120, y, f"- {p}")
            y -= 15
        y -= 10
        if y < 50:  # new page if space runs out
            c.showPage()
            y = 770

    c.save()

    return os.path.abspath(cert_pdf)
