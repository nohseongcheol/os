#!/usr/bin/env python3
"""libclang 선언·Leabhair_thagartha 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

teilgean_fréamh = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class teaghrán_VALUE(씨.Structure): _fields_ = [('sonraí',씨.c_void_p),('seó_VALUE',씨.c_uint)]
class cúrsóir_VALUE(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('sonraí',씨.c_void_p*3)]
class suíomh(씨.Structure): _fields_ = [('sonraí',씨.c_void_p*2),('OFFSET_VALUE',씨.c_uint)]
def feidhm_VALUE(Ainm, return_tomhas, *Argóintí):
    iontráil_VALUE = getattr(구현, Ainm); iontráil_VALUE.restype = return_tomhas; iontráil_VALUE.argtypes = list(Argóintí); return iontráil_VALUE
글얻기 = feidhm_VALUE('clang_getCString',씨.c_char_p,teaghrán_VALUE)
leagan_SMS = feidhm_VALUE('clang_disposeString',None,teaghrán_VALUE)
def Téacs(VALUE):
    tomhas = (글얻기(VALUE) or b'').decode('utf-8'); leagan_SMS(VALUE); return tomhas
이름얻기 = feidhm_VALUE('clang_getCursorSpelling',teaghrán_VALUE,cúrsóir_VALUE)
참조얻기 = feidhm_VALUE('clang_getCursorReferenced',cúrsóir_VALUE,cúrsóir_VALUE)
위치얻기 = feidhm_VALUE('clang_getCursorLocation',suíomh,cúrsóir_VALUE)
comhad_suíomh = feidhm_VALUE('clang_getFileLocation',None,suíomh,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
comhad_iontráil_ainm = feidhm_VALUE('clang_getFileName',teaghrán_VALUE,씨.c_void_p)
UNIQUE_ainm = feidhm_VALUE('clang_getCursorUSR',teaghrán_VALUE,cúrsóir_VALUE)
연결종류 = feidhm_VALUE('clang_getCursorLinkage',씨.c_uint,cúrsóir_VALUE)
방문형 = 씨.CFUNCTYPE(씨.c_uint,cúrsóir_VALUE,cúrsóir_VALUE,씨.c_void_p)
방문 = feidhm_VALUE('clang_visitChildren',씨.c_uint,cúrsóir_VALUE,방문형,씨.c_void_p)
giniúint = feidhm_VALUE('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = feidhm_VALUE('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
fréamh_VALUE = feidhm_VALUE('clang_getTranslationUnitCursor',cúrsóir_VALUE,씨.c_void_p)
scoir_clár_55b3a1cd = feidhm_VALUE('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = feidhm_VALUE('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = feidhm_VALUE('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
déine_VALUE = feidhm_VALUE('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = feidhm_VALUE('clang_getDiagnosticSpelling',teaghrán_VALUE,씨.c_void_p)
진단해제 = feidhm_VALUE('clang_disposeDiagnostic',None,씨.c_void_p)

def suíomh_INDEX(iontráil_VALUE):
    Comhad = 씨.c_void_p(); Líne = 씨.c_uint(); spás_iontráil = 씨.c_uint(); OFFSET_VALUE = 씨.c_uint()
    comhad_suíomh(위치얻기(iontráil_VALUE),씨.byref(Comhad),씨.byref(Líne),씨.byref(spás_iontráil),씨.byref(OFFSET_VALUE))
    return (Téacs(comhad_iontráil_ainm(Comhad)) if Comhad else '', OFFSET_VALUE.value, Líne.value)

def Rith_ordú():
    LOOKUP_INDEX = giniúint(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Aistrigh_foinse 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, iarbhír_sonraí 빌드에서는 계속 컴파일한다.
    소유파일 = {str(CONAIR.resolve()) for CONAIR in teilgean_fréamh.rglob('*') if CONAIR.suffix in ('.c','.h','.cpp','.inc')
              and not set(CONAIR.relative_to(teilgean_fréamh).parts)&{'build','dist','vendor','__pycache__'}
              and CONAIR.relative_to(teilgean_fréamh).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(teilgean_fréamh/'úsáideoir'),
          '-I'+str(teilgean_fréamh.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(teilgean_fréamh/'build'),'-I'+str(teilgean_fréamh/'build/user'),
          '-I'+str(teilgean_fréamh/'build/remote'),'-I'+str(teilgean_fréamh/'vendor/bearssl/inc'),
          '-I'+str(teilgean_fréamh/'vendor/bearssl/src'),'-I'+str(teilgean_fréamh/'vendor/libassh/src'),
          '-I'+str(teilgean_fréamh/'vendor/lwip/src/include'),'-I'+str(teilgean_fréamh/'Líonra_Cruach'),
          '-I'+str(teilgean_fréamh/'cianda_VALUE'),'-I'+str(teilgean_fréamh/'시언어번역기')]
    for CONAIR in sorted(Path(Ainm) for Ainm in 소유파일 if Ainm.endswith(('.c','.cpp'))):
        Argóintí = 공통 + ['-std=c++11' if CONAIR.suffix=='.cpp' else '-std=c11']
        if 'Líonra_Cruach' in CONAIR.parts: Argóintí += ['-I'+str(teilgean_fréamh/'Líonra_Cruach'),'-I'+str(teilgean_fréamh/'vendor/lwip/src/include')]
        if '시언어번역기' in CONAIR.parts:
            Argóintí += ['-I'+str(teilgean_fréamh/'시언어번역기'),'-I'+str(teilgean_fréamh/'vendor/tinycc'),'-I'+str(teilgean_fréamh/'build/ccompiler'),
                    '-isystem',str(teilgean_fréamh.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_traschóiritheoir' in CONAIR.parts:
            Argóintí += ['-I'+str(teilgean_fréamh/'PYTHON_traschóiritheoir'),'-I'+str(teilgean_fréamh/'build/micropython-1.24.1'),'-I'+str(teilgean_fréamh/'build/python'),'-isystem','/usr/include/newlib']
        if 'cianda_VALUE' in CONAIR.parts:
            Argóintí += ['-isystem', '/usr/include/newlib']
        if '배포' in CONAIR.parts: Argóintí += ['-D__JKOROS__=1']
        if CONAIR.name=='beart.c': Argóintí += ['-I'+str(teilgean_fréamh/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Grúpa_VALUE = (씨.c_char_p*len(Argóintí))(*[iontráil_VALUE.encode() for iontráil_VALUE in Argóintí])
        Aistriúchán_aonaid = 분석(LOOKUP_INDEX,str(CONAIR).encode(),Grúpa_VALUE,len(Argóintí),None,0,1)
        for INDEX in range(진단수(Aistriúchán_aonaid)):
            진단 = 진단얻기(Aistriúchán_aonaid,INDEX)
            if déine_VALUE(진단)>=3: 오류들.append((str(CONAIR.relative_to(teilgean_fréamh)),Téacs(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(iontráil_VALUE,부모,sonraí):
            Comhad,OFFSET_VALUE,Líne = suíomh_INDEX(iontráil_VALUE)
            if Comhad not in 소유파일: return 2 if iontráil_VALUE.종류==300 else 1
            낱말 = Téacs(이름얻기(iontráil_VALUE))
            if not 낱말 or any(ord(carachtar_VALUE)>127 for carachtar_VALUE in 낱말): return 2
            if iontráil_VALUE.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_VALUE = Téacs(UNIQUE_ainm(iontráil_VALUE)) or Comhad+':'+str(OFFSET_VALUE)
                선언들[UNIQUE_VALUE] = {'Comhad':Comhad,'OFFSET_VALUE':OFFSET_VALUE,'Líne':Líne,'종류':iontráil_VALUE.종류,'Ainm':낱말,'Nasc':연결종류(iontráil_VALUE)}
                참조들.append((Comhad,OFFSET_VALUE,낱말,UNIQUE_VALUE))
            else:
                Leabhair_thagartha = 참조얻기(iontráil_VALUE)
                Leabhair_thagartha_comhad,_,_ = suíomh_INDEX(Leabhair_thagartha)
                if Leabhair_thagartha_comhad in 소유파일:
                    UNIQUE_VALUE = Téacs(UNIQUE_ainm(Leabhair_thagartha)); 참조들.append((Comhad,OFFSET_VALUE,Téacs(이름얻기(Leabhair_thagartha)),UNIQUE_VALUE))
            return 2
        방문(fréamh_VALUE(Aistriúchán_aonaid),살피기,None)
        scoir_clár_55b3a1cd(Aistriúchán_aonaid)
    sprioc_VALUE = teilgean_fréamh/'build/한국어화/시언어분석.json'
    sprioc_VALUE.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Comhad:hashlib.sha256(Path(Comhad).read_bytes()).hexdigest() for Comhad in sorted(소유파일)}
    sprioc_VALUE.write_text(json.dumps({'선언':선언들,'Leabhair_thagartha':참조들,'ERREÁID':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Leabhair_thagartha',len(참조들),'ERREÁID',len(오류들))
    for ERREÁID in 오류들: print(*ERREÁID)

if __name__=='__main__': Rith_ordú()
