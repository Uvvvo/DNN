import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_data(file_path):
    """
    تحميل البيانات من ملف CSV.
    """
    data = pd.read_csv(file_path)
    print("البيانات المحملة:")
    print(data.head())
    print("عدد الصفوف:", len(data))
    return data

def preprocess_data(data):
    """
    معالجة البيانات الأولية.
    """
    # تحويل التسميات
    le = LabelEncoder()
    data['failure_label'] = le.fit_transform(data['failure_label'])
    
    # تطبيع البيانات
    scaler = StandardScaler()
    features = data[['temperature', 'vibration', 'pressure', 'current', 'rpm']]
    scaled_features = scaler.fit_transform(features)
    
    # إنشاء تسلسل زمني
    sequence_length = 5
    X, y = create_sequences(scaled_features, data['failure_label'], sequence_length)
    
    print("X بعد إنشاء التسلسل الزمني:", X.shape)
    print("y بعد إنشاء التسلسل الزمني:", y.shape)
    
    return X, y, scaler, le

def create_sequences(features, labels, sequence_length):
    """
    إنشاء تسلسل زمني من البيانات.
    """
    X, y = [], []
    for i in range(len(features)-sequence_length):
        X.append(features[i:i+sequence_length])
        y.append(labels[i+sequence_length])
    return np.array(X), np.array(y)