import pandas as pd
import re

def mascarar_cpf(cpf):
    """Aplica máscara ao CPF, mantendo apenas os 3 primeiros dígitos"""
    if pd.isna(cpf) or cpf == '':
        return cpf
    cpf_str = str(cpf).strip()
    if len(cpf_str) >= 3:
        return cpf_str[:3] + '*' * (len(cpf_str) - 3)
    return '*' * len(cpf_str)

def mascarar_nome(nome):
    """Aplica máscara ao nome, mantendo apenas a primeira letra de cada palavra"""
    if pd.isna(nome) or nome == '':
        return nome
    nome_str = str(nome).strip()
    palavras = nome_str.split()
    
    # Mantém a primeira letra de cada palavra e mascara o resto
    palavras_mascaradas = []
    for palavra in palavras:
        if len(palavra) > 1:
            palavras_mascaradas.append(palavra[0] + '*' * (len(palavra) - 1))
        else:
            palavras_mascaradas.append(palavra)
    
    return ' '.join(palavras_mascaradas)

# Ler o arquivo CSV
print("Lendo arquivo CSV...")
df = pd.read_csv('/root/IA/claude/mapa-pesqbrasil/data/raw/EXT_PESCADORES.csv')

print(f"Total de registros: {len(df)}")

# Criar uma cópia para não modificar o original
df_anonimizado = df.copy()

# Aplicar máscaras
print("Aplicando máscaras ao CPF...")
df_anonimizado['cpf'] = df_anonimizado['cpf'].apply(mascarar_cpf)

print("Aplicando máscaras ao nome...")
df_anonimizado['nome_pescador'] = df_anonimizado['nome_pescador'].apply(mascarar_nome)

# Salvar o arquivo anonimizado
output_path = '/root/IA/claude/mapa-pesqbrasil/data/raw/EXT_PESCADORES_ANONIMIZADO.csv'
print(f"Salvando arquivo anonimizado em: {output_path}")
df_anonimizado.to_csv(output_path, index=False)

print("✓ Anonimização concluída!")
print(f"\nExemplos de dados anonimizados:")
print("\nPrimeiros 5 registros:")
print(df_anonimizado[['cpf', 'nome_pescador']].head())
