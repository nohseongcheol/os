#!/usr/bin/env python3
"""go_iawn_data ring 3 ELF/lletya UDP 왕복/diogelu_VALUE Gwall/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

safle = Path(__file__).resolve().parents[1]


class rhith_peiriant:
    def __init__(self, LLWYBR, 종류='elf', Rhwydwaith_VALUE=True, Storio_canolig=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        cyfeiriadur_VALUE = Path(self.임시.name)
        self.LOG_rhes = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_llwybr = cyfeiriadur_VALUE / 'serial.sock', cyfeiriadur_VALUE / 'monitor.sock'
        Gorchymyn = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_llwybr) + ',server,nowait']
        Gorchymyn += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Rhwydwaith_VALUE else ['-net', 'none']
        Gorchymyn += ['-kernel', str(LLWYBR)] if 종류 == 'elf' else ['-cdrom', str(LLWYBR), '-boot', 'd']
        if Storio_canolig is not None:
            Gorchymyn += ['-drive', 'file=' + str(Storio_canolig) + ',format=raw,if=ide,index=0']
        self.Proses_VALUE = subprocess.Popen(Gorchymyn, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_llwybr.exists()):
                if self.Proses_VALUE.poll() is not None:
                    raise AssertionError(self.Proses_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Gweithredu_2 TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VALUE.connect(str(monitor_llwybr))
            self.직렬.setblocking(False)
            self.monitor_VALUE.sendall(b'cont\n')
            self.aros_cyflwr('jkoros> ')
        except BaseException:
            self.Cau()
            raise

    def aros_cyflwr(self, 문구, Gweithredu_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_rhes[Gweithredu_2:]:
                return self.LOG_rhes[Gweithredu_2:].decode('utf-8', 'replace')
            Darllen, _, _ = select.select([self.직렬], [], [], 0.1)
            if Darllen:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_rhes.extend(data)
            if self.Proses_VALUE.poll() is not None: break
        raise AssertionError('aros_VALUE methiant_VALUE: ' + 문구 + '\n' + self.LOG_rhes.decode('utf-8', 'replace'))

    def Gorchymyn(self, testun_VALUE, 기대):
        Gweithredu_2 = len(self.LOG_rhes)
        self.직렬.sendall((testun_VALUE + '\n').encode())
        mesur = self.aros_cyflwr('jkoros> ', Gweithredu_2)
        for 문구 in 기대:
            assert 문구 in mesur, (testun_VALUE, 문구, mesur)
        assert 'PANIC' not in mesur, mesur
        return mesur

    def Cau(self):
        self.직렬.close()
        self.monitor_VALUE.close()
        if self.Proses_VALUE.poll() is None:
            self.Proses_VALUE.terminate()
            try: self.Proses_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proses_VALUE.kill()
                self.Proses_VALUE.wait()
        self.Proses_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(cyfeiriadur_VALUE):
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
    항목들 = ['hello=' + str(safle / 'build/apps/hello.elf')]
    for Enw, Cynnwys_VALUE in 사례들.items():
        FFYNHONNELL = cyfeiriadur_VALUE / (Enw + '.s')
        FFYNHONNELL.write_text('.code32\n.text\n.globl _start\n_start:\n' + Cynnwys_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(cyfeiriadur_VALUE / (Enw + '.o')), str(FFYNHONNELL)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(safle.parent / 'compiler/defnyddiwr_Dolen_Llywio.ld'),
                        '-o', str(cyfeiriadur_VALUE / (Enw + '.elf')), str(cyfeiriadur_VALUE / (Enw + '.o'))], check=True)
        항목들.append(Enw + '=' + str(cyfeiriadur_VALUE / (Enw + '.elf')))
    technoleg_gwybodaeth_normal = bytearray((safle / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    annilys_mesur = bytearray(technoleg_gwybodaeth_normal); annilys_mesur[0] = 0; 변형들['badelf'] = annilys_mesur
    annilys_mesur = bytearray(technoleg_gwybodaeth_normal); struct.pack_into('<I', annilys_mesur, 24, 0x00100000); 변형들['badentry'] = annilys_mesur
    annilys_mesur = bytearray(technoleg_gwybodaeth_normal); struct.pack_into('<I', annilys_mesur, 28, 0x7fffffff); 변형들['badtable'] = annilys_mesur
    annilys_mesur = bytearray(technoleg_gwybodaeth_normal); LOOKUP_tabl = struct.unpack_from('<I', annilys_mesur, 28)[0]
    struct.pack_into('<I', annilys_mesur, LOOKUP_tabl + 20, 0x7fffffff); 변형들['badsize'] = annilys_mesur
    for Enw, data in 변형들.items():
        Ffeil = cyfeiriadur_VALUE / (Enw + '.elf'); Ffeil.write_bytes(data)
        항목들.append(Enw + '=' + str(Ffeil))
    subprocess.run([sys.executable, str(safle / 'Offer/묶기.py'), '-o', str(cyfeiriadur_VALUE / 'apps.bin')] + 항목들, check=True)
    FFYNHONNELL = cyfeiriadur_VALUE / 'apps.s'
    FFYNHONNELL.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(cyfeiriadur_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(cyfeiriadur_VALUE / 'apps.o'), str(FFYNHONNELL)], check=True)
    cnewyllyn_VALUE = cyfeiriadur_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(safle / '부팅/Dolen_Llywio.ld'), '-o', str(cnewyllyn_VALUE),
                    str(safle / 'build/boot.o'), str(safle / 'build/java.o'), str(safle / 'build/user.o'), str(cyfeiriadur_VALUE / 'apps.o')], check=True)
    return cnewyllyn_VALUE


def Gweithredu_gorchymyn():
    mesur = {}
    gweinydd_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    gweinydd_VALUE.bind(('127.0.0.1', 0))
    gweinydd_VALUE.settimeout(0.1)
    porth_VALUE = gweinydd_VALUE.getsockname()[1]
    RECEIVED_eitem = []
    gadael_Rhaglen = threading.Event()
    def 되보내기():
        while not gadael_Rhaglen.is_set():
            try: data, cymar_VALUE = gweinydd_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_eitem.append(data)
            if data != b'drop-me': gweinydd_VALUE.sendto(data, cymar_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            peiriant = rhith_peiriant(safle / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                peiriant.Gorchymyn('apps', ['hello', 'udp', 'netcheck', 'stress'])
                peiriant.Gorchymyn('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                peiriant.Gorchymyn('run missing', ['Exit: -2'])
                peiriant.Gorchymyn('net', ['NET RTL8139'])
                peiriant.Gorchymyn('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Cynnwys_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    peiriant.Gorchymyn('run udp 10.0.2.2 {} {}'.format(porth_VALUE, Cynnwys_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Cynnwys_VALUE.encode() in RECEIVED_eitem, 'lletya 서버에서 자료를 받지 못함'
                peiriant.Gorchymyn('run stress {}'.format(porth_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                peiriant.Gorchymyn('run udp 10.0.2.2 {} drop-me'.format(porth_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                peiriant.Gorchymyn('run hello recovered', ['arg: recovered', 'Exit: 0'])
                mesur[종류] = peiriant.LOG_rhes.decode('utf-8', 'replace')
                print('PASS: {} defnyddiwr ELF/ring 3/인수/UDP lletya 왕복/TIME_VALUE 초과/cragen 복귀'.format(종류), flush=True)
            finally:
                try: peiriant.Gorchymyn('net', [])
                except Exception: pass
                (safle / 'build/사용자통신-last.log').write_bytes(peiriant.LOG_rhes)
                peiriant.Cau()
        peiriant = rhith_peiriant(safle / 'build/kernel.elf', Rhwydwaith_VALUE=False)
        try:
            peiriant.Gorchymyn('net', ['NET unavailable'])
            peiriant.Gorchymyn('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            peiriant.Gorchymyn('run hello', ['USER MODE ring 3', 'Exit: 0'])
            mesur['no_nic'] = peiriant.LOG_rhes.decode()
        finally: peiriant.Cau()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            peiriant = rhith_peiriant(보호커널(Path(임시)), Rhwydwaith_VALUE=False)
            try:
                for Enw, cyflwr_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    peiriant.Gorchymyn('run ' + Enw, ['Exit: ' + str(cyflwr_VALUE)])
                    peiriant.Gorchymyn('run hello', ['USER MODE ring 3', 'Exit: 0'])
                mesur['protection'] = peiriant.LOG_rhes.decode()
                print('PASS: defnyddiwr Cof_data/포트 격리, 잘못된 pwyntydd/ELF, CPU eithriad, 무한 iteriad_VALUE 제한', flush=True)
            finally:
                (safle / 'build/보호시험-last.log').write_bytes(peiriant.LOG_rhes)
                peiriant.Cau()
    finally:
        gadael_Rhaglen.set()
        일꾼.join(timeout=2)
        gweinydd_VALUE.close()
    mesur['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in RECEIVED_eitem]
    (safle / 'build/사용자통신시험.json').write_text(json.dumps(mesur, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Gweithredu_gorchymyn()
