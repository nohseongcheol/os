#!/usr/bin/env python3
"""libclang 선언·참조 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class ষ্ট্ৰিং_মান(씨.Structure): _fields_ = [('ডাটা',씨.c_void_p),('শ্ব_মান',씨.c_uint)]
class কাৰ্ছৰ_মান(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ডাটা',씨.c_void_p*3)]
class অৱস্থান(씨.Structure): _fields_ = [('ডাটা',씨.c_void_p*2),('অফছেট_মান',씨.c_uint)]
def ফাংছন_মান(নাম, 반환, *인수):
    প্রবিষ্ট_মান = getattr(구현, নাম); প্রবিষ্ট_মান.restype = 반환; প্রবিষ্ট_মান.argtypes = list(인수); return প্রবিষ্ট_মান
글얻기 = ফাংছন_মান('clang_getCString',씨.c_char_p,ষ্ট্ৰিং_মান)
ৰিলিজ_পাঠ = ফাংছন_মান('clang_disposeString',None,ষ্ট্ৰিং_মান)
def টেক্সট(মান):
    পৰিমাপ = (글얻기(মান) or b'').decode('utf-8'); ৰিলিজ_পাঠ(মান); return পৰিমাপ
이름얻기 = ফাংছন_মান('clang_getCursorSpelling',ষ্ট্ৰিং_মান,কাৰ্ছৰ_মান)
참조얻기 = ফাংছন_মান('clang_getCursorReferenced',কাৰ্ছৰ_মান,কাৰ্ছৰ_মান)
위치얻기 = ফাংছন_মান('clang_getCursorLocation',অৱস্থান,কাৰ্ছৰ_মান)
ফাইল_স্থান_সলনি_কৰক = ফাংছন_মান('clang_getFileLocation',None,অৱস্থান,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ফাইল_প্রবিষ্ট_নাম = ফাংছন_মান('clang_getFileName',ষ্ট্ৰিং_মান,씨.c_void_p)
고유이름 = ফাংছন_মান('clang_getCursorUSR',ষ্ট্ৰিং_মান,কাৰ্ছৰ_মান)
연결종류 = ফাংছন_মান('clang_getCursorLinkage',씨.c_uint,কাৰ্ছৰ_মান)
방문형 = 씨.CFUNCTYPE(씨.c_uint,কাৰ্ছৰ_মান,কাৰ্ছৰ_মান,씨.c_void_p)
방문 = ফাংছন_মান('clang_visitChildren',씨.c_uint,কাৰ্ছৰ_মান,방문형,씨.c_void_p)
সৃষ্টি_কৰক = ফাংছন_মান('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ফাংছন_মান('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
ৰুট_মান = ফাংছন_মান('clang_getTranslationUnitCursor',কাৰ্ছৰ_মান,씨.c_void_p)
ত্যাগ_এপ্প্ = ফাংছন_মান('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ফাংছন_মান('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ফাংছন_মান('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
গুৰুত্ব_মান = ফাংছন_মান('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ফাংছন_মান('clang_getDiagnosticSpelling',ষ্ট্ৰিং_মান,씨.c_void_p)
진단해제 = ফাংছন_মান('clang_disposeDiagnostic',None,씨.c_void_p)

def স্থান_সলনি_কৰক_ইনডেক্স(প্রবিষ্ট_মান):
    নথিপত্ৰ = 씨.c_void_p(); লাইন = 씨.c_uint(); শ্লট_প্রবিষ্ট = 씨.c_uint(); অফছেট_মান = 씨.c_uint()
    ফাইল_স্থান_সলনি_কৰক(위치얻기(প্রবিষ্ট_মান),씨.byref(নথিপত্ৰ),씨.byref(লাইন),씨.byref(শ্লট_প্রবিষ্ট),씨.byref(অফছেট_মান))
    return (টেক্সট(ফাইল_প্রবিষ্ট_নাম(নথিপত্ৰ)) if নথিপত্ৰ else '', অফছেট_মান.value, লাইন.value)

def নিষ্পাদন_আদেশ():
    লুকআপ_ইনডেক্স = সৃষ্টি_কৰক(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 অনুবাদ_উৎস 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, প্ৰকৃত_ডাটা 빌드에서는 계속 컴파일한다.
    소유파일 = {str(পথ.resolve()) for পথ in 기준.rglob('*') if পথ.suffix in ('.c','.h','.cpp','.inc')
              and not set(পথ.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and পথ.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'ব্যৱহাৰকৰ্তা'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'নেটৱৰ্ক_ষ্টেক'),
          '-I'+str(기준/'দূৰবৰ্তী_মান'),'-I'+str(기준/'시언어번역기')]
    for পথ in sorted(Path(নাম) for নাম in 소유파일 if নাম.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if পথ.suffix=='.cpp' else '-std=c11']
        if 'নেটৱৰ্ক_ষ্টেক' in পথ.parts: 인수 += ['-I'+str(기준/'নেটৱৰ্ক_ষ্টেক'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in পথ.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in পথ.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'দূৰবৰ্তী_মান' in পথ.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in পথ.parts: 인수 += ['-D__JKOROS__=1']
        if পথ.name=='বাণ্ডল.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        দল_মান = (씨.c_char_p*len(인수))(*[প্রবিষ্ট_মান.encode() for প্রবিষ্ট_মান in 인수])
        অনুবাদ_কৰক_পাঠ্য = 분석(লুকআপ_ইনডেক্স,str(পথ).encode(),দল_মান,len(인수),None,0,1)
        for ইনডেক্স in range(진단수(অনুবাদ_কৰক_পাঠ্য)):
            진단 = 진단얻기(অনুবাদ_কৰক_পাঠ্য,ইনডেক্স)
            if গুৰুত্ব_মান(진단)>=3: 오류들.append((str(পথ.relative_to(기준)),টেক্সট(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(প্রবিষ্ট_মান,부모,ডাটা):
            নথিপত্ৰ,অফছেট_মান,লাইন = স্থান_সলনি_কৰক_ইনডেক্স(প্রবিষ্ট_মান)
            if নথিপত্ৰ not in 소유파일: return 2 if প্রবিষ্ট_মান.종류==300 else 1
            낱말 = টেক্সট(이름얻기(প্রবিষ্ট_মান))
            if not 낱말 or any(ord(বৰ্ণ_মান)>127 for বৰ্ণ_মান in 낱말): return 2
            if প্রবিষ্ট_মান.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = টেক্সট(고유이름(প্রবিষ্ট_মান)) or নথিপত্ৰ+':'+str(অফছেট_মান)
                선언들[고유] = {'নথিপত্ৰ':নথিপত্ৰ,'অফছেট_মান':অফছেট_মান,'줄':লাইন,'종류':প্রবিষ্ট_মান.종류,'নাম':낱말,'সংযোগ_স্থাপনা':연결종류(প্রবিষ্ট_মান)}
                참조들.append((নথিপত্ৰ,অফছেট_মান,낱말,고유))
            else:
                참조 = 참조얻기(প্রবিষ্ট_মান)
                참조파일,_,_ = স্থান_সলনি_কৰক_ইনডেক্স(참조)
                if 참조파일 in 소유파일:
                    고유 = টেক্সট(고유이름(참조)); 참조들.append((নথিপত্ৰ,অফছেট_মান,টেক্সট(이름얻기(참조)),고유))
            return 2
        방문(ৰুট_মান(অনুবাদ_কৰক_পাঠ্য),살피기,None)
        ত্যাগ_এপ্প্(অনুবাদ_কৰক_পাঠ্য)
    গন্তব্য_স্থান_মান = 기준/'build/한국어화/시언어분석.json'
    গন্তব্য_স্থান_মান.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {নথিপত্ৰ:hashlib.sha256(Path(নথিপত্ৰ).read_bytes()).hexdigest() for নথিপত্ৰ in sorted(소유파일)}
    গন্তব্য_স্থান_মান.write_text(json.dumps({'선언':선언들,'참조':참조들,'ত্ৰুটি':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'참조',len(참조들),'ত্ৰুটি',len(오류들))
    for ত্ৰুটি in 오류들: print(*ত্ৰুটি)

if __name__=='__main__': নিষ্পাদন_আদেশ()
