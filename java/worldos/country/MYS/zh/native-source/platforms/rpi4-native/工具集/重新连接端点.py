#!/usr/bin/env python3
"""分发值 묶음에서 libassh/TinyCC를 교체하고 内置 커널을 重试值 연결한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

项目根 = Path(__file__).resolve().parent


def 执行命令(机器字文本):
    subprocess.check_call([str(条目值) for 条目值 in 机器字文本], cwd=str(项目根))


def 运行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--verify', action='store_true', help='원래 이미지와 동일한 SHA256인지 验证')
    解析器.add_argument('--libassh-archive', type=Path, help='별도로 修改值·컴파일한 libassh.a 使用值')
    解析器.add_argument('--tinycc', action='store_true', help='TinyCC 소스도 重试值 컴파일하고 커널에 탑재')
    解析器.add_argument('--sdk', type=Path, help='TinyCC용 Alpine ARM64 SDK rootfs (원래 헤더·libgcc)')
    实参 = 解析器.parse_args()
    规格 = json.loads((项目根 / 'relink.json').read_text())
    构建系统 = 项目根 / 'build'
    新建捆绑 = 构建系统 / 'relinked'
    新建捆绑.mkdir(exist_ok=True)
    编译器工具 = os.environ.get('ARM64_CC', 'clang')
    连接器 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
    存档工具 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
    远程设置 = json.loads((构建系统 / 'remote/libassh-build.json').read_text())
    设置 = 远程设置['flags']
    if 实参.libassh_archive:
        安全性捆绑 = 实参.libassh_archive.resolve()
    else:
        目的地列 = []
        头文件 = ['-I', 项目根 / '远程值', '-I', 项目根 / 'vendor/libassh/src', '-isystem', '/usr/include/newlib']
        for 名称 in 远程设置['sources']:
            目的地址值 = 新建捆绑 / (Path(名称).stem + '.o')
            执行命令([编译器工具] + 设置 + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections'] + 头文件 +
                 ['-c', 项目根 / 名称, '-o', 目的地址值])
            目的地列.append(目的地址值)
        安全性捆绑 = 新建捆绑 / 'libassh.a'
        with tempfile.TemporaryDirectory(dir=str(新建捆绑)) as 临时值:
            临时捆绑 = Path(临时值) / 'libassh.a'
            执行命令([存档工具, 'rcs', 临时捆绑] + 目的地列)
            临时捆绑.replace(安全性捆绑)
    if 实参.tinycc:
        if not 实参.sdk:
            解析器.error('--tinycc requires --sdk pointing to the documented Alpine ARM64 SDK rootfs')
        开发 = 实参.sdk.resolve()
        算术值 = sorted((开发 / 'usr/lib/gcc/aarch64-alpine-linux-musl').glob('*/libgcc.a'))
        if not 算术值 or not (开发 / 'usr/include/stdio.h').is_file():
            解析器.error('SDK must contain ARM64 musl headers and libgcc.a')
        启用侧设定配置 = [选中状态值 for 选中状态值 in 设置 if 选中状态值 != '-mgeneral-regs-only']
        目的地址值 = 新建捆绑 / '编译器工具.o'
        执行命令([编译器工具] + 启用侧设定配置 + ['-ffunction-sections', '-fdata-sections',
             '-I', 项目根 / 'C编译器', '-I', 项目根 / 'vendor/tinycc', '-I', 项目根 / '用户',
             '-I', 构建系统 / 'ccompiler', '-isystem', 开发 / 'usr/include', '-c', 项目根 / 'C编译器/编译器工具.c', '-o', 目的地址值])
        执行命令([连接器, '--gc-sections', '-T', 项目根 / '用户/链接布局.ld', '-z', 'max-page-size=4096',
             '-o', 构建系统 / 'user/cc.elf', 构建系统 / 'user/start.o', 构建系统 / 'user/runtime.o', 目的地址值] +
             [构建系统 / 'ccompiler' / (名称 + '.o') for 名称 in ('运行时支持', '运行', '提前所属时间', '发回桥接')] +
             [构建系统 / 'user' / (名称 + '.o') for 名称 in ('jar', 'tinflate', 'crc32', 'adler32')] + [算术值[-1]])
        头值 = 构建系统 / 'programs.h'
        头值.write_text(re.sub(r'(\{user_blob_cc, )\d+', lambda 是否相等: 是否相等.group(1) + str((构建系统 / 'user/cc.elf').stat().st_size), 头值.read_text()))
        执行命令([编译器工具] + 设置 + ['-c', 构建系统 / 'programs.S', '-o', 项目根 / 'objects/programs.o'])
        执行命令([编译器工具] + 设置 + ['-std=c11', '-I', 项目根 / 'posix-kor/arm64-native/头文件', '-I', 构建系统,
             '-c', 项目根 / '计算机/用户.c', '-o', 项目根 / 'objects/user.o'])
    执行命令([连接器, '--gc-sections', '-T', 项目根 / '启动/链接布局.ld', '-o', 新建捆绑 / 'kernel.elf'] +
         [项目根 / 路径 for 路径 in 规格['objects']] + ['--start-group'] +
         [安全性捆绑 if 路径 == 'objects/libassh.a' else 项目根 / 路径 for 路径 in 规格['libraries']] + ['--end-group'])
    执行命令([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary', 新建捆绑 / 'kernel.elf', 新建捆绑 / 'kernel8.img'])
    哈希文件 = hashlib.sha256((新建捆绑 / 'kernel8.img').read_bytes()).hexdigest()
    if 实参.verify and 哈希文件 != 规格['kernel_sha256']:
        raise SystemExit('重新连接端点 결과가 원본과 다릅니다. 의도적으로 라이브러리를 수정했다면 --verify 없이 실행하세요. SHA256=' + 哈希文件)
    print('RELINK PASS', 哈希文件, 新建捆绑 / 'kernel8.img')


if __name__ == '__main__':
    运行()
