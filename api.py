#import sys
#import io
import requests
import datetime

# 출력 인코딩 설정
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_weather(city_name, nx,ny, service_key):
    # 오늘 날짜
    today = datetime.datetime.now().strftime("%Y%m%d")

    # API 기본 설정
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
   
    
    params = {
        "serviceKey": service_key,
        "dataType": "JSON",
        "numOfRows": "1000",
        "pageNo": "1",
        "base_date": today,
        "base_time": "0200",
        "nx": nx,
        "ny": ny
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return f"{city_name}: API 호출 실패 ({response.status_code})"
    
    items = response.json().get('response', {}).get('body', {}).get('items', {}).get('item', [])
    tmx, tmn, pop_list = None, None, [] #최고기온, 최저기온, 강수확률

    for item in items:
        if item['fcstDate'] == today: #오늘인 것만 필터링
            category = item['category']
            value = item['fcstValue']
            if category == 'TMX':
                tmx = value
            elif category == 'TMN':
                tmn = value
            elif category == 'POP':
                pop_list.append(int(value))

    pop = max(pop_list) if pop_list else "정보 없음"

    return f"{city_name}\n  🔺 최고기온: {tmx}℃\n  🔻 최저기온: {tmn}℃\n  ☔ 강수확률: {pop}%\n"

#api
service_key = "m6FlcbXyrynk8Axd0eNhqM4oiDd7KUb/298qAdj6ySlwJQT8PSjr6wR5H/+rctwcEIIItfyH0tlH2mOEGlZF5g=="

cities = [
    ("서울", 60, 127),
    ("부산", 98, 76),
    ("대구", 89, 90),
    ("인천", 55, 124),
    ("광주", 58, 74),
    ("대전", 67, 100),
    ("울산", 102, 84),
    ("세종", 66, 103),
    ("경기도", 60, 120),
    ("강원도", 73, 134),
    ("충북", 69, 107),
    ("충남", 68, 100),
    ("전북", 64, 89),
    ("전남", 51, 67),
    ("경북", 87, 106),
    ("경남", 91, 77),
    ("제주", 52, 38)
]
    
for city_name, nx, ny in cities:
    result = get_weather(city_name, nx, ny, service_key)
    print(result)






