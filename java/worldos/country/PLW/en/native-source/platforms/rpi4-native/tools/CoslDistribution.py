#!/usr/bin/env python3
"""currentItem Native ARM64 산출물을 검사하고 LGPL sourceTree·reconnectEndpoint 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

projectRoot = Path(__file__).resolve().parents[1]
repositoryRoot = projectRoot.parents[1]
destinationName = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
library = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hashFile(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inspectState():
    for name in ('vendor/wolfssh', 'vendor/wolfssl', 'remoteValue/user_settings.h'):
        if (projectRoot / name).exists():
            raise SystemExit('COSL distributionValue stop: previousItem GPL remoteValue 구현이 sourceTree 트리에 남아 있습니다: ' + name)
    wiredValue = (projectRoot / 'networkStack/wiredNetwork.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in wiredValue or 'SPDX-License-Identifier: GPL' in wiredValue:
        raise SystemExit('COSL distributionValue stop: BSD GENET implementation·고지 verify neededValue')
    for name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repositoryRoot / name).is_file():
            raise SystemExit('COSL distributionValue 고지 missingMethod: ' + name)
    symbolValue = subprocess.check_output(['aarch64-linux-gnu-nm', str(projectRoot / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbolValue):
        raise SystemExit('COSL distributionValue stop: 커널에 previousItem GPL passwordValue/SSH 심볼이 남아 있습니다. retryValue 빌드하세요.')
    for name in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + name + r'$', symbolValue, re.M):
            raise SystemExit('COSL 대체 implementation 누락: ' + name)
    with tempfile.TemporaryDirectory(dir=str(projectRoot / 'build')) as temporaryValue:
        imageValue = Path(temporaryValue) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(projectRoot / 'build/kernel.elf'), str(imageValue)])
        if hashFile(imageValue) != hashFile(projectRoot / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    reportValue = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hashFile(projectRoot / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {name: hashFile(projectRoot / 'build' / name) for name in library}}
    (projectRoot / 'build/cosl-distribution-check.json').write_text(json.dumps(reportValue, ensure_ascii=False, indent=2) + '\n')
    return reportValue


def bindEndpoint():
    reportValue = inspectState()
    distributionValue = projectRoot / 'dist'
    distributionValue.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(projectRoot / 'build')) as temporaryValue:
        groupValue = Path(temporaryValue) / 'jkoros-native-relink'
        groupValue.mkdir()
        def copyValue(original, peerValue):
            destinationValue = groupValue / peerValue
            destinationValue.parent.mkdir(parents=True, exist_ok=True)
            if original.is_dir():
                shutil.copytree(str(original), str(destinationValue), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(original), str(destinationValue))
        for name in destinationName:
            copyValue(projectRoot / 'build' / (name + '.o'), 'objects/' + name + '.o')
        for name in library:
            copyValue(projectRoot / 'build' / name, 'objects/' + Path(name).name)
        for name in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'CCompiler', 'User', 'naming', 'machine', 'networkStack/networkStack.h', 'machine_boot/link_layout.ld',
                     'remoteValue/assh_config.h', 'remoteValue/config.h', 'remoteValue/ctype.h', 'remoteValue/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'CoslDistributionGuide.md'):
            copyValue(projectRoot / name, name)
        for name in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            copyValue(repositoryRoot / name, name)
        for path in sorted((projectRoot / 'vendor').glob('LICENSE*')):
            copyValue(path, 'vendor/' + path.name)
        copyValue(projectRoot / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        copyValue(projectRoot / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        copyValue(repositoryRoot / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        copyValue(projectRoot / 'tools/reconnectEndpoint.py', 'relink.py')
        for path in sorted((projectRoot / 'build/user').glob('*.elf')):
            copyValue(path, 'build/user/' + path.name)
        for name in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            copyValue(projectRoot / 'build/user' / (name + '.o'), 'build/user/' + name + '.o')
        for name in ('crt', 'aot-runtime', 'RuntimeSupport', 'run', 'aheadOfTime', 'returnBridge'):
            copyValue(projectRoot / 'build/ccompiler' / (name + '.o'), 'build/ccompiler/' + name + '.o')
        specification = dict(reportValue, objects=['objects/' + name + '.o' for name in destinationName],
                    libraries=['objects/' + Path(path).name for path in library])
        (groupValue / 'relink.json').write_text(json.dumps(specification, ensure_ascii=False, indent=2) + '\n')
        (groupValue / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in CCompiler.
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
        targetValue = distributionValue / 'jkoros-native-relink.tar.gz'
        temporaryArchive = Path(temporaryValue) / targetValue.name
        with tarfile.open(str(temporaryArchive), 'w:gz') as archiveValue:
            archiveValue.add(str(groupValue), arcname=groupValue.name)
        temporaryArchive.replace(targetValue)
    reportValue['relink_archive_sha256'] = hashFile(targetValue)
    (distributionValue / 'cosl-distribution.json').write_text(json.dumps(reportValue, ensure_ascii=False, indent=2) + '\n')
    return targetValue


if __name__ == '__main__':
    Parser = argparse.ArgumentParser(description=__doc__)
    Parser.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    value = Parser.parse_args()
    if value.command == 'bundle':
        print('COSL source/relink kit:', bindEndpoint())
    else:
        print(json.dumps(inspectState(), ensure_ascii=False, indent=2))
