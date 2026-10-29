#!/usr/bin/env python3
"""libclang 선언·පරිශීලනය 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class අනුලකුණු_වැල_අගය(씨.Structure): _fields_ = [('දත්ත',씨.c_void_p),('දර්ශනය_අගය',씨.c_uint)]
class කර්සරය_අගය(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('දත්ත',씨.c_void_p*3)]
class පිහිටීම(씨.Structure): _fields_ = [('දත්ත',씨.c_void_p*2),('ඕෆ්සෙට්_අගය',씨.c_uint)]
def ශ්_රිතය_අගය(නම, 반환, *විස්තාරක):
    පිවිසුම_අගය = getattr(구현, නම); පිවිසුම_අගය.restype = 반환; පිවිසුම_අගය.argtypes = list(විස්තාරක); return පිවිසුම_අගය
글얻기 = ශ්_රිතය_අගය('clang_getCString',씨.c_char_p,අනුලකුණු_වැල_අගය)
මුදාහැරීම_පෙළ = ශ්_රිතය_අගය('clang_disposeString',None,අනුලකුණු_වැල_අගය)
def පෙළ(අගය):
    결과 = (글얻기(අගය) or b'').decode('utf-8'); මුදාහැරීම_පෙළ(අගය); return 결과
이름얻기 = ශ්_රිතය_අගය('clang_getCursorSpelling',අනුලකුණු_වැල_අගය,කර්සරය_අගය)
참조얻기 = ශ්_රිතය_අගය('clang_getCursorReferenced',කර්සරය_අගය,කර්සරය_අගය)
위치얻기 = ශ්_රිතය_අගය('clang_getCursorLocation',පිහිටීම,කර්සරය_අගය)
파일위치 = ශ්_රිතය_අගය('clang_getFileLocation',None,පිහිටීම,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ගොනුව_පිවිසුම_නම = ශ්_රිතය_අගය('clang_getFileName',අනුලකුණු_වැල_අගය,씨.c_void_p)
අනන්_ය_නම = ශ්_රිතය_අගය('clang_getCursorUSR',අනුලකුණු_වැල_අගය,කර්සරය_අගය)
연결종류 = ශ්_රිතය_අගය('clang_getCursorLinkage',씨.c_uint,කර්සරය_අගය)
방문형 = 씨.CFUNCTYPE(씨.c_uint,කර්සරය_අගය,කර්සරය_අගය,씨.c_void_p)
방문 = ශ්_රිතය_අගය('clang_visitChildren',씨.c_uint,කර්සරය_අගය,방문형,씨.c_void_p)
생성 = ශ්_රිතය_අගය('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ශ්_රිතය_අගය('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = ශ්_රිතය_අගය('clang_getTranslationUnitCursor',කර්සරය_අගය,씨.c_void_p)
끝내기 = ශ්_රිතය_අගය('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ශ්_රිතය_අගය('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ශ්_රිතය_අගය('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ප්_රබලතාව_අගය = ශ්_රිතය_අගය('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ශ්_රිතය_අගය('clang_getDiagnosticSpelling',අනුලකුණු_වැල_අගය,씨.c_void_p)
진단해제 = ශ්_රිතය_අගය('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(පිවිසුම_අගය):
    ගොනු = 씨.c_void_p(); පේළිය = 씨.c_uint(); විවරය_පිවිසුම = 씨.c_uint(); ඕෆ්සෙට්_අගය = 씨.c_uint()
    파일위치(위치얻기(පිවිසුම_අගය),씨.byref(ගොනු),씨.byref(පේළිය),씨.byref(විවරය_පිවිසුම),씨.byref(ඕෆ්සෙට්_අගය))
    return (පෙළ(ගොනුව_පිවිසුම_නම(ගොනු)) if ගොනු else '', ඕෆ්සෙට්_අගය.value, පේළිය.value)

def ක්_රියාත්මක_කරන්න_විධානය():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 පරිවර්තනය_මූලය 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, තථ්_ය_දත්ත 빌드에서는 계속 컴파일한다.
    소유파일 = {str(මාර්_ගය.resolve()) for මාර්_ගය in 기준.rglob('*') if මාර්_ගය.suffix in ('.c','.h','.cpp','.inc')
              and not set(මාර්_ගය.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and මාර්_ගය.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'පරිශීලක'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'ජාලය_කැටිය'),
          '-I'+str(기준/'දුරස්ථ_අගය'),'-I'+str(기준/'시언어번역기')]
    for මාර්_ගය in sorted(Path(නම) for නම in 소유파일 if නම.endswith(('.c','.cpp'))):
        විස්තාරක = 공통 + ['-std=c++11' if මාර්_ගය.suffix=='.cpp' else '-std=c11']
        if 'ජාලය_කැටිය' in මාර්_ගය.parts: විස්තාරක += ['-I'+str(기준/'ජාලය_කැටිය'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in මාර්_ගය.parts:
            විස්තාරක += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in මාර්_ගය.parts:
            විස්තාරක += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'දුරස්ථ_අගය' in මාර්_ගය.parts:
            විස්තාරක += ['-isystem', '/usr/include/newlib']
        if '배포' in මාර්_ගය.parts: විස්තාරක += ['-D__JKOROS__=1']
        if මාර්_ගය.name=='පොදිය.c': විස්තාරක += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        සමූහය_අගය = (씨.c_char_p*len(විස්තාරක))(*[පිවිසුම_අගය.encode() for පිවිසුම_අගය in විස්තාරක])
        පරිවර්තනය_ඒකක = 분석(색인,str(මාර්_ගය).encode(),සමූහය_අගය,len(විස්තාරක),None,0,1)
        for සූචිය in range(진단수(පරිවර්තනය_ඒකක)):
            진단 = 진단얻기(පරිවර්තනය_ඒකක,සූචිය)
            if ප්_රබලතාව_අගය(진단)>=3: 오류들.append((str(මාර්_ගය.relative_to(기준)),පෙළ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(පිවිසුම_අගය,부모,දත්ත):
            ගොනු,ඕෆ්සෙට්_අගය,පේළිය = 자리(පිවිසුම_අගය)
            if ගොනු not in 소유파일: return 2 if පිවිසුම_අගය.종류==300 else 1
            낱말 = පෙළ(이름얻기(පිවිසුම_අගය))
            if not 낱말 or any(ord(අනුලකුණ_අගය)>127 for අනුලකුණ_අගය in 낱말): return 2
            if පිවිසුම_අගය.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                අනන්_ය_අගය = පෙළ(අනන්_ය_නම(පිවිසුම_අගය)) or ගොනු+':'+str(ඕෆ්සෙට්_අගය)
                선언들[අනන්_ය_අගය] = {'ගොනු':ගොනු,'ඕෆ්සෙට්_අගය':ඕෆ්සෙට්_අගය,'줄':පේළිය,'종류':පිවිසුම_අගය.종류,'නම':낱말,'සම්බන්ද_වන්න':연결종류(පිවිසුම_අගය)}
                참조들.append((ගොනු,ඕෆ්සෙට්_අගය,낱말,අනන්_ය_අගය))
            else:
                පරිශීලනය = 참조얻기(පිවිසුම_අගය)
                පරිශීලනය_ගොනුව,_,_ = 자리(පරිශීලනය)
                if පරිශීලනය_ගොනුව in 소유파일:
                    අනන්_ය_අගය = පෙළ(අනන්_ය_නම(පරිශීලනය)); 참조들.append((ගොනු,ඕෆ්සෙට්_අගය,පෙළ(이름얻기(පරිශීලනය)),අනන්_ය_අගය))
            return 2
        방문(뿌리(පරිවර්තනය_ඒකක),살피기,None)
        끝내기(පරිවර්තනය_ඒකක)
    ගමනාන්තය_අගය = 기준/'build/한국어화/시언어분석.json'
    ගමනාන්තය_අගය.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ගොනු:hashlib.sha256(Path(ගොනු).read_bytes()).hexdigest() for ගොනු in sorted(소유파일)}
    ගමනාන්තය_අගය.write_text(json.dumps({'선언':선언들,'පරිශීලනය':참조들,'දෝෂය':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'පරිශීලනය',len(참조들),'දෝෂය',len(오류들))
    for දෝෂය in 오류들: print(*දෝෂය)

if __name__=='__main__': ක්_රියාත්මක_කරන්න_විධානය()
