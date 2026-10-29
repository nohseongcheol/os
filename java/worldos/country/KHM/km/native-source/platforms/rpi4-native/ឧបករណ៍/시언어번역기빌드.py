"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(ឬស_ផ្លូវ, ឃ្លាំង_ផ្ទុក_ផ្លូវ, 시언어번역기, 연결편집기, ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ, អនុវត្ត_ពាក្យបញ្ជា):
    ការវាស់វែង_ទិន្នន័យ = ឬស_ផ្លូវ / 'build/ccompiler'; ការវាស់វែង_ទិន្នន័យ.mkdir(exist_ok=True)
    원본자료 = ឬស_ផ្លូវ / '시언어번역기'
    ប្រច្រាស់ទិស = ឬស_ផ្លូវ / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = ឬស_ផ្លូវ / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ = [ការកំណត់_តំលៃ for ការកំណត់_តំលៃ in ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ if ការកំណត់_តំលៃ != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', ប្រច្រាស់ទិស, '-I', ឬស_ផ្លូវ/'អ្នកប្រើ', '-I', ការវាស់វែង_ទិន្នន័យ, '-isystem', 개발꾸러미/'usr/include']
    អនុវត្ត_ពាក្យបញ្ជា([시언어번역기]+ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ការចាប់ផ្តើម_ទម្រ.c','-o',ការវាស់វែង_ទិន្នន័យ/'crt.o'])
    អនុវត្ត_ពាក្យបញ្ជា([시언어번역기]+ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ+['-I',ឃ្លាំង_ផ្ទុក_ផ្លូវ/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ការវាស់វែង_ទិន្នន័យ/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+ទិន្នន័យ_កំណត់ទីតាំង.name,ទិន្នន័យ_កំណត់ទីតាំង) for ទិន្នន័យ_កំណត់ទីតាំង in sorted((ឃ្លាំង_ផ្ទុក_ផ្លូវ/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ទិន្នន័យ_កំណត់ទីតាំង.name,ទិន្នន័យ_កំណត់ទីតាំង) for ទិន្នន័យ_កំណត់ទីតាំង in sorted((ប្រច្រាស់ទិស/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+ទិន្នន័យ_កំណត់ទីតាំង.name,ទិន្នន័យ_កំណត់ទីតាំង) for ទិន្នន័យ_កំណត់ទីតាំង in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',ឬស_ផ្លូវ/'build/user/start.o'),('/sdk/lib/crt.o',ការវាស់វែង_ទិន្នន័យ/'crt.o'),('/sdk/lib/aot-runtime.o',ការវាស់វែង_ទិន្នន័យ/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',ឬស_ផ្លូវ/'build/libposix-kor-user.a')]
    បឋមកថា_តំលៃ=['typedef struct { const char *ឈ្មោះ; const unsigned char *ទិន្នន័យ; unsigned ដាក់ទំហំ; } 번역기자원;']
    for 순번,(_,ផ្លូវ) in enumerate(탑재자료):
        បឋមកថា_តំលៃ.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ផ្លូវ.read_bytes())))
    បឋមកថា_តំលៃ.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ឈ្មោះ,ផ្លូវ) in enumerate(탑재자료): បឋមកថា_តំលៃ.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ឈ្មោះ,ensure_ascii=False),순번,ផ្លូវ.stat().st_size))
    បឋមកថា_តំលៃ.append('};');(ការវាស់វែង_ទិន្នន័យ/'resources.h').write_text('\n'.join(បឋមកថា_តំលៃ)+'\n',encoding='utf-8')
    ទិសដៅ_ឯកសារ=[]
    for ឈ្មោះ in ('번역기.c','ដំណើរការភាសាទូទៅ_ទម្រ.c','រត់.c','미리번역.c','되돌림.S'):
        ទិសដៅឯកសារ=ការវាស់វែង_ទិន្នន័យ/(Path(ឈ្មោះ).stem+'.o');ទិសដៅ_ឯកសារ.append(ទិសដៅឯកសារ)
        អនុវត្ត_ពាក្យបញ្ជា([시언어번역기]+ការរៀបចំ_សេវាកម្ម_ផ្ទេរ_ឆ្លាតវៃ_នៅ_ផ្ទៃ_ខាង_ក្រោយ+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ឈ្មោះ,'-o',ទិសដៅឯកសារ])
    실행파일=ឬស_ផ្លូវ/'build/user/cc.elf'
    អនុវត្ត_ពាក្យបញ្ជា([연결편집기,'--gc-sections','-T',ឬស_ផ្លូវ/'អ្នកប្រើ/តំណ_ប្លង់.ld','-z','max-page-size=4096','-o',실행파일,
         ឬស_ផ្លូវ/'build/user/start.o',ឬស_ផ្លូវ/'build/user/runtime.o']+ទិសដៅ_ឯកសារ+
         [ឬស_ផ្លូវ/'build/user'/ឈ្មោះ for ឈ្មោះ in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
