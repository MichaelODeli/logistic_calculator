import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from dash import (
    dcc,
    html,
)


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