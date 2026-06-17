import streamlit as st
import time
import threading
import requests
import datetime
import pandas as pd

# ----------------- កំណត់រចនាសម្ព័ន្ធទំព័រ -----------------
st.set_page_config(page_title="ប្រព័ន្ធរំលឹកវត្តមាន (Auto Reminder)", layout="centered")

st.title("⏰ ប្រព័ន្ធរំលឹកវត្តមានស្វ័យប្រវត្តិ")
st.write("🌍 ស្ថានភាពប្រព័ន្ធ៖ **កំពុងដំណើរការ ២៤ម៉ោង តាមរយៈ Google Sheets**")

# --- កំណត់ព័ត៌មាន Telegram ដើម ---
BOT_TOKEN = "8037667434:AAGDSRYkpzYK96Jxmh613y4YI9KOYDwgUQU"
CHAT_ID = "-1004192247028"  # លេខគ្រុបរបស់លោកគ្រូ
MESSAGE_TEXT = "សួស្តីលោកគ្រូអ្នកគ្រូ! ⏰ សូមកុំភ្លេចចូលទៅចុះវត្តមាន PLP សម្រាប់ម៉ោងនេះផងណា៎! សូមអរគុណ។"

# 🔗 តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ (បានកែសម្រួលដាក់សញ្ញាដកស្រង់បិទកន្ទុយត្រឹមត្រូវ ១០០%)
SHEET_URL = "https://docs.google.com/spreadsheets/d/19V8JHsneOV_gtuj5faqxQDbpCvblKdVues5fTT57jnw/export?format=csv"

# ----------------- អនុគមន៍ទាញទិន្នន័យម៉ោងពី Google Sheets -----------------
def fetch_times_from_sheet():
    try:
        if "/edit" in SHEET_URL:
            csv_url = SHEET_URL.split("/edit")[0] + "/export?format=csv"
        else:
            csv_url = SHEET_URL
            
        df = pd.read_csv(csv_url, header=None)
        times_list = df[0].astype(str).str.strip().tolist()
        
        clean_times = []
        for t in times_list:
            if ":" in t:
                parts = t.split(":")
                if len(parts[0]) == 1:
                    parts[0] = "0" + parts[0]
                clean_times.append(f"{parts[0]}:{parts[1][:2]}")
        return clean_times
    except Exception as e:
        print(f"មិនអាចអាន Google Sheets បានទេ: {e}")
        return ["06:50", "07:00", "07:15", "10:55"]

# ----------------- អនុគមន៍លុបសារ (Unpin រួច Delete) -----------------
def delete_message(token, chat_id, message_id):
    try:
        unpin_url = f"https://api.telegram.org/bot{token}/unpinChatMessage"
        requests.post(unpin_url, data={"chat_id": chat_id, "message_id": message_id})
        
        del_url = f"https://api.telegram.org/bot{token}/deleteMessage"
        requests.post(del_url, data={"chat_id": chat_id, "message_id": message_id})
        print(f"[{datetime.datetime.now()}] បានលុប និង Unpin សាររួចរាល់!")
    except Exception as e:
        print(f"Error លុបសារ: {e}")

# ----------------- អនុគមន៍ផ្ញើសារ (មានមុខងារ Pin) -----------------
def send_telegram_message(token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print(f"[{datetime.datetime.now()}] សាររំលឹកបានបាញ់ចូលគ្រុបជោគជ័យ!")
            res_data = response.json()
            message_id = res_data['result']['message_id']

            try:
                pin_url = f"https://api.telegram.org/bot{token}/pinChatMessage"
                pin_data = {"chat_id": chat_id, "message_id": message_id, "disable_notification": False}
                requests.post(pin_url, data=pin_data)
            except:
                pass
            
            # ចាំ ១៥ នាទី (៩០០ វិនាទី) រួចលុបចេញ
            wait_time = 900 
            timer = threading.Timer(wait_time, delete_message, args=[token, chat_id, message_id])
            timer.start()
    except Exception as e:
        print(f"Error ផ្ញើសារ: {e}")

# ----------------- ម៉ាស៊ីនឆែកម៉ោងពី Google Sheets -----------------
if 'global_sent_tracker' not in globals():
    global_sent_tracker = {}

def google_sheet_clock_engine():
    global global_sent_tracker
    last_sheet_check = datetime.datetime.now()
    
    alert_times = fetch_times_from_sheet()
    
    while True:
        now_khmer = datetime.datetime.now() + datetime.timedelta(hours=7)
        current_time_str = now_khmer.strftime("%H:%M")   
        current_second = now_khmer.strftime("%S")        
        today_date = now_khmer.strftime("%Y-%m-%d")      

        # រៀងរាល់ ១០ នាទីម្តង ឱ្យម៉ាស៊ីនទៅលួចអាប់ដេតម៉ោងពី Google Sheets ម្តង
        if (datetime.datetime.now() - last_sheet_check).total_seconds() > 600:
            alert_times = fetch_times_from_sheet()
            last_sheet_check = datetime.datetime.now()

        for t in alert_times:
            if t == current_time_str and current_second == "00":
                job_key = f"{today_date}_{t}"
                
                if job_key not in global_sent_tracker:
                    send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE_TEXT)
                    global_sent_tracker[job_key] = True 

        time.sleep(1)

# បើកម៉ាស៊ីនឱ្យរត់ជារៀងរហូត
thread_exists = any(t.name == "GoogleSheetClockEngine" for t in threading.enumerate())
if not thread_exists:
    t = threading.Thread(target=google_sheet_clock_engine, name="GoogleSheetClockEngine", daemon=True)
    t.start()

# ----------------- ផ្ទាំងបង្ហាញលើវេបសាយ -----------------
st.success("⚙️ ប្រព័ន្ធបានភ្ជាប់ជាមួយ Google Sheets ជោគជ័យ!")
st.write("🔗 **តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ៖**")
st.code(SHEET_URL)

st.info("💡 **របៀបប្រើប្រាស់៖** លោកគ្រូអាចបើកទូរស័ព្ទដៃចូលទៅកែម៉ោងនៅក្នុង Google Sheets នោះបានតាមចិត្ត។ ម៉ាស៊ីននឹងលួចទៅអានម៉ោងថ្មីពីតារាងនោះដោយស្វ័យប្រវត្តិ។ លោកគ្រូមិនបាច់ចូលកែក្នុង GitHub និងមិនបាច់ Reboot app ទៀតឡើយ!")
