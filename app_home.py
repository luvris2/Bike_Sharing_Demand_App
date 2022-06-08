import streamlit as st

def run_home() :
    st.write('📝 이 앱은 자전거 대여량을 분석하여 예측 및 차트로 보여주는 앱입니다.')
    st.write('📝 EDA를 눌러보시면 데이터별로 분석된 차트를 확인하실 수 있습니다.')
    st.write('📝 ML은 인공지능이 학습하여 결과를 예측한 값을 확인하실 수 있습니다.')

    st.image('data/bike_img02.png')