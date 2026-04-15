# Importa componentes Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa elementos HTML de Dash
from dash import html


# Función para crear una tarjeta reutilizable para métricas
def stat_card(title, value, help_text=""):
    return dbc.Card(
        dbc.CardBody(
            [
                # Título pequeño de la métrica
                html.Div(title, className="small text-secondary"),

                # Valor principal de la tarjeta
                html.H3(value, className="mb-1"),

                # Texto de apoyo opcional
                html.Div(help_text, className="small text-muted"),
            ]
        ),

        # Clases de estilo de la tarjeta
        className="card-soft h-100",
    )