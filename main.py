"""
Script principal para execução em modo console
Mapa de Pesquisa Brasil
"""

import os
import sys
import argparse
from pathlib import Path
import pandas as pd
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MapaPesquisaBrasil:
    """Classe principal para o projeto Mapa de Pesquisa Brasil"""

    def __init__(self):
        self.data_dir = Path("data")
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.models_dir = Path("models")

        # Criar diretórios se não existirem
        self._create_directories()

    def _create_directories(self):
        """Criar estrutura de diretórios necessária"""
        directories = [self.data_dir, self.raw_dir, self.processed_dir, self.models_dir]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Diretório verificado/criado: {directory}")

    def load_data(self, file_path):
        """Carregar dados de um arquivo"""
        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        try:
            # Determinar tipo de arquivo pela extensão
            if file_path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            elif file_path.suffix.lower() in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            elif file_path.suffix.lower() == '.json':
                df = pd.read_json(file_path)
            elif file_path.suffix.lower() == '.parquet':
                df = pd.read_parquet(file_path)
            else:
                raise ValueError(f"Formato de arquivo não suportado: {file_path.suffix}")

            logger.info(f"Dados carregados: {len(df)} linhas, {len(df.columns)} colunas")
            return df

        except Exception as e:
            logger.error(f"Erro ao carregar arquivo {file_path}: {str(e)}")
            raise

    def save_data(self, df, filename, directory="processed"):
        """Salvar dataframe em arquivo"""
        if directory == "raw":
            save_dir = self.raw_dir
        else:
            save_dir = self.processed_dir

        save_path = save_dir / filename

        try:
            if filename.endswith('.csv'):
                df.to_csv(save_path, index=False)
            elif filename.endswith(('.xlsx', '.xls')):
                df.to_excel(save_path, index=False)
            elif filename.endswith('.json'):
                df.to_json(save_path, orient='records', indent=2)
            elif filename.endswith('.parquet'):
                df.to_parquet(save_path, index=False)
            else:
                # Default para CSV
                save_path = save_path.with_suffix('.csv')
                df.to_csv(save_path, index=False)

            logger.info(f"Dados salvos em: {save_path}")
            return save_path

        except Exception as e:
            logger.error(f"Erro ao salvar dados: {str(e)}")
            raise

    def basic_analysis(self, df):
        """Realizar análise básica dos dados"""
        analysis = {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'null_counts': df.isnull().sum().to_dict(),
            'description': df.describe().to_dict()
        }

        logger.info("Análise básica concluída")
        return analysis

    def list_data_files(self, directory="all"):
        """Listar arquivos de dados disponíveis"""
        files = []

        if directory in ["all", "raw"]:
            raw_files = list(self.raw_dir.glob("*"))
            files.extend([(f, "raw") for f in raw_files if f.is_file()])

        if directory in ["all", "processed"]:
            processed_files = list(self.processed_dir.glob("*"))
            files.extend([(f, "processed") for f in processed_files if f.is_file()])

        return files

    def run_streamlit(self):
        """Executar aplicação Streamlit"""
        import subprocess

        try:
            logger.info("Iniciando aplicação Streamlit...")
            subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Erro ao executar Streamlit: {str(e)}")
            raise
        except FileNotFoundError:
            logger.error("Streamlit não está instalado. Execute: pip install streamlit")
            raise


def main():
    """Função principal para execução via linha de comando"""
    parser = argparse.ArgumentParser(description="Mapa de Pesquisa Brasil")
    parser.add_argument("--streamlit", action="store_true", help="Executar aplicação Streamlit")
    parser.add_argument("--load", type=str, help="Carregar arquivo de dados")
    parser.add_argument("--analyze", type=str, help="Analisar arquivo de dados")
    parser.add_argument("--list", action="store_true", help="Listar arquivos de dados")
    parser.add_argument("--dir", choices=["all", "raw", "processed"], default="all",
                       help="Diretório para listar arquivos")

    args = parser.parse_args()

    # Inicializar aplicação
    app = MapaPesquisaBrasil()

    try:
        if args.streamlit:
            app.run_streamlit()

        elif args.load:
            df = app.load_data(args.load)
            print(f"Arquivo carregado: {args.load}")
            print(f"Shape: {df.shape}")
            print(f"Colunas: {list(df.columns)}")
            print("\nPrimeiras 5 linhas:")
            print(df.head())

        elif args.analyze:
            df = app.load_data(args.analyze)
            analysis = app.basic_analysis(df)

            print(f"Análise do arquivo: {args.analyze}")
            print(f"Shape: {analysis['shape']}")
            print(f"Colunas: {analysis['columns']}")
            print("\nValores nulos:")
            for col, count in analysis['null_counts'].items():
                if count > 0:
                    print(f"  {col}: {count}")

        elif args.list:
            files = app.list_data_files(args.dir)

            if files:
                print(f"Arquivos no diretório '{args.dir}':")
                for file_path, dir_type in files:
                    print(f"  {dir_type}/: {file_path.name}")
            else:
                print("Nenhum arquivo encontrado.")

        else:
            parser.print_help()

    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()