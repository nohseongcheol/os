#!/usr/bin/env python3
"""PyPI 物理硬件 배포와 부정 输入值·RAM 되돌림을 内置 커널에서 검사한다."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import shutil
import socket
import subprocess
import time
import zipfile
from 捆绑中继 import 捆绑代码库, 解压缩
from 执行命令 import 项目根


def 测试滚轮(名称, 文件条目列, 契约值='Root-Is-Purelib: true\n', 依赖项列=''):
    数据 = io.BytesIO()
    with zipfile.ZipFile(数据, 'w', zipfile.ZIP_DEFLATED) as 软件包:
        软件包.writestr(名称 + '-1.0.dist-info/WHEEL', 'Wheel-Version: 1.0\n' + 契约值)
        软件包.writestr(名称 + '-1.0.dist-info/METADATA', 'Metadata-Version: 2.1\nName: ' + 名称 + '\nVersion: 1.0\n' + 依赖项列)
        for 路径, 内容值 in 文件条目列.items():
            软件包.writestr(路径, 内容值)
    return 数据.getvalue()


def 检查宿主():
    是否常规 = 测试滚轮('jkoros-fixture', {'mod.py': '值=42\n'})
    assert 解压缩('jkoros_fixture-1.0-py3-none-any.whl', 是否常规, 'jkoros-fixture', '1.0') == {'mod.py': '值=42\n'.encode()}
    for 数据 in (
            测试滚轮('jkoros-fixture', {'../escape.py': ''}),
            测试滚轮('jkoros-fixture', {'/abs.py': ''}),
            测试滚轮('jkoros-fixture', {'big.py': 'x' * 16385}),
            测试滚轮('jkoros-fixture', {'mod.so': ''}),
            测试滚轮('jkoros-fixture', {'mod.py': ''}, 'Root-Is-Purelib: false\n'),
            测试滚轮('jkoros-fixture', {'mod.py': ''}, 依赖项列='Requires-Dist: requests\n')):
        try:
            解压缩('jkoros_fixture-1.0-py3-none-any.whl', 数据, 'jkoros-fixture', '1.0')
        except ValueError:
            pass
        else:
            raise AssertionError('지원하지 않는 wheel을 받아들였습니다.')
    print('PASS: wheel 路径·大小·C 扩展名值·依赖项列 拒绝值')


def 空端口编号():
    with socket.socket() as 套接字值:
        套接字值.bind(('127.0.0.1', 0))
        return 套接字值.getsockname()[1]


def 运行():
    解析器 = argparse.ArgumentParser(description=__doc__)
    解析器.add_argument('--host-only', action='store_true')
    实参 = 解析器.parse_args()
    检查宿主()
    if 实参.host_only:
        return
    结果路径 = 项目根/'build/verification/pip'
    结果路径.mkdir(parents=True, exist_ok=True)
    存储装置路径 = 结果路径/'cache'
    存储装置路径.mkdir(exist_ok=True)
    # 实际数据 PyPI 分发值 文件. 시험용 wheel과 분리하고 PyPI SHA256도 기록한다.
    捆绑代码库(项目根/'build/pip-cache').准备('micropython-bisect==3.3.3')
    for 尾部值 in ('.archive', '.json'):
        shutil.copyfile(str(项目根/'build/pip-cache'/('micropython-bisect==3.3.3'+尾部值)), str(存储装置路径/('micropython-bisect==3.3.3'+尾部值)))
    硬件日志 = json.loads((存储装置路径/'micropython-bisect==3.3.3.json').read_text())
    assert 硬件日志['sha256'] == 'b8d09d0bb4b2add706078dfa3f306e22fad1f4b5340b87d13f2c852507d720c8'
    for 名称, 文件条目列 in (
            ('jkoros-fixture', {'검증꾸러미/__init__.py': 'from .计算结果 import 添加值列\n', '검증꾸러미/计算结果.py': 'def 添加值列(首位操作数,第二操作数):\n return 首位操作数+第二操作数\n'}),
            ('jkoros-space', {'space%d.py' % 数: '值=1\n' for 数 in range(4)}),
            ('jkoros-syntax', {'bad.py': 'def broken(:\n'})):
        数据 = 测试滚轮(名称, 文件条目列)
        (存储装置路径/(名称+'==1.0.archive')).write_bytes(数据)
        (存储装置路径/(名称+'==1.0.json')).write_text(json.dumps({'name': 名称, 'version': '1.0',
            'filename': 名称.replace('-', '_')+'-1.0-py3-none-any.whl', 'url': 'test-fixture-only', 'sha256': hashlib.sha256(数据).hexdigest()}))
    有效性校验 = {'passed': False, 'kernel_sha256': hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),
            'external_package': 硬件日志, 'checks': []}
    端口编号 = 空端口编号()
    进程 = subprocess.Popen(['python3', str(项目根/'工具集/执行命令.py'), '--network', '--pip', '--pip-offline',
                '--pip-port', str(端口编号), '--pip-cache', str(存储装置路径), '--ftp-port', str(空端口编号())],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    选择器 = selectors.DefaultSelector()
    选择器.register(进程.stdout, selectors.EVENT_READ)
    执行记录 = bytearray()
    def 等待(显示值=b'jkoros-native> '):
        内容值 = bytearray()
        结尾 = time.monotonic()+120
        while 显示值 not in 内容值:
            if time.monotonic() > 结尾 or 进程.poll() is not None:
                raise AssertionError('게스트 回复 缺失方法: '+内容值.decode('utf-8','replace'))
            for 条目值, _ in 选择器.select(.1):
                片段值 = 条目值.fileobj.read(4096)
                内容值.extend(片段值)
                执行记录.extend(片段值)
        return 内容值.decode('utf-8', 'replace').replace('\r\n','\n')
    def 命令壳(命令, 显示值=b'jkoros-native> '):
        进程.stdin.write(命令.encode()+b'\n')
        进程.stdin.flush()
        return 等待(显示值)
    def 执行命令(命令, 预期值列, 状态值=0):
        内容值 = 命令壳(命令)
        assert 预期值列 in 内容值 and '\nexit '+str(状态值)+'\n' in 内容值, 内容值
        有效性校验['checks'].append(命令)
        return 内容值
    def 上传文件集(名称, 数据):
        命令壳('load '+名称, b'hex> ')
        for 位置索引 in range(0, len(数据), 64):
            命令壳(数据[位置索引:位置索引+64].hex(), b'hex> ')
        assert 'LOADED' in 命令壳('.')
    try:
        等待()
        执行命令('pip --help', 'MicroPython 源代码树 설치기')
        上传文件集('오류시험.py', (项目根/'测试/Python/韩语错误测试.py').read_bytes())
        执行命令('python 오류시험.py', '中文 文件 异常 验证')
        执行命令('pip install micropython-bisect==3.3.3 --port '+str(端口编号), '安装值 是否完成: micropython-bisect 3.3.3')
        执行命令('python -c \'from bisect import insort as 순서대로넣기; 值=[1,5]; 순서대로넣기(值,3); print(值)\'', '[1, 3, 5]')
        执行命令('python -m pip list', 'micropython-bisect 3.3.3')
        执行命令('pip install micropython-bisect==3.3.3 --port '+str(端口编号), '이미 설치됨:')
        执行命令('pip install jkoros-fixture==1.0 --port '+str(端口编号), '安装值 是否完成: jkoros-fixture')
        执行命令('python -c \'from 검증꾸러미 import 添加值列; print(添加值列(20,22))\'', '\n42\n')
        执行命令('pip install jkoros-syntax==1.0 --port '+str(端口编号), '软件包 错误:', 1)
        执行命令('python -c \'import jkoros; assert jkoros.path_kind("/lib/bad.py")==0; print("구문 错误 보존")\'', '구문 错误 보존')
        上传文件集('공간시험.py', (项目根/'测试/Python/捆绑命名空间测试.py').read_bytes())
        执行命令('python 공간시험.py '+str(端口编号), '软件包 地址区域 부족 发回桥接 验证')
        执行命令('pip uninstall jkoros-fixture', '移除条目 是否完成: jkoros-fixture')
        执行命令('pip uninstall micropython-bisect', '移除条目 是否完成: micropython-bisect')
        执行命令('python -c \'import jkoros; assert jkoros.path_kind("/lib/bisect.py")==0; print("移除条目 验证")\'', '移除条目 验证')
        有效性校验['passed'] = True
        print('PASS: PyPI 物理硬件 安装值·import·执行命令, 中文 异常, 패키지 目录值, 失败值 发回桥接, pip list/uninstall')
    finally:
        try:
            # mon:stdio의 退出程序 키로 QEMU를 끝내면 실행기의 中继值 문맥도 정리된다.
            进程.stdin.write(b'\x01x')
            进程.stdin.flush()
            进程.wait(timeout=8)
        except (subprocess.TimeoutExpired, BrokenPipeError):
            进程.terminate()
            try:
                进程.wait(timeout=8)
            except subprocess.TimeoutExpired:
                进程.kill()
                进程.wait()
        if 进程.poll() is None:
            进程.kill()
            进程.wait()
        选择器.close()
        进程.stdin.close()
        进程.stdout.close()
        (结果路径/'serial.log').write_bytes(执行记录)
        (结果路径/'report.json').write_text(json.dumps(有效性校验, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__':
    运行()
