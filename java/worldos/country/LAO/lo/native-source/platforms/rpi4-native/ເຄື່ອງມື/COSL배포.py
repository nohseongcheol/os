#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

ໂຄງ_ການ_ເລກຮາກ = Path(__file__).resolve().parents[1]
ຣີໂພຊິທໍຣີ_ເລກຮາກ = ໂຄງ_ການ_ເລກຮາກ.parents[1]
ປາຍທາງ_ຊື່ = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ຫໍສະຫມຸດ = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ແຮຊ_ຟາຍ(ທາງໂຄຈອນ):
    return hashlib.sha256(Path(ທາງໂຄຈອນ).read_bytes()).hexdigest()


def 점검():
    for ຊື່ in ('vendor/wolfssh', 'vendor/wolfssl', 'ທາງ_ໄກ_ຄ່າ/user_settings.h'):
        if (ໂຄງ_ການ_ເລກຮາກ / ຊື່).exists():
            raise SystemExit('COSL 배포 ຢຸດ: 이전 GPL ທາງ_ໄກ_ຄ່າ 구현이 ແຫຼ່ງທີ່ມາ_ຕົ້ນໄມ້ 트리에 남아 있습니다: ' + ຊື່)
    ເປັນສາຍ_ຄ່າ = (ໂຄງ_ການ_ເລກຮາກ / 'ເຄືອຂ່າຍ_ກຸ່ມບັດ/ເປັນສາຍ_ເຄືອຂ່າຍ.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ເປັນສາຍ_ຄ່າ or 'SPDX-License-Identifier: GPL' in ເປັນສາຍ_ຄ່າ:
        raise SystemExit('COSL 배포 ຢຸດ: BSD GENET 구현·고지 확인 필요')
    for ຊື່ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (ຣີໂພຊິທໍຣີ_ເລກຮາກ / ຊື່).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + ຊື່)
    ສັນຍາລັກ_ຄ່າ = subprocess.check_output(['aarch64-linux-gnu-nm', str(ໂຄງ_ການ_ເລກຮາກ / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ສັນຍາລັກ_ຄ່າ):
        raise SystemExit('COSL 배포 ຢຸດ: 커널에 이전 GPL ລະຫັດຜ່ານ_ຄ່າ/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for ຊື່ in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + ຊື່ + r'$', ສັນຍາລັກ_ຄ່າ, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + ຊື່)
    with tempfile.TemporaryDirectory(dir=str(ໂຄງ_ການ_ເລກຮາກ / 'build')) as 임시:
        ຮູບ_ຄ່າ = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(ໂຄງ_ການ_ເລກຮາກ / 'build/kernel.elf'), str(ຮູບ_ຄ່າ)])
        if ແຮຊ_ຟາຍ(ຮູບ_ຄ່າ) != ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ລາຍງານ_ຄ່າ = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {ຊື່: ແຮຊ_ຟາຍ(ໂຄງ_ການ_ເລກຮາກ / 'build' / ຊື່) for ຊື່ in ຫໍສະຫມຸດ}}
    (ໂຄງ_ການ_ເລກຮາກ / 'build/cosl-distribution-check.json').write_text(json.dumps(ລາຍງານ_ຄ່າ, ensure_ascii=False, indent=2) + '\n')
    return ລາຍງານ_ຄ່າ


