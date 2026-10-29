#!/usr/bin/env python3
"""distribuição_VALOR 묶음에서 libassh/TinyCC를 교체하고 nativo 커널을 repetir_VALOR 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ação_raiz = Path(__file__).resolve().parent


def Executar_comando(Word_SMS):
    subprocess.check_call([str(entrada_VALOR_962f286b) for entrada_VALOR_962f286b in Word_SMS], cwd=str(ação_raiz))


def iniciar():
    analisador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analisador_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verificar')
    analisador_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a uso_VALOR')
    analisador_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 repetir_VALOR 컴파일하고 커널에 탑재')
    analisador_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    argumentos = analisador_48ee4b1b.parse_args()
    especificação = json.loads((ação_raiz / 'relink.json').read_text())
    construir = ação_raiz / 'build'
    새묶음 = construir / 'relinked'
    새묶음.mkdir(exist_ok=True)
    compilador_ferramenta = os.environ.get('ARM64_CC', 'clang')
    Conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    arquivo_ferramenta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    remoto_Configurações = json.loads((construir / 'remote/libassh-build.json').read_text())
    Definições = remoto_Configurações['flags']
    if argumentos.libassh_archive:
        Segurança_grupo = argumentos.libassh_archive.resolve()
    else:
        목적들 = []
        declarações = ['-I', ação_raiz / 'remoto_VALOR', '-I', ação_raiz / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nome in remoto_Configurações['sources']:
            destino_VALOR = 새묶음 / (Path(Nome).stem + '.o')
            Executar_comando([compilador_ferramenta] + Definições + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + declarações +
                 ['-c', ação_raiz / Nome, '-o', destino_VALOR])
            목적들.append(destino_VALOR)
        Segurança_grupo = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Executar_comando([arquivo_ferramenta, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Segurança_grupo)
    if argumentos.tinycc:
        if not argumentos.sdk:
            analisador_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = argumentos.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analisador_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [seleção_VALOR for seleção_VALOR in Definições if seleção_VALOR != '-mgeneral-regs-only']
        destino_VALOR = 새묶음 / 'compilador_ferramenta.o'
        Executar_comando([compilador_ferramenta] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', ação_raiz / 'C_compilador', '-I', ação_raiz / 'vendor/tinycc', '-I', ação_raiz / 'espaço_do_utilizador',
             '-I', construir / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', ação_raiz / 'C_compilador/compilador_ferramenta.c', '-o', destino_VALOR])
        Executar_comando([Conector, '--gc-sections', '-T', ação_raiz / 'espaço_do_utilizador/disposição_de_ligação.ld', '-z', 'max-page-size=4096',
             '-o', construir / 'user/cc.elf', construir / 'user/start.o', construir / 'user/runtime.o', destino_VALOR] +
             [construir / 'ccompiler' / (Nome + '.o') for Nome in ('SuporteExecução', 'iniciar', '미리번역', 'devolver_ponte')] +
             [construir / 'user' / (Nome + '.o') for Nome in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        HEAD_VALOR = construir / 'programs.h'
        HEAD_VALOR.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((construir / 'user/cc.elf').stat().st_size), HEAD_VALOR.read_text()))
        Executar_comando([compilador_ferramenta] + Definições + ['-c', construir / 'programs.S', '-o', ação_raiz / 'objects/programs.o'])
        Executar_comando([compilador_ferramenta] + Definições + ['-std=c11', '-I', ação_raiz / 'posix-kor/arm64-native/declarações', '-I', construir,
             '-c', ação_raiz / 'computador/espaço_do_utilizador.c', '-o', ação_raiz / 'objects/user.o'])
    Executar_comando([Conector, '--gc-sections', '-T', ação_raiz / 'arranque_da_máquina/disposição_de_ligação.ld', '-o', 새묶음 / 'kernel.elf'] +
         [ação_raiz / caminho for caminho in especificação['objects']] + ['--start-group'] +
         [Segurança_grupo if caminho == 'objects/libassh.a' else ação_raiz / caminho for caminho in especificação['libraries']] + ['--end-group'])
    Executar_comando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_Arquivo = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if argumentos.verify and hash_Arquivo != especificação['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_Arquivo)
    print('RELINK PASS', hash_Arquivo, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    iniciar()
