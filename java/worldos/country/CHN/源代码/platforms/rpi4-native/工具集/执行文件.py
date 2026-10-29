#!/usr/bin/env python3
"""별도 QEMU에 파일을 업로드하고 Java/Python/ELF를 실행한다. 宿主 실행으로 대체하지 않는다."""
import argparse
from pathlib import Path
import re
import selectors
import shlex
import subprocess
import sys
import time
from 执行命令 import 命令


def 运行():
    参数解析器 = argparse.ArgumentParser(description=__doc__)
    参数解析器.add_argument('file', type=Path)
    参数解析器.add_argument('arguments', nargs='*')
    参数解析器.add_argument('--class-name', help='패키지가 있는 .class의 전체 名称(예: 有效性校验.测试捆绑)')
    参数解析器.add_argument('--linux', action='store_true', help='ELF 입력에 제한된 Linux ARM64 시스템 调用 ABI 使用值')
    参数解析器.add_argument('--vnc', help='예: 127.0.0.1:2')
    参数解析器.add_argument('--include', action='append', type=Path, default=[], help='追加条目 class 文件 또는 class 디렉터리(패키지 名称 保持值)')
    参数数组 = 参数解析器.parse_args()
    数据 = 参数数组.file.read_bytes()
    if 参数数组.class_name and 参数数组.file.suffix != '.class': 参数解析器.error('--class-name은 .class 입력에서 사용합니다.')
    名称 = 参数数组.class_name + '.class' if 参数数组.class_name else 参数数组.file.name
    if len(数据) > 16384 or not 1 <= len(名称.encode('utf-8')) <= 63 or '\n' in 名称 or '\r' in 名称:
        参数解析器.error('파일은 16384바이트, 이름은 UTF-8 63바이트 이하여야 합니다.')
    分类值 = '.elf' if 数据[:4] == b'\x7fELF' else 参数数组.file.suffix
    if 参数数组.linux and 分类值 != '.elf': 参数解析器.error('--linux는 ELF 바이너리에만 사용합니다.')
    if 分类值 not in ('.java', '.class', '.jar', '.c', '.py', '.elf'):
        参数解析器.error('.java / .class / .jar / .c / .py / .elf 파일을 지정하세요.')
    if len(参数数组.arguments) > 7 or any(len(字符串数据.encode('utf-8')) > 255 or '\n' in 字符串数据 or '\r' in 字符串数据 for 字符串数据 in 参数数组.arguments):
        参数解析器.error('인수는 最大值 7개, 각각 UTF-8 255바이트 이하입니다.')
    选择项集 = ['-display', 'none', '-serial', 'stdio', '-monitor', 'none']
    if 参数数组.vnc: 选择项集 += ['-vnc', 参数数组.vnc]
    进程 = subprocess.Popen(命令() + 选择项集, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    就绪选择器 = selectors.DefaultSelector(); 就绪选择器.register(进程.stdout, selectors.EVENT_READ)
    def 接收消息(标记, 执行状态超时=45):
        输出结果 = bytearray(); 结束偏移 = time.monotonic() + 执行状态超时
        while 标记 not in 输出结果:
            if time.monotonic() > 结束偏移: raise RuntimeError('UART timeout: ' + 输出结果.decode('utf-8', 'replace'))
            for 已按下值, _ in 就绪选择器.select(0.1):
                片段值 = 已按下值.fileobj.read(4096)
                if 片段值: 输出结果.extend(片段值)
            if b'PANIC:' in 输出结果 or b'FAIL ' in 输出结果: raise RuntimeError(输出结果.decode('utf-8', 'replace'))
            if 进程.poll() is not None: raise RuntimeError('QEMU exited: ' + 输出结果.decode('utf-8', 'replace'))
        return bytes(输出结果)
    def 发送(行, 标记=b'jkoros-native> '):
        进程.stdin.write(行.encode('utf-8') + b'\n'); 进程.stdin.flush()
        return 接收消息(标记)
    def 执行命令(行):
        输出结果 = 发送(行); sys.stdout.buffer.write(输出结果); sys.stdout.buffer.flush()
        是否相等 = re.search(rb'(?:^|\n)exit (-?\d+)\r?\n', 输出结果)
        if not 是否相等: raise RuntimeError('guest did not report exit status')
        return int(是否相等.group(1))
    try:
        接收消息(b'jkoros-native> ')
        文件列表 = []
        for 包含条目 in 参数数组.include:
            if 包含条目.is_dir():
                文件列表 += [(str(数据位置.relative_to(包含条目).with_suffix('')).replace('/', '.') + '.class', 数据位置.read_bytes()) for 数据位置 in sorted(包含条目.rglob('*.class'))]
            else:
                文件列表.append((包含条目.name, 包含条目.read_bytes()))
        文件列表 = [(项目个数, 目的地址数据) for 项目个数, 目的地址数据 in 文件列表 if 项目个数 != 名称] + [(名称, 数据)]
        for 上传名称, 上传数据 in 文件列表:
            if len(上传数据) > 16384 or len(上传名称.encode('utf-8')) > 63 or '\n' in 上传名称 or '\r' in 上传名称:
                raise ValueError('追加条目 파일의 名称/大小 限制值 초과: ' + 上传名称)
            发送('load ' + shlex.quote(上传名称), b'hex> ')
            for 序数索引 in range(0, len(上传数据), 64): 发送(上传数据[序数索引:序数索引+64].hex(), b'hex> ')
            if b'LOADED' not in 发送('.'): raise RuntimeError('upload failed: ' + 上传名称)
            已转储 = 发送('hex ' + shlex.quote(上传名称))
            是否相等 = re.search(rb'HEX BEGIN (\d+)\r?\n(.*?)HEX END', 已转储, re.S)
            if not 是否相等 or bytes.fromhex(''.join(是否相等.group(2).decode().split())) != 上传数据: raise RuntimeError('upload verification failed')
        if 分类值 == '.java' and 执行命令('javac ' + shlex.quote(名称)) != 0: return 1
        可执行文件映像 = 参数数组.file.stem + '.elf'
        if 分类值 == '.c' and 执行命令('cc ' + shlex.quote(名称) + ' -o ' + shlex.quote(可执行文件映像)) != 0: return 1
        执行条目 = 'java ' + shlex.quote(参数数组.class_name or 参数数组.file.stem) if 分类值 in ('.java', '.class') else ('python ' if 分类值 == '.py' else 'run ') + shlex.quote(名称)
        if 分类值 == '.jar': 执行条目 = 'java -jar ' + shlex.quote(名称)
        if 分类值 == '.c': 执行条目 = 'run ' + shlex.quote(可执行文件映像)
        if 参数数组.linux: 执行条目 = 'run --linux ' + shlex.quote(名称)
        if 参数数组.arguments: 执行条目 += ' ' + ' '.join(shlex.quote(字符串数据) for 字符串数据 in 参数数组.arguments)
        return 0 if 执行命令(执行条目) == 0 else 1
    finally:
        if 进程.poll() is None:
            进程.terminate()
            try: 进程.wait(timeout=5)
            except subprocess.TimeoutExpired: 进程.kill(); 进程.wait(timeout=5)
        就绪选择器.close(); 进程.stdin.close(); 进程.stdout.close()


if __name__ == '__main__':
    raise SystemExit(运行())
