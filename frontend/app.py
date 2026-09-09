import streamlit as st
import requests
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ChurnGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "prediction_history" not in st.session_state:
    st.session_state.prediction_history = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    /* Status cards */
    .status-card {
        padding: 12px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #dddddd;
        margin-bottom: 10px;
    }

    /* Result card */
    .result-card {
        padding: 25px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid #dddddd;
        margin-top: 15px;
    }

    .probability {
        font-size: 48px;
        font-weight: 800;
    }

    .risk-text {
        font-size: 24px;
        font-weight: 700;
    }

    /* Section spacing */
    .section-space {
        margin-top: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ ChurnGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Customer Churn Intelligence'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# API STATUS
# ============================================================

API_URL = "http://127.0.0.1:8000"

status_col1, status_col2, status_col3 = st.columns(3)

with status_col1:

    try:
        health_response = requests.get(
            f"{API_URL}/health",
            timeout=3
        )

        if health_response.status_code == 200:
            st.success("🟢 API Connected")
        else:
            st.warning("🟡 API Response Issue")

    except requests.exceptions.RequestException:
        st.error("🔴 API Offline")


with status_col2:
    st.info("🤖 ML Model: Ready")


with status_col3:
    st.info("⚡ FastAPI Backend")


st.divider()


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.header("👤 Customer Profile")

col1, col2, col3 = st.columns(3)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )


with col2:

    partner = st.selectbox(
        "Partner",
        ["No", "Yes"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["No", "Yes"]
    )


with col3:

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=100,
        value=12
    )


st.divider()


# ============================================================
# SERVICES
# ============================================================

st.header("📡 Service Information")

col1, col2, col3 = st.columns(3)

with col1:

    phone_service = st.selectbox(
        "Phone Service",
        ["No", "Yes"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["No", "Yes", "No phone service"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )


with col2:

    online_security = st.selectbox(
        "Online Security",
        ["No", "Yes", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["No", "Yes", "No internet service"]
    )

    device_protection = st.selectbox(
        "Device Protection",
        ["No", "Yes", "No internet service"]
    )


with col3:

    tech_support = st.selectbox(
        "Tech Support",
        ["No", "Yes", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["No", "Yes", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["No", "Yes", "No internet service"]
    )


st.divider()


# ============================================================
# BILLING
# ============================================================

st.header("💳 Billing Information")

col1, col2, col3, col4 = st.columns(4)

with col1:

    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )


with col2:

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["No", "Yes"]
    )


with col3:

    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )


with col4:

    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0,
        step=0.5
    )


total_charges = st.number_input(
    "Total Charges",
    min_value=0.0,
    value=840.0,
    step=10.0
)


st.divider()


# ============================================================
# PREDICTION BUTTON
# ============================================================

st.header("🤖 Churn Analysis")

predict_button = st.button(
    "🔮 ANALYZE CUSTOMER CHURN",
    use_container_width=True,
    type="primary"
)


# ============================================================
# SEND DATA TO API
# ============================================================

if predict_button:

    customer_data = {

        "gender": gender,

        "SeniorCitizen": (
            1 if senior_citizen == "Yes" else 0
        ),

        "Partner": partner,

        "Dependents": dependents,

        "tenure": tenure,

        "PhoneService": phone_service,

        "MultipleLines": multiple_lines,

        "InternetService": internet_service,

        "OnlineSecurity": online_security,

        "OnlineBackup": online_backup,

        "DeviceProtection": device_protection,

        "TechSupport": tech_support,

        "StreamingTV": streaming_tv,

        "StreamingMovies": streaming_movies,

        "Contract": contract,

        "PaperlessBilling": paperless_billing,

        "PaymentMethod": payment_method,

        "MonthlyCharges": monthly_charges,

        "TotalCharges": total_charges
    }


    try:

        with st.spinner("🤖 AI is analyzing customer behavior..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=customer_data,
                timeout=10
            )


        if response.status_code == 200:

            result = response.json()

            prediction = result["churn_prediction"]
            probability = result["churn_probability"]
            risk = result["risk_level"]
            recommendation = result["recommendation"]


            # ==================================================
            # SAVE TO HISTORY
            # ==================================================

            st.session_state.prediction_history.append(
                {
                    "Time": datetime.now().strftime("%H:%M:%S"),
                    "Prediction": prediction,
                    "Probability": f"{probability}%",
                    "Risk": risk
                }
            )


            # ==================================================
            # RESULT
            # ==================================================

            st.divider()

            st.subheader("📊 Prediction Result")


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Churn Prediction",
                    prediction
                )


            with col2:

                st.metric(
                    "Churn Probability",
                    f"{probability}%"
                )


            with col3:

                st.metric(
                    "Risk Level",
                    risk
                )


            # ==================================================
            # PROBABILITY BAR
            # ==================================================

            st.write("### 🎯 Churn Probability")

            st.progress(
                min(int(probability), 100)
            )


            # ==================================================
            # RISK MESSAGE
            # ==================================================

            if risk == "High":

                st.error(
                    "🚨 HIGH CHURN RISK — Immediate attention recommended."
                )

            elif risk == "Medium":

                st.warning(
                    "⚠️ MEDIUM CHURN RISK — Customer should be monitored."
                )

            else:

                st.success(
                    "✅ LOW CHURN RISK — Customer appears relatively stable."
                )


            # ==================================================
            # RECOMMENDATION
            # ==================================================

            st.subheader("💡 Recommended Action")

            st.info(recommendation)


            # ==================================================
            # CUSTOMER SUMMARY
            # ==================================================

            st.subheader("👤 Customer Summary")

            summary_col1, summary_col2, summary_col3 = st.columns(3)

            with summary_col1:

                st.write(f"**Gender:** {gender}")
                st.write(f"**Tenure:** {tenure} months")
                st.write(f"**Contract:** {contract}")


            with summary_col2:

                st.write(
                    f"**Internet:** {internet_service}"
                )

                st.write(
                    f"**Monthly Charges:** {monthly_charges:.2f}"
                )

                st.write(
                    f"**Payment:** {payment_method}"
                )


            with summary_col3:

                st.write(
                    f"**Tech Support:** {tech_support}"
                )

                st.write(
                    f"**Online Security:** {online_security}"
                )

                st.write(
                    f"**Paperless Billing:** {paperless_billing}"
                )


        else:

            st.error(
                f"❌ API returned error {response.status_code}"
            )


    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Cannot connect to FastAPI. "
            "Please make sure the backend server is running."
        )


    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The API request timed out."
        )


    except Exception as e:

        st.error(
            f"❌ Unexpected error: {str(e)}"
        )


# ============================================================
# PREDICTION HISTORY
# ============================================================

if st.session_state.prediction_history:

    st.divider()

    st.header("📋 Prediction History")

    st.dataframe(
        st.session_state.prediction_history,
        use_container_width=True,
        hide_index=True
    )

    if st.button("🗑️ Clear Prediction History"):

        st.session_state.prediction_history = []

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "ChurnGuard AI • Machine Learning + FastAPI + Streamlit"
)