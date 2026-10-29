#!/usr/bin/env python3
"""libclang declarație·referință 위치를 수집한다. extern_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_sursă
import hashlib
import json
from pathlib import Path

Project_rădăcină = Path(__file__).resolve().parents[1]
구현 = C_sursă.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class șir_VALUE(C_sursă.Structure): _fields_ = [('date',C_sursă.c_void_p),('afișa_VALUE',C_sursă.c_uint)]
class cursor_VALUE(C_sursă.Structure): _fields_ = [('종류',C_sursă.c_uint),('보조',C_sursă.c_int),('date',C_sursă.c_void_p*3)]
class Poziție(C_sursă.Structure): _fields_ = [('date',C_sursă.c_void_p*2),('OFFSET_VALUE',C_sursă.c_uint)]
def funcție_VALUE(Nume, restitui_KR, *Argumente):
    intrare_VALUE = getattr(구현, Nume); intrare_VALUE.restype = restitui_KR; intrare_VALUE.argtypes = list(Argumente); return intrare_VALUE
prelua_SMS = funcție_VALUE('clang_getCString',C_sursă.c_char_p,șir_VALUE)
lansa_SMS = funcție_VALUE('clang_disposeString',None,șir_VALUE)
def SMS(VALUE):
    KR = (prelua_SMS(VALUE) or b'').decode('utf-8'); lansa_SMS(VALUE); return KR
prelua_nume = funcție_VALUE('clang_getCursorSpelling',șir_VALUE,cursor_VALUE)
prelua_referință = funcție_VALUE('clang_getCursorReferenced',cursor_VALUE,cursor_VALUE)
prelua_poziție = funcție_VALUE('clang_getCursorLocation',Poziție,cursor_VALUE)
Fișier_poziție = funcție_VALUE('clang_getFileLocation',None,Poziție,C_sursă.POINTER(C_sursă.c_void_p),C_sursă.POINTER(C_sursă.c_uint),C_sursă.POINTER(C_sursă.c_uint),C_sursă.POINTER(C_sursă.c_uint))
Fișier_intrare_nume = funcție_VALUE('clang_getFileName',șir_VALUE,C_sursă.c_void_p)
UNIQUE_nume = funcție_VALUE('clang_getCursorUSR',șir_VALUE,cursor_VALUE)
연결종류 = funcție_VALUE('clang_getCursorLinkage',C_sursă.c_uint,cursor_VALUE)
방문형 = C_sursă.CFUNCTYPE(C_sursă.c_uint,cursor_VALUE,cursor_VALUE,C_sursă.c_void_p)
방문 = funcție_VALUE('clang_visitChildren',C_sursă.c_uint,cursor_VALUE,방문형,C_sursă.c_void_p)
genera = funcție_VALUE('clang_createIndex',C_sursă.c_void_p,C_sursă.c_int,C_sursă.c_int)
Analiză_VALUE = funcție_VALUE('clang_parseTranslationUnit',C_sursă.c_void_p,C_sursă.c_void_p,C_sursă.c_char_p,C_sursă.POINTER(C_sursă.c_char_p),C_sursă.c_int,C_sursă.c_void_p,C_sursă.c_uint,C_sursă.c_uint)
rădăcină_VALUE = funcție_VALUE('clang_getTranslationUnitCursor',cursor_VALUE,C_sursă.c_void_p)
ieșire_program = funcție_VALUE('clang_disposeTranslationUnit',None,C_sursă.c_void_p)
진단수 = funcție_VALUE('clang_getNumDiagnostics',C_sursă.c_uint,C_sursă.c_void_p)
진단얻기 = funcție_VALUE('clang_getDiagnostic',C_sursă.c_void_p,C_sursă.c_void_p,C_sursă.c_uint)
gravitate_VALUE = funcție_VALUE('clang_getDiagnosticSeverity',C_sursă.c_uint,C_sursă.c_void_p)
진단문 = funcție_VALUE('clang_getDiagnosticSpelling',șir_VALUE,C_sursă.c_void_p)
진단해제 = funcție_VALUE('clang_disposeDiagnostic',None,C_sursă.c_void_p)

def index_de_poziție(intrare_VALUE):
    Fișier = C_sursă.c_void_p(); Linie = C_sursă.c_uint(); 칸 = C_sursă.c_uint(); OFFSET_VALUE = C_sursă.c_uint()
    Fișier_poziție(prelua_poziție(intrare_VALUE),C_sursă.byref(Fișier),C_sursă.byref(Linie),C_sursă.byref(칸),C_sursă.byref(OFFSET_VALUE))
    return (SMS(Fișier_intrare_nume(Fișier)) if Fișier else '', OFFSET_VALUE.value, Linie.value)

def executa_comandă():
    LOOKUP_INDEX = genera(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # compilator_instrument.c는 propriu declarație 없이 TinyCC extern_VALUE 단일 TRANSLATE_sursă 단위만 포함한다.
    # extern_VALUE 선언을 propriu 이름으로 세지 않으며, real_date 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Cale.resolve()) for Cale in Project_rădăcină.rglob('*') if Cale.suffix in ('.c','.h','.cpp','.inc')
              and not set(Cale.relative_to(Project_rădăcină).parts)&{'build','dist','vendor','__pycache__'}
              and Cale.relative_to(Project_rădăcină).as_posix() != 'C_compilator/compilator_instrument.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_rădăcină/'utilizator'),
          '-I'+str(Project_rădăcină.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_rădăcină/'build'),'-I'+str(Project_rădăcină/'build/user'),
          '-I'+str(Project_rădăcină/'build/remote'),'-I'+str(Project_rădăcină/'vendor/bearssl/inc'),
          '-I'+str(Project_rădăcină/'vendor/bearssl/src'),'-I'+str(Project_rădăcină/'vendor/libassh/src'),
          '-I'+str(Project_rădăcină/'vendor/lwip/src/include'),'-I'+str(Project_rădăcină/'rețea_Teanc'),
          '-I'+str(Project_rădăcină/'la_distanță_VALUE'),'-I'+str(Project_rădăcină/'C_compilator')]
    for Cale in sorted(Path(Nume) for Nume in 소유파일 if Nume.endswith(('.c','.cpp'))):
        Argumente = 공통 + ['-std=c++11' if Cale.suffix=='.cpp' else '-std=c11']
        if 'rețea_Teanc' in Cale.parts: Argumente += ['-I'+str(Project_rădăcină/'rețea_Teanc'),'-I'+str(Project_rădăcină/'vendor/lwip/src/include')]
        if 'C_compilator' in Cale.parts:
            Argumente += ['-I'+str(Project_rădăcină/'C_compilator'),'-I'+str(Project_rădăcină/'vendor/tinycc'),'-I'+str(Project_rădăcină/'build/ccompiler'),
                    '-isystem',str(Project_rădăcină.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_punte' in Cale.parts:
            Argumente += ['-I'+str(Project_rădăcină/'PYTHON_punte'),'-I'+str(Project_rădăcină/'build/micropython-1.24.1'),'-I'+str(Project_rădăcină/'build/python'),'-isystem','/usr/include/newlib']
        if 'la_distanță_VALUE' in Cale.parts:
            Argumente += ['-isystem', '/usr/include/newlib']
        if '배포' in Cale.parts: Argumente += ['-D__JKOROS__=1']
        if Cale.name=='set.c': Argumente += ['-I'+str(Project_rădăcină/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        grup_VALUE = (C_sursă.c_char_p*len(Argumente))(*[intrare_VALUE.encode() for intrare_VALUE in Argumente])
        Traducere_lecție = Analiză_VALUE(LOOKUP_INDEX,str(Cale).encode(),grup_VALUE,len(Argumente),None,0,1)
        for INDEX in range(진단수(Traducere_lecție)):
            진단 = 진단얻기(Traducere_lecție,INDEX)
            if gravitate_VALUE(진단)>=3: 오류들.append((str(Cale.relative_to(Project_rădăcină)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(intrare_VALUE,părinte_VALUE,date):
            Fișier,OFFSET_VALUE,Linie = index_de_poziție(intrare_VALUE)
            if Fișier not in 소유파일: return 2 if intrare_VALUE.종류==300 else 1
            낱말 = SMS(prelua_nume(intrare_VALUE))
            if not 낱말 or any(ord(caracter_VALUE)>127 for caracter_VALUE in 낱말): return 2
            if intrare_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = SMS(UNIQUE_nume(intrare_VALUE)) or Fișier+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Fișier':Fișier,'OFFSET_VALUE':OFFSET_VALUE,'Linie':Linie,'종류':intrare_VALUE.종류,'Nume':낱말,'Conectează':연결종류(intrare_VALUE)}
                참조들.append((Fișier,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                referință = prelua_referință(intrare_VALUE)
                referință_Fișier,_,_ = index_de_poziție(referință)
                if referință_Fișier in 소유파일:
                    UNIQUE_VALUE = SMS(UNIQUE_nume(referință)); 참조들.append((Fișier,OFFSET_VALUE,SMS(prelua_nume(referință)),UNIQUE_VALUE))
            return 2
        방문(rădăcină_VALUE(Traducere_lecție),살피기,None)
        ieșire_program(Traducere_lecție)
    destinație_VALUE = Project_rădăcină/'build/한국어화/시언어분석.json'
    destinație_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fișier:hashlib.sha256(Path(Fișier).read_bytes()).hexdigest() for Fișier in sorted(소유파일)}
    destinație_VALUE.write_text(json.dumps({'declarație':선언들,'referință':참조들,'eroare':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('declarație',len(선언들),'referință',len(참조들),'eroare',len(오류들))
    for eroare in 오류들: print(*eroare)

if __name__=='__main__': executa_comandă()
