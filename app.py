import base64
import io

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State
import plotly.graph_objects as go
from PIL import Image
import numpy as np

from moodhoops.features.slow_down_pattern import slow_down_pattern
from moodhoops.features.swap_colors import swap_colors


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def create_upload_section(upload_id: str) -> dbc.Row:
    """Create a reusable file upload section."""
    return dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Upload(
                        id=upload_id,
                        children=html.Div(
                            [
                                "Drag and drop or ",
                                html.A("select a .bmp file"),
                            ]
                        ),
                        style={
                            "width": "100%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "margin": "10px",
                        },
                        accept=".bmp",
                    ),
                ],
                width=12,
            )
        ]
    )


def create_graph_section(graph_id: str) -> dbc.Row:
    """Create a reusable graph display section."""
    return dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Graph(
                        id=graph_id,
                        style={"height": "600px"},
                        config={"responsive": True, "staticPlot": False},
                    )
                ],
                width=12,
            )
        ]
    )


def create_message_section(message_id: str) -> dbc.Row:
    """Create a reusable message display section."""
    return dbc.Row(
        [
            dbc.Col(
                [html.Div(id=message_id, className="mt-3")],
                width=12,
            )
        ]
    )


# ============================================================================
# Home Page
# ============================================================================
home_page = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("BMP Pattern Viewer", className="mb-4 mt-4"),
                        html.P("Upload a .bmp file to preview your pattern."),
                    ],
                    width=12,
                )
            ]
        ),
        create_upload_section("home-upload-image"),
        create_message_section("home-output-message"),
        create_graph_section("home-image-display"),
    ],
    fluid=True,
)

# ============================================================================
# Slow Down Pattern Page
# ============================================================================
slowdown_page = dbc.Container(
    [
        dcc.Store(id="slowdown-image-store"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Slow Down Pattern", className="mb-4 mt-4"),
                        html.P(
                            "Upload a .bmp pattern and choose speeds to slow down your pattern."
                        ),
                    ],
                    width=12,
                )
            ]
        ),
        create_upload_section("slowdown-upload-image"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Mode Speed (1-500 RPS):", className="fw-bold"),
                        dbc.Input(
                            id="slowdown-mode-speed",
                            type="number",
                            placeholder="Current speed in RPS",
                            value=300,
                            min=1,
                            max=500,
                            className="mb-3",
                        ),
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        html.Label("Desired Speed (1-500 RPS):", className="fw-bold"),
                        dbc.Input(
                            id="slowdown-desired-speed",
                            type="number",
                            placeholder="Target speed in RPS",
                            value=200,
                            min=1,
                            max=500,
                            className="mb-3",
                        ),
                    ],
                    md=6,
                ),
            ],
            className="mt-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button(
                            "Apply Slow Down",
                            id="slowdown-apply-btn",
                            color="primary",
                            className="mt-2",
                        ),
                    ],
                    width=12,
                )
            ]
        ),
        create_message_section("slowdown-output-message"),
        create_graph_section("slowdown-image-display"),
    ],
    fluid=True,
)

# ============================================================================
# Swap Colors Page
# ============================================================================
swapcolors_page = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Swap Colors", className="mb-4 mt-4"),
                        html.P("Upload a .bmp pattern and swap colors."),
                    ],
                    width=12,
                )
            ]
        ),
        create_upload_section("swapcolors-upload-image"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            "Color swapping coming soon!",
                            className="text-muted",
                        ),
                    ],
                    width=12,
                )
            ]
        ),
        create_message_section("swapcolors-output-message"),
        create_graph_section("swapcolors-image-display"),
    ],
    fluid=True,
)

