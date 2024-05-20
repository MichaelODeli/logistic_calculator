from dash import (
    dcc,
    html,
    Input,
    Output,
    callback,
    register_page,
    State,
    Input,
    Output,
    no_update,
    ALL,
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from datetime import datetime
from dash_extensions import Purify
from controllers import main_controller as m_c
from random import randint
import networkx as nx
import matplotlib
import matplotlib.pyplot
import io
import base64

register_page(
    __name__, path="/by_time", icon="fa-solid:home", name="Время | Логист. калькулятор"
)

operations_counter_global = 0
transportways_count_global = 0
allow_save_data_in_fields = False
demo_data = True
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


def time_recalculate(time, products, line_type, parallel_works):
    if line_type == "p-p" or line_type == "paral":
        return round((products - 1) * time / parallel_works + time / parallel_works, 2)
    if line_type == "posl":
        return round(time * products / parallel_works, 2)


def get_input_fields_in_table(allow_save_data_in_fields):
    global demo_data
    table_row_1 = html.Tr(
        [
            html.Td(dmc.Text("Количество товаров")),
            html.Td(
                dbc.Input(
                    placeholder="Введите число",
                    id="products_count",
                    type="number",
                    persistence=allow_save_data_in_fields,
                    value=5 if demo_data else None,
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
                    value=6 if demo_data else None,
                ),
            ),
        ]
    )

    table_row_3 = html.Tr(
        [
            html.Td(dmc.Text("Количество путей перевозки")),
            html.Td(
                dbc.Input(
                    placeholder="Введите число",
                    id="transportways_count",
                    type="number",
                    persistence=allow_save_data_in_fields,
                    value=5 if demo_data else None,
                ),
            ),
            html.Td(
                dbc.Button("Далее", id="operations_save_button"),
            ),
        ]
    )

    return html.Table(html.Tbody([table_row_1] + [table_row_2] + [table_row_3]))


def layout():
    line_1 = dmc.Stack(
        [
            html.H3("Переменные для расчета"),
            html.Div(
                [
                    m_c.get_header_with_help_icon(
                        "Предварительные параметры",
                        "Поддерживается ввод только целых чисел",
                    ),
                    dcc.Store(id="productions_counter"),
                    dcc.Store(id="operations_counter"),
                    dmc.Space(h=10),
                    get_input_fields_in_table(allow_save_data_in_fields),
                ],
                className="input-block",
            ),
            html.Div(
                [
                    m_c.get_header_with_help_icon(
                        "Настройка времени операций",
                        "Для сложного производства требуется дополнительно указать тип отдельного производства и время транспортировки грузов между этапами.",
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
                    m_c.get_header_with_help_icon(
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
                id="calc_output",
                className="input-block",
                children=[
                    html.Center(
                        Purify(
                            'В блоках слева введите требуемые данные<br>и нажмите кнопку "Рассчитать"'
                        ),
                        className="cube",
                    ),
                ],
            ),
        ],
        align="center",
        spacing="xl",
    )

    content = (
        dmc.Grid(
            children=[
                dmc.Col(html.Div(line_1), span=4, className="block-col"),
                dmc.Col(html.Div(line_2), span=4, className="block-col"),
                dmc.Col(html.Div(line_3), span=4, className="block-col"),
            ],
            gutter="xl",
            className="block-grid",
        ),
    )
    return content


@callback(
    [
        Output("operations_count", "value"),
        Output("products_count", "value"),
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
        State({"type": "parallel_operations", "index": ALL}, "value"),
        State("products_count", "value"),
        State("transportways_count", "value"),
        State({"type": "operation_time_input", "index": ALL}, "value"),
        State({"type": "operation_time_timetype", "index": ALL}, "value"),
        State({"type": "from_point", "index": ALL}, "value"),
        State({"type": "to_point", "index": ALL}, "value"),
        State({"type": "time_between_points", "index": ALL}, "value"),
        State({"type": "delivery_type", "index": ALL}, "value"),
        State({"type": "parallel_delivery", "index": ALL}, "value"),
        State({"type": "production_type", "index": ALL}, "value"),
    ],
    prevent_initial_call=True,
)
def make_inputs(
    n_clicks,
    operations_count,
    parallel_operations,
    products_count,
    transportways_count,
    operation_time_input,
    operation_time_timetype,
    from_point,
    to_point,
    time_between_points,
    delivery_type,
    parallel_delivery,
    production_type,
):
    if n_clicks == None:
        return [no_update] * 5
    fault_notif = dmc.Notification(
        title="Ошибка ввода данных",
        id="simple-notify",
        action="show",
        message="Вы ввели данные не во все ячейки. Повторите ввод.",
        icon=DashIconify(icon="material-symbols:error-outline"),
        color="red",
    )
    if (
        operations_count == None
        or products_count == None
        or transportways_count == None
    ):
        return no_update, no_update, no_update, no_update, fault_notif

    global operations_counter_global
    global time_dropdown_items
    global transportways_count_global
    global demo_data
    operations_counter_global = operations_count
    transportways_count_global = transportways_count

    if demo_data:
        from_point = [i + 1 for i in range(transportways_count)]
        to_point = [i + 2 for i in range(transportways_count)]
        time_between_points = [randint(1, 7) for i in range(transportways_count)]
        delivery_type = [
            ["paral", "posl", "p-p"][randint(0, 2)] for i in range(transportways_count)
        ]
        parallel_delivery = [randint(1, 3) for i in range(transportways_count)]
    else:
        if transportways_count < len(from_point):
            pass
        else:
            from_point += [None] * (transportways_count - len(from_point))
            to_point += [None] * (transportways_count - len(to_point))
            time_between_points += [None] * (
                transportways_count - len(time_between_points)
            )
            delivery_type += [None] * (transportways_count - len(delivery_type))

    tr_tbl_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("№"),
                    html.Th("Начальный пункт"),
                    html.Th("Конечный пункт"),
                    html.Th("Время перевозки (дн.)"),
                    html.Th("Тип перевозки"),
                    html.Th("Одновр. перевозок"),
                ]
            )
        )
    ]
    tr_inputs_list = [
        html.Tr(
            [
                html.Td(str(i + 1)),
                html.Td(
                    dbc.Select(
                        placeholder="Откуда",
                        id={"type": "from_point", "index": i + 1},
                        options=[
                            {"label": j + 1, "value": j + 1}
                            for j in range(int(operations_count))
                        ],
                        className="custom-back-color",
                        value=from_point[i],
                    )
                ),
                html.Td(
                    dbc.Select(
                        placeholder="Куда",
                        id={"type": "to_point", "index": i + 1},
                        options=[
                            {"label": j + 1, "value": j + 1}
                            for j in range(int(operations_count))
                        ],
                        className="custom-back-color",
                        value=to_point[i],
                    )
                ),
                html.Td(
                    dbc.Input(
                        placeholder=f"Время",
                        id={"type": "time_between_points", "index": i + 1},
                        type="number",
                        style={"text-align": "center"},
                        value=time_between_points[i],
                    ),
                ),
                html.Td(
                    dbc.Select(
                        placeholder="Тип перевозки",
                        id={"type": "delivery_type", "index": i + 1},
                        options=[
                            {"label": "парал.", "value": "paral"},
                            {"label": "посл.", "value": "posl"},
                            {"label": "п.-п.", "value": "p-p"},
                        ],
                        className="custom-back-color",
                        value=delivery_type[i],
                    )
                ),
                html.Td(
                    dbc.Input(
                        placeholder=f"Одновр. перевозок",
                        id={"type": "parallel_delivery", "index": i + 1},
                        type="number",
                        style={"text-align": "center"},
                        value=parallel_delivery[i],
                    ),
                ),
            ]
        )
        for i in range(int(transportways_count))
    ]

    # operations time block
    if demo_data:
        operation_time_input = [randint(1, 7) for i in range(operations_count)]
        operation_time_timetype = ["days" for i in range(operations_count)]
        production_type = [
            ["paral", "posl", "p-p"][randint(0, 2)] for i in range(operations_count)
        ]
        parallel_operations = [randint(1, 3) for i in range(operations_count)]
    else:
        if operations_count < len(operation_time_input):
            operation_time_input = operation_time_input[:operations_count]
            operation_time_timetype = operation_time_timetype[:operations_count]
        else:
            operation_time_input += [None] * (
                operations_count - len(operation_time_input)
            )
            operation_time_timetype += ["days"] * (
                operations_count - len(operation_time_timetype)
            )
            production_type += ["posl"] * (operations_count - len(production_type))
            parallel_operations += [None] * (
                operations_count - len(parallel_operations)
            )

    tbl_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th("№"),
                    html.Th("Одновр. операций"),
                    html.Th("Время 1 операции"),
                    html.Th("Тип производства"),
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
                        id={"type": "parallel_operations", "index": i + 1},
                        value=parallel_operations[i],
                        type="number",
                        persistence=allow_save_data_in_fields,
                        style={"text-align": "center"},
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
                        placeholder="Тип производства",
                        id={"type": "production_type", "index": i + 1},
                        options=[
                            {"label": "парал.", "value": "paral"},
                            {"label": "посл.", "value": "posl"},
                            {"label": "п.-п.", "value": "p-p"},
                        ],
                        className="custom-back-color",
                        value=production_type[i],
                    )
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
    send_button = dbc.Button(
        "Рассчитать простое производство", id="make_calc", class_name="btn_calc"
    )
    send_2_button = dbc.Button(
        "Рассчитать сложное производство", id="make_calc_hard", class_name="btn_calc"
    )

    return (
        dmc.Stack([html.Table(tbl_header + inputs_list), send_button, send_2_button]),
        html.Table(tr_tbl_header + tr_inputs_list),
        str(operations_count),
        str(products_count),
        no_update,
    )


