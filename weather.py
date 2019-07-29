import requests
from bs4 import BeautifulSoup


def getWeather(cityy):
    try:
        city=cityy.split('天')[0];
        site = {'台北': 'Taipei', 'Taipei': 'Taipei', '新北': 'New_Taipei', 'New Taipei': 'New_Taipei', '桃園': 'Taoyuan',
            'Taoyuan': 'Taoyuan', '台中': 'Taichung', 'Taichung': 'Taichung',
            '台南': 'Tainan', 'Tainan': 'Tainan', '高雄': 'Kaohsiung', 'Kaohsiung': 'Kaohsiung', '基隆': 'Keelung',
            'Keelung': 'Keelung', '嘉義': 'Chiayi', 'Chiayi': 'Chiayi',
            '新竹': 'Hsinchu', 'Hsinchu': 'Hsinchu', '苗栗': 'Miaoli', 'Miaoli': 'Miaoli', '彰化': 'Changhua',
            'Changhua': 'Changhua', '南投': 'Nantou', 'Nantou': 'Nantou',
            '雲林': 'Yunlin', 'Yunlin': 'Yunlin', '屏東': 'Pingtung', 'Pingtung': 'Pingtung', '宜蘭': 'Yilan',
            'Yilan': 'Yilan', '花蓮': 'Hualien', 'Hualien': 'Hualien',
            '台東': 'Taitung', 'Taitung': 'Taitung', '澎湖': 'Penghu', 'Penghu': 'Penghu'}

        if city == '台北' or city == '新北' or city == '桃園' or city == '台中' or city == '台南' or city == '高雄' or city == '基隆':
            r = requests.get("https://www.cwb.gov.tw/V7/forecast/taiwan/" + site[city] + "_City.htm")
        else:
         r = requests.get("https://www.cwb.gov.tw/V7/forecast/taiwan/" + site[city] + "_County.htm")

        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, 'html.parser')
        tables = soup.find_all('table')
        tr = tables[0].find_all('tr')
        td = tr[1].find_all('td')

        temperature = td[0].text.strip()
        weather = td[2].text.strip()

        return '氣溫:' + temperature + '°C' + '\n' + weather
    except:
        return '請輸入欲查詢的城市 ( 例如 : 台北天氣 ) !'

#print(getWeather('台東天气'))