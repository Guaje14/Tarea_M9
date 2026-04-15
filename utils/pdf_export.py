# Importa un buffer en memoria para crear el PDF
from io import BytesIO

# Importa colores de ReportLab
from reportlab.lib import colors

# Importa el tamaño de página A4
from reportlab.lib.pagesizes import A4

# Importa estilos de texto predefinidos
from reportlab.lib.styles import getSampleStyleSheet

# Importa componentes para construir el PDF
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle

# Importa la unidad centímetro
from reportlab.lib.units import cm


# Función que construye el PDF resumen de performance
def build_performance_pdf(summary_rows, title="Reporte Performance"):

    # Crea un buffer en memoria
    buffer = BytesIO()

    # Define el documento PDF y sus márgenes
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm
    )

    # Carga estilos básicos de texto
    styles = getSampleStyleSheet()

    # Lista de elementos del PDF
    story = []

    # Añade el título principal
    story.append(Paragraph(title, styles["Title"]))

    # Añade un subtítulo
    story.append(Paragraph("Dashboard Deportivo · Exportación PDF", styles["Heading3"]))

    # Añade un espacio vertical
    story.append(Spacer(1, 12))

    # Prepara los datos de la tabla
    table_data = [["Métrica", "Valor"]]
    table_data.extend(summary_rows)

    # Crea la tabla con dos columnas
    table = Table(table_data, colWidths=[8 * cm, 8 * cm])

    # Aplica estilos visuales a la tabla
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0d6efd")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#d9dfe8")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#f7f9fc")]),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    # Añade la tabla al contenido
    story.append(table)

    # Genera el PDF final
    doc.build(story)

    # Vuelve al inicio del buffer
    buffer.seek(0)

    # Devuelve el PDF en memoria
    return buffer