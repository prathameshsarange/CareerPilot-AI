import os

import pandas as pd
import streamlit as st

from services.dataset_service import analyze_dataset
from utils.chart_generator import generate_histogram


def show_dataset():

    st.title("📊 AI Dataset Analyzer")

    st.markdown(
        """
Analyze your dataset using AI.

✔ Dataset Summary

✔ Data Preview

✔ Visualization

✔ AI Insights

✔ ML Algorithm Recommendation
"""
    )

    uploaded_file = st.file_uploader(
        "Upload CSV Dataset",
        type=["csv"],
        key="dataset"
    )

    if uploaded_file is None:
        return

    os.makedirs("data", exist_ok=True)

    save_path = os.path.join(
        "data",
        uploaded_file.name
    )

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        df = pd.read_csv(save_path)
    except Exception as e:
        st.error(f"Unable to read CSV.\n\n{e}")
        return

    st.success(f"✅ Uploaded: {uploaded_file.name}")

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Rows", len(df))

    with c2:
        st.metric("Columns", len(df.columns))

    with c3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    with c4:
        st.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.divider()

    preview_tab, info_tab = st.tabs(
        [
            "📄 Preview",
            "📋 Dataset Info"
        ]
    )

    with preview_tab:
        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )

    with info_tab:

        info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values
        })

        st.dataframe(
            info,
            use_container_width=True
        )

    st.divider()

    if st.button(
        "🚀 Analyze Dataset",
        use_container_width=True
    ):

        with st.spinner("🤖 AI is analyzing your dataset..."):

            try:

                dataset_result, ml_result = analyze_dataset(
                    save_path
                )

                chart = generate_histogram(
                    save_path
                )

            except Exception as e:

                st.error(str(e))

                return

        st.success("✅ Analysis Completed")

        analysis_tab, chart_tab, ml_tab = st.tabs(
            [
                "📊 AI Analysis",
                "📈 Charts",
                "🧠 ML Advisor"
            ]
        )

        with analysis_tab:

            st.markdown(dataset_result)

        with chart_tab:

            if chart:
                st.image(
                    chart,
                    use_container_width=True
                )
            else:
                st.info("No chart generated.")

        with ml_tab:

            st.markdown(ml_result)

        st.divider()

        st.info(
            "💡 Tip: Clean missing values and engineer better features before training ML models."
        )