# 📸 Telegram Photo Collage Grid Bot

A continuous polling Telegram Bot that accepts images from users and stitches them together into a clean 2x2 grid collage. Built with Python, `python-telegram-bot`, and `Pillow`.

This repository is optimized for deployment as a **Background Worker** on [Render](https://render.com).

---

## 🚀 Features
* **In-Memory Buffer:** Temporarily queues photos per user without filling up server disk space.
* **Auto-Resizing:** Automatically resizes sent photos into equal quadrants.
* **Long Polling Architecture:** Runs continuously without requiring complex webhook URLs or SSL setups.

---

## 🛠️ Local Setup & Installation

If you want to test the bot locally before pushing to production, follow these steps:

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME
