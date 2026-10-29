#!/usr/bin/env python3
"""libclang 선언·پايدىلانما 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

كۆرسىتىش_يىلتىز = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ھەرپ_تىزمىسى_قىممىتى(씨.Structure): _fields_ = [('مەلۇمات',씨.c_void_p),('كۆرسەتمەك_قىممىتى',씨.c_uint)]
class نۇربەلگە_قىممىتى(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('مەلۇمات',씨.c_void_p*3)]
class ئورۇن(씨.Structure): _fields_ = [('مەلۇمات',씨.c_void_p*2),('ئاغما_قىممىتى',씨.c_uint)]
def فۇنكسىيە_قىممىتى(ئاتى, قايتۇرۇپ_بېرىش_ئۆلچەم, *ئۆزگەرگۈچىلەر):
    كىرگۈزۈش_قىممىتى = getattr(구현, ئاتى); كىرگۈزۈش_قىممىتى.restype = قايتۇرۇپ_بېرىش_ئۆلچەم; كىرگۈزۈش_قىممىتى.argtypes = list(ئۆزگەرگۈچىلەر); return كىرگۈزۈش_قىممىتى
글얻기 = فۇنكسىيە_قىممىتى('clang_getCString',씨.c_char_p,ھەرپ_تىزمىسى_قىممىتى)
تارقىتىش_تېكست = فۇنكسىيە_قىممىتى('clang_disposeString',None,ھەرپ_تىزمىسى_قىممىتى)
def تېكىست(قىممىتى):
    ئۆلچەم = (글얻기(قىممىتى) or b'').decode('utf-8'); تارقىتىش_تېكست(قىممىتى); return ئۆلچەم
이름얻기 = فۇنكسىيە_قىممىتى('clang_getCursorSpelling',ھەرپ_تىزمىسى_قىممىتى,نۇربەلگە_قىممىتى)
참조얻기 = فۇنكسىيە_قىممىتى('clang_getCursorReferenced',نۇربەلگە_قىممىتى,نۇربەلگە_قىممىتى)
위치얻기 = فۇنكسىيە_قىممىتى('clang_getCursorLocation',ئورۇن,نۇربەلگە_قىممىتى)
ھۆججەت_ئورۇنلاشتۇرۇش = فۇنكسىيە_قىممىتى('clang_getFileLocation',None,ئورۇن,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ھۆججەت_كىرگۈزۈش_نامى = فۇنكسىيە_قىممىتى('clang_getFileName',ھەرپ_تىزمىسى_قىممىتى,씨.c_void_p)
고유이름 = فۇنكسىيە_قىممىتى('clang_getCursorUSR',ھەرپ_تىزمىسى_قىممىتى,نۇربەلگە_قىممىتى)
연결종류 = فۇنكسىيە_قىممىتى('clang_getCursorLinkage',씨.c_uint,نۇربەلگە_قىممىتى)
방문형 = 씨.CFUNCTYPE(씨.c_uint,نۇربەلگە_قىممىتى,نۇربەلگە_قىممىتى,씨.c_void_p)
방문 = فۇنكسىيە_قىممىتى('clang_visitChildren',씨.c_uint,نۇربەلگە_قىممىتى,방문형,씨.c_void_p)
ھاسىل_قىلىش = فۇنكسىيە_قىممىتى('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
ئانالىز_قىلماق_قىممىتى = فۇنكسىيە_قىممىتى('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
يىلتىز_قىممىتى = فۇنكسىيە_قىممىتى('clang_getTranslationUnitCursor',نۇربەلگە_قىممىتى,씨.c_void_p)
چېكىنىش_ئەپ = فۇنكسىيە_قىممىتى('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = فۇنكسىيە_قىممىتى('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = فۇنكسىيە_قىممىتى('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
جىددىيلىك_قىممىتى = فۇنكسىيە_قىممىتى('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = فۇنكسىيە_قىممىتى('clang_getDiagnosticSpelling',ھەرپ_تىزمىسى_قىممىتى,씨.c_void_p)
진단해제 = فۇنكسىيە_قىممىتى('clang_disposeDiagnostic',None,씨.c_void_p)

def ئورۇنلاشتۇرۇش_ئىندېكس(كىرگۈزۈش_قىممىتى):
    ھۆججەت = 씨.c_void_p(); قۇر = 씨.c_uint(); ئوقۇر_كىرگۈزۈش = 씨.c_uint(); ئاغما_قىممىتى = 씨.c_uint()
    ھۆججەت_ئورۇنلاشتۇرۇش(위치얻기(كىرگۈزۈش_قىممىتى),씨.byref(ھۆججەت),씨.byref(قۇر),씨.byref(ئوقۇر_كىرگۈزۈش),씨.byref(ئاغما_قىممىتى))
    return (تېكىست(ھۆججەت_كىرگۈزۈش_نامى(ھۆججەت)) if ھۆججەت else '', ئاغما_قىممىتى.value, قۇر.value)

def ئىجرا_قىلىش_بۇيرۇق():
    ئىزدەش_ئىندېكس = ھاسىل_قىلىش(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 تەرجىمە_مەنبە 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ھەقىقىي_مەلۇمات 빌드에서는 계속 컴파일한다.
    소유파일 = {str(يول.resolve()) for يول in كۆرسىتىش_يىلتىز.rglob('*') if يول.suffix in ('.c','.h','.cpp','.inc')
              and not set(يول.relative_to(كۆرسىتىش_يىلتىز).parts)&{'build','dist','vendor','__pycache__'}
              and يول.relative_to(كۆرسىتىش_يىلتىز).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(كۆرسىتىش_يىلتىز/'ئىشلەتكۈچى'),
          '-I'+str(كۆرسىتىش_يىلتىز.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(كۆرسىتىش_يىلتىز/'build'),'-I'+str(كۆرسىتىش_يىلتىز/'build/user'),
          '-I'+str(كۆرسىتىش_يىلتىز/'build/remote'),'-I'+str(كۆرسىتىش_يىلتىز/'vendor/bearssl/inc'),
          '-I'+str(كۆرسىتىش_يىلتىز/'vendor/bearssl/src'),'-I'+str(كۆرسىتىش_يىلتىز/'vendor/libassh/src'),
          '-I'+str(كۆرسىتىش_يىلتىز/'vendor/lwip/src/include'),'-I'+str(كۆرسىتىش_يىلتىز/'تور_دۆۋە'),
          '-I'+str(كۆرسىتىش_يىلتىز/'يىراق_قىممىتى'),'-I'+str(كۆرسىتىش_يىلتىز/'시언어번역기')]
    for يول in sorted(Path(ئاتى) for ئاتى in 소유파일 if ئاتى.endswith(('.c','.cpp'))):
        ئۆزگەرگۈچىلەر = 공통 + ['-std=c++11' if يول.suffix=='.cpp' else '-std=c11']
        if 'تور_دۆۋە' in يول.parts: ئۆزگەرگۈچىلەر += ['-I'+str(كۆرسىتىش_يىلتىز/'تور_دۆۋە'),'-I'+str(كۆرسىتىش_يىلتىز/'vendor/lwip/src/include')]
        if '시언어번역기' in يول.parts:
            ئۆزگەرگۈچىلەر += ['-I'+str(كۆرسىتىش_يىلتىز/'시언어번역기'),'-I'+str(كۆرسىتىش_يىلتىز/'vendor/tinycc'),'-I'+str(كۆرسىتىش_يىلتىز/'build/ccompiler'),
                    '-isystem',str(كۆرسىتىش_يىلتىز.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in يول.parts:
            ئۆزگەرگۈچىلەر += ['-I'+str(كۆرسىتىش_يىلتىز/'파이썬연결'),'-I'+str(كۆرسىتىش_يىلتىز/'build/micropython-1.24.1'),'-I'+str(كۆرسىتىش_يىلتىز/'build/python'),'-isystem','/usr/include/newlib']
        if 'يىراق_قىممىتى' in يول.parts:
            ئۆزگەرگۈچىلەر += ['-isystem', '/usr/include/newlib']
        if '배포' in يول.parts: ئۆزگەرگۈچىلەر += ['-D__JKOROS__=1']
        if يول.name=='توپلام.c': ئۆزگەرگۈچىلەر += ['-I'+str(كۆرسىتىش_يىلتىز/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        توپ_قىممىتى = (씨.c_char_p*len(ئۆزگەرگۈچىلەر))(*[كىرگۈزۈش_قىممىتى.encode() for كىرگۈزۈش_قىممىتى in ئۆزگەرگۈچىلەر])
        تەرجىمە_دەرس = ئانالىز_قىلماق_قىممىتى(ئىزدەش_ئىندېكس,str(يول).encode(),توپ_قىممىتى,len(ئۆزگەرگۈچىلەر),None,0,1)
        for ئىندېكس in range(진단수(تەرجىمە_دەرس)):
            진단 = 진단얻기(تەرجىمە_دەرس,ئىندېكس)
            if جىددىيلىك_قىممىتى(진단)>=3: 오류들.append((str(يول.relative_to(كۆرسىتىش_يىلتىز)),تېكىست(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(كىرگۈزۈش_قىممىتى,부모,مەلۇمات):
            ھۆججەت,ئاغما_قىممىتى,قۇر = ئورۇنلاشتۇرۇش_ئىندېكس(كىرگۈزۈش_قىممىتى)
            if ھۆججەت not in 소유파일: return 2 if كىرگۈزۈش_قىممىتى.종류==300 else 1
            낱말 = تېكىست(이름얻기(كىرگۈزۈش_قىممىتى))
            if not 낱말 or any(ord(ھەرپ_بەلگە_قىممىتى)>127 for ھەرپ_بەلگە_قىممىتى in 낱말): return 2
            if كىرگۈزۈش_قىممىتى.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = تېكىست(고유이름(كىرگۈزۈش_قىممىتى)) or ھۆججەت+':'+str(ئاغما_قىممىتى)
                선언들[고유] = {'ھۆججەت':ھۆججەت,'ئاغما_قىممىتى':ئاغما_قىممىتى,'قۇر':قۇر,'종류':كىرگۈزۈش_قىممىتى.종류,'ئاتى':낱말,'ئۇلا':연결종류(كىرگۈزۈش_قىممىتى)}
                참조들.append((ھۆججەت,ئاغما_قىممىتى,낱말,고유))
            else:
                پايدىلانما = 참조얻기(كىرگۈزۈش_قىممىتى)
                پايدىلانما_ھۆججەت,_,_ = ئورۇنلاشتۇرۇش_ئىندېكس(پايدىلانما)
                if پايدىلانما_ھۆججەت in 소유파일:
                    고유 = تېكىست(고유이름(پايدىلانما)); 참조들.append((ھۆججەت,ئاغما_قىممىتى,تېكىست(이름얻기(پايدىلانما)),고유))
            return 2
        방문(يىلتىز_قىممىتى(تەرجىمە_دەرس),살피기,None)
        چېكىنىش_ئەپ(تەرجىمە_دەرس)
    نىشان_قىممىتى = كۆرسىتىش_يىلتىز/'build/한국어화/시언어분석.json'
    نىشان_قىممىتى.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ھۆججەت:hashlib.sha256(Path(ھۆججەت).read_bytes()).hexdigest() for ھۆججەت in sorted(소유파일)}
    نىشان_قىممىتى.write_text(json.dumps({'선언':선언들,'پايدىلانما':참조들,'خاتالىق':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'پايدىلانما',len(참조들),'خاتالىق',len(오류들))
    for خاتالىق in 오류들: print(*خاتالىق)

if __name__=='__main__': ئىجرا_قىلىش_بۇيرۇق()
