# -*- coding: utf-8 -*-
"""
Юнит-тесты функций обработки изображения (ЛР № 1).

Запуск: pytest tests/ -v
"""

import os

import numpy as np
import pytest
from PIL import Image

from image_utils import add_timestamp, permute_channels, plot_histogram, plot_means


def make_test_image(w=8, h=6):
    """Тестовое изображение: значения в каналах R, G, B различны,
    чтобы перестановку каналов легко было проверить."""
    idx = np.arange(w * h)  # считаем в int, затем приводим к uint8
    r = (idx % 256).astype(np.uint8).reshape(h, w)
    g = ((idx * 3 + 1) % 256).astype(np.uint8).reshape(h, w)
    b = ((idx * 7 + 2) % 256).astype(np.uint8).reshape(h, w)
    return Image.fromarray(np.dstack([r, g, b]))


def test_permute_identity():
    """Порядок "RGB" не должен менять каналы."""
    img = make_test_image()
    expected = np.asarray(img)
    result = permute_channels(img, "RGB")
    assert np.array_equal(result, expected)


def test_permute_gbr():
    """Для "GBR": новый R = старый G, новый G = старый B, новый B = старый R."""
    img = make_test_image()
    original = np.asarray(img)
    result = permute_channels(img, "GBR")
    assert np.array_equal(result[..., 0], original[..., 1])  # R <- G
    assert np.array_equal(result[..., 1], original[..., 2])  # G <- B
    assert np.array_equal(result[..., 2], original[..., 0])  # B <- R


def test_permute_shape_preserved():
    img = make_test_image(w=17, h=13)
    result = permute_channels(img, "BRG")
    assert result.shape == (13, 17, 3)
    assert result.dtype == np.uint8


def test_permute_invalid_order():
    with pytest.raises(ValueError):
        permute_channels(make_test_image(), "XYZ")
    with pytest.raises(ValueError):
        permute_channels(make_test_image(), "RG")


def test_add_timestamp_changes_image():
    """Метка меняет изображение, но не меняет его размер и режим."""
    img = make_test_image(w=200, h=100)
    before = np.asarray(img.copy())
    result = add_timestamp(img.copy(), "24.11.2026 10:00:00")
    assert result.size == img.size
    assert result.mode == "RGB"
    assert not np.array_equal(np.asarray(result), before)  # пиксели изменились


def test_plot_histogram_creates_file(tmp_path):
    arr = np.asarray(make_test_image())
    path = tmp_path / "hist.png"
    plot_histogram(arr, str(path))
    assert path.exists() and os.path.getsize(path) > 0


def test_plot_means_creates_file(tmp_path):
    arr = np.asarray(make_test_image())
    path = tmp_path / "means.png"
    plot_means(arr, str(path))
    assert path.exists() and os.path.getsize(path) > 0
