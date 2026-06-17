import streamlit as st
import time
import threading
import requests
import datetime

# ----------------- កំណត់រចនាសម្ព័ន្ធទំព័រ -----------------
st.set_page_config(page_title="ប្រព័ន្ធរំលឹកវត្តមាន (Auto Reminder)", layout="centered")

st.title("⏰ ប្រព័ន្ធរំលឹកវត្តមានស្វ័យប្រវត្តិ")
st.write("កម្មវិធីនេះនឹងលួចចាំមើលម៉ោងនៅពីក្រោយខ្នង និងផ្ញើសារចូល Telegram ម្ដងមួយៗតាមម៉ោងពិតប្រាកដ។")

# ----------------- អនុគមន៍លុបសារ (Unpin រួច Delete) -----------------
def delete_message(token, chat_id, message_id):
    try:
        # ១. ដោះខ្ទាស់ (Unpin)
        unpin_url = f"https://api.telegram.org/bot{token}/unpinChatMessage"
        requests.post(unpin_url, data={"chat_id": chat_id, "message_id": message_id})
        
        # ២. លុបសារ (Delete)
        del_url = f"https://api.telegram.org/bot{token}/deleteMessage"
        requests.post(del_url, data={"chat_id": chat_id, "message_id": message_id})
        print(f"[{datetime.datetime.now()}] បាន Unpin និងលុបសារទី {message_id} រួចរាល់!")
    except Exception as e:
        print(f"មានបញ្ហាក្នុងការលុបសារ: {e}")

# ----------------- អនុគមន៍ផ្ញើសារ (មានមុខងារ Pin) -----------------
def send_telegram_message(token, chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            print(f"[{datetime.datetime.now()}] សារបានផ្ញើជោគជ័យ!")
            res_data = response.json()
            message_id = res_data['result']['message_id']

            # ខ្ទាស់សារ (Pin Message)
            try:
                pin_url = f"https://api.telegram.org/bot{token}/pinChatMessage"
                pin_data = {"chat_id": chat_id, "message_id": message_id, "disable_notification": False}
                requests.post(pin_url, data=pin_data)
            except Exception as pin_err:
                print(f"មានបញ្ហាក្នុងការ Pin: {pin_err}")
            
            # ចាំ ១៥ នាទី (៩០០ វិនាទី) រួចលុបចេញវិញ
            wait_time = 900 
            timer = threading.Timer(wait_time, delete_message, args=[token, chat_id, message_id])
            timer.start()
    except Exception as e:
        print(f"Error: {e}")

# ----------------- ប្រព័ន្ធឆែកម៉ោងពិតប្រាកដ (Background Engine) -----------------
def clock_engine():
    # បង្កើតកន្លែងចំណាំសារដែលបានផ្ញើរួចក្នុងមួយថ្ងៃៗ ដើម្បីកុំឱ្យផ្ញើឌុប
    if 'sent_today' not in st.session_state:
        st.session_state.sent_today = {}

    while True:
        # គណនាម៉ោងបច្ចុប្បន្ននៅកម្ពុជា (ម៉ោង Server + ៧ ម៉ោង)
        now_khmer = datetime.datetime.now() + datetime.timedelta(hours=7)
        current_time_str = now_khmer.strftime("%H:%M")   # ទម្រង់ "10:15"
        current_second = now_khmer.strftime("%S")        # វិនាទី "00"
        today_date = now_khmer.strftime("%Y-%m-%d")      # ថ្ងៃខែឆ្នាំ

        # ឆែកមើលម៉ោងដែលលោកគ្រូបានកំណត់
        if 'active_alert_times' in st.session_state:
            for t in st.session_state.active_alert_times:
                t_clean = t.strip()
                if t_clean == current_time_str and current_second == "00":
                    
                    # បង្កើតសោរចំណាំ៖ ថ្ងៃនេះ + ម៉ោងនេះ (ឧទាហរណ៍៖ "2026-06-17_10:15")
                    job_key = f"{today_date}_{t_clean}"
                    
                    if job_key not in st.session_state.sent_today:
                        # បាញ់សារចេញភ្លាម ចំវិនាទីទី ០០ គត់នៃម៉ោងនោះ
                        send_telegram_message(
                            st.session_state.current_token, 
                            st.session_state.current_chat_id, 
                            st.session_state.current_msg_text
                        )
                        # កត់ចំណាំទុកថា ម៉ោងនេះផ្ញើរួចហើយ ហាមផ្ញើទៀត
                        st.session_state.sent_today[job_key] = True

        time.sleep(1) # សម្រាក ១ វិនាទី រួចដើរឆែកនាឡិកាបន្ត

# ចាប់ផ្តើមបើកម៉ាស៊ីនឆែកម៉ោង (Thread) តែមួយគត់ជានិច្ច
thread_exists = any(t.name == "KhmerClockEngine" for t in threading.enumerate())
if not thread_exists:
    t = threading.Thread(target=clock_engine, name="KhmerClockEngine", daemon=True)
    t.start()

# ----------------- ផ្ទាំងគ្រប់គ្រង (UI) -----------------
st.header("⚙️ កំណត់ព័ត៌មាន Telegram")

bot_token = st.text_input("Bot Token:", value="8037667434:AAGDSRYkpzYK96Jxmh613y4YI9KOYDwgUQU")
chat_id = st.text_input("Chat ID (លេខគ្រុប ឬ លេខបុគ្គល):", value="-4192247028")
message_text = st.text_area("សារដែលត្រូវផ្ញើ:", "សួស្តីលោកគ្រូអ្នកគ្រូ! ⏰ សូមកុំភ្លេចចូលទៅចុះវត្តមានសិស្សសម្រាប់ម៉ោងនេះផងណា៎! សូមអរគុណ។")

# រក្សាទុកតម្លៃ Token/Chat ID ចូលក្នុងប្រព័ន្ធចាំម៉ោង
st.session_state.current_token = bot_token
st.session_state.current_chat_id = chat_id
st.session_state.current_msg_text = message_text

st.header("⏱️ កំណត់ម៉ោងរំលឹក")
st.info("💡 ត្រឹមត្រូវតាមម៉ោងជាក់ស្ដែង៖ វាយបញ្ចូលម៉ោងកម្ពុជា។ ម៉ោងណាដែលហួសវានឹងមិនលោតឡើយ។")

if 'alert_times' not in st.session_state:
    st.session_state.alert_times = ["06:50", "07:00", "07:15", "10:55"]

cols = st.columns(4)
new_times = []
for i in range(4):
    with cols[i]:
        t = st.text_input(f"ម៉ោងទី {i+1}", value=st.session_state.alert_times[i], key=f"time_{i}")
        new_times.append(t)

st.divider()

# ប៊ូតុងរក្សាទុក
if st.button("▶️ រក្សាទុក និង ចាប់ផ្តើមឲ្យប្រព័ន្ធចាំម៉ោងរត់", use_container_width=True):
    if not bot_token or not chat_id or not message_text:
        st.error("សូមបំពេញព័ត៌មានឱ្យបានគ្រប់គ្រាន់សិន!")
    else:
        st.session_state.alert_times = new_times
        # បញ្ជូនបញ្ជីម៉ោងទៅឱ្យម៉ាស៊ីនចងចាំ
        st.session_state.active_alert_times = new_times
        
        st.success(f"✅ កំណត់កាលវិភាគជោគជ័យ! ប្រព័ន្ធនឹងរង់ចាំបាញ់សារម្ដងមួយៗចំៗនាទី៖ {', '.join(new_times)} (ម៉ោងកន្លងហួសត្រូវបានរំលងចោលជានិច្ច)។")
        st.balloons()
