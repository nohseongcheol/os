#!/usr/bin/env python3
"""libclang 선언·Isalathiso 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class uluhlu_lweekharektha_ixabiso(씨.Structure): _fields_ = [('iingcombolo',씨.c_void_p),('bonisa_ixabiso',씨.c_uint)]
class ikhesa_ixabiso(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('iingcombolo',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('iingcombolo',씨.c_void_p*2),('Ukulinganisa_ixabiso',씨.c_uint)]
def INKQUBO_ixabiso(Igama, 반환, *인수):
    ufako_nkcukacha_ixabiso = getattr(구현, Igama); ufako_nkcukacha_ixabiso.restype = 반환; ufako_nkcukacha_ixabiso.argtypes = list(인수); return ufako_nkcukacha_ixabiso
글얻기 = INKQUBO_ixabiso('clang_getCString',씨.c_char_p,uluhlu_lweekharektha_ixabiso)
vulela_I_SMS = INKQUBO_ixabiso('clang_disposeString',None,uluhlu_lweekharektha_ixabiso)
def Umbhalo(ixabiso):
    결과 = (글얻기(ixabiso) or b'').decode('utf-8'); vulela_I_SMS(ixabiso); return 결과
이름얻기 = INKQUBO_ixabiso('clang_getCursorSpelling',uluhlu_lweekharektha_ixabiso,ikhesa_ixabiso)
참조얻기 = INKQUBO_ixabiso('clang_getCursorReferenced',ikhesa_ixabiso,ikhesa_ixabiso)
위치얻기 = INKQUBO_ixabiso('clang_getCursorLocation',위치,ikhesa_ixabiso)
파일위치 = INKQUBO_ixabiso('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ifayile_ufako_nkcukacha_igama = INKQUBO_ixabiso('clang_getFileName',uluhlu_lweekharektha_ixabiso,씨.c_void_p)
EYODWA_igama = INKQUBO_ixabiso('clang_getCursorUSR',uluhlu_lweekharektha_ixabiso,ikhesa_ixabiso)
연결종류 = INKQUBO_ixabiso('clang_getCursorLinkage',씨.c_uint,ikhesa_ixabiso)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ikhesa_ixabiso,ikhesa_ixabiso,씨.c_void_p)
방문 = INKQUBO_ixabiso('clang_visitChildren',씨.c_uint,ikhesa_ixabiso,방문형,씨.c_void_p)
생성 = INKQUBO_ixabiso('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = INKQUBO_ixabiso('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = INKQUBO_ixabiso('clang_getTranslationUnitCursor',ikhesa_ixabiso,씨.c_void_p)
끝내기 = INKQUBO_ixabiso('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = INKQUBO_ixabiso('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = INKQUBO_ixabiso('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
umlinganiselo_ixabiso = INKQUBO_ixabiso('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = INKQUBO_ixabiso('clang_getDiagnosticSpelling',uluhlu_lweekharektha_ixabiso,씨.c_void_p)
진단해제 = INKQUBO_ixabiso('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(ufako_nkcukacha_ixabiso):
    iFayili = 씨.c_void_p(); umgca = 씨.c_uint(); isithuba_ufako_nkcukacha = 씨.c_uint(); Ukulinganisa_ixabiso = 씨.c_uint()
    파일위치(위치얻기(ufako_nkcukacha_ixabiso),씨.byref(iFayili),씨.byref(umgca),씨.byref(isithuba_ufako_nkcukacha),씨.byref(Ukulinganisa_ixabiso))
    return (Umbhalo(ifayile_ufako_nkcukacha_igama(iFayili)) if iFayili else '', Ukulinganisa_ixabiso.value, umgca.value)

def ukwenza_umyalelo():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Ukuguqulela_umthombo 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, eyona_yenzekileyo_iingcombolo 빌드에서는 계속 컴파일한다.
    소유파일 = {str(INDLELA.resolve()) for INDLELA in 기준.rglob('*') if INDLELA.suffix in ('.c','.h','.cpp','.inc')
              and not set(INDLELA.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and INDLELA.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'umsebenzisi'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Inethiwekhi_fumba'),
          '-I'+str(기준/'kude_ixabiso'),'-I'+str(기준/'시언어번역기')]
    for INDLELA in sorted(Path(Igama) for Igama in 소유파일 if Igama.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if INDLELA.suffix=='.cpp' else '-std=c11']
        if 'Inethiwekhi_fumba' in INDLELA.parts: 인수 += ['-I'+str(기준/'Inethiwekhi_fumba'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in INDLELA.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in INDLELA.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'kude_ixabiso' in INDLELA.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in INDLELA.parts: 인수 += ['-D__JKOROS__=1']
        if INDLELA.name=='umqulu.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        iqela_ixabiso = (씨.c_char_p*len(인수))(*[ufako_nkcukacha_ixabiso.encode() for ufako_nkcukacha_ixabiso in 인수])
        Uguqulelo_magama_isifundo = 분석(색인,str(INDLELA).encode(),iqela_ixabiso,len(인수),None,0,1)
        for indeksa in range(진단수(Uguqulelo_magama_isifundo)):
            진단 = 진단얻기(Uguqulelo_magama_isifundo,indeksa)
            if umlinganiselo_ixabiso(진단)>=3: 오류들.append((str(INDLELA.relative_to(기준)),Umbhalo(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ufako_nkcukacha_ixabiso,부모,iingcombolo):
            iFayili,Ukulinganisa_ixabiso,umgca = 자리(ufako_nkcukacha_ixabiso)
            if iFayili not in 소유파일: return 2 if ufako_nkcukacha_ixabiso.종류==300 else 1
            낱말 = Umbhalo(이름얻기(ufako_nkcukacha_ixabiso))
            if not 낱말 or any(ord(ikharakhtha_ixabiso)>127 for ikharakhtha_ixabiso in 낱말): return 2
            if ufako_nkcukacha_ixabiso.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                EYODWA_ixabiso = Umbhalo(EYODWA_igama(ufako_nkcukacha_ixabiso)) or iFayili+':'+str(Ukulinganisa_ixabiso)
                선언들[EYODWA_ixabiso] = {'iFayili':iFayili,'Ukulinganisa_ixabiso':Ukulinganisa_ixabiso,'줄':umgca,'종류':ufako_nkcukacha_ixabiso.종류,'Igama':낱말,'Nxulumanisa':연결종류(ufako_nkcukacha_ixabiso)}
                참조들.append((iFayili,Ukulinganisa_ixabiso,낱말,EYODWA_ixabiso))
            else:
                Isalathiso = 참조얻기(ufako_nkcukacha_ixabiso)
                Isalathiso_ifayile,_,_ = 자리(Isalathiso)
                if Isalathiso_ifayile in 소유파일:
                    EYODWA_ixabiso = Umbhalo(EYODWA_igama(Isalathiso)); 참조들.append((iFayili,Ukulinganisa_ixabiso,Umbhalo(이름얻기(Isalathiso)),EYODWA_ixabiso))
            return 2
        방문(뿌리(Uguqulelo_magama_isifundo),살피기,None)
        끝내기(Uguqulelo_magama_isifundo)
    indawo_ekuyiwa_kuyo_ixabiso = 기준/'build/한국어화/시언어분석.json'
    indawo_ekuyiwa_kuyo_ixabiso.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {iFayili:hashlib.sha256(Path(iFayili).read_bytes()).hexdigest() for iFayili in sorted(소유파일)}
    indawo_ekuyiwa_kuyo_ixabiso.write_text(json.dumps({'선언':선언들,'Isalathiso':참조들,'Impazamo':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Isalathiso',len(참조들),'Impazamo',len(오류들))
    for Impazamo in 오류들: print(*Impazamo)

if __name__=='__main__': ukwenza_umyalelo()
