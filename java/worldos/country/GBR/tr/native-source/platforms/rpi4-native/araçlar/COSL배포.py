#!/usr/bin/env python3
"""geçerli_öğe Öz ARM64 산출물을 검사하고 LGPL kaynak_ağaç·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

işlem_kök = Path(__file__).resolve().parents[1]
depo_kök = işlem_kök.parents[1]
hedef_ad = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
kitaplık = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def özet_Dosya(yol):
    return hashlib.sha256(Path(yol).read_bytes()).hexdigest()


def 점검():
    for İsim in ('vendor/wolfssh', 'vendor/wolfssl', 'uzak_değer/user_settings.h'):
        if (işlem_kök / İsim).exists():
            raise SystemExit('COSL dağıtım_değer Durdur: Önceki_öğe GPL uzak_değer 구현이 kaynak_ağaç 트리에 남아 있습니다: ' + İsim)
    kablolu_değer = (işlem_kök / 'ağ_Yığın/kablolu_ağ.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in kablolu_değer or 'SPDX-License-Identifier: GPL' in kablolu_değer:
        raise SystemExit('COSL dağıtım_değer Durdur: BSD GENET gerçekleme·고지 doğrulamak 필요')
    for İsim in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (depo_kök / İsim).is_file():
            raise SystemExit('COSL dağıtım_değer 고지 없음: ' + İsim)
    simge_değer = subprocess.check_output(['aarch64-linux-gnu-nm', str(işlem_kök / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', simge_değer):
        raise SystemExit('COSL dağıtım_değer Durdur: 커널에 Önceki_öğe GPL parola_değer/SSH 심볼이 남아 있습니다. yeniden_denemek_değer 빌드하세요.')
    for İsim in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + İsim + r'$', simge_değer, re.M):
            raise SystemExit('COSL 대체 gerçekleme 누락: ' + İsim)
    with tempfile.TemporaryDirectory(dir=str(işlem_kök / 'build')) as 임시:
        RESİM_değer = Path(임시) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(işlem_kök / 'build/kernel.elf'), str(RESİM_değer)])
        if özet_Dosya(RESİM_değer) != özet_Dosya(işlem_kök / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    Rapor_değer = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': özet_Dosya(işlem_kök / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {İsim: özet_Dosya(işlem_kök / 'build' / İsim) for İsim in kitaplık}}
    (işlem_kök / 'build/cosl-distribution-check.json').write_text(json.dumps(Rapor_değer, ensure_ascii=False, indent=2) + '\n')
    return Rapor_değer


def BIND_uç_nokta():
    Rapor_değer = 점검()
    dağıtım_değer = işlem_kök / 'dist'
    dağıtım_değer.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(işlem_kök / 'build')) as 임시:
        Grup_değer = Path(임시) / 'jkoros-native-relink'
        Grup_değer.mkdir()
        def örnek_değer(원본, eş_değer):
            hedef_değer = Grup_değer / eş_değer
            hedef_değer.parent.mkdir(parents=True, exist_ok=True)
            if 원본.is_dir():
                shutil.copytree(str(원본), str(hedef_değer), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(원본), str(hedef_değer))
        for İsim in hedef_ad:
            örnek_değer(işlem_kök / 'build' / (İsim + '.o'), 'objects/' + İsim + '.o')
        for İsim in kitaplık:
            örnek_değer(işlem_kök / 'build' / İsim, 'objects/' + Path(İsim).name)
        for İsim in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C_derleyici', 'kullanıcı_alanı', '명명', 'makine', 'ağ_Yığın/ağ_Yığın.h', 'makine_başlatma/bağlama_düzeni.ld',
                     'uzak_değer/assh_config.h', 'uzak_değer/config.h', 'uzak_değer/ctype.h', 'uzak_değer/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            örnek_değer(işlem_kök / İsim, İsim)
        for İsim in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            örnek_değer(depo_kök / İsim, İsim)
        for yol in sorted((işlem_kök / 'vendor').glob('LICENSE*')):
            örnek_değer(yol, 'vendor/' + yol.name)
        örnek_değer(işlem_kök / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        örnek_değer(işlem_kök / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        örnek_değer(depo_kök / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        örnek_değer(işlem_kök / 'araçlar/재연결.py', 'relink.py')
        for yol in sorted((işlem_kök / 'build/user').glob('*.elf')):
            örnek_değer(yol, 'build/user/' + yol.name)
        for İsim in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            örnek_değer(işlem_kök / 'build/user' / (İsim + '.o'), 'build/user/' + İsim + '.o')
        for İsim in ('crt', 'aot-runtime', 'CLR_Destek', 'çalıştır', '미리번역', 'İade_köprü'):
            örnek_değer(işlem_kök / 'build/ccompiler' / (İsim + '.o'), 'build/ccompiler/' + İsim + '.o')
        명세 = dict(Rapor_değer, objects=['objects/' + İsim + '.o' for İsim in hedef_ad],
                    libraries=['objects/' + Path(yol).name for yol in kitaplık])
        (Grup_değer / 'relink.json').write_text(json.dumps(명세, ensure_ascii=False, indent=2) + '\n')
        (Grup_değer / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C_derleyici.
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
        hedef = dağıtım_değer / 'jkoros-native-relink.tar.gz'
        임시압축 = Path(임시) / hedef.name
        with tarfile.open(str(임시압축), 'w:gz') as Arşiv_değer:
            Arşiv_değer.add(str(Grup_değer), arcname=Grup_değer.name)
        임시압축.replace(hedef)
    Rapor_değer['relink_archive_sha256'] = özet_Dosya(hedef)
    (dağıtım_değer / 'cosl-distribution.json').write_text(json.dumps(Rapor_değer, ensure_ascii=False, indent=2) + '\n')
    return hedef


if __name__ == '__main__':
    ayrıştırıcı_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ayrıştırıcı_48ee4b1b.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    değer = ayrıştırıcı_48ee4b1b.parse_args()
    if değer.command == 'bundle':
        print('COSL source/relink kit:', BIND_uç_nokta())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
