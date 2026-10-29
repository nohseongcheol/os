#!/usr/bin/env python3
"""libclang 선언·حوالو 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class اسٽرنگ_قدر(씨.Structure): _fields_ = [('ڪوائف',씨.c_void_p),('نمائش_ڪريو_قدر',씨.c_uint)]
class ڪرسر_قدر(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ڪوائف',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('ڪوائف',씨.c_void_p*2),('آف_سيٽ_قدر',씨.c_uint)]
def فعل_قدر(نالو, 반환, *인수):
    داخلا_قدر = getattr(구현, نالو); داخلا_قدر.restype = 반환; داخلا_قدر.argtypes = list(인수); return داخلا_قدر
글얻기 = فعل_قدر('clang_getCString',씨.c_char_p,اسٽرنگ_قدر)
جاري_ڪريو_متن = فعل_قدر('clang_disposeString',None,اسٽرنگ_قدر)
def متن(قدر):
    결과 = (글얻기(قدر) or b'').decode('utf-8'); جاري_ڪريو_متن(قدر); return 결과
이름얻기 = فعل_قدر('clang_getCursorSpelling',اسٽرنگ_قدر,ڪرسر_قدر)
참조얻기 = فعل_قدر('clang_getCursorReferenced',ڪرسر_قدر,ڪرسر_قدر)
위치얻기 = فعل_قدر('clang_getCursorLocation',위치,ڪرسر_قدر)
파일위치 = فعل_قدر('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
فائل_داخلا_نالو = فعل_قدر('clang_getFileName',اسٽرنگ_قدر,씨.c_void_p)
منفرد_نالو = فعل_قدر('clang_getCursorUSR',اسٽرنگ_قدر,ڪرسر_قدر)
연결종류 = فعل_قدر('clang_getCursorLinkage',씨.c_uint,ڪرسر_قدر)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ڪرسر_قدر,ڪرسر_قدر,씨.c_void_p)
방문 = فعل_قدر('clang_visitChildren',씨.c_uint,ڪرسر_قدر,방문형,씨.c_void_p)
생성 = فعل_قدر('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = فعل_قدر('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = فعل_قدر('clang_getTranslationUnitCursor',ڪرسر_قدر,씨.c_void_p)
끝내기 = فعل_قدر('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = فعل_قدر('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = فعل_قدر('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
شدت_قدر = فعل_قدر('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = فعل_قدر('clang_getDiagnosticSpelling',اسٽرنگ_قدر,씨.c_void_p)
진단해제 = فعل_قدر('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(داخلا_قدر):
    فائل = 씨.c_void_p(); لڪير = 씨.c_uint(); سوراخ_داخلا = 씨.c_uint(); آف_سيٽ_قدر = 씨.c_uint()
    파일위치(위치얻기(داخلا_قدر),씨.byref(فائل),씨.byref(لڪير),씨.byref(سوراخ_داخلا),씨.byref(آف_سيٽ_قدر))
    return (متن(فائل_داخلا_نالو(فائل)) if فائل else '', آف_سيٽ_قدر.value, لڪير.value)

def تعميل_ڪرڻ_حڪم():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 ترجمو_ماخذ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, اصلي_ڪوائف 빌드에서는 계속 컴파일한다.
    소유파일 = {str(راههه.resolve()) for راههه in 기준.rglob('*') if راههه.suffix in ('.c','.h','.cpp','.inc')
              and not set(راههه.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and راههه.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'صارف'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'نيٽ_ورڪ_اڀرڻ'),
          '-I'+str(기준/'بعيد_قدر'),'-I'+str(기준/'시언어번역기')]
    for راههه in sorted(Path(نالو) for نالو in 소유파일 if نالو.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if راههه.suffix=='.cpp' else '-std=c11']
        if 'نيٽ_ورڪ_اڀرڻ' in راههه.parts: 인수 += ['-I'+str(기준/'نيٽ_ورڪ_اڀرڻ'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in راههه.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in راههه.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'بعيد_قدر' in راههه.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in راههه.parts: 인수 += ['-D__JKOROS__=1']
        if راههه.name=='بنڊل.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        گروپ_قدر = (씨.c_char_p*len(인수))(*[داخلا_قدر.encode() for داخلا_قدر in 인수])
        ترجمو_سبق = 분석(색인,str(راههه).encode(),گروپ_قدر,len(인수),None,0,1)
        for ابتدائي in range(진단수(ترجمو_سبق)):
            진단 = 진단얻기(ترجمو_سبق,ابتدائي)
            if شدت_قدر(진단)>=3: 오류들.append((str(راههه.relative_to(기준)),متن(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(داخلا_قدر,부모,ڪوائف):
            فائل,آف_سيٽ_قدر,لڪير = 자리(داخلا_قدر)
            if فائل not in 소유파일: return 2 if داخلا_قدر.종류==300 else 1
            낱말 = متن(이름얻기(داخلا_قدر))
            if not 낱말 or any(ord(ڪريڪٽر_قدر)>127 for ڪريڪٽر_قدر in 낱말): return 2
            if داخلا_قدر.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                منفرد_قدر = متن(منفرد_نالو(داخلا_قدر)) or فائل+':'+str(آف_سيٽ_قدر)
                선언들[منفرد_قدر] = {'فائل':فائل,'آف_سيٽ_قدر':آف_سيٽ_قدر,'줄':لڪير,'종류':داخلا_قدر.종류,'نالو':낱말,'ڪنيڪٽ':연결종류(داخلا_قدر)}
                참조들.append((فائل,آف_سيٽ_قدر,낱말,منفرد_قدر))
            else:
                حوالو = 참조얻기(داخلا_قدر)
                حوالو_فائل,_,_ = 자리(حوالو)
                if حوالو_فائل in 소유파일:
                    منفرد_قدر = متن(منفرد_نالو(حوالو)); 참조들.append((فائل,آف_سيٽ_قدر,متن(이름얻기(حوالو)),منفرد_قدر))
            return 2
        방문(뿌리(ترجمو_سبق),살피기,None)
        끝내기(ترجمو_سبق)
    منزل_مقصود_قدر = 기준/'build/한국어화/시언어분석.json'
    منزل_مقصود_قدر.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {فائل:hashlib.sha256(Path(فائل).read_bytes()).hexdigest() for فائل in sorted(소유파일)}
    منزل_مقصود_قدر.write_text(json.dumps({'선언':선언들,'حوالو':참조들,'نقص':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'حوالو',len(참조들),'نقص',len(오류들))
    for نقص in 오류들: print(*نقص)

if __name__=='__main__': تعميل_ڪرڻ_حڪم()
