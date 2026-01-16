# ⚡ Electricity Bill Bot

> **Track, fetch, and manage your electricity bills instantly via Telegram.**

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)
![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?logo=telegram&logoColor=white)

---

## 🧐 The Problem
Checking electricity bills often involves navigating slow, captcha-filled government portals or downloading heavy utility apps just to see a single number. For many users, finding their current due amount and payment status is a tedious, multi-step process.

## 💡 The Solution
**Electricity Bill Bot** simplifies this into a single chat. By leveraging the Telegram API and Python-based web scraping (or API integration), this bot allows users to enter their Consumer Number and instantly receive their current bill details, due dates, and payment status—all within the chat interface they use every day.

---

## ✨ Key Features

* 🤖 **Instant Bill Fetching**: Get your latest bill amount and due date in seconds.
* 🔔 **Payment Status**: Verify if your last payment has been processed.
* 📄 **PDF Download**: Retrieve the official bill PDF document directly in the chat.
* 💾 **Consumer Number Save**: Remembers your ID so you don't have to type it every time.
* 🔒 **Secure & Private**: Runs locally or on your private server; data is not stored externally.

---

## 🛠️ Tech Stack

* **Language**: ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
* **Interface**: Telegram Bot API
* **Libraries**:
    * `python-telegram-bot` / `telebot` (Bot Interface)
    * `Requests` & `BeautifulSoup` (Data Fetching)
    * `Pandas` (Data Formatting)
    * `Dotenv` (Configuration Management)

---

## 🚀 Getting Started

Follow these steps to get the bot running on your local machine in under 60 seconds.

### Prerequisites
* Python 3.8 or higher installed.
* A Telegram Bot Token (Get one from [@BotFather](https://t.me/BotFather) on Telegram).

### Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/Aniket-Raikwar1/Electricity-Bill-bot.git](https://github.com/Aniket-Raikwar1/Electricity-Bill-bot.git)
    cd Electricity-Bill-bot
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory and add your API keys:
    ```ini
    TELEGRAM_BOT_TOKEN=your_token_here
    ELECTRICITY_PROVIDER_API=your_api_url_here (if applicable)
    ```

---

## 🔌 Usage

1.  **Start the Bot**
    Run the main Python script to start polling:
    ```bash
    python main.py
    ```
    *Output should say: `Bot is polling...`*

2.  **Interact on Telegram**
    * Open Telegram and search for your bot.
    * Click **Start**.
    * Send the command:
        ```text
        /bill <your_consumer_number>
        ```
    * The bot will reply with your current bill details!

---

## 🤝 Contributing

Contributions are welcome! If you want to add support for more electricity boards or improve the scraping logic:

1.  **Fork** the project.
2.  Create your **Feature Branch** (`git checkout -b feature/AmazingFeature`).
3.  **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4.  **Push** to the branch (`git push origin feature/AmazingFeature`).
5.  Open a **Pull Request**.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 📬 Contact

**Aniket Raikwar** Data Analyst | Open Source Enthusiast

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)]([https://www.linkedin.com/in/aniket-raikwar-396510222](https://www.linkedin.com/in/aniket-raikwar/))
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/Aniket-Raikwar1)
