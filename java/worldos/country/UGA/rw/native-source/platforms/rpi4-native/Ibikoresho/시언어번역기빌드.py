"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(기준경로, 저장소경로, 시언어번역기, 연결편집기, 설정비트, gukora_ibwiriza):
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
    설정비트 = [Amagenamiterere_agaciro for Amagenamiterere_agaciro in 설정비트 if Amagenamiterere_agaciro != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', 기준경로/'ukoresha', '-I', 결과자료, '-isystem', 개발꾸러미/'usr/include']
    gukora_ibwiriza([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'iyatsa_Ubufasha.c','-o',결과자료/'crt.o'])
    gukora_ibwiriza([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',결과자료/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+자료위치.name,자료위치) for 자료위치 in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',기준경로/'build/user/start.o'),('/sdk/lib/crt.o',결과자료/'crt.o'),('/sdk/lib/aot-runtime.o',결과자료/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',기준경로/'build/libposix-kor-user.a')]
    Umutwengaruka_agaciro=['typedef struct { const char *Izina; const unsigned char *amakurushingiro; unsigned Ingano; } 번역기자원;']
    for 순번,(_,Inzira) in enumerate(탑재자료):
        Umutwengaruka_agaciro.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Inzira.read_bytes())))
    Umutwengaruka_agaciro.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Izina,Inzira) in enumerate(탑재자료): Umutwengaruka_agaciro.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Izina,ensure_ascii=False),순번,Inzira.stat().st_size))
    Umutwengaruka_agaciro.append('};');(결과자료/'resources.h').write_text('\n'.join(Umutwengaruka_agaciro)+'\n',encoding='utf-8')
    aho_ijya_Dosiye=[]
    for Izina in ('번역기.c','igihe_ururimi_rukorwamo_Ubufasha.c','ihuriro.c','미리번역.c','되돌림.S'):
        dosiye_yerekezwaho=결과자료/(Path(Izina).stem+'.o');aho_ijya_Dosiye.append(dosiye_yerekezwaho)
        gukora_ibwiriza([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Izina,'-o',dosiye_yerekezwaho])
    실행파일=기준경로/'build/user/cc.elf'
    gukora_ibwiriza([연결편집기,'--gc-sections','-T',기준경로/'ukoresha/Ihuza_Imimerere.ld','-z','max-page-size=4096','-o',실행파일,
         기준경로/'build/user/start.o',기준경로/'build/user/runtime.o']+aho_ijya_Dosiye+
         [기준경로/'build/user'/Izina for Izina in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
