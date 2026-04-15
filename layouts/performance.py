# Importa componentes Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa componentes principales de Dash
from dash import dcc, html


# Función que construye el layout de la página de performance
def layout_performance(players, team_options, default_team, min_date, max_date):
    return dbc.Container(
        [
            # Fila superior con título y botón de exportación
            dbc.Row(
                [
                    # Bloque de encabezado
                    dbc.Col(
                        [
                            html.Div("Análisis competitivo", className="eyebrow"),
                            html.H2("Dashboard de Performance", className="mb-1"),
                            html.P(
                                "Filtra por equipo, jugadoras y rango temporal de apoyo GPS.",
                                className="text-secondary mb-0"
                            ),
                        ],
                        md=8,
                    ),

                    # Botón para exportar a PDF
                    dbc.Col(
                        dbc.Button(
                            "Exportar PDF",
                            id="export-performance-pdf",
                            color="dark",
                            className="w-100 mt-md-3"
                        ),
                        md=4,
                    ),
                ],
                className="align-items-end mb-3",
            ),

            # Fila de filtros
            dbc.Row(
                [
                    # Filtro de equipo
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Equipo", className="fw-semibold mb-2"),

                                    # Dropdown de equipo
                                    dcc.Dropdown(
                                        id="perf-team-filter",
                                        options=team_options,
                                        value=default_team,
                                        clearable=False,
                                        optionHeight=56,
                                        className="dropdown-team-large",
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=4,
                    ),

                    # Filtro de jugadoras
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Jugadoras", className="fw-semibold mb-2"),

                                    # Dropdown multiselección de jugadoras
                                    dcc.Dropdown(
                                        id="perf-player-filter",
                                        options=[{"label": p, "value": p} for p in players],
                                        value=players[:5],
                                        multi=True,
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=4,
                    ),

                    # Filtro de fechas GPS
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Label("Fechas de referencia GPS", className="fw-semibold mb-2"),

                                    # Selector de rango de fechas
                                    dcc.DatePickerRange(
                                        id="perf-date-filter",
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
                        md=4,
                    ),
                ],
                className="g-3 mb-3",
            ),

            # Fila para mostrar alertas o mensajes
            dbc.Row(
                [dbc.Col(html.Div(id="perf-error"), md=12)],
                className="mb-2"
            ),

            # Fila de gráficos principales
            dbc.Row(
                [
                    # Scatter de performance
                    dbc.Col(dcc.Graph(id="perf-scatter"), md=6),

                    # Bar chart de recuperaciones
                    dbc.Col(dcc.Graph(id="perf-bar"), md=6),
                ],
                className="g-3",
            ),

            # Fila de gráficos secundarios
            dbc.Row(
                [
                    # Radar de jugadora
                    dbc.Col(dcc.Graph(id="perf-radar"), md=5),

                    # Gráfico de apoyo GPS
                    dbc.Col(dcc.Graph(id="perf-gps-support"), md=7),
                ],
                className="g-3 mt-1",
            ),

            # Componente para descargar el PDF
            dcc.Download(id="download-performance-pdf"),
        ],
        fluid=True,  # Contenedor de ancho completo
    )