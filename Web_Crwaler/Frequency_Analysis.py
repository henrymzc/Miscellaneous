Result2=open("1500015413_ComputingData.txt","w",encoding="gb18030")
with open("1500015413_StatData.txt","r",encoding="gb18030") as r:
    RawData=r.read()
DataList = RawData.splitlines()
CategDict={"111": 0, "112": 0, "121": 0, "122": 0, "123": 0, "210": 0, "220": 0}  #首先创立一个这7类基层统计单位的字典
for OneRow in DataList: #如果每一行最后三位相符，则字典加1
    if OneRow[-3:] == "111":
        CategDict["111"] += 1
    elif OneRow[-3:] == "112":
        CategDict["112"] += 1
    elif OneRow[-3:] == "121":
        CategDict["121"] += 1
    elif OneRow[-3:] == "122":
        CategDict["122"] += 1
    elif OneRow[-3:] == "123":
        CategDict["123"] += 1
    elif OneRow[-3:] == "210":
        CategDict["210"] += 1
    elif OneRow[-3:] == "220":
        CategDict["220"] += 1
for Categ in CategDict:   #输出
    print(Categ+"\t"+str(CategDict[Categ]),file=Result2)

def isChinese(ch):    #使用一个判断是否中文的程序
    if 0x4e00 <= ord(ch) < 0x9fa6:
        return True;
    return False

def Task5(StartProv,EndProv):   #输入StartProv.EndProv,找到这两个Prov之间的文段到Target
    print(StartProv,file=Result2)
    Start = RawData.find(StartProv)
    End = RawData.find(EndProv)
    Target = RawData[Start:End]
    TargetList = Target.splitlines()
    Basic = []        #Basic 捕获的是所有基层单位，并且名字含有“村委会”的行
    CharDict = {}     #创立字符字典，value是字出现次数
    for OneRow in TargetList:
        if OneRow[:4] == "\t\t\t\t" and OneRow[-6:-3]=="村委会":
            Basic.append(OneRow)
    for One in Basic:    #每一行的每一个字符的循环
        for Char in One[:-6]:
            if isChinese(Char) == True: #判断是否是中文
                if Char in CharDict:
                    CharDict[Char] += 1
                else:
                    CharDict[Char] = 1
    CharList = list(CharDict.items())
    CharList.sort(key=lambda X:X[1],reverse=True)  #倒序排序
    for (myKey, myValue) in CharList[:100]:     #输出前100个
        print(str(myKey)+"\t"+str(myValue), file=Result2)
    return  1

Task5("内蒙古自治区","辽宁省")
Task5("河南省","湖北省")

Result2.close()

