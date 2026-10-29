#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL mohlodi_mohlare·재연결 자료를 함께 묶는다."""
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
boyo_leina = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
Bokgobadata = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def haše_faele(Tsejana):
    return hashlib.sha256(Path(Tsejana).read_bytes()).hexdigest()


def 점검():
    for Leina in ('vendor/wolfssh', 'vendor/wolfssl', 'ya_kgole_boleng/user_settings.h'):
        if (기준 / Leina).exists():
            raise SystemExit('COSL 배포 Emiša: 이전 GPL ya_kgole_boleng 구현이 mohlodi_mohlare 트리에 남아 있습니다: ' + Leina)
    ya_mathale_boleng = (기준 / 'Netweke_kgoboko/ya_mathale_Netweke.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in ya_mathale_boleng or 'SPDX-License-Identifier: GPL' in ya_mathale_boleng:
        raise SystemExit('COSL 배포 Emiša: BSD GENET 구현·고지 kgonthiša 필요')
    for Leina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Leina).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Leina)
    leswao_boleng = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', leswao_boleng):
        raise SystemExit('COSL 배포 Emiša: 커널에 이전 GPL phasewete_boleng/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Leina in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Leina + r'$', leswao_boleng, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Leina)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        seswantšho_boleng = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(seswantšho_boleng)])
        if haše_faele(seswantšho_boleng) != haše_faele(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    pego_boleng = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': haše_faele(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Leina: haše_faele(기준 / 'build' / Leina) for Leina in Bokgobadata}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(pego_boleng, ensure_ascii=False, indent=2) + '\n')
    return pego_boleng


def 묶기():
    pego_boleng = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        sehlopha_boleng = Path(임시) / 'jkoros-native-relink'
        sehlopha_boleng.mkdir()
        def kopiša_boleng(원본, sedirišwa_sa_legoro_le_tee_boleng):
            boyo_boleng = sehlopha_boleng / sedirišwa_sa_legoro_le_tee_boleng
            boyo_boleng.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(boyo_boleng), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(boyo_boleng))
        for Leina in boyo_leina:
            kopiša_boleng(기준 / 'build' / (Leina + '.o'), 'objects/' + Leina + '.o')
        for Leina in Bokgobadata:
            kopiša_boleng(기준 / 'build' / Leina, 'objects/' + Path(Leina).name)
        for Leina in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'mošomiši', '명명', 'motšhene', 'Netweke_kgoboko/Netweke_kgoboko.h', '부팅/linke_Sebopego.ld',
                     'ya_kgole_boleng/assh_config.h', 'ya_kgole_boleng/config.h', 'ya_kgole_boleng/ctype.h', 'ya_kgole_boleng/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopiša_boleng(기준 / Leina, Leina)
        for Leina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopiša_boleng(저장소 / Leina, Leina)
        for Tsejana in sorted((기준 / 'vendor').glob('LICENSE*')):
            kopiša_boleng(Tsejana, 'vendor/' + Tsejana.name)
        kopiša_boleng(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopiša_boleng(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopiša_boleng(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopiša_boleng(기준 / 'Ditholosi/재연결.py', 'relink.py')
        for Tsejana in sorted((기준 / 'build/user').glob('*.elf')):
            kopiša_boleng(Tsejana, 'build/user/' + Tsejana.name)
        for Leina in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopiša_boleng(기준 / 'build/user' / (Leina + '.o'), 'build/user/' + Leina + '.o')
        for Leina in ('crt', 'aot-runtime', 'lebakanako_la_polelotlwaelwa_Thekgo', 'Diriša', '미리번역', '되돌림'):
            kopiša_boleng(기준 / 'build/ccompiler' / (Leina + '.o'), 'build/ccompiler/' + Leina + '.o')
        명세 = dict(pego_boleng, objects=['objects/' + Leina + '.o' for Leina in boyo_leina],
                    libraries=['objects/' + Path(Tsejana).name for Tsejana in Bokgobadata])
        (sehlopha_boleng / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (sehlopha_boleng / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        nepo = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / nepo.name
        with tarfile.open(str(임시압축), 'w:gz') as Akhaebe_boleng:
            Akhaebe_boleng.add(str(sehlopha_boleng), arcname=sehlopha_boleng.name)
        임시압축.replace(nepo)
    pego_boleng['relink_archive_sha256'] = haše_faele(nepo)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(pego_boleng, ensure_ascii=False, indent=2) + '\n')
    return nepo


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    boleng = 해석기.parse_args()
    if boleng.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
