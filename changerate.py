import pandas


def getmoney(c):
    name = {'美金':'USD','美元':'USD','港幣':'HKD','英鎊':'GBP','澳幣':'AUD','加拿大幣':'CAD','新加坡幣':'SGD',
            '瑞士法郎':'CHF','日圓':'JPY','南非幣':'ZAR','瑞典幣':'SEK','紐元':'NZD','泰幣':'THB',
            '菲國比索':'PHP','印尼幣':'IDR','歐元':'EUR','韓元':'KRW','越南盾':'VND','馬來幣':'MYR','人民幣':'CNY'}

    dfs = pandas.read_html('https://rate.bot.com.tw/xrt?Lang=zh-TW%27%27')
    currency = dfs[0]
    currency = currency.iloc[:, 0:3]
    currency.columns = [u'幣別', u'買入', u'賣出']
    currency[u'幣別'] = currency[u'幣別'].str.extract('((\w+))')
    a=currency.values


    for i in range(19):
        if name.get(c) == a[i][0] :
            return c+'\n買入'+a[i][1]+'\n賣出'+a[i][2]
        else:
            return '查無此外幣'

#print(getmoney('日圆'))
