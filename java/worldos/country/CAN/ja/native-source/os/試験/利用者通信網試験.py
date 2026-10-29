#!/usr/bin/env python3
"""実際データ ring 3 ELF/ホスト UDP 왕복/値防護 エラー/時間値 上限値/잘못된 ELF를 검증한다."""
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


class 仮想機械:
    def __init__(self, 経路, 種別値='elf', 通信網値=True, 記憶装置中間容量=None):
        self.一時値 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ディレクトリ値 = Path(self.一時値.name)
        self.履歴記録記録 = bytearray()
        self.直列値 = socket.socket(socket.AF_UNIX)
        self.監視器値 = socket.socket(socket.AF_UNIX)
        直列経路, 監視器経路 = ディレクトリ値 / 'serial.sock', ディレクトリ値 / 'monitor.sock'
        命令 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(直列経路) + ',server,nowait',
                '-monitor', 'unix:' + str(監視器経路) + ',server,nowait']
        命令 += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if 通信網値 else ['-net', 'none']
        命令 += ['-kernel', str(経路)] if 種別値 == 'elf' else ['-cdrom', str(経路), '-boot', 'd']
        if 記憶装置中間容量 is not None:
            命令 += ['-drive', 'file=' + str(記憶装置中間容量) + ',format=raw,if=ide,index=0']
        self.プロセス値 = subprocess.Popen(命令, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            終端 = time.monotonic() + 10
            while not (直列経路.exists() and 監視器経路.exists()):
                if self.プロセス値.poll() is not None:
                    raise AssertionError(self.プロセス値.stderr.read().decode())
                if time.monotonic() > 終端: raise AssertionError('QEMU 起動処理 時間値 초과')
                time.sleep(0.03)
            self.直列値.connect(str(直列経路))
            self.監視器値.connect(str(監視器経路))
            self.直列値.setblocking(False)
            self.監視器値.sendall(b'cont\n')
            self.状況待合('jkoros> ')
        except BaseException:
            self.閉鎖()
            raise

    def 状況待合(self, 句値, 起動処理=0, 上限値=15):
        終端 = time.monotonic() + 上限値
        while time.monotonic() < 終端:
            if 句値.encode() in self.履歴記録記録[起動処理:]:
                return self.履歴記録記録[起動処理:].decode('utf-8', 'replace')
            読取, _, _ = select.select([self.直列値], [], [], 0.1)
            if 読取:
                データ = self.直列値.recv(65536)
                if not データ: break
                self.履歴記録記録.extend(データ)
            if self.プロセス値.poll() is not None: break
        raise AssertionError('値待合 失敗値: ' + 句値 + '\n' + self.履歴記録記録.decode('utf-8', 'replace'))

    def 命令(self, 文字列, 期待状態):
        起動処理 = len(self.履歴記録記録)
        self.直列値.sendall((文字列 + '\n').encode())
        結果 = self.状況待合('jkoros> ', 起動処理)
        for 句値 in 期待状態:
            assert 句値 in 結果, (文字列, 句値, 結果)
        assert 'PANIC' not in 結果, 結果
        return 結果

    def 閉鎖(self):
        self.直列値.close()
        self.監視器値.close()
        if self.プロセス値.poll() is None:
            self.プロセス値.terminate()
            try: self.プロセス値.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.プロセス値.kill()
                self.プロセス値.wait()
        self.プロセス値.communicate()
        self.一時値.cleanup()


def 保護済み中核(ディレクトリ値):
    分岐一覧一覧 = {
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
    登録項目一覧一覧 = ['hello=' + str(位置 / 'build/apps/hello.elf')]
    for 名前, 内容物値 in 分岐一覧一覧.items():
        ソース = ディレクトリ値 / (名前 + '.s')
        ソース.write_text('.code32\n.text\n.globl _start\n_start:\n' + 内容物値 +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ディレクトリ値 / (名前 + '.o')), str(ソース)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置.parent / 'compiler/利用者連結配置.ld'),
                        '-o', str(ディレクトリ値 / (名前 + '.elf')), str(ディレクトリ値 / (名前 + '.o'))], check=True)
        登録項目一覧一覧.append(名前 + '=' + str(ディレクトリ値 / (名前 + '.elf')))
    判定通常 = bytearray((位置 / 'build/apps/hello.elf').read_bytes())
    派生一覧一覧 = {}
    無効結果 = bytearray(判定通常); 無効結果[0] = 0; 派生一覧一覧['badelf'] = 無効結果
    無効結果 = bytearray(判定通常); struct.pack_into('<I', 無効結果, 24, 0x00100000); 派生一覧一覧['badentry'] = 無効結果
    無効結果 = bytearray(判定通常); struct.pack_into('<I', 無効結果, 28, 0x7fffffff); 派生一覧一覧['badtable'] = 無効結果
    無効結果 = bytearray(判定通常); 表 = struct.unpack_from('<I', 無効結果, 28)[0]
    struct.pack_into('<I', 無効結果, 表 + 20, 0x7fffffff); 派生一覧一覧['badsize'] = 無効結果
    for 名前, データ in 派生一覧一覧.items():
        ファイル = ディレクトリ値 / (名前 + '.elf'); ファイル.write_bytes(データ)
        登録項目一覧一覧.append(名前 + '=' + str(ファイル))
    subprocess.run([sys.executable, str(位置 / '道具/実行束梱包.py'), '-o', str(ディレクトリ値 / 'apps.bin')] + 登録項目一覧一覧, check=True)
    ソース = ディレクトリ値 / 'apps.s'
    ソース.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ディレクトリ値 / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ディレクトリ値 / 'apps.o'), str(ソース)], check=True)
    中核値 = ディレクトリ値 / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(位置 / '起動/連結配置.ld'), '-o', str(中核値),
                    str(位置 / 'build/boot.o'), str(位置 / 'build/java.o'), str(位置 / 'build/user.o'), str(ディレクトリ値 / 'apps.o')], check=True)
    return 中核値


