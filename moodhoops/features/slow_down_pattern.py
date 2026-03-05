import numpy as np
from pydantic import BaseModel, Field, ConfigDict, field_validator


class SlowDownPatternInput(BaseModel):
    """Validated input parameters for the slow_down_pattern function.

    Attributes:
        canvas: The image data as a numpy array.
        mode_speed: The current speed of the pattern (1-500 Rows Per Second).
        desired_speed: The target speed to slow down to (1-500 RPS, must be less than mode_speed).
    """

    canvas: np.ndarray
    mode_speed: int = Field(
        gt=0, le=500, description="Current pattern speed in RPS (1-500)"
    )
    desired_speed: int = Field(
        gt=0, le=500, description="Target pattern speed in RPS (1-500)"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("desired_speed")
    @classmethod
    def desired_speed_less_than_mode_speed(cls, v: int, info) -> int:
        """Ensure desired_speed is less than mode_speed."""
        if "mode_speed" in info.data and v >= info.data["mode_speed"]:
            raise ValueError("Desired speed must be less than the current mode speed.")
        return v


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
        mode_speed (int): The current speed of the mode the pattern is in (1-500 RPS).
        desired_speed (int): The desired speed to slow down the pattern to (1-500 RPS).

    Raises:
        ValueError: If inputs fail validation (e.g., out of range, invalid relationship).
    """

    # Validate inputs using Pydantic model
    validated_input = SlowDownPatternInput(
        canvas=canvas, mode_speed=mode_speed, desired_speed=desired_speed
    )

    # Distribute duplicates with integer math to avoid float precision issues.
    #
    # mode_speed / desired_speed = base_repeat + remainder / desired_speed
    #
    # We always repeat each row `base_repeat` times, then accumulate `remainder`.
    # Whenever accumulation reaches/exceeds `desired_speed`, we add one extra
    # duplicate for that row and subtract `desired_speed` from the accumulator.
    # This behaves like a Bresenham-style error accumulator.
    base_repeat = validated_input.mode_speed // validated_input.desired_speed
    remainder = validated_input.mode_speed % validated_input.desired_speed

    row_indices = []
    accumulator = 0

    for row_index in range(validated_input.canvas.shape[0]):
        repeat_count = base_repeat
        accumulator += remainder

        if accumulator >= validated_input.desired_speed:
            repeat_count += 1
            accumulator -= validated_input.desired_speed

        row_indices.extend([row_index] * repeat_count)

    return validated_input.canvas[row_indices]