# ============================================================================
# Main App Layout with Side Navigation
# ============================================================================
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                # Side Navigation
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H4("MoodHoops Pattern Utils", className="mb-4"),
                                dbc.Nav(
                                    [
                                        dbc.NavLink(
                                            "Home",
                                            href="/",
                                            active="exact",
                                            className="nav-link-custom",
                                        ),
                                        dbc.NavLink(
                                            "Slow Down Pattern",
                                            href="/slow-down",
                                            active="exact",
                                            className="nav-link-custom",
                                        ),
                                        dbc.NavLink(
                                            "Swap Colors",
                                            href="/swap-colors",
                                            active="exact",
                                            className="nav-link-custom",
                                        ),
                                    ],
                                    vertical=True,
                                    pills=True,
                                    className="flex-column",
                                ),
                            ],
                            style={
                                "padding": "20px",
                                "backgroundColor": "#f8f9fa",
                                "height": "100vh",
                                "position": "sticky",
                                "top": "0",
                            },
                        )
                    ],
                    width=3,
                    style={"maxHeight": "100vh", "overflowY": "auto"},
                ),
                # Main Content
                dbc.Col(
                    [
                        dcc.Location(id="url", refresh=False),
                        html.Div(id="page-content"),
                    ],
                    width=9,
                ),
            ],
            style={"marginLeft": "0", "marginRight": "0"},
        ),
    ],
    fluid=True,
    style={"paddingLeft": "0", "paddingRight": "0"},
)


# ============================================================================
# Callback: Route pages
# ============================================================================
@callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    """Route to the appropriate page based on URL."""
    if pathname == "/slow-down":
        return slowdown_page
    elif pathname == "/swap-colors":
        return swapcolors_page
    else:
        return home_page


# ============================================================================
# Utility function for pixel-perfect image display
# ============================================================================
def create_pixel_perfect_figure(img_array: np.ndarray) -> go.Figure:
    """Create a Plotly figure with pixel-perfect image rendering."""
    fig = go.Figure(data=go.Image(z=img_array))
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode=False,
        dragmode=False,
    )
    return fig


def decode_upload_contents(contents: str) -> np.ndarray:
    """Decode uploaded file contents and return as numpy array."""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded)).convert("RGB")
    return np.array(image)


# ============================================================================
# Callback: Home page upload
# ============================================================================
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


# ============================================================================
# Callback: Slow Down Pattern upload
# ============================================================================
@callback(
    Output("slowdown-image-display", "figure"),
    Output("slowdown-output-message", "children"),
    Output("slowdown-image-store", "data"),
    Input("slowdown-upload-image", "contents"),
    Input("slowdown-apply-btn", "n_clicks"),
    State("slowdown-image-store", "data"),
    State("slowdown-mode-speed", "value"),
    State("slowdown-desired-speed", "value"),
    prevent_initial_call=True,
)
def slowdown_update_image_display(
    contents, n_clicks, stored_image, mode_speed, desired_speed
):
    """Handle slow down pattern upload and apply actions."""
    triggered = dash.callback_context.triggered_id

    try:
        if triggered == "slowdown-upload-image":
            if contents is None:
                return go.Figure(), "", None

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

            return fig, message, img_array.tolist()

        if triggered == "slowdown-apply-btn":
            if stored_image is None:
                error_message = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span("No image uploaded. Please upload an image first."),
                    ],
                    style={"color": "red"},
                )
                return go.Figure(), error_message, None

            img_array = np.array(stored_image, dtype=np.uint8)
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

            return fig, message, result_array.tolist()

        return go.Figure(), "", stored_image

    except ValueError as e:
        error_message = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span(f"Validation error: {str(e)}"),
            ],
            style={"color": "red"},
        )
        return go.Figure(), error_message, stored_image

    except Exception as e:
        error_message = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span(f"Error: {str(e)}"),
            ],
            style={"color": "red"},
        )
        return go.Figure(), error_message, stored_image


# ============================================================================
# Callback: Swap Colors upload
# ============================================================================
@callback(
    Output("swapcolors-image-display", "figure"),
    Output("swapcolors-output-message", "children"),
    Input("swapcolors-upload-image", "contents"),
    prevent_initial_call=True,
)
def swapcolors_update_image_display(contents):
    """Display uploaded BMP image for swap colors feature."""
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


if __name__ == "__main__":
    app.run(debug=True)
