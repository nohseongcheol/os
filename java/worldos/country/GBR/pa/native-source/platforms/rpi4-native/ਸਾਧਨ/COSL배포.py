#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ਸਰੋਤ_ਟ੍ਰੀ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

ਪ੍ਰੋਜੈਕਟ_ਰੂਟ = Path(__file__).resolve().parents[1]
저장소 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ.parents[1]
ਮੰਜਿਲ_ਨਾਮ = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ਪੁਸਤਕਾਲਾ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਮਾਰਗ):
    return hashlib.sha256(Path(ਮਾਰਗ).read_bytes()).hexdigest()


def 점검():
    for ਨਾਂ in ('vendor/wolfssh', 'vendor/wolfssl', 'ਰਿਮੋਟ_ਕੀਮਤ/user_settings.h'):
        if (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / ਨਾਂ).exists():
            raise SystemExit('COSL 배포 ਰੋਕੋ: 이전 GPL ਰਿਮੋਟ_ਕੀਮਤ 구현이 ਸਰੋਤ_ਟ੍ਰੀ 트리에 남아 있습니다: ' + ਨਾਂ)
    ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ = (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਨੈਟਵਰਕ_ਸਟੈਕ/ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਨੈਟਵਰਕ.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ or 'SPDX-License-Identifier: GPL' in ਸਖ਼ਤ_ਮੇਹਨਤੀ_ਕੀਮਤ:
        raise SystemExit('COSL 배포 ਰੋਕੋ: BSD GENET 구현·고지 ਤਸਦੀਕ 필요')
    for ਨਾਂ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / ਨਾਂ).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ਨਾਂ)
    ਪ੍ਰਤੀਕ_ਕੀਮਤ = subprocess.check_output(['aarch64-linux-gnu-nm', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ਪ੍ਰਤੀਕ_ਕੀਮਤ):
        raise SystemExit('COSL 배포 ਰੋਕੋ: 커널에 이전 GPL ਪਾਸਵਰਡ_ਕੀਮਤ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ਨਾਂ in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ਨਾਂ + r'$', ਪ੍ਰਤੀਕ_ਕੀਮਤ, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ਨਾਂ)
    with tempfile.TemporaryDirectory(dir=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build')) as 임시:
        ਤਸਵੀਰ_ਕੀਮਤ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel.elf'), str(ਤਸਵੀਰ_ਕੀਮਤ)])
        if ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਤਸਵੀਰ_ਕੀਮਤ) != ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ਵਿਵਰਨ_ਕੀਮਤ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ਨਾਂ: ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build' / ਨਾਂ) for ਨਾਂ in ਪੁਸਤਕਾਲਾ}}
    (ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/cosl-distribution-check.json').write_text(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ, ensure_ascii=False, indent=2) + '\n')
    return ਵਿਵਰਨ_ਕੀਮਤ


def 묶기():
    ਵਿਵਰਨ_ਕੀਮਤ = 점검()
    배포 = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build')) as 임시:
        ਸਮੂਹ_ਕੀਮਤ = Path(임시) / 'jkoros-native-relink'
        ਸਮੂਹ_ਕੀਮਤ.mkdir()
        def ਇਨਸਟੈਂਸ_ਕੀਮਤ(원본, ਪਿਅਰ_ਕੀਮਤ):
            ਮੰਜਿਲ_ਕੀਮਤ = ਸਮੂਹ_ਕੀਮਤ / ਪਿਅਰ_ਕੀਮਤ
            ਮੰਜਿਲ_ਕੀਮਤ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ਮੰਜਿਲ_ਕੀਮਤ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ਮੰਜਿਲ_ਕੀਮਤ))
        for ਨਾਂ in ਮੰਜਿਲ_ਨਾਮ:
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build' / (ਨਾਂ + '.o'), 'objects/' + ਨਾਂ + '.o')
        for ਨਾਂ in ਪੁਸਤਕਾਲਾ:
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build' / ਨਾਂ, 'objects/' + Path(ਨਾਂ).name)
        for ਨਾਂ in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ਉਪਭੋਗਤਾ', '명명', 'ਮਸ਼ੀਨ', 'ਨੈਟਵਰਕ_ਸਟੈਕ/ਨੈਟਵਰਕ_ਸਟੈਕ.h', '부팅/ਲਿੰਕ_ਖਾਕਾ.ld',
                     'ਰਿਮੋਟ_ਕੀਮਤ/assh_config.h', 'ਰਿਮੋਟ_ਕੀਮਤ/config.h', 'ਰਿਮੋਟ_ਕੀਮਤ/ctype.h', 'ਰਿਮੋਟ_ਕੀਮਤ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / ਨਾਂ, ਨਾਂ)
        for ਨਾਂ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(저장소 / ਨਾਂ, ਨਾਂ)
        for ਮਾਰਗ in sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor').glob('LICENSE*')):
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਮਾਰਗ, 'vendor/' + ਮਾਰਗ.name)
        ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ਇਨਸਟੈਂਸ_ਕੀਮਤ(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'ਸਾਧਨ/재연결.py', 'relink.py')
        for ਮਾਰਗ in sorted((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user').glob('*.elf')):
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਮਾਰਗ, 'build/user/' + ਮਾਰਗ.name)
        for ਨਾਂ in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/user' / (ਨਾਂ + '.o'), 'build/user/' + ਨਾਂ + '.o')
        for ਨਾਂ in ('crt', 'aot-runtime', 'ਸਾਧਾਰਨ_ਭਾਸ਼ਾ_ਰਨਟਾਈਮ_ਸਮਰਥਨ', 'ਚਲਾਓ_2', '미리번역', '되돌림'):
            ਇਨਸਟੈਂਸ_ਕੀਮਤ(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/ccompiler' / (ਨਾਂ + '.o'), 'build/ccompiler/' + ਨਾਂ + '.o')
        명세 = dict(ਵਿਵਰਨ_ਕੀਮਤ, objects=['objects/' + ਨਾਂ + '.o' for ਨਾਂ in ਮੰਜਿਲ_ਨਾਮ],
                    libraries=['objects/' + Path(ਮਾਰਗ).name for ਮਾਰਗ in ਪੁਸਤਕਾਲਾ])
        (ਸਮੂਹ_ਕੀਮਤ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ਸਮੂਹ_ਕੀਮਤ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ਟੀਚਾ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ਟੀਚਾ.name
        with tarfile.open(str(임시압축), 'w:gz') as ਸੰਗ੍ਰਹਿ_ਕੀਮਤ:
            ਸੰਗ੍ਰਹਿ_ਕੀਮਤ.add(str(ਸਮੂਹ_ਕੀਮਤ), arcname=ਸਮੂਹ_ਕੀਮਤ.name)
        임시압축.replace(ਟੀਚਾ)
    ਵਿਵਰਨ_ਕੀਮਤ['relink_archive_sha256'] = ਹੈਸ਼_ਲਿਖਤ_ਪੱਤਰ(ਟੀਚਾ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ, ensure_ascii=False, indent=2) + '\n')
    return ਟੀਚਾ


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ਕੀਮਤ = 해석기.parse_args()
    if ਕੀਮਤ.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
