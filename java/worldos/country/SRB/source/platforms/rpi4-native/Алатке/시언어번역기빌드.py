"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(корен_пут, депо_пут, 시언어번역기, 연결편집기, конфигурација_Услуга_интелигентног_преноса_у_позадини, Изврши_команда):
    мера_подаци = корен_пут / 'build/ccompiler'; мера_подаци.mkdir(exist_ok=True)
    원본자료 = корен_пут / '시언어번역기'
    изворни = корен_пут / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = корен_пут / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    конфигурација_Услуга_интелигентног_преноса_у_позадини = [Поставке_вриједност for Поставке_вриједност in конфигурација_Услуга_интелигентног_преноса_у_позадини if Поставке_вриједност != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', изворни, '-I', корен_пут/'корисник', '-I', мера_подаци, '-isystem', 개발꾸러미/'usr/include']
    Изврши_команда([시언어번역기]+конфигурација_Услуга_интелигентног_преноса_у_позадини+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'покретање_Подршка.c','-o',мера_подаци/'crt.o'])
    Изврши_команда([시언어번역기]+конфигурација_Услуга_интелигентног_преноса_у_позадини+['-I',депо_пут/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',мера_подаци/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+подаци_позиција.name,подаци_позиција) for подаци_позиција in sorted((депо_пут/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+подаци_позиција.name,подаци_позиција) for подаци_позиција in sorted((изворни/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+подаци_позиција.name,подаци_позиција) for подаци_позиција in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',корен_пут/'build/user/start.o'),('/sdk/lib/crt.o',мера_подаци/'crt.o'),('/sdk/lib/aot-runtime.o',мера_подаци/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',корен_пут/'build/libposix-kor-user.a')]
    Заглавље_вриједност=['typedef struct { const char *Назив; const unsigned char *подаци; unsigned Величина; } 번역기자원;']
    for 순번,(_,ПУТАЊА) in enumerate(탑재자료):
        Заглавље_вриједност.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ПУТАЊА.read_bytes())))
    Заглавље_вриједност.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Назив,ПУТАЊА) in enumerate(탑재자료): Заглавље_вриједност.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Назив,ensure_ascii=False),순번,ПУТАЊА.stat().st_size))
    Заглавље_вриједност.append('};');(мера_подаци/'resources.h').write_text('\n'.join(Заглавље_вриједност)+'\n',encoding='utf-8')
    одредиште_Фајлови=[]
    for Назив in ('번역기.c','заједничка_извршна_језичка_компонента_Подршка.c','Покрени.c','미리번역.c','вратити_мост.S'):
        одредишни_фајл=мера_подаци/(Path(Назив).stem+'.o');одредиште_Фајлови.append(одредишни_фајл)
        Изврши_команда([시언어번역기]+конфигурација_Услуга_интелигентног_преноса_у_позадини+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Назив,'-o',одредишни_фајл])
    실행파일=корен_пут/'build/user/cc.elf'
    Изврши_команда([연결편집기,'--gc-sections','-T',корен_пут/'корисник/Веза_изглед.ld','-z','max-page-size=4096','-o',실행파일,
         корен_пут/'build/user/start.o',корен_пут/'build/user/runtime.o']+одредиште_Фајлови+
         [корен_пут/'build/user'/Назив for Назив in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
