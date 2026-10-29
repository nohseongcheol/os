#!/usr/bin/env python3
"""libclang 선언·Royukaay 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class araf_yu_bennoo_xëyma(씨.Structure): _fields_ = [('mbir',씨.c_void_p),('féeñal_xëyma',씨.c_uint)]
class barab_bees_mën_a_bind_xëyma(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('mbir',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('mbir',씨.c_void_p*2),('Randal_xëyma',씨.c_uint)]
def liëey_xëyma(tur_253d1510, 반환, *인수):
    dugal_xabaar_xëyma = getattr(구현, tur_253d1510); dugal_xabaar_xëyma.restype = 반환; dugal_xabaar_xëyma.argtypes = list(인수); return dugal_xabaar_xëyma
글얻기 = liëey_xëyma('clang_getCString',씨.c_char_p,araf_yu_bennoo_xëyma)
yewwi_SMS = liëey_xëyma('clang_disposeString',None,araf_yu_bennoo_xëyma)
def Tekst(xëyma):
    결과 = (글얻기(xëyma) or b'').decode('utf-8'); yewwi_SMS(xëyma); return 결과
이름얻기 = liëey_xëyma('clang_getCursorSpelling',araf_yu_bennoo_xëyma,barab_bees_mën_a_bind_xëyma)
참조얻기 = liëey_xëyma('clang_getCursorReferenced',barab_bees_mën_a_bind_xëyma,barab_bees_mën_a_bind_xëyma)
위치얻기 = liëey_xëyma('clang_getCursorLocation',위치,barab_bees_mën_a_bind_xëyma)
파일위치 = liëey_xëyma('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
bara_denc_dugal_xabaar_tur = liëey_xëyma('clang_getFileName',araf_yu_bennoo_xëyma,씨.c_void_p)
UNIQUE_tur = liëey_xëyma('clang_getCursorUSR',araf_yu_bennoo_xëyma,barab_bees_mën_a_bind_xëyma)
연결종류 = liëey_xëyma('clang_getCursorLinkage',씨.c_uint,barab_bees_mën_a_bind_xëyma)
방문형 = 씨.CFUNCTYPE(씨.c_uint,barab_bees_mën_a_bind_xëyma,barab_bees_mën_a_bind_xëyma,씨.c_void_p)
방문 = liëey_xëyma('clang_visitChildren',씨.c_uint,barab_bees_mën_a_bind_xëyma,방문형,씨.c_void_p)
생성 = liëey_xëyma('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = liëey_xëyma('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = liëey_xëyma('clang_getTranslationUnitCursor',barab_bees_mën_a_bind_xëyma,씨.c_void_p)
끝내기 = liëey_xëyma('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = liëey_xëyma('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = liëey_xëyma('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
taraay_xëyma = liëey_xëyma('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = liëey_xëyma('clang_getDiagnosticSpelling',araf_yu_bennoo_xëyma,씨.c_void_p)
진단해제 = liëey_xëyma('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(dugal_xabaar_xëyma):
    bara_denc = 씨.c_void_p(); buum = 씨.c_uint(); xar_xar_dugal_xabaar = 씨.c_uint(); Randal_xëyma = 씨.c_uint()
    파일위치(위치얻기(dugal_xabaar_xëyma),씨.byref(bara_denc),씨.byref(buum),씨.byref(xar_xar_dugal_xabaar),씨.byref(Randal_xëyma))
    return (Tekst(bara_denc_dugal_xabaar_tur(bara_denc)) if bara_denc else '', Randal_xëyma.value, buum.value)

def def_ndigel():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Tekki_Cosaan 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, liteew_mbir 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Yoonu_jëmale.resolve()) for Yoonu_jëmale in 기준.rglob('*') if Yoonu_jëmale.suffix in ('.c','.h','.cpp','.inc')
              and not set(Yoonu_jëmale.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and Yoonu_jëmale.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'kiy_jariñoo_internet'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'mbaal_Tegalo'),
          '-I'+str(기준/'lu_soree_xëyma'),'-I'+str(기준/'시언어번역기')]
    for Yoonu_jëmale in sorted(Path(tur_253d1510) for tur_253d1510 in 소유파일 if tur_253d1510.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Yoonu_jëmale.suffix=='.cpp' else '-std=c11']
        if 'mbaal_Tegalo' in Yoonu_jëmale.parts: 인수 += ['-I'+str(기준/'mbaal_Tegalo'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in Yoonu_jëmale.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Yoonu_jëmale.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'lu_soree_xëyma' in Yoonu_jëmale.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Yoonu_jëmale.parts: 인수 += ['-D__JKOROS__=1']
        if Yoonu_jëmale.name=='takku_xéewël.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        mboolo_xëyma = (씨.c_char_p*len(인수))(*[dugal_xabaar_xëyma.encode() for dugal_xabaar_xëyma in 인수])
        Tekki_sa = 분석(색인,str(Yoonu_jëmale).encode(),mboolo_xëyma,len(인수),None,0,1)
        for àlluwa_tur in range(진단수(Tekki_sa)):
            진단 = 진단얻기(Tekki_sa,àlluwa_tur)
            if taraay_xëyma(진단)>=3: 오류들.append((str(Yoonu_jëmale.relative_to(기준)),Tekst(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(dugal_xabaar_xëyma,부모,mbir):
            bara_denc,Randal_xëyma,buum = 자리(dugal_xabaar_xëyma)
            if bara_denc not in 소유파일: return 2 if dugal_xabaar_xëyma.종류==300 else 1
            낱말 = Tekst(이름얻기(dugal_xabaar_xëyma))
            if not 낱말 or any(ord(Araf_xëyma)>127 for Araf_xëyma in 낱말): return 2
            if dugal_xabaar_xëyma.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                UNIQUE_xëyma = Tekst(UNIQUE_tur(dugal_xabaar_xëyma)) or bara_denc+':'+str(Randal_xëyma)
                선언들[UNIQUE_xëyma] = {'bara_denc':bara_denc,'Randal_xëyma':Randal_xëyma,'줄':buum,'종류':dugal_xabaar_xëyma.종류,'tur_253d1510':낱말,'JOKKOO':연결종류(dugal_xabaar_xëyma)}
                참조들.append((bara_denc,Randal_xëyma,낱말,UNIQUE_xëyma))
            else:
                Royukaay = 참조얻기(dugal_xabaar_xëyma)
                Royukaay_bara_denc,_,_ = 자리(Royukaay)
                if Royukaay_bara_denc in 소유파일:
                    UNIQUE_xëyma = Tekst(UNIQUE_tur(Royukaay)); 참조들.append((bara_denc,Randal_xëyma,Tekst(이름얻기(Royukaay)),UNIQUE_xëyma))
            return 2
        방문(뿌리(Tekki_sa),살피기,None)
        끝내기(Tekki_sa)
    jëmmukaay_xëyma = 기준/'build/한국어화/시언어분석.json'
    jëmmukaay_xëyma.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {bara_denc:hashlib.sha256(Path(bara_denc).read_bytes()).hexdigest() for bara_denc in sorted(소유파일)}
    jëmmukaay_xëyma.write_text(json.dumps({'선언':선언들,'Royukaay':참조들,'njumte':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Royukaay',len(참조들),'njumte',len(오류들))
    for njumte in 오류들: print(*njumte)

if __name__=='__main__': def_ndigel()
