import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Page configuration
st.set_page_config(page_title="DataViz Pro", page_icon="📊", layout="wide")

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #4F46E5;
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        transform: translateY(-2px);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    h1 {
        color: #111827;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        letter-spacing: -0.025em;
    }
    .report-container {
        padding: 24px;
        border-radius: 12px;
        background-color: white;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }
    .chart-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #F3F4F6;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 DataViz Pro")
st.markdown("<p style='font-size: 1.2rem; color: #4B5563;'>Transform your raw data into stunning visual reports instantly.</p>", unsafe_allow_html=True)
st.divider()

# Sidebar for navigation
st.sidebar.image("https://img.icons8.com/fluency/96/000000/data-configuration.png", width=80)
st.sidebar.title("Configuration")
option = st.sidebar.selectbox(
    "Choose Input Method",
    ("Manual Entry", "Upload Excel/CSV")
)

def render_charts(df, label_col, value_col):
    if df is not None and not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.subheader("📈 Bar Chart")
            fig_bar = px.bar(df, x=label_col, y=value_col, 
                             color=label_col,
                             template="plotly_white",
                             color_discrete_sequence=px.colors.qualitative.Bold)
            fig_bar.update_layout(showlegend=False, margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
            st.subheader("🍕 Pie Chart")
            fig_pie = px.pie(df, names=label_col, values=value_col,
                             hole=0.4,
                             template="plotly_white",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
            fig_pie.update_layout(margin=dict(t=30, b=10, l=10, r=10))
            st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.divider()
        st.subheader("📋 Data Summary")
        st.dataframe(df.style.background_gradient(subset=[value_col], cmap='Blues'), use_container_width=True)

if option == "Manual Entry":
    st.header("✏️ Manual Data Input")
    
    # Initialize session state for manual data
    if 'rows' not in st.session_state:
        st.session_state.rows = [{"label": "", "value": 0.0}]
    
    def add_row():
        st.session_state.rows.append({"label": "", "value": 0.0})
        
    def clear_data():
        st.session_state.rows = [{"label": "", "value": 0.0}]
        st.session_state.clear_triggered = True

    with st.expander("📝 Edit Data Points", expanded=True):
        for i, row in enumerate(st.session_state.rows):
            c1, c2 = st.columns([2, 1])
            st.session_state.rows[i]["label"] = c1.text_input(f"Label {i+1}", value=row["label"], key=f"label_{i}", placeholder="e.g., Sales, Q1...")
            st.session_state.rows[i]["value"] = c2.number_input(f"Value {i+1}", value=float(row["value"]), key=f"value_{i}")
        
        col_btn1, col_btn2, _ = st.columns([1, 1, 2])
        with col_btn1:
            if st.button("➕ Add Row"):
                add_row()
                st.rerun()
        with col_btn2:
            if st.button("🗑️ Clear All"):
                clear_data()
                st.rerun()

    # Create DataFrame from manual input
    valid_data = [r for r in st.session_state.rows if r["label"].strip() != ""]
    
    if valid_data:
        df = pd.DataFrame(valid_data)
        df.columns = ["Category", "Value"]
        render_charts(df, "Category", "Value")
    else:
        st.info("👋 Start entering labels and values above to generate your report.")

elif option == "Upload Excel/CSV":
    st.header("📂 Upload Your Data File")
    
    uploaded_file = st.file_uploader("Drop your Excel or CSV file here", type=["xlsx", "xls", "csv"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"Successfully loaded '{uploaded_file.name}'")
            
            # Column selection
            all_columns = df.columns.tolist()
            st.sidebar.markdown("---")
            st.sidebar.subheader("Select Columns")
            label_col = st.sidebar.selectbox("Category/Label Column", all_columns)
            
            # Filter for numeric columns
            numeric_cols = [c for c in all_columns if pd.api.types.is_numeric_dtype(df[c])]
            if not numeric_cols:
                st.error("No numeric columns found in the uploaded file. Please ensure your file contains numbers for values.")
            else:
                value_col = st.sidebar.selectbox("Value/Numeric Column", numeric_cols)
                
                if label_col and value_col:
                    render_charts(df, label_col, value_col)
                
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.info("Make sure your file is a valid Excel (.xlsx, .xls) or CSV file.")
    else:
        st.info("Please upload an Excel or CSV file. The app will automatically detect columns for you to visualize.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Built with ❤️ by Antigravity")
