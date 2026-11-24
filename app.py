# -*- coding: utf-8 -*-
"""
Лабораторная работа № 1: Разработка веб-приложения на Python
Вариант 7: Анализ и перестановка RGB каналов изображения
Фреймворк: Flask
"""

import io
import os
from datetime import datetime

from PIL import Image
from flask import Flask, render_template, request, send_file

# Функции обработки изображения вынесены в отдельный модуль
# image_utils.py — так их можно тестировать юнит-тестами без Flask
from image_utils import permute_channels, plot_histogram, plot_means, add_timestamp

app = Flask(__name__)

# Папка static нужна для сохранения графиков (гистограмма, средние значения)
os.makedirs("static", exist_ok=True)


@app.route("/")
def index():
    """Главная страница веб-приложения."""
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    """Обработка изображения: перестановка каналов + временная метка."""
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
