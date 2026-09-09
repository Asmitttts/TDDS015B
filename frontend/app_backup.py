import streamlit as st
import requests


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ChurnGuard AI",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
    }

    .metric-number {
        font-size: 40px;
        font-weight: bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ ChurnGuard AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Customer Churn Prediction System'
    '</div>',
    unsafe_allow_html=True
)


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

st.header("📡 Services")

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
# BILLING INFORMATION
# ============================================================

st.header("💳 Billing Information")

col1, col2, col3, col4 = st.columns(4)

with col1:

    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
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

st.subheader("🤖 Churn Prediction")

predict_button = st.button(
    "🔮 Predict Customer Churn",
    use_container_width=True
)


# ============================================================
# API REQUEST
# ============================================================

if predict_button:

    customer_data = {

        "gender": gender,

        "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,

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

        with st.spinner("Analyzing customer data... 🤖"):

            response = requests.post(
                "http://127.0.0.1:8000/predict",
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
            # DISPLAY RESULT
            # ==================================================

            st.divider()

            st.header("📊 Prediction Result")


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
            # RISK MESSAGE
            # ==================================================

            if risk == "High":

                st.error(
                    "🚨 HIGH CHURN RISK"
                )

            elif risk == "Medium":

                st.warning(
                    "⚠️ MEDIUM CHURN RISK"
                )

            else:

                st.success(
                    "✅ LOW CHURN RISK"
                )


            # ==================================================
            # RECOMMENDATION
            # ==================================================

            st.subheader("💡 Recommended Action")

            st.info(recommendation)


        else:

            st.error(
                f"API Error: {response.status_code}"
            )


    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the FastAPI server. "
            "Make sure the backend is running."
        )


    except Exception as e:

        st.error(
            f"Unexpected error: {str(e)}"
        )