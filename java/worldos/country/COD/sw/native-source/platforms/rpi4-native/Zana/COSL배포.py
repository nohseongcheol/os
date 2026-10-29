#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL chanzo_mti·재연결 자료를 함께 묶는다."""
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
fikio_jina = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
maktaba = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def kali_faili(njia):
    return hashlib.sha256(Path(njia).read_bytes()).hexdigest()


def 점검():
    for Jina in ('vendor/wolfssh', 'vendor/wolfssl', 'kwa_mbali_thamani/user_settings.h'):
        if (기준 / Jina).exists():
            raise SystemExit('COSL 배포 Simama: 이전 GPL kwa_mbali_thamani 구현이 chanzo_mti 트리에 남아 있습니다: ' + Jina)
    kuwekwa_waya_thamani = (기준 / 'Mtandao_Mpororo/kuwekwa_waya_Mtandao.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in kuwekwa_waya_thamani or 'SPDX-License-Identifier: GPL' in kuwekwa_waya_thamani:
        raise SystemExit('COSL 배포 Simama: BSD GENET 구현·고지 thibitisha 필요')
    for Jina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Jina).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Jina)
    ishara_thamani = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', ishara_thamani):
        raise SystemExit('COSL 배포 Simama: 커널에 이전 GPL nywila_thamani/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Jina in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Jina + r'$', ishara_thamani, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Jina)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        picha_thamani = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(picha_thamani)])
        if kali_faili(picha_thamani) != kali_faili(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    ripoti_thamani = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': kali_faili(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Jina: kali_faili(기준 / 'build' / Jina) for Jina in maktaba}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(ripoti_thamani, ensure_ascii=False, indent=2) + '\n')
    return ripoti_thamani


def 묶기():
    ripoti_thamani = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        Kikundi_thamani = Path(임시) / 'jkoros-native-relink'
        Kikundi_thamani.mkdir()
        def mfano_thamani(원본, kompyuta_rika_thamani):
            fikio_thamani = Kikundi_thamani / kompyuta_rika_thamani
            fikio_thamani.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(fikio_thamani), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(fikio_thamani))
        for Jina in fikio_jina:
            mfano_thamani(기준 / 'build' / (Jina + '.o'), 'objects/' + Jina + '.o')
        for Jina in maktaba:
            mfano_thamani(기준 / 'build' / Jina, 'objects/' + Path(Jina).name)
        for Jina in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'mtumiaji', '명명', 'mashine', 'Mtandao_Mpororo/Mtandao_Mpororo.h', '부팅/Kiungo_Muundo.ld',
                     'kwa_mbali_thamani/assh_config.h', 'kwa_mbali_thamani/config.h', 'kwa_mbali_thamani/ctype.h', 'kwa_mbali_thamani/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            mfano_thamani(기준 / Jina, Jina)
        for Jina in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            mfano_thamani(저장소 / Jina, Jina)
        for njia in sorted((기준 / 'vendor').glob('LICENSE*')):
            mfano_thamani(njia, 'vendor/' + njia.name)
        mfano_thamani(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        mfano_thamani(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        mfano_thamani(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        mfano_thamani(기준 / 'Zana/재연결.py', 'relink.py')
        for njia in sorted((기준 / 'build/user').glob('*.elf')):
            mfano_thamani(njia, 'build/user/' + njia.name)
        for Jina in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            mfano_thamani(기준 / 'build/user' / (Jina + '.o'), 'build/user/' + Jina + '.o')
        for Jina in ('crt', 'aot-runtime', 'muda_wa_kuendesha_lugha_ya_kawaida_Auni', 'endesha', '미리번역', '되돌림'):
            mfano_thamani(기준 / 'build/ccompiler' / (Jina + '.o'), 'build/ccompiler/' + Jina + '.o')
        명세 = dict(ripoti_thamani, objects=['objects/' + Jina + '.o' for Jina in fikio_jina],
                    libraries=['objects/' + Path(njia).name for njia in maktaba])
        (Kikundi_thamani / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Kikundi_thamani / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        lengo = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / lengo.name
        with tarfile.open(str(임시압축), 'w:gz') as Hifadhi_thamani:
            Hifadhi_thamani.add(str(Kikundi_thamani), arcname=Kikundi_thamani.name)
        임시압축.replace(lengo)
    ripoti_thamani['relink_archive_sha256'] = kali_faili(lengo)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(ripoti_thamani, ensure_ascii=False, indent=2) + '\n')
    return lengo


if __name__ == '__main__':
    kichanganuzi_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    kichanganuzi_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    thamani = kichanganuzi_48ee4b1b.parse_args()
    if thamani.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
