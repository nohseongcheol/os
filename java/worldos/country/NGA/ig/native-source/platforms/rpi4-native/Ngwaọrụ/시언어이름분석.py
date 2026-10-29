#!/usr/bin/env python3
"""libclang 선언·Nrụtụ_aka 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ùsòròokwū_valuu(씨.Structure): _fields_ = [('datà',씨.c_void_p),('gòsi_valuu',씨.c_uint)]
class akàran̄ziebe_valuu(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('datà',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('datà',씨.c_void_p*2),('Nnokwata_valuu',씨.c_uint)]
def ọrụ_valuu(Aha, 반환, *인수):
    ndebà_valuu = getattr(구현, Aha); ndebà_valuu.restype = 반환; ndebà_valuu.argtypes = list(인수); return ndebà_valuu
글얻기 = ọrụ_valuu('clang_getCString',씨.c_char_p,ùsòròokwū_valuu)
bupute_SMS = ọrụ_valuu('clang_disposeString',None,ùsòròokwū_valuu)
def SMS(valuu):
    결과 = (글얻기(valuu) or b'').decode('utf-8'); bupute_SMS(valuu); return 결과
이름얻기 = ọrụ_valuu('clang_getCursorSpelling',ùsòròokwū_valuu,akàran̄ziebe_valuu)
참조얻기 = ọrụ_valuu('clang_getCursorReferenced',akàran̄ziebe_valuu,akàran̄ziebe_valuu)
위치얻기 = ọrụ_valuu('clang_getCursorLocation',위치,akàran̄ziebe_valuu)
파일위치 = ọrụ_valuu('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ọbọakwụkwọ_ndebà_akara_ahà = ọrụ_valuu('clang_getFileName',ùsòròokwū_valuu,씨.c_void_p)
PỤRỤICHE_akara_ahà = ọrụ_valuu('clang_getCursorUSR',ùsòròokwū_valuu,akàran̄ziebe_valuu)
연결종류 = ọrụ_valuu('clang_getCursorLinkage',씨.c_uint,akàran̄ziebe_valuu)
방문형 = 씨.CFUNCTYPE(씨.c_uint,akàran̄ziebe_valuu,akàran̄ziebe_valuu,씨.c_void_p)
방문 = ọrụ_valuu('clang_visitChildren',씨.c_uint,akàran̄ziebe_valuu,방문형,씨.c_void_p)
생성 = ọrụ_valuu('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ọrụ_valuu('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = ọrụ_valuu('clang_getTranslationUnitCursor',akàran̄ziebe_valuu,씨.c_void_p)
끝내기 = ọrụ_valuu('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ọrụ_valuu('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ọrụ_valuu('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ọ́nọ̀dụ̀_valuu = ọrụ_valuu('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ọrụ_valuu('clang_getDiagnosticSpelling',ùsòròokwū_valuu,씨.c_void_p)
진단해제 = ọrụ_valuu('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(ndebà_valuu):
    Faịlụ = 씨.c_void_p(); ahịrī = 씨.c_uint(); oghere_ndebà = 씨.c_uint(); Nnokwata_valuu = 씨.c_uint()
    파일위치(위치얻기(ndebà_valuu),씨.byref(Faịlụ),씨.byref(ahịrī),씨.byref(oghere_ndebà),씨.byref(Nnokwata_valuu))
    return (SMS(ọbọakwụkwọ_ndebà_akara_ahà(Faịlụ)) if Faịlụ else '', Nnokwata_valuu.value, ahịrī.value)

def mee_nnyemiwu():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Tụgharia_ebensìbịa 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ǹdịnezie_datà 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ụzọ_ozi.resolve()) for ụzọ_ozi in 기준.rglob('*') if ụzọ_ozi.suffix in ('.c','.h','.cpp','.inc')
              and not set(ụzọ_ozi.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and ụzọ_ozi.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'òjìàrụ'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Netwọọkụ_ikpo'),
          '-I'+str(기준/'ebe_dị̀anyā_valuu'),'-I'+str(기준/'시언어번역기')]
    for ụzọ_ozi in sorted(Path(Aha) for Aha in 소유파일 if Aha.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ụzọ_ozi.suffix=='.cpp' else '-std=c11']
        if 'Netwọọkụ_ikpo' in ụzọ_ozi.parts: 인수 += ['-I'+str(기준/'Netwọọkụ_ikpo'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in ụzọ_ozi.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ụzọ_ozi.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'ebe_dị̀anyā_valuu' in ụzọ_ozi.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ụzọ_ozi.parts: 인수 += ['-D__JKOROS__=1']
        if ụzọ_ozi.name=='ngwungwu.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        otu_valuu = (씨.c_char_p*len(인수))(*[ndebà_valuu.encode() for ndebà_valuu in 인수])
        Ntụgharị_ihe_ọmụmụ = 분석(색인,str(ụzọ_ozi).encode(),otu_valuu,len(인수),None,0,1)
        for indèks in range(진단수(Ntụgharị_ihe_ọmụmụ)):
            진단 = 진단얻기(Ntụgharị_ihe_ọmụmụ,indèks)
            if ọ́nọ̀dụ̀_valuu(진단)>=3: 오류들.append((str(ụzọ_ozi.relative_to(기준)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ndebà_valuu,부모,datà):
            Faịlụ,Nnokwata_valuu,ahịrī = 자리(ndebà_valuu)
            if Faịlụ not in 소유파일: return 2 if ndebà_valuu.종류==300 else 1
            낱말 = SMS(이름얻기(ndebà_valuu))
            if not 낱말 or any(ord(mkpụrụedemede_valuu)>127 for mkpụrụedemede_valuu in 낱말): return 2
            if ndebà_valuu.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                PỤRỤICHE_valuu = SMS(PỤRỤICHE_akara_ahà(ndebà_valuu)) or Faịlụ+':'+str(Nnokwata_valuu)
                선언들[PỤRỤICHE_valuu] = {'Faịlụ':Faịlụ,'Nnokwata_valuu':Nnokwata_valuu,'줄':ahịrī,'종류':ndebà_valuu.종류,'Aha':낱말,'Banye':연결종류(ndebà_valuu)}
                참조들.append((Faịlụ,Nnokwata_valuu,낱말,PỤRỤICHE_valuu))
            else:
                Nrụtụ_aka = 참조얻기(ndebà_valuu)
                Nrụtụ_aka_ọbọakwụkwọ,_,_ = 자리(Nrụtụ_aka)
                if Nrụtụ_aka_ọbọakwụkwọ in 소유파일:
                    PỤRỤICHE_valuu = SMS(PỤRỤICHE_akara_ahà(Nrụtụ_aka)); 참조들.append((Faịlụ,Nnokwata_valuu,SMS(이름얻기(Nrụtụ_aka)),PỤRỤICHE_valuu))
            return 2
        방문(뿌리(Ntụgharị_ihe_ọmụmụ),살피기,None)
        끝내기(Ntụgharị_ihe_ọmụmụ)
    ebemwèga_valuu = 기준/'build/한국어화/시언어분석.json'
    ebemwèga_valuu.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Faịlụ:hashlib.sha256(Path(Faịlụ).read_bytes()).hexdigest() for Faịlụ in sorted(소유파일)}
    ebemwèga_valuu.write_text(json.dumps({'선언':선언들,'Nrụtụ_aka':참조들,'mmejọ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Nrụtụ_aka',len(참조들),'mmejọ',len(오류들))
    for mmejọ in 오류들: print(*mmejọ)

if __name__=='__main__': mee_nnyemiwu()
