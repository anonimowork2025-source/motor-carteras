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
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── RESET Y BASE ─────────────────────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0B0F19 !important;
    color: #F8FAFC;
}

/* ── FONDO PRINCIPAL con gradiente sutil ──────────────────────────────────── */
.stApp {
    background: radial-gradient(ellipse 80% 50% at 50% -10%,
                rgba(99,102,241,0.08) 0%, transparent 70%),
                #0B0F19 !important;
}

/* ── SIDEBAR ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0F1623 !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stCheckbox label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 400;
    letter-spacing: 0.06em;
    color: #64748B !important;
    text-transform: uppercase;
}

/* ── SLIDER: track y thumb ────────────────────────────────────────────────── */
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[role="slider"] {
    background-color: #6366F1 !important;
    border-color: #6366F1 !important;
}

/* ── BOTÓN PRINCIPAL ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.02em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    width: 100% !important;
    margin-top: 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.25) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.40) !important;
}
[data-testid="stSidebar"] .stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── HEADER PRINCIPAL ─────────────────────────────────────────────────────── */
.qwe-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 0.25rem;
}
.qwe-subheader {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── CARDS / MÉTRICAS ─────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #1E293B !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 16px !important;
    padding: 1.4rem 1.6rem !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.4), 0 0 0 0px rgba(99,102,241,0) !important;
    transition: box-shadow 0.2s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.5), 0 0 0 1px rgba(99,102,241,0.2) !important;
}
[data-testid="stMetric"]::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(99,102,241,0.6) 30%,
        rgba(139,92,246,0.4) 70%,
        transparent);
}
[data-testid="stMetricLabel"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.67rem !important;
    font-weight: 400 !important;
    color: #64748B !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    color: #F8FAFC !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.73rem !important;
    font-weight: 500 !important;
}

/* ── SECTION TITLES ───────────────────────────────────────────────────────── */
.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    padding-bottom: 0.75rem;
    margin: 1.8rem 0 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

