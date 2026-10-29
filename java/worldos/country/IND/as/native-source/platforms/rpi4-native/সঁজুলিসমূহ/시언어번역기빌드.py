"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ৰুট_পথ, 저장소경로, 시언어번역기, 연결편집기, 설정비트, নিষ্পাদন_আদেশ):
    পৰিমাপ_ডাটা = ৰুট_পথ / 'build/ccompiler'; পৰিমাপ_ডাটা.mkdir(exist_ok=True)
    원본자료 = ৰুট_পথ / '시언어번역기'
    외부원문 = ৰুট_পথ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ৰুট_পথ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [ছেটিংছ_মান for ছেটিংছ_মান in 설정비트 if ছেটিংছ_মান != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', ৰুট_পথ/'ব্যৱহাৰকৰ্তা', '-I', পৰিমাপ_ডাটা, '-isystem', 개발꾸러미/'usr/include']
    নিষ্পাদন_আদেশ([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'বুট_সমর্থন.c','-o',পৰিমাপ_ডাটা/'crt.o'])
    নিষ্পাদন_আদেশ([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',পৰিমাপ_ডাটা/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ডাটা_স্থান_সলনি_কৰক.name,ডাটা_স্থান_সলনি_কৰক) for ডাটা_স্থান_সলনি_কৰক in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ডাটা_স্থান_সলনি_কৰক.name,ডাটা_স্থান_সলনি_কৰক) for ডাটা_স্থান_সলনি_কৰক in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ডাটা_স্থান_সলনি_কৰক.name,ডাটা_স্থান_সলনি_কৰক) for ডাটা_স্থান_সলনি_কৰক in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ৰুট_পথ/'build/user/start.o'),('/sdk/lib/crt.o',পৰিমাপ_ডাটা/'crt.o'),('/sdk/lib/aot-runtime.o',পৰিমাপ_ডাটা/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ৰুট_পথ/'build/libposix-kor-user.a')]
    শিৰো_মান=['typedef struct { const char *নাম; const unsigned char *ডাটা; unsigned মাপ; } 번역기자원;']
    for 순번,(_,পথ) in enumerate(탑재자료):
        শিৰো_মান.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in পথ.read_bytes())))
    শিৰো_মান.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(নাম,পথ) in enumerate(탑재자료): শিৰো_মান.append('{%s, 탑재자원_%d, %d},'%(json.dumps(নাম,ensure_ascii=False),순번,পথ.stat().st_size))
    শিৰো_মান.append('};');(পৰিমাপ_ডাটা/'resources.h').write_text('\n'.join(শিৰো_মান)+'\n',encoding='utf-8')
    গন্তব্য_স্থান_ফাইলসমূহ=[]
    for নাম in ('번역기.c','উমৈহতীয়া_ভাষা_ৰানটাইম_সমর্থন.c','সঞ্চালন.c','미리번역.c','되돌림.S'):
        গন্তব্য_ফাইল=পৰিমাপ_ডাটা/(Path(নাম).stem+'.o');গন্তব্য_স্থান_ফাইলসমূহ.append(গন্তব্য_ফাইল)
        নিষ্পাদন_আদেশ([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/নাম,'-o',গন্তব্য_ফাইল])
    실행파일=ৰুট_পথ/'build/user/cc.elf'
    নিষ্পাদন_আদেশ([연결편집기,'--gc-sections','-T',ৰুট_পথ/'ব্যৱহাৰকৰ্তা/লিংক_লেআউট.ld','-z','max-page-size=4096','-o',실행파일,
         ৰুট_পথ/'build/user/start.o',ৰুট_পথ/'build/user/runtime.o']+গন্তব্য_স্থান_ফাইলসমূহ+
         [ৰুট_পথ/'build/user'/নাম for নাম in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
