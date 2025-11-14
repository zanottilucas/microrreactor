import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from math import exp

# ======================================
# INTERFACE
# ======================================
st.title("Simulador PFR")

# Entrada do volume
V = st.number_input("Volume do reator (mL)", min_value=0.00, value=100.0)

# ======================================
# CÁLCULOS DO MODELO
# ======================================

# Temperatura (K)
T = np.arange(273.15, 323.16, 0.1)

# Vazão volumétrica (mL/min)
vazao = np.arange(0.1, 10.1, 0.1)

# Meshgrid
T_mesh, Q_mesh = np.meshgrid(T, vazao)

# Constante cinética k (cinética de pseudo-1a ordem)
k = np.exp(-4246.8 / T_mesh + 10.4)

# Conversão
X = 1 - np.exp(-(k * V) / Q_mesh)
X1 = X * 100

# ======================================
# GRÁFICO 3D
# ======================================

fig = go.Figure(
    data=[go.Surface(
        x=T_mesh,
        y=Q_mesh,
        z=X1,
        colorscale='Viridis'
    )]
)

fig.update_layout(
    title='X (%) em função da Temperatura (K) e da Vazão Volumétrica (mL/min)',
    scene=dict(
        xaxis=dict(
            title=dict(
                text='K',
                font=dict(family='Arial', size=12, color='black')
            )
        ),
        yaxis=dict(
            title=dict(
                text='mL/min',
                font=dict(family='Arial', size=12, color='black')
            )
        ),
        zaxis=dict(
            title=dict(
                text='X',
                font=dict(family='Arial', size=12, color='black')
            )
        )
    )
)


with st.container(border=True):
    st.plotly_chart(fig)
    st.latex(r'''
    \begin{aligned}
    x &= \text{Temperatura (K)} \\
    y &= \text{Vazão (mL/min)} \\
    z &= \text{Conversão (X)}
    \end{aligned}
    ''')

col1, col2 = st.columns(2, border=True)

with col1:
# ======================================
# DATAFRAME
# ======================================
    df = pd.DataFrame({
        'Temperatura (K)': T_mesh.flatten(),
        'Temperatura (°C)': (T_mesh.flatten() - 273.15),  # Nova coluna em °C
        'Vazão volumétrica (mL/min)': Q_mesh.flatten(),
        'X (%)': X1.flatten()
    })

    st.subheader("📊 Tabela de Dados")
    st.dataframe(df)

with col2:
    st.subheader("🔍 Consultar conversão para valores específicos")

    temp_input = st.number_input("Temperatura desejada (°C)", min_value=0.0, max_value=100.0, step=0.1, value=0.0)
    vazao_input = st.number_input("Vazão desejada (mL/min)", min_value=0.1, max_value=10.0, step=0.1, value=0.1)

    if st.button("Buscar Conversão"):
        
        temp_kelvin = temp_input + 273.15
        k = exp(-4246.8 / (temp_input+273.15) + 10.4)

        # Conversão
        X = 1 - np.exp(-(k * V) / vazao_input)
        X1 = X * 100

        st.success(
            f"Resultado:\n"
            f"- Temperatura: {temp_input:.1f}°C ou {temp_kelvin:.2f} K\n"
            f"- Vazão: {vazao_input:.1f} mL/min\n"
            f"- X: {X1:.2f}%"
        )


