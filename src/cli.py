import argparse
import sys
import logging
from pathlib import Path

from src.adapters.csv_reader import CsvReader
from src.adapters.sqlite_writer import SqliteWriter
from src.service.etl_manager import ETLManager

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s',
  handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def run_pipeline(source_file: Path, db_file: Path, mode: str):
  logger.info(f"🚀 Starting Pipeline | Mode: {mode.upper()}")
  logger.info(f"📂 Input: {source_file.name}")
  logger.info(f"💾 Output: {db_file.name}")

  if not source_file.exists():
    logger.error(f"Input file not found: {source_file}")
    sys.exit(1)

  if mode == "optimized":
    csv_reader = CsvReader(filepath=source_file)
    
    try:
      with SqliteWriter(db_path=db_file) as sqlite_writer:
        etl = ETLManager(reader=csv_reader, writer=sqlite_writer, batch_size=100_000)
        etl.run()
    except Exception as e:
      logger.error(f"Fatal pipeline error: {e}", exc_info=True)
      sys.exit(1)

  elif mode == "naive":
    logger.warning("⚠️ NAIVE Mode: Loading everything into memory (OOM Risk)...")
    ...
  
  elif mode == "multiprocess":
    logger.warning("🔥 MULTIPROCESS Mode: Starting worker cluster...")
    ...

def main():
  parser = argparse.ArgumentParser(description="Financial ETL CLI")
  parser.add_argument("--file", type=str, required=True, help="Path to input CSV")
  parser.add_argument("--mode", type=str, choices=["naive", "optimized", "multiprocess"], default="optimized")
  parser.add_argument("--db", type=str, default="data/finance.db", help="Path to output Database")

  args = parser.parse_args()
  
  source = Path(args.file).resolve()
  db = Path(args.db).resolve()
  
  db.parent.mkdir(parents=True, exist_ok=True)
  run_pipeline(source, db, args.mode)

if __name__ == "__main__":
  main()