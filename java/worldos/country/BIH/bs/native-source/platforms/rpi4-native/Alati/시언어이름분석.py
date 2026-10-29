#!/usr/bin/env python3
"""libclang 선언·Reference 위치를 수집한다. iz_eksternog_izvora_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

projicirati_koijen = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class string_VALUE(씨.Structure): _fields_ = [('podaci',씨.c_void_p),('program_VALUE',씨.c_uint)]
class kursor_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('podaci',씨.c_void_p*3)]
class Pozicija(씨.Structure): _fields_ = [('podaci',씨.c_void_p*2),('Pomak_VALUE',씨.c_uint)]
def FUNCTION_VALUE(Naziv, vratiti_mjera, *Argumenti):
    unos_VALUE = getattr(구현, Naziv); unos_VALUE.restype = vratiti_mjera; unos_VALUE.argtypes = list(Argumenti); return unos_VALUE
글얻기 = FUNCTION_VALUE('clang_getCString',씨.c_char_p,string_VALUE)
izdanje_SMS = FUNCTION_VALUE('clang_disposeString',None,string_VALUE)
def Tekst(VALUE):
    mjera = (글얻기(VALUE) or b'').decode('utf-8'); izdanje_SMS(VALUE); return mjera
이름얻기 = FUNCTION_VALUE('clang_getCursorSpelling',string_VALUE,kursor_VALUE)
참조얻기 = FUNCTION_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
위치얻기 = FUNCTION_VALUE('clang_getCursorLocation',Pozicija,kursor_VALUE)
fajl_položaj = FUNCTION_VALUE('clang_getFileLocation',None,Pozicija,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fajl_unos_naziv = FUNCTION_VALUE('clang_getFileName',string_VALUE,씨.c_void_p)
UNIQUE_naziv = FUNCTION_VALUE('clang_getCursorUSR',string_VALUE,kursor_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,kursor_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kursor_VALUE,kursor_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,kursor_VALUE,방문형,씨.c_void_p)
generirati = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
koijen_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,씨.c_void_p)
izađi_program = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ozbiljnost_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',string_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def položaj_INDEX(unos_VALUE):
    Fajl = 씨.c_void_p(); Linija = 씨.c_uint(); prostor_za_unos_unos = 씨.c_uint(); Pomak_VALUE = 씨.c_uint()
    fajl_položaj(위치얻기(unos_VALUE),씨.byref(Fajl),씨.byref(Linija),씨.byref(prostor_za_unos_unos),씨.byref(Pomak_VALUE))
    return (Tekst(fajl_unos_naziv(Fajl)) if Fajl else '', Pomak_VALUE.value, Linija.value)

def Izvrši_komanda():
    LOOKUP_INDEX = generirati(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC iz_eksternog_izvora_VALUE 단일 Prevedi_izvor 단위만 포함한다.
    # iz_eksternog_izvora_VALUE 선언을 자체 이름으로 세지 않으며, stvaran_podaci 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Putanja.resolve()) for Putanja in projicirati_koijen.rglob('*') if Putanja.suffix in ('.c','.h','.cpp','.inc')
              and not set(Putanja.relative_to(projicirati_koijen).parts)&{'build','dist','vendor','__pycache__'}
              and Putanja.relative_to(projicirati_koijen).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(projicirati_koijen/'korisnik'),
          '-I'+str(projicirati_koijen.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(projicirati_koijen/'build'),'-I'+str(projicirati_koijen/'build/user'),
          '-I'+str(projicirati_koijen/'build/remote'),'-I'+str(projicirati_koijen/'vendor/bearssl/inc'),
          '-I'+str(projicirati_koijen/'vendor/bearssl/src'),'-I'+str(projicirati_koijen/'vendor/libassh/src'),
          '-I'+str(projicirati_koijen/'vendor/lwip/src/include'),'-I'+str(projicirati_koijen/'Mreža_snop'),
          '-I'+str(projicirati_koijen/'udaljeno_VALUE'),'-I'+str(projicirati_koijen/'시언어번역기')]
    for Putanja in sorted(Path(Naziv) for Naziv in 소유파일 if Naziv.endswith(('.c','.cpp'))):
        Argumenti = 공통 + ['-std=c++11' if Putanja.suffix=='.cpp' else '-std=c11']
        if 'Mreža_snop' in Putanja.parts: Argumenti += ['-I'+str(projicirati_koijen/'Mreža_snop'),'-I'+str(projicirati_koijen/'vendor/lwip/src/include')]
        if '시언어번역기' in Putanja.parts:
            Argumenti += ['-I'+str(projicirati_koijen/'시언어번역기'),'-I'+str(projicirati_koijen/'vendor/tinycc'),'-I'+str(projicirati_koijen/'build/ccompiler'),
                    '-isystem',str(projicirati_koijen.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_most' in Putanja.parts:
            Argumenti += ['-I'+str(projicirati_koijen/'PYTHON_most'),'-I'+str(projicirati_koijen/'build/micropython-1.24.1'),'-I'+str(projicirati_koijen/'build/python'),'-isystem','/usr/include/newlib']
        if 'udaljeno_VALUE' in Putanja.parts:
            Argumenti += ['-isystem', '/usr/include/newlib']
        if '배포' in Putanja.parts: Argumenti += ['-D__JKOROS__=1']
        if Putanja.name=='paket.c': Argumenti += ['-I'+str(projicirati_koijen/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupa_VALUE = (씨.c_char_p*len(Argumenti))(*[unos_VALUE.encode() for unos_VALUE in Argumenti])
        Prevođenje_lekcija = 분석(LOOKUP_INDEX,str(Putanja).encode(),Grupa_VALUE,len(Argumenti),None,0,1)
        for INDEX in range(진단수(Prevođenje_lekcija)):
            진단 = 진단얻기(Prevođenje_lekcija,INDEX)
            if ozbiljnost_VALUE(진단)>=3: 오류들.append((str(Putanja.relative_to(projicirati_koijen)),Tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(unos_VALUE,roditelj_VALUE,podaci):
            Fajl,Pomak_VALUE,Linija = položaj_INDEX(unos_VALUE)
            if Fajl not in 소유파일: return 2 if unos_VALUE.종류==300 else 1
            낱말 = Tekst(이름얻기(unos_VALUE))
            if not 낱말 or any(ord(znak_VALUE)>127 for znak_VALUE in 낱말): return 2
            if unos_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Tekst(UNIQUE_naziv(unos_VALUE)) or Fajl+':'+str(Pomak_VALUE)
                선언들[UNIQUE_VALUE] = {'Fajl':Fajl,'Pomak_VALUE':Pomak_VALUE,'Linija':Linija,'종류':unos_VALUE.종류,'Naziv':낱말,'Spoji_se':연결종류(unos_VALUE)}
                참조들.append((Fajl,Pomak_VALUE,낱말,UNIQUE_VALUE))
            else:
                Reference = 참조얻기(unos_VALUE)
                Reference_fajl,_,_ = položaj_INDEX(Reference)
                if Reference_fajl in 소유파일:
                    UNIQUE_VALUE = Tekst(UNIQUE_naziv(Reference)); 참조들.append((Fajl,Pomak_VALUE,Tekst(이름얻기(Reference)),UNIQUE_VALUE))
            return 2
        방문(koijen_VALUE(Prevođenje_lekcija),살피기,None)
        izađi_program(Prevođenje_lekcija)
    odredište_VALUE = projicirati_koijen/'build/한국어화/시언어분석.json'
    odredište_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fajl:hashlib.sha256(Path(Fajl).read_bytes()).hexdigest() for Fajl in sorted(소유파일)}
    odredište_VALUE.write_text(json.dumps({'선언':선언들,'Reference':참조들,'GRESKA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Reference',len(참조들),'GRESKA',len(오류들))
    for GRESKA in 오류들: print(*GRESKA)

if __name__=='__main__': Izvrši_komanda()
