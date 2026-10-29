#!/usr/bin/env python3
"""libclang aangifte·verwijzen 위치를 수집한다. extern_WAARDE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_bron
import hashlib
import json
from pathlib import Path

Taken_wortel = Path(__file__).resolve().parents[1]
implementatie = C_bron.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class tekenreeks_WAARDE(C_bron.Structure): _fields_ = [('gegevens',C_bron.c_void_p),('weergeven_WAARDE',C_bron.c_uint)]
class cursor_WAARDE(C_bron.Structure): _fields_ = [('soort_WAARDE',C_bron.c_uint),('보조',C_bron.c_int),('gegevens',C_bron.c_void_p*3)]
class positie(C_bron.Structure): _fields_ = [('gegevens',C_bron.c_void_p*2),('VERSCHUIVING_WAARDE',C_bron.c_uint)]
def FUNCTIE_WAARDE(Naam, Retour_HR, *argumenten):
    invoer_WAARDE_962f286b = getattr(implementatie, Naam); invoer_WAARDE_962f286b.restype = Retour_HR; invoer_WAARDE_962f286b.argtypes = list(argumenten); return invoer_WAARDE_962f286b
ophalen_sms = FUNCTIE_WAARDE('clang_getCString',C_bron.c_char_p,tekenreeks_WAARDE)
versie_sms = FUNCTIE_WAARDE('clang_disposeString',None,tekenreeks_WAARDE)
def tekst(WAARDE):
    resultaat = (ophalen_sms(WAARDE) or b'').decode('utf-8'); versie_sms(WAARDE); return resultaat
ophalen_naam = FUNCTIE_WAARDE('clang_getCursorSpelling',tekenreeks_WAARDE,cursor_WAARDE)
ophalen_verwijzen = FUNCTIE_WAARDE('clang_getCursorReferenced',cursor_WAARDE,cursor_WAARDE)
ophalen_functie = FUNCTIE_WAARDE('clang_getCursorLocation',positie,cursor_WAARDE)
Bestand_functie = FUNCTIE_WAARDE('clang_getFileLocation',None,positie,C_bron.POINTER(C_bron.c_void_p),C_bron.POINTER(C_bron.c_uint),C_bron.POINTER(C_bron.c_uint),C_bron.POINTER(C_bron.c_uint))
Bestand_invoer_naam = FUNCTIE_WAARDE('clang_getFileName',tekenreeks_WAARDE,C_bron.c_void_p)
UNIEK_naam = FUNCTIE_WAARDE('clang_getCursorUSR',tekenreeks_WAARDE,cursor_WAARDE)
verbinding_soort = FUNCTIE_WAARDE('clang_getCursorLinkage',C_bron.c_uint,cursor_WAARDE)
방문형 = C_bron.CFUNCTYPE(C_bron.c_uint,cursor_WAARDE,cursor_WAARDE,C_bron.c_void_p)
방문 = FUNCTIE_WAARDE('clang_visitChildren',C_bron.c_uint,cursor_WAARDE,방문형,C_bron.c_void_p)
genereren = FUNCTIE_WAARDE('clang_createIndex',C_bron.c_void_p,C_bron.c_int,C_bron.c_int)
Analyseren_WAARDE = FUNCTIE_WAARDE('clang_parseTranslationUnit',C_bron.c_void_p,C_bron.c_void_p,C_bron.c_char_p,C_bron.POINTER(C_bron.c_char_p),C_bron.c_int,C_bron.c_void_p,C_bron.c_uint,C_bron.c_uint)
wortel_WAARDE = FUNCTIE_WAARDE('clang_getTranslationUnitCursor',cursor_WAARDE,C_bron.c_void_p)
sluiten_app = FUNCTIE_WAARDE('clang_disposeTranslationUnit',None,C_bron.c_void_p)
진단수 = FUNCTIE_WAARDE('clang_getNumDiagnostics',C_bron.c_uint,C_bron.c_void_p)
진단얻기 = FUNCTIE_WAARDE('clang_getDiagnostic',C_bron.c_void_p,C_bron.c_void_p,C_bron.c_uint)
ernst_WAARDE = FUNCTIE_WAARDE('clang_getDiagnosticSeverity',C_bron.c_uint,C_bron.c_void_p)
진단문 = FUNCTIE_WAARDE('clang_getDiagnosticSpelling',tekenreeks_WAARDE,C_bron.c_void_p)
진단해제 = FUNCTIE_WAARDE('clang_disposeDiagnostic',None,C_bron.c_void_p)

def plaatsingsindex(invoer_WAARDE_962f286b):
    bestand = C_bron.c_void_p(); invoerregel = C_bron.c_uint(); sleuf_invoer = C_bron.c_uint(); VERSCHUIVING_WAARDE = C_bron.c_uint()
    Bestand_functie(ophalen_functie(invoer_WAARDE_962f286b),C_bron.byref(bestand),C_bron.byref(invoerregel),C_bron.byref(sleuf_invoer),C_bron.byref(VERSCHUIVING_WAARDE))
    return (tekst(Bestand_invoer_naam(bestand)) if bestand else '', VERSCHUIVING_WAARDE.value, invoerregel.value)

def Uitvoeren_opdracht():
    ZOEKEN_INDEX = genereren(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # compiler_hulpmiddel.c는 Eigen aangifte 없이 TinyCC extern_WAARDE 단일 VERTALEN_bron 단위만 포함한다.
    # extern_WAARDE 선언을 Eigen 이름으로 세지 않으며, werkelijk_gegevens 빌드에서는 계속 컴파일한다.
    소유파일 = {str(pad.resolve()) for pad in Taken_wortel.rglob('*') if pad.suffix in ('.c','.h','.cpp','.inc')
              and not set(pad.relative_to(Taken_wortel).parts)&{'build','dist','vendor','__pycache__'}
              and pad.relative_to(Taken_wortel).as_posix() != 'C_compiler/compiler_hulpmiddel.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Taken_wortel/'gebruikersruimte'),
          '-I'+str(Taken_wortel.parents[1]/'posix-kor/arm64-native/declaraties'),'-I'+str(Taken_wortel/'build'),'-I'+str(Taken_wortel/'build/user'),
          '-I'+str(Taken_wortel/'build/remote'),'-I'+str(Taken_wortel/'vendor/bearssl/inc'),
          '-I'+str(Taken_wortel/'vendor/bearssl/src'),'-I'+str(Taken_wortel/'vendor/libassh/src'),
          '-I'+str(Taken_wortel/'vendor/lwip/src/include'),'-I'+str(Taken_wortel/'net_stack'),
          '-I'+str(Taken_wortel/'extern_WAARDE_28edcfa1'),'-I'+str(Taken_wortel/'C_compiler')]
    for pad in sorted(Path(Naam) for Naam in 소유파일 if Naam.endswith(('.c','.cpp'))):
        argumenten = 공통 + ['-std=c++11' if pad.suffix=='.cpp' else '-std=c11']
        if 'net_stack' in pad.parts: argumenten += ['-I'+str(Taken_wortel/'net_stack'),'-I'+str(Taken_wortel/'vendor/lwip/src/include')]
        if 'C_compiler' in pad.parts:
            argumenten += ['-I'+str(Taken_wortel/'C_compiler'),'-I'+str(Taken_wortel/'vendor/tinycc'),'-I'+str(Taken_wortel/'build/ccompiler'),
                    '-isystem',str(Taken_wortel.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_brug' in pad.parts:
            argumenten += ['-I'+str(Taken_wortel/'PYTHON_brug'),'-I'+str(Taken_wortel/'build/micropython-1.24.1'),'-I'+str(Taken_wortel/'build/python'),'-isystem','/usr/include/newlib']
        if 'extern_WAARDE_28edcfa1' in pad.parts:
            argumenten += ['-isystem', '/usr/include/newlib']
        if 'distributie_WAARDE' in pad.parts: argumenten += ['-D__JKOROS__=1']
        if pad.name=='bundel.c': argumenten += ['-I'+str(Taken_wortel/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Groep_WAARDE = (C_bron.c_char_p*len(argumenten))(*[invoer_WAARDE_962f286b.encode() for invoer_WAARDE_962f286b in argumenten])
        Vertaling_les = Analyseren_WAARDE(ZOEKEN_INDEX,str(pad).encode(),Groep_WAARDE,len(argumenten),None,0,1)
        for INDEX in range(진단수(Vertaling_les)):
            진단 = 진단얻기(Vertaling_les,INDEX)
            if ernst_WAARDE(진단)>=3: 오류들.append((str(pad.relative_to(Taken_wortel)),tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(invoer_WAARDE_962f286b,bovenliggend_WAARDE,gegevens):
            bestand,VERSCHUIVING_WAARDE,invoerregel = plaatsingsindex(invoer_WAARDE_962f286b)
            if bestand not in 소유파일: return 2 if invoer_WAARDE_962f286b.soort_WAARDE==300 else 1
            낱말 = tekst(ophalen_naam(invoer_WAARDE_962f286b))
            if not 낱말 or any(ord(teken_WAARDE)>127 for teken_WAARDE in 낱말): return 2
            if invoer_WAARDE_962f286b.soort_WAARDE in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIEK_WAARDE = tekst(UNIEK_naam(invoer_WAARDE_962f286b)) or bestand+':'+str(VERSCHUIVING_WAARDE)
                선언들[UNIEK_WAARDE] = {'bestand':bestand,'VERSCHUIVING_WAARDE':VERSCHUIVING_WAARDE,'invoerregel':invoerregel,'soort_WAARDE':invoer_WAARDE_962f286b.soort_WAARDE,'Naam':낱말,'Verbinden':verbinding_soort(invoer_WAARDE_962f286b)}
                참조들.append((bestand,VERSCHUIVING_WAARDE,낱말,UNIEK_WAARDE))
            else:
                verwijzen = ophalen_verwijzen(invoer_WAARDE_962f286b)
                verwijzen_Bestand,_,_ = plaatsingsindex(verwijzen)
                if verwijzen_Bestand in 소유파일:
                    UNIEK_WAARDE = tekst(UNIEK_naam(verwijzen)); 참조들.append((bestand,VERSCHUIVING_WAARDE,tekst(ophalen_naam(verwijzen)),UNIEK_WAARDE))
            return 2
        방문(wortel_WAARDE(Vertaling_les),살피기,None)
        sluiten_app(Vertaling_les)
    doel_WAARDE = Taken_wortel/'build/한국어화/시언어분석.json'
    doel_WAARDE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {bestand:hashlib.sha256(Path(bestand).read_bytes()).hexdigest() for bestand in sorted(소유파일)}
    doel_WAARDE.write_text(json.dumps({'aangifte':선언들,'verwijzen':참조들,'fout':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('aangifte',len(선언들),'verwijzen',len(참조들),'fout',len(오류들))
    for fout in 오류들: print(*fout)

if __name__=='__main__': Uitvoeren_opdracht()
