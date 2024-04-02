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

register_page(__name__, path="/", icon="fa-solid:home", name='Логистический калькулятор')


def layout():
    return html.A("Перейти к расчетам", href="/by_time")
