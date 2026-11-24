# Лабораторная работа №1. Анализ и перестановка RGB каналов изображения

## Вариант 7

Веб-приложение на Flask: загрузка изображения, перестановка цветовых каналов R, G, B,
гистограмма распределения цветов, графики среднего значения по вертикали (по строкам)
и по горизонтали (по столбцам). Дополнительное задание — нанесение временной метки
(дата/время) на изображение по желанию пользователя.

## Структура проекта

```
.
├── app.py                  # серверная часть (Flask)
├── image_utils.py          # функции обработки изображения
├── conftest.py             # настройка путей для pytest
├── requirements.txt        # список зависимостей
├── .gitignore
├── .github
│   └── workflows
│       └── ci.yml          # GitHub Actions: автозапуск тестов при каждом push
├── static                  # сохранённые графики (hist.png, means.png)
├── templates
│   └── index.html          # страница веб-приложения
└── tests
    └── test_image_utils.py # юнит-тесты функций обработки изображения
```

## Запуск

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate    # Linux
pip install -r requirements.txt
python app.py
```

Открыть приложение: http://127.0.0.1:5000

## Тесты

```bash
python -m pytest tests/ -v
```

## CI

Тесты запускаются автоматически при каждом push в репозиторий
(GitHub Actions, файл `.github/workflows/ci.yml`).
