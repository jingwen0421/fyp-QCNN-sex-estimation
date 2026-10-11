import sys
import streamlit as st
import pandas as pd
import random
import time
import altair as alt
from streamlit_option_menu import option_menu

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="QCNN Sex Estimation System",
    page_icon="🧬",
    layout="wide"
)

# =========================
# CSS Design
# =========================
st.markdown("""
<style>
.main {
    background-color: #F7FAF9;
}

.block-container {
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(135deg, #0F766E, #14B8A6);
    padding: 2rem;
    border-radius: 22px;
    color: white;
    margin-bottom: 1.5rem;
}

.hero h1 {
    font-size: 2.1rem;
    margin-bottom: 0.4rem;
}

.hero p {
    font-size: 1rem;
    opacity: 0.95;
}

.card {
    background-color: white;
    padding: 1.4rem;
    border-radius: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    border: 1px solid #E5E7EB;
    margin-bottom: 1rem;
}

.small-title {
    color: #0F766E;
    font-size: 1.1rem;
    font-weight: 700;
}

.status-ready {
    background-color: #DCFCE7;
    color: #166534;
    padding: 0.5rem 0.9rem;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}

.status-demo {
    background-color: #FEF3C7;
    color: #92400E;
    padding: 0.5rem 0.9rem;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
}

.result-box {
    background: linear-gradient(135deg, #ECFDF5, #F0FDFA);
    padding: 1.5rem;
    border-radius: 20px;
    border-left: 6px solid #0F766E;
}

.footer {
    text-align: center;
    color: #6B7280;
    font-size: 0.85rem;
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar Menu
# =========================
with st.sidebar:
    st.markdown("## 🧬 QCNN System")
    st.markdown("**FYP Viva Prototype**")
    st.markdown("---")

    page = option_menu(
        menu_title=None,
        options=[
            "Dashboard",
            "Upload Dataset",
            "QCNN Workflow",
            "Model Performance",
            "About"
        ],
        icons=[
            "house",
            "cloud-upload",
            "cpu",
            "bar-chart-line",
            "info-circle"
        ],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#F7FAF9"
            },
            "icon": {
                "color": "#0F766E",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px 0",
                "border-radius": "12px",
                "padding": "10px"
            },
            "nav-link-selected": {
                "background-color": "#0F766E",
                "color": "white",
                "font-weight": "600"
            },
        }
    )

    st.markdown("---")
    st.caption("Wong Jing Wen")
    st.caption("23004924")
    st.caption("Academic Project I")

# =========================
# Session State
# =========================
if "data" not in st.session_state:
    st.session_state.data = None

if "cleaned_data" not in st.session_state:
    st.session_state.cleaned_data = None

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None

if "sample_index" not in st.session_state:
    st.session_state.sample_index = None

if "sample_id" not in st.session_state:
    st.session_state.sample_id = None

# =========================
# Helper Function: Clean Dataset
# =========================
def clean_dataset(df):
    df = df.copy()

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
        .str.replace("  ", " ", regex=False)
    )

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    return df

# =========================
# Hero Header
# =========================
st.markdown("""
<div class="hero">
    <h1>A Quantum Convolutional Neural Network (QCNN) Framework</h1>
    <p>For Automated Sex Estimation Using Orbital and Nasal Craniofacial Measurements</p>
</div>
""", unsafe_allow_html=True)

# =========================
# Dashboard Page
# =========================
if page == "Dashboard":
    st.markdown("## Dashboard Overview")

    total_records = len(st.session_state.cleaned_data) if st.session_state.cleaned_data is not None else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Dataset Records", total_records)
    col2.metric("Landmarks", "64")
    col3.metric("Measurements", "69")
    col4.metric("Main Model", "QCNN")

    st.markdown("""
<div class="card">
    <div class="small-title">System Workflow</div>
    <br>
    <b>Upload Excel Dataset</b> → 
    <b>Preprocess Measurements</b> → 
    <b>Choose One Sample</b> → 
    <b>Feature Encoding</b> → 
    <b>Run QCNN Workflow</b> → 
    <b>Display Simulated Sex Estimation Result</b>
</div>
""", unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        st.markdown("""
<div class="card">
    <div class="small-title">Prototype Status</div><br>
    <span class="status-ready">Interface Ready</span><br><br>
    This Streamlit prototype demonstrates the intended workflow for the FYP viva.
</div>
""", unsafe_allow_html=True)

    with colB:
        st.markdown("""
<div class="card">
    <div class="small-title">QCNN Status</div><br>
    <span class="status-demo">FYP II Implementation</span><br><br>
    The full QCNN model will be implemented and evaluated during Academic Project II.
</div>
""", unsafe_allow_html=True)

    st.markdown("### Methodology Pipeline")
    st.code("""
HKL CT/DO Data
   ↓
Orbital and Nasal Craniofacial Measurements
   ↓
Data Preprocessing
   ↓
Choose One Sample
   ↓
Quantum Feature Encoding
   ↓
QCNN Model
   ↓
Sex Estimation Output
    """)

    st.info(
        "For Academic Project I, this prototype focuses on dataset upload, preprocessing, "
        "workflow demonstration, and simulated model output. Actual QCNN training will be conducted in Academic Project II."
    )

# =========================
# Upload Dataset Page
# =========================
elif page == "Upload Dataset":
    st.markdown("## Upload Craniofacial Measurement Dataset")

    st.markdown("""
<div class="card">
    Upload the Excel dataset containing orbital and nasal craniofacial measurements.
    For the HKL dataset, the system attempts to read the <b>Raw Data</b> sheet.
</div>
""", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Upload Excel or CSV file",
        type=["xlsx", "csv"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                try:
                    df = pd.read_excel(uploaded_file, sheet_name="Raw Data")
                except Exception:
                    df = pd.read_excel(uploaded_file)

            cleaned_df = clean_dataset(df)

            st.session_state.data = df
            st.session_state.cleaned_data = cleaned_df

            # Reset previous simulated result when new file is uploaded
            st.session_state.prediction = None
            st.session_state.confidence = None
            st.session_state.sample_index = None
            st.session_state.sample_id = None

            st.success("Dataset uploaded and cleaned successfully.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Records", len(cleaned_df))
            col2.metric("Total Columns", len(cleaned_df.columns))
            col3.metric("File Type", uploaded_file.name.split(".")[-1].upper())

            st.markdown("### Dataset Preview")
            st.dataframe(cleaned_df.head(10), use_container_width=True)

            st.markdown("### Dataset Checking")

            missing_df = cleaned_df.isnull().sum().reset_index()
            missing_df.columns = ["Column", "Missing Values"]

            colA, colB = st.columns(2)

            with colA:
                st.markdown("#### Missing Values")
                st.dataframe(missing_df, use_container_width=True)

            with colB:
                st.markdown("#### Duplicate Rows")
                st.metric("Duplicate Rows", cleaned_df.duplicated().sum())

            st.markdown("### Dataset Distribution")

            if "Gender" in cleaned_df.columns:
                gender_counts = cleaned_df["Gender"].value_counts().reset_index()
                gender_counts.columns = ["Gender", "Count"]
                gender_counts["Percentage"] = (
                    gender_counts["Count"] / gender_counts["Count"].sum() * 100
                ).round(1)

                st.markdown("#### Gender Distribution")
                st.dataframe(gender_counts, use_container_width=True)

                gender_chart = alt.Chart(gender_counts).mark_bar(
                    cornerRadiusTopLeft=6,
                    cornerRadiusTopRight=6
                ).encode(
                    x=alt.X("Gender:N", title="Gender", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("Count:Q", title="Number of Cases"),
                    tooltip=["Gender", "Count", "Percentage"]
                ).properties(height=300)

                st.altair_chart(gender_chart, use_container_width=True)

            if "Ethnicity" in cleaned_df.columns:
                ethnicity_counts = cleaned_df["Ethnicity"].value_counts().reset_index()
                ethnicity_counts.columns = ["Ethnicity", "Count"]
                ethnicity_counts["Percentage"] = (
                    ethnicity_counts["Count"] / ethnicity_counts["Count"].sum() * 100
                ).round(1)

                st.markdown("#### Ethnicity Distribution")
                st.dataframe(ethnicity_counts, use_container_width=True)

                ethnicity_chart = alt.Chart(ethnicity_counts).mark_bar(
                    cornerRadiusTopLeft=6,
                    cornerRadiusTopRight=6
                ).encode(
                    x=alt.X("Ethnicity:N", title="Ethnicity", axis=alt.Axis(labelAngle=0)),
                    y=alt.Y("Count:Q", title="Number of Cases"),
                    tooltip=["Ethnicity", "Count", "Percentage"]
                ).properties(height=300)

                st.altair_chart(ethnicity_chart, use_container_width=True)

            st.markdown("### Numerical Feature Summary")

            numeric_df = cleaned_df.select_dtypes(include=["int64", "float64"])

            if len(numeric_df.columns) > 0:
                st.dataframe(numeric_df.describe(), use_container_width=True)
            else:
                st.info("No numerical columns detected for summary statistics.")

        except Exception as e:
            st.error(f"Error reading file: {e}")

# =========================
# QCNN Workflow Page
# =========================
elif page == "QCNN Workflow":
    st.markdown("## QCNN Sex Estimation Workflow")

    if st.session_state.cleaned_data is None:
        st.warning("Please upload a dataset first from the Upload Dataset page.")
    else:
        st.markdown("""
<div class="card">
    This page demonstrates the proposed QCNN-based sex estimation workflow.
    Since the uploaded dataset may contain many subjects, one sample must be chosen for workflow demonstration.
    For Academic Project I, the prediction output is simulated.
</div>
""", unsafe_allow_html=True)

        df = st.session_state.cleaned_data.copy()

        col1, col2, col3 = st.columns(3)
        col1.metric("Feature Set", "Orbital + Nasal")
        col2.metric("Input Type", "Morphometric Measurements")
        col3.metric("Model", "QCNN Framework")

        st.markdown("### Choose One Sample for Demonstration")

        row_options = list(range(len(df)))

        sample_index = st.selectbox(
            "Choose a sample row",
            options=row_options,
            index=None,
            placeholder="Select one sample row first"
        )

        if sample_index is None:
            st.info("Please choose one sample row before running the QCNN workflow demonstration.")
        else:
            # If user changes sample, reset old prediction
            if st.session_state.sample_index != sample_index:
                st.session_state.prediction = None
                st.session_state.confidence = None
                st.session_state.sample_index = sample_index
                st.session_state.sample_id = None

            selected_sample = df.iloc[[sample_index]]

            if "No." in df.columns:
                sample_id = selected_sample["No."].values[0]
            else:
                sample_id = sample_index

            st.session_state.sample_id = sample_id

            st.info(f"Selected sample: Row {sample_index}, Sample ID: {sample_id}")

            st.markdown("### Selected Sample Preview")
            st.dataframe(selected_sample, use_container_width=True)

            st.markdown("### Feature Encoding Plan")

            st.code("""
Selected orbital and nasal measurements
   ↓
Min-Max Normalization
   ↓
Angle Scaling to [0, π]
   ↓
Angle Embedding
   ↓
Quantum Convolution + Pooling Layers
            """)

            st.info(
                "Classical morphometric values from the selected sample will be normalized and encoded "
                "into quantum states using angle embedding before being processed by the QCNN model."
            )

            st.markdown("---")

            if st.button("🚀 Run QCNN Workflow Demonstration", use_container_width=True):
                progress = st.progress(0)

                for percent in range(100):
                    time.sleep(0.01)
                    progress.progress(percent + 1)

                st.session_state.prediction = random.choice(["Male", "Female"])
                st.session_state.confidence = round(random.uniform(80, 95), 2)
                st.session_state.sample_index = sample_index
                st.session_state.sample_id = sample_id

                st.success("Workflow demonstration completed.")

            if st.session_state.prediction is not None:
                st.markdown("## Workflow Demonstration Result")

                st.markdown(f"""
<div class="result-box">
    <h2>Simulated Sex Classification Result: {st.session_state.prediction}</h2>
    <h3>Confidence Score: {st.session_state.confidence}%</h3>
    <p>Selected Sample Row: {st.session_state.sample_index}</p>
    <p>Sample ID: {st.session_state.sample_id}</p>
    <p>Feature Set: Orbital and Nasal Craniofacial Measurements</p>
</div>
""", unsafe_allow_html=True)

                st.warning(
                    "Prototype demonstration only: this prediction is simulated for the selected sample. "
                    "Actual QCNN prediction will be implemented during Academic Project II."
                )

# =========================
# Model Performance Page
# =========================
elif page == "Model Performance":
    st.markdown("## Model Performance Comparison")

    st.warning(
        "Prototype demonstration only: The performance values shown below are simulated. "
        "Actual training and benchmarking using MLP, CNN, XGBoost, and QCNN will be conducted during Academic Project II."
    )

    performance_df = pd.DataFrame({
        "Model": ["MLP", "CNN", "XGBoost", "QCNN"],
        "Status": [
            "Planned classical baseline",
            "Planned classical baseline",
            "Planned classical baseline",
            "Planned proposed model"
        ],
        "Accuracy": [0.72, 0.74, 0.76, 0.80],
        "Precision": [0.71, 0.73, 0.75, 0.79],
        "Recall": [0.70, 0.72, 0.74, 0.78],
        "F1-score": [0.70, 0.72, 0.74, 0.78]
    })

    st.markdown("### Simulated Performance Table")
    st.dataframe(performance_df, use_container_width=True)

    st.caption(
        "Note: These values are dummy values used to demonstrate the intended performance comparison layout."
    )

    df_melt = performance_df.melt(
        id_vars=["Model", "Status"],
        value_vars=["Accuracy", "Precision", "Recall", "F1-score"],
        var_name="Metric",
        value_name="Score"
    )

    df_melt["Score"] = df_melt["Score"].astype(float)

    chart = alt.Chart(df_melt).mark_bar(
        cornerRadiusTopLeft=6,
        cornerRadiusTopRight=6
    ).encode(
        x=alt.X(
            "Model:N",
            title="Model",
            sort=["MLP", "CNN", "XGBoost", "QCNN"],
            axis=alt.Axis(labelAngle=0)
        ),
        xOffset=alt.XOffset("Metric:N"),
        y=alt.Y(
            "Score:Q",
            title="Score",
            scale=alt.Scale(domain=[0, 1])
        ),
        color=alt.Color(
            "Metric:N",
            title="Metric",
            scale=alt.Scale(
                range=["#0F766E", "#14B8A6", "#5EEAD4", "#99F6E4"]
            )
        ),
        tooltip=[
            alt.Tooltip("Model:N"),
            alt.Tooltip("Status:N"),
            alt.Tooltip("Metric:N"),
            alt.Tooltip("Score:Q", format=".2f")
        ]
    ).properties(
        height=380
    )

    st.markdown("### Performance Comparison Chart")
    st.altair_chart(chart, use_container_width=True)

    st.markdown("""
<div class="card">
    <div class="small-title">Interpretation</div><br>
    This chart demonstrates how the final system will compare the proposed QCNN model 
    against selected classical machine learning baselines. In Academic Project II, 
    the dummy values will be replaced with actual experimental results using the same 
    train-test split and evaluation metrics.
</div>
""", unsafe_allow_html=True)

    st.markdown("### Example Confusion Matrix Layout")

    cm = pd.DataFrame(
        [[88, 12], [15, 85]],
        columns=["Predicted Male", "Predicted Female"],
        index=["Actual Male", "Actual Female"]
    )

    st.dataframe(cm, use_container_width=True)

    st.caption(
        "The confusion matrix is a dummy layout for demonstration only."
    )

# =========================
# About Page
# =========================
elif page == "About":
    st.markdown("## About This Prototype")

    st.markdown("""
<div class="card">
    <div class="small-title">Project Title</div><br>
    A Quantum Convolutional Neural Network (QCNN) Framework for Automated Sex Estimation 
    Using Orbital and Nasal Craniofacial Measurements
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
    <div class="small-title">System Purpose</div><br>
    This prototype demonstrates the intended workflow for uploading craniofacial measurement data, 
    preprocessing the dataset, choosing one sample, and displaying a simulated sex estimation result 
    through a QCNN-based framework.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
    <div class="small-title">Current Implementation Scope</div><br>
    For Academic Project I, this prototype focuses on workflow demonstration. 
    Actual QCNN model training, hyperparameter tuning, and benchmarking against classical models 
    will be completed during Academic Project II.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="card">
    <div class="small-title">Collaborator</div><br>
    Hospital Kuala Lumpur Forensic Dentistry<br>
    Primary clinical collaborator: Dr. Lai Poh Soon
</div>
""", unsafe_allow_html=True)

# =========================
# Footer
# =========================
st.markdown("""
<div class="footer">
    FYP Viva Prototype | Wong Jing Wen | 23004924
</div>
""", unsafe_allow_html=True)