"""Utility functions for the web application."""

import base64
import io

import dash_bootstrap_components as dbc  # type: ignore
from dash import dcc, html
import plotly.graph_objects as go  # type: ignore
from PIL import Image
import numpy as np

from moodhoops.utils.colors import ints_to_hex


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


def create_pixel_perfect_figure(img_array: np.ndarray) -> go.Figure:
    """Create a Plotly figure with pixel-perfect image rendering."""
    hex_values = [[ints_to_hex(pixel.tolist()) for pixel in row] for row in img_array]

    fig = go.Figure(
        data=go.Image(
            z=img_array,
            customdata=hex_values,
            hovertemplate="x: %{x}<br>y: %{y}<br>hex: %{customdata}<extra></extra>",
        )
    )
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        hovermode="closest",
        dragmode=False,
    )
    return fig


def decode_upload_contents(contents: str) -> np.ndarray:
    """Decode uploaded file contents and return as numpy array."""
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded)).convert("RGB")
    return np.array(image)
