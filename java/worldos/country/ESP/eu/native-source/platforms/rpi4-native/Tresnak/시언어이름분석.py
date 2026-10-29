#!/usr/bin/env python3
"""libclang deklarazio·Erreferentzia_materiala 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

Project_erro = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class kate_balio(씨.Structure): _fields_ = [('datuak',씨.c_void_p),('erakutsi_balio',씨.c_uint)]
class kurtsore_balio(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('datuak',씨.c_void_p*3)]
class Posizioa(씨.Structure): _fields_ = [('datuak',씨.c_void_p*2),('Geruzak_balio',씨.c_uint)]
def FUNTZIOA_balio(Izena, itzuli_neurria, *Argumentuak):
    sarrera_balio = getattr(구현, Izena); sarrera_balio.restype = itzuli_neurria; sarrera_balio.argtypes = list(Argumentuak); return sarrera_balio
eskuratu_SMS = FUNTZIOA_balio('clang_getCString',씨.c_char_p,kate_balio)
askatu_SMS = FUNTZIOA_balio('clang_disposeString',None,kate_balio)
def Testua(balio):
    EMAITZA = (eskuratu_SMS(balio) or b'').decode('utf-8'); askatu_SMS(balio); return EMAITZA
eskuratu_izen = FUNTZIOA_balio('clang_getCursorSpelling',kate_balio,kurtsore_balio)
eskuratu_Erreferentzia_materiala = FUNTZIOA_balio('clang_getCursorReferenced',kurtsore_balio,kurtsore_balio)
eskuratu_kargu = FUNTZIOA_balio('clang_getCursorLocation',Posizioa,kurtsore_balio)
fitxategi_kargu = FUNTZIOA_balio('clang_getFileLocation',None,Posizioa,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fitxategi_sarrera_izen = FUNTZIOA_balio('clang_getFileName',kate_balio,씨.c_void_p)
ESKLUSIBOAK_izen = FUNTZIOA_balio('clang_getCursorUSR',kate_balio,kurtsore_balio)
연결종류 = FUNTZIOA_balio('clang_getCursorLinkage',씨.c_uint,kurtsore_balio)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kurtsore_balio,kurtsore_balio,씨.c_void_p)
방문 = FUNTZIOA_balio('clang_visitChildren',씨.c_uint,kurtsore_balio,방문형,씨.c_void_p)
sortu = FUNTZIOA_balio('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
Analizatu_balio = FUNTZIOA_balio('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
erro_balio = FUNTZIOA_balio('clang_getTranslationUnitCursor',kurtsore_balio,씨.c_void_p)
irten_aplik_55b3a1cd = FUNTZIOA_balio('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNTZIOA_balio('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNTZIOA_balio('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
larritasun_balio = FUNTZIOA_balio('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNTZIOA_balio('clang_getDiagnosticSpelling',kate_balio,씨.c_void_p)
진단해제 = FUNTZIOA_balio('clang_disposeDiagnostic',None,씨.c_void_p)

def kargu_INDIZE(sarrera_balio):
    Fitxategia = 씨.c_void_p(); Marra = 씨.c_uint(); 칸 = 씨.c_uint(); Geruzak_balio = 씨.c_uint()
    fitxategi_kargu(eskuratu_kargu(sarrera_balio),씨.byref(Fitxategia),씨.byref(Marra),씨.byref(칸),씨.byref(Geruzak_balio))
    return (Testua(fitxategi_sarrera_izen(Fitxategia)) if Fitxategia else '', Geruzak_balio.value, Marra.value)

def exekutatu_komando():
    BEGIRATU_INDIZE = sortu(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 deklarazio 없이 TinyCC 외부 단일 ITZULI_iturburu 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, benetako_datuak 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Bide_izena.resolve()) for Bide_izena in Project_erro.rglob('*') if Bide_izena.suffix in ('.c','.h','.cpp','.inc')
              and not set(Bide_izena.relative_to(Project_erro).parts)&{'build','dist','vendor','__pycache__'}
              and Bide_izena.relative_to(Project_erro).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(Project_erro/'erabiltzaile'),
          '-I'+str(Project_erro.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(Project_erro/'build'),'-I'+str(Project_erro/'build/user'),
          '-I'+str(Project_erro/'build/remote'),'-I'+str(Project_erro/'vendor/bearssl/inc'),
          '-I'+str(Project_erro/'vendor/bearssl/src'),'-I'+str(Project_erro/'vendor/libassh/src'),
          '-I'+str(Project_erro/'vendor/lwip/src/include'),'-I'+str(Project_erro/'sare_pila'),
          '-I'+str(Project_erro/'urruneko_balio'),'-I'+str(Project_erro/'시언어번역기')]
    for Bide_izena in sorted(Path(Izena) for Izena in 소유파일 if Izena.endswith(('.c','.cpp'))):
        Argumentuak = 공통 + ['-std=c++11' if Bide_izena.suffix=='.cpp' else '-std=c11']
        if 'sare_pila' in Bide_izena.parts: Argumentuak += ['-I'+str(Project_erro/'sare_pila'),'-I'+str(Project_erro/'vendor/lwip/src/include')]
        if '시언어번역기' in Bide_izena.parts:
            Argumentuak += ['-I'+str(Project_erro/'시언어번역기'),'-I'+str(Project_erro/'vendor/tinycc'),'-I'+str(Project_erro/'build/ccompiler'),
                    '-isystem',str(Project_erro.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_zubi' in Bide_izena.parts:
            Argumentuak += ['-I'+str(Project_erro/'PYTHON_zubi'),'-I'+str(Project_erro/'build/micropython-1.24.1'),'-I'+str(Project_erro/'build/python'),'-isystem','/usr/include/newlib']
        if 'urruneko_balio' in Bide_izena.parts:
            Argumentuak += ['-isystem', '/usr/include/newlib']
        if '배포' in Bide_izena.parts: Argumentuak += ['-D__JKOROS__=1']
        if Bide_izena.name=='multzo.c': Argumentuak += ['-I'+str(Project_erro/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        talde_balio = (씨.c_char_p*len(Argumentuak))(*[sarrera_balio.encode() for sarrera_balio in Argumentuak])
        Itzulpena_unitate = Analizatu_balio(BEGIRATU_INDIZE,str(Bide_izena).encode(),talde_balio,len(Argumentuak),None,0,1)
        for INDIZE in range(진단수(Itzulpena_unitate)):
            진단 = 진단얻기(Itzulpena_unitate,INDIZE)
            if larritasun_balio(진단)>=3: 오류들.append((str(Bide_izena.relative_to(Project_erro)),Testua(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(sarrera_balio,부모,datuak):
            Fitxategia,Geruzak_balio,Marra = kargu_INDIZE(sarrera_balio)
            if Fitxategia not in 소유파일: return 2 if sarrera_balio.종류==300 else 1
            낱말 = Testua(eskuratu_izen(sarrera_balio))
            if not 낱말 or any(ord(karaktere_balio)>127 for karaktere_balio in 낱말): return 2
            if sarrera_balio.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                ESKLUSIBOAK_balio = Testua(ESKLUSIBOAK_izen(sarrera_balio)) or Fitxategia+':'+str(Geruzak_balio)
                선언들[ESKLUSIBOAK_balio] = {'Fitxategia':Fitxategia,'Geruzak_balio':Geruzak_balio,'Marra':Marra,'종류':sarrera_balio.종류,'Izena':낱말,'Konektatu':연결종류(sarrera_balio)}
                참조들.append((Fitxategia,Geruzak_balio,낱말,ESKLUSIBOAK_balio))
            else:
                Erreferentzia_materiala = eskuratu_Erreferentzia_materiala(sarrera_balio)
                Erreferentzia_materiala_fitxategi,_,_ = kargu_INDIZE(Erreferentzia_materiala)
                if Erreferentzia_materiala_fitxategi in 소유파일:
                    ESKLUSIBOAK_balio = Testua(ESKLUSIBOAK_izen(Erreferentzia_materiala)); 참조들.append((Fitxategia,Geruzak_balio,Testua(eskuratu_izen(Erreferentzia_materiala)),ESKLUSIBOAK_balio))
            return 2
        방문(erro_balio(Itzulpena_unitate),살피기,None)
        irten_aplik_55b3a1cd(Itzulpena_unitate)
    helburu_balio_a0fbc067 = Project_erro/'build/한국어화/시언어분석.json'
    helburu_balio_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fitxategia:hashlib.sha256(Path(Fitxategia).read_bytes()).hexdigest() for Fitxategia in sorted(소유파일)}
    helburu_balio_a0fbc067.write_text(json.dumps({'deklarazio':선언들,'Erreferentzia_materiala':참조들,'errorea':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklarazio',len(선언들),'Erreferentzia_materiala',len(참조들),'errorea',len(오류들))
    for errorea in 오류들: print(*errorea)

if __name__=='__main__': exekutatu_komando()
