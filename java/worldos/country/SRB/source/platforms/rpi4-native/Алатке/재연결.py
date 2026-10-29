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

пројектовати_корен = Path(__file__).resolve().parent


def Изврши_команда(Укрштенице_Текст):
    subprocess.check_call([str(унос_вриједност) for унос_вриједност in Укрштенице_Текст], cwd=str(пројектовати_корен))


def Покрени():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 потврдити')
    анализатор_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    анализатор_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Аргументи = анализатор_48ee4b1b.parse_args()
    명세 = json.loads((пројектовати_корен / 'relink.json').read_text())
    градити_систем = пројектовати_корен / 'build'
    새묶음 = градити_систем / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    Конектор = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архива_алат = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    удаљен_Поставке = json.loads((градити_систем / 'remote/libassh-build.json').read_text())
    Поставке = удаљен_Поставке['flags']
    if Аргументи.libassh_archive:
        Безбедност_пакет = Аргументи.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', пројектовати_корен / 'удаљен_вриједност', '-I', пројектовати_корен / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Назив in удаљен_Поставке['sources']:
            одредиште_вриједност = 새묶음 / (Path(Назив).stem + '.o')
            Изврши_команда([번역기] + Поставке + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', пројектовати_корен / Назив, '-o', одредиште_вриједност])
            목적들.append(одредиште_вриједност)
        Безбедност_пакет = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Изврши_команда([Архива_алат, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Безбедност_пакет)
    if Аргументи.tinycc:
        if not Аргументи.sdk:
            анализатор_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Аргументи.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            анализатор_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [избор_вриједност for избор_вриједност in Поставке if избор_вриједност != '-mgeneral-regs-only']
        одредиште_вриједност = 새묶음 / '번역기.o'
        Изврши_команда([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', пројектовати_корен / '시언어번역기', '-I', пројектовати_корен / 'vendor/tinycc', '-I', пројектовати_корен / 'корисник',
             '-I', градити_систем / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', пројектовати_корен / '시언어번역기/번역기.c', '-o', одредиште_вриједност])
        Изврши_команда([Конектор, '--gc-sections', '-T', пројектовати_корен / 'корисник/Веза_изглед.ld', '-z', 'max-page-size=4096',
             '-o', градити_систем / 'user/cc.elf', градити_систем / 'user/start.o', градити_систем / 'user/runtime.o', одредиште_вриједност] +
             [градити_систем / 'ccompiler' / (Назив + '.o') for Назив in ('заједничка_извршна_језичка_компонента_Подршка', 'Покрени', '미리번역', 'вратити_мост')] +
             [градити_систем / 'user' / (Назив + '.o') for Назив in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = градити_систем / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((градити_систем / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Изврши_команда([번역기] + Поставке + ['-c', градити_систем / 'programs.S', '-o', пројектовати_корен / 'objects/programs.o'])
        Изврши_команда([번역기] + Поставке + ['-std=c11', '-I', пројектовати_корен / 'posix-kor/arm64-native/포함', '-I', градити_систем,
             '-c', пројектовати_корен / 'рачунар/корисник.c', '-o', пројектовати_корен / 'objects/user.o'])
    Изврши_команда([Конектор, '--gc-sections', '-T', пројектовати_корен / '부팅/Веза_изглед.ld', '-o', 새묶음 / 'kernel.elf'] +
         [пројектовати_корен / ПУТАЊА for ПУТАЊА in 명세['objects']] + ['--start-group'] +
         [Безбедност_пакет if ПУТАЊА == 'objects/libassh.a' else пројектовати_корен / ПУТАЊА for ПУТАЊА in 명세['libraries']] + ['--end-group'])
    Изврши_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    хеш_фајл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Аргументи.verify and хеш_фајл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + хеш_фајл)
    print('RELINK PASS', хеш_фајл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Покрени()
