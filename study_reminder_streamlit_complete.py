# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from gtts import gTTS
import os
import datetime

# --- Tiêu đề app ---
st.title("📚 Study Reminder App")

# --- Tải dữ liệu từ CSV nếu có ---
DATA_FILE = "study_reminder_data.csv"

if os.path.exists(DATA_FILE):
    # Thử đọc với UTF-8 hoặc các mã khác phòng lỗi font
    try:
        df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
    except:
        try:
            df = pd.read_csv(DATA_FILE, encoding="utf-8")
        except:
            df = pd.DataFrame(columns=["Task", "Date", "Time"])
else:
    df = pd.DataFrame(columns=["Task", "Date", "Time"])

# --- Thêm nhiệm vụ mới ---
st.header("Thêm nhiệm vụ học tập mới")
with st.form(key="task_form"):
    task = st.text_input("Tên nhiệm vụ:")
    date = st.date_input("Ngày:")
    time = st.time_input("Giờ:")
    submit = st.form_submit_button("Thêm nhiệm vụ")

    if submit:
        if not task.strip():
            st.warning("Vui lòng nhập tên nhiệm vụ.")
        else:
            new_task = {"Task": task, "Date": date, "Time": time}
            df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False, encoding="utf-8-sig")
            st.success(f"✅ Đã thêm nhiệm vụ: {task}")

# --- Hiển thị danh sách nhiệm vụ ---
st.header("📋 Danh sách nhiệm vụ")
if df.empty:
    st.info("Chưa có nhiệm vụ nào.")
else:
    st.dataframe(df)

# --- Chọn nhiệm vụ để nghe ---
st.header("🔊 Nghe nhắc nhở")
if not df.empty:
    selected_task = st.selectbox("Chọn nhiệm vụ để nghe:", df["Task"])
    if st.button("Nghe nhắc nhở"):
        try:
            tts = gTTS(text=selected_task, lang="vi")
            audio_file = "reminder.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3")
        except Exception as e:
            st.error(f"Lỗi khi phát âm thanh: {e}")

# --- Hiển thị nhiệm vụ hôm nay ---
st.header("📅 Nhiệm vụ hôm nay")
today = datetime.date.today()
today_tasks = df[df["Date"] == str(today)]
if today_tasks.empty:
    st.info("Hôm nay không có nhiệm vụ nào.")
else:
    st.table(today_tasks)

# --- Ghi chú ---
st.markdown("---")
st.markdown("**Ghi chú:** Dữ liệu được lưu trong file `study_reminder_data.csv`. "
            "Nếu muốn xóa toàn bộ, chỉ cần xóa file đó hoặc mở và chỉnh sửa.")
