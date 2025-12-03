#!/usr/bin/env python3
"""
🔍 Setup de Dados para Audit-IA
Script para criar dados de exemplo e configuração inicial
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def verificar_ext_pescadores():
    """Verificar se o arquivo EXT_PESCADORES.csv existe"""
    if os.path.exists('data/raw/EXT_PESCADORES.csv'):
        print("✅ EXT_PESCADORES.csv encontrado em data/raw/")
        return True
    else:
        print("⚠️ EXT_PESCADORES.csv não encontrado em data/raw/")
        print("   Este é o arquivo principal para a auditoria do RGP")
        return False

def criar_modelos_mock():
    """Criar modelos mock para o sistema"""
    print("🔄 Criando modelos mock...")

    # Criar diretório models se não existir
    os.makedirs('models', exist_ok=True)

    # Criar arquivo de configuração do modelo
    config_modelo = {
        "nome_modelo": "audit-ia-v1.0",
        "data_treinamento": datetime.now().strftime('%Y-%m-%d'),
        "versao": "1.0.0",
        "parametros": {
            "threshold_risco_alto": 60,
            "threshold_risco_medio": 30,
            "pesos": {
                "idade_vs_tempo": 25,
                "beneficios_vs_renda": 30,
                "escolaridade_vs_renda": 20,
                "tecnologia_vs_declaracoes": 15,
                "filiacao_institucional": 10,
                "produtos_protegidos": 5,
                "endereco_vs_area_pesca": 10
            }
        }
    }

    # Salvar configuração
    import json
    with open('models/config.json', 'w') as f:
        json.dump(config_modelo, f, indent=2)

    # Criar arquivo modelo mock (vazio para representar modelo treinado)
    with open('models/audit_ia_model.pkl', 'wb') as f:
        f.write(b'audit_ia_model_mock_v1.0')

    print("✅ Modelos mock criados com sucesso!")

def verificar_dados_audit():
    """Verificar se os dados de auditoria existem"""
    if os.path.exists('data/processed/PESCADORES_AUDITORIA_IA.csv'):
        print("✅ Dados de auditoria encontrados")
        return True
    else:
        print("⚠️ Dados de auditoria não encontrados")
        return False

def main():
    """Função principal"""
    print("🔍 Audit-IA - Setup de Dados e Modelos")
    print("=" * 40)

    # Verificar diretórios
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('docs', exist_ok=True)

    # Verificar arquivo EXT_PESCADORES.csv
    ext_pescadores_ok = verificar_ext_pescadores()

    # Criar modelos mock
    criar_modelos_mock()

    # Verificar dados de auditoria
    dados_audit_ok = verificar_dados_audit()

    print("\n✅ Setup concluído com sucesso!")
    print("\n📁 Arquivos criados:")
    print("   - models/config.json")
    print("   - models/audit_ia_model.pkl")

    if not ext_pescadores_ok:
        print("\n⚠️ IMPORTANTE: EXT_PESCADORES.csv não encontrado")
        print("   Copie o arquivo para data/raw/EXT_PESCADORES.csv")

    if not dados_audit_ok:
        print("\n⚠️ Para gerar dados de auditoria:")
        print("   python gerar_dados_simulados.py")

    print("\n🚀 Para iniciar a aplicação:")
    print("   streamlit run audit_app.py")

if __name__ == "__main__":
    main()