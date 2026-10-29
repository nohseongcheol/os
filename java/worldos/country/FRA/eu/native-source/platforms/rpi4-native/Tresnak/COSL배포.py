#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL iturburu_zuhaitz·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Project_erro = Path(__file__).resolve().parents[1]
biltegi_erro = Project_erro.parents[1]
helburu_izen = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
liburutegi = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_fitxategi(Bide_izena):
    return hashlib.sha256(Path(Bide_izena).read_bytes()).hexdigest()


def 점검():
    for Izena in ('vendor/wolfssh', 'vendor/wolfssl', 'urruneko_balio/user_settings.h'):
        if (Project_erro / Izena).exists():
            raise SystemExit('COSL 배포 Gelditu: 이전 GPL urruneko_balio 구현이 iturburu_zuhaitz 트리에 남아 있습니다: ' + Izena)
    haridun_balio = (Project_erro / 'sare_pila/haridun_sare.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in haridun_balio or 'SPDX-License-Identifier: GPL' in haridun_balio:
        raise SystemExit('COSL 배포 Gelditu: BSD GENET 구현·고지 egiaztatu 필요')
    for Izena in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (biltegi_erro / Izena).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Izena)
    ikur_balio = subprocess.check_output(['aarch64-linux-gnu-nm', str(Project_erro / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ikur_balio):
        raise SystemExit('COSL 배포 Gelditu: 커널에 이전 GPL pasahitz_balio/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Izena in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Izena + r'$', ikur_balio, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Izena)
    with tempfile.TemporaryDirectory(dir=str(Project_erro / 'build')) as 임시:
        irudi_balio = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Project_erro / 'build/kernel.elf'), str(irudi_balio)])
        if hash_fitxategi(irudi_balio) != hash_fitxategi(Project_erro / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    txosten_balio = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_fitxategi(Project_erro / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Izena: hash_fitxategi(Project_erro / 'build' / Izena) for Izena in liburutegi}}
    (Project_erro / 'build/cosl-distribution-check.json').write_text(json.dumps(txosten_balio, ensure_ascii=False, indent=2) + '\n')
    return txosten_balio


def lotu_amaiera_puntu():
    txosten_balio = 점검()
    배포 = Project_erro / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Project_erro / 'build')) as 임시:
        talde_balio = Path(임시) / 'jkoros-native-relink'
        talde_balio.mkdir()
        def kopiatu_balio(원본, pareko_balio):
            helburu_balio_a0fbc067 = talde_balio / pareko_balio
            helburu_balio_a0fbc067.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(helburu_balio_a0fbc067), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(helburu_balio_a0fbc067))
        for Izena in helburu_izen:
            kopiatu_balio(Project_erro / 'build' / (Izena + '.o'), 'objects/' + Izena + '.o')
        for Izena in liburutegi:
            kopiatu_balio(Project_erro / 'build' / Izena, 'objects/' + Path(Izena).name)
        for Izena in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'erabiltzaile', '명명', 'gailu', 'sare_pila/sare_pila.h', '부팅/lotu_diseinu.ld',
                     'urruneko_balio/assh_config.h', 'urruneko_balio/config.h', 'urruneko_balio/ctype.h', 'urruneko_balio/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopiatu_balio(Project_erro / Izena, Izena)
        for Izena in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopiatu_balio(biltegi_erro / Izena, Izena)
        for Bide_izena in sorted((Project_erro / 'vendor').glob('LICENSE*')):
            kopiatu_balio(Bide_izena, 'vendor/' + Bide_izena.name)
        kopiatu_balio(Project_erro / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopiatu_balio(Project_erro / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopiatu_balio(biltegi_erro / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopiatu_balio(Project_erro / 'Tresnak/재연결.py', 'relink.py')
        for Bide_izena in sorted((Project_erro / 'build/user').glob('*.elf')):
            kopiatu_balio(Bide_izena, 'build/user/' + Bide_izena.name)
        for Izena in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopiatu_balio(Project_erro / 'build/user' / (Izena + '.o'), 'build/user/' + Izena + '.o')
        for Izena in ('crt', 'aot-runtime', '실행지원', 'Exekutatu_2', '미리번역', 'itzuli_zubi'):
            kopiatu_balio(Project_erro / 'build/ccompiler' / (Izena + '.o'), 'build/ccompiler/' + Izena + '.o')
        명세 = dict(txosten_balio, objects=['objects/' + Izena + '.o' for Izena in helburu_izen],
                    libraries=['objects/' + Path(Bide_izena).name for Bide_izena in liburutegi])
        (talde_balio / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (talde_balio / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        helburu_balio = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / helburu_balio.name
        with tarfile.open(str(임시압축), 'w:gz') as artxibo_balio:
            artxibo_balio.add(str(talde_balio), arcname=talde_balio.name)
        임시압축.replace(helburu_balio)
    txosten_balio['relink_archive_sha256'] = hash_fitxategi(helburu_balio)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(txosten_balio, ensure_ascii=False, indent=2) + '\n')
    return helburu_balio


if __name__ == '__main__':
    analizatzaile_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analizatzaile_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    balio = analizatzaile_48ee4b1b.parse_args()
    if balio.command == 'bundle':
        print('COSL source/relink kit:', lotu_amaiera_puntu())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
