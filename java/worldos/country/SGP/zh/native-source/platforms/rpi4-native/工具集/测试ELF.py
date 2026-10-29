#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from 执行命令 import 项目根


def Linux示例(结果数据):
    结果数据.mkdir(parents=True, exist_ok=True)
    for 原始数据, 名称 in [('运行.S', 'start.o'), ('问候例.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(项目根/'用例/LinuxABI'/原始数据), '-o', str(结果数据/名称)])
    可执行文件映像 = 结果数据/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(可执行文件映像), str(结果数据/'start.o'), str(结果数据/'hello.o')])
    内容值 = 可执行文件映像.read_bytes()
    assert len(内容值) <= 16384 and 内容值[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', 内容值, 16) == (2, 183) and b'JKOROS\0' not in 内容值
    预期 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    比较基线 = subprocess.check_output(['qemu-aarch64', str(可执行文件映像), '한글인수'], cwd=str(结果数据)).decode()
    assert 比较基线 == 预期, 比较基线
    (结果数据/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(可执行文件映像)]))
    return 可执行文件映像, 预期


def 运行():
    结果数据 = 项目根/'build/verification/elf'
    结果数据.mkdir(parents=True, exist_ok=True)
    (结果数据/'report.json').write_text('{"passed": false}\n')
    可执行文件映像, 预期 = Linux示例(结果数据)
    结果 = subprocess.check_output(['python3', str(项目根/'工具集/执行文件.py'), '--linux', str(可执行文件映像), '한글인수']).decode().replace('\r\n', '\n')
    assert 预期+'exit 0' in 结果, 结果
    (结果数据/'serial.log').write_text(结果)
    原始=可执行文件映像.read_bytes()
    程序头部偏移=struct.unpack_from('<Q',原始,32)[0]
    for 名称,偏移值,格式指定,值 in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',程序头部偏移+4,'I',7),('kernel-address',程序头部偏移+16,'Q',0x400000)]:
        无效数据=bytearray(原始);struct.pack_into('<'+格式指定,无效数据,偏移值,值)
        路径=结果数据/名称;路径.write_bytes(无效数据)
        拒绝状态结果=subprocess.run(['python3',str(项目根/'工具集/执行文件.py'),'--linux',str(路径)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 拒绝状态结果.returncode==1 and b'exit -8' in 拒绝状态结果.stdout,(名称,拒绝状态结果.stdout)
    有效性验证报告 = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((项目根/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(可执行文件映像.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (结果数据/'report.json').write_text(json.dumps(有效性验证报告, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': 运行()