/* ── INFO BOXES ───────────────────────────────────────────────────────────── */
.info-box {
    background: #1E293B;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.875rem;
    color: #CBD5E1;
    line-height: 1.75;
    margin-bottom: 0.75rem;
}
.info-box strong { color: #F8FAFC; font-weight: 600; }
.info-box.success { border-left: 3px solid #10B981; }
.info-box.warning { border-left: 3px solid #F59E0B; }
.info-box.danger  { border-left: 3px solid #EF4444; }
.info-box.purple  { border-left: 3px solid #8B5CF6; }

/* ── DATAFRAMES ───────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    background-color: #1E293B !important;
}
[data-testid="stDataFrame"] thead tr th {
    background-color: #162032 !important;
    color: #64748B !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stDataFrame"] tbody tr td {
    color: #CBD5E1 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.83rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.03) !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background-color: rgba(99,102,241,0.06) !important;
}

/* ── DIVIDER ──────────────────────────────────────────────────────────────── */
.neo-divider {
    height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(99,102,241,0.25) 30%,
        rgba(139,92,246,0.15) 70%,
        transparent 100%);
    margin: 1.75rem 0;
    border: none;
}

/* ── SIDEBAR LOGO ─────────────────────────────────────────────────────────── */
.sidebar-logo {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #F8FAFC;
    padding: 0.75rem 0 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 1.5rem;
    letter-spacing: -0.01em;
}
.sidebar-logo span {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    display: block;
    color: #475569;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.25rem;
    font-weight: 400;
}

/* ── SPINNER ──────────────────────────────────────────────────────────────── */
.stSpinner > div { border-top-color: #6366F1 !important; }

/* ── CAPTION / FOOTER TEXT ────────────────────────────────────────────────── */
.stCaption, [data-testid="stCaptionContainer"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    color: #475569 !important;
}

/* ── TOAST ────────────────────────────────────────────────────────────────── */
[data-testid="stToast"] {
    background-color: #1E293B !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    color: #CBD5E1 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── SUCCESS / WARNING / ERROR nativos de Streamlit ──────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.85rem !important;
}

/* ── EXPANDER ─────────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #1E293B !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
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


import requests

# ─── SESIÓN Y CACHÉ DE MERCADO (Evita bloqueos de Yahoo Finance) ─────────────
def _crear_sesion_navegador() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    })
    return session

@st.cache_data(ttl=900)
def _descargar_historico_spx(periodo: str) -> pd.DataFrame:
    try:
        ticker_obj = yf.Ticker("^GSPC")
        ticker_obj._session = _crear_sesion_navegador()
        hist = ticker_obj.history(period=periodo)
        if hist.empty: return pd.DataFrame()
        return hist[["Close"]].dropna()
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=900)
def _descargar_historico_urth(periodo: str) -> pd.DataFrame:
    try:
        ticker_obj = yf.Ticker("URTH")
        ticker_obj._session = _crear_sesion_navegador()
        hist = ticker_obj.history(period=periodo)
        if hist.empty: return pd.DataFrame()
        return hist[["Close"]].dropna()
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def _descargar_per_spy() -> float:
    try:
        ticker_obj = yf.Ticker("SPY")
        ticker_obj._session = _crear_sesion_navegador()
        per = ticker_obj.fast_info.get("trailingPE", None)
        if per is None:
            info = ticker_obj.info
            per  = info.get("trailingPE", 0.0)
        return float(per) if per else 0.0
    except Exception as e:
        return 0.0
# ─────────────────────────────────────────────────────────────────────────────


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

        hist_df = _descargar_historico_spx("5y")
        
        if hist_df.empty:
            self.descripcion_tilt = "Sin datos de mercado — asignación estratégica pura"
            self.datos_ok = False
            st.toast("⚠️ Yahoo Finance bloqueó la petición del S&P 500.", icon="📡")
            return

        cierre = hist_df["Close"]
        self.precio_actual   = float(cierre.iloc[-1])
        self.precio_maximo   = float(cierre.max())
        self.drawdown_actual = (self.precio_actual - self.precio_maximo) / self.precio_maximo * 100

        rolling_max = cierre.rolling(window=DIAS_RALLY, min_periods=1).max()
        drawdowns_hist = (cierre - rolling_max) / rolling_max * 100
        self.peor_caida_reciente = abs(float(drawdowns_hist.tail(DIAS_RALLY).min()))

        self.per_mercado = _descargar_per_spy()
        if self.per_mercado and self.per_mercado > UMBRAL_PER_CARO:
            self.mercado_sobrecomprado = True

        self._aplicar_market_tilt()
        self.datos_ok = True

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
        """
        Devuelve (fig, error_msg).
        Estética Fintech: fondo transparente, sin spines, grid horizontal tenue,
        líneas vibrantes con glow suave.
        """
        hist_df = _descargar_historico_urth("3y")

        if hist_df.empty:
            return None, (
                "Yahoo Finance no devolvió datos históricos del MSCI World (URTH). "
                "El gráfico no puede generarse."
            )

        try:
            cierre    = hist_df["Close"]
            hist_norm = (cierre / cierre.iloc[0]) * 100

            ultimo_precio  = float(hist_norm.iloc[-1])
            ultima_fecha   = hist_norm.index[-1]
            fechas_futuras = pd.date_range(start=ultima_fecha, periods=252, freq='B')

            tasa_diaria_mercado = (1 + RETORNO_NIVEL_10         / 100) ** (1/252) - 1
            tasa_diaria_cartera = (1 + self.target_real_retorno / 100) ** (1/252) - 1

            proy_mercado = ultimo_precio * (1 + tasa_diaria_mercado) ** np.arange(252)
            proy_cartera = ultimo_precio * (1 + tasa_diaria_cartera) ** np.arange(252)

            # ── LIENZO ────────────────────────────────────────────────────────────
            BG        = "#0B0F19"   # Idéntico al fondo de la app
            CARD_BG   = "#1E293B"
            COLOR_SPX = "#475569"   # Gris azulado — histórico
            COLOR_RV  = "#EF4444"   # Rojo coral — Bolsa pura (referencia de riesgo)
            COLOR_CAR = "#6366F1"   # Índigo eléctrico — Su cartera
            TEXT_DIM  = "#475569"
            TEXT_MED  = "#94A3B8"

            fig, ax = plt.subplots(figsize=(11, 4.2))
            fig.patch.set_facecolor(BG)
            ax.set_facecolor(BG)

            # Eliminar todos los spines
            for spine in ax.spines.values():
                spine.set_visible(False)

            # Grid horizontal únicamente, muy tenue
            ax.yaxis.grid(True,  linestyle='--', linewidth=0.5,
                          color='rgba(255,255,255,0.04)', alpha=0.6)
            ax.xaxis.grid(False)
            ax.set_axisbelow(True)

            # ── LÍNEAS ────────────────────────────────────────────────────────────
            # Histórico (área rellena sutil)
            ax.fill_between(hist_norm.index, hist_norm,
                            alpha=0.06, color=COLOR_SPX)
            ax.plot(hist_norm.index, hist_norm,
                    label="Histórico MSCI World",
                    color=COLOR_SPX, linewidth=1.5, alpha=0.7)

            # Proyección Bolsa pura — referencia de riesgo
            ax.plot(fechas_futuras, proy_mercado,
                    label=f"Bolsa Global (100% RV): {RETORNO_NIVEL_10:.0f}% anual",
                    color=COLOR_RV, linestyle='--', linewidth=2.0, alpha=0.8)

            # Proyección Cartera — protagonista
            ax.fill_between(fechas_futuras, proy_cartera,
                            alpha=0.08, color=COLOR_CAR)
            ax.plot(fechas_futuras, proy_cartera,
                    label=f"Su Cartera (R{self.perfil.tolerancia_volatilidad}): "
                          f"{self.target_real_retorno:.2f}% anual",
                    color=COLOR_CAR, linewidth=2.8)

            # Punto final de la cartera destacado
            ax.scatter([fechas_futuras[-1]], [proy_cartera[-1]],
                       color=COLOR_CAR, s=60, zorder=5, linewidth=0)

            # Línea vertical HOY
            ax.axvline(x=ultima_fecha,
                       color='rgba(255,255,255,0.15)', linestyle=':', linewidth=1.2)
            ymin, ymax = ax.get_ylim()
            ax.text(ultima_fecha, ymin + (ymax - ymin) * 0.04, "  HOY",
                    rotation=90, color=TEXT_DIM, fontsize=7.5,
                    fontfamily='monospace', verticalalignment='bottom')

            # ── ETIQUETAS FINALES (precio objetivo) ───────────────────────────────
            ax.annotate(
                f"  {proy_cartera[-1]:.0f}",
                xy=(fechas_futuras[-1], proy_cartera[-1]),
                color=COLOR_CAR, fontsize=8.5, fontweight='bold',
                fontfamily='monospace', va='center'
            )
            ax.annotate(
                f"  {proy_mercado[-1]:.0f}",
                xy=(fechas_futuras[-1], proy_mercado[-1]),
                color=COLOR_RV, fontsize=7.5,
                fontfamily='monospace', va='center', alpha=0.8
            )

            # ── ESTILOS DE EJES ───────────────────────────────────────────────────
            ax.set_title(
                f"Contrato de Expectativas — Perfil {self.perfil.perfil_texto}  "
                f"(Riesgo {self.perfil.tolerancia_volatilidad}/10)",
                fontsize=10.5, color='#94A3B8', fontweight='600',
                loc='left', pad=12
            )
            ax.set_ylabel("Base 100", color=TEXT_DIM, fontsize=8)
            ax.tick_params(axis='both', colors=TEXT_DIM, labelsize=7.5, length=0)
            ax.yaxis.set_tick_params(pad=6)

            # Leyenda
            legend = ax.legend(
                loc="upper left", fontsize=8, framealpha=0,
                labelcolor=TEXT_MED,
                handlelength=1.8, handleheight=0.8,
                borderpad=0.5, labelspacing=0.4
            )

            fig.tight_layout(pad=1.2)
            return fig, ""

        except Exception as e:
            return None, f"Error al construir el gráfico: {e}"

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
       # Paleta de badges: fondo casi transparente + texto vibrante
        BADGE_STYLES = {
            "RV":  ("rgba(16,185,129,0.12)",  "#10B981"),  # Verde esmeralda
            "RF":  ("rgba(99,102,241,0.12)",  "#818CF8"),  # Índigo suave
            "ALT": ("rgba(245,158,11,0.12)",  "#FCD34D"),  # Ámbar
            "ORO": ("rgba(251,191,36,0.12)",  "#FDE68A"),  # Dorado pálido
        }
        
        def color_clase(val):
            bg, fg = BADGE_STYLES.get(val, ("rgba(148,163,184,0.10)", "#94A3B8"))
            return (
                f"background-color: {bg}; "
                f"color: {fg}; "
                f"font-family: 'JetBrains Mono', monospace; "
                f"font-size: 0.72rem; "
                f"font-weight: 600; "
                f"letter-spacing: 0.05em; "
                f"border-radius: 6px; "
                f"text-align: center;"
            )

        styled = (
            df_cartera.style
            .format({
                "Años Hist.": "{:.1f}",
                "Score": "{:.2f}",
                "Invertir (€)": "{:,.2f} €",
                "Aportación Mensual (€)": "{:,.2f} €",
            })
            .map(color_clase, subset=["Clase"])
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
            fig, err_graf = cartera.generar_figura_expectativas()
            
        if fig is not None:
            st.pyplot(fig, use_container_width=True)
        else:
            st.markdown(f'<div class="info-box warning">{err_graf}</div>', unsafe_allow_html=True)

    st.markdown("<div class='gold-divider'></div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-family: DM Mono, monospace; font-size: 0.7rem; color: #4a5a4a; text-align: center; padding: 1rem 0;'>"
        f"Quantum Wealth Engine v3.0 · Informe generado {datetime.now().strftime('%d/%m/%Y a las %H:%M')} · "
        f"Solo para uso interno del gestor · No constituye asesoramiento financiero regulado"
        f"</div>",
        unsafe_allow_html=True
    )
