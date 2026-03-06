"""Callbacks for the Choreography page."""

import base64
import io
import time
import zipfile

import dash
import dash_bootstrap_components as dbc  # type: ignore
from dash import callback, Input, Output, State, no_update, dcc, html, ALL
from PIL import Image
import numpy as np

from webapp.utils import decode_upload_contents


@callback(
    Output("choreography-timer-state", "data", allow_duplicate=True),
    Output("choreography-adjustment-message", "children"),
    Input("choreography-adjust-time-btn", "n_clicks"),
    State("choreography-time-adjustment", "value"),
    State("choreography-timer-state", "data"),
    prevent_initial_call=True,
)
def choreography_adjust_times(n_clicks, adjustment_ms, state):
    """Adjust all split times by the specified milliseconds."""
    if not n_clicks or adjustment_ms is None:
        return no_update, ""

    try:
        adjustment_ms = int(adjustment_ms)
        if adjustment_ms == 0:
            return no_update, ""

        splits = state.get("splits", ["00:00:000"])

        if len(splits) <= 1:
            warning_msg = html.Div(
                [
                    html.Span("⚠ ", style={"color": "orange", "fontWeight": "bold"}),
                    html.Span("No splits to adjust."),
                ],
                style={"color": "orange"},
            )
            return no_update, warning_msg

        # Parse and adjust all splits except the first one
        new_splits = [splits[0]]  # Keep 00:00:000

        for split_time in splits[1:]:
            # Parse MM:SS:mmm
            parts = split_time.split(":")
            if len(parts) != 3:
                continue

            minutes = int(parts[0])
            seconds = int(parts[1])
            milliseconds = int(parts[2])

            # Convert to total milliseconds
            total_ms = (minutes * 60 * 1000) + (seconds * 1000) + milliseconds

            # Apply adjustment
            new_total_ms = total_ms + adjustment_ms

            # Ensure non-negative
            if new_total_ms < 0:
                new_total_ms = 0

            # Convert back to MM:SS:mmm
            new_minutes = new_total_ms // (60 * 1000)
            remainder = new_total_ms % (60 * 1000)
            new_seconds = remainder // 1000
            new_milliseconds = remainder % 1000

            new_split = f"{new_minutes:02d}:{new_seconds:02d}:{new_milliseconds:03d}"
            new_splits.append(new_split)

        # Update state
        new_state = {
            "running": state.get("running", False),
            "splits": new_splits,
            "startTime": state.get("startTime"),
        }

        direction = "forward" if adjustment_ms > 0 else "backward"
        success_msg = html.Div(
            [
                html.Span("✓ ", style={"color": "green", "fontWeight": "bold"}),
                html.Span(
                    f"Adjusted {len(new_splits) - 1} splits {direction} by {abs(adjustment_ms)}ms"
                ),
            ]
        )

        return new_state, success_msg

    except Exception as e:
        error_msg = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span(f"Error: {str(e)}"),
            ],
            style={"color": "red"},
        )
        return no_update, error_msg


@callback(
    Output("choreography-timer-state", "data"),
    Output("choreography-interval", "disabled"),
    Output("choreography-split-bmps", "data", allow_duplicate=True),
    Input("choreography-start-split-btn", "n_clicks"),
    Input("choreography-stop-btn", "n_clicks"),
    Input("choreography-reset-btn", "n_clicks"),
    State("choreography-timer-state", "data"),
    prevent_initial_call=True,
)
def choreography_control_timer(start_clicks, stop_clicks, reset_clicks, state):
    """Control the choreography timer (start/split/stop/reset)."""
    triggered = dash.callback_context.triggered_id

    if triggered == "choreography-reset-btn":
        return (
            {
                "running": False,
                "splits": ["00:00:000"],
                "startTime": None,
            },
            True,
            {},
        )

    if triggered == "choreography-start-split-btn":
        if not state["running"]:
            # Start the timer
            return (
                {
                    "running": True,
                    "splits": ["00:00:000"],
                    "startTime": time.time(),
                },
                False,
                no_update,
            )
        else:
            # Add a split
            elapsed = time.time() - state["startTime"]
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            milliseconds = int((elapsed % 1) * 1000)
            split_time = f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

            new_splits = state["splits"] + [split_time]
            return (
                {
                    "running": True,
                    "splits": new_splits,
                    "startTime": state["startTime"],
                },
                False,
                no_update,
            )

    if triggered == "choreography-stop-btn":
        return (
            {
                "running": False,
                "splits": state["splits"],
                "startTime": state["startTime"],
            },
            True,
            no_update,
        )

    return state, not state["running"], no_update


