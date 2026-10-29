"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(тамыр_юл, 저장소경로, 시언어번역기, 연결편집기, 설정비트, үтәргә_команда):
    үлчәм_мәгълүмат = тамыр_юл / 'build/ccompiler'; үлчәм_мәгълүмат.mkdir(exist_ok=True)
    원본자료 = тамыр_юл / '시언어번역기'
    외부원문 = тамыр_юл / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = тамыр_юл / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    설정비트 = [Параметрлар_VALUE for Параметрлар_VALUE in 설정비트 if Параметрлар_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', 외부원문, '-I', тамыр_юл/'кулланучы', '-I', үлчәм_мәгълүмат, '-isystem', 개발꾸러미/'usr/include']
    үтәргә_команда([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'йөкләү_ярдәм.c','-o',үлчәм_мәгълүмат/'crt.o'])
    үтәргә_команда([시언어번역기]+설정비트+['-I',저장소경로/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',үлчәм_мәгълүмат/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+мәгълүмат_урнаштыру.name,мәгълүмат_урнаштыру) for мәгълүмат_урнаштыру in sorted((저장소경로/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+мәгълүмат_урнаштыру.name,мәгълүмат_урнаштыру) for мәгълүмат_урнаштыру in sorted((외부원문/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+мәгълүмат_урнаштыру.name,мәгълүмат_урнаштыру) for мәгълүмат_урнаштыру in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',тамыр_юл/'build/user/start.o'),('/sdk/lib/crt.o',үлчәм_мәгълүмат/'crt.o'),('/sdk/lib/aot-runtime.o',үлчәм_мәгълүмат/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',тамыр_юл/'build/libposix-kor-user.a')]
    Башлама_VALUE=['typedef struct { const char *исем; const unsigned char *мәгълүмат; unsigned үлчәмен_үзгәртү; } 번역기자원;']
    for 순번,(_,Yul) in enumerate(탑재자료):
        Башлама_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in Yul.read_bytes())))
    Башлама_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(исем,Yul) in enumerate(탑재자료): Башлама_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(исем,ensure_ascii=False),순번,Yul.stat().st_size))
    Башлама_VALUE.append('};');(үлчәм_мәгълүмат/'resources.h').write_text('\n'.join(Башлама_VALUE)+'\n',encoding='utf-8')
    күчерү_урыны_Файллар=[]
    for исем in ('번역기.c','CLR_мохите_ярдәм.c','эшләтү.c','미리번역.c','кайтару_күпер.S'):
        максат_файл=үлчәм_мәгълүмат/(Path(исем).stem+'.o');күчерү_урыны_Файллар.append(максат_файл)
        үтәргә_команда([시언어번역기]+설정비트+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/исем,'-o',максат_файл])
    실행파일=тамыр_юл/'build/user/cc.elf'
    үтәргә_команда([연결편집기,'--gc-sections','-T',тамыр_юл/'кулланучы/бәйләү_план.ld','-z','max-page-size=4096','-o',실행파일,
         тамыр_юл/'build/user/start.o',тамыр_юл/'build/user/runtime.o']+күчерү_урыны_Файллар+
         [тамыр_юл/'build/user'/исем for исем in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
