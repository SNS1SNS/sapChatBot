import requests
import json
from
sap_url = "https://ao-qarmet-q-1-techwins-rj5nyvl2-dev-sap-btp-tech-suppor4df0f4cd.cfapps.eu10-005.hana.ondemand.com/odata/v4/bot"

# Получение всех вопросов
def get_all_questions():
    url = f"{sap_url}/Questions"
    response = requests.get(url)
    return response.json()


# Получение всех ответов
def get_all_answers():
    url = f"{sap_url}/Answers"
    response = requests.get(url)
    return response.json()


# Обновление вектора вопроса
def update_question_vector(question_id, question_vector):
    url = f"{sap_url}/Questions({question_id})"
    payload = {"questionVector": json.dumps(question_vector)}
    headers = {"Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, data=json.dumps(payload))
    return response.status_code, response.json() if response.status_code != 204 else None


# Сравнение нового вопроса с существующими по косинусному сходству
def find_similar_questions(new_question_text, threshold=0.7):
    # Проверка на минимальное количество слов и минимальную длину текста
    if len(new_question_text.split()) < 3 or len(new_question_text) < 10:
        return {"answer": "Задайте более детальный вопрос"}

    new_question_vector = get_embedding(new_question_text)
    if new_question_vector is None:
        return {"error": "Ошибка: не удалось создать вектор для нового вопроса."}

    questions_data = get_all_questions()
    answers_data = get_all_answers()
    questions = questions_data.get("value", [])
    answers = answers_data.get("value", [])

    if not questions:
        return {"error": "Ошибка: нет вопросов для сравнения."}

    answers_dict = {answer["ID"]: answer for answer in answers}

    max_similarity = -1
    best_match = None
    for question in questions:
        question_id = question.get("ID")
        question_text = question.get("question")
        question_vector = json.loads(question.get("questionVector"))
        answer_id = question.get("answer_ID")

        similarity = cosine_similarity_score(new_question_vector, question_vector)

        if similarity > max_similarity:
            max_similarity = similarity
            best_match = {
                "ID": question_id,
                "text": question_text,
                "similarity": similarity,
                "answer_id": answer_id
            }

    # Проверка на максимальное сходство ниже порога
    if max_similarity < 0.85:
        # Проверка на ключевые слова в тексте вопроса
        lower_text = new_question_text.lower()
        if any(word in lower_text for word in ["sap", "озм", "тнвэд", "озу", "afi", "ппм", "закупки", "сбыту", "pm", "hr", "закупки"]):
            return {"answer": "Для решения данной проблемы вы можете перейти по следующий ссылке и создать инцидент: <ссылка_на_SOP>"}
        # elif any(word in lower_text for word in ["сломался", "сломан","не работает"]):
        #     return {"answer": "<ссылка_на_Helpdesk>"}
        else:
            return {"answer": "Для решения данной проблемы вы можете перейти по следующий ссылке и создать инцидент: <ссылка_на_Helpdesk>"}
    if best_match:
        answer = answers_dict.get(best_match['answer_id'])
        if answer:
            return {
                "ID": best_match['ID'],
                "similarity": best_match['similarity'],
                "text": best_match['text'],
                "answer": answer['answer']
            }
        else:
            return {"error": "Ответ не найден."}
    else:
        return {"answer": "Нет вопросов, похожих на новый вопрос с заданным порогом."}

