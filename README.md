# 🔍 Audit-IA - Auditoria Inteligente do RGP

Sistema de auditoria inteligente para detecção de inconsistências e fraudes no Registro Geral da Atividade Pesqueira (RGP) usando Inteligência Artificial Generativa.

## 🎯 Objetivo

Combater a concessão indevida de benefícios no RGP através da análise automatizada de perfis de pescadores, identificando inconsistências socioeconômicas e de logística em larga escala.

## 🚀 Funcionalidades Principais

- 🔍 **Análise Inteligente**: Detecção automática de inconsistências usando IA
- 📊 **Score de Risco**: Classificação em níveis Baixo/Médio/Alto com justificativas
- 📈 **Visualizações Interativas**: Dashboards e gráficos dinâmicos
- 🗺️ **Análise Geográfica**: Mapas de risco por estado e município
- 📋 **Relatórios Detalhados**: Insights e top casos suspeitos
- 🔒 **Processamento Local**: 100% offline e seguro, sem envio de dados para APIs externas

### Funcionalidades Adicionais

- 📊 **Carregamento de Dados**: Suporte para CSV, Excel, JSON, Parquet
- 📈 **Análise Estatística**: Estatísticas descritivas e análise exploratória
- 🗺️ **Visualização Interativa**: Mapas e gráficos interativos com Streamlit
- 🔍 **Processamento de Dados**: Limpeza e transformação de dados
- 📱 **Interface Web**: Aplicação web amigável com Streamlit

## 📁 Estrutura do Projeto

```
mapa-pesqbrasil/
├── audit_app.py                     # 🚀 Aplicação principal de auditoria IA
├── app.py                          # Aplicação Streamlit genérica
├── main.py                         # Script para execução via linha de comando
├── gerar_dados_simulados.py        # Gerador de dados para testes
├── requirements.txt                # Dependências Python
├── .gitignore                     # Arquivos ignorados pelo Git
├── .streamlit/                    # Configurações do Streamlit
│   └── config.toml
├── data/                          # 📂 Diretório de dados
│   ├── raw/                      # Dados brutos (EXT_PESCADORES.csv)
│   └── processed/                # Dados processados com análise IA
├── models/                       # Modelos treinados
├── docs/                         # 📋 Documentação e relatórios
├── prompts/                      # Especificações e prompts
└── app_checkpoints/              # Versões intermediárias
```

## 🚀 Como Executar

### 🌐 **Via Streamlit Cloud (Recomendado)**

Acesse diretamente: **https://share.streamlit.io/user/andreipacheco/mapa-pesqbrasil**

### 💻 **Execução Local**

1. **Clonar o repositório:**
```bash
git clone https://github.com/andreipacheco/mapa-pesqbrasil.git
cd mapa-pesqbrasil
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Executar aplicação principal:**
```bash
streamlit run audit_app_final.py
```

4. **Acessar no navegador:** http://localhost:8501

3. **Navegar pelas funcionalidades:**
   - **🏠 Dashboard**: Visão geral e métricas
   - **📂 Carregar Dados**: Upload do EXT_PESCADORES.csv
   - **🔍 Análise de Auditoria**: Executar análise IA
   - **📊 Relatórios**: Insights e visualizações
   - **⚙️ Configurações**: Parâmetros do sistema

### 📊 Gerar Dados de Teste

Para testes sem dados reais:
```bash
python gerar_dados_simulados.py
```

Isso cria:
- `data/processed/PESCADORES_AUDITORIA_IA.csv` com 1.000 perfis analisados
- `docs/RELATORIO_AUDITORIA_IA.md` com top 20 casos suspeitos

### Interface Web Genérica (Opcional)

Para funcionalidades básicas de análise de dados:
```bash
streamlit run app.py
```

### Linha de Comando

```bash
# Executar interface web
python main.py --streamlit

# Carregar e visualizar dados
python main.py --load data/raw/seu_arquivo.csv

# Analisar arquivo
python main.py --analyze data/raw/seu_arquivo.csv

# Listar arquivos disponíveis
python main.py --list

# Listar arquivos de um diretório específico
python main.py --list --dir raw
```

## 📊 Formatos de Arquivo Suportados

- **CSV** (.csv)
- **Excel** (.xlsx, .xls)
- **JSON** (.json)
- **Parquet** (.parquet)

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações da aplicação
APP_NAME="Mapa Pesquisa Brasil"
DEBUG=False

# Configurações de dados
DATA_DIR="data"
MAX_FILE_SIZE=100MB

# Configurações do Streamlit
STREAMLIT_PORT=8501
STREAMLIT_HOST="0.0.0.0"
```

### Personalização do Streamlit

Edite o arquivo `.streamlit/config.toml` para personalizar:

- Tema e cores
- Configurações do servidor
- Fontes e layout

## 🎯 Critérios de Análise da IA

O sistema analisa 7 critérios principais para detectar inconsistências:

1. **📅 Idade vs Tempo de Registro** (25 pontos)
   - Idade incompatível com tempo de registro no RGP

2. **💰 Benefícios Sociais vs Outra Renda** (30 pontos)
   - Recebe bolsa família mas declara outra fonte de renda

3. **🎓 Escolaridade vs Faixa de Renda** (20 pontos)
   - Alta escolaridade com renda muito baixa para pesca

4. **📱 Tecnologia vs Declarações** (15 pontos)
   - Acesso a internet/celular com residência própria vs renda baixa

5. **🏢 Filiação Institucional** (10 pontos)
   - Não filiado a colônia ou associação de pesca

6. **🐢 Produtos Protegidos** (5 pontos)
   - Pesca de quelônios, répteis ou espécies protegidas

7. **📍 Localização vs Área de Pesca** (10 pontos)
   - Endereço diferente da área de pesca declarada

## 📊 Como Funciona

### 1. Carregar Dados
- Upload do arquivo EXT_PESCADORES.csv (115 colunas)
- Sistema processa automaticamente até 1.000 registros
- Validação e limpeza de dados

### 2. Executar Auditoria
- Análise automatizada de cada perfil
- Cálculo de score de risco (0-100)
- Classificação: Baixo (<30), Médio (30-59), Alto (≥60)

### 3. Analisar Resultados
- Dashboard com métricas gerais
- Filtros interativos por risco e score
- Relatórios detalhados por estado e faixa etária
- Exportação de resultados em CSV

### 4. Identificar Casos Suspeitos
- Top casos de alto risco com justificativas
- Análise geográfica de padrões
- Insights acionáveis para fiscalização

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de importação:**
   ```bash
   pip install -r requirements.txt --upgrade
   ```

2. **Arquivo não encontrado:**
   - Verifique o caminho do arquivo
   - Use caminhos relativos à raiz do projeto

3. **Problemas com encoding:**
   ```python
   # Para arquivos CSV com encoding específico
   df = pd.read_csv('arquivo.csv', encoding='utf-8')
   ```

### Logs

- Logs da aplicação: `app.log`
- Logs do Streamlit: terminal

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT.

## 📞 Suporte

Para dúvidas e suporte:

- Abra uma issue no GitHub
- Consulte a documentação em `docs/`
- Verifique os prompts em `prompts/`

---

🚀 **Desenvolvido com Python, Pandas, e Streamlit** 🗺️