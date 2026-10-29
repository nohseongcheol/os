#!/usr/bin/env python3
"""libclang deklaration·referens 위치를 수집한다. extern_värde 헤더의 멤버는 변환하지 않는다."""
import ctypes as C_källa
import hashlib
import json
from pathlib import Path

åtgärd_rot = Path(__file__).resolve().parents[1]
implementation = C_källa.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class sträng_värde(C_källa.Structure): _fields_ = [('data',C_källa.c_void_p),('visa_värde',C_källa.c_uint)]
class markör_värde_04ee3e20(C_källa.Structure): _fields_ = [('variant_värde',C_källa.c_uint),('보조',C_källa.c_int),('data',C_källa.c_void_p*3)]
class position(C_källa.Structure): _fields_ = [('data',C_källa.c_void_p*2),('FÖRSKJUTNING_värde',C_källa.c_uint)]
def FUNKTION_värde(Namn, Retur_KR, *argument):
    post_värde = getattr(implementation, Namn); post_värde.restype = Retur_KR; post_värde.argtypes = list(argument); return post_värde
hämta_SMS = FUNKTION_värde('clang_getCString',C_källa.c_char_p,sträng_värde)
släppa_SMS = FUNKTION_värde('clang_disposeString',None,sträng_värde)
def text(värde):
    RESULTAT = (hämta_SMS(värde) or b'').decode('utf-8'); släppa_SMS(värde); return RESULTAT
hämta_namn = FUNKTION_värde('clang_getCursorSpelling',sträng_värde,markör_värde_04ee3e20)
hämta_referens = FUNKTION_värde('clang_getCursorReferenced',markör_värde_04ee3e20,markör_värde_04ee3e20)
hämta_placera = FUNKTION_värde('clang_getCursorLocation',position,markör_värde_04ee3e20)
fil_placera = FUNKTION_värde('clang_getFileLocation',None,position,C_källa.POINTER(C_källa.c_void_p),C_källa.POINTER(C_källa.c_uint),C_källa.POINTER(C_källa.c_uint),C_källa.POINTER(C_källa.c_uint))
fil_post_namn = FUNKTION_värde('clang_getFileName',sträng_värde,C_källa.c_void_p)
UNIK_namn = FUNKTION_värde('clang_getCursorUSR',sträng_värde,markör_värde_04ee3e20)
kontakt_variant = FUNKTION_värde('clang_getCursorLinkage',C_källa.c_uint,markör_värde_04ee3e20)
방문형 = C_källa.CFUNCTYPE(C_källa.c_uint,markör_värde_04ee3e20,markör_värde_04ee3e20,C_källa.c_void_p)
방문 = FUNKTION_värde('clang_visitChildren',C_källa.c_uint,markör_värde_04ee3e20,방문형,C_källa.c_void_p)
generera = FUNKTION_värde('clang_createIndex',C_källa.c_void_p,C_källa.c_int,C_källa.c_int)
Analysera_värde = FUNKTION_värde('clang_parseTranslationUnit',C_källa.c_void_p,C_källa.c_void_p,C_källa.c_char_p,C_källa.POINTER(C_källa.c_char_p),C_källa.c_int,C_källa.c_void_p,C_källa.c_uint,C_källa.c_uint)
rot_värde = FUNKTION_värde('clang_getTranslationUnitCursor',markör_värde_04ee3e20,C_källa.c_void_p)
avsluta_app = FUNKTION_värde('clang_disposeTranslationUnit',None,C_källa.c_void_p)
진단수 = FUNKTION_värde('clang_getNumDiagnostics',C_källa.c_uint,C_källa.c_void_p)
진단얻기 = FUNKTION_värde('clang_getDiagnostic',C_källa.c_void_p,C_källa.c_void_p,C_källa.c_uint)
allvarlighetsgrad_värde = FUNKTION_värde('clang_getDiagnosticSeverity',C_källa.c_uint,C_källa.c_void_p)
진단문 = FUNKTION_värde('clang_getDiagnosticSpelling',sträng_värde,C_källa.c_void_p)
진단해제 = FUNKTION_värde('clang_disposeDiagnostic',None,C_källa.c_void_p)

def positionsindex(post_värde):
    filnamn = C_källa.c_void_p(); inmatningsrad = C_källa.c_uint(); fack_post = C_källa.c_uint(); FÖRSKJUTNING_värde = C_källa.c_uint()
    fil_placera(hämta_placera(post_värde),C_källa.byref(filnamn),C_källa.byref(inmatningsrad),C_källa.byref(fack_post),C_källa.byref(FÖRSKJUTNING_värde))
    return (text(fil_post_namn(filnamn)) if filnamn else '', FÖRSKJUTNING_värde.value, inmatningsrad.value)

