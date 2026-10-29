#!/usr/bin/env python3
"""libclang deklaratsioon·viide 위치를 수집한다. väline_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as _15_lähe
import hashlib
import json
from pathlib import Path

Project_juur = Path(__file__).resolve().parents[1]
구현 = _15_lähe.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class string_VALUE(_15_lähe.Structure): _fields_ = [('andmed',_15_lähe.c_void_p),('saade_VALUE',_15_lähe.c_uint)]
class kursor_VALUE(_15_lähe.Structure): _fields_ = [('종류',_15_lähe.c_uint),('보조',_15_lähe.c_int),('andmed',_15_lähe.c_void_p*3)]
class Asukoht(_15_lähe.Structure): _fields_ = [('andmed',_15_lähe.c_void_p*2),('nihe_VALUE',_15_lähe.c_uint)]
def FUNCTION_VALUE(Nimi_2, tagasi_saatma_näitaja, *Argumendid):
    kirje_VALUE = getattr(구현, Nimi_2); kirje_VALUE.restype = tagasi_saatma_näitaja; kirje_VALUE.argtypes = list(Argumendid); return kirje_VALUE
tooma_SMS = FUNCTION_VALUE('clang_getCString',_15_lähe.c_char_p,string_VALUE)
vabastama_SMS = FUNCTION_VALUE('clang_disposeString',None,string_VALUE)
def Tekst(VALUE):
    TULEMUS = (tooma_SMS(VALUE) or b'').decode('utf-8'); vabastama_SMS(VALUE); return TULEMUS
tooma_nimetus = FUNCTION_VALUE('clang_getCursorSpelling',string_VALUE,kursor_VALUE)
tooma_viide = FUNCTION_VALUE('clang_getCursorReferenced',kursor_VALUE,kursor_VALUE)
tooma_ametikoht = FUNCTION_VALUE('clang_getCursorLocation',Asukoht,kursor_VALUE)
Fail_ametikoht = FUNCTION_VALUE('clang_getFileLocation',None,Asukoht,_15_lähe.POINTER(_15_lähe.c_void_p),_15_lähe.POINTER(_15_lähe.c_uint),_15_lähe.POINTER(_15_lähe.c_uint),_15_lähe.POINTER(_15_lähe.c_uint))
Fail_kirje_nimetus = FUNCTION_VALUE('clang_getFileName',string_VALUE,_15_lähe.c_void_p)
UNIQUE_nimetus = FUNCTION_VALUE('clang_getCursorUSR',string_VALUE,kursor_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',_15_lähe.c_uint,kursor_VALUE)
방문형 = _15_lähe.CFUNCTYPE(_15_lähe.c_uint,kursor_VALUE,kursor_VALUE,_15_lähe.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',_15_lähe.c_uint,kursor_VALUE,방문형,_15_lähe.c_void_p)
genereerima = FUNCTION_VALUE('clang_createIndex',_15_lähe.c_void_p,_15_lähe.c_int,_15_lähe.c_int)
Analüüs_VALUE = FUNCTION_VALUE('clang_parseTranslationUnit',_15_lähe.c_void_p,_15_lähe.c_void_p,_15_lähe.c_char_p,_15_lähe.POINTER(_15_lähe.c_char_p),_15_lähe.c_int,_15_lähe.c_void_p,_15_lähe.c_uint,_15_lähe.c_uint)
juur_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursor_VALUE,_15_lähe.c_void_p)
välju_programm = FUNCTION_VALUE('clang_disposeTranslationUnit',None,_15_lähe.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',_15_lähe.c_uint,_15_lähe.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',_15_lähe.c_void_p,_15_lähe.c_void_p,_15_lähe.c_uint)
raskusaste_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',_15_lähe.c_uint,_15_lähe.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',string_VALUE,_15_lähe.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,_15_lähe.c_void_p)

def asukohaindeks(kirje_VALUE):
    Fail = _15_lähe.c_void_p(); Joon = _15_lähe.c_uint(); 칸 = _15_lähe.c_uint(); nihe_VALUE = _15_lähe.c_uint()
    Fail_ametikoht(tooma_ametikoht(kirje_VALUE),_15_lähe.byref(Fail),_15_lähe.byref(Joon),_15_lähe.byref(칸),_15_lähe.byref(nihe_VALUE))
    return (Tekst(Fail_kirje_nimetus(Fail)) if Fail else '', nihe_VALUE.value, Joon.value)

def Täida_käsk():
    LOOKUP_INDEX = genereerima(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilaator_tööriist.c는 oma deklaratsioon 없이 TinyCC väline_VALUE 단일 Tõlgi_lähe 단위만 포함한다.
    # väline_VALUE 선언을 oma 이름으로 세지 않으며, tegelik_andmed 빌드에서는 계속 컴파일한다.
    소유파일 = {str(RADA.resolve()) for RADA in Project_juur.rglob('*') if RADA.suffix in ('.c','.h','.cpp','.inc')
              and not set(RADA.relative_to(Project_juur).parts)&{'build','dist','vendor','__pycache__'}
              and RADA.relative_to(Project_juur).as_posix() != '_15_kompilaator/kompilaator_tööriist.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_juur/'kasutaja'),
          '-I'+str(Project_juur.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_juur/'build'),'-I'+str(Project_juur/'build/user'),
          '-I'+str(Project_juur/'build/remote'),'-I'+str(Project_juur/'vendor/bearssl/inc'),
          '-I'+str(Project_juur/'vendor/bearssl/src'),'-I'+str(Project_juur/'vendor/libassh/src'),
          '-I'+str(Project_juur/'vendor/lwip/src/include'),'-I'+str(Project_juur/'võrk_Virn'),
          '-I'+str(Project_juur/'kauge_VALUE'),'-I'+str(Project_juur/'_15_kompilaator')]
    for RADA in sorted(Path(Nimi_2) for Nimi_2 in 소유파일 if Nimi_2.endswith(('.c','.cpp'))):
        Argumendid = 공통 + ['-std=c++11' if RADA.suffix=='.cpp' else '-std=c11']
        if 'võrk_Virn' in RADA.parts: Argumendid += ['-I'+str(Project_juur/'võrk_Virn'),'-I'+str(Project_juur/'vendor/lwip/src/include')]
        if '_15_kompilaator' in RADA.parts:
            Argumendid += ['-I'+str(Project_juur/'_15_kompilaator'),'-I'+str(Project_juur/'vendor/tinycc'),'-I'+str(Project_juur/'build/ccompiler'),
                    '-isystem',str(Project_juur.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_sild' in RADA.parts:
            Argumendid += ['-I'+str(Project_juur/'PYTHON_sild'),'-I'+str(Project_juur/'build/micropython-1.24.1'),'-I'+str(Project_juur/'build/python'),'-isystem','/usr/include/newlib']
        if 'kauge_VALUE' in RADA.parts:
            Argumendid += ['-isystem', '/usr/include/newlib']
        if 'turustus_VALUE' in RADA.parts: Argumendid += ['-D__JKOROS__=1']
        if RADA.name=='kogum.c': Argumendid += ['-I'+str(Project_juur/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Rühm_VALUE = (_15_lähe.c_char_p*len(Argumendid))(*[kirje_VALUE.encode() for kirje_VALUE in Argumendid])
        Tõlkimine_ühik = Analüüs_VALUE(LOOKUP_INDEX,str(RADA).encode(),Rühm_VALUE,len(Argumendid),None,0,1)
        for INDEX in range(진단수(Tõlkimine_ühik)):
            진단 = 진단얻기(Tõlkimine_ühik,INDEX)
            if raskusaste_VALUE(진단)>=3: 오류들.append((str(RADA.relative_to(Project_juur)),Tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(kirje_VALUE,ema_VALUE,andmed):
            Fail,nihe_VALUE,Joon = asukohaindeks(kirje_VALUE)
            if Fail not in 소유파일: return 2 if kirje_VALUE.종류==300 else 1
            낱말 = Tekst(tooma_nimetus(kirje_VALUE))
            if not 낱말 or any(ord(märk_VALUE)>127 for märk_VALUE in 낱말): return 2
            if kirje_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Tekst(UNIQUE_nimetus(kirje_VALUE)) or Fail+':'+str(nihe_VALUE)
                선언들[UNIQUE_VALUE] = {'Fail':Fail,'nihe_VALUE':nihe_VALUE,'Joon':Joon,'종류':kirje_VALUE.종류,'Nimi_2':낱말,'Ühendu':연결종류(kirje_VALUE)}
                참조들.append((Fail,nihe_VALUE,낱말,UNIQUE_VALUE))
            else:
                viide = tooma_viide(kirje_VALUE)
                viide_Fail,_,_ = asukohaindeks(viide)
                if viide_Fail in 소유파일:
                    UNIQUE_VALUE = Tekst(UNIQUE_nimetus(viide)); 참조들.append((Fail,nihe_VALUE,Tekst(tooma_nimetus(viide)),UNIQUE_VALUE))
            return 2
        방문(juur_VALUE(Tõlkimine_ühik),살피기,None)
        välju_programm(Tõlkimine_ühik)
    sihtkoht_VALUE = Project_juur/'build/한국어화/시언어분석.json'
    sihtkoht_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fail:hashlib.sha256(Path(Fail).read_bytes()).hexdigest() for Fail in sorted(소유파일)}
    sihtkoht_VALUE.write_text(json.dumps({'deklaratsioon':선언들,'viide':참조들,'VIGA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklaratsioon',len(선언들),'viide',len(참조들),'VIGA',len(오류들))
    for VIGA in 오류들: print(*VIGA)

if __name__=='__main__': Täida_käsk()
