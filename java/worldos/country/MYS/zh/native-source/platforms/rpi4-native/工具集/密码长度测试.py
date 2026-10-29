#!/usr/bin/env python3
"""개인 接通状态 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from 远程设置 import 准备
from COSL分发 import 目的地址名称, 库

项目根 = Path(__file__).resolve().parents[1]


def 运行():
    输出 = 项目根 / 'build/verification/password-length'
    输出.mkdir(parents=True, exist_ok=True)
    个人设置 = 项目根 / 'build/remote/access.json'
    原始设置 = 个人设置.read_bytes()
    报告值 = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 临时值:
            测试工作区 = Path(临时值)
            设置路径 = 测试工作区 / 'build/remote'
            设置路径.mkdir(parents=True)
            设置文件 = 设置路径 / 'access.json'
            def 写入设置(数据):
                设置文件.write_text(json.dumps(数据, ensure_ascii=False) + '\n')
                设置文件.chmod(0o600)
            def 验证设置(命令壳, 屏幕):
                写入设置({'user': 'user', 'ssh_password': 命令壳, 'vnc_password': 屏幕})
                原始 = 设置文件.read_bytes()
                准备(测试工作区)
                assert 设置文件.read_bytes() == 原始, 'Settings were rewritten'
                头值 = (设置路径 / '配置档.h').read_text()
                是否相等 = re.search(r'屏幕密码\[\] = \{([^}]+)\}', 头值)
                assert 是否相等 and len(是否相等.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (设置路径 / '配置档.h').stat().st_mode & 0o777 == 0o600
            for 命令壳, 屏幕 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                验证设置(命令壳, 屏幕)
            报告值['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for 更改值, 条目值 in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                数据 = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                数据.update(更改值)
                写入设置(数据)
                try:
                    准备(测试工作区)
                except SystemExit as 错误:
                    assert 条目值 in str(错误), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + 条目值)
            报告值['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            设置 = json.loads((项目根 / 'build/remote/libassh-build.json').read_text())['flags']
            编译器工具 = os.environ.get('ARM64_CC', 'clang')
            连接器 = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            存档工具 = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def 执行命令(实参, 日志记录):
                subprocess.run(list(map(str, 实参)), cwd=str(项目根), stdout=日志记录,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for 名称, 命令壳, 屏幕 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + 名称, flush=True)
                验证设置(命令壳, 屏幕)
                结果 = 输出 / 名称
                结果.mkdir(exist_ok=True)
                with (结果 / 'build.log').open('wb') as 日志记录:
                    目的地列 = []
                    for 原始 in sorted((项目根 / '远程值').glob('*.c')):
                        目的地址值 = 测试工作区 / (原始.stem + '.o')
                        执行命令([编译器工具] + 设置 + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', 设置路径, '-I', 项目根 / '远程值', '-I', 项目根 / 'vendor/libassh/src',
                             '-I', 项目根 / 'vendor/bearssl/inc', '-I', 项目根 / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 原始, '-o', 目的地址值], 日志记录)
                        目的地列.append(目的地址值)
                    远程捆绑 = 测试工作区 / 'libremote.a'
                    执行命令([存档工具, 'rcs', 远程捆绑] + 目的地列, 日志记录)
                    执行命令([连接器, '--gc-sections', '-T', 项目根 / '启动/链接布局.ld', '-o', 测试工作区 / 'kernel.elf'] +
                         [项目根 / 'build' / (名称 + '.o') for 名称 in 目的地址名称] + ['--start-group'] +
                         [远程捆绑 if 路径 == 'remote/libremote.a' else 项目根 / 'build' / 路径 for 路径 in 库] + ['--end-group'], 日志记录)
                    执行命令([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         测试工作区 / 'kernel.elf', 测试工作区 / 'kernel8.img'], 日志记录)
                with (结果 / 'remote-test.log').open('wb') as 日志记录:
                    执行命令(['python3', 项目根 / '工具集/远程连接状态测试.py', '--kernel', 测试工作区 / 'kernel8.img',
                         '--access', 设置文件, '--output', 结果], 日志记录)
                有效性校验 = json.loads((结果 / 'report.json').read_text())
                assert 有效性校验['passed']
                报告值['checks'].append(名称 + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        报告值['passed'] = True
    finally:
        报告值['personal_settings_unchanged'] = 个人设置.read_bytes() == 原始设置
        if not 报告值['personal_settings_unchanged']:
            报告值['passed'] = False
        报告值['kernel_sha256'] = hashlib.sha256((项目根 / 'build/kernel8.img').read_bytes()).hexdigest()
        (输出 / 'report.json').write_text(json.dumps(报告值, ensure_ascii=False, indent=2) + '\n')
    assert 报告值['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(报告值, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    运行()
