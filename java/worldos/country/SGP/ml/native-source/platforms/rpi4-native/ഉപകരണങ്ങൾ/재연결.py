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

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parent


def നടപ്പാക്കുക_കമാന്_ഡ്(വാക്ക്_ലിഖിതം):
    subprocess.check_call([str(എന്_ട്രി_മൂല്യം) for എന്_ട്രി_മൂല്യം in വാക്ക്_ലിഖിതം], cwd=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം))


def നടപ്പിലാക്കുക():
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 പരിശോധിക്കുക')
    പാഴ്_സർ_48ee4b1b.add_argument('--libassh-archive', type=Path, help='별도로 수정·컴파일한 libassh.a 사용')
    പാഴ്_സർ_48ee4b1b.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 다시 컴파일하고 커널에 탑재')
    പാഴ്_സർ_48ee4b1b.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    인수 = പാഴ്_സർ_48ee4b1b.parse_args()
    명세 = json.loads((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'relink.json').read_text())
    ബിൽഡ്_సిస్టమ్ = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build'
    새묶음 = ബിൽഡ്_సిస్టమ్ / 'relinked'
    새묶음.mkdir(exist_ok=True)
    번역기 = os.environ.get('ARM64_CC', 'clang')
    കണക്ടര് = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    ശേഖരം_ഉപകരണം = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    വിദൂര_ക്രമീകരണം = json.loads((ബിൽഡ്_సిస్టమ్ / 'remote/libassh-build.json').read_text())
    സജ്ജീകരണം = വിദൂര_ക്രമീകരണം['flags']
    if 인수.libassh_archive:
        സുരക്ഷ_ബണ്ടിൽ = 인수.libassh_archive.resolve()
    else:
        목적들 = []
        포함 = ['-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'വിദൂര_മൂല്യം', '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for പേരു് in വിദൂര_ക്രമീകരണം['sources']:
            ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = 새묶음 / (Path(പേരു്).stem + '.o')
            നടപ്പാക്കുക_കമാന്_ഡ്([번역기] + സജ്ജീകരണം + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 포함 +
                 ['-c', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / പേരു്, '-o', ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം])
            목적들.append(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം)
        സുരക്ഷ_ബണ്ടിൽ = 새묶음 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(새묶음)) as 임시:
            임시묶음 = Path(임시) / 'libassh.a'
            നടപ്പാക്കുക_കമാന്_ഡ്([ശേഖരം_ഉപകരണം, 'rcs', 임시묶음] + 목적들)
            임시묶음.replace(സുരക്ഷ_ബണ്ടിൽ)
    if 인수.tinycc:
        if not 인수.sdk:
            പാഴ്_സർ_48ee4b1b.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        개발 = 인수.sdk.resolve()
        산술 = sorted((개발 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 산술 or not (개발 / 'usr/include/stdio.h').is_file():
            പാഴ്_സർ_48ee4b1b.error('SDK must contain ARM64 musl headers and libgcc.a')
        설정시 = [തിരഞ്ഞെടുക്കല്_മൂല്യം for തിരഞ്ഞെടുക്കല്_മൂല്യം in സജ്ജീകരണം if തിരഞ്ഞെടുക്കല്_മൂല്യം != '-mgeneral-regs-only']
        ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = 새묶음 / '번역기.o'
        നടപ്പാക്കുക_കമാന്_ഡ്([번역기] + 설정시 + ['-ffunction-sections', '-fdata-sections',
             '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '시언어번역기', '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/tinycc', '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപയോക്താവ്',
             '-I', ബിൽഡ്_సిస్టమ్ / 'ccompiler', '-isystem', 개발 / 'usr/include', '-c', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '시언어번역기/번역기.c', '-o', ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം])
        നടപ്പാക്കുക_കമാന്_ഡ്([കണക്ടര്, '--gc-sections', '-T', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപയോക്താവ്/ലിങ്ക്_ലേഔട്ട്.ld', '-z', 'max-page-size=4096',
             '-o', ബിൽഡ്_సిస్టమ్ / 'user/cc.elf', ബിൽഡ്_సిస్టమ్ / 'user/start.o', ബിൽഡ്_సిస్టమ్ / 'user/runtime.o', ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം] +
             [ബിൽഡ്_సిస్టమ్ / 'ccompiler' / (പേരു് + '.o') for പേരു് in ('പൊതുവായ_ഭാഷ_പ്രവര്_ത്തന_സമയം_പിന്തുണ', 'നടപ്പിലാക്കുക', '미리번역', '되돌림')] +
             [ബിൽഡ്_సిస్టమ్ / 'user' / (പേരു് + '.o') for പേരു് in ('jar', 'tinflate', 'crc32', 'adler32')] + [산술[-1]])
        머리 = ബിൽഡ്_సిస్టమ్ / 'programs.h'
        머리.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 일치: 일치.group(1) + str((ബിൽഡ്_సిస్టమ్ / 'user/cc.elf').stat().st_size), 머리.read_text()))
        നടപ്പാക്കുക_കമാന്_ഡ്([번역기] + സജ്ജീകരണം + ['-c', ബിൽഡ്_సిస్టమ్ / 'programs.S', '-o', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'objects/programs.o'])
        നടപ്പാക്കുക_കമാന്_ഡ്([번역기] + സജ്ജീകരണം + ['-std=c11', '-I', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'posix-kor/arm64-native/포함', '-I', ബിൽഡ്_సిస్టమ్,
             '-c', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'മെഷീൻ/ഉപയോക്താവ്.c', '-o', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'objects/user.o'])
    നടപ്പാക്കുക_കമാന്_ഡ്([കണക്ടര്, '--gc-sections', '-T', പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / '부팅/ലിങ്ക്_ലേഔട്ട്.ld', '-o', 새묶음 / 'kernel.elf'] +
         [പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / വഴി for വഴി in 명세['objects']] + ['--start-group'] +
         [സുരക്ഷ_ബണ്ടിൽ if വഴി == 'objects/libassh.a' else പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / വഴി for വഴി in 명세['libraries']] + ['--end-group'])
    നടപ്പാക്കുക_കമാന്_ഡ്([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 새묶음 / 'kernel.elf', 새묶음 / 'kernel8.img'])
    ഹാഷ്_ഫയല് = hashlib.sha256((새묶음 / 'kernel8.img').read_bytes()).hexdigest()
    if 인수.verify and ഹാഷ്_ഫയല് != 명세['kernel_sha256']:
        raise SystemExit('재연결 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + ഹാഷ്_ഫയല്)
    print('RELINK PASS', ഹാഷ്_ഫയല്, 새묶음 / 'kernel8.img')


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
