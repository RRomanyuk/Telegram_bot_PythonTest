# Telegram Quiz Bot (Python)

## Overview

This project is a Telegram bot that implements an interactive quiz for testing Python knowledge.
The bot presents multiple-choice questions, evaluates user answers, and provides immediate feedback with explanations.

The system tracks user progress, calculates results, and displays final statistics including score and completion time.

---

## Features

* Interactive quiz via Telegram
* Multiple-choice questions with inline buttons
* Instant feedback after each answer
* Randomized question order
* Score tracking
* Quiz duration measurement
* Final results summary

---

## Technologies Used

* Python
* python-telegram-bot library (async version)
* Telegram Bot API

---

## How It Works

### 1. Quiz Start

* User sends `/start` command
* Bot initializes session:

  * randomizes questions
  * resets score
  * starts timer

### 2. Question Flow

* Each question is sent with answer options (inline keyboard)
* User selects an answer
* Bot:

  * checks correctness
  * shows correct answer
  * provides feedback

### 3. Quiz Completion

* After all questions:

  * total correct answers displayed
  * time spent is calculated
  * timestamp is shown

---

## Project Structure

* Question database (list of dictionaries)
* User session storage (`user_data`)
* Handlers:

  * `/start` command
  * answer processing (callback queries)
* Core logic:

  * question generation
  * answer validation
  * result calculation

---

## How to Run

1. Install dependencies:

```
pip install python-telegram-bot
```

2. Insert your Telegram Bot Token:

* Replace token in:

```
ApplicationBuilder().token("YOUR_TOKEN")
```

3. Run the bot:

```
python bot.py
```

4. Open Telegram and start the bot using `/start`

---

## Example Functionality

* Question display:

  * "Питання 1: ..."
* Answer selection via buttons
* Feedback:

  * ✅ Correct
  * ❌ Incorrect
* Final result:

  * Score (e.g., 7/10)
  * Time spent
  * Date and time

---

## Limitations

* Data stored in memory (no database)
* Single-session logic per user
* No persistent statistics

---

## Notes

* The project uses asynchronous handlers for better performance
* Designed for educational purposes and demonstration of bot logic
* Can be extended into a full learning platform
