"""
🔍 Audit-IA - Versão Simplificada (Dados Pré-Carregados)
Sistema de auditoria inteligente do RGP - já inicia com análise pronta
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import json

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
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

class AuditIA:
    """Classe principal para a Auditoria Inteligente do RGP"""

    def __init__(self):
        self.df_analisado = None
        self.carregar_dados_analisados()

    def carregar_dados_analisados(self):
        """Carregar dados já analisados do arquivo processado"""
        try:
            self.df_analisado = pd.read_csv('data/processed/PESCADORES_AUDITORIA_IA.csv')
            return True
        except Exception as e:
            st.error(f"Erro ao carregar dados analisados: {str(e)}")
            return False

# Inicializar aplicação
audit = AuditIA()

# Sidebar
st.sidebar.title("🔍 Audit-IA")
st.sidebar.markdown("**Auditoria Inteligente do RGP**")

# Navegação simplificada
pagina = st.sidebar.selectbox(
    "Navegação",
    ["📊 Dashboard", "🔍 Resultados da Auditoria", "📋 Relatórios Detalhados"]
)

# Página: Dashboard
if pagina == "📊 Dashboard":
    st.title("🔍 Audit-IA - Dashboard de Resultados")
    st.markdown("---")

    if audit.df_analisado is not None:
        df = audit.df_analisado

        # Informações do dataset
        st.info(f"📊 **Dataset Carregado**: {len(df)} pescadores analisados")

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_registros = len(df)
            st.metric("📊 Total Analisado", total_registros)

        with col2:
            risco_alto = len(df[df['IA_Categoria_Risco'] == 'ALTO'])
            st.metric("🚨 Risco Alto", risco_alto, f"{risco_alto/total_registros*100:.1f}%")

        with col3:
            risco_medio = len(df[df['IA_Categoria_Risco'] == 'MEDIO'])
            st.metric("⚠️ Risco Médio", risco_medio, f"{risco_medio/total_registros*100:.1f}%")

        with col4:
            risco_baixo = len(df[df['IA_Categoria_Risco'] == 'BAIXO'])
            st.metric("✅ Risco Baixo", risco_baixo, f"{risco_baixo/total_registros*100:.1f}%")

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

        # Data da última análise
        if 'IA_Data_Analise' in df.columns:
            data_ultima = df['IA_Data_Analise'].iloc[0]
            st.markdown(f"**📅 Data da Última Análise**: {data_ultima}")

    else:
        st.error("❌ Não foi possível carregar os dados analisados. Verifique o arquivo em data/processed/")

# Página: Resultados da Auditoria
elif pagina == "🔍 Resultados da Auditoria":
    st.title("🔍 Resultados Detalhados da Auditoria")
    st.markdown("---")

    if audit.df_analisado is not None:
        df = audit.df_analisado

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

        # Tabela de resultados
        st.markdown("### 📋 Tabela de Resultados")

        if len(df_filtrado) > 0:
            # Preparar dados para exibição
            df_exibir = df_filtrado[[
                'nome_pescador', 'rgp', 'IA_Score_Risco', 'IA_Categoria_Risco',
                'municipio', 'uf', 'IA_Justificativa'
            ]].copy()

            # Renomear colunas
            df_exibir = df_exibir.rename(columns={
                'nome_pescador': 'Nome do Pescador',
                'rgp': 'RGP',
                'IA_Score_Risco': 'Score Risco',
                'IA_Categoria_Risco': 'Categoria Risco',
                'municipio': 'Município',
                'uf': 'UF',
                'IA_Justificativa': 'Justificativas'
            })

            # Adicionar formatação
            def colorir_risco(val):
                if val == 'ALTO':
                    return 'background-color: #ffebee'
                elif val == 'MEDIO':
                    return 'background-color: #fff3e0'
                else:
                    return 'background-color: #e8f5e8'

            st.dataframe(
                df_exibir.style.applymap(colorir_risco, subset=['Categoria Risco']),
                use_container_width=True
            )

            # Opção de download
            st.markdown("---")
            st.markdown("### 💾 Exportar Resultados Filtrados")

            csv = df_filtrado.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"audit_resultados_filtrados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ Nenhum registro encontrado com os filtros selecionados.")

# Página: Relatórios Detalhados
elif pagina == "📋 Relatórios Detalhados":
    st.title("📋 Relatórios e Insights da Auditoria")
    st.markdown("---")

    if audit.df_analisado is not None:
        df = audit.df_analisado

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
                        <p><strong>Justificativas:</strong></p>
                        <ul>
                    """, unsafe_allow_html=True)

                    justificativas = str(caso['IA_Justificativa'])
                    if justificativas and justificativas != 'nan':
                        for justificativa in justificativas.split(';'):
                            if justificativa.strip():
                                st.markdown(f"<li>{justificativa.strip()}</li>", unsafe_allow_html=True)
                    else:
                        st.markdown("<li>Sem justificativas registradas</li>", unsafe_allow_html=True)

                    st.markdown("</ul></div>", unsafe_allow_html=True)

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
            justificativas_limpias = [j.strip() for j in todas_justificativas if j.strip() and j.strip() != 'nan']
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

        # Calcular insights
        percentual_alto = (len(df[df['IA_Categoria_Risco'] == 'ALTO']) / len(df)) * 100
        if percentual_alto > 20:
            insights.append(f"🚨 **Alerta Vermelho**: {percentual_alto:.1f}% dos casos apresentam risco alto")

        media_score_uf = df.groupby('uf')['IA_Score_Risco'].mean()
        if len(media_score_uf) > 0:
            uf_max_risco = media_score_uf.idxmax()
            insights.append(f"🗺️ **Estado de Maior Risco**: {uf_max_risco} com score médio de {media_score_uf.max():.1f}")

        casos_com_justificativas = len(df[df['IA_Justificativa'].str.len() > 10])
        insights.append(f"📝 **Casos com Alertas**: {casos_com_justificativas} pescadores com justificativas detalhadas")

        for insight in insights:
            st.markdown(f"- {insight}")

        # Informações do Sistema
        st.markdown("---")
        st.markdown("### ℹ️ Informações do Sistema")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**📁 Fonte de Dados**: data/processed/PESCADORES_AUDITORIA_IA.csv")
            st.markdown(f"**📊 Total de Registros**: {len(df)} pescadores")

        with col2:
            if 'IA_Versao_Modelo' in df.columns:
                versao = df['IA_Versao_Modelo'].iloc[0]
                st.markdown(f"**🤖 Versão do Modelo**: {versao}")

            if 'IA_Data_Analise' in df.columns:
                data_analise = df['IA_Data_Analise'].iloc[0]
                st.markdown(f"**📅 Data da Análise**: {data_analise}")

    else:
        st.error("❌ Não foi possível carregar os dados analisados.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🔍 Audit-IA - Auditoria Inteligente do RGP | Processamento 100% Local e Seguro
</div>
""", unsafe_allow_html=True)