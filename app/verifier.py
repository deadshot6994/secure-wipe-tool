import json
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_certificate(paths):
    """Generate wipe certificate in JSON + PDF formats."""
    data = {
        "wiped_paths": paths,
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }

    # JSON certificate
    cert_json = "wipe_certificate.json"
    with open(cert_json, "w") as f:
        json.dump(data, f, indent=4)

    # PDF certificate
    cert_pdf = "wipe_certificate.pdf"
    c = canvas.Canvas(cert_pdf)
    c.drawString(100, 800, "Secure Wipe Certificate")
    c.drawString(100, 780, f"Date: {data['timestamp']}")
    c.drawString(100, 760, "Wiped Files/Folders:")
    y = 740
    for p in paths:
        c.drawString(120, y, p)
        y -= 20
    c.save()

    return os.path.abspath(cert_pdf)
