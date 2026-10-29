#!/usr/bin/env python3
"""libclang 선언·Pūranga_kōrero 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

whakaatu_pūtake = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class aho_uara(씨.Structure): _fields_ = [('raraunga',씨.c_void_p),('whakaatu_uara',씨.c_uint)]
class pehu_uara(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('raraunga',씨.c_void_p*3)]
class tūranga(씨.Structure): _fields_ = [('raraunga',씨.c_void_p*2),('OFFSET_uara',씨.c_uint)]
def TAUMAHI_uara(Ingoa, 반환, *인수):
    tāurunga_uara = getattr(구현, Ingoa); tāurunga_uara.restype = 반환; tāurunga_uara.argtypes = list(인수); return tāurunga_uara
글얻기 = TAUMAHI_uara('clang_getCString',씨.c_char_p,aho_uara)
tuku_TEXT = TAUMAHI_uara('clang_disposeString',None,aho_uara)
def Ngā_kupu(uara):
    mēhua = (글얻기(uara) or b'').decode('utf-8'); tuku_TEXT(uara); return mēhua
이름얻기 = TAUMAHI_uara('clang_getCursorSpelling',aho_uara,pehu_uara)
참조얻기 = TAUMAHI_uara('clang_getCursorReferenced',pehu_uara,pehu_uara)
위치얻기 = TAUMAHI_uara('clang_getCursorLocation',tūranga,pehu_uara)
kōnae_tūranga = TAUMAHI_uara('clang_getFileLocation',None,tūranga,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
kōnae_tāurunga_ingoa = TAUMAHI_uara('clang_getFileName',aho_uara,씨.c_void_p)
UNIQUE_ingoa = TAUMAHI_uara('clang_getCursorUSR',aho_uara,pehu_uara)
연결종류 = TAUMAHI_uara('clang_getCursorLinkage',씨.c_uint,pehu_uara)
방문형 = 씨.CFUNCTYPE(씨.c_uint,pehu_uara,pehu_uara,씨.c_void_p)
방문 = TAUMAHI_uara('clang_visitChildren',씨.c_uint,pehu_uara,방문형,씨.c_void_p)
waihanga = TAUMAHI_uara('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = TAUMAHI_uara('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
pūtake_uara = TAUMAHI_uara('clang_getTranslationUnitCursor',pehu_uara,씨.c_void_p)
wehe_kaupapa = TAUMAHI_uara('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = TAUMAHI_uara('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = TAUMAHI_uara('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
kaha_uara = TAUMAHI_uara('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = TAUMAHI_uara('clang_getDiagnosticSpelling',aho_uara,씨.c_void_p)
진단해제 = TAUMAHI_uara('clang_disposeDiagnostic',None,씨.c_void_p)

def tūranga_INDEX(tāurunga_uara):
    Kōnae = 씨.c_void_p(); hononga = 씨.c_uint(); kāniwha_tāurunga = 씨.c_uint(); OFFSET_uara = 씨.c_uint()
    kōnae_tūranga(위치얻기(tāurunga_uara),씨.byref(Kōnae),씨.byref(hononga),씨.byref(kāniwha_tāurunga),씨.byref(OFFSET_uara))
    return (Ngā_kupu(kōnae_tāurunga_ingoa(Kōnae)) if Kōnae else '', OFFSET_uara.value, hononga.value)

def kawe_tono():
    Rapu_INDEX = waihanga(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 TRANSLATE_pūtake 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, tūturu_raraunga 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ara.resolve()) for ara in whakaatu_pūtake.rglob('*') if ara.suffix in ('.c','.h','.cpp','.inc')
              and not set(ara.relative_to(whakaatu_pūtake).parts)&{'build','dist','vendor','__pycache__'}
              and ara.relative_to(whakaatu_pūtake).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(whakaatu_pūtake/'kaiwhakamahi'),
          '-I'+str(whakaatu_pūtake.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(whakaatu_pūtake/'build'),'-I'+str(whakaatu_pūtake/'build/user'),
          '-I'+str(whakaatu_pūtake/'build/remote'),'-I'+str(whakaatu_pūtake/'vendor/bearssl/inc'),
          '-I'+str(whakaatu_pūtake/'vendor/bearssl/src'),'-I'+str(whakaatu_pūtake/'vendor/libassh/src'),
          '-I'+str(whakaatu_pūtake/'vendor/lwip/src/include'),'-I'+str(whakaatu_pūtake/'whatunga_Huinga'),
          '-I'+str(whakaatu_pūtake/'mamao_uara'),'-I'+str(whakaatu_pūtake/'시언어번역기')]
    for ara in sorted(Path(Ingoa) for Ingoa in 소유파일 if Ingoa.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ara.suffix=='.cpp' else '-std=c11']
        if 'whatunga_Huinga' in ara.parts: 인수 += ['-I'+str(whakaatu_pūtake/'whatunga_Huinga'),'-I'+str(whakaatu_pūtake/'vendor/lwip/src/include')]
        if '시언어번역기' in ara.parts:
            인수 += ['-I'+str(whakaatu_pūtake/'시언어번역기'),'-I'+str(whakaatu_pūtake/'vendor/tinycc'),'-I'+str(whakaatu_pūtake/'build/ccompiler'),
                    '-isystem',str(whakaatu_pūtake.parent/'rpi4/build/rootfs/usr/include')]
        if 'PYTHON_arawhata' in ara.parts:
            인수 += ['-I'+str(whakaatu_pūtake/'PYTHON_arawhata'),'-I'+str(whakaatu_pūtake/'build/micropython-1.24.1'),'-I'+str(whakaatu_pūtake/'build/python'),'-isystem','/usr/include/newlib']
        if 'mamao_uara' in ara.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ara.parts: 인수 += ['-D__JKOROS__=1']
        if ara.name=='pūpū.c': 인수 += ['-I'+str(whakaatu_pūtake/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        rōpū_uara = (씨.c_char_p*len(인수))(*[tāurunga_uara.encode() for tāurunga_uara in 인수])
        Whakawhiti_Reo_ngā_wae = 분석(Rapu_INDEX,str(ara).encode(),rōpū_uara,len(인수),None,0,1)
        for INDEX in range(진단수(Whakawhiti_Reo_ngā_wae)):
            진단 = 진단얻기(Whakawhiti_Reo_ngā_wae,INDEX)
            if kaha_uara(진단)>=3: 오류들.append((str(ara.relative_to(whakaatu_pūtake)),Ngā_kupu(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(tāurunga_uara,부모,raraunga):
            Kōnae,OFFSET_uara,hononga = tūranga_INDEX(tāurunga_uara)
            if Kōnae not in 소유파일: return 2 if tāurunga_uara.종류==300 else 1
            낱말 = Ngā_kupu(이름얻기(tāurunga_uara))
            if not 낱말 or any(ord(pūāhua_uara)>127 for pūāhua_uara in 낱말): return 2
            if tāurunga_uara.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_uara = Ngā_kupu(UNIQUE_ingoa(tāurunga_uara)) or Kōnae+':'+str(OFFSET_uara)
                선언들[UNIQUE_uara] = {'Kōnae':Kōnae,'OFFSET_uara':OFFSET_uara,'줄':hononga,'종류':tāurunga_uara.종류,'Ingoa':낱말,'TŪHONO':연결종류(tāurunga_uara)}
                참조들.append((Kōnae,OFFSET_uara,낱말,UNIQUE_uara))
            else:
                Pūranga_kōrero = 참조얻기(tāurunga_uara)
                Pūranga_kōrero_kōnae,_,_ = tūranga_INDEX(Pūranga_kōrero)
                if Pūranga_kōrero_kōnae in 소유파일:
                    UNIQUE_uara = Ngā_kupu(UNIQUE_ingoa(Pūranga_kōrero)); 참조들.append((Kōnae,OFFSET_uara,Ngā_kupu(이름얻기(Pūranga_kōrero)),UNIQUE_uara))
            return 2
        방문(pūtake_uara(Whakawhiti_Reo_ngā_wae),살피기,None)
        wehe_kaupapa(Whakawhiti_Reo_ngā_wae)
    ūnga_uara = whakaatu_pūtake/'build/한국어화/시언어분석.json'
    ūnga_uara.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Kōnae:hashlib.sha256(Path(Kōnae).read_bytes()).hexdigest() for Kōnae in sorted(소유파일)}
    ūnga_uara.write_text(json.dumps({'선언':선언들,'Pūranga_kōrero':참조들,'Pōhēhē':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Pūranga_kōrero',len(참조들),'Pōhēhē',len(오류들))
    for Pōhēhē in 오류들: print(*Pōhēhē)

if __name__=='__main__': kawe_tono()
