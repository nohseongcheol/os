#!/usr/bin/env python3
"""libclang skýrsla·tilvísun 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

verk_rót = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class strengur_VALUE(씨.Structure): _fields_ = [('gögn',씨.c_void_p),('sýna_VALUE',씨.c_uint)]
class bendill_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('gögn',씨.c_void_p*3)]
class Staðsetning(씨.Structure): _fields_ = [('gögn',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def fall_VALUE(Heiti, skila_mæld_stærð, *Viðföng):
    færsla_VALUE = getattr(구현, Heiti); færsla_VALUE.restype = skila_mæld_stærð; færsla_VALUE.argtypes = list(Viðföng); return færsla_VALUE
sækja_SMS = fall_VALUE('clang_getCString',씨.c_char_p,strengur_VALUE)
losa_SMS = fall_VALUE('clang_disposeString',None,strengur_VALUE)
def Texti(VALUE):
    NIÐURSTAÐA = (sækja_SMS(VALUE) or b'').decode('utf-8'); losa_SMS(VALUE); return NIÐURSTAÐA
sækja_heiti = fall_VALUE('clang_getCursorSpelling',strengur_VALUE,bendill_VALUE)
sækja_tilvísun = fall_VALUE('clang_getCursorReferenced',bendill_VALUE,bendill_VALUE)
sækja_staða = fall_VALUE('clang_getCursorLocation',Staðsetning,bendill_VALUE)
skrá_staða_2aa21a9a = fall_VALUE('clang_getFileLocation',None,Staðsetning,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
skrá_færsla_heiti = fall_VALUE('clang_getFileName',strengur_VALUE,씨.c_void_p)
UNIQUE_heiti = fall_VALUE('clang_getCursorUSR',strengur_VALUE,bendill_VALUE)
연결종류 = fall_VALUE('clang_getCursorLinkage',씨.c_uint,bendill_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,bendill_VALUE,bendill_VALUE,씨.c_void_p)
방문 = fall_VALUE('clang_visitChildren',씨.c_uint,bendill_VALUE,방문형,씨.c_void_p)
skapa = fall_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = fall_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
rót_VALUE = fall_VALUE('clang_getTranslationUnitCursor',bendill_VALUE,씨.c_void_p)
hætta_forrit = fall_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = fall_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = fall_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
alvarleiki_VALUE = fall_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = fall_VALUE('clang_getDiagnosticSpelling',strengur_VALUE,씨.c_void_p)
진단해제 = fall_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def staða_INDEX(færsla_VALUE):
    Skrá = 씨.c_void_p(); Lína = 씨.c_uint(); rauf_færsla = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    skrá_staða_2aa21a9a(sækja_staða(færsla_VALUE),씨.byref(Skrá),씨.byref(Lína),씨.byref(rauf_færsla),씨.byref(OFFSET_VALUE))
    return (Texti(skrá_færsla_heiti(Skrá)) if Skrá else '', OFFSET_VALUE.value, Lína.value)

def keyra_skipun():
    LOOKUP_INDEX = skapa(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 eigin skýrsla 없이 TinyCC 외부 단일 Þýða_uppruni 단위만 포함한다.
    # 외부 선언을 eigin 이름으로 세지 않으며, raun_gögn 빌드에서는 계속 컴파일한다.
    소유파일 = {str(SLÓÐ.resolve()) for SLÓÐ in verk_rót.rglob('*') if SLÓÐ.suffix in ('.c','.h','.cpp','.inc')
              and not set(SLÓÐ.relative_to(verk_rót).parts)&{'build','dist','vendor','__pycache__'}
              and SLÓÐ.relative_to(verk_rót).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(verk_rót/'notandi'),
          '-I'+str(verk_rót.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(verk_rót/'build'),'-I'+str(verk_rót/'build/user'),
          '-I'+str(verk_rót/'build/remote'),'-I'+str(verk_rót/'vendor/bearssl/inc'),
          '-I'+str(verk_rót/'vendor/bearssl/src'),'-I'+str(verk_rót/'vendor/libassh/src'),
          '-I'+str(verk_rót/'vendor/lwip/src/include'),'-I'+str(verk_rót/'Net_bunki'),
          '-I'+str(verk_rót/'fjartengdur_VALUE'),'-I'+str(verk_rót/'시언어번역기')]
    for SLÓÐ in sorted(Path(Heiti) for Heiti in 소유파일 if Heiti.endswith(('.c','.cpp'))):
        Viðföng = 공통 + ['-std=c++11' if SLÓÐ.suffix=='.cpp' else '-std=c11']
        if 'Net_bunki' in SLÓÐ.parts: Viðföng += ['-I'+str(verk_rót/'Net_bunki'),'-I'+str(verk_rót/'vendor/lwip/src/include')]
        if '시언어번역기' in SLÓÐ.parts:
            Viðföng += ['-I'+str(verk_rót/'시언어번역기'),'-I'+str(verk_rót/'vendor/tinycc'),'-I'+str(verk_rót/'build/ccompiler'),
                    '-isystem',str(verk_rót.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_brú' in SLÓÐ.parts:
            Viðföng += ['-I'+str(verk_rót/'PYTHON_brú'),'-I'+str(verk_rót/'build/micropython-1.24.1'),'-I'+str(verk_rót/'build/python'),'-isystem','/usr/include/newlib']
        if 'fjartengdur_VALUE' in SLÓÐ.parts:
            Viðföng += ['-isystem', '/usr/include/newlib']
        if 'dreifing_VALUE' in SLÓÐ.parts: Viðföng += ['-D__JKOROS__=1']
        if SLÓÐ.name=='búnt.c': Viðföng += ['-I'+str(verk_rót/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Hópur_VALUE = (씨.c_char_p*len(Viðföng))(*[færsla_VALUE.encode() for færsla_VALUE in Viðföng])
        Þýðing_eining = 분석(LOOKUP_INDEX,str(SLÓÐ).encode(),Hópur_VALUE,len(Viðföng),None,0,1)
        for INDEX in range(진단수(Þýðing_eining)):
            진단 = 진단얻기(Þýðing_eining,INDEX)
            if alvarleiki_VALUE(진단)>=3: 오류들.append((str(SLÓÐ.relative_to(verk_rót)),Texti(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(færsla_VALUE,yfireining_VALUE,gögn):
            Skrá,OFFSET_VALUE,Lína = staða_INDEX(færsla_VALUE)
            if Skrá not in 소유파일: return 2 if færsla_VALUE.종류==300 else 1
            낱말 = Texti(sækja_heiti(færsla_VALUE))
            if not 낱말 or any(ord(stafur_VALUE)>127 for stafur_VALUE in 낱말): return 2
            if færsla_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Texti(UNIQUE_heiti(færsla_VALUE)) or Skrá+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Skrá':Skrá,'OFFSET_VALUE':OFFSET_VALUE,'Lína':Lína,'종류':færsla_VALUE.종류,'Heiti':낱말,'Tengjast':연결종류(færsla_VALUE)}
                참조들.append((Skrá,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                tilvísun = sækja_tilvísun(færsla_VALUE)
                tilvísun_skrá,_,_ = staða_INDEX(tilvísun)
                if tilvísun_skrá in 소유파일:
                    UNIQUE_VALUE = Texti(UNIQUE_heiti(tilvísun)); 참조들.append((Skrá,OFFSET_VALUE,Texti(sækja_heiti(tilvísun)),UNIQUE_VALUE))
            return 2
        방문(rót_VALUE(Þýðing_eining),살피기,None)
        hætta_forrit(Þýðing_eining)
    endastaður_VALUE = verk_rót/'build/한국어화/시언어분석.json'
    endastaður_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Skrá:hashlib.sha256(Path(Skrá).read_bytes()).hexdigest() for Skrá in sorted(소유파일)}
    endastaður_VALUE.write_text(json.dumps({'skýrsla':선언들,'tilvísun':참조들,'Villa':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('skýrsla',len(선언들),'tilvísun',len(참조들),'Villa',len(오류들))
    for Villa in 오류들: print(*Villa)

if __name__=='__main__': keyra_skipun()
