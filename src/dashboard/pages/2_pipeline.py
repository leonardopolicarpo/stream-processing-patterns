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

st.markdown("ETL Execution Orchestrator.")

if file_exists:
  st.success(f"📂 Target File: **`{target_file}`** (Auto-detected)")
else:
  st.error(f"⚠️ File **`{target_file}`** not found in data/ directory.")
  st.info("Go to the 'Data Factory' tab to generate this file first.")

st.markdown("---")

col1, col2 = st.columns([1, 2])

with col1:
  st.subheader("⚙️ Configuration")
  
  strategy = st.radio(
    "Processing Strategy",
    [
      "v1: Naive (In-Memory)", 
      "v2: Optimized (Generators)", 
      "v3: Multiprocessing (Turbo)"
    ],
    index=1,
    help="v1 loads all to RAM (Risky!). v2 uses Streams (Ideal). v3 uses all Cores."
  )
  
  total_rows = st.number_input(
    "Expected Records (For Progress Bar)", 
    min_value=100_000, 
    max_value=50_000_000, 
    value=1_000_000, 
    step=100_000,
    help="Enter approximate dataset size for correct progress tracking."
  )
  
  mode_map = {
    "v1: Naive (In-Memory)": "naive",
    "v2: Optimized (Generators)": "optimized",
    "v3: Multiprocessing (Turbo)": "multiprocess"
  }
  selected_mode = mode_map[strategy]
  
  st.info(f"Selected Mode: **{selected_mode.upper()}**")
  
  if selected_mode == "naive":
    st.warning("⚠️ Naive mode may crash your machine if CSV is > 2GB!")
  
  run_btn = st.button(
    "▶️ Run Pipeline", 
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
    
    status_text.info(f"🔥 Starting ETL engine in {selected_mode} mode...")
    
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
        
        match = re.search(r"Progress: (\d+)", clean_line)
        
        if match:
          current_val = int(match.group(1))
          processed_count = current_val
          
          percent = min(current_val / total_rows, 1.0)
          progress_bar.progress(percent)
          
          elapsed = time.time() - start_time
          if elapsed > 0:
            speed = current_val / elapsed
            status_text.markdown(f"🚀 **Speed:** `{speed:,.0f} tx/s` | **Processed:** `{current_val:,}` / {total_rows:,}")
        
        elif "INFO" in clean_line:
          status_text.caption(f"📜 {clean_line}")

    end_time = time.time()
    duration = end_time - start_time
    
    if process.returncode == 0:
      progress_bar.progress(100)
      status_text.success(f"✅ Pipeline finished in {duration:.2f}s with average {processed_count/duration:,.0f} tx/s")
      st.balloons()
    else:
      status_text.error(f"❌ Execution Error (Exit Code: {process.returncode})")