"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def Create_C_компилятор(корень_путь, репозиторий_путь, C_компилятор, компоновщик_средство, настройки_BITS, 실행):
    KR_данные = корень_путь / 'build/ccompiler'; KR_данные.mkdir(exist_ok=True)
    원본자료 = корень_путь / 'C_компилятор'
    вышестоящий = корень_путь / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    комплект_SDK = корень_путь / 'vendor/sdk'
    if not (комплект_SDK/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((комплект_SDK/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    настройки_BITS = [Настройки_ЗНАЧЕН for Настройки_ЗНАЧЕН in настройки_BITS if Настройки_ЗНАЧЕН != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', вышестоящий, '-I', корень_путь/'пространство_пользователя', '-I', KR_данные, '-isystem', комплект_SDK/'usr/include']
    실행([C_компилятор]+настройки_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'запуск_опора.c','-o',KR_данные/'crt.o'])
    실행([C_компилятор]+настройки_BITS+['-I',репозиторий_путь/'posix-kor/arm64-native/объявления']+포함인수+['-c',원본자료/'AOT_среда_CLR.c','-o',KR_данные/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+данные_позиция.name,данные_позиция) for данные_позиция in sorted((репозиторий_путь/'posix-kor/arm64-native/объявления').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+данные_позиция.name,данные_позиция) for данные_позиция in sorted((вышестоящий/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+данные_позиция.name,данные_позиция) for данные_позиция in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',корень_путь/'build/user/start.o'),('/sdk/lib/crt.o',KR_данные/'crt.o'),('/sdk/lib/aot-runtime.o',KR_данные/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',корень_путь/'build/libposix-kor-user.a')]
    Заголовок_ЗНАЧЕН=['typedef struct { const char *Название; const unsigned char *данные; unsigned Размер; } компилятор_ресурс;']
    for 순번,(_,путь) in enumerate(탑재자료):
        Заголовок_ЗНАЧЕН.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in путь.read_bytes())))
    Заголовок_ЗНАЧЕН.append('static const компилятор_ресурс компилятор_Ресурсы[] = {')
    for 순번,(Название,путь) in enumerate(탑재자료): Заголовок_ЗНАЧЕН.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Название,ensure_ascii=False),순번,путь.stat().st_size))
    Заголовок_ЗНАЧЕН.append('};');(KR_данные/'resources.h').write_text('\n'.join(Заголовок_ЗНАЧЕН)+'\n',encoding='utf-8')
    цель_Файлы=[]
    for Название in ('компилятор_средство.c','ПоддержкаВыполнения.c','запустить.c','미리번역.c','Возврат_мост.S'):
        конечный_файл=KR_данные/(Path(Название).stem+'.o');цель_Файлы.append(конечный_файл)
        실행([C_компилятор]+настройки_BITS+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Название,'-o',конечный_файл])
    исполняемый_файл=корень_путь/'build/user/cc.elf'
    실행([компоновщик_средство,'--gc-sections','-T',корень_путь/'пространство_пользователя/схема_компоновки.ld','-z','max-page-size=4096','-o',исполняемый_файл,
         корень_путь/'build/user/start.o',корень_путь/'build/user/runtime.o']+цель_Файлы+
         [корень_путь/'build/user'/Название for Название in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
