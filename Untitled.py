#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.title("💈 Berber Randevu Sistemi")

CSV_FILE = "randevular.csv"

# Çalışma saatleri
start_time = datetime.strptime("10:00", "%H:%M").time()
end_time = datetime.strptime("18:00", "%H:%M").time()

# Slot oluşturucu
def generate_slots(selected_date):
    slots = []
    current = datetime.combine(selected_date, start_time)
    end = datetime.combine(selected_date, end_time)
    while current <= end - timedelta(minutes=15):
        slots.append(current.time())
        current += timedelta(minutes=15)
    return slots

# Çakışma kontrolü
def is_slot_available(new_start, new_end, existing):
    for _, row in existing.iterrows():
        existing_start = datetime.strptime(f"{row['date']} {row['time']}", "%Y-%m-%d %H:%M:%S")
        existing_end = existing_start + timedelta(minutes=int(row['duration']))
        if (new_start < existing_end) and (new_end > existing_start):
            return False
    return True

# CSV'den mevcut randevuları yükle
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["name", "date", "time", "duration"])

# Kullanıcı girişi
name = st.text_input("Adınız ve Soyadınız")
date = st.date_input("Randevu Tarihi", datetime.today())
duration = st.selectbox("Randevu Süresi", [15, 30, 45])
available_slots = []

# Uygun saatleri hesapla
for slot in generate_slots(date):
    new_start = datetime.combine(date, slot)
    new_end = new_start + timedelta(minutes=duration)
    if is_slot_available(new_start, new_end, df):
        available_slots.append(slot.strftime("%H:%M"))

selected_slot = st.selectbox("Uygun Saatler", available_slots)

# Randevu alma
if st.button("Randevu Al"):
    if name and selected_slot:
        new_row = {
            "name": name,
            "date": date.strftime("%Y-%m-%d"),
            "time": selected_slot + ":00",  # saniyeyi de eklemek için
            "duration": duration
        }
        # .append yerine pd.concat kullanıyoruz
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success(f"Randevunuz alındı: {date} günü saat {selected_slot}, süre: {duration} dk")
    else:
        st.warning("Lütfen adınızı ve saat seçimini yapın.")

# Randevuları göster
if not df.empty:
    st.subheader("Alınan Randevular:")
    st.dataframe(df)
else:
    st.write("Henüz herhangi bir randevu alınmamış.")


# In[ ]:




