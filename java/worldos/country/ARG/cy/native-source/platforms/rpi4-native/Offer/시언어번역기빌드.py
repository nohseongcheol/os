"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(gwraidd_llwybr, 저장소경로, 시언어번역기, 연결편집기, 설정비트, Gweithredu_gorchymyn):
    mesur_data = gwraidd_llwybr / 'build/ccompiler'; mesur_data.mkdir(exist_ok=True)
    원본자료 = gwraidd_llwybr / '시언어번역기'
    외부원문 = gwraidd_llwybr / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = gwraidd_llwybr / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Gosodiadau_VALUE for Gosodiadau_VALUE in 설정비트 if Gosodiadau_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', gwraidd_llwybr/'defnyddiwr', '-I', mesur_data, '-isystem', 개발꾸러미/'usr/include']
    Gweithredu_gorchymyn([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'bwtio_Cymorth.c','-o',mesur_data/'crt.o'])
    Gweithredu_gorchymyn([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',mesur_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_safle.name,data_safle) for data_safle in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_safle.name,data_safle) for data_safle in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_safle.name,data_safle) for data_safle in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',gwraidd_llwybr/'build/user/start.o'),('/sdk/lib/crt.o',mesur_data/'crt.o'),('/sdk/lib/aot-runtime.o',mesur_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',gwraidd_llwybr/'build/libposix-kor-user.a')]
    Pennyn_VALUE=['typedef struct { const char *Enw; const unsigned char *data; unsigned Maint; } 번역기자원;']
    for 순번,(_,LLWYBR) in enumerate(탑재자료):
        Pennyn_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in LLWYBR.read_bytes())))
    Pennyn_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Enw,LLWYBR) in enumerate(탑재자료): Pennyn_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Enw,ensure_ascii=False),순번,LLWYBR.stat().st_size))
    Pennyn_VALUE.append('};');(mesur_data/'resources.h').write_text('\n'.join(Pennyn_VALUE)+'\n',encoding='utf-8')
    cyrchfan_Ffeil=[]
    for Enw in ('번역기.c','amser_rhedeg_iaith_gyffredin_Cymorth.c','Gweithredu_2.c','미리번역.c','return_pont.S'):
        ffeil_derbyn=mesur_data/(Path(Enw).stem+'.o');cyrchfan_Ffeil.append(ffeil_derbyn)
        Gweithredu_gorchymyn([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Enw,'-o',ffeil_derbyn])
    실행파일=gwraidd_llwybr/'build/user/cc.elf'
    Gweithredu_gorchymyn([연결편집기,'--gc-sections','-T',gwraidd_llwybr/'defnyddiwr/Dolen_Llywio.ld','-z','max-page-size=4096','-o',실행파일,
         gwraidd_llwybr/'build/user/start.o',gwraidd_llwybr/'build/user/runtime.o']+cyrchfan_Ffeil+
         [gwraidd_llwybr/'build/user'/Enw for Enw in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
