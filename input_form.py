from formulas import *
import mysql.connector
from flask import Flask, request


# Подключение к базе данных MySQL
connection = mysql.connector.connect(
    host='127.0.0.1',
    database='Nestro',
    user='root',
    password='ZXCursed18'
)

if connection.is_connected():
    print("Connection Successfully")

cursor = connection.cursor()

# Создание веб-приложения с использованием Flask
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получение данных из формы
        facility_name = request.form['facility_name']
        sources = request.form['sources']

        # Запись данных в базу данных
        cursor.execute("INSERT INTO facility (facility_name, sources) VALUES (%s, %s)", (facility_name, sources))
        connection.commit()

        print(facility_name, sources)

    # Отображение формы на вашем сайте
    return '''
        <form method="POST">
            <label for="facility_name">Название месторождения:</label>
            <input type="text" id="facility_name" name="facility_name" required><br><br>
            <label for="sources">Источники выбросов:</label>
            <input type="text" id="sources" name="sources" required><br><br>
            <input type="submit" value="Отправить">
        </form>
    '''


if __name__ == '__main__':
    app.run()