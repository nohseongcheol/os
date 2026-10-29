#!/usr/bin/env python3
"""libclang 선언·ପ୍ରସଙ୍ଗ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ(씨.Structure): _fields_ = [('ଡାଟା',씨.c_void_p),('ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ',씨.c_uint)]
class କରସର୍_ମୂଲ୍ୟ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ଡାଟା',씨.c_void_p*3)]
class ଅବସ୍ଥାନ(씨.Structure): _fields_ = [('ଡାଟା',씨.c_void_p*2),('ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ',씨.c_uint)]
def Excel_ଟେବଲ୍_ମୂଲ୍ୟ(ନାମ, 반환, *인수):
    ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ = getattr(구현, ନାମ); ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.restype = 반환; ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.argtypes = list(인수); return ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ
글얻기 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getCString',씨.c_char_p,ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ)
ରିଲିଜ୍_ପାଠ = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_disposeString',None,ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ)
def ପାଠ୍ଯ(ମୂଲ୍ୟ):
    ମାପ = (글얻기(ମୂଲ୍ୟ) or b'').decode('utf-8'); ରିଲିଜ୍_ପାଠ(ମୂଲ୍ୟ); return ମାପ
이름얻기 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getCursorSpelling',ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ,କରସର୍_ମୂଲ୍ୟ)
참조얻기 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getCursorReferenced',କରସର୍_ମୂଲ୍ୟ,କରସର୍_ମୂଲ୍ୟ)
위치얻기 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getCursorLocation',ଅବସ୍ଥାନ,କରସର୍_ମୂଲ୍ୟ)
ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getFileLocation',None,ଅବସ୍ଥାନ,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getFileName',ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ,씨.c_void_p)
고유이름 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getCursorUSR',ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ,କରସର୍_ମୂଲ୍ୟ)
연결종류 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getCursorLinkage',씨.c_uint,କରସର୍_ମୂଲ୍ୟ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,କରସର୍_ମୂଲ୍ୟ,କରସର୍_ମୂଲ୍ୟ,씨.c_void_p)
방문 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_visitChildren',씨.c_uint,କରସର୍_ମୂଲ୍ୟ,방문형,씨.c_void_p)
ସୃଷ୍ଟି_କରିବା = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ରୁଟ୍_ମୂଲ୍ୟ = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getTranslationUnitCursor',କରସର୍_ମୂଲ୍ୟ,씨.c_void_p)
ଛାଡିବା_ଅନୁପ୍ରୟୋଗ = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ସୁରକ୍ଷା_ମୂଲ୍ୟ = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_getDiagnosticSpelling',ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ,씨.c_void_p)
진단해제 = Excel_ଟେବଲ୍_ମୂଲ୍ୟ('clang_disposeDiagnostic',None,씨.c_void_p)

def ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ):
    ଫାଇଲ = 씨.c_void_p(); ରେଖା = 씨.c_uint(); ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି = 씨.c_uint(); ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ = 씨.c_uint()
    ଫାଇଲ୍_ସ୍ଥିତି_2aa21a9a(위치얻기(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ),씨.byref(ଫାଇଲ),씨.byref(ରେଖା),씨.byref(ସ୍ଲଟ୍_ଏଣ୍ଟ୍ରି),씨.byref(ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ))
    return (ପାଠ୍ଯ(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି_ନାମ(ଫାଇଲ)) if ଫାଇଲ else '', ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ.value, ରେଖା.value)

def ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ():
    ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା = ସୃଷ୍ଟି_କରିବା(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 ଅନୁବାଦ_ଉତ୍ସ 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ପ୍ରକୃତ_ଡାଟା 빌드에서는 계속 컴파일한다.
    소유파일 = {str(ପଥ.resolve()) for ପଥ in ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.rglob('*') if ପଥ.suffix in ('.c','.h','.cpp','.inc')
              and not set(ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍).parts)&{'build','dist','vendor','__pycache__'}
              and ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଉପଭୋକ୍ତା'),
          '-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/user'),
          '-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/remote'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'vendor/bearssl/inc'),
          '-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'vendor/bearssl/src'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'vendor/libassh/src'),
          '-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'vendor/lwip/src/include'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ନେଟ୍_ୱାର୍କ୍_ଗଦା'),
          '-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시언어번역기')]
    for ପଥ in sorted(Path(ନାମ) for ନାମ in 소유파일 if ନାମ.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if ପଥ.suffix=='.cpp' else '-std=c11']
        if 'ନେଟ୍_ୱାର୍କ୍_ଗଦା' in ପଥ.parts: 인수 += ['-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'ନେଟ୍_ୱାର୍କ୍_ଗଦା'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'vendor/lwip/src/include')]
        if '시언어번역기' in ପଥ.parts:
            인수 += ['-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시언어번역기'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'vendor/tinycc'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/ccompiler'),
                    '-isystem',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in ପଥ.parts:
            인수 += ['-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'파이썬연결'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/micropython-1.24.1'),'-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/python'),'-isystem','/usr/include/newlib']
        if 'ଦୂରବର୍ତ୍ତୀ_ମୂଲ୍ୟ' in ପଥ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in ପଥ.parts: 인수 += ['-D__JKOROS__=1']
        if ପଥ.name=='ବଣ୍ଡଲ୍.c': 인수 += ['-I'+str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ = (씨.c_char_p*len(인수))(*[ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.encode() for ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ in 인수])
        ଅନୁବାଦ_ଶିକ୍ଷା = 분석(ଦୃଷ୍ଟିପାତ_ଅନୁକ୍ରମଣିକା,str(ପଥ).encode(),ଗୋଷ୍ଠୀ_ମୂଲ୍ୟ,len(인수),None,0,1)
        for ଅନୁକ୍ରମଣିକା in range(진단수(ଅନୁବାଦ_ଶିକ୍ଷା)):
            진단 = 진단얻기(ଅନୁବାଦ_ଶିକ୍ଷା,ଅନୁକ୍ରମଣିକା)
            if ସୁରକ୍ଷା_ମୂଲ୍ୟ(진단)>=3: 오류들.append((str(ପଥ.relative_to(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍)),ପାଠ୍ଯ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ,부모,ଡାଟା):
            ଫାଇଲ,ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ,ରେଖା = ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)
            if ଫାଇଲ not in 소유파일: return 2 if ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.종류==300 else 1
            낱말 = ପାଠ୍ଯ(이름얻기(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ))
            if not 낱말 or any(ord(ବର୍ଣ୍ଣ_ମୂଲ୍ୟ)>127 for ବର୍ଣ୍ଣ_ମୂଲ୍ୟ in 낱말): return 2
            if ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = ପାଠ୍ଯ(고유이름(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)) or ଫାଇଲ+':'+str(ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ)
                선언들[고유] = {'ଫାଇଲ':ଫାଇଲ,'ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ':ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ,'줄':ରେଖା,'종류':ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ.종류,'ନାମ':낱말,'ସଂଯୋଗ_କରନ୍ତୁ':연결종류(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)}
                참조들.append((ଫାଇଲ,ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ,낱말,고유))
            else:
                ପ୍ରସଙ୍ଗ = 참조얻기(ଏଣ୍ଟ୍ରି_ମୂଲ୍ୟ)
                ପ୍ରସଙ୍ଗ_ଫାଇଲ୍,_,_ = ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା(ପ୍ରସଙ୍ଗ)
                if ପ୍ରସଙ୍ଗ_ଫାଇଲ୍ in 소유파일:
                    고유 = ପାଠ୍ଯ(고유이름(ପ୍ରସଙ୍ଗ)); 참조들.append((ଫାଇଲ,ଅଫ୍_ସେଟ୍_ମୂଲ୍ୟ,ପାଠ୍ଯ(이름얻기(ପ୍ରସଙ୍ଗ)),고유))
            return 2
        방문(ରୁଟ୍_ମୂଲ୍ୟ(ଅନୁବାଦ_ଶିକ୍ଷା),살피기,None)
        ଛାଡିବା_ଅନୁପ୍ରୟୋଗ(ଅନୁବାଦ_ଶିକ୍ଷା)
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/한국어화/시언어분석.json'
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {ଫାଇଲ:hashlib.sha256(Path(ଫାଇଲ).read_bytes()).hexdigest() for ଫାଇଲ in sorted(소유파일)}
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ.write_text(json.dumps({'선언':선언들,'ପ୍ରସଙ୍ଗ':참조들,'ତ୍ରୁଟି':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'ପ୍ରସଙ୍ଗ',len(참조들),'ତ୍ରୁଟି',len(오류들))
    for ତ୍ରୁଟି in 오류들: print(*ତ୍ରୁଟି)

if __name__=='__main__': ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ()
