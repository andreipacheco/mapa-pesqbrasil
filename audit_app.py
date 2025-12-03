"""
🔍 Audit-IA - Auditoria Inteligente do RGP
Sistema de detecção de inconsistências e fraudes em registros de pescadores
usando Inteligência Artificial Generativa
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta
import re
from pathlib import Path
import json

# Configuração da página
st.set_page_config(
    page_title="🔍 Audit-IA - Auditoria Inteligente do RGP",
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
        self.df = None
        self.df_analisado = None

    def carregar_dados(self, arquivo):
        """Carregar e processar dados do arquivo CSV"""
        try:
            # Ler CSV
            df = pd.read_csv(arquivo)

            # Converter colunas de data
            colunas_data = ['dt_nascimento', 'data_criacao_pescador', 'dt_primeiro_rgp']
            for col in colunas_data:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')

            # Calcular idade
            if 'dt_nascimento' in df.columns:
                hoje = datetime.now()
                df['idade'] = df['dt_nascimento'].apply(
                    lambda x: hoje.year - x.year if pd.notna(x) else np.nan
                )

            # Padronizar valores booleanos
            colunas_bool = [
                'renda_brasil_ou_bolsa_familia', 'seguro_defeso',
                'st_possui_outra_fonte_renda', 'possui_internet',
                'possui_celular', 'st_filiado_instituicao'
            ]

            for col in colunas_bool:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.upper().map({
                        'TRUE': True, 'VERDADEIRO': True, 'SIM': True,
                        'FALSE': False, 'FALSO': False, 'NÃO': False, 'NAO': False
                    })

            self.df = df
            return True

        except Exception as e:
            st.error(f"Erro ao carregar arquivo: {str(e)}")
            return False

    def analisar_perfil(self, row):
        """Analisar perfil de pescador e detectar inconsistências"""
        risco_score = 0
        justificativas = []

        # 1. Análise de Idade vs Tempo de Registro
        if pd.notna(row.get('idade')) and pd.notna(row.get('dt_primeiro_rgp')):
            idade_registro = datetime.now().year - row['dt_primeiro_rgp'].year
            if row['idade'] < idade_registro - 2:
                risco_score += 25
                justificativas.append(f"Idade inconsistente: {row['idade']} anos mas registro há {idade_registro} anos")

        # 2. Análise de Benefícios Sociais vs Outra Renda
        if (row.get('renda_brasil_ou_bolsa_familia') == True and
            row.get('st_possui_outra_fonte_renda') == True):
            risco_score += 30
            justificativas.append("Recebe benefício social mas declara outra fonte de renda")

        # 3. Análise de Escolaridade vs Tipo de Renda
        if (row.get('nivel_escolaridade') in ['ENSINO MEDIO COMPLETO', 'ENSINO SUPERIOR'] and
            row.get('fonte_renda_faixa_renda') == 'Menor que R$1.045,00 por mês'):
            risco_score += 20
            justificativas.append("Alta escolaridade com renda muito baixa para atividade de pesca")

        # 4. Análise de Tecnologia vs Declaração
        if (row.get('possui_internet') == True and
            row.get('possui_celular') == True and
            row.get('tipo_residencia') == 'PROPRIA' and
            row.get('fonte_renda_faixa_renda') in ['Menor que R$1.045,00 por mês']):
            risco_score += 15
            justificativas.append("Acesso a tecnologia e residência própria incompatíveis com renda declarada")

        # 5. Análise de Filiação Institucional
        if row.get('st_filiado_instituicao') == False:
            risco_score += 10
            justificativas.append("Não é filiado a instituição de pesca")

        # 6. Análise de Produtos vs Ambiente
        produtos_raros = []
        if row.get('produto_quelonio') == 'SIM':
            produtos_raros.append('Quelônios')
        if row.get('produto_repteis') == 'SIM':
            produtos_raros.append('Répteis')

        if produtos_raros:
            risco_score += 5
            justificativas.append(f"Pesca de produtos protegidos/raros: {', '.join(produtos_raros)}")

        # 7. Análise de Endereço vs Local de Pesca
        if (pd.notna(row.get('municipio')) and
            pd.notna(row.get('nome_municipio')) and
            row['municipio'] != row['nome_municipio']):
            risco_score += 10
            justificativas.append(f"Endereço ({row['municipio']}) diferente de área de pesca ({row['nome_municipio']})")

        # Determinar categoria de risco
        if risco_score >= 60:
            risco_categoria = 'ALTO'
        elif risco_score >= 30:
            risco_categoria = 'MEDIO'
        else:
            risco_categoria = 'BAIXO'

        return {
            'risco_score': risco_score,
            'risco_categoria': risco_categoria,
            'justificativas': justificativas
        }

    def executar_auditoria(self):
        """Executar auditoria completa em todos os registros"""
        if self.df is None:
            return None

        st.info("🔄 Executando análise de auditoria inteligente...")

        resultados = []

        # Iterar sobre as linhas (limitar para demonstração)
        for idx, row in self.df.iterrows():
            if idx >= 1000:  # Limitar para 1000 registros como no projeto
                break

            resultado = self.analisar_perfil(row)

            # Adicionar informações básicas
            resultado.update({
                'cpf': row.get('cpf', ''),
                'nome_pescador': row.get('nome_pescador', ''),
                'rgp': row.get('rgp', ''),
                'municipio': row.get('municipio', ''),
                'uf': row.get('uf', ''),
                'idade': row.get('idade', ''),
                'fonte_renda_faixa_renda': row.get('fonte_renda_faixa_renda', ''),
                'renda_brasil_ou_bolsa_familia': row.get('renda_brasil_ou_bolsa_familia', False),
                'st_possui_outra_fonte_renda': row.get('st_possui_outra_fonte_renda', False),
                'st_situacao_pescador': row.get('st_situacao_pescador', '')
            })

            resultados.append(resultado)

        self.df_analisado = pd.DataFrame(resultos)
        return self.df_analisado

# Inicializar aplicação
audit = AuditIA()

# Sidebar
st.sidebar.title("🔍 Audit-IA")
st.sidebar.markdown("**Auditoria Inteligente do RGP**")

# Navegação
pagina = st.sidebar.selectbox(
    "Navegação",
    ["🏠 Dashboard", "📂 Carregar Dados", "🔍 Análise de Auditoria",
     "📊 Relatórios", "⚙️ Configurações"]
)

# Página: Dashboard
if pagina == "🏠 Dashboard":
    st.title("🔍 Audit-IA - Dashboard Principal")
    st.markdown("---")

    # Verificar se há dados carregados
    if audit.df_analisado is not None:
        df = audit.df_analisado

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_registros = len(df)
            st.metric("📊 Total Analisado", total_registros)

        with col2:
            risco_alto = len(df[df['risco_categoria'] == 'ALTO'])
            st.metric("🚨 Risco Alto", risco_alto, f"{risco_alto/total_registros*100:.1f}%")

        with col3:
            risco_medio = len(df[df['risco_categoria'] == 'MEDIO'])
            st.metric("⚠️ Risco Médio", risco_medio, f"{risco_medio/total_registros*100:.1f}%")

        with col4:
            risco_baixo = len(df[df['risco_categoria'] == 'BAIXO'])
            st.metric("✅ Risco Baixo", risco_baixo, f"{risco_baixo/total_registros*100:.1f}%")

        st.markdown("---")

        # Gráficos
        col1, col2 = st.columns(2)

        with col1:
            # Distribuição de Risco
            fig_risco = px.pie(
                df,
                names='risco_categoria',
                title='🎯 Distribuição de Risco',
                color='risco_categoria',
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
                x='risco_score',
                title='📈 Distribuição do Score de Risco',
                nbins=20,
                color_discrete_sequence=['#2196f3']
            )
            st.plotly_chart(fig_score, use_container_width=True)

        # Top 10 casos de alto risco
        st.markdown("### 🚨 Casos de Alto Risco")

        casos_alto_risco = df[df['risco_categoria'] == 'ALTO'].nlargest(10, 'risco_score')

        for _, caso in casos_alto_risco.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="risco-alto">
                    <h4>{caso['nome_pescador']} (RGP: {caso['rgp']})</h4>
                    <p><strong>Score:</strong> {caso['risco_score']} | <strong>Local:</strong> {caso['municipio']}-{caso['uf']}</p>
                    <p><strong>Justificativas:</strong></p>
                    <ul>
                """, unsafe_allow_html=True)

                for justificativa in caso['justificativas']:
                    st.markdown(f"<li>{justificativa}</li>", unsafe_allow_html=True)

                st.markdown("</ul></div>", unsafe_allow_html=True)

    else:
        st.info("👆 Carregue os dados na aba 'Carregar Dados' para começar a análise.")

        # Informações do projeto
        st.markdown("""
        ## 📋 Sobre o Audit-IA

        O **Audit-IA** é um sistema de auditoria inteligente que utiliza Inteligência Artificial
        para detectar inconsistências e possíveis fraudes no Registro Geral da Atividade Pesqueira (RGP).

        ### 🔎 Funcionalidades Principais

        - **Análise Automatizada**: Processa milhares de registros em minutos
        - **Detecção de Inconsistências**: Identifica padrões suspeitos usando IA
        - **Score de Risco**: Classifica os perfis em níveis de risco (Baixo, Médio, Alto)
        - **Justificativas Detalhadas**: Gera explicações para cada alerta
        - **Visualizações Interativas**: Gráficos e dashboards para análise

        ### 🎯 Critérios de Análise

        1. **Idade vs Tempo de Registro**
        2. **Benefícios Sociais vs Outra Renda**
        3. **Escolaridade vs Faixa de Renda**
        4. **Acesso a Tecnologia vs Declarações**
        5. **Filiação Institucional**
        6. **Produtos de Pesca vs Regulamentação**
        7. **Localização vs Área de Pesca**

        ### 📊 Fonte de Dados

        - **Dataset**: EXT_PESCADORES.csv
        - **Volume**: 115 colunas × 1.000 registros (amostra)
        - **Processamento**: 100% local e seguro
        """)

