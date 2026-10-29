"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(rot_bane, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Utfør_kommando):
    forretningsmål_data = rot_bane / 'build/ccompiler'; forretningsmål_data.mkdir(exist_ok=True)
    원본자료 = rot_bane / '시언어번역기'
    외부원문 = rot_bane / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = rot_bane / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Innstillingar_VALUE for Innstillingar_VALUE in 설정비트 if Innstillingar_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', rot_bane/'brukar', '-I', forretningsmål_data, '-isystem', 개발꾸러미/'usr/include']
    Utfør_kommando([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'oppstart_støtte.c','-o',forretningsmål_data/'crt.o'])
    Utfør_kommando([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',forretningsmål_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_plassere.name,data_plassere) for data_plassere in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_plassere.name,data_plassere) for data_plassere in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_plassere.name,data_plassere) for data_plassere in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rot_bane/'build/user/start.o'),('/sdk/lib/crt.o',forretningsmål_data/'crt.o'),('/sdk/lib/aot-runtime.o',forretningsmål_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rot_bane/'build/libposix-kor-user.a')]
    hode_VALUE=['typedef struct { const char *Namn; const unsigned char *data; unsigned Storleik; } 번역기자원;']
    for 순번,(_,STIGE) in enumerate(탑재자료):
        hode_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in STIGE.read_bytes())))
    hode_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Namn,STIGE) in enumerate(탑재자료): hode_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Namn,ensure_ascii=False),순번,STIGE.stat().st_size))
    hode_VALUE.append('};');(forretningsmål_data/'resources.h').write_text('\n'.join(hode_VALUE)+'\n',encoding='utf-8')
    mål_Filer=[]
    for Namn in ('번역기.c','Common_Language_Runtime_støtte.c','Køyr_2.c','미리번역.c','levere_tilbake_bru.S'):
        målfil=forretningsmål_data/(Path(Namn).stem+'.o');mål_Filer.append(målfil)
        Utfør_kommando([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Namn,'-o',målfil])
    실행파일=rot_bane/'build/user/cc.elf'
    Utfør_kommando([연결편집기,'--gc-sections','-T',rot_bane/'brukar/kople_Oppsett.ld','-z','max-page-size=4096','-o',실행파일,
         rot_bane/'build/user/start.o',rot_bane/'build/user/runtime.o']+mål_Filer+
         [rot_bane/'build/user'/Namn for Namn in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
