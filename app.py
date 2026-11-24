# -*- coding: utf-8 -*-
"""
Лабораторная работа № 1: Разработка веб-приложения на Python
Вариант 7: Анализ и перестановка RGB каналов изображения
Фреймворк: Flask
"""

import io
import os
import re
import hashlib
from datetime import datetime, date

from PIL import Image
from flask import Flask, render_template, request, send_file, make_response

# Функции обработки изображений вынесены в отдельный модуль
# image_utils.py - так их можно тестировать юнит-тестами без Flask
from image_utils import permute_channels, plot_histogram, plot_means, add_timestamp

app = Flask(__name__)

# Папка static нужна для сохранения графиков (гистограмма, средние значения)
os.makedirs("static", exist_ok=True)

# Токен для верификации развёрнутого приложения
VERIFY_TOKEN = 'TUSUR-KURBANOV-20261122-B2F7FE96'


def normalize_html(html: str) -> str:
    """Приводит HTML к каноническому виду для хэширования.

    Правила нормализации:
    1. Убираем пробелы в начале и конце каждой строки (strip)
    2. Убираем пустые строки
    3. Заменяем все последовательности пробелов на один пробел
    4. Объединяем строки одинарным \n
    """
    lines = [line.strip() for line in html.split('\n')]
    lines = [line for line in lines if line]
    lines = [re.sub(r'\s+', ' ', line) for line in lines]
    return '\n'.join(lines)


@app.route("/")
def index():
    """Главная страница веб-приложения."""
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    """Обработка изображения: перестановка каналов и временная метка."""
    file = request.files.get("image")
    if not file:
        return "Изображение не загружено", 400

    order = request.form.get("order", "RGB")
    with_ts = "with_timestamp" in request.form

    img = Image.open(file.stream).convert("RGB")

    # Дополнительное задание: временная метка по желанию пользователя
    if with_ts:
        stamp = (request.form.get("timestamp")
                 or datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
        img = add_timestamp(img, stamp)

    # Перестановка каналов и построение графиков
    result = permute_channels(img, order)
    plot_histogram(result, "static/hist.png")
    plot_means(result, "static/means.png")

    buf = io.BytesIO()
    Image.fromarray(result).save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/verify")
def verify():
    """Эндпоинт верификации: токен + SHA-256 от нормализованного HTML."""
    today = date.today().isoformat()
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Verification</title>
</head>
<body>
<h1>Verification</h1>
<p>Token: {VERIFY_TOKEN}</p>
<p>Date: {today}</p>
</body>
</html>'''
    normalized = normalize_html(html)
    body_hash = hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    response = make_response(html)
    response.headers['X-Verify-Hash'] = body_hash
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
