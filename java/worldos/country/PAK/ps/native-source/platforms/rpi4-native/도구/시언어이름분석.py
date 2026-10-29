#!/usr/bin/env python3
"""libclang 선언·참조 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class مزى_ارزښت_6ca8363c(씨.Structure): _fields_ = [('اومتوک',씨.c_void_p),('표시',씨.c_uint)]
class ځرى_ارزښت(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('اومتوک',씨.c_void_p*3)]
class ځای(씨.Structure): _fields_ = [('اومتوک',씨.c_void_p*2),('변위',씨.c_uint)]
def 함수(نوم, 반환, *인수):
    ننوت_ارزښت = getattr(구현, نوم); ننوت_ارزښت.restype = 반환; ننوت_ارزښت.argtypes = list(인수); return ننوت_ارزښت
글얻기 = 함수('clang_getCString',씨.c_char_p,مزى_ارزښت_6ca8363c)
글해제 = 함수('clang_disposeString',None,مزى_ارزښت_6ca8363c)
def ليکنه(ارزښت):
    결과 = (글얻기(ارزښت) or b'').decode('utf-8'); 글해제(ارزښت); return 결과
이름얻기 = 함수('clang_getCursorSpelling',مزى_ارزښت_6ca8363c,ځرى_ارزښت)
참조얻기 = 함수('clang_getCursorReferenced',ځرى_ارزښت,ځرى_ارزښت)
위치얻기 = 함수('clang_getCursorLocation',ځای,ځرى_ارزښت)
파일위치 = 함수('clang_getFileLocation',None,ځای,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
파일이름 = 함수('clang_getFileName',مزى_ارزښت_6ca8363c,씨.c_void_p)
고유이름 = 함수('clang_getCursorUSR',مزى_ارزښت_6ca8363c,ځرى_ارزښت)
연결종류 = 함수('clang_getCursorLinkage',씨.c_uint,ځرى_ارزښت)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ځرى_ارزښت,ځرى_ارزښت,씨.c_void_p)
방문 = 함수('clang_visitChildren',씨.c_uint,ځرى_ارزښت,방문형,씨.c_void_p)
생성 = 함수('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = 함수('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = 함수('clang_getTranslationUnitCursor',ځرى_ارزښت,씨.c_void_p)
끝내기 = 함수('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = 함수('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = 함수('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
심각도 = 함수('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = 함수('clang_getDiagnosticSpelling',مزى_ارزښت_6ca8363c,씨.c_void_p)
진단해제 = 함수('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(ننوت_ارزښت):
    دوتنه = 씨.c_void_p(); ليکه = 씨.c_uint(); 칸 = 씨.c_uint(); 변위 = 씨.c_uint()
    파일위치(위치얻기(ننوت_ارزښت),씨.byref(دوتنه),씨.byref(ليکه),씨.byref(칸),씨.byref(변위))
    return (ليکنه(파일이름(دوتنه)) if دوتنه else '', 변위.value, ليکه.value)

def 실행():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 번역 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, 실제 빌드에서는 계속 컴파일한다.
    소유파일 = {str(يونلور.resolve()) for يونلور in 기준.rglob('*') if يونلور.suffix in ('.c','.h','.cpp','.inc')
              and not set(يونلور.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and يونلور.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'کارن'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'통신망'),
          '-I'+str(기준/'원격'),'-I'+str(기준/'시언어번역기')]
    for يونلور in sorted(Path(نوم) for نوم in 소유파일 if نوم.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if يونلور.suffix=='.cpp' else '-std=c11']
        if '통신망' in يونلور.parts: 인수 += ['-I'+str(기준/'통신망'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in يونلور.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in يونلور.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if '원격' in يونلور.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in يونلور.parts: 인수 += ['-D__JKOROS__=1']
        if يونلور.name=='꾸러미.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ډله_ارزښت = (씨.c_char_p*len(인수))(*[ننوت_ارزښت.encode() for ننوت_ارزښت in 인수])
        번역단위 = 분석(색인,str(يونلور).encode(),ډله_ارزښت,len(인수),None,0,1)
        for لړیال in range(진단수(번역단위)):
            진단 = 진단얻기(번역단위,لړیال)
            if 심각도(진단)>=3: 오류들.append((str(يونلور.relative_to(기준)),ليکنه(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ننوت_ارزښت,부모,اومتوک):
            دوتنه,변위,ليکه = 자리(ننوت_ارزښت)
            if دوتنه not in 소유파일: return 2 if ننوت_ارزښت.종류==300 else 1
            낱말 = ليکنه(이름얻기(ننوت_ارزښت))
            if not 낱말 or any(ord(لوښه_ارزښت)>127 for لوښه_ارزښت in 낱말): return 2
            if ننوت_ارزښت.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ليکنه(고유이름(ننوت_ارزښت)) or دوتنه+':'+str(변위)
                선언들[고유] = {'دوتنه':دوتنه,'변위':변위,'줄':ليکه,'종류':ننوت_ارزښت.종류,'نوم':낱말,'نښلېدل':연결종류(ننوت_ارزښت)}
                참조들.append((دوتنه,변위,낱말,고유))
            else:
                참조 = 참조얻기(ننوت_ارزښت)
                참조파일,_,_ = 자리(참조)
                if 참조파일 in 소유파일:
                    고유 = ليکنه(고유이름(참조)); 참조들.append((دوتنه,변위,ليکنه(이름얻기(참조)),고유))
            return 2
        방문(뿌리(번역단위),살피기,None)
        끝내기(번역단위)
    موخه_ارزښت = 기준/'build/한국어화/시언어분석.json'
    موخه_ارزښت.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {دوتنه:hashlib.sha256(Path(دوتنه).read_bytes()).hexdigest() for دوتنه in sorted(소유파일)}
    موخه_ارزښت.write_text(json.dumps({'선언':선언들,'참조':참조들,'تېروتنه':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'참조',len(참조들),'تېروتنه',len(오류들))
    for تېروتنه in 오류들: print(*تېروتنه)

if __name__=='__main__': 실행()
