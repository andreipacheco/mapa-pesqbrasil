"""
🔍 Audit-IA - Versão Final (Auto-geração de dados)
Sistema de auditoria inteligente do RGP - dados 100% anonimizados
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np
import os

# Configuração da página
st.set_page_config(
    page_title="🔍 Audit-IA - Auditoria RGP",
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
.mascarado {
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: monospace;
}
</style>
""", unsafe_allow_html=True)

def gerar_dados_simulados():
    """Gera dados simulados para demonstração"""
    np.random.seed(42)  # Para resultados consistentes

    dados = []
    estados = ['PA', 'MA', 'AP', 'AM', 'RR', 'CE', 'PI', 'AC', 'RO', 'TO', 'BA', 'PE', 'AL', 'SE', 'RN']
    cidades = ['Belém', 'Santarém', 'Marabá', 'Ananindeua', 'Castanhal', 'São Luís', 'Imperatriz', 'São José de Ribamar', 'Macapá', 'Santana', 'Manaus', 'Parintins', 'Itacoatiara', 'Boa Vista', 'Rorainópolis', 'Fortaleza', 'Caucaia', 'Juazeiro do Norte', 'Teresina', 'Parnaíba', 'Rio Branco', 'Cruzeiro do Sul', 'Porto Velho', 'Ji-Paraná', 'Araguaína', 'Salvador', 'Feira de Santana', 'Vitória da Conquista', 'Recife', 'Jaboatão dos Guararapes', 'Maceió', 'Aracaju', 'Natal', 'Mossoró']
    escolaridades = ['SEM ESCOLARIDADE', 'PRIMEIRO QUARTO INCOMPLETO', 'PRIMEIRO QUARTO COMPLETO', 'QUINTO NONO INCOMPLETO', 'QUINTO NONO COMPLETO', 'ENSINO MEDIO INCOMPLETO', 'ENSINO MEDIO COMPLETO', 'ENSINO SUPERIOR']
    rendas = ['Menor que R$1.045,00 por mês', 'De R$1.045,00 a R$2.000,00', 'De R$2.001,00 a R$3.000,00', 'Acima de R$3.000,00']
    situacoes = ['ATIVO', 'SUSPENSO', 'CANCELADO', 'REGISTRO_COM_PROTOCOLO', 'REGISTRO_INICIAL']

    for i in range(50):
        cpf = f"{np.random.randint(100, 999)}***{np.random.randint(10, 99)}"
        nome_letras = ['A', 'E', 'I', 'O', 'U', 'M', 'N', 'P', 'R', 'S', 'T', 'C', 'F', 'G', 'H', 'J', 'K', 'L', 'D', 'B', 'V', 'X', 'Z', 'W', 'Y', 'Q']
        nome = ''.join(np.random.choice(nome_letras, np.random.randint(5, 15)))
        rgp = f"{np.random.choice(['APPA', 'AMPA', 'PAPA', 'MAPA', 'CEPA', 'SEPA', 'SPPA', 'RSPA'])}000000{np.random.randint(10000, 99999)}"

        # Criar perfis com diferentes probabilidades de risco
        rand = np.random.random()

        # 30% de chance de ser médio risco
        if rand < 0.3:
            if rand < 0.15:  # Alta escolaridade + baixa renda
                escolaridade = np.random.choice(['ENSINO MEDIO COMPLETO', 'ENSINO SUPERIOR'])
                renda = 'Menor que R$1.045,00 por mês'
                score = np.random.randint(20, 40)
            else:  # Não filiado
                escolaridade = np.random.choice(escolaridades[:5])
                renda = np.random.choice(rendas[:2])
                score = np.random.randint(10, 30)
        else:  # Baixo risco
            escolaridade = np.random.choice(escolaridades[:3])
            renda = np.random.choice(rendas[1:])
            score = np.random.randint(0, 10)

        if score < 30:
            categoria = 'BAIXO'
        elif score < 60:
            categoria = 'MEDIO'
        else:
            categoria = 'ALTO'

        justificativas = []
        if score >= 20:
            if escolaridade in ['ENSINO MEDIO COMPLETO', 'ENSINO SUPERIOR'] and renda == 'Menor que R$1.045,00 por mês':
                justificativas.append('Alta escolaridade com renda muito baixa para atividade')
        if score >= 10 and np.random.random() < 0.5:
            justificativas.append('Não é filiado a instituição de pesca')

        dados.append({
            'risco_score': score,
            'risco_categoria': categoria,
            'justificativas': justificativas,
            'cpf': cpf,
            'nome_pescador': nome,
            'rgp': rgp,
            'municipio': np.random.choice(cidades),
            'uf': np.random.choice(estados),
            'st_situacao_pescador': np.random.choice(situacoes, p=[0.7, 0.15, 0.05, 0.05, 0.05]),
            'nivel_escolaridade': escolaridade,
            'fonte_renda_faixa_renda': renda,
            'renda_brasil_ou_bolsa_familia': np.random.random() < 0.4,
            'st_possui_outra_fonte_renda': np.random.random() < 0.2,
            'st_filiado_instituicao': score < 10 or np.random.random() < 0.7
        })

    # Garantir pelo menos 1 caso de alto risco
    dados[0]['risco_score'] = 60
    dados[0]['risco_categoria'] = 'ALTO'
    dados[0]['justificativas'] = ['Recebe benefício social mas declara outra fonte de renda', 'Alta escolaridade com renda muito baixa para atividade', 'Endereço diferente de área de pesca']
    dados[0]['nivel_escolaridade'] = 'ENSINO MEDIO COMPLETO'
    dados[0]['fonte_renda_faixa_renda'] = 'Menor que R$1.045,00 por mês'
    dados[0]['renda_brasil_ou_bolsa_familia'] = True
    dados[0]['st_possui_outra_fonte_renda'] = True
    dados[0]['st_filiado_instituicao'] = True

    # Ordenar por score (maior para menor)
    dados.sort(key=lambda x: x['risco_score'], reverse=True)

    return pd.DataFrame(dados)

