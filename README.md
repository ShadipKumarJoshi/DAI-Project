# 🛠️ Django + Tailwind Setup Guide

This guide outlines how to activate the virtual environment, run the development server, and start Tailwind CSS in your Django project.

---

## 📦 Setup Instructions

### ✅ 1. Create the Virtual Environment

```bash
python -m venv venv
```


### ✅ 1.1. Activate the Virtual Environment

```bash
source venv/Scripts/activate
```

> 💡 **Note:** If you're on Mac/Linux, the path may differ (e.g., `source venv/bin/activate`).

---

### 🚀 2. Run the Django Development Server

```bash
py manage.py runserver
```

> This will start your local server at `http://127.0.0.1:8000/`.

---

### 🎨 3. Start Tailwind CSS (Watch Mode)

```bash
python manage.py tailwind start
```

> This command watches your Tailwind CSS files and automatically compiles styles during development.

---

## 📁 Additional Notes

- Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

- Tailwind should be properly configured in `settings.py` using [django-tailwind](https://django-tailwind.readthedocs.io/en/latest/).

---

Happy Coding! 💻