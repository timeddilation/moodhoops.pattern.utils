"""Callbacks for the home page (pattern previewer)."""

from dash import callback, Input, Output, html
import plotly.graph_objects as go  # type: ignore

from webapp.utils import create_pixel_perfect_figure, decode_upload_contents


@callback(
    [Output("home-image-display", "figure"), Output("home-output-message", "children")],
    Input("home-upload-image", "contents"),
    prevent_initial_call=True,
)
def home_update_image_display(contents):
    """Display uploaded BMP image with pixel-perfect rendering."""
    if contents is None:
        return go.Figure(), ""

    try:
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

        return fig, message

    except Exception as e:
        error_message = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span(f"Error: {str(e)}"),
            ],
            style={"color": "red"},
        )
        return go.Figure(), error_message
