import streamlit as st
import time
import threading
import requests
import datetime
import urllib.request

# ----------------- កំណត់រចនាសម្ព័ន្ធទំព័រ -----------------
st.set_page_config(page_title="ប្រព័ន្ធរំលឹកវត្តមាន (Auto Reminder)", layout="centered")

st.title("⏰ ប្រព័ន្ធរំលឹកវត្តមានស្វ័យប្រវត្តិ")
st.write("🌍 ស្ថានភាពប្រព័ន្ធ៖ **កំពុងដំណើរការ ២៤ម៉ោង តាមរយៈ Google Sheets**")

# --- កំណត់ព័ត៌មាន Telegram ដើម ---
BOT_TOKEN = "8037667434:AAGDSRYkpzYK96Jxmh613y4YI9KOYDwgUQU"
CHAT_ID = "-4192247028"  # លេខគ្រុបរបស់លោកគ្រូ
MESSAGE_TEXT = "សួស្តីលោកគ្រូអ្នកគ្រូ! ⏰ សូមកុំភ្លេចចូលទៅចុះវត្តមានសិស្សសម្រាប់ម៉ោងនេះផងណា៎! សូមអរគុណ។"

# 🔗 តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ (កែសម្រួលទម្រង់ទាញទិន្នន័យត្រឹមត្រូវជានិច្ច)
RAW_URL = "https://docs.google.com/spreadsheets/d/import streamlit as st
import time
import threading
import requests
import datetime
import urllib.request

# ----------------- កំណត់រចនាសម្ព័ន្ធទំព័រ -----------------
st.set_page_config(page_title="ប្រព័ន្ធរំលឹកវត្តមាន (Auto Reminder)", layout="centered")

st.title("⏰ ប្រព័ន្ធរំលឹកវត្តមានស្វ័យប្រវត្តិ")
st.write("🌍 ស្ថានភាពប្រព័ន្ធ៖ **កំពុងដំណើរការ ២៤ម៉ោង តាមរយៈ Google Sheets**")

# --- កំណត់ព័ត៌មាន Telegram ដើម ---
BOT_TOKEN = "8037667434:AAGDSRYkpzYK96Jxmh613y4YI9KOYDwgUQU"
CHAT_ID = "-4192247028"  # លេខគ្រុបរបស់លោកគ្រូ
MESSAGE_TEXT = "សួស្តីលោកគ្រូអ្នកគ្រូ! ⏰ សូមកុំភ្លេចចូលទៅចុះវត្តមានសិស្សសម្រាប់ម៉ោងនេះផងណា៎! សូមអរគុណ។"

# 🔗 តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ (កែសម្រួលទម្រង់ទាញទិន្នន័យត្រឹមត្រូវជានិច្ច)
RAW_URL = "https://docs.google.com/spreadsheets/d/import streamlit as st
import time
import threading
import requests
import datetime
import urllib.request

# ----------------- កំណត់រចនាសម្ព័ន្ធទំព័រ -----------------
st.set_page_config(page_title="ប្រព័ន្ធរំលឹកវត្តមាន (Auto Reminder)", layout="centered")

st.title("⏰ ប្រព័ន្ធរំលឹកវត្តមានស្វ័យប្រវត្តិ")
st.write("🌍 ស្ថានភាពប្រព័ន្ធ៖ **កំពុងដំណើរការ ២៤ម៉ោង តាមរយៈ Google Sheets**")

# --- កំណត់ព័ត៌មាន Telegram ដើម ---
BOT_TOKEN = "8037667434:AAGDSRYkpzYK96Jxmh613y4YI9KOYDwgUQU"
CHAT_ID = "-4192247028"  # លេខគ្រុបរបស់លោកគ្រូ
MESSAGE_TEXT = "សួស្តីលោកគ្រូអ្នកគ្រូ! ⏰ សូមកុំភ្លេចចូលទៅចុះវត្តមានសិស្សសម្រាប់ម៉ោងនេះផងណា៎! សូមអរគុណ។"

