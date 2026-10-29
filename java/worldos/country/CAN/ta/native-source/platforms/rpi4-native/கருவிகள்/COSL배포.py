#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL மூலம்_மரம்·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

திட்டப்பணி_மூலம் = Path(__file__).resolve().parents[1]
தொகுபதிவகம்_மூலம் = திட்டப்பணி_மூலம்.parents[1]
இலக்கு_பெயர் = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
நூலகம் = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ஹாஷ்_கோப்பு(பாதை_2):
    return hashlib.sha256(Path(பாதை_2).read_bytes()).hexdigest()


def 점검():
    for பெயர் in ('vendor/wolfssh', 'vendor/wolfssl', 'தொலைநிலை_மதிப்பு/user_settings.h'):
        if (திட்டப்பணி_மூலம் / பெயர்).exists():
            raise SystemExit('COSL 배포 நிறுத்து: 이전 GPL தொலைநிலை_மதிப்பு 구현이 மூலம்_மரம் 트리에 남아 있습니다: ' + பெயர்)
    கம்பியிலான_மதிப்பு = (திட்டப்பணி_மூலம் / 'பிணையம்_அடுக்கு_49fba3da/கம்பியிலான_பிணையம்.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in கம்பியிலான_மதிப்பு or 'SPDX-License-Identifier: GPL' in கம்பியிலான_மதிப்பு:
        raise SystemExit('COSL 배포 நிறுத்து: BSD GENET 구현·고지 சரிபார் 필요')
    for பெயர் in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (தொகுபதிவகம்_மூலம் / பெயர்).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + பெயர்)
    சின்னம்_மதிப்பு = subprocess.check_output(['aarch64-linux-gnu-nm', str(திட்டப்பணி_மூலம் / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', சின்னம்_மதிப்பு):
        raise SystemExit('COSL 배포 நிறுத்து: 커널에 이전 GPL கடவுச்சொல்_மதிப்பு/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for பெயர் in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + பெயர் + r'$', சின்னம்_மதிப்பு, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + பெயர்)
    with tempfile.TemporaryDirectory(dir=str(திட்டப்பணி_மூலம் / 'build')) as 임시:
        படம்_மதிப்பு = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(திட்டப்பணி_மூலம் / 'build/kernel.elf'), str(படம்_மதிப்பு)])
        if ஹாஷ்_கோப்பு(படம்_மதிப்பு) != ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம் / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    அறிக்கை_மதிப்பு = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம் / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {பெயர்: ஹாஷ்_கோப்பு(திட்டப்பணி_மூலம் / 'build' / பெயர்) for பெயர் in நூலகம்}}
    (திட்டப்பணி_மூலம் / 'build/cosl-distribution-check.json').write_text(json.dumps(அறிக்கை_மதிப்பு, ensure_ascii=False, indent=2) + '\n')
    return அறிக்கை_மதிப்பு


def கட்டு_முடிவுப்_புள்ளி():
    அறிக்கை_மதிப்பு = 점검()
    배포 = திட்டப்பணி_மூலம் / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(திட்டப்பணி_மூலம் / 'build')) as 임시:
        குழு_மதிப்பு = Path(임시) / 'jkoros-native-relink'
        குழு_மதிப்பு.mkdir()
        def நகலெடு_மதிப்பு(원본, பியர்_மதிப்பு):
            இலக்கு_மதிப்பு = குழு_மதிப்பு / பியர்_மதிப்பு
            இலக்கு_மதிப்பு.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(இலக்கு_மதிப்பு), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(இலக்கு_மதிப்பு))
        for பெயர் in இலக்கு_பெயர்:
            நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / 'build' / (பெயர் + '.o'), 'objects/' + பெயர் + '.o')
        for பெயர் in நூலகம்:
            நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / 'build' / பெயர், 'objects/' + Path(பெயர்).name)
        for பெயர் in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'பயனர்', '명명', 'இயந்திரம்', 'பிணையம்_அடுக்கு_49fba3da/பிணையம்_அடுக்கு_49fba3da.h', '부팅/இணை_லேஅவுட்.ld',
                     'தொலைநிலை_மதிப்பு/assh_config.h', 'தொலைநிலை_மதிப்பு/config.h', 'தொலைநிலை_மதிப்பு/ctype.h', 'தொலைநிலை_மதிப்பு/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / பெயர், பெயர்)
        for பெயர் in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            நகலெடு_மதிப்பு(தொகுபதிவகம்_மூலம் / பெயர், பெயர்)
        for பாதை_2 in sorted((திட்டப்பணி_மூலம் / 'vendor').glob('LICENSE*')):
            நகலெடு_மதிப்பு(பாதை_2, 'vendor/' + பாதை_2.name)
        நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        நகலெடு_மதிப்பு(தொகுபதிவகம்_மூலம் / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / 'கருவிகள்/재연결.py', 'relink.py')
        for பாதை_2 in sorted((திட்டப்பணி_மூலம் / 'build/user').glob('*.elf')):
            நகலெடு_மதிப்பு(பாதை_2, 'build/user/' + பாதை_2.name)
        for பெயர் in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / 'build/user' / (பெயர் + '.o'), 'build/user/' + பெயர் + '.o')
        for பெயர் in ('crt', 'aot-runtime', 'பொது_மொழி_இயக்க_நேரம்_ஆதரவு', 'செயல்படுத்துக', '미리번역', '되돌림'):
            நகலெடு_மதிப்பு(திட்டப்பணி_மூலம் / 'build/ccompiler' / (பெயர் + '.o'), 'build/ccompiler/' + பெயர் + '.o')
        명세 = dict(அறிக்கை_மதிப்பு, objects=['objects/' + பெயர் + '.o' for பெயர் in இலக்கு_பெயர்],
                    libraries=['objects/' + Path(பாதை_2).name for பாதை_2 in நூலகம்])
        (குழு_மதிப்பு / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (குழு_மதிப்பு / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        இலக்கு = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / இலக்கு.name
        with tarfile.open(str(임시압축), 'w:gz') as காப்பகம்_மதிப்பு:
            காப்பகம்_மதிப்பு.add(str(குழு_மதிப்பு), arcname=குழு_மதிப்பு.name)
        임시압축.replace(இலக்கு)
    அறிக்கை_மதிப்பு['relink_archive_sha256'] = ஹாஷ்_கோப்பு(இலக்கு)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(அறிக்கை_மதிப்பு, ensure_ascii=False, indent=2) + '\n')
    return இலக்கு


if __name__ == '__main__':
    பார்சர்_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    பார்சர்_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    மதிப்பு = பார்சர்_48ee4b1b.parse_args()
    if மதிப்பு.command == 'bundle':
        print('COSL source/relink kit:', கட்டு_முடிவுப்_புள்ளி())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
