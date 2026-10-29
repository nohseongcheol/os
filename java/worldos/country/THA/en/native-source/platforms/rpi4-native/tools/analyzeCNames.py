#!/usr/bin/env python3
"""libclang Declaration·reference 위치를 수집한다. externalValue 헤더의 멤버는 변환하지 않는다."""
import ctypes as cSource
import hashlib
import json
from pathlib import Path

projectRoot = Path(__file__).resolve().parents[1]
implementation = cSource.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class stringValue(cSource.Structure): _fields_ = [('data',cSource.c_void_p),('showValue',cSource.c_uint)]
class cursorValue(cSource.Structure): _fields_ = [('kindValue',cSource.c_uint),('auxiliaryValue',cSource.c_int),('data',cSource.c_void_p*3)]
class position(cSource.Structure): _fields_ = [('data',cSource.c_void_p*2),('offsetValue',cSource.c_uint)]
def functionValue(name, returnResult, *arguments):
    entryValue = getattr(implementation, name); entryValue.restype = returnResult; entryValue.argtypes = list(arguments); return entryValue
getText = functionValue('clang_getCString',cSource.c_char_p,stringValue)
releaseText = functionValue('clang_disposeString',None,stringValue)
def text(value):
    result = (getText(value) or b'').decode('utf-8'); releaseText(value); return result
getName = functionValue('clang_getCursorSpelling',stringValue,cursorValue)
getReference = functionValue('clang_getCursorReferenced',cursorValue,cursorValue)
getPosition = functionValue('clang_getCursorLocation',position,cursorValue)
filePosition = functionValue('clang_getFileLocation',None,position,cSource.POINTER(cSource.c_void_p),cSource.POINTER(cSource.c_uint),cSource.POINTER(cSource.c_uint),cSource.POINTER(cSource.c_uint))
fileEntryName = functionValue('clang_getFileName',stringValue,cSource.c_void_p)
uniqueName = functionValue('clang_getCursorUSR',stringValue,cursorValue)
connectionKind = functionValue('clang_getCursorLinkage',cSource.c_uint,cursorValue)
visitedType = cSource.CFUNCTYPE(cSource.c_uint,cursorValue,cursorValue,cSource.c_void_p)
visitValue = functionValue('clang_visitChildren',cSource.c_uint,cursorValue,visitedType,cSource.c_void_p)
generate = functionValue('clang_createIndex',cSource.c_void_p,cSource.c_int,cSource.c_int)
analyzeValue = functionValue('clang_parseTranslationUnit',cSource.c_void_p,cSource.c_void_p,cSource.c_char_p,cSource.POINTER(cSource.c_char_p),cSource.c_int,cSource.c_void_p,cSource.c_uint,cSource.c_uint)
rootValue = functionValue('clang_getTranslationUnitCursor',cursorValue,cSource.c_void_p)
quitProgram = functionValue('clang_disposeTranslationUnit',None,cSource.c_void_p)
diagnosticCount = functionValue('clang_getNumDiagnostics',cSource.c_uint,cSource.c_void_p)
getDiagnostic = functionValue('clang_getDiagnostic',cSource.c_void_p,cSource.c_void_p,cSource.c_uint)
severityValue = functionValue('clang_getDiagnosticSeverity',cSource.c_uint,cSource.c_void_p)
diagnosticMessage = functionValue('clang_getDiagnosticSpelling',stringValue,cSource.c_void_p)
releaseDiagnostic = functionValue('clang_disposeDiagnostic',None,cSource.c_void_p)

def positionIndex(entryValue):
    file = cSource.c_void_p(); line = cSource.c_uint(); slotEntry = cSource.c_uint(); offsetValue = cSource.c_uint()
    filePosition(getPosition(entryValue),cSource.byref(file),cSource.byref(line),cSource.byref(slotEntry),cSource.byref(offsetValue))
    return (text(fileEntryName(file)) if file else '', offsetValue.value, line.value)