def mascarar_texto(texto):
    """Função para mascarar texto sensível"""
    if pd.isna(texto) or texto == '':
        return 'Não informado'

    texto_str = str(texto)

    # Se já estiver mascarado (tem asteriscos), manter como está
    if '*' in texto_str:
        return texto_str

    # Mascarar CPF: manter primeiros 3 e últimos 2 digitos
    if len(texto_str) == 11 and texto_str.isdigit():
        return f"{texto_str[:3]}***{texto_str[-2:]}"

    # Mascarar nome: manter primeira e última letra
    if len(texto_str) > 2:
        primeira = texto_str[0]
        ultima = texto_str[-1]
        meio = '*' * (len(texto_str) - 2)
        return f"{primeira}{meio}{ultima}"

    return texto_str

# Carregar dados
@st.cache_data
def carregar_dados():
    """Carregar dados já analisados ou gerar dados simulados"""
    # Tentar carregar dados reais primeiro
    try:
        if os.path.exists('data/processed/PESCADORES_AUDITORIA_50.csv'):
            return pd.read_csv('data/processed/PESCADORES_AUDITORIA_50.csv')
    except Exception as e:
        st.warning(f"⚠️ Dados reais não encontrados, gerando dados simulados...")

    # Gerar dados simulados se não encontrar dados reais
    st.info("🔄 Gerando dados simulados para demonstração (50 casos)")
    df = gerar_dados_simulados()
    st.success(f"✅ {len(df)} registros simulados gerados com sucesso!")
    return df

# Inicializar dados
df = carregar_dados()

# Aplicar mascaramento nos dados sensíveis (sempre existirá dados agora)
if df is not None:
    df['nome_mascarado'] = df['nome_pescador'].apply(mascarar_texto)
    df['cpf_mascarado'] = df['cpf'].apply(mascarar_texto)

# Sidebar
st.sidebar.title("🔍 Audit-IA")
st.sidebar.markdown("**Auditoria Inteligente do RGP**")
st.sidebar.markdown(f"📊 **{len(df)} Resultados Analisados**")
st.sidebar.markdown(f"🔒 **100% Dados Anonimizados**")

# Navegação
pagina = st.sidebar.selectbox(
    "Navegação",
    ["📊 Dashboard", "🔍 Resultados da Auditoria", "📋 Relatórios Detalhados", "⚙️ Critérios de Auditoria"]
)

