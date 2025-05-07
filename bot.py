import random
import time
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

questions = [
    {
        "question": "Яке ключове слово використовується для створення класу у Python?",
        "options": ["function", "define", "class", "object"],
        "correct_option": 2
    },
    {
        "question": "Що таке інкапсуляція в ООП?",
        "options": [
            "Можливість об'єднувати код у функції",
            "Можливість приховувати деталі реалізації класу",
            "Можливість наслідувати функціонал від інших класів",
            "Можливість змінювати типи даних"
        ],
        "correct_option": 1
    },
    {
        "question": "Який результат виконує оператор `is` у Python?",
        "options": [
            "Порівнює значення змінних",
            "Перевіряє, чи об'єкти мають однаковий тип",
            "Перевіряє, чи об'єкти — це один і той самий екземпляр",
            "Визначає тип об'єкта"
        ],
        "correct_option": 2
    },
    {
        "question": "Яка стандартна бібліотека використовується для роботи з регулярними виразами?",
        "options": ["regex", "re", "match", "pattern"],
        "correct_option": 1
    },
    {
        "question": "Що таке метод `__init__` у класі Python?",
        "options": [
            "Метод для копіювання об'єкта",
            "Метод, який викликається при створенні об'єкта",
            "Метод, який викликається при видаленні об'єкта",
            "Метод, що визначає тип об'єкта"
        ],
        "correct_option": 1
    },
    {
        "question": "Що таке список (list) у Python?",
        "options": [
            "Невпорядкована структура даних з унікальними елементами",
            "Набір пар ключ-значення",
            "Впорядкована змінна колекція елементів",
            "Невпорядкована послідовність змінних"
        ],
        "correct_option": 2
    },
    {
        "question": "Як викликати метод батьківського класу в дочірньому класі?",
        "options": ["base.method()", "super().method()", "self.parent()", "inherit.method()"],
        "correct_option": 1
    },
    {
        "question": "Яка функція використовується для перетворення рядка в число?",
        "options": ["str()", "float()", "int()", "number()"],
        "correct_option": 2
    },
    {
        "question": "Що робить інструкція `break` у циклі?",
        "options": [
            "Пропускає одну ітерацію",
            "Повертає результат з функції",
            "Завершує виконання програми",
            "Перериває виконання циклу"
        ],
        "correct_option": 3
    },
    {
        "question": "Який результат виконає `len([1, 2, 3])`?",
        "options": ["2", "3", "4", "0"],
        "correct_option": 1
    }
]

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {
        "questions": random.sample(questions, len(questions)),
        "current_index": 0,
        "correct": 0,
        "start_time": time.time()
    }
    await ask_question(update, context)

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data = user_data[chat_id]
    index = data["current_index"]

    if index < len(data["questions"]):
        q = data["questions"][index]
        options = q["options"]
        keyboard = [
            [InlineKeyboardButton(text=opt, callback_data=str(i))]
            for i, opt in enumerate(options)
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"Питання {index + 1}: {q['question']}",
            reply_markup=reply_markup
        )
    else:
        await finish_quiz(update, context)

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    data = user_data[chat_id]
    index = data["current_index"]
    question = data["questions"][index]
    correct_index = question["correct_option"]

    selected_index = int(query.data)
    is_correct = selected_index == correct_index

    if is_correct:
        data["correct"] += 1

    # Формування повідомлення з поясненням
    response_text = (
        f"Питання {index + 1}: {question['question']}\n\n"
        f"Ваша відповідь: {question['options'][selected_index]}\n"
        f"Правильна відповідь: {question['options'][correct_index]}\n\n"
        f"{'✅ Вірно!' if is_correct else '❌ Невірно!'}"
    )

    await query.edit_message_text(response_text)

    data["current_index"] += 1
    await ask_question(update, context)


async def finish_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data = user_data[chat_id]
    duration = round(time.time() - data["start_time"])
    score = data["correct"]
    total = len(data["questions"])
    result_text = (
        f"🎓 Тест завершено!\n"
        f"✅ Правильних відповідей: {score} з {total}\n"
        f"📅 Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"⏱ Тривалість: {duration} сек"
    )
    await context.bot.send_message(chat_id=chat_id, text=result_text)

# Основна функція
def main():
    app = ApplicationBuilder().token("7924136393:AAFjSxj2Lw2uxqAxR_QO3CWeVmh7NculAO0").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_answer))
    app.run_polling()

if __name__ == "__main__":
    main()