#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ഉറവിടം_ശാഖി·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം = Path(__file__).resolve().parents[1]
കലവറ_വർഗ്ഗമൂലം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം.parents[1]
ഉദ്ദിഷ്ടസ്ഥാനം_നാ_മം = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
లైబ్రరీ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ഹാഷ്_ഫയല്(വഴി):
    return hashlib.sha256(Path(വഴി).read_bytes()).hexdigest()


def 점검():
    for പേരു് in ('vendor/wolfssh', 'vendor/wolfssl', 'വിദൂര_മൂല്യം/user_settings.h'):
        if (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / പേരു്).exists():
            raise SystemExit('COSL 배포 നിര്_ത്തുക: 이전 GPL വിദൂര_മൂല്യം 구현이 ഉറവിടം_ശാഖി 트리에 남아 있습니다: ' + പേരു്)
    പരസ്പരബന്ധിതമായ_മൂല്യം = (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക/പരസ്പരബന്ധിതമായ_നെറ്റ്_വർക്ക്.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in പരസ്പരബന്ധിതമായ_മൂല്യം or 'SPDX-License-Identifier: GPL' in പരസ്പരബന്ധിതമായ_മൂല്യം:
        raise SystemExit('COSL 배포 നിര്_ത്തുക: BSD GENET 구현·고지 പരിശോധിക്കുക 필요')
    for പേരു് in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (കലവറ_വർഗ്ഗമൂലം / പേരു്).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + പേരു്)
    nbsp_ചിഹ്നം_മൂല്യം = subprocess.check_output(['aarch64-linux-gnu-nm', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', nbsp_ചിഹ്നം_മൂല്യം):
        raise SystemExit('COSL 배포 നിര്_ത്തുക: 커널에 이전 GPL പാസ്_വേഡ്_മൂല്യം/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for പേരു് in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + പേരു് + r'$', nbsp_ചിഹ്നം_മൂല്യം, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + പേരു്)
    with tempfile.TemporaryDirectory(dir=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build')) as 임시:
        ഇമേജ്_മൂല്യം = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel.elf'), str(ഇമേജ്_മൂല്യം)])
        if ഹാഷ്_ഫയല്(ഇമേജ്_മൂല്യം) != ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    నివేదిక_മൂല്യം = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {പേരു്: ഹാഷ്_ഫയല്(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build' / പേരു്) for പേരു് in లైబ్రరీ}}
    (പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/cosl-distribution-check.json').write_text(json.dumps(నివేదిక_മൂല്യം, ensure_ascii=False, indent=2) + '\n')
    return నివేదిక_മൂല്യം


def బైండ్_చేయి_അവസാനബിന്ദു():
    నివేదిక_മൂല്യം = 점검()
    배포 = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build')) as 임시:
        സംഘം_മൂല്യം = Path(임시) / 'jkoros-native-relink'
        സംഘം_മൂല്യം.mkdir()
        def ദൃഷ്ടാന്തം_മൂല്യം(원본, പീര്_മൂല്യം):
            ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം = സംഘം_മൂല്യം / പീര്_മൂല്യം
            ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം))
        for പേരു് in ഉദ്ദിഷ്ടസ്ഥാനം_നാ_മം:
            ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build' / (പേരു് + '.o'), 'objects/' + പേരു് + '.o')
        for പേരു് in లైబ్రరీ:
            ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build' / പേരു്, 'objects/' + Path(പേരു്).name)
        for പേരു് in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ഉപയോക്താവ്', '명명', 'മെഷീൻ', 'നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക/നെറ്റ്_വർക്ക്_സ്റ്റാക്ക്_ചെയ്യുക.h', '부팅/ലിങ്ക്_ലേഔട്ട്.ld',
                     'വിദൂര_മൂല്യം/assh_config.h', 'വിദൂര_മൂല്യം/config.h', 'വിദൂര_മൂല്യം/ctype.h', 'വിദൂര_മൂല്യം/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / പേരു്, പേരു്)
        for പേരു് in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ദൃഷ്ടാന്തം_മൂല്യം(കലവറ_വർഗ്ഗമൂലം / പേരു്, പേരു്)
        for വഴി in sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor').glob('LICENSE*')):
            ദൃഷ്ടാന്തം_മൂല്യം(വഴി, 'vendor/' + വഴി.name)
        ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ദൃഷ്ടാന്തം_മൂല്യം(കലവറ_വർഗ്ഗമൂലം / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'ഉപകരണങ്ങൾ/재연결.py', 'relink.py')
        for വഴി in sorted((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user').glob('*.elf')):
            ദൃഷ്ടാന്തം_മൂല്യം(വഴി, 'build/user/' + വഴി.name)
        for പേരു് in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/user' / (പേരു് + '.o'), 'build/user/' + പേരു് + '.o')
        for പേരു് in ('crt', 'aot-runtime', 'പൊതുവായ_ഭാഷ_പ്രവര്_ത്തന_സമയം_പിന്തുണ', 'നടപ്പിലാക്കുക', '미리번역', '되돌림'):
            ദൃഷ്ടാന്തം_മൂല്യം(പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/ccompiler' / (പേരു് + '.o'), 'build/ccompiler/' + പേരു് + '.o')
        명세 = dict(నివేదిక_മൂല്യം, objects=['objects/' + പേരു് + '.o' for പേരു് in ഉദ്ദിഷ്ടസ്ഥാനം_നാ_മം],
                    libraries=['objects/' + Path(വഴി).name for വഴി in లైబ్రరీ])
        (സംഘം_മൂല്യം / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (സംഘം_മൂല്യം / 'README.md').write_text('''# jkoros native LGPL source and relink kit

This kit accompanies the matching kernel image. Retain it with binary distributions.
Application terms: LICENSE. Library terms: vendor/libassh/COPYING and vendor/tinycc/COPYING.
Other notices: THIRD_PARTY_NOTICES.md. COSL does not override the LGPL permissions.
This product includes software developed by Bill Paul.

Host dependencies: Python 3, Clang supporting aarch64-none-elf, libnewlib-dev headers,
and aarch64-linux-gnu binutils. No Linux kernel is linked into the guest.

From this extracted directory:

    python3 relink.py --verify

This recompiles libassh from the included source/configuration and relinks the kernel.
The original unmodified library must produce the recorded kernel SHA256.
To change libassh, edit vendor/libassh/src, then run without --verify.
Alternatively: python3 relink.py --libassh-archive /path/to/modified/libassh.a

TinyCC source is included in vendor/tinycc; the native port is in 시언어번역기.
To rebuild a modified TinyCC and replace its embedded executable:

    python3 relink.py --tinycc --sdk /path/to/alpine-arm64-rootfs

Use the same Alpine 3.24.2 ARM64 SDK headers and GCC 15.2.0 libgcc runtime as the
original build (jkoros/platforms/rpi4: make prepare-runtime; see that platform's docs).
The SDK is a host build prerequisite and is not included here. Its libgcc exception
and GPL text are in vendor/LICENSE.libgcc-runtime and vendor/LICENSE.gcc-gpl3.
GCC sources: https://gcc.gnu.org/pub/gcc/releases/gcc-15.2.0/
Both the cc ELF size table and user/program objects are regenerated when --tinycc is used.
Output: build/relinked/kernel8.img. Boot it using the same Pi4 firmware/config or QEMU
runner as the original image. There is no signature lock against modified libraries.

This is a relink kit for one device image. Objects contain the same embedded device
key as that image. Keep personal development images and build/remote credentials
out of public source uploads; provision appropriate images for recipients.
''')
        ലക്_ഷ്യം = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ലക്_ഷ്യം.name
        with tarfile.open(str(임시압축), 'w:gz') as ശേഖരം_മൂല്യം:
            ശേഖരം_മൂല്യം.add(str(സംഘം_മൂല്യം), arcname=സംഘം_മൂല്യം.name)
        임시압축.replace(ലക്_ഷ്യം)
    నివేదిక_മൂല്യം['relink_archive_sha256'] = ഹാഷ്_ഫയല്(ലക്_ഷ്യം)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(నివేదిక_മൂല്യം, ensure_ascii=False, indent=2) + '\n')
    return ലക്_ഷ്യം


if __name__ == '__main__':
    പാഴ്_സർ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    പാഴ്_സർ_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    മൂല്യം = പാഴ്_സർ_48ee4b1b.parse_args()
    if മൂല്യം.command == 'bundle':
        print('COSL source/relink kit:', బైండ్_చేయి_അവസാനബിന്ദു())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
