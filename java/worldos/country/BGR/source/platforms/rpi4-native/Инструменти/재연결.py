#!/usr/bin/env python3
"""배포 묶음에서 libassh/TinyCC를 교체하고 자체 커널을 опитвам_повторно_стойност 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

проект_корен = Path(__file__).resolve().parent


def изпълнявам_команда(Игри_с_думи_Текст):
    subprocess.check_call([str(запис_стойност) for запис_стойност in Игри_с_думи_Текст], cwd=str(проект_корен))


def Стартиране():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 проверявам')
    анализатор_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a използвам_стойност')
    анализатор_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 опитвам_повторно_стойност 컴파일하고 커널에 탑재')
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Параметри = анализатор_48ee4b1b.parse_args()
    명세 = json.loads((проект_корен / 'relink.json').read_text())
    компилация_система = проект_корен / 'build'
    새묶음 = компилация_система / 'relinked'
    새묶음.mkdir(exist_ok=True)
    компилатор_инструмент = os.environ.get('ARM64_CC', 'clang')
    Конектор = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архив_инструмент = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    отдалечен_Настройки = json.loads((компилация_система / 'remote/libassh-build.json').read_text())
    Настройки = отдалечен_Настройки['flags']
    if Параметри.libassh_archive:
        Защита_пакет = Параметри.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', проект_корен / 'отдалечен_стойност', '-I', проект_корен / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Име in отдалечен_Настройки['sources']:
            местоназначение_стойност = 새묶음 / (Path(Име).stem + '.o')
            изпълнявам_команда([компилатор_инструмент] + Настройки + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', проект_корен / Име, '-o', местоназначение_стойност])
            목적들.append(местоназначение_стойност)
        Защита_пакет = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            изпълнявам_команда([Архив_инструмент, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Защита_пакет)
    if Параметри.tinycc:
        if not Параметри.sdk:
            анализатор_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Параметри.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            анализатор_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [избор_стойност for избор_стойност in Настройки if избор_стойност != '-mgeneral-regs-only']
        местоназначение_стойност = 새묶음 / 'компилатор_инструмент.o'
        изпълнявам_команда([компилатор_инструмент] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', проект_корен / '시언어번역기', '-I', проект_корен / 'vendor/tinycc', '-I', проект_корен / 'потребител',
             '-I', компилация_система / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', проект_корен / '시언어번역기/компилатор_инструмент.c', '-o', местоназначение_стойност])
        изпълнявам_команда([Конектор, '--gc-sections', '-T', проект_корен / 'потребител/Връзка_схема.ld', '-z', 'max-page-size=4096',
             '-o', компилация_система / 'user/cc.elf', компилация_система / 'user/start.o', компилация_система / 'user/runtime.o', местоназначение_стойност] +
             [компилация_система / 'ccompiler' / (Име + '.o') for Име in ('обща_езикова_среда_Поддръжка', 'Стартиране', '미리번역', 'връщам_мост')] +
             [компилация_система / 'user' / (Име + '.o') for Име in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = компилация_система / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((компилация_система / 'user/cc.elf').stat().st_size), 머리.read_text()))
        изпълнявам_команда([компилатор_инструмент] + Настройки + ['-c', компилация_система / 'programs.S', '-o', проект_корен / 'objects/programs.o'])
        изпълнявам_команда([компилатор_инструмент] + Настройки + ['-std=c11', '-I', проект_корен / 'posix-kor/arm64-native/포함', '-I', компилация_система,
             '-c', проект_корен / 'машина/потребител.c', '-o', проект_корен / 'objects/user.o'])
    изпълнявам_команда([Конектор, '--gc-sections', '-T', проект_корен / '부팅/Връзка_схема.ld', '-o', 새묶음 / 'kernel.elf'] +
         [проект_корен / ПЪТ for ПЪТ in 명세['objects']] + ['--start-group'] +
         [Защита_пакет if ПЪТ == 'objects/libassh.a' else проект_корен / ПЪТ for ПЪТ in 명세['libraries']] + ['--end-group'])
    изпълнявам_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    хеширане_Файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Параметри.verify and хеширане_Файл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + хеширане_Файл)
    print('RELINK PASS', хеширане_Файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Стартиране()
