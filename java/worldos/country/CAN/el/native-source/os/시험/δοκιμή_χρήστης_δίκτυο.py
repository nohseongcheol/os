#!/usr/bin/env python3
"""πραγματικός_δεδομένα ring 3 ELF/φιλοξενώ UDP 왕복/προστασία_τιμή ΣΦΑΛΜΑ/τιμή_ώρας 제한/잘못된 ELF를 검증한다."""
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

Θέση = Path(__file__).resolve().parents[1]


class εικονική_μηχανή:
    def __init__(self, ΔΙΑΔΡΟΜΗ, 종류='elf', δίκτυο_τιμή=True, Χώρος_αποθήκευσης_μέσο=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Κατάλογος_τιμή = Path(self.임시.name)
        self.καταγράφω_ρεκόρ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.οθόνη_τιμή = socket.socket(socket.AF_UNIX)
        직렬경로, οθόνη_διαδρομή = Κατάλογος_τιμή / 'serial.sock', Κατάλογος_τιμή / 'monitor.sock'
        Εντολή = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(οθόνη_διαδρομή) + ',server,nowait']
        Εντολή += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if δίκτυο_τιμή else ['-net', 'none']
        Εντολή += ['-kernel', str(ΔΙΑΔΡΟΜΗ)] if 종류 == 'elf' else ['-cdrom', str(ΔΙΑΔΡΟΜΗ), '-boot', 'd']
        if Χώρος_αποθήκευσης_μέσο is not None:
            Εντολή += ['-drive', 'file=' + str(Χώρος_αποθήκευσης_μέσο) + ',format=raw,if=ide,index=0']
        self.διεργασία_τιμή = subprocess.Popen(Εντολή, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and οθόνη_διαδρομή.exists()):
                if self.διεργασία_τιμή.poll() is not None:
                    raise AssertionError(self.διεργασία_τιμή.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Εκτέλεση_2 τιμή_ώρας 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.οθόνη_τιμή.connect(str(οθόνη_διαδρομή))
            self.직렬.setblocking(False)
            self.οθόνη_τιμή.sendall(b'cont\n')
            self.κατάσταση_αναμονής('jkoros> ')
        except BaseException:
            self.Κλείσιμο()
            raise

    def κατάσταση_αναμονής(self, 문구, Εκτέλεση_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.καταγράφω_ρεκόρ[Εκτέλεση_2:]:
                return self.καταγράφω_ρεκόρ[Εκτέλεση_2:].decode('utf-8', 'replace')
            Ανάγνωση, _, _ = select.select([self.직렬], [], [], 0.1)
            if Ανάγνωση:
                δεδομένα = self.직렬.recv(65536)
                if not δεδομένα: break
                self.καταγράφω_ρεκόρ.extend(δεδομένα)
            if self.διεργασία_τιμή.poll() is not None: break
        raise AssertionError('περίμενε_τιμή αποτυχία_τιμή: ' + 문구 + '\n' + self.καταγράφω_ρεκόρ.decode('utf-8', 'replace'))

    def Εντολή(self, συμβολοσειρά_τιμή, 기대):
        Εκτέλεση_2 = len(self.καταγράφω_ρεκόρ)
        self.직렬.sendall((συμβολοσειρά_τιμή + '\n').encode())
        μέτρηση = self.κατάσταση_αναμονής('jkoros> ', Εκτέλεση_2)
        for 문구 in 기대:
            assert 문구 in μέτρηση, (συμβολοσειρά_τιμή, 문구, μέτρηση)
        assert 'PANIC' not in μέτρηση, μέτρηση
        return μέτρηση

    def Κλείσιμο(self):
        self.직렬.close()
        self.οθόνη_τιμή.close()
        if self.διεργασία_τιμή.poll() is None:
            self.διεργασία_τιμή.terminate()
            try: self.διεργασία_τιμή.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.διεργασία_τιμή.kill()
                self.διεργασία_τιμή.wait()
        self.διεργασία_τιμή.communicate()
        self.임시.cleanup()


def 보호커널(Κατάλογος_τιμή):
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
    항목들 = ['hello=' + str(Θέση / 'build/apps/hello.elf')]
    for Όνομα, Περιεχόμενο_τιμή in 사례들.items():
        ΠΗΓΗ = Κατάλογος_τιμή / (Όνομα + '.s')
        ΠΗΓΗ.write_text('.code32\n.text\n.globl _start\n_start:\n' + Περιεχόμενο_τιμή +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Κατάλογος_τιμή / (Όνομα + '.o')), str(ΠΗΓΗ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Θέση.parent / 'compiler/χρήστης_συνδέω_Διάταξη.ld'),
                        '-o', str(Κατάλογος_τιμή / (Όνομα + '.elf')), str(Κατάλογος_τιμή / (Όνομα + '.o'))], check=True)
        항목들.append(Όνομα + '=' + str(Κατάλογος_τιμή / (Όνομα + '.elf')))
    πληροφοριακά_συστήματα_απλά = bytearray((Θέση / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    άκυρος_μέτρηση = bytearray(πληροφοριακά_συστήματα_απλά); άκυρος_μέτρηση[0] = 0; 변형들['badelf'] = άκυρος_μέτρηση
    άκυρος_μέτρηση = bytearray(πληροφοριακά_συστήματα_απλά); struct.pack_into('<I', άκυρος_μέτρηση, 24, 0x00100000); 변형들['badentry'] = άκυρος_μέτρηση
    άκυρος_μέτρηση = bytearray(πληροφοριακά_συστήματα_απλά); struct.pack_into('<I', άκυρος_μέτρηση, 28, 0x7fffffff); 변형들['badtable'] = άκυρος_μέτρηση
    άκυρος_μέτρηση = bytearray(πληροφοριακά_συστήματα_απλά); Αναζήτηση_πίνακας = struct.unpack_from('<I', άκυρος_μέτρηση, 28)[0]
    struct.pack_into('<I', άκυρος_μέτρηση, Αναζήτηση_πίνακας + 20, 0x7fffffff); 변형들['badsize'] = άκυρος_μέτρηση
    for Όνομα, δεδομένα in 변형들.items():
        Αρχείο = Κατάλογος_τιμή / (Όνομα + '.elf'); Αρχείο.write_bytes(δεδομένα)
        항목들.append(Όνομα + '=' + str(Αρχείο))
    subprocess.run([sys.executable, str(Θέση / 'Εργαλεία/συνδέω_τελικό_σημείο_bbe6b410.py'), '-o', str(Κατάλογος_τιμή / 'apps.bin')] + 항목들, check=True)
    ΠΗΓΗ = Κατάλογος_τιμή / 'apps.s'
    ΠΗΓΗ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Κατάλογος_τιμή / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Κατάλογος_τιμή / 'apps.o'), str(ΠΗΓΗ)], check=True)
    πυρήνας_τιμή = Κατάλογος_τιμή / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Θέση / '부팅/συνδέω_Διάταξη.ld'), '-o', str(πυρήνας_τιμή),
                    str(Θέση / 'build/boot.o'), str(Θέση / 'build/java.o'), str(Θέση / 'build/user.o'), str(Κατάλογος_τιμή / 'apps.o')], check=True)
    return πυρήνας_τιμή


