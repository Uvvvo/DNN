import numpy as np
from utils import log_prediction, send_email

class RealTimeMonitor:
    def __init__(self, model, scaler, threshold=0.8):
        self.model = model
        self.scaler = scaler
        self.threshold = threshold
        self.data_buffer = []  # مخزن مؤقت للبيانات الجديدة
    
    def add_data(self, new_reading):
        """
        إضافة بيانات جديدة والتنبؤ بالفشل.
        """
        if new_reading is None or len(new_reading) != 5:
            print("تحذير: البيانات المدخلة غير صالحة أو غير مكتملة.")
            return None
        
        # إضافة القراءة الجديدة إلى المخزن المؤقت
        self.data_buffer.append(new_reading)
        print(f"طول البيانات في المخزن المؤقت: {len(self.data_buffer)}")
        
        # إذا كان هناك بيانات كافية (10 قراءات)
        if len(self.data_buffer) >= 10:
            # معالجة البيانات
            processed_data = self.scaler.transform(self.data_buffer[-10:])
            
            # التنبؤ بالفشل
            prediction = self.model.predict(processed_data)
            print(f"احتمالية الفشل: {prediction[-1][0]:.2f}")  # آخر تنبؤ
            
            # إرسال تنبيه إذا كانت احتمالية الفشل عالية
            if prediction[-1][0] > self.threshold:
                self.trigger_maintenance()
            return prediction[-1][0]  # إرجاع آخر تنبؤ
        else:
            print("في انتظار المزيد من البيانات...")
            return None
    
    def trigger_maintenance(self):
        """
        إرسال تنبيه للصيانة.
        """
        print("تنبيه: مطلوب صيانة عاجلة!")
        # هنا يمكنك إرسال إشعار إلى نظام الصيانة
