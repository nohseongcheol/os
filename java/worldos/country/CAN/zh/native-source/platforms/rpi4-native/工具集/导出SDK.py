#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
from 执行命令 import 项目根


def 运行():
    分发路径 = 项目根 / 'dist'
    分发路径.mkdir(exist_ok=True)
    POSIX = 项目根.parents[1] / 'posix-kor/arm64-native'
    with tempfile.TemporaryDirectory(prefix='sdk-', dir=str(项目根 / 'build')) as 工作中路径:
        开发工具套件 = Path(工作中路径) / 'jkoros-native-sdk'
        文件列表 = {
            项目根.parents[1] / 'LICENSE': 'LICENSE',
            项目根.parents[1] / 'THIRD_PARTY_NOTICES.md': 'THIRD_PARTY_NOTICES.md',
            项目根 / '工具集/SDK编译.py': 'compile.py',
            项目根 / '用户/调用.h': 'include/调用.h',
            项目根 / '命名/计算机连接名称列.h': '命名/计算机连接名称列.h',
            项目根 / '用户/链接布局.ld': 'user.ld',
            POSIX / '头文件/文件ABI.h': 'include/文件ABI.h',
            POSIX / '头文件/网络ABI.h': 'include/网络ABI.h',
            项目根 / 'build/user/start.o': 'lib/start.o',
            项目根 / 'build/user/runtime.o': 'lib/runtime.o',
            项目根 / 'build/libposix-kor-user.a': 'lib/libposix-kor-user.a',
            项目根 / '用户/文件例.cpp': 'examples/文件例.cpp',
            项目根 / '用例/韩文字母编码方式/问候例.c': 'examples/问候例.c',
            项目根 / '用例/韩文字母编码方式/流值.c': 'examples/流值.c',
            项目根 / '用例/韩文字母编码方式/问候例.cpp': 'examples/问候例.cpp',
            项目根 / '用户/通信示例.cpp': 'examples/通信示例.cpp',
            项目根 / 'build/user/demo.elf': 'examples/demo.elf',
            项目根 / 'build/user/network.elf': 'examples/network.elf',
        }
        捆绑构建清单 = {'abi': 'JKOROS AArch64 EL0 v1', 'libc': False, 'libstdcxx': False, 'sha256': {}}
        for 原始数据, 目标值 in 文件列表.items():
            目的地址数据地址 = 开发工具套件 / 目标值
            目的地址数据地址.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(原始数据), str(目的地址数据地址))
            捆绑构建清单['sha256'][目标值] = hashlib.sha256(目的地址数据地址.read_bytes()).hexdigest()
        (开发工具套件 / 'manifest.json').write_text(json.dumps(捆绑构建清单, indent=2) + '\n')
        (开发工具套件 / 'README.txt').write_text('JKOROS native AArch64 EL0 SDK, ABI v1.\n'
            'python3 compile.py examples/文件例.cpp -o demo.elf\n'
            'python3 compile.py examples/问候例.c -o hello-c.elf\n'
            'Requires host Clang/Clang++ and aarch64-linux-gnu-ld. No libc/libstdc++/exceptions/RTTI.\n'
            'Host SDK entry: extern "C" int 开始用户程序(int). Korean file/UDP/stream APIs in include/.\n'
            'Guest cc uses main(argc,argv); jaot accepts the documented static Java subset.\n'
            'FTP upload: 工具集/执行命令.py --network, then guest ftpd start; localhost:2121.\n'
            'From platforms/rpi4-native: python3 工具集/执行文件.py /path/demo.elf\n'
            'Or paste hex with guest load FILE, then run FILE. Maximum RAM file: 16384 bytes.\n'
            'UTF-8 arguments: 用户参数个数()/用户参数() in 调用.h.\n'
            'Not compatible with Linux binaries. OpenJDK/CPython not yet ported.\n')
        存档 = Path(工作中路径) / 'jkoros-native-aarch64-sdk.tar.gz'
        with tarfile.open(str(存档), 'w:gz') as 结果数据:
            结果数据.add(str(开发工具套件), arcname=开发工具套件.name)
        存档.replace(分发路径 / 存档.name)
        # Supply the vendored LGPL compiler sources and local port/relink objects.
        编译器存档 = Path(工作中路径) / 'jkoros-native-compiler-source.tar.gz'
        with tarfile.open(str(编译器存档), 'w:gz') as 结果数据:
            for 名称 in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
                结果数据.add(str(项目根.parents[1] / 名称), arcname='jkoros-native/' + 名称)
            for 相对路径 in ('vendor/tinycc', 'vendor/uzlib', 'vendor/README.md', 'vendor/LICENSE.gcc-gpl3',
                             'vendor/LICENSE.libgcc-runtime', 'C编译器', '用户', '命名',
                             '工具集/构建C编译器.py', '工具集/构建用户空间.py', '文件传送与编译过程.md'):
                结果数据.add(str(项目根 / 相对路径), arcname='jkoros-native/' + 相对路径)
            for 名称 in ('crt.o', 'aot-runtime.o', '运行时支持.o', '运行.o', '提前所属时间.o', '发回桥接.o'):
                目的地址文件 = 项目根 / 'build/ccompiler' / 名称
                结果数据.add(str(目的地址文件), arcname='jkoros-native/relink/' + 名称)
            for 名称 in ('start.o','runtime.o','jar.o','tinflate.o','crc32.o','adler32.o'):
                结果数据.add(str(项目根 / 'build/user' / 名称), arcname='jkoros-native/relink/user/' + 名称)
            结果数据.add(str(项目根 / 'build/ccompiler/resources.h'), arcname='jkoros-native/relink/resources.h')
            结果数据.add(str(POSIX), arcname='posix-kor/arm64-native')
        编译器存档.replace(分发路径 / 编译器存档.name)
    print('SDK:', 分发路径 / 'jkoros-native-aarch64-sdk.tar.gz')


if __name__ == '__main__':
    运行()
