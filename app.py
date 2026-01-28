import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from shadow_trace import ShadowTraceAgent

st.set_page_config(page_title="ShadowTrace AI Dashboard", layout="wide")
st.title("🛡️ ShadowTrace AI: Security Audit Portal")

# Sidebar for configuration
st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Upload Network Logs (CSV)", type="csv")

# Logic to handle both uploaded and sample data
df = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("💡 Don't have a CSV? Click below to use sample security logs.")
    if st.button("Generate Sample Logs"):
        sample_data = {
            "timestamp": ["2026-01-29 10:00", "2026-01-29 10:15", "2026-01-29 11:00"],
            "user": ["shubh_dev", "hr_admin", "intern_01"],
            "activity": ["Uploaded source code to ChatGPT", "Moved salary sheet to personal Dropbox", "Accessing internal docs"],
            "data_type": ["source_code", "employee_records", "documentation"],
            "destination": ["chatgpt.com", "dropbox.com", "internal"]
        }
        df = pd.DataFrame(sample_data)
        st.session_state['df'] = df

# Use session state to keep data visible after button clicks
if 'df' in st.session_state and df is None:
    df = st.session_state['df']

if df is not None:
    st.write("### 📝 Activity Logs Preview", df)
    
    if st.button("🚀 Run AI Audit"):
        agent = ShadowTraceAgent("policy.json")
        results = []
        
        with st.spinner('Agent is tracing data lineage...'):
            for _, row in df.iterrows():
                report = agent.analyze_event(row.to_dict())
                results.append(report)
        
        # Convert results to DataFrame
        res_df = pd.DataFrame([r.dict() for r in results])
        
        # --- VISUALS: RISK GAUGE ---
        avg_risk = res_df['risk_score'].mean()
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_risk,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "System-Wide Risk Score", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [0, 10]},
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, 4], 'color': "#2ecc71"},
                    {'range': [4, 7], 'color': "#f1c40f"},
                    {'range': [7, 10], 'color': "#e74c3c"}],
                'threshold': {'line': {'color': "black", 'width': 4}, 'value': avg_risk}}))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # --- RESULTS TABLE ---
        st.success("✅ Audit Complete!")
        st.write("### 🚩 Detailed Findings")
        st.dataframe(res_df.style.applymap(lambda x: 'background-color: #ffcccc' if x == True else '', subset=['is_breach']))

        from fpdf import FPDF
import base64

def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ShadowTrace AI: Security Audit Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    for i, row in df.iterrows():
        status = "🚨 BREACH" if row['is_breach'] else "✅ SAFE"
        pdf.multi_cell(0, 10, txt=f"Event {i+1}: {status}\nRisk Score: {row['risk_score']}/10\nSummary: {row['summary']}\n" + "-"*30)
        pdf.ln(5)
        
    return pdf.output(dest='S').encode('latin-1')

if st.button("📄 Generate PDF Report"):
    pdf_data = create_pdf(res_df)
    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_data,
        file_name="ShadowTrace_Audit_Report.pdf",
        mime="application/pdf"
    )