# 🔗 តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ (កែសម្រួលទម្រង់ទាញទិន្នន័យត្រឹមត្រូវជានិច្ច)
RAW_URL = "https://docs.google.com/spreadsheets/d/19V8JHsneOV_gtuj5faqxQDbpCvblKdVues5fTT57jnw"
SHEET_URL = RAW_URL.split("/edit")[0] + "/export?format=csv"

# ----------------- អនុគមន៍ទាញទិន្នន័យម៉ោងពី Google Sheets (ជំនាន់ថ្មី មិនប្រើ pandas) -----------------
def fetch_times_from_sheet():
    try:
        # ទាញយកទិន្នន័យ CSV ផ្ទាល់ពី Google Sheets តាមអ៊ីនធឺណិត
        response = urllib.request.urlopen(SHEET_URL)
        csv_data = response.read().decode('utf-8')
        
        # បំបែកទិន្នន័យជួរឈរនីមួយៗ
        lines = csv_data.strip().split('\n')
        times_list = []
        for line in lines:
            if line:
                # យកតែទិន្នន័យក្នុងប្រអប់ទី១ (ជួរឈរ A)
                cell_value = line.split(',')[0].replace('"', '').strip()
                times_list.append(cell_value)
        
        # សម្អាត និងរៀបចំទម្រង់ម៉ោងឱ្យស្អាត (ថែមលេខសូន្យពីមុខបើខ្វះ)
        clean_times = []
        for t in times_list:
            if ":" in t:
                parts = t.split(":")
                h = parts[0].strip()
                m = parts[1].strip()[:2]
                if len(h) == 1:
                    h = "0" + h
                clean_times.append(f"{h}:{m}")
        return clean_times
    except Exception as e:
        print(f"មិនអាចអាន Google Sheets បានទេ: {e}")
        # ប្រព័ន្ធការពារ៖ បើអ៊ីនធឺណិតគាំង ឬអានសន្លឹកបៀរមិនដាច់ ឱ្យប្រើម៉ោងដើមនេះបណ្តោះអាសន្នសិន
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
            
            # ចាំ ១៥ នាទី (៩០០ វិនាទី) រួចលុបចេញទាំងផ្ទាំង Pin
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
    
    # ទាញយកម៉ោងពី Sheet ពេលបើកប្រព័ន្ធលើកដំបូង
    alert_times = fetch_times_from_sheet()
    
    while True:
        # គណនាមងនៅកម្ពុជា (ម៉ោង Server បរទេស + ៧ ម៉ោង)
        now_khmer = datetime.datetime.now() + datetime.timedelta(hours=7)
        current_time_str = now_khmer.strftime("%H:%M")   
        current_second = now_khmer.strftime("%S")        
        today_date = now_khmer.strftime("%Y-%m-%d")      

        # រៀងរាល់ ៥ នាទីម្តង (៣០០ វិនាទី) ឱ្យម៉ាស៊ីនទៅលួចអាប់ដេតម៉ោងពី Google Sheets ឡើងវិញ
        if (datetime.datetime.now() - last_sheet_check).total_seconds() > 300:
            alert_times = fetch_times_from_sheet()
            last_sheet_check = datetime.datetime.now()

        # ដើរពិនិត្យម៉ោងជាក់ស្តែង
        for t in alert_times:
            if t == current_time_str and current_second == "00":
                job_key = f"{today_date}_{t}"
                
                if job_key not in global_sent_tracker:
                    send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE_TEXT)
                    global_sent_tracker[job_key] = True 

        time.sleep(1)

# បើកម៉ាស៊ីនឱ្យរត់ពីក្រោយខ្នងជារៀងរហូត
thread_exists = any(t.name == "GoogleSheetClockEngine" for t in threading.enumerate())
if not thread_exists:
    t = threading.Thread(target=google_sheet_clock_engine, name="GoogleSheetClockEngine", daemon=True)
    t.start()

