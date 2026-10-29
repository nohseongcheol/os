#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from 執行命令 import 項目根


def Linux範例(結果資料):
    結果資料.mkdir(parents=True, exist_ok=True)
    for 原始資料, 名稱 in [('運行.S', 'start.o'), ('問候例.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(項目根/'範例/LinuxABI'/原始資料), '-o', str(結果資料/名稱)])
    可執行文件映像 = 結果資料/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(可執行文件映像), str(結果資料/'start.o'), str(結果資料/'hello.o')])
    內容值 = 可執行文件映像.read_bytes()
    assert len(內容值) <= 16384 and 內容值[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', 內容值, 16) == (2, 183) and b'JKOROS\0' not in 內容值
    預期 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    比較基線 = subprocess.check_output(['qemu-aarch64', str(可執行文件映像), '한글인수'], cwd=str(結果資料)).decode()
    assert 比較基線 == 預期, 比較基線
    (結果資料/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(可執行文件映像)]))
    return 可執行文件映像, 預期


def 運行():
    結果資料 = 項目根/'build/verification/elf'
    結果資料.mkdir(parents=True, exist_ok=True)
    (結果資料/'report.json').write_text('{"passed": false}\n')
    可執行文件映像, 預期 = Linux範例(結果資料)
    結果 = subprocess.check_output(['python3', str(項目根/'工具集/執行檔案.py'), '--linux', str(可執行文件映像), '한글인수']).decode().replace('\r\n', '\n')
    assert 預期+'exit 0' in 結果, 結果
    (結果資料/'serial.log').write_text(結果)
    原始=可執行文件映像.read_bytes()
    程式標頭偏移=struct.unpack_from('<Q',原始,32)[0]
    for 名稱,偏移值,格式指定,值 in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',程式標頭偏移+4,'I',7),('kernel-address',程式標頭偏移+16,'Q',0x400000)]:
        無效資料=bytearray(原始);struct.pack_into('<'+格式指定,無效資料,偏移值,值)
        路徑=結果資料/名稱;路徑.write_bytes(無效資料)
        拒絕狀態結果=subprocess.run(['python3',str(項目根/'工具集/執行檔案.py'),'--linux',str(路徑)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 拒絕狀態結果.returncode==1 and b'exit -8' in 拒絕狀態結果.stdout,(名稱,拒絕狀態結果.stdout)
    有效性驗證報告 = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((項目根/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(可執行文件映像.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (結果資料/'report.json').write_text(json.dumps(有效性驗證報告, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': 運行()
