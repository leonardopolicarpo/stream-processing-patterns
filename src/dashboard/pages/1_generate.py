import streamlit as st
import subprocess
import sys
import os
import re
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

st.set_page_config(page_title="Data Generator", page_icon="🏭", layout="wide")

css_file = Path(__file__).parent.parent / "styles.css"
if css_file.exists():
  with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_terminal(logs):
  return st.code("".join(logs[-20:]), language="bash")

st.title("🏭 Data Factory")
st.markdown("---")

col1, col2 = st.columns([1, 2])

if "shared_filename" not in st.session_state:
  st.session_state["shared_filename"] = "ledger"

def update_filename():
  st.session_state["shared_filename"] = st.session_state["_filename_input"]

with col1:
  st.subheader("Configuração")
  
  rows = st.number_input(
    "Quantidade de Registros", 
    min_value=100_000, 
    max_value=50_000_000, 
    value=1_000_000, 
    step=100_000,
    help="Cuidado com a RAM se for gerar acima de 20M!"
  )
  
  currency = st.selectbox(
    "Filtrar Moeda (Opcional)",
    ["Todas", "BRL", "USD", "EUR", "GBP"],
    index=0
  )

  filename = st.text_input(
    "Nome do Arquivo",
    key="_filename_input",
    value=st.session_state['shared_filename'],
    on_change=update_filename,
    help="Aperte ENTER para confirmar o nome antes de mudar de aba!"
  )
  
  generate_btn = st.button("🚀 Iniciar Geração", type="primary", use_container_width=True)

with col2:
  st.subheader("Terminal Output")
  
  progress_bar = st.progress(0)
  status_text = st.empty()
  terminal_placeholder = st.empty()

  if generate_btn:
    output_path = f"data/{filename}.csv"
    
    cmd = [sys.executable, "-m", "src.scripts.generate_data", "--rows", str(rows), "--out", output_path]
    
    if currency != "Todas":
      cmd.extend(["--currency", currency])
        
    status_text.info(f"Executando: {' '.join(cmd)}")
    
    process = subprocess.Popen(
      cmd,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      text=True,
      bufsize=1
    )
    
    logs = []
    
    while True:
      line = process.stdout.readline()
      if not line and process.poll() is not None:
        break
      
      if line:
        if "PROGRESS:" in line:
          try:
            percent = int(re.search(r"PROGRESS:(\d+)", line).group(1))
            progress_bar.progress(min(percent / 100, 1.0))
          except:
            ...
        else:
          logs.append(line)
          terminal_placeholder.code("".join(logs[-15:]), language="bash")
    
    if process.returncode == 0:
      progress_bar.progress(100)
      status_text.success("✅ Geração concluída com sucesso!")
      st.toast("Dados gerados!", icon="🎉")
    else:
      status_text.error("❌ Erro na execução do script.")