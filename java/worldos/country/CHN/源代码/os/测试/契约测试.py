#!/usr/bin/env python3
"""宿主 libc 없이 연결한 中文 C 프로그램을 实际数据 ring 3에서 실행한다."""
import json
from pathlib import Path
import socket
import threading
from 测试用户网络 import 虚拟机

位置 = Path(__file__).resolve().parents[1]

def 执行命令():
    结果 = {}
    服务器值 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    服务器值.bind(('127.0.0.1', 0))
    服务器值.settimeout(0.1)
    端口编号 = 服务器值.getsockname()[1]
    已接收数据 = []
    终止状态状态 = threading.Event()
    def 回显回复():
        while not 终止状态状态.is_set():
            try:
                数据, 地址 = 服务器值.recvfrom(4096)
            except socket.timeout:
                continue
            已接收数据.append(数据)
            服务器值.sendto(数据, 地址)
    后台任务值 = threading.Thread(target=回显回复, daemon=True)
    后台任务值.start()
    try:
        for 种类值 in ('elf', 'iso'):
            计算机 = 虚拟机(位置 / ('build/kernel.' + 种类值), 种类值)
            try:
                for 迭代值 in range(2):
                    计算机.命令('run posixcheck check', ['POSIX FILE CHECK PASS', 'Korean identifiers and C ABI PASS', 'Exit: 0'])
                    计算机.命令('run posixudp ' + str(端口编号), ['POSIX UDP CHECK PASS', 'Exit: 0'])
                运行 = len(计算机.日志记录)
                计算机.串行值.sendall(b'run posixinput\n')
                计算机.等待状态状态('POSIX INPUT READY', 运行)
                计算机.串行值.sendall(b'abcdef')
                输出 = 计算机.等待状态状态('jkoros> ', 运行)
                assert 'POSIX INPUT PASS' in 输出 and 'Exit: 0' in 输出, 输出
                计算机.命令('javac Hello.java', ['Exit: 0'])
                计算机.命令('java Hello', ['Hello from jkoros JVM!', '55', 'Exit: 0'])
                计算机.命令('run hello recovered', ['arg: recovered', 'Exit: 0'])
                结果[种类值] = 计算机.日志记录.decode('utf-8', 'replace')
                print('PASS:', 种类值, 'POSIX 文件/공유 位置/삭제 수명/地址 保护值/UDP/표준 输入值/기존 Java', flush=True)
            finally:
                计算机.关闭()
        assert b'posix-udp' in 已接收数据 and b'truncate' in 已接收数据 and b'' in 已接收数据
    finally:
        终止状态状态.set(); 后台任务值.join(timeout=2); 服务器值.close()
    结果['host_datagrams'] = [数据.decode() for 数据 in 已接收数据]
    (位置 / 'build/契约测试.json').write_text(json.dumps(结果, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    执行命令()
