#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 propi 커널을 tornar_ho_a_provar_VALOR 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

Project_rel = Path(__file__).resolve().parent


def Executa_ordre(Word_SMS):
    subprocess.check_call([str(introducció_VALOR) for introducció_VALOR in Word_SMS], cwd=str(Project_rel))


def Executa_2():
    analitzador_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analitzador_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 verificar')
    analitzador_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a ús_VALOR')
    analitzador_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 tornar_ho_a_provar_VALOR 컴파일하고 커널에 탑재')
    analitzador_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = analitzador_48ee4b1b.parse_args()
    명세 = json.loads((Project_rel / 'relink.json').read_text())
    generar_sistema = Project_rel / 'build'
    새묶음 = generar_sistema / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Connector = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arxiu_eina = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    remot_Configuració = json.loads((generar_sistema / 'remote/libassh-build.json').read_text())
    Ajusts = remot_Configuració['flags']
    if 인수.libassh_archive:
        Seguretat_paquet = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_rel / 'remot_VALOR', '-I', Project_rel / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Nom in remot_Configuració['sources']:
            destinació_VALOR = 새묶음 / (Path(Nom).stem + '.o')
            Executa_ordre([번역기] + Ajusts + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_rel / Nom, '-o', destinació_VALOR])
            목적들.append(destinació_VALOR)
        Seguretat_paquet = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Executa_ordre([Arxiu_eina, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Seguretat_paquet)
    if 인수.tinycc:
        if not 인수.sdk:
            analitzador_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            analitzador_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [selecció_VALOR for selecció_VALOR in Ajusts if selecció_VALOR != '-mgeneral-regs-only']
        destinació_VALOR = 새묶음 / '번역기.o'
        Executa_ordre([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_rel / '시언어번역기', '-I', Project_rel / 'vendor/tinycc', '-I', Project_rel / 'usuari',
             '-I', generar_sistema / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_rel / '시언어번역기/번역기.c', '-o', destinació_VALOR])
        Executa_ordre([Connector, '--gc-sections', '-T', Project_rel / 'usuari/enllaç_disseny.ld', '-z', 'max-page-size=4096',
             '-o', generar_sistema / 'user/cc.elf', generar_sistema / 'user/start.o', generar_sistema / 'user/runtime.o', destinació_VALOR] +
             [generar_sistema / 'ccompiler' / (Nom + '.o') for Nom in ('실행지원', 'Executa_2', '미리번역', 'tornar_les_tasques_pont')] +
             [generar_sistema / 'user' / (Nom + '.o') for Nom in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = generar_sistema / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((generar_sistema / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Executa_ordre([번역기] + Ajusts + ['-c', generar_sistema / 'programs.S', '-o', Project_rel / 'objects/programs.o'])
        Executa_ordre([번역기] + Ajusts + ['-std=c11', '-I', Project_rel / 'posix-kor/arm64-native/포함', '-I', generar_sistema,
             '-c', Project_rel / 'màquina/usuari.c', '-o', Project_rel / 'objects/user.o'])
    Executa_ordre([Connector, '--gc-sections', '-T', Project_rel / '부팅/enllaç_disseny.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_rel / Camí for Camí in 명세['objects']] + ['--start-group'] +
         [Seguretat_paquet if Camí == 'objects/libassh.a' else Project_rel / Camí for Camí in 명세['libraries']] + ['--end-group'])
    Executa_ordre([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_arxiu = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hash_arxiu != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_arxiu)
    print('RELINK PASS', hash_arxiu, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Executa_2()
