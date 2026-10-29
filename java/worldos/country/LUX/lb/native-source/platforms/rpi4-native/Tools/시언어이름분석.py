#!/usr/bin/env python3
"""libclang 선언·Referenzen 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

projezéieren_Racinn = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class Zeechefolleg_VALUE(씨.Structure): _fields_ = [('Daten',씨.c_void_p),('Show_VALUE',씨.c_uint)]
class Curseur_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('Daten',씨.c_void_p*3)]
class positionéieren(씨.Structure): _fields_ = [('Daten',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def FUNCTION_VALUE(Numm, 반환, *인수):
    Agab_VALUE = getattr(구현, Numm); Agab_VALUE.restype = 반환; Agab_VALUE.argtypes = list(인수); return Agab_VALUE
글얻기 = FUNCTION_VALUE('clang_getCString',씨.c_char_p,Zeechefolleg_VALUE)
Versioun_SMS = FUNCTION_VALUE('clang_disposeString',None,Zeechefolleg_VALUE)
def SMS(VALUE):
    Mooss = (글얻기(VALUE) or b'').decode('utf-8'); Versioun_SMS(VALUE); return Mooss
이름얻기 = FUNCTION_VALUE('clang_getCursorSpelling',Zeechefolleg_VALUE,Curseur_VALUE)
참조얻기 = FUNCTION_VALUE('clang_getCursorReferenced',Curseur_VALUE,Curseur_VALUE)
위치얻기 = FUNCTION_VALUE('clang_getCursorLocation',positionéieren,Curseur_VALUE)
Fichier_positionéieren = FUNCTION_VALUE('clang_getFileLocation',None,positionéieren,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
Fichier_Agab_Numm = FUNCTION_VALUE('clang_getFileName',Zeechefolleg_VALUE,씨.c_void_p)
UNIQUE_Numm = FUNCTION_VALUE('clang_getCursorUSR',Zeechefolleg_VALUE,Curseur_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,Curseur_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,Curseur_VALUE,Curseur_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,Curseur_VALUE,방문형,씨.c_void_p)
generéieren = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
Racinn_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',Curseur_VALUE,씨.c_void_p)
verloossen_App = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
Gewiicht_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',Zeechefolleg_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def positionéieren_INDEX(Agab_VALUE):
    Fichier = 씨.c_void_p(); Zeil = 씨.c_uint(); Slot_Agab = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    Fichier_positionéieren(위치얻기(Agab_VALUE),씨.byref(Fichier),씨.byref(Zeil),씨.byref(Slot_Agab),씨.byref(OFFSET_VALUE))
    return (SMS(Fichier_Agab_Numm(Fichier)) if Fichier else '', OFFSET_VALUE.value, Zeil.value)

def ausféieren_Befeel():
    LOOKUP_INDEX = generéieren(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 TRANSLATE_Quell 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, aktuell_Daten 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Wee.resolve()) for Wee in projezéieren_Racinn.rglob('*') if Wee.suffix in ('.c','.h','.cpp','.inc')
              and not set(Wee.relative_to(projezéieren_Racinn).parts)&{'build','dist','vendor','__pycache__'}
              and Wee.relative_to(projezéieren_Racinn).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(projezéieren_Racinn/'Benotzer'),
          '-I'+str(projezéieren_Racinn.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(projezéieren_Racinn/'build'),'-I'+str(projezéieren_Racinn/'build/user'),
          '-I'+str(projezéieren_Racinn/'build/remote'),'-I'+str(projezéieren_Racinn/'vendor/bearssl/inc'),
          '-I'+str(projezéieren_Racinn/'vendor/bearssl/src'),'-I'+str(projezéieren_Racinn/'vendor/libassh/src'),
          '-I'+str(projezéieren_Racinn/'vendor/lwip/src/include'),'-I'+str(projezéieren_Racinn/'Reseau_Stapel'),
          '-I'+str(projezéieren_Racinn/'extern_VALUE'),'-I'+str(projezéieren_Racinn/'시언어번역기')]
    for Wee in sorted(Path(Numm) for Numm in 소유파일 if Numm.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Wee.suffix=='.cpp' else '-std=c11']
        if 'Reseau_Stapel' in Wee.parts: 인수 += ['-I'+str(projezéieren_Racinn/'Reseau_Stapel'),'-I'+str(projezéieren_Racinn/'vendor/lwip/src/include')]
        if '시언어번역기' in Wee.parts:
            인수 += ['-I'+str(projezéieren_Racinn/'시언어번역기'),'-I'+str(projezéieren_Racinn/'vendor/tinycc'),'-I'+str(projezéieren_Racinn/'build/ccompiler'),
                    '-isystem',str(projezéieren_Racinn.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_Bréck' in Wee.parts:
            인수 += ['-I'+str(projezéieren_Racinn/'PYTHON_Bréck'),'-I'+str(projezéieren_Racinn/'build/micropython-1.24.1'),'-I'+str(projezéieren_Racinn/'build/python'),'-isystem','/usr/include/newlib']
        if 'extern_VALUE' in Wee.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Wee.parts: 인수 += ['-D__JKOROS__=1']
        if Wee.name=='Bëndel.c': 인수 += ['-I'+str(projezéieren_Racinn/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grupp_VALUE = (씨.c_char_p*len(인수))(*[Agab_VALUE.encode() for Agab_VALUE in 인수])
        Iwwersetzung_Lektioun = 분석(LOOKUP_INDEX,str(Wee).encode(),Grupp_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(Iwwersetzung_Lektioun)):
            진단 = 진단얻기(Iwwersetzung_Lektioun,INDEX)
            if Gewiicht_VALUE(진단)>=3: 오류들.append((str(Wee.relative_to(projezéieren_Racinn)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(Agab_VALUE,부모,Daten):
            Fichier,OFFSET_VALUE,Zeil = positionéieren_INDEX(Agab_VALUE)
            if Fichier not in 소유파일: return 2 if Agab_VALUE.종류==300 else 1
            낱말 = SMS(이름얻기(Agab_VALUE))
            if not 낱말 or any(ord(Zeechen_VALUE)>127 for Zeechen_VALUE in 낱말): return 2
            if Agab_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = SMS(UNIQUE_Numm(Agab_VALUE)) or Fichier+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Fichier':Fichier,'OFFSET_VALUE':OFFSET_VALUE,'줄':Zeil,'종류':Agab_VALUE.종류,'Numm':낱말,'Verbannen':연결종류(Agab_VALUE)}
                참조들.append((Fichier,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Referenzen = 참조얻기(Agab_VALUE)
                Referenzen_Fichier,_,_ = positionéieren_INDEX(Referenzen)
                if Referenzen_Fichier in 소유파일:
                    UNIQUE_VALUE = SMS(UNIQUE_Numm(Referenzen)); 참조들.append((Fichier,OFFSET_VALUE,SMS(이름얻기(Referenzen)),UNIQUE_VALUE))
            return 2
        방문(Racinn_VALUE(Iwwersetzung_Lektioun),살피기,None)
        verloossen_App(Iwwersetzung_Lektioun)
    Zil_VALUE = projezéieren_Racinn/'build/한국어화/시언어분석.json'
    Zil_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fichier:hashlib.sha256(Path(Fichier).read_bytes()).hexdigest() for Fichier in sorted(소유파일)}
    Zil_VALUE.write_text(json.dumps({'선언':선언들,'Referenzen':참조들,'Feeler':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Referenzen',len(참조들),'Feeler',len(오류들))
    for Feeler in 오류들: print(*Feeler)

if __name__=='__main__': ausféieren_Befeel()
