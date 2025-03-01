import numpy as np
from utils import log_prediction, send_email

class RealTimeMonitor:
    def __init__(self, model, scaler, threshold=0.8):
        self.model = model
        self.scaler = scaler
        self.threshold = threshold
        self.data_buffer = []
    
    def add_data(self, new_reading):
        """
        إضافة بيانات جديدة والتنبؤ بالفشل.
        """
        self.data_buffer.append(new_reading)
        print(f"طول البيانات في المخزن المؤقت: {len(self.data_buffer)}")
        if len(self.data_buffer) >= 10:
            processed_data = self.scaler.transform([self.data_buffer[-10:]])
            prediction = self.model.predict(processed_data)
            log_prediction(prediction[0][0])  # تسجيل التنبؤ
            if prediction[0][0] > self.threshold:
                self.trigger_maintenance()
            return prediction
        else:
            print("لا يوجد بيانات كافية للتنبؤ.")
            return None
    
    def trigger_maintenance(self):
        """
        إرسال تنبيه للصيانة.
        """
        print("تنبيه: مطلوب صيانة عاجلة!")
        send_email("Maintenance Alert", "Immediate maintenance required!")