import base64
import io

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Input, Output, State, no_update, ALL
import plotly.graph_objects as go
from PIL import Image
import numpy as np

from moodhoops.features.slow_down_pattern import slow_down_pattern
from moodhoops.features.swap_colors import swap_colors


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)


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


def create_swapcolors_mapping_row(
    index: int,
    from_value: str | None = None,
    to_value: str | None = None,
) -> dbc.Card:
    """Create one swap-color mapping card with from/to inputs."""
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                f"Mapping {index + 1}",
                                className="fw-semibold text-muted mb-2",
                                style={"fontSize": "0.85rem"},
                            ),
                            width=9,
                        ),
                        dbc.Col(
                            dbc.Button(
                                "✕",
                                id={
                                    "type": "swapcolors-remove-mapping-btn",
                                    "index": index,
                                },
                                color="light",
                                size="sm",
                                title="Remove mapping",
                                className="py-0 px-2",
                            ),
                            width=3,
                            className="text-end",
                        ),
                    ],
                    align="start",
                ),
                dbc.Label("From", className="mb-1"),
                dbc.Input(
                    id={"type": "swapcolors-from", "index": index},
                    type="text",
                    placeholder="#RRGGBB",
                    value=from_value,
                    className="mb-2",
                ),
                dbc.Label("To", className="mb-1"),
                dbc.Input(
                    id={"type": "swapcolors-to", "index": index},
                    type="text",
                    placeholder="#RRGGBB",
                    value=to_value,
                ),
            ]
        ),
        className="mb-2",
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
        dcc.Store(id="slowdown-original-image-store"),
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        create_upload_section("slowdown-upload-image"),
                        create_message_section("slowdown-output-message"),
                        create_graph_section("slowdown-image-display"),
                    ],
                    width=10,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Apply Slow Down",
                                            id="slowdown-apply-btn",
                                            color="primary",
                                            className="w-100",
                                        ),
                                    ],
                                    width=12,
                                )
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Download BMP",
                                            id="slowdown-download-btn",
                                            color="secondary",
                                            outline=True,
                                            className="w-100",
                                        ),
                                        dcc.Download(id="slowdown-download-bmp"),
                                    ],
                                    width=12,
                                )
                            ],
                            className="mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Mode Speed (1-500 RPS):",
                                            className="fw-bold",
                                        ),
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
                                    width=12,
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Desired Speed (1-500 RPS):",
                                            className="fw-bold",
                                        ),
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
                                    width=12,
                                )
                            ]
                        ),
                    ],
                    width=2,
                ),
            ],
            className="mt-3",
        ),
    ],
    fluid=True,
)

# ============================================================================
# Swap Colors Page
# ============================================================================
swapcolors_page = dbc.Container(
    [
        dcc.Store(id="swapcolors-image-store"),
        dcc.Store(id="swapcolors-original-image-store"),
        dcc.Store(id="swapcolors-mapping-count", data=1),
        dcc.Store(id="swapcolors-mapping-indices", data=[0]),
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        create_upload_section("swapcolors-upload-image"),
                        create_message_section("swapcolors-output-message"),
                        create_graph_section("swapcolors-image-display"),
                    ],
                    width=10,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Apply Swap",
                                            id="swapcolors-apply-btn",
                                            color="primary",
                                            className="w-100",
                                        ),
                                    ],
                                    width=12,
                                )
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Download BMP",
                                            id="swapcolors-download-btn",
                                            color="secondary",
                                            outline=True,
                                            className="w-100",
                                        ),
                                        dcc.Download(id="swapcolors-download-bmp"),
                                    ],
                                    width=12,
                                )
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label(
                                            "Color Mappings", className="fw-bold"
                                        ),
                                        html.Div(
                                            id="swapcolors-mapping-rows",
                                            children=[
                                                create_swapcolors_mapping_row(0),
                                            ],
                                        ),
                                        dbc.Button(
                                            "Add Mapping",
                                            id="swapcolors-add-mapping-btn",
                                            color="light",
                                            className="w-100 mt-2",
                                        ),
                                    ],
                                    width=12,
                                )
                            ]
                        ),
                    ],
                    width=2,
                ),
            ],
            className="mt-3",
        ),
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
                                            "Pattern Previewer",
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


# ============================================================================
# Callback: Swap Colors mapping rows
# ============================================================================
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


# ============================================================================
# Callback: Swap Colors upload/apply
# ============================================================================
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


# ============================================================================
# Callback: Slow Down Pattern download
# ============================================================================
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


# ============================================================================
# Callback: Swap Colors download
# ============================================================================
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


if __name__ == "__main__":
    app.run(debug=True)
