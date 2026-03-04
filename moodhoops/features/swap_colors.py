import numpy as np
from moodhoops.utils.colors import normalize_color


def swap_colors(canvas: np.ndarray, color_maps: list[dict[str, str]]) -> np.ndarray:
    """Swaps colors in the canvas based on provided color maps.

    Args:
        canvas (np.ndarray): The image data as a numpy array.
        color_maps (list[dict[str, str]]): A list of dictionaries where each dictionary
            has 'from' and 'to' keys representing the colors to swap. Colors can be
            specified as hex strings (e.g., '#FF5733') or RGB tuples/lists (e.g., [255, 87, 51]).

    Returns:
        np.ndarray: The modified canvas with colors swapped.
    """

    # Validate and normalize color maps
    normalized_maps = []
    for color_map in color_maps:
        if "from" not in color_map or "to" not in color_map:
            raise ValueError("Each color map must have 'from' and 'to' keys.")

        from_color = normalize_color(color_map["from"])
        to_color = normalize_color(color_map["to"])
        normalized_maps.append((from_color, to_color))

    # Create a copy of the canvas to modify
    modified_canvas = np.copy(canvas)

    # Swap colors based on the normalized maps
    for from_color, to_color in normalized_maps:
        mask = np.all(canvas == from_color, axis=-1)
        modified_canvas[mask] = to_color

    return modified_canvas
