"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, ýerine_ýetir_buýruk):
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
    설정비트 = [Sazlamalar_baha for Sazlamalar_baha in 설정비트 if Sazlamalar_baha != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', 기준경로/'ulanyjy', '-I', 결과자료, '-isystem', 개발꾸러미/'usr/include']
    ýerine_ýetir_buýruk([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'başlangyç_Goldaw.c','-o',결과자료/'crt.o'])
    ýerine_ýetir_buýruk([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',결과자료/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',기준경로/'build/user/start.o'),('/sdk/lib/crt.o',결과자료/'crt.o'),('/sdk/lib/aot-runtime.o',결과자료/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',기준경로/'build/libposix-kor-user.a')]
    At_baha=['typedef struct { const char *Ad; const unsigned char *maglumat; unsigned Ululyk; } 번역기자원;']
    for 순번,(_,Ýol) in enumerate(탑재자료):
        At_baha.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Ýol.read_bytes())))
    At_baha.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Ad,Ýol) in enumerate(탑재자료): At_baha.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Ad,ensure_ascii=False),순번,Ýol.stat().st_size))
    At_baha.append('};');(결과자료/'resources.h').write_text('\n'.join(At_baha)+'\n',encoding='utf-8')
    barylmaly_ýer_Faýllar=[]
    for Ad in ('번역기.c','umumy_dil_işlediş_gurşawy_Goldaw.c','Bitir.c','미리번역.c','되돌림.S'):
        çykyş_faýly=결과자료/(Path(Ad).stem+'.o');barylmaly_ýer_Faýllar.append(çykyş_faýly)
        ýerine_ýetir_buýruk([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Ad,'-o',çykyş_faýly])
    실행파일=기준경로/'build/user/cc.elf'
    ýerine_ýetir_buýruk([연결편집기,'--gc-sections','-T',기준경로/'ulanyjy/Bag_Ýerleşiş.ld','-z','max-page-size=4096','-o',실행파일,
         기준경로/'build/user/start.o',기준경로/'build/user/runtime.o']+barylmaly_ýer_Faýllar+
         [기준경로/'build/user'/Ad for Ad in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
