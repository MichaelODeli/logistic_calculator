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

register_page(__name__, path="/by_price", icon="fa-solid:home", name='Цена | Логист. калькулятор')


def layout():
    return html.A("Раздел не готов. Перейдите к расчетам по времени.", href="/by_time")