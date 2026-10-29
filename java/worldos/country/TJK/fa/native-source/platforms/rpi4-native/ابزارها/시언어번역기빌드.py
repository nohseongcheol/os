"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(جذر_مسیر, مخزن_مسیر, 시언어번역기, 연결편집기, 설정비트, اجرا_فرمان):
    سنجش_داده_ها = جذر_مسیر / 'build/ccompiler'; سنجش_داده_ها.mkdir(exist_ok=True)
    원본자료 = جذر_مسیر / '시언어번역기'
    بالادست = جذر_مسیر / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = جذر_مسیر / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [تنظیمات_مقدار for تنظیمات_مقدار in 설정비트 if تنظیمات_مقدار != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', بالادست, '-I', جذر_مسیر/'کاربر', '-I', سنجش_داده_ها, '-isystem', 개발꾸러미/'usr/include']
    اجرا_فرمان([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'راه_اندازی_پشتیبان.c','-o',سنجش_داده_ها/'crt.o'])
    اجرا_فرمان([시언어번역기]+설정비트+['-I',مخزن_مسیر/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',سنجش_داده_ها/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+داده_ها_مرتب_کردن.name,داده_ها_مرتب_کردن) for داده_ها_مرتب_کردن in sorted((مخزن_مسیر/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+داده_ها_مرتب_کردن.name,داده_ها_مرتب_کردن) for داده_ها_مرتب_کردن in sorted((بالادست/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+داده_ها_مرتب_کردن.name,داده_ها_مرتب_کردن) for داده_ها_مرتب_کردن in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',جذر_مسیر/'build/user/start.o'),('/sdk/lib/crt.o',سنجش_داده_ها/'crt.o'),('/sdk/lib/aot-runtime.o',سنجش_داده_ها/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',جذر_مسیر/'build/libposix-kor-user.a')]
    سرصفحه_مقدار=['typedef struct { const char *نام; const unsigned char *داده_ها; unsigned اندازه; } 번역기자원;']
    for 순번,(_,مسیر) in enumerate(탑재자료):
        سرصفحه_مقدار.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in مسیر.read_bytes())))
    سرصفحه_مقدار.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(نام,مسیر) in enumerate(탑재자료): سرصفحه_مقدار.append('{%s, 탑재자원_%d, %d},'%(json.dumps(نام,ensure_ascii=False),순번,مسیر.stat().st_size))
    سرصفحه_مقدار.append('};');(سنجش_داده_ها/'resources.h').write_text('\n'.join(سرصفحه_مقدار)+'\n',encoding='utf-8')
    مقصد_فایل=[]
    for نام in ('번역기.c','زمان_اجرای_زبان_مشترک_پشتیبان.c','اجرا_2.c','미리번역.c','بازگرداندن_پل.S'):
        پرونده_مقصد=سنجش_داده_ها/(Path(نام).stem+'.o');مقصد_فایل.append(پرونده_مقصد)
        اجرا_فرمان([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/نام,'-o',پرونده_مقصد])
    실행파일=جذر_مسیر/'build/user/cc.elf'
    اجرا_فرمان([연결편집기,'--gc-sections','-T',جذر_مسیر/'کاربر/پیوند_پیمایش.ld','-z','max-page-size=4096','-o',실행파일,
         جذر_مسیر/'build/user/start.o',جذر_مسیر/'build/user/runtime.o']+مقصد_فایل+
         [جذر_مسیر/'build/user'/نام for نام in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
