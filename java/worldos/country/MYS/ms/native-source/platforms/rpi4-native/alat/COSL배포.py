#!/usr/bin/env python3
"""현재 Asli ARM64 산출물을 검사하고 LGPL sumber_pepohon·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

projek_akar = Path(__file__).resolve().parents[1]
repositori_akar = projek_akar.parents[1]
destinasi_nama = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
pustaka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def cincangan_fail(LALUAN):
    return hashlib.sha256(Path(LALUAN).read_bytes()).hexdigest()


def 점검():
    for Nama in ('vendor/wolfssh', 'vendor/wolfssl', 'jauh_VALUE/user_settings.h'):
        if (projek_akar / Nama).exists():
            raise SystemExit('COSL 배포 Henti: 이전 GPL jauh_VALUE 구현이 sumber_pepohon 트리에 남아 있습니다: ' + Nama)
    berwayar_VALUE = (projek_akar / 'rangkaian_tindan/berwayar_rangkaian.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in berwayar_VALUE or 'SPDX-License-Identifier: GPL' in berwayar_VALUE:
        raise SystemExit('COSL 배포 Henti: BSD GENET pelaksanaan·고지 tentu_sahkan 필요')
    for Nama in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repositori_akar / Nama).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Nama)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(projek_akar / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Henti: 커널에 이전 GPL kata_laluan_VALUE/SSH 심볼이 남아 있습니다. 다시 빌드하세요.')
    for Nama in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nama + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 pelaksanaan 누락: ' + Nama)
    with tempfile.TemporaryDirectory(dir=str(projek_akar / 'build')) as 임시:
        imej_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(projek_akar / 'build/kernel.elf'), str(imej_VALUE)])
        if cincangan_fail(imej_VALUE) != cincangan_fail(projek_akar / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    lapor_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': cincangan_fail(projek_akar / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nama: cincangan_fail(projek_akar / 'build' / Nama) for Nama in pustaka}}
    (projek_akar / 'build/cosl-distribution-check.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    return lapor_VALUE


def ikat_peserta():
    lapor_VALUE = 점검()
    배포 = projek_akar / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(projek_akar / 'build')) as 임시:
        Kumpulan_VALUE = Path(임시) / 'jkoros-native-relink'
        Kumpulan_VALUE.mkdir()
        def tika_VALUE(원본, rakan_VALUE):
            destinasi_VALUE = Kumpulan_VALUE / rakan_VALUE
            destinasi_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(destinasi_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(destinasi_VALUE))
        for Nama in destinasi_nama:
            tika_VALUE(projek_akar / 'build' / (Nama + '.o'), 'objects/' + Nama + '.o')
        for Nama in pustaka:
            tika_VALUE(projek_akar / 'build' / Nama, 'objects/' + Path(Nama).name)
        for Nama in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ruang_pengguna', '명명', 'mesin', 'rangkaian_tindan/rangkaian_tindan.h', 'permulaan_mesin/susun_atur_pautan.ld',
                     'jauh_VALUE/assh_config.h', 'jauh_VALUE/config.h', 'jauh_VALUE/ctype.h', 'jauh_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            tika_VALUE(projek_akar / Nama, Nama)
        for Nama in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            tika_VALUE(repositori_akar / Nama, Nama)
        for LALUAN in sorted((projek_akar / 'vendor').glob('LICENSE*')):
            tika_VALUE(LALUAN, 'vendor/' + LALUAN.name)
        tika_VALUE(projek_akar / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        tika_VALUE(projek_akar / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        tika_VALUE(repositori_akar / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        tika_VALUE(projek_akar / 'alat/재연결.py', 'relink.py')
        for LALUAN in sorted((projek_akar / 'build/user').glob('*.elf')):
            tika_VALUE(LALUAN, 'build/user/' + LALUAN.name)
        for Nama in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            tika_VALUE(projek_akar / 'build/user' / (Nama + '.o'), 'build/user/' + Nama + '.o')
        for Nama in ('crt', 'aot-runtime', 'masa_jalan_bahasa_biasa_Sokongan', 'Jalan', '미리번역', 'kembalikan_penghubung'):
            tika_VALUE(projek_akar / 'build/ccompiler' / (Nama + '.o'), 'build/ccompiler/' + Nama + '.o')
        명세 = dict(lapor_VALUE, objects=['objects/' + Nama + '.o' for Nama in destinasi_nama],
                    libraries=['objects/' + Path(LALUAN).name for LALUAN in pustaka])
        (Kumpulan_VALUE / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Kumpulan_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        sasaran = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / sasaran.name
        with tarfile.open(str(임시압축), 'w:gz') as Arkib_VALUE:
            Arkib_VALUE.add(str(Kumpulan_VALUE), arcname=Kumpulan_VALUE.name)
        임시압축.replace(sasaran)
    lapor_VALUE['relink_archive_sha256'] = cincangan_fail(sasaran)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    return sasaran


if __name__ == '__main__':
    penghurai_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    penghurai_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = penghurai_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', ikat_peserta())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
