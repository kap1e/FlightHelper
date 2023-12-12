import sqlite3
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, \
    QMessageBox, QInputDialog, QDialog, QFormLayout, QDialogButtonBox, QTableWidget, QTableWidgetItem, QHeaderView

# ниже стиль и разметка
style = """

QWidget {
    background-color: #001F3F;
    color: #ffffff;
}


QLabel {
    font-size: 14px;
}


QLineEdit {
    font-size: 12px;
    color: #ffffff;  /* Устанавливаем белый цвет текста */
    background-color: #001F3F;  /* Темно-синий фон для полей ввода */
    border: 1px solid #ffffff;  /* Белая обводка */
}


QPushButton {
    font-size: 12px;
}


QPushButton#register_button {
    background-color: #FFA500;
    color: #ffffff;
    padding: 5px 10px;
    border: 2px solid #FFA500;
    border-radius: 3px;
}


QPushButton#register_button:hover {
    background-color: #FF8C00;
}


QPushButton#check_miles_button,
QPushButton#check_registrations_button,
QPushButton#flight_info_button {
    background-color: #FFA500;
    color: #ffffff;
    padding: 5px 10px;
    border: 2px solid #FFA500;
    border-radius: 3px;
}


QPushButton#check_miles_button:hover,
QPushButton#check_registrations_button:hover,
QPushButton#flight_info_button:hover {
    background-color: #FF8C00;
}


QPushButton#developer_info_button {
    background-color: #FFA500;
    color: #ffffff;
    padding: 5px 10px;
    border: 2px solid #FFA500;
    border-radius: 3px;
}


QPushButton#developer_info_button:hover {
    background-color: #FF8C00;
}


QDialog, QMessageBox {
    background-color: #001F3F;
    color: #ffffff;
}


QTableWidget {
    border: 1px solid #FFA500;
}


QTableWidget QHeaderView::section {
    background-color: #FFA500;
    color: #ffffff;
    padding: 5px;
    border: none;
}


QTableWidget QHeaderView::section:horizontal {
    border: 1px solid #FFA500;
}
"""

conn = sqlite3.connect('flight_helper.db')


