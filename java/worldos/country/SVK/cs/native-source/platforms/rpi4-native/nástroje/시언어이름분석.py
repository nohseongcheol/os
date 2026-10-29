#!/usr/bin/env python3
"""libclang deklarace_4f4f026b·odkaz 위치를 수집한다. externí_HODNOTA 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_zdroj
import hashlib
import json
from pathlib import Path

akce_kořen = Path(__file__).resolve().parents[1]
implementace = C_zdroj.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class řetězec_HODNOTA(C_zdroj.Structure): _fields_ = [('data',C_zdroj.c_void_p),('zobrazit_HODNOTA',C_zdroj.c_uint)]
class kurzor_HODNOTA(C_zdroj.Structure): _fields_ = [('Druh_HODNOTA',C_zdroj.c_uint),('보조',C_zdroj.c_int),('data',C_zdroj.c_void_p*3)]
class pozice(C_zdroj.Structure): _fields_ = [('data',C_zdroj.c_void_p*2),('POSUN_HODNOTA',C_zdroj.c_uint)]
def funkce_HODNOTA(Název, Vratka_KV, *argumenty):
    položka_HODNOTA = getattr(implementace, Název); položka_HODNOTA.restype = Vratka_KV; položka_HODNOTA.argtypes = list(argumenty); return položka_HODNOTA
get_SMS = funkce_HODNOTA('clang_getCString',C_zdroj.c_char_p,řetězec_HODNOTA)
verze_SMS = funkce_HODNOTA('clang_disposeString',None,řetězec_HODNOTA)
def text(HODNOTA):
    VÝSLEDEK = (get_SMS(HODNOTA) or b'').decode('utf-8'); verze_SMS(HODNOTA); return VÝSLEDEK
get_název = funkce_HODNOTA('clang_getCursorSpelling',řetězec_HODNOTA,kurzor_HODNOTA)
get_odkaz = funkce_HODNOTA('clang_getCursorReferenced',kurzor_HODNOTA,kurzor_HODNOTA)
get_pozice = funkce_HODNOTA('clang_getCursorLocation',pozice,kurzor_HODNOTA)
Soubor_pozice = funkce_HODNOTA('clang_getFileLocation',None,pozice,C_zdroj.POINTER(C_zdroj.c_void_p),C_zdroj.POINTER(C_zdroj.c_uint),C_zdroj.POINTER(C_zdroj.c_uint),C_zdroj.POINTER(C_zdroj.c_uint))
Soubor_položka_název = funkce_HODNOTA('clang_getFileName',řetězec_HODNOTA,C_zdroj.c_void_p)
UNIQUE_název = funkce_HODNOTA('clang_getCursorUSR',řetězec_HODNOTA,kurzor_HODNOTA)
kontakt_Druh = funkce_HODNOTA('clang_getCursorLinkage',C_zdroj.c_uint,kurzor_HODNOTA)
방문형 = C_zdroj.CFUNCTYPE(C_zdroj.c_uint,kurzor_HODNOTA,kurzor_HODNOTA,C_zdroj.c_void_p)
방문 = funkce_HODNOTA('clang_visitChildren',C_zdroj.c_uint,kurzor_HODNOTA,방문형,C_zdroj.c_void_p)
generovat = funkce_HODNOTA('clang_createIndex',C_zdroj.c_void_p,C_zdroj.c_int,C_zdroj.c_int)
Analýza_HODNOTA = funkce_HODNOTA('clang_parseTranslationUnit',C_zdroj.c_void_p,C_zdroj.c_void_p,C_zdroj.c_char_p,C_zdroj.POINTER(C_zdroj.c_char_p),C_zdroj.c_int,C_zdroj.c_void_p,C_zdroj.c_uint,C_zdroj.c_uint)
kořen_HODNOTA = funkce_HODNOTA('clang_getTranslationUnitCursor',kurzor_HODNOTA,C_zdroj.c_void_p)
ukončit_program = funkce_HODNOTA('clang_disposeTranslationUnit',None,C_zdroj.c_void_p)
진단수 = funkce_HODNOTA('clang_getNumDiagnostics',C_zdroj.c_uint,C_zdroj.c_void_p)
진단얻기 = funkce_HODNOTA('clang_getDiagnostic',C_zdroj.c_void_p,C_zdroj.c_void_p,C_zdroj.c_uint)
závažnost_HODNOTA = funkce_HODNOTA('clang_getDiagnosticSeverity',C_zdroj.c_uint,C_zdroj.c_void_p)
진단문 = funkce_HODNOTA('clang_getDiagnosticSpelling',řetězec_HODNOTA,C_zdroj.c_void_p)
진단해제 = funkce_HODNOTA('clang_disposeDiagnostic',None,C_zdroj.c_void_p)

def poziční_index(položka_HODNOTA):
    název_souboru = C_zdroj.c_void_p(); vstupní_řádek = C_zdroj.c_uint(); přihrádka_položka = C_zdroj.c_uint(); POSUN_HODNOTA = C_zdroj.c_uint()
    Soubor_pozice(get_pozice(položka_HODNOTA),C_zdroj.byref(název_souboru),C_zdroj.byref(vstupní_řádek),C_zdroj.byref(přihrádka_položka),C_zdroj.byref(POSUN_HODNOTA))
    return (text(Soubor_položka_název(název_souboru)) if název_souboru else '', POSUN_HODNOTA.value, vstupní_řádek.value)

def Provést_příkaz():
    VYHLEDAT_INDEX = generovat(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilátor_nástroj.c는 vlastní deklarace_4f4f026b 없이 TinyCC externí_HODNOTA 단일 převést_zdroj 단위만 포함한다.
    # externí_HODNOTA 선언을 vlastní 이름으로 세지 않으며, skutečný_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(cesta_2.resolve()) for cesta_2 in akce_kořen.rglob('*') if cesta_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(cesta_2.relative_to(akce_kořen).parts)&{'build','dist','vendor','__pycache__'}
              and cesta_2.relative_to(akce_kořen).as_posix() != 'C_kompilátor/kompilátor_nástroj.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(akce_kořen/'uživatelský_prostor'),
          '-I'+str(akce_kořen.parents[1]/'posix-kor/arm64-native/deklarace'),'-I'+str(akce_kořen/'build'),'-I'+str(akce_kořen/'build/user'),
          '-I'+str(akce_kořen/'build/remote'),'-I'+str(akce_kořen/'vendor/bearssl/inc'),
          '-I'+str(akce_kořen/'vendor/bearssl/src'),'-I'+str(akce_kořen/'vendor/libassh/src'),
          '-I'+str(akce_kořen/'vendor/lwip/src/include'),'-I'+str(akce_kořen/'síť_Štos'),
          '-I'+str(akce_kořen/'vzdálený_HODNOTA'),'-I'+str(akce_kořen/'C_kompilátor')]
    for cesta_2 in sorted(Path(Název) for Název in 소유파일 if Název.endswith(('.c','.cpp'))):
        argumenty = 공통 + ['-std=c++11' if cesta_2.suffix=='.cpp' else '-std=c11']
        if 'síť_Štos' in cesta_2.parts: argumenty += ['-I'+str(akce_kořen/'síť_Štos'),'-I'+str(akce_kořen/'vendor/lwip/src/include')]
        if 'C_kompilátor' in cesta_2.parts:
            argumenty += ['-I'+str(akce_kořen/'C_kompilátor'),'-I'+str(akce_kořen/'vendor/tinycc'),'-I'+str(akce_kořen/'build/ccompiler'),
                    '-isystem',str(akce_kořen.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_most' in cesta_2.parts:
            argumenty += ['-I'+str(akce_kořen/'PYTHON_most'),'-I'+str(akce_kořen/'build/micropython-1.24.1'),'-I'+str(akce_kořen/'build/python'),'-isystem','/usr/include/newlib']
        if 'vzdálený_HODNOTA' in cesta_2.parts:
            argumenty += ['-isystem', '/usr/include/newlib']
        if 'distribuce_HODNOTA' in cesta_2.parts: argumenty += ['-D__JKOROS__=1']
        if cesta_2.name=='sada.c': argumenty += ['-I'+str(akce_kořen/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Skupina_HODNOTA = (C_zdroj.c_char_p*len(argumenty))(*[položka_HODNOTA.encode() for položka_HODNOTA in argumenty])
        jednotka_překladu = Analýza_HODNOTA(VYHLEDAT_INDEX,str(cesta_2).encode(),Skupina_HODNOTA,len(argumenty),None,0,1)
        for INDEX in range(진단수(jednotka_překladu)):
            진단 = 진단얻기(jednotka_překladu,INDEX)
            if závažnost_HODNOTA(진단)>=3: 오류들.append((str(cesta_2.relative_to(akce_kořen)),text(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(položka_HODNOTA,nadřazený_HODNOTA,data):
            název_souboru,POSUN_HODNOTA,vstupní_řádek = poziční_index(položka_HODNOTA)
            if název_souboru not in 소유파일: return 2 if položka_HODNOTA.Druh_HODNOTA==300 else 1
            낱말 = text(get_název(položka_HODNOTA))
            if not 낱말 or any(ord(znak_HODNOTA)>127 for znak_HODNOTA in 낱말): return 2
            if položka_HODNOTA.Druh_HODNOTA in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_HODNOTA = text(UNIQUE_název(položka_HODNOTA)) or název_souboru+':'+str(POSUN_HODNOTA)
                선언들[UNIQUE_HODNOTA] = {'název_souboru':název_souboru,'POSUN_HODNOTA':POSUN_HODNOTA,'vstupní_řádek':vstupní_řádek,'Druh_HODNOTA':položka_HODNOTA.Druh_HODNOTA,'Název':낱말,'Připojit':kontakt_Druh(položka_HODNOTA)}
                참조들.append((název_souboru,POSUN_HODNOTA,낱말,UNIQUE_HODNOTA))
            else:
                odkaz = get_odkaz(položka_HODNOTA)
                odkaz_Soubor,_,_ = poziční_index(odkaz)
                if odkaz_Soubor in 소유파일:
                    UNIQUE_HODNOTA = text(UNIQUE_název(odkaz)); 참조들.append((název_souboru,POSUN_HODNOTA,text(get_název(odkaz)),UNIQUE_HODNOTA))
            return 2
        방문(kořen_HODNOTA(jednotka_překladu),살피기,None)
        ukončit_program(jednotka_překladu)
    cíl_HODNOTA = akce_kořen/'build/한국어화/시언어분석.json'
    cíl_HODNOTA.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {název_souboru:hashlib.sha256(Path(název_souboru).read_bytes()).hexdigest() for název_souboru in sorted(소유파일)}
    cíl_HODNOTA.write_text(json.dumps({'deklarace_4f4f026b':선언들,'odkaz':참조들,'chyba':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklarace_4f4f026b',len(선언들),'odkaz',len(참조들),'chyba',len(오류들))
    for chyba in 오류들: print(*chyba)

if __name__=='__main__': Provést_příkaz()
