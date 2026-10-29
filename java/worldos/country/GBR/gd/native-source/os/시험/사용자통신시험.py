#!/usr/bin/env python3
"""dearbh_dàta ring 3 ELF/òstair UDP 왕복/dìon_VALUE Mearachd/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

suidhich = Path(__file__).resolve().parents[1]


class mas_fhìor_inneal:
    def __init__(self, Slighe, 종류='elf', lìonra_VALUE=True, stòras_meadhanach=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        eòlaire_VALUE = Path(self.임시.name)
        self.LOG_ràgh = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monatair_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, monatair_slighe = eòlaire_VALUE / 'serial.sock', eòlaire_VALUE / 'monitor.sock'
        àithne = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monatair_slighe) + ',server,nowait']
        àithne += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if lìonra_VALUE else ['-net', 'none']
        àithne += ['-kernel', str(Slighe)] if 종류 == 'elf' else ['-cdrom', str(Slighe), '-boot', 'd']
        if stòras_meadhanach is not None:
            àithne += ['-drive', 'file=' + str(stòras_meadhanach) + ',format=raw,if=ide,index=0']
        self.Pròiseas_VALUE = subprocess.Popen(àithne, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monatair_slighe.exists()):
                if self.Pròiseas_VALUE.poll() is not None:
                    raise AssertionError(self.Pròiseas_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ruith TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monatair_VALUE.connect(str(monatair_slighe))
            self.직렬.setblocking(False)
            self.monatair_VALUE.sendall(b'cont\n')
            self.fuirich_cor('jkoros> ')
        except BaseException:
            self.dùin()
            raise

    def fuirich_cor(self, 문구, ruith=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_ràgh[ruith:]:
                return self.LOG_ràgh[ruith:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                dàta = self.직렬.recv(65536)
                if not dàta: break
                self.LOG_ràgh.extend(dàta)
            if self.Pròiseas_VALUE.poll() is not None: break
        raise AssertionError('fuirich_VALUE fàilligeadh_VALUE: ' + 문구 + '\n' + self.LOG_ràgh.decode('utf-8', 'replace'))

    def àithne(self, sreang_VALUE, 기대):
        ruith = len(self.LOG_ràgh)
        self.직렬.sendall((sreang_VALUE + '\n').encode())
        tomhas = self.fuirich_cor('jkoros> ', ruith)
        for 문구 in 기대:
            assert 문구 in tomhas, (sreang_VALUE, 문구, tomhas)
        assert 'PANIC' not in tomhas, tomhas
        return tomhas

    def dùin(self):
        self.직렬.close()
        self.monatair_VALUE.close()
        if self.Pròiseas_VALUE.poll() is None:
            self.Pròiseas_VALUE.terminate()
            try: self.Pròiseas_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Pròiseas_VALUE.kill()
                self.Pròiseas_VALUE.wait()
        self.Pròiseas_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(eòlaire_VALUE):
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
    항목들 = ['hello=' + str(suidhich / 'build/apps/hello.elf')]
    for Ainm, susbaint_VALUE in 사례들.items():
        tùs = eòlaire_VALUE / (Ainm + '.s')
        tùs.write_text('.code32\n.text\n.globl _start\n_start:\n' + susbaint_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(eòlaire_VALUE / (Ainm + '.o')), str(tùs)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(suidhich.parent / 'compiler/cleachdaiche_ceangal_co_dhealbhachd.ld'),
                        '-o', str(eòlaire_VALUE / (Ainm + '.elf')), str(eòlaire_VALUE / (Ainm + '.o'))], check=True)
        항목들.append(Ainm + '=' + str(eòlaire_VALUE / (Ainm + '.elf')))
    정상 = bytearray((suidhich / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    mì_dhligheach_tomhas = bytearray(정상); mì_dhligheach_tomhas[0] = 0; 변형들['badelf'] = mì_dhligheach_tomhas
    mì_dhligheach_tomhas = bytearray(정상); struct.pack_into('<I', mì_dhligheach_tomhas, 24, 0x00100000); 변형들['badentry'] = mì_dhligheach_tomhas
    mì_dhligheach_tomhas = bytearray(정상); struct.pack_into('<I', mì_dhligheach_tomhas, 28, 0x7fffffff); 변형들['badtable'] = mì_dhligheach_tomhas
    mì_dhligheach_tomhas = bytearray(정상); LOOKUP_clàr = struct.unpack_from('<I', mì_dhligheach_tomhas, 28)[0]
    struct.pack_into('<I', mì_dhligheach_tomhas, LOOKUP_clàr + 20, 0x7fffffff); 변형들['badsize'] = mì_dhligheach_tomhas
    for Ainm, dàta in 변형들.items():
        faidhle = eòlaire_VALUE / (Ainm + '.elf'); faidhle.write_bytes(dàta)
        항목들.append(Ainm + '=' + str(faidhle))
    subprocess.run([sys.executable, str(suidhich / 'innealan/묶기.py'), '-o', str(eòlaire_VALUE / 'apps.bin')] + 항목들, check=True)
    tùs = eòlaire_VALUE / 'apps.s'
    tùs.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(eòlaire_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(eòlaire_VALUE / 'apps.o'), str(tùs)], check=True)
    eitean_VALUE = eòlaire_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(suidhich / '부팅/ceangal_co_dhealbhachd.ld'), '-o', str(eitean_VALUE),
                    str(suidhich / 'build/boot.o'), str(suidhich / 'build/java.o'), str(suidhich / 'build/user.o'), str(eòlaire_VALUE / 'apps.o')], check=True)
    return eitean_VALUE


def gnìomhaich_àithne():
    tomhas = {}
    frithealaiche_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    frithealaiche_VALUE.bind(('127.0.0.1', 0))
    frithealaiche_VALUE.settimeout(0.1)
    port_VALUE = frithealaiche_VALUE.getsockname()[1]
    RECEIVED_nì = []
    fàg_ap = threading.Event()
    def 되보내기():
        while not fàg_ap.is_set():
            try: dàta, seise_VALUE = frithealaiche_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_nì.append(dàta)
            if dàta != b'drop-me': frithealaiche_VALUE.sendto(dàta, seise_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            inneal = mas_fhìor_inneal(suidhich / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                inneal.àithne('apps', ['hello', 'udp', 'netcheck', 'stress'])
                inneal.àithne('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                inneal.àithne('run missing', ['Exit: -2'])
                inneal.àithne('net', ['NET RTL8139'])
                inneal.àithne('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for susbaint_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    inneal.àithne('run udp 10.0.2.2 {} {}'.format(port_VALUE, susbaint_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert susbaint_VALUE.encode() in RECEIVED_nì, 'òstair 서버에서 자료를 받지 못함'
                inneal.àithne('run stress {}'.format(port_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                inneal.àithne('run udp 10.0.2.2 {} drop-me'.format(port_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                inneal.àithne('run hello recovered', ['arg: recovered', 'Exit: 0'])
                tomhas[종류] = inneal.LOG_ràgh.decode('utf-8', 'replace')
                print('PASS: {} cleachdaiche ELF/ring 3/인수/UDP òstair 왕복/TIME_VALUE 초과/slige 복귀'.format(종류), flush=True)
            finally:
                try: inneal.àithne('net', [])
                except Exception: pass
                (suidhich / 'build/사용자통신-last.log').write_bytes(inneal.LOG_ràgh)
                inneal.dùin()
        inneal = mas_fhìor_inneal(suidhich / 'build/kernel.elf', lìonra_VALUE=False)
        try:
            inneal.àithne('net', ['NET unavailable'])
            inneal.àithne('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            inneal.àithne('run hello', ['USER MODE ring 3', 'Exit: 0'])
            tomhas['no_nic'] = inneal.LOG_ràgh.decode()
        finally: inneal.dùin()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            inneal = mas_fhìor_inneal(보호커널(Path(임시)), lìonra_VALUE=False)
            try:
                for Ainm, cor_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    inneal.àithne('run ' + Ainm, ['Exit: ' + str(cor_VALUE)])
                    inneal.àithne('run hello', ['USER MODE ring 3', 'Exit: 0'])
                tomhas['protection'] = inneal.LOG_ràgh.decode()
                print('PASS: cleachdaiche cuimhne_dàta/포트 격리, 잘못된 tomhaire/ELF, CPU 예외, 무한 ath_thriall_VALUE 제한', flush=True)
            finally:
                (suidhich / 'build/보호시험-last.log').write_bytes(inneal.LOG_ràgh)
                inneal.dùin()
    finally:
        fàg_ap.set()
        일꾼.join(timeout=2)
        frithealaiche_VALUE.close()
    tomhas['host_udp_received'] = [{'length': len(dàta), 'sha256': hashlib.sha256(dàta).hexdigest()} for dàta in RECEIVED_nì]
    (suidhich / 'build/사용자통신시험.json').write_text(json.dumps(tomhas, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    gnìomhaich_àithne()