# это короче только для нас, я не нашел бд в интернете, так что было бы славно инфу о рейсах в бд вписать ручками
class FlightInfoDialog(QDialog):

    def __init__(self, parent=None):

        super(FlightInfoDialog, self).__init__(parent)

        self.setWindowTitle("Добавить информацию о рейсе")
        self.setGeometry(200, 200, 400, 200)

        layout = QFormLayout(self)

        self.flight_number_input = QLineEdit(self)
        layout.addRow("Номер рейса:", self.flight_number_input)

        self.departure_time_input = QLineEdit(self)
        layout.addRow("Время вылета:", self.departure_time_input)

        self.arrival_time_input = QLineEdit(self)
        layout.addRow("Время прилета:", self.arrival_time_input)

        self.departure_city_input = QLineEdit(self)
        layout.addRow("Город вылета:", self.departure_city_input)

        self.arrival_city_input = QLineEdit(self)
        layout.addRow("Город прибытия:", self.arrival_city_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    def get_flight_info(self):
        # берет инфу из ввода
        flight_number = self.flight_number_input.text()
        departure_time = self.departure_time_input.text()
        arrival_time = self.arrival_time_input.text()
        departure_city = self.departure_city_input.text()
        arrival_city = self.arrival_city_input.text()
        return flight_number, departure_time, arrival_time, departure_city, arrival_city


# окошко показа регистраций
class RegistrationInfoDialog(QDialog):
    def __init__(self, user_id, parent=None):
        super(RegistrationInfoDialog, self).__init__(parent)

        self.setWindowTitle("Информация о регистрациях")
        self.setGeometry(200, 200, 400, 300)

        self.layout = QVBoxLayout(self)

        self.user_id_label = QLabel(f"Рейсы пользователя с ID {user_id}:", self)
        self.layout.addWidget(self.user_id_label)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_registration_info(user_id)

    # запрос к базе данных по информации о рейсах

    def load_registration_info(self, user_id):
        global conn
        try:
            conn = sqlite3.connect('flight_helper.db')
            cursor = conn.cursor()

            # запрос информации о регистрациях пользователя по его user_id
            cursor.execute('SELECT flight_number FROM users WHERE user_id = ?', (user_id,))
            registrations = cursor.fetchall()

            # отображение информации в QTableWidget
            self.table_widget.setColumnCount(1)
            self.table_widget.setRowCount(len(registrations))
            self.table_widget.setHorizontalHeaderLabels(["Номер рейса"])
            self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            for row, registration in enumerate(registrations):
                for col, value in enumerate(registration):
                    item = QTableWidgetItem(str(value))
                    self.table_widget.setItem(row, col, item)
        # может выдавать ошибку, приколы иногда бывают, выводит инфу об ошибке
        except Exception as e:
            print(f"Ошибка при получении информации о регистрациях: {e}")

        finally:
            if conn:
                conn.close()


# добавленее новых рейсов

class DeveloperInfoDialog(QDialog):

    def __init__(self, parent=None):
        super(DeveloperInfoDialog, self).__init__(parent)

        self.setWindowTitle("Добавить информацию о рейсе")
        self.setGeometry(200, 200, 400, 200)

        layout = QFormLayout(self)

        self.flight_number_input = QLineEdit(self)
        layout.addRow("Номер рейса:", self.flight_number_input)

        self.departure_time_input = QLineEdit(self)
        layout.addRow("Время вылета:", self.departure_time_input)

        self.arrival_time_input = QLineEdit(self)
        layout.addRow("Время прилета:", self.arrival_time_input)

        self.departure_city_input = QLineEdit(self)
        layout.addRow("Город вылета:", self.departure_city_input)

        self.arrival_city_input = QLineEdit(self)
        layout.addRow("Город прибытия:", self.arrival_city_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.add_flight_info)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)

    # запросы к бд

    def add_flight_info(self):

        global conn

        flight_number = self.flight_number_input.text()
        departure_time = self.departure_time_input.text()
        arrival_time = self.arrival_time_input.text()
        departure_city = self.departure_city_input.text()
        arrival_city = self.arrival_city_input.text()

        try:
            conn = sqlite3.connect('flight_info.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS flights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_number TEXT NOT NULL,
                    departure_time TEXT NOT NULL,
                    arrival_time TEXT NOT NULL,
                    departure_city TEXT NOT NULL,
                    arrival_city TEXT NOT NULL
                )
            ''')

            cursor.execute(
                'INSERT INTO flights (flight_number, departure_time, arrival_time, departure_city, arrival_city) '
                'VALUES (?, ?, ?, ?, ?)',
                (flight_number, departure_time, arrival_time, departure_city, arrival_city))
            conn.commit()

            QMessageBox.information(self, "Информация о рейсе",
                                    f"Информация о рейсе добавлена: {flight_number}, {departure_time}, {arrival_time},"
                                    f" {departure_city}, {arrival_city}")

        except Exception as e:
            print(f"Ошибка при добавлении информации о рейсе: {e}")
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при добавлении информации о рейсе.")

        finally:
            if conn:
                conn.close()


class FlightHelperApp(QMainWindow):
    # главное окно
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Flight Helper")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)

        # верхняя часть: поля ввода и кнопка регистрации на рейс
        self.left_layout = QVBoxLayout()

        self.flight_number_label = QLabel("Номер рейса:", self)
        self.left_layout.addWidget(self.flight_number_label)

        self.flight_number_input = QLineEdit(self)
        self.left_layout.addWidget(self.flight_number_input)

        self.user_id_label = QLabel("Введите свой ID:", self)
        self.left_layout.addWidget(self.user_id_label)

        self.user_id_input = QLineEdit(self)
        self.left_layout.addWidget(self.user_id_input)

        self.register_button = QPushButton("Зарегистрироваться на рейс", self)
        self.register_button.setObjectName("register_button")
        self.register_button.clicked.connect(self.register_user)
        self.left_layout.addWidget(self.register_button)

        self.central_layout.addLayout(self.left_layout)

        # нижняя часть: остальные кнопки и кнопка для разработчиков

        self.right_layout = QVBoxLayout()

        self.check_miles_button = QPushButton("Проверить мили", self)
        self.check_miles_button.setObjectName("check_miles_button")
        self.check_miles_button.clicked.connect(self.check_miles)
        self.right_layout.addWidget(self.check_miles_button)

        self.check_registrations_button = QPushButton("Проверить регистрации", self)
        self.check_registrations_button.setObjectName("check_registrations_button")
        self.check_registrations_button.clicked.connect(self.check_registrations)
        self.right_layout.addWidget(self.check_registrations_button)

        self.flight_info_button = QPushButton("Информация по рейсу", self)
        self.flight_info_button.setObjectName("flight_info_button")
        self.flight_info_button.clicked.connect(self.show_flight_info_dialog)
        self.right_layout.addWidget(self.flight_info_button)

        self.developer_info_button = QPushButton("dev", self)
        self.developer_info_button.setObjectName("developer_info_button")
        self.developer_info_button.clicked.connect(self.show_developer_info_dialog)
        self.developer_info_button.setFixedSize(120, 30)
        self.developer_info_button.setStyleSheet(
            "QPushButton#developer_info_button { background-color: #FFA500; color: #ffffff; border: 2px solid "
            "#FFA500; border-radius: 3px; } QPushButton#developer_info_button:hover { background-color: #FF8C00; }")
        self.right_layout.addWidget(self.developer_info_button, alignment=Qt.AlignBottom | Qt.AlignRight)

        self.central_layout.addLayout(self.right_layout)

        self.setCentralWidget(self.central_widget)

        # применяем стили
        self.setStyleSheet(style)

    def register_user(self):
        global conn
        flight_number = self.flight_number_input.text()
        user_id = self.user_id_input.text()

        try:
            conn = sqlite3.connect('flight_helper.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_number TEXT NOT NULL,
                    user_id TEXT NOT NULL
                )
            ''')

            # проверяем, существует ли запись о пользователе и рейсе
            cursor.execute('SELECT * FROM users WHERE user_id = ? AND flight_number = ?', (user_id, flight_number))
            existing_registration = cursor.fetchone()

            if existing_registration:
                QMessageBox.warning(self, "Повторная регистрация",
                                    f"Пользователь с ID {user_id} уже зарегистрирован на рейс {flight_number}.")
            else:
                # если записи нет, регистрируем пользователя на рейс
                cursor.execute('INSERT INTO users (flight_number, user_id) VALUES (?, ?)', (flight_number, user_id))
                conn.commit()

                # обновляем мили пользователя при каждой регистрации на рейс
                self.update_miles(user_id)

                QMessageBox.information(self, "Регистрация", f"Пользователь с ID {user_id} зарегистрирован на рейс с "
                                                             f"номером {flight_number}")

        except Exception as e:
            print(f"Ошибка при регистрации пользователя: {e}")
            QMessageBox.critical(self, "Ошибка", "Произошла ошибка при регистрации пользователя.")

        finally:
            if conn:
                conn.close()

    def check_registrations(self):
        user_id, ok_pressed = QInputDialog.getText(self, "Проверка регистраций", "Введите свой ID:")
        if ok_pressed:
            dialog = RegistrationInfoDialog(user_id, self)
            dialog.exec_()

    # вторичная функция для показа и отключение окна девелопера
    def show_developer_info_dialog(self):
        dialog = DeveloperInfoDialog(self)
        dialog.exec_()

    # функция вывода информации по рейсу
    def show_flight_info_dialog(self):
        global conn, conn
        flight_number, ok_pressed = QInputDialog.getText(self, "Информация о рейсе", "Введите номер рейса:")
        if ok_pressed:
            try:
                conn = sqlite3.connect('flight_info.db')
                cursor = conn.cursor()

                cursor.execute('SELECT * FROM flights WHERE flight_number = ?', (flight_number,))
                flight_info = cursor.fetchone()

                if flight_info:
                    info_text = f"Номер рейса: {flight_info[1]}\n" \
                                f"Время вылета: {flight_info[2]}\n" \
                                f"Время прилета: {flight_info[3]}\n" \
                                f"Город вылета: {flight_info[4]}\n" \
                                f"Город прибытия: {flight_info[5]}"
                    QMessageBox.information(self, "Информация о рейсе", info_text)
                else:
                    QMessageBox.warning(self, "Информация о рейсе", f"Рейс с номером {flight_number} не найден.")

            except Exception as e:
                print(f"Ошибка при получении информации о рейсе: {e}")

            finally:
                if conn:
                    conn.close()

    # проеврка лояльности еслм есть в базе
    def check_miles(self):
        global conn, conn
        user_id, ok_pressed = QInputDialog.getText(self, "Проверка миль", "Введите свой ID:")
        if ok_pressed:
            try:
                conn = sqlite3.connect('loyalty_program.db')
                cursor = conn.cursor()

                # запрос информации о милях пользователя по его user_id
                cursor.execute('SELECT miles_quantity FROM loyalty_program WHERE user_id = ?', (user_id,))
                miles_info = cursor.fetchone()

                if miles_info:
                    QMessageBox.information(self, "Информация о милях", f"У вас {miles_info[0]} миль.")
                else:
                    QMessageBox.warning(self, "Информация о милях", "Информации о милях не найдено.")
            # обработка ошибок
            except Exception as e:
                print(f"Ошибка при получении информации о милях: {e}")

            finally:
                if conn:
                    conn.close()

    # обновляем информацию о милях

    def update_miles(self, user_id):

        # может ругаться на название функции
        global conn
        # везде обьявляю глоабал чтобы убрать ошибку на ссылку переменной
        try:
            conn = sqlite3.connect('loyalty_program.db')
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS loyalty_program (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    miles_quantity INTEGER NOT NULL
                )
            ''')

            # проверяем, существует ли пользователь в программе лояльности
            cursor.execute('SELECT * FROM loyalty_program WHERE user_id = ?', (user_id,))
            user_info = cursor.fetchone()

            if user_info:
                # обновляем количество миль пользователя
                cursor.execute('UPDATE loyalty_program SET miles_quantity = miles_quantity + 100 WHERE user_id = ?',
                               (user_id,))

            else:
                # добавляем пользователя в программу лояльности
                cursor.execute('INSERT INTO loyalty_program (user_id, miles_quantity) VALUES (?, ?)', (user_id, 100))

            conn.commit()

        except Exception as e:
            print(f"Ошибка при обновлении миль пользователя: {e}")

        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style)

    window = FlightHelperApp()
    window.show()

    sys.exit(app.exec_())
