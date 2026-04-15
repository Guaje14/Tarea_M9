# Importa componentes Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa elementos HTML de Dash
from dash import html


# Función que construye el layout de la página principal
def layout_home():
    return dbc.Container(
        [
            # Primera fila de bienvenida
            dbc.Row(
                [
                    # Columna izquierda con mensaje principal
                    dbc.Col(
                        [
                            # Texto superior pequeño
                            html.Div("Bienvenido a Datathletics", className="eyebrow"),

                            # Título principal de la home
                            html.H1("Control deportivo en una sola plataforma", className="display-4 fw-bold mb-3"),

                            # Descripción de la app
                            html.P(
                                "Una aplicación pensada para visualizar rendimiento competitivo y carga GPS con una experiencia clara, visual y profesional.",
                                className="lead text-secondary mb-4",
                            ),

                            # Botones de acceso rápido
                            html.Div(
                                [
                                    dbc.Button("Entrar a Performance", href="/performance", color="primary", className="me-2 px-4"),
                                    dbc.Button("Entrar a GPS", href="/non-competitive", color="dark", outline=True, className="px-4"),
                                ],
                                className="d-flex flex-wrap gap-2",
                            ),
                        ],
                        md=7,  # Ancho en pantallas medianas
                    ),

                    # Columna derecha con resumen visual
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    # Etiqueta del panel
                                    html.Div("Visión general", className="eyebrow"),

                                    # Título del bloque
                                    html.H4("Panel técnico de análisis", className="mb-3"),

                                    # Texto explicativo
                                    html.P(
                                        "Consulta jugadoras, compara rendimiento, revisa carga de entrenamiento y genera un reporte en PDF desde una interfaz única.",
                                        className="text-secondary mb-3"
                                    ),

                                    # Métricas rápidas del sistema
                                    html.Div(
                                        [
                                            html.Div([html.Span("2"), html.Small("bases SQLite")], className="metric-pill"),
                                            html.Div([html.Span("3"), html.Small("páginas")], className="metric-pill"),
                                            html.Div([html.Span("4+"), html.Small("visualizaciones")], className="metric-pill"),
                                        ],
                                        className="d-flex gap-3 flex-wrap",
                                    ),
                                ]
                            ),
                            className="hero-panel p-2",
                        ),
                        md=5,  # Ancho en pantallas medianas
                    ),
                ],
                className="align-items-center g-4 mb-4 hero-row",
            ),

            # Segunda fila con módulos principales
            dbc.Row(
                [
                    # Tarjeta del módulo Performance
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Módulo 1", className="eyebrow"),
                                    html.H5("Performance"),
                                    html.P(
                                        "Gráficos interactivos para goles, xG, recuperaciones y perfil de jugadora.",
                                        className="text-secondary mb-0"
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=4,
                    ),

                    # Tarjeta del módulo GPS
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Módulo 2", className="eyebrow"),
                                    html.H5("GPS"),
                                    html.P(
                                        "Seguimiento de distancia, intensidad, aceleraciones y carga por sesión.",
                                        className="text-secondary mb-0"
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=4,
                    ),

                    # Tarjeta del módulo exportación
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Módulo 3", className="eyebrow"),
                                    html.H5("Exportación"),
                                    html.P(
                                        "Descarga un resumen en PDF del dashboard competitivo con los filtros aplicados.",
                                        className="text-secondary mb-0"
                                    ),
                                ]
                            ),
                            className="card-soft h-100",
                        ),
                        md=4,
                    ),
                ],
                className="g-3",
            ),
        ],
        fluid=True,  # Contenedor de ancho completo
    )