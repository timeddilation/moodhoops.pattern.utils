"""Callbacks for the Slow Down Pattern page."""

import dash
from dash import callback, Input, Output, State, no_update, dcc, html
from PIL import Image
import numpy as np
import plotly.graph_objects as go  # type: ignore

from moodhoops.features.slow_down_pattern import slow_down_pattern
from webapp.utils import create_pixel_perfect_figure, decode_upload_contents


@callback(
    Output("slowdown-image-display", "figure"),
    Output("slowdown-output-message", "children"),
    Output("slowdown-image-store", "data"),
    Output("slowdown-original-image-store", "data"),
    Input("slowdown-upload-image", "contents"),
    Input("slowdown-apply-btn", "n_clicks"),
    State("slowdown-image-store", "data"),
    State("slowdown-original-image-store", "data"),
    State("slowdown-mode-speed", "value"),
    State("slowdown-desired-speed", "value"),
    prevent_initial_call=True,
)
def slowdown_update_image_display(
    contents,
    n_clicks,
    stored_image,
    original_stored_image,
    mode_speed,
    desired_speed,
):
    """Handle slow down pattern upload and apply actions."""
    triggered = dash.callback_context.triggered_id

    try:
        if triggered == "slowdown-upload-image":
            if contents is None:
                return go.Figure(), "", None, None

            img_array = decode_upload_contents(contents)
            fig = create_pixel_perfect_figure(img_array)

            message = html.Div(
                [
                    html.Span("✓ ", style={"color": "green", "fontWeight": "bold"}),
                    html.Span(
                        f"Image loaded: {img_array.shape[1]}×{img_array.shape[0]} pixels"
                    ),
                ]
            )

            image_data = img_array.tolist()
            return fig, message, image_data, image_data

        if triggered == "slowdown-apply-btn":
            if original_stored_image is None:
                error_message = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span("No image uploaded. Please upload an image first."),
                    ],
                    style={"color": "red"},
                )
                return go.Figure(), error_message, stored_image, original_stored_image

            # Always apply to the original uploaded image, not the currently displayed result
            img_array = np.array(original_stored_image, dtype=np.uint8)
            result_array = slow_down_pattern(img_array, mode_speed, desired_speed)
            fig = create_pixel_perfect_figure(result_array)

            message = html.Div(
                [
                    html.Span("✓ ", style={"color": "green", "fontWeight": "bold"}),
                    html.Span(
                        f"Applied slow down: {mode_speed}→{desired_speed} RPS. "
                        f"Result: {result_array.shape[1]}×{result_array.shape[0]} pixels"
                    ),
                ]
            )

            return fig, message, result_array.tolist(), original_stored_image

        return go.Figure(), "", stored_image, original_stored_image

    except ValueError as e:
        error_message = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span(f"Validation error: {str(e)}"),
            ],
            style={"color": "red"},
        )
        return go.Figure(), error_message, stored_image, original_stored_image

    except Exception as e:
        error_message = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span(f"Error: {str(e)}"),
            ],
            style={"color": "red"},
        )
        return go.Figure(), error_message, stored_image, original_stored_image


@callback(
    Output("slowdown-download-bmp", "data"),
    Input("slowdown-download-btn", "n_clicks"),
    State("slowdown-image-store", "data"),
    prevent_initial_call=True,
)
def download_slowdown_image(n_clicks, stored_image):
    """Download the currently displayed slow down image as a BMP file."""
    if not n_clicks or stored_image is None:
        return no_update

    img_array = np.array(stored_image, dtype=np.uint8)

    def write_bmp(bytes_io):
        Image.fromarray(img_array).save(bytes_io, format="BMP")

    return dcc.send_bytes(write_bmp, "slowdown_pattern.bmp")
