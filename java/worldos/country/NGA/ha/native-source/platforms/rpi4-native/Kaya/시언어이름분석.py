#!/usr/bin/env python3
"""libclang bayyanarwa·Manazarta 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class Zare_Daraja(씨.Structure): _fields_ = [('Tarin_bayani',씨.c_void_p),('Nuna_Daraja',씨.c_uint)]
class Ɗan_jagora_Daraja(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('Tarin_bayani',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('Tarin_bayani',씨.c_void_p*2),('Sassautawa_Daraja',씨.c_uint)]
def AIKI_Daraja(Suna, 반환, *인수):
    Mashigar_bayanai_Daraja = getattr(구현, Suna); Mashigar_bayanai_Daraja.restype = 반환; Mashigar_bayanai_Daraja.argtypes = list(인수); return Mashigar_bayanai_Daraja
samo_SMS = AIKI_Daraja('clang_getCString',씨.c_char_p,Zare_Daraja)
saka_SMS = AIKI_Daraja('clang_disposeString',None,Zare_Daraja)
def SMS(Daraja):
    결과 = (samo_SMS(Daraja) or b'').decode('utf-8'); saka_SMS(Daraja); return 결과
samo_Suna = AIKI_Daraja('clang_getCursorSpelling',Zare_Daraja,Ɗan_jagora_Daraja)
samo_Manazarta = AIKI_Daraja('clang_getCursorReferenced',Ɗan_jagora_Daraja,Ɗan_jagora_Daraja)
위치얻기 = AIKI_Daraja('clang_getCursorLocation',위치,Ɗan_jagora_Daraja)
파일위치 = AIKI_Daraja('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
Fayil_Mashigar_bayanai_Suna = AIKI_Daraja('clang_getFileName',Zare_Daraja,씨.c_void_p)
MUSAMMAN_Suna = AIKI_Daraja('clang_getCursorUSR',Zare_Daraja,Ɗan_jagora_Daraja)
연결종류 = AIKI_Daraja('clang_getCursorLinkage',씨.c_uint,Ɗan_jagora_Daraja)
방문형 = 씨.CFUNCTYPE(씨.c_uint,Ɗan_jagora_Daraja,Ɗan_jagora_Daraja,씨.c_void_p)
방문 = AIKI_Daraja('clang_visitChildren',씨.c_uint,Ɗan_jagora_Daraja,방문형,씨.c_void_p)
생성 = AIKI_Daraja('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = AIKI_Daraja('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = AIKI_Daraja('clang_getTranslationUnitCursor',Ɗan_jagora_Daraja,씨.c_void_p)
끝내기 = AIKI_Daraja('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = AIKI_Daraja('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = AIKI_Daraja('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
tsananin_kuskure_Daraja = AIKI_Daraja('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = AIKI_Daraja('clang_getDiagnosticSpelling',Zare_Daraja,씨.c_void_p)
진단해제 = AIKI_Daraja('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(Mashigar_bayanai_Daraja):
    Fayil = 씨.c_void_p(); Layi = 씨.c_uint(); rami_Mashigar_bayanai = 씨.c_uint(); Sassautawa_Daraja = 씨.c_uint()
    파일위치(위치얻기(Mashigar_bayanai_Daraja),씨.byref(Fayil),씨.byref(Layi),씨.byref(rami_Mashigar_bayanai),씨.byref(Sassautawa_Daraja))
    return (SMS(Fayil_Mashigar_bayanai_Suna(Fayil)) if Fayil else '', Sassautawa_Daraja.value, Layi.value)

def gudanar_Umarni():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 bayyanarwa 없이 TinyCC 외부 단일 Fasara_tushe 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, Na_hakika_Tarin_bayani 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Hanyar_shiga.resolve()) for Hanyar_shiga in 기준.rglob('*') if Hanyar_shiga.suffix in ('.c','.h','.cpp','.inc')
              and not set(Hanyar_shiga.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and Hanyar_shiga.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'Mai_anfani_da_kwamfuta'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Hanyar_sadarwa_tara'),
          '-I'+str(기준/'na_nesa_Daraja'),'-I'+str(기준/'시언어번역기')]
    for Hanyar_shiga in sorted(Path(Suna) for Suna in 소유파일 if Suna.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Hanyar_shiga.suffix=='.cpp' else '-std=c11']
        if 'Hanyar_sadarwa_tara' in Hanyar_shiga.parts: 인수 += ['-I'+str(기준/'Hanyar_sadarwa_tara'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in Hanyar_shiga.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Hanyar_shiga.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'na_nesa_Daraja' in Hanyar_shiga.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Hanyar_shiga.parts: 인수 += ['-D__JKOROS__=1']
        if Hanyar_shiga.name=='dami.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        gungu_Daraja = (씨.c_char_p*len(인수))(*[Mashigar_bayanai_Daraja.encode() for Mashigar_bayanai_Daraja in 인수])
        번역단위 = 분석(색인,str(Hanyar_shiga).encode(),gungu_Daraja,len(인수),None,0,1)
        for Indes in range(진단수(번역단위)):
            진단 = 진단얻기(번역단위,Indes)
            if tsananin_kuskure_Daraja(진단)>=3: 오류들.append((str(Hanyar_shiga.relative_to(기준)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(Mashigar_bayanai_Daraja,부모,Tarin_bayani):
            Fayil,Sassautawa_Daraja,Layi = 자리(Mashigar_bayanai_Daraja)
            if Fayil not in 소유파일: return 2 if Mashigar_bayanai_Daraja.종류==300 else 1
            낱말 = SMS(samo_Suna(Mashigar_bayanai_Daraja))
            if not 낱말 or any(ord(Harafi_Daraja)>127 for Harafi_Daraja in 낱말): return 2
            if Mashigar_bayanai_Daraja.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                MUSAMMAN_Daraja = SMS(MUSAMMAN_Suna(Mashigar_bayanai_Daraja)) or Fayil+':'+str(Sassautawa_Daraja)
                선언들[MUSAMMAN_Daraja] = {'Fayil':Fayil,'Sassautawa_Daraja':Sassautawa_Daraja,'줄':Layi,'종류':Mashigar_bayanai_Daraja.종류,'Suna':낱말,'Haɗi':연결종류(Mashigar_bayanai_Daraja)}
                참조들.append((Fayil,Sassautawa_Daraja,낱말,MUSAMMAN_Daraja))
            else:
                Manazarta = samo_Manazarta(Mashigar_bayanai_Daraja)
                Manazarta_Fayil,_,_ = 자리(Manazarta)
                if Manazarta_Fayil in 소유파일:
                    MUSAMMAN_Daraja = SMS(MUSAMMAN_Suna(Manazarta)); 참조들.append((Fayil,Sassautawa_Daraja,SMS(samo_Suna(Manazarta)),MUSAMMAN_Daraja))
            return 2
        방문(뿌리(번역단위),살피기,None)
        끝내기(번역단위)
    Zangon_ƙarshe_Daraja = 기준/'build/한국어화/시언어분석.json'
    Zangon_ƙarshe_Daraja.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fayil:hashlib.sha256(Path(Fayil).read_bytes()).hexdigest() for Fayil in sorted(소유파일)}
    Zangon_ƙarshe_Daraja.write_text(json.dumps({'bayyanarwa':선언들,'Manazarta':참조들,'Kuskure':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('bayyanarwa',len(선언들),'Manazarta',len(참조들),'Kuskure',len(오류들))
    for Kuskure in 오류들: print(*Kuskure)

if __name__=='__main__': gudanar_Umarni()
