from dash import (
    html,
    register_page,
)
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

register_page(__name__, path="/", icon="fa-solid:home", name='Логистический калькулятор')


def layout():
    return html.Div(
        [
            dmc.Space(h=10),
            html.Center(html.H4('Выберите вид расчета логистических операций')),
            dmc.Space(h=10),
            dmc.Grid(
                [
                    dmc.Col(span='auto'),
                    dmc.Col([
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("По времени", className="card-title"),
                                        html.P(
                                            "Учет временных этапов производства и транспортировки товаров",
                                            className="card-text",
                                        ),
                                        dmc.Space(h=10),
                                        dbc.Button("Перейти к расчету", color="primary", href='/by_time'),
                                    ]
                                ),
                            ],
                            style={"width": "20rem"},
                        )
                    ], span='content'),
                    dmc.Col([
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4("По цене", className="card-title"),
                                        html.P(
                                            "Учет стоимостей перевозки, хранения и обработки товаров на складах",
                                            className="card-text",
                                        ),
                                        dmc.Space(h=10),
                                        dbc.Button("Перейти к расчету", color="primary", href='/by_price'),
                                    ]
                                ),
                            ],
                            style={"width": "20rem"},
                        )
                    ], span='content'),
                    dmc.Col(span='auto')
                ]
            )
        ]
    )
