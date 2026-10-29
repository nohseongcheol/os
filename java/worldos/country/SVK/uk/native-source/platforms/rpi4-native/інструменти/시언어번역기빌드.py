"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(корінь_шлях, репозиторій_шлях, 시언어번역기, 연결편집기, конфігурація_служба_фонового_передавання_файлів, Виконати_команда):
    КР_дані = корінь_шлях / 'build/ccompiler'; КР_дані.mkdir(exist_ok=True)
    원본자료 = корінь_шлях / '시언어번역기'
    початковий = корінь_шлях / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    пакет_розробки = корінь_шлях / 'vendor/sdk'
    if not (пакет_розробки/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((пакет_розробки/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    конфігурація_служба_фонового_передавання_файлів = [Настройки_значення for Настройки_значення in конфігурація_служба_фонового_передавання_файлів if Настройки_значення != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', початковий, '-I', корінь_шлях/'простір_користувача', '-I', КР_дані, '-isystem', пакет_розробки/'usr/include']
    Виконати_команда([시언어번역기]+конфігурація_служба_фонового_передавання_файлів+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'завантаження_опора.c','-o',КР_дані/'crt.o'])
    Виконати_команда([시언어번역기]+конфігурація_служба_фонового_передавання_файлів+['-I',репозиторій_шлях/'posix-kor/arm64-native/оголошення']+포함인수+['-c',원본자료/'미리번역실행.c','-o',КР_дані/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+дані_посада.name,дані_посада) for дані_посада in sorted((репозиторій_шлях/'posix-kor/arm64-native/оголошення').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+дані_посада.name,дані_посада) for дані_посада in sorted((початковий/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+дані_посада.name,дані_посада) for дані_посада in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',корінь_шлях/'build/user/start.o'),('/sdk/lib/crt.o',КР_дані/'crt.o'),('/sdk/lib/aot-runtime.o',КР_дані/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',корінь_шлях/'build/libposix-kor-user.a')]
    Заголовок_значення=['typedef struct { const char *Назва; const unsigned char *дані; unsigned Розмір; } компілятор_ресурс;']
    for 순번,(_,шлях) in enumerate(탑재자료):
        Заголовок_значення.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in шлях.read_bytes())))
    Заголовок_значення.append('static const компілятор_ресурс компілятор_Ресурси[] = {')
    for 순번,(Назва,шлях) in enumerate(탑재자료): Заголовок_значення.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Назва,ensure_ascii=False),순번,шлях.stat().st_size))
    Заголовок_значення.append('};');(КР_дані/'resources.h').write_text('\n'.join(Заголовок_значення)+'\n',encoding='utf-8')
    місце_Файли=[]
    for Назва in ('компілятор_інструмент.c','загальномовне_середовище_виконання_опора.c','запустити.c','미리번역.c','повернути_міст.S'):
        кінцевий_файл=КР_дані/(Path(Назва).stem+'.o');місце_Файли.append(кінцевий_файл)
        Виконати_команда([시언어번역기]+конфігурація_служба_фонового_передавання_файлів+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Назва,'-o',кінцевий_файл])
    실행파일=корінь_шлях/'build/user/cc.elf'
    Виконати_команда([연결편집기,'--gc-sections','-T',корінь_шлях/'простір_користувача/схема_компонування.ld','-z','max-page-size=4096','-o',실행파일,
         корінь_шлях/'build/user/start.o',корінь_шлях/'build/user/runtime.o']+місце_Файли+
         [корінь_шлях/'build/user'/Назва for Назва in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
