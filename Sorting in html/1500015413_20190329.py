with open("1500015413_chinaAirPortData.txt","r",encoding="utf-8") as r:
    RawData=r.read()
RawList=RawData.splitlines()
RawList=RawList[0:227]
AllAirport=[]
for OneAirport in RawList:
    OneList = OneAirport.split(",")
    OneList.pop(0)
    Temp=float(OneList[2])          #将2017年数据存入Temp
    OneList[2]=float(OneList[1])    #将第三列换为2018年数据
    OneList[1]=Temp                 #将第二列换为2017年数据
    Growth=(OneList[2]/OneList[1]-1)*100
    OneList.append(Growth)
    AllAirport.append(OneList)
AllAirport.sort(key=lambda x:x[1])


def Sort(List,Column,Seq):   #Column为按照第几列排序参数（集合{2,3,4}) Seq为顺序/倒序参数,集合为{0,1}(0是升序，1是倒序）
    List.sort(key=lambda x:x[Column-1],reverse=Seq)
    return List

from flask import  Flask,request,render_template
MyWeb=Flask(__name__)

 #网页内容
@MyWeb.route("/")
def MainPage():
    wwwcontent ="<tr> <td> 机场名称 </td> <td> 2017年 </td> <td> 2018年 </td> <td> 增长率 </td> </tr>"
    for OneAirport in AllAirport:
        wwwcontent += "<tr>"
        for i in range(0,4):
            if i!=0:
                wwwcontent += "<td>{}</td>".format(str(round(OneAirport[i], 2)))
            else:
                wwwcontent += "<td>{}</td>".format(str(OneAirport[i]))
        wwwcontent += "</tr>"
    return render_template("template.html",WWWcontent=wwwcontent)

@MyWeb.route("/WebInput/",methods=["post"])
def browseInput():
    Column=request.form["Column"]
    Seq=request.form["Seq"]
    SortedAllAirport=Sort(AllAirport,int(Column),int(Seq))

    wwwcontent ="<tr> <td> 机场名称 </td> <td> 2017年 </td> <td> 2018年 </td> <td> 增长率 </td> </tr>"
    for OneAirport in SortedAllAirport:
        wwwcontent += "<tr>"
        for i in range(0,4):
            if i!=0:
                wwwcontent += "<td>{}</td>".format(str(round(OneAirport[i], 2)))
            else:
                wwwcontent += "<td>{}</td>".format(str(OneAirport[i]))
        wwwcontent += "</tr>"


    return render_template("template.html",WWWcontent=wwwcontent)

#Main Process
if __name__== "__main__":
    MyWeb.run()

