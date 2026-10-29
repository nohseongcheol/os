#!/usr/bin/env python3
"""libclang 선언·참조 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class qimiaq_atuutilik(씨.Structure): _fields_ = [('titiqqat',씨.c_void_p),('saqqilli_atuutilik',씨.c_uint)]
class pigiarut_atuutilik(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('titiqqat',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('titiqqat',씨.c_void_p*2),('변위',씨.c_uint)]
def sugiakkannirut_atuutilik(atiq, 반환, *인수):
    Iliniku_atuutilik = getattr(구현, atiq); Iliniku_atuutilik.restype = 반환; Iliniku_atuutilik.argtypes = list(인수); return Iliniku_atuutilik
글얻기 = sugiakkannirut_atuutilik('clang_getCString',씨.c_char_p,qimiaq_atuutilik)
anititaujuq_titiqqaq = sugiakkannirut_atuutilik('clang_disposeString',None,qimiaq_atuutilik)
def titiqqaq(atuutilik):
    결과 = (글얻기(atuutilik) or b'').decode('utf-8'); anititaujuq_titiqqaq(atuutilik); return 결과
이름얻기 = sugiakkannirut_atuutilik('clang_getCursorSpelling',qimiaq_atuutilik,pigiarut_atuutilik)
참조얻기 = sugiakkannirut_atuutilik('clang_getCursorReferenced',pigiarut_atuutilik,pigiarut_atuutilik)
위치얻기 = sugiakkannirut_atuutilik('clang_getCursorLocation',위치,pigiarut_atuutilik)
파일위치 = sugiakkannirut_atuutilik('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ini_Iliniku_atiq = sugiakkannirut_atuutilik('clang_getFileName',qimiaq_atuutilik,씨.c_void_p)
고유이름 = sugiakkannirut_atuutilik('clang_getCursorUSR',qimiaq_atuutilik,pigiarut_atuutilik)
연결종류 = sugiakkannirut_atuutilik('clang_getCursorLinkage',씨.c_uint,pigiarut_atuutilik)
방문형 = 씨.CFUNCTYPE(씨.c_uint,pigiarut_atuutilik,pigiarut_atuutilik,씨.c_void_p)
방문 = sugiakkannirut_atuutilik('clang_visitChildren',씨.c_uint,pigiarut_atuutilik,방문형,씨.c_void_p)
생성 = sugiakkannirut_atuutilik('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = sugiakkannirut_atuutilik('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = sugiakkannirut_atuutilik('clang_getTranslationUnitCursor',pigiarut_atuutilik,씨.c_void_p)
끝내기 = sugiakkannirut_atuutilik('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = sugiakkannirut_atuutilik('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = sugiakkannirut_atuutilik('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
assualuurninga_atuutilik = sugiakkannirut_atuutilik('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = sugiakkannirut_atuutilik('clang_getDiagnosticSpelling',qimiaq_atuutilik,씨.c_void_p)
진단해제 = sugiakkannirut_atuutilik('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(Iliniku_atuutilik):
    ini = 씨.c_void_p(); titikutaak = 씨.c_uint(); 칸 = 씨.c_uint(); 변위 = 씨.c_uint()
    파일위치(위치얻기(Iliniku_atuutilik),씨.byref(ini),씨.byref(titikutaak),씨.byref(칸),씨.byref(변위))
    return (titiqqaq(ini_Iliniku_atiq(ini)) if ini else '', 변위.value, titikutaak.value)

def 실행():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 번역 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, taannallarik_titiqqat 빌드에서는 계속 컴파일한다.
    소유파일 = {str(aqqut.resolve()) for aqqut in 기준.rglob('*') if aqqut.suffix in ('.c','.h','.cpp','.inc')
              and not set(aqqut.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and aqqut.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'atuqtuq'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'통신망'),
          '-I'+str(기준/'ungasittuq_atuutilik'),'-I'+str(기준/'시언어번역기')]
    for aqqut in sorted(Path(atiq) for atiq in 소유파일 if atiq.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if aqqut.suffix=='.cpp' else '-std=c11']
        if '통신망' in aqqut.parts: 인수 += ['-I'+str(기준/'통신망'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in aqqut.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in aqqut.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'ungasittuq_atuutilik' in aqqut.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in aqqut.parts: 인수 += ['-D__JKOROS__=1']
        if aqqut.name=='꾸러미.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        katinngajut_atuutilik = (씨.c_char_p*len(인수))(*[Iliniku_atuutilik.encode() for Iliniku_atuutilik in 인수])
        번역단위 = 분석(색인,str(aqqut).encode(),katinngajut_atuutilik,len(인수),None,0,1)
        for nalunaiqsimavik in range(진단수(번역단위)):
            진단 = 진단얻기(번역단위,nalunaiqsimavik)
            if assualuurninga_atuutilik(진단)>=3: 오류들.append((str(aqqut.relative_to(기준)),titiqqaq(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(Iliniku_atuutilik,부모,titiqqat):
            ini,변위,titikutaak = 자리(Iliniku_atuutilik)
            if ini not in 소유파일: return 2 if Iliniku_atuutilik.종류==300 else 1
            낱말 = titiqqaq(이름얻기(Iliniku_atuutilik))
            if not 낱말 or any(ord(immikkuuqtuq_atuutilik)>127 for immikkuuqtuq_atuutilik in 낱말): return 2
            if Iliniku_atuutilik.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = titiqqaq(고유이름(Iliniku_atuutilik)) or ini+':'+str(변위)
                선언들[고유] = {'ini':ini,'변위':변위,'줄':titikutaak,'종류':Iliniku_atuutilik.종류,'atiq':낱말,'kasurli':연결종류(Iliniku_atuutilik)}
                참조들.append((ini,변위,낱말,고유))
            else:
                참조 = 참조얻기(Iliniku_atuutilik)
                참조파일,_,_ = 자리(참조)
                if 참조파일 in 소유파일:
                    고유 = titiqqaq(고유이름(참조)); 참조들.append((ini,변위,titiqqaq(이름얻기(참조)),고유))
            return 2
        방문(뿌리(번역단위),살피기,None)
        끝내기(번역단위)
    namunngarvik_atuutilik = 기준/'build/한국어화/시언어분석.json'
    namunngarvik_atuutilik.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ini:hashlib.sha256(Path(ini).read_bytes()).hexdigest() for ini in sorted(소유파일)}
    namunngarvik_atuutilik.write_text(json.dumps({'선언':선언들,'참조':참조들,'tammarniq':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'참조',len(참조들),'tammarniq',len(오류들))
    for tammarniq in 오류들: print(*tammarniq)

if __name__=='__main__': 실행()
