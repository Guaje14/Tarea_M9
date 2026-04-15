# Importa Dash
import dash

# Importa inputs, outputs, estados y no_update
from dash import Input, Output, State, no_update

# Importa gráficos rápidos con Plotly Express
import plotly.express as px

# Importa gráficos más personalizados con Graph Objects
import plotly.graph_objects as go

# Importa componentes de Bootstrap para Dash
import dash_bootstrap_components as dbc

# Importa la función que construye el PDF
from utils.pdf_export import build_performance_pdf


# Función para registrar los callbacks de la página de performance
def register_performance_callbacks(app, get_stats_cached, get_gps_cached):

    # Callback para sincronizar jugadoras según el equipo
    @app.callback(
        Output("perf-player-filter", "options"),
        Output("perf-player-filter", "value"),
        Input("perf-team-filter", "value"),
    )
    
    # Función auxiliar para sincronizar las opciones de jugadoras según el equipo seleccionado
    def sync_players(team):

        # Carga los datos estadísticos
        df = get_stats_cached()

        # Filtra por equipo si hay uno seleccionado
        filtered = df[df["Equipo"] == team] if team else df.copy()

        # Obtiene la lista ordenada de jugadoras
        players = filtered["Nombre"].dropna().sort_values().tolist()

        # Devuelve opciones y selección inicial
        return [{"label": p, "value": p} for p in players], players[:5]

    # Callback principal para actualizar gráficos
    @app.callback(
        Output("perf-scatter", "figure"),
        Output("perf-bar", "figure"),
        Output("perf-radar", "figure"),
        Output("perf-gps-support", "figure"),
        Output("perf-error", "children"),
        Input("perf-team-filter", "value"),
        Input("perf-player-filter", "value"),
        Input("perf-date-filter", "start_date"),
        Input("perf-date-filter", "end_date"),
    )
    
    # Función para actualizar los gráficos de performance
    def update_performance(team, players, start_date, end_date):
        try:
            # Copia los datos de stats y GPS
            stats_df = get_stats_cached().copy()
            gps_df = get_gps_cached().copy()

            # Filtra stats por equipo
            if team:
                stats_df = stats_df[stats_df["Equipo"] == team]

            # Filtra stats y GPS por jugadoras
            if players:
                stats_df = stats_df[stats_df["Nombre"].isin(players)]
                gps_df = gps_df[gps_df["Jugadora"].isin(players)]

            # Filtra GPS por rango de fechas
            if start_date and end_date and "Fecha" in gps_df.columns:
                gps_df = gps_df[gps_df["Fecha"].between(start_date, end_date)]

            # Si no hay datos, devuelve gráficos vacíos
            if stats_df.empty:
                empty = go.Figure()
                empty.update_layout(template="plotly_white", title="Sin datos")
                return empty, empty, empty, empty, dbc.Alert("No hay datos con los filtros seleccionados.", color="warning")

            # Crea scatter de xG vs goles
            scatter = px.scatter(
                stats_df, x="xG", y="Goles", size="Rem", color="Posición", hover_name="Nombre",
                title="xG vs Goles", template="plotly_white", custom_data=["Equipo"]
            )

            # Añade borde blanco a los puntos
            scatter.update_traces(marker=dict(line=dict(width=1, color="white")))

            # Prepara datos del bar chart
            bar_df = stats_df.sort_values("Recuperaciones", ascending=False).head(8)

            # Crea gráfico de barras
            bar = px.bar(
                bar_df, x="Nombre", y="Recuperaciones", color="Posición",
                title="Top recuperaciones", template="plotly_white"
            )

            # Ajusta títulos de ejes
            bar.update_layout(xaxis_title="", yaxis_title="Recuperaciones")

            # Selecciona la primera jugadora para el radar
            radar_player = stats_df.iloc[0]

            # Crea figura radar
            radar = go.Figure()

            # Variables del radar
            categories = ["Goles", "Asistencias", "Recuperaciones", "RegCmp", "DnG"]

            # Añade la traza polar
            radar.add_trace(go.Scatterpolar(
                r=[float(radar_player[c]) for c in categories],
                theta=categories, fill="toself", name=radar_player["Nombre"]
            ))

            # Ajusta estilo del radar
            radar.update_layout(template="plotly_white", title=f"Radar resumido · {radar_player['Nombre']}")

            # Si no hay datos GPS, crea gráfico vacío
            if gps_df.empty:
                gps_support = go.Figure()
                gps_support.update_layout(template="plotly_white", title="Apoyo GPS · sin datos con este filtro")

                # Mensaje informativo si no hay GPS
                info = dbc.Alert(
                    "No hay coincidencias GPS para las jugadoras elegidas en ese rango. Prueba ampliando fechas o cambiando selección.",
                    color="info"
                )
            else:
                # Agrupa medias GPS por jugadora
                aux = gps_df.groupby("Jugadora", as_index=False)[["DistPorMin", "DistAltaVel_m", "Sprints"]].mean()

                # Ordena por distancia por minuto
                aux = aux.sort_values("DistPorMin", ascending=True)

                # Crea scatter de apoyo GPS
                gps_support = px.scatter(
                    aux,
                    x="DistPorMin",
                    y="DistAltaVel_m",
                    size="Sprints",
                    color="Jugadora",
                    hover_name="Jugadora",
                    title="Apoyo GPS · intensidad vs alta velocidad",
                    template="plotly_white",
                    labels={"DistPorMin": "Metros por minuto", "DistAltaVel_m": "Distancia alta velocidad"},
                )

                # Ajusta el título de la leyenda
                gps_support.update_layout(legend_title_text="Jugadora")

                # Mensaje explicativo del gráfico GPS
                info = dbc.Alert(
                    "Cruce visual entre intensidad relativa, metros a alta velocidad y sprints medios en el rango elegido.",
                    color="secondary"
                )

            # Devuelve todas las figuras y el mensaje
            return scatter, bar, radar, gps_support, info

        except Exception as exc:
            # Si hay error, devuelve figuras vacías
            empty = go.Figure()
            empty.update_layout(template="plotly_white", title="Error")
            return empty, empty, empty, empty, dbc.Alert(f"Error al actualizar performance: {exc}", color="danger")

    # Callback para exportar el PDF
    @app.callback(
        Output("download-performance-pdf", "data"),
        Input("export-performance-pdf", "n_clicks"),
        State("perf-team-filter", "value"),
        State("perf-player-filter", "value"),
        State("perf-date-filter", "start_date"),
        State("perf-date-filter", "end_date"),
        prevent_initial_call=True,
    )
    
    # Función para exportar el PDF de performance
    def export_pdf(n_clicks, team, players, start_date, end_date):

        # Evita ejecutar si no hay clic
        if not n_clicks:
            return no_update

        # Carga los datos
        df = get_stats_cached()

        # Filtra por equipo
        if team:
            df = df[df["Equipo"] == team]

        # Filtra por jugadoras
        if players:
            df = df[df["Nombre"].isin(players)]

        # Prepara filas resumen para el PDF
        rows = [
            ["Equipo", team or "Todos"],
            ["Jugadoras seleccionadas", ", ".join(players) if players else "Todas"],
            ["Fechas de referencia", f"{start_date} a {end_date}"],
            ["Total jugadoras en vista", str(len(df))],
            ["Promedio goles", f"{df['Goles'].mean():.2f}" if not df.empty else "0"],
            ["Promedio xG", f"{df['xG'].mean():.2f}" if not df.empty else "0"],
            ["Promedio recuperaciones", f"{df['Recuperaciones'].mean():.2f}" if not df.empty else "0"],
        ]

        # Genera el PDF en memoria
        pdf_buffer = build_performance_pdf(rows, title="Reporte de Performance")

        # Lanza la descarga del archivo
        return dash.dcc.send_bytes(pdf_buffer.getvalue(), "reporte_performance.pdf")