<!-- Banner -->
<p align="center">
  <img src="https://img.icons8.com/external-flat-juicy-fish/100/ffffff/external-eye-medical-flat-flat-juicy-fish.png" width="80" />
</p>
<h1 align="center" style="color:white;">🏥 TDEH Automation</h1>
<p align="center">
  <i style="color:lightgray;">Lightweight Clinic Management & WhatsApp Reminder System</i>
</p>

<!-- Badges -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-App-red.svg?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/SQLite-Database-yellow.svg?style=for-the-badge&logo=sqlite" />
  <img src="https://img.shields.io/badge/Automation-WhatsApp-green.svg?style=for-the-badge&logo=whatsapp" />
</p>

---

## ✨ Features  

- 📋 **Patient Registration** – Simple form for receptionist to log patient details  
- 🩺 **Diagnosis Recording** – Store diagnosis, prescribed meds, and follow-up date  
- 📅 **Automated Appointment Reminders** – Sends WhatsApp reminders the night before the revisit  
- 💬 **Thank You Messages** – Auto-send appreciation message after each visit  
- 🗄 **Paperless Records** – Stored securely in SQLite database  
- ⚡ **One-Man Deployable** – Works on a single laptop/PC without cloud setup  

---

## 📸 Workflow  

```mermaid
flowchart LR
    A[Receptionist Logs In] --> B[Enter Patient Details]
    B --> C[Doctor Diagnosis & Follow-up Date]
    C --> D[Send Thank You Message]
    D --> E[WhatsApp Reminder Before Revisit]
