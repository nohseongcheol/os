#!/usr/bin/env python3
"""libclang 선언·Indanga 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class igicenteruro_agaciro(씨.Structure): _fields_ = [('amakurushingiro',씨.c_void_p),('kugaragaza_agaciro',씨.c_uint)]
class inyoboranyandika_agaciro(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('amakurushingiro',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('amakurushingiro',씨.c_void_p*2),('Ofuseti_agaciro',씨.c_uint)]
def FUNCTION_agaciro(Izina, 반환, *인수):
    icyinjizwa_agaciro = getattr(구현, Izina); icyinjizwa_agaciro.restype = 반환; icyinjizwa_agaciro.argtypes = list(인수); return icyinjizwa_agaciro
글얻기 = FUNCTION_agaciro('clang_getCString',씨.c_char_p,igicenteruro_agaciro)
kurekura_SMS = FUNCTION_agaciro('clang_disposeString',None,igicenteruro_agaciro)
def Umwandiko(agaciro):
    결과 = (글얻기(agaciro) or b'').decode('utf-8'); kurekura_SMS(agaciro); return 결과
이름얻기 = FUNCTION_agaciro('clang_getCursorSpelling',igicenteruro_agaciro,inyoboranyandika_agaciro)
참조얻기 = FUNCTION_agaciro('clang_getCursorReferenced',inyoboranyandika_agaciro,inyoboranyandika_agaciro)
위치얻기 = FUNCTION_agaciro('clang_getCursorLocation',위치,inyoboranyandika_agaciro)
파일위치 = FUNCTION_agaciro('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
dosiye_icyinjizwa_izina = FUNCTION_agaciro('clang_getFileName',igicenteruro_agaciro,씨.c_void_p)
RUKUMBI_izina = FUNCTION_agaciro('clang_getCursorUSR',igicenteruro_agaciro,inyoboranyandika_agaciro)
연결종류 = FUNCTION_agaciro('clang_getCursorLinkage',씨.c_uint,inyoboranyandika_agaciro)
방문형 = 씨.CFUNCTYPE(씨.c_uint,inyoboranyandika_agaciro,inyoboranyandika_agaciro,씨.c_void_p)
방문 = FUNCTION_agaciro('clang_visitChildren',씨.c_uint,inyoboranyandika_agaciro,방문형,씨.c_void_p)
생성 = FUNCTION_agaciro('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = FUNCTION_agaciro('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = FUNCTION_agaciro('clang_getTranslationUnitCursor',inyoboranyandika_agaciro,씨.c_void_p)
끝내기 = FUNCTION_agaciro('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = FUNCTION_agaciro('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = FUNCTION_agaciro('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ubukare_agaciro = FUNCTION_agaciro('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = FUNCTION_agaciro('clang_getDiagnosticSpelling',igicenteruro_agaciro,씨.c_void_p)
진단해제 = FUNCTION_agaciro('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(icyinjizwa_agaciro):
    Idosiye = 씨.c_void_p(); umurongo = 씨.c_uint(); umwanya_icyinjizwa = 씨.c_uint(); Ofuseti_agaciro = 씨.c_uint()
    파일위치(위치얻기(icyinjizwa_agaciro),씨.byref(Idosiye),씨.byref(umurongo),씨.byref(umwanya_icyinjizwa),씨.byref(Ofuseti_agaciro))
    return (Umwandiko(dosiye_icyinjizwa_izina(Idosiye)) if Idosiye else '', Ofuseti_agaciro.value, umurongo.value)

def gukora_ibwiriza():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Gusemura_inkomoko 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, nyakuri_amakurushingiro 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Inzira.resolve()) for Inzira in 기준.rglob('*') if Inzira.suffix in ('.c','.h','.cpp','.inc')
              and not set(Inzira.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and Inzira.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'ukoresha'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Urusobemiyoboro_Ikirundo'),
          '-I'+str(기준/'kure_agaciro'),'-I'+str(기준/'시언어번역기')]
    for Inzira in sorted(Path(Izina) for Izina in 소유파일 if Izina.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Inzira.suffix=='.cpp' else '-std=c11']
        if 'Urusobemiyoboro_Ikirundo' in Inzira.parts: 인수 += ['-I'+str(기준/'Urusobemiyoboro_Ikirundo'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in Inzira.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Inzira.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'kure_agaciro' in Inzira.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Inzira.parts: 인수 += ['-D__JKOROS__=1']
        if Inzira.name=='ipaki.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        itsinda_agaciro = (씨.c_char_p*len(인수))(*[icyinjizwa_agaciro.encode() for icyinjizwa_agaciro in 인수])
        Isemura_ibinyabumwe = 분석(색인,str(Inzira).encode(),itsinda_agaciro,len(인수),None,0,1)
        for umugerekashakiro in range(진단수(Isemura_ibinyabumwe)):
            진단 = 진단얻기(Isemura_ibinyabumwe,umugerekashakiro)
            if ubukare_agaciro(진단)>=3: 오류들.append((str(Inzira.relative_to(기준)),Umwandiko(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(icyinjizwa_agaciro,부모,amakurushingiro):
            Idosiye,Ofuseti_agaciro,umurongo = 자리(icyinjizwa_agaciro)
            if Idosiye not in 소유파일: return 2 if icyinjizwa_agaciro.종류==300 else 1
            낱말 = Umwandiko(이름얻기(icyinjizwa_agaciro))
            if not 낱말 or any(ord(inyuguti_agaciro)>127 for inyuguti_agaciro in 낱말): return 2
            if icyinjizwa_agaciro.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                RUKUMBI_agaciro = Umwandiko(RUKUMBI_izina(icyinjizwa_agaciro)) or Idosiye+':'+str(Ofuseti_agaciro)
                선언들[RUKUMBI_agaciro] = {'Idosiye':Idosiye,'Ofuseti_agaciro':Ofuseti_agaciro,'줄':umurongo,'종류':icyinjizwa_agaciro.종류,'Izina':낱말,'Guhuza':연결종류(icyinjizwa_agaciro)}
                참조들.append((Idosiye,Ofuseti_agaciro,낱말,RUKUMBI_agaciro))
            else:
                Indanga = 참조얻기(icyinjizwa_agaciro)
                Indanga_dosiye,_,_ = 자리(Indanga)
                if Indanga_dosiye in 소유파일:
                    RUKUMBI_agaciro = Umwandiko(RUKUMBI_izina(Indanga)); 참조들.append((Idosiye,Ofuseti_agaciro,Umwandiko(이름얻기(Indanga)),RUKUMBI_agaciro))
            return 2
        방문(뿌리(Isemura_ibinyabumwe),살피기,None)
        끝내기(Isemura_ibinyabumwe)
    aho_ijya_agaciro = 기준/'build/한국어화/시언어분석.json'
    aho_ijya_agaciro.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Idosiye:hashlib.sha256(Path(Idosiye).read_bytes()).hexdigest() for Idosiye in sorted(소유파일)}
    aho_ijya_agaciro.write_text(json.dumps({'선언':선언들,'Indanga':참조들,'IKOSA':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Indanga',len(참조들),'IKOSA',len(오류들))
    for IKOSA in 오류들: print(*IKOSA)

if __name__=='__main__': gukora_ibwiriza()
