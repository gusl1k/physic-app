from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    STANDARD_COLOR = "QPushButton {background-color: rgb(225, 225, 225)}"
    GREEN_COLOR = "QPushButton {background-color: rgb(191, 255, 191)}"
    RED_COLOR = "QPushButton {background-color: rgb(252, 192, 191)}"

    LABEL_QUESTION_TEXT = '<html><head/><body><p align="center"><span style=" font-size:14pt;">{0}</span></p></body></html>'
    LABEL_RESULT_TEXT = '<html><head/><body><p><span style=" font-size:10pt;">{0}</span></p></body></html>'
    LABEL_RESULTS_TEXT = '<html><head/><body><p align="center"><span style=" font-size:10pt;">{0} из {1}</span></p></body></html>'

    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0)

        self.current_question = 0
        self.right_answers = 0
        self.answered_button = None
        self.create_questions()

        # page 1
        self.ui.pushButton_exit.clicked.connect(QApplication.closeAllWindows)
        self.ui.pushButton_start.clicked.connect(self.go_to_page_2)

        # page 2
        self.ui.pushButton_answer1.clicked.connect(self.pushButton_answer1_clicked)
        self.ui.pushButton_answer2.clicked.connect(self.pushButton_answer2_clicked)
        self.ui.pushButton_answer3.clicked.connect(self.pushButton_answer3_clicked)
        self.ui.pushButton_answer4.clicked.connect(self.pushButton_answer4_clicked)
        self.ui.pushButton_next.clicked.connect(self.set_data_to_page_2)

        # page 3
        self.ui.pushButton_exit_2.clicked.connect(QApplication.closeAllWindows)
        self.ui.pushButton_repeat.clicked.connect(self.go_to_page_2)

    # Создание списка вопросов
    # "formula": "",
    # 1: "",
    # 2: "",
    # 3: "",
    # 4: "",
    # "answer": 0

    def create_questions(self) -> None:
        self.questions = [
            {
                "formula": "a = (v - v0)/t",
                1: "Скорость",
                2: "Ускорение",
                3: "Время",
                4: "Длина пути",
                "answer": 2
            },
            {
                "formula": "p=F/S",
                1: "Давление",
                2: "Расстояние",
                3: "Плотность",
                4: "Скорость",
                "answer": 1
            },
            {
                "formula": "F=kΔl",
                1: "Закон Архимеда",
                2: "Закон сохранения скорости",
                3: "Первый закон Ньютона",
                4: "Закон Гука",
                "answer": 4
            },
            {"formula": "Формула кинетической энергии: ",
             1: "E=mc*c",
             2: "E=mgh",
             3: "E=mv*v/2",
             4: "F=ma",
             "answer": 3
             },
        ]

    # Переход на 2ю страницу (вопрос-ответ)
    def go_to_page_2(self) -> None:
        self.ui.stackedWidget.setCurrentIndex(1)
        self.set_data_to_page_2()

    # Переход на 3ю страницу (итоги)
    def go_to_page_3(self) -> None:
        self.current_question = 0
        self.ui.stackedWidget.setCurrentIndex(2)
        self.ui.label_results.setText(self.LABEL_RESULTS_TEXT.format(self.right_answers, len(self.questions)))
        self.right_answers = 0

    # Задаем данные 2й странице
    def set_data_to_page_2(self) -> None:
        if self.current_question == len(self.questions):
            self.go_to_page_3()
            return

        if self.answered_button != None:
            self.answered_button.setStyleSheet(self.STANDARD_COLOR)

        # Активация кнопок
        self.ui.pushButton_answer1.setEnabled(True)
        self.ui.pushButton_answer2.setEnabled(True)
        self.ui.pushButton_answer3.setEnabled(True)
        self.ui.pushButton_answer4.setEnabled(True)

        # Задаем необходимые тексты 
        self.ui.label_question.setText(
            self.LABEL_QUESTION_TEXT.format(self.questions[self.current_question]["formula"]))

        self.ui.pushButton_answer1.setText(self.questions[self.current_question][1])
        self.ui.pushButton_answer2.setText(self.questions[self.current_question][2])
        self.ui.pushButton_answer3.setText(self.questions[self.current_question][3])
        self.ui.pushButton_answer4.setText(self.questions[self.current_question][4])

        self.ui.label_result.setText(self.LABEL_RESULT_TEXT.format("Выберите ответ"))

        self.current_question += 1

    # При нажатии кнопки 1
    def pushButton_answer1_clicked(self) -> None:
        self.set_answered_button_color(self.ui.pushButton_answer1, answered=1)
        self.ui.pushButton_answer2.setDisabled(True)
        self.ui.pushButton_answer3.setDisabled(True)
        self.ui.pushButton_answer4.setDisabled(True)

    # При нажатии кнопки 2
    def pushButton_answer2_clicked(self) -> None:
        self.set_answered_button_color(self.ui.pushButton_answer2, answered=2)
        self.ui.pushButton_answer1.setDisabled(True)
        self.ui.pushButton_answer3.setDisabled(True)
        self.ui.pushButton_answer4.setDisabled(True)

    # При нажатии кнопки 3
    def pushButton_answer3_clicked(self) -> None:
        self.set_answered_button_color(self.ui.pushButton_answer3, answered=3)
        self.ui.pushButton_answer1.setDisabled(True)
        self.ui.pushButton_answer2.setDisabled(True)
        self.ui.pushButton_answer4.setDisabled(True)

    # При нажатии кнопки 4
    def pushButton_answer4_clicked(self) -> None:
        self.set_answered_button_color(self.ui.pushButton_answer4, answered=4)
        self.ui.pushButton_answer1.setDisabled(True)
        self.ui.pushButton_answer2.setDisabled(True)
        self.ui.pushButton_answer3.setDisabled(True)

    # Меняем цвет нажатой кнопки в зависимости от правильности ответа
    def set_answered_button_color(self, button: QPushButton, answered: int) -> None:
        self.answered_button = button
        if self.is_right_answer(answered) == True:
            stylesheet = self.GREEN_COLOR
        else:
            stylesheet = self.RED_COLOR
        button.setStyleSheet(stylesheet)

    # Проверка на правильный ли ответ
    def is_right_answer(self, your_answer: int) -> bool:
        right_answer = self.questions[self.current_question - 1]["answer"]
        if right_answer == your_answer:
            self.right_answers += 1
            result_text = "Молодец, ты ответил верно!"
            result = True
        else:
            result_text = "Упс, в следующий раз думай лучше..."
            result = False

        self.ui.label_result.setText(self.LABEL_RESULT_TEXT.format(result_text))
        return result


def main() -> None:
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
