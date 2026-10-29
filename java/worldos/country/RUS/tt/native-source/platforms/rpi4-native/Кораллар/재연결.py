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

экранга_җибәрү_тамыр = Path(__file__).resolve().parent


def үтәргә_команда(Word_СМС):
    subprocess.check_call([str(кертү_VALUE) for кертү_VALUE in Word_СМС], cwd=str(экранга_җибәрү_тамыр))


def эшләтү():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 раслау')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((экранга_җибәрү_тамыр / 'relink.json').read_text())
    төзү_система = экранга_җибәрү_тамыр / 'build'
    새묶음 = төзү_система / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    бәйләүче = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Архив_чара = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    читтәге_Параметрлар = json.loads((төзү_система / 'remote/libassh-build.json').read_text())
    Caylaw = читтәге_Параметрлар['flags']
    if 인수.libassh_archive:
        Иминлек_пакет = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', экранга_җибәрү_тамыр / 'читтәге_VALUE', '-I', экранга_җибәрү_тамыр / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for исем in читтәге_Параметрлар['sources']:
            күчерү_урыны_VALUE = 새묶음 / (Path(исем).stem + '.o')
            үтәргә_команда([번역기] + Caylaw + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', экранга_җибәрү_тамыр / исем, '-o', күчерү_урыны_VALUE])
            목적들.append(күчерү_урыны_VALUE)
        Иминлек_пакет = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            үтәргә_команда([Архив_чара, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Иминлек_пакет)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [тамгаланган_өлеш_VALUE for тамгаланган_өлеш_VALUE in Caylaw if тамгаланган_өлеш_VALUE != '-mgeneral-regs-only']
        күчерү_урыны_VALUE = 새묶음 / '번역기.o'
        үтәргә_команда([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', экранга_җибәрү_тамыр / '시언어번역기', '-I', экранга_җибәрү_тамыр / 'vendor/tinycc', '-I', экранга_җибәрү_тамыр / 'кулланучы',
             '-I', төзү_система / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', экранга_җибәрү_тамыр / '시언어번역기/번역기.c', '-o', күчерү_урыны_VALUE])
        үтәргә_команда([бәйләүче, '--gc-sections', '-T', экранга_җибәрү_тамыр / 'кулланучы/бәйләү_план.ld', '-z', 'max-page-size=4096',
             '-o', төзү_система / 'user/cc.elf', төзү_система / 'user/start.o', төзү_система / 'user/runtime.o', күчерү_урыны_VALUE] +
             [төзү_система / 'ccompiler' / (исем + '.o') for исем in ('CLR_мохите_ярдәм', 'эшләтү', '미리번역', 'кайтару_күпер')] +
             [төзү_система / 'user' / (исем + '.o') for исем in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = төзү_система / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((төзү_система / 'user/cc.elf').stat().st_size), 머리.read_text()))
        үтәргә_команда([번역기] + Caylaw + ['-c', төзү_система / 'programs.S', '-o', экранга_җибәрү_тамыр / 'objects/programs.o'])
        үтәргә_команда([번역기] + Caylaw + ['-std=c11', '-I', экранга_җибәрү_тамыр / 'posix-kor/arm64-native/포함', '-I', төзү_система,
             '-c', экранга_җибәрү_тамыр / 'машина/кулланучы.c', '-o', экранга_җибәрү_тамыр / 'objects/user.o'])
    үтәргә_команда([бәйләүче, '--gc-sections', '-T', экранга_җибәрү_тамыр / '부팅/бәйләү_план.ld', '-o', 새묶음 / 'kernel.elf'] +
         [экранга_җибәрү_тамыр / Yul for Yul in 명세['objects']] + ['--start-group'] +
         [Иминлек_пакет if Yul == 'objects/libassh.a' else экранга_җибәрү_тамыр / Yul for Yul in 명세['libraries']] + ['--end-group'])
    үтәргә_команда([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    Хәш_файл = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and Хәш_файл != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + Хәш_файл)
    print('RELINK PASS', Хәш_файл, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    эшләтү()
