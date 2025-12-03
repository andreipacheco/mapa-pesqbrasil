# 📋 ESTRUTURA DO PROJETO AUDIT-IA

## 🎯 Foco Principal

Este projeto está focado exclusivamente no arquivo **EXT_PESCADORES.csv** que contém os dados do Registro Geral da Atividade Pesqueira (RGP).

## 📁 Arquivos Essenciais

### Dados Principais
- ✅ **`data/raw/EXT_PESCADORES.csv`** - Dataset principal com dados dos pescadores
- ✅ **`data/processed/PESCADORES_AUDITORIA_IA.csv`** - Dados enriquecidos com análise IA

### Configuração
- ✅ **`models/config.json`** - Configuração do modelo de auditoria
- ✅ **`models/audit_ia_model.pkl`** - Arquivo do modelo (mock)

### Aplicações
- ✅ **`audit_app.py`** - Aplicação principal de auditoria
- ✅ **`gerar_dados_simulados.py`** - Gerador de dados para testes

### Utilitários
- ✅ **`setup_modelo.py`** - Script de configuração inicial
- ✅ **`start.sh`** - Script de inicialização do sistema

## ❌ Arquivos Removidos

- ~~`safras.csv`~~ - Pertencia ao projeto anterior (vibe-coding-v3)
- ~~Documentação sobre safras.csv~~ - Não aplicável ao Audit-IA

## 🚀 Como Funciona

1. **Carregamento**: O sistema lê `EXT_PESCADORES.csv` (115 colunas)
2. **Análise**: Aplica algoritmos de detecção de inconsistências
3. **Enriquecimento**: Gera colunas `IA_Score_Risco`, `IA_Categoria_Risco`, `IA_Justificativa`
4. **Visualização**: Interface web para exploração dos resultados

## 📊 Estrutura de Dados

### EXT_PESCADORES.csv
- **Colunas**: 115 campos com dados cadastrais e operacionais
- **Registros**: Até 1.000 pescadores (amostra para PoC)
- **Campos principais**: cpf, nome_pescador, rgp, municipio, uf, idade, renda, etc.

### PESCADORES_AUDITORIA_IA.csv
- **Colunas originais**: Mantidas do arquivo fonte
- **Colunas IA**:
  - `IA_Score_Risco` (0-100)
  - `IA_Categoria_Risco` (BAIXO/MEDIO/ALTO)
  - `IA_Justificativa` (texto explicativo)
  - `IA_Data_Analise` (timestamp)

## 🔍 Critérios de Análise

1. **Idade vs Tempo de Registro** (25 pontos)
2. **Benefícios Sociais vs Outra Renda** (30 pontos)
3. **Escolaridade vs Faixa de Renda** (20 pontos)
4. **Tecnologia vs Declarações** (15 pontos)
5. **Filiação Institucional** (10 pontos)
6. **Produtos Protegidos** (5 pontos)
7. **Localização vs Área de Pesca** (10 pontos)

## 🚀 Comandos

```bash
./start.sh checkpoint    # Verificar arquivos necessários
./start.sh fix           # Corrigir problemas
./start.sh demo          # Iniciar demonstração
```

## ✅ Checkpoint 5

O **Checkpoint 5: Sistema de Auditoria RGP** verifica:

- ✅ `data/raw/EXT_PESCADORES.csv`
- ✅ `models/config.json`
- ✅ `models/audit_ia_model.pkl`
- ✅ `audit_app.py`
- ✅ `data/processed/PESCADORES_AUDITORIA_IA.csv`

**Status**: 🎉 CONCLUÍDO