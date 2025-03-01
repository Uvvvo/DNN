# نظام مراقبة الحالة والتنبؤ بالفشل

## الوصف
هذا المشروع يستخدم التعلم العميق لمراقبة حالة المعدات والتنبؤ بالفشل، مع دعم لوحة تحكم تفاعلية، تعلم معزز، وتكامل مع IoT.

## المتطلبات
- Python 3.8+
- المكتبات المذكورة في requirements.txt

## التنفيذ
1. تثبيت المتطلبات:

   pip install -r requirements.txt
   
2. تشغيل لوحة التحكم

streamlit run dashboard.py

3. تشغيل نظام IoT (اختياري):

python iot_integration.py

## 
---

### 10. **ملف التشغيل الرئيسي (`app.py`)**:
```python
from dashboard import st
from reinforcement_learning import DeepQLearning
from iot_integration import client
import threading

# نظام التعلم المعزز
rl_agent = DeepQLearning(state_size=5, action_size=3)  # مثال: 5 حالات و 3 إجراءات

# دمج IoT مع لوحة التحكم
def iot_listener():
    while True:
        client.loop()

# بدء الاستماع لبيانات IoT في خيط منفصل
threading.Thread(target=iot_listener, daemon=True).start()

# تشغيل لوحة التحكم
if __name__ == "__main__":
    st.run()