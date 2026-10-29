#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL మూలం_వృక్షాకృతి·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

ప్రొజెక్ట్_మూలం = Path(__file__).resolve().parents[1]
రిపోజిటరీ_మూలం = ప్రొజెక్ట్_మూలం.parents[1]
గమ్యం_పేరు = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
లైబ్రరీ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def హాష్_ఫైలు(పాత్):
    return hashlib.sha256(Path(పాత్).read_bytes()).hexdigest()


def 점검():
    for పేరు in ('vendor/wolfssh', 'vendor/wolfssl', 'రిమోట్_మూల్యం/user_settings.h'):
        if (ప్రొజెక్ట్_మూలం / పేరు).exists():
            raise SystemExit('COSL 배포 నిలిపి_వేయు: 이전 GPL రిమోట్_మూల్యం 구현이 మూలం_వృక్షాకృతి 트리에 남아 있습니다: ' + పేరు)
    తంత్రీసంధాన_మూల్యం = (ప్రొజెక్ట్_మూలం / 'నెట్_వర్క్_దొంతర/తంత్రీసంధాన_నెట్_వర్క్.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in తంత్రీసంధాన_మూల్యం or 'SPDX-License-Identifier: GPL' in తంత్రీసంధాన_మూల్యం:
        raise SystemExit('COSL 배포 నిలిపి_వేయు: BSD GENET 구현·고지 సరిచూడు 필요')
    for పేరు in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (రిపోజిటరీ_మూలం / పేరు).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + పేరు)
    చిహ్నం_మూల్యం = subprocess.check_output(['aarch64-linux-gnu-nm', str(ప్రొజెక్ట్_మూలం / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', చిహ్నం_మూల్యం):
        raise SystemExit('COSL 배포 నిలిపి_వేయు: 커널에 이전 GPL అనుమతిపదం_మూల్యం/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for పేరు in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + పేరు + r'$', చిహ్నం_మూల్యం, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + పేరు)
    with tempfile.TemporaryDirectory(dir=str(ప్రొజెక్ట్_మూలం / 'build')) as 임시:
        చిత్రం_మూల్యం = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(ప్రొజెక్ట్_మూలం / 'build/kernel.elf'), str(చిత్రం_మూల్యం)])
        if హాష్_ఫైలు(చిత్రం_మూల్యం) != హాష్_ఫైలు(ప్రొజెక్ట్_మూలం / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    నివేదిక_మూల్యం = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': హాష్_ఫైలు(ప్రొజెక్ట్_మూలం / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {పేరు: హాష్_ఫైలు(ప్రొజెక్ట్_మూలం / 'build' / పేరు) for పేరు in లైబ్రరీ}}
    (ప్రొజెక్ట్_మూలం / 'build/cosl-distribution-check.json').write_text(json.dumps(నివేదిక_మూల్యం, ensure_ascii=False, indent=2) + '\n')
    return నివేదిక_మూల్యం


def 묶기():
    నివేదిక_మూల్యం = 점검()
    배포 = ప్రొజెక్ట్_మూలం / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(ప్రొజెక్ట్_మూలం / 'build')) as 임시:
        సమూహం_మూల్యం = Path(임시) / 'jkoros-native-relink'
        సమూహం_మూల్యం.mkdir()
        def కాపీ_మూల్యం(원본, పియర్_మూల్యం):
            గమ్యం_మూల్యం = సమూహం_మూల్యం / పియర్_మూల్యం
            గమ్యం_మూల్యం.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(గమ్యం_మూల్యం), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(గమ్యం_మూల్యం))
        for పేరు in గమ్యం_పేరు:
            కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / 'build' / (పేరు + '.o'), 'objects/' + పేరు + '.o')
        for పేరు in లైబ్రరీ:
            కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / 'build' / పేరు, 'objects/' + Path(పేరు).name)
        for పేరు in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'వినియోగదారు', '명명', 'యంత్రం', 'నెట్_వర్క్_దొంతర/నెట్_వర్క్_దొంతర.h', '부팅/బంధం_లేవుట్.ld',
                     'రిమోట్_మూల్యం/assh_config.h', 'రిమోట్_మూల్యం/config.h', 'రిమోట్_మూల్యం/ctype.h', 'రిమోట్_మూల్యం/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / పేరు, పేరు)
        for పేరు in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            కాపీ_మూల్యం(రిపోజిటరీ_మూలం / పేరు, పేరు)
        for పాత్ in sorted((ప్రొజెక్ట్_మూలం / 'vendor').glob('LICENSE*')):
            కాపీ_మూల్యం(పాత్, 'vendor/' + పాత్.name)
        కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        కాపీ_మూల్యం(రిపోజిటరీ_మూలం / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / 'ఉపకరణాలు/재연결.py', 'relink.py')
        for పాత్ in sorted((ప్రొజెక్ట్_మూలం / 'build/user').glob('*.elf')):
            కాపీ_మూల్యం(పాత్, 'build/user/' + పాత్.name)
        for పేరు in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / 'build/user' / (పేరు + '.o'), 'build/user/' + పేరు + '.o')
        for పేరు in ('crt', 'aot-runtime', 'సాధారణ_భాష_అమలు_సమయం_మద్దతు', 'నడుపుము', '미리번역', '되돌림'):
            కాపీ_మూల్యం(ప్రొజెక్ట్_మూలం / 'build/ccompiler' / (పేరు + '.o'), 'build/ccompiler/' + పేరు + '.o')
        명세 = dict(నివేదిక_మూల్యం, objects=['objects/' + పేరు + '.o' for పేరు in గమ్యం_పేరు],
                    libraries=['objects/' + Path(పాత్).name for పాత్ in లైబ్రరీ])
        (సమూహం_మూల్యం / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (సమూహం_మూల్యం / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        లక్ష్యం = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / లక్ష్యం.name
        with tarfile.open(str(임시압축), 'w:gz') as ఆర్కైవ్_మూల్యం:
            ఆర్కైవ్_మూల్యం.add(str(సమూహం_మూల్యం), arcname=సమూహం_మూల్యం.name)
        임시압축.replace(లక్ష్యం)
    నివేదిక_మూల్యం['relink_archive_sha256'] = హాష్_ఫైలు(లక్ష్యం)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(నివేదిక_మూల్యం, ensure_ascii=False, indent=2) + '\n')
    return లక్ష్యం


if __name__ == '__main__':
    పార్సర్_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    పార్సర్_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    మూల్యం = పార్సర్_48ee4b1b.parse_args()
    if మూల్యం.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
