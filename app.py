from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# Импорт функций из модулей
from sap.model.embedding import get_embedding
from sap.algorithm.cosin import cosine_similarity_score
from sap.database.db import get_all_questions, get_all_answers, update_question_vector, get_question_by_id
from sap.database.db import find_similar_questions

app = Flask(__name__)
load_dotenv()  # Загружаем переменные окружения из .env

cf_port = os.getenv("PORT")
AICORE_AUTH_URL = os.getenv('AICORE_AUTH_URL')
AICORE_CLIENT_ID = os.getenv('AICORE_CLIENT_ID')
AICORE_CLIENT_SECRET = os.getenv('AICORE_CLIENT_SECRET')
DEPLOYMENT_ID = os.getenv('DEPLOYMENT_ID')

# Создаем конечные точки для вызова функций

@app.route('/get_embedding', methods=['POST'])
def get_text_embedding():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "Text field is required"}), 400

    embedding = get_embedding(text)  # Вызываем функцию из модуля embedding.py

    if embedding is None:
        return jsonify({"error": "Embedding generation failed"}), 500

    return jsonify({"embedding": embedding})


@app.route('/find_similar', methods=['POST'])
def find_similar():
    data = request.get_json()
    text = data.get('text')
    threshold = data.get('threshold', 0.7)

    if not text:
        return jsonify({"error": "Text field is required"}), 400

    result = find_similar_questions(text, threshold)  # Вызываем функцию, определенную ниже
    return jsonify(result)


@app.route('/update_all_vectors', methods=['POST'])
def update_all_vectors():
    response_data = get_all_questions()  # Получаем вопросы из модуля db.py
    if not response_data:
        return jsonify({"error": "No response data."}), 500

    questions = response_data.get("value", [])
    if not isinstance(questions, list):
        return jsonify({"error": "Expected list of questions in 'value'."}), 500

    for question in questions:
        question_id = question.get("ID")
        question_text = question.get("question")

        if not question_id or not question_text:
            continue

        question_vector = get_embedding(question_text)
        if question_vector is None:
            continue

        status_code, result = update_question_vector(question_id, question_vector)
        if status_code != 204:
            return jsonify({"error": f"Error updating question ID {question_id}"}), 500

    return jsonify({"answer": "All question vectors updated successfully."})


@app.route('/update_vector/<question_id>', methods=['POST'])
def update_vector_by_id(question_id):
    question_data = get_question_by_id(question_id)  # Вызываем функцию из db.py
    if not question_data:
        return jsonify({"error": "Question not found"}), 404

    question_text = question_data.get("question")
    if not question_text:
        return jsonify({"error": "Question text is missing"}), 400

    question_vector = get_embedding(question_text)
    if question_vector is None:
        return jsonify({"error": "Failed to generate embedding for the question"}), 500

    status_code, result = update_question_vector(question_id, question_vector)
    if status_code != 204:
        return jsonify({"error": f"Error updating question vector for ID {question_id}"}), 500

    return jsonify({"answer": "Question vector updated successfully."}), 200


if __name__ == '__main__':
    if cf_port is None:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=int(cf_port), debug=True)
