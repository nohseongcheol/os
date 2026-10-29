"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(মূল_পথ, সংগ্রহস্থলের_পথ, 시언어번역기, 연결편집기, বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস, কার্যকর_করুন_আদেশ):
    পরিমাপ_ডাটা = মূল_পথ / 'build/ccompiler'; পরিমাপ_ডাটা.mkdir(exist_ok=True)
    원본자료 = মূল_পথ / '시언어번역기'
    আপস্ট্রীম = মূল_পথ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = মূল_পথ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস = [সেটিংস_মান for সেটিংস_মান in বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস if সেটিংস_মান != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', আপস্ট্রীম, '-I', মূল_পথ/'ব্যবহারকারী', '-I', পরিমাপ_ডাটা, '-isystem', 개발꾸러미/'usr/include']
    কার্যকর_করুন_আদেশ([시언어번역기]+বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'বুট_সমর্থন.c','-o',পরিমাপ_ডাটা/'crt.o'])
    কার্যকর_করুন_আদেশ([시언어번역기]+বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস+['-I',সংগ্রহস্থলের_পথ/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',পরিমাপ_ডাটা/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ডাটা_পদ.name,ডাটা_পদ) for ডাটা_পদ in sorted((সংগ্রহস্থলের_পথ/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ডাটা_পদ.name,ডাটা_পদ) for ডাটা_পদ in sorted((আপস্ট্রীম/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ডাটা_পদ.name,ডাটা_পদ) for ডাটা_পদ in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',মূল_পথ/'build/user/start.o'),('/sdk/lib/crt.o',পরিমাপ_ডাটা/'crt.o'),('/sdk/lib/aot-runtime.o',পরিমাপ_ডাটা/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',মূল_পথ/'build/libposix-kor-user.a')]
    হেডার_মান=['typedef struct { const char *নাম; const unsigned char *ডাটা; unsigned আকার; } 번역기자원;']
    for 순번,(_,পথ_2) in enumerate(탑재자료):
        হেডার_মান.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in পথ_2.read_bytes())))
    হেডার_মান.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(নাম,পথ_2) in enumerate(탑재자료): হেডার_মান.append('{%s, 탑재자원_%d, %d},'%(json.dumps(নাম,ensure_ascii=False),순번,পথ_2.stat().st_size))
    হেডার_মান.append('};');(পরিমাপ_ডাটা/'resources.h').write_text('\n'.join(হেডার_মান)+'\n',encoding='utf-8')
    গন্তব্য_ফাইলগুলি=[]
    for নাম in ('번역기.c','সাধারণ_ভাষা_রানটাইম_সমর্থন.c','চালনা.c','미리번역.c','되돌림.S'):
        গন্তব্য_ফাইল=পরিমাপ_ডাটা/(Path(নাম).stem+'.o');গন্তব্য_ফাইলগুলি.append(গন্তব্য_ফাইল)
        কার্যকর_করুন_আদেশ([시언어번역기]+বিন্যাসন_ব্যাকগ্রাউন্ড_ইনটেলিজেন্ট_ট্র্যান্সফার_সার্ভিস+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/নাম,'-o',গন্তব্য_ফাইল])
    실행파일=মূল_পথ/'build/user/cc.elf'
    কার্যকর_করুন_আদেশ([연결편집기,'--gc-sections','-T',মূল_পথ/'ব্যবহারকারী/লিংক_লেআউট.ld','-z','max-page-size=4096','-o',실행파일,
         মূল_পথ/'build/user/start.o',মূল_পথ/'build/user/runtime.o']+গন্তব্য_ফাইলগুলি+
         [মূল_পথ/'build/user'/নাম for নাম in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
