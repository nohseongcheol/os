#!/usr/bin/env python3
"""ga_jaana_selwana 자체 ARM64 산출물을 검사하고 LGPL Motswedi_sebopego_sa_tshedimosetso·재연결 자료를 함께 묶는다."""
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
bogorogelo_leina = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
laeborari = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def heše_faele(tsela):
    return hashlib.sha256(Path(tsela).read_bytes()).hexdigest()


def 점검():
    for leina in ('vendor/wolfssh', 'vendor/wolfssl', 'kgakala_Boleng/user_settings.h'):
        if (기준 / leina).exists():
            raise SystemExit('COSL 배포 emisa: 이전 GPL kgakala_Boleng 구현이 Motswedi_sebopego_sa_tshedimosetso 트리에 남아 있습니다: ' + leina)
    golagantsweng_ka_megala_Boleng = (기준 / 'Neteweke_kokoanyodinepe/golagantsweng_ka_megala_Neteweke.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in golagantsweng_ka_megala_Boleng or 'SPDX-License-Identifier: GPL' in golagantsweng_ka_megala_Boleng:
        raise SystemExit('COSL 배포 emisa: BSD GENET 구현·고지 netefatsa 필요')
    for leina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / leina).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + leina)
    letshwao_Boleng = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', letshwao_Boleng):
        raise SystemExit('COSL 배포 emisa: 커널에 이전 GPL khoututseno_Boleng/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for leina in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + leina + r'$', letshwao_Boleng, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + leina)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        Setshwantsho_Boleng = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(Setshwantsho_Boleng)])
        if heše_faele(Setshwantsho_Boleng) != heše_faele(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    pego_Boleng = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': heše_faele(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {leina: heše_faele(기준 / 'build' / leina) for leina in laeborari}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(pego_Boleng, ensure_ascii=False, indent=2) + '\n')
    return pego_Boleng


def 묶기():
    pego_Boleng = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        setlhopha_Boleng = Path(임시) / 'jkoros-native-relink'
        setlhopha_Boleng.mkdir()
        def leloko_Boleng(원본, semphato_Boleng):
            bogorogelo_Boleng = setlhopha_Boleng / semphato_Boleng
            bogorogelo_Boleng.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(bogorogelo_Boleng), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(bogorogelo_Boleng))
        for leina in bogorogelo_leina:
            leloko_Boleng(기준 / 'build' / (leina + '.o'), 'objects/' + leina + '.o')
        for leina in laeborari:
            leloko_Boleng(기준 / 'build' / leina, 'objects/' + Path(leina).name)
        for leina in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'modirisi', '명명', 'motšhine', 'Neteweke_kokoanyodinepe/Neteweke_kokoanyodinepe.h', '부팅/Kgokagano_Boalo.ld',
                     'kgakala_Boleng/assh_config.h', 'kgakala_Boleng/config.h', 'kgakala_Boleng/ctype.h', 'kgakala_Boleng/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            leloko_Boleng(기준 / leina, leina)
        for leina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            leloko_Boleng(저장소 / leina, leina)
        for tsela in sorted((기준 / 'vendor').glob('LICENSE*')):
            leloko_Boleng(tsela, 'vendor/' + tsela.name)
        leloko_Boleng(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        leloko_Boleng(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        leloko_Boleng(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        leloko_Boleng(기준 / 'Thuluse/재연결.py', 'relink.py')
        for tsela in sorted((기준 / 'build/user').glob('*.elf')):
            leloko_Boleng(tsela, 'build/user/' + tsela.name)
        for leina in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            leloko_Boleng(기준 / 'build/user' / (leina + '.o'), 'build/user/' + leina + '.o')
        for leina in ('crt', 'aot-runtime', 'nakotsamaiso_ya_puo_e_e_tlwaelegileng_Thuso', 'dirisa', '미리번역', '되돌림'):
            leloko_Boleng(기준 / 'build/ccompiler' / (leina + '.o'), 'build/ccompiler/' + leina + '.o')
        명세 = dict(pego_Boleng, objects=['objects/' + leina + '.o' for leina in bogorogelo_leina],
                    libraries=['objects/' + Path(tsela).name for tsela in laeborari])
        (setlhopha_Boleng / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (setlhopha_Boleng / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        setotwa = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / setotwa.name
        with tarfile.open(str(임시압축), 'w:gz') as boloka_Boleng:
            boloka_Boleng.add(str(setlhopha_Boleng), arcname=setlhopha_Boleng.name)
        임시압축.replace(setotwa)
    pego_Boleng['relink_archive_sha256'] = heše_faele(setotwa)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(pego_Boleng, ensure_ascii=False, indent=2) + '\n')
    return setotwa


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    Boleng = 해석기.parse_args()
    if Boleng.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
