#!/usr/bin/env python3
"""libclang 선언·حوالہ_جات 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

عکس_ڈالنا_روٹ = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class سلک_قدر(씨.Structure): _fields_ = [('کوائف',씨.c_void_p),('دکھانا_قدر',씨.c_uint)]
class کرسر_قدر(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('کوائف',씨.c_void_p*3)]
class مقام(씨.Structure): _fields_ = [('کوائف',씨.c_void_p*2),('آفسٹ_قدر',씨.c_uint)]
def فعل_قدر(نام, 반환, *دلائل):
    اندراج_قدر = getattr(구현, نام); اندراج_قدر.restype = 반환; اندراج_قدر.argtypes = list(دلائل); return اندراج_قدر
글얻기 = فعل_قدر('clang_getCString',씨.c_char_p,سلک_قدر)
ریلیز_متن = فعل_قدر('clang_disposeString',None,سلک_قدر)
def متن(قدر):
    پیمائش = (글얻기(قدر) or b'').decode('utf-8'); ریلیز_متن(قدر); return پیمائش
이름얻기 = فعل_قدر('clang_getCursorSpelling',سلک_قدر,کرسر_قدر)
참조얻기 = فعل_قدر('clang_getCursorReferenced',کرسر_قدر,کرسر_قدر)
위치얻기 = فعل_قدر('clang_getCursorLocation',مقام,کرسر_قدر)
فائل_پوزیشن_ٹھیک_کریں = فعل_قدر('clang_getFileLocation',None,مقام,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
فائل_اندراج_نام = فعل_قدر('clang_getFileName',سلک_قدر,씨.c_void_p)
고유이름 = فعل_قدر('clang_getCursorUSR',سلک_قدر,کرسر_قدر)
연결종류 = فعل_قدر('clang_getCursorLinkage',씨.c_uint,کرسر_قدر)
방문형 = 씨.CFUNCTYPE(씨.c_uint,کرسر_قدر,کرسر_قدر,씨.c_void_p)
방문 = فعل_قدر('clang_visitChildren',씨.c_uint,کرسر_قدر,방문형,씨.c_void_p)
تخلیق_کرنا = فعل_قدر('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = فعل_قدر('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
روٹ_قدر = فعل_قدر('clang_getTranslationUnitCursor',کرسر_قدر,씨.c_void_p)
نکل_جائيں_ایپ = فعل_قدر('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = فعل_قدر('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = فعل_قدر('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
شدت_قدر = فعل_قدر('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = فعل_قدر('clang_getDiagnosticSpelling',سلک_قدر,씨.c_void_p)
진단해제 = فعل_قدر('clang_disposeDiagnostic',None,씨.c_void_p)

def پوزیشن_ٹھیک_کریں_اشاریہ(اندراج_قدر):
    فائل_کا_نام = 씨.c_void_p(); اندراج_کی_سطر = 씨.c_uint(); سلاٹ_اندراج = 씨.c_uint(); آفسٹ_قدر = 씨.c_uint()
    فائل_پوزیشن_ٹھیک_کریں(위치얻기(اندراج_قدر),씨.byref(فائل_کا_نام),씨.byref(اندراج_کی_سطر),씨.byref(سلاٹ_اندراج),씨.byref(آفسٹ_قدر))
    return (متن(فائل_اندراج_نام(فائل_کا_نام)) if فائل_کا_نام else '', آفسٹ_قدر.value, اندراج_کی_سطر.value)

def نفاذ_کریں_حکم():
    لُک_اپ_اشاریہ = تخلیق_کرنا(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 اپنا 선언 없이 TinyCC 외부 단일 ترجمہ_ماخذ 단위만 포함한다.
    # 외부 선언을 اپنا 이름으로 세지 않으며, اصل_کوائف 빌드에서는 계속 컴파일한다.
    소유파일 = {str(راستہ_2.resolve()) for راستہ_2 in عکس_ڈالنا_روٹ.rglob('*') if راستہ_2.suffix in ('.c','.h','.cpp','.inc')
              and not set(راستہ_2.relative_to(عکس_ڈالنا_روٹ).parts)&{'build','dist','vendor','__pycache__'}
              and راستہ_2.relative_to(عکس_ڈالنا_روٹ).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(عکس_ڈالنا_روٹ/'صارف'),
          '-I'+str(عکس_ڈالنا_روٹ.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(عکس_ڈالنا_روٹ/'build'),'-I'+str(عکس_ڈالنا_روٹ/'build/user'),
          '-I'+str(عکس_ڈالنا_روٹ/'build/remote'),'-I'+str(عکس_ڈالنا_روٹ/'vendor/bearssl/inc'),
          '-I'+str(عکس_ڈالنا_روٹ/'vendor/bearssl/src'),'-I'+str(عکس_ڈالنا_روٹ/'vendor/libassh/src'),
          '-I'+str(عکس_ڈالنا_روٹ/'vendor/lwip/src/include'),'-I'+str(عکس_ڈالنا_روٹ/'نیٹ_ورک_اسٹیک'),
          '-I'+str(عکس_ڈالنا_روٹ/'بعید_قدر'),'-I'+str(عکس_ڈالنا_روٹ/'시언어번역기')]
    for راستہ_2 in sorted(Path(نام) for نام in 소유파일 if نام.endswith(('.c','.cpp'))):
        دلائل = 공통 + ['-std=c++11' if راستہ_2.suffix=='.cpp' else '-std=c11']
        if 'نیٹ_ورک_اسٹیک' in راستہ_2.parts: دلائل += ['-I'+str(عکس_ڈالنا_روٹ/'نیٹ_ورک_اسٹیک'),'-I'+str(عکس_ڈالنا_روٹ/'vendor/lwip/src/include')]
        if '시언어번역기' in راستہ_2.parts:
            دلائل += ['-I'+str(عکس_ڈالنا_روٹ/'시언어번역기'),'-I'+str(عکس_ڈالنا_روٹ/'vendor/tinycc'),'-I'+str(عکس_ڈالنا_روٹ/'build/ccompiler'),
                    '-isystem',str(عکس_ڈالنا_روٹ.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in راستہ_2.parts:
            دلائل += ['-I'+str(عکس_ڈالنا_روٹ/'파이썬연결'),'-I'+str(عکس_ڈالنا_روٹ/'build/micropython-1.24.1'),'-I'+str(عکس_ڈالنا_روٹ/'build/python'),'-isystem','/usr/include/newlib']
        if 'بعید_قدر' in راستہ_2.parts:
            دلائل += ['-isystem', '/usr/include/newlib']
        if '배포' in راستہ_2.parts: دلائل += ['-D__JKOROS__=1']
        if راستہ_2.name=='بنڈل.c': دلائل += ['-I'+str(عکس_ڈالنا_روٹ/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        گروپ_قدر = (씨.c_char_p*len(دلائل))(*[اندراج_قدر.encode() for اندراج_قدر in دلائل])
        ترجمہ_سبق = 분석(لُک_اپ_اشاریہ,str(راستہ_2).encode(),گروپ_قدر,len(دلائل),None,0,1)
        for اشاریہ in range(진단수(ترجمہ_سبق)):
            진단 = 진단얻기(ترجمہ_سبق,اشاریہ)
            if شدت_قدر(진단)>=3: 오류들.append((str(راستہ_2.relative_to(عکس_ڈالنا_روٹ)),متن(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(اندراج_قدر,부모,کوائف):
            فائل_کا_نام,آفسٹ_قدر,اندراج_کی_سطر = پوزیشن_ٹھیک_کریں_اشاریہ(اندراج_قدر)
            if فائل_کا_نام not in 소유파일: return 2 if اندراج_قدر.종류==300 else 1
            낱말 = متن(이름얻기(اندراج_قدر))
            if not 낱말 or any(ord(کریکٹر_قدر)>127 for کریکٹر_قدر in 낱말): return 2
            if اندراج_قدر.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = متن(고유이름(اندراج_قدر)) or فائل_کا_نام+':'+str(آفسٹ_قدر)
                선언들[고유] = {'فائل_کا_نام':فائل_کا_نام,'آفسٹ_قدر':آفسٹ_قدر,'اندراج_کی_سطر':اندراج_کی_سطر,'종류':اندراج_قدر.종류,'نام':낱말,'متصل_ہوں':연결종류(اندراج_قدر)}
                참조들.append((فائل_کا_نام,آفسٹ_قدر,낱말,고유))
            else:
                حوالہ_جات = 참조얻기(اندراج_قدر)
                حوالہ_جات_فائل,_,_ = پوزیشن_ٹھیک_کریں_اشاریہ(حوالہ_جات)
                if حوالہ_جات_فائل in 소유파일:
                    고유 = متن(고유이름(حوالہ_جات)); 참조들.append((فائل_کا_نام,آفسٹ_قدر,متن(이름얻기(حوالہ_جات)),고유))
            return 2
        방문(روٹ_قدر(ترجمہ_سبق),살피기,None)
        نکل_جائيں_ایپ(ترجمہ_سبق)
    منزل_مقصود_قدر = عکس_ڈالنا_روٹ/'build/한국어화/시언어분석.json'
    منزل_مقصود_قدر.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {فائل_کا_نام:hashlib.sha256(Path(فائل_کا_نام).read_bytes()).hexdigest() for فائل_کا_نام in sorted(소유파일)}
    منزل_مقصود_قدر.write_text(json.dumps({'선언':선언들,'حوالہ_جات':참조들,'غلطی':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('선언',len(선언들),'حوالہ_جات',len(참조들),'غلطی',len(오류들))
    for غلطی in 오류들: print(*غلطی)

if __name__=='__main__': نفاذ_کریں_حکم()
