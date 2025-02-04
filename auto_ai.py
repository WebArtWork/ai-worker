import requests
import json
import time

# URL API
GET_REQUESTS_URL = "https://webart.work/api/ai/get"
POST_ANSWER_URL = "https://webart.work/api/ai/update"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

def get_ai_requests():
    """Отримує список AI-запитів"""
    response = requests.get(GET_REQUESTS_URL)
    if response.status_code == 200:
        return response.json()
    return []

def send_to_ollama(question, request_type):
    """Генерує відповідь через deepseek-coder в Ollama"""
    prompt = question
    if request_type == "Review":
        prompt = f"Summarize the changes in max 72 characters:\n\n{question}"

    payload = {
        "model": "deepseek-coder:6.7b",
        "prompt": prompt,
        "stream": False,
        "max_tokens": 50  # Додано обмеження токенів
    }
    
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        answer = response.json().get("response", "").strip()
        return answer[:72]  # Обрізаємо відповідь до 72 символів
    return "Помилка генерації відповіді."

def send_answer(_id, answer):
    """Відправляє відповідь назад в API"""
    payload = {"_id": _id, "answer": answer}
    response = requests.post(POST_ANSWER_URL, json=payload)
    return response.status_code == 200

def main():
    """Основний цикл обробки запитів"""
    print("Отримуємо список запитів...")
    requests_list = get_ai_requests()

    if not requests_list:
        print("Немає нових запитів.")
        return

    for req in requests_list:
        _id = req["_id"]
        question = req["question"]
        request_type = req.get("type", "")

        print(f"Обробляємо запит: {_id} -> \"{question}\"")
        answer = send_to_ollama(question, request_type)
        print(f"Отримано відповідь: {answer}")

        if send_answer(_id, answer):
            print(f"✅ Відповідь успішно надіслано для {_id}")
        else:
            print(f"❌ Помилка надсилання відповіді для {_id}")

if __name__ == "__main__":
    while True:
        main()
        print("🔁 Очікуємо 5 хвилин перед наступним запуском...")
        time.sleep(300)  # Чекаємо 5 хвилин перед наступним запуском
