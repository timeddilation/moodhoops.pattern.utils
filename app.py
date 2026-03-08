"""Main application file for MoodHoops Pattern Utils web app."""

import dash
import dash_bootstrap_components as dbc  # type: ignore
from dash import dcc, html, callback, Input, Output

from webapp.utils import (
    create_upload_section,
    create_graph_section,
    create_message_section,
    create_swapcolors_mapping_row,
)

# Import callbacks to register them with the app
import webapp.home_callbacks  # noqa: F401
import webapp.slowdown_callbacks  # noqa: F401
import webapp.swapcolors_callbacks  # noqa: F401
import webapp.choreography_callbacks  # noqa: F401


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)

# Expose Flask server for WSGI deployment (gunicorn)
server = app.server


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
# Choreography Page
# ============================================================================
choreography_page = dbc.Container(
    [
        dcc.Store(
            id="choreography-timer-state",
            data={"running": False, "splits": ["00:00:000"], "startTime": None},
        ),
        dcc.Store(
            id="choreography-split-bmps",
            data={},
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Choreography Maker", className="mb-4 mt-4"),
                        html.P(
                            "Create timecoded splits for your MoodHoop choreography. "
                            "Upload BMP images for each split. "
                            "Then download a ZIP file containing all split images and a mhc choreo file with split timings. "
                            "Press the Start/Split button or space bar to record splits."
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
                            "Or upload an existing choreography:",
                            className="fw-bold mb-2",
                        ),
                        dcc.Upload(
                            id="choreography-upload-zip",
                            children=html.Div(
                                [
                                    "Drag and drop or ",
                                    html.A(",select a .zip file"),
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
                                "margin": "10px 0",
                            },
                            accept=".zip",
                        ),
                        html.Div(id="choreography-upload-message"),
                    ],
                    className="mb-4",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                html.Div(
                                    id="choreography-timer-display",
                                    children="00:00:000",
                                    style={
                                        "fontSize": "4rem",
                                        "fontWeight": "bold",
                                        "textAlign": "center",
                                        "fontFamily": "monospace",
                                        "padding": "30px",
                                        "marginBottom": "20px",
                                        "backgroundColor": "#f8f9fa",
                                        "borderRadius": "10px",
                                    },
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Button(
                                    "Start / Split (space)",
                                    id="choreography-start-split-btn",
                                    color="primary",
                                    size="lg",
                                    className="w-100",
                                ),
                            ],
                            className="mb-3",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Stop",
                                            id="choreography-stop-btn",
                                            color="danger",
                                            size="lg",
                                            className="w-100",
                                        ),
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Reset",
                                            id="choreography-reset-btn",
                                            color="secondary",
                                            outline=True,
                                            size="lg",
                                            className="w-100",
                                        ),
                                    ],
                                    width=6,
                                ),
                            ],
                            className="mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Button(
                                            "Download Choreo",
                                            id="choreography-download-btn",
                                            color="success",
                                            outline=True,
                                            size="lg",
                                            className="w-100",
                                        ),
                                        dcc.Download(id="choreography-download-zip"),
                                    ],
                                    width=12,
                                )
                            ],
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H4("Splits", className="mb-3"),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label(
                                        "Adjust All Split Times",
                                        className="fw-bold mb-2",
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dbc.Input(
                                                        id="choreography-time-adjustment",
                                                        type="number",
                                                        placeholder="Milliseconds (+/-)",
                                                        value=0,
                                                    ),
                                                ],
                                                width=8,
                                            ),
                                            dbc.Col(
                                                [
                                                    dbc.Button(
                                                        "Apply",
                                                        id="choreography-adjust-time-btn",
                                                        color="primary",
                                                        className="w-100",
                                                    ),
                                                ],
                                                width=4,
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        id="choreography-adjustment-message",
                                        className="mt-2",
                                    ),
                                ]
                            ),
                            className="mb-3",
                        ),
                        html.Div(id="choreography-splits-display"),
                    ],
                    width=9,
                ),
            ],
            className="mb-4",
        ),
    ],
    fluid=True,
)

