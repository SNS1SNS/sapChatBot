import requests
import json

# URL вашего OData-сервиса
odata_url = "https://ao-qarmet-q-1-techwins-rj5nyvl2-dev-sap-btp-tech-suppor4df0f4cd.cfapps.eu10-005.hana.ondemand.com/odata/v4/bot/Questions"

# Данные для загрузки (извлекаем value из основного JSON)
data = [
{
      "ID": "551941a7-8256-441d-a5ae-973eb63090af",
      "answer_ID": "2979c7fd-fbec-4dc8-8f6c-4e519a94688c",
      "createdAt": "2024-11-12T00:00:00.000Z",
      "createdBy": "syrym_khamidullaev@qarmet.kz",
      "modifiedAt": "2024-11-12T07:31:41.401Z",
      "modifiedBy": "anonymous",
      "question": "Как правильно настроить SAP HANA CLOUD?",
      "questionVector": "[0.0076359473, 0.014231782, ...]"
    }
]


headers = {
    "Content-Type": "application/json",
    # Укажите аутентификацию, если требуется
    # "Authorization": "Bearer <your_access_token>"
}

# Функция для загрузки каждого объекта в OData
for item in data:
    try:
        # Отправляем каждый элемент отдельно
        response = requests.post(odata_url, headers=headers, data=json.dumps(item))
        # Проверка кода ответа и вывод результата
        item_id = item.get("ID", "Без ID")  # Используем "Без ID", если ID не найден
        if response.status_code == 201:
            print(f"Успешно добавлено: {item_id}")
        else:
            print(f"Ошибка при добавлении {item_id}: {response.status_code}, {response.text}")
    except Exception as e:
        item_id = item.get("ID", "Без ID")
        print(f"Ошибка при отправке запроса для {item_id}: {e}")
