from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal

@dataclass(slots=True, frozen=True)
class Transaction:
  id: str
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