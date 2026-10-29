#!/usr/bin/env python3
"""libclang deklaracija·Gradiva 위치를 수집한다. zunanji_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_vir
import hashlib
import json
from pathlib import Path

pobuda_koren = Path(__file__).resolve().parents[1]
구현 = C_vir.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class niz_VALUE(C_vir.Structure): _fields_ = [('podatki',C_vir.c_void_p),('oddaja_VALUE_487749b8',C_vir.c_uint)]
class kazalec_VALUE(C_vir.Structure): _fields_ = [('종류',C_vir.c_uint),('보조',C_vir.c_int),('podatki',C_vir.c_void_p*3)]
class Položaj(C_vir.Structure): _fields_ = [('podatki',C_vir.c_void_p*2),('odmik_VALUE',C_vir.c_uint)]
def FUNCTION_VALUE(Ime, vrni_KR, *Argumenti):
    vnos_VALUE = getattr(구현, Ime); vnos_VALUE.restype = vrni_KR; vnos_VALUE.argtypes = list(Argumenti); return vnos_VALUE
dobiti_SMS = FUNCTION_VALUE('clang_getCString',C_vir.c_char_p,niz_VALUE)
izdaja_SMS = FUNCTION_VALUE('clang_disposeString',None,niz_VALUE)
def Besedilo(VALUE):
    REZULTAT = (dobiti_SMS(VALUE) or b'').decode('utf-8'); izdaja_SMS(VALUE); return REZULTAT
dobiti_ime = FUNCTION_VALUE('clang_getCursorSpelling',niz_VALUE,kazalec_VALUE)
dobiti_Gradiva = FUNCTION_VALUE('clang_getCursorReferenced',kazalec_VALUE,kazalec_VALUE)
dobiti_položaj = FUNCTION_VALUE('clang_getCursorLocation',Položaj,kazalec_VALUE)
Datoteka_položaj = FUNCTION_VALUE('clang_getFileLocation',None,Položaj,C_vir.POINTER(C_vir.c_void_p),C_vir.POINTER(C_vir.c_uint),C_vir.POINTER(C_vir.c_uint),C_vir.POINTER(C_vir.c_uint))
Datoteka_vnos_ime = FUNCTION_VALUE('clang_getFileName',niz_VALUE,C_vir.c_void_p)
UNIQUE_ime = FUNCTION_VALUE('clang_getCursorUSR',niz_VALUE,kazalec_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',C_vir.c_uint,kazalec_VALUE)
방문형 = C_vir.CFUNCTYPE(C_vir.c_uint,kazalec_VALUE,kazalec_VALUE,C_vir.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',C_vir.c_uint,kazalec_VALUE,방문형,C_vir.c_void_p)
ustvariti = FUNCTION_VALUE('clang_createIndex',C_vir.c_void_p,C_vir.c_int,C_vir.c_int)
analiza_VALUE = FUNCTION_VALUE('clang_parseTranslationUnit',C_vir.c_void_p,C_vir.c_void_p,C_vir.c_char_p,C_vir.POINTER(C_vir.c_char_p),C_vir.c_int,C_vir.c_void_p,C_vir.c_uint,C_vir.c_uint)
koren_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kazalec_VALUE,C_vir.c_void_p)
izhod_aplikacija = FUNCTION_VALUE('clang_disposeTranslationUnit',None,C_vir.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',C_vir.c_uint,C_vir.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',C_vir.c_void_p,C_vir.c_void_p,C_vir.c_uint)
resnost_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',C_vir.c_uint,C_vir.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',niz_VALUE,C_vir.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,C_vir.c_void_p)

def kazalec_mesta(vnos_VALUE):
    Datoteka = C_vir.c_void_p(); Črtni = C_vir.c_uint(); 칸 = C_vir.c_uint(); odmik_VALUE = C_vir.c_uint()
    Datoteka_položaj(dobiti_položaj(vnos_VALUE),C_vir.byref(Datoteka),C_vir.byref(Črtni),C_vir.byref(칸),C_vir.byref(odmik_VALUE))
    return (Besedilo(Datoteka_vnos_ime(Datoteka)) if Datoteka else '', odmik_VALUE.value, Črtni.value)

def Izvedi_ukaz():
    LOOKUP_INDEX = ustvariti(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # prevajalnik_orodje.c는 lastno deklaracija 없이 TinyCC zunanji_VALUE 단일 prevesti_vir 단위만 포함한다.
    # zunanji_VALUE 선언을 lastno 이름으로 세지 않으며, dejanski_podatki 빌드에서는 계속 컴파일한다.
    소유파일 = {str(POT.resolve()) for POT in pobuda_koren.rglob('*') if POT.suffix in ('.c','.h','.cpp','.inc')
              and not set(POT.relative_to(pobuda_koren).parts)&{'build','dist','vendor','__pycache__'}
              and POT.relative_to(pobuda_koren).as_posix() != 'C_prevajalnik/prevajalnik_orodje.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(pobuda_koren/'uporabnik'),
          '-I'+str(pobuda_koren.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(pobuda_koren/'build'),'-I'+str(pobuda_koren/'build/user'),
          '-I'+str(pobuda_koren/'build/remote'),'-I'+str(pobuda_koren/'vendor/bearssl/inc'),
          '-I'+str(pobuda_koren/'vendor/bearssl/src'),'-I'+str(pobuda_koren/'vendor/libassh/src'),
          '-I'+str(pobuda_koren/'vendor/lwip/src/include'),'-I'+str(pobuda_koren/'mreža_Sklad'),
          '-I'+str(pobuda_koren/'oddaljen_VALUE'),'-I'+str(pobuda_koren/'C_prevajalnik')]
    for POT in sorted(Path(Ime) for Ime in 소유파일 if Ime.endswith(('.c','.cpp'))):
        Argumenti = 공통 + ['-std=c++11' if POT.suffix=='.cpp' else '-std=c11']
        if 'mreža_Sklad' in POT.parts: Argumenti += ['-I'+str(pobuda_koren/'mreža_Sklad'),'-I'+str(pobuda_koren/'vendor/lwip/src/include')]
        if 'C_prevajalnik' in POT.parts:
            Argumenti += ['-I'+str(pobuda_koren/'C_prevajalnik'),'-I'+str(pobuda_koren/'vendor/tinycc'),'-I'+str(pobuda_koren/'build/ccompiler'),
                    '-isystem',str(pobuda_koren.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_most' in POT.parts:
            Argumenti += ['-I'+str(pobuda_koren/'PYTHON_most'),'-I'+str(pobuda_koren/'build/micropython-1.24.1'),'-I'+str(pobuda_koren/'build/python'),'-isystem','/usr/include/newlib']
        if 'oddaljen_VALUE' in POT.parts:
            Argumenti += ['-isystem', '/usr/include/newlib']
        if '배포' in POT.parts: Argumenti += ['-D__JKOROS__=1']
        if POT.name=='sveženj.c': Argumenti += ['-I'+str(pobuda_koren/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Skupina_VALUE = (C_vir.c_char_p*len(Argumenti))(*[vnos_VALUE.encode() for vnos_VALUE in Argumenti])
        Prevod_enota = analiza_VALUE(LOOKUP_INDEX,str(POT).encode(),Skupina_VALUE,len(Argumenti),None,0,1)
        for INDEX in range(진단수(Prevod_enota)):
            진단 = 진단얻기(Prevod_enota,INDEX)
            if resnost_VALUE(진단)>=3: 오류들.append((str(POT.relative_to(pobuda_koren)),Besedilo(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(vnos_VALUE,nadrejen_VALUE,podatki):
            Datoteka,odmik_VALUE,Črtni = kazalec_mesta(vnos_VALUE)
            if Datoteka not in 소유파일: return 2 if vnos_VALUE.종류==300 else 1
            낱말 = Besedilo(dobiti_ime(vnos_VALUE))
            if not 낱말 or any(ord(znak_VALUE)>127 for znak_VALUE in 낱말): return 2
            if vnos_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Besedilo(UNIQUE_ime(vnos_VALUE)) or Datoteka+':'+str(odmik_VALUE)
                선언들[UNIQUE_VALUE] = {'Datoteka':Datoteka,'odmik_VALUE':odmik_VALUE,'Črtni':Črtni,'종류':vnos_VALUE.종류,'Ime':낱말,'Poveži':연결종류(vnos_VALUE)}
                참조들.append((Datoteka,odmik_VALUE,낱말,UNIQUE_VALUE))
            else:
                Gradiva = dobiti_Gradiva(vnos_VALUE)
                Gradiva_Datoteka,_,_ = kazalec_mesta(Gradiva)
                if Gradiva_Datoteka in 소유파일:
                    UNIQUE_VALUE = Besedilo(UNIQUE_ime(Gradiva)); 참조들.append((Datoteka,odmik_VALUE,Besedilo(dobiti_ime(Gradiva)),UNIQUE_VALUE))
            return 2
        방문(koren_VALUE(Prevod_enota),살피기,None)
        izhod_aplikacija(Prevod_enota)
    cilj_VALUE = pobuda_koren/'build/한국어화/시언어분석.json'
    cilj_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Datoteka:hashlib.sha256(Path(Datoteka).read_bytes()).hexdigest() for Datoteka in sorted(소유파일)}
    cilj_VALUE.write_text(json.dumps({'deklaracija':선언들,'Gradiva':참조들,'NAPAKA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklaracija',len(선언들),'Gradiva',len(참조들),'NAPAKA',len(오류들))
    for NAPAKA in 오류들: print(*NAPAKA)

if __name__=='__main__': Izvedi_ukaz()
