"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        MOTOR DE ASIGNACIÓN DINÁMICA DE CARTERAS POR OBJETIVOS (V3 - WEB)    ║
║                  Quantitative Wealth Management Engine                      ║
║                              v3.0 Streamlit                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import warnings
warnings.filterwarnings("ignore")

import math
import numpy as np
import pandas as pd
import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA (Debe ser lo primero)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quantum Wealth Engine",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS PERSONALIZADO: ESTÉTICA BANCA PRIVADA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Fondo principal — azul noche con textura sutil */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0d1428 50%, #0a1020 100%);
    color: #e8e4d9;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060c1a 0%, #0a1228 100%);
    border-right: 1px solid rgba(180,150,80,0.2);
}
[data-testid="stSidebar"] * {
    color: #d4c9a8 !important;
}
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stCheckbox label {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    color: #9a8f70 !important;
    text-transform: uppercase;
}

/* Header principal */
.qwe-header {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #f0e8cc;
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}
.qwe-subheader {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #7a8a6a;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Tarjetas de métricas personalizadas */
.metric-card {
    background: linear-gradient(135deg, rgba(20,28,50,0.9) 0%, rgba(15,22,40,0.95) 100%);
    border: 1px solid rgba(180,150,80,0.25);
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, rgba(180,150,80,0.8), rgba(180,150,80,0.1));
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #7a8a6a;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 600;
    color: #f0e8cc;
    line-height: 1;
}
.metric-delta {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    margin-top: 0.4rem;
}
.metric-positive { color: #6db88a; }
.metric-negative { color: #c8725a; }
.metric-neutral  { color: #8a9a7a; }

/* Secciones */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    font-weight: 600;
    color: #c8b87a;
    border-bottom: 1px solid rgba(180,150,80,0.2);
    padding-bottom: 0.5rem;
    margin: 1.8rem 0 1rem 0;
    letter-spacing: 0.02em;
}

/* Info boxes */
.info-box {
    background: rgba(20,28,50,0.7);
    border: 1px solid rgba(180,150,80,0.15);
    border-left: 3px solid rgba(180,150,80,0.7);
    border-radius: 4px;
    padding: 1rem 1.2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    color: #c8c0a8;
    line-height: 1.7;
    margin-bottom: 0.8rem;
}
.info-box.success {
    border-left-color: #6db88a;
}
.info-box.warning {
    border-left-color: #c8a05a;
}
.info-box.danger {
    border-left-color: #c8725a;
}

/* Tabla de fondos */
.stDataFrame {
    border: 1px solid rgba(180,150,80,0.15) !important;
    border-radius: 6px !important;
}

/* Botón principal */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #b4963e 0%, #8a7030 100%) !important;
    color: #0a0f1e !important;
    font-family: 'DM Mono', monospace !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 4px !important;
    padding: 0.75rem 1.5rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #c8aa52 0%, #9a8040 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(180,150,60,0.3) !important;
}

/* Ocultar los metrics nativos y usar los nuestros */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(20,28,50,0.9) 0%, rgba(15,22,40,0.95) 100%);
    border: 1px solid rgba(180,150,80,0.25);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    position: relative;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, rgba(180,150,80,0.8), rgba(180,150,80,0.1));
    border-radius: 8px 8px 0 0;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.68rem !important;
    color: #7a8a6a !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.9rem !important;
    color: #f0e8cc !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* Plot / Matplotlib */
.stPlotlyChart, [data-testid="stImage"] {
    border: 1px solid rgba(180,150,80,0.15);
    border-radius: 8px;
    overflow: hidden;
}

/* Divisor dorado */
.gold-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(180,150,80,0.4), transparent);
    margin: 1.5rem 0;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #b4963e !important;
}

