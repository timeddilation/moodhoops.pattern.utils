from typing import Any


def hex_to_ints(hex_val: str) -> list[int]:
    """
    Convert a hex color string to a list of integers [R, G, B].

    Parameters:
        hex_val (str): Hex color string, e.g. '#FF5733' or 'FF5733'.

    Returns:
        list: List of integers representing the RGB values.
    """
    if hex_val.startswith("#"):
        hex_val = hex_val[1:]

    if len(hex_val) != 6:
        raise ValueError("Hex value must be 6 characters long.")

    return [int(hex_val[i : i + 2], 16) for i in (0, 2, 4)]


def normalize_color(color: Any) -> list[int]:
    """
    Validate if the input is a valid RGB color.

    Parameters:
        color: Can be a list of integers [R, G, B], a hex string, or a tuple.

    Returns:
        List[int]: List of integers [R, G, B]
    """
    if isinstance(color, str):
        return hex_to_ints(color)
    elif isinstance(color, (list, tuple)):
        if len(color) != 3 or not all(0 <= c <= 255 for c in color):
            raise ValueError(
                "Color must be a list or tuple of three integers [R, G, B] in the range 0-255."
            )
        return list(color)
    else:
        raise TypeError("Color must be a string (hex), list, or tuple.")


def ints_to_hex(rgb: list[int]) -> str:
    """
    Convert a list of integers [R, G, B] to a hex color string.

    Parameters:
        rgb (list[int]): List of integers representing the RGB values.

    Returns:
        str: Hex color string, e.g. '#FF5733'.
    """
    if len(rgb) != 3 or not all(0 <= c <= 255 for c in rgb):
        raise ValueError(
            "Input must be a list of three integers [R, G, B] in the range 0-255."
        )
    return "#{:02X}{:02X}{:02X}".format(*rgb)
