#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL inkomoko_igiti·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

기준 = Path(__file__).resolve().parents[1]
저장소 = 기준.parents[1]
aho_ijya_izina = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
isomero = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hashi_dosiye(Inzira):
    return hashlib.sha256(Path(Inzira).read_bytes()).hexdigest()


def 점검():
    for Izina in ('vendor/wolfssh', 'vendor/wolfssl', 'kure_agaciro/user_settings.h'):
        if (기준 / Izina).exists():
            raise SystemExit('COSL 배포 Guhagarara: 이전 GPL kure_agaciro 구현이 inkomoko_igiti 트리에 남아 있습니다: ' + Izina)
    y_umugozi_agaciro = (기준 / 'Urusobemiyoboro_Ikirundo/y_umugozi_Urusobemiyoboro.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in y_umugozi_agaciro or 'SPDX-License-Identifier: GPL' in y_umugozi_agaciro:
        raise SystemExit('COSL 배포 Guhagarara: BSD GENET 구현·고지 gusuzuma 필요')
    for Izina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Izina).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Izina)
    ikimenyetso_agaciro = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ikimenyetso_agaciro):
        raise SystemExit('COSL 배포 Guhagarara: 커널에 이전 GPL ijambobanga_agaciro/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Izina in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Izina + r'$', ikimenyetso_agaciro, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Izina)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        ishusho_agaciro = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(ishusho_agaciro)])
        if hashi_dosiye(ishusho_agaciro) != hashi_dosiye(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    raporo_agaciro = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hashi_dosiye(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Izina: hashi_dosiye(기준 / 'build' / Izina) for Izina in isomero}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(raporo_agaciro, ensure_ascii=False, indent=2) + '\n')
    return raporo_agaciro


def 묶기():
    raporo_agaciro = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        itsinda_agaciro = Path(임시) / 'jkoros-native-relink'
        itsinda_agaciro.mkdir()
        def kopi_agaciro(원본, Mugenzi_agaciro):
            aho_ijya_agaciro = itsinda_agaciro / Mugenzi_agaciro
            aho_ijya_agaciro.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(aho_ijya_agaciro), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(aho_ijya_agaciro))
        for Izina in aho_ijya_izina:
            kopi_agaciro(기준 / 'build' / (Izina + '.o'), 'objects/' + Izina + '.o')
        for Izina in isomero:
            kopi_agaciro(기준 / 'build' / Izina, 'objects/' + Path(Izina).name)
        for Izina in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ukoresha', '명명', 'imashini', 'Urusobemiyoboro_Ikirundo/Urusobemiyoboro_Ikirundo.h', '부팅/Ihuza_Imimerere.ld',
                     'kure_agaciro/assh_config.h', 'kure_agaciro/config.h', 'kure_agaciro/ctype.h', 'kure_agaciro/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopi_agaciro(기준 / Izina, Izina)
        for Izina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopi_agaciro(저장소 / Izina, Izina)
        for Inzira in sorted((기준 / 'vendor').glob('LICENSE*')):
            kopi_agaciro(Inzira, 'vendor/' + Inzira.name)
        kopi_agaciro(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopi_agaciro(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopi_agaciro(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopi_agaciro(기준 / 'Ibikoresho/재연결.py', 'relink.py')
        for Inzira in sorted((기준 / 'build/user').glob('*.elf')):
            kopi_agaciro(Inzira, 'build/user/' + Inzira.name)
        for Izina in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopi_agaciro(기준 / 'build/user' / (Izina + '.o'), 'build/user/' + Izina + '.o')
        for Izina in ('crt', 'aot-runtime', 'igihe_ururimi_rukorwamo_Ubufasha', 'ihuriro', '미리번역', '되돌림'):
            kopi_agaciro(기준 / 'build/ccompiler' / (Izina + '.o'), 'build/ccompiler/' + Izina + '.o')
        명세 = dict(raporo_agaciro, objects=['objects/' + Izina + '.o' for Izina in aho_ijya_izina],
                    libraries=['objects/' + Path(Inzira).name for Inzira in isomero])
        (itsinda_agaciro / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (itsinda_agaciro / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        gusimbuza_igishya = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / gusimbuza_igishya.name
        with tarfile.open(str(임시압축), 'w:gz') as gushyingura_agaciro:
            gushyingura_agaciro.add(str(itsinda_agaciro), arcname=itsinda_agaciro.name)
        임시압축.replace(gusimbuza_igishya)
    raporo_agaciro['relink_archive_sha256'] = hashi_dosiye(gusimbuza_igishya)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(raporo_agaciro, ensure_ascii=False, indent=2) + '\n')
    return gusimbuza_igishya


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    agaciro = 해석기.parse_args()
    if agaciro.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
