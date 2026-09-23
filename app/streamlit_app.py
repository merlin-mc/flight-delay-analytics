import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="航班延误预测平台", layout="wide")
st.title("✈️ 航班延误分析与预测平台")
st.markdown("基于五大枢纽机场（PEK, CAN, PVG, SHA, SZX）1126万条运行数据训练")

@st.cache_resource
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'delay_model.pkl')
    return joblib.load(model_path)

try:
    model = load_model()
    st.sidebar.success("✅ 模型加载成功！")
except Exception as e:
    st.sidebar.error(f"❌ 模型加载失败: {e}")
    model = None

st.sidebar.header("📊 输入航班计划信息")
hour = st.sidebar.slider("计划起飞小时 (0-23)", 0, 23, 18)
weekday = st.sidebar.selectbox("星期", options=list(range(7)), 
                              format_func=lambda x: ['周一','周二','周三','周四','周五','周六','周日'][x])
month = st.sidebar.slider("月份", 1, 12, 6)
dep_airport = st.sidebar.selectbox("出发机场", ['PEK', 'CAN', 'PVG', 'SHA', 'SZX'])
arr_airport = st.sidebar.selectbox("到达机场", ['PEK', 'CAN', 'PVG', 'SHA', 'SZX'])

if st.sidebar.button("预测延误概率"):
    if model is not None:
        input_df = pd.DataFrame(0, index=[0], columns=model.feature_names_in_)
        
        input_df['hour'] = hour
        input_df['weekday'] = weekday
        input_df['month'] = month
        input_df['is_weekend'] = 1 if weekday >= 5 else 0
        
        dep_col = f'dep_airport_{dep_airport}'
        arr_col = f'arr_airport_{arr_airport}'
        if dep_col in input_df.columns:
            input_df[dep_col] = 1
        if arr_col in input_df.columns:
            input_df[arr_col] = 1
            
        prob = model.predict_proba(input_df)[0][1]
        
        st.metric(label=f"航班 {dep_airport} → {arr_airport} 的延误概率（>15分钟）", value=f"{prob:.1%}")
        
        if prob > 0.6:
            st.error("⚠️ 高风险：该航班有极高概率延误，建议提前做好预案。")
        elif prob > 0.4:
            st.warning("🟡 中风险：该航班有一定概率延误，请保持关注。")
        else:
            st.success("🟢 低风险：该航班准点概率较高。")
    else:
        st.error("模型未加载，请检查终端是否报错。")