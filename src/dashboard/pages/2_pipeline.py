import streamlit as st
import subprocess
import sys
import os
import time
import re
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

st.set_page_config(page_title="Pipeline Runner", page_icon="⚡", layout="wide")

css_file = Path(__file__).parent.parent / "styles.css"
if css_file.exists():
  with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("⚡ Pipeline Runner")

if "shared_filename" not in st.session_state:
  st.session_state["shared_filename"] = "ledger"

current_filename = st.session_state["shared_filename"]

target_file = f"{current_filename}.csv"
db_file = f"{current_filename}.db"

project_root = Path(__file__).resolve().parent.parent.parent.parent
file_path = project_root / "data" / target_file
file_exists = file_path.exists()

st.markdown("Orquestrador de execução do ETL.")

if file_exists:
  st.success(f"📂 Arquivo Alvo: **`{target_file}`** (Detectado automaticamente)")
else:
  st.error(f"⚠️ Arquivo **`{target_file}`** não encontrado na pasta data/.")
  st.info("Vá até a aba 'Data Factory' para gerar este arquivo primeiro.")

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
  st.subheader("⚙️ Configuração")
  
  strategy = st.radio(
    "Estratégia de Processamento",
    [
      "v1: Naive (In-Memory)", 
      "v2: Optimized (Generators)", 
      "v3: Multiprocessing (Turbo)"
    ],
    index=1,
    help="v1 carrega tudo na RAM (Cuidado!). v2 usa Streams (Ideal). v3 usa todos os Cores."
  )
  
  total_rows = st.number_input(
    "Expectativa de Registros (Para Barra de Progresso)", 
    min_value=100_000, 
    max_value=50_000_000, 
    value=1_000_000, 
    step=100_000,
    help="Informe o tamanho aproximado do dataset para a barra funcionar corretamente."
  )
  
  mode_map = {
    "v1: Naive (In-Memory)": "naive",
    "v2: Optimized (Generators)": "optimized",
    "v3: Multiprocessing (Turbo)": "multiprocess"
  }
  selected_mode = mode_map[strategy]
  
  st.info(f"Modo selecionado: **{selected_mode.upper()}**")
  
  if selected_mode == "naive":
    st.warning("⚠️ O modo Naive pode travar sua máquina se o CSV for > 2GB!")
  
  run_btn = st.button(
    "▶️ Executar Pipeline", 
    type="primary", 
    use_container_width=True,
    disabled=not file_exists
  )

with col2:
  st.subheader("🖥️ Execution Logs")
  
  progress_bar = st.progress(0)
  status_text = st.empty()
  terminal = st.empty()
  
  if run_btn:
    cmd = [
      sys.executable, "-m", "src.cli",
      "--mode", selected_mode,
      "--file", f"data/{target_file}",
      "--db", f"data/{db_file}"
    ]
    
    status_text.info(f"🔥 Iniciando motor ETL no modo {selected_mode}...")
    
    process = subprocess.Popen(
      cmd,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      text=True,
      bufsize=1
    )
    
    logs = []
    start_time = time.time()
    processed_count = 0
    
    while True:
      line = process.stdout.readline()
      if not line and process.poll() is not None:
        break
      
      if line:
        clean_line = line.strip()
        logs.append(clean_line)
        
        terminal.code("\n".join(logs[-15:]), language="bash")
        
        match = re.search(r"Progresso: (\d+)", clean_line)
        
        if match:
          current_val = int(match.group(1))
          processed_count = current_val
          
          percent = min(current_val / total_rows, 1.0)
          progress_bar.progress(percent)
          
          elapsed = time.time() - start_time
          if elapsed > 0:
            speed = current_val / elapsed
            status_text.markdown(f"🚀 **Velocidade:** `{speed:,.0f} tx/s` | **Processado:** `{current_val:,}` / {total_rows:,}")
        
        elif "INFO" in clean_line:
          status_text.caption(f"📜 {clean_line}")

    end_time = time.time()
    duration = end_time - start_time
    
    if process.returncode == 0:
      progress_bar.progress(100)
      status_text.success(f"✅ Pipeline finalizado em {duration:.2f}s com média de {processed_count/duration:,.0f} tx/s")
      st.balloons()
    else:
      status_text.error(f"❌ Erro na execução (Exit Code: {process.returncode})")