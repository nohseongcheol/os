#!/usr/bin/env python3
"""real_ma_lumotlar ring 3 ELF/tashkilotchi UDP 왕복/himoya_qilmoq_VALUE Xato/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

Holati = Path(__file__).resolve().parents[1]


class 가상기계:
    def __init__(self, yo_l, 종류='elf', Tarmoq_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        katalog_VALUE = Path(self.임시.name)
        self.LOG_satr = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_yo_l = katalog_VALUE / 'serial.sock', katalog_VALUE / 'monitor.sock'
        Buyruq = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_yo_l) + ',server,nowait']
        Buyruq += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Tarmoq_VALUE else ['-net', 'none']
        Buyruq += ['-kernel', str(yo_l)] if 종류 == 'elf' else ['-cdrom', str(yo_l), '-boot', 'd']
        if 저장매체 is not None:
            Buyruq += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Jarayon_VALUE = subprocess.Popen(Buyruq, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_yo_l.exists()):
                if self.Jarayon_VALUE.poll() is not None:
                    raise AssertionError(self.Jarayon_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Bajarish TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_yo_l))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.bir_daqiqa_holat('jkoros> ')
        except BaseException:
            self.Yopish()
            raise

    def bir_daqiqa_holat(self, 문구, Bajarish=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_satr[Bajarish:]:
                return self.LOG_satr[Bajarish:].decode('utf-8', 'replace')
            Oʻqish, _, _ = select.select([self.직렬], [], [], 0.1)
            if Oʻqish:
                ma_lumotlar = self.직렬.recv(65536)
                if not ma_lumotlar: break
                self.LOG_satr.extend(ma_lumotlar)
            if self.Jarayon_VALUE.poll() is not None: break
        raise AssertionError('bir_daqiqa_VALUE to_xtab_qolish_VALUE: ' + 문구 + '\n' + self.LOG_satr.decode('utf-8', 'replace'))

    def Buyruq(self, satr_VALUE, 기대):
        Bajarish = len(self.LOG_satr)
        self.직렬.sendall((satr_VALUE + '\n').encode())
        o_lchov = self.bir_daqiqa_holat('jkoros> ', Bajarish)
        for 문구 in 기대:
            assert 문구 in o_lchov, (satr_VALUE, 문구, o_lchov)
        assert 'PANIC' not in o_lchov, o_lchov
        return o_lchov

    def Yopish(self):
        self.직렬.close()
        self.monitor_VALUE.close()
        if self.Jarayon_VALUE.poll() is None:
            self.Jarayon_VALUE.terminate()
            try: self.Jarayon_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Jarayon_VALUE.kill()
                self.Jarayon_VALUE.wait()
        self.Jarayon_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(katalog_VALUE):
    사례들 = {
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
    항목들 = ['hello=' + str(Holati / 'build/apps/hello.elf')]
    for Nomi, tarkib_VALUE in 사례들.items():
        manba = katalog_VALUE / (Nomi + '.s')
        manba.write_text('.code32\n.text\n.globl _start\n_start:\n' + tarkib_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(katalog_VALUE / (Nomi + '.o')), str(manba)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Holati.parent / 'compiler/foydalanuvchi_ulash_Maket.ld'),
                        '-o', str(katalog_VALUE / (Nomi + '.elf')), str(katalog_VALUE / (Nomi + '.o'))], check=True)
        항목들.append(Nomi + '=' + str(katalog_VALUE / (Nomi + '.elf')))
    정상 = bytearray((Holati / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    xato_o_lchov = bytearray(정상); xato_o_lchov[0] = 0; 변형들['badelf'] = xato_o_lchov
    xato_o_lchov = bytearray(정상); struct.pack_into('<I', xato_o_lchov, 24, 0x00100000); 변형들['badentry'] = xato_o_lchov
    xato_o_lchov = bytearray(정상); struct.pack_into('<I', xato_o_lchov, 28, 0x7fffffff); 변형들['badtable'] = xato_o_lchov
    xato_o_lchov = bytearray(정상); LOOKUP_jadval = struct.unpack_from('<I', xato_o_lchov, 28)[0]
    struct.pack_into('<I', xato_o_lchov, LOOKUP_jadval + 20, 0x7fffffff); 변형들['badsize'] = xato_o_lchov
    for Nomi, ma_lumotlar in 변형들.items():
        Fayl = katalog_VALUE / (Nomi + '.elf'); Fayl.write_bytes(ma_lumotlar)
        항목들.append(Nomi + '=' + str(Fayl))
    subprocess.run([sys.executable, str(Holati / 'Vositalar/묶기.py'), '-o', str(katalog_VALUE / 'apps.bin')] + 항목들, check=True)
    manba = katalog_VALUE / 'apps.s'
    manba.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(katalog_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(katalog_VALUE / 'apps.o'), str(manba)], check=True)
    o_zak_VALUE = katalog_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Holati / '부팅/ulash_Maket.ld'), '-o', str(o_zak_VALUE),
                    str(Holati / 'build/boot.o'), str(Holati / 'build/java.o'), str(Holati / 'build/user.o'), str(katalog_VALUE / 'apps.o')], check=True)
    return o_zak_VALUE


def bajarmoq_buyruq():
    o_lchov = {}
    server_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VALUE.bind(('127.0.0.1', 0))
    server_VALUE.settimeout(0.1)
    port_VALUE = server_VALUE.getsockname()[1]
    RECEIVED_element = []
    Chiqish_ilova = threading.Event()
    def 되보내기():
        while not Chiqish_ilova.is_set():
            try: ma_lumotlar, bir_rangli_VALUE = server_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_element.append(ma_lumotlar)
            if ma_lumotlar != b'drop-me': server_VALUE.sendto(ma_lumotlar, bir_rangli_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            기계 = 가상기계(Holati / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                기계.Buyruq('apps', ['hello', 'udp', 'netcheck', 'stress'])
                기계.Buyruq('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                기계.Buyruq('run missing', ['Exit: -2'])
                기계.Buyruq('net', ['NET RTL8139'])
                기계.Buyruq('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for tarkib_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    기계.Buyruq('run udp 10.0.2.2 {} {}'.format(port_VALUE, tarkib_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert tarkib_VALUE.encode() in RECEIVED_element, 'tashkilotchi 서버에서 자료를 받지 못함'
                기계.Buyruq('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                기계.Buyruq('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                기계.Buyruq('run hello recovered', ['arg: recovered', 'Exit: 0'])
                o_lchov[종류] = 기계.LOG_satr.decode('utf-8', 'replace')
                print('PASS: {} foydalanuvchi ELF/ring 3/인수/UDP tashkilotchi 왕복/TIME_VALUE 초과/qobiq 복귀'.format(종류), flush=True)
            finally:
                try: 기계.Buyruq('net', [])
                except Exception: pass
                (Holati / 'build/사용자통신-last.log').write_bytes(기계.LOG_satr)
                기계.Yopish()
        기계 = 가상기계(Holati / 'build/kernel.elf', Tarmoq_VALUE=False)
        try:
            기계.Buyruq('net', ['NET unavailable'])
            기계.Buyruq('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            기계.Buyruq('run hello', ['USER MODE ring 3', 'Exit: 0'])
            o_lchov['no_nic'] = 기계.LOG_satr.decode()
        finally: 기계.Yopish()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            기계 = 가상기계(보호커널(Path(임시)), Tarmoq_VALUE=False)
            try:
                for Nomi, holat_VALUE_e10195a1 in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    기계.Buyruq('run ' + Nomi, ['Exit: ' + str(holat_VALUE_e10195a1)])
                    기계.Buyruq('run hello', ['USER MODE ring 3', 'Exit: 0'])
                o_lchov['protection'] = 기계.LOG_satr.decode()
                print('PASS: foydalanuvchi Xotira_ma_lumotlar/포트 격리, 잘못된 kursor/ELF, CPU istisno, 무한 sprint_VALUE 제한', flush=True)
            finally:
                (Holati / 'build/보호시험-last.log').write_bytes(기계.LOG_satr)
                기계.Yopish()
    finally:
        Chiqish_ilova.set()
        일꾼.join(timeout=2)
        server_VALUE.close()
    o_lchov['host_udp_received'] = [{'length': len(ma_lumotlar), 'sha256': hashlib.sha256(ma_lumotlar).hexdigest()} for ma_lumotlar in RECEIVED_element]
    (Holati / 'build/사용자통신시험.json').write_text(json.dumps(o_lchov, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    bajarmoq_buyruq()
