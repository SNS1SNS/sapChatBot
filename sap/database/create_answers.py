import requests
import json

# URL вашего OData-сервиса
odata_url = "https://ao-qarmet-q-1-techwins-rj5nyvl2-dev-sap-btp-tech-suppor4df0f4cd.cfapps.eu10-005.hana.ondemand.com/odata/v4/bot/Answers"

# Данные для загрузки (извлекаем value из основного JSON)
data = [{
    "ID": "140422a7-d1e2-46b6-91f7-10d2873d09h0",
    "createdAt": "2024-11-12T00:00:00.000Z",
    "createdBy": "syrym_khamidullaev@qarmet.kz",
    "modifiedAt": "2024-11-12T07:31:41.401Z",
    "modifiedBy": "anonymous",
    "answer": "https://help.sap.com/docs/SAP_S4HANA_CLOUD/0f69f8fb28ac4bf48d2b57b9637e81fa/32afd67be8dc4e66890171e9924098f6.html?locale=ru-RU"
}
]

headers = {
    "Content-Type": "application/json",
}

for item in data:
    try:
        response = requests.post(odata_url, headers=headers, data=json.dumps(item))
        item_id = item.get("ID", "Без ID")
        if response.status_code == 201:
            print(f"Успешно добавлено: {item_id}")
        else:
            print(f"Ошибка при добавлении {item_id}: {response.status_code}, {response.text}")
    except Exception as e:
        item_id = item.get("ID", "Без ID")
        print(f"Ошибка при отправке запроса для {item_id}: {e}")
