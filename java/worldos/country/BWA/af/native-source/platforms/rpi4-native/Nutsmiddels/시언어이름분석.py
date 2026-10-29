#!/usr/bin/env python3
"""libclang verklaring·Naslaan 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_wortel = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class string_VALUE(씨.Structure): _fields_ = [('data',씨.c_void_p),('wys_VALUE',씨.c_uint)]
class loper_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class Posisie(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def funksie_VALUE(Naam, teruggee_maatreël, *인수):
    inskrywing_VALUE = getattr(구현, Naam); inskrywing_VALUE.restype = teruggee_maatreël; inskrywing_VALUE.argtypes = list(인수); return inskrywing_VALUE
kry_SMS = funksie_VALUE('clang_getCString',씨.c_char_p,string_VALUE)
stel_vry_SMS = funksie_VALUE('clang_disposeString',None,string_VALUE)
def Teks(VALUE):
    maatreël = (kry_SMS(VALUE) or b'').decode('utf-8'); stel_vry_SMS(VALUE); return maatreël
kry_naam = funksie_VALUE('clang_getCursorSpelling',string_VALUE,loper_VALUE)
kry_Naslaan = funksie_VALUE('clang_getCursorReferenced',loper_VALUE,loper_VALUE)
kry_plaas = funksie_VALUE('clang_getCursorLocation',Posisie,loper_VALUE)
lêer_plaas = funksie_VALUE('clang_getFileLocation',None,Posisie,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
lêer_inskrywing_naam = funksie_VALUE('clang_getFileName',string_VALUE,씨.c_void_p)
UNIQUE_naam = funksie_VALUE('clang_getCursorUSR',string_VALUE,loper_VALUE)
연결종류 = funksie_VALUE('clang_getCursorLinkage',씨.c_uint,loper_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,loper_VALUE,loper_VALUE,씨.c_void_p)
방문 = funksie_VALUE('clang_visitChildren',씨.c_uint,loper_VALUE,방문형,씨.c_void_p)
genereer = funksie_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = funksie_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
wortel_VALUE = funksie_VALUE('clang_getTranslationUnitCursor',loper_VALUE,씨.c_void_p)
gaan_uit_program = funksie_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = funksie_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = funksie_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
erns_VALUE = funksie_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = funksie_VALUE('clang_getDiagnosticSpelling',string_VALUE,씨.c_void_p)
진단해제 = funksie_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def plaas_INDEX(inskrywing_VALUE):
    Lêer = 씨.c_void_p(); lyn = 씨.c_uint(); gleuf_inskrywing = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    lêer_plaas(kry_plaas(inskrywing_VALUE),씨.byref(Lêer),씨.byref(lyn),씨.byref(gleuf_inskrywing),씨.byref(OFFSET_VALUE))
    return (Teks(lêer_inskrywing_naam(Lêer)) if Lêer else '', OFFSET_VALUE.value, lyn.value)

def uitvoer_bevel():
    LOOKUP_INDEX = genereer(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 verklaring 없이 TinyCC 외부 단일 Vertaal_bron 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, werklik_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Pad.resolve()) for Pad in Project_wortel.rglob('*') if Pad.suffix in ('.c','.h','.cpp','.inc')
              and not set(Pad.relative_to(Project_wortel).parts)&{'build','dist','vendor','__pycache__'}
              and Pad.relative_to(Project_wortel).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_wortel/'gebruiker'),
          '-I'+str(Project_wortel.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_wortel/'build'),'-I'+str(Project_wortel/'build/user'),
          '-I'+str(Project_wortel/'build/remote'),'-I'+str(Project_wortel/'vendor/bearssl/inc'),
          '-I'+str(Project_wortel/'vendor/bearssl/src'),'-I'+str(Project_wortel/'vendor/libassh/src'),
          '-I'+str(Project_wortel/'vendor/lwip/src/include'),'-I'+str(Project_wortel/'Netwerk_Stapel'),
          '-I'+str(Project_wortel/'afstands_VALUE'),'-I'+str(Project_wortel/'시언어번역기')]
    for Pad in sorted(Path(Naam) for Naam in 소유파일 if Naam.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Pad.suffix=='.cpp' else '-std=c11']
        if 'Netwerk_Stapel' in Pad.parts: 인수 += ['-I'+str(Project_wortel/'Netwerk_Stapel'),'-I'+str(Project_wortel/'vendor/lwip/src/include')]
        if '시언어번역기' in Pad.parts:
            인수 += ['-I'+str(Project_wortel/'시언어번역기'),'-I'+str(Project_wortel/'vendor/tinycc'),'-I'+str(Project_wortel/'build/ccompiler'),
                    '-isystem',str(Project_wortel.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_brug' in Pad.parts:
            인수 += ['-I'+str(Project_wortel/'PYTHON_brug'),'-I'+str(Project_wortel/'build/micropython-1.24.1'),'-I'+str(Project_wortel/'build/python'),'-isystem','/usr/include/newlib']
        if 'afstands_VALUE' in Pad.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Pad.parts: 인수 += ['-D__JKOROS__=1']
        if Pad.name=='bondel.c': 인수 += ['-I'+str(Project_wortel/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Groep_VALUE = (씨.c_char_p*len(인수))(*[inskrywing_VALUE.encode() for inskrywing_VALUE in 인수])
        Vertaling_les = 분석(LOOKUP_INDEX,str(Pad).encode(),Groep_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Vertaling_les)):
            진단 = 진단얻기(Vertaling_les,INDEX)
            if erns_VALUE(진단)>=3: 오류들.append((str(Pad.relative_to(Project_wortel)),Teks(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(inskrywing_VALUE,부모,data):
            Lêer,OFFSET_VALUE,lyn = plaas_INDEX(inskrywing_VALUE)
            if Lêer not in 소유파일: return 2 if inskrywing_VALUE.종류==300 else 1
            낱말 = Teks(kry_naam(inskrywing_VALUE))
            if not 낱말 or any(ord(karakter_VALUE)>127 for karakter_VALUE in 낱말): return 2
            if inskrywing_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Teks(UNIQUE_naam(inskrywing_VALUE)) or Lêer+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Lêer':Lêer,'OFFSET_VALUE':OFFSET_VALUE,'줄':lyn,'종류':inskrywing_VALUE.종류,'Naam':낱말,'Koppel':연결종류(inskrywing_VALUE)}
                참조들.append((Lêer,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Naslaan = kry_Naslaan(inskrywing_VALUE)
                Naslaan_lêer,_,_ = plaas_INDEX(Naslaan)
                if Naslaan_lêer in 소유파일:
                    UNIQUE_VALUE = Teks(UNIQUE_naam(Naslaan)); 참조들.append((Lêer,OFFSET_VALUE,Teks(kry_naam(Naslaan)),UNIQUE_VALUE))
            return 2
        방문(wortel_VALUE(Vertaling_les),살피기,None)
        gaan_uit_program(Vertaling_les)
    bestemming_VALUE = Project_wortel/'build/한국어화/시언어분석.json'
    bestemming_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Lêer:hashlib.sha256(Path(Lêer).read_bytes()).hexdigest() for Lêer in sorted(소유파일)}
    bestemming_VALUE.write_text(json.dumps({'verklaring':선언들,'Naslaan':참조들,'Fout':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('verklaring',len(선언들),'Naslaan',len(참조들),'Fout',len(오류들))
    for Fout in 오류들: print(*Fout)

if __name__=='__main__': uitvoer_bevel()
