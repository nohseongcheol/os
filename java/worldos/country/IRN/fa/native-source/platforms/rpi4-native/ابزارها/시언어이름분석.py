#!/usr/bin/env python3
"""libclang اعلامیه·مرجع 위치를 수집한다. 외부 헤더의 멤버는 변환하지 않는다."""
import ctypes as 씨
import hashlib
import json
from pathlib import Path

نمایش_دادن_جذر = Path(__file__).resolve().parents[1]
구현 = 씨.CDLL('/usr/lib/llvm-6.0/lib/libclang.so.1')
class رشته_مقدار_6ca8363c(씨.Structure): _fields_ = [('داده_ها',씨.c_void_p),('نمایش_مقدار',씨.c_uint)]
class مکان_نما_مقدار(씨.Structure): _fields_ = [('종류',씨.c_uint),('보조',씨.c_int),('داده_ها',씨.c_void_p*3)]
class مرتب_کردن(씨.Structure): _fields_ = [('داده_ها',씨.c_void_p*2),('جابجایی_لایه_ای_مقدار',씨.c_uint)]
def عملکرد_مقدار(نام, بازگرداندن_سنجش, *نشانوندها):
    ورودی_مقدار = getattr(구현, نام); ورودی_مقدار.restype = بازگرداندن_سنجش; ورودی_مقدار.argtypes = list(نشانوندها); return ورودی_مقدار
دریافت_متن = عملکرد_مقدار('clang_getCString',씨.c_char_p,رشته_مقدار_6ca8363c)
انتشار_متن = عملکرد_مقدار('clang_disposeString',None,رشته_مقدار_6ca8363c)
def متن(مقدار):
    سنجش = (دریافت_متن(مقدار) or b'').decode('utf-8'); انتشار_متن(مقدار); return سنجش
دریافت_نام = عملکرد_مقدار('clang_getCursorSpelling',رشته_مقدار_6ca8363c,مکان_نما_مقدار)
دریافت_مرجع = عملکرد_مقدار('clang_getCursorReferenced',مکان_نما_مقدار,مکان_نما_مقدار)
دریافت_مرتب_کردن = عملکرد_مقدار('clang_getCursorLocation',مرتب_کردن,مکان_نما_مقدار)
فایل_مرتب_کردن = عملکرد_مقدار('clang_getFileLocation',None,مرتب_کردن,씨.POINTER(씨.c_void_p),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint),씨.POINTER(씨.c_uint))
فایل_ورودی_نام = عملکرد_مقدار('clang_getFileName',رشته_مقدار_6ca8363c,씨.c_void_p)
고유이름 = عملکرد_مقدار('clang_getCursorUSR',رشته_مقدار_6ca8363c,مکان_نما_مقدار)
연결종류 = عملکرد_مقدار('clang_getCursorLinkage',씨.c_uint,مکان_نما_مقدار)
방문형 = 씨.CFUNCTYPE(씨.c_uint,مکان_نما_مقدار,مکان_نما_مقدار,씨.c_void_p)
방문 = عملکرد_مقدار('clang_visitChildren',씨.c_uint,مکان_نما_مقدار,방문형,씨.c_void_p)
ایجاد = عملکرد_مقدار('clang_createIndex',씨.c_void_p,씨.c_int,씨.c_int)
분석 = عملکرد_مقدار('clang_parseTranslationUnit',씨.c_void_p,씨.c_void_p,씨.c_char_p,씨.POINTER(씨.c_char_p),씨.c_int,씨.c_void_p,씨.c_uint,씨.c_uint)
جذر_مقدار = عملکرد_مقدار('clang_getTranslationUnitCursor',مکان_نما_مقدار,씨.c_void_p)
خروج_برنامه_55b3a1cd = عملکرد_مقدار('clang_disposeTranslationUnit',None,씨.c_void_p)
진단수 = عملکرد_مقدار('clang_getNumDiagnostics',씨.c_uint,씨.c_void_p)
진단얻기 = عملکرد_مقدار('clang_getDiagnostic',씨.c_void_p,씨.c_void_p,씨.c_uint)
شدت_مقدار = عملکرد_مقدار('clang_getDiagnosticSeverity',씨.c_uint,씨.c_void_p)
진단문 = عملکرد_مقدار('clang_getDiagnosticSpelling',رشته_مقدار_6ca8363c,씨.c_void_p)
진단해제 = عملکرد_مقدار('clang_disposeDiagnostic',None,씨.c_void_p)

