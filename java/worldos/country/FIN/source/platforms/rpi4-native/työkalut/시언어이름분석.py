#!/usr/bin/env python3
"""libclang esittely·viite 위치를 수집한다. ulkoinen_ARVO 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_lähde
import hashlib
import json
from pathlib import Path

aloite_juuri = Path(__file__).resolve().parents[1]
toteutus = C_lähde.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class merkkijono_ARVO(C_lähde.Structure): _fields_ = [('data',C_lähde.c_void_p),('näyttää_ARVO',C_lähde.c_uint)]
class kohdistin_ARVO(C_lähde.Structure): _fields_ = [('종류',C_lähde.c_uint),('보조',C_lähde.c_int),('data',C_lähde.c_void_p*3)]
class paikka(C_lähde.Structure): _fields_ = [('data',C_lähde.c_void_p*2),('SIIRTYMÄ_ARVO',C_lähde.c_uint)]
def funktio_ARVO(Nimi, palauttaa_KR, *argumentit):
    merkintä_ARVO_962f286b = getattr(toteutus, Nimi); merkintä_ARVO_962f286b.restype = palauttaa_KR; merkintä_ARVO_962f286b.argtypes = list(argumentit); return merkintä_ARVO_962f286b
noutaa_SMS = funktio_ARVO('clang_getCString',C_lähde.c_char_p,merkkijono_ARVO)
julkaista_SMS = funktio_ARVO('clang_disposeString',None,merkkijono_ARVO)
def teksti(ARVO):
    TULOS = (noutaa_SMS(ARVO) or b'').decode('utf-8'); julkaista_SMS(ARVO); return TULOS
noutaa_nimi = funktio_ARVO('clang_getCursorSpelling',merkkijono_ARVO,kohdistin_ARVO)
noutaa_viite = funktio_ARVO('clang_getCursorReferenced',kohdistin_ARVO,kohdistin_ARVO)
noutaa_toimi = funktio_ARVO('clang_getCursorLocation',paikka,kohdistin_ARVO)
Tiedosto_toimi = funktio_ARVO('clang_getFileLocation',None,paikka,C_lähde.POINTER(C_lähde.c_void_p),C_lähde.POINTER(C_lähde.c_uint),C_lähde.POINTER(C_lähde.c_uint),C_lähde.POINTER(C_lähde.c_uint))
Tiedosto_merkintä_nimi = funktio_ARVO('clang_getFileName',merkkijono_ARVO,C_lähde.c_void_p)
AINUTKERTAISET_ARVOT_nimi = funktio_ARVO('clang_getCursorUSR',merkkijono_ARVO,kohdistin_ARVO)
연결종류 = funktio_ARVO('clang_getCursorLinkage',C_lähde.c_uint,kohdistin_ARVO)
방문형 = C_lähde.CFUNCTYPE(C_lähde.c_uint,kohdistin_ARVO,kohdistin_ARVO,C_lähde.c_void_p)
방문 = funktio_ARVO('clang_visitChildren',C_lähde.c_uint,kohdistin_ARVO,방문형,C_lähde.c_void_p)
generoida = funktio_ARVO('clang_createIndex',C_lähde.c_void_p,C_lähde.c_int,C_lähde.c_int)
Analysoi_ARVO = funktio_ARVO('clang_parseTranslationUnit',C_lähde.c_void_p,C_lähde.c_void_p,C_lähde.c_char_p,C_lähde.POINTER(C_lähde.c_char_p),C_lähde.c_int,C_lähde.c_void_p,C_lähde.c_uint,C_lähde.c_uint)
juuri_ARVO = funktio_ARVO('clang_getTranslationUnitCursor',kohdistin_ARVO,C_lähde.c_void_p)
lopeta_ohjelma = funktio_ARVO('clang_disposeTranslationUnit',None,C_lähde.c_void_p)
진단수 = funktio_ARVO('clang_getNumDiagnostics',C_lähde.c_uint,C_lähde.c_void_p)
진단얻기 = funktio_ARVO('clang_getDiagnostic',C_lähde.c_void_p,C_lähde.c_void_p,C_lähde.c_uint)
vakavuus_ARVO = funktio_ARVO('clang_getDiagnosticSeverity',C_lähde.c_uint,C_lähde.c_void_p)
진단문 = funktio_ARVO('clang_getDiagnosticSpelling',merkkijono_ARVO,C_lähde.c_void_p)
진단해제 = funktio_ARVO('clang_disposeDiagnostic',None,C_lähde.c_void_p)

def sijainti(merkintä_ARVO_962f286b):
    tiedoston_nimi = C_lähde.c_void_p(); syöterivi = C_lähde.c_uint(); paikka_merkintä = C_lähde.c_uint(); SIIRTYMÄ_ARVO = C_lähde.c_uint()
    Tiedosto_toimi(noutaa_toimi(merkintä_ARVO_962f286b),C_lähde.byref(tiedoston_nimi),C_lähde.byref(syöterivi),C_lähde.byref(paikka_merkintä),C_lähde.byref(SIIRTYMÄ_ARVO))
    return (teksti(Tiedosto_merkintä_nimi(tiedoston_nimi)) if tiedoston_nimi else '', SIIRTYMÄ_ARVO.value, syöterivi.value)

def Suorita_komento():
    HAKU_INDEKSI = generoida(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kääntäjä_työkalu.c는 oma esittely 없이 TinyCC ulkoinen_ARVO 단일 KÄÄNNÄ_lähde 단위만 포함한다.
    # ulkoinen_ARVO 선언을 oma 이름으로 세지 않으며, todellinen_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(polku_2.resolve()) for polku_2 in aloite_juuri.rglob('*') if polku_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(polku_2.relative_to(aloite_juuri).parts)&{'build','dist','vendor','__pycache__'}
              and polku_2.relative_to(aloite_juuri).as_posix() != 'C_kääntäjä/kääntäjä_työkalu.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(aloite_juuri/'käyttäjätila'),
          '-I'+str(aloite_juuri.parents[1]/'posix-kor/arm64-native/esittelyt'),'-I'+str(aloite_juuri/'build'),'-I'+str(aloite_juuri/'build/user'),
          '-I'+str(aloite_juuri/'build/remote'),'-I'+str(aloite_juuri/'vendor/bearssl/inc'),
          '-I'+str(aloite_juuri/'vendor/bearssl/src'),'-I'+str(aloite_juuri/'vendor/libassh/src'),
          '-I'+str(aloite_juuri/'vendor/lwip/src/include'),'-I'+str(aloite_juuri/'verkko_Pino'),
          '-I'+str(aloite_juuri/'etä_ARVO'),'-I'+str(aloite_juuri/'C_kääntäjä')]
    for polku_2 in sorted(Path(Nimi) for Nimi in 소유파일 if Nimi.endswith(('.c','.cpp'))):
        argumentit = 공통 + ['-std=c++11' if polku_2.suffix=='.cpp' else '-std=c11']
        if 'verkko_Pino' in polku_2.parts: argumentit += ['-I'+str(aloite_juuri/'verkko_Pino'),'-I'+str(aloite_juuri/'vendor/lwip/src/include')]
        if 'C_kääntäjä' in polku_2.parts:
            argumentit += ['-I'+str(aloite_juuri/'C_kääntäjä'),'-I'+str(aloite_juuri/'vendor/tinycc'),'-I'+str(aloite_juuri/'build/ccompiler'),
                    '-isystem',str(aloite_juuri.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_silta' in polku_2.parts:
            argumentit += ['-I'+str(aloite_juuri/'PYTHON_silta'),'-I'+str(aloite_juuri/'build/micropython-1.24.1'),'-I'+str(aloite_juuri/'build/python'),'-isystem','/usr/include/newlib']
        if 'etä_ARVO' in polku_2.parts:
            argumentit += ['-isystem', '/usr/include/newlib']
        if 'jakelu_ARVO' in polku_2.parts: argumentit += ['-D__JKOROS__=1']
        if polku_2.name=='nippu.c': argumentit += ['-I'+str(aloite_juuri/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Ryhmä_ARVO = (C_lähde.c_char_p*len(argumentit))(*[merkintä_ARVO_962f286b.encode() for merkintä_ARVO_962f286b in argumentit])
        Käännös_osio = Analysoi_ARVO(HAKU_INDEKSI,str(polku_2).encode(),Ryhmä_ARVO,len(argumentit),None,0,1)
        for INDEKSI in range(진단수(Käännös_osio)):
            진단 = 진단얻기(Käännös_osio,INDEKSI)
            if vakavuus_ARVO(진단)>=3: 오류들.append((str(polku_2.relative_to(aloite_juuri)),teksti(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(merkintä_ARVO_962f286b,pää_ARVO,data):
            tiedoston_nimi,SIIRTYMÄ_ARVO,syöterivi = sijainti(merkintä_ARVO_962f286b)
            if tiedoston_nimi not in 소유파일: return 2 if merkintä_ARVO_962f286b.종류==300 else 1
            낱말 = teksti(noutaa_nimi(merkintä_ARVO_962f286b))
            if not 낱말 or any(ord(merkki_ARVO)>127 for merkki_ARVO in 낱말): return 2
            if merkintä_ARVO_962f286b.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                AINUTKERTAISET_ARVOT_ARVO = teksti(AINUTKERTAISET_ARVOT_nimi(merkintä_ARVO_962f286b)) or tiedoston_nimi+':'+str(SIIRTYMÄ_ARVO)
                선언들[AINUTKERTAISET_ARVOT_ARVO] = {'tiedoston_nimi':tiedoston_nimi,'SIIRTYMÄ_ARVO':SIIRTYMÄ_ARVO,'syöterivi':syöterivi,'종류':merkintä_ARVO_962f286b.종류,'Nimi':낱말,'Yhdistä':연결종류(merkintä_ARVO_962f286b)}
                참조들.append((tiedoston_nimi,SIIRTYMÄ_ARVO,낱말,AINUTKERTAISET_ARVOT_ARVO))
            else:
                viite = noutaa_viite(merkintä_ARVO_962f286b)
                viite_Tiedosto,_,_ = sijainti(viite)
                if viite_Tiedosto in 소유파일:
                    AINUTKERTAISET_ARVOT_ARVO = teksti(AINUTKERTAISET_ARVOT_nimi(viite)); 참조들.append((tiedoston_nimi,SIIRTYMÄ_ARVO,teksti(noutaa_nimi(viite)),AINUTKERTAISET_ARVOT_ARVO))
            return 2
        방문(juuri_ARVO(Käännös_osio),살피기,None)
        lopeta_ohjelma(Käännös_osio)
    kohde_ARVO = aloite_juuri/'build/한국어화/시언어분석.json'
    kohde_ARVO.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {tiedoston_nimi:hashlib.sha256(Path(tiedoston_nimi).read_bytes()).hexdigest() for tiedoston_nimi in sorted(소유파일)}
    kohde_ARVO.write_text(json.dumps({'esittely':선언들,'viite':참조들,'VIRHE':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('esittely',len(선언들),'viite',len(참조들),'VIRHE',len(오류들))
    for VIRHE in 오류들: print(*VIRHE)

if __name__=='__main__': Suorita_komento()
