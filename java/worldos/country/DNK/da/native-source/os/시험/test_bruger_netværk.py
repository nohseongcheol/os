#!/usr/bin/env python3
"""faktisk_data ring 3 ELF/vært UDP 왕복/beskytte_VÆRDI fejl/TID_VÆRDI 제한/잘못된 ELF를 검증한다."""
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

Placering = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, Sti, 종류='elf', netværk_VÆRDI=True, Lager_medie=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        mappe_VÆRDI = Path(self.임시.name)
        self.LOG_post = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.monitor_VÆRDI = socket.socket(socket.AF_UNIX)
        직렬경로, monitor_sti = mappe_VÆRDI / 'serial.sock', mappe_VÆRDI / 'monitor.sock'
        Kommando = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(monitor_sti) + ',server,nowait']
        Kommando += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if netværk_VÆRDI else ['-net', 'none']
        Kommando += ['-kernel', str(Sti)] if 종류 == 'elf' else ['-cdrom', str(Sti), '-boot', 'd']
        if Lager_medie is not None:
            Kommando += ['-drive', 'file=' + str(Lager_medie) + ',format=raw,if=ide,index=0']
        self.Proces_VÆRDI = subprocess.Popen(Kommando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and monitor_sti.exists()):
                if self.Proces_VÆRDI.poll() is not None:
                    raise AssertionError(self.Proces_VÆRDI.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Kør_2 TID_VÆRDI 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.monitor_VÆRDI.connect(str(monitor_sti))
            self.직렬.setblocking(False)
            self.monitor_VÆRDI.sendall(b'cont\n')
            self.ventetilstand('jkoros> ')
        except BaseException:
            self.Luk()
            raise

    def ventetilstand(self, 문구, Kør_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_post[Kør_2:]:
                return self.LOG_post[Kør_2:].decode('utf-8', 'replace')
            Læse, _, _ = select.select([self.직렬], [], [], 0.1)
            if Læse:
                data = self.직렬.recv(65536)
                if not data: break
                self.LOG_post.extend(data)
            if self.Proces_VÆRDI.poll() is not None: break
        raise AssertionError('vent_VÆRDI fejl_VÆRDI: ' + 문구 + '\n' + self.LOG_post.decode('utf-8', 'replace'))

    def Kommando(self, streng_VÆRDI, 기대):
        Kør_2 = len(self.LOG_post)
        self.직렬.sendall((streng_VÆRDI + '\n').encode())
        KR = self.ventetilstand('jkoros> ', Kør_2)
        for 문구 in 기대:
            assert 문구 in KR, (streng_VÆRDI, 문구, KR)
        assert 'PANIC' not in KR, KR
        return KR

    def Luk(self):
        self.직렬.close()
        self.monitor_VÆRDI.close()
        if self.Proces_VÆRDI.poll() is None:
            self.Proces_VÆRDI.terminate()
            try: self.Proces_VÆRDI.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Proces_VÆRDI.kill()
                self.Proces_VÆRDI.wait()
        self.Proces_VÆRDI.communicate()
        self.임시.cleanup()


def 보호커널(mappe_VÆRDI):
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
    항목들 = ['hello=' + str(Placering / 'build/apps/hello.elf')]
    for Navn, Indhold_VÆRDI in 사례들.items():
        KILDE = mappe_VÆRDI / (Navn + '.s')
        KILDE.write_text('.code32\n.text\n.globl _start\n_start:\n' + Indhold_VÆRDI +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(mappe_VÆRDI / (Navn + '.o')), str(KILDE)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Placering.parent / 'compiler/bruger_Link_Layout.ld'),
                        '-o', str(mappe_VÆRDI / (Navn + '.elf')), str(mappe_VÆRDI / (Navn + '.o'))], check=True)
        항목들.append(Navn + '=' + str(mappe_VÆRDI / (Navn + '.elf')))
    it_normal = bytearray((Placering / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ugyldig_KR = bytearray(it_normal); ugyldig_KR[0] = 0; 변형들['badelf'] = ugyldig_KR
    ugyldig_KR = bytearray(it_normal); struct.pack_into('<I', ugyldig_KR, 24, 0x00100000); 변형들['badentry'] = ugyldig_KR
    ugyldig_KR = bytearray(it_normal); struct.pack_into('<I', ugyldig_KR, 28, 0x7fffffff); 변형들['badtable'] = ugyldig_KR
    ugyldig_KR = bytearray(it_normal); Opslag_tabel = struct.unpack_from('<I', ugyldig_KR, 28)[0]
    struct.pack_into('<I', ugyldig_KR, Opslag_tabel + 20, 0x7fffffff); 변형들['badsize'] = ugyldig_KR
    for Navn, data in 변형들.items():
        Fil = mappe_VÆRDI / (Navn + '.elf'); Fil.write_bytes(data)
        항목들.append(Navn + '=' + str(Fil))
    subprocess.run([sys.executable, str(Placering / 'Værktøjer/BIND_slutpunkt.py'), '-o', str(mappe_VÆRDI / 'apps.bin')] + 항목들, check=True)
    KILDE = mappe_VÆRDI / 'apps.s'
    KILDE.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(mappe_VÆRDI / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(mappe_VÆRDI / 'apps.o'), str(KILDE)], check=True)
    kerne_VÆRDI = mappe_VÆRDI / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Placering / '부팅/Link_Layout.ld'), '-o', str(kerne_VÆRDI),
                    str(Placering / 'build/boot.o'), str(Placering / 'build/java.o'), str(Placering / 'build/user.o'), str(mappe_VÆRDI / 'apps.o')], check=True)
    return kerne_VÆRDI


