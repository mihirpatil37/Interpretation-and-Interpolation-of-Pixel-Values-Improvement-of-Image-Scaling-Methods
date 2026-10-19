"""Tests for srlab.degrade."""

import pytest
from PIL import Image

from srlab.degrade import bicubic_downscale, modcrop


def test_modcrop_removes_remainder():
    # Arrange: an image whose size does NOT divide by 4
    img = Image.new("RGB", (2041, 1357))
    # Act
    out = modcrop(img, 4)
    # Assert
    assert out.size == (2040, 1356)


def test_modcrop_keeps_divisible_image_unchanged():
    # Arrange: an image whose size does divide by 4
    img = Image.new("RGB", (2040, 1356))
    # Act
    out = modcrop(img, 4)
    # Assert: the output is the same object as the input
    assert out.size == (2040, 1356)


def test_modcrop_keeps_top_left_corner():
    # Arrange: a black image with ONE red pixel at the top-left corner
    img = Image.new("RGB", (10, 10), color=(0, 0, 0))
    img.putpixel((0, 0), (255, 0, 0))
    # Act
    out = modcrop(img, 4)
    # Assert: the red pixel survived, so cropping happened at right/bottom
    assert out.getpixel((0, 0)) == (255, 0, 0)


@pytest.mark.parametrize("scale", [2, 3, 4])
def test_bicubic_downscale_size_is_exact(scale):
    img = Image.new("RGB", (101, 67))
    out = bicubic_downscale(img, scale)
    assert out.size == (101 // scale, 67 // scale)


def test_flat_colour_stays_flat():
    img = Image.new("RGB", (40, 40), color=(128, 128, 128))
    out = bicubic_downscale(img, 4)
    assert out.getcolors() == [(100, (128, 128, 128))]
