# Importa inputs y outputs de Dash
from dash import Input, Output

# Importa gráficos rápidos con Plotly Express
import plotly.express as px

# Importa gráficos más personalizados con Graph Objects
import plotly.graph_objects as go


# Función para registrar los callbacks de la página GPS no competitiva
def register_non_competitive_callbacks(app, get_gps_cached):

    # Callback para actualizar gráficos y tabla
    @app.callback(
        Output("gps-line", "figure"),
        Output("gps-box", "figure"),
        Output("gps-table", "data"),
        Output("gps-table", "columns"),
        Input("gps-player-filter", "value"),
        Input("gps-type-filter", "value"),
        Input("gps-date-filter", "start_date"),
        Input("gps-date-filter", "end_date"),
    )
    
    # Función auxiliar que actualiza los gráficos y la tabla según los filtros seleccionados
    def update_gps(players, session_types, start_date, end_date):

        # Carga una copia de los datos GPS
        df = get_gps_cached().copy()

        # Filtra por jugadoras seleccionadas
        if players:
            df = df[df["Jugadora"].isin(players)]

        # Filtra por tipo de sesión
        if session_types:
            df = df[df["Tipo"].isin(session_types)]

        # Filtra por rango de fechas
        if start_date and end_date:
            df = df[df["Fecha"].between(start_date, end_date)]

        # Si no hay datos, devuelve figuras vacías y tabla vacía
        if df.empty:
            empty = go.Figure()
            empty.update_layout(template="plotly_white", title="Sin datos")
            return empty, empty, [], []

        # Agrupa la distancia total por fecha y jugadora
        line_df = df.groupby(["Fecha", "Jugadora"], as_index=False)["DistTotal_m"].sum()

        # Crea gráfico de líneas de evolución
        line_fig = px.line(
            line_df, x="Fecha", y="DistTotal_m", color="Jugadora",
            markers=True, title="Evolución de distancia total", template="plotly_white"
        )

        # Crea boxplot de intensidad por tipo de sesión
        box_fig = px.box(
            df, x="Tipo", y="DistPorMin", color="Tipo",
            title="Intensidad relativa por tipo de sesión", template="plotly_white"
        )

        # Define las columnas preferidas para la tabla
        preferred_cols = ["Jugadora", "Mes", "Fecha", "Tipo", "Minutos", "DistTotal_m", "DistAltaVel_m", "Sprints", "Acel_Alta", "Decel_Alta", "CargaMetabolica", "DistPorMin"]

        # Conserva solo las columnas que existan
        table_cols = [c for c in preferred_cols if c in df.columns]

        # Prepara los datos de la tabla ordenados por fecha
        table_df = df[table_cols].sort_values("Fecha", ascending=False).copy()

        # Convierte la fecha a texto para mostrarla bien
        table_df["Fecha"] = table_df["Fecha"].astype(str)

        # Construye la definición de columnas para Dash
        columns = [{"name": col, "id": col} for col in table_cols]

        # Devuelve gráficos y tabla
        return line_fig, box_fig, table_df.to_dict("records"), columns