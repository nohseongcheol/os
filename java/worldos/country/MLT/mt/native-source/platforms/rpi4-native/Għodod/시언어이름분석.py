#!/usr/bin/env python3
"""libclang 선언·Referenza 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

pprojetta_għerq = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class string_VALUE(씨.Structure): _fields_ = [('data',씨.c_void_p),('wera_VALUE_487749b8',씨.c_uint)]
class kerser_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class pożizzjoni(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def FUNCTION_VALUE(isem, 반환, *인수):
    entrata_VALUE = getattr(구현, isem); entrata_VALUE.restype = 반환; entrata_VALUE.argtypes = list(인수); return entrata_VALUE
글얻기 = FUNCTION_VALUE('clang_getCString',씨.c_char_p,string_VALUE)
mexxi_SMS = FUNCTION_VALUE('clang_disposeString',None,string_VALUE)
def SMS(VALUE):
    miżura = (글얻기(VALUE) or b'').decode('utf-8'); mexxi_SMS(VALUE); return miżura
이름얻기 = FUNCTION_VALUE('clang_getCursorSpelling',string_VALUE,kerser_VALUE)
참조얻기 = FUNCTION_VALUE('clang_getCursorReferenced',kerser_VALUE,kerser_VALUE)
위치얻기 = FUNCTION_VALUE('clang_getCursorLocation',pożizzjoni,kerser_VALUE)
fajl_pożizzjoni = FUNCTION_VALUE('clang_getFileLocation',None,pożizzjoni,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fajl_entrata_isem = FUNCTION_VALUE('clang_getFileName',string_VALUE,씨.c_void_p)
UNIQUE_isem = FUNCTION_VALUE('clang_getCursorUSR',string_VALUE,kerser_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,kerser_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kerser_VALUE,kerser_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,kerser_VALUE,방문형,씨.c_void_p)
iġġenera = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
għerq_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',kerser_VALUE,씨.c_void_p)
ħruġ_programm = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
severità_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',string_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def pożizzjoni_INDEX(entrata_VALUE):
    fajl = 씨.c_void_p(); linja = 씨.c_uint(); slott_entrata = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    fajl_pożizzjoni(위치얻기(entrata_VALUE),씨.byref(fajl),씨.byref(linja),씨.byref(slott_entrata),씨.byref(OFFSET_VALUE))
    return (SMS(fajl_entrata_isem(fajl)) if fajl else '', OFFSET_VALUE.value, linja.value)

def eżegwixxa_kmand():
    LOOKUP_INDEX = iġġenera(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Ittraduċi_sors 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, attwali_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(mogħdija.resolve()) for mogħdija in pprojetta_għerq.rglob('*') if mogħdija.suffix in ('.c','.h','.cpp','.inc')
              and not set(mogħdija.relative_to(pprojetta_għerq).parts)&{'build','dist','vendor','__pycache__'}
              and mogħdija.relative_to(pprojetta_għerq).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(pprojetta_għerq/'utent'),
          '-I'+str(pprojetta_għerq.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(pprojetta_għerq/'build'),'-I'+str(pprojetta_għerq/'build/user'),
          '-I'+str(pprojetta_għerq/'build/remote'),'-I'+str(pprojetta_għerq/'vendor/bearssl/inc'),
          '-I'+str(pprojetta_għerq/'vendor/bearssl/src'),'-I'+str(pprojetta_għerq/'vendor/libassh/src'),
          '-I'+str(pprojetta_għerq/'vendor/lwip/src/include'),'-I'+str(pprojetta_għerq/'netwerk_Munzell'),
          '-I'+str(pprojetta_għerq/'mill_bogħod_VALUE'),'-I'+str(pprojetta_għerq/'시언어번역기')]
    for mogħdija in sorted(Path(isem) for isem in 소유파일 if isem.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if mogħdija.suffix=='.cpp' else '-std=c11']
        if 'netwerk_Munzell' in mogħdija.parts: 인수 += ['-I'+str(pprojetta_għerq/'netwerk_Munzell'),'-I'+str(pprojetta_għerq/'vendor/lwip/src/include')]
        if '시언어번역기' in mogħdija.parts:
            인수 += ['-I'+str(pprojetta_għerq/'시언어번역기'),'-I'+str(pprojetta_għerq/'vendor/tinycc'),'-I'+str(pprojetta_għerq/'build/ccompiler'),
                    '-isystem',str(pprojetta_għerq.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_pont' in mogħdija.parts:
            인수 += ['-I'+str(pprojetta_għerq/'PYTHON_pont'),'-I'+str(pprojetta_għerq/'build/micropython-1.24.1'),'-I'+str(pprojetta_għerq/'build/python'),'-isystem','/usr/include/newlib']
        if 'mill_bogħod_VALUE' in mogħdija.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in mogħdija.parts: 인수 += ['-D__JKOROS__=1']
        if mogħdija.name=='lott.c': 인수 += ['-I'+str(pprojetta_għerq/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        grupp_VALUE = (씨.c_char_p*len(인수))(*[entrata_VALUE.encode() for entrata_VALUE in 인수])
        Traduzzjoni_lezzjoni = 분석(LOOKUP_INDEX,str(mogħdija).encode(),grupp_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Traduzzjoni_lezzjoni)):
            진단 = 진단얻기(Traduzzjoni_lezzjoni,INDEX)
            if severità_VALUE(진단)>=3: 오류들.append((str(mogħdija.relative_to(pprojetta_għerq)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(entrata_VALUE,부모,data):
            fajl,OFFSET_VALUE,linja = pożizzjoni_INDEX(entrata_VALUE)
            if fajl not in 소유파일: return 2 if entrata_VALUE.종류==300 else 1
            낱말 = SMS(이름얻기(entrata_VALUE))
            if not 낱말 or any(ord(karattru_VALUE)>127 for karattru_VALUE in 낱말): return 2
            if entrata_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = SMS(UNIQUE_isem(entrata_VALUE)) or fajl+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'fajl':fajl,'OFFSET_VALUE':OFFSET_VALUE,'줄':linja,'종류':entrata_VALUE.종류,'isem':낱말,'AQBAD':연결종류(entrata_VALUE)}
                참조들.append((fajl,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Referenza = 참조얻기(entrata_VALUE)
                Referenza_fajl,_,_ = pożizzjoni_INDEX(Referenza)
                if Referenza_fajl in 소유파일:
                    UNIQUE_VALUE = SMS(UNIQUE_isem(Referenza)); 참조들.append((fajl,OFFSET_VALUE,SMS(이름얻기(Referenza)),UNIQUE_VALUE))
            return 2
        방문(għerq_VALUE(Traduzzjoni_lezzjoni),살피기,None)
        ħruġ_programm(Traduzzjoni_lezzjoni)
    destinazzjoni_VALUE = pprojetta_għerq/'build/한국어화/시언어분석.json'
    destinazzjoni_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {fajl:hashlib.sha256(Path(fajl).read_bytes()).hexdigest() for fajl in sorted(소유파일)}
    destinazzjoni_VALUE.write_text(json.dumps({'선언':선언들,'Referenza':참조들,'żball':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Referenza',len(참조들),'żball',len(오류들))
    for żball in 오류들: print(*żball)

if __name__=='__main__': eżegwixxa_kmand()
