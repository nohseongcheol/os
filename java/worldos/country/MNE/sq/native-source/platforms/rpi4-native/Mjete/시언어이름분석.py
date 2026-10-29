#!/usr/bin/env python3
"""libclang deklarata·Referencë 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_rrënjë = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class varg_VALUE(씨.Structure): _fields_ = [('të_dhëna',씨.c_void_p),('shfaq_VALUE',씨.c_uint)]
class kursor_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('të_dhëna',씨.c_void_p*3)]
class Pozicioni(씨.Structure): _fields_ = [('të_dhëna',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def FUNCTION_VALUE(Emër, Kthe_llogaritje, *Argumente):
    futje_VALUE = getattr(구현, Emër); futje_VALUE.restype = Kthe_llogaritje; futje_VALUE.argtypes = list(Argumente); return futje_VALUE
marr_SMS = FUNCTION_VALUE('clang_getCString',씨.c_char_p,varg_VALUE)
liroj_SMS = FUNCTION_VALUE('clang_disposeString',None,varg_VALUE)
def Teksti(VALUE):
    llogaritje = (marr_SMS(VALUE) or b'').decode('utf-8'); liroj_SMS(VALUE); return llogaritje
marr_emër = FUNCTION_VALUE('clang_getCursorSpelling',varg_VALUE,kursor_VALUE)
marr_Referencë = FUNCTION_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
marr_pozicioni = FUNCTION_VALUE('clang_getCursorLocation',Pozicioni,kursor_VALUE)
skedar_pozicioni = FUNCTION_VALUE('clang_getFileLocation',None,Pozicioni,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
skedar_futje_emër = FUNCTION_VALUE('clang_getFileName',varg_VALUE,씨.c_void_p)
UNIQUE_emër = FUNCTION_VALUE('clang_getCursorUSR',varg_VALUE,kursor_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,kursor_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kursor_VALUE,kursor_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,kursor_VALUE,방문형,씨.c_void_p)
gjeneroj = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
rrënjë_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,씨.c_void_p)
mbyll_program = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
rëndësia_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',varg_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def pozicioni_INDEX(futje_VALUE):
    Kartelë = 씨.c_void_p(); linjë = 씨.c_uint(); hapësirë_për_tekst_futje = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    skedar_pozicioni(marr_pozicioni(futje_VALUE),씨.byref(Kartelë),씨.byref(linjë),씨.byref(hapësirë_për_tekst_futje),씨.byref(OFFSET_VALUE))
    return (Teksti(skedar_futje_emër(Kartelë)) if Kartelë else '', OFFSET_VALUE.value, linjë.value)

def zbatoj_komandë():
    LOOKUP_INDEX = gjeneroj(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 deklarata 없이 TinyCC 외부 단일 Përkthe_burim 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, aktual_të_dhëna 빌드에서는 계속 컴파일한다.
    소유파일 = {str(POZICIONI.resolve()) for POZICIONI in Project_rrënjë.rglob('*') if POZICIONI.suffix in ('.c','.h','.cpp','.inc')
              and not set(POZICIONI.relative_to(Project_rrënjë).parts)&{'build','dist','vendor','__pycache__'}
              and POZICIONI.relative_to(Project_rrënjë).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_rrënjë/'përdorues'),
          '-I'+str(Project_rrënjë.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_rrënjë/'build'),'-I'+str(Project_rrënjë/'build/user'),
          '-I'+str(Project_rrënjë/'build/remote'),'-I'+str(Project_rrënjë/'vendor/bearssl/inc'),
          '-I'+str(Project_rrënjë/'vendor/bearssl/src'),'-I'+str(Project_rrënjë/'vendor/libassh/src'),
          '-I'+str(Project_rrënjë/'vendor/lwip/src/include'),'-I'+str(Project_rrënjë/'rrjet_Stivë'),
          '-I'+str(Project_rrënjë/'në_largësi_VALUE'),'-I'+str(Project_rrënjë/'시언어번역기')]
    for POZICIONI in sorted(Path(Emër) for Emër in 소유파일 if Emër.endswith(('.c','.cpp'))):
        Argumente = 공통 + ['-std=c++11' if POZICIONI.suffix=='.cpp' else '-std=c11']
        if 'rrjet_Stivë' in POZICIONI.parts: Argumente += ['-I'+str(Project_rrënjë/'rrjet_Stivë'),'-I'+str(Project_rrënjë/'vendor/lwip/src/include')]
        if '시언어번역기' in POZICIONI.parts:
            Argumente += ['-I'+str(Project_rrënjë/'시언어번역기'),'-I'+str(Project_rrënjë/'vendor/tinycc'),'-I'+str(Project_rrënjë/'build/ccompiler'),
                    '-isystem',str(Project_rrënjë.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_urë' in POZICIONI.parts:
            Argumente += ['-I'+str(Project_rrënjë/'PYTHON_urë'),'-I'+str(Project_rrënjë/'build/micropython-1.24.1'),'-I'+str(Project_rrënjë/'build/python'),'-isystem','/usr/include/newlib']
        if 'në_largësi_VALUE' in POZICIONI.parts:
            Argumente += ['-isystem', '/usr/include/newlib']
        if '배포' in POZICIONI.parts: Argumente += ['-D__JKOROS__=1']
        if POZICIONI.name=='grupoj.c': Argumente += ['-I'+str(Project_rrënjë/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        grup_VALUE = (씨.c_char_p*len(Argumente))(*[futje_VALUE.encode() for futje_VALUE in Argumente])
        Përkthimi_mësim = 분석(LOOKUP_INDEX,str(POZICIONI).encode(),grup_VALUE,len(Argumente),None,0,1)
        for INDEX in range(진단수(Përkthimi_mësim)):
            진단 = 진단얻기(Përkthimi_mësim,INDEX)
            if rëndësia_VALUE(진단)>=3: 오류들.append((str(POZICIONI.relative_to(Project_rrënjë)),Teksti(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(futje_VALUE,부모,të_dhëna):
            Kartelë,OFFSET_VALUE,linjë = pozicioni_INDEX(futje_VALUE)
            if Kartelë not in 소유파일: return 2 if futje_VALUE.종류==300 else 1
            낱말 = Teksti(marr_emër(futje_VALUE))
            if not 낱말 or any(ord(karakter_VALUE)>127 for karakter_VALUE in 낱말): return 2
            if futje_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Teksti(UNIQUE_emër(futje_VALUE)) or Kartelë+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Kartelë':Kartelë,'OFFSET_VALUE':OFFSET_VALUE,'줄':linjë,'종류':futje_VALUE.종류,'Emër':낱말,'Lidhu':연결종류(futje_VALUE)}
                참조들.append((Kartelë,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Referencë = marr_Referencë(futje_VALUE)
                Referencë_skedar,_,_ = pozicioni_INDEX(Referencë)
                if Referencë_skedar in 소유파일:
                    UNIQUE_VALUE = Teksti(UNIQUE_emër(Referencë)); 참조들.append((Kartelë,OFFSET_VALUE,Teksti(marr_emër(Referencë)),UNIQUE_VALUE))
            return 2
        방문(rrënjë_VALUE(Përkthimi_mësim),살피기,None)
        mbyll_program(Përkthimi_mësim)
    vendmbërritje_VALUE = Project_rrënjë/'build/한국어화/시언어분석.json'
    vendmbërritje_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Kartelë:hashlib.sha256(Path(Kartelë).read_bytes()).hexdigest() for Kartelë in sorted(소유파일)}
    vendmbërritje_VALUE.write_text(json.dumps({'deklarata':선언들,'Referencë':참조들,'GABIM':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklarata',len(선언들),'Referencë',len(참조들),'GABIM',len(오류들))
    for GABIM in 오류들: print(*GABIM)

if __name__=='__main__': zbatoj_komandë()
