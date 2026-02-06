import streamlit as st
from pathlib import Path

st.set_page_config(
  page_title="Stream Processing Patterns",
  page_icon="⚡",
  layout="wide"
)

css_file = Path(__file__).parent / "styles.css"
if css_file.exists():
  with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
  if "shared_filename" not in st.session_state:
    st.session_state["shared_filename"] = "ledger"
  
  st.title("⚡ Stream Processing Patterns")
  st.subheader("High Performance ETL Engine & Audit System")
  
  st.markdown("""
  ### Welcome to the Control Plane
  
  This system demonstrates advanced Data Engineering patterns using Python, 
  memory optimization, and batch processing.
  
  #### 🚀 Available Modules (Sidebar):
  
  * **🏭 Data Factory:** High-performance synthetic data generator (Big Data Simulation).
  * **⚡ Pipeline Runner:** ETL Orchestrator with real-time monitoring.
  * **📊 Analytics:** Financial reconciliation and fraud detection dashboard.
  
  ---
  """)
  
  col1, col2 = st.columns(2)
  
  with col1:
    st.info("""
    **Architecture:**
    * **Core:** Python 3.12 (Generators + Batch Processing)
    * **Database:** SQLite (WAL Mode)
    * **Interface:** Streamlit (MVC Pattern)
    """)
      
  with col2:
    st.success("""
    **Current Performance:**
    * Ingestion: ~40k rows/second
    * RAM Usage: < 100MB (Constant)
    * Capacity: Tested with 10M+ records
    """)

if __name__ == "__main__":
  main()