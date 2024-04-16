import dash
from dash import html, Output, Input, State, callback, dcc, clientside_callback
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

spravka = """ ##### Описание программы:
`бла-бла-бла`

---

##### Использованная литература:
- Богданова, Е. С. Концепция инфокоммуникационной сети как основа разработки интегрированных логистических систем предприятия в условиях цифровой экономики / Е. С. Богданова, Д. Г. Неволин, З. Б. Хмельницкая. – Екатеринбург : Уральский государственный университет путей сообщения, 2022. – 140 с. – ISBN 978-5-94614-504-6. – EDN BOMBRR."""

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.ZEPHYR, dbc.icons.FONT_AWESOME],
    title="Логистический калькулятор",
    update_title="Обновляю...",
)

server = app.server
app.config.suppress_callback_exceptions = True

# components
header_buttons = dbc.ButtonGroup(
    [
        dbc.Button(
            html.Div("Логистическая схема предприятия", className='hide-text'),
            outline=True,
            id="open-flowchart",
            color="primary",
        ),
        dbc.Button(
            "Справка",
            outline=True,
            id="drawer-init",
            color="primary",
        ),
    ]
)

main_container = html.Div(
    children=[
        html.Div(id="notifications-container"),
        html.Div(id="notifications-container-2"),
        dbc.Navbar(
            [
                dmc.Grid(
                    [
                        dmc.Col(
                            html.A(
                                dbc.NavbarBrand("Логистический калькулятор", className="ms-2 h4"),
                                href="/",
                                style={"text-decoration": "unset"},
                            ),
                            span="content",
                        ),
                        dmc.Col(span="auto"),
                        dmc.Col(header_buttons, span="content"),
                        dmc.Col(
                            [
                                html.Span(
                                    [
                                        dbc.Label(className="fa fa-moon", html_for="color-mode-switch", color='primary'),
                                        dbc.Switch( id="color-mode-switch", value=True, className="d-inline-block ms-1", persistence=True),
                                        dbc.Label(className="fa fa-sun", html_for="color-mode-switch", color='primary'), 
                                    ]
                                )
                            ],
                            span="content",
                            className='d-flex align-items-center' 
                        ),
                    ],
                    className="header-grid",
                    gutter="xs",
                ),
            ],
            style={'min-height': '80px'},
            class_name='rounded border-bottom',
            color='default',
            # dark=True
        ),
        dmc.Space(h=10), 
        dash.page_container,
        dmc.Modal(
            title=html.H4("Интегрированная логистическая система предприятия"),
            id="modal-with-picture",
            size="70%",
            zIndex=10000,
            children=[
                dmc.Center(
                    children=[
                        dmc.Image(
                            src="/assets/flowchart.jpg", alt="flowchart", width="90%"
                        )
                    ]
                )
            ],
        ),
        dbc.Offcanvas(
            title=html.H4("Справка"),
            className='offcanvas-adaptive',
            style={'width': '55%'},
            id="drawer-help",
            children=[dcc.Markdown(spravka)],
        ),
    ],
    style={"padding": "0 10px 0 10px"},
)

app.layout = dmc.NotificationsProvider(main_container)


# callbacks
clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)

@callback(
    Output("modal-with-picture", "opened"),
    Input("open-flowchart", "n_clicks"),
    State("modal-with-picture", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(_, opened):
    return not opened


# drawer with help
@app.callback(
    Output("drawer-help", "is_open"),
    Input("drawer-init", "n_clicks"),
    [State("drawer-help", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


dev = False
if __name__ == "__main__":
    if dev: 
        app.run_server(debug=True, host="0.0.0.0", port=82)
    else: 
        from waitress import serve
        serve(app.server, host="0.0.0.0", port=82)
