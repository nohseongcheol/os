#!/usr/bin/env python3
"""实际数据 ring 3 ELF/宿主 UDP 왕복/保护值 错误/时间值 限制值/잘못된 ELF를 검증한다."""
import json
import hashlib
from pathlib import Path
import select
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time

位置 = Path(__file__).resolve().parents[1]


class 虚拟机:
    def __init__(self, 路径, 种类值='elf', 网络值=True, 存储装置中型=None):
        self.临时值 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        目录值 = Path(self.临时值.name)
        self.日志记录 = bytearray()
        self.串行值 = socket.socket(socket.AF_UNIX)
        self.监视器值 = socket.socket(socket.AF_UNIX)
        串行路径, 监视器路径 = 目录值 / 'serial.sock', 目录值 / 'monitor.sock'
        命令 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(串行路径) + ',server,nowait',
                '-monitor', 'unix:' + str(监视器路径) + ',server,nowait']
        命令 += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if 网络值 else ['-net', 'none']
        命令 += ['-kernel', str(路径)] if 种类值 == 'elf' else ['-cdrom', str(路径), '-boot', 'd']
        if 存储装置中型 is not None:
            命令 += ['-drive', 'file=' + str(存储装置中型) + ',format=raw,if=ide,index=0']
        self.进程值 = subprocess.Popen(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            结尾 = time.monotonic() + 10
            while not (串行路径.exists() and 监视器路径.exists()):
                if self.进程值.poll() is not None:
                    raise AssertionError(self.进程值.stderr.read().decode())
                if time.monotonic() > 结尾: raise AssertionError('QEMU 运行 时间值 초과')
                time.sleep(0.03)
            self.串行值.connect(str(串行路径))
            self.监视器值.connect(str(监视器路径))
            self.串行值.setblocking(False)
            self.监视器值.sendall(b'cont\n')
            self.等待状态状态('jkoros> ')
        except BaseException:
            self.关闭()
            raise

    def 等待状态状态(self, 短语值, 运行=0, 限制值=15):
        结尾 = time.monotonic() + 限制值
        while time.monotonic() < 结尾:
            if 短语值.encode() in self.日志记录[运行:]:
                return self.日志记录[运行:].decode('utf-8', 'replace')
            读取, _, _ = select.select([self.串行值], [], [], 0.1)
            if 读取:
                数据 = self.串行值.recv(65536)
                if not 数据: break
                self.日志记录.extend(数据)
            if self.进程值.poll() is not None: break
        raise AssertionError('等待状态值 失败值: ' + 短语值 + '\n' + self.日志记录.decode('utf-8', 'replace'))

    def 命令(self, 字符串, 期望状态):
        运行 = len(self.日志记录)
        self.串行值.sendall((字符串 + '\n').encode())
        结果 = self.等待状态状态('jkoros> ', 运行)
        for 短语值 in 期望状态:
            assert 短语值 in 结果, (字符串, 短语值, 结果)
        assert 'PANIC' not in 结果, 结果
        return 结果

    def 关闭(self):
        self.串行值.close()
        self.监视器值.close()
        if self.进程值.poll() is None:
            self.进程值.terminate()
            try: self.进程值.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.进程值.kill()
                self.进程值.wait()
        self.进程值.communicate()
        self.临时值.cleanup()


def 已保护内核(目录值):
    分支项集列表 = {
        'badmem': 'movl $7, 0x00100000',
        'badport': 'movw $0x3f8, %dx\noutb %al, %dx',
        'spin': '1: jmp 1b',
        'badptr': 'movl $1,%eax\nmovl $0x00100000,%ebx\nint $0x80\ncmpl $-14,%eax\njne fail\n'
                  'movl $999,%eax\nint $0x80\ncmpl $-38,%eax\njne fail\n'
                  'xorl %ebx,%ebx\nxorl %eax,%eax\nint $0x80\nfail: movl $1,%ebx\nxorl %eax,%eax\nint $0x80',
        'fault': 'ud2',
        'badfile': '''
            movl $20,%eax
            movl $0x00100000,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $20,%eax
            movl $name,%ebx
            movl $0x00100000,%ecx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $negative,%ecx
            xorl %edx,%edx
            int $0x80
            cmpl $-14,%eax
            jne fail
            movl $21,%eax
            movl $name,%ebx
            movl $empty,%ecx
            movl $1,%edx
            int $0x80
            cmpl $-22,%eax
            jne fail
            movl $20,%eax
            movl $empty,%ebx
            movl $empty,%ecx
            int $0x80
            cmpl $-22,%eax
            jne fail
            xorl %eax,%eax
            xorl %ebx,%ebx
            int $0x80
        fail:
            xorl %eax,%eax
            movl $1,%ebx
            int $0x80
        .balign 4
        name: .long 1,88
        empty: .long 0
        negative: .long -1
        ''',
    }
    条目列列表 = ['hello=' + str(位置 / 'build/apps/hello.elf')]
    for 名称, 内容值 in 分支项集列表.items():
        源代码 = 目录值 / (名称 + '.s')
        源代码.write_text('.code32\n.text\n.globl _start\n_start:\n' + 内容值 +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(目录值 / (名称 + '.o')), str(源代码)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置.parent / 'compiler/用户连接导航.ld'),
                        '-o', str(目录值 / (名称 + '.elf')), str(目录值 / (名称 + '.o'))], check=True)
        条目列列表.append(名称 + '=' + str(目录值 / (名称 + '.elf')))
    是否常规 = bytearray((位置 / 'build/apps/hello.elf').read_bytes())
    变体列列表 = {}
    无效结果 = bytearray(是否常规); 无效结果[0] = 0; 变体列列表['badelf'] = 无效结果
    无效结果 = bytearray(是否常规); struct.pack_into('<I', 无效结果, 24, 0x00100000); 变体列列表['badentry'] = 无效结果
    无效结果 = bytearray(是否常规); struct.pack_into('<I', 无效结果, 28, 0x7fffffff); 变体列列表['badtable'] = 无效结果
    无效结果 = bytearray(是否常规); 表 = struct.unpack_from('<I', 无效结果, 28)[0]
    struct.pack_into('<I', 无效结果, 表 + 20, 0x7fffffff); 变体列列表['badsize'] = 无效结果
    for 名称, 数据 in 变体列列表.items():
        文件 = 目录值 / (名称 + '.elf'); 文件.write_bytes(数据)
        条目列列表.append(名称 + '=' + str(文件))
    subprocess.run([sys.executable, str(位置 / '工具集/可执行束打包.py'), '-o', str(目录值 / 'apps.bin')] + 条目列列表, check=True)
    源代码 = 目录值 / 'apps.s'
    源代码.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(目录值 / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(目录值 / 'apps.o'), str(源代码)], check=True)
    内核值 = 目录值 / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置 / '启动/链接布局.ld'), '-o', str(内核值),
                    str(位置 / 'build/boot.o'), str(位置 / 'build/java.o'), str(位置 / 'build/user.o'), str(目录值 / 'apps.o')], check=True)
    return 内核值