# ----------------- ផ្ទាំងបង្ហាញលើវេបសាយ -----------------
st.success("⚙️ ប្រព័ន្ធដំណើរការជាមួយស្ថាបត្យកម្មល្បឿនលឿន (គាំទ្រ Google Sheets) ជោគជ័យ!")
st.write("🔗 **តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ៖**")
st.code(RAW_URL)

try:
    current_active_times = fetch_times_from_sheet()
    st.subheader("⏱️ ម៉ោងដែលប្រព័ន្ធកំពុងយាមរក្សានៅកម្ពុជា (ទាញចេញពី Sheet)៖")
    cols = st.columns(len(current_active_times))
    for i, t in enumerate(current_active_times):
        with cols[i]:
            st.metric(label=f"ម៉ោងទី {i+1}", value=t)
except:
    st.warning("កំពុងរង់ចាំទាញយកទិន្នន័យម៉ោងពីតារាងអនឡាញ...")

st.info("💡 **របៀបប្រើប្រាស់៖** លោកគ្រូគ្រាន់តែកែម៉ោងក្នុង Google Sheets តាមទូរស័ព្ទដៃជាការស្រេច (វាយក្នុងជួរឈរ A ផ្ដេកចុះក្រោម)។ រៀងរាល់ ៥ នាទីម្តង ប្រព័ន្ធនឹងទៅបឺតយកម៉ោងថ្មីមកយាមដោយស្វ័យប្រវត្តិតែម្ដង ដោយមិនបាច់ចុចប៊ូតុងរក្សាទុក ឬ Reboot កម្មវិធីទៀតឡើយ!")"
SHEET_URL = RAW_URL.split("/edit")[0] + "/export?format=csv"

# ----------------- អនុគមន៍ទាញទិន្នន័យម៉ោងពី Google Sheets (ជំនាន់ថ្មី មិនប្រើ pandas) -----------------
def fetch_times_from_sheet():
    try:
        # ទាញយកទិន្នន័យ CSV ផ្ទាល់ពី Google Sheets តាមអ៊ីនធឺណិត
        response = urllib.request.urlopen(SHEET_URL)
        csv_data = response.read().decode('utf-8')
        
        # បំបែកទិន្នន័យជួរឈរនីមួយៗ
        lines = csv_data.strip().split('\n')
        times_list = []
        for line in lines:
            if line:
                # យកតែទិន្នន័យក្នុងប្រអប់ទី១ (ជួរឈរ A)
                cell_value = line.split(',')[0].replace('"', '').strip()
                times_list.append(cell_value)
        
        # សម្អាត និងរៀបចំទម្រង់ម៉ោងឱ្យស្អាត (ថែមលេខសូន្យពីមុខបើខ្វះ)
        clean_times = []
        for t in times_list:
            if ":" in t:
                parts = t.split(":")
                h = parts[0].strip()
                m = parts[1].strip()[:2]
                if len(h) == 1:
                    h = "0" + h
                clean_times.append(f"{h}:{m}")
        return clean_times
    except Exception as e:
        print(f"មិនអាចអាន Google Sheets បានទេ: {e}")
        # ប្រព័ន្ធការពារ៖ បើអ៊ីនធឺណិតគាំង ឬអានសន្លឹកបៀរមិនដាច់ ឱ្យប្រើម៉ោងដើមនេះបណ្តោះអាសន្នសិន
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
            
            # ចាំ ១៥ នាទី (៩០០ វិនាទី) រួចលុបចេញទាំងផ្ទាំង Pin
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
    
    # ទាញយកម៉ោងពី Sheet ពេលបើកប្រព័ន្ធលើកដំបូង
    alert_times = fetch_times_from_sheet()
    
    while True:
        # គណនាមងនៅកម្ពុជា (ម៉ោង Server បរទេស + ៧ ម៉ោង)
        now_khmer = datetime.datetime.now() + datetime.timedelta(hours=7)
        current_time_str = now_khmer.strftime("%H:%M")   
        current_second = now_khmer.strftime("%S")        
        today_date = now_khmer.strftime("%Y-%m-%d")      

        # រៀងរាល់ ៥ នាទីម្តង (៣០០ វិនាទី) ឱ្យម៉ាស៊ីនទៅលួចអាប់ដេតម៉ោងពី Google Sheets ឡើងវិញ
        if (datetime.datetime.now() - last_sheet_check).total_seconds() > 300:
            alert_times = fetch_times_from_sheet()
            last_sheet_check = datetime.datetime.now()

        # ដើរពិនិត្យម៉ោងជាក់ស្តែង
        for t in alert_times:
            if t == current_time_str and current_second == "00":
                job_key = f"{today_date}_{t}"
                
                if job_key not in global_sent_tracker:
                    send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE_TEXT)
                    global_sent_tracker[job_key] = True 

        time.sleep(1)

