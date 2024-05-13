import math
import random
from docx import Document
from enum import Enum
import WriteFile


# 数学
# 加减乘除计算类型
class OperationType(Enum):
    Add = 1#+
    Reduce = 2#-
    # AddReduce = 3#+-
    Mutiplication = 4#x
    Divition = 5#%
    # MutiAndDivition = 6#x%
    # AllType = 7#所有

minRangeNumber = 0 # 最小数字（多少以内的数学加减乘除式子）
maxRangeNumber = 20 # 20以内（多少以内的数学加减乘除式子）与minRangeNumber结合标识[0,20]以内的加减乘除法
numOfOperation = 2 # 运算位数 比如1+1=2为2位 即参与运算的数字个数
isRandomSpaceNumber = True # 是否随机出现空格排列数字 加法为例: False: xx + xx=__; True: xx + __ = xx
isHaveNegNumber = False # 减法是否有负数参与
isHaveRemainder4Division = False # 除法是否有余数计算

numberLine = 100 # 输出多少个式子（每份试卷有多少个数学提）
numberOfPage = 5 # 生成多少分试卷

fillItemContentStr = "____"
addContentStr = " + "
reduceContentStr = " - "
muutiplicationContentStr = " * "
divitionContentStr = " ÷ "
equalContentStr = " = "
remainderContentStr = " ··· "

buildOpterationType = OperationType.Add # 当前生成的式子类型参考OperationType

#生成的文件放在哪个路径
writeFilePath =  "C:/Users/Administrator/Desktop/TempDir/"

def getSignalNumber(maxNumber:int, isCanZero:bool = True, minNumber:int = minRangeNumber):
    """获取一个单独数字

    Args:
        maxNumber (int): 随机出来的最大数字上线
        isCanZero (bool, optional): 是否可以为0/最小数字 false&&结果等于最小数字的时候 会自动+1

    Returns:
        int: 随机的数字结果
    """    
    result = random.randint(minNumber, maxNumber)
    if isCanZero == False and result == minNumber:
        result += 1
    return result

def buildAdd(maxNumber, isRandomSpace:bool = False, numOfOperation = 2):
    """加法构建

    Args:
        maxNumber (int): 最大数字
        isRandomSpace (bool): 是否随机缺省位置
        digiteNumber (int): 在isRandomSpace==true的时候确定缺省位置是哪一个位置的时候使用 缺省位置最大数

    Returns:
        [str]: 按顺序排列好的字符串数组 例如["xx","+","xx","=","__"]
    """    
    contentList = []
    if isRandomSpace == False:
        for index in range(0, numOfOperation):
            item = getSignalNumber(maxNumber)
            if len(contentList) <= 0:
                contentList.append(str(item))
            else:
                contentList.append(addContentStr)
                contentList.append(str(item))
        contentList.append(equalContentStr)
        contentList.append(fillItemContentStr)
    else:
        spaceNumber = random.randint(0,numOfOperation)
        itemContent = fillItemContentStr
        tempSum = 0
        for index in range(0, numOfOperation):
            item = getSignalNumber(maxNumber)
            if spaceNumber == index:
                if len(contentList) <= 0:
                    contentList.append(itemContent)
                else:
                    contentList.append(addContentStr)
                    contentList.append(itemContent)
            else:
                if len(contentList) <= 0:
                    contentList.append(str(item))
                else:
                    contentList.append(addContentStr)
                    contentList.append(str(item))
                tempSum += item
        contentList.append(equalContentStr) 
        if spaceNumber >= numOfOperation:
            contentList.append(itemContent)
        else:
            contentList.append(str(tempSum + getSignalNumber(maxNumber)))
    return contentList

def buildReduce(maxNumber, isRandomSpace:bool = False, numOfOperation = 2):
    """减法

    Args:
        maxNumber (_type_): _description_
        isRandomSpace (bool, optional): _description_. Defaults to False.
        numOfOperation (int, optional): _description_. Defaults to 2.

    Returns:
        _type_: _description_
    """    
    contentList = []
    itemContent = fillItemContentStr
    randomSpaceIndex = random.randint(0, numOfOperation)
    if isRandomSpace == False:
        randomSpaceIndex = numOfOperation
    summer = 0
    addNumberList = []

    for numIndex in range(0, numOfOperation):
        item = getSignalNumber(maxNumber)
        summer = summer + item
        addNumberList.append(item)
    if isHaveNegNumber == False:
        addNumberList.insert(0, summer)
    else:
        tempSummer = random.randint(0, summer*2)
        addNumberList.insert(0, tempSummer)
        lastItem = addNumberList[len(addNumberList) - 1]
        addNumberList.pop(len(addNumberList) - 1)
        addNumberList.append(tempSummer - summer)

    for itemIndex in range(0, len(addNumberList)):
        item = addNumberList[itemIndex]
        
        if itemIndex > 0:
            if itemIndex >= len(addNumberList) - 1:
                contentList.append(equalContentStr)
            else:
                contentList.append(reduceContentStr)

        if randomSpaceIndex == itemIndex:
            contentList.append(itemContent)
        else:
            contentList.append(str(item))
           
    return contentList