@callback(
    Output("choreography-timer-display", "children"),
    Input("choreography-interval", "n_intervals"),
    Input("choreography-timer-state", "data"),
)
def choreography_update_timer_display(n_intervals, state):
    """Update the timer display."""
    if not state["running"] or state["startTime"] is None:
        if state["splits"]:
            return state["splits"][-1]
        return "00:00:000"

    elapsed = time.time() - state["startTime"]
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    milliseconds = int((elapsed % 1) * 1000)

    return f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"


@callback(
    Output("choreography-splits-display", "children"),
    Input("choreography-timer-state", "data"),
    Input("choreography-split-bmps", "data"),
)
def choreography_display_splits(state, split_bmps):
    """Display all recorded splits in cards."""
    splits = state.get("splits", ["00:00:000"])
    split_bmps = split_bmps or {}

    cards = []
    for i, split_time in enumerate(splits):
        bmp_info = split_bmps.get(str(i))

        card_content = [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            f"Split {i + 1}",
                            className="fw-semibold text-muted",
                            style={"fontSize": "0.9rem"},
                        ),
                        width=4,
                    ),
                    dbc.Col(
                        html.Div(
                            split_time,
                            className="fw-bold",
                            style={
                                "fontSize": "1.2rem",
                                "fontFamily": "monospace",
                                "textAlign": "right",
                            },
                        ),
                        width=8,
                    ),
                ]
            ),
            html.Hr(className="my-2"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Upload(
                                id={"type": "choreography-upload-split", "index": i},
                                children=html.Div(
                                    [
                                        "Drag or ",
                                        html.A("select .bmp"),
                                    ]
                                ),
                                style={
                                    "width": "100%",
                                    "height": "40px",
                                    "lineHeight": "40px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "fontSize": "0.85rem",
                                },
                                accept=".bmp",
                            ),
                        ],
                        width=12,
                    )
                ],
                className="mb-2",
            ),
        ]

        if bmp_info:
            card_content.append(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.Span("✓ ", style={"color": "green"}),
                                        html.Span(
                                            f"{bmp_info['filename']} ({bmp_info['width']}×{bmp_info['height']})",
                                            style={"fontSize": "0.85rem"},
                                        ),
                                    ]
                                )
                            ],
                            width=12,
                        )
                    ]
                )
            )

        card = dbc.Card(
            dbc.CardBody(card_content),
            className="mb-2",
        )
        cards.append(card)

    return cards


@callback(
    Output("choreography-split-bmps", "data"),
    Input({"type": "choreography-upload-split", "index": ALL}, "contents"),
    Input({"type": "choreography-upload-split", "index": ALL}, "filename"),
    State({"type": "choreography-upload-split", "index": ALL}, "id"),
    State("choreography-split-bmps", "data"),
    prevent_initial_call=True,
)
def choreography_handle_split_uploads(
    contents_list, filenames_list, ids_list, split_bmps
):
    """Handle BMP file uploads for each split."""
    split_bmps = split_bmps or {}

    triggered = dash.callback_context.triggered_id
    if not triggered or not isinstance(triggered, dict):
        return split_bmps

    # Find which upload triggered
    split_index = triggered.get("index")
    if split_index is None:
        return split_bmps

    # Find the corresponding content and filename
    for upload_id, content, filename in zip(ids_list, contents_list, filenames_list):
        if upload_id["index"] == split_index and content:
            try:
                img_array = decode_upload_contents(content)
                split_bmps[str(split_index)] = {
                    "filename": filename,
                    "width": img_array.shape[1],
                    "height": img_array.shape[0],
                    "contents": content,
                }
                break
            except Exception:
                # If there's an error, just skip this upload
                pass

    return split_bmps


