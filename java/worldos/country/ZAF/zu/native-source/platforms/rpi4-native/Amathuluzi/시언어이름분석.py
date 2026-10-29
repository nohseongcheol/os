#!/usr/bin/env python3
"""libclang 선언·Ireferensi 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class uchunge_inani(씨.Structure): _fields_ = [('imininingwane',씨.c_void_p),('khombisa_inani',씨.c_uint)]
class isikhombisi_inani(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('imininingwane',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('imininingwane',씨.c_void_p*2),('I_ofisethi_inani',씨.c_uint)]
def umsebenzi_inani(Igama, 반환, *인수):
    okufakwayo_inani = getattr(구현, Igama); okufakwayo_inani.restype = 반환; okufakwayo_inani.argtypes = list(인수); return okufakwayo_inani
글얻기 = umsebenzi_inani('clang_getCString',씨.c_char_p,uchunge_inani)
khulula_I_SMS = umsebenzi_inani('clang_disposeString',None,uchunge_inani)
def Itekisi(inani):
    결과 = (글얻기(inani) or b'').decode('utf-8'); khulula_I_SMS(inani); return 결과
이름얻기 = umsebenzi_inani('clang_getCursorSpelling',uchunge_inani,isikhombisi_inani)
참조얻기 = umsebenzi_inani('clang_getCursorReferenced',isikhombisi_inani,isikhombisi_inani)
위치얻기 = umsebenzi_inani('clang_getCursorLocation',위치,isikhombisi_inani)
파일위치 = umsebenzi_inani('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ifayela_okufakwayo_igama = umsebenzi_inani('clang_getFileName',uchunge_inani,씨.c_void_p)
OKUHLUKILE_igama = umsebenzi_inani('clang_getCursorUSR',uchunge_inani,isikhombisi_inani)
연결종류 = umsebenzi_inani('clang_getCursorLinkage',씨.c_uint,isikhombisi_inani)
방문형 = 씨.CFUNCTYPE(씨.c_uint,isikhombisi_inani,isikhombisi_inani,씨.c_void_p)
방문 = umsebenzi_inani('clang_visitChildren',씨.c_uint,isikhombisi_inani,방문형,씨.c_void_p)
생성 = umsebenzi_inani('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = umsebenzi_inani('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = umsebenzi_inani('clang_getTranslationUnitCursor',isikhombisi_inani,씨.c_void_p)
끝내기 = umsebenzi_inani('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = umsebenzi_inani('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = umsebenzi_inani('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
isimo_esiyinkinga_inani = umsebenzi_inani('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = umsebenzi_inani('clang_getDiagnosticSpelling',uchunge_inani,씨.c_void_p)
진단해제 = umsebenzi_inani('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(okufakwayo_inani):
    Ihele = 씨.c_void_p(); umugqa = 씨.c_uint(); isikhala_okufakwayo = 씨.c_uint(); I_ofisethi_inani = 씨.c_uint()
    파일위치(위치얻기(okufakwayo_inani),씨.byref(Ihele),씨.byref(umugqa),씨.byref(isikhala_okufakwayo),씨.byref(I_ofisethi_inani))
    return (Itekisi(ifayela_okufakwayo_igama(Ihele)) if Ihele else '', I_ofisethi_inani.value, umugqa.value)

def yenza_umyalo():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Ukuhumusha_umthombo 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ulwazi_ngokwenzekile_imininingwane 빌드에서는 계속 컴파일한다.
    소유파일 = {str(Indlela_2.resolve()) for Indlela_2 in 기준.rglob('*') if Indlela_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(Indlela_2.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and Indlela_2.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'umsebenzisi'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'iNethiwekhi_Isitaki'),
          '-I'+str(기준/'kude_inani'),'-I'+str(기준/'시언어번역기')]
    for Indlela_2 in sorted(Path(Igama) for Igama in 소유파일 if Igama.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if Indlela_2.suffix=='.cpp' else '-std=c11']
        if 'iNethiwekhi_Isitaki' in Indlela_2.parts: 인수 += ['-I'+str(기준/'iNethiwekhi_Isitaki'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in Indlela_2.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in Indlela_2.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'kude_inani' in Indlela_2.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in Indlela_2.parts: 인수 += ['-D__JKOROS__=1']
        if Indlela_2.name=='isigaxa.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        iqoqo_inani = (씨.c_char_p*len(인수))(*[okufakwayo_inani.encode() for okufakwayo_inani in 인수])
        Ukuhumusha_isifundo = 분석(색인,str(Indlela_2).encode(),iqoqo_inani,len(인수),None,0,1)
        for thola_inkomba in range(진단수(Ukuhumusha_isifundo)):
            진단 = 진단얻기(Ukuhumusha_isifundo,thola_inkomba)
            if isimo_esiyinkinga_inani(진단)>=3: 오류들.append((str(Indlela_2.relative_to(기준)),Itekisi(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(okufakwayo_inani,부모,imininingwane):
            Ihele,I_ofisethi_inani,umugqa = 자리(okufakwayo_inani)
            if Ihele not in 소유파일: return 2 if okufakwayo_inani.종류==300 else 1
            낱말 = Itekisi(이름얻기(okufakwayo_inani))
            if not 낱말 or any(ord(uhlamvusimo_inani)>127 for uhlamvusimo_inani in 낱말): return 2
            if okufakwayo_inani.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                OKUHLUKILE_inani = Itekisi(OKUHLUKILE_igama(okufakwayo_inani)) or Ihele+':'+str(I_ofisethi_inani)
                선언들[OKUHLUKILE_inani] = {'Ihele':Ihele,'I_ofisethi_inani':I_ofisethi_inani,'줄':umugqa,'종류':okufakwayo_inani.종류,'Igama':낱말,'Xhumanisa':연결종류(okufakwayo_inani)}
                참조들.append((Ihele,I_ofisethi_inani,낱말,OKUHLUKILE_inani))
            else:
                Ireferensi = 참조얻기(okufakwayo_inani)
                Ireferensi_ifayela,_,_ = 자리(Ireferensi)
                if Ireferensi_ifayela in 소유파일:
                    OKUHLUKILE_inani = Itekisi(OKUHLUKILE_igama(Ireferensi)); 참조들.append((Ihele,I_ofisethi_inani,Itekisi(이름얻기(Ireferensi)),OKUHLUKILE_inani))
            return 2
        방문(뿌리(Ukuhumusha_isifundo),살피기,None)
        끝내기(Ukuhumusha_isifundo)
    isikhumulo_inani = 기준/'build/한국어화/시언어분석.json'
    isikhumulo_inani.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Ihele:hashlib.sha256(Path(Ihele).read_bytes()).hexdigest() for Ihele in sorted(소유파일)}
    isikhumulo_inani.write_text(json.dumps({'선언':선언들,'Ireferensi':참조들,'Iphutha':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Ireferensi',len(참조들),'Iphutha',len(오류들))
    for Iphutha in 오류들: print(*Iphutha)

if __name__=='__main__': yenza_umyalo()
