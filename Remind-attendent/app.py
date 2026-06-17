import streamlit as st
import schedule
import time
import threading
import requests
import datetime

# ----------------- កំណត់រចនាសម្ព័ន្ធទំព័រ -----------------
st.set_page_config(page_title="ប្រព័ន្ធរំលឹកវត្តមាន (Auto Reminder)", layout="centered")

st.title("⏰ ប្រព័ន្ធរំលឹកវត្តមានស្វ័យប្រវត្តិ")
st.write("កម្មវិធីនេះនឹងលួចចាំមើលម៉ោងនៅពីក្រោយខ្នង និងផ្ញើសារចូល Telegram ដោយស្វ័យប្រវត្តិ។")

# ----------------- អនុគមន៍លុបសារ -----------------
def delete_message(token, chat_id, message_id):
    try:
        url = f"https://api.telegram.org/bot{token}/deleteMessage"
        data = {"chat_id": chat_id, "message_id": message_id}
        requests.post(url, data=data)
        print(f"[{datetime.datetime.now()}] បានលុបសារទី {message_id} វិញដោយជោគជ័យ!")
    except Exception as e:
        print(f"មានបញ្ហាក្នុងការលុបសារ: {e}")

# ----------------- អនុគមន៍ផ្ញើសារ (កែប្រែឲ្យចេះលុបវិញ) -----------------
def send_telegram_message(token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print(f"[{datetime.datetime.now()}] សារបានផ្ញើជោគជ័យ!")
            
            # ចាប់យកលេខ ID របស់សារដែលទើបតែផ្ញើចេញ
            res_data = response.json()
            message_id = res_data['result']['message_id']
            
            # កំណត់ម៉ោងរង់ចាំដើម្បីលុប (គិតជាវិនាទី)
            # លោកគ្រូអាចកែលេខ 60 នេះបាន (ឧទាហរណ៍៖ ៦០ = ១ នាទី, ៩០០ = ១៥ នាទី, ៣៦០០ = ១ ម៉ោង)
            wait_time = 900
            
            # បញ្ជាឲ្យកូនចៅម្នាក់ទៀតចាំរាប់ម៉ោង រួចលុបសារនោះចោល
            timer = threading.Timer(wait_time, delete_message, args=[token, chat_id, message_id])
            timer.start()
            
        else:
            print(f"[{datetime.datetime.now()}] បរាជ័យក្នុងការផ្ញើ: {response.text}")
    except Exception as e:
        print(f"មានបញ្ហា Error: {e}")

# ----------------- ប្រព័ន្ធចាំមើលម៉ោង (Background Task) -----------------
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1) # សម្រាក 1 វិនាទី សឹមឆែកម៉ោងម្តងទៀត

# បើកខួរក្បាលទី២ (Thread) ឲ្យចាំមើលម៉ោង តែបើកម្តងគត់កុំឲ្យជាន់គ្នា
if 'thread_started' not in st.session_state:
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    st.session_state.thread_started = True

# ----------------- ផ្ទាំងគ្រប់គ្រង (UI) -----------------
st.header("⚙️ កំណត់ព័ត៌មាន Telegram")

# លេខកូដ និង Chat ID ត្រូវបានចាក់សោរទុកជាមុន មិនបាច់វាយបញ្ចូលទៀតទេ
bot_token = st.text_input("Bot Token:", value="8037667434:AAGDSRYkpzYK96Jxmh613y4YI9KOYDwgUQU")
chat_id = st.text_input("Chat ID (លេខគ្រុប ឬ លេខបុគ្គល):", value="-1002706061510")
message_text = st.text_area("សារដែលត្រូវផ្ញើ:", "សួស្តីលោកគ្រូអ្នកគ្រូ! ⏰ សូមកុំភ្លេចចូលទៅចុះវត្តមានសិស្សសម្រាប់ម៉ោងនេះផងណា៎! សូមអរគុណ។")

st.header("⏱️ កំណត់ម៉ោងរំលឹក")
st.write("ម៉ោងខាងក្រោមនេះត្រូវបានដក ៧ ម៉ោងរួចរាល់ហើយ ដើម្បីឲ្យស៊ីគ្នាជាមួយម៉ោងនៅកម្ពុជា។")

# រៀបចំកន្លែងផ្ទុកម៉ោងដើម (ម៉ោងដក៧រួចរាល់៖ 06:50, 07:00, 07:15, 10:55)
if 'alert_times' not in st.session_state:
    st.session_state.alert_times = ["23:50", "00:00", "00:15", "03:55"]

# បង្ហាញប្រអប់ឲ្យកែម៉ោង
cols = st.columns(4)
new_times = []
for i in range(4):
    with cols[i]:
        t = st.text_input(f"ម៉ោងទី {i+1}", value=st.session_state.alert_times[i], key=f"time_{i}")
        new_times.append(t)

st.divider()

# ប៊ូតុងសម្រាប់រក្សាទុកការកំណត់
if st.button("▶️ រក្សាទុក និង ចាប់ផ្តើមឲ្យប្រព័ន្ធចាំម៉ោងរត់", use_container_width=True):
    if not bot_token or not chat_id or not message_text:
        st.error("សូមបំពេញ Bot Token, Chat ID និង សារឲ្យបានត្រឹមត្រូវសិន!")
    else:
        # រក្សាទុកម៉ោងថ្មី
        st.session_state.alert_times = new_times
        
        # លុបចោលការចាំម៉ោងចាស់ រួចបញ្ចូលម៉ោងថ្មី
        schedule.clear()
        for t in new_times:
            schedule.every().day.at(t).do(send_telegram_message, bot_token, chat_id, message_text)
            
        st.success(f"✅ ប្រព័ន្ធកំពុងដំណើរការ! វានឹងលួចផ្ញើសារជារៀងរាល់ថ្ងៃនៅម៉ោង៖ {', '.join(new_times)} ហើយវានឹងលុបសារខ្លួនឯងវិញដោយស្វ័យប្រវត្តិ។")
        st.balloons()
