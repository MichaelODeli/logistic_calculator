import dash
from dash import html, Output, Input, State, callback, dcc, ALL, no_update
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import dash_bootstrap_components as dbc
from dash_extensions import Purify, Mermaid
from datetime import datetime, date

operations_counter_global = 0
allow_save_data_in_fields = False
time_dropdown_items = [
    {"label": "мес.", "value": "month"},
    {"label": "нед.", "value": "week"},
    {"label": "дн.", "value": "days"},
    {"label": "час", "value": "hour"},
]

spravka = """ ##### Описание программы:
`бла-бла-бла`

---

##### Использованная литература:
- Богданова, Е. С. Концепция инфокоммуникационной сети как основа разработки интегрированных логистических систем предприятия в условиях цифровой экономики / Е. С. Богданова, Д. Г. Неволин, З. Б. Хмельницкая. – Екатеринбург : Уральский государственный университет путей сообщения, 2022. – 140 с. – ISBN 978-5-94614-504-6. – EDN BOMBRR."""
# css styles
icons_link = (
    "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.2/font/bootstrap-icons.min.css"
)
app = dash.Dash(
    __name__,
    use_pages=False,
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


# function for generating Dash Iconify content
def get_icon(icon):
    """
    param:  \n
    `icon`: icon name
    """
    return dmc.ThemeIcon(
        DashIconify(icon=icon, width=18, color="var(--bs-primary)"),
        size=20,
        radius=20,
        variant="subtle",
    )


def get_hover(item, content, width=300):
    return dmc.HoverCard(
        withArrow=True,
        width=width,
        shadow="md",
        children=[
            dmc.HoverCardTarget(item),
            dmc.HoverCardDropdown(dcc.Markdown(content)),
        ],
    )


def get_header_with_help_icon(header_text, hover_text):
    return dmc.Center(
        dmc.Group(
            [
                html.H5(header_text),
                get_hover(get_icon("material-symbols:info-outline"), hover_text),
            ],
            spacing="xs",
        )
    )


def get_input_fields_in_table():
    table_row_1 = html.Tr(
        [
            html.Td(dmc.Text("Количество товаров")),
            html.Td(
                dbc.Input(
                    placeholder="Введите число",
                    id="productions_count",
                    type="number",
                    persistence=allow_save_data_in_fields,
                )
            ),
        ]
    )

    table_row_2 = html.Tr(
        [
            html.Td(dmc.Text("Количество этапов")),
            html.Td(
                dbc.Input(
                    placeholder="Введите число",
                    id="operations_count",
                    type="number",
                    persistence=allow_save_data_in_fields,
                ),
            ),
            html.Td(
                dbc.Button("Далее", id="operations_save_button"),
            ),
        ]
    )

    return html.Table(html.Tbody([table_row_1] + [table_row_2]))


line_1 = dmc.Stack(
    [
        html.H3("Переменные для расчета"),
        html.Div(
            [
                get_header_with_help_icon(
                    "Предварительные параметры",
                    "Поддерживается ввод только целых чисел",
                ),
                dcc.Store(id="productions_counter"),
                dcc.Store(id="operations_counter"),
                dmc.Space(h=10),
                get_input_fields_in_table(),
            ],
            className="input-block",
        ),
        html.Div(
            [
                get_header_with_help_icon(
                    "Настройка времени операций",
                    "",
                ),
                dmc.Space(h=10),
                html.Div(
                    children=[
                        html.Center(
                            Purify(
                                'В блоке выше введите необходимое количество операций<br>и нажмите кнопку "Далее"'
                            )
                        )
                    ],
                    id="times_block",
                ),
            ],
            className="input-block",
        ),
    ],
    align="center",
    spacing="xl",
)

line_2 = dmc.Stack(
    [
        html.H3("ㅤ"),
        html.Div(
            [
                get_header_with_help_icon(
                    "Настройка времени транспортировки",
                    "",
                ),
                dmc.Space(h=10),
                html.Div(
                    html.Center(
                        Purify(
                            'В блоке слева введите необходимое количество операций<br>и нажмите кнопку "Далее"'
                        )
                    ),
                    id="div-transport-time",
                ),
            ],
            className="input-block",
        ),
    ],
    align="center",
    spacing="xl",
)

line_3 = dmc.Stack(
    [
        html.H3("Результаты расчетов"),
        html.Div(
            id="test_output",
            className="input-block",
        ),
    ],
    align="center",
    spacing="xl",
)

main_container = html.Div(
    children=[
        html.Div(id="notifications-container"),
        html.Div(id="notifications-container-2"),
        dmc.Header(
            [
                dmc.Grid(
                    [
                        dmc.Col(html.H4("Логистический калькулятор"), span="content"),
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
        dmc.Grid(
            children=[
                dmc.Col(html.Div(line_1), span=4, className="block-col"),
                dmc.Col(html.Div(line_2), span=3, className="block-col"),
                dmc.Col(html.Div(line_3), span=5, className="block-col"),
            ],
            gutter="xl",
            className="block-grid",
        ),
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
            children=[
                dcc.Markdown(spravka)
            ],
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


# drawer with help
@callback(
    [
        Output("operations_count", "value"),
        Output("productions_count", "value"),
        Output({"type": "operation_time_input", "index": ALL}, "value"),
        Output({"type": "operation_time_timetype", "index": ALL}, "value"),
    ],
    Input("fields-reset", "n_clicks"),
    State({"type": "operation_time_input", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def clear_all_fields(n_clicks, counter):
    return [None, None, [None] * len(counter), ["days"] * len(counter)]


@callback(
    [
        Output("times_block", "children"),
        Output("div-transport-time", "children"),
        Output("operations_counter", "data"),
        Output("productions_counter", "data"),
        Output("notifications-container", "children"),
    ],
    Input("operations_save_button", "n_clicks"),
    [
        State("operations_count", "value"),
        State("productions_count", "value"),
        State({"type": "operation_time_input", "index": ALL}, "value"),
        State({"type": "operation_time_timetype", "index": ALL}, "value"),
    ],
    prevent_initial_call=True,
)
def make_inputs(
    n_clicks,
    operations_count,
    productions_count,
    operation_time_input,
    operation_time_timetype,
):
    fault_notif = dmc.Notification(
        title="Ошибка ввода данных",
        id="simple-notify",
        action="show",
        message="Вы ввели данные не во все ячейки. Повторите ввод.",
        icon=DashIconify(icon="material-symbols:error-outline"),
        color="red",
    )
    if operations_count == None or productions_count == None:
        return no_update, no_update, no_update, no_update, fault_notif

    global operations_counter_global
    global time_dropdown_items
    operations_counter_global = operations_count

    # transport time block
    tr_block = dmc.Timeline(
        active=operations_count,
        bulletSize=20,
        lineWidth=2,
        children=[
            dmc.TimelineItem(
                title=f"Операция {cnt+1}",
                color="gray.7",
                children=dmc.Stack(
                    [
                        dbc.InputGroup(
                            [
                                dbc.InputGroupText(
                                    f"Время транспортировки до пункта {cnt+1}",
                                    style={'font-size': '14px'}
                                ),
                                dbc.Input(
                                    # placeholder=f"Время транспортировки до пункта {cnt+1}",
                                    id={"type": "transport_time", "index": cnt + 1},
                                    type="number",
                                ),
                                dbc.InputGroupText("дн."),
                            ]
                        ),
                        dmc.Group(
                            [
                                "Значимость",
                                dmc.Slider(
                                    min=0,
                                    max=100,
                                    value=100,
                                    step=5,
                                    style={"width": "70%", "margin-bottom": "15px"},
                                    marks=[
                                        {"value": 20, "label": "20%"},
                                        {"value": 50, "label": "50%"},
                                        {"value": 80, "label": "80%"},
                                    ],
                                    id={
                                        "type": "transport_time_important",
                                        "index": cnt + 1,
                                    },
                                    color="gray.7",
                                ),
                            ]
                        ),
                    ]
                ),
            )
            for cnt in range(int(operations_count))
        ],
    )

    # operations time block

    if operations_count < len(operation_time_input):
        operation_time_input = operation_time_input[:operations_count]
        operation_time_timetype = operation_time_timetype[:operations_count]
    else:
        operation_time_input += [None] * (operations_count - len(operation_time_input))
        operation_time_timetype += ["days"] * (
            operations_count - len(operation_time_timetype)
        )
    sk = "{"
    ks = "}"

    tbl_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("№"),
                    html.Th("Одновременных операций"),
                    html.Th("Время 1 операции"),
                    html.Th("Тип времени"),
                ]
            )
        )
    ]
    inputs_list = [
        html.Tr(
            [
                html.Td(str(i + 1)),
                html.Td(
                    dbc.Input(
                        placeholder=f"Одновременных операций",
                        id={"type": "operation_time_lines", "index": i + 1},
                        value="1",
                        type="number",
                        persistence=allow_save_data_in_fields,
                        style={"text-align": "center"},
                        disabled=True,
                    ),
                ),
                html.Td(
                    dbc.Input(
                        placeholder=f"t({str(i+1)})",
                        id={"type": "operation_time_input", "index": i + 1},
                        value=operation_time_input[i],
                        type="number",
                        persistence=allow_save_data_in_fields,
                        style={"text-align": "center"},
                    ),
                ),
                html.Td(
                    dbc.Select(
                        placeholder="Тип введенного времени",
                        id={"type": "operation_time_timetype", "index": i + 1},
                        options=time_dropdown_items,
                        value=operation_time_timetype[i],
                    )
                ),
            ]
        )
        for i in range(int(operations_count))
    ]
    send_button = dbc.Button("Рассчитать", id="make_calc")

    return (
        dmc.Stack([html.Table(tbl_header + inputs_list), send_button]),
        tr_block,
        str(operations_count),
        str(productions_count),
        None,
    )


@callback(
    [
        Output("test_output", "children"),
        Output("make_calc", "n_clicks"),
        Output("notifications-container-2", "children"),
    ],
    Input("make_calc", "n_clicks"),
    [
        State({"type": "operation_time_input", "index": ALL}, "value"),
        State({"type": "operation_time_timetype", "index": ALL}, "value"),
        State({"type": "operation_time_lines", "index": ALL}, "value"),
        State({"type": "transport_time", "index": ALL}, "value"),
        State({"type": "transport_time_important", "index": ALL}, "value"),
        State("productions_counter", "data"),
        State("test_output", "children"),
    ],
    prevent_initial_call=True,
)
def calculate(
    n_clicks,
    operation_time_input,
    operation_time_timetype,
    operation_time_lines,
    transport_time,
    transport_time_important,
    productions_counter,
    children,
):
    fault_notif = dmc.Notification(
        title="Ошибка расчета",
        id="simple-notify",
        action="show",
        message="Вы ввели время не во все ячейки. Повторите ввод.",
        icon=DashIconify(icon="material-symbols:error-outline"),
        color="red",
    )

    if n_clicks is None:
        return None, None, None
    # elif None in operation_time_input or None in operation_time_lines or None in transport_time:
    elif None in operation_time_input or None in operation_time_lines:
        return None, None, fault_notif
    else:
        productions_count = float(productions_counter)
        source_data = [
            dcc.Markdown("##### Длительность основного технологического цикла"),
            dcc.Markdown("**Исходные данные**"),
        ]
        proc_time = []
        proc_time_str = []
        for process_time, process_timeprefix, process_lines, i in zip(
            operation_time_input,
            operation_time_timetype,
            operation_time_lines,
            range(len(operation_time_input)),
        ):
            if process_timeprefix == "days":
                process_time_conv = float(process_time)
                process_timeprefix = "дн."
            elif process_timeprefix == "week":
                process_time_conv = float(process_time) * 7
                process_timeprefix = "нед."
            elif process_timeprefix == "month":
                process_time_conv = float(process_time) * 30
                process_timeprefix = "мес."
            elif process_timeprefix == "hour":
                process_time_conv = round(float(process_time) / 24, 2)
                process_timeprefix = "час."
            else:
                process_time_conv = None
            source_data.append(
                dcc.Markdown(
                    (
                        f"$$t_{i+1} = {process_time}~({process_timeprefix}) = {str(process_time_conv)}~(дн.)$$"
                        if process_timeprefix != "дн."
                        else f"$$t_{i+1} = {str(process_time_conv)}~(дн.)$$"
                    ),
                    mathjax=True,
                )
            )
            proc_time.append(float(process_time_conv))
            proc_time_str.append(str(process_time_conv))

        posl_value = sum(proc_time) * productions_count
        posl_data = [
            dcc.Markdown("**Последовательный метод**"),
            dcc.Markdown(
                f'$$t_{"{посл}"} = ({" + ".join(proc_time_str)})*{str(productions_count)} = {str(posl_value)}~(дн.)$$',
                mathjax=True,
            ),
        ]

        paral_value = sum(proc_time) + ((productions_count - 1) * max(proc_time))
        paral_data = [
            dcc.Markdown("**Параллельный метод**"),
            dcc.Markdown(
                [
                    f'$t_{"{парал}"} = ({" + ".join(proc_time_str)})+$\n',
                    f"$+({str(productions_count)}-1)*{str(max(proc_time_str))} = {str(paral_value)}~(дн.)$",
                ],
                mathjax=True,
            ),
        ]

        time_divider = [
            dmc.Divider(
                variant="solid",
                label=datetime.now().strftime("%d/%b/%Y %H:%M:%S"),
                labelPosition="center",
            )
        ]

        results = dmc.Stack(
            time_divider
            + source_data
            + [dmc.Space(h=10)]
            + posl_data
            + [dmc.Space(h=10)]
            + paral_data,
            spacing=0,
        )

        if children is None:
            children = []
        children.append(results)
        return children, None, None
        # return results, None, None


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=82)