# បើកម៉ាស៊ីនឱ្យរត់ពីក្រោយខ្នងជារៀងរហូត
thread_exists = any(t.name == "GoogleSheetClockEngine" for t in threading.enumerate())
if not thread_exists:
    t = threading.Thread(target=google_sheet_clock_engine, name="GoogleSheetClockEngine", daemon=True)
    t.start()

# ----------------- ផ្ទាំងបង្ហាញលើវេបសាយ -----------------
st.success("⚙️ ប្រព័ន្ធដំណើរការជាមួយស្ថាបត្យកម្មល្បឿនលឿន (គាំទ្រ Google Sheets) ជោគជ័យ!")
st.write("🔗 **តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ៖**")
st.code(RAW_URL)

try:
    current_active_times = fetch_times_from_sheet()
    st.subheader("⏱️ ម៉ោងដែលប្រព័ន្ធកំពុងយាមរក្សានៅកម្ពុជា (ទាញចេញពី Sheet)៖")
    cols = st.columns(len(current_active_times))
    for i, t in enumerate(current_active_times):
        with cols[i]:
            st.metric(label=f"ម៉ោងទី {i+1}", value=t)
except:
    st.warning("កំពុងរង់ចាំទាញយកទិន្នន័យម៉ោងពីតារាងអនឡាញ...")

st.info("💡 **របៀបប្រើប្រាស់៖** លោកគ្រូគ្រាន់តែកែម៉ោងក្នុង Google Sheets តាមទូរស័ព្ទដៃជាការស្រេច (វាយក្នុងជួរឈរ A ផ្ដេកចុះក្រោម)។ រៀងរាល់ ៥ នាទីម្តង ប្រព័ន្ធនឹងទៅបឺតយកម៉ោងថ្មីមកយាមដោយស្វ័យប្រវត្តិតែម្ដង ដោយមិនបាច់ចុចប៊ូតុងរក្សាទុក ឬ Reboot កម្មវិធីទៀតឡើយ!")"
SHEET_URL = RAW_URL.split("/edit")[0] + "/export?format=csv"

