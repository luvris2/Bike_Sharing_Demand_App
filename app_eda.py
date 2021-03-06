import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 각 운영체제에 따른 한글 출력
# 리눅스의 경우 해당 글꼴이 설치되어있어야 합니다.
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = 'c:/windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
elif platform.system() == 'Linux':
    rc('font', family='NanumGothic')
else:
    print('Unknown system... sorry~~~~')

# csv 파일 호출
train = pd.read_csv('data/train.csv', parse_dates=['datetime'])

# 피쳐 엔지니어링
train['year'] = train['datetime'].dt.year
train['month'] = train['datetime'].dt.month
train['day'] = train['datetime'].dt.day
train['hour'] = train['datetime'].dt.hour
train["dayofweek"] = train["datetime"].dt.dayofweek
def concatenate_year_month(datetime):
    return "{0}-{1}".format(datetime.year, datetime.month)
train["year_month"] = train["datetime"].apply(concatenate_year_month)

# add_eda.py 파일 호출시 가장 먼저 실행 될 함수 run_eda
def run_eda() :
    global train

    st.subheader('데이터 분석')


    if st.button('데이터 보기') :
        st.write(train.loc[ : , :'count' ])


    with st.expander('데이터프레임 컬럼 상세 설명') :
        st.subheader('데이터프레임 컬럼 상세 설명')
        st.text('datetime : 날짜와 시간')
        st.text('season : 계절 (1:봄, 2:여름, 3:가을, 4:겨울)')
        st.text('holiday : 공휴일 여부 (0:평일, 1:공휴일)')
        st.text('workingday : 평일 여부 (0:휴일, 1:평일)')
        st.text('weather : 날씨 (1:맑음, 2:흐림, 3:이슬비, 4:호우)')
        st.text('temp : 온도')
        st.text('atemp : 체감온도')
        st.text('humidity : 습도')
        st.text('windspeed : 풍속')
        st.text('casual : 미등록 회원 대여 횟수')
        st.text('registered : 등록 회원 대여 횟수')
        st.text('count : 총 대여 횟수')

    # 원하는 데이터를 선택하여 화면에 차트로 출력
    st.subheader('차트 분석')
    chart_list = ['날짜/시간별 대여량', '휴일/평일별 대여량', '시간대별 대여량 심화 분석', '날씨/계절별 대여량', '온도별 대여량', '상관계수']
    selected = st.selectbox('보고싶은 분석 차트를 선택해주세요.', chart_list)
    if selected == chart_list[0] :
        st.text('')
        st.subheader('날짜/시간별 대여량 분석')
        figure, (ax1,ax2) = plt.subplots(nrows=1, ncols=2)
        figure.set_size_inches(15,5)
        sns.barplot(data=train, x='year' , y= 'count' , ax=ax1)
        sns.barplot(data=train, x='month' , y= 'count' , ax=ax2)
        ax1.set_title("연도별 대여량", fontsize=30)
        ax1.set_xlabel("연도", fontsize=20)
        ax1.set_ylabel("대여량", fontsize=20)
        ax2.set_title("월별 대여량", fontsize=30)
        ax2.set_xlabel("월", fontsize=20)
        ax2.set_ylabel("대여량", fontsize=20)   
        st.pyplot(figure)
    
        figure, (ax3,ax4) = plt.subplots(nrows=1, ncols=2)
        figure.set_size_inches(15,5)
        sns.barplot(data=train, x='day' , y= 'count' , ax=ax3)
        sns.barplot(data=train, x='hour' , y= 'count' , ax=ax4)
        ax3.set_title("일별 대여량", fontsize=30)
        ax3.set_xlabel("일", fontsize=20)
        ax3.set_ylabel("대여량", fontsize=20)
        ax4.set_title("시간별 대여량", fontsize=30)
        ax4.set_xlabel("시간", fontsize=20)
        ax4.set_ylabel("대여량", fontsize=20)
        st.pyplot(figure)    

        fig, ax5 = plt.subplots(nrows=1, ncols=1)
        fig.set_size_inches(18, 4)
        sns.barplot(data=train, x="year_month", y="count", ax=ax5)
        ax5.set_title("연도/월별 대여량", fontsize=40)
        ax5.set_xlabel("연도-월", fontsize=25)
        ax5.set_ylabel("대여량", fontsize=25)
        st.pyplot(fig)

    elif selected == chart_list[1] :
        st.text('')
        st.subheader('계절별, 휴일/평일별 대여량 분석')
        fig, axes = plt.subplots(ncols=2)
        fig.set_size_inches(10, 5)
        sns.boxplot(data=train,y="count",x="season",orient="v",ax=axes[0])
        sns.boxplot(data=train,y="count",x="workingday",orient="v",ax=axes[1])

        axes[0].set_title('계절별 대여량', fontsize=25)
        axes[0].set_xlabel('계절(1:봄, 2:여름, 3:가을, 4:겨울)', fontsize=15)
        axes[0].set_ylabel('대여량', fontsize=15)
        axes[1].set_title('휴일/평일별 대여량', fontsize=25)
        axes[1].set_xlabel('휴일/평일(0:휴일, 1:평일', fontsize=15)
        axes[1].set_ylabel('대여량', fontsize=15)
        st.pyplot(fig)

    elif selected == chart_list[2] :
        st.text('')
        st.subheader('시간별 대여량 심화 분석')
        fig,ax1 = plt.subplots(nrows=1)
        fig.set_size_inches(10, 3)
        sns.pointplot(data=train, x="hour", y="count", ax=ax1)
        ax1.set_title("시간별 대여량", fontsize=25)
        ax1.set_xlabel("시간", fontsize=15)
        ax1.set_ylabel("대여량", fontsize=15)
        st.pyplot(fig)
        fig,ax2 = plt.subplots(nrows=1)
        fig.set_size_inches(10, 3)
        sns.pointplot(data=train, x="hour", y="count", hue="workingday", ax=ax2)
        ax2.set_title("휴일/평일에 따른 시간별 대여량", fontsize=25)
        ax2.set_xlabel("휴일/평일(0:휴일, 1:평일)", fontsize=15)
        ax2.set_ylabel("대여량", fontsize=15)
        st.pyplot(fig)
        fig,ax3 = plt.subplots(nrows=1)
        fig.set_size_inches(10, 3)
        sns.pointplot(data=train, x="hour", y="count", hue="dayofweek", ax=ax3)
        ax3.set_title("요일에 따른 시간별대여량", fontsize=25)
        ax3.set_xlabel("요일(0:월, 1:화, 2:수, 3:목, 4:금, 5:토, 6:일)", fontsize=15)
        ax3.set_ylabel("대여량", fontsize=15)
        st.pyplot(fig)

    elif selected == chart_list[3] :
        fig,ax4 = plt.subplots(nrows=1)
        fig.set_size_inches(10, 3)
        sns.pointplot(data=train, x="hour", y="count", hue="weather", ax=ax4)
        ax4.set_title("날씨에 따른 시간별 대여량", fontsize=25)
        ax4.set_xlabel("날씨(1:맑음, 2:흐림, 3:이슬비, 4:호우))", fontsize=15)
        ax4.set_ylabel("대여량", fontsize=15)
        st.pyplot(fig)
        fig,ax5 = plt.subplots(nrows=1)
        fig.set_size_inches(10, 3)
        sns.pointplot(data=train, x="hour", y="count", hue="season", ax=ax5)
        ax5.set_title("계절에 따른 시간별 대여량", fontsize=25)
        ax5.set_xlabel("계절(1:봄, 2:여름, 3:가을, 4:겨울)", fontsize=15)
        ax5.set_ylabel("대여량", fontsize=15)
        st.pyplot(fig)

    elif selected == chart_list[4] :
        train_temp_count = pd.DataFrame()
        train_temp_count['count'] = train['count']
        train_temp_count['0-5'] = train[ 'count' ].loc [ (train['temp'] > 0) & (train['temp'] <=5) ]
        train_temp_count['6-10'] = train[ 'count' ].loc [ (train['temp'] > 6) & (train['temp'] <=10) ]
        train_temp_count['11-15'] = train[ 'count' ].loc [ (train['temp'] > 11) & (train['temp'] <=15) ]
        train_temp_count['16-20'] = train[ 'count' ].loc [ (train['temp'] > 16) & (train['temp'] <=20) ]
        train_temp_count['21-25'] = train[ 'count' ].loc [ (train['temp'] > 21) & (train['temp'] <=25) ]
        train_temp_count['26-30'] = train[ 'count' ].loc [ (train['temp'] > 26) & (train['temp'] <=30) ]
        train_temp_count['31-35'] = train[ 'count' ].loc [ (train['temp'] > 31) & (train['temp'] <=35) ]
        train_temp_count['36-40'] = train[ 'count' ].loc [ (train['temp'] > 36) & (train['temp'] <=40) ]
        train_temp_count['41-'] = train[ 'count' ].loc [ train['temp'] > 40 ]

        fig,ax6 = plt.subplots(nrows=1)
        fig.set_size_inches(10, 3)
        sns.pointplot(data=train_temp_count.iloc[:,1:], ax=ax6)
        st.text('')
        st.subheader('온도별 대여량 분석')
        ax6.set_title("온도에 따른 대여량", fontsize=25)
        ax6.set_xlabel("온도", fontsize=15)
        ax6.set_ylabel("대여량", fontsize=15)
        st.pyplot(fig)

    elif selected == chart_list[5] :
        st.text('')
        st.subheader('상관계수 표현')
        corrMatt = train[["temp", "atemp", "casual", "registered", "humidity", "windspeed", "count"]]
        corrMatt = corrMatt.corr()
        st.text(corrMatt)

        mask = np.array(corrMatt)
        mask[np.tril_indices_from(mask)] = False

        fig, ax = plt.subplots()
        fig.set_size_inches(20,10)
        sns.heatmap(corrMatt, mask=mask,vmax=.8, square=True,annot=True)
        st.pyplot(fig)

        fig,(ax1,ax2,ax3) = plt.subplots(ncols=3)
        fig.set_size_inches(12, 5)
        sns.regplot(x="temp", y="count", data=train,ax=ax1)
        sns.regplot(x="windspeed", y="count", data=train,ax=ax2)
        sns.regplot(x="humidity", y="count", data=train,ax=ax3)