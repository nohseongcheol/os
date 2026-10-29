#!/usr/bin/env python3
"""נוכחי_פריט עצמי ARM64 산출물을 검사하고 LGPL מקור_עץ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

לשקף_בסיס = Path(__file__).resolve().parents[1]
מאגר_בסיס = לשקף_בסיס.parents[1]
יעד_שם = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ספריה = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def קוד_Hash_קובץ(נתיב):
    return hashlib.sha256(Path(נתיב).read_bytes()).hexdigest()


def 점검():
    for שם in ('vendor/wolfssh', 'vendor/wolfssl', 'מרוחק_ערך/user_settings.h'):
        if (לשקף_בסיס / שם).exists():
            raise SystemExit('COSL הפצה_ערך עצירה: 이전 GPL מרוחק_ערך 구현이 מקור_עץ 트리에 남아 있습니다: ' + שם)
    קווי_ערך = (לשקף_בסיס / 'רשת_רמז/קווי_רשת.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in קווי_ערך or 'SPDX-License-Identifier: GPL' in קווי_ערך:
        raise SystemExit('COSL הפצה_ערך עצירה: BSD GENET 구현·고지 ודא_אמת 필요')
    for שם in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (מאגר_בסיס / שם).is_file():
            raise SystemExit('COSL הפצה_ערך 고지 없음: ' + שם)
    סימן_ערך = subprocess.check_output(['aarch64-linux-gnu-nm', str(לשקף_בסיס / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', סימן_ערך):
        raise SystemExit('COSL הפצה_ערך עצירה: 커널에 이전 GPL סיסמה_ערך/SSH 심볼이 남아 있습니다. נסה_שנית_ערך 빌드하세요.')
    for שם in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + שם + r'$', סימן_ערך, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + שם)
    with tempfile.TemporaryDirectory(dir=str(לשקף_בסיס / 'build')) as 임시:
        תמונה_ערך = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(לשקף_בסיס / 'build/kernel.elf'), str(תמונה_ערך)])
        if קוד_Hash_קובץ(תמונה_ערך) != קוד_Hash_קובץ(לשקף_בסיס / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    דוח_ערך_ddf2aaf3 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': קוד_Hash_קובץ(לשקף_בסיס / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {שם: קוד_Hash_קובץ(לשקף_בסיס / 'build' / שם) for שם in ספריה}}
    (לשקף_בסיס / 'build/cosl-distribution-check.json').write_text(json.dumps(דוח_ערך_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return דוח_ערך_ddf2aaf3


def לאגד_משתתף():
    דוח_ערך_ddf2aaf3 = 점검()
    הפצה_ערך = לשקף_בסיס / 'dist'
    הפצה_ערך.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(לשקף_בסיס / 'build')) as 임시:
        לקבץ_ערך = Path(임시) / 'jkoros-native-relink'
        לקבץ_ערך.mkdir()
        def מופע_ערך(원본, עמית_ערך):
            יעד_ערך = לקבץ_ערך / עמית_ערך
            יעד_ערך.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(יעד_ערך), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(יעד_ערך))
        for שם in יעד_שם:
            מופע_ערך(לשקף_בסיס / 'build' / (שם + '.o'), 'objects/' + שם + '.o')
        for שם in ספריה:
            מופע_ערך(לשקף_בסיס / 'build' / שם, 'objects/' + Path(שם).name)
        for שם in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'מ_מהדר', 'משתמש', '명명', 'מחשב', 'רשת_רמז/רשת_רמז.h', '부팅/לקשר_ניווט.ld',
                     'מרוחק_ערך/assh_config.h', 'מרוחק_ערך/config.h', 'מרוחק_ערך/ctype.h', 'מרוחק_ערך/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            מופע_ערך(לשקף_בסיס / שם, שם)
        for שם in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            מופע_ערך(מאגר_בסיס / שם, שם)
        for נתיב in sorted((לשקף_בסיס / 'vendor').glob('LICENSE*')):
            מופע_ערך(נתיב, 'vendor/' + נתיב.name)
        מופע_ערך(לשקף_בסיס / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        מופע_ערך(לשקף_בסיס / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        מופע_ערך(מאגר_בסיס / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        מופע_ערך(לשקף_בסיס / 'כלים/재연결.py', 'relink.py')
        for נתיב in sorted((לשקף_בסיס / 'build/user').glob('*.elf')):
            מופע_ערך(נתיב, 'build/user/' + נתיב.name)
        for שם in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            מופע_ערך(לשקף_בסיס / 'build/user' / (שם + '.o'), 'build/user/' + שם + '.o')
        for שם in ('crt', 'aot-runtime', 'זמן_ריצה_תמך', 'הפעלה', '미리번역', 'החזר_גשר'):
            מופע_ערך(לשקף_בסיס / 'build/ccompiler' / (שם + '.o'), 'build/ccompiler/' + שם + '.o')
        מפרט = dict(דוח_ערך_ddf2aaf3, objects=['objects/' + שם + '.o' for שם in יעד_שם],
                    libraries=['objects/' + Path(נתיב).name for נתיב in ספריה])
        (לקבץ_ערך / 'relink.json').write_text(json.dumps(מפרט, ensure_ascii=False, indent=2) + '\n')
        (לקבץ_ערך / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in מ_מהדר.
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
        יעד = הפצה_ערך / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / יעד.name
        with tarfile.open(str(임시압축), 'w:gz') as ארכיון_ערך:
            ארכיון_ערך.add(str(לקבץ_ערך), arcname=לקבץ_ערך.name)
        임시압축.replace(יעד)
    דוח_ערך_ddf2aaf3['relink_archive_sha256'] = קוד_Hash_קובץ(יעד)
    (הפצה_ערך / 'cosl-distribution.json').write_text(json.dumps(דוח_ערך_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return יעד


if __name__ == '__main__':
    מנתח_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    מנתח_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ערך = מנתח_48ee4b1b.parse_args()
    if ערך.command == 'bundle':
        print('COSL source/relink kit:', לאגד_משתתף())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
