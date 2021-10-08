#!/usr/bin/python3
# This code comes from https://m.blog.naver.com/PostView.naver?blogId=emperonics&logNo=222247749109&proxyReferer=https:%2F%2Fwww.google.com%2F
# This is for my education only.
# The code is modified per my environment.

import requests                                      # http 요청용 모듈
import glob, os                                      # 파일 리스트 확인, 경로 지정 등에 필요한 모듈
import datetime as dt                                # 날짜, 시간용 모듈
import json                                          # json 파일 변환용 모듈
import xmltodict                                     # xml 파일 변환용 모듈
from bs4 import BeautifulSoup                        # html파싱용 모듈
from fake_useragent import UserAgent                 # 봇으로 인식할 때 사용하는 모듈
from inky import InkyPHAT                            # e-ink 디스플레이용 모듈
from PIL import Image, ImageFont, ImageDraw, ImageColor   # 이미지 처리용 모듈
from fonts.ttf import Intuitive                           # 사용 폰트용 모듈(Intuitive)
 
def get_stock():                                           #  주식 정보 파싱용 함수
    URL = 'https://finance.naver.com/item/sise_day.nhn?code=005930'  #네이버 파이낸스 삼성전자 주식 현황 주소
    ua = UserAgent()                                                  # 봇으로 인식하지 않도록 설정
    headers = {
            'User-Agent':ua.random, 
            }
    stock = {}                                                        #주가 정보 저장용 딕셔너리 생성
    response = requests.get(URL, headers = headers)                   # URL주소로 get요청
    if response.status_code == 200:                                   # 상태코드가 200(정상) 이면
        html = response.text                                           # html 파일 저장
        soup = BeautifulSoup(html, 'html.parser')                       # html파서로 파일 변환
        stock['price'] = soup.find('span',{'class':"p11"}).text         # class명이 p11인 첫번째 span 요소를 추출 해서 stock에 저장
        stock['up_down']= soup.select_one('img').get('alt')            # 경로가 img인 첫번째 요소를 추출해서 stock에 저장
        if stock['up_down']=="하락":                                    # 등락 정보가 하락이면 
            stock['up_down_price']= soup.find('span',{'class':"nv01"}).text     # 하락 금액 추출해서 stock에 저장
        elif stock['up_down']== "상승":                                  # 등락 정보가 상승이면 
            stock['up_down_price'] = soup.find('span',{'class':"red02"}).text  # 상승 금액 추출해서 stock에 저장
        return stock                                                          # stock 정보 반환
    else:                                       # http요청에 에러가 있으면
        return stock                            # 비어있는 stock 요소 반환


def get_weather():                                            # 날씨 정보 파싱용 함수
    API_KEY="API키"                                 # openweathermap에서 발급받은 API키 입력
    API_ADDRESS="http://api.openweathermap.org/data/2.5/weather?q=Sejong&appid={}".format(API_KEY) #API주소
    weather = {}                                  # 날씨 정보 저장용 dict생성
    response = requests.get(API_ADDRESS)          # 날씨 API에 정보 요청
    if response.status_code==200:                  # 상태코드가 200(정상) 이면
        weather_json = json.loads(response.text)   # weather정보를 불러옴
        weather['weather']=weather_json['weather'][0]['main']  #weather_json 정보에서 메임 날씨 정보를 추출해서 weather에 저장
        weather['temp']=weather_json['main']['temp']-273.15   #weather_json 정보에서 현재온도를 추출해서 weather에 저장
        print(weather) 
        return weather                                        # 날씨 정보 반환
    else:                                # http요청에 에러가 있으면
        return weather                   # 비어있는 weather 요소 반환


#def get_dust():                          # 미세먼지 정보 파싱용 함수
#    API_KEY = "API키"                    # data포털에서 발급받은 API키 입력
#    API_ADDRESS="http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst?sidoName=%EC%84%B8%EC%A2%85&searchCondition=DAILY&pageNo=1&numOfRows=1&ServiceKey={}".format(API_KEY)
#    response = requests.get(API_ADDRESS)     # 미세먼지 API에 http요청 
#    if response.status_code == 200:         # 상태코드가 200(정상)이면
#        dust_data = xmltodict.parse(response.text)      #미세먼지 정보 저장
#        dust=dust_data['response']['body']['items']['item']['pm10Value']  # 미세먼지 정보에서 pm10에 해당하는 미세먼지 추출
#        print(dust) 
#        return int(dust)                        # 미세먼지 수치 반환
#    else:                                        # 요청에 에러가 있으면
#        dust=None
#        return dust                          # 비어있는 미세먼지 수치 반환


PATH = os.path.dirname(__file__)             # 현재 파일의 경로 지정용 변수

inky_display = InkyPHAT("black")                    # inkydisplay 객체 생성
inky_display.set_border(inky_display.BLACK)       # 디스플레이의 경계를 검정색으로 설정

bg_img = Image.open(os.path.join(PATH,'images/template.png'))     # 배경이미지 불러오기
draw = ImageDraw.Draw(bg_img)                                     # draw에 배경이미지 그리기

stock_font = ImageFont.truetype(Intuitive, 18)                      # 사용할 폰트 불러오기
stock_font2 = ImageFont.truetype(os.path.join(PATH,"font/NanumPen.ttf"), 18)
date_font = ImageFont.truetype(os.path.join(PATH,"font/NanumPen.ttf"), 20)
weather_font = ImageFont.truetype(Intuitive, 20)
weather_font2 = ImageFont.truetype(os.path.join(PATH, "font/NanumPen.ttf"), 20)

