"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Cဘာသာပြန်စက်ဖန်တီး(အမြစ်လမ်းကြောင်း, 저장소경로, Cဘာသာပြန်စက်, ချိတ်ဆက်စက်ကိရိယာတစ်ခု, ပြင်ဆင်မှုဘစ်များ, စက်မောင်း):
    ရလဒ်ဒေတာ = အမြစ်လမ်းကြောင်း / 'build/ccompiler'; ရလဒ်ဒေတာ.mkdir(exist_ok=True)
    မူရင်းဒေတာ = အမြစ်လမ်းကြောင်း / 'Cဘာသာပြန်စက်'
    외부원문 = အမြစ်လမ်းကြောင်း / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = အမြစ်လမ်းကြောင်း / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    ပြင်ဆင်မှုဘစ်များ = [သတ်မှတ်ချက်တန်ဖိုး for သတ်မှတ်ချက်တန်ဖိုး in ပြင်ဆင်မှုဘစ်များ if သတ်မှတ်ချက်တန်ဖိုး != '-mgeneral-regs-only']
    포함인수 = ['-I', မူရင်းဒေတာ, '-I', 외부원문, '-I', အမြစ်လမ်းကြောင်း/'သုံးစွဲသူ', '-I', ရလဒ်ဒေတာ, '-isystem', 개발꾸러미/'usr/include']
    စက်မောင်း([Cဘာသာပြန်စက်]+ပြင်ဆင်မှုဘစ်များ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',မူရင်းဒေတာ/'시작지원.c','-o',ရလဒ်ဒေတာ/'crt.o'])
    စက်မောင်း([Cဘာသာပြန်စက်]+ပြင်ဆင်မှုဘစ်များ+['-I',저장소경로/'posix-kor/arm64-native/ခေါင်းစီးဖိုင်']+포함인수+['-c',မူရင်းဒေတာ/'ကြိုတင်ဘာသာပြန်လည်ပတ်ဝန်းကျင်.c','-o',ရလဒ်ဒေတာ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ဒေတာနေရာ.name,ဒေတာနေရာ) for ဒေတာနေရာ in sorted((저장소경로/'posix-kor/arm64-native/ခေါင်းစီးဖိုင်').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ဒေတာနေရာ.name,ဒေတာနေရာ) for ဒေတာနေရာ in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ဒေတာနေရာ.name,ဒေတာနေရာ) for ဒေတာနေရာ in sorted((မူရင်းဒေတာ/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',အမြစ်လမ်းကြောင်း/'build/user/start.o'),('/sdk/lib/crt.o',ရလဒ်ဒေတာ/'crt.o'),('/sdk/lib/aot-runtime.o',ရလဒ်ဒေတာ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',အမြစ်လမ်းကြောင်း/'build/libposix-kor-user.a')]
    ခေါင်းစီးတန်ဖိုး=['typedef struct { const char *အမည်; const unsigned char *ဒေတာ; unsigned အရွယ်; } ဘာသာပြန်စက်အရင်းအမြစ်;']
    for အစဉ်အမှတ်,(_,လမ်း) in enumerate(탑재자료):
        ခေါင်းစီးတန်ဖိုး.append('static const unsigned char 탑재자원_%d[] = {%s};'%(အစဉ်အမှတ်,','.join(str(ယာယီဒေတာ) for ယာယီဒေတာ in လမ်း.read_bytes())))
    ခေါင်းစီးတန်ဖိုး.append('static const ဘာသာပြန်စက်အရင်းအမြစ် 번역기자원들[] = {')
    for အစဉ်အမှတ်,(အမည်,လမ်း) in enumerate(탑재자료): ခေါင်းစီးတန်ဖိုး.append('{%s, 탑재자원_%d, %d},'%(json.dumps(အမည်,ensure_ascii=False),အစဉ်အမှတ်,လမ်း.stat().st_size))
    ခေါင်းစီးတန်ဖိုး.append('};');(ရလဒ်ဒေတာ/'resources.h').write_text('\n'.join(ခေါင်းစီးတန်ဖိုး)+'\n',encoding='utf-8')
    ဦးတည်ရာဖိုင်များ=[]
    for အမည် in ('ဘာသာပြန်စက်ကိရိယာတစ်ခု.c','လည်ပတ်ဝန်းကျင်ထောက်ပံ့မှု.c','လုပ်ဆောင်.c','미리번역.c','ပြန်ပေးတံတား.S'):
        ဦးတည်ရာဖိုင်=ရလဒ်ဒေတာ/(Path(အမည်).stem+'.o');ဦးတည်ရာဖိုင်များ.append(ဦးတည်ရာဖိုင်)
        စက်မောင်း([Cဘာသာပြန်စက်]+ပြင်ဆင်မှုဘစ်များ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',မူရင်းဒေတာ/အမည်,'-o',ဦးတည်ရာဖိုင်])
    စက်ဖိုင်ဖိုင်=အမြစ်လမ်းကြောင်း/'build/user/cc.elf'
    စက်မောင်း([ချိတ်ဆက်စက်ကိရိယာတစ်ခု,'--gc-sections','-T',အမြစ်လမ်းကြောင်း/'သုံးစွဲသူ/နေရာချထားပုံ.ld','-z','max-page-size=4096','-o',စက်ဖိုင်ဖိုင်,
         အမြစ်လမ်းကြောင်း/'build/user/start.o',အမြစ်လမ်းကြောင်း/'build/user/runtime.o']+ဦးတည်ရာဖိုင်များ+
         [အမြစ်လမ်းကြောင်း/'build/user'/အမည် for အမည် in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
