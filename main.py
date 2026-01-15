import sys
import logging
from pathlib import Path

from src.adapters.csv_reader import CsvReader
from src.adapters.sqlite_writer import SqliteWriter
from src.service.etl_manager import ETLManager

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
  data_dir = Path(__file__).parent.parent / "data"
  input_file = data_dir / "ledger.csv"
  db_file = data_dir / "finance.db"

  logger.info(f"Iniciando ETL...")
  logger.info(f"Lendo de: {input_file}")
  logger.info(f"Salvando em: {db_file}")

  csv_reader = CsvReader(filepath=input_file)

  sqlite_writer = SqliteWriter(db_path=db_file)

  etl_service = ETLManager(
    reader=csv_reader,
    writer=sqlite_writer
  )

  try:
    etl_service.run()
    logger.info("Pipeline finalizado com sucesso")
  except Exception as e:
    logger.error(f"Erro no pipeline", exc_info=True)
    sys.exit(1)

if __name__ == "__main__":
  main()