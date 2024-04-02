import dash
from dash import html, Output, Input, State, callback, dcc
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

spravka = """ ##### Описание программы:
`бла-бла-бла`

---

##### Использованная литература:
- Богданова, Е. С. Концепция инфокоммуникационной сети как основа разработки интегрированных логистических систем предприятия в условиях цифровой экономики / Е. С. Богданова, Д. Г. Неволин, З. Б. Хмельницкая. – Екатеринбург : Уральский государственный университет путей сообщения, 2022. – 140 с. – ISBN 978-5-94614-504-6. – EDN BOMBRR."""
# css styles

app = dash.Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Логистический калькулятор",
    update_title="Обновляю...",
)

server = app.server
app.config.suppress_callback_exceptions = True

# components
header_buttons = dbc.ButtonGroup(
    [
        dbc.Button(
            "Открыть логистическую схему предприятия",
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
        dbc.Button(
            "Сбросить все поля",
            outline=True,
            color="danger",
            id="fields-reset",
            # disabled=True,
            # href='/'
        ),
    ]
)

main_container = html.Div(
    children=[
        html.Div(id="notifications-container"),
        html.Div(id="notifications-container-2"),
        dmc.Header(
            [
                dmc.Grid(
                    [
                        dmc.Col(
                            html.A(
                                "Логистический калькулятор",
                                href="/",
                                style={"text-decoration": "unset"},
                                className="h4",
                            ),
                            span="content",
                        ),
                        dmc.Col(span="auto"),
                        dmc.Col(header_buttons, span="content"),
                    ],
                    className="header-grid",
                    gutter="xs",
                ),
            ],
            fixed=True,
            height=65,
        ),
        dmc.Space(h=65),
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
        dmc.Drawer(
            title=html.H4("Справка"),
            size="55%",
            id="drawer-help",
            padding="md",
            zIndex=10000,
            children=[dcc.Markdown(spravka)],
        ),
    ],
    style={"padding": "10px"},
)

app.layout = dmc.NotificationsProvider(main_container)


# callbacks
@callback(
    Output("modal-with-picture", "opened"),
    Input("open-flowchart", "n_clicks"),
    State("modal-with-picture", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(_, opened):
    return not opened


# drawer with help
@callback(
    Output("drawer-help", "opened"),
    Input("drawer-init", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_show(_):
    return True


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=82)
