from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt 
from random import randint, shuffle #new

new_quest_templ = 'Нове запитання' # цей рядок встановлюється за замовчуванням до нових запитань
new_answer_templ = 'Нова відповідь' # цей рядок встановлюється за замовчуванням до нових відповідей

text_wrong = 'Неправильно'
text_correct = 'Правильно'

class Question():
    ''' Зберігає інформацію про одну анкету'''
    def __init__(self, question, answer, 
                       wrong_answer1, wrong_answer2, wrong_answer3):
        self.question = question # запитання
        self.answer = answer # правильна відповідь
        self.wrong_answer1 = wrong_answer1 # неправильна відповідь
        self.wrong_answer2 = wrong_answer2 # неправильна відповідь
        self.wrong_answer3 = wrong_answer3 # неправильна відповідь
        self.is_active = True # чи продовжуємо задавати це запитання?
        self.attempts = 0 # скільки разів задавали запитання
        self.correct = 0 # кількість правильних відповідей
    def got_right(self): #метод, що викликається при правильній выдповіді
        self.attempts += 1 #до кількості спроб додаємо 1
        self.correct += 1  #до кількості правильних відповідей додаємо 1
    def got_wrong(self):#метод, що викликається при неправильній выдповіді
        self.attempts += 1  #до кількості спроб додаємо 1

class QuestionView():
    '''співставляє дані та віджети'''
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        # конструктор, що отримує дані про віджети та співставляє їх зі значеннями (питання, відповіді заносяться до віджетів)
        self.frm_model = frm_model   #екземпрял класу Form із запитанням
                                    
        self.question = question #запитання
        self.answer = answer # правильна відповідь
        self.wrong_answer1 = wrong_answer1 # не правильна відповідь
        self.wrong_answer2 = wrong_answer2 # не правильна відповідь
        self.wrong_answer3 = wrong_answer3   # не правильна відповідь
    def change(self, frm_model):
        ''' оновлення даних про запитання'''
        self.frm_model = frm_model
    def show(self):
        ''' виводить на екран усі дані із об'єкта '''
        self.question.setText(self.frm_model.question)
        self.answer.setText(self.frm_model.answer)
        self.wrong_answer1.setText(self.frm_model.wrong_answer1)
        self.wrong_answer2.setText(self.frm_model.wrong_answer2)
        self.wrong_answer3.setText(self.frm_model.wrong_answer3)

'''new function'''
class QuestionEdit(QuestionView):
    ''' використовується, якщо треба редагувати форму: встановлює обробники подій, що зберігають текст'''
    def save_question(self):
        ''' зберігає текст запитання '''
        self.frm_model.question = self.question.text() # копіюємо дані з віджета в об'єкт
    def save_answer(self):
        ''' зберігає текст правильної відповіді '''
        self.frm_model.answer = self.answer.text() # копіює дані з віджета в об'єкт
    def save_wrong(self):
        ''' зберігає всі неправильні відповіді '''
        self.frm_model.wrong_answer1 = self.wrong_answer1.text()
        self.frm_model.wrong_answer2 = self.wrong_answer2.text()
        self.frm_model.wrong_answer3 = self.wrong_answer3.text()
    def set_connects(self):
        self.question.editingFinished.connect(self.save_question)
        self.answer.editingFinished.connect(self.save_answer)
        self.wrong_answer1.editingFinished.connect(self.save_wrong) 
        self.wrong_answer2.editingFinished.connect(self.save_wrong)
        self.wrong_answer3.editingFinished.connect(self.save_wrong)
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.set_connects()



class AnswerCheck(QuestionView):
    ''' вважаючи, що запитання анкети візуалізуються чекбоксами, перевіряє, чи правильну відповідь обрали'''
    def __init__(self, frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3, showed_answer, result):
        '''запам'ятовує усі властивості. showed_answer - віджет, у якому записана правильна відповідь (показується пізніше)
        result - віджет, у який буде записано txt_right або txt_wrong'''
        super().__init__(frm_model, question, answer, wrong_answer1, wrong_answer2, wrong_answer3)
        self.showed_answer = showed_answer
        self.result = result
    def check(self):
        ''' відповідь заноситься у статистику, але перемикання в формі не відбувається: 
        цьому класу не відомі панелі на формі '''
        if self.answer.isChecked():
            # правильна відповідь
            self.result.setText(text_correct) # напис "правильно" чи "неправильно"
            self.showed_answer.setText(self.frm_model.answer) # пишемо текст відповіді у відповідному віджеті
            self.frm_model.got_right() # оновлюємо статистику, додаємо правильну відповідь
        else:
            # відповідь неправильна
            self.result.setText(text_wrong) # напис "правильно" чи "неправильно"
            self.showed_answer.setText(self.frm_model.answer) # пишемо текст відповіді у відповідному віджеті
            self.frm_model.got_wrong() # оновлюємо статистику, додаємо неправильну відповідь
            
class QuestionListModel(QAbstractListModel):
    ''' у даних знаходиться список об'єктів Question, 
    а також список активних запитань, щоб показати його на екрані '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form_list = []
    def rowCount(self, index):
        ''' кількість елементів для показу: обов'язковий метод для моделі, з якою буде пов'язано віджет "список"'''
        return len(self.form_list)
    def data(self, index, role):
        if role == Qt.DisplayRole:
            # передаємо інтерфейсу текст запитання для відображення
            form = self.form_list[index.row()]
            return form.question
    def insertRows(self, parent=QModelIndex()):
        ''' цей метод викликається, щоб додати до списку об'єктів нові дані;
        генерується та вставляється одне порожнє запитання'''
        position = len(self.form_list) # вставляємо в кінець, повідомляємо про це наступним рядком
        self.beginInsertRows(parent, position, position) # вставка даних має бути після цього рядка і перед endInsertRows()
        self.form_list.append(Question('Нове запитання','правильна відповідь','неправильна відповідь','неправильна відповідь','неправильна відповідь')) # додали нове хапитання до списку даних
        self.endInsertRows() # закінчили вставку, тепер працюємо з моделлю
        QModelIndex()
        return True # повідомляє, що все ок
    def removeRows(self, position, parent=QModelIndex()):
        ''' стандартний метод для видалення рядків - після видалення з моделі, рядок автоматично видаляється з екрану'''
        self.beginRemoveRows(parent, position, position) # повідомляємо, що хочемо видалити рядок від position до position 
        self.form_list.pop(position) # видаляємо зі списку елемент з номером position
        self.endRemoveRows() # закінчили видалення (далі бібліотека сама оновлює список на екрані)
        return True # повідомляє, що все вдалось 
    def random_question(self):
        ''' Видає випадкове запитання '''
        total = len(self.form_list)
        current = randint(0, total - 1)
        return self.form_list[current]

def random_AnswerCheck(list_model, w_question, widgets_list, w_showed_answer, w_result):
    '''повертає новий екземпляр класу AnswerCheck, 
    з випадковим запитанням та випадковим розподіленням відповідей по віджетам'''
    frm = list_model.random_question()
    shuffle(widgets_list)
    frm_card = AnswerCheck(frm, w_question, widgets_list[0], widgets_list[1], widgets_list[2], widgets_list[3], w_showed_answer, w_result)
    return frm_card
