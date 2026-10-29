"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(freumh_slighe, 저장소경로, 시언어번역기, 연결편집기, 설정비트, gnìomhaich_àithne):
    tomhas_dàta = freumh_slighe / 'build/ccompiler'; tomhas_dàta.mkdir(exist_ok=True)
    원본자료 = freumh_slighe / '시언어번역기'
    외부원문 = freumh_slighe / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = freumh_slighe / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [roghainnean_VALUE for roghainnean_VALUE in 설정비트 if roghainnean_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', freumh_slighe/'cleachdaiche', '-I', tomhas_dàta, '-isystem', 개발꾸러미/'usr/include']
    gnìomhaich_àithne([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'tòiseachadh_taic.c','-o',tomhas_dàta/'crt.o'])
    gnìomhaich_àithne([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',tomhas_dàta/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+dàta_suidhich.name,dàta_suidhich) for dàta_suidhich in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dàta_suidhich.name,dàta_suidhich) for dàta_suidhich in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+dàta_suidhich.name,dàta_suidhich) for dàta_suidhich in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',freumh_slighe/'build/user/start.o'),('/sdk/lib/crt.o',tomhas_dàta/'crt.o'),('/sdk/lib/aot-runtime.o',tomhas_dàta/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',freumh_slighe/'build/libposix-kor-user.a')]
    bann_cinn_VALUE=['typedef struct { const char *Ainm; const unsigned char *dàta; unsigned atharraich_am_meud; } 번역기자원;']
    for 순번,(_,Slighe) in enumerate(탑재자료):
        bann_cinn_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Slighe.read_bytes())))
    bann_cinn_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Ainm,Slighe) in enumerate(탑재자료): bann_cinn_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Ainm,ensure_ascii=False),순번,Slighe.stat().st_size))
    bann_cinn_VALUE.append('};');(tomhas_dàta/'resources.h').write_text('\n'.join(bann_cinn_VALUE)+'\n',encoding='utf-8')
    ceann_uidhe_faidhlichean=[]
    for Ainm in ('번역기.c','Common_Language_Runtime_taic.c','ruith.c','미리번역.c','return_drochaid.S'):
        faidhle_uidhe=tomhas_dàta/(Path(Ainm).stem+'.o');ceann_uidhe_faidhlichean.append(faidhle_uidhe)
        gnìomhaich_àithne([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Ainm,'-o',faidhle_uidhe])
    실행파일=freumh_slighe/'build/user/cc.elf'
    gnìomhaich_àithne([연결편집기,'--gc-sections','-T',freumh_slighe/'cleachdaiche/ceangal_co_dhealbhachd.ld','-z','max-page-size=4096','-o',실행파일,
         freumh_slighe/'build/user/start.o',freumh_slighe/'build/user/runtime.o']+ceann_uidhe_faidhlichean+
         [freumh_slighe/'build/user'/Ainm for Ainm in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
