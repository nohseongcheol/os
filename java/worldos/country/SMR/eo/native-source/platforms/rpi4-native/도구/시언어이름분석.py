#!/usr/bin/env python3
"""libclang 선언·참조 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class 문자열(씨.Structure): _fields_ = [('자료',씨.c_void_p),('표시',씨.c_uint)]
class 커서(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('자료',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('자료',씨.c_void_p*2),('변위',씨.c_uint)]
def 함수(Nomo, 반환, *Argumentoj):
    항목 = getattr(구현, Nomo); 항목.restype = 반환; 항목.argtypes = list(Argumentoj); return 항목
글얻기 = 함수('clang_getCString',씨.c_char_p,문자열)
글해제 = 함수('clang_disposeString',None,문자열)
def Teksto(값):
    결과 = (글얻기(값) or b'').decode('utf-8'); 글해제(값); return 결과
이름얻기 = 함수('clang_getCursorSpelling',문자열,커서)
참조얻기 = 함수('clang_getCursorReferenced',커서,커서)
위치얻기 = 함수('clang_getCursorLocation',위치,커서)
파일위치 = 함수('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
파일이름 = 함수('clang_getFileName',문자열,씨.c_void_p)
고유이름 = 함수('clang_getCursorUSR',문자열,커서)
연결종류 = 함수('clang_getCursorLinkage',씨.c_uint,커서)
방문형 = 씨.CFUNCTYPE(씨.c_uint,커서,커서,씨.c_void_p)
방문 = 함수('clang_visitChildren',씨.c_uint,커서,방문형,씨.c_void_p)
생성 = 함수('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = 함수('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = 함수('clang_getTranslationUnitCursor',커서,씨.c_void_p)
끝내기 = 함수('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = 함수('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = 함수('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
심각도 = 함수('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = 함수('clang_getDiagnosticSpelling',문자열,씨.c_void_p)
진단해제 = 함수('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(항목):
    Dosiero = 씨.c_void_p(); Linio = 씨.c_uint(); 칸 = 씨.c_uint(); 변위 = 씨.c_uint()
    파일위치(위치얻기(항목),씨.byref(Dosiero),씨.byref(Linio),씨.byref(칸),씨.byref(변위))
    return (Teksto(파일이름(Dosiero)) if Dosiero else '', 변위.value, Linio.value)

def 실행():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 번역 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, 실제 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Vojo.resolve()) for Vojo in 기준.rglob('*') if Vojo.suffix in ('.c','.h','.cpp','.inc')
              and not set(Vojo.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and Vojo.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'사용자'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'통신망'),
          '-I'+str(기준/'원격'),'-I'+str(기준/'시언어번역기')]
    for Vojo in sorted(Path(Nomo) for Nomo in 소유파일 if Nomo.endswith(('.c','.cpp'))):
        Argumentoj = 공통 + ['-std=c++11' if Vojo.suffix=='.cpp' else '-std=c11']
        if '통신망' in Vojo.parts: Argumentoj += ['-I'+str(기준/'통신망'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in Vojo.parts:
            Argumentoj += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Vojo.parts:
            Argumentoj += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if '원격' in Vojo.parts:
            Argumentoj += ['-isystem', '/usr/include/newlib']
        if '배포' in Vojo.parts: Argumentoj += ['-D__JKOROS__=1']
        if Vojo.name=='꾸러미.c': Argumentoj += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        묶음 = (씨.c_char_p*len(Argumentoj))(*[항목.encode() for 항목 in Argumentoj])
        번역단위 = 분석(색인,str(Vojo).encode(),묶음,len(Argumentoj),None,0,1)
        for 번호 in range(진단수(번역단위)):
            진단 = 진단얻기(번역단위,번호)
            if 심각도(진단)>=3: 오류들.append((str(Vojo.relative_to(기준)),Teksto(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(항목,부모,자료):
            Dosiero,변위,Linio = 자리(항목)
            if Dosiero not in 소유파일: return 2 if 항목.종류==300 else 1
            낱말 = Teksto(이름얻기(항목))
            if not 낱말 or any(ord(글자)>127 for 글자 in 낱말): return 2
            if 항목.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = Teksto(고유이름(항목)) or Dosiero+':'+str(변위)
                선언들[고유] = {'Dosiero':Dosiero,'변위':변위,'Linio':Linio,'종류':항목.종류,'Nomo':낱말,'Konekti':연결종류(항목)}
                참조들.append((Dosiero,변위,낱말,고유))
            else:
                참조 = 참조얻기(항목)
                참조파일,_,_ = 자리(참조)
                if 참조파일 in 소유파일:
                    고유 = Teksto(고유이름(참조)); 참조들.append((Dosiero,변위,Teksto(이름얻기(참조)),고유))
            return 2
        방문(뿌리(번역단위),살피기,None)
        끝내기(번역단위)
    목적 = 기준/'build/한국어화/시언어분석.json'
    목적.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Dosiero:hashlib.sha256(Path(Dosiero).read_bytes()).hexdigest() for Dosiero in sorted(소유파일)}
    목적.write_text(json.dumps({'선언':선언들,'참조':참조들,'eraro':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'참조',len(참조들),'eraro',len(오류들))
    for eraro in 오류들: print(*eraro)

if __name__=='__main__': 실행()
