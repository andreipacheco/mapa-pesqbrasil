#!/bin/bash

# 🔍 Iniciar Audit-IA - Sistema de Auditoria RGP
echo "🔍 Iniciando Audit-IA - Sistema de Auditoria Inteligente do RGP"
echo "================================================================="

# Verificar se estamos no diretório correto
if [ ! -f "audit_app.py" ]; then
    echo "❌ Erro: audit_app.py não encontrado"
    echo "   Certifique-se de estar no diretório raiz do projeto Audit-IA"
    exit 1
fi

# Matar processos Streamlit existentes na porta 8501
echo "🔄 Limpando processos antigos..."
pkill -f "streamlit.*8501" 2>/dev/null
lsof -ti:8501 | xargs kill -9 2>/dev/null

# Aguardar um momento
sleep 2

# Verificar arquivo principal
if [ ! -f "data/raw/EXT_PESCADORES.csv" ]; then
    echo "⚠️ AVISO: EXT_PESCADORES.csv não encontrado em data/raw/"
    echo "   A aplicação iniciará no modo de demonstração"
fi

# Verificar dados processados
if [ ! -f "data/processed/PESCADORES_AUDITORIA_IA.csv" ]; then
    echo "📊 Gerando dados de demonstração..."
    python3 gerar_dados_simulados.py 2>/dev/null || echo "   Dados de demonstração já existentes"
fi

# Verificar ambiente virtual
if [ -d ".venv" ]; then
    echo "🔧 Ativando ambiente virtual..."
    source .venv/bin/activate
    export PYTHONPATH="$(pwd):$PYTHONPATH"
fi

# Iniciar a aplicação correta
echo ""
echo "🚀 Iniciando Audit-IA..."
echo "📱 Aplicação: audit_app.py (Sistema de Auditoria RGP)"
echo "🌐 Endereço: http://localhost:8501"
echo "📁 Dados: data/raw/EXT_PESCADORES.csv"
echo ""
echo "⚠️ IMPORTANTE: Não confunda com o projeto anterior (safras.csv)"
echo "   Este é o projeto Audit-IA focado em EXT_PESCADORES.csv"
echo ""
echo "Pressione CTRL+C para parar"
echo ""

# Iniciar o Streamlit com a aplicação correta
streamlit run audit_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless false \
    --browser.gatherUsageStats false