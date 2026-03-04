import numpy as np


def slow_down_pattern(
    canvas: np.ndarray, mode_speed: int, desired_speed: int
) -> np.ndarray:
    """Simulates slowing down a pattern to a lower speed by repeating rows in the image.

    Supports non-integer stretch ratios by distributing extra duplicated rows over time.
    Example: mode_speed=300, desired_speed=250 -> ratio=1.2, so every 5th row
    gets one additional duplicate.

    The speed integer value refers to the same value used in the moodhoops mode configuration,
    which is a unit of *Rows Per Second* (RPS).
    For example, if the mode is configured to run at 300 RPS, then mode_speed should be 300.
    If you want to slow it down to 250 RPS, then desired_speed should be 250.

    Args:
        canvas (np.ndarray): The image data as a numpy array.
        mode_speed (int): The current speed of the mode the pattern is in.
        desired_speed (int): The desired speed to slow down the pattern to.
    """

    if mode_speed <= 0 or desired_speed <= 0:
        raise ValueError("Mode speed and desired speed must be positive integers.")

    if mode_speed > 500 or desired_speed > 500:
        raise ValueError(
            "Mode speed and desired speed must be less than or equal to 500."
        )

    if desired_speed >= mode_speed:
        raise ValueError("Desired speed must be less than the current mode speed.")

    # Distribute duplicates with integer math to avoid float precision issues.
    #
    # mode_speed / desired_speed = base_repeat + remainder / desired_speed
    #
    # We always repeat each row `base_repeat` times, then accumulate `remainder`.
    # Whenever accumulation reaches/exceeds `desired_speed`, we add one extra
    # duplicate for that row and subtract `desired_speed` from the accumulator.
    # This behaves like a Bresenham-style error accumulator.
    base_repeat = mode_speed // desired_speed
    remainder = mode_speed % desired_speed

    row_indices = []
    accumulator = 0

    for row_index in range(canvas.shape[0]):
        repeat_count = base_repeat
        accumulator += remainder

        if accumulator >= desired_speed:
            repeat_count += 1
            accumulator -= desired_speed

        row_indices.extend([row_index] * repeat_count)

    return canvas[row_indices]
