# Datathletics · Dashboard Deportivo con Dash

Aplicación web deportiva desarrollada con **Dash + Flask + Bootstrap** para cumplir la tarea del módulo M9 usando la estructura real del proyecto.

## Funcionalidades incluidas

- Login con **Flask-Login**
  - usuario: `admin`
  - contraseña: `admin`
- Logout y protección de rutas
- Navegación multipágina:
  - Home
  - Dashboard de Performance
  - Dashboard de Área No Competitiva (GPS)
- CSS personalizado y diseño responsive con **Dash Bootstrap Components**
- Dashboard de Performance:
  - gráfico de dispersión
  - gráfico de barras
  - radar resumido
  - apoyo temporal con datos GPS
  - filtros por equipo, jugadoras y fechas
  - exportación a PDF
- Dashboard GPS:
  - gráfico de línea
  - boxplot
  - tabla interactiva
  - filtros por jugadora, tipo de sesión y fechas
- Datos cargados desde **dos bases de datos SQLite**
- Caché con **Flask-Caching**
- Manejo básico de errores y estados de carga

## Estructura real usada

```python
mi_proyecto/
│
├── assets/
│   ├── shields/
│   ├── img/
│   ├── login.css
│   └── fonts/
├── callbacks/
├── components/
├── data/
│   ├── stats_players.db
│   ├── gps_players.db
│   ├── shields_base64.json
│   └── csv de apoyo
├── layouts/
├── utils/
├── app.py
├── requirements.txt
└── config.py
```

## Bases de datos

La app está preparada para trabajar con **dos fuentes de datos distintas**, tal como pide la rúbrica:

- `stats_players.db`
  - tabla de estadísticas competitivas (`stats_players` o `liga_players_stats_2526`)
  - glosario (`glosario_stats`)
- `gps_players.db`
  - tabla de totales GPS (`gps_global_totals_2526`)
  - tabla de temporada GPS (`gps_full_season_2526`)
  - glosario (`glosario_gps`)

Además, la app usa `shields_base64.json` para resolver los escudos ya codificados en base64.

## Cómo ejecutarlo en Visual Studio Code

1. Abre la carpeta `mi_proyecto`.
2. Crea un entorno virtual:

```bash
python -m venv .venv
```

3. Actívalo:

### Windows
```bash
.venv\Scripts\activate
```

### Mac / Linux
```bash
source .venv/bin/activate
```

4. Instala dependencias:

```bash
pip install -r requirements.txt
```

5. Ejecuta la app:

```bash
python app.py
```