def 묶기():
    ລາຍງານ_ຄ່າ = 점검()
    배포 = ໂຄງ_ການ_ເລກຮາກ / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(ໂຄງ_ການ_ເລກຮາກ / 'build')) as 임시:
        ກຸ່ມ_ຄ່າ = Path(임시) / 'jkoros-native-relink'
        ກຸ່ມ_ຄ່າ.mkdir()
        def ກ່າຍ_ຄ່າ(원본, ລຸ້ນດຽວກັນ_ຄ່າ):
            ປາຍທາງ_ຄ່າ = ກຸ່ມ_ຄ່າ / ລຸ້ນດຽວກັນ_ຄ່າ
            ປາຍທາງ_ຄ່າ.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(ປາຍທາງ_ຄ່າ), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(ປາຍທາງ_ຄ່າ))
        for ຊື່ in ປາຍທາງ_ຊື່:
            ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / 'build' / (ຊື່ + '.o'), 'objects/' + ຊື່ + '.o')
        for ຊື່ in ຫໍສະຫມຸດ:
            ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / 'build' / ຊື່, 'objects/' + Path(ຊື່).name)
        for ຊື່ in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ຜູ້ໃຊ້', '명명', 'ເຄື່ອງຈັກ', 'ເຄືອຂ່າຍ_ກຸ່ມບັດ/ເຄືອຂ່າຍ_ກຸ່ມບັດ.h', '부팅/ລິ້ງ_ຮູບແບບ.ld',
                     'ທາງ_ໄກ_ຄ່າ/assh_config.h', 'ທາງ_ໄກ_ຄ່າ/config.h', 'ທາງ_ໄກ_ຄ່າ/ctype.h', 'ທາງ_ໄກ_ຄ່າ/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / ຊື່, ຊື່)
        for ຊື່ in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            ກ່າຍ_ຄ່າ(ຣີໂພຊິທໍຣີ_ເລກຮາກ / ຊື່, ຊື່)
        for ທາງໂຄຈອນ in sorted((ໂຄງ_ການ_ເລກຮາກ / 'vendor').glob('LICENSE*')):
            ກ່າຍ_ຄ່າ(ທາງໂຄຈອນ, 'vendor/' + ທາງໂຄຈອນ.name)
        ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        ກ່າຍ_ຄ່າ(ຣີໂພຊິທໍຣີ_ເລກຮາກ / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / 'ເຄື່ອງມື/재연결.py', 'relink.py')
        for ທາງໂຄຈອນ in sorted((ໂຄງ_ການ_ເລກຮາກ / 'build/user').glob('*.elf')):
            ກ່າຍ_ຄ່າ(ທາງໂຄຈອນ, 'build/user/' + ທາງໂຄຈອນ.name)
        for ຊື່ in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / 'build/user' / (ຊື່ + '.o'), 'build/user/' + ຊື່ + '.o')
        for ຊື່ in ('crt', 'aot-runtime', '실행지원', 'ແລ່ນ', '미리번역', '되돌림'):
            ກ່າຍ_ຄ່າ(ໂຄງ_ການ_ເລກຮາກ / 'build/ccompiler' / (ຊື່ + '.o'), 'build/ccompiler/' + ຊື່ + '.o')
        명세 = dict(ລາຍງານ_ຄ່າ, objects=['objects/' + ຊື່ + '.o' for ຊື່ in ປາຍທາງ_ຊື່],
                    libraries=['objects/' + Path(ທາງໂຄຈອນ).name for ທາງໂຄຈອນ in ຫໍສະຫມຸດ])
        (ກຸ່ມ_ຄ່າ / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (ກຸ່ມ_ຄ່າ / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ເປົ້າ_ຫມາຍ = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ເປົ້າ_ຫມາຍ.name
        with tarfile.open(str(임시압축), 'w:gz') as ການສໍາເນົາ_ຄ່າ:
            ການສໍາເນົາ_ຄ່າ.add(str(ກຸ່ມ_ຄ່າ), arcname=ກຸ່ມ_ຄ່າ.name)
        임시압축.replace(ເປົ້າ_ຫມາຍ)
    ລາຍງານ_ຄ່າ['relink_archive_sha256'] = ແຮຊ_ຟາຍ(ເປົ້າ_ຫມາຍ)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ລາຍງານ_ຄ່າ, ensure_ascii=False, indent=2) + '\n')
    return ເປົ້າ_ຫມາຍ


if __name__ == '__main__':
    ຕົວແຍກວິເຄາະ_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ຕົວແຍກວິເຄາະ_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ຄ່າ = ຕົວແຍກວິເຄາະ_48ee4b1b.parse_args()
    if ຄ່າ.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