def Udfør_kommando():
    KR = {}
    server_VÆRDI = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_VÆRDI.bind(('127.0.0.1', 0))
    server_VÆRDI.settimeout(0.1)
    port_VÆRDI = server_VÆRDI.getsockname()[1]
    MODTAGET_VED_UDLØB_vare = []
    Afslut_app = threading.Event()
    def ekko_svar():
        while not Afslut_app.is_set():
            try: data, peer_VÆRDI = server_VÆRDI.recvfrom(4096)
            except socket.timeout: continue
            MODTAGET_VED_UDLØB_vare.append(data)
            if data != b'drop-me': server_VÆRDI.sendto(data, peer_VÆRDI)
    arbejder_VÆRDI = threading.Thread(target=ekko_svar, daemon=True)
    arbejder_VÆRDI.start()
    try:
        for 종류 in ('elf', 'iso'):
            maskine = VM(Placering / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                maskine.Kommando('apps', ['hello', 'udp', 'netcheck', 'stress'])
                maskine.Kommando('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                maskine.Kommando('run missing', ['Exit: -2'])
                maskine.Kommando('net', ['NET RTL8139'])
                maskine.Kommando('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Indhold_VÆRDI in ('hello-network', 'odd', 'even', 'repeat-123'):
                    maskine.Kommando('run udp 10.0.2.2 {} {}'.format(port_VÆRDI, Indhold_VÆRDI), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Indhold_VÆRDI.encode() in MODTAGET_VED_UDLØB_vare, 'vært 서버에서 자료를 받지 못함'
                maskine.Kommando('run stress {}'.format(port_VÆRDI), ['UDP STRESS PASS', 'Exit: 0'])
                maskine.Kommando('run udp 10.0.2.2 {} drop-me'.format(port_VÆRDI), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                maskine.Kommando('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[종류] = maskine.LOG_post.decode('utf-8', 'replace')
                print('PASS: {} bruger ELF/ring 3/Argumenter/UDP vært 왕복/TID_VÆRDI 초과/Shell 복귀'.format(종류), flush=True)
            finally:
                try: maskine.Kommando('net', [])
                except Exception: pass
                (Placering / 'build/사용자통신-last.log').write_bytes(maskine.LOG_post)
                maskine.Luk()
        maskine = VM(Placering / 'build/kernel.elf', netværk_VÆRDI=False)
        try:
            maskine.Kommando('net', ['NET unavailable'])
            maskine.Kommando('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            maskine.Kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
            KR['no_nic'] = maskine.LOG_post.decode()
        finally: maskine.Luk()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            maskine = VM(보호커널(Path(임시)), netværk_VÆRDI=False)
            try:
                for Navn, status_VÆRDI in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    maskine.Kommando('run ' + Navn, ['Exit: ' + str(status_VÆRDI)])
                    maskine.Kommando('run hello', ['USER MODE ring 3', 'Exit: 0'])
                KR['protection'] = maskine.LOG_post.decode()
                print('PASS: bruger Hukommelse_data/hardware_port 격리, 잘못된 markør/ELF, CPU undtagelse, 무한 sprint_VÆRDI 제한', flush=True)
            finally:
                (Placering / 'build/Beskyttelse_test-last.log').write_bytes(maskine.LOG_post)
                maskine.Luk()
    finally:
        Afslut_app.set()
        arbejder_VÆRDI.join(timeout=2)
        server_VÆRDI.close()
    KR['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in MODTAGET_VED_UDLØB_vare]
    (Placering / 'build/test_bruger_netværk.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Udfør_kommando()
