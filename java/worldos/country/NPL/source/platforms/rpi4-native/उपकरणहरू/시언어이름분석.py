#!/usr/bin/env python3
"""libclang 선언·निर्देश 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

परियोजना_रूट = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class स्ट्रिङ_मान(씨.Structure): _fields_ = [('लगत',씨.c_void_p),('शो_मान',씨.c_uint)]
class कर्सर_मान(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('लगत',씨.c_void_p*3)]
class स्थिति(씨.Structure): _fields_ = [('लगत',씨.c_void_p*2),('अफसेट_मान',씨.c_uint)]
def प्रकार्य_मान(नाम, 반환, *तर्क):
    प्रविष्टि_मान = getattr(구현, नाम); प्रविष्टि_मान.restype = 반환; प्रविष्टि_मान.argtypes = list(तर्क); return प्रविष्टि_मान
글얻기 = प्रकार्य_मान('clang_getCString',씨.c_char_p,स्ट्रिङ_मान)
जारी_पाठ = प्रकार्य_मान('clang_disposeString',None,स्ट्रिङ_मान)
def पाठ(मान):
    मापन = (글얻기(मान) or b'').decode('utf-8'); जारी_पाठ(मान); return मापन
이름얻기 = प्रकार्य_मान('clang_getCursorSpelling',स्ट्रिङ_मान,कर्सर_मान)
참조얻기 = प्रकार्य_मान('clang_getCursorReferenced',कर्सर_मान,कर्सर_मान)
위치얻기 = प्रकार्य_मान('clang_getCursorLocation',स्थिति,कर्सर_मान)
फाइल_राख्नुहोस् = प्रकार्य_मान('clang_getFileLocation',None,स्थिति,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
फाइल_प्रविष्टि_नाम = प्रकार्य_मान('clang_getFileName',स्ट्रिङ_मान,씨.c_void_p)
고유이름 = प्रकार्य_मान('clang_getCursorUSR',स्ट्रिङ_मान,कर्सर_मान)
연결종류 = प्रकार्य_मान('clang_getCursorLinkage',씨.c_uint,कर्सर_मान)
방문형 = 씨.CFUNCTYPE(씨.c_uint,कर्सर_मान,कर्सर_मान,씨.c_void_p)
방문 = प्रकार्य_मान('clang_visitChildren',씨.c_uint,कर्सर_मान,방문형,씨.c_void_p)
सिर्जना_गर्नुहोस् = प्रकार्य_मान('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = प्रकार्य_मान('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
रूट_मान = प्रकार्य_मान('clang_getTranslationUnitCursor',कर्सर_मान,씨.c_void_p)
बाहिरिनुहोस्_अनुप्रयोग = प्रकार्य_मान('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = प्रकार्य_मान('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = प्रकार्य_मान('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
उग्रता_मान = प्रकार्य_मान('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = प्रकार्य_मान('clang_getDiagnosticSpelling',स्ट्रिङ_मान,씨.c_void_p)
진단해제 = प्रकार्य_मान('clang_disposeDiagnostic',None,씨.c_void_p)

def राख्नुहोस्_अनुक्रमणिका(प्रविष्टि_मान):
    फाइल = 씨.c_void_p(); रेखा = 씨.c_uint(); स्लट_प्रविष्टि = 씨.c_uint(); अफसेट_मान = 씨.c_uint()
    फाइल_राख्नुहोस्(위치얻기(प्रविष्टि_मान),씨.byref(फाइल),씨.byref(रेखा),씨.byref(स्लट_प्रविष्टि),씨.byref(अफसेट_मान))
    return (पाठ(फाइल_प्रविष्टि_नाम(फाइल)) if फाइल else '', अफसेट_मान.value, रेखा.value)

def कार्यान्वयन_गर्नुहोस्_आदेश():
    विवरण_हेर्ने_सुविधा_अनुक्रमणिका = सिर्जना_गर्नुहोस्(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 निज 선언 없이 TinyCC 외부 단일 अनुवाद_स्रोत 단위만 포함한다.
    # 외부 선언을 निज 이름으로 세지 않으며, वास्तविक_लगत 빌드에서는 계속 컴파일한다.
    소유파일 = {str(मार्ग.resolve()) for मार्ग in परियोजना_रूट.rglob('*') if मार्ग.suffix in ('.c','.h','.cpp','.inc')
              and not set(मार्ग.relative_to(परियोजना_रूट).parts)&{'build','dist','vendor','__pycache__'}
              and मार्ग.relative_to(परियोजना_रूट).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(परियोजना_रूट/'प्रयोगकर्ता'),
          '-I'+str(परियोजना_रूट.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(परियोजना_रूट/'build'),'-I'+str(परियोजना_रूट/'build/user'),
          '-I'+str(परियोजना_रूट/'build/remote'),'-I'+str(परियोजना_रूट/'vendor/bearssl/inc'),
          '-I'+str(परियोजना_रूट/'vendor/bearssl/src'),'-I'+str(परियोजना_रूट/'vendor/libassh/src'),
          '-I'+str(परियोजना_रूट/'vendor/lwip/src/include'),'-I'+str(परियोजना_रूट/'सञ्जाल_चाङ'),
          '-I'+str(परियोजना_रूट/'दूर_मान'),'-I'+str(परियोजना_रूट/'시언어번역기')]
    for मार्ग in sorted(Path(नाम) for नाम in 소유파일 if नाम.endswith(('.c','.cpp'))):
        तर्क = 공통 + ['-std=c++11' if मार्ग.suffix=='.cpp' else '-std=c11']
        if 'सञ्जाल_चाङ' in मार्ग.parts: तर्क += ['-I'+str(परियोजना_रूट/'सञ्जाल_चाङ'),'-I'+str(परियोजना_रूट/'vendor/lwip/src/include')]
        if '시언어번역기' in मार्ग.parts:
            तर्क += ['-I'+str(परियोजना_रूट/'시언어번역기'),'-I'+str(परियोजना_रूट/'vendor/tinycc'),'-I'+str(परियोजना_रूट/'build/ccompiler'),
                    '-isystem',str(परियोजना_रूट.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in मार्ग.parts:
            तर्क += ['-I'+str(परियोजना_रूट/'파이썬연결'),'-I'+str(परियोजना_रूट/'build/micropython-1.24.1'),'-I'+str(परियोजना_रूट/'build/python'),'-isystem','/usr/include/newlib']
        if 'दूर_मान' in मार्ग.parts:
            तर्क += ['-isystem', '/usr/include/newlib']
        if '배포' in मार्ग.parts: तर्क += ['-D__JKOROS__=1']
        if मार्ग.name=='पोको.c': तर्क += ['-I'+str(परियोजना_रूट/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        समूह_मान = (씨.c_char_p*len(तर्क))(*[प्रविष्टि_मान.encode() for प्रविष्टि_मान in तर्क])
        अनुवाद_शिक्षा = 분석(विवरण_हेर्ने_सुविधा_अनुक्रमणिका,str(मार्ग).encode(),समूह_मान,len(तर्क),None,0,1)
        for अनुक्रमणिका in range(진단수(अनुवाद_शिक्षा)):
            진단 = 진단얻기(अनुवाद_शिक्षा,अनुक्रमणिका)
            if उग्रता_मान(진단)>=3: 오류들.append((str(मार्ग.relative_to(परियोजना_रूट)),पाठ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(प्रविष्टि_मान,부모,लगत):
            फाइल,अफसेट_मान,रेखा = राख्नुहोस्_अनुक्रमणिका(प्रविष्टि_मान)
            if फाइल not in 소유파일: return 2 if प्रविष्टि_मान.종류==300 else 1
            낱말 = पाठ(이름얻기(प्रविष्टि_मान))
            if not 낱말 or any(ord(वर्ण_मान)>127 for वर्ण_मान in 낱말): return 2
            if प्रविष्टि_मान.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = पाठ(고유이름(प्रविष्टि_मान)) or फाइल+':'+str(अफसेट_मान)
                선언들[고유] = {'फाइल':फाइल,'अफसेट_मान':अफसेट_मान,'줄':रेखा,'종류':प्रविष्टि_मान.종류,'नाम':낱말,'जडान':연결종류(प्रविष्टि_मान)}
                참조들.append((फाइल,अफसेट_मान,낱말,고유))
            else:
                निर्देश = 참조얻기(प्रविष्टि_मान)
                निर्देश_फाइल,_,_ = राख्नुहोस्_अनुक्रमणिका(निर्देश)
                if निर्देश_फाइल in 소유파일:
                    고유 = पाठ(고유이름(निर्देश)); 참조들.append((फाइल,अफसेट_मान,पाठ(이름얻기(निर्देश)),고유))
            return 2
        방문(रूट_मान(अनुवाद_शिक्षा),살피기,None)
        बाहिरिनुहोस्_अनुप्रयोग(अनुवाद_शिक्षा)
    गन्तव्य_मान = परियोजना_रूट/'build/한국어화/시언어분석.json'
    गन्तव्य_मान.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {फाइल:hashlib.sha256(Path(फाइल).read_bytes()).hexdigest() for फाइल in sorted(소유파일)}
    गन्तव्य_मान.write_text(json.dumps({'선언':선언들,'निर्देश':참조들,'त्रुटि':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'निर्देश',len(참조들),'त्रुटि',len(오류들))
    for त्रुटि in 오류들: print(*त्रुटि)

if __name__=='__main__': कार्यान्वयन_गर्नुहोस्_आदेश()