@callback(
    [
        Output("calc_output", "children", allow_duplicate=True),
        Output("make_calc", "n_clicks"),
        Output("notifications-container-2", "children"),
    ],
    Input("make_calc", "n_clicks"),
    [
        State({"type": "operation_time_input", "index": ALL}, "value"),
        State({"type": "operation_time_timetype", "index": ALL}, "value"),
        State({"type": "parallel_operations", "index": ALL}, "value"),
        State({"type": "transport_time", "index": ALL}, "value"),
        State({"type": "transport_time_important", "index": ALL}, "value"),
        State("productions_counter", "data"),
        State("calc_output", "children"),
    ],
    prevent_initial_call=True,
)
def calculate(
    n_clicks,
    operation_time_input,
    operation_time_timetype,
    parallel_operations,
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
        return no_update, None, None
    # elif None in operation_time_input or None in parallel_operations or None in transport_time:
    elif None in operation_time_input or None in parallel_operations:
        return None, None, fault_notif
    else:
        products_count = float(productions_counter)
        source_data = [
            dcc.Markdown("##### Длительность основного технологического цикла"),
            dcc.Markdown("**Исходные данные**"),
        ]
        proc_time = []
        proc_time_str = []
        for process_time, process_timeprefix, process_lines, i in zip(
            operation_time_input,
            operation_time_timetype,
            parallel_operations,
            range(len(operation_time_input)),
        ):
            match process_timeprefix:
                case "days":
                    process_time_conv = int(process_time)
                    process_timeprefix = "дн."
                case "week":
                    process_time_conv = int(process_time) * 7
                    process_timeprefix = "нед."
                case "month":
                    process_time_conv = int(process_time) * 30
                    process_timeprefix = "мес."
                case "hour":
                    process_time_conv = round(float(process_time) / 24, 2)
                    process_timeprefix = "час."
                case _:
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
            proc_time.append(process_time_conv / int(process_lines))
            proc_time_str.append(f"{str(process_time_conv)}/{str(process_lines)}")

        posl_value = sum(proc_time) * products_count
        posl_data = [
            dcc.Markdown("**Последовательный метод**"),
            dcc.Markdown(
                f'$$t_{"{посл}"} = ({" + ".join(proc_time_str)})*{str(products_count)} = {str(posl_value)} ~ (дн.)$$',
                mathjax=True,
            ),
        ]

        paral_value = sum(proc_time) + ((products_count - 1) * max(proc_time))
        paral_data = [
            dcc.Markdown("**Параллельный метод**"),
            dcc.Markdown(
                [
                    f'$$t_{"{парал}"} = ({" + ".join(proc_time_str)})+$$\n',
                    f"$$+({str(products_count)}-1)*{str(max(proc_time_str))} = {str(paral_value)}~(дн.)$$",
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


@callback(
    Output("calc_output", "children"),
    Input("make_calc_hard", "n_clicks"),
    [
        State("operations_count", "value"),
        State({"type": "parallel_operations", "index": ALL}, "value"),
        State("products_count", "value"),
        State("transportways_count", "value"),
        State({"type": "operation_time_input", "index": ALL}, "value"),
        State({"type": "operation_time_timetype", "index": ALL}, "value"),
        State({"type": "from_point", "index": ALL}, "value"),
        State({"type": "to_point", "index": ALL}, "value"),
        State({"type": "time_between_points", "index": ALL}, "value"),
        State({"type": "delivery_type", "index": ALL}, "value"),
        State({"type": "parallel_delivery", "index": ALL}, "value"),
        State({"type": "production_type", "index": ALL}, "value"),
    ],
    prevent_initial_call=True,
)
def calculate_hard(
    n_clicks,
    operations_count,
    parallel_operations,
    products_count,
    transportways_count,
    operation_time_input,
    operation_time_timetype,
    from_point,
    to_point,
    time_between_points,
    delivery_type,
    parallel_delivery,
    production_type,
):
    if n_clicks == None:
        return no_update
    else:
        G = nx.DiGraph(directed=True)

        # add NODES with properties
        node_labels = {}
        for (
            node_id,
            process_time,
            process_timeprefix,
            production_type1,
            parallel_operations1,
        ) in zip(
            range(operations_count),
            operation_time_input,
            operation_time_timetype,
            production_type,
            parallel_operations,
        ):
            node_id += 1
            # decode timeprefix
            recalc_time = time_recalculate(
                process_time, products_count, production_type1, parallel_operations1
            )
            match process_timeprefix:
                case "days":
                    process_time = int(process_time)
                case "week":
                    process_time = int(process_time) * 7
                case "month":
                    process_time = int(process_time) * 30
                case "hour":
                    process_time = round(float(process_time) / 24, 2)
            G.add_node(
                node_id,
                weight=recalc_time,
                production_type=production_type1,
                parallel_operations=parallel_operations1,
            )
            node_labels[node_id] = f"{recalc_time} ({production_type1})"

        # add EDGES with properties
        for (
            from_point1,
            to_point1,
            time_between_points1,
            delivery_type1,
            parallel_delivery1,
        ) in zip(
            from_point, to_point, time_between_points, delivery_type, parallel_delivery
        ):
            G.add_edge(
                int(from_point1),
                int(to_point1),
                weight=time_recalculate(
                    time_between_points1,
                    products_count,
                    delivery_type1,
                    parallel_delivery1,
                ),
                delivery_type=delivery_type1,
                parallel_delivery=parallel_delivery1,
            )

        # draw fig
        options = {
            "node_color": "#4e6de6",  # color of node
            "node_size": 700,  # size of node
            "width": 1.5,  # line width of edges
            "arrowstyle": "-|>",  # array style for directed graph
            "arrowsize": 20,  # size of arrow
            "font_size": 12,
        }
        fig = matplotlib.pyplot.figure(figsize=(7, 7))
        weight_edge_labels = nx.get_edge_attributes(G, "weight")
        dtype_edge_labels = nx.get_edge_attributes(G, "delivery_type")
        pos = nx.circular_layout(G)
        nx.draw(
            G,
            ax=fig.add_subplot(),
            pos=pos,
            with_labels=True,
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="circle,pad=0.2"),
            **options,
        )

        # all labels to edges
        edge_labels = {}
        for key in dtype_edge_labels:
            edge_labels[key] = f"{weight_edge_labels[key]} ({dtype_edge_labels[key]})"
        nx.draw_networkx_edge_labels(
            G,
            pos,
            edge_labels=edge_labels,
            bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.2"),
            font_size=11,
        )

        # add nodes labels
        for p in pos:  # raise text positions
            pos[p][1] += 0.14
        nx.draw_networkx_labels(
            G,
            pos,
            node_labels,
            font_size=11,
            font_color="black",
            bbox=dict(
                facecolor="skyblue",
                edgecolor="black",
                boxstyle="round,pad=0.2",
                alpha=0.5,
            ),
        )

        # encode fig to base64
        buf = io.BytesIO()  # in-memory files
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("utf8")

        # critical way calc
        longest_way = nx.dag_longest_path(G)
        weight_sum = nx.path_weight(G, longest_way, "weight") + sum(
            [G.nodes[node]["weight"] for node in G.nodes]
        )

        return dmc.Stack(
            [
                html.Img(
                    src="data:image/png;base64,{}".format(data), style={"width": "90%"}
                ),
                html.P(
                    [
                        "longest way ",
                        str(longest_way),
                        " = ",
                        round(weight_sum, 2),
                    ]
                ),
            ]
        )
