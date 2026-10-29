#!/usr/bin/env python3
"""libclang 선언·Dipadišo 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class molokoloko_boleng(씨.Structure): _fields_ = [('data',씨.c_void_p),('bontšha_boleng',씨.c_uint)]
class kheusa_boleng(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('data',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('data',씨.c_void_p*2),('E_Šetšego_boleng',씨.c_uint)]
def TIRO_boleng(Leina, 반환, *인수):
    go_tsenya_tshedimošo_boleng = getattr(구현, Leina); go_tsenya_tshedimošo_boleng.restype = 반환; go_tsenya_tshedimošo_boleng.argtypes = list(인수); return go_tsenya_tshedimošo_boleng
글얻기 = TIRO_boleng('clang_getCString',씨.c_char_p,molokoloko_boleng)
lokolla_SMS = TIRO_boleng('clang_disposeString',None,molokoloko_boleng)
def Sengwalwa(boleng):
    결과 = (글얻기(boleng) or b'').decode('utf-8'); lokolla_SMS(boleng); return 결과
이름얻기 = TIRO_boleng('clang_getCursorSpelling',molokoloko_boleng,kheusa_boleng)
참조얻기 = TIRO_boleng('clang_getCursorReferenced',kheusa_boleng,kheusa_boleng)
위치얻기 = TIRO_boleng('clang_getCursorLocation',위치,kheusa_boleng)
파일위치 = TIRO_boleng('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
faele_go_tsenya_tshedimošo_leina = TIRO_boleng('clang_getFileName',molokoloko_boleng,씨.c_void_p)
SETEE_leina = TIRO_boleng('clang_getCursorUSR',molokoloko_boleng,kheusa_boleng)
연결종류 = TIRO_boleng('clang_getCursorLinkage',씨.c_uint,kheusa_boleng)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kheusa_boleng,kheusa_boleng,씨.c_void_p)
방문 = TIRO_boleng('clang_visitChildren',씨.c_uint,kheusa_boleng,방문형,씨.c_void_p)
생성 = TIRO_boleng('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = TIRO_boleng('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = TIRO_boleng('clang_getTranslationUnitCursor',kheusa_boleng,씨.c_void_p)
끝내기 = TIRO_boleng('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = TIRO_boleng('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = TIRO_boleng('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
bokotsi_boleng = TIRO_boleng('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = TIRO_boleng('clang_getDiagnosticSpelling',molokoloko_boleng,씨.c_void_p)
진단해제 = TIRO_boleng('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(go_tsenya_tshedimošo_boleng):
    Faele = 씨.c_void_p(); mothaladi = 씨.c_uint(); sekgobana_go_tsenya_tshedimošo = 씨.c_uint(); E_Šetšego_boleng = 씨.c_uint()
    파일위치(위치얻기(go_tsenya_tshedimošo_boleng),씨.byref(Faele),씨.byref(mothaladi),씨.byref(sekgobana_go_tsenya_tshedimošo),씨.byref(E_Šetšego_boleng))
    return (Sengwalwa(faele_go_tsenya_tshedimošo_leina(Faele)) if Faele else '', E_Šetšego_boleng.value, mothaladi.value)

def phethagatša_taelo():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Fetolela_mohlodi 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, kgonthe_data 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Tsejana.resolve()) for Tsejana in 기준.rglob('*') if Tsejana.suffix in ('.c','.h','.cpp','.inc')
              and not set(Tsejana.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and Tsejana.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'mošomiši'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Netweke_kgoboko'),
          '-I'+str(기준/'ya_kgole_boleng'),'-I'+str(기준/'시언어번역기')]
    for Tsejana in sorted(Path(Leina) for Leina in 소유파일 if Leina.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Tsejana.suffix=='.cpp' else '-std=c11']
        if 'Netweke_kgoboko' in Tsejana.parts: 인수 += ['-I'+str(기준/'Netweke_kgoboko'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in Tsejana.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Tsejana.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'ya_kgole_boleng' in Tsejana.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Tsejana.parts: 인수 += ['-D__JKOROS__=1']
        if Tsejana.name=='sehlopha.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        sehlopha_boleng = (씨.c_char_p*len(인수))(*[go_tsenya_tshedimošo_boleng.encode() for go_tsenya_tshedimošo_boleng in 인수])
        Phetolelo_thutišo = 분석(색인,str(Tsejana).encode(),sehlopha_boleng,len(인수),None,0,1)
        for lokela in range(진단수(Phetolelo_thutišo)):
            진단 = 진단얻기(Phetolelo_thutišo,lokela)
            if bokotsi_boleng(진단)>=3: 오류들.append((str(Tsejana.relative_to(기준)),Sengwalwa(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(go_tsenya_tshedimošo_boleng,부모,data):
            Faele,E_Šetšego_boleng,mothaladi = 자리(go_tsenya_tshedimošo_boleng)
            if Faele not in 소유파일: return 2 if go_tsenya_tshedimošo_boleng.종류==300 else 1
            낱말 = Sengwalwa(이름얻기(go_tsenya_tshedimošo_boleng))
            if not 낱말 or any(ord(tlhaka_boleng)>127 for tlhaka_boleng in 낱말): return 2
            if go_tsenya_tshedimošo_boleng.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                SETEE_boleng = Sengwalwa(SETEE_leina(go_tsenya_tshedimošo_boleng)) or Faele+':'+str(E_Šetšego_boleng)
                선언들[SETEE_boleng] = {'Faele':Faele,'E_Šetšego_boleng':E_Šetšego_boleng,'줄':mothaladi,'종류':go_tsenya_tshedimošo_boleng.종류,'Leina':낱말,'Ikgokaganye':연결종류(go_tsenya_tshedimošo_boleng)}
                참조들.append((Faele,E_Šetšego_boleng,낱말,SETEE_boleng))
            else:
                Dipadišo = 참조얻기(go_tsenya_tshedimošo_boleng)
                Dipadišo_faele,_,_ = 자리(Dipadišo)
                if Dipadišo_faele in 소유파일:
                    SETEE_boleng = Sengwalwa(SETEE_leina(Dipadišo)); 참조들.append((Faele,E_Šetšego_boleng,Sengwalwa(이름얻기(Dipadišo)),SETEE_boleng))
            return 2
        방문(뿌리(Phetolelo_thutišo),살피기,None)
        끝내기(Phetolelo_thutišo)
    boyo_boleng = 기준/'build/한국어화/시언어분석.json'
    boyo_boleng.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Faele:hashlib.sha256(Path(Faele).read_bytes()).hexdigest() for Faele in sorted(소유파일)}
    boyo_boleng.write_text(json.dumps({'선언':선언들,'Dipadišo':참조들,'Phošo':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Dipadišo',len(참조들),'Phošo',len(오류들))
    for Phošo in 오류들: print(*Phošo)

if __name__=='__main__': phethagatša_taelo()