# Página: Carregar Dados
elif pagina == "📂 Carregar Dados":
    st.title("📂 Carregar Dados")
    st.markdown("---")

    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Selecione o arquivo CSV com dados dos pescadores",
        type=['csv'],
        help="Formato esperado: CSV com colunas do PESQBRASIL"
    )

    if uploaded_file is not None:
        st.success(f"✅ Arquivo '{uploaded_file.name}' carregado com sucesso!")

        # Opções de processamento
        st.markdown("### ⚙️ Opções de Processamento")

        limitar_registros = st.checkbox(
            "Limitar para 1.000 registros (recomendado para demonstração)",
            value=True
        )

        if st.button("🚀 Iniciar Processamento", type="primary"):
            with st.spinner("Processando dados..."):
                if audit.carregar_dados(uploaded_file):
                    if limitar_registros and len(audit.df) > 1000:
                        audit.df = audit.df.head(1000)
                        st.info(f"Limitado para 1.000 registros para demonstração")

                    st.success(f"✅ {len(audit.df)} registros carregados com sucesso!")

                    # Mostrar amostra dos dados
                    st.markdown("### 📋 Amostra dos Dados")
                    st.dataframe(audit.df.head())

                    # Informações do dataset
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("📊 Registros", len(audit.df))

                    with col2:
                        st.metric("📁 Colunas", len(audit.df.columns))

                    with col3:
                        # Verificar colunas principais
                        colunas_principais = ['cpf', 'nome_pescador', 'rgp', 'municipio', 'uf']
                        colunas_presentes = [col for col in colunas_principais if col in audit.df.columns]
                        st.metric("✅ Colunas Principais", f"{len(colunas_presentes)}/{len(colunas_principais)}")

    # Verificar arquivo existente
    st.markdown("---")
    st.markdown("### 📁 Arquivo Disponível")

    arquivo_existente = Path("data/raw/EXT_PESCADORES.csv")
    if arquivo_existente.exists():
        st.info("✅ Arquivo EXT_PESCADORES.csv encontrado na pasta data/raw/")

        if st.button("📂 Usar Arquivo Existente"):
            with st.spinner("Carregando arquivo existente..."):
                if audit.carregar_dados(arquivo_existente):
                    audit.df = audit.df.head(1000)  # Limitar para 1000
                    st.success(f"✅ {len(audit.df)} registros carregados do arquivo existente!")
                    st.rerun()
    else:
        st.warning("⚠️ Nenhum arquivo encontrado em data/raw/")

