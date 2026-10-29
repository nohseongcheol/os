#!/usr/bin/env python3
"""libclang 선언·참조 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ɓoggol_njaru(씨.Structure): _fields_ = [('keɓe',씨.c_void_p),('hollirde_njaru',씨.c_uint)]
class kirseer_njaru(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('keɓe',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('keɓe',씨.c_void_p*2),('변위',씨.c_uint)]
def juɓɓol_njaru(innde, 반환, *인수):
    naatnugol_njaru = getattr(구현, innde); naatnugol_njaru.restype = 반환; naatnugol_njaru.argtypes = list(인수); return naatnugol_njaru
글얻기 = juɓɓol_njaru('clang_getCString',씨.c_char_p,ɓoggol_njaru)
글해제 = juɓɓol_njaru('clang_disposeString',None,ɓoggol_njaru)
def binndi(njaru):
    결과 = (글얻기(njaru) or b'').decode('utf-8'); 글해제(njaru); return 결과
이름얻기 = juɓɓol_njaru('clang_getCursorSpelling',ɓoggol_njaru,kirseer_njaru)
참조얻기 = juɓɓol_njaru('clang_getCursorReferenced',kirseer_njaru,kirseer_njaru)
위치얻기 = juɓɓol_njaru('clang_getCursorLocation',위치,kirseer_njaru)
파일위치 = juɓɓol_njaru('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fiilde_naatnugol_innde = juɓɓol_njaru('clang_getFileName',ɓoggol_njaru,씨.c_void_p)
고유이름 = juɓɓol_njaru('clang_getCursorUSR',ɓoggol_njaru,kirseer_njaru)
연결종류 = juɓɓol_njaru('clang_getCursorLinkage',씨.c_uint,kirseer_njaru)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kirseer_njaru,kirseer_njaru,씨.c_void_p)
방문 = juɓɓol_njaru('clang_visitChildren',씨.c_uint,kirseer_njaru,방문형,씨.c_void_p)
생성 = juɓɓol_njaru('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = juɓɓol_njaru('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = juɓɓol_njaru('clang_getTranslationUnitCursor',kirseer_njaru,씨.c_void_p)
끝내기 = juɓɓol_njaru('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = juɓɓol_njaru('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = juɓɓol_njaru('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
kittugol_njaru = juɓɓol_njaru('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = juɓɓol_njaru('clang_getDiagnosticSpelling',ɓoggol_njaru,씨.c_void_p)
진단해제 = juɓɓol_njaru('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(naatnugol_njaru):
    fiilde = 씨.c_void_p(); diidol = 씨.c_uint(); 칸 = 씨.c_uint(); 변위 = 씨.c_uint()
    파일위치(위치얻기(naatnugol_njaru),씨.byref(fiilde),씨.byref(diidol),씨.byref(칸),씨.byref(변위))
    return (binndi(fiilde_naatnugol_innde(fiilde)) if fiilde else '', 변위.value, diidol.value)

def 실행():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 번역 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, laatii_keɓe 빌드에서는 계속 컴파일한다.
    소유파일 = {str(laawol.resolve()) for laawol in 기준.rglob('*') if laawol.suffix in ('.c','.h','.cpp','.inc')
              and not set(laawol.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and laawol.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'kuutoro'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'통신망'),
          '-I'+str(기준/'원격'),'-I'+str(기준/'시언어번역기')]
    for laawol in sorted(Path(innde) for innde in 소유파일 if innde.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if laawol.suffix=='.cpp' else '-std=c11']
        if '통신망' in laawol.parts: 인수 += ['-I'+str(기준/'통신망'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in laawol.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in laawol.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if '원격' in laawol.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in laawol.parts: 인수 += ['-D__JKOROS__=1']
        if laawol.name=='꾸러미.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        seto_njaru = (씨.c_char_p*len(인수))(*[naatnugol_njaru.encode() for naatnugol_njaru in 인수])
        번역단위 = 분석(색인,str(laawol).encode(),seto_njaru,len(인수),None,0,1)
        for joopirdu in range(진단수(번역단위)):
            진단 = 진단얻기(번역단위,joopirdu)
            if kittugol_njaru(진단)>=3: 오류들.append((str(laawol.relative_to(기준)),binndi(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(naatnugol_njaru,부모,keɓe):
            fiilde,변위,diidol = 자리(naatnugol_njaru)
            if fiilde not in 소유파일: return 2 if naatnugol_njaru.종류==300 else 1
            낱말 = binndi(이름얻기(naatnugol_njaru))
            if not 낱말 or any(ord(alkulal_njaru)>127 for alkulal_njaru in 낱말): return 2
            if naatnugol_njaru.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = binndi(고유이름(naatnugol_njaru)) or fiilde+':'+str(변위)
                선언들[고유] = {'fiilde':fiilde,'변위':변위,'줄':diidol,'종류':naatnugol_njaru.종류,'innde':낱말,'seŋaade':연결종류(naatnugol_njaru)}
                참조들.append((fiilde,변위,낱말,고유))
            else:
                참조 = 참조얻기(naatnugol_njaru)
                참조파일,_,_ = 자리(참조)
                if 참조파일 in 소유파일:
                    고유 = binndi(고유이름(참조)); 참조들.append((fiilde,변위,binndi(이름얻기(참조)),고유))
            return 2
        방문(뿌리(번역단위),살피기,None)
        끝내기(번역단위)
    tiindaare_njaru = 기준/'build/한국어화/시언어분석.json'
    tiindaare_njaru.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {fiilde:hashlib.sha256(Path(fiilde).read_bytes()).hexdigest() for fiilde in sorted(소유파일)}
    tiindaare_njaru.write_text(json.dumps({'선언':선언들,'참조':참조들,'juumre':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'참조',len(참조들),'juumre',len(오류들))
    for juumre in 오류들: print(*juumre)

if __name__=='__main__': 실행()
