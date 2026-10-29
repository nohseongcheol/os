#!/usr/bin/env python3
"""libclang 선언·fiosrachadh 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

tilg_freumh = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class sreang_VALUE(씨.Structure): _fields_ = [('dàta',씨.c_void_p),('show_VALUE',씨.c_uint)]
class cursair_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('dàta',씨.c_void_p*3)]
class suidhich(씨.Structure): _fields_ = [('dàta',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def FUNCTION_VALUE(Ainm, return_tomhas, *인수):
    cur_a_steach_VALUE = getattr(구현, Ainm); cur_a_steach_VALUE.restype = return_tomhas; cur_a_steach_VALUE.argtypes = list(인수); return cur_a_steach_VALUE
글얻기 = FUNCTION_VALUE('clang_getCString',씨.c_char_p,sreang_VALUE)
sgaoileadh_SMS = FUNCTION_VALUE('clang_disposeString',None,sreang_VALUE)
def SMS(VALUE):
    tomhas = (글얻기(VALUE) or b'').decode('utf-8'); sgaoileadh_SMS(VALUE); return tomhas
이름얻기 = FUNCTION_VALUE('clang_getCursorSpelling',sreang_VALUE,cursair_VALUE)
참조얻기 = FUNCTION_VALUE('clang_getCursorReferenced',cursair_VALUE,cursair_VALUE)
위치얻기 = FUNCTION_VALUE('clang_getCursorLocation',suidhich,cursair_VALUE)
faidhle_suidhich = FUNCTION_VALUE('clang_getFileLocation',None,suidhich,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
faidhle_cur_a_steach_ainm = FUNCTION_VALUE('clang_getFileName',sreang_VALUE,씨.c_void_p)
UNIQUE_ainm = FUNCTION_VALUE('clang_getCursorUSR',sreang_VALUE,cursair_VALUE)
연결종류 = FUNCTION_VALUE('clang_getCursorLinkage',씨.c_uint,cursair_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,cursair_VALUE,cursair_VALUE,씨.c_void_p)
방문 = FUNCTION_VALUE('clang_visitChildren',씨.c_uint,cursair_VALUE,방문형,씨.c_void_p)
gin = FUNCTION_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
freumh_VALUE = FUNCTION_VALUE('clang_getTranslationUnitCursor',cursair_VALUE,씨.c_void_p)
fàg_an_seo_ap = FUNCTION_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
donad_VALUE = FUNCTION_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_VALUE('clang_getDiagnosticSpelling',sreang_VALUE,씨.c_void_p)
진단해제 = FUNCTION_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def suidhich_INDEX(cur_a_steach_VALUE):
    faidhle = 씨.c_void_p(); loidhne = 씨.c_uint(); slot_cur_a_steach = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    faidhle_suidhich(위치얻기(cur_a_steach_VALUE),씨.byref(faidhle),씨.byref(loidhne),씨.byref(slot_cur_a_steach),씨.byref(OFFSET_VALUE))
    return (SMS(faidhle_cur_a_steach_ainm(faidhle)) if faidhle else '', OFFSET_VALUE.value, loidhne.value)

def gnìomhaich_àithne():
    LOOKUP_INDEX = gin(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 TRANSLATE_tùs 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, dearbh_dàta 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Slighe.resolve()) for Slighe in tilg_freumh.rglob('*') if Slighe.suffix in ('.c','.h','.cpp','.inc')
              and not set(Slighe.relative_to(tilg_freumh).parts)&{'build','dist','vendor','__pycache__'}
              and Slighe.relative_to(tilg_freumh).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(tilg_freumh/'cleachdaiche'),
          '-I'+str(tilg_freumh.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(tilg_freumh/'build'),'-I'+str(tilg_freumh/'build/user'),
          '-I'+str(tilg_freumh/'build/remote'),'-I'+str(tilg_freumh/'vendor/bearssl/inc'),
          '-I'+str(tilg_freumh/'vendor/bearssl/src'),'-I'+str(tilg_freumh/'vendor/libassh/src'),
          '-I'+str(tilg_freumh/'vendor/lwip/src/include'),'-I'+str(tilg_freumh/'lìonra_stac'),
          '-I'+str(tilg_freumh/'cian_VALUE'),'-I'+str(tilg_freumh/'시언어번역기')]
    for Slighe in sorted(Path(Ainm) for Ainm in 소유파일 if Ainm.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Slighe.suffix=='.cpp' else '-std=c11']
        if 'lìonra_stac' in Slighe.parts: 인수 += ['-I'+str(tilg_freumh/'lìonra_stac'),'-I'+str(tilg_freumh/'vendor/lwip/src/include')]
        if '시언어번역기' in Slighe.parts:
            인수 += ['-I'+str(tilg_freumh/'시언어번역기'),'-I'+str(tilg_freumh/'vendor/tinycc'),'-I'+str(tilg_freumh/'build/ccompiler'),
                    '-isystem',str(tilg_freumh.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_drochaid' in Slighe.parts:
            인수 += ['-I'+str(tilg_freumh/'PYTHON_drochaid'),'-I'+str(tilg_freumh/'build/micropython-1.24.1'),'-I'+str(tilg_freumh/'build/python'),'-isystem','/usr/include/newlib']
        if 'cian_VALUE' in Slighe.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Slighe.parts: 인수 += ['-D__JKOROS__=1']
        if Slighe.name=='trusgan.c': 인수 += ['-I'+str(tilg_freumh/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        buidheann_VALUE = (씨.c_char_p*len(인수))(*[cur_a_steach_VALUE.encode() for cur_a_steach_VALUE in 인수])
        eadar_theangachadh_leasan = 분석(LOOKUP_INDEX,str(Slighe).encode(),buidheann_VALUE,len(인수),None,0,1)
        for INDEX in range(진단수(eadar_theangachadh_leasan)):
            진단 = 진단얻기(eadar_theangachadh_leasan,INDEX)
            if donad_VALUE(진단)>=3: 오류들.append((str(Slighe.relative_to(tilg_freumh)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(cur_a_steach_VALUE,부모,dàta):
            faidhle,OFFSET_VALUE,loidhne = suidhich_INDEX(cur_a_steach_VALUE)
            if faidhle not in 소유파일: return 2 if cur_a_steach_VALUE.종류==300 else 1
            낱말 = SMS(이름얻기(cur_a_steach_VALUE))
            if not 낱말 or any(ord(caractar_VALUE)>127 for caractar_VALUE in 낱말): return 2
            if cur_a_steach_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = SMS(UNIQUE_ainm(cur_a_steach_VALUE)) or faidhle+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'faidhle':faidhle,'OFFSET_VALUE':OFFSET_VALUE,'줄':loidhne,'종류':cur_a_steach_VALUE.종류,'Ainm':낱말,'CONNECT':연결종류(cur_a_steach_VALUE)}
                참조들.append((faidhle,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                fiosrachadh = 참조얻기(cur_a_steach_VALUE)
                fiosrachadh_faidhle,_,_ = suidhich_INDEX(fiosrachadh)
                if fiosrachadh_faidhle in 소유파일:
                    UNIQUE_VALUE = SMS(UNIQUE_ainm(fiosrachadh)); 참조들.append((faidhle,OFFSET_VALUE,SMS(이름얻기(fiosrachadh)),UNIQUE_VALUE))
            return 2
        방문(freumh_VALUE(eadar_theangachadh_leasan),살피기,None)
        fàg_an_seo_ap(eadar_theangachadh_leasan)
    ceann_uidhe_VALUE = tilg_freumh/'build/한국어화/시언어분석.json'
    ceann_uidhe_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {faidhle:hashlib.sha256(Path(faidhle).read_bytes()).hexdigest() for faidhle in sorted(소유파일)}
    ceann_uidhe_VALUE.write_text(json.dumps({'선언':선언들,'fiosrachadh':참조들,'Mearachd':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'fiosrachadh',len(참조들),'Mearachd',len(오류들))
    for Mearachd in 오류들: print(*Mearachd)

if __name__=='__main__': gnìomhaich_àithne()
