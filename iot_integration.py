import paho.mqtt.client as mqtt
import json
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

# إعداد عميل MQTT
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("sensors/#")  # الاشتراك في جميع أجهزة الاستشعار

def on_message(client, userdata, msg):
    """
    معالجة البيانات الواردة من أجهزة IoT.
    """
    try:
        data = json.loads(msg.payload.decode())
        print(f"Received data from {msg.topic}: {data}")
        
        # إضافة البيانات إلى نظام المراقبة
        if 'temperature' in data and 'vibration' in data and 'pressure' in data and 'current' in data and 'rpm' in data:
            new_reading = [data['temperature'], data['vibration'], data['pressure'], data['current'], data['rpm']]
            prediction = monitor.add_data(new_reading)
            if prediction is not None and prediction[0][0] > 0.8:
                client.publish("actuators/maintenance", "ON")  # إرسال أمر صيانة
    except Exception as e:
        print(f"Error processing message: {e}")

# تعيين دوال الاستدعاء
client.on_connect = on_connect
client.on_message = on_message

# الاتصال بالخادم
client.connect("mqtt.eclipseprojects.io", 1883, 60)

# بدء الاستماع للرسائل
client.loop_start()