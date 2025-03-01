import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from monitoring import RealTimeMonitor
from data_processing import load_data, preprocess_data
from model_training import build_model, train_model

# تحميل البيانات ومعالجتها
data = load_data('historical_data.csv')
X, y, scaler, le = preprocess_data(data)

# بناء النموذج وتدريبه
model = build_model(X.shape[1:])
model, history = train_model(model, X, y)

# إنشاء نظام المراقبة
monitor = RealTimeMonitor(model, scaler)

# واجهة Streamlit
st.title("نظام مراقبة الحالة والتنبؤ بالفشل")

# عرض البيانات التاريخية
if st.checkbox("عرض البيانات التاريخية"):
    st.write(data)
    st.subheader("إحصاءات البيانات")
    st.write(data.describe())

    # رسم بياني تفاعلي
    st.subheader("رسم بياني للبيانات")
    column = st.selectbox("اختر العمود للرسم", data.columns)
    fig = px.line(data, y=column, title=f"تغير {column} مع الوقت")
    st.plotly_chart(fig)

# إدخال بيانات جديدة
st.header("إدخال بيانات جديدة")
temperature = st.number_input("درجة الحرارة")
vibration = st.number_input("الاهتزاز")
pressure = st.number_input("الضغط")
current = st.number_input("التيار")
rpm = st.number_input("السرعة الدورانية")

if st.button("تنبؤ بالفشل"):
    new_reading = [temperature, vibration, pressure, current, rpm]
    prediction = monitor.add_data(new_reading)
    if prediction is not None:
        st.success(f"احتمالية الفشل: {prediction[0][0]:.2f}")
    else:
        st.warning("في انتظار المزيد من البيانات...")

# تحميل بيانات جديدة
st.header("تحميل بيانات جديدة")
uploaded_file = st.file_uploader("اختر ملف CSV", type="csv")
if uploaded_file is not None:
    new_data = pd.read_csv(uploaded_file)
    st.write("البيانات الجديدة:")
    st.write(new_data)