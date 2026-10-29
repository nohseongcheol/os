#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL umthombo_umthi·재연결 자료를 함께 묶는다."""
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
indawo_ekuyiwa_kuyo_igama = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
ilayibhrari = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def i_hash_ifayile(INDLELA):
    return hashlib.sha256(Path(INDLELA).read_bytes()).hexdigest()


def 점검():
    for Igama in ('vendor/wolfssh', 'vendor/wolfssl', 'kude_ixabiso/user_settings.h'):
        if (기준 / Igama).exists():
            raise SystemExit('COSL 배포 Yima: 이전 GPL kude_ixabiso 구현이 umthombo_umthi 트리에 남아 있습니다: ' + Igama)
    eqhagamshelweyo_ixabiso = (기준 / 'Inethiwekhi_fumba/eqhagamshelweyo_Inethiwekhi.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in eqhagamshelweyo_ixabiso or 'SPDX-License-Identifier: GPL' in eqhagamshelweyo_ixabiso:
        raise SystemExit('COSL 배포 Yima: BSD GENET 구현·고지 ngqinisisa 필요')
    for Igama in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Igama).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Igama)
    isimboli_ixabiso = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', isimboli_ixabiso):
        raise SystemExit('COSL 배포 Yima: 커널에 이전 GPL iphaswedi_ixabiso/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Igama in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Igama + r'$', isimboli_ixabiso, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Igama)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        umfanekiso_ixabiso = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(umfanekiso_ixabiso)])
        if i_hash_ifayile(umfanekiso_ixabiso) != i_hash_ifayile(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ingxelo_ixabiso_ddf2aaf3 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': i_hash_ifayile(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Igama: i_hash_ifayile(기준 / 'build' / Igama) for Igama in ilayibhrari}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(ingxelo_ixabiso_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return ingxelo_ixabiso_ddf2aaf3


def 묶기():
    ingxelo_ixabiso_ddf2aaf3 = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        iqela_ixabiso = Path(임시) / 'jkoros-native-relink'
        iqela_ixabiso.mkdir()
        def kopa_ixabiso(원본, untanga_ixabiso):
            indawo_ekuyiwa_kuyo_ixabiso = iqela_ixabiso / untanga_ixabiso
            indawo_ekuyiwa_kuyo_ixabiso.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(indawo_ekuyiwa_kuyo_ixabiso), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(indawo_ekuyiwa_kuyo_ixabiso))
        for Igama in indawo_ekuyiwa_kuyo_igama:
            kopa_ixabiso(기준 / 'build' / (Igama + '.o'), 'objects/' + Igama + '.o')
        for Igama in ilayibhrari:
            kopa_ixabiso(기준 / 'build' / Igama, 'objects/' + Path(Igama).name)
        for Igama in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'umsebenzisi', '명명', 'umatshini', 'Inethiwekhi_fumba/Inethiwekhi_fumba.h', '부팅/Ilinki_ubume.ld',
                     'kude_ixabiso/assh_config.h', 'kude_ixabiso/config.h', 'kude_ixabiso/ctype.h', 'kude_ixabiso/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            kopa_ixabiso(기준 / Igama, Igama)
        for Igama in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            kopa_ixabiso(저장소 / Igama, Igama)
        for INDLELA in sorted((기준 / 'vendor').glob('LICENSE*')):
            kopa_ixabiso(INDLELA, 'vendor/' + INDLELA.name)
        kopa_ixabiso(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        kopa_ixabiso(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        kopa_ixabiso(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        kopa_ixabiso(기준 / 'Izixhobo/재연결.py', 'relink.py')
        for INDLELA in sorted((기준 / 'build/user').glob('*.elf')):
            kopa_ixabiso(INDLELA, 'build/user/' + INDLELA.name)
        for Igama in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            kopa_ixabiso(기준 / 'build/user' / (Igama + '.o'), 'build/user/' + Igama + '.o')
        for Igama in ('crt', 'aot-runtime', 'ixesha_lokusebenza_kolwimi_oluqhelekileyo_inkxaso', 'Phumeza', '미리번역', '되돌림'):
            kopa_ixabiso(기준 / 'build/ccompiler' / (Igama + '.o'), 'build/ccompiler/' + Igama + '.o')
        명세 = dict(ingxelo_ixabiso_ddf2aaf3, objects=['objects/' + Igama + '.o' for Igama in indawo_ekuyiwa_kuyo_igama],
                    libraries=['objects/' + Path(INDLELA).name for INDLELA in ilayibhrari])
        (iqela_ixabiso / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (iqela_ixabiso / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        ithagethi = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / ithagethi.name
        with tarfile.open(str(임시압축), 'w:gz') as Uvimba_ixabiso:
            Uvimba_ixabiso.add(str(iqela_ixabiso), arcname=iqela_ixabiso.name)
        임시압축.replace(ithagethi)
    ingxelo_ixabiso_ddf2aaf3['relink_archive_sha256'] = i_hash_ifayile(ithagethi)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ingxelo_ixabiso_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    return ithagethi


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    ixabiso = 해석기.parse_args()
    if ixabiso.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
