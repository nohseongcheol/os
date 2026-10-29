#!/usr/bin/env python3
"""libclang ঘোষণা·প্রসঙ্গ 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

প্রকল্প_মূল = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class স্ট্রিং_মান(씨.Structure): _fields_ = [('ডাটা',씨.c_void_p),('শো_মান',씨.c_uint)]
class কার্সর_মান(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('ডাটা',씨.c_void_p*3)]
class অবস্থান(씨.Structure): _fields_ = [('ডাটা',씨.c_void_p*2),('অফসেট_মান',씨.c_uint)]
def ফাংশন_মান(নাম, 반환, *আর্গুমেন্ট_তালিকা):
    ভুক্তি_মান = getattr(구현, নাম); ভুক্তি_মান.restype = 반환; ভুক্তি_মান.argtypes = list(আর্গুমেন্ট_তালিকা); return ভুক্তি_মান
পান_পাঠ = ফাংশন_মান('clang_getCString',씨.c_char_p,স্ট্রিং_মান)
রিলিজ_পাঠ = ফাংশন_মান('clang_disposeString',None,স্ট্রিং_মান)
def পাঠ(মান):
    পরিমাপ = (পান_পাঠ(মান) or b'').decode('utf-8'); রিলিজ_পাঠ(মান); return পরিমাপ
পান_নাম = ফাংশন_মান('clang_getCursorSpelling',স্ট্রিং_মান,কার্সর_মান)
পান_প্রসঙ্গ = ফাংশন_মান('clang_getCursorReferenced',কার্সর_মান,কার্সর_মান)
পান_পদ = ফাংশন_মান('clang_getCursorLocation',অবস্থান,কার্সর_মান)
ফাইল_পদ = ফাংশন_মান('clang_getFileLocation',None,অবস্থান,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
ফাইল_ভুক্তি_নাম = ফাংশন_মান('clang_getFileName',স্ট্রিং_মান,씨.c_void_p)
고유이름 = ফাংশন_মান('clang_getCursorUSR',স্ট্রিং_মান,কার্সর_মান)
연결종류 = ফাংশন_মান('clang_getCursorLinkage',씨.c_uint,কার্সর_মান)
방문형 = 씨.CFUNCTYPE(씨.c_uint,কার্সর_মান,কার্সর_মান,씨.c_void_p)
방문 = ফাংশন_মান('clang_visitChildren',씨.c_uint,কার্সর_মান,방문형,씨.c_void_p)
সৃষ্টি_করুন = ফাংশন_মান('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = ফাংশন_মান('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
মূল_মান = ফাংশন_মান('clang_getTranslationUnitCursor',কার্সর_মান,씨.c_void_p)
প্রস্থান_অ্যাপ_55b3a1cd = ফাংশন_মান('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = ফাংশন_মান('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = ফাংশন_মান('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
গুরুত্ব_মান = ফাংশন_মান('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = ফাংশন_মান('clang_getDiagnosticSpelling',স্ট্রিং_মান,씨.c_void_p)
진단해제 = ফাংশন_মান('clang_disposeDiagnostic',None,씨.c_void_p)

def পদ_সূচি(ভুক্তি_মান):
    নথির_নাম = 씨.c_void_p(); নিবেশের_পঙ্_ক্তি = 씨.c_uint(); স্লট_ভুক্তি = 씨.c_uint(); অফসেট_মান = 씨.c_uint()
    ফাইল_পদ(পান_পদ(ভুক্তি_মান),씨.byref(নথির_নাম),씨.byref(নিবেশের_পঙ্_ক্তি),씨.byref(স্লট_ভুক্তি),씨.byref(অফসেট_মান))
    return (পাঠ(ফাইল_ভুক্তি_নাম(নথির_নাম)) if নথির_নাম else '', অফসেট_মান.value, নিবেশের_পঙ্_ক্তি.value)

def কার্যকর_করুন_আদেশ():
    লুকআপ_সূচি = সৃষ্টি_করুন(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 নিজ ঘোষণা 없이 TinyCC 외부 단일 অনুবাদ_করুন_উত্স 단위만 포함한다.
    # 외부 선언을 নিজ 이름으로 세지 않으며, প্রকৃত_ডাটা 빌드에서는 계속 컴파일한다.
    소유파일 = {str(পথ_2.resolve()) for পথ_2 in প্রকল্প_মূল.rglob('*') if পথ_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(পথ_2.relative_to(প্রকল্প_মূল).parts)&{'build','dist','vendor','__pycache__'}
              and পথ_2.relative_to(প্রকল্প_মূল).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(প্রকল্প_মূল/'ব্যবহারকারী'),
          '-I'+str(প্রকল্প_মূল.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(প্রকল্প_মূল/'build'),'-I'+str(প্রকল্প_মূল/'build/user'),
          '-I'+str(প্রকল্প_মূল/'build/remote'),'-I'+str(প্রকল্প_মূল/'vendor/bearssl/inc'),
          '-I'+str(প্রকল্প_মূল/'vendor/bearssl/src'),'-I'+str(প্রকল্প_মূল/'vendor/libassh/src'),
          '-I'+str(প্রকল্প_মূল/'vendor/lwip/src/include'),'-I'+str(প্রকল্প_মূল/'নেটওয়ার্ক_গাদা'),
          '-I'+str(প্রকল্প_মূল/'দূরবর্তী_মান'),'-I'+str(প্রকল্প_মূল/'시언어번역기')]
    for পথ_2 in sorted(Path(নাম) for নাম in 소유파일 if নাম.endswith(('.c','.cpp'))):
        আর্গুমেন্ট_তালিকা = 공통 + ['-std=c++11' if পথ_2.suffix=='.cpp' else '-std=c11']
        if 'নেটওয়ার্ক_গাদা' in পথ_2.parts: আর্গুমেন্ট_তালিকা += ['-I'+str(প্রকল্প_মূল/'নেটওয়ার্ক_গাদা'),'-I'+str(প্রকল্প_মূল/'vendor/lwip/src/include')]
        if '시언어번역기' in পথ_2.parts:
            আর্গুমেন্ট_তালিকা += ['-I'+str(প্রকল্প_মূল/'시언어번역기'),'-I'+str(প্রকল্প_মূল/'vendor/tinycc'),'-I'+str(প্রকল্প_মূল/'build/ccompiler'),
                    '-isystem',str(প্রকল্প_মূল.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in পথ_2.parts:
            আর্গুমেন্ট_তালিকা += ['-I'+str(প্রকল্প_মূল/'파이썬연결'),'-I'+str(প্রকল্প_মূল/'build/micropython-1.24.1'),'-I'+str(প্রকল্প_মূল/'build/python'),'-isystem','/usr/include/newlib']
        if 'দূরবর্তী_মান' in পথ_2.parts:
            আর্গুমেন্ট_তালিকা += ['-isystem', '/usr/include/newlib']
        if '배포' in পথ_2.parts: আর্গুমেন্ট_তালিকা += ['-D__JKOROS__=1']
        if পথ_2.name=='পাঁজা.c': আর্গুমেন্ট_তালিকা += ['-I'+str(প্রকল্প_মূল/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        দল_মান = (씨.c_char_p*len(আর্গুমেন্ট_তালিকা))(*[ভুক্তি_মান.encode() for ভুক্তি_মান in আর্গুমেন্ট_তালিকা])
        অনুবাদ_একক = 분석(লুকআপ_সূচি,str(পথ_2).encode(),দল_মান,len(আর্গুমেন্ট_তালিকা),None,0,1)
        for সূচি in range(진단수(অনুবাদ_একক)):
            진단 = 진단얻기(অনুবাদ_একক,সূচি)
            if গুরুত্ব_মান(진단)>=3: 오류들.append((str(পথ_2.relative_to(প্রকল্প_মূল)),পাঠ(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ভুক্তি_মান,부모,ডাটা):
            নথির_নাম,অফসেট_মান,নিবেশের_পঙ্_ক্তি = পদ_সূচি(ভুক্তি_মান)
            if নথির_নাম not in 소유파일: return 2 if ভুক্তি_মান.종류==300 else 1
            낱말 = পাঠ(পান_নাম(ভুক্তি_মান))
            if not 낱말 or any(ord(অক্ষর_মান)>127 for অক্ষর_মান in 낱말): return 2
            if ভুক্তি_মান.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = পাঠ(고유이름(ভুক্তি_মান)) or নথির_নাম+':'+str(অফসেট_মান)
                선언들[고유] = {'নথির_নাম':নথির_নাম,'অফসেট_মান':অফসেট_মান,'নিবেশের_পঙ্_ক্তি':নিবেশের_পঙ্_ক্তি,'종류':ভুক্তি_মান.종류,'নাম':낱말,'সংযোগ_স্থাপনা':연결종류(ভুক্তি_মান)}
                참조들.append((নথির_নাম,অফসেট_মান,낱말,고유))
            else:
                প্রসঙ্গ = পান_প্রসঙ্গ(ভুক্তি_মান)
                প্রসঙ্গ_ফাইল,_,_ = পদ_সূচি(প্রসঙ্গ)
                if প্রসঙ্গ_ফাইল in 소유파일:
                    고유 = পাঠ(고유이름(প্রসঙ্গ)); 참조들.append((নথির_নাম,অফসেট_মান,পাঠ(পান_নাম(প্রসঙ্গ)),고유))
            return 2
        방문(মূল_মান(অনুবাদ_একক),살피기,None)
        প্রস্থান_অ্যাপ_55b3a1cd(অনুবাদ_একক)
    গন্তব্য_মান = প্রকল্প_মূল/'build/한국어화/시언어분석.json'
    গন্তব্য_মান.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {নথির_নাম:hashlib.sha256(Path(নথির_নাম).read_bytes()).hexdigest() for নথির_নাম in sorted(소유파일)}
    গন্তব্য_মান.write_text(json.dumps({'ঘোষণা':선언들,'প্রসঙ্গ':참조들,'ত্রুটি':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('ঘোষণা',len(선언들),'প্রসঙ্গ',len(참조들),'ত্রুটি',len(오류들))
    for ত্রুটি in 오류들: print(*ত্রুটি)

if __name__=='__main__': কার্যকর_করুন_আদেশ()
