#!/usr/bin/env python3
"""libclang deklaracija·referenca 위치를 수집한다. spoljni_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_izvor
import hashlib
import json
from pathlib import Path

radnja_koren = Path(__file__).resolve().parents[1]
구현 = C_izvor.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class niska_VALUE(C_izvor.Structure): _fields_ = [('podaci',C_izvor.c_void_p),('emisija_VALUE',C_izvor.c_uint)]
class kursor_VALUE(C_izvor.Structure): _fields_ = [('종류',C_izvor.c_uint),('보조',C_izvor.c_int),('podaci',C_izvor.c_void_p*3)]
class pozicija(C_izvor.Structure): _fields_ = [('podaci',C_izvor.c_void_p*2),('Pomak_VALUE',C_izvor.c_uint)]
def FUNCTION_VALUE(ime, vratiti_KR, *인수):
    stavka_VALUE = getattr(구현, ime); stavka_VALUE.restype = vratiti_KR; stavka_VALUE.argtypes = list(인수); return stavka_VALUE
preuzeti_SMS = FUNCTION_VALUE('clang_getCString',C_izvor.c_char_p,niska_VALUE)
izdanje_SMS = FUNCTION_VALUE('clang_disposeString',None,niska_VALUE)
def SMS(VALUE):
    KR = (preuzeti_SMS(VALUE) or b'').decode('utf-8'); izdanje_SMS(VALUE); return KR
preuzeti_ime = FUNCTION_VALUE('clang_getCursorSpelling',niska_VALUE,kursor_VALUE)
preuzeti_referenca = FUNCTION_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
preuzeti_pozicija = FUNCTION_VALUE('clang_getCursorLocation',pozicija,kursor_VALUE)
Datoteka_pozicija = FUNCTION_VALUE('clang_getFileLocation',None,pozicija,C_izvor.POINTER(C_izvor.c_void_p),C_izvor.POINTER(C_izvor.c_uint),C_izvor.POINTER(C_izvor.c_uint),C_izvor.POINTER(C_izvor.c_uint))
Datoteka_stavka_ime = FUNCTION_VALUE('clang_getFileName',niska_VALUE,C_izvor.c_void_p)
UNIQUE_ime = FUNCTION_VALUE('clang_getCursorUSR',niska_VALUE,kursor_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',C_izvor.c_uint,kursor_VALUE)
방문형 = C_izvor.CFUNCTYPE(C_izvor.c_uint,kursor_VALUE,kursor_VALUE,C_izvor.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',C_izvor.c_uint,kursor_VALUE,방문형,C_izvor.c_void_p)
generisati = FUNCTION_VALUE('clang_createIndex',C_izvor.c_void_p,C_izvor.c_int,C_izvor.c_int)
Analiza_VALUE = FUNCTION_VALUE('clang_parseTranslationUnit',C_izvor.c_void_p,C_izvor.c_void_p,C_izvor.c_char_p,C_izvor.POINTER(C_izvor.c_char_p),C_izvor.c_int,C_izvor.c_void_p,C_izvor.c_uint,C_izvor.c_uint)
koren_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,C_izvor.c_void_p)
Napusti_program = FUNCTION_VALUE('clang_disposeTranslationUnit',None,C_izvor.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',C_izvor.c_uint,C_izvor.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',C_izvor.c_void_p,C_izvor.c_void_p,C_izvor.c_uint)
ozbiljnost_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',C_izvor.c_uint,C_izvor.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',niska_VALUE,C_izvor.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,C_izvor.c_void_p)

def indeks_pozicije(stavka_VALUE):
    Datoteka = C_izvor.c_void_p(); red = C_izvor.c_uint(); 칸 = C_izvor.c_uint(); Pomak_VALUE = C_izvor.c_uint()
    Datoteka_pozicija(preuzeti_pozicija(stavka_VALUE),C_izvor.byref(Datoteka),C_izvor.byref(red),C_izvor.byref(칸),C_izvor.byref(Pomak_VALUE))
    return (SMS(Datoteka_stavka_ime(Datoteka)) if Datoteka else '', Pomak_VALUE.value, red.value)

def Izvrši_komanda():
    LOOKUP_INDEX = generisati(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompajler_alatka.c는 자체 deklaracija 없이 TinyCC spoljni_VALUE 단일 prevesti_izvor 단위만 포함한다.
    # spoljni_VALUE 선언을 자체 이름으로 세지 않으며, stvarni_podaci 빌드에서는 계속 컴파일한다.
    소유파일 = {str(putanja.resolve()) for putanja in radnja_koren.rglob('*') if putanja.suffix in ('.c','.h','.cpp','.inc')
              and not set(putanja.relative_to(radnja_koren).parts)&{'build','dist','vendor','__pycache__'}
              and putanja.relative_to(radnja_koren).as_posix() != 'C_kompajler/kompajler_alatka.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(radnja_koren/'korisnik'),
          '-I'+str(radnja_koren.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(radnja_koren/'build'),'-I'+str(radnja_koren/'build/user'),
          '-I'+str(radnja_koren/'build/remote'),'-I'+str(radnja_koren/'vendor/bearssl/inc'),
          '-I'+str(radnja_koren/'vendor/bearssl/src'),'-I'+str(radnja_koren/'vendor/libassh/src'),
          '-I'+str(radnja_koren/'vendor/lwip/src/include'),'-I'+str(radnja_koren/'Mreža_stek'),
          '-I'+str(radnja_koren/'udaljen_VALUE'),'-I'+str(radnja_koren/'C_kompajler')]
    for putanja in sorted(Path(ime) for ime in 소유파일 if ime.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if putanja.suffix=='.cpp' else '-std=c11']
        if 'Mreža_stek' in putanja.parts: 인수 += ['-I'+str(radnja_koren/'Mreža_stek'),'-I'+str(radnja_koren/'vendor/lwip/src/include')]
        if 'C_kompajler' in putanja.parts:
            인수 += ['-I'+str(radnja_koren/'C_kompajler'),'-I'+str(radnja_koren/'vendor/tinycc'),'-I'+str(radnja_koren/'build/ccompiler'),
                    '-isystem',str(radnja_koren.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_most' in putanja.parts:
            인수 += ['-I'+str(radnja_koren/'PYTHON_most'),'-I'+str(radnja_koren/'build/micropython-1.24.1'),'-I'+str(radnja_koren/'build/python'),'-isystem','/usr/include/newlib']
        if 'udaljen_VALUE' in putanja.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in putanja.parts: 인수 += ['-D__JKOROS__=1']
        if putanja.name=='komplet.c': 인수 += ['-I'+str(radnja_koren/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupa_VALUE = (C_izvor.c_char_p*len(인수))(*[stavka_VALUE.encode() for stavka_VALUE in 인수])
        Prevođenje_lekcija = Analiza_VALUE(LOOKUP_INDEX,str(putanja).encode(),Grupa_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Prevođenje_lekcija)):
            진단 = 진단얻기(Prevođenje_lekcija,INDEX)
            if ozbiljnost_VALUE(진단)>=3: 오류들.append((str(putanja.relative_to(radnja_koren)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(stavka_VALUE,nadređen_VALUE,podaci):
            Datoteka,Pomak_VALUE,red = indeks_pozicije(stavka_VALUE)
            if Datoteka not in 소유파일: return 2 if stavka_VALUE.종류==300 else 1
            낱말 = SMS(preuzeti_ime(stavka_VALUE))
            if not 낱말 or any(ord(znak_VALUE)>127 for znak_VALUE in 낱말): return 2
            if stavka_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = SMS(UNIQUE_ime(stavka_VALUE)) or Datoteka+':'+str(Pomak_VALUE)
                선언들[UNIQUE_VALUE] = {'Datoteka':Datoteka,'Pomak_VALUE':Pomak_VALUE,'줄':red,'종류':stavka_VALUE.종류,'ime':낱말,'veze':연결종류(stavka_VALUE)}
                참조들.append((Datoteka,Pomak_VALUE,낱말,UNIQUE_VALUE))
            else:
                referenca = preuzeti_referenca(stavka_VALUE)
                referenca_Datoteka,_,_ = indeks_pozicije(referenca)
                if referenca_Datoteka in 소유파일:
                    UNIQUE_VALUE = SMS(UNIQUE_ime(referenca)); 참조들.append((Datoteka,Pomak_VALUE,SMS(preuzeti_ime(referenca)),UNIQUE_VALUE))
            return 2
        방문(koren_VALUE(Prevođenje_lekcija),살피기,None)
        Napusti_program(Prevođenje_lekcija)
    odredište_VALUE = radnja_koren/'build/한국어화/시언어분석.json'
    odredište_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Datoteka:hashlib.sha256(Path(Datoteka).read_bytes()).hexdigest() for Datoteka in sorted(소유파일)}
    odredište_VALUE.write_text(json.dumps({'deklaracija':선언들,'referenca':참조들,'greška':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklaracija',len(선언들),'referenca',len(참조들),'greška',len(오류들))
    for greška in 오류들: print(*greška)

if __name__=='__main__': Izvrši_komanda()
