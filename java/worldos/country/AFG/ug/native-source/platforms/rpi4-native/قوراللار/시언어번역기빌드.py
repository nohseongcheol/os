"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(يىلتىز_يول, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ئىجرا_قىلىش_بۇيرۇق):
    ئۆلچەم_مەلۇمات = يىلتىز_يول / 'build/ccompiler'; ئۆلچەم_مەلۇمات.mkdir(exist_ok=True)
    원본자료 = يىلتىز_يول / '시언어번역기'
    외부원문 = يىلتىز_يول / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = يىلتىز_يول / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [تەڭشەك_قىممىتى for تەڭشەك_قىممىتى in 설정비트 if تەڭشەك_قىممىتى != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', يىلتىز_يول/'ئىشلەتكۈچى', '-I', ئۆلچەم_مەلۇمات, '-isystem', 개발꾸러미/'usr/include']
    ئىجرا_قىلىش_بۇيرۇق([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'قوزغىتىش_قوللاش.c','-o',ئۆلچەم_مەلۇمات/'crt.o'])
    ئىجرا_قىلىش_بۇيرۇق([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',ئۆلچەم_مەلۇمات/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+مەلۇمات_ئورۇنلاشتۇرۇش.name,مەلۇمات_ئورۇنلاشتۇرۇش) for مەلۇمات_ئورۇنلاشتۇرۇش in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+مەلۇمات_ئورۇنلاشتۇرۇش.name,مەلۇمات_ئورۇنلاشتۇرۇش) for مەلۇمات_ئورۇنلاشتۇرۇش in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+مەلۇمات_ئورۇنلاشتۇرۇش.name,مەلۇمات_ئورۇنلاشتۇرۇش) for مەلۇمات_ئورۇنلاشتۇرۇش in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',يىلتىز_يول/'build/user/start.o'),('/sdk/lib/crt.o',ئۆلچەم_مەلۇمات/'crt.o'),('/sdk/lib/aot-runtime.o',ئۆلچەم_مەلۇمات/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',يىلتىز_يول/'build/libposix-kor-user.a')]
    بېشى_قىممىتى=['typedef struct { const char *ئاتى; const unsigned char *مەلۇمات; unsigned چوڭلۇقى; } 번역기자원;']
    for 순번,(_,يول) in enumerate(탑재자료):
        بېشى_قىممىتى.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in يول.read_bytes())))
    بېشى_قىممىتى.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(ئاتى,يول) in enumerate(탑재자료): بېشى_قىممىتى.append('{%s, 탑재자원_%d, %d},'%(json.dumps(ئاتى,ensure_ascii=False),순번,يول.stat().st_size))
    بېشى_قىممىتى.append('};');(ئۆلچەم_مەلۇمات/'resources.h').write_text('\n'.join(بېشى_قىممىتى)+'\n',encoding='utf-8')
    نىشان_ھۆججەت_417c7a10=[]
    for ئاتى in ('번역기.c','ئورتاق_تىل_ئىجرا_ۋاقتى_قوللاش.c','ئىجرا_قىل_2.c','미리번역.c','قايتۇرۇپ_بېرىش_كۆۋرۈك.S'):
        نىشان_ھۆججەت=ئۆلچەم_مەلۇمات/(Path(ئاتى).stem+'.o');نىشان_ھۆججەت_417c7a10.append(نىشان_ھۆججەت)
        ئىجرا_قىلىش_بۇيرۇق([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/ئاتى,'-o',نىشان_ھۆججەت])
    실행파일=يىلتىز_يول/'build/user/cc.elf'
    ئىجرا_قىلىش_بۇيرۇق([연결편집기,'--gc-sections','-T',يىلتىز_يول/'ئىشلەتكۈچى/ئۇلانما_لايىھە.ld','-z','max-page-size=4096','-o',실행파일,
         يىلتىز_يول/'build/user/start.o',يىلتىز_يول/'build/user/runtime.o']+نىشان_ھۆججەت_417c7a10+
         [يىلتىز_يول/'build/user'/ئاتى for ئاتى in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
