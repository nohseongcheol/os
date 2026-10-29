#!/usr/bin/env python3
"""libclang deklaracija·Reference 위치를 수집한다. vanjski_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_izvor
import hashlib
import json
from pathlib import Path

akcija_korijen = Path(__file__).resolve().parents[1]
구현 = C_izvor.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class niz_VALUE(C_izvor.Structure): _fields_ = [('podaci',C_izvor.c_void_p),('emisija_VALUE',C_izvor.c_uint)]
class kursor_VALUE(C_izvor.Structure): _fields_ = [('종류',C_izvor.c_uint),('보조',C_izvor.c_int),('podaci',C_izvor.c_void_p*3)]
class Položaj(C_izvor.Structure): _fields_ = [('podaci',C_izvor.c_void_p*2),('pomak_VALUE',C_izvor.c_uint)]
def FUNCTION_VALUE(Ime, vratiti_KR, *Argumenti):
    unos_VALUE = getattr(구현, Ime); unos_VALUE.restype = vratiti_KR; unos_VALUE.argtypes = list(Argumenti); return unos_VALUE
dohvatiti_SMS = FUNCTION_VALUE('clang_getCString',C_izvor.c_char_p,niz_VALUE)
izdati_SMS = FUNCTION_VALUE('clang_disposeString',None,niz_VALUE)
def Tekst(VALUE):
    REZULTAT = (dohvatiti_SMS(VALUE) or b'').decode('utf-8'); izdati_SMS(VALUE); return REZULTAT
dohvatiti_naziv = FUNCTION_VALUE('clang_getCursorSpelling',niz_VALUE,kursor_VALUE)
dohvatiti_Reference = FUNCTION_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
dohvatiti_položaj = FUNCTION_VALUE('clang_getCursorLocation',Položaj,kursor_VALUE)
Datoteka_položaj = FUNCTION_VALUE('clang_getFileLocation',None,Položaj,C_izvor.POINTER(C_izvor.c_void_p),C_izvor.POINTER(C_izvor.c_uint),C_izvor.POINTER(C_izvor.c_uint),C_izvor.POINTER(C_izvor.c_uint))
Datoteka_unos_naziv = FUNCTION_VALUE('clang_getFileName',niz_VALUE,C_izvor.c_void_p)
UNIQUE_naziv = FUNCTION_VALUE('clang_getCursorUSR',niz_VALUE,kursor_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',C_izvor.c_uint,kursor_VALUE)
방문형 = C_izvor.CFUNCTYPE(C_izvor.c_uint,kursor_VALUE,kursor_VALUE,C_izvor.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',C_izvor.c_uint,kursor_VALUE,방문형,C_izvor.c_void_p)
generirati = FUNCTION_VALUE('clang_createIndex',C_izvor.c_void_p,C_izvor.c_int,C_izvor.c_int)
analiza_VALUE = FUNCTION_VALUE('clang_parseTranslationUnit',C_izvor.c_void_p,C_izvor.c_void_p,C_izvor.c_char_p,C_izvor.POINTER(C_izvor.c_char_p),C_izvor.c_int,C_izvor.c_void_p,C_izvor.c_uint,C_izvor.c_uint)
korijen_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,C_izvor.c_void_p)
izlaz_program = FUNCTION_VALUE('clang_disposeTranslationUnit',None,C_izvor.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',C_izvor.c_uint,C_izvor.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',C_izvor.c_void_p,C_izvor.c_void_p,C_izvor.c_uint)
ozbiljnost_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',C_izvor.c_uint,C_izvor.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',niz_VALUE,C_izvor.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,C_izvor.c_void_p)

def indeks_položaja(unos_VALUE):
    Datoteka = C_izvor.c_void_p(); red = C_izvor.c_uint(); 칸 = C_izvor.c_uint(); pomak_VALUE = C_izvor.c_uint()
    Datoteka_položaj(dohvatiti_položaj(unos_VALUE),C_izvor.byref(Datoteka),C_izvor.byref(red),C_izvor.byref(칸),C_izvor.byref(pomak_VALUE))
    return (Tekst(Datoteka_unos_naziv(Datoteka)) if Datoteka else '', pomak_VALUE.value, red.value)

def Izvrši_naredba():
    LOOKUP_INDEX = generirati(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilator_alat.c는 vlastiti deklaracija 없이 TinyCC vanjski_VALUE 단일 prevesti_izvor 단위만 포함한다.
    # vanjski_VALUE 선언을 vlastiti 이름으로 세지 않으며, stvaran_podaci 빌드에서는 계속 컴파일한다.
    소유파일 = {str(PUTANJA.resolve()) for PUTANJA in akcija_korijen.rglob('*') if PUTANJA.suffix in ('.c','.h','.cpp','.inc')
              and not set(PUTANJA.relative_to(akcija_korijen).parts)&{'build','dist','vendor','__pycache__'}
              and PUTANJA.relative_to(akcija_korijen).as_posix() != 'C_kompilator/kompilator_alat.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(akcija_korijen/'korisnik'),
          '-I'+str(akcija_korijen.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(akcija_korijen/'build'),'-I'+str(akcija_korijen/'build/user'),
          '-I'+str(akcija_korijen/'build/remote'),'-I'+str(akcija_korijen/'vendor/bearssl/inc'),
          '-I'+str(akcija_korijen/'vendor/bearssl/src'),'-I'+str(akcija_korijen/'vendor/libassh/src'),
          '-I'+str(akcija_korijen/'vendor/lwip/src/include'),'-I'+str(akcija_korijen/'mreža_hrpa'),
          '-I'+str(akcija_korijen/'udaljeno_VALUE'),'-I'+str(akcija_korijen/'C_kompilator')]
    for PUTANJA in sorted(Path(Ime) for Ime in 소유파일 if Ime.endswith(('.c','.cpp'))):
        Argumenti = 공통 + ['-std=c++11' if PUTANJA.suffix=='.cpp' else '-std=c11']
        if 'mreža_hrpa' in PUTANJA.parts: Argumenti += ['-I'+str(akcija_korijen/'mreža_hrpa'),'-I'+str(akcija_korijen/'vendor/lwip/src/include')]
        if 'C_kompilator' in PUTANJA.parts:
            Argumenti += ['-I'+str(akcija_korijen/'C_kompilator'),'-I'+str(akcija_korijen/'vendor/tinycc'),'-I'+str(akcija_korijen/'build/ccompiler'),
                    '-isystem',str(akcija_korijen.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_most' in PUTANJA.parts:
            Argumenti += ['-I'+str(akcija_korijen/'PYTHON_most'),'-I'+str(akcija_korijen/'build/micropython-1.24.1'),'-I'+str(akcija_korijen/'build/python'),'-isystem','/usr/include/newlib']
        if 'udaljeno_VALUE' in PUTANJA.parts:
            Argumenti += ['-isystem', '/usr/include/newlib']
        if '배포' in PUTANJA.parts: Argumenti += ['-D__JKOROS__=1']
        if PUTANJA.name=='komplet.c': Argumenti += ['-I'+str(akcija_korijen/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupa_VALUE = (C_izvor.c_char_p*len(Argumenti))(*[unos_VALUE.encode() for unos_VALUE in Argumenti])
        Prevođenje_lekcija = analiza_VALUE(LOOKUP_INDEX,str(PUTANJA).encode(),Grupa_VALUE,len(Argumenti),None,0,1)
        for INDEX in range(진단수(Prevođenje_lekcija)):
            진단 = 진단얻기(Prevođenje_lekcija,INDEX)
            if ozbiljnost_VALUE(진단)>=3: 오류들.append((str(PUTANJA.relative_to(akcija_korijen)),Tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(unos_VALUE,roditeljski_VALUE,podaci):
            Datoteka,pomak_VALUE,red = indeks_položaja(unos_VALUE)
            if Datoteka not in 소유파일: return 2 if unos_VALUE.종류==300 else 1
            낱말 = Tekst(dohvatiti_naziv(unos_VALUE))
            if not 낱말 or any(ord(znak_VALUE)>127 for znak_VALUE in 낱말): return 2
            if unos_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Tekst(UNIQUE_naziv(unos_VALUE)) or Datoteka+':'+str(pomak_VALUE)
                선언들[UNIQUE_VALUE] = {'Datoteka':Datoteka,'pomak_VALUE':pomak_VALUE,'줄':red,'종류':unos_VALUE.종류,'Ime':낱말,'Spoji_se':연결종류(unos_VALUE)}
                참조들.append((Datoteka,pomak_VALUE,낱말,UNIQUE_VALUE))
            else:
                Reference = dohvatiti_Reference(unos_VALUE)
                Reference_Datoteka,_,_ = indeks_položaja(Reference)
                if Reference_Datoteka in 소유파일:
                    UNIQUE_VALUE = Tekst(UNIQUE_naziv(Reference)); 참조들.append((Datoteka,pomak_VALUE,Tekst(dohvatiti_naziv(Reference)),UNIQUE_VALUE))
            return 2
        방문(korijen_VALUE(Prevođenje_lekcija),살피기,None)
        izlaz_program(Prevođenje_lekcija)
    odredište_VALUE = akcija_korijen/'build/한국어화/시언어분석.json'
    odredište_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Datoteka:hashlib.sha256(Path(Datoteka).read_bytes()).hexdigest() for Datoteka in sorted(소유파일)}
    odredište_VALUE.write_text(json.dumps({'deklaracija':선언들,'Reference':참조들,'GREŠKA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklaracija',len(선언들),'Reference',len(참조들),'GREŠKA',len(오류들))
    for GREŠKA in 오류들: print(*GREŠKA)

if __name__=='__main__': Izvrši_naredba()
