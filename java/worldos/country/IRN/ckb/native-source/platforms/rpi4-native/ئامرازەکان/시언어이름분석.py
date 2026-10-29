#!/usr/bin/env python3
"""libclang 선언·سەرچاوە 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

기준 = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class رست_نرخ(씨.Structure): _fields_ = [('دەیتا',씨.c_void_p),('نیشاندان_نرخ',씨.c_uint)]
class جێنیشاندەر_نرخ(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('دەیتا',씨.c_void_p*3)]
class 위치(씨.Structure): _fields_ = [('دەیتا',씨.c_void_p*2),('ئۆفسێت_نرخ',씨.c_uint)]
def کردار_نرخ(ناو, 반환, *인수):
    تێنووسین_نرخ = getattr(구현, ناو); تێنووسین_نرخ.restype = 반환; تێنووسین_نرخ.argtypes = list(인수); return تێنووسین_نرخ
글얻기 = کردار_نرخ('clang_getCString',씨.c_char_p,رست_نرخ)
وەشان_دەق = کردار_نرخ('clang_disposeString',None,رست_نرخ)
def دەق(نرخ):
    결과 = (글얻기(نرخ) or b'').decode('utf-8'); وەشان_دەق(نرخ); return 결과
이름얻기 = کردار_نرخ('clang_getCursorSpelling',رست_نرخ,جێنیشاندەر_نرخ)
참조얻기 = کردار_نرخ('clang_getCursorReferenced',جێنیشاندەر_نرخ,جێنیشاندەر_نرخ)
위치얻기 = کردار_نرخ('clang_getCursorLocation',위치,جێنیشاندەر_نرخ)
파일위치 = کردار_نرخ('clang_getFileLocation',None,위치,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
فایل_تێنووسین_ناو = کردار_نرخ('clang_getFileName',رست_نرخ,씨.c_void_p)
بێهاوتا_ناو = کردار_نرخ('clang_getCursorUSR',رست_نرخ,جێنیشاندەر_نرخ)
연결종류 = کردار_نرخ('clang_getCursorLinkage',씨.c_uint,جێنیشاندەر_نرخ)
방문형 = 씨.CFUNCTYPE(씨.c_uint,جێنیشاندەر_نرخ,جێنیشاندەر_نرخ,씨.c_void_p)
방문 = کردار_نرخ('clang_visitChildren',씨.c_uint,جێنیشاندەر_نرخ,방문형,씨.c_void_p)
생성 = کردار_نرخ('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = کردار_نرخ('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
뿌리 = کردار_نرخ('clang_getTranslationUnitCursor',جێنیشاندەر_نرخ,씨.c_void_p)
끝내기 = کردار_نرخ('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = کردار_نرخ('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = کردار_نرخ('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
ئاستی_مەترسی_نرخ = کردار_نرخ('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = کردار_نرخ('clang_getDiagnosticSpelling',رست_نرخ,씨.c_void_p)
진단해제 = کردار_نرخ('clang_disposeDiagnostic',None,씨.c_void_p)

def 자리(تێنووسین_نرخ):
    فایل = 씨.c_void_p(); دێڕ = 씨.c_uint(); کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین = 씨.c_uint(); ئۆفسێت_نرخ = 씨.c_uint()
    파일위치(위치얻기(تێنووسین_نرخ),씨.byref(فایل),씨.byref(دێڕ),씨.byref(کەلێن_بۆ_نووسین_یان_رەمز_تێنووسین),씨.byref(ئۆفسێت_نرخ))
    return (دەق(فایل_تێنووسین_ناو(فایل)) if فایل else '', ئۆفسێت_نرخ.value, دێڕ.value)

def جێبەجێکردن_فەرمان():
    색인 = 생성(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 자체 선언 없이 TinyCC 외부 단일 وەرگێڕان_ژێدەر 단위만 포함한다.
    # 외부 선언을 자체 이름으로 세지 않으며, ڕاستەکی_دەیتا 빌드에서는 계속 컴파일한다.
    소유파일 = {str(گوزەر.resolve()) for گوزەر in 기준.rglob('*') if گوزەر.suffix in ('.c','.h','.cpp','.inc')
              and not set(گوزەر.relative_to(기준).parts)&{'build','dist','vendor','__pycache__'}
              and گوزەر.relative_to(기준).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(기준/'بەکارهێنەر'),
          '-I'+str(기준.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(기준/'build'),'-I'+str(기준/'build/user'),
          '-I'+str(기준/'build/remote'),'-I'+str(기준/'vendor/bearssl/inc'),
          '-I'+str(기준/'vendor/bearssl/src'),'-I'+str(기준/'vendor/libassh/src'),
          '-I'+str(기준/'vendor/lwip/src/include'),'-I'+str(기준/'تۆڕ_ستاك'),
          '-I'+str(기준/'دوورەدەس_نرخ'),'-I'+str(기준/'시언어번역기')]
    for گوزەر in sorted(Path(ناو) for ناو in 소유파일 if ناو.endswith(('.c','.cpp'))):
        인수 = 공통 + ['-std=c++11' if گوزەر.suffix=='.cpp' else '-std=c11']
        if 'تۆڕ_ستاك' in گوزەر.parts: 인수 += ['-I'+str(기준/'تۆڕ_ستاك'),'-I'+str(기준/'vendor/lwip/src/include')]
        if '시언어번역기' in گوزەر.parts:
            인수 += ['-I'+str(기준/'시언어번역기'),'-I'+str(기준/'vendor/tinycc'),'-I'+str(기준/'build/ccompiler'),
                    '-isystem',str(기준.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in گوزەر.parts:
            인수 += ['-I'+str(기준/'파이썬연결'),'-I'+str(기준/'build/micropython-1.24.1'),'-I'+str(기준/'build/python'),'-isystem','/usr/include/newlib']
        if 'دوورەدەس_نرخ' in گوزەر.parts:
            인수 += ['-isystem', '/usr/include/newlib']
        if '배포' in گوزەر.parts: 인수 += ['-D__JKOROS__=1']
        if گوزەر.name=='گورزە.c': 인수 += ['-I'+str(기준/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        گروپ_نرخ = (씨.c_char_p*len(인수))(*[تێنووسین_نرخ.encode() for تێنووسین_نرخ in 인수])
        وەرگێڕان_وانە = 분석(색인,str(گوزەر).encode(),گروپ_نرخ,len(인수),None,0,1)
        for پێرست in range(진단수(وەرگێڕان_وانە)):
            진단 = 진단얻기(وەرگێڕان_وانە,پێرست)
            if ئاستی_مەترسی_نرخ(진단)>=3: 오류들.append((str(گوزەر.relative_to(기준)),دەق(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(تێنووسین_نرخ,부모,دەیتا):
            فایل,ئۆفسێت_نرخ,دێڕ = 자리(تێنووسین_نرخ)
            if فایل not in 소유파일: return 2 if تێنووسین_نرخ.종류==300 else 1
            낱말 = دەق(이름얻기(تێنووسین_نرخ))
            if not 낱말 or any(ord(نووسە_نرخ)>127 for نووسە_نرخ in 낱말): return 2
            if تێنووسین_نرخ.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                بێهاوتا_نرخ = دەق(بێهاوتا_ناو(تێنووسین_نرخ)) or فایل+':'+str(ئۆفسێت_نرخ)
                선언들[بێهاوتا_نرخ] = {'فایل':فایل,'ئۆفسێت_نرخ':ئۆفسێت_نرخ,'줄':دێڕ,'종류':تێنووسین_نرخ.종류,'ناو':낱말,'لكاندن':연결종류(تێنووسین_نرخ)}
                참조들.append((فایل,ئۆفسێت_نرخ,낱말,بێهاوتا_نرخ))
            else:
                سەرچاوە = 참조얻기(تێنووسین_نرخ)
                سەرچاوە_فایل,_,_ = 자리(سەرچاوە)
                if سەرچاوە_فایل in 소유파일:
                    بێهاوتا_نرخ = دەق(بێهاوتا_ناو(سەرچاوە)); 참조들.append((فایل,ئۆفسێت_نرخ,دەق(이름얻기(سەرچاوە)),بێهاوتا_نرخ))
            return 2
        방문(뿌리(وەرگێڕان_وانە),살피기,None)
        끝내기(وەرگێڕان_وانە)
    جێمەبەست_نرخ = 기준/'build/한국어화/시언어분석.json'
    جێمەبەست_نرخ.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {فایل:hashlib.sha256(Path(فایل).read_bytes()).hexdigest() for فایل in sorted(소유파일)}
    جێمەبەست_نرخ.write_text(json.dumps({'선언':선언들,'سەرچاوە':참조들,'هەڵە':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'سەرچاوە',len(참조들),'هەڵە',len(오류들))
    for هەڵە in 오류들: print(*هەڵە)

if __name__=='__main__': جێبەجێکردن_فەرمان()
