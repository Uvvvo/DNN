import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class DeepQLearning:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []  # ذاكرة للتجارب
        self.gamma = 0.95  # عامل الخصم
        self.epsilon = 1.0  # استكشاف
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
    
    def _build_model(self):
        """
        بناء نموذج التعلم العميق.
        """
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model
    
    def remember(self, state, action, reward, next_state, done):
        """
        تخزين التجربة في الذاكرة.
        """
        self.memory.append((state, action, reward, next_state, done))
    
    def choose_action(self, state):
        """
        اختيار إجراء باستخدام سياسة إبسيلون جشعة.
        """
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)  # إجراء عشوائي
        q_values = self.model.predict(state)
        return np.argmax(q_values[0])  # أفضل إجراء
    
    def replay(self, batch_size):
        """
        تدريب النموذج على مجموعة من التجارب.
        """
        minibatch = np.random.choice(len(self.memory), batch_size, replace=False)
        for idx in minibatch:
            state, action, reward, next_state, done = self.memory[idx]
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay