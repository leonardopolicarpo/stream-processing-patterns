import argparse
import csv
import random
import uuid
import time
from pathlib import Path

DEFAULT_ROWS = 10_000_000
CURRENCIES = ['BRL', 'USD', 'EUR', 'GBP']
STATUSES = ['CONFIRMED', 'CONFIRMED', 'CONFIRMED', 'FAILED', 'FRAUD_DETECTED']
NETWORKS = ['PIX', 'SWIFT', 'BLOCKCHAIN_ETH', 'VISA_DIRECT']

def generate_wallet():
  return f"0x{random.getrandbits(160):040x}"

def log(msg):
  print(msg, flush=True)

def generate_dataset(rows: int, output_path: str, currency_filter: str = None):
  log(f"🚀 Iniciando geração de {rows:,} transações financeiras...")
  log(f"📂 Saída: {output_path}")
  
  if currency_filter:
    log(f"💲 Filtro de Moeda Ativo: {currency_filter}")
    target_currencies = [currency_filter]
  else:
    target_currencies = CURRENCIES
      
  log(f"📝 Schema: UUID | Wallet (Source) | Wallet (Dest) | Amount | Fee | Currency | Network | Status | Timestamp(ns)")

  start_time = time.time()
  
  Path(output_path).parent.mkdir(parents=True, exist_ok=True)

  with open(output_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([
      'tx_id', 'sender_wallet', 'receiver_wallet', 'amount',
      'fee', 'currency', 'network', 'status', 'timestamp_ns'
    ])

    active_wallets = [generate_wallet() for _ in range(1000)]
    batch_size = 100_000

    for i in range(rows):
      sender = random.choice(active_wallets) if random.random() > 0.3 else generate_wallet()
      receiver = random.choice(active_wallets) if random.random() > 0.3 else generate_wallet()

      amount = round(random.uniform(1.0, 5000.0), 2)
      network = random.choice(NETWORKS)
      
      fee_percent = 0.01 if network == 'BLOCKCHAIN_ETH' else 0.001
      fee = round(amount * fee_percent, 4)

      row = [
        str(uuid.uuid4()),
        sender,
        receiver,
        amount,
        fee,
        random.choice(target_currencies),
        network,
        random.choice(STATUSES),
        time.time_ns()
      ]
      writer.writerow(row)

      if (i + 1) % batch_size == 0:
        percent = int(((i + 1) / rows) * 100)
        log(f"PROGRESS:{percent}") 
        log(f"   ... {i + 1:,} transações geradas")

  elapsed = time.time() - start_time
  file_size = Path(output_path).stat().st_size / (1024 * 1024)

  log(f"✅ Concluído em {elapsed:.2f}s")
  log(f"📦 Tamanho Final: {file_size:.2f} MB")

def main():
  parser = argparse.ArgumentParser(description='Gerador de Ledger Financeiro')
  parser.add_argument('--rows', type=int, default=DEFAULT_ROWS)
  parser.add_argument('--out', type=str, default='data/ledger.csv')
  parser.add_argument('--currency', type=str, default=None)

  args = parser.parse_args()
  
  output_path = args.out
  if not Path(output_path).is_absolute():
    root = Path(__file__).resolve().parent.parent.parent
    output_path = str(root / args.out)

  generate_dataset(args.rows, output_path, args.currency)

if __name__ == "__main__" :
  main()