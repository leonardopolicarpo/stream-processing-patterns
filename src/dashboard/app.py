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
  ### Bem-vindo ao Control Plane
  
  Este sistema demonstra padrões avançados de Engenharia de Dados utilizando Python, 
  otimização de memória e processamento em lote.
  
  #### 🚀 Módulos Disponíveis (Menu Lateral):
  
  * **🏭 Data Factory:** Gerador de dados sintéticos de alta performance (Simulação de Big Data).
  * **⚡ Pipeline Runner:** (Em breve) Orquestrador de ETL com monitoramento em tempo real.
  * **📊 Analytics:** Dashboard de conciliação financeira e detecção de fraudes.
  
  ---
  """)
  
  col1, col2 = st.columns(2)
  
  with col1:
    st.info("""
    **Arquitetura:**
    * **Core:** Python 3.12 (Generators + Batch Processing)
    * **Database:** SQLite (WAL Mode)
    * **Interface:** Streamlit (MVC Pattern)
    """)
      
  with col2:
    st.success("""
    **Performance Atual:**
    * Ingestão: ~26k linhas/segundo
    * Uso de RAM: < 100MB (Constante)
    * Capacidade: Testado com 10M+ registros
    """)

if __name__ == "__main__":
  main()