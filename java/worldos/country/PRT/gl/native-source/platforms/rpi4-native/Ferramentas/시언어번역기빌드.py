"""Build TinyCC as a native EL0 program; no Linux runtime or host compiler service."""
import json
from pathlib import Path


def 시언어번역기만들기(raíz_camiño, repositorio_camiño, 시언어번역기, 연결편집기, configuración_Servizo_de_transferencia_intelixente_en_segundo_plano, executar_comando):
    medida_datos = raíz_camiño / 'build/ccompiler'; medida_datos.mkdir(exist_ok=True)
    원본자료 = raíz_camiño / '시언어번역기'
    ascendente = raíz_camiño / 'vendor/tinycc'
    # Only declarations and arithmetic builtins are used from the prepared SDK.
    # No musl libc, startup file, dynamic loader, or Linux syscall code is linked.
    개발꾸러미 = raíz_camiño / 'vendor/sdk'
    if not (개발꾸러미/'usr/include/stdio.h').exists():
        raise SystemExit('C compiler build needs ARM64 SDK headers: make rpi-prepare')
    내장연산 = sorted((개발꾸러미/'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
    if not 내장연산: raise SystemExit('ARM64 libgcc arithmetic builtins missing in prepared SDK')
    configuración_Servizo_de_transferencia_intelixente_en_segundo_plano = [Configuración_VALOR for Configuración_VALOR in configuración_Servizo_de_transferencia_intelixente_en_segundo_plano if Configuración_VALOR != '-mgeneral-regs-only']
    포함인수 = ['-I', 원본자료, '-I', ascendente, '-I', raíz_camiño/'usuario', '-I', medida_datos, '-isystem', 개발꾸러미/'usr/include']
    executar_comando([시언어번역기]+configuración_Servizo_de_transferencia_intelixente_en_segundo_plano+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/'inicio_soporte.c','-o',medida_datos/'crt.o'])
    executar_comando([시언어번역기]+configuración_Servizo_de_transferencia_intelixente_en_segundo_plano+['-I',repositorio_camiño/'posix-kor/arm64-native/포함']+포함인수+['-c',원본자료/'미리번역실행.c','-o',medida_datos/'aot-runtime.o'])
    탑재자료 = [('/sdk/include/'+datos_cargo.name,datos_cargo) for datos_cargo in sorted((repositorio_camiño/'posix-kor/arm64-native/포함').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+datos_cargo.name,datos_cargo) for datos_cargo in sorted((ascendente/'include').glob('*.h'))]
    탑재자료 += [('/sdk/include/'+datos_cargo.name,datos_cargo) for datos_cargo in sorted((원본자료/'개발규약').glob('*.h'))]
    탑재자료 += [('/sdk/lib/start.o',raíz_camiño/'build/user/start.o'),('/sdk/lib/crt.o',medida_datos/'crt.o'),('/sdk/lib/aot-runtime.o',medida_datos/'aot-runtime.o'),('/sdk/lib/libposix-kor-user.a',raíz_camiño/'build/libposix-kor-user.a')]
    Cabeceira_VALOR=['typedef struct { const char *Nome; const unsigned char *datos; unsigned Tamaño; } 번역기자원;']
    for 순번,(_,CAMIÑO) in enumerate(탑재자료):
        Cabeceira_VALOR.append('static const unsigned char 탑재자원_%d[] = {%s};'%(순번,','.join(str(임시값) for 임시값 in CAMIÑO.read_bytes())))
    Cabeceira_VALOR.append('static const 번역기자원 번역기자원들[] = {')
    for 순번,(Nome,CAMIÑO) in enumerate(탑재자료): Cabeceira_VALOR.append('{%s, 탑재자원_%d, %d},'%(json.dumps(Nome,ensure_ascii=False),순번,CAMIÑO.stat().st_size))
    Cabeceira_VALOR.append('};');(medida_datos/'resources.h').write_text('\n'.join(Cabeceira_VALOR)+'\n',encoding='utf-8')
    destino_Ficheiros=[]
    for Nome in ('번역기.c','실행지원.c','Executar_2.c','미리번역.c','devolver_ponte.S'):
        ficheiro_de_destino=medida_datos/(Path(Nome).stem+'.o');destino_Ficheiros.append(ficheiro_de_destino)
        executar_comando([시언어번역기]+configuración_Servizo_de_transferencia_intelixente_en_segundo_plano+['-ffunction-sections','-fdata-sections']+포함인수+['-c',원본자료/Nome,'-o',ficheiro_de_destino])
    실행파일=raíz_camiño/'build/user/cc.elf'
    executar_comando([연결편집기,'--gc-sections','-T',raíz_camiño/'usuario/Ligar_deseño.ld','-z','max-page-size=4096','-o',실행파일,
         raíz_camiño/'build/user/start.o',raíz_camiño/'build/user/runtime.o']+destino_Ficheiros+
         [raíz_camiño/'build/user'/Nome for Nome in ('jar.o','tinflate.o','crc32.o','adler32.o')]+[내장연산[-1]])
