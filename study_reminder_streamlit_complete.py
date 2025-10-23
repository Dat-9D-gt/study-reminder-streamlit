# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from gtts import gTTS
import datetime
import io
import os
import time

st.set_page_config(page_title="📚 Study Reminder + Pomodoro", layout="centered")
st.title("📚 Study Reminder App + ⏰ Pomodoro Timer")

DATA_FILE = "study_reminder_data.csv"

# --- Hàm đọc & ghi dữ liệu ---
def load_data(path):
    if not os.path.exists(path):
        return pd.DataFrame(columns=["Task", "Date", "Time"])
    encodings = ["utf-8-sig", "utf-8", "cp1252", "latin1"]
    for e in encodings:
        try:
            return pd.read_csv(path, encoding=e)
        except Exception:
            continue
    return pd.DataFrame(columns=["Task", "Date", "Time"])

def save_data(df, path):
    df.to_csv(path, index=False, encoding="utf-8-sig")

df = load_data(DATA_FILE)

# --- Form thêm nhiệm vụ ---
st.header("📝 Thêm nhiệm vụ học tập mới")
with st.form(key="task_form"):
    task = st.text_input("Tên nhiệm vụ:")
    date = st.date_input("Ngày:", value=datetime.date.today())
    time_input = st.time_input("Giờ:", value=datetime.datetime.now().time().replace(second=0, microsecond=0))
    submit = st.form_submit_button("Thêm nhiệm vụ")
    if submit:
        if not task.strip():
            st.error("Vui lòng nhập tên nhiệm vụ.")
        else:
            new_task = {"Task": task, "Date": str(date), "Time": str(time_input)}
            df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
            save_data(df, DATA_FILE)
            st.success(f"✅ Đã thêm nhiệm vụ: {task}")

# --- Danh sách nhiệm vụ ---
st.header("📋 Danh sách nhiệm vụ")
if df.empty:
    st.info("Chưa có nhiệm vụ nào.")
else:
    st.dataframe(df)

# --- Nghe nhắc nhở ---
st.header("🔊 Nghe nhắc nhở")
if not df.empty:
    selected = st.selectbox("Chọn nhiệm vụ để nghe:", df["Task"].tolist())
    if st.button("Nghe nhắc nhở"):
        try:
            tts = gTTS(text=f"Đừng quên nhiệm vụ: {selected}", lang="vi")
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"Lỗi khi phát âm thanh: {e}")

# --- Nhiệm vụ hôm nay ---
st.header("📅 Nhiệm vụ hôm nay")
today = str(datetime.date.today())
today_tasks = df[df["Date"] == today] if not df.empty else pd.DataFrame()
if today_tasks.empty:
    st.info("Hôm nay không có nhiệm vụ nào.")
else:
    st.table(today_tasks)

# --- ⏰ Pomodoro Timer ---
st.header("🍅 Pomodoro Timer")
st.write("Phương pháp Pomodoro giúp bạn tập trung học hiệu quả hơn!")

pomodoro_minutes = st.number_input("⏱️ Thời gian học (phút):", min_value=1, max_value=120, value=25)
break_minutes = st.number_input("💤 Thời gian nghỉ (phút):", min_value=1, max_value=30, value=5)

if st.button("▶️ Bắt đầu Pomodoro"):
    with st.empty():
        total_seconds = pomodoro_minutes * 60
        for sec in range(total_seconds, -1, -1):
            mins, secs = divmod(sec, 60)
            st.metric(label="⏳ Thời gian còn lại", value=f"{mins:02d}:{secs:02d}")
            time.sleep(1)
        st.success("🎉 Hết giờ học rồi, nghỉ ngơi một chút nhé!")

        try:
            tts = gTTS(text="Hết giờ học rồi, nghỉ ngơi một chút nhé!", lang="vi")
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
        except:
            st.warning("Không thể phát âm thanh thông báo kết thúc.")

# --- Footer ---
st.markdown("---")
st.markdown("**Ghi chú:** Dữ liệu lưu trong `study_reminder_data.csv`. Có thể xóa file để reset.")
st.markdown("---")
st.markdown("""
### 👨‍💻 Nhà sáng lập
**NHOM 1 9D**  
Ứng dụng được phát triển nhằm hỗ trợ học tập hiệu quả hơn qua hệ thống nhắc nhở và giọng nói tự động.
""")




