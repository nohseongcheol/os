#!/usr/bin/env python3
"""현재 자체 ARM64 산출물을 검사하고 LGPL tushe_Li_irabin_tarin_bayanai·재연결 자료를 함께 묶는다."""
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
Zangon_ƙarshe_Suna = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
laburare = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_Fayil(Hanyar_shiga):
    return hashlib.sha256(Path(Hanyar_shiga).read_bytes()).hexdigest()


def 점검():
    for Suna in ('vendor/wolfssh', 'vendor/wolfssl', 'na_nesa_Daraja/user_settings.h'):
        if (기준 / Suna).exists():
            raise SystemExit('COSL 배포 Tsai_da: 이전 GPL na_nesa_Daraja 구현이 tushe_Li_irabin_tarin_bayanai 트리에 남아 있습니다: ' + Suna)
    Hade_da_waya_Daraja = (기준 / 'Hanyar_sadarwa_tara/Hade_da_waya_Hanyar_sadarwa.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in Hade_da_waya_Daraja or 'SPDX-License-Identifier: GPL' in Hade_da_waya_Daraja:
        raise SystemExit('COSL 배포 Tsai_da: BSD GENET 구현·고지 Tabbatar_da 필요')
    for Suna in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / Suna).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Suna)
    alama_Daraja = subprocess.check_output(['aarch64-linux-gnu-nm', str(기준 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', alama_Daraja):
        raise SystemExit('COSL 배포 Tsai_da: 커널에 이전 GPL kalmar_sirri_Daraja/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Suna in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Suna + r'$', alama_Daraja, re.M):
            raise SystemExit('COSL 대체 구현 누락: ' + Suna)
    with tempfile.TemporaryDirectory(dir=str(기준 / 'build')) as 임시:
        Hoto_Daraja = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(기준 / 'build/kernel.elf'), str(Hoto_Daraja)])
        if hash_Fayil(Hoto_Daraja) != hash_Fayil(기준 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Rahoto_Daraja = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_Fayil(기준 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Suna: hash_Fayil(기준 / 'build' / Suna) for Suna in laburare}}
    (기준 / 'build/cosl-distribution-check.json').write_text(json.dumps(Rahoto_Daraja, ensure_ascii=False, indent=2) + '\n')
    return Rahoto_Daraja


def 묶기():
    Rahoto_Daraja = 점검()
    배포 = 기준 / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(기준 / 'build')) as 임시:
        gungu_Daraja = Path(임시) / 'jkoros-native-relink'
        gungu_Daraja.mkdir()
        def Kwafi_Daraja(원본, Fiya_Daraja):
            Zangon_ƙarshe_Daraja = gungu_Daraja / Fiya_Daraja
            Zangon_ƙarshe_Daraja.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(Zangon_ƙarshe_Daraja), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(Zangon_ƙarshe_Daraja))
        for Suna in Zangon_ƙarshe_Suna:
            Kwafi_Daraja(기준 / 'build' / (Suna + '.o'), 'objects/' + Suna + '.o')
        for Suna in laburare:
            Kwafi_Daraja(기준 / 'build' / Suna, 'objects/' + Path(Suna).name)
        for Suna in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'Mai_anfani_da_kwamfuta', '명명', 'na_ura_mai_kwakwalwa', 'Hanyar_sadarwa_tara/Hanyar_sadarwa_tara.h', '부팅/Kafa_Zagaye.ld',
                     'na_nesa_Daraja/assh_config.h', 'na_nesa_Daraja/config.h', 'na_nesa_Daraja/ctype.h', 'na_nesa_Daraja/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            Kwafi_Daraja(기준 / Suna, Suna)
        for Suna in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            Kwafi_Daraja(저장소 / Suna, Suna)
        for Hanyar_shiga in sorted((기준 / 'vendor').glob('LICENSE*')):
            Kwafi_Daraja(Hanyar_shiga, 'vendor/' + Hanyar_shiga.name)
        Kwafi_Daraja(기준 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        Kwafi_Daraja(기준 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        Kwafi_Daraja(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        Kwafi_Daraja(기준 / 'Kaya/재연결.py', 'relink.py')
        for Hanyar_shiga in sorted((기준 / 'build/user').glob('*.elf')):
            Kwafi_Daraja(Hanyar_shiga, 'build/user/' + Hanyar_shiga.name)
        for Suna in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            Kwafi_Daraja(기준 / 'build/user' / (Suna + '.o'), 'build/user/' + Suna + '.o')
        for Suna in ('crt', 'aot-runtime', 'lokacin_bude_yaren_gama_gari_taimako', 'Tafiyar_da', '미리번역', '되돌림'):
            Kwafi_Daraja(기준 / 'build/ccompiler' / (Suna + '.o'), 'build/ccompiler/' + Suna + '.o')
        명세 = dict(Rahoto_Daraja, objects=['objects/' + Suna + '.o' for Suna in Zangon_ƙarshe_Suna],
                    libraries=['objects/' + Path(Hanyar_shiga).name for Hanyar_shiga in laburare])
        (gungu_Daraja / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (gungu_Daraja / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        tageti = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / tageti.name
        with tarfile.open(str(임시압축), 'w:gz') as Rumbun_ajiya_Daraja:
            Rumbun_ajiya_Daraja.add(str(gungu_Daraja), arcname=gungu_Daraja.name)
        임시압축.replace(tageti)
    Rahoto_Daraja['relink_archive_sha256'] = hash_Fayil(tageti)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(Rahoto_Daraja, ensure_ascii=False, indent=2) + '\n')
    return tageti


if __name__ == '__main__':
    tatsar_manhaja_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    tatsar_manhaja_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    Daraja = tatsar_manhaja_48ee4b1b.parse_args()
    if Daraja.command == 'bundle':
        print('COSL source/relink kit:', 묶기())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
