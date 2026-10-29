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

Project_корен = Path(__file__).resolve().parent


def Изврши_наредба(Word_СМС):
    subprocess.check_call([str(внес_VALUE) for внес_VALUE in Word_СМС], cwd=str(Project_корен))


def Изврши_2():
    анализатор_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    анализатор_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 провери')
    анализатор_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    анализатор_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    анализатор_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    Аргументи = анализатор_48ee4b1b.parse_args()
    명세 = json.loads((Project_корен / 'relink.json').read_text())
    верзија_систем = Project_корен / 'build'
    새묶음 = верзија_систем / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    приклучок = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архива_алатка = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    далечинскo_Параметри = json.loads((верзија_систем / 'remote/libassh-build.json').read_text())
    Подесувања = далечинскo_Параметри['flags']
    if Аргументи.libassh_archive:
        Безбедност_пакет = Аргументи.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_корен / 'далечинскo_VALUE', '-I', Project_корен / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for Име in далечинскo_Параметри['sources']:
            одредиште_VALUE = 새묶음 / (Path(Име).stem + '.o')
            Изврши_наредба([번역기] + Подесувања + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_корен / Име, '-o', одредиште_VALUE])
            목적들.append(одредиште_VALUE)
        Безбедност_пакет = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Изврши_наредба([Архива_алатка, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Безбедност_пакет)
    if Аргументи.tinycc:
        if not Аргументи.sdk:
            анализатор_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = Аргументи.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            анализатор_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [селекција_VALUE for селекција_VALUE in Подесувања if селекција_VALUE != '-mgeneral-regs-only']
        одредиште_VALUE = 새묶음 / '번역기.o'
        Изврши_наредба([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_корен / '시언어번역기', '-I', Project_корен / 'vendor/tinycc', '-I', Project_корен / 'корисник',
             '-I', верзија_систем / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_корен / '시언어번역기/번역기.c', '-o', одредиште_VALUE])
        Изврши_наредба([приклучок, '--gc-sections', '-T', Project_корен / 'корисник/Врска_Распоред.ld', '-z', 'max-page-size=4096',
             '-o', верзија_систем / 'user/cc.elf', верзија_систем / 'user/start.o', верзија_систем / 'user/runtime.o', одредиште_VALUE] +
             [верзија_систем / 'ccompiler' / (Име + '.o') for Име in ('заеднички_јазик_за_време_на_извршување_Поддршка', 'Изврши_2', '미리번역', '되돌림')] +
             [верзија_систем / 'user' / (Име + '.o') for Име in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = верзија_систем / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((верзија_систем / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Изврши_наредба([번역기] + Подесувања + ['-c', верзија_систем / 'programs.S', '-o', Project_корен / 'objects/programs.o'])
        Изврши_наредба([번역기] + Подесувања + ['-std=c11', '-I', Project_корен / 'posix-kor/arm64-native/포함', '-I', верзија_систем,
             '-c', Project_корен / 'машина/корисник.c', '-o', Project_корен / 'objects/user.o'])
    Изврши_наредба([приклучок, '--gc-sections', '-T', Project_корен / '부팅/Врска_Распоред.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_корен / ПАТЕКА for ПАТЕКА in 명세['objects']] + ['--start-group'] +
         [Безбедност_пакет if ПАТЕКА == 'objects/libassh.a' else Project_корен / ПАТЕКА for ПАТЕКА in 명세['libraries']] + ['--end-group'])
    Изврши_наредба([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    хаш_датотека = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if Аргументи.verify and хаш_датотека != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + хаш_датотека)
    print('RELINK PASS', хаш_датотека, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    Изврши_2()
