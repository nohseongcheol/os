"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, نفاذ_کرو_حکم):
    결과자료 = 기준경로 / 'build/ccompiler'; 결과자료.mkdir(exist_ok=True)
    원본자료 = 기준경로 / '시언어번역기'
    외부원문 = 기준경로 / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = 기준경로 / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [سیٹنگاں_قدر for سیٹنگاں_قدر in 설정비트 if سیٹنگاں_قدر != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', 기준경로/'صارف', '-I', 결과자료, '-isystem', 개발꾸러미/'usr/include']
    نفاذ_کرو_حکم([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'آغاز_مدد.c','-o',결과자료/'crt.o'])
    نفاذ_کرو_حکم([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',결과자료/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',기준경로/'build/user/start.o'),('/sdk/lib/crt.o',결과자료/'crt.o'),('/sdk/lib/aot-runtime.o',결과자료/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',기준경로/'build/libposix-kor-user.a')]
    سرتحریر_قدر=['typedef struct { const char *ناں; const unsigned char *کوائف; unsigned سائز; } 번역기자원;']
    for 순번,(_,راہ) in enumerate(탑재자료):
        سرتحریر_قدر.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in راہ.read_bytes())))
    سرتحریر_قدر.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ناں,راہ) in enumerate(탑재자료): سرتحریر_قدر.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ناں,ensure_ascii=False),순번,راہ.stat().st_size))
    سرتحریر_قدر.append('};');(결과자료/'resources.h').write_text('\n'.join(سرتحریر_قدر)+'\n',encoding='utf-8')
    منزل_مقصود_فائلاں=[]
    for ناں in ('번역기.c','عام_زبان_چلانڑ_لگیان_مدد.c','چلاؤ.c','미리번역.c','되돌림.S'):
        منزل_فائل=결과자료/(Path(ناں).stem+'.o');منزل_مقصود_فائلاں.append(منزل_فائل)
        نفاذ_کرو_حکم([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ناں,'-o',منزل_فائل])
    실행파일=기준경로/'build/user/cc.elf'
    نفاذ_کرو_حکم([연결편집기,'--gc-sections','-T',기준경로/'صارف/ربط_لے_آؤٹ.ld','-z','max-page-size=4096','-o',실행파일,
         기준경로/'build/user/start.o',기준경로/'build/user/runtime.o']+منزل_مقصود_فائلاں+
         [기준경로/'build/user'/ناں for ناں in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
