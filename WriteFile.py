def writeContent2File(contentStr:str, pathFile:str, fileName:str, sufixStr:str):
    fullPath4File = pathFile + "/" + fileName + "." + sufixStr
    pyWriteFile = open(fullPath4File, 'w', encoding='UTF-8')
    pyWriteFile.write(contentStr)
    pyWriteFile.close()

def writeContent2FullPathFile(contentStr:str, pathFile:str):
    fullPath4File = pathFile 
    pyWriteFile = open(fullPath4File, 'w', encoding='UTF-8')
    pyWriteFile.write(contentStr)
    pyWriteFile.close()