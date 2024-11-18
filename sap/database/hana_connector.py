from hana_ml import ConnectionContext
from hdbcli import dbapi
import json
try:
    cc= dbapi.connect(
        address='0a8c7c52-296a-46b5-b549-3f24059f5475.hna2.prod-eu10.hanacloud.ondemand.com',
        port='443',
        user='DBADMIN',
        password='Admin12345',
        )
except Exception as e:
    print(f"Connection failed: {e}")

cursor=cc.cursor()
cursor.execute("SELECT * FROM Answers")
tables = cursor.fetchall()

# Вывод названий таблиц
for table in tables:
    print(table[2])
result = cursor.fetchall()
for row in result:
    print(row)
