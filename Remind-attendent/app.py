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

# ----------------- អនុគមន៍ផ្ញើសារ (មានមុខងារ Pin និងលុបវិញ) -----------------
def send_telegram_message(token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print(f"[{datetime.datetime.now()}] សារបានផ្ញើជោគជ័យ!")
            
            res_data = response.json()
            message_id = res_data['result']['message_id']

            try:
                pin_url = f"https://api.telegram.org/bot{token}/pinChatMessage"
                pin_data = {
                    "chat_id": chat_id, 
                    "message_id": message_id, 
                    "disable_notification": False 
                }
                requests.post(pin_url, data=pin_data)
            except Exception as pin_err:
                print(f"មានបញ្ហាក្នុងការ Pin សារ: {pin_err}")
            
            # កំណត់ម៉ោងលុបសារ (តេស្តត្រឹម ៦០ វិនាទីសិន ដើម្បីងាយមើល)
            wait_time = 60 
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
        time.sleep(1)

if 'thread_started' not in st.session_state:
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    st.session_state.thread_started = True

# ----------------- ផ្ទាំងគ្រប់គ្រង (UI) -----------------
st.header("⚙️ កំណត់ព័ត៌មាន Telegram")

bot_token = st.text_input("Bot Token:", value="8037667434:AAGDSRYkpzYK96Jxmh613y4YI9KOYDwgUQU")
chat_id = st.text_input("Chat ID (លេខគ្រុប ឬ លេខបុគ្គល):", value="-1004192247028")
message_text = st.text_area("សារដែលត្រូវផ្ញើ:", "សួស្តីលោកគ្រូអ្នកគ្រូ! ⏰ សូមកុំភ្លេចចូលទៅចុះវត្តមានសិស្សសម្រាប់ម៉ោងនេះផងណា៎! សូមអរគុណ។")

# === ផ្នែកថ្មី៖ ប៊ូតុងតេស្តបាញ់សារភ្លាមៗ ===
st.divider()
st.subheader("🛠️ ផ្នែកសាកល្បងប្រព័ន្ធ (Test System)")
if st.button("🚀 សាកល្បងបាញ់សារចូលគ្រុបឥឡូវនេះ (Test Now)"):
    if not bot_token or not chat_id:
        st.error("សូមបំពេញ Token និង Chat ID សិន!")
    else:
        st.info("កំពុងបញ្ជូនសារទៅកាន់ Telegram...")
        send_telegram_message(bot_token, chat_id, "នេះគឺជាសារតេស្តសាកល្បងពីប្រព័ន្ធ! វានឹងលុបទៅវិញក្នុងរយៈពេល ៦០វិនាទី។")
        st.success("ការបញ្ជាបានបញ្ជូនរួចរាល់! សូមឆែកមើលក្នុងគ្រុប Telegram ឥឡូវនេះ។")
# =================================

st.header("⏱️ កំណត់ម៉ោងរំលឹក")
st.info("💡 ងាយស្រួលជាងមុន! លោកគ្រូគ្រាន់តែវាយបញ្ចូល **ម៉ោងនៅកម្ពុជា** ផ្ទាល់តែម្តង (ប្រព័ន្ធនឹងគណនាដក ៧ ម៉ោងឲ្យដោយស្វ័យប្រវត្តិ)។")

if 'alert_times' not in st.session_state:
    st.session_state.alert_times = ["06:50", "07:00", "07:15", "10:55"]

cols = st.columns(4)
new_times = []
for i in range(4):
    with cols[i]:
        t = st.text_input(f"ម៉ោងទី {i+1}", value=st.session_state.alert_times[i], key=f"time_{i}")
        new_times.append(t)

st.divider()

def khmer_to_utc(khmer_time_str):
    try:
        h, m = map(int, khmer_time_str.split(':'))
        h_utc = (h - 7) % 24
        return f"{h_utc:02d}:{m:02d}"
    except:
        return khmer_time_str

if st.button("▶️ រក្សាទុក និង ចាប់ផ្តើមឲ្យប្រព័ន្ធចាំម៉ោងរត់", use_container_width=True):
    if not bot_token or not chat_id or not message_text:
        st.error("សូមបំពេញ Bot Token, Chat ID និង សារឲ្យបានត្រឹមត្រូវសិន!")
    else:
        st.session_state.alert_times = new_times
        schedule.clear()
        
        for t in new_times:
            server_time = khmer_to_utc(t)
            schedule.every().day.at(server_time).do(send_telegram_message, bot_token, chat_id, message_text)
            
        st.success(f"✅ ប្រព័ន្ធកំពុងដំណើរការ! វានឹងលួចផ្ញើនិង Pin សារជារៀងរាល់ថ្ងៃនៅម៉ោងកម្ពុជា៖ {', '.join(new_times)}")
        st.balloons()
