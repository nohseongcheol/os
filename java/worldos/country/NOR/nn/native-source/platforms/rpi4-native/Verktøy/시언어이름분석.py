#!/usr/bin/env python3
"""libclang erklæring·Oppslagsverk 위치를 수집한다. ekstern_VALUE 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

spegle_rot = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class streng_VALUE(씨.Structure): _fields_ = [('data',씨.c_void_p),('vise_VALUE_487749b8',씨.c_uint)]
class markør_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class Posisjon(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def FUNCTION_VALUE(Namn, levere_tilbake_forretningsmål, *Argument):
    oppføring_VALUE = getattr(구현, Namn); oppføring_VALUE.restype = levere_tilbake_forretningsmål; oppføring_VALUE.argtypes = list(Argument); return oppføring_VALUE
글얻기 = FUNCTION_VALUE('clang_getCString',씨.c_char_p,streng_VALUE)
frigi_SMS = FUNCTION_VALUE('clang_disposeString',None,streng_VALUE)
def Tekst(VALUE):
    forretningsmål = (글얻기(VALUE) or b'').decode('utf-8'); frigi_SMS(VALUE); return forretningsmål
이름얻기 = FUNCTION_VALUE('clang_getCursorSpelling',streng_VALUE,markør_VALUE)
참조얻기 = FUNCTION_VALUE('clang_getCursorReferenced',markør_VALUE,markør_VALUE)
위치얻기 = FUNCTION_VALUE('clang_getCursorLocation',Posisjon,markør_VALUE)
fil_plassere = FUNCTION_VALUE('clang_getFileLocation',None,Posisjon,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fil_oppføring_namn = FUNCTION_VALUE('clang_getFileName',streng_VALUE,씨.c_void_p)
UNIQUE_namn = FUNCTION_VALUE('clang_getCursorUSR',streng_VALUE,markør_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,markør_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,markør_VALUE,markør_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,markør_VALUE,방문형,씨.c_void_p)
generere = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
rot_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',markør_VALUE,씨.c_void_p)
avslutt_app = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
alvorsgrad_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',streng_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def plassere_INDEX(oppføring_VALUE):
    Fil = 씨.c_void_p(); linje = 씨.c_uint(); felt_oppføring = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    fil_plassere(위치얻기(oppføring_VALUE),씨.byref(Fil),씨.byref(linje),씨.byref(felt_oppføring),씨.byref(OFFSET_VALUE))
    return (Tekst(fil_oppføring_namn(Fil)) if Fil else '', OFFSET_VALUE.value, linje.value)

def Utfør_kommando():
    LOOKUP_INDEX = generere(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 erklæring 없이 TinyCC ekstern_VALUE 단일 TRANSLATE_kjelde 단위만 포함한다.
    # ekstern_VALUE 선언을 자체 이름으로 세지 않으며, faktisk_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(STIGE.resolve()) for STIGE in spegle_rot.rglob('*') if STIGE.suffix in ('.c','.h','.cpp','.inc')
              and not set(STIGE.relative_to(spegle_rot).parts)&{'build','dist','vendor','__pycache__'}
              and STIGE.relative_to(spegle_rot).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(spegle_rot/'brukar'),
          '-I'+str(spegle_rot.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(spegle_rot/'build'),'-I'+str(spegle_rot/'build/user'),
          '-I'+str(spegle_rot/'build/remote'),'-I'+str(spegle_rot/'vendor/bearssl/inc'),
          '-I'+str(spegle_rot/'vendor/bearssl/src'),'-I'+str(spegle_rot/'vendor/libassh/src'),
          '-I'+str(spegle_rot/'vendor/lwip/src/include'),'-I'+str(spegle_rot/'Nettverk_Stabel'),
          '-I'+str(spegle_rot/'fjern_VALUE'),'-I'+str(spegle_rot/'시언어번역기')]
    for STIGE in sorted(Path(Namn) for Namn in 소유파일 if Namn.endswith(('.c','.cpp'))):
        Argument = 공통 + ['-std=c++11' if STIGE.suffix=='.cpp' else '-std=c11']
        if 'Nettverk_Stabel' in STIGE.parts: Argument += ['-I'+str(spegle_rot/'Nettverk_Stabel'),'-I'+str(spegle_rot/'vendor/lwip/src/include')]
        if '시언어번역기' in STIGE.parts:
            Argument += ['-I'+str(spegle_rot/'시언어번역기'),'-I'+str(spegle_rot/'vendor/tinycc'),'-I'+str(spegle_rot/'build/ccompiler'),
                    '-isystem',str(spegle_rot.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_bru' in STIGE.parts:
            Argument += ['-I'+str(spegle_rot/'PYTHON_bru'),'-I'+str(spegle_rot/'build/micropython-1.24.1'),'-I'+str(spegle_rot/'build/python'),'-isystem','/usr/include/newlib']
        if 'fjern_VALUE' in STIGE.parts:
            Argument += ['-isystem', '/usr/include/newlib']
        if '배포' in STIGE.parts: Argument += ['-D__JKOROS__=1']
        if STIGE.name=='bunt.c': Argument += ['-I'+str(spegle_rot/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        gruppe_VALUE = (씨.c_char_p*len(Argument))(*[oppføring_VALUE.encode() for oppføring_VALUE in Argument])
        Omsetjing_leksjon = 분석(LOOKUP_INDEX,str(STIGE).encode(),gruppe_VALUE,len(Argument),None,0,1)
        for INDEX in range(진단수(Omsetjing_leksjon)):
            진단 = 진단얻기(Omsetjing_leksjon,INDEX)
            if alvorsgrad_VALUE(진단)>=3: 오류들.append((str(STIGE.relative_to(spegle_rot)),Tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(oppføring_VALUE,forelder_VALUE,data):
            Fil,OFFSET_VALUE,linje = plassere_INDEX(oppføring_VALUE)
            if Fil not in 소유파일: return 2 if oppføring_VALUE.종류==300 else 1
            낱말 = Tekst(이름얻기(oppføring_VALUE))
            if not 낱말 or any(ord(teikn_VALUE)>127 for teikn_VALUE in 낱말): return 2
            if oppføring_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Tekst(UNIQUE_namn(oppføring_VALUE)) or Fil+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Fil':Fil,'OFFSET_VALUE':OFFSET_VALUE,'linje':linje,'종류':oppføring_VALUE.종류,'Namn':낱말,'Kopla_til':연결종류(oppføring_VALUE)}
                참조들.append((Fil,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Oppslagsverk = 참조얻기(oppføring_VALUE)
                Oppslagsverk_fil,_,_ = plassere_INDEX(Oppslagsverk)
                if Oppslagsverk_fil in 소유파일:
                    UNIQUE_VALUE = Tekst(UNIQUE_namn(Oppslagsverk)); 참조들.append((Fil,OFFSET_VALUE,Tekst(이름얻기(Oppslagsverk)),UNIQUE_VALUE))
            return 2
        방문(rot_VALUE(Omsetjing_leksjon),살피기,None)
        avslutt_app(Omsetjing_leksjon)
    mål_VALUE = spegle_rot/'build/한국어화/시언어분석.json'
    mål_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fil:hashlib.sha256(Path(Fil).read_bytes()).hexdigest() for Fil in sorted(소유파일)}
    mål_VALUE.write_text(json.dumps({'erklæring':선언들,'Oppslagsverk':참조들,'FEIL':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('erklæring',len(선언들),'Oppslagsverk',len(참조들),'FEIL',len(오류들))
    for FEIL in 오류들: print(*FEIL)

if __name__=='__main__': Utfør_kommando()
