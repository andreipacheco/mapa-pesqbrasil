"""
🔍 Audit-IA - Versão Corrigida (Dados Pré-Carregados)
Sistema de auditoria inteligente do RGP - sem erros de dependência
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="🔍 Audit-IA - Resultados da Auditoria",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para cores de risco
st.markdown("""
<style>
.risco-alto {
    background-color: #ffebee;
    border-left: 5px solid #f44336;
    padding: 10px;
    margin: 10px 0;
}
.risco-medio {
    background-color: #fff3e0;
    border-left: 5px solid #ff9800;
    padding: 10px;
    margin: 10px 0;
}
.risco-baixo {
    background-color: #e8f5e8;
    border-left: 5px solid #4caf50;
    padding: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Carregar dados
@st.cache_data
def carregar_dados():
    """Carregar dados já analisados"""
    try:
        return pd.read_csv('data/processed/PESCADORES_AUDITORIA_IA.csv')
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

# Inicializar dados
df = carregar_dados()

# Sidebar
st.sidebar.title("🔍 Audit-IA")
st.sidebar.markdown("**Auditoria Inteligente do RGP**")

# Navegação
pagina = st.sidebar.selectbox(
    "Navegação",
    ["📊 Dashboard", "🔍 Resultados da Auditoria", "📋 Relatórios Detalhados"]
)

# Página: Dashboard
if pagina == "📊 Dashboard":
    st.title("🔍 Audit-IA PESQBRASIL - Dashboard de Resultados")
    st.markdown("---")

    if df is not None:
        # Informações do dataset
        st.info(f"📊 **Dataset Carregado**: {len(df)} pescadores analisados")

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 Total Analisado", len(df))

        with col2:
            risco_alto = len(df[df['IA_Categoria_Risco'] == 'ALTO'])
            st.metric("🚨 Risco Alto", risco_alto, f"{risco_alto/len(df)*100:.1f}%")

        with col3:
            risco_medio = len(df[df['IA_Categoria_Risco'] == 'MEDIO'])
            st.metric("⚠️ Risco Médio", risco_medio, f"{risco_medio/len(df)*100:.1f}%")

        with col4:
            risco_baixo = len(df[df['IA_Categoria_Risco'] == 'BAIXO'])
            st.metric("✅ Risco Baixo", risco_baixo, f"{risco_baixo/len(df)*100:.1f}%")

        st.markdown("---")

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            # Distribuição de Risco
            fig_risco = px.pie(
                df,
                names='IA_Categoria_Risco',
                title='🎯 Distribuição de Risco',
                color='IA_Categoria_Risco',
                color_discrete_map={
                    'ALTO': '#ff4444',
                    'MEDIO': '#ffaa00',
                    'BAIXO': '#00c851'
                }
            )
            st.plotly_chart(fig_risco, use_container_width=True)

        with col2:
            # Score de Risco
            fig_score = px.histogram(
                df,
                x='IA_Score_Risco',
                title='📈 Distribuição do Score de Risco',
                nbins=20,
                color_discrete_sequence=['#2196f3']
            )
            st.plotly_chart(fig_score, use_container_width=True)

        # Resumo Estatístico
        st.markdown("### 📈 Resumo Estatístico")

        col1, col2, col3 = st.columns(3)

        with col1:
            media_score = df['IA_Score_Risco'].mean()
            st.metric("📊 Score Médio", f"{media_score:.1f}")

        with col2:
            max_score = df['IA_Score_Risco'].max()
            st.metric("🚨 Score Máximo", max_score)

        with col3:
            casos_com_alerta = len(df[df['IA_Justificativa'].str.len() > 10])
            st.metric("📝 Casos com Alerta", casos_com_alerta)

    else:
        st.error("❌ Não foi possível carregar os dados analisados.")

# Página: Resultados da Auditoria
elif pagina == "🔍 Resultados da Auditoria":
    st.title("🔍 Resultados Detalhados da Auditoria")
    st.markdown("---")

    if df is not None:
        # Filtros
        st.markdown("### 🔍 Filtros de Análise")

        col1, col2 = st.columns(2)

        with col1:
            filtro_risco = st.selectbox(
                "Filtrar por Categoria de Risco:",
                ['Todos', 'ALTO', 'MEDIO', 'BAIXO']
            )

        with col2:
            min_score = st.slider(
                "Score Mínimo:",
                min_value=0,
                max_value=100,
                value=0
            )

        # Aplicar filtros
        df_filtrado = df.copy()

        if filtro_risco != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['IA_Categoria_Risco'] == filtro_risco]

        df_filtrado = df_filtrado[df_filtrado['IA_Score_Risco'] >= min_score]

        # Estatísticas dos dados filtrados
        st.markdown("### 📊 Estatísticas dos Dados Filtrados")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📊 Registros Filtrados", len(df_filtrado))

        with col2:
            if len(df_filtrado) > 0:
                media_filtrada = df_filtrado['IA_Score_Risco'].mean()
                st.metric("📈 Score Médio Filtrado", f"{media_filtrada:.1f}")
            else:
                st.metric("📈 Score Médio Filtrado", "0.0")

        with col3:
            if len(df_filtrado) > 0:
                alto_risco_filtro = len(df_filtrado[df_filtrado['IA_Categoria_Risco'] == 'ALTO'])
                st.metric("🚨 Risco Alto", alto_risco_filtro)
            else:
                st.metric("🚨 Risco Alto", 0)

        # Tabela de resultados (sem estilo para evitar o erro jinja2)
        st.markdown("### 📋 Tabela de Resultados")

        if len(df_filtrado) > 0:
            # Preparar dados para exibição
            df_exibir = df_filtrado[[
                'nome_pescador', 'rgp', 'IA_Score_Risco', 'IA_Categoria_Risco',
                'municipio', 'uf', 'IA_Justificativa'
            ]].copy()

            # Renomear colunas
            df_exibir.columns = ['Nome', 'RGP', 'Score', 'Categoria', 'Município', 'UF', 'Justificativas']

            st.dataframe(df_exibir, use_container_width=True)

            # Opção de download
            st.markdown("---")
            st.markdown("### 💾 Exportar Resultados Filtrados")

            csv = df_filtrado.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"audit_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Nenhum registro encontrado com os filtros selecionados.")

