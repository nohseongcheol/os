#!/usr/bin/env python3
"""libclang erklæring·referere 위치를 수집한다. ekstern_VERDI 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_kilde
import hashlib
import json
from pathlib import Path

speile_rot = Path(__file__).resolve().parents[1]
구현 = C_kilde.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class streng_VERDI(C_kilde.Structure): _fields_ = [('data',C_kilde.c_void_p),('vise_VERDI_487749b8',C_kilde.c_uint)]
class markør_VERDI(C_kilde.Structure): _fields_ = [('종류',C_kilde.c_uint),('보조',C_kilde.c_int),('data',C_kilde.c_void_p*3)]
class Posisjon(C_kilde.Structure): _fields_ = [('data',C_kilde.c_void_p*2),('FORSKYVNING_VERDI',C_kilde.c_uint)]
def FUNKSJON_VERDI(Navn, return_KR, *Argumenter):
    oppføring_VERDI = getattr(구현, Navn); oppføring_VERDI.restype = return_KR; oppføring_VERDI.argtypes = list(Argumenter); return oppføring_VERDI
hente_SMS = FUNKSJON_VERDI('clang_getCString',C_kilde.c_char_p,streng_VERDI)
frigi_SMS = FUNKSJON_VERDI('clang_disposeString',None,streng_VERDI)
def Tekst(VERDI):
    KR = (hente_SMS(VERDI) or b'').decode('utf-8'); frigi_SMS(VERDI); return KR
hente_navn = FUNKSJON_VERDI('clang_getCursorSpelling',streng_VERDI,markør_VERDI)
hente_referere = FUNKSJON_VERDI('clang_getCursorReferenced',markør_VERDI,markør_VERDI)
hente_plassere = FUNKSJON_VERDI('clang_getCursorLocation',Posisjon,markør_VERDI)
Fil_plassere = FUNKSJON_VERDI('clang_getFileLocation',None,Posisjon,C_kilde.POINTER(C_kilde.c_void_p),C_kilde.POINTER(C_kilde.c_uint),C_kilde.POINTER(C_kilde.c_uint),C_kilde.POINTER(C_kilde.c_uint))
Fil_oppføring_navn = FUNKSJON_VERDI('clang_getFileName',streng_VERDI,C_kilde.c_void_p)
UNIK_navn = FUNKSJON_VERDI('clang_getCursorUSR',streng_VERDI,markør_VERDI)
연결종류 = FUNKSJON_VERDI('clang_getCursorLinkage',C_kilde.c_uint,markør_VERDI)
방문형 = C_kilde.CFUNCTYPE(C_kilde.c_uint,markør_VERDI,markør_VERDI,C_kilde.c_void_p)
방문 = FUNKSJON_VERDI('clang_visitChildren',C_kilde.c_uint,markør_VERDI,방문형,C_kilde.c_void_p)
generere = FUNKSJON_VERDI('clang_createIndex',C_kilde.c_void_p,C_kilde.c_int,C_kilde.c_int)
Analyser_VERDI = FUNKSJON_VERDI('clang_parseTranslationUnit',C_kilde.c_void_p,C_kilde.c_void_p,C_kilde.c_char_p,C_kilde.POINTER(C_kilde.c_char_p),C_kilde.c_int,C_kilde.c_void_p,C_kilde.c_uint,C_kilde.c_uint)
rot_VERDI = FUNKSJON_VERDI('clang_getTranslationUnitCursor',markør_VERDI,C_kilde.c_void_p)
avslutt_app = FUNKSJON_VERDI('clang_disposeTranslationUnit',None,C_kilde.c_void_p)
진단수 = FUNKSJON_VERDI('clang_getNumDiagnostics',C_kilde.c_uint,C_kilde.c_void_p)
진단얻기 = FUNKSJON_VERDI('clang_getDiagnostic',C_kilde.c_void_p,C_kilde.c_void_p,C_kilde.c_uint)
alvorsgrad_VERDI = FUNKSJON_VERDI('clang_getDiagnosticSeverity',C_kilde.c_uint,C_kilde.c_void_p)
진단문 = FUNKSJON_VERDI('clang_getDiagnosticSpelling',streng_VERDI,C_kilde.c_void_p)
진단해제 = FUNKSJON_VERDI('clang_disposeDiagnostic',None,C_kilde.c_void_p)

def posisjonsindeks(oppføring_VERDI):
    Fil = C_kilde.c_void_p(); Linje = C_kilde.c_uint(); åpning_oppføring = C_kilde.c_uint(); FORSKYVNING_VERDI = C_kilde.c_uint()
    Fil_plassere(hente_plassere(oppføring_VERDI),C_kilde.byref(Fil),C_kilde.byref(Linje),C_kilde.byref(åpning_oppføring),C_kilde.byref(FORSKYVNING_VERDI))
    return (Tekst(Fil_oppføring_navn(Fil)) if Fil else '', FORSKYVNING_VERDI.value, Linje.value)

def Utfør_kommando():
    Oppslag_INDEKS = generere(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilator_verktøy.c는 eget erklæring 없이 TinyCC ekstern_VERDI 단일 OVERSETT_kilde 단위만 포함한다.
    # ekstern_VERDI 선언을 eget 이름으로 세지 않으며, faktisk_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Sti.resolve()) for Sti in speile_rot.rglob('*') if Sti.suffix in ('.c','.h','.cpp','.inc')
              and not set(Sti.relative_to(speile_rot).parts)&{'build','dist','vendor','__pycache__'}
              and Sti.relative_to(speile_rot).as_posix() != 'C_kompilator/kompilator_verktøy.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(speile_rot/'bruker'),
          '-I'+str(speile_rot.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(speile_rot/'build'),'-I'+str(speile_rot/'build/user'),
          '-I'+str(speile_rot/'build/remote'),'-I'+str(speile_rot/'vendor/bearssl/inc'),
          '-I'+str(speile_rot/'vendor/bearssl/src'),'-I'+str(speile_rot/'vendor/libassh/src'),
          '-I'+str(speile_rot/'vendor/lwip/src/include'),'-I'+str(speile_rot/'nettverk_stakk'),
          '-I'+str(speile_rot/'ekstern_VERDI_28edcfa1'),'-I'+str(speile_rot/'C_kompilator')]
    for Sti in sorted(Path(Navn) for Navn in 소유파일 if Navn.endswith(('.c','.cpp'))):
        Argumenter = 공통 + ['-std=c++11' if Sti.suffix=='.cpp' else '-std=c11']
        if 'nettverk_stakk' in Sti.parts: Argumenter += ['-I'+str(speile_rot/'nettverk_stakk'),'-I'+str(speile_rot/'vendor/lwip/src/include')]
        if 'C_kompilator' in Sti.parts:
            Argumenter += ['-I'+str(speile_rot/'C_kompilator'),'-I'+str(speile_rot/'vendor/tinycc'),'-I'+str(speile_rot/'build/ccompiler'),
                    '-isystem',str(speile_rot.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_bro' in Sti.parts:
            Argumenter += ['-I'+str(speile_rot/'PYTHON_bro'),'-I'+str(speile_rot/'build/micropython-1.24.1'),'-I'+str(speile_rot/'build/python'),'-isystem','/usr/include/newlib']
        if 'ekstern_VERDI_28edcfa1' in Sti.parts:
            Argumenter += ['-isystem', '/usr/include/newlib']
        if 'distribusjon_VERDI' in Sti.parts: Argumenter += ['-D__JKOROS__=1']
        if Sti.name=='bunt.c': Argumenter += ['-I'+str(speile_rot/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        gruppe_VERDI = (C_kilde.c_char_p*len(Argumenter))(*[oppføring_VERDI.encode() for oppføring_VERDI in Argumenter])
        Oversettelse_enhet = Analyser_VERDI(Oppslag_INDEKS,str(Sti).encode(),gruppe_VERDI,len(Argumenter),None,0,1)
        for INDEKS in range(진단수(Oversettelse_enhet)):
            진단 = 진단얻기(Oversettelse_enhet,INDEKS)
            if alvorsgrad_VERDI(진단)>=3: 오류들.append((str(Sti.relative_to(speile_rot)),Tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(oppføring_VERDI,overordnet_VERDI_881a8172,data):
            Fil,FORSKYVNING_VERDI,Linje = posisjonsindeks(oppføring_VERDI)
            if Fil not in 소유파일: return 2 if oppføring_VERDI.종류==300 else 1
            낱말 = Tekst(hente_navn(oppføring_VERDI))
            if not 낱말 or any(ord(tegn_VERDI)>127 for tegn_VERDI in 낱말): return 2
            if oppføring_VERDI.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIK_VERDI = Tekst(UNIK_navn(oppføring_VERDI)) or Fil+':'+str(FORSKYVNING_VERDI)
                선언들[UNIK_VERDI] = {'Fil':Fil,'FORSKYVNING_VERDI':FORSKYVNING_VERDI,'Linje':Linje,'종류':oppføring_VERDI.종류,'Navn':낱말,'Koble_til':연결종류(oppføring_VERDI)}
                참조들.append((Fil,FORSKYVNING_VERDI,낱말,UNIK_VERDI))
            else:
                referere = hente_referere(oppføring_VERDI)
                referere_Fil,_,_ = posisjonsindeks(referere)
                if referere_Fil in 소유파일:
                    UNIK_VERDI = Tekst(UNIK_navn(referere)); 참조들.append((Fil,FORSKYVNING_VERDI,Tekst(hente_navn(referere)),UNIK_VERDI))
            return 2
        방문(rot_VERDI(Oversettelse_enhet),살피기,None)
        avslutt_app(Oversettelse_enhet)
    mål_VERDI = speile_rot/'build/한국어화/시언어분석.json'
    mål_VERDI.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fil:hashlib.sha256(Path(Fil).read_bytes()).hexdigest() for Fil in sorted(소유파일)}
    mål_VERDI.write_text(json.dumps({'erklæring':선언들,'referere':참조들,'feil':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('erklæring',len(선언들),'referere',len(참조들),'feil',len(오류들))
    for feil in 오류들: print(*feil)

if __name__=='__main__': Utfør_kommando()
