import streamlit as st
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

# إدخال بيانات جديدة
st.header("إدخال بيانات جديدة")
temperature = st.number_input("درجة الحرارة")
vibration = st.number_input("الاهتزاز")
pressure = st.number_input("الضغط")
current = st.number_input("التيار")
rpm = st.number_input("السرعة الدورانية")

if st.button("تنفيذ"):
    # تجميع جميع المدخلات في قائمة واحدة
    new_reading = [temperature, vibration, pressure, current, rpm]
    
    # إضافة البيانات إلى النظام
    prediction = monitor.add_data(new_reading)
    
    # عرض النتيجة
    if prediction is not None:
        st.success(f"احتمالية الفشل: {prediction:.2f}")
    else:
        st.warning("في انتظار المزيد من البيانات...")
