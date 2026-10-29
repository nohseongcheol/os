#!/usr/bin/env python3
"""当前项目 内置 ARM64 산출물을 검사하고 LGPL 源代码树·重新连接端点 자료를 함께 묶는다."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import tempfile

项目根 = Path(__file__).resolve().parents[1]
代码库根 = 项目根.parents[1]
目的地址名称 = ('entry', 'java', 'board', 'drawing', 'terminal', 'widgets', 'font', 'user', 'programs', 'cpp')
库 = ('libposix-kor-arm64.a', 'network/libnetwork.a', 'remote/libremote.a', 'remote/libassh.a', 'remote/libbearssl.a')


def 哈希文件(路径):
    return hashlib.sha256(Path(路径).read_bytes()).hexdigest()


def 审查状态():
    for 名称 in ('vendor/wolfssh', 'vendor/wolfssl', '远程值/user_settings.h'):
        if (项目根 / 名称).exists():
            raise SystemExit('COSL 分发值 停止: 上一个项目 GPL 远程值 구현이 源代码树 트리에 남아 있습니다: ' + 名称)
    有线值 = (项目根 / '通信网络/有线网络.c').read_text()
    if 'BSD-2-Clause AND BSD-4-Clause' not in 有线值 or 'SPDX-License-Identifier: GPL' in 有线值:
        raise SystemExit('COSL 分发值 停止: BSD GENET 实现·고지 验证 所需条件值')
    for 名称 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
        if not (代码库根 / 名称).is_file():
            raise SystemExit('COSL 分发值 고지 缺失方法: ' + 名称)
    符号值 = subprocess.check_output(['aarch64-linux-gnu-nm', str(项目根 / 'build/kernel.elf')]).decode()
    if re.search(r'\b(?:wolfSSH_|wolfSSL_|wc_[A-Z])\w*', 符号值):
        raise SystemExit('COSL 分发值 停止: 커널에 上一个项目 GPL 密码值/SSH 심볼이 남아 있습니다. 重试值 빌드하세요.')
    for 名称 in ('assh_context_create', 'br_des_ct_cbcenc_run', 'br_sha256_init'):
        if not re.search(r'\b' + 名称 + r'$', 符号值, re.M):
            raise SystemExit('COSL 대체 实现 누락: ' + 名称)
    with tempfile.TemporaryDirectory(dir=str(项目根 / 'build')) as 临时值:
        映像值 = Path(临时值) / 'kernel.img'
        subprocess.check_call(['aarch64-linux-gnu-objcopy', '-O', 'binary', str(项目根 / 'build/kernel.elf'), str(映像值)])
        if 哈希文件(映像值) != 哈希文件(项目根 / 'build/kernel8.img'):
            raise SystemExit('kernel.elf와 kernel8.img가 서로 다른 빌드입니다.')
    报告值 = {'scope': 'current jkoros ARM64 native kernel only', 'license': 'COSL with third-party/LGPL carve-outs',
          'kernel_sha256': 哈希文件(项目根 / 'build/kernel8.img'), 'wolf_symbols': False,
          'genet': 'FreeBSD BSD-2-Clause AND BSD-4-Clause port', 'ssh': 'libassh LGPL-2.1-or-later',
          'vnc_crypto': 'BearSSL MIT', 'physical_board_tested': False,
          'third_party_terms_preserved': True, 'legal_certification': False,
          'libraries': {名称: 哈希文件(项目根 / 'build' / 名称) for 名称 in 库}}
    (项目根 / 'build/cosl-distribution-check.json').write_text(json.dumps(报告值, ensure_ascii=False, indent=2) + '\n')
    return 报告值


def 可执行束打包():
    报告值 = 审查状态()
    分发值 = 项目根 / 'dist'
    分发值.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cosl-', dir=str(项目根 / 'build')) as 临时值:
        组值 = Path(临时值) / 'jkoros-native-relink'
        组值.mkdir()
        def 复制值(原始, 对端值):
            目的地址值 = 组值 / 对端值
            目的地址值.parent.mkdir(parents=True, exist_ok=True)
            if 原始.is_dir():
                shutil.copytree(str(原始), str(目的地址值), ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            else:
                shutil.copy2(str(原始), str(目的地址值))
        for 名称 in 目的地址名称:
            复制值(项目根 / 'build' / (名称 + '.o'), 'objects/' + 名称 + '.o')
        for 名称 in 库:
            复制值(项目根 / 'build' / 名称, 'objects/' + Path(名称).name)
        for 名称 in ('vendor/libassh', 'vendor/tinycc', 'vendor/uzlib', 'vendor/bearssl', 'vendor/freebsd-genet',
                     'C编译器', '用户', '命名', '计算机', '通信网络/通信网络.h', '启动/链接布局.ld',
                     '远程值/assh_config.h', '远程值/config.h', '远程值/ctype.h', '远程值/arpa',
                     'build/remote/libassh-build.json', 'build/programs.S', 'build/programs.h',
                     'build/ccompiler/resources.h', 'vendor/remote-sources.json', 'COSL分发指南.md'):
            复制值(项目根 / 名称, 名称)
        for 名称 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            复制值(代码库根 / 名称, 名称)
        for 路径 in sorted((项目根 / 'vendor').glob('LICENSE*')):
            复制值(路径, 'vendor/' + 路径.name)
        复制值(项目根 / 'vendor/LICENCE.broadcom', 'vendor/LICENCE.broadcom')
        复制值(项目根 / 'vendor/lwip/COPYING', 'vendor/LICENSE.lwip')
        复制值(代码库根 / 'posix-kor/arm64-native', 'posix-kor/arm64-native')
        复制值(项目根 / '工具集/重新连接端点.py', 'relink.py')
        for 路径 in sorted((项目根 / 'build/user').glob('*.elf')):
            复制值(路径, 'build/user/' + 路径.name)
        for 名称 in ('start', 'runtime', 'jar', 'tinflate', 'crc32', 'adler32'):
            复制值(项目根 / 'build/user' / (名称 + '.o'), 'build/user/' + 名称 + '.o')
        for 名称 in ('crt', 'aot-runtime', '运行时支持', '运行', '提前所属时间', '发回桥接'):
            复制值(项目根 / 'build/ccompiler' / (名称 + '.o'), 'build/ccompiler/' + 名称 + '.o')
        规格 = dict(报告值, objects=['objects/' + 名称 + '.o' for 名称 in 目的地址名称],
                    libraries=['objects/' + Path(路径).name for 路径 in 库])
        (组值 / 'relink.json').write_text(json.dumps(规格, ensure_ascii=False, indent=2) + '\n')
        (组值 / 'README.md').write_text('''# jkoros native LGPL source and relink kit

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

TinyCC source is included in vendor/tinycc; the native port is in C编译器.
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
        目标值 = 分发值 / 'jkoros-native-relink.tar.gz'
        临时存档 = Path(临时值) / 目标值.name
        with tarfile.open(str(临时存档), 'w:gz') as 存档值:
            存档值.add(str(组值), arcname=组值.name)
        临时存档.replace(目标值)
    报告值['relink_archive_sha256'] = 哈希文件(目标值)
    (分发值 / 'cosl-distribution.json').write_text(json.dumps(报告值, ensure_ascii=False, indent=2) + '\n')
    return 目标值


if __name__ == '__main__':
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('command', choices=('check', 'bundle'), nargs='?', default='check')
    值 = 解析器.parse_args()
    if 值.command == 'bundle':
        print('COSL source/relink kit:', 可执行束打包())
    else:
        print(json.dumps(审查状态(), ensure_ascii=False, indent=2))