def 命令実行():
    結果 = {}
    サーバー値 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    サーバー値.bind(('127.0.0.1', 0))
    サーバー値.settimeout(0.1)
    ポート値 = サーバー値.getsockname()[1]
    受信済み項目 = []
    終了点プログラム = threading.Event()
    def 復唱返答():
        while not 終了点プログラム.is_set():
            try: データ, 通信相手値 = サーバー値.recvfrom(4096)
            except socket.timeout: continue
            受信済み項目.append(データ)
            if データ != b'drop-me': サーバー値.sendto(データ, 通信相手値)
    作業担当値 = threading.Thread(target=復唱返答, daemon=True)
    作業担当値.start()
    try:
        for 種別値 in ('elf', 'iso'):
            機械 = 仮想機械(位置 / ('build/kernel.elf' if 種別値 == 'elf' else 'build/kernel.iso'), 種別値)
            try:
                機械.命令('apps', ['hello', 'udp', 'netcheck', 'stress'])
                機械.命令('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                機械.命令('run missing', ['Exit: -2'])
                機械.命令('net', ['NET RTL8139'])
                機械.命令('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for 内容物値 in ('hello-network', 'odd', 'even', 'repeat-123'):
                    機械.命令('run udp 10.0.2.2 {} {}'.format(ポート値, 内容物値), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert 内容物値.encode() in 受信済み項目, 'ホスト 서버에서 자료를 받지 못함'
                機械.命令('run stress {}'.format(ポート値), ['UDP STRESS PASS', 'Exit: 0'])
                機械.命令('run udp 10.0.2.2 {} drop-me'.format(ポート値), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                機械.命令('run hello recovered', ['arg: recovered', 'Exit: 0'])
                結果[種別値] = 機械.履歴記録記録.decode('utf-8', 'replace')
                print('PASS: {} 利用者 ELF/ring 3/引数/UDP ホスト 왕복/時間値 초과/シェル 복귀'.format(種別値), flush=True)
            finally:
                try: 機械.命令('net', [])
                except Exception: pass
                (位置 / 'build/사용자통신-last.log').write_bytes(機械.履歴記録記録)
                機械.閉鎖()
        機械 = 仮想機械(位置 / 'build/kernel.elf', 通信網値=False)
        try:
            機械.命令('net', ['NET unavailable'])
            機械.命令('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            機械.命令('run hello', ['USER MODE ring 3', 'Exit: 0'])
            結果['no_nic'] = 機械.履歴記録記録.decode()
        finally: 機械.閉鎖()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 一時値:
            機械 = 仮想機械(保護済み中核(Path(一時値)), 通信網値=False)
            try:
                for 名前, 状況値 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    機械.命令('run ' + 名前, ['Exit: ' + str(状況値)])
                    機械.命令('run hello', ['USER MODE ring 3', 'Exit: 0'])
                結果['protection'] = 機械.履歴記録記録.decode()
                print('PASS: 利用者 記憶データ/機器ポート 격리, 잘못된 ポインタ/ELF, CPU 例外, 무한 反復回値 上限値', flush=True)
            finally:
                (位置 / 'build/保護試験-last.log').write_bytes(機械.履歴記録記録)
                機械.閉鎖()
    finally:
        終了点プログラム.set()
        作業担当値.join(timeout=2)
        サーバー値.close()
    結果['host_udp_received'] = [{'length': len(データ), 'sha256': hashlib.sha256(データ).hexdigest()} for データ in 受信済み項目]
    (位置 / 'build/利用者通信網試験.json').write_text(json.dumps(結果, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    命令実行()
