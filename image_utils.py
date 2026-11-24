# -*- coding: utf-8 -*-
"""
Функции обработки изображения для лабораторной работы № 1.
Анализ и перестановка RGB каналов изображения.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")  # без графической подсистемы X11
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

CHANNELS = {"R": 0, "G": 1, "B": 2}


def permute_channels(image, order):
    """Перестановка каналов.

    order - строка вида "GBR": в новый канал R попадает
    исходный G, в новый G - исходный B, в новый B - исходный R.
    """
    if not isinstance(order, str) or len(order) != 3 \
            or not set(order) <= set(CHANNELS):
        raise ValueError(f"Недопустимый порядок каналов: {order}")
    arr = np.asarray(image.convert("RGB"), dtype=np.uint8)
    perm = [CHANNELS[ch] for ch in order]
    # perm[i] - номер исходного канала, попадающего в выходной канал i
    return arr[..., perm]


def plot_histogram(arr, path):
    """Гистограмма распределения цветов R, G, B."""
    fig, ax = plt.subplots(figsize=(8, 4))
    for i, (color, label) in enumerate((("r", "R"), ("g", "G"), ("b", "B"))):
        hist, _ = np.histogram(arr[..., i], bins=256, range=(0, 256))
        ax.plot(hist, color=color, label=label, alpha=0.7)
    ax.set_xlabel("Яркость")
    ax.set_ylabel("Число пикселей")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def plot_means(arr, path):
    """Средняя яркость по вертикали (по строкам) и
    по горизонтали (по столбцам)."""
    row_mean = arr.mean(axis=(1, 2))  # среднее по каждой строке
    col_mean = arr.mean(axis=(0, 2))  # среднее по каждому столбцу
    fig, axes = plt.subplots(1, 2, figsize=(10, 3))
    axes[0].plot(row_mean, color="k")
    axes[0].set_title("Среднее по вертикали (по строкам)")
    axes[1].plot(col_mean, color="k")
    axes[1].set_title("Среднее по горизонтали (по столбцам)")
    for ax_ in axes:
        ax_.set_xlabel("Номер строки / столбца")
        ax_.grid(True)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def add_timestamp(image, text):
    """Нанесение временной метки на изображение (доп. задание)."""
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
    x, y = 12, image.height - 42
    # тень для читаемости на любом фоне
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))
    return image
