#!/usr/bin/env python3
"""Declaration 고유번호와 UTF-8 byteValue 위치로 Native C 이름을 옮기는 일회성 이행 tools.

externalValue 구조체의 멤버, stringValue, C 표준 functionValue, Porting 규약은 보존한다.
입력은 changeValue beforeValue 소스에 대한 analyzeCNames.py 결과여야 한다.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

projectRoot = Path(__file__).resolve().parents[1]

def executeCommand():
    analyzeValue = json.loads((projectRoot/'build/한국어화/시언어분석.json').read_text())
    if analyzeValue['error']: raise SystemExit('analyzeValue 오류를 먼저 해결해야 합니다.')
    nameTable = json.loads((projectRoot/'naming/cNames.json').read_text())
    standardDefinition = set(json.loads((projectRoot/'naming/standardNames.json').read_text()))
    declarationTable = analyzeValue['Declaration']
    declarationToReplace = {uniqueValue:nameTable[entryValue['name']] for uniqueValue,entryValue in declarationTable.items()
                if entryValue['name'] in nameTable and entryValue['name'] not in standardDefinition}
    connectionTable = {entryValue['name']:nameTable[entryValue['name']] for entryValue in declarationTable.values()
              if entryValue.get('connect')==4 and entryValue['kindValue'] in (8,9)
              and entryValue['name'] in nameTable and entryValue['name'] not in standardDefinition}
    # generate AOT C·어셈블리·공개 SDK가 공유하는 바이너리 connect 이름만 유지한다.
    headValue = ['/* English sourceTree 이름과 기존 machine connect contractValue. 자동 generate: naming/cNames.json */',
           '#ifndef nativeMachineLinkNamesHeader', '#define nativeMachineLinkNamesHeader']
    headValue += ['#define '+newName+' '+oldName for oldName,newName in sorted(connectionTable.items())]
    headValue += ['#endif','']
    (projectRoot/'naming/machineLinkNames.h').write_text('\n'.join(headValue))
    changesList = defaultdict(dict)
    for file,offsetValue,name,uniqueValue in analyzeValue['reference']:
        if uniqueValue in declarationToReplace:
            changesList[file][offsetValue] = (name,declarationToReplace[uniqueValue])
    logRecord = ['file\t원래바이트위치\t이전이름\t한국어이름']
    ignoreValue = []
    for file,changeValue in changesList.items():
        path = Path(file); original = path.read_bytes(); data = original
        for offsetValue,(oldName,newName) in sorted(changeValue.items(),reverse=True):
            ending = offsetValue+len(oldName.encode())
            if original[offsetValue:ending] != oldName.encode():
                ignoreValue.append((str(path.relative_to(projectRoot)),offsetValue,oldName));continue
            data = data[:offsetValue]+newName.encode()+data[ending:]
            logRecord.append('{}\t{}\t{}\t{}'.format(path.relative_to(projectRoot),offsetValue,oldName,newName))
        path.write_bytes(data)
    # preprocessSource 매개변수는 AST의 선언으로 나타나지 않는다. preprocessSource 줄만 보완한다.
    lexicalWord = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?\*/|\b[A-Za-z_]\w*\b')
    macroValue = {entryValue['name']:nameTable[entryValue['name']] for entryValue in declarationTable.values()
              if entryValue['kindValue']==501 and entryValue['name'] in nameTable and entryValue['name'] not in standardDefinition}
    for path in sorted({Path(entryValue['file']) for entryValue in declarationTable.values()}):
        lineList = path.read_text().splitlines(True); isContinuation = False
        for index,line in enumerate(lineList):
            preprocessSource = isContinuation or bool(re.match(r'\s*#',line))
            isContinuation = preprocessSource and line.rstrip().endswith('\\')
            if preprocessSource:
                lookupTable = nameTable if re.match(r'\s*#\s*define\b',line) or isContinuation else macroValue
                lineList[index] = lexicalWord.sub(lambda isMatched: lookupTable.get(isMatched[0],isMatched[0]) if isMatched[0] not in standardDefinition else isMatched[0],line)
        path.write_text(''.join(lineList))
    # 각 Native translateSource 단위에만 연결표를 넣는다. externalValue 배포본에는 전파하지 않는다.
    for path in sorted({Path(entryValue['file']) for entryValue in declarationTable.values()}):
        if path.suffix not in ('.c','.cpp'):continue
        peerValue = '../' * len(path.relative_to(projectRoot).parts[:-1]) + 'naming/machineLinkNames.h'
        path.write_text('#include "'+peerValue+'"\n'+path.read_text())
    (projectRoot/'naming/cNameMapping.tsv').write_text('\n'.join(logRecord)+'\n')
    (projectRoot/'build/한국어화/전처리참조.json').write_text(json.dumps(ignoreValue,ensure_ascii=False,indent=2)+'\n')
    print('changeValue',len(logRecord)-1,'preprocessSource 재검토',len(ignoreValue),'machine connect',len(connectionTable))

if __name__=='__main__': executeCommand()
