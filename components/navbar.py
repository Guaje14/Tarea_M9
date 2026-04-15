# Importa componentes Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa elementos HTML de Dash
from dash import html

# Importa las posibles rutas del logo
from config import LOGO_CANDIDATES


# Función para crear el logo de la marca
def _brand_logo():
    return html.Img(
        src=LOGO_CANDIDATES[0],  # Usa el primer logo disponible
        height="42px",  # Altura del logo
        className="brand-logo me-2",  # Clases de estilo
        alt="Datathletics",  # Texto alternativo
    )


# Función para construir la barra de navegación principal
def build_navbar():

    # Marca compuesta por logo y nombre
    brand = html.Div(
        [_brand_logo(), html.Span("Datathletics", className="fw-bold fs-5")],
        className="d-flex align-items-center"
    )

    return dbc.Navbar(
        dbc.Container(
            [
                # Nombre y logo con enlace al inicio
                dbc.NavbarBrand(brand, href="/", className="d-flex align-items-center"),

                # Enlaces de navegación
                dbc.Nav(
                    [
                        dbc.NavLink("Home", href="/", active="exact"),
                        dbc.NavLink("Performance", href="/performance", active="exact"),
                        dbc.NavLink("GPS", href="/non-competitive", active="exact"),
                        dbc.NavLink("Logout", href="/logout", external_link=True),
                    ],
                    pills=True,  # Activa estilo tipo pastilla
                    className="ms-auto gap-2",  # Alineación y separación
                ),
            ],
            fluid=True,  # Contenedor de ancho completo
        ),
        color="dark",  # Color base del navbar
        dark=True,  # Activa tema oscuro
        className="shadow-sm mb-4 main-navbar",  # Clases de estilo extra
    )