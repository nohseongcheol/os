#!/usr/bin/env python3
"""libclang 선언·संदर्भ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

प्रॉजॅक्ट_रूट = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class स्ट्रिंग_मोल(씨.Structure): _fields_ = [('डेटा',씨.c_void_p),('शो_मोल',씨.c_uint)]
class कर्सर_मोल(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('डेटा',씨.c_void_p*3)]
class स्थिती(씨.Structure): _fields_ = [('डेटा',씨.c_void_p*2),('ऑफसॅट_मोल',씨.c_uint)]
def फंक्शन_मोल(नांव, return_मेजप, *인수):
    प्रवेश_मोल = getattr(구현, नांव); प्रवेश_मोल.restype = return_मेजप; प्रवेश_मोल.argtypes = list(인수); return प्रवेश_मोल
글얻기 = फंक्शन_मोल('clang_getCString',씨.c_char_p,स्ट्रिंग_मोल)
रिलीज_SMS = फंक्शन_मोल('clang_disposeString',None,स्ट्रिंग_मोल)
def SMS(मोल):
    मेजप = (글얻기(मोल) or b'').decode('utf-8'); रिलीज_SMS(मोल); return मेजप
이름얻기 = फंक्शन_मोल('clang_getCursorSpelling',स्ट्रिंग_मोल,कर्सर_मोल)
참조얻기 = फंक्शन_मोल('clang_getCursorReferenced',कर्सर_मोल,कर्सर_मोल)
위치얻기 = फंक्शन_मोल('clang_getCursorLocation',स्थिती,कर्सर_मोल)
फायल_स्थिती_2aa21a9a = फंक्शन_मोल('clang_getFileLocation',None,स्थिती,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
फायल_प्रवेश_नांव = फंक्शन_मोल('clang_getFileName',स्ट्रिंग_मोल,씨.c_void_p)
UNIQUE_नांव = फंक्शन_मोल('clang_getCursorUSR',स्ट्रिंग_मोल,कर्सर_मोल)
연결종류 = फंक्शन_मोल('clang_getCursorLinkage',씨.c_uint,कर्सर_मोल)
방문형 = 씨.CFUNCTYPE(씨.c_uint,कर्सर_मोल,कर्सर_मोल,씨.c_void_p)
방문 = फंक्शन_मोल('clang_visitChildren',씨.c_uint,कर्सर_मोल,방문형,씨.c_void_p)
तयार_करचें = फंक्शन_मोल('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = फंक्शन_मोल('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
रूट_मोल = फंक्शन_मोल('clang_getTranslationUnitCursor',कर्सर_मोल,씨.c_void_p)
सोडचें_एप्लिकेशन = फंक्शन_मोल('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = फंक्शन_मोल('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = फंक्शन_मोल('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
कळोवणी_मोल = फंक्शन_मोल('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = फंक्शन_मोल('clang_getDiagnosticSpelling',स्ट्रिंग_मोल,씨.c_void_p)
진단해제 = फंक्शन_मोल('clang_disposeDiagnostic',None,씨.c_void_p)

def स्थिती_INDEX(प्रवेश_मोल):
    फायल = 씨.c_void_p(); रेग = 씨.c_uint(); स्लॉट_प्रवेश = 씨.c_uint(); ऑफसॅट_मोल = 씨.c_uint()
    फायल_स्थिती_2aa21a9a(위치얻기(प्रवेश_मोल),씨.byref(फायल),씨.byref(रेग),씨.byref(स्लॉट_प्रवेश),씨.byref(ऑफसॅट_मोल))
    return (SMS(फायल_प्रवेश_नांव(फायल)) if फायल else '', ऑफसॅट_मोल.value, रेग.value)

def पाळो_दिवचो_आदेश():
    लूकअप_INDEX = तयार_करचें(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 अणकारप_स्त्रोत 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, प्रत्यक्ष_डेटा 빌드에서는 계속 컴파일한다.
    소유파일 = {str(पाथ.resolve()) for पाथ in प्रॉजॅक्ट_रूट.rglob('*') if पाथ.suffix in ('.c','.h','.cpp','.inc')
              and not set(पाथ.relative_to(प्रॉजॅक्ट_रूट).parts)&{'build','dist','vendor','__pycache__'}
              and पाथ.relative_to(प्रॉजॅक्ट_रूट).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(प्रॉजॅक्ट_रूट/'उपेगकर्तो'),
          '-I'+str(प्रॉजॅक्ट_रूट.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(प्रॉजॅक्ट_रूट/'build'),'-I'+str(प्रॉजॅक्ट_रूट/'build/user'),
          '-I'+str(प्रॉजॅक्ट_रूट/'build/remote'),'-I'+str(प्रॉजॅक्ट_रूट/'vendor/bearssl/inc'),
          '-I'+str(प्रॉजॅक्ट_रूट/'vendor/bearssl/src'),'-I'+str(प्रॉजॅक्ट_रूट/'vendor/libassh/src'),
          '-I'+str(प्रॉजॅक्ट_रूट/'vendor/lwip/src/include'),'-I'+str(प्रॉजॅक्ट_रूट/'नॅटवर्क_स्टॅक'),
          '-I'+str(प्रॉजॅक्ट_रूट/'दुर्मीळ_मोल'),'-I'+str(प्रॉजॅक्ट_रूट/'시언어번역기')]
    for पाथ in sorted(Path(नांव) for नांव in 소유파일 if नांव.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if पाथ.suffix=='.cpp' else '-std=c11']
        if 'नॅटवर्क_स्टॅक' in पाथ.parts: 인수 += ['-I'+str(प्रॉजॅक्ट_रूट/'नॅटवर्क_स्टॅक'),'-I'+str(प्रॉजॅक्ट_रूट/'vendor/lwip/src/include')]
        if '시언어번역기' in पाथ.parts:
            인수 += ['-I'+str(प्रॉजॅक्ट_रूट/'시언어번역기'),'-I'+str(प्रॉजॅक्ट_रूट/'vendor/tinycc'),'-I'+str(प्रॉजॅक्ट_रूट/'build/ccompiler'),
                    '-isystem',str(प्रॉजॅक्ट_रूट.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_ब्रिज' in पाथ.parts:
            인수 += ['-I'+str(प्रॉजॅक्ट_रूट/'PYTHON_ब्रिज'),'-I'+str(प्रॉजॅक्ट_रूट/'build/micropython-1.24.1'),'-I'+str(प्रॉजॅक्ट_रूट/'build/python'),'-isystem','/usr/include/newlib']
        if 'दुर्मीळ_मोल' in पाथ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in पाथ.parts: 인수 += ['-D__JKOROS__=1']
        if पाथ.name=='रास.c': 인수 += ['-I'+str(प्रॉजॅक्ट_रूट/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        गट_मोल = (씨.c_char_p*len(인수))(*[प्रवेश_मोल.encode() for प्रवेश_मोल in 인수])
        अणकार_एकक = 분석(लूकअप_INDEX,str(पाथ).encode(),गट_मोल,len(인수),None,0,1)
        for INDEX in range(진단수(अणकार_एकक)):
            진단 = 진단얻기(अणकार_एकक,INDEX)
            if कळोवणी_मोल(진단)>=3: 오류들.append((str(पाथ.relative_to(प्रॉजॅक्ट_रूट)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(प्रवेश_मोल,부모,डेटा):
            फायल,ऑफसॅट_मोल,रेग = स्थिती_INDEX(प्रवेश_मोल)
            if फायल not in 소유파일: return 2 if प्रवेश_मोल.종류==300 else 1
            낱말 = SMS(이름얻기(प्रवेश_मोल))
            if not 낱말 or any(ord(वर्ण_मोल)>127 for वर्ण_मोल in 낱말): return 2
            if प्रवेश_मोल.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_मोल = SMS(UNIQUE_नांव(प्रवेश_मोल)) or फायल+':'+str(ऑफसॅट_मोल)
                선언들[UNIQUE_मोल] = {'फायल':फायल,'ऑफसॅट_मोल':ऑफसॅट_मोल,'줄':रेग,'종류':प्रवेश_मोल.종류,'नांव':낱말,'कनॅक्ट':연결종류(प्रवेश_मोल)}
                참조들.append((फायल,ऑफसॅट_मोल,낱말,UNIQUE_मोल))
            else:
                संदर्भ = 참조얻기(प्रवेश_मोल)
                संदर्भ_फायल,_,_ = स्थिती_INDEX(संदर्भ)
                if संदर्भ_फायल in 소유파일:
                    UNIQUE_मोल = SMS(UNIQUE_नांव(संदर्भ)); 참조들.append((फायल,ऑफसॅट_मोल,SMS(이름얻기(संदर्भ)),UNIQUE_मोल))
            return 2
        방문(रूट_मोल(अणकार_एकक),살피기,None)
        सोडचें_एप्लिकेशन(अणकार_एकक)
    नियुक्त_स्थान_मोल = प्रॉजॅक्ट_रूट/'build/한국어화/시언어분석.json'
    नियुक्त_स्थान_मोल.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {फायल:hashlib.sha256(Path(फायल).read_bytes()).hexdigest() for फायल in sorted(소유파일)}
    नियुक्त_स्थान_मोल.write_text(json.dumps({'선언':선언들,'संदर्भ':참조들,'चूक':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'संदर्भ',len(참조들),'चूक',len(오류들))
    for चूक in 오류들: print(*चूक)

if __name__=='__main__': पाळो_दिवचो_आदेश()
