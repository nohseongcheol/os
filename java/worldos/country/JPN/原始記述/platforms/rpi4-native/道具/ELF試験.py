#!/usr/bin/env python3
"""Compare one unmodified, extensionless Linux AArch64 ELF on both ABIs."""
import hashlib
import json
import struct
import subprocess
from 命令実行 import 計画根


def Linux例(結果データ):
    結果データ.mkdir(parents=True, exist_ok=True)
    for 原本データ, 名前 in [('起動処理.S', 'start.o'), ('挨拶例.c', 'hello.o')]:
        subprocess.check_call(['clang', '--target=aarch64-linux-gnu', '-mcpu=cortex-a72',
            '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-pic',
            '-fno-unwind-tables', '-fno-asynchronous-unwind-tables', '-O2',
            '-c', str(計画根/'用例/LinuxABI'/原本データ), '-o', str(結果データ/名前)])
    実行形式イメージ = 結果データ/'리눅스인사'
    subprocess.check_call(['aarch64-linux-gnu-ld', '-static', '-z', 'max-page-size=4096',
        '-Ttext-segment=0x02000000', '-s', '-o', str(実行形式イメージ), str(結果データ/'start.o'), str(結果データ/'hello.o')])
    内容物値 = 実行形式イメージ.read_bytes()
    assert len(内容物値) <= 16384 and 内容物値[:7] == b'\x7fELF\x02\x01\x01'
    assert struct.unpack_from('<HH', 内容物値, 16) == (2, 183) and b'JKOROS\0' not in 内容物値
    期待 = 'LINUX ARM64 ELF PASS\n한글인수\n'
    比較状態基準線 = subprocess.check_output(['qemu-aarch64', str(実行形式イメージ), '한글인수'], cwd=str(結果データ)).decode()
    assert 比較状態基準線 == 期待, 比較状態基準線
    (結果データ/'readelf.txt').write_bytes(subprocess.check_output(['readelf', '-hl', str(実行形式イメージ)]))
    return 実行形式イメージ, 期待


def 起動処理():
    結果データ = 計画根/'build/verification/elf'
    結果データ.mkdir(parents=True, exist_ok=True)
    (結果データ/'report.json').write_text('{"passed": false}\n')
    実行形式イメージ, 期待 = Linux例(結果データ)
    結果 = subprocess.check_output(['python3', str(計画根/'道具/ファイル実行.py'), '--linux', str(実行形式イメージ), '한글인수']).decode().replace('\r\n', '\n')
    assert 期待+'exit 0' in 結果, 結果
    (結果データ/'serial.log').write_text(結果)
    原本=実行形式イメージ.read_bytes()
    プログラムヘッダー変位量=struct.unpack_from('<Q',原本,32)[0]
    for 名前,変位量値,書式指定,値 in [('wrong-cpu',18,'H',62),('pie',16,'H',3),
            ('write-execute',プログラムヘッダー変位量+4,'I',7),('kernel-address',プログラムヘッダー変位量+16,'Q',0x400000)]:
        無効データ=bytearray(原本);struct.pack_into('<'+書式指定,無効データ,変位量値,値)
        経路=結果データ/名前;経路.write_bytes(無効データ)
        却下状態結果=subprocess.run(['python3',str(計画根/'道具/ファイル実行.py'),'--linux',str(経路)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        assert 却下状態結果.returncode==1 and b'exit -8' in 却下状態結果.stdout,(名前,却下状態結果.stdout)
    妥当性報告 = {'passed': True, 'linux_kernel_loaded': False,
        'kernel_sha256': hashlib.sha256((計画根/'build/kernel8.img').read_bytes()).hexdigest(),
        'executable_sha256': hashlib.sha256(実行形式イメージ.read_bytes()).hexdigest(),
        'checks': ['extensionless ELF64 ET_EXEC EM_AARCH64 without JKOROS note',
                   'identical bytes execute in qemu-aarch64 Linux user mode and own raspi4b kernel',
                   'Linux argc/argv stack, openat/write/lseek/read/close/clock_gettime/exit',
                   'Linux syscall 6 is not dispatched to native exit; invalid kernel pointer rejected',
                   'wrong CPU, PIE, writable executable pages and kernel load address rejected in Linux ABI mode'],
        'full_linux_binary_compatibility': False}
    (結果データ/'report.json').write_text(json.dumps(妥当性報告, ensure_ascii=False, indent=2)+'\n')
    print('PASS same extensionless Linux ARM64 ELF on Linux syscall ABI and own kernel')


if __name__ == '__main__': 起動処理()
