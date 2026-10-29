#!/usr/bin/env python3
"""libclang tamko·Marejeleo 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class tungo_thamani(씨.Structure): _fields_ = [('data',씨.c_void_p),('onyesha_thamani',씨.c_uint)]
class kielekezi_thamani(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('Chipua_thamani',씨.c_uint)]
def KITENDAKAZI_thamani(Jina, 반환, *인수):
    ingizo_thamani = getattr(구현, Jina); ingizo_thamani.restype = 반환; ingizo_thamani.argtypes = list(인수); return ingizo_thamani
pata_SMS = KITENDAKAZI_thamani('clang_getCString',씨.c_char_p,tungo_thamani)
toleo_SMS = KITENDAKAZI_thamani('clang_disposeString',None,tungo_thamani)
def SMS(thamani):
    결과 = (pata_SMS(thamani) or b'').decode('utf-8'); toleo_SMS(thamani); return 결과
pata_jina = KITENDAKAZI_thamani('clang_getCursorSpelling',tungo_thamani,kielekezi_thamani)
pata_Marejeleo = KITENDAKAZI_thamani('clang_getCursorReferenced',kielekezi_thamani,kielekezi_thamani)
위치얻기 = KITENDAKAZI_thamani('clang_getCursorLocation',위치,kielekezi_thamani)
파일위치 = KITENDAKAZI_thamani('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
faili_ingizo_jina = KITENDAKAZI_thamani('clang_getFileName',tungo_thamani,씨.c_void_p)
KIPEKEE_jina = KITENDAKAZI_thamani('clang_getCursorUSR',tungo_thamani,kielekezi_thamani)
연결종류 = KITENDAKAZI_thamani('clang_getCursorLinkage',씨.c_uint,kielekezi_thamani)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kielekezi_thamani,kielekezi_thamani,씨.c_void_p)
방문 = KITENDAKAZI_thamani('clang_visitChildren',씨.c_uint,kielekezi_thamani,방문형,씨.c_void_p)
생성 = KITENDAKAZI_thamani('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = KITENDAKAZI_thamani('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = KITENDAKAZI_thamani('clang_getTranslationUnitCursor',kielekezi_thamani,씨.c_void_p)
끝내기 = KITENDAKAZI_thamani('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = KITENDAKAZI_thamani('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = KITENDAKAZI_thamani('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ukali_thamani = KITENDAKAZI_thamani('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = KITENDAKAZI_thamani('clang_getDiagnosticSpelling',tungo_thamani,씨.c_void_p)
진단해제 = KITENDAKAZI_thamani('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(ingizo_thamani):
    faili = 씨.c_void_p(); laini = 씨.c_uint(); Sloti_ingizo = 씨.c_uint(); Chipua_thamani = 씨.c_uint()
    파일위치(위치얻기(ingizo_thamani),씨.byref(faili),씨.byref(laini),씨.byref(Sloti_ingizo),씨.byref(Chipua_thamani))
    return (SMS(faili_ingizo_jina(faili)) if faili else '', Chipua_thamani.value, laini.value)

def tekeleza_amri():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 tamko 없이 TinyCC 외부 단일 Tafsiri_chanzo 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, halisi_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(njia.resolve()) for njia in 기준.rglob('*') if njia.suffix in ('.c','.h','.cpp','.inc')
              and not set(njia.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and njia.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'mtumiaji'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Mtandao_Mpororo'),
          '-I'+str(기준/'kwa_mbali_thamani'),'-I'+str(기준/'시언어번역기')]
    for njia in sorted(Path(Jina) for Jina in 소유파일 if Jina.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if njia.suffix=='.cpp' else '-std=c11']
        if 'Mtandao_Mpororo' in njia.parts: 인수 += ['-I'+str(기준/'Mtandao_Mpororo'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in njia.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in njia.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'kwa_mbali_thamani' in njia.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in njia.parts: 인수 += ['-D__JKOROS__=1']
        if njia.name=='fungasha.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Kikundi_thamani = (씨.c_char_p*len(인수))(*[ingizo_thamani.encode() for ingizo_thamani in 인수])
        Tafsiri_funzo = 분석(색인,str(njia).encode(),Kikundi_thamani,len(인수),None,0,1)
        for kielezo in range(진단수(Tafsiri_funzo)):
            진단 = 진단얻기(Tafsiri_funzo,kielezo)
            if ukali_thamani(진단)>=3: 오류들.append((str(njia.relative_to(기준)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ingizo_thamani,부모,data):
            faili,Chipua_thamani,laini = 자리(ingizo_thamani)
            if faili not in 소유파일: return 2 if ingizo_thamani.종류==300 else 1
            낱말 = SMS(pata_jina(ingizo_thamani))
            if not 낱말 or any(ord(kibambo_thamani)>127 for kibambo_thamani in 낱말): return 2
            if ingizo_thamani.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                KIPEKEE_thamani = SMS(KIPEKEE_jina(ingizo_thamani)) or faili+':'+str(Chipua_thamani)
                선언들[KIPEKEE_thamani] = {'faili':faili,'Chipua_thamani':Chipua_thamani,'줄':laini,'종류':ingizo_thamani.종류,'Jina':낱말,'UNGANISHA':연결종류(ingizo_thamani)}
                참조들.append((faili,Chipua_thamani,낱말,KIPEKEE_thamani))
            else:
                Marejeleo = pata_Marejeleo(ingizo_thamani)
                Marejeleo_faili,_,_ = 자리(Marejeleo)
                if Marejeleo_faili in 소유파일:
                    KIPEKEE_thamani = SMS(KIPEKEE_jina(Marejeleo)); 참조들.append((faili,Chipua_thamani,SMS(pata_jina(Marejeleo)),KIPEKEE_thamani))
            return 2
        방문(뿌리(Tafsiri_funzo),살피기,None)
        끝내기(Tafsiri_funzo)
    fikio_thamani = 기준/'build/한국어화/시언어분석.json'
    fikio_thamani.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {faili:hashlib.sha256(Path(faili).read_bytes()).hexdigest() for faili in sorted(소유파일)}
    fikio_thamani.write_text(json.dumps({'tamko':선언들,'Marejeleo':참조들,'kosa':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('tamko',len(선언들),'Marejeleo',len(참조들),'kosa',len(오류들))
    for kosa in 오류들: print(*kosa)

if __name__=='__main__': tekeleza_amri()
