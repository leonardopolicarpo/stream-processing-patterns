import csv
import logging
from datetime import datetime
from typing import Iterator
from pathlib import Path

from src.domain.transaction import Transaction

logger = logging.getLogger(__name__)

class CsvReader:
  def __init__(self, filepath: Path):
    self.filepath = filepath

  def read(self) -> Iterator[Transaction]:
    with open(self.filepath, mode='r', encoding='utf-8', newline='') as file:
      csv_reader = csv.reader(file)
      next(csv_reader, None)
      
      for row in csv_reader:
        try:
          yield Transaction(
            id=row[0],
            sender=row[1],
            receiver=row[2],
            amount=row[3],
            fee=row[4],
            currency=row[5],
            network=row[6],
            status=row[7],
            timestamp=datetime.fromtimestamp(int(row[8]) / 1_000_000_000)
          )
        except Exception as e:
          logger.error(f"Falha ao parsear linha: {row} - Erro: {e}")
          continue