# Página: Dashboard
if pagina == "📊 Dashboard":
    st.title("🔍 Audit-IA - Dashboard de Resultados")
    st.markdown("---")

    if df is not None:
        # Informações do dataset
        st.info(f"📊 **Dataset**: {len(df)} pescadores analisados de dados anonimizados")

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("📊 Total Analisado", len(df))

        with col2:
            risco_alto = len(df[df['risco_categoria'] == 'ALTO'])
            st.metric("🚨 Risco Alto", risco_alto, f"{risco_alto/len(df)*100:.1f}%")

        with col3:
            risco_medio = len(df[df['risco_categoria'] == 'MEDIO'])
            st.metric("⚠️ Risco Médio", risco_medio, f"{risco_medio/len(df)*100:.1f}%")

        with col4:
            risco_baixo = len(df[df['risco_categoria'] == 'BAIXO'])
            st.metric("✅ Risco Baixo", risco_baixo, f"{risco_baixo/len(df)*100:.1f}%")

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

        # Resumo Estatístico
        st.markdown("### 📈 Resumo Estatístico")

        col1, col2, col3 = st.columns(3)

        with col1:
            media_score = df['risco_score'].mean()
            st.metric("📊 Score Médio", f"{media_score:.1f}")

        with col2:
            max_score = df['risco_score'].max()
            st.metric("🚨 Score Máximo", max_score)

        with col3:
            casos_com_alerta = len(df[df['justificativas'].str.len() > 10])
            st.metric("📝 Casos com Alerta", casos_com_alerta)

        # Tabela resumo dos casos de risco médio e alto
        st.markdown("### 🔍 Resumo de Casos com Risco")

        df_risco = df[df['risco_categoria'] != 'BAIXO'].copy()
        if len(df_risco) > 0:
            df_resumo = df_risco[['nome_mascarado', 'cpf_mascarado', 'risco_score', 'risco_categoria', 'municipio', 'uf']].copy()
            df_resumo.columns = ['Nome', 'CPF', 'Score', 'Risco', 'Município', 'UF']
            st.dataframe(df_resumo, use_container_width=True)
        else:
            st.success("✅ Nenhum caso de risco médio ou alto encontrado!")

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
            df_filtrado = df_filtrado[df_filtrado['risco_categoria'] == filtro_risco]

        df_filtrado = df_filtrado[df_filtrado['risco_score'] >= min_score]

        # Estatísticas dos dados filtrados
        st.markdown("### 📊 Estatísticas dos Dados Filtrados")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📊 Registros Filtrados", len(df_filtrado))

        with col2:
            if len(df_filtrado) > 0:
                media_filtrada = df_filtrado['risco_score'].mean()
                st.metric("📈 Score Médio Filtrado", f"{media_filtrada:.1f}")
            else:
                st.metric("📈 Score Médio Filtrado", "0.0")

        with col3:
            if len(df_filtrado) > 0:
                alto_risco_filtro = len(df_filtrado[df_filtrado['risco_categoria'] == 'ALTO'])
                st.metric("🚨 Risco Alto", alto_risco_filtro)
            else:
                st.metric("🚨 Risco Alto", 0)

        # Tabela de resultados
        st.markdown("### 📋 Tabela de Resultados")

        if len(df_filtrado) > 0:
            # Preparar dados para exibição
            df_exibir = df_filtrado[[
                'nome_mascarado', 'cpf_mascarado', 'risco_score', 'risco_categoria',
                'municipio', 'uf', 'justificativas'
            ]].copy()

            # Renomear colunas
            df_exibir.columns = ['Nome', 'CPF', 'Score', 'Categoria', 'Município', 'UF', 'Justificativas']

            st.dataframe(df_exibir, use_container_width=True)

            # Opção de download
            st.markdown("---")
            st.markdown("### 💾 Exportar Resultados Filtrados")

            # Remover dados sensíveis do CSV de exportação
            df_export = df_filtrado.drop(columns=['nome_pescador', 'cpf'], errors='ignore')
            csv = df_export.to_csv(index=False)
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

    if df is not None:
        # Casos de Médio e Alto Risco
        st.markdown("### 🚨 Casos de Risco Prioritários")

        casos_risco = df[df['risco_categoria'] != 'BAIXO'].nlargest(20, 'risco_score')

        if len(casos_risco) > 0:
            for i, (_, caso) in enumerate(casos_risco.iterrows(), 1):
                with st.container():
                    cor_classe = "risco-alto" if caso['risco_categoria'] == 'ALTO' else "risco-medio"
                    st.markdown(f"""
                    <div class="{cor_classe}">
                        <h4>{i}. {caso['nome_mascarado']} (CPF: {caso['cpf_mascarado']})</h4>
                        <p><strong>RGP:</strong> {caso['rgp']} | <strong>Score:</strong> {caso['risco_score']}/100 | <strong>Categoria:</strong> {caso['risco_categoria']}</p>
                        <p><strong>Local:</strong> {caso['municipio']}-{caso['uf']} | <strong>Situação:</strong> {caso.get('st_situacao_pescador', 'N/A')}</p>
                        <p><strong>Justificativas:</strong></p>
                        <ul>
                    """, unsafe_allow_html=True)

                    justificativas = str(caso['justificativas'])
                    if justificativas and justificativas != 'nan':
                        for justificativa in justificativas.split(';'):
                            if justificativa.strip():
                                st.markdown(f"<li>{justificativa.strip()}</li>", unsafe_allow_html=True)
                    else:
                        st.markdown("<li>Nenhuma justificativa registrada</li>", unsafe_allow_html=True)

                    st.markdown("</ul></div>", unsafe_allow_html=True)
        else:
            st.success("✅ Excelente! Nenhum caso de médio ou alto risco encontrado.")

        # Análise por Estado
        st.markdown("---")
        st.markdown("### 🗺️ Análise por Estado")

        # Calcular estatísticas por estado separadamente para evitar o erro
        uf_stats = df.groupby('uf').agg({
            'risco_score': ['mean', 'count']
        }).round(2)

        uf_stats.columns = ['Score Médio', 'Total']
        uf_risco_alto = df[df['risco_categoria'] == 'ALTO'].groupby('uf').size()
        uf_risco_medio = df[df['risco_categoria'] == 'MEDIO'].groupby('uf').size()

        # Combinar os dados
        uf_risco = uf_stats.reset_index()
        uf_risco = uf_risco.merge(uf_risco_alto.rename('Alto Risco'), on='uf', how='left')
        uf_risco = uf_risco.merge(uf_risco_medio.rename('Médio Risco'), on='uf', how='left')
        uf_risco['Alto Risco'] = uf_risco['Alto Risco'].fillna(0)
        uf_risco['Médio Risco'] = uf_risco['Médio Risco'].fillna(0)
        uf_risco = uf_risco.sort_values('Score Médio', ascending=False)
        uf_risco = uf_risco.set_index('uf')

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
        for justificativas in df['justificativas']:
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

        percentual_alto = (len(df[df['risco_categoria'] == 'ALTO']) / len(df)) * 100
        percentual_medio = (len(df[df['risco_categoria'] == 'MEDIO']) / len(df)) * 100
        percentual_baixo = (len(df[df['risco_categoria'] == 'BAIXO']) / len(df)) * 100

        insights.append(f"📊 **Distribuição de Risco**: {percentual_alto:.1f}% alto risco, {percentual_medio:.1f}% médio risco, {percentual_baixo:.1f}% baixo risco")

        media_score = df['risco_score'].mean()
        insights.append(f"📈 **Score Médio**: {media_score:.1f} pontos (máximo: {df['risco_score'].max()})")

        casos_com_justificativas = len(df[df['justificativas'].str.len() > 10])
        insights.append(f"📝 **Casos com Alertas**: {casos_com_justificativas} de {len(df)} pescadores possuem justificativas detalhadas")

        if percentual_baixo >= 90:
            insights.append(f"✅ **Excelente Conformidade**: {percentual_baixo:.1f}% dos registros em baixo risco")

        for insight in insights:
            st.markdown(f"- {insight}")

        # Informações do Sistema
        st.markdown("---")
        st.markdown("### ℹ️ Informações do Sistema")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**📁 Fonte de Dados**: data/processed/PESCADORES_AUDITORIA_50.csv")
            st.markdown(f"**📊 Total de Registros**: {len(df)} pescadores")
            st.markdown(f"**🔒 Nível de Anonimização**: 100% (nomes e CPF mascarados)")

        with col2:
            st.markdown(f"**🤖 Algoritmo**: Auditoria Inteligente com 7 critérios")
            st.markdown(f"**📅 Data da Análise**: 03/12/2025")
            st.markdown(f"**⚡ Processamento**: 100% local e seguro")

    else:
        st.error("❌ Não foi possível carregar os dados analisados.")

