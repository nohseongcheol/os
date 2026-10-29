#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 자체 커널을 다시 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Project_raíz = Path(__file__).resolve().parent


def executar_comando(Word_SMS):
    subprocess.check_call([str(introdución_VALOR) for introdución_VALOR in Word_SMS], cwd=str(Project_raíz))


def Executar_2():
    analizador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizador_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verificar')
    analizador_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    analizador_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    analizador_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Argumentos = analizador_48ee4b1b.parse_args()
    명세 = json.loads((Project_raíz / 'relink.json').read_text())
    compilar_sistema = Project_raíz / 'build'
    새묶음 = compilar_sistema / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Conector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arquivo_ferramenta = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    remoto_Configuración = json.loads((compilar_sistema / 'remote/libassh-build.json').read_text())
    Configuración = remoto_Configuración['flags']
    if Argumentos.libassh_archive:
        Seguranza_paquete = Argumentos.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_raíz / 'remoto_VALOR', '-I', Project_raíz / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nome in remoto_Configuración['sources']:
            destino_VALOR = 새묶음 / (Path(Nome).stem + '.o')
            executar_comando([번역기] + Configuración + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_raíz / Nome, '-o', destino_VALOR])
            목적들.append(destino_VALOR)
        Seguranza_paquete = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            executar_comando([Arquivo_ferramenta, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Seguranza_paquete)
    if Argumentos.tinycc:
        if not Argumentos.sdk:
            analizador_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Argumentos.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analizador_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [selección_VALOR for selección_VALOR in Configuración if selección_VALOR != '-mgeneral-regs-only']
        destino_VALOR = 새묶음 / '번역기.o'
        executar_comando([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_raíz / '시언어번역기', '-I', Project_raíz / 'vendor/tinycc', '-I', Project_raíz / 'usuario',
             '-I', compilar_sistema / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_raíz / '시언어번역기/번역기.c', '-o', destino_VALOR])
        executar_comando([Conector, '--gc-sections', '-T', Project_raíz / 'usuario/Ligar_deseño.ld', '-z', 'max-page-size=4096',
             '-o', compilar_sistema / 'user/cc.elf', compilar_sistema / 'user/start.o', compilar_sistema / 'user/runtime.o', destino_VALOR] +
             [compilar_sistema / 'ccompiler' / (Nome + '.o') for Nome in ('실행지원', 'Executar_2', '미리번역', 'devolver_ponte')] +
             [compilar_sistema / 'user' / (Nome + '.o') for Nome in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = compilar_sistema / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((compilar_sistema / 'user/cc.elf').stat().st_size), 머리.read_text()))
        executar_comando([번역기] + Configuración + ['-c', compilar_sistema / 'programs.S', '-o', Project_raíz / 'objects/programs.o'])
        executar_comando([번역기] + Configuración + ['-std=c11', '-I', Project_raíz / 'posix-kor/arm64-native/포함', '-I', compilar_sistema,
             '-c', Project_raíz / 'máquina/usuario.c', '-o', Project_raíz / 'objects/user.o'])
    executar_comando([Conector, '--gc-sections', '-T', Project_raíz / '부팅/Ligar_deseño.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_raíz / CAMIÑO for CAMIÑO in 명세['objects']] + ['--start-group'] +
         [Seguranza_paquete if CAMIÑO == 'objects/libassh.a' else Project_raíz / CAMIÑO for CAMIÑO in 명세['libraries']] + ['--end-group'])
    executar_comando([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_Ficheiro = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Argumentos.verify and hash_Ficheiro != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_Ficheiro)
    print('RELINK PASS', hash_Ficheiro, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Executar_2()
