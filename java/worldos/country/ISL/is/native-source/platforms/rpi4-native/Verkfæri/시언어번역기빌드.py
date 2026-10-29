"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(rót_slóð_3f268910, gagnageymsla_slóð, 시언어번역기, 연결편집기, afbrigði_Background_Intelligent_Transfer_Service, keyra_skipun):
    mæld_stærð_gögn = rót_slóð_3f268910 / 'build/ccompiler'; mæld_stærð_gögn.mkdir(exist_ok=True)
    원본자료 = rót_slóð_3f268910 / '시언어번역기'
    fyrir_ofan = rót_slóð_3f268910 / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = rót_slóð_3f268910 / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    afbrigði_Background_Intelligent_Transfer_Service = [Stillingar_VALUE for Stillingar_VALUE in afbrigði_Background_Intelligent_Transfer_Service if Stillingar_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', fyrir_ofan, '-I', rót_slóð_3f268910/'notandi', '-I', mæld_stærð_gögn, '-isystem', 개발꾸러미/'usr/include']
    keyra_skipun([시언어번역기]+afbrigði_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'ræsa_Aðstoð.c','-o',mæld_stærð_gögn/'crt.o'])
    keyra_skipun([시언어번역기]+afbrigði_Background_Intelligent_Transfer_Service+['-I',gagnageymsla_slóð/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'AOT_CLR.c','-o',mæld_stærð_gögn/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+gögn_staða.name,gögn_staða) for gögn_staða in sorted((gagnageymsla_slóð/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+gögn_staða.name,gögn_staða) for gögn_staða in sorted((fyrir_ofan/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+gögn_staða.name,gögn_staða) for gögn_staða in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',rót_slóð_3f268910/'build/user/start.o'),('/sdk/lib/crt.o',mæld_stærð_gögn/'crt.o'),('/sdk/lib/aot-runtime.o',mæld_stærð_gögn/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',rót_slóð_3f268910/'build/libposix-kor-user.a')]
    Haus_VALUE=['typedef struct { const char *Heiti; const unsigned char *gögn; unsigned Stærð; } 번역기자원;']
    for 순번,(_,SLÓÐ) in enumerate(탑재자료):
        Haus_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in SLÓÐ.read_bytes())))
    Haus_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Heiti,SLÓÐ) in enumerate(탑재자료): Haus_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Heiti,ensure_ascii=False),순번,SLÓÐ.stat().st_size))
    Haus_VALUE.append('};');(mæld_stærð_gögn/'resources.h').write_text('\n'.join(Haus_VALUE)+'\n',encoding='utf-8')
    endastaður_Skrár=[]
    for Heiti in ('번역기.c','CLR_Aðstoð.c','Keyra_2.c','미리번역.c','skila_brú.S'):
        viðtökuskrá=mæld_stærð_gögn/(Path(Heiti).stem+'.o');endastaður_Skrár.append(viðtökuskrá)
        keyra_skipun([시언어번역기]+afbrigði_Background_Intelligent_Transfer_Service+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Heiti,'-o',viðtökuskrá])
    실행파일=rót_slóð_3f268910/'build/user/cc.elf'
    keyra_skipun([연결편집기,'--gc-sections','-T',rót_slóð_3f268910/'notandi/tengja_útlit.ld','-z','max-page-size=4096','-o',실행파일,
         rót_slóð_3f268910/'build/user/start.o',rót_slóð_3f268910/'build/user/runtime.o']+endastaður_Skrár+
         [rót_slóð_3f268910/'build/user'/Heiti for Heiti in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
