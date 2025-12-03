"""
Aplicação principal Streamlit
Mapa de Pesquisa Brasil
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Mapa Pesquisa Brasil",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🗺️ Mapa de Pesquisa Brasil")
st.markdown("---")

# Sidebar
st.sidebar.title("Navegação")
page = st.sidebar.selectbox(
    "Selecione uma página:",
    ["Home", "Carregar Dados", "Análise", "Visualização"]
)

# Página Home
if page == "Home":
    st.header("Bem-vindo ao Mapa de Pesquisa Brasil!")

    st.markdown("""
    ### Sobre este projeto

    Este aplicativo permite visualizar e analisar dados de pesquisa geográfica do Brasil.

    ### Funcionalidades

    - **Carregar Dados**: Importe arquivos CSV, Excel ou outros formatos
    - **Análise**: Realize análises estatísticas e processamento de dados
    - **Visualização**: Crie mapas interativos e gráficos

    ### Como usar

    1. Comece carregando seus dados na aba "Carregar Dados"
    2. Explore as análises disponíveis
    3. Crie visualizações interativas

    ### Estrutura do Projeto

    - `data/`: Armazenamento de arquivos de dados
      - `raw/`: Dados brutos
      - `processed/`: Dados processados
    - `models/`: Modelos de machine learning treinados
    - `docs/`: Documentação do projeto
    - `prompts/`: Especificações e prompts
    """)

    # Informações do sistema
    st.subheader("Informações do Sistema")
    st.info(f"Diretório atual: {os.getcwd()}")
    st.info(f"Diretório de dados: {Path('data').absolute()}")

# Página Carregar Dados
elif page == "Carregar Dados":
    st.header("Carregar Dados")

    st.markdown("### Upload de Arquivos")

    uploaded_file = st.file_uploader(
        "Escolha um arquivo",
        type=['csv', 'xlsx', 'json', 'parquet'],
        help="Suporta: CSV, Excel, JSON, Parquet"
    )

    if uploaded_file is not None:
        st.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")

        try:
            # Ler arquivo baseado na extensão
            file_extension = uploaded_file.name.split('.')[-1].lower()

            if file_extension == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_extension == 'xlsx':
                df = pd.read_excel(uploaded_file)
            elif file_extension == 'json':
                df = pd.read_json(uploaded_file)
            elif file_extension == 'parquet':
                df = pd.read_parquet(uploaded_file)

            # Mostrar informações do dataframe
            st.subheader("Informações do Dataset")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Linhas", df.shape[0])

            with col2:
                st.metric("Colunas", df.shape[1])

            with col3:
                st.metric("Memória", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")

            # Mostrar primeiras linhas
            st.subheader("Primeiras Linhas")
            st.dataframe(df.head())

            # Mostrar tipos de dados
            st.subheader("Tipos de Dados")
            st.dataframe(df.dtypes)

            # Opção de salvar
            if st.button("Salvar arquivo na pasta data/raw"):
                save_path = Path(f"data/raw/{uploaded_file.name}")
                df.to_csv(save_path, index=False)
                st.success(f"Arquivo salvo em: {save_path}")

        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {str(e)}")

# Página Análise
elif page == "Análise":
    st.header("Análise de Dados")

    st.info("Carregue um arquivo na aba 'Carregar Dados' para começar a análise.")

    # Listar arquivos disponíveis
    data_dir = Path("data/raw")
    if data_dir.exists():
        csv_files = list(data_dir.glob("*.csv"))
        excel_files = list(data_dir.glob("*.xlsx"))

        if csv_files or excel_files:
            st.subheader("Arquivos Disponíveis")

            for file in csv_files + excel_files:
                if st.button(f"Analisar {file.name}"):
                    try:
                        if file.suffix == '.csv':
                            df = pd.read_csv(file)
                        else:
                            df = pd.read_excel(file)

                        st.success(f"Arquivo {file.name} carregado para análise!")

                        # Estatísticas básicas
                        st.subheader("Estatísticas Descritivas")
                        st.dataframe(df.describe())

                        # Valores nulos
                        st.subheader("Valores Nulos")
                        null_data = df.isnull().sum()
                        st.bar_chart(null_data[null_data > 0])

                    except Exception as e:
                        st.error(f"Erro ao analisar arquivo: {str(e)}")

# Página Visualização
elif page == "Visualização":
    st.header("Visualização de Dados")

    st.info("Carregue um arquivo na aba 'Carregar Dados' para criar visualizações.")

    # Placeholder para visualizações futuras
    st.markdown("""
    ### Visualizações Disponíveis (Em Desenvolvimento)

    - 📊 Gráficos de barras e linhas
    - 🗺️ Mapas interativos
    - 📈 Gráficos de dispersão
    - 🥧 Gráficos de pizza
    - 📊 Histogramas
    """)

# Footer
st.markdown("---")
st.markdown("🚀 Desenvolvido com Streamlit | Mapa Pesquisa Brasil")

if __name__ == "__main__":
    st.run()