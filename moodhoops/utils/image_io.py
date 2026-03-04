import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def load_image(image_file_path: str) -> np.ndarray:
    """Loads an image from a file path and converts it to a numpy array.

    Args:
        image_file_path (str): The path to the image file.

    Raises:
        FileNotFoundError: If the image file does not exist.
        ValueError: If the image file is not a .bmp file.

    Returns:
        np.ndarray: The image data as a numpy array.
    """

    if not os.path.exists(image_file_path):
        raise FileNotFoundError(f"Image file path '{image_file_path}' does not exist.")

    if not image_file_path.lower().endswith(".bmp"):
        raise ValueError(f"Image file '{image_file_path}' is not a .bmp file.")

    img = Image.open(image_file_path).convert("RGB")
    return np.array(img)


def save_image(
    image_array: np.ndarray, file_name: str, custom_filepath: bool = False
) -> None:
    """Saves canvas to bmp

    Args:
        image_array (np.ndarray): The image data as a numpy array.
        file_name (str): The name of the file where the image will be saved.
        custom_filepath (bool): Whether the file_name is a custom file path. If False, the image will be saved in the "exports" directory.
    """

    if not file_name.lower().endswith(".bmp"):
        file_name += ".bmp"

    if custom_filepath:
        image_file_path = file_name
    else:
        image_file_path = os.path.join("exports", file_name)

    output_image = Image.fromarray(image_array)
    output_image.save(image_file_path, format="BMP")


def preview_pattern(image_array: np.ndarray) -> None:
    """Previews the pattern by displaying it as an image.

    Specifically for use in Jupyter notebooks or environments where image display is supported.

    Args:
        image_array (np.ndarray): The image data as a numpy array.
    """
    img_filepath = "temp/preview_pattern.bmp"
    save_image(image_array, img_filepath, custom_filepath=True)

    # Load the image
    img = mpimg.imread(img_filepath)

    # Display the image
    plt.imshow(img)
    plt.axis("off")  # Hide axes
    plt.show()
