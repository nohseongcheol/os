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

pprojetta_għerq = Path(__file__).resolve().parent


def eżegwixxa_kmand(Word_SMS):
    subprocess.check_call([str(entrata_VALUE) for entrata_VALUE in Word_SMS], cwd=str(pprojetta_għerq))


def serje():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 vverifika')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = 해석기.parse_args()
    명세 = json.loads((pprojetta_għerq / 'relink.json').read_text())
    bena_sistema = pprojetta_għerq / 'build'
    새묶음 = bena_sistema / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    konnettur = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    Arkivju_għodda = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    mill_bogħod_Settings = json.loads((bena_sistema / 'remote/libassh-build.json').read_text())
    Settings = mill_bogħod_Settings['flags']
    if 인수.libassh_archive:
        Sigurtà_lott = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', pprojetta_għerq / 'mill_bogħod_VALUE', '-I', pprojetta_għerq / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for isem in mill_bogħod_Settings['sources']:
            destinazzjoni_VALUE = 새묶음 / (Path(isem).stem + '.o')
            eżegwixxa_kmand([번역기] + Settings + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', pprojetta_għerq / isem, '-o', destinazzjoni_VALUE])
            목적들.append(destinazzjoni_VALUE)
        Sigurtà_lott = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            eżegwixxa_kmand([Arkivju_għodda, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(Sigurtà_lott)
    if 인수.tinycc:
        if not 인수.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [għażla_VALUE for għażla_VALUE in Settings if għażla_VALUE != '-mgeneral-regs-only']
        destinazzjoni_VALUE = 새묶음 / '번역기.o'
        eżegwixxa_kmand([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', pprojetta_għerq / '시언어번역기', '-I', pprojetta_għerq / 'vendor/tinycc', '-I', pprojetta_għerq / 'utent',
             '-I', bena_sistema / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', pprojetta_għerq / '시언어번역기/번역기.c', '-o', destinazzjoni_VALUE])
        eżegwixxa_kmand([konnettur, '--gc-sections', '-T', pprojetta_għerq / 'utent/Link_Tqassim.ld', '-z', 'max-page-size=4096',
             '-o', bena_sistema / 'user/cc.elf', bena_sistema / 'user/start.o', bena_sistema / 'user/runtime.o', destinazzjoni_VALUE] +
             [bena_sistema / 'ccompiler' / (isem + '.o') for isem in ('tħaddim_tal_lingwa_komuni_Appoġġ', 'serje', '미리번역', '되돌림')] +
             [bena_sistema / 'user' / (isem + '.o') for isem in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = bena_sistema / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((bena_sistema / 'user/cc.elf').stat().st_size), 머리.read_text()))
        eżegwixxa_kmand([번역기] + Settings + ['-c', bena_sistema / 'programs.S', '-o', pprojetta_għerq / 'objects/programs.o'])
        eżegwixxa_kmand([번역기] + Settings + ['-std=c11', '-I', pprojetta_għerq / 'posix-kor/arm64-native/포함', '-I', bena_sistema,
             '-c', pprojetta_għerq / 'kompjuter/utent.c', '-o', pprojetta_għerq / 'objects/user.o'])
    eżegwixxa_kmand([konnettur, '--gc-sections', '-T', pprojetta_għerq / '부팅/Link_Tqassim.ld', '-o', 새묶음 / 'kernel.elf'] +
         [pprojetta_għerq / mogħdija for mogħdija in 명세['objects']] + ['--start-group'] +
         [Sigurtà_lott if mogħdija == 'objects/libassh.a' else pprojetta_għerq / mogħdija for mogħdija in 명세['libraries']] + ['--end-group'])
    eżegwixxa_kmand([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    hash_fajl = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and hash_fajl != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + hash_fajl)
    print('RELINK PASS', hash_fajl, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    serje()
