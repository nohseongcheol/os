#!/usr/bin/env python3
"""libclang 선언·Ìtọ́ka 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class fọ́nrán_iye(씨.Structure): _fields_ = [('détà',씨.c_void_p),('ṣàfihàn_iye',씨.c_uint)]
class kọ́sọ̀_iye(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('détà',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('détà',씨.c_void_p*2),('Ìtayọ_iye',씨.c_uint)]
def ÀKÀNṢEFỌMÚLÀ_iye(Orúkọ, 반환, *인수):
    ìgbéwọlé_iye = getattr(구현, Orúkọ); ìgbéwọlé_iye.restype = 반환; ìgbéwọlé_iye.argtypes = list(인수); return ìgbéwọlé_iye
글얻기 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getCString',씨.c_char_p,fọ́nrán_iye)
dápadà_SMS = ÀKÀNṢEFỌMÚLÀ_iye('clang_disposeString',None,fọ́nrán_iye)
def SMS(iye):
    결과 = (글얻기(iye) or b'').decode('utf-8'); dápadà_SMS(iye); return 결과
이름얻기 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getCursorSpelling',fọ́nrán_iye,kọ́sọ̀_iye)
참조얻기 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getCursorReferenced',kọ́sọ̀_iye,kọ́sọ̀_iye)
위치얻기 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getCursorLocation',위치,kọ́sọ̀_iye)
파일위치 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
fáìlì_ìgbéwọlé_orúkọ = ÀKÀNṢEFỌMÚLÀ_iye('clang_getFileName',fọ́nrán_iye,씨.c_void_p)
Ọ̀TỌ̀_orúkọ = ÀKÀNṢEFỌMÚLÀ_iye('clang_getCursorUSR',fọ́nrán_iye,kọ́sọ̀_iye)
연결종류 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getCursorLinkage',씨.c_uint,kọ́sọ̀_iye)
방문형 = 씨.CFUNCTYPE(씨.c_uint,kọ́sọ̀_iye,kọ́sọ̀_iye,씨.c_void_p)
방문 = ÀKÀNṢEFỌMÚLÀ_iye('clang_visitChildren',씨.c_uint,kọ́sọ̀_iye,방문형,씨.c_void_p)
생성 = ÀKÀNṢEFỌMÚLÀ_iye('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ÀKÀNṢEFỌMÚLÀ_iye('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getTranslationUnitCursor',kọ́sọ̀_iye,씨.c_void_p)
끝내기 = ÀKÀNṢEFỌMÚLÀ_iye('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
Ìwọ̀n_iye = ÀKÀNṢEFỌMÚLÀ_iye('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ÀKÀNṢEFỌMÚLÀ_iye('clang_getDiagnosticSpelling',fọ́nrán_iye,씨.c_void_p)
진단해제 = ÀKÀNṢEFỌMÚLÀ_iye('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(ìgbéwọlé_iye):
    Fáìlì = 씨.c_void_p(); ìlà = 씨.c_uint(); ààyè_ìfàyọkàsí_ìgbéwọlé = 씨.c_uint(); Ìtayọ_iye = 씨.c_uint()
    파일위치(위치얻기(ìgbéwọlé_iye),씨.byref(Fáìlì),씨.byref(ìlà),씨.byref(ààyè_ìfàyọkàsí_ìgbéwọlé),씨.byref(Ìtayọ_iye))
    return (SMS(fáìlì_ìgbéwọlé_orúkọ(Fáìlì)) if Fáìlì else '', Ìtayọ_iye.value, ìlà.value)

def ṣiṣẹ́_àṣẹ():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 Aṣàtúmọ̀_èdè_orísun 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, gangan_détà 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ọ̀nà.resolve()) for ọ̀nà in 기준.rglob('*') if ọ̀nà.suffix in ('.c','.h','.cpp','.inc')
              and not set(ọ̀nà.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and ọ̀nà.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'aṣàmúlò'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'Alásopọ̀_kójọ'),
          '-I'+str(기준/'Ìjìnnà_iye'),'-I'+str(기준/'시언어번역기')]
    for ọ̀nà in sorted(Path(Orúkọ) for Orúkọ in 소유파일 if Orúkọ.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ọ̀nà.suffix=='.cpp' else '-std=c11']
        if 'Alásopọ̀_kójọ' in ọ̀nà.parts: 인수 += ['-I'+str(기준/'Alásopọ̀_kójọ'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in ọ̀nà.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ọ̀nà.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'Ìjìnnà_iye' in ọ̀nà.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ọ̀nà.parts: 인수 += ['-D__JKOROS__=1']
        if ọ̀nà.name=='àkópọ̀.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        Àjọṣe_iye = (씨.c_char_p*len(인수))(*[ìgbéwọlé_iye.encode() for ìgbéwọlé_iye in 인수])
        Ìtumọ̀_ìkẹ́kọ̀ọ́ = 분석(색인,str(ọ̀nà).encode(),Àjọṣe_iye,len(인수),None,0,1)
        for wá_atọ̀ka_àkóónú in range(진단수(Ìtumọ̀_ìkẹ́kọ̀ọ́)):
            진단 = 진단얻기(Ìtumọ̀_ìkẹ́kọ̀ọ́,wá_atọ̀ka_àkóónú)
            if Ìwọ̀n_iye(진단)>=3: 오류들.append((str(ọ̀nà.relative_to(기준)),SMS(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ìgbéwọlé_iye,부모,détà):
            Fáìlì,Ìtayọ_iye,ìlà = 자리(ìgbéwọlé_iye)
            if Fáìlì not in 소유파일: return 2 if ìgbéwọlé_iye.종류==300 else 1
            낱말 = SMS(이름얻기(ìgbéwọlé_iye))
            if not 낱말 or any(ord(ẹyọ_ọ̀rọ̀_iye)>127 for ẹyọ_ọ̀rọ̀_iye in 낱말): return 2
            if ìgbéwọlé_iye.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                Ọ̀TỌ̀_iye = SMS(Ọ̀TỌ̀_orúkọ(ìgbéwọlé_iye)) or Fáìlì+':'+str(Ìtayọ_iye)
                선언들[Ọ̀TỌ̀_iye] = {'Fáìlì':Fáìlì,'Ìtayọ_iye':Ìtayọ_iye,'줄':ìlà,'종류':ìgbéwọlé_iye.종류,'Orúkọ':낱말,'Darapọ̀':연결종류(ìgbéwọlé_iye)}
                참조들.append((Fáìlì,Ìtayọ_iye,낱말,Ọ̀TỌ̀_iye))
            else:
                Ìtọ́ka = 참조얻기(ìgbéwọlé_iye)
                Ìtọ́ka_fáìlì,_,_ = 자리(Ìtọ́ka)
                if Ìtọ́ka_fáìlì in 소유파일:
                    Ọ̀TỌ̀_iye = SMS(Ọ̀TỌ̀_orúkọ(Ìtọ́ka)); 참조들.append((Fáìlì,Ìtayọ_iye,SMS(이름얻기(Ìtọ́ka)),Ọ̀TỌ̀_iye))
            return 2
        방문(뿌리(Ìtumọ̀_ìkẹ́kọ̀ọ́),살피기,None)
        끝내기(Ìtumọ̀_ìkẹ́kọ̀ọ́)
    èbúté_iye = 기준/'build/한국어화/시언어분석.json'
    èbúté_iye.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {Fáìlì:hashlib.sha256(Path(Fáìlì).read_bytes()).hexdigest() for Fáìlì in sorted(소유파일)}
    èbúté_iye.write_text(json.dumps({'선언':선언들,'Ìtọ́ka':참조들,'àṣìṣe':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'Ìtọ́ka',len(참조들),'àṣìṣe',len(오류들))
    for àṣìṣe in 오류들: print(*àṣìṣe)

if __name__=='__main__': ṣiṣẹ́_àṣẹ()
