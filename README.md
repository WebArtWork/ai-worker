# AI Worker

**Auto AI** — це скрипт для автоматичної обробки AI-запитів за допомогою **Ollama** і моделі `deepseek-coder:6.7b`.  
Система отримує запити через API, генерує відповіді та відправляє їх назад.  
Додатково підтримується **TTS** для генерації голосових відповідей та **Whisper** для розпізнавання аудіо.

---

## **Вимоги**
Перед запуском переконайтеся, що у вас встановлено:

- Python **3.9 - 3.11**  
- Віртуальне середовище (**рекомендовано**)  
- Бібліотека `requests`  
- **Ollama** із завантаженою моделлю `deepseek-coder:6.7b`  
- **TTS** для генерації голосових відповідей (необов’язково)  
- **Whisper** для розпізнавання мови з аудіо (необов’язково)  

---

## **Встановлення**
### **1. Клонуйте репозиторій**
```bash
git clone https://github.com/WebArtWork/ai-worker.git
cd ai-worker
```

### **2. Створіть та активуйте віртуальне середовище**
```bash
python3.9 -m venv myenv
source myenv/bin/activate
```

### **3. Встановіть необхідні залежності**
```bash
pip install requests torch torchvision torchaudio
```

### **4. Запустіть Ollama та завантажте модель**
```bash
ollama pull deepseek-coder:6.7b
ollama serve &
```

---

## **Налаштування TTS (Text-to-Speech)**

Якщо вам потрібно **генерувати аудіо-відповіді**, встановіть **TTS**.

### **1. Встановіть `TTS` та необхідні залежності**
```bash
pip install TTS
```

### **2. Перевірте, чи `TTS` встановлено правильно**
```bash
python -c "from TTS.api import TTS; print(TTS.list_models())"
```

### **3. Генеруйте аудіо-файл**
```bash
tts --model_name tts_models/en/ljspeech/tacotron2-DDC --text "Hello, world!" --out_path output.wav
```

### **4. Використання `TTS` у Python**
```python
from TTS.api import TTS

tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
tts.tts_to_file(text="Hello, this is an AI-generated voice.", file_path="output.wav")
```

---

## **Налаштування Whisper (Speech-to-Text)**

**Whisper** — це AI-модель від OpenAI для розпізнавання мови з аудіофайлів.  
Ця секція допоможе налаштувати та використовувати її.

### **1. Встановіть Whisper**
```bash
pip install openai-whisper
```

### **2. Встановіть FFmpeg (необхідно для обробки аудіо)**
```bash
sudo apt update
sudo apt install ffmpeg
```

### **3. Завантажте модель**
Whisper підтримує кілька моделей (`tiny`, `base`, `small`, `medium`, `large`).  
Чим **більша модель**, тим **краща точність**, але **довше обробка**.

Наприклад, для **"medium"** моделі:
```bash
whisper --model medium
```

### **4. Розпізнайте текст з аудіофайлу**
```bash
whisper output.wav --model medium
```

### **5. Використання Whisper у Python**
```python
import whisper

model = whisper.load_model("medium")  # або "small", "large"
result = model.transcribe("output.wav")
print("Розпізнаний текст:", result["text"])
```

---

## **Запуск**

### **1. Переконайтеся, що процес не запущений**
```bash
ps aux | grep auto_ai.py
```
Якщо процес працює, його можна завершити:
```bash
kill -9 $(pgrep -f auto_ai.py)
```

### **2. Запустіть скрипт у фоні**
```bash
nohup python3 auto_ai.py > log.txt 2>&1 &
```

---

## **API Ендпоінти**
### **Отримання списку AI-запитів**
- **GET** `https://webart.work/api/ai/get`
- Відповідь: Масив запитів

### **Надсилання відповіді на запит**
- **POST** `https://webart.work/api/ai/update`
- Очікує `{ _id, answer }`

---

## **Основний цикл роботи**
Скрипт працює у нескінченному циклі:
1. Отримує список нових запитів.
2. Використовує модель **`deepseek-coder:6.7b`** для генерації відповіді.
3. Якщо увімкнено **TTS**, конвертує текст у голос.
4. Якщо увімкнено **Whisper**, розпізнає текст з аудіо.
5. Відправляє відповідь через API.
6. Повторює процес кожні **10 секунд**.

---

## **Логи**
Всі логи зберігаються у файлі `log.txt`.  
Переглянути останні записи можна так:
```bash
tail -f log.txt
```

---

## **Завершення роботи**
Щоб зупинити роботу скрипта:
```bash
kill -9 $(pgrep -f auto_ai.py)
```

---

### **🔹 Додатково**
- Якщо виникають помилки під час встановлення **TTS**, перевірте версію Python:
  ```bash
  python --version
  ```
- Деякі моделі можуть вимагати **PyTorch**, його можна встановити вручну:
  ```bash
  pip install torch torchvision torchaudio
  ```
- Щоб змінити голос у **TTS**, перегляньте список доступних моделей:
  ```bash
  python -c "from TTS.api import TTS; print(TTS.list_models())"
  ```
