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
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from datetime import datetime
from dash_extensions import Purify

register_page(
    __name__, path="/by_price", icon="fa-solid:home", name="Цена | Логист. калькулятор"
)


def layout():
    # return html.A("Раздел не готов. Перейдите к расчетам по времени.", href="/by_time")
    values_div = dmc.Stack(
        [
            html.H3("Исходные данные"),
            html.Div(
                [
                    # оформить ввод данных в виде таблицы
                    dbc.InputGroup([dbc.InputGroupText('Description'), dbc.Input(type='number')]),
                ],
                className="input-block",
                style={"height": "200px"},
            ),
        ],
        align="center",
        spacing="xl",
    )

    calc_div = dmc.Stack(
        [
            html.H3("Результаты расчетов"),
            html.Div(className="input-block", style={"height": "200px"}),
        ],
        align="center",
        spacing="xl",
    )

    return dmc.Grid(
        [
            dmc.Col(span="auto"),
            dmc.Col(html.Div(values_div), span=5, className="block-col"),
            dmc.Col(html.Div(calc_div), span=5, className="block-col"),
            dmc.Col(span="auto"),
        ]
    )