def مرتب_کردن_فهرست(ورودی_مقدار):
    پرونده = 씨.c_void_p(); خط = 씨.c_uint(); شکاف_ورودی = 씨.c_uint(); جابجایی_لایه_ای_مقدار = 씨.c_uint()
    فایل_مرتب_کردن(دریافت_مرتب_کردن(ورودی_مقدار),씨.byref(پرونده),씨.byref(خط),씨.byref(شکاف_ورودی),씨.byref(جابجایی_لایه_ای_مقدار))
    return (متن(فایل_ورودی_نام(پرونده)) if پرونده else '', جابجایی_لایه_ای_مقدار.value, خط.value)

def اجرا_فرمان():
    جستجو_فهرست = ایجاد(0,0); 선언들 = {}; 참조들 = []; 오류들 = []
    # 번역기.c는 بومی اعلامیه 없이 TinyCC 외부 단일 تبدیل_منبع 단위만 포함한다.
    # 외부 선언을 بومی 이름으로 세지 않으며, واقعی_داده_ها 빌드에서는 계속 컴파일한다.
    소유파일 = {str(مسیر.resolve()) for مسیر in نمایش_دادن_جذر.rglob('*') if مسیر.suffix in ('.c','.h','.cpp','.inc')
              and not set(مسیر.relative_to(نمایش_دادن_جذر).parts)&{'build','dist','vendor','__pycache__'}
              and مسیر.relative_to(نمایش_دادن_جذر).as_posix() != '시언어번역기/번역기.c'}
    공통 = ['--target=aarch64-none-elf','-mcpu=cortex-a72','-ffreestanding','-I'+str(نمایش_دادن_جذر/'کاربر'),
          '-I'+str(نمایش_دادن_جذر.parents[1]/'posix-kor/arm64-native/포함'),'-I'+str(نمایش_دادن_جذر/'build'),'-I'+str(نمایش_دادن_جذر/'build/user'),
          '-I'+str(نمایش_دادن_جذر/'build/remote'),'-I'+str(نمایش_دادن_جذر/'vendor/bearssl/inc'),
          '-I'+str(نمایش_دادن_جذر/'vendor/bearssl/src'),'-I'+str(نمایش_دادن_جذر/'vendor/libassh/src'),
          '-I'+str(نمایش_دادن_جذر/'vendor/lwip/src/include'),'-I'+str(نمایش_دادن_جذر/'شبکه_پشته'),
          '-I'+str(نمایش_دادن_جذر/'راه_دور_مقدار'),'-I'+str(نمایش_دادن_جذر/'시언어번역기')]
    for مسیر in sorted(Path(نام) for نام in 소유파일 if نام.endswith(('.c','.cpp'))):
        نشانوندها = 공통 + ['-std=c++11' if مسیر.suffix=='.cpp' else '-std=c11']
        if 'شبکه_پشته' in مسیر.parts: نشانوندها += ['-I'+str(نمایش_دادن_جذر/'شبکه_پشته'),'-I'+str(نمایش_دادن_جذر/'vendor/lwip/src/include')]
        if '시언어번역기' in مسیر.parts:
            نشانوندها += ['-I'+str(نمایش_دادن_جذر/'시언어번역기'),'-I'+str(نمایش_دادن_جذر/'vendor/tinycc'),'-I'+str(نمایش_دادن_جذر/'build/ccompiler'),
                    '-isystem',str(نمایش_دادن_جذر.parent/'rpi4/build/rootfs/usr/include')]
        if '파이썬연결' in مسیر.parts:
            نشانوندها += ['-I'+str(نمایش_دادن_جذر/'파이썬연결'),'-I'+str(نمایش_دادن_جذر/'build/micropython-1.24.1'),'-I'+str(نمایش_دادن_جذر/'build/python'),'-isystem','/usr/include/newlib']
        if 'راه_دور_مقدار' in مسیر.parts:
            نشانوندها += ['-isystem', '/usr/include/newlib']
        if '배포' in مسیر.parts: نشانوندها += ['-D__JKOROS__=1']
        if مسیر.name=='دسته_کردن.c': نشانوندها += ['-I'+str(نمایش_دادن_جذر/'vendor/uzlib'),'-DUZLIB_CONF_PARANOID_CHECKS=1']
        گروه_مقدار = (씨.c_char_p*len(نشانوندها))(*[ورودی_مقدار.encode() for ورودی_مقدار in نشانوندها])
        ترجمه_درس = 분석(جستجو_فهرست,str(مسیر).encode(),گروه_مقدار,len(نشانوندها),None,0,1)
        for فهرست in range(진단수(ترجمه_درس)):
            진단 = 진단얻기(ترجمه_درس,فهرست)
            if شدت_مقدار(진단)>=3: 오류들.append((str(مسیر.relative_to(نمایش_دادن_جذر)),متن(진단문(진단))))
            진단해제(진단)
        @방문형
        def 살피기(ورودی_مقدار,부모,داده_ها):
            پرونده,جابجایی_لایه_ای_مقدار,خط = مرتب_کردن_فهرست(ورودی_مقدار)
            if پرونده not in 소유파일: return 2 if ورودی_مقدار.종류==300 else 1
            낱말 = متن(دریافت_نام(ورودی_مقدار))
            if not 낱말 or any(ord(نویسه_مقدار)>127 for نویسه_مقدار in 낱말): return 2
            if ورودی_مقدار.종류 in (2,3,4,5,6,7,8,9,10,20,21,501):
                고유 = متن(고유이름(ورودی_مقدار)) or پرونده+':'+str(جابجایی_لایه_ای_مقدار)
                선언들[고유] = {'پرونده':پرونده,'جابجایی_لایه_ای_مقدار':جابجایی_لایه_ای_مقدار,'خط':خط,'종류':ورودی_مقدار.종류,'نام':낱말,'اتصال':연결종류(ورودی_مقدار)}
                참조들.append((پرونده,جابجایی_لایه_ای_مقدار,낱말,고유))
            else:
                مرجع = دریافت_مرجع(ورودی_مقدار)
                مرجع_فایل,_,_ = مرتب_کردن_فهرست(مرجع)
                if مرجع_فایل in 소유파일:
                    고유 = متن(고유이름(مرجع)); 참조들.append((پرونده,جابجایی_لایه_ای_مقدار,متن(دریافت_نام(مرجع)),고유))
            return 2
        방문(جذر_مقدار(ترجمه_درس),살피기,None)
        خروج_برنامه_55b3a1cd(ترجمه_درس)
    مقصد_مقدار = نمایش_دادن_جذر/'build/한국어화/시언어분석.json'
    مقصد_مقدار.parent.mkdir(parents=True, exist_ok=True)
    해시들 = {پرونده:hashlib.sha256(Path(پرونده).read_bytes()).hexdigest() for پرونده in sorted(소유파일)}
    مقصد_مقدار.write_text(json.dumps({'اعلامیه':선언들,'مرجع':참조들,'خطا':오류들,'원문해시':해시들},ensure_ascii=False,indent=2)+'\n')
    print('اعلامیه',len(선언들),'مرجع',len(참조들),'خطا',len(오류들))
    for خطا in 오류들: print(*خطا)

if __name__=='__main__': اجرا_فرمان()