def εκτελώ_εντολή():
    μέτρηση = {}
    διακομιστής_τιμή = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    διακομιστής_τιμή.bind(('127.0.0.1', 0))
    διακομιστής_τιμή.settimeout(0.1)
    θύρα_τιμή = διακομιστής_τιμή.getsockname()[1]
    받은것 = []
    Έξοδος_εφαρμογή = threading.Event()
    def ηχώ_απαντώ():
        while not Έξοδος_εφαρμογή.is_set():
            try: δεδομένα, ομότιμος_τιμή = διακομιστής_τιμή.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(δεδομένα)
            if δεδομένα != b'drop-me': διακομιστής_τιμή.sendto(δεδομένα, ομότιμος_τιμή)
    일꾼 = threading.Thread(target=ηχώ_απαντώ, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                υπολογιστής_5eb260fa.Εντολή('apps', ['hello', 'udp', 'netcheck', 'stress'])
                υπολογιστής_5eb260fa.Εντολή('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                υπολογιστής_5eb260fa.Εντολή('run missing', ['Exit: -2'])
                υπολογιστής_5eb260fa.Εντολή('net', ['NET RTL8139'])
                υπολογιστής_5eb260fa.Εντολή('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Περιεχόμενο_τιμή in ('hello-network', 'odd', 'even', 'repeat-123'):
                    υπολογιστής_5eb260fa.Εντολή('run udp 10.0.2.2 {} {}'.format(θύρα_τιμή, Περιεχόμενο_τιμή), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Περιεχόμενο_τιμή.encode() in 받은것, 'φιλοξενώ 서버에서 자료를 받지 못함'
                υπολογιστής_5eb260fa.Εντολή('run stress {}'.format(θύρα_τιμή), ['UDP STRESS PASS', 'Exit: 0'])
                υπολογιστής_5eb260fa.Εντολή('run udp 10.0.2.2 {} drop-me'.format(θύρα_τιμή), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                υπολογιστής_5eb260fa.Εντολή('run hello recovered', ['arg: recovered', 'Exit: 0'])
                μέτρηση[종류] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode('utf-8', 'replace')
                print('PASS: {} χρήστης ELF/ring 3/Παράμετροι/UDP φιλοξενώ 왕복/τιμή_ώρας 초과/κέλυφος 복귀'.format(종류), flush=True)
            finally:
                try: υπολογιστής_5eb260fa.Εντολή('net', [])
                except Exception: pass
                (Θέση / 'build/사용자통신-last.log').write_bytes(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
                υπολογιστής_5eb260fa.Κλείσιμο()
        υπολογιστής_5eb260fa = εικονική_μηχανή(Θέση / 'build/kernel.elf', δίκτυο_τιμή=False)
        try:
            υπολογιστής_5eb260fa.Εντολή('net', ['NET unavailable'])
            υπολογιστής_5eb260fa.Εντολή('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            υπολογιστής_5eb260fa.Εντολή('run hello', ['USER MODE ring 3', 'Exit: 0'])
            μέτρηση['no_nic'] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode()
        finally: υπολογιστής_5eb260fa.Κλείσιμο()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            υπολογιστής_5eb260fa = εικονική_μηχανή(보호커널(Path(임시)), δίκτυο_τιμή=False)
            try:
                for Όνομα, Κατάσταση_τιμή in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    υπολογιστής_5eb260fa.Εντολή('run ' + Όνομα, ['Exit: ' + str(Κατάσταση_τιμή)])
                    υπολογιστής_5eb260fa.Εντολή('run hello', ['USER MODE ring 3', 'Exit: 0'])
                μέτρηση['protection'] = υπολογιστής_5eb260fa.καταγράφω_ρεκόρ.decode()
                print('PASS: χρήστης Μνήμη_δεδομένα/υλικό_θύρα 격리, 잘못된 δείκτης/ELF, CPU εξαίρεση, 무한 επανάληψη_τιμή 제한', flush=True)
            finally:
                (Θέση / 'build/Προστασία_δοκιμή-last.log').write_bytes(υπολογιστής_5eb260fa.καταγράφω_ρεκόρ)
                υπολογιστής_5eb260fa.Κλείσιμο()
    finally:
        Έξοδος_εφαρμογή.set()
        일꾼.join(timeout=2)
        διακομιστής_τιμή.close()
    μέτρηση['host_udp_received'] = [{'length': len(δεδομένα), 'sha256': hashlib.sha256(δεδομένα).hexdigest()} for δεδομένα in 받은것]
    (Θέση / 'build/δοκιμή_χρήστης_δίκτυο.json').write_text(json.dumps(μέτρηση, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    εκτελώ_εντολή()
