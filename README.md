# AI Worker

Auto AI — це скрипт для автоматичної обробки AI-запитів за допомогою Ollama і моделі `deepseek-coder:6.7b`. Він отримує запити через API, генерує відповіді та відправляє їх назад.

## Вимоги

Перед запуском переконайтеся, що у вас встановлено:

- Python 3
- Віртуальне середовище (рекомендовано)
- `requests` бібліотека
- Ollama із завантаженою моделлю `deepseek-coder:6.7b`
- TTS для генерації голосових відповідей (необов’язково)

## Встановлення

1. **Клонуйте репозиторій**:
   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository
   ```

2. **Створіть та активуйте віртуальне середовище**:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Встановіть необхідні залежності**:
   ```bash
   pip install requests
   ```

4. **Запустіть Ollama та завантажте модель**:
   ```bash
   ollama pull deepseek-coder:6.7b
   ollama serve &
   ```

---

## Налаштування TTS (Text-to-Speech)

Якщо вам потрібно генерувати аудіо-відповіді, встановіть **TTS**.

### **1. Встановіть `TTS` та необхідні залежності**
```bash
pip install TTS
```
Якщо версія Python не підтримується, рекомендується використовувати Python **3.9-3.11**.

### **2. Перевірте, чи `TTS` встановлено правильно**
```bash
python -c "from TTS.api import TTS; print(TTS.list_models())"
```
Ця команда виведе список доступних моделей.

### **3. Завантажте та використовуйте модель для синтезу голосу**
```bash
tts --model_name tts_models/en/ljspeech/tacotron2-DDC --text "Hello, world!" --out_path output.wav
```
Це згенерує `output.wav` із синтезованою відповіддю.

### **4. Використання `TTS` у Python**
Ви можете інтегрувати TTS у свій код:
```python
from TTS.api import TTS

tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
tts.tts_to_file(text="Hello, this is an AI-generated voice.", file_path="output.wav")
```
Цей код згенерує голосовий файл `output.wav`.

---

## Запуск

1. **Переконайтеся, що процес не запущений**:
   ```bash
   ps aux | grep auto_ai.py
   ```
   Якщо процес працює, його можна завершити:
   ```bash
   kill -9 $(pgrep -f auto_ai.py)
   ```

2. **Запустіть скрипт у фоні**:
   ```bash
   nohup python3 auto_ai.py > log.txt 2>&1 &
   ```

---

## API Ендпоінти

### Отримання списку AI-запитів
- **GET** `https://webart.work/api/ai/get`
- Відповідь: Масив запитів

### Надсилання відповіді на запит
- **POST** `https://webart.work/api/ai/update`
- Очікує `{ _id, answer }`

---

## Основний цикл роботи

Скрипт працює в нескінченному циклі:
1. Отримує список нових запитів.
2. Використовує модель `deepseek-coder:6.7b` для генерації відповіді.
3. Якщо увімкнено **TTS**, конвертує текст у голос.
4. Відправляє відповідь через API.
5. Повторює процес кожні 10 секунд.

---

## Логи

Всі логи зберігаються у файлі `log.txt`. Для перегляду останніх записів використовуйте:
```bash
 tail -f log.txt
```

---

## Завершення роботи

Щоб зупинити роботу скрипта, використовуйте команду:
```bash
kill -9 $(pgrep -f auto_ai.py)
```

---

### 🔹 **Додатково**
- Якщо виникають помилки під час встановлення **TTS**, перевірте **версію Python** (`python --version`).  
- Деякі моделі можуть вимагати встановлення **PyTorch**, його можна додати:
  ```bash
  pip install torch torchvision torchaudio
  ```
- Якщо потрібно змінити голос, перегляньте список доступних моделей:
  ```bash
  python -c "from TTS.api import TTS; print(TTS.list_models())"
  ```
