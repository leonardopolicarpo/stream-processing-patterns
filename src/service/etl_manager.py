import logging
from typing import List
from src.domain.transaction import Transaction
from src.ports.input_port import TransactionReader, TransactionWriter

logger = logging.getLogger(__name__)

class ETLManager:
  def __init__(self, reader: TransactionReader, writer: TransactionWriter, batch_size: int = 100_000):
    self.reader = reader
    self.writer = writer
    self.batch_size = batch_size

  def run(self):
    logger.info(f"Starting processing. Batch Size: {self.batch_size}")

    batch: List[Transaction] = []
    total_processed = 0
    total_frauds = 0

    for transaction in self.reader.read():
      if transaction.status == 'FRAUD_DETECTED':
        total_frauds += 1
        # Uncomment 'continue' to actually discard frauds from the database
        # continue
    
      batch.append(transaction)

      if len(batch) >= self.batch_size:
        current_batch_size = len(batch)
        self._flush(batch)
        total_processed += current_batch_size

        if total_processed % 100_000 == 0:
          logger.info(f"Progress: {total_processed} transactions saved ... ")

    if batch:
      self._flush(batch)
      total_processed += len(batch)

    logger.info(f"Processing finished")
    logger.info(f"Valid: {total_processed}")
    logger.info(f"Frauds discarded: {total_frauds}")

  def _flush(self, batch: List[Transaction]) -> None:
    self.writer.write_batch(batch)
    batch.clear()