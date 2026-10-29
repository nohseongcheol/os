#!/usr/bin/env python3
"""libclang deklaracja·odwołanie 위치를 수집한다. zewnętrzny_WARTOŚĆ 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_źródło
import hashlib
import json
from pathlib import Path

Project_korzeń = Path(__file__).resolve().parents[1]
implementacja = C_źródło.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ciąg_WARTOŚĆ(C_źródło.Structure): _fields_ = [('dane',C_źródło.c_void_p),('program_WARTOŚĆ',C_źródło.c_uint)]
class kursor_WARTOŚĆ(C_źródło.Structure): _fields_ = [('Rodzaj_WARTOŚĆ',C_źródło.c_uint),('보조',C_źródło.c_int),('dane',C_źródło.c_void_p*3)]
class pozycja(C_źródło.Structure): _fields_ = [('dane',C_źródło.c_void_p*2),('przesunąć_WARTOŚĆ_450fc799',C_źródło.c_uint)]
def FUNKCJA_WARTOŚĆ(Nazwa, Zwrot_KR, *argumenty):
    wpis_WARTOŚĆ = getattr(implementacja, Nazwa); wpis_WARTOŚĆ.restype = Zwrot_KR; wpis_WARTOŚĆ.argtypes = list(argumenty); return wpis_WARTOŚĆ
pobrać_SMS = FUNKCJA_WARTOŚĆ('clang_getCString',C_źródło.c_char_p,ciąg_WARTOŚĆ)
wersja_SMS = FUNKCJA_WARTOŚĆ('clang_disposeString',None,ciąg_WARTOŚĆ)
def tekst(WARTOŚĆ):
    WYNIK = (pobrać_SMS(WARTOŚĆ) or b'').decode('utf-8'); wersja_SMS(WARTOŚĆ); return WYNIK
pobrać_nazwa = FUNKCJA_WARTOŚĆ('clang_getCursorSpelling',ciąg_WARTOŚĆ,kursor_WARTOŚĆ)
pobrać_odwołanie = FUNKCJA_WARTOŚĆ('clang_getCursorReferenced',kursor_WARTOŚĆ,kursor_WARTOŚĆ)
pobrać_stanowisko = FUNKCJA_WARTOŚĆ('clang_getCursorLocation',pozycja,kursor_WARTOŚĆ)
Plik_stanowisko = FUNKCJA_WARTOŚĆ('clang_getFileLocation',None,pozycja,C_źródło.POINTER(C_źródło.c_void_p),C_źródło.POINTER(C_źródło.c_uint),C_źródło.POINTER(C_źródło.c_uint),C_źródło.POINTER(C_źródło.c_uint))
Plik_wpis_nazwa = FUNKCJA_WARTOŚĆ('clang_getFileName',ciąg_WARTOŚĆ,C_źródło.c_void_p)
UNIKATOWE_nazwa = FUNKCJA_WARTOŚĆ('clang_getCursorUSR',ciąg_WARTOŚĆ,kursor_WARTOŚĆ)
połączenie_Rodzaj = FUNKCJA_WARTOŚĆ('clang_getCursorLinkage',C_źródło.c_uint,kursor_WARTOŚĆ)
방문형 = C_źródło.CFUNCTYPE(C_źródło.c_uint,kursor_WARTOŚĆ,kursor_WARTOŚĆ,C_źródło.c_void_p)
방문 = FUNKCJA_WARTOŚĆ('clang_visitChildren',C_źródło.c_uint,kursor_WARTOŚĆ,방문형,C_źródło.c_void_p)
generować = FUNKCJA_WARTOŚĆ('clang_createIndex',C_źródło.c_void_p,C_źródło.c_int,C_źródło.c_int)
Analiza_WARTOŚĆ = FUNKCJA_WARTOŚĆ('clang_parseTranslationUnit',C_źródło.c_void_p,C_źródło.c_void_p,C_źródło.c_char_p,C_źródło.POINTER(C_źródło.c_char_p),C_źródło.c_int,C_źródło.c_void_p,C_źródło.c_uint,C_źródło.c_uint)
korzeń_WARTOŚĆ = FUNKCJA_WARTOŚĆ('clang_getTranslationUnitCursor',kursor_WARTOŚĆ,C_źródło.c_void_p)
zakończ_program = FUNKCJA_WARTOŚĆ('clang_disposeTranslationUnit',None,C_źródło.c_void_p)
진단수 = FUNKCJA_WARTOŚĆ('clang_getNumDiagnostics',C_źródło.c_uint,C_źródło.c_void_p)
진단얻기 = FUNKCJA_WARTOŚĆ('clang_getDiagnostic',C_źródło.c_void_p,C_źródło.c_void_p,C_źródło.c_uint)
stopień_WARTOŚĆ = FUNKCJA_WARTOŚĆ('clang_getDiagnosticSeverity',C_źródło.c_uint,C_źródło.c_void_p)
진단문 = FUNKCJA_WARTOŚĆ('clang_getDiagnosticSpelling',ciąg_WARTOŚĆ,C_źródło.c_void_p)
진단해제 = FUNKCJA_WARTOŚĆ('clang_disposeDiagnostic',None,C_źródło.c_void_p)

def indeks_pozycji(wpis_WARTOŚĆ):
    nazwa_pliku = C_źródło.c_void_p(); wiersz_wejścia = C_źródło.c_uint(); gniazdo_wpis = C_źródło.c_uint(); przesunąć_WARTOŚĆ_450fc799 = C_źródło.c_uint()
    Plik_stanowisko(pobrać_stanowisko(wpis_WARTOŚĆ),C_źródło.byref(nazwa_pliku),C_źródło.byref(wiersz_wejścia),C_źródło.byref(gniazdo_wpis),C_źródło.byref(przesunąć_WARTOŚĆ_450fc799))
    return (tekst(Plik_wpis_nazwa(nazwa_pliku)) if nazwa_pliku else '', przesunąć_WARTOŚĆ_450fc799.value, wiersz_wejścia.value)

def Wykonaj_polecenie():
    WYSZUKAJ_INDEKS = generować(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilator_narzędzie.c는 własny deklaracja 없이 TinyCC zewnętrzny_WARTOŚĆ 단일 TŁUMACZ_źródło 단위만 포함한다.
    # zewnętrzny_WARTOŚĆ 선언을 własny 이름으로 세지 않으며, rzeczywisty_dane 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ścieżka_2.resolve()) for ścieżka_2 in Project_korzeń.rglob('*') if ścieżka_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(ścieżka_2.relative_to(Project_korzeń).parts)&{'build','dist','vendor','__pycache__'}
              and ścieżka_2.relative_to(Project_korzeń).as_posix() != 'C_kompilator/kompilator_narzędzie.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_korzeń/'przestrzeń_użytkownika'),
          '-I'+str(Project_korzeń.parents[1]/'posix-kor/arm64-native/deklaracje'),'-I'+str(Project_korzeń/'build'),'-I'+str(Project_korzeń/'build/user'),
          '-I'+str(Project_korzeń/'build/remote'),'-I'+str(Project_korzeń/'vendor/bearssl/inc'),
          '-I'+str(Project_korzeń/'vendor/bearssl/src'),'-I'+str(Project_korzeń/'vendor/libassh/src'),
          '-I'+str(Project_korzeń/'vendor/lwip/src/include'),'-I'+str(Project_korzeń/'sieć_Stos'),
          '-I'+str(Project_korzeń/'zdalny_WARTOŚĆ'),'-I'+str(Project_korzeń/'C_kompilator')]
    for ścieżka_2 in sorted(Path(Nazwa) for Nazwa in 소유파일 if Nazwa.endswith(('.c','.cpp'))):
        argumenty = 공통 + ['-std=c++11' if ścieżka_2.suffix=='.cpp' else '-std=c11']
        if 'sieć_Stos' in ścieżka_2.parts: argumenty += ['-I'+str(Project_korzeń/'sieć_Stos'),'-I'+str(Project_korzeń/'vendor/lwip/src/include')]
        if 'C_kompilator' in ścieżka_2.parts:
            argumenty += ['-I'+str(Project_korzeń/'C_kompilator'),'-I'+str(Project_korzeń/'vendor/tinycc'),'-I'+str(Project_korzeń/'build/ccompiler'),
                    '-isystem',str(Project_korzeń.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_mostek' in ścieżka_2.parts:
            argumenty += ['-I'+str(Project_korzeń/'PYTHON_mostek'),'-I'+str(Project_korzeń/'build/micropython-1.24.1'),'-I'+str(Project_korzeń/'build/python'),'-isystem','/usr/include/newlib']
        if 'zdalny_WARTOŚĆ' in ścieżka_2.parts:
            argumenty += ['-isystem', '/usr/include/newlib']
        if 'dystrybucja_WARTOŚĆ' in ścieżka_2.parts: argumenty += ['-D__JKOROS__=1']
        if ścieżka_2.name=='pakiet.c': argumenty += ['-I'+str(Project_korzeń/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        grupa_WARTOŚĆ = (C_źródło.c_char_p*len(argumenty))(*[wpis_WARTOŚĆ.encode() for wpis_WARTOŚĆ in argumenty])
        jednostka_translacji = Analiza_WARTOŚĆ(WYSZUKAJ_INDEKS,str(ścieżka_2).encode(),grupa_WARTOŚĆ,len(argumenty),None,0,1)
        for INDEKS in range(진단수(jednostka_translacji)):
            진단 = 진단얻기(jednostka_translacji,INDEKS)
            if stopień_WARTOŚĆ(진단)>=3: 오류들.append((str(ścieżka_2.relative_to(Project_korzeń)),tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(wpis_WARTOŚĆ,nadrzędny_WARTOŚĆ,dane):
            nazwa_pliku,przesunąć_WARTOŚĆ_450fc799,wiersz_wejścia = indeks_pozycji(wpis_WARTOŚĆ)
            if nazwa_pliku not in 소유파일: return 2 if wpis_WARTOŚĆ.Rodzaj_WARTOŚĆ==300 else 1
            낱말 = tekst(pobrać_nazwa(wpis_WARTOŚĆ))
            if not 낱말 or any(ord(znak_WARTOŚĆ)>127 for znak_WARTOŚĆ in 낱말): return 2
            if wpis_WARTOŚĆ.Rodzaj_WARTOŚĆ in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIKATOWE_WARTOŚĆ = tekst(UNIKATOWE_nazwa(wpis_WARTOŚĆ)) or nazwa_pliku+':'+str(przesunąć_WARTOŚĆ_450fc799)
                선언들[UNIKATOWE_WARTOŚĆ] = {'nazwa_pliku':nazwa_pliku,'przesunąć_WARTOŚĆ_450fc799':przesunąć_WARTOŚĆ_450fc799,'wiersz_wejścia':wiersz_wejścia,'Rodzaj_WARTOŚĆ':wpis_WARTOŚĆ.Rodzaj_WARTOŚĆ,'Nazwa':낱말,'Połącz':połączenie_Rodzaj(wpis_WARTOŚĆ)}
                참조들.append((nazwa_pliku,przesunąć_WARTOŚĆ_450fc799,낱말,UNIKATOWE_WARTOŚĆ))
            else:
                odwołanie = pobrać_odwołanie(wpis_WARTOŚĆ)
                odwołanie_Plik,_,_ = indeks_pozycji(odwołanie)
                if odwołanie_Plik in 소유파일:
                    UNIKATOWE_WARTOŚĆ = tekst(UNIKATOWE_nazwa(odwołanie)); 참조들.append((nazwa_pliku,przesunąć_WARTOŚĆ_450fc799,tekst(pobrać_nazwa(odwołanie)),UNIKATOWE_WARTOŚĆ))
            return 2
        방문(korzeń_WARTOŚĆ(jednostka_translacji),살피기,None)
        zakończ_program(jednostka_translacji)
    cel_WARTOŚĆ = Project_korzeń/'build/한국어화/시언어분석.json'
    cel_WARTOŚĆ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {nazwa_pliku:hashlib.sha256(Path(nazwa_pliku).read_bytes()).hexdigest() for nazwa_pliku in sorted(소유파일)}
    cel_WARTOŚĆ.write_text(json.dumps({'deklaracja':선언들,'odwołanie':참조들,'błąd':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklaracja',len(선언들),'odwołanie',len(참조들),'błąd',len(오류들))
    for błąd in 오류들: print(*błąd)

if __name__=='__main__': Wykonaj_polecenie()
