#!/usr/bin/env python3
"""libclang bevallás·hivatkozik 위치를 수집한다. külső_ÉRTÉK 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_forrás
import hashlib
import json
from pathlib import Path

teendő_gyök = Path(__file__).resolve().parents[1]
구현 = C_forrás.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class sztring_ÉRTÉK(C_forrás.Structure): _fields_ = [('adat',C_forrás.c_void_p),('bemutató_ÉRTÉK',C_forrás.c_uint)]
class kurzor_ÉRTÉK(C_forrás.Structure): _fields_ = [('Altípus_ÉRTÉK',C_forrás.c_uint),('보조',C_forrás.c_int),('adat',C_forrás.c_void_p*3)]
class Pozíció(C_forrás.Structure): _fields_ = [('adat',C_forrás.c_void_p*2),('Ofszet_ÉRTÉK',C_forrás.c_uint)]
def FÜGGVÉNY_ÉRTÉK(Név, visszaküld_KR, *Argumentumok):
    bejegyzés_ÉRTÉK = getattr(구현, Név); bejegyzés_ÉRTÉK.restype = visszaküld_KR; bejegyzés_ÉRTÉK.argtypes = list(Argumentumok); return bejegyzés_ÉRTÉK
áthúz_SMS = FÜGGVÉNY_ÉRTÉK('clang_getCString',C_forrás.c_char_p,sztring_ÉRTÉK)
kiad_SMS = FÜGGVÉNY_ÉRTÉK('clang_disposeString',None,sztring_ÉRTÉK)
def Szöveg(ÉRTÉK):
    KR = (áthúz_SMS(ÉRTÉK) or b'').decode('utf-8'); kiad_SMS(ÉRTÉK); return KR
áthúz_név = FÜGGVÉNY_ÉRTÉK('clang_getCursorSpelling',sztring_ÉRTÉK,kurzor_ÉRTÉK)
áthúz_hivatkozik = FÜGGVÉNY_ÉRTÉK('clang_getCursorReferenced',kurzor_ÉRTÉK,kurzor_ÉRTÉK)
áthúz_pozíció = FÜGGVÉNY_ÉRTÉK('clang_getCursorLocation',Pozíció,kurzor_ÉRTÉK)
Fájl_pozíció = FÜGGVÉNY_ÉRTÉK('clang_getFileLocation',None,Pozíció,C_forrás.POINTER(C_forrás.c_void_p),C_forrás.POINTER(C_forrás.c_uint),C_forrás.POINTER(C_forrás.c_uint),C_forrás.POINTER(C_forrás.c_uint))
Fájl_bejegyzés_név = FÜGGVÉNY_ÉRTÉK('clang_getFileName',sztring_ÉRTÉK,C_forrás.c_void_p)
EGYEDI_név = FÜGGVÉNY_ÉRTÉK('clang_getCursorUSR',sztring_ÉRTÉK,kurzor_ÉRTÉK)
ismerős_Altípus = FÜGGVÉNY_ÉRTÉK('clang_getCursorLinkage',C_forrás.c_uint,kurzor_ÉRTÉK)
방문형 = C_forrás.CFUNCTYPE(C_forrás.c_uint,kurzor_ÉRTÉK,kurzor_ÉRTÉK,C_forrás.c_void_p)
방문 = FÜGGVÉNY_ÉRTÉK('clang_visitChildren',C_forrás.c_uint,kurzor_ÉRTÉK,방문형,C_forrás.c_void_p)
generálás = FÜGGVÉNY_ÉRTÉK('clang_createIndex',C_forrás.c_void_p,C_forrás.c_int,C_forrás.c_int)
Elemzés_ÉRTÉK = FÜGGVÉNY_ÉRTÉK('clang_parseTranslationUnit',C_forrás.c_void_p,C_forrás.c_void_p,C_forrás.c_char_p,C_forrás.POINTER(C_forrás.c_char_p),C_forrás.c_int,C_forrás.c_void_p,C_forrás.c_uint,C_forrás.c_uint)
gyök_ÉRTÉK = FÜGGVÉNY_ÉRTÉK('clang_getTranslationUnitCursor',kurzor_ÉRTÉK,C_forrás.c_void_p)
kilépés_app = FÜGGVÉNY_ÉRTÉK('clang_disposeTranslationUnit',None,C_forrás.c_void_p)
진단수 = FÜGGVÉNY_ÉRTÉK('clang_getNumDiagnostics',C_forrás.c_uint,C_forrás.c_void_p)
진단얻기 = FÜGGVÉNY_ÉRTÉK('clang_getDiagnostic',C_forrás.c_void_p,C_forrás.c_void_p,C_forrás.c_uint)
súlyosság_ÉRTÉK = FÜGGVÉNY_ÉRTÉK('clang_getDiagnosticSeverity',C_forrás.c_uint,C_forrás.c_void_p)
진단문 = FÜGGVÉNY_ÉRTÉK('clang_getDiagnosticSpelling',sztring_ÉRTÉK,C_forrás.c_void_p)
진단해제 = FÜGGVÉNY_ÉRTÉK('clang_disposeDiagnostic',None,C_forrás.c_void_p)

def helyzetindex(bejegyzés_ÉRTÉK):
    Fájl = C_forrás.c_void_p(); Vonal = C_forrás.c_uint(); tárolóhely_bejegyzés = C_forrás.c_uint(); Ofszet_ÉRTÉK = C_forrás.c_uint()
    Fájl_pozíció(áthúz_pozíció(bejegyzés_ÉRTÉK),C_forrás.byref(Fájl),C_forrás.byref(Vonal),C_forrás.byref(tárolóhely_bejegyzés),C_forrás.byref(Ofszet_ÉRTÉK))
    return (Szöveg(Fájl_bejegyzés_név(Fájl)) if Fájl else '', Ofszet_ÉRTÉK.value, Vonal.value)

def végrehajt_parancs():
    KERES_INDEX = generálás(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # fordítóprogram_eszköz.c는 saját bevallás 없이 TinyCC külső_ÉRTÉK 단일 FORDÍTÁS_forrás 단위만 포함한다.
    # külső_ÉRTÉK 선언을 saját 이름으로 세지 않으며, tényleges_adat 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ÚTVONAL.resolve()) for ÚTVONAL in teendő_gyök.rglob('*') if ÚTVONAL.suffix in ('.c','.h','.cpp','.inc')
              and not set(ÚTVONAL.relative_to(teendő_gyök).parts)&{'build','dist','vendor','__pycache__'}
              and ÚTVONAL.relative_to(teendő_gyök).as_posix() != 'C_fordítóprogram/fordítóprogram_eszköz.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(teendő_gyök/'felhasználó'),
          '-I'+str(teendő_gyök.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(teendő_gyök/'build'),'-I'+str(teendő_gyök/'build/user'),
          '-I'+str(teendő_gyök/'build/remote'),'-I'+str(teendő_gyök/'vendor/bearssl/inc'),
          '-I'+str(teendő_gyök/'vendor/bearssl/src'),'-I'+str(teendő_gyök/'vendor/libassh/src'),
          '-I'+str(teendő_gyök/'vendor/lwip/src/include'),'-I'+str(teendő_gyök/'hálózat_Sor'),
          '-I'+str(teendő_gyök/'távoli_ÉRTÉK'),'-I'+str(teendő_gyök/'C_fordítóprogram')]
    for ÚTVONAL in sorted(Path(Név) for Név in 소유파일 if Név.endswith(('.c','.cpp'))):
        Argumentumok = 공통 + ['-std=c++11' if ÚTVONAL.suffix=='.cpp' else '-std=c11']
        if 'hálózat_Sor' in ÚTVONAL.parts: Argumentumok += ['-I'+str(teendő_gyök/'hálózat_Sor'),'-I'+str(teendő_gyök/'vendor/lwip/src/include')]
        if 'C_fordítóprogram' in ÚTVONAL.parts:
            Argumentumok += ['-I'+str(teendő_gyök/'C_fordítóprogram'),'-I'+str(teendő_gyök/'vendor/tinycc'),'-I'+str(teendő_gyök/'build/ccompiler'),
                    '-isystem',str(teendő_gyök.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_híd' in ÚTVONAL.parts:
            Argumentumok += ['-I'+str(teendő_gyök/'PYTHON_híd'),'-I'+str(teendő_gyök/'build/micropython-1.24.1'),'-I'+str(teendő_gyök/'build/python'),'-isystem','/usr/include/newlib']
        if 'távoli_ÉRTÉK' in ÚTVONAL.parts:
            Argumentumok += ['-isystem', '/usr/include/newlib']
        if 'elosztás_ÉRTÉK' in ÚTVONAL.parts: Argumentumok += ['-D__JKOROS__=1']
        if ÚTVONAL.name=='köteg.c': Argumentumok += ['-I'+str(teendő_gyök/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Csoport_ÉRTÉK = (C_forrás.c_char_p*len(Argumentumok))(*[bejegyzés_ÉRTÉK.encode() for bejegyzés_ÉRTÉK in Argumentumok])
        Fordítás_lecke = Elemzés_ÉRTÉK(KERES_INDEX,str(ÚTVONAL).encode(),Csoport_ÉRTÉK,len(Argumentumok),None,0,1)
        for INDEX in range(진단수(Fordítás_lecke)):
            진단 = 진단얻기(Fordítás_lecke,INDEX)
            if súlyosság_ÉRTÉK(진단)>=3: 오류들.append((str(ÚTVONAL.relative_to(teendő_gyök)),Szöveg(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(bejegyzés_ÉRTÉK,szülő_ÉRTÉK,adat):
            Fájl,Ofszet_ÉRTÉK,Vonal = helyzetindex(bejegyzés_ÉRTÉK)
            if Fájl not in 소유파일: return 2 if bejegyzés_ÉRTÉK.Altípus_ÉRTÉK==300 else 1
            낱말 = Szöveg(áthúz_név(bejegyzés_ÉRTÉK))
            if not 낱말 or any(ord(karakter_ÉRTÉK)>127 for karakter_ÉRTÉK in 낱말): return 2
            if bejegyzés_ÉRTÉK.Altípus_ÉRTÉK in (2,3,4,5,6,7,8,9,10,20,21,501):
                EGYEDI_ÉRTÉK = Szöveg(EGYEDI_név(bejegyzés_ÉRTÉK)) or Fájl+':'+str(Ofszet_ÉRTÉK)
                선언들[EGYEDI_ÉRTÉK] = {'Fájl':Fájl,'Ofszet_ÉRTÉK':Ofszet_ÉRTÉK,'Vonal':Vonal,'Altípus_ÉRTÉK':bejegyzés_ÉRTÉK.Altípus_ÉRTÉK,'Név':낱말,'Kapcsolódás':ismerős_Altípus(bejegyzés_ÉRTÉK)}
                참조들.append((Fájl,Ofszet_ÉRTÉK,낱말,EGYEDI_ÉRTÉK))
            else:
                hivatkozik = áthúz_hivatkozik(bejegyzés_ÉRTÉK)
                hivatkozik_Fájl,_,_ = helyzetindex(hivatkozik)
                if hivatkozik_Fájl in 소유파일:
                    EGYEDI_ÉRTÉK = Szöveg(EGYEDI_név(hivatkozik)); 참조들.append((Fájl,Ofszet_ÉRTÉK,Szöveg(áthúz_név(hivatkozik)),EGYEDI_ÉRTÉK))
            return 2
        방문(gyök_ÉRTÉK(Fordítás_lecke),살피기,None)
        kilépés_app(Fordítás_lecke)
    cél_ÉRTÉK = teendő_gyök/'build/한국어화/시언어분석.json'
    cél_ÉRTÉK.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fájl:hashlib.sha256(Path(Fájl).read_bytes()).hexdigest() for Fájl in sorted(소유파일)}
    cél_ÉRTÉK.write_text(json.dumps({'bevallás':선언들,'hivatkozik':참조들,'HIBA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('bevallás',len(선언들),'hivatkozik',len(참조들),'HIBA',len(오류들))
    for HIBA in 오류들: print(*HIBA)

if __name__=='__main__': végrehajt_parancs()
