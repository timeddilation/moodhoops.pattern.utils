"""Callbacks for the Swap Colors page."""

import dash
from dash import callback, Input, Output, State, no_update, dcc, html, ALL
from PIL import Image
import numpy as np
import plotly.graph_objects as go  # type: ignore

from moodhoops.features.swap_colors import swap_colors
from webapp.utils import (
    create_pixel_perfect_figure,
    decode_upload_contents,
    create_swapcolors_mapping_row,
)


@callback(
    Output("swapcolors-mapping-rows", "children"),
    Output("swapcolors-mapping-count", "data"),
    Output("swapcolors-mapping-indices", "data"),
    Input("swapcolors-add-mapping-btn", "n_clicks"),
    Input({"type": "swapcolors-remove-mapping-btn", "index": ALL}, "n_clicks"),
    State("swapcolors-mapping-count", "data"),
    State("swapcolors-mapping-indices", "data"),
    State({"type": "swapcolors-from", "index": ALL}, "id"),
    State({"type": "swapcolors-from", "index": ALL}, "value"),
    State({"type": "swapcolors-to", "index": ALL}, "id"),
    State({"type": "swapcolors-to", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def add_swapcolors_mapping_row(
    add_clicks,
    remove_clicks,
    mapping_count,
    mapping_indices,
    from_ids,
    from_values,
    to_ids,
    to_values,
):
    """Add/remove swap-color mapping cards."""
    indices = list(mapping_indices or [0])
    triggered = dash.callback_context.triggered_id

    # Preserve currently typed values for existing mapping indices.
    from_by_index = {
        item["index"]: value
        for item, value in zip(from_ids or [], from_values or [])
        if isinstance(item, dict) and "index" in item
    }
    to_by_index = {
        item["index"]: value
        for item, value in zip(to_ids or [], to_values or [])
        if isinstance(item, dict) and "index" in item
    }

    if (
        isinstance(triggered, dict)
        and triggered.get("type") == "swapcolors-remove-mapping-btn"
    ):
        remove_index = triggered.get("index")
        indices = [idx for idx in indices if idx != remove_index]
    elif triggered == "swapcolors-add-mapping-btn":
        indices.append(mapping_count)
        mapping_count += 1

    rows = [
        create_swapcolors_mapping_row(
            idx,
            from_value=from_by_index.get(idx),
            to_value=to_by_index.get(idx),
        )
        for idx in indices
    ]
    return rows, mapping_count, indices


@callback(
    Output("swapcolors-image-display", "figure"),
    Output("swapcolors-output-message", "children"),
    Output("swapcolors-image-store", "data"),
    Output("swapcolors-original-image-store", "data"),
    Input("swapcolors-upload-image", "contents"),
    Input("swapcolors-apply-btn", "n_clicks"),
    State("swapcolors-image-store", "data"),
    State("swapcolors-original-image-store", "data"),
    State({"type": "swapcolors-from", "index": ALL}, "value"),
    State({"type": "swapcolors-to", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def swapcolors_update_image_display(
    contents,
    n_clicks,
    stored_image,
    original_stored_image,
    from_values,
    to_values,
):
    """Handle swap colors upload and apply actions."""
    triggered = dash.callback_context.triggered_id

    try:
        if triggered == "swapcolors-upload-image":
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

        if triggered == "swapcolors-apply-btn":
            if original_stored_image is None:
                error_message = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span("No image uploaded. Please upload an image first."),
                    ],
                    style={"color": "red"},
                )
                return (
                    go.Figure(),
                    error_message,
                    stored_image,
                    original_stored_image,
                )

            valid_mappings = []
            for from_color, to_color in zip(from_values or [], to_values or []):
                from_color = (from_color or "").strip()
                to_color = (to_color or "").strip()
                if from_color and to_color:
                    valid_mappings.append({"from": from_color, "to": to_color})

            if not valid_mappings:
                error_message = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span(
                            "Add at least one valid mapping with both From and To colors."
                        ),
                    ],
                    style={"color": "red"},
                )
                return (
                    go.Figure(),
                    error_message,
                    stored_image,
                    original_stored_image,
                )

            img_array = np.array(original_stored_image, dtype=np.uint8)
            result_array = swap_colors(img_array, valid_mappings)
            fig = create_pixel_perfect_figure(result_array)

            message = html.Div(
                [
                    html.Span("✓ ", style={"color": "green", "fontWeight": "bold"}),
                    html.Span(
                        f"Applied {len(valid_mappings)} color mapping(s). "
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
    Output("swapcolors-download-bmp", "data"),
    Input("swapcolors-download-btn", "n_clicks"),
    State("swapcolors-image-store", "data"),
    prevent_initial_call=True,
)
def download_swapcolors_image(n_clicks, stored_image):
    """Download the currently displayed swap colors image as a BMP file."""
    if not n_clicks or stored_image is None:
        return no_update

    img_array = np.array(stored_image, dtype=np.uint8)

    def write_bmp(bytes_io):
        Image.fromarray(img_array).save(bytes_io, format="BMP")

    return dcc.send_bytes(write_bmp, "swap_colors_pattern.bmp")
