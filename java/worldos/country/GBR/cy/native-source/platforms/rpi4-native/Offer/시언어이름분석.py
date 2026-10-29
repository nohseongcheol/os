#!/usr/bin/env python3
"""libclang 선언·cyfeiriad 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

prosiect_gwraidd = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class testun_VALUE(씨.Structure): _fields_ = [('data',씨.c_void_p),('sioe_VALUE',씨.c_uint)]
class cyrchwr_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class safle(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def SWYDDOGAETH_VALUE(Enw, return_mesur, *인수):
    cofnod_VALUE = getattr(구현, Enw); cofnod_VALUE.restype = return_mesur; cofnod_VALUE.argtypes = list(인수); return cofnod_VALUE
글얻기 = SWYDDOGAETH_VALUE('clang_getCString',씨.c_char_p,testun_VALUE)
rhyddhau_SMS = SWYDDOGAETH_VALUE('clang_disposeString',None,testun_VALUE)
def Testun(VALUE):
    mesur = (글얻기(VALUE) or b'').decode('utf-8'); rhyddhau_SMS(VALUE); return mesur
이름얻기 = SWYDDOGAETH_VALUE('clang_getCursorSpelling',testun_VALUE,cyrchwr_VALUE)
참조얻기 = SWYDDOGAETH_VALUE('clang_getCursorReferenced',cyrchwr_VALUE,cyrchwr_VALUE)
위치얻기 = SWYDDOGAETH_VALUE('clang_getCursorLocation',safle,cyrchwr_VALUE)
ffeil_safle = SWYDDOGAETH_VALUE('clang_getFileLocation',None,safle,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ffeil_cofnod_enw = SWYDDOGAETH_VALUE('clang_getFileName',testun_VALUE,씨.c_void_p)
UNIQUE_enw = SWYDDOGAETH_VALUE('clang_getCursorUSR',testun_VALUE,cyrchwr_VALUE)
연결종류 = SWYDDOGAETH_VALUE('clang_getCursorLinkage',씨.c_uint,cyrchwr_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,cyrchwr_VALUE,cyrchwr_VALUE,씨.c_void_p)
방문 = SWYDDOGAETH_VALUE('clang_visitChildren',씨.c_uint,cyrchwr_VALUE,방문형,씨.c_void_p)
cynhyrchu = SWYDDOGAETH_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
Dadansoddi_VALUE = SWYDDOGAETH_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
gwraidd_VALUE = SWYDDOGAETH_VALUE('clang_getTranslationUnitCursor',cyrchwr_VALUE,씨.c_void_p)
gadael_Rhaglen_55b3a1cd = SWYDDOGAETH_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = SWYDDOGAETH_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = SWYDDOGAETH_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
difrifoldeb_VALUE = SWYDDOGAETH_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = SWYDDOGAETH_VALUE('clang_getDiagnosticSpelling',testun_VALUE,씨.c_void_p)
진단해제 = SWYDDOGAETH_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def safle_INDEX(cofnod_VALUE):
    Ffeil = 씨.c_void_p(); llinell = 씨.c_uint(); slot_cofnod = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    ffeil_safle(위치얻기(cofnod_VALUE),씨.byref(Ffeil),씨.byref(llinell),씨.byref(slot_cofnod),씨.byref(OFFSET_VALUE))
    return (Testun(ffeil_cofnod_enw(Ffeil)) if Ffeil else '', OFFSET_VALUE.value, llinell.value)

def Gweithredu_gorchymyn():
    LOOKUP_INDEX = cynhyrchu(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Cyfieithu_ffynhonnell 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, go_iawn_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(LLWYBR.resolve()) for LLWYBR in prosiect_gwraidd.rglob('*') if LLWYBR.suffix in ('.c','.h','.cpp','.inc')
              and not set(LLWYBR.relative_to(prosiect_gwraidd).parts)&{'build','dist','vendor','__pycache__'}
              and LLWYBR.relative_to(prosiect_gwraidd).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(prosiect_gwraidd/'defnyddiwr'),
          '-I'+str(prosiect_gwraidd.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(prosiect_gwraidd/'build'),'-I'+str(prosiect_gwraidd/'build/user'),
          '-I'+str(prosiect_gwraidd/'build/remote'),'-I'+str(prosiect_gwraidd/'vendor/bearssl/inc'),
          '-I'+str(prosiect_gwraidd/'vendor/bearssl/src'),'-I'+str(prosiect_gwraidd/'vendor/libassh/src'),
          '-I'+str(prosiect_gwraidd/'vendor/lwip/src/include'),'-I'+str(prosiect_gwraidd/'Rhwydwaith_pentwr'),
          '-I'+str(prosiect_gwraidd/'pell_VALUE'),'-I'+str(prosiect_gwraidd/'시언어번역기')]
    for LLWYBR in sorted(Path(Enw) for Enw in 소유파일 if Enw.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if LLWYBR.suffix=='.cpp' else '-std=c11']
        if 'Rhwydwaith_pentwr' in LLWYBR.parts: 인수 += ['-I'+str(prosiect_gwraidd/'Rhwydwaith_pentwr'),'-I'+str(prosiect_gwraidd/'vendor/lwip/src/include')]
        if '시언어번역기' in LLWYBR.parts:
            인수 += ['-I'+str(prosiect_gwraidd/'시언어번역기'),'-I'+str(prosiect_gwraidd/'vendor/tinycc'),'-I'+str(prosiect_gwraidd/'build/ccompiler'),
                    '-isystem',str(prosiect_gwraidd.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_pont' in LLWYBR.parts:
            인수 += ['-I'+str(prosiect_gwraidd/'PYTHON_pont'),'-I'+str(prosiect_gwraidd/'build/micropython-1.24.1'),'-I'+str(prosiect_gwraidd/'build/python'),'-isystem','/usr/include/newlib']
        if 'pell_VALUE' in LLWYBR.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in LLWYBR.parts: 인수 += ['-D__JKOROS__=1']
        if LLWYBR.name=='bwndel.c': 인수 += ['-I'+str(prosiect_gwraidd/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grŵp_VALUE = (씨.c_char_p*len(인수))(*[cofnod_VALUE.encode() for cofnod_VALUE in 인수])
        Cyfieithu_gwers = Dadansoddi_VALUE(LOOKUP_INDEX,str(LLWYBR).encode(),Grŵp_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Cyfieithu_gwers)):
            진단 = 진단얻기(Cyfieithu_gwers,INDEX)
            if difrifoldeb_VALUE(진단)>=3: 오류들.append((str(LLWYBR.relative_to(prosiect_gwraidd)),Testun(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(cofnod_VALUE,부모,data):
            Ffeil,OFFSET_VALUE,llinell = safle_INDEX(cofnod_VALUE)
            if Ffeil not in 소유파일: return 2 if cofnod_VALUE.종류==300 else 1
            낱말 = Testun(이름얻기(cofnod_VALUE))
            if not 낱말 or any(ord(nod_VALUE)>127 for nod_VALUE in 낱말): return 2
            if cofnod_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Testun(UNIQUE_enw(cofnod_VALUE)) or Ffeil+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Ffeil':Ffeil,'OFFSET_VALUE':OFFSET_VALUE,'줄':llinell,'종류':cofnod_VALUE.종류,'Enw':낱말,'Cysylltu':연결종류(cofnod_VALUE)}
                참조들.append((Ffeil,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                cyfeiriad = 참조얻기(cofnod_VALUE)
                cyfeiriad_ffeil,_,_ = safle_INDEX(cyfeiriad)
                if cyfeiriad_ffeil in 소유파일:
                    UNIQUE_VALUE = Testun(UNIQUE_enw(cyfeiriad)); 참조들.append((Ffeil,OFFSET_VALUE,Testun(이름얻기(cyfeiriad)),UNIQUE_VALUE))
            return 2
        방문(gwraidd_VALUE(Cyfieithu_gwers),살피기,None)
        gadael_Rhaglen_55b3a1cd(Cyfieithu_gwers)
    cyrchfan_VALUE = prosiect_gwraidd/'build/한국어화/시언어분석.json'
    cyrchfan_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Ffeil:hashlib.sha256(Path(Ffeil).read_bytes()).hexdigest() for Ffeil in sorted(소유파일)}
    cyrchfan_VALUE.write_text(json.dumps({'선언':선언들,'cyfeiriad':참조들,'Gwall':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'cyfeiriad',len(참조들),'Gwall',len(오류들))
    for Gwall in 오류들: print(*Gwall)

if __name__=='__main__': Gweithredu_gorchymyn()
