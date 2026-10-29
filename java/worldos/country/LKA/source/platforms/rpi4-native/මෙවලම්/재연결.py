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

기준 = Path(__file__).resolve().parent


def ක්_රියාත්මක_කරන්න_විධානය(말):
    subprocess.check_call([str(පිවිසුම_අගය) for පිවිසුම_අගය in 말], cwd=str(기준))


def ක්_රියාත්මක_කරන්න_2():
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 තහවුරු_කරන්න')
    해석기.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    해석기.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    해석기.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    විස්තාරක = 해석기.parse_args()
    명세 = json.loads((기준 / 'relink.json').read_text())
    තැනුම_පද්ධතිය = 기준 / 'build'
    새묶음 = තැනුම_පද්ධතිය / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    සම්බන්ධකය = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    සංරක්ෂිතය_මෙවලම = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    දුරස්ථ_පසුතල = json.loads((තැනුම_පද්ධතිය / 'remote/libassh-build.json').read_text())
    සැකසුම් = දුරස්ථ_පසුතල['flags']
    if විස්තාරක.libassh_archive:
        ආරක්ෂණය_පොදිය = විස්තාරක.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', 기준 / 'දුරස්ථ_අගය', '-I', 기준 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for නම in දුරස්ථ_පසුතල['sources']:
            ගමනාන්තය_අගය = 새묶음 / (Path(නම).stem + '.o')
            ක්_රියාත්මක_කරන්න_විධානය([번역기] + සැකසුම් + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', 기준 / නම, '-o', ගමනාන්තය_අගය])
            목적들.append(ගමනාන්තය_අගය)
        ආරක්ෂණය_පොදිය = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            ක්_රියාත්මක_කරන්න_විධානය([සංරක්ෂිතය_මෙවලම, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(ආරක්ෂණය_පොදිය)
    if විස්තාරක.tinycc:
        if not විස්තාරක.sdk:
            해석기.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = විස්තාරක.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            해석기.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [තේරීම_අගය for තේරීම_අගය in සැකසුම් if තේරීම_අගය != '-mgeneral-regs-only']
        ගමනාන්තය_අගය = 새묶음 / '번역기.o'
        ක්_රියාත්මක_කරන්න_විධානය([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', 기준 / '시언어번역기', '-I', 기준 / 'vendor/tinycc', '-I', 기준 / 'පරිශීලක',
             '-I', තැනුම_පද්ධතිය / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', 기준 / '시언어번역기/번역기.c', '-o', ගමනාන්තය_අගය])
        ක්_රියාත්මක_කරන්න_විධානය([සම්බන්ධකය, '--gc-sections', '-T', 기준 / 'පරිශීලක/සබැඳිය_සැකැස්ම.ld', '-z', 'max-page-size=4096',
             '-o', තැනුම_පද්ධතිය / 'user/cc.elf', තැනුම_පද්ධතිය / 'user/start.o', තැනුම_පද්ධතිය / 'user/runtime.o', ගමනාන්තය_අගය] +
             [තැනුම_පද්ධතිය / 'ccompiler' / (නම + '.o') for නම in ('පොදු_භාෂා_ධාවන_කාලය_සහාය', 'ක්_රියාත්මක_කරන්න_2', '미리번역', '되돌림')] +
             [තැනුම_පද්ධතිය / 'user' / (නම + '.o') for නම in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = තැනුම_පද්ධතිය / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((තැනුම_පද්ධතිය / 'user/cc.elf').stat().st_size), 머리.read_text()))
        ක්_රියාත්මක_කරන්න_විධානය([번역기] + සැකසුම් + ['-c', තැනුම_පද්ධතිය / 'programs.S', '-o', 기준 / 'objects/programs.o'])
        ක්_රියාත්මක_කරන්න_විධානය([번역기] + සැකසුම් + ['-std=c11', '-I', 기준 / 'posix-kor/arm64-native/포함', '-I', තැනුම_පද්ධතිය,
             '-c', 기준 / 'යන්ත්_රය/පරිශීලක.c', '-o', 기준 / 'objects/user.o'])
    ක්_රියාත්මක_කරන්න_විධානය([සම්බන්ධකය, '--gc-sections', '-T', 기준 / '부팅/සබැඳිය_සැකැස්ම.ld', '-o', 새묶음 / 'kernel.elf'] +
         [기준 / මාර්_ගය for මාර්_ගය in 명세['objects']] + ['--start-group'] +
         [ආරක්ෂණය_පොදිය if මාර්_ගය == 'objects/libassh.a' else 기준 / මාර්_ගය for මාර්_ගය in 명세['libraries']] + ['--end-group'])
    ක්_රියාත්මක_කරන්න_විධානය([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    හෑෂ්_ගොනුව = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if විස්තාරක.verify and හෑෂ්_ගොනුව != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + හෑෂ්_ගොනුව)
    print('RELINK PASS', හෑෂ්_ගොනුව, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