# Página: Relatórios Detalhados
elif pagina == "📋 Relatórios Detalhados":
    st.title("📋 Relatórios e Insights da Auditoria")
    st.markdown("---")

    if df is not None:
        # Casos de Alto Risco
        st.markdown("### 🚨 Casos de Alto Risco Prioritários")

        casos_alto_risco = df[df['IA_Categoria_Risco'] == 'ALTO'].nlargest(10, 'IA_Score_Risco')

        if len(casos_alto_risco) > 0:
            for i, (_, caso) in enumerate(casos_alto_risco.iterrows(), 1):
                with st.container():
                    st.markdown(f"""
                    <div class="risco-alto">
                        <h4>{i}. {caso['nome_pescador']}</h4>
                        <p><strong>RGP:</strong> {caso['rgp']} | <strong>Score:</strong> {caso['IA_Score_Risco']}/100 | <strong>Local:</strong> {caso['municipio']}-{caso['uf']}</p>
                        <p><strong>Justificativas:</strong> {caso['IA_Justificativa']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Análise por Estado
        st.markdown("---")
        st.markdown("### 🗺️ Análise por Estado")

        uf_risco = df.groupby('uf').agg({
            'IA_Score_Risco': ['mean', 'count'],
            'IA_Categoria_Risco': lambda x: (x == 'ALTO').sum()
        }).round(2)

        uf_risco.columns = ['Score Médio', 'Total', 'Casos Alto Risco']
        uf_risco = uf_risco.sort_values('Score Médio', ascending=False)

        if len(uf_risco) > 0:
            st.dataframe(uf_risco, use_container_width=True)

            # Gráfico de barras por estado
            fig_uf = px.bar(
                uf_risco.reset_index(),
                x='uf',
                y='Score Médio',
                title='📊 Score Médio de Risco por Estado',
                color='Score Médio',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_uf, use_container_width=True)

        # Principais Alertas
        st.markdown("---")
        st.markdown("### 🚨 Principais Tipos de Alerta")

        todas_justificativas = []
        for justificativas in df['IA_Justificativa']:
            if pd.notna(justificativas) and justificativas != 'nan':
                todas_justificativas.extend(justificativas.split(';'))

        if todas_justificativas:
            # Limpar e contar justificativas
            justificativas_limpas = []
            for j in todas_justificativas:
                j_limpo = j.strip()
                if j_limpo and j_limpo != 'nan':
                    justificativas_limpas.append(j_limpo)

            if justificativas_limpas:
                justificativas_count = pd.Series(justificativas_limpas).value_counts().head(10)

                fig_alertas = px.bar(
                    x=justificativas_count.values,
                    y=justificativas_count.index,
                    title='🚨 Top 10 Alertas Mais Comuns',
                    labels={'x': 'Frequência', 'y': 'Tipo de Alerta'},
                    orientation='h'
                )
                fig_alertas.update_layout(height=500)
                st.plotly_chart(fig_alertas, use_container_width=True)

        # Insights Principais
        st.markdown("---")
        st.markdown("### 💡 Insights Principais")

        insights = []

        percentual_alto = (len(df[df['IA_Categoria_Risco'] == 'ALTO']) / len(df)) * 100
        insights.append(f"📊 **Distribuição de Risco**: {percentual_alto:.1f}% alto risco, {(len(df[df['IA_Categoria_Risco'] == 'MEDIO'])/len(df)*100):.1f}% médio risco, {(len(df[df['IA_Categoria_Risco'] == 'BAIXO'])/len(df)*100):.1f}% baixo risco")

        media_score = df['IA_Score_Risco'].mean()
        insights.append(f"📈 **Score Médio**: {media_score:.1f} pontos (máximo: {df['IA_Score_Risco'].max()})")

        casos_com_justificativas = len(df[df['IA_Justificativa'].str.len() > 10])
        insights.append(f"📝 **Casos com Alertas**: {casos_com_justificativas} de {len(df)} pescadores possuem justificativas detalhadas")

        for insight in insights:
            st.markdown(f"- {insight}")

    else:
        st.error("❌ Não foi possível carregar os dados analisados.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🔍 Audit-IA - Auditoria Inteligente do RGP | Processamento 100% Local e Seguro
</div>
""", unsafe_allow_html=True)