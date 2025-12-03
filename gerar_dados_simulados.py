#!/usr/bin/env python3
"""
🔍 Gerador de Dados Simulados para Audit-IA
Gera uma versão enriquecida do dataset com colunas de análise IA
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def gerar_justificativas(risco_score, row):
    """Gera justificativas baseadas no perfil e score"""
    justificativas = []

    # Lógica baseada no score e dados do perfil
    if risco_score >= 60:
        # Casos de alto risco
        justificativas_aleatorias = [
            "Idade inconsistente com tempo de registro",
            "Recebe benefício social mas declara outra fonte de renda",
            "Alta escolaridade com renda muito baixa para atividade",
            "Acesso a tecnologia incompatível com declarações",
            "Não é filiado a instituição de pesca",
            "Pesca de produtos protegidos/raros",
            "Endereço diferente de área de pesca declarada"
        ]
        # Selecionar 3-5 justificativas
        n_justificativas = random.randint(3, 5)
        justificativas = random.sample(justificativas_aleatorias, n_justificativas)

    elif risco_score >= 30:
        # Casos de médio risco
        justificativas_aleatorias = [
            "Diferença entre idade e tempo de registro",
            "Padrão de benefícios suspeito",
            "Escolaridade vs renda inconsistente",
            "Falta de filiação institucional",
            "Localização vs área de pesca divergente"
        ]
        # Selecionar 1-3 justificativas
        n_justificativas = random.randint(1, 3)
        justificativas = random.sample(justificativas_aleatorias, n_justificativas)

    else:
        # Casos de baixo risco
        if random.random() < 0.2:  # 20% de chance de ter alguma observação
            justificativas = ["Observações menores sem grande relevância"]

    return justificativas

def gerar_dados_simulados():
    """Gera dataset simulado com análise IA"""
    print("🔄 Gerando dados simulados...")

    # Ler dados originais (se existirem)
    try:
        df_original = pd.read_csv("data/raw/EXT_PESCADORES.csv")
        print(f"✅ Dataset original carregado: {len(df_original)} registros")

        # Limitar para 1000 registros para PoC
        df = df_original.head(1000).copy()

    except FileNotFoundError:
        print("⚠️ Arquivo original não encontrado. Gerando dataset simulado...")
        # Criar dataset simulado básico
        n_registros = 1000
        df = pd.DataFrame({
            'cpf': [f"{i:011d}" for i in range(1, n_registros + 1)],
            'nome_pescador': [f"Pescador {i}" for i in range(1, n_registros + 1)],
            'rgp': [f"RGP{i:08d}" for i in range(1, n_registros + 1)],
            'municipio': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Salvador', 'Brasília'], n_registros),
            'uf': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'DF'], n_registros),
            'st_situacao_pescador': np.random.choice(['ATIVO', 'CANCELADO', 'REGISTRO_COM_PROTOCOLO'], n_registros, p=[0.8, 0.15, 0.05])
        })

    # Gerar scores de risco baseados em padrões realistas
    np.random.seed(42)  # Para reprodutibilidade

    # Distribuição: 60% baixo risco, 30% médio risco, 10% alto risco
    riscos = np.random.choice(['BAIXO', 'MEDIO', 'ALTO'], len(df), p=[0.6, 0.3, 0.1])

    scores = []
    categorias = []
    justificativas_lista = []

    for i, risco in enumerate(riscos):
        if risco == 'ALTO':
            score = random.randint(60, 95)
        elif risco == 'MEDIO':
            score = random.randint(30, 59)
        else:
            score = random.randint(0, 29)

        scores.append(score)
        categorias.append(risco)

        # Gerar justificativas baseadas no score e dados da linha
        justificativas = gerar_justificativas(score, df.iloc[i] if i < len(df) else {})
        justificativas_lista.append(justificativas)

    # Adicionar colunas de análise ao dataframe
    df['IA_Score_Risco'] = scores
    df['IA_Categoria_Risco'] = categorias
    df['IA_Justificativa'] = ['; '.join(just) for just in justificativas_lista]

    # Adicionar metadados da análise
    df['IA_Data_Analise'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['IA_Versao_Modelo'] = 'Llama-3-8B-Instruct-v1.0'
    df['IA_Status_Processamento'] = 'CONCLUIDO'

    # Salvar dataset enriquecido
    arquivo_saida = "data/processed/PESCADORES_AUDITORIA_IA.csv"
    df.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')

    print(f"✅ Dataset enriquecido salvo em: {arquivo_saida}")
    print(f"📊 Estatísticas:")
    print(f"   - Total de registros: {len(df)}")
    print(f"   - Risco Alto: {len(df[df['IA_Categoria_Risco'] == 'ALTO'])} ({len(df[df['IA_Categoria_Risco'] == 'ALTO'])/len(df)*100:.1f}%)")
    print(f"   - Risco Médio: {len(df[df['IA_Categoria_Risco'] == 'MEDIO'])} ({len(df[df['IA_Categoria_Risco'] == 'MEDIO'])/len(df)*100:.1f}%)")
    print(f"   - Risco Baixo: {len(df[df['IA_Categoria_Risco'] == 'BAIXO'])} ({len(df[df['IA_Categoria_Risco'] == 'BAIXO'])/len(df)*100:.1f}%)")

    # Gerar relatório dos top casos suspeitos
    gerar_relatorio_top_casos(df)

    return df

def gerar_relatorio_top_casos(df):
    """Gera relatório com os casos mais suspeitos"""
    print("\n📋 Gerando relatório dos casos mais suspeitos...")

    # Ordenar por score (maior para menor)
    df_ordenado = df.sort_values('IA_Score_Risco', ascending=False)
    top_casos = df_ordenado.head(20)

    # Criar relatório
    relatorio = []
    relatorio.append("# 🔍 RELATÓRIO - AUDITORIA INTELIGENTE RGP")
    relatorio.append(f"## Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    relatorio.append(f"## Total de Registros Analisados: {len(df)}")
    relatorio.append("")
    relatorio.append("## 🚨 TOP 20 CASOS MAIS SUSPEITOS")
    relatorio.append("")

    for i, (_, caso) in enumerate(top_casos.iterrows(), 1):
        relatorio.append(f"### {i:2d}. {caso.get('nome_pescador', 'N/A')}")
        relatorio.append(f"**RGP:** {caso.get('rgp', 'N/A')}")
        relatorio.append(f"**Score:** {caso['IA_Score_Risco']}/100 | **Risco:** {caso['IA_Categoria_Risco']}")
        relatorio.append(f"**Local:** {caso.get('municipio', 'N/A')}-{caso.get('uf', 'N/A')}")
        relatorio.append(f"**Situação:** {caso.get('st_situacao_pescador', 'N/A')}")

        if caso['IA_Justificativa']:
            relatorio.append("**Justificativas:**")
            for justificativa in caso['IA_Justificativa'].split('; '):
                relatorio.append(f"- {justificativa}")

        relatorio.append("---")

    # Estatísticas adicionais
    relatorio.append("## 📊 ESTATÍSTICAS GERAIS")
    relatorio.append("")
    relatorio.append(f"- **Média de Score:** {df['IA_Score_Risco'].mean():.1f}")
    relatorio.append(f"- **Score Máximo:** {df['IA_Score_Risco'].max()}")
    relatorio.append(f"- **Score Mínimo:** {df['IA_Score_Risco'].min()}")
    relatorio.append("")

    relatorio.append("### Distribuição por Categoria de Risco:")
    for categoria in ['ALTO', 'MEDIO', 'BAIXO']:
        count = len(df[df['IA_Categoria_Risco'] == categoria])
        percentual = count / len(df) * 100
        relatorio.append(f"- **{categoria}:** {count} casos ({percentual:.1f}%)")

    # Salvar relatório
    arquivo_relatorio = "docs/RELATORIO_AUDITORIA_IA.md"
    with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
        f.write('\n'.join(relatorio))

    print(f"✅ Relatório salvo em: {arquivo_relatorio}")
    print(f"🚨 Top 20 casos suspeitos identificados com scores entre {top_casos['IA_Score_Risco'].min()} e {top_casos['IA_Score_Risco'].max()}")

if __name__ == "__main__":
    print("🔍 Audit-IA - Gerador de Dados Simulados")
    print("=" * 50)

    # Gerar dados simulados
    df_simulado = gerar_dados_simulados()

    print("\n✅ Processo concluído com sucesso!")
    print("\n📂 Arquivos gerados:")
    print("   - data/processed/PESCADORES_AUDITORIA_IA.csv")
    print("   - docs/RELATORIO_AUDITORIA_IA.md")
    print("\n🚀 Para testar o sistema, execute:")
    print("   streamlit run audit_app.py")