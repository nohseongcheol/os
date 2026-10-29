#!/usr/bin/env python3
"""libclang erklæring·referere 위치를 수집한다. ekstern_VÆRDI 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_kilde
import hashlib
import json
from pathlib import Path

To_do_rod = Path(__file__).resolve().parents[1]
구현 = C_kilde.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class streng_VÆRDI(C_kilde.Structure): _fields_ = [('data',C_kilde.c_void_p),('vise_VÆRDI',C_kilde.c_uint)]
class markør_VÆRDI(C_kilde.Structure): _fields_ = [('종류',C_kilde.c_uint),('보조',C_kilde.c_int),('data',C_kilde.c_void_p*3)]
class Placering(C_kilde.Structure): _fields_ = [('data',C_kilde.c_void_p*2),('FORSKYDNING_VÆRDI',C_kilde.c_uint)]
def FUNKTION_VÆRDI(Navn, returnere_KR, *Argumenter):
    post_VÆRDI_962f286b = getattr(구현, Navn); post_VÆRDI_962f286b.restype = returnere_KR; post_VÆRDI_962f286b.argtypes = list(Argumenter); return post_VÆRDI_962f286b
hente_sms = FUNKTION_VÆRDI('clang_getCString',C_kilde.c_char_p,streng_VÆRDI)
udgive_sms = FUNKTION_VÆRDI('clang_disposeString',None,streng_VÆRDI)
def Tekst(VÆRDI):
    KR = (hente_sms(VÆRDI) or b'').decode('utf-8'); udgive_sms(VÆRDI); return KR
hente_navn = FUNKTION_VÆRDI('clang_getCursorSpelling',streng_VÆRDI,markør_VÆRDI)
hente_referere = FUNKTION_VÆRDI('clang_getCursorReferenced',markør_VÆRDI,markør_VÆRDI)
hente_placere = FUNKTION_VÆRDI('clang_getCursorLocation',Placering,markør_VÆRDI)
fil_placere = FUNKTION_VÆRDI('clang_getFileLocation',None,Placering,C_kilde.POINTER(C_kilde.c_void_p),C_kilde.POINTER(C_kilde.c_uint),C_kilde.POINTER(C_kilde.c_uint),C_kilde.POINTER(C_kilde.c_uint))
fil_post_navn = FUNKTION_VÆRDI('clang_getFileName',streng_VÆRDI,C_kilde.c_void_p)
ENTYDIGE_navn = FUNKTION_VÆRDI('clang_getCursorUSR',streng_VÆRDI,markør_VÆRDI)
연결종류 = FUNKTION_VÆRDI('clang_getCursorLinkage',C_kilde.c_uint,markør_VÆRDI)
방문형 = C_kilde.CFUNCTYPE(C_kilde.c_uint,markør_VÆRDI,markør_VÆRDI,C_kilde.c_void_p)
방문 = FUNKTION_VÆRDI('clang_visitChildren',C_kilde.c_uint,markør_VÆRDI,방문형,C_kilde.c_void_p)
generere = FUNKTION_VÆRDI('clang_createIndex',C_kilde.c_void_p,C_kilde.c_int,C_kilde.c_int)
Analyse_VÆRDI = FUNKTION_VÆRDI('clang_parseTranslationUnit',C_kilde.c_void_p,C_kilde.c_void_p,C_kilde.c_char_p,C_kilde.POINTER(C_kilde.c_char_p),C_kilde.c_int,C_kilde.c_void_p,C_kilde.c_uint,C_kilde.c_uint)
rod_VÆRDI = FUNKTION_VÆRDI('clang_getTranslationUnitCursor',markør_VÆRDI,C_kilde.c_void_p)
afslut_app = FUNKTION_VÆRDI('clang_disposeTranslationUnit',None,C_kilde.c_void_p)
진단수 = FUNKTION_VÆRDI('clang_getNumDiagnostics',C_kilde.c_uint,C_kilde.c_void_p)
진단얻기 = FUNKTION_VÆRDI('clang_getDiagnostic',C_kilde.c_void_p,C_kilde.c_void_p,C_kilde.c_uint)
alvorsgrad_VÆRDI = FUNKTION_VÆRDI('clang_getDiagnosticSeverity',C_kilde.c_uint,C_kilde.c_void_p)
진단문 = FUNKTION_VÆRDI('clang_getDiagnosticSpelling',streng_VÆRDI,C_kilde.c_void_p)
진단해제 = FUNKTION_VÆRDI('clang_disposeDiagnostic',None,C_kilde.c_void_p)

def positionsindeks(post_VÆRDI_962f286b):
    Fil = C_kilde.c_void_p(); Linje = C_kilde.c_uint(); udvidelsesstik_post = C_kilde.c_uint(); FORSKYDNING_VÆRDI = C_kilde.c_uint()
    fil_placere(hente_placere(post_VÆRDI_962f286b),C_kilde.byref(Fil),C_kilde.byref(Linje),C_kilde.byref(udvidelsesstik_post),C_kilde.byref(FORSKYDNING_VÆRDI))
    return (Tekst(fil_post_navn(Fil)) if Fil else '', FORSKYDNING_VÆRDI.value, Linje.value)

def Udfør_kommando():
    Opslag_INDEKS = generere(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # compiler_værktøj.c는 eget erklæring 없이 TinyCC ekstern_VÆRDI 단일 OVERSÆT_kilde 단위만 포함한다.
    # ekstern_VÆRDI 선언을 eget 이름으로 세지 않으며, faktisk_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Sti.resolve()) for Sti in To_do_rod.rglob('*') if Sti.suffix in ('.c','.h','.cpp','.inc')
              and not set(Sti.relative_to(To_do_rod).parts)&{'build','dist','vendor','__pycache__'}
              and Sti.relative_to(To_do_rod).as_posix() != 'C_compiler/compiler_værktøj.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(To_do_rod/'bruger'),
          '-I'+str(To_do_rod.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(To_do_rod/'build'),'-I'+str(To_do_rod/'build/user'),
          '-I'+str(To_do_rod/'build/remote'),'-I'+str(To_do_rod/'vendor/bearssl/inc'),
          '-I'+str(To_do_rod/'vendor/bearssl/src'),'-I'+str(To_do_rod/'vendor/libassh/src'),
          '-I'+str(To_do_rod/'vendor/lwip/src/include'),'-I'+str(To_do_rod/'netværk_Stak'),
          '-I'+str(To_do_rod/'fjern_VÆRDI'),'-I'+str(To_do_rod/'C_compiler')]
    for Sti in sorted(Path(Navn) for Navn in 소유파일 if Navn.endswith(('.c','.cpp'))):
        Argumenter = 공통 + ['-std=c++11' if Sti.suffix=='.cpp' else '-std=c11']
        if 'netværk_Stak' in Sti.parts: Argumenter += ['-I'+str(To_do_rod/'netværk_Stak'),'-I'+str(To_do_rod/'vendor/lwip/src/include')]
        if 'C_compiler' in Sti.parts:
            Argumenter += ['-I'+str(To_do_rod/'C_compiler'),'-I'+str(To_do_rod/'vendor/tinycc'),'-I'+str(To_do_rod/'build/ccompiler'),
                    '-isystem',str(To_do_rod.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_bro' in Sti.parts:
            Argumenter += ['-I'+str(To_do_rod/'PYTHON_bro'),'-I'+str(To_do_rod/'build/micropython-1.24.1'),'-I'+str(To_do_rod/'build/python'),'-isystem','/usr/include/newlib']
        if 'fjern_VÆRDI' in Sti.parts:
            Argumenter += ['-isystem', '/usr/include/newlib']
        if 'distribution_VÆRDI' in Sti.parts: Argumenter += ['-D__JKOROS__=1']
        if Sti.name=='bundt.c': Argumenter += ['-I'+str(To_do_rod/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        gruppe_VÆRDI = (C_kilde.c_char_p*len(Argumenter))(*[post_VÆRDI_962f286b.encode() for post_VÆRDI_962f286b in Argumenter])
        Oversættelse_enhed = Analyse_VÆRDI(Opslag_INDEKS,str(Sti).encode(),gruppe_VÆRDI,len(Argumenter),None,0,1)
        for INDEKS in range(진단수(Oversættelse_enhed)):
            진단 = 진단얻기(Oversættelse_enhed,INDEKS)
            if alvorsgrad_VÆRDI(진단)>=3: 오류들.append((str(Sti.relative_to(To_do_rod)),Tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(post_VÆRDI_962f286b,overordnet_VÆRDI,data):
            Fil,FORSKYDNING_VÆRDI,Linje = positionsindeks(post_VÆRDI_962f286b)
            if Fil not in 소유파일: return 2 if post_VÆRDI_962f286b.종류==300 else 1
            낱말 = Tekst(hente_navn(post_VÆRDI_962f286b))
            if not 낱말 or any(ord(tegn_VÆRDI)>127 for tegn_VÆRDI in 낱말): return 2
            if post_VÆRDI_962f286b.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                ENTYDIGE_VÆRDI = Tekst(ENTYDIGE_navn(post_VÆRDI_962f286b)) or Fil+':'+str(FORSKYDNING_VÆRDI)
                선언들[ENTYDIGE_VÆRDI] = {'Fil':Fil,'FORSKYDNING_VÆRDI':FORSKYDNING_VÆRDI,'Linje':Linje,'종류':post_VÆRDI_962f286b.종류,'Navn':낱말,'Tilslut':연결종류(post_VÆRDI_962f286b)}
                참조들.append((Fil,FORSKYDNING_VÆRDI,낱말,ENTYDIGE_VÆRDI))
            else:
                referere = hente_referere(post_VÆRDI_962f286b)
                referere_fil,_,_ = positionsindeks(referere)
                if referere_fil in 소유파일:
                    ENTYDIGE_VÆRDI = Tekst(ENTYDIGE_navn(referere)); 참조들.append((Fil,FORSKYDNING_VÆRDI,Tekst(hente_navn(referere)),ENTYDIGE_VÆRDI))
            return 2
        방문(rod_VÆRDI(Oversættelse_enhed),살피기,None)
        afslut_app(Oversættelse_enhed)
    destination_VÆRDI = To_do_rod/'build/한국어화/시언어분석.json'
    destination_VÆRDI.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fil:hashlib.sha256(Path(Fil).read_bytes()).hexdigest() for Fil in sorted(소유파일)}
    destination_VÆRDI.write_text(json.dumps({'erklæring':선언들,'referere':참조들,'fejl':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('erklæring',len(선언들),'referere',len(참조들),'fejl',len(오류들))
    for fejl in 오류들: print(*fejl)

if __name__=='__main__': Udfør_kommando()
