"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(корен_път, хранилище_път, 시언어번역기, 연결편집기, конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим, изпълнявам_команда):
    мярка_данни = корен_път / 'build/ccompiler'; мярка_данни.mkdir(exist_ok=True)
    원본자료 = корен_път / '시언어번역기'
    начален = корен_път / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    развоен_пакет = корен_път / 'vendor/sdk'
    if not (развоен_пакет/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((развоен_пакет/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим = [Настройки_стойност for Настройки_стойност in конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим if Настройки_стойност != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', начален, '-I', корен_път/'потребител', '-I', мярка_данни, '-isystem', развоен_пакет/'usr/include']
    изпълнявам_команда([시언어번역기]+конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'начално_зареждане_на_ОС_Поддръжка.c','-o',мярка_данни/'crt.o'])
    изпълнявам_команда([시언어번역기]+конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим+['-I',хранилище_път/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',мярка_данни/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+данни_позиция.name,данни_позиция) for данни_позиция in sorted((хранилище_път/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+данни_позиция.name,данни_позиция) for данни_позиция in sorted((начален/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+данни_позиция.name,данни_позиция) for данни_позиция in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',корен_път/'build/user/start.o'),('/sdk/lib/crt.o',мярка_данни/'crt.o'),('/sdk/lib/aot-runtime.o',мярка_данни/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',корен_път/'build/libposix-kor-user.a')]
    Заглавка_стойност=['typedef struct { const char *Име; const unsigned char *данни; unsigned Размер; } компилатор_ресурс;']
    for 순번,(_,ПЪТ) in enumerate(탑재자료):
        Заглавка_стойност.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ПЪТ.read_bytes())))
    Заглавка_стойност.append('static const компилатор_ресурс компилатор_Ресурси[] = {')
    for 순번,(Име,ПЪТ) in enumerate(탑재자료): Заглавка_стойност.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Име,ensure_ascii=False),순번,ПЪТ.stat().st_size))
    Заглавка_стойност.append('};');(мярка_данни/'resources.h').write_text('\n'.join(Заглавка_стойност)+'\n',encoding='utf-8')
    местоназначение_Файлове=[]
    for Име in ('компилатор_инструмент.c','обща_езикова_среда_Поддръжка.c','Стартиране.c','미리번역.c','връщам_мост.S'):
        файл_местоназначение=мярка_данни/(Path(Име).stem+'.o');местоназначение_Файлове.append(файл_местоназначение)
        изпълнявам_команда([시언어번역기]+конфигурация_Услуга_за_интелигентно_прехвърляне_във_фонов_режим+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Име,'-o',файл_местоназначение])
    실행파일=корен_път/'build/user/cc.elf'
    изпълнявам_команда([연결편집기,'--gc-sections','-T',корен_път/'потребител/Връзка_схема.ld','-z','max-page-size=4096','-o',실행파일,
         корен_път/'build/user/start.o',корен_път/'build/user/runtime.o']+местоназначение_Файлове+
         [корен_път/'build/user'/Име for Име in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
