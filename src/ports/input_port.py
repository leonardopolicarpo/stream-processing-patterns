from typing import Protocol, Iterator
from src.domain.transaction import Transaction

class TransactionReader(Protocol):
  def read(self) -> Iterator[Transaction]:
    ...

class TransactionWriter(Protocol):
  def write_batch(self, transactions: list[Transaction]) -> None:
    ...