# ============================================================================
# Main App Layout with Side Navigation
# ============================================================================
app.layout = dbc.Container(
    [
        dcc.Store(id="copied-hex-store"),
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
                                        dbc.NavLink(
                                            "Choreography",
                                            href="/choreography",
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
    elif pathname == "/choreography":
        return choreography_page
    else:
        return home_page


# ============================================================================
# Client-side: click pixel to clipboard
# ============================================================================
app.clientside_callback(
    """
    function(homeClickData, slowdownClickData, swapClickData) {
        const ctx = dash_clientside.callback_context;
        if (!ctx.triggered || ctx.triggered.length === 0) {
            return window.dash_clientside.no_update;
        }

        const triggeredProp = ctx.triggered[0].prop_id || "";
        let clickData = null;

        if (triggeredProp.startsWith("home-image-display")) {
            clickData = homeClickData;
        } else if (triggeredProp.startsWith("slowdown-image-display")) {
            clickData = slowdownClickData;
        } else if (triggeredProp.startsWith("swapcolors-image-display")) {
            clickData = swapClickData;
        }

        const hex = clickData?.points?.[0]?.customdata;
        if (!hex) {
            return window.dash_clientside.no_update;
        }

        if (navigator?.clipboard?.writeText) {
            navigator.clipboard.writeText(hex).catch(() => {});
        }

        return { hex: hex, copiedAt: Date.now() };
    }
    """,
    Output("copied-hex-store", "data"),
    Input("home-image-display", "clickData", allow_optional=True),
    Input("slowdown-image-display", "clickData", allow_optional=True),
    Input("swapcolors-image-display", "clickData", allow_optional=True),
    prevent_initial_call=True,
)


# ============================================================================
# Client-side: Timer display (runs completely in browser)
# ============================================================================
app.clientside_callback(
    """
    function(state) {
        if (!state) {
            return '00:00:000';
        }

        // If not running, show the last split time
        if (!state.running || state.startTime === null) {
            if (state.splits && state.splits.length > 0) {
                return state.splits[state.splits.length - 1];
            }
            return '00:00:000';
        }

        // Calculate elapsed time
        const elapsed = (Date.now() / 1000) - state.startTime;
        const minutes = Math.floor(elapsed / 60);
        const seconds = Math.floor(elapsed % 60);
        const milliseconds = Math.floor((elapsed % 1) * 1000);

        // Format as MM:SS:mmm
        const mm = String(minutes).padStart(2, '0');
        const ss = String(seconds).padStart(2, '0');
        const mmm = String(milliseconds).padStart(3, '0');

        return `${mm}:${ss}:${mmm}`;
    }
    """,
    Output("choreography-timer-display", "children"),
    Input("choreography-timer-state", "data"),
)


# ============================================================================
# Client-side: Space bar trigger for start/split
# ============================================================================
app.clientside_callback(
    """
    function(pathname) {
        // Remove any existing listener
        if (window.choreoSpaceHandler) {
            document.removeEventListener('keydown', window.choreoSpaceHandler);
        }

        // Only add listener when on choreography page
        if (pathname === '/choreography') {
            window.choreoSpaceHandler = function(event) {
                if (event.code === 'Space' &&
                    event.target.tagName !== 'INPUT' &&
                    event.target.tagName !== 'TEXTAREA') {
                    event.preventDefault();
                    const btn = document.getElementById('choreography-start-split-btn');
                    if (btn) btn.click();
                }
            };
            document.addEventListener('keydown', window.choreoSpaceHandler);
        }

        return window.dash_clientside.no_update;
    }
    """,
    Output("choreography-start-split-btn", "n_clicks", allow_duplicate=True),
    Input("url", "pathname"),
    prevent_initial_call=True,
)


# ============================================================================
# Client-side: Auto-refresh timer display when running
# ============================================================================
app.clientside_callback(
    """
    function(state) {
        // Clear any existing interval
        if (window.choreoTimerInterval) {
            clearInterval(window.choreoTimerInterval);
            window.choreoTimerInterval = null;
        }

        // If timer is running, set up interval to trigger state refresh
        if (state && state.running) {
            window.choreoTimerInterval = setInterval(function() {
                // Trigger a tiny state update to refresh display
                // This doesn't send data to server, just triggers the display callback
                const timerDisplay = document.getElementById('choreography-timer-display');
                if (timerDisplay && state.running && state.startTime) {
                    const elapsed = (Date.now() / 1000) - state.startTime;
                    const minutes = Math.floor(elapsed / 60);
                    const seconds = Math.floor(elapsed % 60);
                    const milliseconds = Math.floor((elapsed % 1) * 1000);
                    const mm = String(minutes).padStart(2, '0');
                    const ss = String(seconds).padStart(2, '0');
                    const mmm = String(milliseconds).padStart(3, '0');
                    timerDisplay.textContent = `${mm}:${ss}:${mmm}`;
                }
            }, 10);  // Update every 10ms, but purely client-side
        }

        return window.dash_clientside.no_update;
    }
    """,
    Output("choreography-timer-display", "style", allow_duplicate=True),
    Input("choreography-timer-state", "data"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run(debug=True)
