#!/usr/bin/env python3
"""
🔍 Audit-IA - Análise de 50 Resultados
Processa EXT_PESCADORES_ANONIMIZADO.csv e gera auditoria para 50 registros
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json

class AuditoriaIA:
    """Classe para análise inteligente de dados do RGP"""

    def __init__(self):
        self.df = None
        self.df_analisado = None

    def carregar_dados_anonimizados(self):
        """Carregar dados do arquivo anonimizado"""
        try:
            print("🔄 Carregando dados anonimizados...")
            self.df = pd.read_csv('data/raw/EXT_PESCADORES_ANONIMIZADO.csv')
            print(f"✅ {len(self.df)} registros carregados")
            return True
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {str(e)}")
            return False

    def analisar_perfil(self, row):
        """Analisar perfil de pescador e detectar inconsistências"""
        risco_score = 0
        justificativas = []

        # Converter tipos de dados
        try:
            # Valores booleanos
            beneficios = str(row.get('renda_brasil_ou_bolsa_familia', 'False')).upper() == 'TRUE'
            seguro = str(row.get('seguro_defeso', 'False')).upper() == 'TRUE'
            outra_renda = str(row.get('st_possui_outra_fonte_renda', 'False')).upper() == 'TRUE'
            internet = str(row.get('possui_internet', 'False')).upper() == 'TRUE'
            celular = str(row.get('possui_celular', 'False')).upper() == 'TRUE'
            filiado = str(row.get('st_filiado_instituicao', 'False')).upper() == 'TRUE'

            # Valores categóricos
            escolaridade = str(row.get('nivel_escolaridade', '')).strip()
            residencia = str(row.get('tipo_residencia', '')).strip()
            faixa_renda = str(row.get('fonte_renda_faixa_renda', '')).strip()
            municipio = str(row.get('municipio', '')).strip()
            nome_municipio = str(row.get('nome_municipio', '')).strip()

            # Verificar produtos protegidos
            produtos_protegidos = []
            if str(row.get('produto_quelonio', '')).upper() == 'SIM':
                produtos_protegidos.append('Quelônios')
            if str(row.get('produto_repteis', '')).upper() == 'SIM':
                produtos_protegidos.append('Répteis')

            # 1. Benefícios vs Outra Renda (30 pontos)
            if beneficios and outra_renda:
                risco_score += 30
                justificativas.append("Recebe benefício social mas declara outra fonte de renda")

            # 2. Escolaridade vs Faixa Renda (20 pontos)
            if (escolaridade in ['ENSINO MEDIO COMPLETO', 'ENSINO MEDIO INCOMPLETO', 'ENSINO SUPERIOR'] and
                faixa_renda == 'Menor que R$1.045,00 por mês'):
                risco_score += 20
                justificativas.append("Alta escolaridade com renda muito baixa para atividade")

            # 3. Tecnologia vs Renda (15 pontos)
            if (internet and celular and residencia == 'PROPRIA' and
                faixa_renda in ['Menor que R$1.045,00 por mês', 'De R$1.045,00 a R$2.000,00']):
                risco_score += 15
                justificativas.append("Acesso a tecnologia com residência própria incompatível com renda baixa")

            # 4. Filiação Institucional (10 pontos)
            if not filiado:
                risco_score += 10
                justificativas.append("Não é filiado a instituição de pesca")

            # 5. Produtos Protegidos (5 pontos)
            if produtos_protegidos:
                risco_score += 5
                justificativas.append(f"Pesca de produtos protegidos: {', '.join(produtos_protegidos)}")

            # 6. Localização vs Área Pesca (10 pontos)
            if municipio and nome_municipio and municipio != nome_municipio and municipio.strip() and nome_municipio.strip():
                risco_score += 10
                justificativas.append(f"Endereço ({municipio}) diferente de área de pesca ({nome_municipio})")

            # 7. Análise Temporal (Idade vs Tempo) - Simplificada
            try:
                if pd.notna(row.get('dt_primeiro_rgp')) and pd.notna(row.get('dt_nascimento')):
                    ano_registro = pd.to_datetime(row['dt_primeiro_rgp']).year
                    ano_nascimento = pd.to_datetime(row['dt_nascimento']).year

                    if ano_registro < 2000:  # Registro muito antigo
                        idade_estimada = 2025 - ano_nascimento
                        tempo_registro = 2025 - ano_registro
                        if idade_estimada < tempo_registro - 5:
                            risco_score += 25
                            justificativas.append("Inconsistência entre idade e tempo de registro no RGP")
            except:
                pass  # Ignorar erros de data

        except Exception as e:
            justificativas.append(f"Erro na análise: {str(e)}")

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
        """Executar auditoria completa"""
        if self.df is None:
            return None

        print("🔍 Executando auditoria inteligente...")

        resultados = []

        for idx, row in self.df.iterrows():
            if idx % 10 == 0:
                print(f"  Processando registro {idx + 1}/{len(self.df)}...")

            resultado = self.analisar_perfil(row)

            # Adicionar informações do registro
            resultado.update({
                'cpf': row.get('cpf', ''),
                'nome_pescador': row.get('nome_pescador', ''),
                'rgp': row.get('rgp', ''),
                'municipio': row.get('municipio', ''),
                'uf': row.get('uf', ''),
                'st_situacao_pescador': row.get('st_situacao_pescador', ''),
                'nivel_escolaridade': row.get('nivel_escolaridade', ''),
                'fonte_renda_faixa_renda': row.get('fonte_renda_faixa_renda', ''),
                'renda_brasil_ou_bolsa_familia': row.get('renda_brasil_ou_bolsa_familia', ''),
                'st_possui_outra_fonte_renda': row.get('st_possui_outra_fonte_renda', ''),
                'st_filiado_instituicao': row.get('st_filiado_instituicao', '')
            })

            resultados.append(resultado)

        self.df_analisado = pd.DataFrame(resultados)
        print(f"✅ Auditoria completa! {len(self.df_analisado)} perfis analisados")

        # Selecionar os 50 casos mais suspeitos (maior score)
        print("🎯 SELECIONANDO OS 50 CASOS MAIS SUSPEITOS...")
        self.df_analisado = self.df_analisado.sort_values('risco_score', ascending=False).head(50)
        self.df_analisado = self.df_analisado.reset_index(drop=True)
        print(f"✅ Selecionados {len(self.df_analisado)} casos de maior risco")

        return self.df_analisado

    def gerar_relatorio(self):
        """Gerar relatório da auditoria"""
        if self.df_analisado is None:
            return None

        print("\n📊 GERANDO RELATÓRIO DE AUDITORIA")
        print("=" * 50)

        # Estatísticas gerais
        total = len(self.df_analisado)
        alto_risco = len(self.df_analisado[self.df_analisado['risco_categoria'] == 'ALTO'])
        medio_risco = len(self.df_analisado[self.df_analisado['risco_categoria'] == 'MEDIO'])
        baixo_risco = len(self.df_analisado[self.df_analisado['risco_categoria'] == 'BAIXO'])

        print(f"📈 ESTATÍSTICAS GERAIS:")
        print(f"   • Total de registros: {total}")
        print(f"   • Risco Alto: {alto_risco} ({alto_risco/total*100:.1f}%)")
        print(f"   • Risco Médio: {medio_risco} ({medio_risco/total*100:.1f}%)")
        print(f"   • Risco Baixo: {baixo_risco} ({baixo_risco/total*100:.1f}%)")
        print(f"   • Score médio: {self.df_analisado['risco_score'].mean():.1f}")
        print(f"   • Score máximo: {self.df_analisado['risco_score'].max()}")

        # Top casos de alto risco
        print(f"\n🚨 TOP {min(10, alto_risco)} CASOS DE ALTO RISCO:")
        print("-" * 50)

        casos_alto_risco = self.df_analisado[self.df_analisado['risco_categoria'] == 'ALTO'].nlargest(10, 'risco_score')

        for i, (_, caso) in enumerate(casos_alto_risco.iterrows(), 1):
            print(f"\n{i}. {caso['nome_pescador']}")
            print(f"   RGP: {caso['rgp']} | Score: {caso['risco_score']}/100")
            print(f"   Local: {caso['municipio']}-{caso['uf']} | Situação: {caso['st_situacao_pescador']}")
            print(f"   Justificativas:")
            for justificativa in caso['justificativas']:
                print(f"     • {justificativa}")

        # Análise por estado
        print(f"\n🗺️ ANÁLISE POR ESTADO:")
        print("-" * 50)

        uf_risco = self.df_analisado.groupby('uf').agg({
            'risco_score': ['mean', 'count'],
            'risco_categoria': lambda x: (x == 'ALTO').sum()
        }).round(2)

        uf_risco.columns = ['Score Médio', 'Total', 'Casos Alto Risco']
        uf_risco = uf_risco.sort_values('Score Médio', ascending=False)

        for uf, row in uf_risco.iterrows():
            print(f"   {uf}: Score {row['Score Médio']:.1f} ({row['Total']} casos, {row['Casos Alto Risco']} alto risco)")

        # Principais alertas
        print(f"\n📋 PRINCIPAIS ALERTAS:")
        print("-" * 50)

        todas_justificativas = []
        for justificativas in self.df_analisado['justificativas']:
            todas_justificativas.extend(justificativas)

        if todas_justificativas:
            justificativas_count = pd.Series(todas_justificativas).value_counts().head(5)

            for alerta, count in justificativas_count.items():
                print(f"   • {alerta}: {count} ocorrências")

        return self.df_analisado

def main():
    """Função principal"""
    print("🔍 AUDIT-IA - ANÁLISE DE 50 RESULTADOS")
    print("=" * 50)

    # Inicializar auditoria
    auditoria = AuditoriaIA()

    # Carregar dados
    if not auditoria.carregar_dados_anonimizados():
        return False

    # Executar auditoria
    resultados = auditoria.executar_auditoria()

    if resultados is None:
        return False

    # Gerar relatório
    auditoria.gerar_relatorio()

    # Salvar resultados
    print(f"\n💾 SALVANDO RESULTADOS...")

    # Salvar CSV completo
    arquivo_csv = f"data/processed/PESCADORES_AUDITORIA_50_RESULTADOS_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    resultados.to_csv(arquivo_csv, index=False)
    print(f"✅ Resultados salvos em: {arquivo_csv}")

    # Salvar versão principal
    resultados.to_csv('data/processed/PESCADORES_AUDITORIA_50.csv', index=False)
    print(f"✅ Versão principal salva em: data/processed/PESCADORES_AUDITORIA_50.csv")

    print(f"\n🎉 ANÁLISE CONCLUÍDA COM SUCESSO!")
    print(f"🌐 Para visualizar os resultados: streamlit run audit_app_corrigido.py")

    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)