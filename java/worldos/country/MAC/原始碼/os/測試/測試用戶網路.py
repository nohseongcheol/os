#!/usr/bin/env python3
"""實際資料 ring 3 ELF/宿主 UDP 왕복/保護值 錯誤/時間值 限制值/잘못된 ELF를 검증한다."""
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


class 虛擬機器:
    def __init__(self, 路徑, 種類值='elf', 網路值=True, 存儲裝置中型=None):
        self.臨時值 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        目錄值 = Path(self.臨時值.name)
        self.日誌記錄 = bytearray()
        self.串行值 = socket.socket(socket.AF_UNIX)
        self.監視器值 = socket.socket(socket.AF_UNIX)
        串行路徑, 監視器路徑 = 目錄值 / 'serial.sock', 目錄值 / 'monitor.sock'
        命令 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(串行路徑) + ',server,nowait',
                '-monitor', 'unix:' + str(監視器路徑) + ',server,nowait']
        命令 += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if 網路值 else ['-net', 'none']
        命令 += ['-kernel', str(路徑)] if 種類值 == 'elf' else ['-cdrom', str(路徑), '-boot', 'd']
        if 存儲裝置中型 is not None:
            命令 += ['-drive', 'file=' + str(存儲裝置中型) + ',format=raw,if=ide,index=0']
        self.程序值 = subprocess.Popen(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            結尾 = time.monotonic() + 10
            while not (串行路徑.exists() and 監視器路徑.exists()):
                if self.程序值.poll() is not None:
                    raise AssertionError(self.程序值.stderr.read().decode())
                if time.monotonic() > 結尾: raise AssertionError('QEMU 運行 時間值 초과')
                time.sleep(0.03)
            self.串行值.connect(str(串行路徑))
            self.監視器值.connect(str(監視器路徑))
            self.串行值.setblocking(False)
            self.監視器值.sendall(b'cont\n')
            self.等待狀態狀態('jkoros> ')
        except BaseException:
            self.關閉()
            raise

    def 等待狀態狀態(self, 短語值, 運行=0, 限制值=15):
        結尾 = time.monotonic() + 限制值
        while time.monotonic() < 結尾:
            if 短語值.encode() in self.日誌記錄[運行:]:
                return self.日誌記錄[運行:].decode('utf-8', 'replace')
            讀取, _, _ = select.select([self.串行值], [], [], 0.1)
            if 讀取:
                資料 = self.串行值.recv(65536)
                if not 資料: break
                self.日誌記錄.extend(資料)
            if self.程序值.poll() is not None: break
        raise AssertionError('等待狀態值 失敗值: ' + 短語值 + '\n' + self.日誌記錄.decode('utf-8', 'replace'))

    def 命令(self, 字符串, 期望狀態):
        運行 = len(self.日誌記錄)
        self.串行值.sendall((字符串 + '\n').encode())
        結果 = self.等待狀態狀態('jkoros> ', 運行)
        for 短語值 in 期望狀態:
            assert 短語值 in 結果, (字符串, 短語值, 結果)
        assert 'PANIC' not in 結果, 結果
        return 結果

    def 關閉(self):
        self.串行值.close()
        self.監視器值.close()
        if self.程序值.poll() is None:
            self.程序值.terminate()
            try: self.程序值.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.程序值.kill()
                self.程序值.wait()
        self.程序值.communicate()
        self.臨時值.cleanup()


def 已保護內核(目錄值):
    分支項集列表 = {
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
    條目列列表 = ['hello=' + str(位置 / 'build/apps/hello.elf')]
    for 名稱, 內容值 in 分支項集列表.items():
        原始碼 = 目錄值 / (名稱 + '.s')
        原始碼.write_text('.code32\n.text\n.globl _start\n_start:\n' + 內容值 +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(目錄值 / (名稱 + '.o')), str(原始碼)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置.parent / 'compiler/用戶連接導航.ld'),
                        '-o', str(目錄值 / (名稱 + '.elf')), str(目錄值 / (名稱 + '.o'))], check=True)
        條目列列表.append(名稱 + '=' + str(目錄值 / (名稱 + '.elf')))
    是否常規 = bytearray((位置 / 'build/apps/hello.elf').read_bytes())
    變體列列表 = {}
    無效結果 = bytearray(是否常規); 無效結果[0] = 0; 變體列列表['badelf'] = 無效結果
    無效結果 = bytearray(是否常規); struct.pack_into('<I', 無效結果, 24, 0x00100000); 變體列列表['badentry'] = 無效結果
    無效結果 = bytearray(是否常規); struct.pack_into('<I', 無效結果, 28, 0x7fffffff); 變體列列表['badtable'] = 無效結果
    無效結果 = bytearray(是否常規); 表 = struct.unpack_from('<I', 無效結果, 28)[0]
    struct.pack_into('<I', 無效結果, 表 + 20, 0x7fffffff); 變體列列表['badsize'] = 無效結果
    for 名稱, 資料 in 變體列列表.items():
        檔案 = 目錄值 / (名稱 + '.elf'); 檔案.write_bytes(資料)
        條目列列表.append(名稱 + '=' + str(檔案))
    subprocess.run([sys.executable, str(位置 / '工具集/可執行束打包.py'), '-o', str(目錄值 / 'apps.bin')] + 條目列列表, check=True)
    原始碼 = 目錄值 / 'apps.s'
    原始碼.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(目錄值 / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(目錄值 / 'apps.o'), str(原始碼)], check=True)
    內核值 = 目錄值 / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置 / '啓動/鏈接佈局.ld'), '-o', str(內核值),
                    str(位置 / 'build/boot.o'), str(位置 / 'build/java.o'), str(位置 / 'build/user.o'), str(目錄值 / 'apps.o')], check=True)
    return 內核值


