import urllib
import json
import urllib.request

import html2text


def remove_duplicates(l):
    return list(set(l))


def getUrl(index, data):
    image = True
    url = data[index]
    i = 1
    while image:
        if "Starting" not in data[index+i]:
            url += data[index+i]
            i+=1
        else:
            image = False
    if url.startswith("![]("):
        url = url[4:]
    if url.endswith(")"):
        url = url[:-1]
    return(url)


def getName(index, data):
    test = True
    name = data[index]
    i = 1
    while test:
        if "![]" not in data[index+i]:
            name += data[index+i]
            #name += " "
            i += 1
        else:
            test = False
    if name.endswith("Counter-Strike:GlobalOffensive"):
        name = name[:-30]
    if "|" in name:
        index = name.index("|")
        nameX = name[index+1:]
        itemType = name[:-(len(nameX)+1)]
    else:
        nameX = name
        itemType = "Case"
    return(nameX, itemType)


def getData(dataLink, itemDict):
    data = urllib.request.urlopen(dataLink)     #These lines are for when using the live data
    data = data.readall().decode("utf-8")       # ^^^
    #data = open("data.json")                   #This line is for reading from files
    #data = data.read()                         # ^^^
    data = json.loads(data)
    data = data["results_html"]
    h = html2text.HTML2Text()
    h.ignore_links = True
    data = h.handle(data)
    data = data.split()
    data = data[3:]

    #print(data[0:20])                          #Debug code

    ##for x in range(20):
    ##    print(data[x])
    ##    print()

    tempUrl = ""
    tempPrice = ""
    tempAmount = ""
    tempName = ""
    tempType = ""

    for x in range(len(data)):
        if "![]" in data[x]:
            tempUrl = getUrl(x, data)
            #print(tempUrl)
        if "$" in data[x]:
            tempPrice = data[x]
            #print(tempPrice)
        if "USD" in data[x]:
            tempAmount = data[x+1]
            #print(tempAmount)
            try:
                tempName, tempType = getName(x+2, data)
            except:
                pass
            #print(tempName)
        if tempName != "":
            itemDict.update({tempName:{"Price":tempPrice,
                                       "Amount":tempAmount,
                                       "Image":tempUrl,
                                       "Type": tempType
                                       }
                             })
            tempUrl = ""
            tempPrice = ""
            tempAmount = ""
            tempName = ""
            tempType = ""

dataLink = ""
itemDict = {}

for x in range(0,4000,100):
    eval('getData("http://steamcommunity.com/market/search/render/?query=&start='+str(x)+'&count=100&search_descriptions=0&sort_column=quantity&sort_dir=desc&appid=730", itemDict)')

##types = []
##
##for x in itemDict.keys():
##    types.append(itemDict[x]["Type"])
##types = remove_duplicates(types)
##types.sort()
##for x in types:
##    print(x)
