import streamlit as st
from db import SessionLocal, init_db, Patient, Visit
from datetime import datetime, timedelta
import os
from whatsapp_web import send_whatsapp_web
from werkzeug.utils import secure_filename

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

init_db()
session = SessionLocal()

st.set_page_config(page_title="TDEH", layout="wide")

def auth():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if not st.session_state["logged_in"]:
        with st.form("login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                if username == "reception" and password == "clinic123":
                    st.session_state["logged_in"] = True
                    st.success("Logged in")
                else:
                    st.error("Wrong credentials")
    return st.session_state["logged_in"]

if not auth():
    st.stop()

st.title("Tamhane's Dental and Eye Hospital Portal")

menu = st.sidebar.selectbox("Menu", ["Register Patient", "New Visit / Diagnose", "Search", "Manual Backup"])

if menu == "Register Patient":
    st.header("Register Patient")
    with st.form("register"):
        name = st.text_input("Full name")
        contact = st.text_input("Contact (e.g. +91XXXXXXXXXX)")
        patients_age = st.number_input("Age", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male","Female","Other"])
        submitted = st.form_submit_button("Register")
        if submitted:
            p = Patient(name=name, contact=contact, patients_age=patients_age, gender=gender)
            session.add(p)
            session.commit()
            st.success(f"Patient registered with ID {p.id}")

if menu == "New Visit / Diagnose":
    st.header("New Visit")
    patients = session.query(Patient).order_by(Patient.name).all()
    patient_map = {f"{p.id} - {p.name}": p.id for p in patients}
    sel = st.selectbox("Select patient", ["-- Select --"] + list(patient_map.keys()))
    if sel != "-- Select --":
        pid = patient_map[sel]
        with st.form("visit"):
            diagnosis = st.text_area("Diagnosis")
            meds = st.text_area("Medications")
            revisit = st.date_input("Revisit Date", value=(datetime.today() + timedelta(days=3)).date())
            uploaded = st.file_uploader("Upload file (optional)", type=["pdf","png","jpg","jpeg"])
            submitted = st.form_submit_button("Submit Visit")
            if submitted:
                file_path = None
                if uploaded:
                    filename = secure_filename(uploaded.name)
                    file_path = os.path.join(UPLOAD_DIR, f"{pid}_{int(datetime.utcnow().timestamp())}_{filename}")
                    with open(file_path, "wb") as f:
                        f.write(uploaded.getbuffer())
                v = Visit(patient_id=pid, diagnosis=diagnosis, meds=meds, revisit_date=revisit, uploaded_file=file_path)
                session.add(v)
                session.commit()
                st.success("Visit saved.")
                p = session.query(Patient).get(pid)
                msg = f"Hello {p.name}, thank you for visiting our clinic today. Diagnosis: {diagnosis}. Medicines: {meds}. Revisit on: {revisit}."
                if send_whatsapp_web(p.contact, msg):
                    st.info("Thank you message sent via WhatsApp")
                else:
                    st.error("Failed to send WhatsApp message")

if menu == "Search":
    st.header("Search Records")
    q = st.text_input("Search by name/contact")
    if st.button("Search"):
        results = session.query(Patient).filter((Patient.name.contains(q)) | (Patient.contact.contains(q))).all()
        for p in results:
            st.write(f"**{p.name}** ({p.contact}) - ID: {p.id}")
            for v in p.visits:
                st.write(f"  Visit {v.id} on {v.visit_date.date()} — {v.diagnosis} — Revisit: {v.revisit_date}")

if menu == "Manual Backup":
    st.header("Backup")
    if st.button("Create backup zip"):
        import zipfile, time
        backup_name = os.path.join("backups", f"backup_{int(time.time())}.zip")
        os.makedirs("backups", exist_ok=True)
        with zipfile.ZipFile(backup_name, 'w') as zf:
            zf.write('clinic.db')
            for root, _, files in os.walk(UPLOAD_DIR):
                for file in files:
                    zf.write(os.path.join(root, file))
        st.success(f"Backup created: {backup_name}")
