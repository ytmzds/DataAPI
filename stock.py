import requests
from bs4 import BeautifulSoup
from stockinfo import stock2code,code2stock



def getstock(code):
    # now = datetime.datetime.now()
    # today = now.strftime('%Y%m%d')

    try:
        if code.isdigit():
            # title = code + code2stock.get(code, ' ')
            url = 'https://tw.stock.yahoo.com/q/q?s=' + code
        else:
            res = stock2code.get(code, '查無該股')
            # title = res + code
            url = 'https://tw.stock.yahoo.com/q/q?s=' + res
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all(text='成交')[0].parent.parent.parent
        name = table.select('tr')[1].select('td')[0].text.rstrip('加到投資組合')
        price = table.select('tr')[1].select('td')[2].text
        price1 = table.select('tr')[1].select('td')[8].text
        price2 = table.select('tr')[1].select('td')[9].text
        price3 = table.select('tr')[1].select('td')[10].text
        return '['+name+']股票資訊如下:\n成交價:'+price+'\n開盤價:'+price1+'\n最高價:'+price2+'\n最低價:'+price3
    except:
        return '股票代碼錯誤或查無此代碼!!'

# print(getstock('1101'))