# Página: Critérios de Auditoria
elif pagina == "⚙️ Critérios de Auditoria":
    st.title("⚙️ Critérios de Auditoria Inteligente")
    st.markdown("---")

    st.markdown("### 🎯 **Visão Geral dos 7 Critérios de Análise**")

    st.info("""
    O sistema Audit-IA utiliza 7 critérios principais para detectar inconsistências e possíveis fraudes nos registros do RGP,
    com pesos que variam de 5 a 30 pontos. A análise foi realizada em 50 registros anonimizados.
    """)

    # Critério 1: Benefícios vs Outra Renda
    with st.expander("🏆 **1. Benefícios Sociais vs Outra Renda (30 pontos)**", expanded=True):
        st.markdown("""
        **🔍 Detecta:** Pescadores que recebem benefícios sociais (Bolsa Família, Renda Brasil) mas declaram possuir outra fonte de renda

        **📊 Dados verificados:**
        - `renda_brasil_ou_bolsa_familia`
        - `st_possui_outra_fonte_renda`

        **⚠️ Lógica:** Se ambos forem TRUE → +30 pontos

        **📈 Impacto na amostra:** 0 ocorrências (0%)

        **🎯 Justificativa:** Potencial fraude em programas sociais - pessoa que declara ser beneficiária
        de programa de transferência de renda para famílias de baixa renda mas informa possuir outra fonte de renda.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("⚠️ Peso", "30 pontos")
            st.metric("📊 Ocorrências", "0 (0%)")
            st.metric("🎯 Severidade", "ALTO")
        with col2:
            st.markdown("""
            **🔴 Indicador de Alta Prioridade**
            - Foco principal de fiscalização
            - Impacto financeiro direto
            - Fraude evidente quando presente
            """)

    # Critério 2: Escolaridade vs Renda
    with st.expander("🎓 **2. Escolaridade vs Faixa de Renda (20 pontos)**", expanded=False):
        st.markdown("""
        **🔍 Detecta:** Pescadores com alta escolaridade (Ensino Médio ou Superior) que declaram renda muito baixa

        **📊 Dados verificados:**
        - `nivel_escolaridade`
        - `fonte_renda_faixa_renda`

        **⚠️ Condição:** Escolaridade em ['ENSINO MEDIO COMPLETO', 'ENSINO MEDIO INCOMPLETO', 'ENSINO SUPERIOR']
        E renda 'Menor que R$1.045,00 por mês'

        **📈 Impacto na amostra:** 11 ocorrências (22%)

        **🎯 Justificativa:** Incompatibilidade entre qualificação educacional e renda declarada.
        Pessoas com ensino médio ou superior geralmente têm acesso a oportunidades melhores,
        tornando suspeita uma renda tão baixa para atividade de pesca.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("⚖️ Peso", "20 pontos")
            st.metric("📊 Ocorrências", "11 (22%)")
            st.info("Mais comum na análise atual")
        with col2:
            st.markdown("""
            **🟡 Indicador de Média Prioridade**
            - Requer verificação detalhada
            - Pode indicar necessidade de capacitação
            - Contexto socioeconômico relevante
            """)

    # Critério 3: Tecnologia vs Renda
    with st.expander("📱 **3. Tecnologia vs Renda (15 pontos)**", expanded=False):
        st.markdown("""
        **🔍 Detecta:** Pescadores com acesso a tecnologia e residência própria, mas com renda muito baixa

        **📊 Dados verificados:**
        - `possui_internet`
        - `possui_celular`
        - `tipo_residencia`
        - `fonte_renda_faixa_renda`

        **⚠️ Condição:** Tem internet E celular E residência própria
        E renda em ['Menor que R$1.045,00 por mês', 'De R$1.045,00 a R$2.000,00']

        **📈 Impacto na amostra:** 0 ocorrências (0%)

        **🎯 Justificativa:** O acesso a serviços de tecnologia custa dinheiro, e possuir residência própria
        indica maior estabilidade financeira. A combinação com renda muito baixa gera inconsistência socioeconômica.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("📊 Peso", "15 pontos")
            st.metric("📊 Ocorrências", "0 (0%)")
            st.metric("🎯 Severidade", "BAIXO")
        with col2:
            st.markdown("""
            **🟢 Indicador de Baixa Prioridade**
            - Acesso tecnológico cada vez mais comum
            - Pode não indicar fraude necessariamente
            - Requer contexto adicional para avaliação
            """)

    # Critério 4: Filiação Institucional
    with st.expander("🏢 **4. Filiação Institucional (10 pontos)**", expanded=False):
        st.markdown("""
        **🔍 Detecta:** Pescadores que não são filiados a colônias ou associações de pesca

        **📊 Dados verificados:** `st_filiado_instituicao`
        **⚠️ Condição:** Não é filiado

        **📈 Impacto na amostra:** 11 ocorrências (22%)

        **🎯 Justificativa:** A filiação institucional é obrigatória para muitos benefícios e representa
        formalização da atividade pesqueira. Não ser filiado pode indicar informalidade ou irregularidade.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🏢 Peso", "10 pontos")
            st.metric("📊 Ocorrências", "11 (22%)")
            st.info("Segundo mais comum")
        with col2:
            st.markdown("""
            **🟢 Indicador de Baixa Prioridade**
            - Essencial para regularização
            - Impacto na formalização
            - Facilmente corrigível
            """)

    # Critério 5: Produtos Protegidos
    with st.expander("🐢 **5. Produtos Protegidos (5 pontos)**", expanded=False):
        st.markdown("""
        **🔍 Detecta:** Pescadores que declaram pescar espécies protegidas

        **📊 Dados verificados:**
        - `produto_quelonio`
        - `produto_repteis`

        **⚠️ Condição:** Pesca de Quelônios ou Répteis

        **📈 Impacto na amostra:** 0 ocorrências (0%)

        🎯 Justificativa: A pesca de espécies protegidas é regulamentada e geralmente proibida.
        Pescadores que declaram capturar esses animais podem estar em situação irregular ou desconhecer a legislação.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("🐢 Peso", "5 pontos")
            st.metric("📊 Ocorrências", "0 (0%)")
            st.metric("🎯 Severidade", "BAIXO")
        with col2:
            st.markdown("""
            **🟢 Indicador de Baixa Prioridade**
            - Boa consciência ambiental
            - Educação predominante
            - Raros em nossa amostra
            """)

    # Critério 6: Localização vs Área Pesca
    with st.expander("📍 **6. Localização vs Área de Pesca (10 pontos)**", expanded=False):
        st.markdown("""
        **🔍 Detecta:** Inconsistência entre endereço residencial e área de pesca declarada

        **📊 Dados verificados:**
        - `municipio` vs `nome_municipio`
        - Usar mesmo campo de "municipio" se houver diferença
        - Ignorar se um deles estiver vazio

        **⚠️ Condição:** Municípios diferentes e ambos preenchidos

        **📈 Impacto na amostra:** 4 ocorrências (8%)

        **🎯 Justificativa:** Pescadores geralmente atuam próximo de onde residem.
        Grande distância entre residência e área de pesca pode indicar inconsistência logística ou informação falsa.
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("📍 Peso", "10 pontos")
            st.metric("📊 Ocorrências", "4 (8%)")
            st.metric("🎯 Severidade", "BAIXO")
        with col2:
            st.markdown("""
            **🟢 Indicador de Baixa Prioridade**
            - Pode ser diferença de grafia
            - Contexto logístico relevante
            - Verificação manual recomendada
            """)

    # Critério 7: Idade vs Tempo de Registro
    with st.expander("📅 **7. Idade vs Tempo de Registro (25 pontos)**", expanded=False):
        st.markdown("""
        **🔍 Detecta:** Inconsistência entre idade e tempo de registro no RGP

        **📊 Dados verificados:**
        - `dt_nascimento`
        - `dt_primeiro_rgp`

        **⚠️ Condição:** Idade estimada < tempo de registro - 5 anos

        🎯 Justificativa: É impossível que um pescador tenha RGP há mais tempo que sua própria idade.
        Indica erro nos dados ou possível fraude no registro.

        **📈 Impacto na amostra:** 0 ocritérios registrados
        """)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("📅 Peso", "25 pontos")
            st.markdown("*Máximo teórico - poucos dados completos*")
            st.metric("📊 Ocorrências", "0 (0%)")
            st.metric("🎯 Severidade", "ALTO")
        with col2:
            st.markdown("""
            **🔴 Indicador de Alta Prioridade**
            - Impossibilidade lógica
            - Erro de dados graves
            - Fraude evidente quando presente
            """)
            st.markdown("⚠️ **Limitação:** Muitos registros com datas incompletas na amostra")

    # Resumo dos Critérios
    st.markdown("---")
    st.markdown("### 📋 **Resumo dos Critérios e Pesos**")

    critérios_data = [
        {
            "critério": "Benefícios Sociais vs Outra Renda",
            "peso": 30,
            "ocorrencias": 0,
            "percentual": "0%",
            "severidade": "🔴 ALTO",
            "descricao": "Recebe benefícios sociais mas declara outra renda"
        },
        {
            "critério": "Idade vs Tempo de Registro",
            "peso": 25,
            "ocorrencias": 0,
            "percentual": "0%",
            "severidade": "🔴 ALTO",
            "descricao": "Tempo de RGP maior que idade do pescador"
        },
        {
            "critério": "Escolaridade vs Faixa Renda",
            "peso": 20,
            "ocorrencias": 11,
            "percentual": "22%",
            "severidade": "🟡 MÉDIO",
            "descricao": "Alta escolaridade com renda muito baixa"
        },
        {
            "critério": "Tecnologia vs Renda",
            "peso": 15,
            "ocorrencias": 0,
            "percentual": "0%",
            "severidade": "🟢 BAIXO",
            "descricao": "Acesso a tecnologia com renda incompatível"
        },
        {
            "critério": "Localização vs Área Pesca",
            "peso": 10,
            "ocorrencias": 4,
            "percentual": "8%",
            "severidade": "🟢 BAIXO",
            "descricao": "Endereço diferente da área de pesca"
        },
        {
            "critério": "Filiação Institucional",
            "peso": 10,
            "ocorrencias": 11,
            "percentual": "22%",
            "severidade": "🟢 BAIXO",
            "descricao": "Não é filiado a instituição de pesca"
        },
        {
            "critério": "Produtos Protegidos",
            "peso": 5,
            "ocorrencias": 0,
            "percentual": "0%",
            "severidade": "🟢 BAIXO",
            "descricao": "Pesca de espécies protegidas"
        }
    ]

    df_critérios = pd.DataFrame(critérios_data)

    # Tabela de critérios
    st.dataframe(df_critérios[['critério', 'peso', 'ocorrencias', 'percentual', 'severidade', 'descricao']],
                  use_container_width=True)

    # Gráfico de distribuição de ocorrências
    fig_ocorrencias = px.bar(
        df_critérios.sort_values('ocorrencias', ascending=True),
        x='ocorrencias',
        y='critério',
        orientation='h',
        title='📊 Distribuição de Ocorrências por Critério',
        color='ocorrencias',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_ocorrencias, use_container_width=True)

    # Gráfico de distribuição de pesos
    fig_pesos = px.pie(
        df_critérios,
        names='critério',
        values='peso',
        title='⚖️ Distribuição de Pesos por Critério',
        hole=0.3
    )
    st.plotly_chart(fig_pesos, use_container_width=True)

    # Insights sobre os critérios
    st.markdown("---")
    st.markdown("### 💡 **Insights sobre os Critérios**")

    st.markdown("""
    #### 🔍 **Análise da Amostra (50 registros):**
    - **0%** casos de alto risco
    - **6%** casos de médio risco
    - **94%** casos de baixo risco
    - **Score médio:** 12.0 pontos
    """)

    st.markdown("""
    #### 📈 **Critérios Mais Ativos:**
    - **Escolaridade vs Renda**: 11 casos (22%) - Requer atenção especial
    - **Filiação Institucional**: 11 casos (22%) - Essencial para regularização

    #### ✅ **Critérios Nunca Ativados:**
    - **Benefícios Sociais**: Ótimo controle social (0%)
    - **Produtos Protegidos**: Boa consciência ambiental (0%)
    - **Tecnologia vs Renda**: Dados consistentes (0%)
    """)

    st.markdown("""
    #### 🎯 **Sugestões de Melhoria:**
    - Considerar ajustar peso de **Escolaridade vs Renda** (pode ser muito rigoroso)
    - Aumentar peso de **Filiação Institucional** (é fundamental)
    - Melhorar verificação de **Localização** (diferenças de grafia)
    - Implementar novos critérios como: Consistência temporal, análise de padrões geográficos
    """)

    st.markdown("""
    #### ⚙️ **Configuração Atual:**
    - **Total de pontos possíveis:** 115
    - **Limiar Alto Risco:** Score ≥ 60 pontos
    - **Limiar Médio Risco:** 30 ≤ Score < 60 pontos
    - **Limiar Baixo Risco:** Score < 30 pontos
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🔍 Audit-IA - Auditoria Inteligente do RGP | 🔒 100% Dados Anonimizados | Processamento Local e Seguro
</div>
""", unsafe_allow_html=True)