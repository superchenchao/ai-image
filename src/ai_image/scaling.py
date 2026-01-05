"""Aspect-ratio aware scaling helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Dimensions:
    """Represents image dimensions."""

    width: int
    height: int

    @classmethod
    def from_iterable(cls, values: Iterable[int]) -> "Dimensions":
        width, height = values
        return cls(int(width), int(height))

    def assert_positive(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive.")


def scale_to_fit(
    original: Dimensions,
    max_dimensions: Dimensions,
    *,
    allow_upscale: bool = False,
) -> Dimensions:
    """Scale ``original`` dimensions to fit inside ``max_dimensions``.

    The function preserves aspect ratio and can optionally allow upscaling.
    A guard ensures we never return a zero dimension even when rounding down
    extreme aspect ratios.
    """

    original.assert_positive()
    max_dimensions.assert_positive()

    scale_x = max_dimensions.width / original.width
    scale_y = max_dimensions.height / original.height
    scale = min(scale_x, scale_y)

    if scale >= 1.0 and not allow_upscale:
        return original

    new_width = max(1, round(original.width * scale))
    new_height = max(1, round(original.height * scale))

    # Avoid overflows caused by rounding up.
    new_width = min(max_dimensions.width, new_width)
    new_height = min(max_dimensions.height, new_height)

    return Dimensions(int(new_width), int(new_height))
