from google import genai
import sys
import time

# =========================
# FRONTEND CONSOLA
# =========================

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.markdown import Markdown
from rich.align import Align
from rich import box
from pyfiglet import Figlet

# =========================
# CONFIGURAR CONSOLA
# =========================

console = Console()

# =========================
# CONFIGURACIÓN API GEMINI
# =========================

API_KEY = "AIzaSyBsRugcuyqExeeTtSNWbrNpC4RSUiL6nIg"

# Inicializar cliente
try:
    client = genai.Client(api_key=API_KEY)

except Exception as e:

    console.print(
        "[bold red]❌ Error al inicializar Gemini[/bold red]"
    )

    sys.exit()

# =====================================================
# MODELO MATEMÁTICO
# =====================================================

class ModeloArbolDecision:

    def __init__(self, alternativas, probabilidades, pagos):

        self.alternativas = alternativas
        self.probabilidades = probabilidades
        self.pagos = pagos

    # =================================================

    def calcular_vme(self):

        resultados = {}

        for alt in self.alternativas:

            vme = sum(
                self.probabilidades[estado] *
                self.pagos[alt][estado]
                for estado in self.probabilidades
            )

            resultados[alt] = vme

        mejor_decision = max(
            resultados,
            key=resultados.get
        )

        return resultados, mejor_decision

# =====================================================
# AGENTE IA GEMINI
# =====================================================

class AgenteIAGemini:

    def __init__(
        self,
        resultados,
        mejor_decision,
        pagos,
        probabilidades
    ):

        self.resultados = resultados
        self.mejor_decision = mejor_decision
        self.pagos = pagos
        self.probabilidades = probabilidades

        self.modelo_id = 'gemini-2.0-flash'

    # =================================================

    def generar_prompt(self):

        prompt = f"""
Eres un consultor experto en estrategia empresarial e investigación de operaciones.
Se te han entregado los resultados matemáticos de un Árbol de Decisiones para una startup en Bogotá.

DATOS DEL MODELO:
- Demanda Alta: {self.probabilidades['Alta']*100}% | Demanda Baja: {self.probabilidades['Baja']*100}%

- Resultados Matemáticos (Valor Monetario Esperado):
"""

        for alt, vme in self.resultados.items():

            prompt += f"\n  * {alt}: ${vme:.2f}k USD"

        prompt += f"""

- Decisión Óptima Matemática:
{self.mejor_decision}

TU TAREA:

Genera un análisis ejecutivo respondiendo a estos 4 puntos clave
(usa formato Markdown y viñetas):

1. Explicación Estratégica
2. Análisis de Riesgos
3. Análisis de Sensibilidad
4. Propuesta de Mejoras usando Bayes o VEIP
"""

        return prompt

    # =================================================

    def mostrar_dashboard(self):

        table = Table(
            title="📊 RESULTADOS DEL ÁRBOL DE DECISIÓN",
            box=box.DOUBLE_EDGE,
            border_style="bright_cyan"
        )

        table.add_column(
            "Alternativa",
            style="bold yellow"
        )

        table.add_column(
            "VME",
            justify="center",
            style="bold green"
        )

        for alt, vme in self.resultados.items():

            table.add_row(
                alt,
                f"${vme:.2f}k"
            )

        console.print()
        console.print(table)

        panel = Panel.fit(
            f"[bold green]✅ Mejor decisión:[/bold green]\n\n"
            f"[bold white]{self.mejor_decision}[/bold white]",
            title="DECISIÓN ÓPTIMA",
            border_style="green",
            padding=(1, 5)
        )

        console.print()
        console.print(panel)

    # =================================================

    def animacion_carga(self):

        console.print()

        for _ in track(
            range(40),
            description="[bold cyan]Consultando IA Gemini..."
        ):
            time.sleep(0.03)

    # =================================================

    def consultar_gemini(self):

        self.mostrar_dashboard()

        self.animacion_carga()

        prompt_estructurado = self.generar_prompt()

        try:

            response = client.models.generate_content(
                model=self.modelo_id,
                contents=prompt_estructurado
            )

            markdown = Markdown(response.text)

            respuesta_panel = Panel(
                markdown,
                title="🤖 RESPUESTA DEL AGENTE IA (GEMINI)",
                border_style="magenta",
                padding=(1, 2),
                expand=False
            )

            console.print()
            console.print(respuesta_panel)

        except Exception as e:

            respuesta_demo = """
        # 📌 Análisis Ejecutivo

        ## 1. Explicación Estratégica

        - Desarrollo Interno posee el mayor Valor Monetario Esperado.
        - Representa mayor control tecnológico y escalabilidad.

        ## 2. Riesgos

        - Riesgo alto de inversión inicial.
        - Subcontratar reduce costos pero genera dependencia.
        - Comprar plataforma limita personalización.

        ## 3. Sensibilidad

        - Si aumenta la demanda baja al 60%,
        Desarrollo Interno pierde atractivo.

        - En ese escenario se recomienda:
        - Subcontratar
        - Implementar MVP
        - Reducir costos fijos

        ## 4. Mejoras

        - Aplicar Teorema de Bayes.
        - Implementar prueba piloto.
        - Calcular VEIP para reducir incertidumbre.
        """

            markdown = Markdown(respuesta_demo)

            panel_demo = Panel(
                markdown,
                title="🤖 RESPUESTA IA (MODO DEMO)",
                border_style="yellow",
                padding=(1, 2)
            )

            console.print(panel_demo)

            console.print(
                "\n[bold yellow]⚠ Gemini no disponible. Mostrando análisis de respaldo.[/bold yellow]"
            )

# =====================================================
# PORTADA
# =====================================================

def portada():

    f = Figlet(font='slant')

    titulo = f.renderText('Decision AI')

    console.print(
        f"[bold bright_cyan]{titulo}[/bold bright_cyan]"
    )

    subtitulo = Panel.fit(
        "[bold white]Sistema Inteligente de Árboles de Decisión[/bold white]\n"
        "[cyan]Investigación de Operaciones + Gemini AI[/cyan]",
        border_style="blue",
        padding=(1, 4)
    )

    console.print(Align.center(subtitulo))

# =====================================================
# MAIN
# =====================================================

alternativas = [
    'Desarrollo Interno',
    'Subcontratar',
    'Comprar Plataforma'
]

probabilidades = {
    'Alta': 0.6,
    'Baja': 0.4
}

pagos = {

    'Desarrollo Interno': {
        'Alta': 150,
        'Baja': -30
    },

    'Subcontratar': {
        'Alta': 120,
        'Baja': -10
    },

    'Comprar Plataforma': {
        'Alta': 100,
        'Baja': 20
    }
}

# =====================================================

portada()

modelo = ModeloArbolDecision(
    alternativas,
    probabilidades,
    pagos
)

resultados_vme, mejor_opcion = modelo.calcular_vme()

agente = AgenteIAGemini(
    resultados_vme,
    mejor_opcion,
    pagos,
    probabilidades
)

agente.consultar_gemini()