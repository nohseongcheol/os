#!/usr/bin/env python3
"""ปัจจุบัน_รายการ เอง ARM64 산출물을 검사하고 LGPL แหล่ง_ทรี·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

แสดง_ราก = Path(__file__).resolve().parents[1]
ที่เก็บ_ราก = แสดง_ราก.parents[1]
ปลายทาง_ชื่อ = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ไลบรารี = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def แฮช_แฟ้ม(เส้นทาง):
    return hashlib.sha256(Path(เส้นทาง).read_bytes()).hexdigest()


def 점검():
    for ชื่อ in ('vendor/wolfssh', 'vendor/wolfssl', 'ระยะไกล_ค่า/user_settings.h'):
        if (แสดง_ราก / ชื่อ).exists():
            raise SystemExit('COSL การกระจาย_ค่า หยุด: 이전 GPL ระยะไกล_ค่า 구현이 แหล่ง_ทรี 트리에 남아 있습니다: ' + ชื่อ)
    แบบผ่านสาย_ค่า = (แสดง_ราก / 'เครือข่าย_สแตก/แบบผ่านสาย_เครือข่าย.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in แบบผ่านสาย_ค่า or 'SPDX-License-Identifier: GPL' in แบบผ่านสาย_ค่า:
        raise SystemExit('COSL การกระจาย_ค่า หยุด: BSD GENET 구현·고지 ยืนยัน 필요')
    for ชื่อ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (ที่เก็บ_ราก / ชื่อ).is_file():
            raise SystemExit('COSL การกระจาย_ค่า 고지 없음: ' + ชื่อ)
    สัญลักษณ์_ค่า = subprocess.check_output(['aarch64-linux-gnu-nm', str(แสดง_ราก / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', สัญลักษณ์_ค่า):
        raise SystemExit('COSL การกระจาย_ค่า หยุด: 커널에 이전 GPL รหัสผ่าน_ค่า/SSH 심볼이 남아 있습니다. ลองอีกครั้ง_ค่า 빌드하세요.')
    for ชื่อ in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ชื่อ + r'$', สัญลักษณ์_ค่า, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ชื่อ)
    with tempfile.TemporaryDirectory(dir=str(แสดง_ราก / 'build')) as 임시:
        รูป_ค่า = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(แสดง_ราก / 'build/kernel.elf'), str(รูป_ค่า)])
        if แฮช_แฟ้ม(รูป_ค่า) != แฮช_แฟ้ม(แสดง_ราก / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    รายงาน_ค่า = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': แฮช_แฟ้ม(แสดง_ราก / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ชื่อ: แฮช_แฟ้ม(แสดง_ราก / 'build' / ชื่อ) for ชื่อ in ไลบรารี}}
    (แสดง_ราก / 'build/cosl-distribution-check.json').write_text(json.dumps(รายงาน_ค่า, ensure_ascii=False, indent=2) + '\n')
    return รายงาน_ค่า


def ผูก_ปลายทาง():
    รายงาน_ค่า = 점검()
    การกระจาย_ค่า = แสดง_ราก / 'dist'
    การกระจาย_ค่า.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(แสดง_ราก / 'build')) as 임시:
        กลุ่ม_ค่า = Path(임시) / 'jkoros-native-relink'
        กลุ่ม_ค่า.mkdir()
        def คัดลอก_ค่า(원본, ชั้น_ค่า):
            ปลายทาง_ค่า_a0fbc067 = กลุ่ม_ค่า / ชั้น_ค่า
            ปลายทาง_ค่า_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ปลายทาง_ค่า_a0fbc067), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ปลายทาง_ค่า_a0fbc067))
        for ชื่อ in ปลายทาง_ชื่อ:
            คัดลอก_ค่า(แสดง_ราก / 'build' / (ชื่อ + '.o'), 'objects/' + ชื่อ + '.o')
        for ชื่อ in ไลบรารี:
            คัดลอก_ค่า(แสดง_ราก / 'build' / ชื่อ, 'objects/' + Path(ชื่อ).name)
        for ชื่อ in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ผู้ใช้', '명명', 'เครื่อง', 'เครือข่าย_สแตก/เครือข่าย_สแตก.h', '부팅/ลิงก์_การนําทาง.ld',
                     'ระยะไกล_ค่า/assh_config.h', 'ระยะไกล_ค่า/config.h', 'ระยะไกล_ค่า/ctype.h', 'ระยะไกล_ค่า/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            คัดลอก_ค่า(แสดง_ราก / ชื่อ, ชื่อ)
        for ชื่อ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            คัดลอก_ค่า(ที่เก็บ_ราก / ชื่อ, ชื่อ)
        for เส้นทาง in sorted((แสดง_ราก / 'vendor').glob('LICENSE*')):
            คัดลอก_ค่า(เส้นทาง, 'vendor/' + เส้นทาง.name)
        คัดลอก_ค่า(แสดง_ราก / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        คัดลอก_ค่า(แสดง_ราก / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        คัดลอก_ค่า(ที่เก็บ_ราก / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        คัดลอก_ค่า(แสดง_ราก / 'เครื่องมือ/재연결.py', 'relink.py')
        for เส้นทาง in sorted((แสดง_ราก / 'build/user').glob('*.elf')):
            คัดลอก_ค่า(เส้นทาง, 'build/user/' + เส้นทาง.name)
        for ชื่อ in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            คัดลอก_ค่า(แสดง_ราก / 'build/user' / (ชื่อ + '.o'), 'build/user/' + ชื่อ + '.o')
        for ชื่อ in ('crt', 'aot-runtime', 'รันไทม์_สนับสนุน', 'เรียกใช้งาน', '미리번역', 'ส่งคืน_บริดจ์'):
            คัดลอก_ค่า(แสดง_ราก / 'build/ccompiler' / (ชื่อ + '.o'), 'build/ccompiler/' + ชื่อ + '.o')
        명세 = dict(รายงาน_ค่า, objects=['objects/' + ชื่อ + '.o' for ชื่อ in ปลายทาง_ชื่อ],
                    libraries=['objects/' + Path(เส้นทาง).name for เส้นทาง in ไลบรารี])
        (กลุ่ม_ค่า / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (กลุ่ม_ค่า / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        เป้าหมาย = การกระจาย_ค่า / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / เป้าหมาย.name
        with tarfile.open(str(임시압축), 'w:gz') as เก็บถาวร_ค่า:
            เก็บถาวร_ค่า.add(str(กลุ่ม_ค่า), arcname=กลุ่ม_ค่า.name)
        임시압축.replace(เป้าหมาย)
    รายงาน_ค่า['relink_archive_sha256'] = แฮช_แฟ้ม(เป้าหมาย)
    (การกระจาย_ค่า / 'cosl-distribution.json').write_text(json.dumps(รายงาน_ค่า, ensure_ascii=False, indent=2) + '\n')
    return เป้าหมาย


if __name__ == '__main__':
    ตัวแยกวิเคราะห์_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ตัวแยกวิเคราะห์_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ค่า = ตัวแยกวิเคราะห์_48ee4b1b.parse_args()
    if ค่า.command == 'bundle':
        print('COSL source/relink kit:', ผูก_ปลายทาง())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
