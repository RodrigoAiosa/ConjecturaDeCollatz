"""
Conjectura de Collatz - Aplicativo Streamlit
=============================================
Este aplicativo recebe um número inteiro do usuário e exibe todo o
processo da Conjectura de Collatz (também conhecida como problema 3n+1)
até que a sequência alcance o número 1.

Regra da conjectura:
    - Se o número for par, divida por 2.
    - Se o número for ímpar, multiplique por 3 e some 1.
    - Repita até chegar a 1.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path


# ----------------------------------------------------------------------
# Configuração da página
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Conjectura de Collatz",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ----------------------------------------------------------------------
# Carrega o CSS customizado
# ----------------------------------------------------------------------
def carregar_css(caminho_arquivo: str) -> None:
    """Lê um arquivo .css e injeta seu conteúdo na página."""
    css_path = Path(caminho_arquivo)
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


carregar_css("style.css")


# ----------------------------------------------------------------------
# Lógica da Conjectura de Collatz
# ----------------------------------------------------------------------
def gerar_sequencia_collatz(numero: int) -> list[int]:
    """
    Gera a sequência completa de Collatz a partir de um número inteiro
    positivo, até chegar a 1.

    Retorna uma lista com todos os valores da sequência, incluindo o
    número inicial e o número final (1).
    """
    sequencia = [numero]
    atual = numero

    while atual != 1:
        if atual % 2 == 0:
            atual = atual // 2
        else:
            atual = atual * 3 + 1
        sequencia.append(atual)

    return sequencia


def classificar_passo(valor_atual: int, valor_anterior: int) -> str:
    """Classifica cada passo da sequência como Par ou Ímpar (em relação
    ao valor anterior, que foi o número transformado)."""
    if valor_anterior % 2 == 0:
        return "Par (÷ 2)"
    return "Ímpar (× 3 + 1)"


# ----------------------------------------------------------------------
# Cabeçalho
# ----------------------------------------------------------------------
st.title("🔢 Conjectura de Collatz")
st.markdown(
    """
    A **Conjectura de Collatz** (também chamada de *problema 3n + 1*)
    afirma que, partindo de qualquer número inteiro positivo, a seguinte
    sequência sempre chega ao número **1**:

    - Se o número é **par**, divida-o por **2**.
    - Se o número é **ímpar**, multiplique-o por **3** e some **1**.

    Repita o processo até chegar a 1. Ninguém provou matematicamente que
    isso sempre acontece — mas até hoje, para todo número já testado,
    a conjectura se confirma.
    """
)

st.divider()

# ----------------------------------------------------------------------
# Entrada do usuário
# ----------------------------------------------------------------------
with st.sidebar:
    st.header("🖍️ Sua vez no quadro")
    numero_usuario = st.number_input(
        "Escreva um número inteiro positivo:",
        min_value=1,
        max_value=1_000_000_000,
        value=27,
        step=1,
        help="Escolha um número inteiro maior que zero para calcular a sequência de Collatz.",
    )
    calcular = st.button("✏️ Resolver no quadro", use_container_width=True)

    st.markdown("---")
    st.markdown(
        """
        **Sugestões de números interessantes:**
        - `27` → sequência longa (111 passos)
        - `97` → também bem longa
        - `6`, `7`, `8` → sequências curtas para comparação
        """
    )

# ----------------------------------------------------------------------
# Processamento e exibição dos resultados
# ----------------------------------------------------------------------
if calcular or "sequencia" in st.session_state:

    if calcular:
        numero_inteiro = int(numero_usuario)
        sequencia = gerar_sequencia_collatz(numero_inteiro)
        st.session_state["sequencia"] = sequencia
        st.session_state["numero_inicial"] = numero_inteiro

    sequencia = st.session_state["sequencia"]
    numero_inicial = st.session_state["numero_inicial"]

    # --- Métricas principais -------------------------------------------------
    total_passos = len(sequencia) - 1
    valor_maximo = max(sequencia)
    passo_do_maximo = sequencia.index(valor_maximo)
    qtd_pares = sum(1 for v in sequencia if v % 2 == 0)
    qtd_impares = len(sequencia) - qtd_pares

    st.subheader(f"Resultados para o número **{numero_inicial}**")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de passos", total_passos)
    col2.metric("Maior valor atingido", f"{valor_maximo:,}".replace(",", "."))
    col3.metric("Passos pares", qtd_pares)
    col4.metric("Passos ímpares", qtd_impares)

    st.divider()

    # --- Gráfico de linha: evolução da sequência ------------------------------
    st.markdown("### 📈 Evolução da sequência")

    fig_linha = go.Figure()
    fig_linha.add_trace(
        go.Scatter(
            x=list(range(len(sequencia))),
            y=sequencia,
            mode="lines+markers",
            line=dict(color="#F1EFE7", width=2, dash="dot"),
            marker=dict(size=5, color="#F1EFE7"),
            name="Valor",
        )
    )
    fig_linha.add_trace(
        go.Scatter(
            x=[passo_do_maximo],
            y=[valor_maximo],
            mode="markers+text",
            marker=dict(size=13, color="#E8917B", symbol="star"),
            text=["Pico"],
            textposition="top center",
            textfont=dict(color="#E8917B", family="Kalam, cursive", size=14),
            name="Valor máximo",
        )
    )
    fig_linha.update_layout(
        xaxis_title="Passo",
        yaxis_title="Valor",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Patrick Hand, cursive", color="#F1EFE7", size=14),
        xaxis=dict(gridcolor="rgba(241,239,231,0.15)", zerolinecolor="rgba(241,239,231,0.2)"),
        yaxis=dict(gridcolor="rgba(241,239,231,0.15)", zerolinecolor="rgba(241,239,231,0.2)"),
        height=450,
        margin=dict(l=10, r=10, t=30, b=10),
    )
    st.plotly_chart(fig_linha, use_container_width=True)

    # --- Gráfico em escala logarítmica ----------------------------------------
    with st.expander("📊 Ver gráfico em escala logarítmica"):
        fig_log = go.Figure()
        fig_log.add_trace(
            go.Scatter(
                x=list(range(len(sequencia))),
                y=sequencia,
                mode="lines+markers",
                line=dict(color="#F2D66B", width=2, dash="dot"),
                marker=dict(size=4, color="#F2D66B"),
            )
        )
        fig_log.update_layout(
            xaxis_title="Passo",
            yaxis_title="Valor (log)",
            yaxis_type="log",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Patrick Hand, cursive", color="#F1EFE7", size=14),
            xaxis=dict(gridcolor="rgba(241,239,231,0.15)"),
            yaxis=dict(gridcolor="rgba(241,239,231,0.15)"),
            height=400,
            margin=dict(l=10, r=10, t=30, b=10),
        )
        st.plotly_chart(fig_log, use_container_width=True)

    # --- Gráfico de barras: pares vs ímpares -----------------------------------
    st.markdown("### 🧮 Distribuição de passos (par x ímpar)")
    fig_barras = go.Figure(
        data=[
            go.Bar(
                x=["Pares", "Ímpares"],
                y=[qtd_pares, qtd_impares],
                marker_color=["#F1EFE7", "#E8917B"],
            )
        ]
    )
    fig_barras.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Patrick Hand, cursive", color="#F1EFE7", size=14),
        xaxis=dict(gridcolor="rgba(241,239,231,0.1)"),
        yaxis=dict(gridcolor="rgba(241,239,231,0.15)"),
        height=350,
        margin=dict(l=10, r=10, t=30, b=10),
        yaxis_title="Quantidade",
    )
    st.plotly_chart(fig_barras, use_container_width=True)

    st.divider()

    # --- Tabela detalhada com todos os passos ----------------------------------
    st.markdown("### 📋 Detalhamento passo a passo")

    dados_tabela = []
    for i, valor in enumerate(sequencia):
        if i == 0:
            operacao = "Número inicial"
        else:
            anterior = sequencia[i - 1]
            operacao = classificar_passo(valor, anterior)
        dados_tabela.append(
            {
                "Passo": i,
                "Valor": valor,
                "Operação aplicada": operacao,
            }
        )

    df = pd.DataFrame(dados_tabela)
    st.dataframe(df, use_container_width=True, height=400)

    # --- Download dos dados -----------------------------------------------------
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Baixar sequência em CSV",
        data=csv,
        file_name=f"collatz_{numero_inicial}.csv",
        mime="text/csv",
    )

else:
    st.info("👈 Digite um número na barra lateral e clique em **Calcular sequência** para começar.")


# ----------------------------------------------------------------------
# Rodapé
# ----------------------------------------------------------------------
st.markdown(
    """
    <div class="rodape">
        Feito com ❤️ usando <b>Streamlit</b> — Conjectura de Collatz (3n + 1)
    </div>
    """,
    unsafe_allow_html=True,
)
