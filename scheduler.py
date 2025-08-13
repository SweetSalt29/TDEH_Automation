from db import SessionLocal, init_db, Patient, Visit
from datetime import date, timedelta, datetime
from whatsapp_web import send_whatsapp_web

init_db()
session = SessionLocal()

def send_tomorrow_reminders():
    tomorrow = date.today() + timedelta(days=1)
    visits = session.query(Visit).filter(Visit.revisit_date == tomorrow).all()
    for v in visits:
        p = session.query(Patient).get(v.patient_id)
        if not p:
            continue
        msg = f"Hello {p.name}, reminder: you have a follow-up appointment at our clinic tomorrow ({v.revisit_date}). Please reach on time."
        if send_whatsapp_web(p.contact, msg):
            print(datetime.now(), f"Reminder sent to {p.contact}")
        else:
            print(datetime.now(), f"Failed to send to {p.contact}")

if __name__ == "__main__":
    send_tomorrow_reminders()
