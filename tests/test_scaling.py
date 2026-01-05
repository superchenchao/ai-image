import pytest

from ai_image.scaling import Dimensions, scale_to_fit


def test_scale_prevents_zero_dimension_on_extreme_aspect_ratio():
    original = Dimensions(width=1, height=1000)
    max_dimensions = Dimensions(width=100, height=100)

    scaled = scale_to_fit(original, max_dimensions)

    assert scaled.width == 1
    assert scaled.height == 100


def test_scale_avoids_upscaling_when_not_requested():
    original = Dimensions(width=400, height=300)
    max_dimensions = Dimensions(width=800, height=800)

    scaled = scale_to_fit(original, max_dimensions, allow_upscale=False)

    assert scaled == original


def test_scale_respects_upscale_flag():
    original = Dimensions(width=400, height=300)
    max_dimensions = Dimensions(width=800, height=800)

    scaled = scale_to_fit(original, max_dimensions, allow_upscale=True)

    assert scaled == Dimensions(width=800, height=600)


def test_invalid_dimension_inputs_raise():
    with pytest.raises(ValueError):
        scale_to_fit(Dimensions(width=0, height=10), Dimensions(width=10, height=10))

    with pytest.raises(ValueError):
        scale_to_fit(Dimensions(width=10, height=10), Dimensions(width=-1, height=10))