def 執行命令():
    結果 = {}
    服務器值 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    服務器值.bind(('127.0.0.1', 0))
    服務器值.settimeout(0.1)
    埠值 = 服務器值.getsockname()[1]
    已接收項目 = []
    退出程式 = threading.Event()
    def 回顯回覆():
        while not 退出程式.is_set():
            try: 資料, 對端值 = 服務器值.recvfrom(4096)
            except socket.timeout: continue
            已接收項目.append(資料)
            if 資料 != b'drop-me': 服務器值.sendto(資料, 對端值)
    後臺任務值 = threading.Thread(target=回顯回覆, daemon=True)
    後臺任務值.start()
    try:
        for 種類值 in ('elf', 'iso'):
            計算機 = 虛擬機器(位置 / ('build/kernel.elf' if 種類值 == 'elf' else 'build/kernel.iso'), 種類值)
            try:
                計算機.命令('apps', ['hello', 'udp', 'netcheck', 'stress'])
                計算機.命令('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                計算機.命令('run missing', ['Exit: -2'])
                計算機.命令('net', ['NET RTL8139'])
                計算機.命令('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for 內容值 in ('hello-network', 'odd', 'even', 'repeat-123'):
                    計算機.命令('run udp 10.0.2.2 {} {}'.format(埠值, 內容值), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert 內容值.encode() in 已接收項目, '宿主 서버에서 자료를 받지 못함'
                計算機.命令('run stress {}'.format(埠值), ['UDP STRESS PASS', 'Exit: 0'])
                計算機.命令('run udp 10.0.2.2 {} drop-me'.format(埠值), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                計算機.命令('run hello recovered', ['arg: recovered', 'Exit: 0'])
                結果[種類值] = 計算機.日誌記錄.decode('utf-8', 'replace')
                print('PASS: {} 使用者 ELF/ring 3/實參/UDP 宿主 왕복/時間值 초과/命令殼 복귀'.format(種類值), flush=True)
            finally:
                try: 計算機.命令('net', [])
                except Exception: pass
                (位置 / 'build/사용자통신-last.log').write_bytes(計算機.日誌記錄)
                計算機.關閉()
        計算機 = 虛擬機器(位置 / 'build/kernel.elf', 網路值=False)
        try:
            計算機.命令('net', ['NET unavailable'])
            計算機.命令('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            計算機.命令('run hello', ['USER MODE ring 3', 'Exit: 0'])
            結果['no_nic'] = 計算機.日誌記錄.decode()
        finally: 計算機.關閉()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 臨時值:
            計算機 = 虛擬機器(已保護內核(Path(臨時值)), 網路值=False)
            try:
                for 名稱, 狀態值 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    計算機.命令('run ' + 名稱, ['Exit: ' + str(狀態值)])
                    計算機.命令('run hello', ['USER MODE ring 3', 'Exit: 0'])
                結果['protection'] = 計算機.日誌記錄.decode()
                print('PASS: 使用者 記憶體資料/硬件埠 격리, 잘못된 指針/ELF, CPU 異常, 무한 迭代值 限制值', flush=True)
            finally:
                (位置 / 'build/保護測試-last.log').write_bytes(計算機.日誌記錄)
                計算機.關閉()
    finally:
        退出程式.set()
        後臺任務值.join(timeout=2)
        服務器值.close()
    結果['host_udp_received'] = [{'length': len(資料), 'sha256': hashlib.sha256(資料).hexdigest()} for 資料 in 已接收項目]
    (位置 / 'build/測試用戶網路.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    執行命令()
