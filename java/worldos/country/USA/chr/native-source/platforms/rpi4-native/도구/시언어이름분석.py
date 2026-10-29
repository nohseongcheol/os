#!/usr/bin/env python3
"""libclang 선언·참조 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ(씨.Structure): _fields_ = [('ᎦᏟᏌᏅᎯ',씨.c_void_p),('ᏍᎩᎪᏩᏛᏓ_ᏧᎬᏩᎶᏗᏯ',씨.c_uint)]
class ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ᎦᏟᏌᏅᎯ',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('ᎦᏟᏌᏅᎯ',씨.c_void_p*2),('변위',씨.c_uint)]
def ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ(ᏚᏙᎥᎢ, 반환, *인수):
    Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ = getattr(구현, ᏚᏙᎥᎢ); Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.restype = 반환; Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.argtypes = list(인수); return Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ
글얻기 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getCString',씨.c_char_p,ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ)
글해제 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_disposeString',None,ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ)
def ᎠᎪᎵᏰᏗ(ᏧᎬᏩᎶᏗᏯ):
    결과 = (글얻기(ᏧᎬᏩᎶᏗᏯ) or b'').decode('utf-8'); 글해제(ᏧᎬᏩᎶᏗᏯ); return 결과
이름얻기 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getCursorSpelling',ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
참조얻기 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getCursorReferenced',ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
위치얻기 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getCursorLocation',위치,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
파일위치 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getFileName',ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ,씨.c_void_p)
고유이름 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getCursorUSR',ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
연결종류 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getCursorLinkage',씨.c_uint,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ,씨.c_void_p)
방문 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_visitChildren',씨.c_uint,ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ,방문형,씨.c_void_p)
생성 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getTranslationUnitCursor',ᎥᎪᏪᎵᏍᎬ_ᎠᎴᏅᏙᏗ_ᏧᎬᏩᎶᏗᏯ,씨.c_void_p)
끝내기 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ᎤᏍᎦᏎᏛ_ᏗᎳᏏᏅᏍᏗ_ᏧᎬᏩᎶᏗᏯ = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_getDiagnosticSpelling',ᎠᏍᏘ_ᏧᎬᏩᎶᏗᏯ,씨.c_void_p)
진단해제 = ᏧᎸᏫᏍᏓᏁᏗᏱ_ᏧᎬᏩᎶᏗᏯ('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ):
    ᎠᏍᏆᏂᎪᏙᏗ = 씨.c_void_p(); ᏚᏓᏅᏅᎢ = 씨.c_uint(); 칸 = 씨.c_uint(); 변위 = 씨.c_uint()
    파일위치(위치얻기(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ),씨.byref(ᎠᏍᏆᏂᎪᏙᏗ),씨.byref(ᏚᏓᏅᏅᎢ),씨.byref(칸),씨.byref(변위))
    return (ᎠᎪᎵᏰᏗ(ᎠᏍᏆᏂᎪᏙᏗ_Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏚᏙᎥᎢ(ᎠᏍᏆᏂᎪᏙᏗ)) if ᎠᏍᏆᏂᎪᏙᏗ else '', 변위.value, ᏚᏓᏅᏅᎢ.value)

def ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 번역 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ᎤᏙᎯᏳ_ᎾᏍᎩ_ᎨᏒ_ᎦᏟᏌᏅᎯ 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ᎠᏍᏓᏩᏛᏍᏗ.resolve()) for ᎠᏍᏓᏩᏛᏍᏗ in 기준.rglob('*') if ᎠᏍᏓᏩᏛᏍᏗ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ᎠᏍᏓᏩᏛᏍᏗ.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and ᎠᏍᏓᏩᏛᏍᏗ.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'ᎬᏗᏍᎩ'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'통신망'),
          '-I'+str(기준/'원격'),'-I'+str(기준/'시언어번역기')]
    for ᎠᏍᏓᏩᏛᏍᏗ in sorted(Path(ᏚᏙᎥᎢ) for ᏚᏙᎥᎢ in 소유파일 if ᏚᏙᎥᎢ.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ᎠᏍᏓᏩᏛᏍᏗ.suffix=='.cpp' else '-std=c11']
        if '통신망' in ᎠᏍᏓᏩᏛᏍᏗ.parts: 인수 += ['-I'+str(기준/'통신망'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in ᎠᏍᏓᏩᏛᏍᏗ.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ᎠᏍᏓᏩᏛᏍᏗ.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if '원격' in ᎠᏍᏓᏩᏛᏍᏗ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ᎠᏍᏓᏩᏛᏍᏗ.parts: 인수 += ['-D__JKOROS__=1']
        if ᎠᏍᏓᏩᏛᏍᏗ.name=='ᎦᏇᏅᎯ.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ = (씨.c_char_p*len(인수))(*[Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.encode() for Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ in 인수])
        번역단위 = 분석(색인,str(ᎠᏍᏓᏩᏛᏍᏗ).encode(),ᎤᎾᏓᏡᎬᎢ_ᏧᎬᏩᎶᏗᏯ,len(인수),None,0,1)
        for ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ in range(진단수(번역단위)):
            진단 = 진단얻기(번역단위,ᏂᎬᎿᏅ_ᎠᏓᏎᎮᎯ)
            if ᎤᏍᎦᏎᏛ_ᏗᎳᏏᏅᏍᏗ_ᏧᎬᏩᎶᏗᏯ(진단)>=3: 오류들.append((str(ᎠᏍᏓᏩᏛᏍᏗ.relative_to(기준)),ᎠᎪᎵᏰᏗ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ,부모,ᎦᏟᏌᏅᎯ):
            ᎠᏍᏆᏂᎪᏙᏗ,변위,ᏚᏓᏅᏅᎢ = 자리(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
            if ᎠᏍᏆᏂᎪᏙᏗ not in 소유파일: return 2 if Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.종류==300 else 1
            낱말 = ᎠᎪᎵᏰᏗ(이름얻기(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ))
            if not 낱말 or any(ord(ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ)>127 for ᎪᏪᎸ_ᏧᎬᏩᎶᏗᏯ in 낱말): return 2
            if Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ᎠᎪᎵᏰᏗ(고유이름(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)) or ᎠᏍᏆᏂᎪᏙᏗ+':'+str(변위)
                선언들[고유] = {'ᎠᏍᏆᏂᎪᏙᏗ':ᎠᏍᏆᏂᎪᏙᏗ,'변위':변위,'줄':ᏚᏓᏅᏅᎢ,'종류':Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ.종류,'ᏚᏙᎥᎢ':낱말,'ᎫᏓᎳ':연결종류(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)}
                참조들.append((ᎠᏍᏆᏂᎪᏙᏗ,변위,낱말,고유))
            else:
                참조 = 참조얻기(Ꭵ_ᎧᏁᏉᎢᏍᏙᏗ_ᏧᎬᏩᎶᏗᏯ)
                참조파일,_,_ = 자리(참조)
                if 참조파일 in 소유파일:
                    고유 = ᎠᎪᎵᏰᏗ(고유이름(참조)); 참조들.append((ᎠᏍᏆᏂᎪᏙᏗ,변위,ᎠᎪᎵᏰᏗ(이름얻기(참조)),고유))
            return 2
        방문(뿌리(번역단위),살피기,None)
        끝내기(번역단위)
    ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ = 기준/'build/한국어화/시언어분석.json'
    ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ᎠᏍᏆᏂᎪᏙᏗ:hashlib.sha256(Path(ᎠᏍᏆᏂᎪᏙᏗ).read_bytes()).hexdigest() for ᎠᏍᏆᏂᎪᏙᏗ in sorted(소유파일)}
    ᏮᎦᏛᎢ_ᏧᎬᏩᎶᏗᏯ.write_text(json.dumps({'선언':선언들,'참조':참조들,'ᎦᎵᏓᏍᏔᏅ':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'참조',len(참조들),'ᎦᎵᏓᏍᏔᏅ',len(오류들))
    for ᎦᎵᏓᏍᏔᏅ in 오류들: print(*ᎦᎵᏓᏍᏔᏅ)

if __name__=='__main__': ᎠᎴᏅᏗᏱ_ᎤᏁᏤᎸᎩ()
