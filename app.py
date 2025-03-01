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