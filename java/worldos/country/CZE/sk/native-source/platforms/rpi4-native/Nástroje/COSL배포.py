#!/usr/bin/env python3
"""v_termíne_splatnosti_položka vlastné ARM64 산출물을 검사하고 LGPL zdroj_strom·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

akcia_koreň = Path(__file__).resolve().parents[1]
odkladací_priestor_koreň = akcia_koreň.parents[1]
cieľ_názov = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
knižnica = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hodnota_hash_Súbor(Cesta):
    return hashlib.sha256(Path(Cesta).read_bytes()).hexdigest()


def 점검():
    for Názov in ('vendor/wolfssh', 'vendor/wolfssl', 'vzdialený_VALUE/user_settings.h'):
        if (akcia_koreň / Názov).exists():
            raise SystemExit('COSL 배포 Zastaviť: 이전 GPL vzdialený_VALUE 구현이 zdroj_strom 트리에 남아 있습니다: ' + Názov)
    drôtový_VALUE = (akcia_koreň / 'sieť_Vrstvy/drôtový_sieť.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in drôtový_VALUE or 'SPDX-License-Identifier: GPL' in drôtový_VALUE:
        raise SystemExit('COSL 배포 Zastaviť: BSD GENET 구현·고지 overiť 필요')
    for Názov in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (odkladací_priestor_koreň / Názov).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Názov)
    symbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(akcia_koreň / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', symbol_VALUE):
        raise SystemExit('COSL 배포 Zastaviť: 커널에 이전 GPL heslo_VALUE/SSH 심볼이 남아 있습니다. skúsiť_znova_VALUE 빌드하세요.')
    for Názov in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Názov + r'$', symbol_VALUE, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Názov)
    with tempfile.TemporaryDirectory(dir=str(akcia_koreň / 'build')) as 임시:
        IMAGE_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(akcia_koreň / 'build/kernel.elf'), str(IMAGE_VALUE)])
        if hodnota_hash_Súbor(IMAGE_VALUE) != hodnota_hash_Súbor(akcia_koreň / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    správa_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hodnota_hash_Súbor(akcia_koreň / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Názov: hodnota_hash_Súbor(akcia_koreň / 'build' / Názov) for Názov in knižnica}}
    (akcia_koreň / 'build/cosl-distribution-check.json').write_text(json.dumps(správa_VALUE, ensure_ascii=False, indent=2) + '\n')
    return správa_VALUE


def BIND_účastník():
    správa_VALUE = 점검()
    배포 = akcia_koreň / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(akcia_koreň / 'build')) as 임시:
        Skupina_VALUE = Path(임시) / 'jkoros-native-relink'
        Skupina_VALUE.mkdir()
        def inštancia_VALUE(원본, partnerský_uzol_VALUE):
            cieľ_VALUE = Skupina_VALUE / partnerský_uzol_VALUE
            cieľ_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(cieľ_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(cieľ_VALUE))
        for Názov in cieľ_názov:
            inštancia_VALUE(akcia_koreň / 'build' / (Názov + '.o'), 'objects/' + Názov + '.o')
        for Názov in knižnica:
            inštancia_VALUE(akcia_koreň / 'build' / Názov, 'objects/' + Path(Názov).name)
        for Názov in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_kompilátor', 'používateľ', '명명', 'počítač_5eb260fa', 'sieť_Vrstvy/sieť_Vrstvy.h', '부팅/odkaz_Navigácia.ld',
                     'vzdialený_VALUE/assh_config.h', 'vzdialený_VALUE/config.h', 'vzdialený_VALUE/ctype.h', 'vzdialený_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            inštancia_VALUE(akcia_koreň / Názov, Názov)
        for Názov in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            inštancia_VALUE(odkladací_priestor_koreň / Názov, Názov)
        for Cesta in sorted((akcia_koreň / 'vendor').glob('LICENSE*')):
            inštancia_VALUE(Cesta, 'vendor/' + Cesta.name)
        inštancia_VALUE(akcia_koreň / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        inštancia_VALUE(akcia_koreň / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        inštancia_VALUE(odkladací_priestor_koreň / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        inštancia_VALUE(akcia_koreň / 'Nástroje/재연결.py', 'relink.py')
        for Cesta in sorted((akcia_koreň / 'build/user').glob('*.elf')):
            inštancia_VALUE(Cesta, 'build/user/' + Cesta.name)
        for Názov in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            inštancia_VALUE(akcia_koreň / 'build/user' / (Názov + '.o'), 'build/user/' + Názov + '.o')
        for Názov in ('crt', 'aot-runtime', 'CLR_Podpora', 'Spustiť_2', '미리번역', 'vrátiť_most'):
            inštancia_VALUE(akcia_koreň / 'build/ccompiler' / (Názov + '.o'), 'build/ccompiler/' + Názov + '.o')
        명세 = dict(správa_VALUE, objects=['objects/' + Názov + '.o' for Názov in cieľ_názov],
                    libraries=['objects/' + Path(Cesta).name for Cesta in knižnica])
        (Skupina_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Skupina_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_kompilátor.
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
        cieľová_hodnota = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / cieľová_hodnota.name
        with tarfile.open(str(임시압축), 'w:gz') as Archív_VALUE:
            Archív_VALUE.add(str(Skupina_VALUE), arcname=Skupina_VALUE.name)
        임시압축.replace(cieľová_hodnota)
    správa_VALUE['relink_archive_sha256'] = hodnota_hash_Súbor(cieľová_hodnota)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(správa_VALUE, ensure_ascii=False, indent=2) + '\n')
    return cieľová_hodnota


if __name__ == '__main__':
    analyzátor_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    analyzátor_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = analyzátor_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', BIND_účastník())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
