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

allow_save_data_in_fields = False


def get_tablerow_with_input(parameter_id=None, value_name=None, divider=False):
    global allow_save_data_in_fields
    return html.Tr(
        [
            html.Td(dcc.Markdown(value_name), style={"text-align": "left"}),
            html.Td(
                dbc.Input(
                    placeholder=f"Введите {parameter_id}",
                    id=f"price-{parameter_id}",
                    type="number",
                    persistence=allow_save_data_in_fields,
                )
            ),
        ]
    ) if divider==False else html.Tr(dmc.Divider())


def layout():
    # return html.A("Раздел не готов. Перейдите к расчетам по времени.", href="/by_time")
    values_div = dmc.Stack(
        [
            html.H3("Исходные данные"),
            html.Div(
                [
                    # оформить ввод данных в виде таблицы
                    html.Table(
                        html.Tbody(
                            [
                                # get_tablerow_with_input("R1", "Test"),
                                # html.Tr(dcc.Markdown('**header**')),
                                html.Tr(dcc.Markdown('**Основные расходы**')),
                                get_tablerow_with_input("R1", "Расходы на аренду 1 кв.м площади"),
                                get_tablerow_with_input("R2", "Коммунальные платежи на 1 кв.м"),
                                get_tablerow_with_input("R3", "Прочие расходы на экспл. и содержание склада"),
                                html.Tr(dcc.Markdown('**Амортизация**')),
                                get_tablerow_with_input("A1", "Срок амортизации стеллажей в мес."),
                                get_tablerow_with_input("A2", "Срок амортизации прочего скл. оборудования в мес."),
                                html.Tr(dcc.Markdown('**Расходы на эксплуатацию**')),
                                get_tablerow_with_input("C1", "Стоимость стеллажей"),
                                get_tablerow_with_input("C2", "Обслуживание стеллажей"),
                                get_tablerow_with_input("C3", "Стоимость прочего скл. оборудования"),
                                get_tablerow_with_input("C4", "Прочие расходы на эксплуатацию"),
                            ]
                        )
                    ),
                    html.Table(
                        html.Tbody(
                            [
                                
                            ]
                        )
                    ),
                ],
                className="input-block",
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
