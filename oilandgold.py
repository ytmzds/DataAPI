import ergate
import bs4

OIL_URL = "https://www.cnyes.com/futures/energy3.aspx"
GOLD_URL = "https://www.goldlegend.com/tw/price"


def _updated_function(switch):
    '''mark target function that it will be updated when
    this component be invalid'''

    def _(func):
        def _new(*args, **kwargs):
            if switch:
                print("function %s is a active component" % func.__name__)
            return func(*args, **kwargs)

        return _new

    return _


class _Oil_Record:
    '''a simple data structure to describe oil'''

    _Oil_DataID = [
        "date",
        "name",
        "transaction_location",
        "unit",
        "closing_price",
        "up_and_down",
        "up",
        "yesterday_closing"
    ]

    def __init__(self, **kwargs):
        '''initialize base values'''

        self.date = kwargs.get("date")
        self.name = kwargs.get("name")
        self.transaction_location = kwargs.get("transaction_location")
        self.unit = kwargs.get("unit")
        self.closing_price = kwargs.get("closing_price")
        self.up_and_down = kwargs.get("up_and_down")
        self.up = kwargs.get("up")
        self.yesterday_closing = kwargs.get("yesterday_closing")
        self.initialize()
        # oil record

    def initialize(self):
        ''' handle name error '''

        if self.name: self.name.replace(" ", "")

    def output(self):
        '''show record in console'''

        print("日期{}商品名稱{}分割地{}單位{}收盤價{}漲跌{}漲幅{}昨日收盤價{}".format(
            self.date, self.name, self.transaction_location,
            self.unit, self.closing_price,
            self.up_and_down, self.up, self.yesterday_closing))

    @staticmethod
    def _Oil_IndexToName(index):
        '''translate index to data id name'''

        assert index < len(_Oil_Record._Oil_DataID)
        return _Oil_Record._Oil_DataID[index]


class _Oil_ParseUtils:
    ''' note that this function is a configure utils to
    parse oil datas , it means tools provided by this utils would
    be invalid in the future'''

    @staticmethod
    def _Oil_HandleTr(tr):
        '''parse a tr label to Oil Object'''

        _kwargs, _values = {}, _Oil_ParseUtils._Oil_TrToList(tr)
        for _index in range(len(_values)):
            _kwargs.setdefault(_Oil_Record._Oil_IndexToName(_index), _values[_index])
        return _Oil_Record(**_kwargs)

    @staticmethod
    def _Oil_HandleTable(table):
        '''parse a table label to tr list
        note that , this function will ignore the first tr of a table'''

        return [_tr for _tr in table.find_all("tr")][1:]

    @staticmethod
    def _Oil_HandleHtml(html):
        ''' parse html to datas '''

        _Ret = []
        _soup = bs4.BeautifulSoup(html, "html.parser")
        _table_list = _soup.find_all("table")
        for _table in _table_list:
            for _tr in _Oil_ParseUtils._Oil_HandleTable(_table):
                _Ret.append(_Oil_ParseUtils._Oil_HandleTr(_tr))
        return _Ret

    @staticmethod
    def OilHandleHtml(html, show_error=False):
        '''make sure spider won't break when exception occurred'''

        try:
            return _Oil_ParseUtils._Oil_HandleHtml(html)
        except Exception as e:
            if show_error:
                print(e)
            return []

    @staticmethod
    def _Oil_TrToList(tr):
        ''' split a tr label and save td to a list'''

        return [_td.get_text() for _td in tr]


class _Gold_Record:
    ''' a simple data sturcture to save gold's value '''

    _Gold_DataID = ["buy", "up_and_down1", "sell", "up_and_down2"]

    def __init__(self, **kwargs):
        ''' initialize attributes '''

        self.buy = kwargs["buy"]
        self.up_and_down1 = kwargs["up_and_down1"]
        self.sell = kwargs["sell"]
        self.up_and_down2 = kwargs["up_and_down2"]

    def __output(self):
        ''' return data of current gold'''

        return "買進{}漲跌{}賣出{}漲跌{}".format(self.buy, self.up_and_down1, self.sell, self.up_and_down2)

    def output(self):
        '''output all data of this'''

        print(self.__output())

    def __repr__(self):

        return self.__output()    

    @staticmethod
    def _Gold_IndexToName(index):
        '''translate index to data id name'''

        assert index < len(_Gold_Record._Gold_DataID)
        return _Gold_Record._Gold_DataID[index]


class _Gold_ParseUtils:
    ''' provide tools to parse gold's page , these tools
    may be invalid in the future  '''

    _FLAG_UP = "▲"
    _FLAG_DOWN = "▼"

    @staticmethod
    def _Gold_HandleHtml(html, show_error=False):
        ''' parse html to tr list and find today's data '''

        try:
            _soup = bs4.BeautifulSoup(html, "html.parser")
            _table = _soup.find("table")
            _tr = _table.find_all("tr")[1]
            _kwargs, _values = {}, _Gold_ParseUtils._Gold_TdList(_tr)
            for _index in range(len(_values)):
                _kwargs.setdefault(_Gold_Record._Gold_IndexToName(_index), _values[_index])
            return _Gold_Record(**_kwargs)
        except Exception as e:
            if show_error:
                print(e)
            return None

    @staticmethod
    def _Gold_TdList(tr):
        '''parse tr to td list , this function will ignore
        first td value for some reason '''

        return [_td.get_text() for _td in tr.find_all("td")][1:]


@_updated_function(False)
def GetOilDatas():
    ''' this function should be updated in future'''

    try:
        _html = ergate.download_page(OIL_URL, show_error=True)
        if _html:
            return _Oil_ParseUtils.OilHandleHtml(_html)
        return []
    except Exception as e:
        return []


@_updated_function(True)
def ShowOilData(name):
    for _data in GetOilDatas():
        if name in _data.name:
            print("收盤價{}漲跌{}漲幅{}昨日收盤價{}".format(_data.closing_price, _data.up_and_down, _data.up, _data.yesterday_closing))


@_updated_function(True)
def GetGoldData(show_error=True):
    try:
        _html = ergate.download_page(GOLD_URL, show_error=True)
        if _html:
            _data = _Gold_ParseUtils._Gold_HandleHtml(_html)
            if _data:
                return "{}{}".format(str(_data),"\n")
            else:
                return "error occurred when parsing datas"
        else:
            return "error occurred when visit {}".format(GOLD_URL)
    except Exception as e:
        if show_error:
            print(e)


#ShowGoldData()
#ShowOilData("西德州中級(WTI)原油")
