#!/usr/bin/env python3
"""독립 QEMU를 디스크 없이 실행해 ELF/GRUB ISO 및 串行值/PS2 입력을 검증한다."""
import json
from pathlib import Path
import select
import socket
import subprocess
import tempfile
import time

位置 = Path(__file__).resolve().parents[1]


def 等待(检查项, 说明, 限制值=15):
    结尾 = time.monotonic() + 限制值
    while time.monotonic() < 结尾:
        结果 = 检查项()
        if 结果:
            return 结果
        time.sleep(0.05)
    raise AssertionError('时间值 초과: ' + 说明)


def 测试(种类值):
    with tempfile.TemporaryDirectory(prefix='jkoros-boot-test-') as 临时值:
        临时值 = Path(临时值)
        串行路径 = 临时值 / 'serial.sock'
        监视器路径 = 临时值 / 'monitor.sock'
        命令 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot',
                '-serial', 'unix:' + str(串行路径) + ',server,nowait',
                '-monitor', 'unix:' + str(监视器路径) + ',server,nowait']
        命令 += ['-kernel', str(位置 / 'build/kernel.elf')] if 种类值 == 'elf' else [
            '-cdrom', str(位置 / 'build/kernel.iso'), '-boot', 'd']
        # 串行值 클라이언트가 연결되기 전에 출력이 유실되지 않도록 CPU를 일시 정지한다.
        命令 += ['-S']
        进程值 = subprocess.Popen(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        串行值 = socket.socket(socket.AF_UNIX)
        监视器值 = socket.socket(socket.AF_UNIX)
        日志记录 = bytearray()
        try:
            def 准备套接字():
                if 进程值.poll() is not None:
                    raise AssertionError(进程值.stderr.read().decode('utf-8', 'replace'))
                return 串行路径.exists() and 监视器路径.exists()
            等待(准备套接字, 'QEMU 套接字值')
            串行值.connect(str(串行路径))
            监视器值.connect(str(监视器路径))
            串行值.setblocking(False)
            监视器值.sendall(b'cont\n')

            def 头文件(字符串, 运行=0):
                读取, _, _ = select.select([串行值], [], [], 0.1)
                if 读取:
                    数据 = 串行值.recv(65536)
                    if not 数据:
                        raise AssertionError('串行值 连接 退出程序')
                    日志记录.extend(数据)
                if 进程值.poll() is not None:
                    raise AssertionError('QEMU 비정상 退出程序: ' + str(进程值.returncode))
                return 字符串.encode('utf-8') in 日志记录[运行:]

            def 测试命令列(输入值, 期望状态):
                运行 = len(日志记录)
                串行值.sendall(输入值.encode('ascii'))
                等待(lambda: 头文件(期望状态, 运行), 期望状态)
                等待(lambda: 头文件('jkoros> ', 运行), '命令 之后状态 프롬프트')

            等待(lambda: 头文件('READY'), 种类值 + ' 启动')
            assert b'JAVA SELFTEST PASS' in 日志记录
            assert 'Java 기계어 内核值 运行'.encode() in 日志记录
            测试命令列('info\r\n', 'embedded subset JVM / polling kernel')
            测试命令列('help\n', 'free N | echo TEXT')
            测试命令列('mem\n', ' / 8 (각 4096바이트)')
            测试命令列('echo natix\bve\n', 'native\r\n')
            for 编号 in range(8):
                测试命令列('alloc\n', '区段值 编号: ' + str(编号))
            测试命令列('alloc\n', '区段值 编号: -1')
            测试命令列('free 3\n', '반환됨')
            测试命令列('free 3\n', '할당되지 않은 区段值')
            测试命令列('free 99\n', '사용법: free 0..7')
            测试命令列('alloc\n', '区段值 编号: 3')
            测试命令列('free 0\n', '반환됨')
            测试命令列('test\n', 'JAVA SELFTEST PASS')
            测试命令列('unknown\n', '알 数 없는 명령입니다')
            测试命令列('clear\n', 'jkoros> ')

            # GUI 자판과 동일한 PS/2 장치를 통해 명령을 주입한다.
            运行 = len(日志记录)
            for 键值 in ('i', 'n', 'f', 'o', 'ret'):
                监视器值.sendall(('sendkey ' + 键值 + ' 30\n').encode())
                time.sleep(0.09)
            等待(lambda: 头文件('embedded subset JVM / polling kernel', 运行), 'PS/2 info 输入值')
            测试命令列('echo ' + 'a' * 150 + '\n', 'a' * 123)
            串行值.sendall(b'halt\n')
            等待(lambda: 头文件('HALTED'), '停机执行状态 命令')
            assert b'PANIC' not in 日志记录 and b'SELFTEST FAIL' not in 日志记录
            print('PASS: {} 启动, Java 内置 测试, 串行值 命令, PS/2 输入值, 分配存储装置/发回结果, 停机执行状态'.format(种类值))
            return 日志记录.decode('utf-8', 'replace')
        finally:
            串行值.close()
            监视器值.close()
            进程值.terminate()
            try:
                进程值.wait(timeout=3)
            except subprocess.TimeoutExpired:
                进程值.kill()
                进程值.wait()


if __name__ == '__main__':
    结果 = {种类值: 测试(种类值) for 种类值 in ('elf', 'iso')}
    (位置 / 'build/启动测试.json').write_text(json.dumps(结果, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
