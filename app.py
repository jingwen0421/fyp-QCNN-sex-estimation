from html import escape
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import streamlit as st
import pandas as pd
import altair as alt

MEASUREMENTS = {
    "Ec-Dc Orbital Width": "Overall orbital width",
    "REc-RDc Right Orbital Width": "Right orbital width",
    "LEc-LDc Left Orbital Width": "Left orbital width",
    "UMo-Lmo Orbital Height": "Overall orbital height",
    "RUMo-RLMo Right Orbital Height": "Right orbital height",
    "LUMo-LLMo Left Orbital Height": "Left orbital height",
    "RAI-LAI Nasal Width": "Nasal width",
    "Rh-Ns Nasal Height": "Nasal height",
}
RESULTS = Path(__file__).resolve().parent / "results" / "qcnn_baseline"


def measurement_columns(data):
    return {" ".join(str(column).split()).casefold(): column for column in data.columns}

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="QCNN Sex Estimation System",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS Design
# =========================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #F7FAF9;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1280px;
    padding-top: 2.75rem;
    padding-bottom: 2rem;
}

[data-testid="stMetric"] {
    padding: 1rem 1.15rem;
    background: #FFFFFF;
    border: 1px solid #DCECE8;
    border-radius: 14px;
}

[data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
    color: #17433F;
}

[data-testid="stFileUploaderDropzone"] {
    background: #EDF8F5;
    border: 1px dashed #8FC9BD;
    border-radius: 14px;
    padding: 1.15rem;
}