def köra_kommando():
    LETAUPP_INDEX = generera(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # kompilerare_verktyg.c는 eget deklaration 없이 TinyCC extern_värde 단일 ÖVERSÄTT_källa 단위만 포함한다.
    # extern_värde 선언을 eget 이름으로 세지 않으며, verklig_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(sökväg_2.resolve()) for sökväg_2 in åtgärd_rot.rglob('*') if sökväg_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(sökväg_2.relative_to(åtgärd_rot).parts)&{'build','dist','vendor','__pycache__'}
              and sökväg_2.relative_to(åtgärd_rot).as_posix() != 'C_kompilerare/kompilerare_verktyg.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(åtgärd_rot/'användarutrymme'),
          '-I'+str(åtgärd_rot.parents[1]/'posix-kor/arm64-native/deklarationer'),'-I'+str(åtgärd_rot/'build'),'-I'+str(åtgärd_rot/'build/user'),
          '-I'+str(åtgärd_rot/'build/remote'),'-I'+str(åtgärd_rot/'vendor/bearssl/inc'),
          '-I'+str(åtgärd_rot/'vendor/bearssl/src'),'-I'+str(åtgärd_rot/'vendor/libassh/src'),
          '-I'+str(åtgärd_rot/'vendor/lwip/src/include'),'-I'+str(åtgärd_rot/'nätverk_Stack'),
          '-I'+str(åtgärd_rot/'fjärr_värde'),'-I'+str(åtgärd_rot/'C_kompilerare')]
    for sökväg_2 in sorted(Path(Namn) for Namn in 소유파일 if Namn.endswith(('.c','.cpp'))):
        argument = 공통 + ['-std=c++11' if sökväg_2.suffix=='.cpp' else '-std=c11']
        if 'nätverk_Stack' in sökväg_2.parts: argument += ['-I'+str(åtgärd_rot/'nätverk_Stack'),'-I'+str(åtgärd_rot/'vendor/lwip/src/include')]
        if 'C_kompilerare' in sökväg_2.parts:
            argument += ['-I'+str(åtgärd_rot/'C_kompilerare'),'-I'+str(åtgärd_rot/'vendor/tinycc'),'-I'+str(åtgärd_rot/'build/ccompiler'),
                    '-isystem',str(åtgärd_rot.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_brygga' in sökväg_2.parts:
            argument += ['-I'+str(åtgärd_rot/'PYTHON_brygga'),'-I'+str(åtgärd_rot/'build/micropython-1.24.1'),'-I'+str(åtgärd_rot/'build/python'),'-isystem','/usr/include/newlib']
        if 'fjärr_värde' in sökväg_2.parts:
            argument += ['-isystem', '/usr/include/newlib']
        if 'fördelning_värde' in sökväg_2.parts: argument += ['-D__JKOROS__=1']
        if sökväg_2.name=='bunt.c': argument += ['-I'+str(åtgärd_rot/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        grupp_värde = (C_källa.c_char_p*len(argument))(*[post_värde.encode() for post_värde in argument])
        Översättning_enhet = Analysera_värde(LETAUPP_INDEX,str(sökväg_2).encode(),grupp_värde,len(argument),None,0,1)
        for INDEX in range(진단수(Översättning_enhet)):
            진단 = 진단얻기(Översättning_enhet,INDEX)
            if allvarlighetsgrad_värde(진단)>=3: 오류들.append((str(sökväg_2.relative_to(åtgärd_rot)),text(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(post_värde,överordnad_värde,data):
            filnamn,FÖRSKJUTNING_värde,inmatningsrad = positionsindex(post_värde)
            if filnamn not in 소유파일: return 2 if post_värde.variant_värde==300 else 1
            낱말 = text(hämta_namn(post_värde))
            if not 낱말 or any(ord(tecken_värde)>127 for tecken_värde in 낱말): return 2
            if post_värde.variant_värde in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIK_värde = text(UNIK_namn(post_värde)) or filnamn+':'+str(FÖRSKJUTNING_värde)
                선언들[UNIK_värde] = {'filnamn':filnamn,'FÖRSKJUTNING_värde':FÖRSKJUTNING_värde,'inmatningsrad':inmatningsrad,'variant_värde':post_värde.variant_värde,'Namn':낱말,'Anslut':kontakt_variant(post_värde)}
                참조들.append((filnamn,FÖRSKJUTNING_värde,낱말,UNIK_värde))
            else:
                referens = hämta_referens(post_värde)
                referens_fil,_,_ = positionsindex(referens)
                if referens_fil in 소유파일:
                    UNIK_värde = text(UNIK_namn(referens)); 참조들.append((filnamn,FÖRSKJUTNING_värde,text(hämta_namn(referens)),UNIK_värde))
            return 2
        방문(rot_värde(Översättning_enhet),살피기,None)
        avsluta_app(Översättning_enhet)
    mål_värde = åtgärd_rot/'build/한국어화/시언어분석.json'
    mål_värde.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {filnamn:hashlib.sha256(Path(filnamn).read_bytes()).hexdigest() for filnamn in sorted(소유파일)}
    mål_värde.write_text(json.dumps({'deklaration':선언들,'referens':참조들,'fel':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('deklaration',len(선언들),'referens',len(참조들),'fel',len(오류들))
    for fel in 오류들: print(*fel)

if __name__=='__main__': köra_kommando()
