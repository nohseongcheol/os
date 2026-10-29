#!/usr/bin/env python3
"""libclang deklaracija·nuoroda 위치를 수집한다. išorinis_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_šaltinis
import hashlib
import json
from pathlib import Path

Project_šaknis = Path(__file__).resolve().parents[1]
구현 = C_šaltinis.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class eilutė_VALUE(C_šaltinis.Structure): _fields_ = [('duomenys',C_šaltinis.c_void_p),('laida_VALUE',C_šaltinis.c_uint)]
class žymiklis_VALUE(C_šaltinis.Structure): _fields_ = [('종류',C_šaltinis.c_uint),('보조',C_šaltinis.c_int),('duomenys',C_šaltinis.c_void_p*3)]
class Pozicija(C_šaltinis.Structure): _fields_ = [('duomenys',C_šaltinis.c_void_p*2),('OFFSET_VALUE',C_šaltinis.c_uint)]
def FUNCTION_VALUE(Pavadinimas_2, grąžinti_KR, *Argumentai):
    įrašas_VALUE = getattr(구현, Pavadinimas_2); įrašas_VALUE.restype = grąžinti_KR; įrašas_VALUE.argtypes = list(Argumentai); return įrašas_VALUE
gauti_SMS = FUNCTION_VALUE('clang_getCString',C_šaltinis.c_char_p,eilutė_VALUE)
išleisti_SMS = FUNCTION_VALUE('clang_disposeString',None,eilutė_VALUE)
def Tekstas(VALUE):
    REZULTATAS = (gauti_SMS(VALUE) or b'').decode('utf-8'); išleisti_SMS(VALUE); return REZULTATAS
gauti_pavadinimas = FUNCTION_VALUE('clang_getCursorSpelling',eilutė_VALUE,žymiklis_VALUE)
gauti_nuoroda_10d0a960 = FUNCTION_VALUE('clang_getCursorReferenced',žymiklis_VALUE,žymiklis_VALUE)
gauti_padėtis_9492ef84 = FUNCTION_VALUE('clang_getCursorLocation',Pozicija,žymiklis_VALUE)
Failas_padėtis = FUNCTION_VALUE('clang_getFileLocation',None,Pozicija,C_šaltinis.POINTER(C_šaltinis.c_void_p),C_šaltinis.POINTER(C_šaltinis.c_uint),C_šaltinis.POINTER(C_šaltinis.c_uint),C_šaltinis.POINTER(C_šaltinis.c_uint))
Failas_įrašas_pavadinimas = FUNCTION_VALUE('clang_getFileName',eilutė_VALUE,C_šaltinis.c_void_p)
UNIQUE_pavadinimas = FUNCTION_VALUE('clang_getCursorUSR',eilutė_VALUE,žymiklis_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',C_šaltinis.c_uint,žymiklis_VALUE)
방문형 = C_šaltinis.CFUNCTYPE(C_šaltinis.c_uint,žymiklis_VALUE,žymiklis_VALUE,C_šaltinis.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',C_šaltinis.c_uint,žymiklis_VALUE,방문형,C_šaltinis.c_void_p)
generuoti = FUNCTION_VALUE('clang_createIndex',C_šaltinis.c_void_p,C_šaltinis.c_int,C_šaltinis.c_int)
Analizė_VALUE = FUNCTION_VALUE('clang_parseTranslationUnit',C_šaltinis.c_void_p,C_šaltinis.c_void_p,C_šaltinis.c_char_p,C_šaltinis.POINTER(C_šaltinis.c_char_p),C_šaltinis.c_int,C_šaltinis.c_void_p,C_šaltinis.c_uint,C_šaltinis.c_uint)
šaknis_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',žymiklis_VALUE,C_šaltinis.c_void_p)
išeiti_programa = FUNCTION_VALUE('clang_disposeTranslationUnit',None,C_šaltinis.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',C_šaltinis.c_uint,C_šaltinis.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',C_šaltinis.c_void_p,C_šaltinis.c_void_p,C_šaltinis.c_uint)
svarba_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',C_šaltinis.c_uint,C_šaltinis.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',eilutė_VALUE,C_šaltinis.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,C_šaltinis.c_void_p)

def vietos_rodyklė(įrašas_VALUE):
    Failas = C_šaltinis.c_void_p(); Eilutė = C_šaltinis.c_uint(); 칸 = C_šaltinis.c_uint(); OFFSET_VALUE = C_šaltinis.c_uint()
    Failas_padėtis(gauti_padėtis_9492ef84(įrašas_VALUE),C_šaltinis.byref(Failas),C_šaltinis.byref(Eilutė),C_šaltinis.byref(칸),C_šaltinis.byref(OFFSET_VALUE))
    return (Tekstas(Failas_įrašas_pavadinimas(Failas)) if Failas else '', OFFSET_VALUE.value, Eilutė.value)

def Vykdyti_komanda():
    LOOKUP_INDEX = generuoti(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompiliatorius_įrankis.c는 savas deklaracija 없이 TinyCC išorinis_VALUE 단일 Versti_šaltinis 단위만 포함한다.
    # išorinis_VALUE 선언을 savas 이름으로 세지 않으며, faktinis_duomenys 빌드에서는 계속 컴파일한다.
    소유파일 = {str(KELIAS.resolve()) for KELIAS in Project_šaknis.rglob('*') if KELIAS.suffix in ('.c','.h','.cpp','.inc')
              and not set(KELIAS.relative_to(Project_šaknis).parts)&{'build','dist','vendor','__pycache__'}
              and KELIAS.relative_to(Project_šaknis).as_posix() != 'C_kompiliatorius/kompiliatorius_įrankis.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_šaknis/'naudotojas'),
          '-I'+str(Project_šaknis.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_šaknis/'build'),'-I'+str(Project_šaknis/'build/user'),
          '-I'+str(Project_šaknis/'build/remote'),'-I'+str(Project_šaknis/'vendor/bearssl/inc'),
          '-I'+str(Project_šaknis/'vendor/bearssl/src'),'-I'+str(Project_šaknis/'vendor/libassh/src'),
          '-I'+str(Project_šaknis/'vendor/lwip/src/include'),'-I'+str(Project_šaknis/'tinklas_eilė'),
          '-I'+str(Project_šaknis/'nuotolinis_VALUE'),'-I'+str(Project_šaknis/'C_kompiliatorius')]
    for KELIAS in sorted(Path(Pavadinimas_2) for Pavadinimas_2 in 소유파일 if Pavadinimas_2.endswith(('.c','.cpp'))):
        Argumentai = 공통 + ['-std=c++11' if KELIAS.suffix=='.cpp' else '-std=c11']
        if 'tinklas_eilė' in KELIAS.parts: Argumentai += ['-I'+str(Project_šaknis/'tinklas_eilė'),'-I'+str(Project_šaknis/'vendor/lwip/src/include')]
        if 'C_kompiliatorius' in KELIAS.parts:
            Argumentai += ['-I'+str(Project_šaknis/'C_kompiliatorius'),'-I'+str(Project_šaknis/'vendor/tinycc'),'-I'+str(Project_šaknis/'build/ccompiler'),
                    '-isystem',str(Project_šaknis.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_tiltas' in KELIAS.parts:
            Argumentai += ['-I'+str(Project_šaknis/'PYTHON_tiltas'),'-I'+str(Project_šaknis/'build/micropython-1.24.1'),'-I'+str(Project_šaknis/'build/python'),'-isystem','/usr/include/newlib']
        if 'nuotolinis_VALUE' in KELIAS.parts:
            Argumentai += ['-isystem', '/usr/include/newlib']
        if 'paskirstymas_VALUE' in KELIAS.parts: Argumentai += ['-D__JKOROS__=1']
        if KELIAS.name=='paketas.c': Argumentai += ['-I'+str(Project_šaknis/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupė_VALUE = (C_šaltinis.c_char_p*len(Argumentai))(*[įrašas_VALUE.encode() for įrašas_VALUE in Argumentai])
        Vertimas_pamoka = Analizė_VALUE(LOOKUP_INDEX,str(KELIAS).encode(),Grupė_VALUE,len(Argumentai),None,0,1)
        for INDEX in range(진단수(Vertimas_pamoka)):
            진단 = 진단얻기(Vertimas_pamoka,INDEX)
            if svarba_VALUE(진단)>=3: 오류들.append((str(KELIAS.relative_to(Project_šaknis)),Tekstas(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(įrašas_VALUE,pirminis_VALUE,duomenys):
            Failas,OFFSET_VALUE,Eilutė = vietos_rodyklė(įrašas_VALUE)
            if Failas not in 소유파일: return 2 if įrašas_VALUE.종류==300 else 1
            낱말 = Tekstas(gauti_pavadinimas(įrašas_VALUE))
            if not 낱말 or any(ord(simbolis_VALUE_068c2631)>127 for simbolis_VALUE_068c2631 in 낱말): return 2
            if įrašas_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Tekstas(UNIQUE_pavadinimas(įrašas_VALUE)) or Failas+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Failas':Failas,'OFFSET_VALUE':OFFSET_VALUE,'Eilutė':Eilutė,'종류':įrašas_VALUE.종류,'Pavadinimas_2':낱말,'Prisijungti':연결종류(įrašas_VALUE)}
                참조들.append((Failas,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                nuoroda = gauti_nuoroda_10d0a960(įrašas_VALUE)
                nuoroda_Failas,_,_ = vietos_rodyklė(nuoroda)
                if nuoroda_Failas in 소유파일:
                    UNIQUE_VALUE = Tekstas(UNIQUE_pavadinimas(nuoroda)); 참조들.append((Failas,OFFSET_VALUE,Tekstas(gauti_pavadinimas(nuoroda)),UNIQUE_VALUE))
            return 2
        방문(šaknis_VALUE(Vertimas_pamoka),살피기,None)
        išeiti_programa(Vertimas_pamoka)
    vieta_VALUE = Project_šaknis/'build/한국어화/시언어분석.json'
    vieta_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Failas:hashlib.sha256(Path(Failas).read_bytes()).hexdigest() for Failas in sorted(소유파일)}
    vieta_VALUE.write_text(json.dumps({'deklaracija':선언들,'nuoroda':참조들,'KLAIDA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklaracija',len(선언들),'nuoroda',len(참조들),'KLAIDA',len(오류들))
    for KLAIDA in 오류들: print(*KLAIDA)

if __name__=='__main__': Vykdyti_komanda()