def executeCommand():
    lookupIndex = generate(0,0); declarationsList = {}; referencesList = []; errors = []
    # compilerTool.c는 Native Declaration 없이 TinyCC externalValue 단일 translateSource 단위만 포함한다.
    # externalValue 선언을 Native 이름으로 세지 않으며, actualData 빌드에서는 continueProcessing 컴파일한다.
    ownedFile = {str(path.resolve()) for path in projectRoot.rglob('*') if path.suffix in ('.c','.h','.cpp','.inc')
              and not set(path.relative_to(projectRoot).parts)&{'build','dist','vendor','__pycache__'}
              and path.relative_to(projectRoot).as_posix() != 'CCompiler/compilerTool.c'}
    commonValue = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(projectRoot/'User'),
          '-I'+str(projectRoot.parents[1]/'posix-kor/arm64-native/headers'),'-I'+str(projectRoot/'build'),'-I'+str(projectRoot/'build/user'),
          '-I'+str(projectRoot/'build/remote'),'-I'+str(projectRoot/'vendor/bearssl/inc'),
          '-I'+str(projectRoot/'vendor/bearssl/src'),'-I'+str(projectRoot/'vendor/libassh/src'),
          '-I'+str(projectRoot/'vendor/lwip/src/include'),'-I'+str(projectRoot/'networkStack'),
          '-I'+str(projectRoot/'remoteValue'),'-I'+str(projectRoot/'CCompiler')]
    for path in sorted(Path(name) for name in ownedFile if name.endswith(('.c','.cpp'))):
        arguments = commonValue + ['-std=c++11' if path.suffix=='.cpp' else '-std=c11']
        if 'networkStack' in path.parts: arguments += ['-I'+str(projectRoot/'networkStack'),'-I'+str(projectRoot/'vendor/lwip/src/include')]
        if 'CCompiler' in path.parts:
            arguments += ['-I'+str(projectRoot/'CCompiler'),'-I'+str(projectRoot/'vendor/tinycc'),'-I'+str(projectRoot/'build/ccompiler'),
                    '-isystem',str(projectRoot.parent/'rpi4/build/rootfs/usr/include')]
        if 'pythonBridge' in path.parts:
            arguments += ['-I'+str(projectRoot/'pythonBridge'),'-I'+str(projectRoot/'build/micropython-1.24.1'),'-I'+str(projectRoot/'build/python'),'-isystem','/usr/include/newlib']
        if 'remoteValue' in path.parts:
            arguments += ['-isystem', '/usr/include/newlib']
        if 'distributionValue' in path.parts: arguments += ['-D__JKOROS__=1']
        if path.name=='Bundle.c': arguments += ['-I'+str(projectRoot/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        groupValue = (cSource.c_char_p*len(arguments))(*[entryValue.encode() for entryValue in arguments])
        translationUnit = analyzeValue(lookupIndex,str(path).encode(),groupValue,len(arguments),None,0,1)
        for index in range(diagnosticCount(translationUnit)):
            diagnosticValue = getDiagnostic(translationUnit,index)
            if severityValue(diagnosticValue)>=3: errors.append((str(path.relative_to(projectRoot)),text(diagnosticMessage(diagnosticValue))))
            releaseDiagnostic(diagnosticValue)
        @visitedType
        def inspectValue(entryValue,parentValue,data):
            file,offsetValue,line = positionIndex(entryValue)
            if file not in ownedFile: return 2 if entryValue.kindValue==300 else 1
            lexicalWord = text(getName(entryValue))
            if not lexicalWord or any(ord(characterValue)>127 for characterValue in lexicalWord): return 2
            if entryValue.kindValue in (2,3,4,5,6,7,8,9,10,20,21,501):
                uniqueValue = text(uniqueName(entryValue)) or file+':'+str(offsetValue)
                declarationsList[uniqueValue] = {'file':file,'offsetValue':offsetValue,'line':line,'kindValue':entryValue.kindValue,'name':lexicalWord,'connect':connectionKind(entryValue)}
                referencesList.append((file,offsetValue,lexicalWord,uniqueValue))
            else:
                reference = getReference(entryValue)
                referenceFile,_,_ = positionIndex(reference)
                if referenceFile in ownedFile:
                    uniqueValue = text(uniqueName(reference)); referencesList.append((file,offsetValue,text(getName(reference)),uniqueValue))
            return 2
        visitValue(rootValue(translationUnit),inspectValue,None)
        quitProgram(translationUnit)
    destinationValue = projectRoot/'build/한국어화/시언어분석.json'
    destinationValue.parent.mkdir(parents=True, exist_ok=True)
    hashesList = {file:hashlib.sha256(Path(file).read_bytes()).hexdigest() for file in sorted(ownedFile)}
    destinationValue.write_text(json.dumps({'Declaration':declarationsList,'reference':referencesList,'error':errors,'원문해시':hashesList},ensure_ascii=False,indent=2)+'\n')
    print('Declaration',len(declarationsList),'reference',len(referencesList),'error',len(errors))
    for error in errors: print(*error)

if __name__=='__main__': executeCommand()
