#!/usr/bin/env python3
"""trenutno_stavka 자체 ARM64 산출물을 검사하고 LGPL izvor_stablo·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

projicirati_koijen = Path(__file__).resolve().parents[1]
저장소 = projicirati_koijen.parents[1]
odredište_naziv = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
biblioteka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def raspršivanje_fajl(Putanja):
    return hashlib.sha256(Path(Putanja).read_bytes()).hexdigest()


def 점검():
    for Naziv in ('vendor/wolfssh', 'vendor/wolfssl', 'udaljeno_VALUE/user_settings.h'):
        if (projicirati_koijen / Naziv).exists():
            raise SystemExit('COSL 배포 Zaustavi: 이전 GPL udaljeno_VALUE 구현이 izvor_stablo 트리에 남아 있습니다: ' + Naziv)
    ožičen_VALUE = (projicirati_koijen / 'Mreža_snop/ožičen_Mreža.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ožičen_VALUE or 'SPDX-License-Identifier: GPL' in ožičen_VALUE:
        raise SystemExit('COSL 배포 Zaustavi: BSD GENET 구현·고지 potvrditi 필요')
    for Naziv in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Naziv).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Naziv)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(projicirati_koijen / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Zaustavi: 커널에 이전 GPL lozinka_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Naziv in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Naziv + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Naziv)
    with tempfile.TemporaryDirectory(dir=str(projicirati_koijen / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(projicirati_koijen / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if raspršivanje_fajl(IMAGE_VALUE) != raspršivanje_fajl(projicirati_koijen / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    izvještaj_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': raspršivanje_fajl(projicirati_koijen / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Naziv: raspršivanje_fajl(projicirati_koijen / 'build' / Naziv) for Naziv in biblioteka}}
    (projicirati_koijen / 'build/cosl-distribution-check.json').write_text(json.dumps(izvještaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    return izvještaj_VALUE


def BIND_završna_tačka():
    izvještaj_VALUE = 점검()
    배포 = projicirati_koijen / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(projicirati_koijen / 'build')) as 임시:
        Grupa_VALUE = Path(임시) / 'jkoros-native-relink'
        Grupa_VALUE.mkdir()
        def instanca_VALUE(원본, peer_VALUE):
            odredište_VALUE = Grupa_VALUE / peer_VALUE
            odredište_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(odredište_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(odredište_VALUE))
        for Naziv in odredište_naziv:
            instanca_VALUE(projicirati_koijen / 'build' / (Naziv + '.o'), 'objects/' + Naziv + '.o')
        for Naziv in biblioteka:
            instanca_VALUE(projicirati_koijen / 'build' / Naziv, 'objects/' + Path(Naziv).name)
        for Naziv in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'korisnik', '명명', 'mašina', 'Mreža_snop/Mreža_snop.h', '부팅/Veza_izgled.ld',
                     'udaljeno_VALUE/assh_config.h', 'udaljeno_VALUE/config.h', 'udaljeno_VALUE/ctype.h', 'udaljeno_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            instanca_VALUE(projicirati_koijen / Naziv, Naziv)
        for Naziv in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            instanca_VALUE(저장소 / Naziv, Naziv)
        for Putanja in sorted((projicirati_koijen / 'vendor').glob('LICENSE*')):
            instanca_VALUE(Putanja, 'vendor/' + Putanja.name)
        instanca_VALUE(projicirati_koijen / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        instanca_VALUE(projicirati_koijen / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        instanca_VALUE(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        instanca_VALUE(projicirati_koijen / 'Alati/재연결.py', 'relink.py')
        for Putanja in sorted((projicirati_koijen / 'build/user').glob('*.elf')):
            instanca_VALUE(Putanja, 'build/user/' + Putanja.name)
        for Naziv in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            instanca_VALUE(projicirati_koijen / 'build/user' / (Naziv + '.o'), 'build/user/' + Naziv + '.o')
        for Naziv in ('crt', 'aot-runtime', 'zajednička_jezička_biblioteka_Podrška', 'Pokreni', '미리번역', 'vratiti_most'):
            instanca_VALUE(projicirati_koijen / 'build/ccompiler' / (Naziv + '.o'), 'build/ccompiler/' + Naziv + '.o')
        명세 = dict(izvještaj_VALUE, objects=['objects/' + Naziv + '.o' for Naziv in odredište_naziv],
                    libraries=['objects/' + Path(Putanja).name for Putanja in biblioteka])
        (Grupa_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grupa_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        cilj = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / cilj.name
        with tarfile.open(str(임시압축), 'w:gz') as Arhiva_VALUE:
            Arhiva_VALUE.add(str(Grupa_VALUE), arcname=Grupa_VALUE.name)
        임시압축.replace(cilj)
    izvještaj_VALUE['relink_archive_sha256'] = raspršivanje_fajl(cilj)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(izvještaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    return cilj


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = 해석기.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_završna_tačka())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
