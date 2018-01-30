string = ("This is some **text** that is **bold**\n" +
          "And *here* is some *italic*")

boldPosLst = []
italicPosLst = []
parsedStr = string
if '**' in parsedStr:
    for pos, char in enumerate(parsedStr):
        if parsedStr[pos:pos+2] == '**':
            boldPosLst.append(pos)
    parsedStr = parsedStr.replace('**',"")

if '*' in parsedStr:
    for pos, char in enumerate(parsedStr):
        if char == '*':
            italicPosLst.append(pos)
    parsedStr = parsedStr.replace('*',"")

print(boldPosLst)
print(italicPosLst)
