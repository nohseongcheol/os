#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ምንጭ_ዛፍ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

አሳይ_ስር = Path(__file__).resolve().parents[1]
ማከማቻ_ስር = አሳይ_ስር.parents[1]
መድረሻ_ስም = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ማከማቻ_ስፍራ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ሃሽ_ፋይል(መተላለፊያ):
    return hashlib.sha256(Path(መተላለፊያ).read_bytes()).hexdigest()


def 점검():
    for ስም in ('vendor/wolfssh', 'vendor/wolfssl', 'የሩቅ_እሴት/user_settings.h'):
        if (አሳይ_ስር / ስም).exists():
            raise SystemExit('COSL 배포 ማስቆሚያ: 이전 GPL የሩቅ_እሴት 구현이 ምንጭ_ዛፍ 트리에 남아 있습니다: ' + ስም)
    ባለሽቦ_እሴት = (አሳይ_ስር / 'መረብ_ክምር/ባለሽቦ_መረብ.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ባለሽቦ_እሴት or 'SPDX-License-Identifier: GPL' in ባለሽቦ_እሴት:
        raise SystemExit('COSL 배포 ማስቆሚያ: BSD GENET 구현·고지 አረጋግጥ 필요')
    for ስም in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (ማከማቻ_ስር / ስም).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ስም)
    ምልክት_እሴት = subprocess.check_output(['aarch64-linux-gnu-nm', str(አሳይ_ስር / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ምልክት_እሴት):
        raise SystemExit('COSL 배포 ማስቆሚያ: 커널에 이전 GPL የይለፍ_ቃል_እሴት/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ስም in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ስም + r'$', ምልክት_እሴት, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ስም)
    with tempfile.TemporaryDirectory(dir=str(አሳይ_ስር / 'build')) as 임시:
        ምስል_እሴት = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(አሳይ_ስር / 'build/kernel.elf'), str(ምስል_እሴት)])
        if ሃሽ_ፋይል(ምስል_እሴት) != ሃሽ_ፋይል(አሳይ_ስር / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ዘገባ_እሴት = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ሃሽ_ፋይል(አሳይ_ስር / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ስም: ሃሽ_ፋይል(አሳይ_ስር / 'build' / ስም) for ስም in ማከማቻ_ስፍራ}}
    (አሳይ_ስር / 'build/cosl-distribution-check.json').write_text(json.dumps(ዘገባ_እሴት, ensure_ascii=False, indent=2) + '\n')
    return ዘገባ_እሴት


def 묶기():
    ዘገባ_እሴት = 점검()
    배포 = አሳይ_ስር / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(አሳይ_ስር / 'build')) as 임시:
        ቡድን_እሴት = Path(임시) / 'jkoros-native-relink'
        ቡድን_እሴት.mkdir()
        def ቅዳ_እሴት(원본, አቻ_እሴት):
            መድረሻ_እሴት = ቡድን_እሴት / አቻ_እሴት
            መድረሻ_እሴት.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(መድረሻ_እሴት), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(መድረሻ_እሴት))
        for ስም in መድረሻ_ስም:
            ቅዳ_እሴት(አሳይ_ስር / 'build' / (ስም + '.o'), 'objects/' + ስም + '.o')
        for ስም in ማከማቻ_ስፍራ:
            ቅዳ_እሴት(አሳይ_ስር / 'build' / ስም, 'objects/' + Path(ስም).name)
        for ስም in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ተጠቃሚ', '명명', 'ማሽን', 'መረብ_ክምር/መረብ_ክምር.h', '부팅/አገናኝ_አሰሳ.ld',
                     'የሩቅ_እሴት/assh_config.h', 'የሩቅ_እሴት/config.h', 'የሩቅ_እሴት/ctype.h', 'የሩቅ_እሴት/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ቅዳ_እሴት(አሳይ_ስር / ስም, ስም)
        for ስም in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ቅዳ_እሴት(ማከማቻ_ስር / ስም, ስም)
        for መተላለፊያ in sorted((አሳይ_ስር / 'vendor').glob('LICENSE*')):
            ቅዳ_እሴት(መተላለፊያ, 'vendor/' + መተላለፊያ.name)
        ቅዳ_እሴት(አሳይ_ስር / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ቅዳ_እሴት(አሳይ_ስር / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ቅዳ_እሴት(ማከማቻ_ስር / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ቅዳ_እሴት(አሳይ_ስር / 'መሳሪያዎች/재연결.py', 'relink.py')
        for መተላለፊያ in sorted((አሳይ_ስር / 'build/user').glob('*.elf')):
            ቅዳ_እሴት(መተላለፊያ, 'build/user/' + መተላለፊያ.name)
        for ስም in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ቅዳ_እሴት(አሳይ_ስር / 'build/user' / (ስም + '.o'), 'build/user/' + ስም + '.o')
        for ስም in ('crt', 'aot-runtime', 'የጋራ_ቋንቋ_ማስኬጃ_ጊዜ_ድገፍ', 'ማስኬጃ', '미리번역', '되돌림'):
            ቅዳ_እሴት(አሳይ_ስር / 'build/ccompiler' / (ስም + '.o'), 'build/ccompiler/' + ስም + '.o')
        명세 = dict(ዘገባ_እሴት, objects=['objects/' + ስም + '.o' for ስም in መድረሻ_ስም],
                    libraries=['objects/' + Path(መተላለፊያ).name for መተላለፊያ in ማከማቻ_ስፍራ])
        (ቡድን_እሴት / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ቡድን_እሴት / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ዓላማ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ዓላማ.name
        with tarfile.open(str(임시압축), 'w:gz') as ከዝን_እሴት:
            ከዝን_እሴት.add(str(ቡድን_እሴት), arcname=ቡድን_እሴት.name)
        임시압축.replace(ዓላማ)
    ዘገባ_እሴት['relink_archive_sha256'] = ሃሽ_ፋይል(ዓላማ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ዘገባ_እሴት, ensure_ascii=False, indent=2) + '\n')
    return ዓላማ


if __name__ == '__main__':
    አግልሎ_ማስቀመጥ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    አግልሎ_ማስቀመጥ_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    እሴት = አግልሎ_ማስቀመጥ_48ee4b1b.parse_args()
    if እሴት.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
