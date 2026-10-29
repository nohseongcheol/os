#!/usr/bin/env python3
"""libclang deklarācija·Uzziņas 위치를 수집한다. ārējs_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_avots
import hashlib
import json
from pathlib import Path

Project_sakne = Path(__file__).resolve().parents[1]
구현 = C_avots.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class virkne_VALUE(C_avots.Structure): _fields_ = [('dati',C_avots.c_void_p),('rādīt_VALUE',C_avots.c_uint)]
class kursors_VALUE(C_avots.Structure): _fields_ = [('종류',C_avots.c_uint),('보조',C_avots.c_int),('dati',C_avots.c_void_p*3)]
class Novietojums(C_avots.Structure): _fields_ = [('dati',C_avots.c_void_p*2),('Nobīde_VALUE',C_avots.c_uint)]
def FUNCTION_VALUE(Nosaukums, atdot_mērs, *Parametri):
    ievade_VALUE = getattr(구현, Nosaukums); ievade_VALUE.restype = atdot_mērs; ievade_VALUE.argtypes = list(Parametri); return ievade_VALUE
iegūt_SMS = FUNCTION_VALUE('clang_getCString',C_avots.c_char_p,virkne_VALUE)
izlaist_SMS = FUNCTION_VALUE('clang_disposeString',None,virkne_VALUE)
def Teksts(VALUE):
    mērs = (iegūt_SMS(VALUE) or b'').decode('utf-8'); izlaist_SMS(VALUE); return mērs
iegūt_nosaukums = FUNCTION_VALUE('clang_getCursorSpelling',virkne_VALUE,kursors_VALUE)
iegūt_Uzziņas = FUNCTION_VALUE('clang_getCursorReferenced',kursors_VALUE,kursors_VALUE)
iegūt_amats = FUNCTION_VALUE('clang_getCursorLocation',Novietojums,kursors_VALUE)
Fails_amats = FUNCTION_VALUE('clang_getFileLocation',None,Novietojums,C_avots.POINTER(C_avots.c_void_p),C_avots.POINTER(C_avots.c_uint),C_avots.POINTER(C_avots.c_uint),C_avots.POINTER(C_avots.c_uint))
Fails_ievade_nosaukums = FUNCTION_VALUE('clang_getFileName',virkne_VALUE,C_avots.c_void_p)
UNIQUE_nosaukums = FUNCTION_VALUE('clang_getCursorUSR',virkne_VALUE,kursors_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',C_avots.c_uint,kursors_VALUE)
방문형 = C_avots.CFUNCTYPE(C_avots.c_uint,kursors_VALUE,kursors_VALUE,C_avots.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',C_avots.c_uint,kursors_VALUE,방문형,C_avots.c_void_p)
ģenerēt = FUNCTION_VALUE('clang_createIndex',C_avots.c_void_p,C_avots.c_int,C_avots.c_int)
analīze_VALUE = FUNCTION_VALUE('clang_parseTranslationUnit',C_avots.c_void_p,C_avots.c_void_p,C_avots.c_char_p,C_avots.POINTER(C_avots.c_char_p),C_avots.c_int,C_avots.c_void_p,C_avots.c_uint,C_avots.c_uint)
sakne_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kursors_VALUE,C_avots.c_void_p)
iziet_programma = FUNCTION_VALUE('clang_disposeTranslationUnit',None,C_avots.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',C_avots.c_uint,C_avots.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',C_avots.c_void_p,C_avots.c_void_p,C_avots.c_uint)
nozīmīgums_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',C_avots.c_uint,C_avots.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',virkne_VALUE,C_avots.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,C_avots.c_void_p)

def pozīcijas_indekss(ievade_VALUE):
    Fails = C_avots.c_void_p(); Līniju = C_avots.c_uint(); 칸 = C_avots.c_uint(); Nobīde_VALUE = C_avots.c_uint()
    Fails_amats(iegūt_amats(ievade_VALUE),C_avots.byref(Fails),C_avots.byref(Līniju),C_avots.byref(칸),C_avots.byref(Nobīde_VALUE))
    return (Teksts(Fails_ievade_nosaukums(Fails)) if Fails else '', Nobīde_VALUE.value, Līniju.value)

def Izpildīt_komanda():
    LOOKUP_INDEX = ģenerēt(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilators_rīks.c는 savs deklarācija 없이 TinyCC ārējs_VALUE 단일 translēt_avots 단위만 포함한다.
    # ārējs_VALUE 선언을 savs 이름으로 세지 않으며, faktisks_dati 빌드에서는 계속 컴파일한다.
    소유파일 = {str(CEĻŠ.resolve()) for CEĻŠ in Project_sakne.rglob('*') if CEĻŠ.suffix in ('.c','.h','.cpp','.inc')
              and not set(CEĻŠ.relative_to(Project_sakne).parts)&{'build','dist','vendor','__pycache__'}
              and CEĻŠ.relative_to(Project_sakne).as_posix() != 'C_kompilators/kompilators_rīks.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_sakne/'lietotājs'),
          '-I'+str(Project_sakne.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_sakne/'build'),'-I'+str(Project_sakne/'build/user'),
          '-I'+str(Project_sakne/'build/remote'),'-I'+str(Project_sakne/'vendor/bearssl/inc'),
          '-I'+str(Project_sakne/'vendor/bearssl/src'),'-I'+str(Project_sakne/'vendor/libassh/src'),
          '-I'+str(Project_sakne/'vendor/lwip/src/include'),'-I'+str(Project_sakne/'tīkls_kopa'),
          '-I'+str(Project_sakne/'attāls_VALUE'),'-I'+str(Project_sakne/'C_kompilators')]
    for CEĻŠ in sorted(Path(Nosaukums) for Nosaukums in 소유파일 if Nosaukums.endswith(('.c','.cpp'))):
        Parametri = 공통 + ['-std=c++11' if CEĻŠ.suffix=='.cpp' else '-std=c11']
        if 'tīkls_kopa' in CEĻŠ.parts: Parametri += ['-I'+str(Project_sakne/'tīkls_kopa'),'-I'+str(Project_sakne/'vendor/lwip/src/include')]
        if 'C_kompilators' in CEĻŠ.parts:
            Parametri += ['-I'+str(Project_sakne/'C_kompilators'),'-I'+str(Project_sakne/'vendor/tinycc'),'-I'+str(Project_sakne/'build/ccompiler'),
                    '-isystem',str(Project_sakne.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_tilts' in CEĻŠ.parts:
            Parametri += ['-I'+str(Project_sakne/'PYTHON_tilts'),'-I'+str(Project_sakne/'build/micropython-1.24.1'),'-I'+str(Project_sakne/'build/python'),'-isystem','/usr/include/newlib']
        if 'attāls_VALUE' in CEĻŠ.parts:
            Parametri += ['-isystem', '/usr/include/newlib']
        if 'sadale_VALUE' in CEĻŠ.parts: Parametri += ['-D__JKOROS__=1']
        if CEĻŠ.name=='saistīt.c': Parametri += ['-I'+str(Project_sakne/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupa_VALUE = (C_avots.c_char_p*len(Parametri))(*[ievade_VALUE.encode() for ievade_VALUE in Parametri])
        Tulkošana_vienība = analīze_VALUE(LOOKUP_INDEX,str(CEĻŠ).encode(),Grupa_VALUE,len(Parametri),None,0,1)
        for INDEX in range(진단수(Tulkošana_vienība)):
            진단 = 진단얻기(Tulkošana_vienība,INDEX)
            if nozīmīgums_VALUE(진단)>=3: 오류들.append((str(CEĻŠ.relative_to(Project_sakne)),Teksts(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ievade_VALUE,vecākobjekts_VALUE,dati):
            Fails,Nobīde_VALUE,Līniju = pozīcijas_indekss(ievade_VALUE)
            if Fails not in 소유파일: return 2 if ievade_VALUE.종류==300 else 1
            낱말 = Teksts(iegūt_nosaukums(ievade_VALUE))
            if not 낱말 or any(ord(rakstzīme_VALUE)>127 for rakstzīme_VALUE in 낱말): return 2
            if ievade_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Teksts(UNIQUE_nosaukums(ievade_VALUE)) or Fails+':'+str(Nobīde_VALUE)
                선언들[UNIQUE_VALUE] = {'Fails':Fails,'Nobīde_VALUE':Nobīde_VALUE,'Līniju':Līniju,'종류':ievade_VALUE.종류,'Nosaukums':낱말,'Savienoties':연결종류(ievade_VALUE)}
                참조들.append((Fails,Nobīde_VALUE,낱말,UNIQUE_VALUE))
            else:
                Uzziņas = iegūt_Uzziņas(ievade_VALUE)
                Uzziņas_Fails,_,_ = pozīcijas_indekss(Uzziņas)
                if Uzziņas_Fails in 소유파일:
                    UNIQUE_VALUE = Teksts(UNIQUE_nosaukums(Uzziņas)); 참조들.append((Fails,Nobīde_VALUE,Teksts(iegūt_nosaukums(Uzziņas)),UNIQUE_VALUE))
            return 2
        방문(sakne_VALUE(Tulkošana_vienība),살피기,None)
        iziet_programma(Tulkošana_vienība)
    mērķis_VALUE = Project_sakne/'build/한국어화/시언어분석.json'
    mērķis_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fails:hashlib.sha256(Path(Fails).read_bytes()).hexdigest() for Fails in sorted(소유파일)}
    mērķis_VALUE.write_text(json.dumps({'deklarācija':선언들,'Uzziņas':참조들,'Kļūda':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklarācija',len(선언들),'Uzziņas',len(참조들),'Kļūda',len(오류들))
    for Kļūda in 오류들: print(*Kļūda)

if __name__=='__main__': Izpildīt_komanda()
