"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(wortel_pad, bewaarplek_pad, 시언어번역기, 연결편집기, konfigurasie_Agtergrond_intelligente_oordragdiens, uitvoer_bevel):
    maatreël_data = wortel_pad / 'build/ccompiler'; maatreël_data.mkdir(exist_ok=True)
    원본자료 = wortel_pad / '시언어번역기'
    stroomop = wortel_pad / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = wortel_pad / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    konfigurasie_Agtergrond_intelligente_oordragdiens = [Instellings_VALUE for Instellings_VALUE in konfigurasie_Agtergrond_intelligente_oordragdiens if Instellings_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', stroomop, '-I', wortel_pad/'gebruiker', '-I', maatreël_data, '-isystem', 개발꾸러미/'usr/include']
    uitvoer_bevel([시언어번역기]+konfigurasie_Agtergrond_intelligente_oordragdiens+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'selflaai_Bystand.c','-o',maatreël_data/'crt.o'])
    uitvoer_bevel([시언어번역기]+konfigurasie_Agtergrond_intelligente_oordragdiens+['-I',bewaarplek_pad/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',maatreël_data/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+data_plaas.name,data_plaas) for data_plaas in sorted((bewaarplek_pad/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_plaas.name,data_plaas) for data_plaas in sorted((stroomop/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+data_plaas.name,data_plaas) for data_plaas in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',wortel_pad/'build/user/start.o'),('/sdk/lib/crt.o',maatreël_data/'crt.o'),('/sdk/lib/aot-runtime.o',maatreël_data/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',wortel_pad/'build/libposix-kor-user.a')]
    Loopkop_VALUE=['typedef struct { const char *Naam; const unsigned char *data; unsigned Grootte; } 번역기자원;']
    for 순번,(_,Pad) in enumerate(탑재자료):
        Loopkop_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Pad.read_bytes())))
    Loopkop_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Naam,Pad) in enumerate(탑재자료): Loopkop_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Naam,ensure_ascii=False),순번,Pad.stat().st_size))
    Loopkop_VALUE.append('};');(maatreël_data/'resources.h').write_text('\n'.join(Loopkop_VALUE)+'\n',encoding='utf-8')
    bestemming_Lêers=[]
    for Naam in ('번역기.c','algemene_taallooptyd_Bystand.c','Loop.c','미리번역.c','teruggee_brug.S'):
        bestemmingslêer=maatreël_data/(Path(Naam).stem+'.o');bestemming_Lêers.append(bestemmingslêer)
        uitvoer_bevel([시언어번역기]+konfigurasie_Agtergrond_intelligente_oordragdiens+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Naam,'-o',bestemmingslêer])
    실행파일=wortel_pad/'build/user/cc.elf'
    uitvoer_bevel([연결편집기,'--gc-sections','-T',wortel_pad/'gebruiker/Skakel_Uitleg.ld','-z','max-page-size=4096','-o',실행파일,
         wortel_pad/'build/user/start.o',wortel_pad/'build/user/runtime.o']+bestemming_Lêers+
         [wortel_pad/'build/user'/Naam for Naam in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
