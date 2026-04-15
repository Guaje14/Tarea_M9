# Importa Dash
import dash

# Importa componentes y herramientas principales de Dash
from dash import dcc, html, Input, Output

# Importa componentes Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa utilidades de Flask
from flask import Flask, request, redirect, render_template_string, url_for

# Importa sistema de caché para Flask
from flask_caching import Cache

# Importa herramientas de autenticación
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

# Importa configuración general de la app
from config import SECRET_KEY, APP_TITLE, CACHE_TIMEOUT, LOGO_CANDIDATES

# Importa autenticación de usuario
from utils.auth import User, validate_user

# Importa acceso a datos y escudos
from utils.database import get_performance_data, get_gps_season, get_shield_src

# Importa componentes y layouts
from components.navbar import build_navbar
from layouts.home import layout_home
from layouts.performance import layout_performance
from layouts.non_competitive import layout_non_competitive

# Importa callbacks de las páginas
from callbacks.performance_callbacks import register_performance_callbacks
from callbacks.non_competitive_callbacks import register_non_competitive_callbacks


# Crea el servidor Flask
server = Flask(__name__)

# Configura la clave secreta
server.config["SECRET_KEY"] = SECRET_KEY

# Configura caché simple en memoria
server.config["CACHE_TYPE"] = "SimpleCache"

# Configura tiempo por defecto de la caché
server.config["CACHE_DEFAULT_TIMEOUT"] = CACHE_TIMEOUT


# Inicializa la caché
cache = Cache(server)

# Inicializa el gestor de login
login_manager = LoginManager()
login_manager.init_app(server)

# Define la ruta de login por defecto
login_manager.login_view = "/login"


# Función que carga el usuario a partir de su id
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Función que protege las rutas privadas antes de cada request
@server.before_request
def protect_dash_routes():
    public_paths = {"/login"}

    # Permite acceso a assets, dash interno y favicon
    if request.path.startswith("/assets") or request.path.startswith("/_dash") or request.path.startswith("/favicon.ico"):
        return None

    # Permite acceso a rutas públicas
    if request.path in public_paths:
        return None

    # Redirige al login si no está autenticado
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    return None


# Función que maneja la ruta de login
@server.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    # Procesa el formulario si se envía por POST
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Valida usuario y contraseña
        if validate_user(username, password):
            login_user(User(username))
            return redirect("/")

        error = "Usuario o contraseña incorrectos"

    # Renderiza la página de login
    return render_template_string(
        """
        <!doctype html>
        <html lang="es">
        <head>
            <meta charset="utf-8">
            <title>Login Dashboard Deportivo</title>
            <link rel="stylesheet" href="/assets/login.css">
        </head>
        <body>
            <div class="login-shell">
                <div class="login-card">
                    <img src="{{ logo_src }}" alt="Datathletics" class="login-logo">
                    <p class="eyebrow">M9 · Dashboard Deportivo</p>
                    <h1>Iniciar sesión</h1>
                    <p>Para acceder a la aplicación ingresar admin en usuario y contraseña</p>
                    <form method="post">
                        <input name="username" placeholder="Usuario" required>
                        <input name="password" placeholder="Contraseña" type="password" required>
                        <button type="submit">Entrar</button>
                    </form>
                    {% if error %}
                        <div class="error-box">{{ error }}</div>
                    {% endif %}
                </div>
            </div>
        </body>
        </html>
        """,
        error=error,
        logo_src=LOGO_CANDIDATES[0],
    )


# Función que maneja la ruta de cierre de sesión
@server.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# Función que devuelve los datos de performance en caché
@cache.memoize()
def get_stats_cached():
    return get_performance_data()


# Función que devuelve los datos GPS en caché
@cache.memoize()
def get_gps_cached():
    return get_gps_season()


# Función que construye las opciones del dropdown de equipos
def build_team_options(teams):
    options = []

    for team in teams:
        shield = get_shield_src(team)
        label_children = []

        # Añade el escudo si existe
        if shield:
            label_children.append(html.Img(src=shield, className="team-option-badge"))

        # Añade el nombre del equipo
        label_children.append(html.Span(team))

        # Crea la opción del dropdown
        options.append({
            "label": html.Span(label_children, className="d-flex align-items-center gap-2"),
            "value": team,
            "search": team,
        })

    return options


# Crea la app Dash
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    title=APP_TITLE,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
)


# Obtiene la lista de jugadoras de performance
players_stats = sorted(get_stats_cached()["Nombre"].dropna().unique().tolist())

# Obtiene la lista de equipos
teams = sorted(get_stats_cached()["Equipo"].dropna().unique().tolist())

# Construye las opciones visuales de equipos
team_options = build_team_options(teams)

# Obtiene la lista de jugadoras GPS
players_gps = sorted(get_gps_cached()["Jugadora"].dropna().unique().tolist())

# Obtiene la fecha mínima disponible
min_date = get_gps_cached()["Fecha"].min().date()

# Obtiene la fecha máxima disponible
max_date = get_gps_cached()["Fecha"].max().date()


# Define el layout principal de la app
app.layout = dbc.Container(
    [
        dcc.Location(id="url"),
        html.Div(id="page-content"),
    ],
    fluid=True,
    className="px-0",
)


# Callback para cambiar de página según la URL
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname):

    # Página de inicio
    if pathname == "/" or pathname == "":
        content = layout_home()

    # Página de performance
    elif pathname == "/performance":
        content = layout_performance(
            players_stats,
            team_options,
            teams[0] if teams else None,
            min_date,
            max_date
        )

    # Página GPS no competitiva
    elif pathname == "/non-competitive":
        content = layout_non_competitive(players_gps, min_date, max_date)

    # Página no encontrada
    else:
        content = dbc.Container(
            [html.H2("404"), html.P("Página no encontrada.")],
            className="py-4"
        )

    # Devuelve navbar + contenido
    return html.Div([build_navbar(), content])


# Registra callbacks de performance
register_performance_callbacks(app, get_stats_cached, get_gps_cached)

# Registra callbacks de GPS
register_non_competitive_callbacks(app, get_gps_cached)


# Ejecuta la app en modo debug
if __name__ == "__main__":
    app.run(debug=True)