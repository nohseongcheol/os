#!/usr/bin/env python3
"""libclang 선언·Tshupiso 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class dikwalwa_Boleng(씨.Structure): _fields_ = [('tshedimosetso',씨.c_void_p),('bontsha_Boleng',씨.c_uint)]
class khesara_Boleng(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('tshedimosetso',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('tshedimosetso',씨.c_void_p*2),('Baya_ka_Tekatekanyo_Boleng',씨.c_uint)]
def TIRISO_Boleng(leina, 반환, *인수):
    tsenyo_Boleng = getattr(구현, leina); tsenyo_Boleng.restype = 반환; tsenyo_Boleng.argtypes = list(인수); return tsenyo_Boleng
글얻기 = TIRISO_Boleng('clang_getCString',씨.c_char_p,dikwalwa_Boleng)
ntsha_SMS = TIRISO_Boleng('clang_disposeString',None,dikwalwa_Boleng)
def SMS(Boleng):
    결과 = (글얻기(Boleng) or b'').decode('utf-8'); ntsha_SMS(Boleng); return 결과
이름얻기 = TIRISO_Boleng('clang_getCursorSpelling',dikwalwa_Boleng,khesara_Boleng)
참조얻기 = TIRISO_Boleng('clang_getCursorReferenced',khesara_Boleng,khesara_Boleng)
위치얻기 = TIRISO_Boleng('clang_getCursorLocation',위치,khesara_Boleng)
파일위치 = TIRISO_Boleng('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
faele_tsenyo_leina = TIRISO_Boleng('clang_getFileName',dikwalwa_Boleng,씨.c_void_p)
TLHOMOLOGA_leina = TIRISO_Boleng('clang_getCursorUSR',dikwalwa_Boleng,khesara_Boleng)
연결종류 = TIRISO_Boleng('clang_getCursorLinkage',씨.c_uint,khesara_Boleng)
방문형 = 씨.CFUNCTYPE(씨.c_uint,khesara_Boleng,khesara_Boleng,씨.c_void_p)
방문 = TIRISO_Boleng('clang_visitChildren',씨.c_uint,khesara_Boleng,방문형,씨.c_void_p)
생성 = TIRISO_Boleng('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = TIRISO_Boleng('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = TIRISO_Boleng('clang_getTranslationUnitCursor',khesara_Boleng,씨.c_void_p)
끝내기 = TIRISO_Boleng('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = TIRISO_Boleng('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = TIRISO_Boleng('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
kgakalo_Boleng = TIRISO_Boleng('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = TIRISO_Boleng('clang_getDiagnosticSpelling',dikwalwa_Boleng,씨.c_void_p)
진단해제 = TIRISO_Boleng('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(tsenyo_Boleng):
    faele = 씨.c_void_p(); Mola = 씨.c_uint(); sebaka_tsenyo = 씨.c_uint(); Baya_ka_Tekatekanyo_Boleng = 씨.c_uint()
    파일위치(위치얻기(tsenyo_Boleng),씨.byref(faele),씨.byref(Mola),씨.byref(sebaka_tsenyo),씨.byref(Baya_ka_Tekatekanyo_Boleng))
    return (SMS(faele_tsenyo_leina(faele)) if faele else '', Baya_ka_Tekatekanyo_Boleng.value, Mola.value)

def diragatsa_Taelo():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Ranola_Motswedi 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, tota_tshedimosetso 빌드에서는 계속 컴파일한다.
    소유파일 = {str(tsela.resolve()) for tsela in 기준.rglob('*') if tsela.suffix in ('.c','.h','.cpp','.inc')
              and not set(tsela.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and tsela.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'modirisi'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Neteweke_kokoanyodinepe'),
          '-I'+str(기준/'kgakala_Boleng'),'-I'+str(기준/'시언어번역기')]
    for tsela in sorted(Path(leina) for leina in 소유파일 if leina.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if tsela.suffix=='.cpp' else '-std=c11']
        if 'Neteweke_kokoanyodinepe' in tsela.parts: 인수 += ['-I'+str(기준/'Neteweke_kokoanyodinepe'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in tsela.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in tsela.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'kgakala_Boleng' in tsela.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in tsela.parts: 인수 += ['-D__JKOROS__=1']
        if tsela.name=='ngatanngwe.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        setlhopha_Boleng = (씨.c_char_p*len(인수))(*[tsenyo_Boleng.encode() for tsenyo_Boleng in 인수])
        Thanolo_thuto = 분석(색인,str(tsela).encode(),setlhopha_Boleng,len(인수),None,0,1)
        for tshupane in range(진단수(Thanolo_thuto)):
            진단 = 진단얻기(Thanolo_thuto,tshupane)
            if kgakalo_Boleng(진단)>=3: 오류들.append((str(tsela.relative_to(기준)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(tsenyo_Boleng,부모,tshedimosetso):
            faele,Baya_ka_Tekatekanyo_Boleng,Mola = 자리(tsenyo_Boleng)
            if faele not in 소유파일: return 2 if tsenyo_Boleng.종류==300 else 1
            낱말 = SMS(이름얻기(tsenyo_Boleng))
            if not 낱말 or any(ord(Letshwao_Boleng)>127 for Letshwao_Boleng in 낱말): return 2
            if tsenyo_Boleng.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                TLHOMOLOGA_Boleng = SMS(TLHOMOLOGA_leina(tsenyo_Boleng)) or faele+':'+str(Baya_ka_Tekatekanyo_Boleng)
                선언들[TLHOMOLOGA_Boleng] = {'faele':faele,'Baya_ka_Tekatekanyo_Boleng':Baya_ka_Tekatekanyo_Boleng,'줄':Mola,'종류':tsenyo_Boleng.종류,'leina':낱말,'Golaganya':연결종류(tsenyo_Boleng)}
                참조들.append((faele,Baya_ka_Tekatekanyo_Boleng,낱말,TLHOMOLOGA_Boleng))
            else:
                Tshupiso = 참조얻기(tsenyo_Boleng)
                Tshupiso_faele,_,_ = 자리(Tshupiso)
                if Tshupiso_faele in 소유파일:
                    TLHOMOLOGA_Boleng = SMS(TLHOMOLOGA_leina(Tshupiso)); 참조들.append((faele,Baya_ka_Tekatekanyo_Boleng,SMS(이름얻기(Tshupiso)),TLHOMOLOGA_Boleng))
            return 2
        방문(뿌리(Thanolo_thuto),살피기,None)
        끝내기(Thanolo_thuto)
    bogorogelo_Boleng = 기준/'build/한국어화/시언어분석.json'
    bogorogelo_Boleng.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {faele:hashlib.sha256(Path(faele).read_bytes()).hexdigest() for faele in sorted(소유파일)}
    bogorogelo_Boleng.write_text(json.dumps({'선언':선언들,'Tshupiso':참조들,'phoso':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Tshupiso',len(참조들),'phoso',len(오류들))
    for phoso in 오류들: print(*phoso)

if __name__=='__main__': diragatsa_Taelo()