def buildMutiplication(maxNumber, isRandomSpace:bool = False, numOfOperation = 2):
    """乘法

    Args:
        maxNumber (_type_): _description_
        isRandomSpace (bool, optional): _description_. Defaults to False.
        numOfOperation (int, optional): _description_. Defaults to 2.

    Returns:
        _type_: _description_
    """    
    contentList = []
    spaceNumber = random.randint(0, numOfOperation)
    if isRandomSpace == False:
        spaceNumber = numOfOperation
    summer = 0
    remainder = 0
    numberList = []
    for index in range(0, numOfOperation):
        item = getSignalNumber(maxNumber, False)
        if index == 0:
            summer = item
        else:
            summer = summer * item
        numberList.append(item)
    # if isHaveRemainder4Division:
    #     remainder = random.randint(1, summer) 
    numberList.append(summer + remainder)
    for itemIndex in range(0, len(numberList)):
        item = numberList[itemIndex]
        if itemIndex > 0:
            if itemIndex >= len(numberList) - 1:
                contentList.append(equalContentStr)
            else:
                contentList.append(muutiplicationContentStr)
        if itemIndex == spaceNumber:
            contentList.append(fillItemContentStr)
        else:
            contentList.append(str(item))
    return contentList

def buildDivition(maxNumber, isRandomSpace:bool = False, numOfOperation = 2):
    contentList = []
    spaceNumber = random.randint(0, numOfOperation)
    summer = 0
    remainder = 0
    numberList = []
    for index in range(0, numOfOperation):
        item = getSignalNumber(maxNumber, False)
        if index == 0:
            summer = item
        else:
            summer = summer * item
        numberList.append(item)
    if isHaveRemainder4Division:
        remainder = random.randint(1, summer) 
    numberList.insert(0, summer + remainder)
    
    for itemIndex in range(0, len(numberList)):
        if itemIndex != 0:
            if itemIndex < len(numberList) - 1:
                contentList.append(divitionContentStr)
            else:
                contentList.append(equalContentStr)

        if itemIndex == spaceNumber:
            contentList.append(fillItemContentStr)
        else:
            contentList.append(str(numberList[itemIndex]))
            
    if isHaveRemainder4Division:
        isShowRemainder = random.randint(0, 1) == 1
        if isShowRemainder == False:
            contentList.append(remainderContentStr)
            contentList.append(fillItemContentStr)
        else:
            contentList.append(remainderContentStr)
            contentList.append(str(remainder) )
    return contentList

def buildFormula(oType:OperationType, maxNumber:int):
    contentList:list = []
    tempItemNumber = 0
    result = ""
    if oType == OperationType.Add:
        contentList = buildAdd(maxNumber, False)
            
    elif oType == OperationType.Reduce:
        contentList = buildReduce(maxNumber, False)

    elif oType == OperationType.AddReduce:
        temp = random.randint(0, 100)
        if temp % 2 == 1:
            contentList.append(str(getSignalNumber(maxNumber)))
            contentList.append(addContentStr)
            contentList.append(str(getSignalNumber(maxNumber)))
            tempItemNumber = contentList[0] + contentList[1]
        else:
            temp = getSignalNumber(maxNumber, False)
            contentList.append(str(temp))
            contentList.append(reduceContentStr)
            temp2 = getSignalNumber(temp)
            contentList.append(str(temp2))
            tempItemNumber = contentList[0]- contentList[1]

        temp = random.randint(0, 100)
        if temp % 2 == 1:
            contentList.append(addContentStr)
            contentList.append(str(getSignalNumber(maxNumber)))
        else:
            contentList.append(reduceContentStr)
            if tempItemNumber == 0:
                contentList.append("0")
            else:
                contentList.append(str(getSignalNumber(tempItemNumber)))
        contentList.append(equalContentStr)

    elif oType == OperationType.Mutiplication:
        contentList = buildMutiplication(maxNumber, False)

    elif oType == OperationType.Divition:
        contentList = buildDivition(maxNumber, False)

    elif oType == OperationType.MutiAndDivition:
        temp = random.randint(0, 100)
        if temp % 2 == 1:
            contentList.append(str(getSignalNumber(maxNumber)))
            contentList.append(" x ")
            contentList.append(str(getSignalNumber(maxNumber)))
            tempItemNumber = contentList[0] + contentList[1]
        else:
            temp = getSignalNumber(maxNumber)
            temp2 = getSignalNumber(temp, False)
            while temp % temp2 != 0 :
                temp2 = getSignalNumber(temp, False)
            contentList.append(str(temp))
            contentList.append(divitionContentStr)
            contentList.append(str(temp2))
            tempItemNumber = contentList[0] / contentList[1]

        temp = random.randint(0, 100)
        if temp % 2 == 1:
            contentList.append(" x ")
            contentList.append(str(getSignalNumber(maxNumber)))
        else:
            contentList.append(divitionContentStr)
            temp3 = getSignalNumber(tempItemNumber, False)
            while tempItemNumber % temp3 != 0 :
                temp3 = getSignalNumber(tempItemNumber, False)
            contentList.append(str(temp3))
        contentList.append(equalContentStr)

    for item in contentList:
        result += item
    return result


