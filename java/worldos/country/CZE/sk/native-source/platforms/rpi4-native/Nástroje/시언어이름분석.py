#!/usr/bin/env python3
"""libclang deklarácia·zdroj 위치를 수집한다. externý_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_zdroj
import hashlib
import json
from pathlib import Path

akcia_koreň = Path(__file__).resolve().parents[1]
구현 = C_zdroj.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class reťazec_VALUE(C_zdroj.Structure): _fields_ = [('údaje',C_zdroj.c_void_p),('zobraziť_VALUE_487749b8',C_zdroj.c_uint)]
class kurzor_VALUE(C_zdroj.Structure): _fields_ = [('종류',C_zdroj.c_uint),('보조',C_zdroj.c_int),('údaje',C_zdroj.c_void_p*3)]
class Pozícia(C_zdroj.Structure): _fields_ = [('údaje',C_zdroj.c_void_p*2),('Posun_VALUE',C_zdroj.c_uint)]
def funkcia_VALUE(Názov, vrátiť_KR, *Argumenty):
    položka_VALUE = getattr(구현, Názov); položka_VALUE.restype = vrátiť_KR; položka_VALUE.argtypes = list(Argumenty); return položka_VALUE
načítať_SMS = funkcia_VALUE('clang_getCString',C_zdroj.c_char_p,reťazec_VALUE)
vydať_SMS = funkcia_VALUE('clang_disposeString',None,reťazec_VALUE)
def Spracovanie_textu(VALUE):
    KR = (načítať_SMS(VALUE) or b'').decode('utf-8'); vydať_SMS(VALUE); return KR
načítať_názov = funkcia_VALUE('clang_getCursorSpelling',reťazec_VALUE,kurzor_VALUE)
načítať_zdroj = funkcia_VALUE('clang_getCursorReferenced',kurzor_VALUE,kurzor_VALUE)
načítať_pozícia = funkcia_VALUE('clang_getCursorLocation',Pozícia,kurzor_VALUE)
Súbor_pozícia = funkcia_VALUE('clang_getFileLocation',None,Pozícia,C_zdroj.POINTER(C_zdroj.c_void_p),C_zdroj.POINTER(C_zdroj.c_uint),C_zdroj.POINTER(C_zdroj.c_uint),C_zdroj.POINTER(C_zdroj.c_uint))
Súbor_položka_názov = funkcia_VALUE('clang_getFileName',reťazec_VALUE,C_zdroj.c_void_p)
UNIQUE_názov = funkcia_VALUE('clang_getCursorUSR',reťazec_VALUE,kurzor_VALUE)
연결종류 = funkcia_VALUE('clang_getCursorLinkage',C_zdroj.c_uint,kurzor_VALUE)
방문형 = C_zdroj.CFUNCTYPE(C_zdroj.c_uint,kurzor_VALUE,kurzor_VALUE,C_zdroj.c_void_p)
방문 = funkcia_VALUE('clang_visitChildren',C_zdroj.c_uint,kurzor_VALUE,방문형,C_zdroj.c_void_p)
generovať = funkcia_VALUE('clang_createIndex',C_zdroj.c_void_p,C_zdroj.c_int,C_zdroj.c_int)
Analýza_VALUE = funkcia_VALUE('clang_parseTranslationUnit',C_zdroj.c_void_p,C_zdroj.c_void_p,C_zdroj.c_char_p,C_zdroj.POINTER(C_zdroj.c_char_p),C_zdroj.c_int,C_zdroj.c_void_p,C_zdroj.c_uint,C_zdroj.c_uint)
koreň_VALUE = funkcia_VALUE('clang_getTranslationUnitCursor',kurzor_VALUE,C_zdroj.c_void_p)
ukončiť_program = funkcia_VALUE('clang_disposeTranslationUnit',None,C_zdroj.c_void_p)
진단수 = funkcia_VALUE('clang_getNumDiagnostics',C_zdroj.c_uint,C_zdroj.c_void_p)
진단얻기 = funkcia_VALUE('clang_getDiagnostic',C_zdroj.c_void_p,C_zdroj.c_void_p,C_zdroj.c_uint)
závažnosť_VALUE = funkcia_VALUE('clang_getDiagnosticSeverity',C_zdroj.c_uint,C_zdroj.c_void_p)
진단문 = funkcia_VALUE('clang_getDiagnosticSpelling',reťazec_VALUE,C_zdroj.c_void_p)
진단해제 = funkcia_VALUE('clang_disposeDiagnostic',None,C_zdroj.c_void_p)

def pozičný_index(položka_VALUE):
    Súbor = C_zdroj.c_void_p(); riadok = C_zdroj.c_uint(); 칸 = C_zdroj.c_uint(); Posun_VALUE = C_zdroj.c_uint()
    Súbor_pozícia(načítať_pozícia(položka_VALUE),C_zdroj.byref(Súbor),C_zdroj.byref(riadok),C_zdroj.byref(칸),C_zdroj.byref(Posun_VALUE))
    return (Spracovanie_textu(Súbor_položka_názov(Súbor)) if Súbor else '', Posun_VALUE.value, riadok.value)

def Vykonať_príkaz():
    LOOKUP_INDEX = generovať(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilátor_nástroj.c는 vlastné deklarácia 없이 TinyCC externý_VALUE 단일 Preložiť_zdroj 단위만 포함한다.
    # externý_VALUE 선언을 vlastné 이름으로 세지 않으며, skutočný_údaje 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Cesta.resolve()) for Cesta in akcia_koreň.rglob('*') if Cesta.suffix in ('.c','.h','.cpp','.inc')
              and not set(Cesta.relative_to(akcia_koreň).parts)&{'build','dist','vendor','__pycache__'}
              and Cesta.relative_to(akcia_koreň).as_posix() != 'C_kompilátor/kompilátor_nástroj.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(akcia_koreň/'používateľ'),
          '-I'+str(akcia_koreň.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(akcia_koreň/'build'),'-I'+str(akcia_koreň/'build/user'),
          '-I'+str(akcia_koreň/'build/remote'),'-I'+str(akcia_koreň/'vendor/bearssl/inc'),
          '-I'+str(akcia_koreň/'vendor/bearssl/src'),'-I'+str(akcia_koreň/'vendor/libassh/src'),
          '-I'+str(akcia_koreň/'vendor/lwip/src/include'),'-I'+str(akcia_koreň/'sieť_Vrstvy'),
          '-I'+str(akcia_koreň/'vzdialený_VALUE'),'-I'+str(akcia_koreň/'C_kompilátor')]
    for Cesta in sorted(Path(Názov) for Názov in 소유파일 if Názov.endswith(('.c','.cpp'))):
        Argumenty = 공통 + ['-std=c++11' if Cesta.suffix=='.cpp' else '-std=c11']
        if 'sieť_Vrstvy' in Cesta.parts: Argumenty += ['-I'+str(akcia_koreň/'sieť_Vrstvy'),'-I'+str(akcia_koreň/'vendor/lwip/src/include')]
        if 'C_kompilátor' in Cesta.parts:
            Argumenty += ['-I'+str(akcia_koreň/'C_kompilátor'),'-I'+str(akcia_koreň/'vendor/tinycc'),'-I'+str(akcia_koreň/'build/ccompiler'),
                    '-isystem',str(akcia_koreň.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_most' in Cesta.parts:
            Argumenty += ['-I'+str(akcia_koreň/'PYTHON_most'),'-I'+str(akcia_koreň/'build/micropython-1.24.1'),'-I'+str(akcia_koreň/'build/python'),'-isystem','/usr/include/newlib']
        if 'vzdialený_VALUE' in Cesta.parts:
            Argumenty += ['-isystem', '/usr/include/newlib']
        if '배포' in Cesta.parts: Argumenty += ['-D__JKOROS__=1']
        if Cesta.name=='zväzok.c': Argumenty += ['-I'+str(akcia_koreň/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Skupina_VALUE = (C_zdroj.c_char_p*len(Argumenty))(*[položka_VALUE.encode() for položka_VALUE in Argumenty])
        Preklad_lekcia = Analýza_VALUE(LOOKUP_INDEX,str(Cesta).encode(),Skupina_VALUE,len(Argumenty),None,0,1)
        for INDEX in range(진단수(Preklad_lekcia)):
            진단 = 진단얻기(Preklad_lekcia,INDEX)
            if závažnosť_VALUE(진단)>=3: 오류들.append((str(Cesta.relative_to(akcia_koreň)),Spracovanie_textu(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(položka_VALUE,nadradený_VALUE,údaje):
            Súbor,Posun_VALUE,riadok = pozičný_index(položka_VALUE)
            if Súbor not in 소유파일: return 2 if položka_VALUE.종류==300 else 1
            낱말 = Spracovanie_textu(načítať_názov(položka_VALUE))
            if not 낱말 or any(ord(znak_VALUE)>127 for znak_VALUE in 낱말): return 2
            if položka_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Spracovanie_textu(UNIQUE_názov(položka_VALUE)) or Súbor+':'+str(Posun_VALUE)
                선언들[UNIQUE_VALUE] = {'Súbor':Súbor,'Posun_VALUE':Posun_VALUE,'riadok':riadok,'종류':položka_VALUE.종류,'Názov':낱말,'Pripojiť':연결종류(položka_VALUE)}
                참조들.append((Súbor,Posun_VALUE,낱말,UNIQUE_VALUE))
            else:
                zdroj = načítať_zdroj(položka_VALUE)
                zdroj_Súbor,_,_ = pozičný_index(zdroj)
                if zdroj_Súbor in 소유파일:
                    UNIQUE_VALUE = Spracovanie_textu(UNIQUE_názov(zdroj)); 참조들.append((Súbor,Posun_VALUE,Spracovanie_textu(načítať_názov(zdroj)),UNIQUE_VALUE))
            return 2
        방문(koreň_VALUE(Preklad_lekcia),살피기,None)
        ukončiť_program(Preklad_lekcia)
    cieľ_VALUE = akcia_koreň/'build/한국어화/시언어분석.json'
    cieľ_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Súbor:hashlib.sha256(Path(Súbor).read_bytes()).hexdigest() for Súbor in sorted(소유파일)}
    cieľ_VALUE.write_text(json.dumps({'deklarácia':선언들,'zdroj':참조들,'chyba':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklarácia',len(선언들),'zdroj',len(참조들),'chyba',len(오류들))
    for chyba in 오류들: print(*chyba)

if __name__=='__main__': Vykonať_príkaz()
