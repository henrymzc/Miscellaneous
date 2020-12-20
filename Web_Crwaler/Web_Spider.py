

import  time
import requests
import random
from bs4 import  BeautifulSoup

Result=open("1500015413_StatData.txt","w",encoding="gb18030")   #把爬虫结果储存在Result.txt
Basic = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/"  #基本的网页地址
MainPage=requests.get("http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2017/index.html")  #爬取主页
MainPage.encoding='gb2312'  #字体格式为gb2312
MainHtml=MainPage.text
MainBS = BeautifulSoup(MainHtml,"html.parser")
AllTr = MainBS.find_all("tr",{"class":"provincetr"}) #获取所有类型为省份的行
ProvDict={}  #做一个{省份：链接}的字典,方便以后
for Tr in AllTr:            #通过主页得到ProvDict的字典，得到最高级各个省与其链接的pair
    AllProv = Tr.find_all("a")
    for Prov in AllProv:
        ProvName = Prov.get_text()
        ProvLink = Prov.attrs["href"]
        ProvDict[ProvName]=ProvLink


def TownVillage(Page):   #从Town主页爬取每一个Village的信息，page为输入的地址，返回1
    #time.sleep(random.uniform(0.1, 0.15))   #设置随机间隔时间，防止国家统计局反爬，但是有while flag就不用了。
    print(Page)                           #告诉我爬到哪里了
    Flag=True                             #以下程序如果报错，则会进入except，暂停两秒钟之后继续；
    while Flag:
        try:
            TownPage = requests.get(Page)
            Flag=False
        except Exception as error:
            print(error)
            time.sleep(2)
    TownPage.encoding = "gb2312"         #字体设置为gb2312
    TownHtml = TownPage.text
    TownBS = BeautifulSoup(TownHtml, "html.parser")
    AllTr = TownBS.find_all("tr", {"class": "villagetr"})
    for Tr in AllTr:                       #由于基层没有进一步链接，所以通过<td>来获取数据
        AllTd = Tr.find_all("td")
        VillageCode = AllTd[0].string        #Village代码
        print("\t\t\t\t"+VillageCode, file=Result, end="")   #通过四个间隔符输出Village代码，结束不换行
        VillageUrbanCode = AllTd[2].string        #城乡代码
        print(VillageUrbanCode, file=Result, end="")         #输出Village的城乡代码
        VillageName = AllTd[1].string          #Village名字
        print(VillageName, file=Result)                      #输出Village名字
    return 1

def CountyTown(Page):     #从County主页爬取每个Town的信息，返回1
    print(Page)            #告诉我爬到哪里了
    Flag = True  # 以下程序如果报错，则会进入except，暂停两秒钟之后继续；
    while Flag:
        try:
            CountyPage = requests.get(Page)
            Flag = False
        except Exception as error:
            print(error)
            time.sleep(2)
    CountyPage.encoding = "gb2312"
    CountyHtml = CountyPage.text
    CountyBS = BeautifulSoup(CountyHtml, "html.parser")
    AllTr = CountyBS.find_all("tr", {"class": "towntr"})  #获取所有class为towntr的行
    for Tr in AllTr:
        AllTown = Tr.find_all("a")
        if len(AllTown) == 0:  #如果tr没有链接（已经最底层），则找不到超链接（<a></a>，则通过<td>寻找
            AllTd = Tr.find_all("td")      #寻找所有的<td>
            for i, Td in enumerate(AllTd):
                if i == 0:
                    TownCode = Td.string     #获取Town代码
                    print("\t\t\t"+TownCode, file=Result, end="")  #空三个间隔符输出Town代码，结尾不换行
                else:
                    TownName = Td.string
                    print(TownName, file=Result)     #紧接着输出Town的名字
        else:   #如果有超链接
            for i, Town in enumerate(AllTown):
                TownLink = Town.attrs["href"]    #Town的链接地址（尾部分）
                if i == 0:
                    TownCode = Town.get_text()
                    print("\t\t\t"+TownCode, file=Result, end="")  #空三个间隔符输出Town代码，结尾不换行
                else:
                    TownName = Town.get_text()   #Town的名字
                    print(TownName, file=Result)
            TownVillage(Page[:59]+"/"+TownLink)  #这里是取County网址的前60个字符，再加上Townlink，能到达Town的页面，爬取Village的信息
    return 1

def CityCounty(Page):        #从City主页爬取每一个County的信息，返回1
    print(Page)           #告诉我爬到哪了
    Flag = True
    while Flag:          #反爬措施，如上
        try:
            CityPage = requests.get(Page)
            Flag = False
        except Exception as error:
            print(error)
            time.sleep(2)
    CityPage.encoding="gb2312"
    CityHtml = CityPage.text
    CityBS = BeautifulSoup(CityHtml, "html.parser")
    AllTr = CityBS.find_all("tr", {"class": "countytr"})
    CountyDict = {}
    for Tr in AllTr:
        AllCounty = Tr.find_all("a")
        if len(AllCounty) == 0:         #如果没有链接（最底层），则找不到超链接（<a></a>
            AllTd = Tr.find_all("td")
            for i, Td in enumerate(AllTd):
                if i == 0:
                    CountyCode = Td.string
                    print("\t\t"+CountyCode, file=Result,end="")
                else:
                    CountyName=Td.string
                    print(CountyName,file=Result)
        else:                           #如果有超链接，则要获取链接
            for i, County in enumerate(AllCounty):
                CountyLink = County.attrs["href"]     #获取链接地址到CountyLink
                if i == 0:
                    CountyCode = County.get_text()
                    print("\t\t"+CountyCode,file=Result,end="")  #输出County代码，首行两个缩进符，结尾不换行
                else:
                    CountyName = County.get_text()
                    print(CountyName, file=Result)         #输出County名字
                    CountyDict[CountyName] = CountyLink
            CountyTown(Basic+CountyCode[:2]+"/"+CountyLink) #这里是取Basic的网址，再加上Countycode的前两位，能到达County的页面，爬取Town的信息
    return 1

def ProvCity(Page):         #从Prov主页爬取每一个City的信息，Page为输入的地址
    print(Page)          #告诉我爬到哪里了
    Flag=True
    while Flag:          #反爬措施，如上
        try:
            ProvPage = requests.get(Page)
            Flag = False
        except Exception as error:
            print(error)
            time.sleep(2)
    ProvPage.encoding = "gb2312"
    ProvHtml = ProvPage.text
    ProvBS = BeautifulSoup(ProvHtml, "html.parser")
    AllTr = ProvBS.find_all("tr", {"class": "citytr"})
    CityDict = {}
    for Tr in AllTr:
        AllCity = Tr.find_all("a")
        for i, City in enumerate(AllCity):
            CityLink = City.attrs["href"]
            if i == 0:
                CityCode = City.get_text()    #输出城市代码
                print("\t"+CityCode, file=Result,end="")
            else:
                CityName = City.get_text()
                print(CityName, file=Result)   #输出城市名字
                CityDict[CityName] = CityLink  #创建城市字典
        CityCounty(Basic+CityLink)   #这里是取Basic的网址，再加上CityLink，能到达City的页面，爬取County的信息
    return 1

for i, Prov in enumerate(ProvDict):
    print(ProvDict[Prov][:2]+"0000000000"+Prov, file=Result)
    ProvCity(Basic+ProvDict[Prov])

Result.close()
