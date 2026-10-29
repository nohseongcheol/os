#!/usr/bin/env python3
"""saat_ini_item Asli ARM64 산출물을 검사하고 LGPL sumber_pohon·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

Tugas_akar = Path(__file__).resolve().parents[1]
repositori_akar = Tugas_akar.parents[1]
tujuan_nama = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
pustaka = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def hash_file(jalur):
    return hashlib.sha256(Path(jalur).read_bytes()).hexdigest()


def 점검():
    for Nama_2 in ('vendor/wolfssh', 'vendor/wolfssl', 'jarak_jauh_VALUE/user_settings.h'):
        if (Tugas_akar / Nama_2).exists():
            raise SystemExit('COSL 배포 Hentikan: 이전 GPL jarak_jauh_VALUE 구현이 sumber_pohon 트리에 남아 있습니다: ' + Nama_2)
    terkabel_VALUE = (Tugas_akar / 'jaringan_tumpuk/terkabel_jaringan.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in terkabel_VALUE or 'SPDX-License-Identifier: GPL' in terkabel_VALUE:
        raise SystemExit('COSL 배포 Hentikan: BSD GENET implementasi·고지 periksa 필요')
    for Nama_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (repositori_akar / Nama_2).is_file():
            raise SystemExit('COSL 배포 고지 없음: ' + Nama_2)
    simbol_VALUE = subprocess.check_output(['aarch64-linux-gnu-nm', str(Tugas_akar / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simbol_VALUE):
        raise SystemExit('COSL 배포 Hentikan: 커널에 이전 GPL sandi_VALUE/SSH 심볼이 남아 있습니다. coba_lagi_VALUE 빌드하세요.')
    for Nama_2 in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + Nama_2 + r'$', simbol_VALUE, re.M):
            raise SystemExit('COSL 대체 implementasi 누락: ' + Nama_2)
    with tempfile.TemporaryDirectory(dir=str(Tugas_akar / 'build')) as 임시:
        foto_VALUE = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(Tugas_akar / 'build/kernel.elf'), str(foto_VALUE)])
        if hash_file(foto_VALUE) != hash_file(Tugas_akar / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    lapor_VALUE = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': hash_file(Tugas_akar / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {Nama_2: hash_file(Tugas_akar / 'build' / Nama_2) for Nama_2 in pustaka}}
    (Tugas_akar / 'build/cosl-distribution-check.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    return lapor_VALUE


def ikat_peserta():
    lapor_VALUE = 점검()
    배포 = Tugas_akar / 'dist'
    배포.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(Tugas_akar / 'build')) as 임시:
        grup_VALUE = Path(임시) / 'jkoros-native-relink'
        grup_VALUE.mkdir()
        def salin_VALUE(원본, serekan_VALUE):
            tujuan_VALUE = grup_VALUE / serekan_VALUE
            tujuan_VALUE.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(tujuan_VALUE), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(tujuan_VALUE))
        for Nama_2 in tujuan_nama:
            salin_VALUE(Tugas_akar / 'build' / (Nama_2 + '.o'), 'objects/' + Nama_2 + '.o')
        for Nama_2 in pustaka:
            salin_VALUE(Tugas_akar / 'build' / Nama_2, 'objects/' + Path(Nama_2).name)
        for Nama_2 in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     '시언어번역기', 'ruang_pengguna', '명명', 'mesin', 'jaringan_tumpuk/jaringan_tumpuk.h', 'awal_mesin/tata_letak_penautan.ld',
                     'jarak_jauh_VALUE/assh_config.h', 'jarak_jauh_VALUE/config.h', 'jarak_jauh_VALUE/ctype.h', 'jarak_jauh_VALUE/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            salin_VALUE(Tugas_akar / Nama_2, Nama_2)
        for Nama_2 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            salin_VALUE(repositori_akar / Nama_2, Nama_2)
        for jalur in sorted((Tugas_akar / 'vendor').glob('LICENSE*')):
            salin_VALUE(jalur, 'vendor/' + jalur.name)
        salin_VALUE(Tugas_akar / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        salin_VALUE(Tugas_akar / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        salin_VALUE(repositori_akar / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        salin_VALUE(Tugas_akar / 'alat/재연결.py', 'relink.py')
        for jalur in sorted((Tugas_akar / 'build/user').glob('*.elf')):
            salin_VALUE(jalur, 'build/user/' + jalur.name)
        for Nama_2 in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            salin_VALUE(Tugas_akar / 'build/user' / (Nama_2 + '.o'), 'build/user/' + Nama_2 + '.o')
        for Nama_2 in ('crt', 'aot-runtime', 'runtime_bahasa_umum_dukung', 'jalankan', '미리번역', 'kembalikan_bridge'):
            salin_VALUE(Tugas_akar / 'build/ccompiler' / (Nama_2 + '.o'), 'build/ccompiler/' + Nama_2 + '.o')
        spes = dict(lapor_VALUE, objects=['objects/' + Nama_2 + '.o' for Nama_2 in tujuan_nama],
                    libraries=['objects/' + Path(jalur).name for jalur in pustaka])
        (grup_VALUE / 'relink.json').write_text(json.dumps(spes, ensure_ascii=False, indent=2) + '\n')
        (grup_VALUE / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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
        target = 배포 / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / target.name
        with tarfile.open(str(임시압축), 'w:gz') as Arsip_VALUE:
            Arsip_VALUE.add(str(grup_VALUE), arcname=grup_VALUE.name)
        임시압축.replace(target)
    lapor_VALUE['relink_archive_sha256'] = hash_file(target)
    (배포 / 'cosl-distribution.json').write_text(json.dumps(lapor_VALUE, ensure_ascii=False, indent=2) + '\n')
    return target


if __name__ == '__main__':
    parser_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    parser_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    VALUE = parser_48ee4b1b.parse_args()
    if VALUE.command == 'bundle':
        print('COSL source/relink kit:', ikat_peserta())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
