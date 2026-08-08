import io
import os
from datetime import datetime

from flask import Flask, request, render_template, send_file
from docxtpl import DocxTemplate

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH = os.path.join(BASE_DIR, "MOU_template.docx")
TEMPLATES_DIR = os.path.join(os.path.dirname(BASE_DIR), "templates")

app = Flask(__name__, template_folder=TEMPLATES_DIR)


@app.route("/", methods=["GET"])
def index():
    return render_template("form.html")


@app.route("/generate", methods=["POST"])
def generate():
    f = request.form

    guarantors = [g.strip() for g in f.getlist("guarantor_name") if g.strip()]

    context = {
        "mou_date": f.get("mou_date", ""),
        "lessee_name": f.get("lessee_name", ""),
        "lessee_address_line1": f.get("lessee_address_line1", ""),
        "lessee_address_line2": f.get("lessee_address_line2", ""),
        "lessee_contact_name": f.get("lessee_contact_name", ""),
        "guarantors": guarantors,
        "num_units": f.get("num_units", ""),
        "asset_model": f.get("asset_model", ""),
        "oem_name": f.get("oem_name", ""),
        "asset_location": f.get("asset_location", ""),
        "tenure_months": f.get("tenure_months", ""),
        "security_deposit": f.get("security_deposit", ""),
        "upfront_fee": f.get("upfront_fee", ""),
        "monthly_rental": f.get("monthly_rental", ""),
        "penalty_per_day": f.get("penalty_per_day", ""),
        "max_km": f.get("max_km", ""),
        "escrow_days": f.get("escrow_days", ""),
        "rc_send_days": f.get("rc_send_days", ""),
        "rc_endorsement_days": f.get("rc_endorsement_days", ""),
        "lessor_signatory_name": f.get("lessor_signatory_name", ""),
        "lessee_signatory_name": f.get("lessee_signatory_name", ""),
    }

    tpl = DocxTemplate(TEMPLATE_PATH)
    tpl.render(context)

    buf = io.BytesIO()
    tpl.save(buf)
    buf.seek(0)

    lessee_slug = "".join(c if c.isalnum() else "_" for c in context["lessee_name"]) or "Lessee"
    filename = f"MOU_{lessee_slug}_{datetime.now().strftime('%b%Y')}.docx"

    return send_file(
        buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


# Vercel's Python runtime looks for a WSGI-compatible `app` object in this file.
