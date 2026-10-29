"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(روٹ_راہ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, نفاذ_کریں_حکم):
    پیمائش_کوائف = روٹ_راہ / 'build/ccompiler'; پیمائش_کوائف.mkdir(exist_ok=True)
    원본자료 = روٹ_راہ / '시언어번역기'
    외부원문 = روٹ_راہ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = روٹ_راہ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [سیٹنگز_قدر for سیٹنگز_قدر in 설정비트 if سیٹنگز_قدر != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', روٹ_راہ/'صارف', '-I', پیمائش_کوائف, '-isystem', 개발꾸러미/'usr/include']
    نفاذ_کریں_حکم([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'بوٹ_کریں_معاونت.c','-o',پیمائش_کوائف/'crt.o'])
    نفاذ_کریں_حکم([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',پیمائش_کوائف/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+کوائف_پوزیشن_ٹھیک_کریں.name,کوائف_پوزیشن_ٹھیک_کریں) for کوائف_پوزیشن_ٹھیک_کریں in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+کوائف_پوزیشن_ٹھیک_کریں.name,کوائف_پوزیشن_ٹھیک_کریں) for کوائف_پوزیشن_ٹھیک_کریں in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+کوائف_پوزیشن_ٹھیک_کریں.name,کوائف_پوزیشن_ٹھیک_کریں) for کوائف_پوزیشن_ٹھیک_کریں in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',روٹ_راہ/'build/user/start.o'),('/sdk/lib/crt.o',پیمائش_کوائف/'crt.o'),('/sdk/lib/aot-runtime.o',پیمائش_کوائف/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',روٹ_راہ/'build/libposix-kor-user.a')]
    سرصفحہ_قدر=['typedef struct { const char *نام; const unsigned char *کوائف; unsigned حجم; } 번역기자원;']
    for 순번,(_,راستہ_2) in enumerate(탑재자료):
        سرصفحہ_قدر.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in راستہ_2.read_bytes())))
    سرصفحہ_قدر.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(نام,راستہ_2) in enumerate(탑재자료): سرصفحہ_قدر.append('{%s, 탑재자원_%d, %d},'%(json.dumps(نام,ensure_ascii=False),순번,راستہ_2.stat().st_size))
    سرصفحہ_قدر.append('};');(پیمائش_کوائف/'resources.h').write_text('\n'.join(سرصفحہ_قدر)+'\n',encoding='utf-8')
    منزل_مقصود_فائلیں=[]
    for نام in ('번역기.c','عام_زبان_چلت_عرصہ_معاونت.c','چلائیں.c','미리번역.c','되돌림.S'):
        مقصود_فائل=پیمائش_کوائف/(Path(نام).stem+'.o');منزل_مقصود_فائلیں.append(مقصود_فائل)
        نفاذ_کریں_حکم([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/نام,'-o',مقصود_فائل])
    실행파일=روٹ_راہ/'build/user/cc.elf'
    نفاذ_کریں_حکم([연결편집기,'--gc-sections','-T',روٹ_راہ/'صارف/ربط_ترتیب.ld','-z','max-page-size=4096','-o',실행파일,
         روٹ_راہ/'build/user/start.o',روٹ_راہ/'build/user/runtime.o']+منزل_مقصود_فائلیں+
         [روٹ_راہ/'build/user'/نام for نام in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