[data-testid="stSidebarCollapsedControl"] { display: none; }
.block-container { padding-top: 2.3rem; }
.st-key-cranio_nav { border-bottom: 1px solid #D6E7E2; padding-bottom: .65rem; }
.st-key-cranio_nav [data-testid="stHorizontalBlock"] { align-items: center; flex-wrap: wrap; }
.st-key-cranio_nav [data-testid="stColumn"] { min-width: max-content; }
.st-key-cranio_nav button { border: none; white-space: nowrap; }
.st-key-cranio_nav button[kind="primary"] { background: #E5F3EF; color: #17433F; }
.cranio-brand { font-size: 1.3rem; font-weight: 700; color: #17433F; }
.cranio-kicker { font-size: .76rem; letter-spacing: .08em; color: #0F766E; }
.cranio-title { margin: .15rem 0 .5rem; font-size: clamp(1.65rem, 3vw, 2.25rem); }
.cranio-rule { border-bottom: 1px solid #D6E7E2; padding: .15rem 0 .55rem; margin: .2rem 0 .85rem; }
.cranio-panel { background: white; border: 1px solid #D6E7E2; border-radius: 14px; padding: 1rem; }
.cranio-panel h3 { font-size: 1.05rem; margin: 0 0 .55rem; padding: 0; }
.cranio-panel p { margin: 0; }
.cranio-mint { background: #E4F3EE; }
.cranio-readiness { background: #FCFEFD; }
.cranio-sample { background: #FAFCF8; }
.cranio-pair { display: grid; grid-template-columns: 1.8fr 1fr; gap: .7rem; }
.cranio-summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: .7rem; margin-top: .7rem; }
.cranio-values { display: flex; flex-wrap: wrap; gap: .7rem 1.2rem; margin: .6rem 0 1.2rem; font-size: .84rem; }
.cranio-values strong { display: block; font-size: 1.2rem; }
.cranio-count { padding: .55rem .8rem; background: #DDEFE9; border-radius: 8px; }
.cranio-count-nasal { background: #D2E9E0; }
.cranio-list { list-style: none; margin: .65rem 0 0; padding: 0; }
.cranio-list li { display: flex; justify-content: space-between; gap: .5rem; padding: .62rem 0; border-top: 1px solid #D6E7E2; font-size: .9rem; }
.cranio-list b { font-weight: 500; text-align: right; }
.cranio-bar { display: grid; grid-template-columns: 4rem minmax(0,1fr) 3.6rem; gap: .55rem; align-items: center; margin: .55rem 0; font-size: .8rem; }
.cranio-track { height: .48rem; border-radius: 20px; background: white; overflow: hidden; }
.cranio-track span { display: block; height: 100%; background: #0F766E; border-radius: 20px; }
.cranio-track .cranio-qcnn { background: #478B78; }
.cranio-bar b { text-align: right; }
@media (max-width: 950px) {
    .cranio-pair { grid-template-columns: 1fr; }
}
@media (max-width: 560px) {
    .cranio-summary { grid-template-columns: 1fr; }
}
[class*="st-key-cranio_inner"] {
    background: #FFFFFF;
    border-color: #D6E7E2;
    border-radius: 14px;
}
.st-key-cranio_inner_schema, .st-key-cranio_inner_result { background: #E8F5F1; }
.cranio-matrix { width: 100%; border-spacing: 5px; text-align: center; }
.cranio-matrix th { padding: .45rem; font-size: .82rem; font-weight: 500; }
.cranio-matrix td { background: #F1F8F6; border-radius: 8px; padding: .8rem .4rem; font-weight: 600; }
.cranio-matrix td.correct { background: #D4EBE4; }
.cranio-output { font-size: 1.75rem; font-weight: 650; margin: .3rem 0; }
.cranio-table-wrap { overflow-x: auto; background: white; border: 1px solid #D6E7E2; border-radius: 12px; }
.cranio-table { width: 100%; border-collapse: collapse; font-size: .85rem; }
.cranio-table th, .cranio-table td { padding: .66rem .75rem; text-align: right; white-space: nowrap; border-bottom: 1px solid #E3EFEB; }
.cranio-table thead th { background: #F0F8F6; color: #17433F; font-weight: 600; }
.cranio-table thead tr:first-child th { background: #E5F3EF; text-align: center; }
.cranio-table td { font-variant-numeric: tabular-nums; }
.cranio-table tbody tr:nth-child(even) { background: #F8FCFB; }
.cranio-table tbody tr:last-child td { border-bottom: 0; }
.cranio-table tbody td:first-child { text-align: left; font-weight: 600; }
[data-testid="stTabs"] [role="tablist"] {
    gap: .5rem;
    flex-wrap: wrap;
    padding: .15rem .15rem .55rem;
}
[data-testid="stTabs"] [role="tab"] {
    min-height: 2.65rem;
    padding: .4rem .95rem;
    border: 1px solid #D6E7E2;
    border-radius: 9px;
    background: #FFFFFF;
    color: #17433F;
}
[data-testid="stTabs"] [role="tab"]:hover { background: #F0F8F6; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #DFF2EC;
    border-color: #8FC9BD;
    color: #0F665F;
    font-weight: 600;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"],
[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none; }
</style>
""", unsafe_allow_html=True)

def page_heading(title, label):
    st.markdown(
        f'<div class="cranio-kicker">{label}</div><h1 class="cranio-title">{title}</h1>',
        unsafe_allow_html=True,
    )


# Top navigation
def open_page(destination):
    st.session_state.page = destination


page = st.session_state.get("page", "Dashboard")
if page == "About":
    page = "Dashboard"
    st.session_state.page = page
with st.container(key="cranio_nav"):
    brand, *tabs = st.columns([2.4, 1, .9, 1.3, 1], gap="small")
    brand.markdown('<div class="cranio-brand">◒ CranioLab</div>', unsafe_allow_html=True)
    for tab, label, destination in zip(tabs,
        ("Overview", "Dataset", "Sex estimation", "Evaluation"),
        ("Dashboard", "Upload Dataset", "QCNN Workflow", "Model Performance")):
        tab.button(label, key=f"nav_{destination}", on_click=open_page, args=(destination,),
                   type="primary" if page == destination else "secondary", width="stretch")

# =========================
# Session State
# =========================
if "data" not in st.session_state:
    st.session_state.data = None

if "cleaned_data" not in st.session_state:
    st.session_state.cleaned_data = None

if "prediction" not in st.session_state:
    st.session_state.prediction = None

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
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype("string").str.strip()

    return df

# =========================
# Dashboard Page
# =========================
if page == "Dashboard":
    data = st.session_state.cleaned_data
    comparison_path = RESULTS / "model_comparison.csv"
    comparison = pd.read_csv(comparison_path) if comparison_path.is_file() else None
    main, sample = st.columns([2.85, 1], gap="medium")

    with main:
        title, action = st.columns([3, 1.2], vertical_alignment="center")
        title.markdown(
            '<div class="cranio-kicker">ORBITAL + NASAL MORPHOMETRICS</div>'
            '<h1 class="cranio-title">Craniofacial workspace</h1>',
            unsafe_allow_html=True,
        )
        action.button("Upload dataset", key="overview_upload", type="primary",
                      on_click=open_page, args=("Upload Dataset",), width="stretch")
        st.markdown('<div class="cranio-rule">Research overview</div>', unsafe_allow_html=True)

        bars = ""
        if comparison is not None:
            for name, accuracy in comparison[["Model", "Accuracy"]].itertuples(index=False):
                percent = min(100, max(0, 100 * float(accuracy)))
                bars += (
                    f'<div class="cranio-bar"><span>{escape(str(name))}</span>'
                    f'<div class="cranio-track" aria-hidden="true"><span class="{"cranio-qcnn" if name == "QCNN" else ""}" style="width:{percent:.2f}%"></span></div>'
                    f'<b>{percent:.2f}%</b></div>'
                )
        count = len(data) if data is not None else 0
        dataset_status = "Uploaded" if data is not None else "Awaiting upload"
        model_status = "Saved" if comparison is not None else "No saved results"
        model_count = f"{len(comparison)} saved models" if comparison is not None else "No saved results"
        st.markdown(f"""
<div class="cranio-pair">
    <section class="cranio-panel cranio-mint">
        <h3>Measurement dataset</h3>
        <div class="cranio-values">
            <div>Uploaded records<strong>{count:,}</strong></div>
            <div>Selected features<strong>{len(MEASUREMENTS)}</strong></div>
            <div>Input format<strong>Excel / CSV</strong></div>
        </div>
        <h3>Saved test accuracy</h3>
        {bars or '<p>No saved results</p>'}
    </section>
    <section class="cranio-panel cranio-readiness">
        <h3>Experiment readiness</h3>
        <ul class="cranio-list">
            <li>Required inputs · {len(MEASUREMENTS)}</li>
            <li>Dataset · {dataset_status}</li>
            <li>Model results · {model_status}</li>
            <li>Live prediction · Saved QCNN</li>
        </ul>
    </section>
</div>
<div class="cranio-summary">
    <section class="cranio-panel"><h3>Model evaluation</h3><p>{model_count}</p></section>
    <section class="cranio-panel"><h3>Input quality</h3><p>{"See upload checks" if data is not None else "Check after upload"}</p></section>
    <section class="cranio-panel"><h3>Research scope</h3><p>{len(MEASUREMENTS)} measurements</p></section>
</div>
""", unsafe_allow_html=True)

    with sample:
        position = st.session_state.get("sample_index")
        selected = data.iloc[position] if data is not None and position is not None and 0 <= position < len(data) else None
        columns = measurement_columns(data) if selected is not None else {}
        rows = []
        for heading, label in MEASUREMENTS.items():
            column = columns.get(heading.casefold())
            value = escape(str(selected[column])) if column is not None else "—"
            rows.append(f"<li><span>{label}</span><b>{value}</b></li>")
        selected_label = f"Selected row: {position}" if selected is not None else "No sample selected"
        st.markdown(f"""
<section class="cranio-panel cranio-sample">
    <div class="cranio-kicker">SAMPLE INSPECTION</div>
    <h2>Measurements</h2>
    <div class="cranio-values">
        <div class="cranio-count">Orbital<strong>06</strong></div>
        <div class="cranio-count cranio-count-nasal">Nasal<strong>02</strong></div>
    </div>
    <p>{selected_label}</p>
    <ul class="cranio-list">{"".join(rows)}</ul>
</section>
""", unsafe_allow_html=True)

# =========================
# Upload Dataset Page
# =========================
elif page == "Upload Dataset":
    page_heading("Measurement dataset", "DATASET")
    upload, schema = st.columns([1.65, 1], gap="medium")
    with upload:
        with st.container(border=True, key="cranio_inner_upload"):
            st.markdown("### Upload dataset")
            uploaded_file = st.file_uploader("Measurement file", type=["xls", "xlsx", "csv"], label_visibility="collapsed")
            st.download_button("Download CSV template", pd.DataFrame(columns=list(MEASUREMENTS)).to_csv(index=False),
                               file_name="cranioLab_measurements.csv", mime="text/csv")
    with schema:
        with st.container(border=True, key="cranio_inner_schema"):
            st.markdown("### Required measurements")
            items = "".join(f"<li>{label}</li>" for label in MEASUREMENTS.values())
            st.markdown(f'<ul class="cranio-list">{items}</ul>', unsafe_allow_html=True)

    upload_key = (uploaded_file.name, sha256(uploaded_file.getvalue()).hexdigest()) if uploaded_file is not None else None
    if upload_key is not None and upload_key != st.session_state.get("dataset_key"):
        try:
            contents = BytesIO(uploaded_file.getvalue())
            if uploaded_file.name.lower().endswith(".csv"):
                df = pd.read_csv(contents)
            else:
                with pd.ExcelFile(contents) as workbook:
                    sheet = "Raw Data" if "Raw Data" in workbook.sheet_names else 0
                    df = workbook.parse(sheet)

            cleaned_df = clean_dataset(df)
            if cleaned_df.empty:
                raise ValueError("The file contains no measurement records.")
            normalized = [" ".join(col.split()).casefold() for col in cleaned_df.columns]
            if len(set(normalized)) != len(normalized):
                raise ValueError("The file contains duplicate column headings.")

            st.session_state.data = df
            st.session_state.cleaned_data = cleaned_df
            st.session_state.dataset_key = upload_key

            # Reset the previous result when a new file is uploaded
            st.session_state.prediction = None
            st.session_state.sample_index = None
            st.session_state.sample_id = None

        except (ValueError, ImportError, OSError) as e:
            st.error(f"Could not load the file: {e}")

    if st.session_state.cleaned_data is not None:
        try:
            cleaned_df = st.session_state.cleaned_data
            filename = st.session_state.get("dataset_key", ("Dataset",))[0]
            st.caption(f"Active dataset: {filename}")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Records", len(cleaned_df))
            col2.metric("Total Columns", len(cleaned_df.columns))
            col3.metric("File Type", filename.split(".")[-1].upper())

            preview, quality, distributions, summary = st.tabs(
                ["Preview", "Input checks", "Distributions", "Summary"]
            )
            with preview:
                headings = measurement_columns(cleaned_df)
                preview_rows = cleaned_df.head(10)
                st.caption(f"First {len(preview_rows)} of {len(cleaned_df):,} records")
                short_labels = ("Overall width", "Right width", "Left width",
                                "Overall height", "Right height", "Left height", "Width", "Height")
                header = "".join(f'<th scope="col">{label}</th>' for label in short_labels)
                rows = []
                for position, (_, record) in enumerate(preview_rows.iterrows(), start=1):
                    values = [record.get("No.", position), record.get("Gender", "—")]
                    for heading in MEASUREMENTS:
                        column = headings.get(heading.casefold())
                        value = record[column] if column is not None else None
                        number = pd.to_numeric(value, errors="coerce")
                        values.append(f"{number:.2f}" if pd.notna(number) else "—")
                    cells = "".join(f"<td>{escape(str(value))}</td>" for value in values)
                    rows.append(f"<tr>{cells}</tr>")
                st.markdown(
                    '<div class="cranio-table-wrap"><table class="cranio-table" aria-label="Measurement preview">'
                    '<thead><tr><th rowspan="2" scope="col">Record</th><th rowspan="2" scope="col">Reference sex</th>'
                    '<th colspan="6" scope="colgroup">Orbital measurements</th><th colspan="2" scope="colgroup">Nasal measurements</th>'
                    f'</tr><tr>{header}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>',
                    unsafe_allow_html=True,
                )
                with st.expander("All columns"):
                    st.dataframe(preview_rows, hide_index=True, width="stretch")
            with quality:
                columns = measurement_columns(cleaned_df)
                checks = []
                for heading, label in MEASUREMENTS.items():
                    column = columns.get(heading.casefold())
                    invalid = None if column is None else int(pd.to_numeric(cleaned_df[column], errors="coerce").isna().sum())
                    checks.append({"Measurement": label, "Column present": column is not None, "Missing or nonnumeric": invalid})
                st.dataframe(pd.DataFrame(checks), hide_index=True, width="stretch")


                missing_df = cleaned_df.isnull().sum().reset_index()
                missing_df.columns = ["Column", "Missing Values"]

                colA, colB = st.columns(2)

                with colA:
                    st.markdown("#### Missing Values")
                    st.dataframe(missing_df, use_container_width=True)

                with colB:
                    st.markdown("#### Duplicate Rows")
                    st.metric("Duplicate Rows", cleaned_df.duplicated().sum())

            with distributions:

                if "Gender" in cleaned_df.columns:
                    gender_counts = cleaned_df["Gender"].value_counts().reset_index()
                    gender_counts.columns = ["Gender", "Count"]
                    gender_counts["Percentage"] = (
                        gender_counts["Count"] / gender_counts["Count"].sum() * 100
                    ).round(1)

                    st.markdown("#### Gender Distribution")
                    st.dataframe(gender_counts, use_container_width=True)

                    gender_chart = alt.Chart(gender_counts).mark_bar(
                        color="#0F766E",
                        cornerRadiusTopLeft=6,
                        cornerRadiusTopRight=6
                    ).encode(
                        x=alt.X("Gender:N", title="Gender", axis=alt.Axis(labelAngle=0)),
                        y=alt.Y("Count:Q", title="Number of Cases"),
                        tooltip=["Gender", "Count", "Percentage"]
                    ).properties(height=225)

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
                        color="#0F766E",
                        cornerRadiusTopLeft=6,
                        cornerRadiusTopRight=6
                    ).encode(
                        x=alt.X("Ethnicity:N", title="Ethnicity", axis=alt.Axis(labelAngle=0)),
                        y=alt.Y("Count:Q", title="Number of Cases"),
                        tooltip=["Ethnicity", "Count", "Percentage"]
                    ).properties(height=225)

                    st.altair_chart(ethnicity_chart, use_container_width=True)

            with summary:

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
    page_heading("Sex estimation", "SAMPLE WORKSPACE")
    data = st.session_state.cleaned_data
    mode = st.radio("Input source", ["Manual entry", "Uploaded dataset"], horizontal=True)

    @st.cache_resource
    def saved_qcnn():
        from qcnn_inference import load_qcnn
        return load_qcnn(RESULTS)

    sample, result = st.columns([1.5, 1], gap="medium")
    values = {}
    submitted = False
    source = (mode, None)

    with sample:
        with st.container(border=True, key="cranio_inner_sample"):
            if mode == "Manual entry":
                with st.form("manual_measurements"):
                    st.markdown("### Measurements")
                    st.caption("Enter all eight values in millimetres.")
                    left, right = st.columns(2)
                    for index, (heading, label) in enumerate(MEASUREMENTS.items()):
                        with (left if index % 2 == 0 else right):
                            values[heading] = st.number_input(
                                label, value=None, min_value=0.0, step=0.01,
                                format="%.2f", placeholder="mm", key=f"manual_{index}",
                            )
                    submitted = st.form_submit_button("Predict", type="primary", width="stretch")
            elif data is None or data.empty:
                st.info("Upload a dataset first or choose Manual entry.")
            else:
                st.markdown("### Sample")
                previous = st.session_state.sample_index
                default = previous if previous is not None and 0 <= previous < len(data) else None
                position = st.selectbox("Row", range(len(data)), index=default, placeholder="Select a row")
                st.session_state.sample_index = position
                source = (mode, position)
                if position is not None:
                    selected = data.iloc[position]
                    columns = measurement_columns(data)
                    for heading in MEASUREMENTS:
                        column = columns.get(heading.casefold())
                        values[heading] = pd.to_numeric(selected[column], errors="coerce") if column is not None else None
                    st.dataframe(pd.DataFrame([
                        {"Measurement": label, "Value": f"{values[heading]:.2f}" if pd.notna(values[heading]) else "—"}
                        for heading, label in MEASUREMENTS.items()
                    ]), hide_index=True, width="stretch")
                    submitted = st.button("Predict", type="primary", width="stretch")

    if submitted:
        st.session_state.prediction = None
        if any(value is None or pd.isna(value) for value in values.values()):
            st.error("Provide all eight numeric measurements before predicting.")
        else:
            try:
                from qcnn_inference import predict_measurements
                label, clipped = predict_measurements(values, saved_qcnn())
                st.session_state.prediction = {"source": source, "label": label, "clipped": clipped}
            except (ValueError, KeyError, OSError, ImportError) as error:
                st.error(f"Prediction unavailable: {error}")

    with result:
        with st.container(border=True, key="cranio_inner_result"):
            st.markdown("### Result")
            st.caption("Initial QCNN · simulated quantum circuit")
            prediction = st.session_state.prediction
            if isinstance(prediction, dict) and prediction["source"] == source:
                st.markdown(f'<div class="cranio-output">{escape(prediction["label"])}</div>', unsafe_allow_html=True)
                st.caption("Prediction for the last submitted measurements.")
                if prediction["clipped"]:
                    names = ", ".join(MEASUREMENTS[name] for name in prediction["clipped"])
                    st.warning(f"Outside the training range and clipped: {names}.")
            else:
                st.write("No prediction yet")

# =========================
# Model Performance Page
# =========================
elif page == "Model Performance":
    page_heading("Model evaluation", "SAVED EXPERIMENTS")

    comparison_path = RESULTS / "model_comparison.csv"
    matrix_path = RESULTS / "confusion_matrix.csv"
    if not comparison_path.is_file():
        st.info("No saved experiment results yet.")
    else:
        comparison = pd.read_csv(comparison_path)
        st.caption("Grouped split · 832 training / 210 test · 8 measurements")

        accuracy_panel, matrix_panel = st.columns([1.3, 1], gap="medium")
        with accuracy_panel:
            with st.container(border=True, key="cranio_inner_accuracy"):
                st.markdown("### Test accuracy")
                chart = alt.Chart(comparison).encode(
                    y=alt.Y("Model:N", title=None, sort=comparison["Model"].tolist()),
                    x=alt.X("Accuracy:Q", title=None,
                            scale=alt.Scale(domain=[0, 1]),
                            axis=alt.Axis(format=".0%", values=[0, 0.25, 0.5, 0.75, 1])),
                    tooltip=[alt.Tooltip("Model:N"), alt.Tooltip("Accuracy:Q", format=".2%")],
                )
                bars = chart.mark_bar(color="#0F766E", cornerRadiusEnd=4, size=18)
                labels = chart.mark_text(align="right", dx=-5, color="white").encode(
                    text=alt.Text("Accuracy:Q", format=".2%")
                )
                st.altair_chart((bars + labels).properties(height=200), width="stretch")

        with matrix_panel:
            with st.container(border=True, key="cranio_inner_matrix"):
                st.markdown("### QCNN confusion matrix")
                if matrix_path.is_file():
                    matrix = pd.read_csv(matrix_path, index_col=0)
                    headings = "".join(f'<th scope="col">{escape(str(label).removeprefix("Predicted "))}</th>' for label in matrix.columns)
                    rows = []
                    for i, (label, values) in enumerate(matrix.iterrows()):
                        cells = "".join(
                            f'<td class="{"correct" if i == j else ""}">{escape(str(value))}</td>'
                            for j, value in enumerate(values)
                        )
                        rows.append(f'<tr><th scope="row">{escape(str(label).removeprefix("Actual "))}</th>{cells}</tr>')
                    st.markdown(
                        f'<table class="cranio-matrix" aria-label="QCNN confusion matrix">'
                        f'<thead><tr><th>Actual / Predicted</th>{headings}</tr></thead>'
                        f'<tbody>{"".join(rows)}</tbody></table>', unsafe_allow_html=True
                    )
                else:
                    st.info("No saved confusion matrix.")

        with st.expander("All metrics"):
            display_scores = comparison.copy()
            percentage_columns = [name for name in comparison if name not in ("Model", "ROC AUC")]
            display_scores[percentage_columns] = display_scores[percentage_columns] * 100
            st.dataframe(display_scores, hide_index=True, width="stretch", column_config={
                "Model": st.column_config.Column("Model", pinned=True),
                "ROC AUC": st.column_config.NumberColumn(format="%.4f"),
                **{column: st.column_config.NumberColumn(format="%.2f%%") for column in percentage_columns},
            })
            st.caption("Binary precision, recall and F1 use male as the positive class.")
