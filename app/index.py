from dash import (
    Dash,
    page_container,
    dcc,
    clientside_callback,
    ClientsideFunction,
    Output,
    Input,
)
from app import app as my_app


class MainApplication:
    def __init__(self):
        self.__app = my_app

    @property
    def app(self):
        return self.__app


Application = MainApplication()
app = Application.app.server
