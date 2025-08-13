import pywhatkit
import datetime
import time

def send_whatsapp_web(phone: str, message: str):
    """
    Send a WhatsApp message instantly via WhatsApp Web.
    phone: "+91XXXXXXXXXX" (include country code)
    """
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=20,  # seconds to wait before sending
            tab_close=True,
            close_time=3
        )
        time.sleep(5)  # buffer
        return True
    except Exception as e:
        print(f"Failed to send message to {phone}: {e}")
        return False
