from flask import Flask, request, render_template
with open("hzFollow.txt", "r", encoding="utf-8") as rFile:
    CharList = rFile.readlines()
CharDict = {}
for OneLine in CharList:
    TempList=OneLine[2:].split(";")
    TempList.pop() #删除最后面的换行符
    FollowList = []
    for i in TempList:
        FollowList.append(i[0])  #去掉数字，仅保留第一个的汉字
    StrFollow = ""
    for j in range(min(10, len(FollowList))):  #输出格式：0、们;	1、的;	2、国;	3、是;	4、不;……  前10个
        StrFollow = StrFollow+str(j)+"、"+str(FollowList[j])+";"+"\t"
    CharDict[OneLine[0]] = StrFollow

MyWeb=Flask(__name__)
@MyWeb.route("/")
def MainPage():
    return render_template("Page.html")

@MyWeb.route("/link",methods=["get","post"])     #如果用request.form实现页面向服务器的传输，但这就不是网页内的交互；如果用$.post()就无法实现页面向服务器的传输
def Link():
    Input = request.form["LastChar"]
    if Input in CharDict:
        return CharDict[Input]
    else:
        return Input


if __name__=="__main__":
    MyWeb.run()
