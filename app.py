import streamlit as st
import pandas as pd
from datetime import datetime

######################
###  페이지  레이아웃  ###
######################

st.set_page_config(
    page_title="국가검진 대상자 조회",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

######################
### SIDE BAR 영역   ###
######################


with st.sidebar :
    st.header('필수입력')
    st.subheader('(필수)태어난 연도를 입력해 주세요')
    born_year = st.text_input('연도', '1992')

    st.header('(필수)성별을 선택해 주세요')
    sex = st.radio('성별',('남', '여'))

    st.write('----')
    st.header('선택입력')
    st.subheader('(선택)건강보험 종류를 선택해 주세요')
    health_insurance = st.radio('건강보험',('직장가입자','지역가입자','의료급여수급권자'), index=None)
    if health_insurance == '직장가입자' :
        work_start = st.text_input('직장가입자라면 입사연도를 입력해 주세요!',value=None)
    st.subheader('(선택)2024년 외에 다른 연도가 궁금하신가요?')
    standard_year = st.slider("연도", 2020, 2030, 2024)

# with st.form("individual_status"):
#     with st.sidebar :
#         st.header('필수입력')
#         st.subheader('(필수)태어난 연도를 입력해 주세요')
#         born_year = st.text_input('연도', '1992')

#         st.header('(필수)성별을 선택해 주세요')
#         sex = st.radio('성별',('남', '여'))

#         st.write('----')
#         st.header('선택입력')
#         st.subheader('(선택)건강보험 종류를 선택해 주세요')
#         health_insurance = st.radio('건강보험',('직장가입자','지역가입자','의료급여수급권자'), index=None)
#         if health_insurance == '직장가입자' :
#             work_start = st.text_input('입사연도','2023')
    
#     submitted = st.form_submit_button("제출하기")

######################
###    함수 선언부    ###
######################
    
## 공통 항목
def exam_common(age, health_insurance) : 
    if age % 2 == 0 :
        return True
    elif health_insurance == '직장가입자' and work_start == str(datetime.today().year-1) :
        return True
    else : return False

## 우울증
def exam_depression(age) :
    if age % 10 == 0 and age // 10 in [x for x in range(3,8)] :
        return True
    else : return False

## 콜레스테롤
def exam_cholesterol(age, sex) :
    if sex == 1 :
        if age % 4 == 0 and age // 4 in [x for x in range(6,20)] :
            return True
        else : return False
    elif sex == 2 :
        if age % 4 == 0 and age // 4 in [x for x in range(10,20)] :
            return True
        else : return False

## B형 간염
def exam_HBV(age) :
    if age == 40 :
        return True
    else : return False

## 골밀도
def exam_BMD(age) :
    if sex == 2 and age in [54,66] :
        return True
    else : return False

## 인지기능장애
def exam_Alzheimer(age) :
    if age in [66+2*x for x in range(0,10)] :
        return True
    else : return False

## 생활습관평가
def exam_habits(age) :
    if age in [40,50,60,70] :
        return True
    else : return False

## 노인신체기능검사
def exam_oldman(age) :
    if age in [66,70,80] :
        return True
    else : return False

## 치면세균막 검사
def exam_mouth(age) :
    if age == 40 :
        return True
    else : return False

## 위암 검사
def exam_ulcer(age) :
    if age in [40+2*x for x in range(0,20)] :
        return True
    else : return False

## 대장암 검사
def exam_colon(age) :
    if age >= 50 :
        return True
    else : return False

## 유방암 검사
def exam_mammo(age, sex) :
    if sex == 2 and age in [40+2*x for x in range(0,20)] :
        return True
    else : return False

## 자궁경부암 검사
def exam_womb(age, sex) :
    if sex == 2 and age in [20+2*x for x in range(0,20)] :
        return True
    else : return False


######################
###    연산 실행부    ###
######################
age = standard_year - int(born_year)
if sex == '남' :
    sex = 1
elif sex == '여' :
    sex = 2

if exam_common(age, health_insurance) is True : 
    st.header(f'당신은 {standard_year}년에 국가검진 대상입니다.')
    st.subheader('아래에서 무슨 검사를 받는지 확인해 보세요!')

    left_side,right_side = st.columns(2)
    exam_basic = ['공통항목','우울증','콜레스테롤','B형간염','골밀도','인지기능장애','생활습관평가','노인신체기능검사','치면세균막검사']
    exam_cancer = ['위암','간암','대장암','유방암','자궁경부암','폐암']
    with left_side :
        st.header('일반검진')
        df = pd.DataFrame(
            index=exam_basic,
            data={'검진 항목':[exam_common(age,health_insurance),
                            exam_depression(age),
                            exam_cholesterol(age,sex),
                            exam_HBV(age),
                            exam_BMD(age),
                            exam_Alzheimer(age),
                            exam_habits(age),
                            exam_oldman(age),
                            exam_mouth(age)]})
        st.write(df)
    with right_side :
        st.header('암검진')
        df = pd.DataFrame(
            index=exam_cancer,
            data={'검진 항목':[exam_ulcer(age),
                            False,
                            exam_colon(age),
                            exam_mammo(age,sex),
                            exam_womb(age,sex),
                            False]})
        st.write(df)
elif exam_common(age, health_insurance) is False : 
    st.header(f'당신은 {standard_year}년에 국가검진 대상이 아닙니다.')
    st.subheader('내년에 국가검진을 받으세요!')

st.error('대충 정확하게 보려면 간편인증을 통해 확인해주겠다는 메시지', icon="🚨")