# Página: Análise de Auditoria
elif pagina == "🔍 Análise de Auditoria":
    st.title("🔍 Análise de Auditoria")
    st.markdown("---")

    if audit.df is None:
        st.warning("⚠️ Carregue os dados primeiro na aba 'Carregar Dados'")
    else:
        if st.button("🚀 Executar Auditoria Completa", type="primary"):
            df_resultados = audit.executar_auditoria()

            if df_resultados is not None:
                st.success(f"✅ Auditoria concluída! {len(df_resultados)} perfis analisados.")

                # Estatísticas gerais
                st.markdown("### 📊 Estatísticas Gerais")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    media_score = df_resultados['risco_score'].mean()
                    st.metric("📈 Score Médio", f"{media_score:.1f}")

                with col2:
                    max_score = df_resultados['risco_score'].max()
                    st.metric("🚨 Score Máximo", max_score)

                with col3:
                    risco_alto_count = len(df_resultados[df_resultados['risco_categoria'] == 'ALTO'])
                    percentual_alto = (risco_alto_count / len(df_resultados)) * 100
                    st.metric("🔴 % Risco Alto", f"{percentual_alto:.1f}%")

                with col4:
                    casos_com_justificativa = len(df_resultados[df_resultados['justificativas'].apply(len) > 0])
                    st.metric("📝 Casos Alerta", casos_com_justificativa)

                # Tabela de resultados
                st.markdown("### 📋 Resultados Detalhados")

                # Filtros
                col1, col2 = st.columns(2)

                with col1:
                    filtro_risco = st.selectbox(
                        "Filtrar por Risco:",
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
                df_filtrado = df_resultados.copy()

                if filtro_risco != 'Todos':
                    df_filtrado = df_filtrado[df_filtrado['risco_categoria'] == filtro_risco]

                df_filtrado = df_filtrado[df_filtrado['risco_score'] >= min_score]

                # Exibir tabela
                df_exibir = df_filtrado[[
                    'nome_pescador', 'rgp', 'risco_score', 'risco_categoria',
                    'municipio', 'uf', 'idade', 'fonte_renda_faixa_renda'
                ]].copy()

                # Adicionar formatação
                def colorir_risco(val):
                    if val == 'ALTO':
                        return 'background-color: #ffebee'
                    elif val == 'MEDIO':
                        return 'background-color: #fff3e0'
                    else:
                        return 'background-color: #e8f5e8'

                df_exibir = df_exibir.rename(columns={
                    'nome_pescador': 'Nome',
                    'rgp': 'RGP',
                    'risco_score': 'Score',
                    'risco_categoria': 'Risco',
                    'municipio': 'Município',
                    'uf': 'UF',
                    'idade': 'Idade',
                    'fonte_renda_faixa_renda': 'Faixa Renda'
                })

                st.dataframe(
                    df_exibir.style.applymap(colorir_risco, subset=['Risco']),
                    use_container_width=True
                )

                # Opção de download
                st.markdown("---")
                st.markdown("### 💾 Exportar Resultados")

                csv = df_filtrado.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"audit_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )

# Página: Relatórios
elif pagina == "📊 Relatórios":
    st.title("📊 Relatórios e Insights")
    st.markdown("---")

    if audit.df_analisado is None:
        st.warning("⚠️ Execute a auditoria primeiro para gerar relatórios")
    else:
        df = audit.df_analisado

        # Análise por Estado
        st.markdown("### 🗺️ Análise por Estado")

        uf_risco = df.groupby('uf').agg({
            'risco_score': ['mean', 'count'],
            'risco_categoria': lambda x: (x == 'ALTO').sum()
        }).round(2)

        uf_risco.columns = ['Score Médio', 'Total', 'Casos Alto Risco']
        uf_risco = uf_risco.sort_values('Score Médio', ascending=False)

        st.dataframe(uf_risco, use_container_width=True)

        # Mapa de calor por UF
        if len(uf_risco) > 0:
            fig_mapa = px.choropleth_mapbox(
                df.groupby(['uf']).agg({'risco_score': 'mean'}).reset_index(),
                locations='uf',
                geojson='https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson',
                featureidkey='properties.sigla',
                color='risco_score',
                hover_name='uf',
                hover_data={'risco_score': True},
                title='🗺️ Mapa de Risco por Estado',
                mapbox_style="open-street-map",
                opacity=0.7,
                center={"lat": -14.235, "lon": -51.9253},
                zoom=3
            )
            st.plotly_chart(fig_mapa, use_container_width=True)

        # Análise de Faixa Etária
        st.markdown("### 👥 Análise por Faixa Etária")

        # Criar faixas etárias
        def classificar_idade(idade):
            if pd.isna(idade):
                return 'Não informado'
            elif idade < 25:
                return '18-24 anos'
            elif idade < 35:
                return '25-34 anos'
            elif idade < 45:
                return '35-44 anos'
            elif idade < 55:
                return '45-54 anos'
            else:
                return '55+ anos'

        df['faixa_etaria'] = df['idade'].apply(classificar_idade)

        idade_risco = df.groupby('faixa_etaria').agg({
            'risco_score': ['mean', 'count'],
            'risco_categoria': lambda x: (x == 'ALTO').sum()
        }).round(2)

        idade_risco.columns = ['Score Médio', 'Total', 'Casos Alto Risco']
        st.dataframe(idade_risco, use_container_width=True)

        # Principais Justificativas
        st.markdown("### 🚨 Principais Alertas")

        todas_justificativas = []
        for justificativas in df['justificativas']:
            todas_justificativas.extend(justificativas)

        if todas_justificativas:
            justificativas_count = pd.Series(todas_justificativas).value_counts().head(10)

            fig_alertas = px.bar(
                x=justificativas_count.values,
                y=justificativas_count.index,
                title='🚨 Top 10 Alertas Mais Comuns',
                labels={'x': 'Frequência', 'y': 'Tipo de Alerta'},
                orientation='h'
            )
            fig_alertas.update_layout(height=500)
            st.plotly_chart(fig_alertas, use_container_width=True)

        # Insights
        st.markdown("---")
        st.markdown("### 💡 Insights Principais")

        insights = []

        # Calcular insights
        percentual_alto = (len(df[df['risco_categoria'] == 'ALTO']) / len(df)) * 100
        if percentual_alto > 20:
            insights.append(f"🚨 **Alerta Vermelho**: {percentual_alto:.1f}% dos casos apresentam risco alto")

        beneficio_renda_conflito = df[
            (df['renda_brasil_ou_bolsa_familia'] == True) &
            (df['st_possui_outra_fonte_renda'] == True)
        ]
        if len(beneficio_renda_conflito) > 0:
            insights.append(f"⚠️ **Conflito de Benefícios**: {len(beneficio_renda_conflito)} casos recebem benefícios mas declaram outra renda")

        media_score_uf = df.groupby('uf')['risco_score'].mean()
        uf_max_risco = media_score_uf.idxmax()
        insights.append(f"🗺️ **Estado de Maior Risco**: {uf_max_risco} com score médio de {media_score_uf.max():.1f}")

        for insight in insights:
            st.markdown(f"- {insight}")

# Página: Configurações
elif pagina == "⚙️ Configurações":
    st.title("⚙️ Configurações")
    st.markdown("---")

    st.markdown("### 🎛️ Parâmetros de Análise")

    # Pesos para análise (simulação)
    with st.expander("⚖️ Pesos dos Critérios de Análise"):
        st.markdown("""
        **Configurações dos pesos para cálculo do score de risco:**

        - **Idade vs Tempo de Registro**: 25 pontos
        - **Benefícios vs Outra Renda**: 30 pontos
        - **Escolaridade vs Renda**: 20 pontos
        - **Tecnologia vs Declaração**: 15 pontos
        - **Filiação Institucional**: 10 pontos
        - **Produtos Protegidos**: 5 pontos
        - **Endereço vs Área Pesca**: 10 pontos
        """)

    st.markdown("### 📊 Limiares de Classificação")

    with st.expander("🎯 Configurar Limiares"):
        limiar_alto = st.slider(
            "Limiar para Risco Alto:",
            min_value=40,
            max_value=80,
            value=60,
            help="Score mínimo para classificar como risco alto"
        )

        limiar_medio = st.slider(
            "Limiar para Risco Médio:",
            min_value=20,
            max_value=60,
            value=30,
            help="Score mínimo para classificar como risco médio"
        )

        st.info(f"""
        Configuração atual:
        - **Risco Alto**: Score ≥ {limiar_alto}
        - **Risco Médio**: {limiar_medio} ≤ Score < {limiar_alto}
        - **Risco Baixo**: Score < {limiar_medio}
        """)

    st.markdown("### 💾 Exportar Configurações")

    config = {
        "pesos": {
            "idade_vs_tempo": 25,
            "beneficios_vs_renda": 30,
            "escolaridade_vs_renda": 20,
            "tecnologia_vs_declaracao": 15,
            "filiacao_institucional": 10,
            "produtos_protegidos": 5,
            "endereco_vs_area_pesca": 10
        },
        "limiares": {
            "risco_alto": limiar_alto,
            "risco_medio": limiar_medio
        }
    }

    if st.button("📥 Download Configurações"):
        config_json = json.dumps(config, indent=2)
        st.download_button(
            label="💾 Baixar config.json",
            data=config_json,
            file_name="audit_config.json",
            mime="application/json"
        )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🔍 Audit-IA - Auditoria Inteligente do RGP | Processamento 100% Local e Seguro
</div>
""", unsafe_allow_html=True)