# ----------------- អនុគមន៍ទាញទិន្នន័យម៉ោងពី Google Sheets (ជំនាន់ថ្មី មិនប្រើ pandas) -----------------
def fetch_times_from_sheet():
    try:
        # ទាញយកទិន្នន័យ CSV ផ្ទាល់ពី Google Sheets តាមអ៊ីនធឺណិត
        response = urllib.request.urlopen(SHEET_URL)
        csv_data = response.read().decode('utf-8')
        
        # បំបែកទិន្នន័យជួរឈរនីមួយៗ
        lines = csv_data.strip().split('\n')
        times_list = []
        for line in lines:
            if line:
                # យកតែទិន្នន័យក្នុងប្រអប់ទី១ (ជួរឈរ A)
                cell_value = line.split(',')[0].replace('"', '').strip()
                times_list.append(cell_value)
        
        # សម្អាត និងរៀបចំទម្រង់ម៉ោងឱ្យស្អាត (ថែមលេខសូន្យពីមុខបើខ្វះ)
        clean_times = []
        for t in times_list:
            if ":" in t:
                parts = t.split(":")
                h = parts[0].strip()
                m = parts[1].strip()[:2]
                if len(h) == 1:
                    h = "0" + h
                clean_times.append(f"{h}:{m}")
        return clean_times
    except Exception as e:
        print(f"មិនអាចអាន Google Sheets បានទេ: {e}")
        # ប្រព័ន្ធការពារ៖ បើអ៊ីនធឺណិតគាំង ឬអានសន្លឹកបៀរមិនដាច់ ឱ្យប្រើម៉ោងដើមនេះបណ្តោះអាសន្នសិន
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
            
            # ចាំ ១៥ នាទី (៩០០ វិនាទី) រួចលុបចេញទាំងផ្ទាំង Pin
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
    
    # ទាញយកម៉ោងពី Sheet ពេលបើកប្រព័ន្ធលើកដំបូង
    alert_times = fetch_times_from_sheet()
    
    while True:
        # គណនាមងនៅកម្ពុជា (ម៉ោង Server បរទេស + ៧ ម៉ោង)
        now_khmer = datetime.datetime.now() + datetime.timedelta(hours=7)
        current_time_str = now_khmer.strftime("%H:%M")   
        current_second = now_khmer.strftime("%S")        
        today_date = now_khmer.strftime("%Y-%m-%d")      

        # រៀងរាល់ ៥ នាទីម្តង (៣០០ វិនាទី) ឱ្យម៉ាស៊ីនទៅលួចអាប់ដេតម៉ោងពី Google Sheets ឡើងវិញ
        if (datetime.datetime.now() - last_sheet_check).total_seconds() > 300:
            alert_times = fetch_times_from_sheet()
            last_sheet_check = datetime.datetime.now()

        # ដើរពិនិត្យម៉ោងជាក់ស្តែង
        for t in alert_times:
            if t == current_time_str and current_second == "00":
                job_key = f"{today_date}_{t}"
                
                if job_key not in global_sent_tracker:
                    send_telegram_message(BOT_TOKEN, CHAT_ID, MESSAGE_TEXT)
                    global_sent_tracker[job_key] = True 

        time.sleep(1)

# បើកម៉ាស៊ីនឱ្យរត់ពីក្រោយខ្នងជារៀងរហូត
thread_exists = any(t.name == "GoogleSheetClockEngine" for t in threading.enumerate())
if not thread_exists:
    t = threading.Thread(target=google_sheet_clock_engine, name="GoogleSheetClockEngine", daemon=True)
    t.start()

# ----------------- ផ្ទាំងបង្ហាញលើវេបសាយ -----------------
st.success("⚙️ ប្រព័ន្ធដំណើរការជាមួយស្ថាបត្យកម្មល្បឿនលឿន (គាំទ្រ Google Sheets) ជោគជ័យ!")
st.write("🔗 **តំណភ្ជាប់ Google Sheets របស់លោកគ្រូ៖**")
st.code(RAW_URL)

try:
    current_active_times = fetch_times_from_sheet()
    st.subheader("⏱️ ម៉ោងដែលប្រព័ន្ធកំពុងយាមរក្សានៅកម្ពុជា (ទាញចេញពី Sheet)៖")
    cols = st.columns(len(current_active_times))
    for i, t in enumerate(current_active_times):
        with cols[i]:
            st.metric(label=f"ម៉ោងទី {i+1}", value=t)
except:
    st.warning("កំពុងរង់ចាំទាញយកទិន្នន័យម៉ោងពីតារាងអនឡាញ...")

st.info("💡 **របៀបប្រើប្រាស់៖** លោកគ្រូគ្រាន់តែកែម៉ោងក្នុង Google Sheets តាមទូរស័ព្ទដៃជាការស្រេច (វាយក្នុងជួរឈរ A ផ្ដេកចុះក្រោម)។ រៀងរាល់ ៥ នាទីម្តង ប្រព័ន្ធនឹងទៅបឺតយកម៉ោងថ្មីមកយាមដោយស្វ័យប្រវត្តិតែម្ដង ដោយមិនបាច់ចុចប៊ូតុងរក្សាទុក ឬ Reboot កម្មវិធីទៀតឡើយ!")