dust_font = ImageFont.truetype(os.path.join(PATH, "font/NanumPen.ttf"), 30)
dust_font2 = ImageFont.truetype(os.path.join(PATH, "font/NanumPen.ttf"), 20)

up_image = Image.open(os.path.join(PATH, 'images/up.png'))        # 주식 상승시 표시할 화살표 이미지
down_image = Image.open(os.path.join(PATH, 'images/down.png'))    # 주식 하락시 표시할 화살표 이미지

weather_map={                                         #openweathermap에서 불러온 main 날씨에 따른 이미지 대응표
        'storm':['Thunderstorm'],   
        'rain':['Rain', 'Drizzle'],                  # main 날씨가 'Rain' 또는 'Drizzle'이면 rain 아이콘 보여줌
        'snow':['Snow'],
        'atmosphere':[],
        'sun':['Clear'],
        'cloud':['Clouds'] 
        }

weather_icon = None                                 # 표시할 날씨 아이콘 변수 생성
icons ={}                                          # 날씨 이미지 아이콘 저장용 변수

samsung = get_stock()                                 # 삼성의 주식정보 얻어오기
weather = get_weather()                              # 현재 날씨 정보 얻어오기
#dust = get_dust()                                  # 현재 미세먼지 정보 얻어오기
 
if samsung:                                         # 삼성 주식정보가 값이 들어 있으면  
    draw.text((10,40), samsung['price'], inky_display.BLACK, stock_font)   # draw에 삼성의 현재 주가 그리기

    if samsung['up_down'] == "하락":                           # 삼성 주식정보에서 얻은 주가가 하락 이면
        bg_img.paste(down_image, (10, 65))                    # 아래쪽 화살표 표시
    else:                                                      # 주가가 상승이면
        bg_img.paste(up_image, (10, 65))                     # 위쪽 화살표 표시
    draw.text((8, 35),samsung['up_down_price'], inky_display.RED, stock_font2) # draw 객체에 상승 및 하락 가격 표시
else:
    pirnt("Warning, no Stock information found!")           # 삼성 주식 정보가 없으면 경고 문구 터미널에 표시


if weather:                                           # 날씨 정보 값이 있으면 
    draw.text((95,70), str(weather['temp'])+"C", inky_display.RED, weather_font2) # draw객체에 현재 온도 표시
    for main_weather in weather_map:                               # 현재 날씨가 해당하는 아이콘이 이미지 대응표에 있으면 
        if weather['weather'] in weather_map[main_weather]:        # 날씨 아이콘 변수를 해당 날씨로 설정
            weather_icon = main_weather                             # 날씨 아이콘 변수를 해당 날씨로 설정
            break; 
else:
    print("Warning, no weather information found!")                # 날씨 정보 값이 없으면 경고문구 터미널에 표시


for icon in glob.glob(os.path.join(PATH, 'images/icon-*.png')):    #'image'폴더에서 'icon'으로 시작하는 모든 파일을 찾아서
    icon_name = icon.split("icon-")[1].replace(".png","")         # .png 확장자 제거후 파일이름에서 'icon-'부분 제거
    icon_image = Image.open(icon)                                 # 전체 닐씨 아이콘 이미지를 불러와서
    icons[icon_name]=icon_image                                   # icons에 해당 날씨이미지 저장. 예시: icons['rain']="icon-rain.png"


if weather_icon is not None:                                      # 표시할 날씨 아이콘 변수에 날씨가 설정되어 있으면
    bg_img.paste(icons[weather_icon], (90, 45))                   # icons에서 표시할 날씨의 아이콘 이미지를 불러와서 bg_image에 그려줌.
else:                                                             # 표시할 날씨 아아콘 변수가 없으면
    draw.text((90, 45), "?", inky_display.RED, font=weather_font)   # 물음표 표시




dt = dt.datetime.now()                                           # datetime객체에서 현재 datetime정보를 불러옴
dt_msg = dt.strftime("%m월%d일 %H:%M")                            # 날짜 및 시간를 표시해줄 형식 지정
draw.text((100, 3),dt_msg, inky_display.BLACK, date_font)         # draw객체에 날짜 및 현재 시간 표시


#if dust:                                                          # 미세먼지 정보가 있으면 
#    if dust <= 30:                                               # 미세먼지 수치에 따라 '좋음', '보통', '나쁨', '매우나쁨'과 미세먼지 수치를 draw객체에 표시
#        draw.text((165, 40), "좋음", inky_display.BLACK, dust_font) 
#        draw.text((170, 70), str(dust), inky_display.RED, dust_font2) 
#    elif dust > 30 and dust <=80:
#        draw.text((165, 40), "보통", inky_display.BLACK, dust_font) 
#        draw.text((170, 70), str(dust), inky_display.RED, dust_font2) 
#    elif dust > 80 and dust <=150:
#        draw.text((165, 40), "나쁨", inky_display.BLACK, dust_font) 
#        draw.text((170, 70), str(dust), inky_display.RED, dust_font2) 
#    elif dust > 150:   
#
#        draw.text((165, 40), "매우나쁨", inky_display.BLACK, dust_font) 
#        draw.text((170, 70), str(dust), inky_display.RED, dust_font2) 
#else:                                                         # 미세먼지 정보가 없으면 
#    pirnt("Warning, no Dust information found!")              # 터미널창에 경고 문구 표시                                                        


flipped = bg_img.rotate(180)                                #케이스의 전원부를 위쪽에서 꽂기 위해서 화면을 180도 전환했음.

inky_display.set_image(flipped)                            # e-display에 이미지 지정
inky_display.show()                                         # 이미지 표시 
