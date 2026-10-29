#!/usr/bin/env python3
"""လက်ရှိအချက်အလက်တစ်ခု ကိုယ်ပိုင် ARM64 산출물을 검사하고 LGPL မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ·재연결 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

စီမံကိန်းအမြစ် = Path(__file__).resolve().parents[1]
저장소 = စီမံကိန်းအမြစ်.parents[1]
ဦးတည်ရာအမည် = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
စာကြည့်တိုက် = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def ဖိုင်ဟက်ရှ်တွက်(လမ်း):
    return hashlib.sha256(Path(လမ်း).read_bytes()).hexdigest()


def 점검():
    for အမည် in ('vendor/wolfssh', 'vendor/wolfssl', 'အဝေးတန်ဖိုး/user_settings.h'):
        if (စီမံကိန်းအမြစ် / အမည်).exists():
            raise SystemExit('COSL ဖြန့်ချိမှုတန်ဖိုး ရပ်: ယခင်အချက်အလက်တစ်ခု GPL အဝေးတန်ဖိုး 구현이 မူရင်းကုဒ်အပင်ဖွဲ့စည်းပုံ 트리에 남아 있습니다: ' + အမည်)
    유선 = (စီမံကိန်းအမြစ် / 'ကွန်ရက်အလွှာစု/유선망.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 유선 or 'SPDX-License-Identifier: GPL' in 유선:
        raise SystemExit('COSL ဖြန့်ချိမှုတန်ဖိုး ရပ်: BSD GENET အကောင်အထည်ဖော်မှု·고지 အတည်ပြု 필요')
    for အမည် in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (저장소 / အမည်).is_file():
            raise SystemExit('COSL ဖြန့်ချိမှုတန်ဖိုး 고지 없음: ' + အမည်)
    သင်္ကေတတန်ဖိုး = subprocess.check_output(['aarch64-linux-gnu-nm', str(စီမံကိန်းအမြစ် / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', သင်္ကေတတန်ဖိုး):
        raise SystemExit('COSL ဖြန့်ချိမှုတန်ဖိုး ရပ်: 커널에 ယခင်အချက်အလက်တစ်ခု GPL စကားဝှက်တန်ဖိုး/SSH 심볼이 남아 있습니다. ပြန်ကြိုးစား 빌드하세요.')
    for အမည် in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + အမည် + r'$', သင်္ကေတတန်ဖိုး, re.M):
            raise SystemExit('COSL 대체 အကောင်အထည်ဖော်မှု 누락: ' + အမည်)
    with tempfile.TemporaryDirectory(dir=str(စီမံကိန်းအမြစ် / 'build')) as ယာယီတန်ဖိုး:
        စက်ပုံရိပ်တန်ဖိုး = Path(ယာယီတန်ဖိုး) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(စီမံကိန်းအမြစ် / 'build/kernel.elf'), str(စက်ပုံရိပ်တန်ဖိုး)])
        if ဖိုင်ဟက်ရှ်တွက်(စက်ပုံရိပ်တန်ဖိုး) != ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ် / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    အစီရင်ခံစာတန်ဖိုး = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ် / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {အမည်: ဖိုင်ဟက်ရှ်တွက်(စီမံကိန်းအမြစ် / 'build' / အမည်) for အမည် in စာကြည့်တိုက်}}
    (စီမံကိန်းအမြစ် / 'build/cosl-distribution-check.json').write_text(json.dumps(အစီရင်ခံစာတန်ဖိုး, ensure_ascii=False, indent=2) + '\n')
    return အစီရင်ခံစာတန်ဖိုး


def စက်ဖိုင်ထုပ်ပိုး():
    အစီရင်ခံစာတန်ဖိုး = 점검()
    ဖြန့်ချိမှုတန်ဖိုး = စီမံကိန်းအမြစ် / 'dist'
    ဖြန့်ချိမှုတန်ဖိုး.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(စီမံကိန်းအမြစ် / 'build')) as ယာယီတန်ဖိုး:
        အုပ်စုတန်ဖိုး = Path(ယာယီတန်ဖိုး) / 'jkoros-native-relink'
        အုပ်စုတန်ဖိုး.mkdir()
        def တန်ဖိုးမိတ္တူကူး(မူရင်း, တစ်ဖက်တန်ဖိုး):
            ဦးတည်ရာတန်ဖိုး = အုပ်စုတန်ဖိုး / တစ်ဖက်တန်ဖိုး
            ဦးတည်ရာတန်ဖိုး.parent.mkdir(parents=True, exist_ok=True)
            if မူရင်း.is_dir():
                shutil.copytree(str(မူရင်း), str(ဦးတည်ရာတန်ဖိုး), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(မူရင်း), str(ဦးတည်ရာတန်ဖိုး))
        for အမည် in ဦးတည်ရာအမည်:
            တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / 'build' / (အမည် + '.o'), 'objects/' + အမည် + '.o')
        for အမည် in စာကြည့်တိုက်:
            တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / 'build' / အမည်, 'objects/' + Path(အမည်).name)
        for အမည် in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'Cဘာသာပြန်စက်', 'သုံးစွဲသူ', '명명', 'စက်', 'ကွန်ရက်အလွှာစု/ကွန်ရက်အလွှာစု.h', 'စက်တင်/နေရာချထားပုံ.ld',
                     'အဝေးတန်ဖိုး/assh_config.h', 'အဝေးတန်ဖိုး/config.h', 'အဝေးတန်ဖိုး/ctype.h', 'အဝေးတန်ဖိုး/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL배포안내.md'):
            တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / အမည်, အမည်)
        for အမည် in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            တန်ဖိုးမိတ္တူကူး(저장소 / အမည်, အမည်)
        for လမ်း in sorted((စီမံကိန်းအမြစ် / 'vendor').glob('LICENSE*')):
            တန်ဖိုးမိတ္တူကူး(လမ်း, 'vendor/' + လမ်း.name)
        တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        တန်ဖိုးမိတ္တူကူး(저장소 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / 'ကိရိယာစု/재연결.py', 'relink.py')
        for လမ်း in sorted((စီမံကိန်းအမြစ် / 'build/user').glob('*.elf')):
            တန်ဖိုးမိတ္တူကူး(လမ်း, 'build/user/' + လမ်း.name)
        for အမည် in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / 'build/user' / (အမည် + '.o'), 'build/user/' + အမည် + '.o')
        for အမည် in ('crt', 'aot-runtime', 'လည်ပတ်ဝန်းကျင်ထောက်ပံ့မှု', 'လုပ်ဆောင်', '미리번역', 'ပြန်ပေးတံတား'):
            တန်ဖိုးမိတ္တူကူး(စီမံကိန်းအမြစ် / 'build/ccompiler' / (အမည် + '.o'), 'build/ccompiler/' + အမည် + '.o')
        သတ်မှတ်စံ = dict(အစီရင်ခံစာတန်ဖိုး, objects=['objects/' + အမည် + '.o' for အမည် in ဦးတည်ရာအမည်],
                    libraries=['objects/' + Path(လမ်း).name for လမ်း in စာကြည့်တိုက်])
        (အုပ်စုတန်ဖိုး / 'relink.json').write_text(json.dumps(သတ်မှတ်စံ, ensure_ascii=False, indent=2) + '\n')
        (အုပ်စုတန်ဖိုး / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in Cဘာသာပြန်စက်.
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
        ဦးတည်ချက်တန်ဖိုး = ဖြန့်ချိမှုတန်ဖိုး / 'jkoros-native-relink.tar.gz'
        ယာယီမော်ကွန်း = Path(ယာယီတန်ဖိုး) / ဦးတည်ချက်တန်ဖိုး.name
        with tarfile.open(str(ယာယီမော်ကွန်း), 'w:gz') as မော်ကွန်းတန်ဖိုး:
            မော်ကွန်းတန်ဖိုး.add(str(အုပ်စုတန်ဖိုး), arcname=အုပ်စုတန်ဖိုး.name)
        ယာယီမော်ကွန်း.replace(ဦးတည်ချက်တန်ဖိုး)
    အစီရင်ခံစာတန်ဖိုး['relink_archive_sha256'] = ဖိုင်ဟက်ရှ်တွက်(ဦးတည်ချက်တန်ဖိုး)
    (ဖြန့်ချိမှုတန်ဖိုး / 'cosl-distribution.json').write_text(json.dumps(အစီရင်ခံစာတန်ဖိုး, ensure_ascii=False, indent=2) + '\n')
    return ဦးတည်ချက်တန်ဖိုး


if __name__ == '__main__':
    해석기 = argparse.ArgumentParser(description=__doc__)
    해석기.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    တန်ဖိုး = 해석기.parse_args()
    if တန်ဖိုး.command == 'bundle':
        print('COSL source/relink kit:', စက်ဖိုင်ထုပ်ပိုး())
    else:
        print(json.dumps(점검(), ensure_ascii=False, indent=2))
