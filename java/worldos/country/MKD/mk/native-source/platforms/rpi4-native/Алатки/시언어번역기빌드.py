"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(корен_патека, склад_патека, 시언어번역기, 연결편집기, конфигурација_Услуга_за_интелигентен_пренос_во_заднина, Изврши_наредба):
    мерка_податоци = корен_патека / 'build/ccompiler'; мерка_податоци.mkdir(exist_ok=True)
    원본자료 = корен_патека / '시언어번역기'
    изворно = корен_патека / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = корен_патека / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    конфигурација_Услуга_за_интелигентен_пренос_во_заднина = [Параметри_VALUE for Параметри_VALUE in конфигурација_Услуга_за_интелигентен_пренос_во_заднина if Параметри_VALUE != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', изворно, '-I', корен_патека/'корисник', '-I', мерка_податоци, '-isystem', 개발꾸러미/'usr/include']
    Изврши_наредба([시언어번역기]+конфигурација_Услуга_за_интелигентен_пренос_во_заднина+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'подигање_Поддршка.c','-o',мерка_податоци/'crt.o'])
    Изврши_наредба([시언어번역기]+конфигурација_Услуга_за_интелигентен_пренос_во_заднина+['-I',склад_патека/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',мерка_податоци/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+податоци_позиционирање.name,податоци_позиционирање) for податоци_позиционирање in sorted((склад_патека/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+податоци_позиционирање.name,податоци_позиционирање) for податоци_позиционирање in sorted((изворно/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+податоци_позиционирање.name,податоци_позиционирање) for податоци_позиционирање in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',корен_патека/'build/user/start.o'),('/sdk/lib/crt.o',мерка_податоци/'crt.o'),('/sdk/lib/aot-runtime.o',мерка_податоци/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',корен_патека/'build/libposix-kor-user.a')]
    Заглавие_VALUE=['typedef struct { const char *Име; const unsigned char *податоци; unsigned Големина; } 번역기자원;']
    for 순번,(_,ПАТЕКА) in enumerate(탑재자료):
        Заглавие_VALUE.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in ПАТЕКА.read_bytes())))
    Заглавие_VALUE.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Име,ПАТЕКА) in enumerate(탑재자료): Заглавие_VALUE.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Име,ensure_ascii=False),순번,ПАТЕКА.stat().st_size))
    Заглавие_VALUE.append('};');(мерка_податоци/'resources.h').write_text('\n'.join(Заглавие_VALUE)+'\n',encoding='utf-8')
    одредиште_Датотеки=[]
    for Име in ('번역기.c','заеднички_јазик_за_време_на_извршување_Поддршка.c','Изврши_2.c','미리번역.c','되돌림.S'):
        одредишна_датотека=мерка_податоци/(Path(Име).stem+'.o');одредиште_Датотеки.append(одредишна_датотека)
        Изврши_наредба([시언어번역기]+конфигурација_Услуга_за_интелигентен_пренос_во_заднина+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Име,'-o',одредишна_датотека])
    실행파일=корен_патека/'build/user/cc.elf'
    Изврши_наредба([연결편집기,'--gc-sections','-T',корен_патека/'корисник/Врска_Распоред.ld','-z','max-page-size=4096','-o',실행파일,
         корен_патека/'build/user/start.o',корен_патека/'build/user/runtime.o']+одредиште_Датотеки+
         [корен_патека/'build/user'/Име for Име in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
