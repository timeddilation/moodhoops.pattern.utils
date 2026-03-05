import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator
from moodhoops.utils.colors import normalize_color


class ColorMap(BaseModel):
    """A validated color mapping with normalized color values.

    Attributes:
        from_color: The source color (hex string or RGB value) to replace.
        to_color: The target color (hex string or RGB value) to replace with.
    """

    from_color: list[int] = Field(alias="from")
    to_color: list[int] = Field(alias="to")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("from_color", "to_color", mode="before")
    @classmethod
    def normalize_colors(cls, v: str) -> list[int]:
        """Normalize and validate color values."""
        return normalize_color(v)


class SwapColorsInput(BaseModel):
    """Validated input parameters for the swap_colors function.

    Attributes:
        canvas: The image data as a numpy array.
        color_maps: A list of color mappings with 'from' and 'to' colors.
    """

    canvas: np.ndarray
    color_maps: list[ColorMap]

    model_config = ConfigDict(arbitrary_types_allowed=True)


def swap_colors(canvas: np.ndarray, color_maps: list[dict[str, str]]) -> np.ndarray:
    """Swaps colors in the canvas based on provided color maps.

    Args:
        canvas (np.ndarray): The image data as a numpy array.
        color_maps (list[dict[str, str]]): A list of dictionaries where each dictionary
            has 'from' and 'to' keys representing the colors to swap. Colors can be
            specified as hex strings (e.g., '#FF5733') or RGB tuples/lists (e.g., [255, 87, 51]).

    Returns:
        np.ndarray: The modified canvas with colors swapped.

    Raises:
        ValueError: If color_maps validation fails.
    """

    # Validate inputs using Pydantic models
    validate_color_maps = [ColorMap(**color_map) for color_map in color_maps]  # type: ignore
    validated_input = SwapColorsInput(canvas=canvas, color_maps=validate_color_maps)

    # Create a copy of the canvas to modify
    modified_canvas = np.copy(validated_input.canvas)

    # Swap colors based on the validated and normalized maps
    for color_map in validated_input.color_maps:
        mask = np.all(validated_input.canvas == color_map.from_color, axis=-1)
        modified_canvas[mask] = color_map.to_color

    return modified_canvas
