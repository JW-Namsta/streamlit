import streamlit as st

st.set_page_config(
    page_title="인생체중 테스트 페이지",
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

st.sidebar.header('건강 vs 미용')
health_weight = st.sidebar.slider('건강과 미용 중 어디를 중시하나요? ', 1, 99)

st.sidebar.header('나이, 성별')
age_group = st.sidebar.selectbox('연령대가 어떻게 되세요?',(20,30,40,50,60,70))

sex = st.sidebar.radio("성별을 선택해주세요.",('남', '녀'))

if sex == '남' :
    sex = 1
else :
    sex = 2

st.sidebar.header('키, 체중, 허리둘레')
height = st.sidebar.number_input('키 입력(cm)', min_value=100.0, max_value=200.0, value=170.0, step=0.1)
weight = st.sidebar.number_input('체중 입력(kg)', min_value=30.0, max_value=200.0, value=60.0, step=0.1)
wc = st.sidebar.number_input('허리둘레 입력(inch)', min_value=10.0, max_value=100.0, value=32.0, step=0.1)*2.54

st.sidebar.header('자존감')
esteem_val = st.sidebar.select_slider('당신의 자존감은 어느정도이신가요?', options=['매우양호','양호','나쁨','매우나쁨'])

st.sidebar.header('컨디션')
condition_val = st.sidebar.select_slider('당신의 컨디션은 어느정도이신가요?', options=['매우양호','양호','나쁨','매우나쁨'])

st.sidebar.header('질환')
disease = st.sidebar.checkbox('기저질환 여부')
health_check = st.sidebar.checkbox('검진결과 상 문제가 있나요?')
forecasting = st.sidebar.number_input('질병예보 결과입력', min_value=0.0, max_value=5.0, value=1.0, step=0.1)


######################
### input값 확인 영역 ###
######################
st.write('나는 건강이 "{}" 미용이 "{}"만큼 중요하다.'.format(health_weight, 100-health_weight))
st.write('연령 : {}대로 선택하셨습니다.'.format(age_group))
st.write('성별 : {} 선택하셨습니다.'.format(sex))

st.write('키 : {:.2f}cm'.format(height))
st.write('체중 : {:.2f}kg'.format(weight))
st.write('허리둘레 : {:.2f}cm'.format(wc))

st.write('자존감상태 : {}'.format(esteem_val))

st.write('컨디션상태 : {}'.format(condition_val))

st.write('기저질환 유무 : {}'.format(disease))
st.write('건강검진 결과 : {}'.format(health_check))
st.write('질병예보 결과 : {:.2f}배'.format(forecasting))

######################
###    함수 선언부    ###
######################
    
def cal_bmi(height:float, weight:float) : # BMI 계산
    return round(weight/(height/100)**2,1)

def cal_whtr(height:float, waist:float) : # WHtR 계산
    return round(waist/height,2)

def group_user(BMI, WHtR) : # 유저 유형구분
    if BMI > 22.9 and WHtR > 0.49 :
        return 1
    elif BMI > 22.9 and WHtR <= 0.49 and WHtR >= 0.4 :
        return 4
    elif BMI > 22.9 and WHtR < 0.4 :
        return 7
    elif BMI <= 22.9 and BMI>=18.5 and WHtR > 0.49 :
        return 2
    elif BMI <= 22.9 and BMI>=18.5 and WHtR <= 0.49 and WHtR >= 0.4 :
        return 5
    elif BMI <= 22.9 and BMI>=18.5 and WHtR < 0.4 :
        return 8
    elif BMI < 18.5 and WHtR > 0.49 :
        return 3
    elif BMI < 18.5 and WHtR <= 0.49 and WHtR >= 0.4 :
        return 6
    elif BMI < 18.5 and WHtR < 0.4 :
        return 9
    
def group_user_group(user_group) : # 유형군 구분
    if user_group in [1,2,3,5,6,9] :
        return 'BMI'
    elif user_group in [4,7,8] :
        return 'WHtR'
    

# 기초 미용체중
def cal_beauty_weight(user_group_group, weight, height, wc, sex) :
    if user_group_group == 'BMI' and sex == 1 :
        return 18.5*(height/100)**2
    elif user_group_group == 'BMI' and sex == 2 :
        return 17.5*(height/100)**2
    elif user_group_group == 'WHtR' :
        diff = 0.38*height - wc
        r = 2.3/2.54
        return weight + r * diff
    
# 기초 건강체중
def cal_health_weight(user_group_group, weight, height, wc, sex, age_group) :
    c_bmi = (height/100)**2
    if user_group_group == 'BMI' and sex == 1 :
        adquate_bmi = {20:21,30:22,40:23,50:24,60:25,70:25}
        return adquate_bmi[age_group]*c_bmi
    elif user_group_group == 'BMI' and sex == 2 :
        adquate_bmi = {20:20,30:21,40:22,50:23,60:24,70:24}
        return adquate_bmi[age_group]*c_bmi
    elif user_group_group == 'WHtR' and sex == 1 :
        adquate_whtr = {20:0.43,30:0.43,40:0.44,50:0.44,60:0.45,70:0.45}
        return weight + (adquate_whtr[age_group]*height-wc)*(2.3/2.54)
    elif user_group_group == 'WHtR' and sex == 2 :
        adquate_whtr = {20:0.42,30:0.42,40:0.43,50:0.43,60:0.44,70:0.44}
        return weight + (adquate_whtr[age_group]*height-wc)*(2.3/2.54)

# 자존감
def esteem(esteem, weight, weight_b) :
    if weight >= weight_b :
        if esteem==3 :
            return weight_b + 0.75 * (weight-weight_b)
        elif esteem==2 :
            return weight_b + 0.5 * (weight-weight_b)
        elif esteem in [0,1] :
            return weight_b
    if weight < weight_b :
        return weight_b
    
def medical(weight_h, disease, health_check, forecasting) :
    if disease is True :
        return weight_h * 0.925
    if disease is False :
        if health_check is False and forecasting <= 2.5 :
            return weight_h
        else :
            return weight_h * 0.925

def condition(condition_val, weight, weight_b, weight_h) :
    if condition_val in [0,1] :
        return weight_h
    r = condition_val/4
    if weight_b < weight_h :
        if weight <= weight_b :
            return weight_h - (weight_h-weight_b)*r
        elif weight > weight_b :
            return weight_h + (weight-weight_h)*r
    elif weight_b > weight_h :
        if weight > weight_b :
            return weight_h + (weight_b-weight_h)*r
        elif weight <= weight_b :
            return weight_h + (weight-weight_h)*r
        elif weight <= weight_h :
            return weight_h + (weight_h-weight)*r
    elif weight_b == weight_h :
        if weight == weight_b :
            return weight_h
        else :
            return weight_h + (weight-weight_h)*r


######################
###    연산 실행부    ###
######################
st.write('---')
st.header('결과부')
# 변수명
# health_weight : 건강 가치관
# age_group : 연령대
# sex : 성별
# height : 키
# weight : 체중
# wc : 허리둘레
# esteem : 자존감 점수
# condition : 컨디션 점수
# disease : 기저질환 유무
# health_check : 건강검진 위험
# forcasting : 질병예보

# 적정체중 : BMI = 21인 체중
proper_weight = 21 * (height/100)**2

# 유형 구분
user_bmi = cal_bmi(height, weight)
user_whtr = cal_whtr(height, wc)
user_group = group_user(user_bmi, user_whtr)
user_group_group = group_user_group(user_group)

questionnaire_mapper = {'매우양호':3,'양호':2,'나쁨':1,'매우나쁨':0}
# 미용체중 계산
weight_b = cal_beauty_weight(user_group_group, weight, height, wc, sex)
weight_b = esteem(questionnaire_mapper[esteem_val], weight, weight_b)

# 건강체중 계산
weight_h = cal_health_weight(user_group_group, weight, height, wc, sex, age_group)
weight_h = condition(questionnaire_mapper[condition_val], weight, weight_b, weight_h)
weight_h = medical(weight_h, disease, health_check, forecasting)

st.write('미용체중 : {:.1f}'.format(weight_b))
st.write('건강체중 : {:.1f}'.format(weight_h))
ideal_weight = (weight_b*(100-health_weight) + weight_h*health_weight)/100
st.write('인생체중 : {:.1f}'.format(ideal_weight))