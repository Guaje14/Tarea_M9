# Importa componentes Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa componentes principales de Dash
from dash import dcc, html, dash_table


# Función que construye el layout de la página GPS no competitiva
def layout_non_competitive(players, min_date, max_date):
    return dbc.Container(
        [
            # Título principal de la página
            html.H2("Dashboard de Área No Competitiva · GPS", className="mb-3"),

            # Fila de filtros
            dbc.Row(
                [
                    # Filtro de jugadoras
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Jugadora", className="fw-semibold"),

                                    # Dropdown para seleccionar jugadoras
                                    dcc.Dropdown(
                                        id="gps-player-filter",
                                        options=[{"label": p, "value": p} for p in players],
                                        value=players[:4],
                                        multi=True,
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=4,
                    ),

                    # Filtro de tipo de sesión
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Tipo de sesión", className="fw-semibold"),

                                    # Dropdown para elegir entrenamiento o partido
                                    dcc.Dropdown(
                                        id="gps-type-filter",
                                        options=[
                                            {"label": "Entrenamiento", "value": "E"},
                                            {"label": "Partido", "value": "P"},
                                        ],
                                        value=["E", "P"],
                                        multi=True,
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=3,
                    ),

                    # Filtro de rango de fechas
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Fechas", className="fw-semibold"),

                                    # Selector de rango de fechas
                                    dcc.DatePickerRange(
                                        id="gps-date-filter",
                                        min_date_allowed=min_date,
                                        max_date_allowed=max_date,
                                        start_date=min_date,
                                        end_date=max_date,
                                        display_format="YYYY-MM-DD",
                                        className="w-100",
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=5,
                    ),
                ],
                className="g-3 mb-4",
            ),

            # Fila de gráficos
            dbc.Row(
                [
                    # Gráfico de líneas GPS
                    dbc.Col(dbc.Spinner(dcc.Graph(id="gps-line")), md=7),

                    # Boxplot GPS
                    dbc.Col(dbc.Spinner(dcc.Graph(id="gps-box")), md=5),
                ],
                className="g-3 mb-4",
            ),

            # Fila de tabla de datos
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # Título de la tabla
                                    html.H5("Detalle de sesiones GPS"),

                                    # Tabla interactiva con datos GPS
                                    dash_table.DataTable(
                                        id="gps-table",
                                        page_size=10,
                                        sort_action="native",
                                        filter_action="native",
                                        style_table={"overflowX": "auto"},
                                        style_header={"backgroundColor": "#122033", "color": "white", "fontWeight": "bold"},
                                        style_cell={"backgroundColor": "#ffffff", "padding": "8px", "border": "1px solid #eef2f7", "textAlign": "left"},
                                    ),
                                ]
                            ),
                            className="card-soft",
                        ),
                        md=12,
                    )
                ]
            )
        ],
        fluid=True,  # Contenedor de ancho completo
    )