def 执行命令():
    结果 = {}
    服务器值 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    服务器值.bind(('127.0.0.1', 0))
    服务器值.settimeout(0.1)
    端口值 = 服务器值.getsockname()[1]
    已接收项目 = []
    退出程序 = threading.Event()
    def 回显回复():
        while not 退出程序.is_set():
            try: 数据, 对端值 = 服务器值.recvfrom(4096)
            except socket.timeout: continue
            已接收项目.append(数据)
            if 数据 != b'drop-me': 服务器值.sendto(数据, 对端值)
    后台任务值 = threading.Thread(target=回显回复, daemon=True)
    后台任务值.start()
    try:
        for 种类值 in ('elf', 'iso'):
            计算机 = 虚拟机(位置 / ('build/kernel.elf' if 种类值 == 'elf' else 'build/kernel.iso'), 种类值)
            try:
                计算机.命令('apps', ['hello', 'udp', 'netcheck', 'stress'])
                计算机.命令('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                计算机.命令('run missing', ['Exit: -2'])
                计算机.命令('net', ['NET RTL8139'])
                计算机.命令('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for 内容值 in ('hello-network', 'odd', 'even', 'repeat-123'):
                    计算机.命令('run udp 10.0.2.2 {} {}'.format(端口值, 内容值), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert 内容值.encode() in 已接收项目, '宿主 서버에서 자료를 받지 못함'
                计算机.命令('run stress {}'.format(端口值), ['UDP STRESS PASS', 'Exit: 0'])
                计算机.命令('run udp 10.0.2.2 {} drop-me'.format(端口值), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                计算机.命令('run hello recovered', ['arg: recovered', 'Exit: 0'])
                结果[种类值] = 计算机.日志记录.decode('utf-8', 'replace')
                print('PASS: {} 用户 ELF/ring 3/实参/UDP 宿主 왕복/时间值 초과/命令壳 복귀'.format(种类值), flush=True)
            finally:
                try: 计算机.命令('net', [])
                except Exception: pass
                (位置 / 'build/사용자통신-last.log').write_bytes(计算机.日志记录)
                计算机.关闭()
        计算机 = 虚拟机(位置 / 'build/kernel.elf', 网络值=False)
        try:
            计算机.命令('net', ['NET unavailable'])
            计算机.命令('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            计算机.命令('run hello', ['USER MODE ring 3', 'Exit: 0'])
            结果['no_nic'] = 计算机.日志记录.decode()
        finally: 计算机.关闭()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 临时值:
            计算机 = 虚拟机(已保护内核(Path(临时值)), 网络值=False)
            try:
                for 名称, 状态值 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    计算机.命令('run ' + 名称, ['Exit: ' + str(状态值)])
                    计算机.命令('run hello', ['USER MODE ring 3', 'Exit: 0'])
                结果['protection'] = 计算机.日志记录.decode()
                print('PASS: 用户 内存数据/硬件端口 격리, 잘못된 指针/ELF, CPU 异常, 무한 迭代值 限制值', flush=True)
            finally:
                (位置 / 'build/保护测试-last.log').write_bytes(计算机.日志记录)
                计算机.关闭()
    finally:
        退出程序.set()
        后台任务值.join(timeout=2)
        服务器值.close()
    结果['host_udp_received'] = [{'length': len(数据), 'sha256': hashlib.sha256(数据).hexdigest()} for 数据 in 已接收项目]
    (位置 / 'build/测试用户网络.json').write_text(json.dumps(结果, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    执行命令()
