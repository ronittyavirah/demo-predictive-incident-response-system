import streamlit as st
import pandas as pd
from sklearn.ensemble import IsolationForest
import json
from datetime import datetime

st.set_page_config(page_title="Cyber Incident Response Demo", layout="wide")

st.title("🛡️ Predictive Human-Verified Cyber Incident Response System")

# -------------------------------
# STEP 1: CREATE SAMPLE LOG DATA
# -------------------------------
data = pd.DataFrame({
    "User": ["Alice", "Bob", "Charlie", "David"],
    "Login_Time": [10, 2, 11, 3],
    "Failed_Attempts": [0, 5, 0, 6],
    "Privilege_Change": [0, 1, 0, 1]
})

st.subheader("📊 System Logs")
st.dataframe(data)

# -------------------------------
# STEP 2: AI THREAT DETECTION
# -------------------------------
model = IsolationForest(contamination=0.25)
model.fit(data[["Failed_Attempts", "Privilege_Change"]])
data["Anomaly"] = model.predict(data[["Failed_Attempts", "Privilege_Change"]])

threats = data[data["Anomaly"] == -1]

# -------------------------------
# STEP 3: RISK SCORING
# -------------------------------
def calculate_risk(row):
    risk = row["Failed_Attempts"] * 10
    if row["Privilege_Change"] == 1:
        risk += 40
    if row["Login_Time"] < 6:
        risk += 20
    return risk

if not threats.empty:
    threat = threats.iloc[0]
    risk_score = calculate_risk(threat)

    st.subheader("🚨 Predicted Threat Detected")

    st.write(f"**User:** {threat['User']}")
    st.write(f"**Risk Score:** {risk_score}")

    explanation = []
    if threat["Failed_Attempts"] > 0:
        explanation.append("Multiple failed login attempts")
    if threat["Privilege_Change"] == 1:
        explanation.append("Privilege escalation attempt")
    if threat["Login_Time"] < 6:
        explanation.append("Unusual login time")

    st.subheader("🧠 Explainable AI Reasoning")
    for reason in explanation:
        st.write("•", reason)

    # -------------------------------
    # STEP 4: HUMAN VERIFICATION
    # -------------------------------
    st.subheader("👨‍💼 Human Verification Required")

    approve = st.button("✅ Approve Containment Action")
    reject = st.button("❌ Reject Action")

    # -------------------------------
    # STEP 5: RESPONSE EXECUTION
    # -------------------------------
    if approve:
        action = f"User {threat['User']} isolated and privileges revoked."
        st.success(action)

        log = {
            "time": str(datetime.now()),
            "user": threat["User"],
            "risk_score": risk_score,
            "decision": "APPROVED",
            "action": action
        }

        with open("audit_log.json", "a") as f:
            json.dump(log, f)
            f.write("\n")

    if reject:
        st.warning("Action rejected by human analyst.")

else:
    st.success("✅ No threats detected")

st.subheader("📁 Audit & Compliance")
st.write("All AI decisions and human approvals are logged.")