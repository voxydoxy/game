from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel, QButtonGroup
import random

class Question:
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

app = QApplication([])

window = QWidget()
window.setWindowTitle('Memory Card')

lb_Question = QLabel('Какой национальности не существует?')

RadioGroupBox = QGroupBox('Варианты ответа')
rbtn_1 = QRadioButton()
rbtn_2 = QRadioButton()
rbtn_3 = QRadioButton()
rbtn_4 = QRadioButton()

radio_group = QButtonGroup()
radio_group.addButton(rbtn_1)
radio_group.addButton(rbtn_2)
radio_group.addButton(rbtn_3)
radio_group.addButton(rbtn_4)

layout_ans1 = QHBoxLayout()
layout_ans2 = QVBoxLayout()
layout_ans3 = QVBoxLayout()

layout_ans2.addWidget(rbtn_1)
layout_ans2.addWidget(rbtn_3)
layout_ans3.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)
RadioGroupBox.setLayout(layout_ans1)

ResultGroupBox = QGroupBox('Результат теста')
lb_Result = QLabel('Правильно/Неправильно')

result_layout = QVBoxLayout()
result_layout.addWidget(lb_Result, alignment=Qt.AlignCenter)
ResultGroupBox.setLayout(result_layout)

ResultGroupBox.hide()

btn_OK = QPushButton('Ответить')

main_layout = QVBoxLayout()
main_layout.addWidget(lb_Question, alignment=Qt.AlignCenter)
main_layout.addWidget(RadioGroupBox)
main_layout.addWidget(ResultGroupBox)
main_layout.addWidget(btn_OK, alignment=Qt.AlignCenter)

window.setLayout(main_layout)

questions_list = [
    Question('Какой национальности не существует?', 'Смурфы', 'Энцы', 'Чулымцы', 'Алеуты'),
    Question('Какой язык является официальным в Бразилии?', 'Португальский', 'Испанский', 'Английский', 'Французский'),
    Question('Сколько океанов на планете?', '5', '3', '4', '7'),
    Question('Какой континент самый большой?', 'Азия', 'Африка', 'Европа', 'Австралия')
]

correct_answers = 0
total_questions = 0

window.question_index = -1

def update_stats():
    if total_questions > 0:
        rating = (correct_answers / total_questions) * 100
    else:
        rating = 0  # Если нет вопросов, рейтинг равен 0
    print(f"Правильных ответов: {correct_answers}")
    print(f"Общее количество вопросов: {total_questions}")
    print(f"Рейтинг: {rating:.2f}%")

def ask(q):
    lb_Question.setText(q.question)
    answers = [q.right_answer, q.wrong1, q.wrong2, q.wrong3]
    random.shuffle(answers)
    rbtn_1.setText(answers[0])
    rbtn_2.setText(answers[1])
    rbtn_3.setText(answers[2])
    rbtn_4.setText(answers[3])
    show_question()
    update_stats()

def check_answer():
    global correct_answers, total_questions
    selected_button = radio_group.checkedButton()
    total_questions += 1 
    if selected_button and selected_button.text() == questions_list[window.question_index].right_answer:
        correct_answers += 1 
        return True  
    return False 

def show_result():
    is_correct = check_answer()
    if is_correct:
        lb_Result.setText(f'Правильно! {questions_list[window.question_index].right_answer} - это верный ответ.')
    else:
        selected_button = radio_group.checkedButton()
        if selected_button:
            lb_Result.setText(f'Неправильно! {questions_list[window.question_index].right_answer} - это верный ответ.')
        else:
            lb_Result.setText(f'Неправильно! Вы не выбрали ответ.')

    RadioGroupBox.hide()
    ResultGroupBox.show()
    btn_OK.setText('Следующий вопрос')

def show_question():
    ResultGroupBox.hide()
    RadioGroupBox.show()
    btn_OK.setText('Ответить')
    radio_group.setExclusive(False)  
    for button in radio_group.buttons():
        button.setChecked(False)
    radio_group.setExclusive(True)  

def next_question():
    window.question_index += 1
    if window.question_index >= len(questions_list):
        window.question_index = 0
    ask(questions_list[window.question_index])

def click_ok():
    if btn_OK.text() == 'Ответить':
        show_result()
    else:
        next_question()

btn_OK.clicked.connect(click_ok)

next_question()

window.show()
app.exec_()