/* Logo sidebar */
.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #c8b87a;
    padding: 1rem 0 0.5rem 0;
    border-bottom: 1px solid rgba(180,150,80,0.2);
    margin-bottom: 1.5rem;
}
.sidebar-logo span {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    display: block;
    color: #6a7a5a;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 🎛️ PANEL DE CONTROL PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

URL_CSV = "https://script.google.com/macros/s/AKfycbw0WVpDOtYfGsN1xPJSPAeEGEm-GDtxWg84z05JB89lO-uLT6Xy2qJO3fVJod60lB7-/exec"

PERIODO_MERCADO   = "max"
USAR_TILT_MERCADO = True
ACTIVAR_ROTACION_VALUE = True
UMBRAL_PER_CARO = 23.0

PESOS_RV  = {
    "RV_Global_Index": 0.60,
    "RV_Value": 0.20,
    "RV_Emergentes_Index": 0.20
}

GLIDEPATH_RF = {
    "Ultra-Conservador": {"RF_Monetaria": 1.00},
    "Conservador": {"RF_Corto_Plazo": 0.70, "RF_Flexible": 0.30},
    "Moderado": {"RF_Flexible": 0.40, "RF_Corto_Plazo": 0.40, "RF_Credito": 0.20},
    "Dinámico": {"RF_Flexible": 0.50, "RF_Credito": 0.40, "RF_Corto_Plazo": 0.10},
    "Agresivo": {"RF_Credito": 0.60, "RF_Flexible": 0.40, "RF_Largo_Plazo": 0},
}

GLIDEPATH_ALT = {
    "Conservador": {"ALT_Prudente": 1.00},
    "Moderado": {"ALT_Prudente": 0.50, "ALT_Multiestrategia": 0.50},
    "Dinámico": {"ALT_Multiestrategia": 0.55, "ALT_Flexible": 0.45},
    "Agresivo": {"ALT_Flexible": 0.60, "ALT_Multiestrategia": 0.40},
}

PESOS_ORO = {"Oro": 1.00}

LIMITE_CONCENTRACION_ACTIVA = 0.075
TOPE_MAXIMO_ORO             = 10.0
CAPITAL_MINIMO_ALT          = 75000.0
RATIO_AHORRO_ALT            = 50.0
MINIMO_RF_PARA_ALT          = 15.0
ALT_FUNDING_RATE            = 0.40
MAX_ALT_TOTAL               = 10.0
MINIMO_RF_RESERVA           = 5.0

TECHO_ALT_POR_PERFIL = {
    "Conservador": 5.0, "Moderado": 7.5, "Dinámico": 10.0, "Agresivo": 10.0,
}

MAX_RV_POR_RIESGO = {
    1: 0.0, 2: 10.0, 3: 25.0, 4: 40.0, 5: 50.0,
    6: 65.0, 7: 75.0, 8: 85.0, 9: 100.0, 10: 100.0
}

UMBRAL_MINIMO_MACRO = 3.0
RUTAS_BARRIDO = {"ALT": "RF", "ORO": None, "RF": "RV", "RV": "RF"}

RETORNO_NIVEL_1  = 2.0
RETORNO_NIVEL_10 = 8.0
VOLAT_NIVEL_1    = 0.5
VOLAT_NIVEL_10   = 16.0

REGLA_EDAD_BASE           = 120
TOLERANCIA_NEUTRAL        = 1
MULTIPLICADOR_PSICOLOGICO = 2.0

IMPACTO_AHORRO_ALTO   = 0.20
BONUS_RV_AHORRO_ALTO  = 10.0
IMPACTO_AHORRO_MEDIO  = 0.10
BONUS_RV_AHORRO_MEDIO = 5.0

UMBRAL_PANICO     = 20.0
TILT_PANICO       = 15.0
UMBRAL_CORRECCION = 10.0
TILT_CORRECCION   = 7.5
UMBRAL_REBACHE    = 5.0
TILT_REBACHE      = 2.5
DIAS_RALLY         = 252
UMBRAL_SOBRECOMPRA = 5.0
TILT_SOBRECOMPRA   = -2.5

MODO_PSICOLOGIA_MANDA = False
MAPA_RV_PSICOLOGICA = {1: 0.0, 2: 10.0, 3: 20.0, 4: 35.0, 5: 50.0, 6: 60.0, 7: 70.0, 8: 80.0, 9: 90.0, 10: 100.0}
EXENTOS_CONCENTRACION   = ["INDEX", "ORO"]
PROYECCION_RENTABILIDAD = 0.07
PROYECCION_HORIZONTES   = [5, 10, 15, 20, 25, 30]


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 1: PERFILADOR
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class PerfilInversor:
    edad: int
    capital_total: float
    necesidad_liquidez_corto_plazo: float
    ahorro_mensual: float
    quiere_aportar_mensual: bool
    quiere_oro: bool
    tolerancia_volatilidad: int
    porcentaje_oro_manual: float

    capital_blindado:   float = field(init=False)
    capital_invertible: float = field(init=False)
    perfil_texto:       str   = field(init=False)

    def __post_init__(self):
        self._validar_inputs()
        if not self.quiere_aportar_mensual:
            self.ahorro_mensual = 0.0
        self.capital_blindado   = self.necesidad_liquidez_corto_plazo
        self.capital_invertible = max(0.0, self.capital_total - self.capital_blindado)
        self.perfil_texto       = self._clasificar_perfil()

    def _validar_inputs(self):
        if not (18 <= self.edad <= 100): raise ValueError(f"Edad fuera de rango legal: {self.edad}.")
        if self.capital_total < 0: raise ValueError("El capital inicial no puede ser negativo.")
        if self.necesidad_liquidez_corto_plazo > self.capital_total:
            raise ValueError("La liquidez solicitada supera el patrimonio total.")
        if not (1 <= self.tolerancia_volatilidad <= 10):
            raise ValueError("La escala de riesgo debe ser entre 1 y 10.")

    def _clasificar_perfil(self) -> str:
        if self.tolerancia_volatilidad == 1: return "Ultra-Conservador"
        elif self.tolerancia_volatilidad <= 3: return "Conservador"
        elif self.tolerancia_volatilidad <= 6: return "Moderado"
        elif self.tolerancia_volatilidad <= 8: return "Dinámico"
        else: return "Agresivo"


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 2: MOTOR DE ASIGNACIÓN
# ─────────────────────────────────────────────────────────────────────────────
class MotorAsignacion:
    def __init__(self, perfil: PerfilInversor):
        self.perfil = perfil
        self.pct_monetario: float = 0.0
        self.pct_rv:        float = 0.0
        self.pct_rf:        float = 0.0
        self.pct_alt:       float = 0.0
        self.pct_oro:       float = 0.0

    def calcular_asignacion_base(self, drawdown_mercado: float = 0.0) -> dict:
        p  = self.perfil
        dd = abs(drawdown_mercado)

        self.pct_monetario = (p.capital_blindado / p.capital_total * 100 if p.capital_total > 0 else 0.0)
        oro = min(TOPE_MAXIMO_ORO, p.porcentaje_oro_manual) if p.quiere_oro else 0.0

        if MODO_PSICOLOGIA_MANDA:
            rv_base = MAPA_RV_PSICOLOGICA.get(p.tolerancia_volatilidad, 50.0)
            ajuste_psicologico = 0.0
        else:
            rv_base = max(0, REGLA_EDAD_BASE - p.edad)
            ajuste_psicologico = (p.tolerancia_volatilidad - TOLERANCIA_NEUTRAL) * MULTIPLICADOR_PSICOLOGICO

        tasa_ahorro_anual = (p.ahorro_mensual * 12) / p.capital_invertible if p.capital_invertible > 0 else float('inf')
        ajuste_flujos = 0.0
        if tasa_ahorro_anual >= IMPACTO_AHORRO_ALTO:    ajuste_flujos = BONUS_RV_AHORRO_ALTO
        elif tasa_ahorro_anual >= IMPACTO_AHORRO_MEDIO: ajuste_flujos = BONUS_RV_AHORRO_MEDIO

        rv_teorica = rv_base + ajuste_psicologico + ajuste_flujos

        tilt_tactico = 0.0
        if p.tolerancia_volatilidad > 2:
            if   dd >= UMBRAL_PANICO:     tilt_tactico = TILT_PANICO
            elif dd >= UMBRAL_CORRECCION: tilt_tactico = TILT_CORRECCION
            elif dd >= UMBRAL_REBACHE:    tilt_tactico = TILT_REBACHE
            elif dd < UMBRAL_SOBRECOMPRA: tilt_tactico = TILT_SOBRECOMPRA

        rv_con_tilt = rv_teorica + tilt_tactico
        techo_psicologico = MAX_RV_POR_RIESGO.get(p.tolerancia_volatilidad, 100.0)
        techo_rv = min(techo_psicologico, 100.0 - oro)
        rv_final = np.clip(rv_con_tilt, 0, techo_rv)
        rf_preliminar = max(0.0, 100.0 - rv_final - oro)

        alt = 0.0
        ratio_patrimonio_ahorro = (p.capital_invertible / p.ahorro_mensual) if p.ahorro_mensual > 0 else float('inf')
        condicion_rf      = rf_preliminar >= MINIMO_RF_PARA_ALT
        condicion_capital = p.capital_invertible >= CAPITAL_MINIMO_ALT
        condicion_ratio   = ratio_patrimonio_ahorro >= RATIO_AHORRO_ALT

        if condicion_rf or condicion_capital or condicion_ratio:
            rf_financiable = max(0.0, rf_preliminar - MINIMO_RF_RESERVA)
            transferencia_propuesta = rf_financiable * ALT_FUNDING_RATE
            techo_perfil = TECHO_ALT_POR_PERFIL.get(p.perfil_texto, 10.0)
            alt = min(transferencia_propuesta, techo_perfil, MAX_ALT_TOTAL)

        rf_final = rf_preliminar - alt

        if p.tolerancia_volatilidad <= 2:
            oro = 0.0
            alt = 0.0
            rf_final = 100.0 - rv_final

        pesos = {"RV": rv_final, "RF": rf_final, "ALT": alt, "ORO": oro}
        for cat in ["ALT", "ORO", "RF", "RV"]:
            destino = RUTAS_BARRIDO.get(cat)
            if destino is not None and 0 < pesos[cat] < UMBRAL_MINIMO_MACRO:
                pesos[destino] += pesos[cat]
                pesos[cat]      = 0.0

        self.pct_rv  = round(pesos["RV"],  1)
        self.pct_rf  = round(pesos["RF"],  1)
        self.pct_alt = round(pesos["ALT"], 1)
        self.pct_oro = round(pesos["ORO"], 1)

        return {
            "pct_rv": self.pct_rv, "pct_rf": self.pct_rf,
            "pct_alt": self.pct_alt, "pct_oro": self.pct_oro, "tilt_aplicado": tilt_tactico,
        }


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 3: ANALIZADOR DE MERCADO
# ─────────────────────────────────────────────────────────────────────────────
class AnalizadorMercado:
    TICKER_REFERENCIA = "^GSPC"
    TICKER_ETF_SPY = "SPY"

    def __init__(self):
        self.drawdown_actual: float = 0.0
        self.peor_caida_reciente: float = 0.0
        self.precio_actual:   float = 0.0
        self.precio_maximo:   float = 0.0
        self.tilt_rv:         float = 0.0
        self.descripcion_tilt: str  = "Sin ajuste táctico"
        self.datos_ok:        bool  = False
        self.per_mercado: float = 0.0
        self.mercado_sobrecomprado: bool = False

    def analizar(self) -> None:
        if not USAR_TILT_MERCADO:
            self.tilt_rv = 0.0
            self.descripcion_tilt = "Apagado por el Gestor (Asignación pura)"
            self.datos_ok = True
            return

        try:
            spx = yf.download(self.TICKER_REFERENCIA, period="5y", progress=False)
            cierre = spx["Close"].dropna()

            self.precio_actual = float(cierre.iloc[-1])
            self.precio_maximo = float(cierre.max())
            self.drawdown_actual = ((self.precio_actual - self.precio_maximo) / self.precio_maximo * 100)

            rolling_max = cierre.rolling(window=DIAS_RALLY, min_periods=1).max()
            drawdowns_historicos = (cierre - rolling_max) / rolling_max * 100
            self.peor_caida_reciente = abs(float(drawdowns_historicos.tail(DIAS_RALLY).min()))

            try:
                spy_info = yf.Ticker(self.TICKER_ETF_SPY).info
                self.per_mercado = spy_info.get('trailingPE', 0.0)
                if self.per_mercado and self.per_mercado > UMBRAL_PER_CARO:
                    self.mercado_sobrecomprado = True
            except Exception:
                pass

            self._aplicar_market_tilt()
            self.datos_ok = True

        except Exception as e:
            self.descripcion_tilt = f"Sin conexión al mercado: {e}"

    def _aplicar_market_tilt(self) -> None:
        dd = abs(self.drawdown_actual)

        if dd >= UMBRAL_PANICO:
            self.tilt_rv, self.descripcion_tilt = TILT_PANICO, f"🟢 Caída severa (>{UMBRAL_PANICO}%): +{TILT_PANICO}% RV — Máxima Oportunidad"
        elif dd >= UMBRAL_CORRECCION:
            self.tilt_rv, self.descripcion_tilt = TILT_CORRECCION, f"🟡 Caída moderada (>{UMBRAL_CORRECCION}%): +{TILT_CORRECCION}% RV"
        elif dd >= UMBRAL_REBACHE:
            self.tilt_rv, self.descripcion_tilt = TILT_REBACHE, f"🟡 Corrección menor (>{UMBRAL_REBACHE}%): +{TILT_REBACHE}% RV"
        elif self.peor_caida_reciente < UMBRAL_SOBRECOMPRA:
            self.tilt_rv, self.descripcion_tilt = TILT_SOBRECOMPRA, f"🔴 Rally Extremo (sin caídas >{UMBRAL_SOBRECOMPRA}% en 1 año): Toma de beneficios"
        else:
            self.tilt_rv, self.descripcion_tilt = 0.0, "⚪ Mercado Estable: Sin sesgo táctico activo"

        if self.mercado_sobrecomprado and ACTIVAR_ROTACION_VALUE:
            self.descripcion_tilt += f" | 🔄 PER={self.per_mercado:.1f}x — Rotando a VALUE"


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 4: LECTOR DE GOOGLE SHEETS
# ─────────────────────────────────────────────────────────────────────────────
class LectorColiseoCSV:
    def __init__(self, url_csv: str):
        self.url_csv = url_csv
        self.df_metricas = pd.DataFrame()
        self.ranking_categorias = {}

    def ejecutar(self) -> None:
        try:
            df = pd.read_csv(self.url_csv)
            df.columns = [c.strip() for c in df.columns]

            cols_num = ['Rentabilidad', 'Volatilidad', 'DRAWDOWN', 'Años_Hist', 'Confianza', 'Score_Final']
            for col in cols_num:
                if col in df.columns:
                    if df[col].dtype == object:
                        df[col] = df[col].str.replace(',', '.').str.replace('%', '')
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            self.df_metricas = df.dropna(subset=['Score_Final', 'Categoria'])

            if self.df_metricas.empty:
                raise ValueError("El CSV está vacío o sin columnas correctas.")

            categorias = self.df_metricas['Categoria'].unique()
            for cat in categorias:
                subset = self.df_metricas[self.df_metricas['Categoria'] == cat]
                self.ranking_categorias[cat] = subset.sort_values('Score_Final', ascending=False)

        except Exception as e:
            st.error(f"❌ Error leyendo Google Sheets: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# MÓDULO 5: CONSTRUCCIÓN DE CARTERA
# ─────────────────────────────────────────────────────────────────────────────
class ConstruccionCartera:
    def __init__(self, perfil, asignador, mercado, scoring):
        self.perfil    = perfil
        self.asignador = asignador
        self.mercado   = mercado
        self.scoring   = scoring
        self.distribucion: dict = {}
        self.mandato_retorno = 0.0
        self.mandato_volat   = 0.0
        self.target_real_retorno = 0.0

    def construir(self) -> None:
        p, a = self.perfil, self.asignador
        self.pct_rv_final, self.pct_rf_final = a.pct_rv, a.pct_rf
        self.pct_alt_final, self.pct_oro = a.pct_alt, a.pct_oro

        ci = p.capital_invertible
        self.capital_rv  = ci * self.pct_rv_final  / 100
        self.capital_rf  = ci * self.pct_rf_final  / 100
        self.capital_alt = ci * self.pct_alt_final / 100
        self.capital_oro = ci * self.pct_oro       / 100

        self._distribuir_por_activo()
        self.calcular_expectativas_tier1()

    def calcular_expectativas_tier1(self) -> None:
        riesgo = self.perfil.tolerancia_volatilidad
        self.mandato_retorno = RETORNO_NIVEL_1 + (riesgo - 1) * (RETORNO_NIVEL_10 - RETORNO_NIVEL_1) / 9
        self.mandato_volat   = VOLAT_NIVEL_1 + (riesgo - 1) * (VOLAT_NIVEL_10 - VOLAT_NIVEL_1) / 9

        w_rv  = self.pct_rv_final  / 100
        w_alt = self.pct_alt_final / 100
        w_oro = self.pct_oro       / 100

        if riesgo == 1:
            w_rf  = 0.0
            w_liq = max(0, 1.0 - (w_rv + w_alt + w_oro))
        else:
            w_rf  = self.pct_rf_final / 100
            w_liq = max(0, 1.0 - (w_rv + w_rf + w_alt + w_oro))

        self.target_real_retorno = (w_rv * 8.0) + (w_rf * 3.5) + (w_alt * 5.0) + (w_oro * 4.5) + (w_liq * 2.5)

    def _distribuir_por_activo(self) -> None:
        perfil_texto = self.perfil.perfil_texto
        rankings     = self.scoring.ranking_categorias
        am, ci       = self.perfil.ahorro_mensual, self.perfil.capital_invertible
        pesos_rf_activos  = GLIDEPATH_RF.get(perfil_texto, GLIDEPATH_RF["Moderado"])
        pesos_alt_activos = GLIDEPATH_ALT.get(perfil_texto, GLIDEPATH_ALT["Moderado"])

        pesos_rv_actuales = PESOS_RV.copy()
        if ACTIVAR_ROTACION_VALUE and self.mercado and self.mercado.datos_ok and self.mercado.mercado_sobrecomprado:
            if "RV_Global_Index" in pesos_rv_actuales:
                pesos_rv_actuales["RV_Global_Index"]     = 0.45
                pesos_rv_actuales["RV_Value"]            = 0.30
                pesos_rv_actuales["RV_Emergentes_Index"] = 0.25

        def asignar_pesos_manuales(diccionario_pesos, capital_clase, ahorro_clase, etiqueta_clase):
            for cat_m, peso in diccionario_pesos.items():
                if cat_m not in rankings:
                    cat_f = self._buscar_fallback(cat_m, rankings)
                    if cat_f is None: continue
                    df_cat, cat_final = rankings[cat_f], cat_f
                else:
                    df_cat, cat_final = rankings[cat_m], cat_m

                imp_cat = capital_clase * peso
                ahr_cat = ahorro_clase * peso
                if imp_cat <= 0: continue
                es_exento = any(p in cat_final.upper() for p in EXENTOS_CONCENTRACION)
                tope = ci * 1.0 if es_exento else ci * LIMITE_CONCENTRACION_ACTIVA
                n_fondos = math.ceil(imp_cat / tope) if tope > 0 else 1
                n_fondos_r = min(n_fondos, len(df_cat))
                if n_fondos_r == 0: continue
                imp_f, ahr_f = imp_cat / n_fondos_r, ahr_cat / n_fondos_r
                mejores = df_cat.head(n_fondos_r)
                for _, f in mejores.iterrows():
                    ticker = str(f.get('Ticker', 'N/A'))
                    while ticker in self.distribucion: ticker += "*"
                    self.distribucion[ticker] = {
                        "Nombre": str(f.get('Nombre', 'Desconocido')),
                        "Categoría": cat_final,
                        "Clase": etiqueta_clase,
                        "Rent_%": f.get('Rentabilidad', 0.0),
                        "Vol_%": f.get('Volatilidad', 0.0),
                        "Años": f.get('Años_Hist', 0.0),
                        "Score": f.get('Score_Final', 0.0),
                        "Importe_€": round(imp_f, 2),
                        "Ahorro_€": round(ahr_f, 2),
                    }

        asignar_pesos_manuales(PESOS_ORO,         self.capital_oro, am * self.pct_oro       / 100, "ORO")
        asignar_pesos_manuales(pesos_rv_actuales,  self.capital_rv,  am * self.pct_rv_final  / 100, "RV")
        asignar_pesos_manuales(pesos_alt_activos,  self.capital_alt, am * self.pct_alt_final / 100, "ALT")
        asignar_pesos_manuales(pesos_rf_activos,   self.capital_rf,  am * self.pct_rf_final  / 100, "RF")

    def _buscar_fallback(self, categoria: str, rankings: dict) -> Optional[str]:
        pref_f = {"ALT_": ["Alternativo", "ALT"], "RF_": ["RF_Flexible", "RF_Mixta", "RF_Largo_Plazo"]}
        for pref, cand in pref_f.items():
            if categoria.startswith(pref):
                for c in cand:
                    if c in rankings: return c
        return None

    def proyeccion_patrimonial(self) -> pd.DataFrame:
        r  = self.target_real_retorno / 100
        ci = self.perfil.capital_invertible
        am = self.perfil.ahorro_mensual * 12
        filas = []
        for años in PROYECCION_HORIZONTES:
            pat = (ci * (1+r)**años + am * ((1+r)**años - 1)/r) if r > 0 else (ci + am*años)
            filas.append({
                "Horizonte": f"{años} años",
                "Patrimonio Proyectado (€)": round(pat, 2),
                "Multiplicador (x)": round(pat / self.perfil.capital_total, 2),
            })
        return pd.DataFrame(filas).set_index("Horizonte")

    def generar_figura_expectativas(self):
        """Devuelve la figura de matplotlib para st.pyplot()"""
        try:
            hist = yf.download("URTH", period="3y", progress=False)['Close'].dropna()
            if hist.empty:
                return None

            hist_norm = (hist / hist.iloc[0]) * 100
            ultimo_precio = float(hist_norm.iloc[-1])
            ultima_fecha  = hist_norm.index[-1]
            fechas_futuras = pd.date_range(start=ultima_fecha, periods=252, freq='B')

            tasa_diaria_mercado = (1 + (RETORNO_NIVEL_10 / 100)) ** (1/252) - 1
            tasa_diaria_cartera = (1 + (self.target_real_retorno / 100)) ** (1/252) - 1

            proy_mercado = ultimo_precio * (1 + tasa_diaria_mercado) ** np.arange(252)
            proy_cartera = ultimo_precio * (1 + tasa_diaria_cartera) ** np.arange(252)

            # Estilo oscuro coherente
            fig, ax = plt.subplots(figsize=(11, 4.5))
            fig.patch.set_facecolor('#0a0f1e')
            ax.set_facecolor('#0d1428')

            ax.plot(hist_norm.index, hist_norm,
                    label="Histórico MSCI World (URTH)", color='#5a6a8a', linewidth=1.5, alpha=0.8)
            ax.plot(fechas_futuras, proy_mercado,
                    label=f"Bolsa Global 100% RV: {RETORNO_NIVEL_10:.1f}% anual",
                    color='#c8725a', linestyle='--', linewidth=1.8)
            ax.plot(fechas_futuras, proy_cartera,
                    label=f"Su Cartera (R{self.perfil.tolerancia_volatilidad}): {self.target_real_retorno:.2f}% anual",
                    color='#b4963e', linewidth=2.8)

            ax.axvline(x=ultima_fecha, color='#c8c0a8', linestyle=':', linewidth=1.5, alpha=0.6)
            ymin, ymax = ax.get_ylim()
            ax.text(ultima_fecha, ymin + (ymax-ymin)*0.05, '  HOY',
                    rotation=90, color='#c8c0a8', fontsize=8, alpha=0.7,
                    fontfamily='monospace', verticalalignment='bottom')

            ax.set_title(
                f"Evolución y Contrato de Expectativas a 1 Año — Perfil {self.perfil.perfil_texto}",
                fontsize=11, color='#f0e8cc', fontweight='bold', pad=14
            )
            ax.set_ylabel("Base 100", color='#7a8a6a', fontsize=9)
            ax.tick_params(colors='#7a8a6a', labelsize=8)
            for spine in ax.spines.values():
                spine.set_edgecolor('#1a2440')
            ax.grid(True, linestyle='--', alpha=0.15, color='#c8c0a8')

            legend = ax.legend(loc="upper left", fontsize=8.5, framealpha=0.3,
                               facecolor='#0a0f1e', edgecolor='#3a4460', labelcolor='#c8c0a8')

            fig.tight_layout(pad=1.5)
            return fig

        except Exception:
            return None


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR: INPUTS DEL CLIENTE
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sidebar-logo">
            🏦 Quantum Wealth<br>
            <span>Motor de Asignación v3.0</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("**DATOS DEL INVERSOR**")

    edad = st.slider("Edad", min_value=18, max_value=90, value=45, step=1)
    tolerancia = st.slider("Tolerancia al Riesgo (1–10)", min_value=1, max_value=10, value=6, step=1)

    st.markdown("---")
    st.markdown("**PATRIMONIO**")

    capital_total = st.number_input(
        "Capital Total (€)", min_value=0.0, value=100_000.0, step=5_000.0, format="%.2f"
    )
    liquidez = st.number_input(
        "Liquidez Reservada / Emergencia (€)", min_value=0.0, value=10_000.0, step=1_000.0, format="%.2f"
    )

    st.markdown("---")
    st.markdown("**FLUJOS DE CAJA**")

    quiere_aportar = st.checkbox("¿Aportaciones periódicas?", value=True)
    ahorro_mensual = 0.0
    if quiere_aportar:
        ahorro_mensual = st.number_input(
            "Ahorro Mensual (€)", min_value=0.0, value=500.0, step=100.0, format="%.2f"
        )

    st.markdown("---")
    st.markdown("**ACTIVOS REFUGIO**")

    quiere_oro = st.checkbox("¿Incluir Oro (ETC Físico)?", value=False)
    pct_oro_manual = 0.0
    if quiere_oro:
        pct_oro_manual = st.slider("% Oro sobre cartera", min_value=0.0, max_value=10.0, value=5.0, step=0.5)

    st.markdown("---")

    ejecutar = st.button("🚀 Ejecutar Motor de Asignación", type="primary")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN AREA: HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="qwe-header">Motor de Asignación Dinámica de Carteras</div>
    <div class="qwe-subheader">Quantitative Wealth Management Engine — v3.0 · Conectado a Google Sheets</div>
    <div class="gold-divider"></div>
""", unsafe_allow_html=True)

if not ejecutar:
    # Estado de reposo: instrucciones
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
            <div class="info-box">
                <strong>Bienvenido al Motor Cuantitativo de Carteras.</strong><br><br>
                Configure los parámetros de su cliente en el menú lateral y pulse
                <strong>🚀 Ejecutar Motor de Asignación</strong> para generar la propuesta
                de inversión institucional.
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="info-box">
                <strong>El motor integra tres capas de análisis:</strong><br><br>
                📐 <strong>Ciclo de vida</strong> — Regla de la edad y psicometría de riesgo<br>
                📡 <strong>Market timing</strong> — Drawdown en tiempo real del S&amp;P 500<br>
                🏆 <strong>El Coliseo</strong> — Ranking cuantitativo de fondos vía Google Sheets
            </div>
        """, unsafe_allow_html=True)

else:
    # ─────────────────────────────────────────────────────────────────────────
    # EJECUCIÓN DEL MOTOR
    # ─────────────────────────────────────────────────────────────────────────
    with st.spinner("Analizando mercado y construyendo cartera..."):

        # 1. Perfil
        try:
            perfil = PerfilInversor(
                edad=edad,
                capital_total=capital_total,
                necesidad_liquidez_corto_plazo=liquidez,
                ahorro_mensual=ahorro_mensual,
                quiere_aportar_mensual=quiere_aportar,
                quiere_oro=quiere_oro,
                tolerancia_volatilidad=tolerancia,
                porcentaje_oro_manual=pct_oro_manual,
            )
        except ValueError as ve:
            st.error(f"Error en los datos del cliente: {ve}")
            st.stop()

        # 2. Mercado
        mercado = AnalizadorMercado()
        mercado.analizar()

        # 3. Asignación
        asignador = MotorAsignacion(perfil)
        asignador.calcular_asignacion_base(mercado.drawdown_actual)

        # 4. Scoring (Google Sheets)
        scoring = LectorColiseoCSV(URL_CSV)
        scoring.ejecutar()

        if scoring.df_metricas.empty:
            st.error("No se pudieron cargar los fondos del Coliseo. Revisa la URL del Google Sheets.")
            st.stop()

        # 5. Construcción
        cartera = ConstruccionCartera(perfil, asignador, mercado, scoring)
        cartera.construir()

    # ─────────────────────────────────────────────────────────────────────────
    # KPI ROW
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown(f"<div class='section-title'>📊 Indicadores Clave — {datetime.now().strftime('%d/%m/%Y %H:%M')}</div>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    dd_val = mercado.drawdown_actual if mercado.datos_ok else 0.0
    dd_delta = "Bear Market 🔴" if abs(dd_val) >= 20 else ("Corrección 🟡" if abs(dd_val) >= 10 else "Estable ⚪")

    with k1:
        st.metric(
            label="Drawdown S&P 500",
            value=f"{dd_val:.2f}%",
            delta=dd_delta,
            delta_color="off"
        )
    with k2:
        st.metric(
            label="Capital Invertible",
            value=f"{perfil.capital_invertible:,.0f} €",
            delta=f"Blindado: {perfil.capital_blindado:,.0f} €",
            delta_color="off"
        )
    with k3:
        st.metric(
            label="Renta Variable",
            value=f"{cartera.pct_rv_final:.1f}%",
            delta=f"Renta Fija: {cartera.pct_rf_final:.1f}%",
            delta_color="off"
        )
    with k4:
        alfa = cartera.target_real_retorno - cartera.mandato_retorno
        st.metric(
            label="Retorno Real Esperado",
            value=f"{cartera.target_real_retorno:.2f}%",
            delta=f"Alfa vs Mandato: {alfa:+.2f}%",
            delta_color="normal"
        )

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # RESUMEN PERFIL + MERCADO
    # ─────────────────────────────────────────────────────────────────────────
    col_perfil, col_mercado = st.columns(2)

    with col_perfil:
        st.markdown("<div class='section-title'>👤 Perfil del Inversor</div>", unsafe_allow_html=True)
        color_perfil = "success" if tolerancia <= 4 else ("warning" if tolerancia <= 7 else "danger")
        st.markdown(f"""
            <div class="info-box {color_perfil}">
                <strong>{perfil.perfil_texto}</strong> · Riesgo {tolerancia}/10 · {edad} años<br><br>
                🏛️ Capital total: <strong>{capital_total:,.2f} €</strong><br>
                📈 Capital en cartera: <strong>{perfil.capital_invertible:,.2f} €</strong><br>
                🔒 Liquidez blindada: <strong>{perfil.capital_blindado:,.2f} €</strong><br>
                💳 Ahorro mensual: <strong>{perfil.ahorro_mensual:,.2f} €/mes</strong>
            </div>
        """, unsafe_allow_html=True)

        # Mandato de expectativas
        st.markdown(f"""
            <div class="info-box">
                <strong>🎯 Contrato de Expectativas — Nivel {tolerancia}</strong><br><br>
                📋 Mandato teórico (perfil): <strong>{cartera.mandato_retorno:.2f}%</strong> anual<br>
                ✅ Retorno real de la cartera: <strong>{cartera.target_real_retorno:.2f}%</strong> anual<br>
                📊 Volatilidad target: <strong>{cartera.mandato_volat:.2f}%</strong>
            </div>
        """, unsafe_allow_html=True)

    with col_mercado:
        st.markdown("<div class='section-title'>📡 Diagnóstico del Mercado</div>", unsafe_allow_html=True)
        if mercado.datos_ok:
            per_txt = f"PER S&P 500: <strong>{mercado.per_mercado:.1f}x</strong> {'⚠️ Caro' if mercado.mercado_sobrecomprado else '✅ Neutral'}<br>" if mercado.per_mercado > 0 else ""
            st.markdown(f"""
                <div class="info-box {'warning' if mercado.tilt_rv < 0 else 'success' if mercado.tilt_rv > 0 else ''}">
                    <strong>S&P 500 — Análisis Táctico</strong><br><br>
                    📉 Drawdown actual: <strong>{mercado.drawdown_actual:.2f}%</strong><br>
                    🎯 Sesgo táctico: <strong>{mercado.tilt_rv:+.1f}% RV</strong><br>
                    {per_txt}
                    <br>🔍 {mercado.descripcion_tilt}
                </div>
            """, unsafe_allow_html=True)

            # Asignación macro
            alloc_data = {
                "Clase de Activo": ["📈 Renta Variable", "🛡️ Renta Fija", "🪙 Alternativos", "🏅 Oro"],
                "Peso (%)": [cartera.pct_rv_final, cartera.pct_rf_final, cartera.pct_alt_final, cartera.pct_oro],
                "Capital (€)": [cartera.capital_rv, cartera.capital_rf, cartera.capital_alt, cartera.capital_oro],
            }
            df_alloc = pd.DataFrame(alloc_data)
            df_alloc = df_alloc[df_alloc["Peso (%)"] > 0]
            st.dataframe(
                df_alloc.style
                    .format({"Peso (%)": "{:.1f}%", "Capital (€)": "{:,.2f} €"})
                    .set_properties(**{"background-color": "#0d1428", "color": "#e8e4d9"}),
                hide_index=True,
                use_container_width=True,
            )
        else:
            st.markdown('<div class="info-box warning">⚠️ Datos de mercado no disponibles. Se aplicó asignación estratégica pura.</div>', unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TABLA DE CAMPEONES
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>🏆 Los Campeones — Composición Final de la Cartera</div>", unsafe_allow_html=True)

    if cartera.distribucion:
        filas_cartera = []
        total_importe = 0.0
        total_ahorro  = 0.0
        for ticker, info in sorted(cartera.distribucion.items(), key=lambda x: x[1]["Clase"]):
            filas_cartera.append({
                "Clase": info["Clase"],
                "Categoría": info["Categoría"],
                "Fondo / Nombre": info["Nombre"],
                "Años Hist.": info["Años"],
                "Score": info["Score"],
                "Invertir (€)": info["Importe_€"],
                "Aportación Mensual (€)": info["Ahorro_€"],
            })
            total_importe += info["Importe_€"]
            total_ahorro  += info["Ahorro_€"]

        df_cartera = pd.DataFrame(filas_cartera)

        # Colores por clase
        def color_clase(val):
            mapa = {
                "RV":  "background-color: rgba(109,184,138,0.15); color: #6db88a",
                "RF":  "background-color: rgba(90,106,138,0.15); color: #8aa0c8",
                "ALT": "background-color: rgba(180,150,80,0.15); color: #c8aa52",
                "ORO": "background-color: rgba(200,160,90,0.15); color: #d4a852",
            }
            return mapa.get(val, "")

        styled = (
            df_cartera.style
            .format({
                "Años Hist.": "{:.1f}",
                "Score": "{:.2f}",
                "Invertir (€)": "{:,.2f} €",
                "Aportación Mensual (€)": "{:,.2f} €",
            })
            .applymap(color_clase, subset=["Clase"])
            .set_properties(**{"background-color": "#0d1428", "color": "#e8e4d9", "font-size": "13px"})
        )

        st.dataframe(styled, hide_index=True, use_container_width=True, height=min(400, 55 + len(df_cartera) * 38))

        # Totales
        col_t1, col_t2, col_t3 = st.columns([3, 1, 1])
        with col_t2:
            st.metric("Total Invertido", f"{total_importe:,.2f} €")
        with col_t3:
            st.metric("Aportación Mensual", f"{total_ahorro:,.2f} €")

    else:
        st.markdown('<div class="info-box warning">⚠️ No se generó distribución. Revisa los nombres de categorías en Google Sheets.</div>', unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # PROYECCIÓN PATRIMONIAL + GRÁFICO
    # ─────────────────────────────────────────────────────────────────────────
    col_proy, col_graf = st.columns([1, 2])

    with col_proy:
        st.markdown("<div class='section-title'>📈 Proyección Patrimonial</div>", unsafe_allow_html=True)
        df_proy = cartera.proyeccion_patrimonial()
        st.dataframe(
            df_proy.style
                .format({
                    "Patrimonio Proyectado (€)": "{:,.2f} €",
                    "Multiplicador (x)": "{:.2f}x"
                })
                .bar(subset=["Patrimonio Proyectado (€)"], color="rgba(180,150,80,0.35)")
                .set_properties(**{"background-color": "#0d1428", "color": "#e8e4d9"}),
            use_container_width=True,
        )
        st.caption(f"Tasa de capitalización: {cartera.target_real_retorno:.2f}% anual · Incluye aportaciones periódicas")

    with col_graf:
        st.markdown("<div class='section-title'>📊 Contrato de Expectativas vs Mercado</div>", unsafe_allow_html=True)
        with st.spinner("Descargando datos históricos del MSCI World..."):
            fig = cartera.generar_figura_expectativas()
        if fig is not None:
            st.pyplot(fig, use_container_width=True)
        else:
            st.markdown('<div class="info-box warning">⚠️ No se pudo generar el gráfico de expectativas (sin datos históricos).</div>', unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-family: DM Mono, monospace; font-size: 0.7rem; color: #4a5a4a; text-align: center; padding: 1rem 0;'>"
        f"Quantum Wealth Engine v3.0 · Informe generado {datetime.now().strftime('%d/%m/%Y a las %H:%M')} · "
        f"Solo para uso interno del gestor · No constituye asesoramiento financiero regulado"
        f"</div>",
        unsafe_allow_html=True
    )
