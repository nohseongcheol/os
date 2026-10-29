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

Project_root = Path(__file__).resolve().parent


def Mag_execute_utos(Word_SMS):
    subprocess.check_call([str(pagpasok_VALUE) for pagpasok_VALUE in Word_SMS], cwd=str(Project_root))


def run():
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 tiyakin_kumpirmahin')
    parser_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    parser_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    parser_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = parser_48ee4b1b.parse_args()
    명세 = json.loads((Project_root / 'relink.json').read_text())
    build_system = Project_root / 'build'
    새묶음 = build_system / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    tagapagkabit = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Archive_tool = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    malayuan_Mga_Setting = json.loads((build_system / 'remote/libassh-build.json').read_text())
    Mga_Setting = malayuan_Mga_Setting['flags']
    if 인수.libassh_archive:
        Seguridad_bundle = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', Project_root / 'malayuan_VALUE', '-I', Project_root / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for pangalan in malayuan_Mga_Setting['sources']:
            patutunguhan_VALUE = 새묶음 / (Path(pangalan).stem + '.o')
            Mag_execute_utos([번역기] + Mga_Setting + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', Project_root / pangalan, '-o', patutunguhan_VALUE])
            목적들.append(patutunguhan_VALUE)
        Seguridad_bundle = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            Mag_execute_utos([Archive_tool, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Seguridad_bundle)
    if 인수.tinycc:
        if not 인수.sdk:
            parser_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            parser_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [seleksyon_VALUE for seleksyon_VALUE in Mga_Setting if seleksyon_VALUE != '-mgeneral-regs-only']
        patutunguhan_VALUE = 새묶음 / '번역기.o'
        Mag_execute_utos([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', Project_root / '시언어번역기', '-I', Project_root / 'vendor/tinycc', '-I', Project_root / 'gumagamit',
             '-I', build_system / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', Project_root / '시언어번역기/번역기.c', '-o', patutunguhan_VALUE])
        Mag_execute_utos([tagapagkabit, '--gc-sections', '-T', Project_root / 'gumagamit/Link_Layout.ld', '-z', 'max-page-size=4096',
             '-o', build_system / 'user/cc.elf', build_system / 'user/start.o', build_system / 'user/runtime.o', patutunguhan_VALUE] +
             [build_system / 'ccompiler' / (pangalan + '.o') for pangalan in ('common_language_runtime_Suporta', 'run', '미리번역', '되돌림')] +
             [build_system / 'user' / (pangalan + '.o') for pangalan in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = build_system / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((build_system / 'user/cc.elf').stat().st_size), 머리.read_text()))
        Mag_execute_utos([번역기] + Mga_Setting + ['-c', build_system / 'programs.S', '-o', Project_root / 'objects/programs.o'])
        Mag_execute_utos([번역기] + Mga_Setting + ['-std=c11', '-I', Project_root / 'posix-kor/arm64-native/포함', '-I', build_system,
             '-c', Project_root / 'machine/gumagamit.c', '-o', Project_root / 'objects/user.o'])
    Mag_execute_utos([tagapagkabit, '--gc-sections', '-T', Project_root / '부팅/Link_Layout.ld', '-o', 새묶음 / 'kernel.elf'] +
         [Project_root / path for path in 명세['objects']] + ['--start-group'] +
         [Seguridad_bundle if path == 'objects/libassh.a' else Project_root / path for path in 명세['libraries']] + ['--end-group'])
    Mag_execute_utos([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_file = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hash_file != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_file)
    print('RELINK PASS', hash_file, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    run()
