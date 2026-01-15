from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(slots=True, frozen=True)
class Transaction:
  id: UUID
  sender: str
  receiver: str
  amount: Decimal
  fee: Decimal
  currency: str
  network: str
  status: str
  timestamp: datetime

  @property
  def total_cost(self) -> Decimal:
    return self.amount + self.fee