@callback(
    Output("choreography-timer-state", "data", allow_duplicate=True),
    Output("choreography-split-bmps", "data", allow_duplicate=True),
    Output("choreography-upload-message", "children"),
    Input("choreography-upload-zip", "contents"),
    State("choreography-upload-zip", "filename"),
    prevent_initial_call=True,
)
def choreography_upload_zip(contents, filename):
    """Upload and parse choreography zip file."""
    if not contents:
        return no_update, no_update, ""

    try:
        # Decode the uploaded file
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        zip_bytes = io.BytesIO(decoded)

        # Open and validate zip file
        with zipfile.ZipFile(zip_bytes, "r") as zf:
            file_list = zf.namelist()

            # Find .mhc and .bmp files
            mhc_files = [f for f in file_list if f.lower().endswith(".mhc")]
            bmp_files = [f for f in file_list if f.lower().endswith(".bmp")]
            other_files = [
                f
                for f in file_list
                if not f.lower().endswith(".mhc")
                and not f.lower().endswith(".bmp")
                and not f.endswith("/")
            ]

            # Validation
            if len(mhc_files) == 0:
                error_msg = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span("Error: No .mhc file found in zip."),
                    ],
                    style={"color": "red"},
                )
                return no_update, no_update, error_msg

            if len(mhc_files) > 1:
                error_msg = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span(
                            f"Error: Multiple .mhc files found. Expected 1, found {len(mhc_files)}."
                        ),
                    ],
                    style={"color": "red"},
                )
                return no_update, no_update, error_msg

            if len(bmp_files) == 0:
                error_msg = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span("Error: No .bmp files found in zip."),
                    ],
                    style={"color": "red"},
                )
                return no_update, no_update, error_msg

            if len(other_files) > 0:
                error_msg = html.Div(
                    [
                        html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                        html.Span(
                            f"Error: Invalid files found (only .mhc and .bmp allowed): {', '.join(other_files)}"
                        ),
                    ],
                    style={"color": "red"},
                )
                return no_update, no_update, error_msg

            # Read and parse .mhc file
            mhc_content = zf.read(mhc_files[0]).decode("utf-8")
            split_times = [
                line.strip() for line in mhc_content.strip().split("\n") if line.strip()
            ]

            # Add initial 00:00:000 split
            all_splits = ["00:00:000"] + split_times

            # Sort BMP files alphabetically
            bmp_files.sort()

            # Read BMP files and create split_bmps mapping
            split_bmps = {}
            for i, bmp_filename in enumerate(bmp_files):
                if i < len(
                    all_splits
                ):  # Only process BMPs if we have corresponding splits
                    bmp_data = zf.read(bmp_filename)

                    # Convert to base64 for storage (same format as upload)
                    bmp_base64 = base64.b64encode(bmp_data).decode("utf-8")
                    bmp_contents = f"data:image/bmp;base64,{bmp_base64}"

                    # Decode to get dimensions
                    img = Image.open(io.BytesIO(bmp_data)).convert("RGB")
                    img_array = np.array(img)

                    split_bmps[str(i)] = {
                        "filename": bmp_filename,
                        "width": img_array.shape[1],
                        "height": img_array.shape[0],
                        "contents": bmp_contents,
                    }

            # Create new timer state
            new_state = {
                "running": False,
                "splits": all_splits,
                "startTime": None,
            }

            success_msg = html.Div(
                [
                    html.Span("✓ ", style={"color": "green", "fontWeight": "bold"}),
                    html.Span(
                        f"Loaded choreography: {len(split_times)} splits, {len(bmp_files)} BMPs"
                    ),
                ]
            )

            return new_state, split_bmps, success_msg

    except zipfile.BadZipFile:
        error_msg = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span("Error: Invalid zip file."),
            ],
            style={"color": "red"},
        )
        return no_update, no_update, error_msg

    except Exception as e:
        error_msg = html.Div(
            [
                html.Span("✗ ", style={"color": "red", "fontWeight": "bold"}),
                html.Span(f"Error: {str(e)}"),
            ],
            style={"color": "red"},
        )
        return no_update, no_update, error_msg


@callback(
    Output("choreography-download-zip", "data"),
    Input("choreography-download-btn", "n_clicks"),
    State("choreography-timer-state", "data"),
    State("choreography-split-bmps", "data"),
    prevent_initial_call=True,
)
def choreography_download_zip(n_clicks, state, split_bmps):
    """Download choreography as a zip file with .mhc file and BMP files."""
    if not n_clicks:
        return no_update

    splits = state.get("splits", ["00:00:000"])
    split_bmps = split_bmps or {}

    def create_choreo_zip(bytes_io):
        with zipfile.ZipFile(bytes_io, "w", zipfile.ZIP_DEFLATED) as zf:
            # Create choreo.mhc file with splits (excluding the first 00:00:000)
            choreo_content = "\n".join(splits[1:])
            zf.writestr("choreo.mhc", choreo_content)

            # Add BMP files with zero-padded index names
            for i in range(len(splits)):
                bmp_info = split_bmps.get(str(i))
                if bmp_info and "contents" in bmp_info:
                    # Decode the BMP content
                    img_array = decode_upload_contents(bmp_info["contents"])

                    # Create BMP in memory
                    bmp_bytes = io.BytesIO()
                    Image.fromarray(img_array).save(bmp_bytes, format="BMP")
                    bmp_bytes.seek(0)

                    # Add to zip with zero-padded index name
                    filename = f"{i:03d}.bmp"
                    zf.writestr(filename, bmp_bytes.read())

    return dcc.send_bytes(create_choreo_zip, "choreography.zip")