resultContent = ""
#region add method 加法
def buildAddListStr():
    opType = OperationType.Add
    addMap:dict = {}
    while len(addMap) < numberLine:
        itemResult = buildFormula(opType, maxRangeNumber)
        item = addMap.get(addMap.keys)
        if addMap.get(itemResult) is None:
            addMap[itemResult] = itemResult     
    #keys = addMap.keys
    itemResultContent = ""
    index = 0
    for item in addMap:
        if index == 0:
            itemResultContent = item
            index += 1
            continue
        elif index % 2 == 0:
            itemResultContent += "\n"
        else:
            itemResultContent += "\t\t"
        index += 1
        itemResultContent += item
    return itemResultContent
#endregion

#region method 减法
def buildReduceListStr():
    reduceMap = {}
    opType = OperationType.Reduce     
    while len(reduceMap) < numberLine:
        itemResult = buildFormula(opType, maxRangeNumber)
        item = reduceMap.get(reduceMap.keys)
        if reduceMap.get(itemResult) is None:
            reduceMap[itemResult] = itemResult
    
    index = 0
    itemResultContent = ""
    for item in reduceMap:
        if index == 0:
            itemResultContent += item
            index += 1
            continue
        elif index % 2 == 0:
            itemResultContent += "\n"
        else:
            itemResultContent += "\t\t"
        index += 1
        itemResultContent += item
    return itemResultContent
#endregion

#region method 乘法
def buildMutiplicationListStr():
    mutiplicationMap = {}
    opType = OperationType.Mutiplication
    while len(mutiplicationMap) < numberLine:
        itemResult = buildFormula(opType, maxRangeNumber)
        item = mutiplicationMap.get(mutiplicationMap.keys)
        if mutiplicationMap.get(itemResult) is None:
            mutiplicationMap[itemResult] = itemResult
    itemResultContent = ""
    index = 0
    for item in mutiplicationMap:
        if index == 0:
            itemResultContent += item
            index += 1
            continue
        elif index % 2 == 0:
            itemResultContent += "\n"
        else:
            itemResultContent += "\t\t"
        index += 1
        itemResultContent += item
    return itemResultContent
#endregion

#region method 除法
def buildDivitionListStr():
    divitionMap = {}
    opType = OperationType.Divition
    while len(divitionMap) < numberLine:
        itemResult = buildFormula(opType, maxRangeNumber)
        item = divitionMap.get(divitionMap.keys)
        if divitionMap.get(itemResult) is None:
            divitionMap[itemResult] = itemResult
    itemResultContent = ""
    index = 0
    for item in divitionMap:
        if index == 0:
            itemResultContent += item
            index += 1
            continue
        elif index % 2 == 0:
            itemResultContent += "\n"
        else:
            itemResultContent += "\t\t"
        index += 1
        itemResultContent += item
    return itemResultContent
#endregion

for testIndex in range(0, numberOfPage):
    #resultContent = buildReduceListStr()
    filePath = writeFilePath + "WestonLeeWorkBook" + str(testIndex) + ".docx"
    doc = Document()
    rowItemStr = ""
    columIndex = 0

    for itemIndex in range(0, numberLine):
        if buildOpterationType == OperationType.Add:# +
            itemResultList = buildAdd(maxRangeNumber, isRandomSpaceNumber, numOfOperation)
        elif buildOpterationType == OperationType.Reduce:# -
            itemResultList = buildReduce(maxRangeNumber, isRandomSpaceNumber, numOfOperation)
        elif buildOpterationType == OperationType.Mutiplication:# *
            itemResultList = buildMutiplication(maxRangeNumber, isRandomSpaceNumber, numOfOperation)
        elif buildOpterationType == OperationType.Divition:# %
            itemResultList = buildDivition(maxRangeNumber, isRandomSpaceNumber, numOfOperation)

        for itemStr in itemResultList:
            while len(itemStr) < 3:
                itemStr += " "
            rowItemStr += itemStr
        rowItemStr += "\t\t"
        columIndex += 1
        maxColum = 4
        if isHaveRemainder4Division:
            maxColum = 2
            rowItemStr += "\t\t\t\t"
        if columIndex >= maxColum:
            paragraph = doc.add_paragraph(rowItemStr)
            rowItemStr = ""
            columIndex = 0
    doc.save(filePath)
    #WriteFile.writeContent2FullPathFile(resultContent, filePath)