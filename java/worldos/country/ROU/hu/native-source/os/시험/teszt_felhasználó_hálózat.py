#!/usr/bin/env python3
"""tényleges_adat ring 3 ELF/gazda UDP 왕복/véd_ÉRTÉK HIBA/IDŐ_ÉRTÉK 제한/잘못된 ELF를 검증한다."""
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

Pozíció = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, ÚTVONAL, Altípus_ÉRTÉK='elf', hálózat_ÉRTÉK=True, tár_Közepes=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        címtár_ÉRTÉK = Path(self.임시.name)
        self.LOG_REKORD = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.figyelő_ÉRTÉK = socket.socket(socket.AF_UNIX)
        직렬경로, figyelő_útvonal = címtár_ÉRTÉK / 'serial.sock', címtár_ÉRTÉK / 'monitor.sock'
        Parancs = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(figyelő_útvonal) + ',server,nowait']
        Parancs += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if hálózat_ÉRTÉK else ['-net', 'none']
        Parancs += ['-kernel', str(ÚTVONAL)] if Altípus_ÉRTÉK == 'elf' else ['-cdrom', str(ÚTVONAL), '-boot', 'd']
        if tár_Közepes is not None:
            Parancs += ['-drive', 'file=' + str(tár_Közepes) + ',format=raw,if=ide,index=0']
        self.folyamat_ÉRTÉK = subprocess.Popen(Parancs, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and figyelő_útvonal.exists()):
                if self.folyamat_ÉRTÉK.poll() is not None:
                    raise AssertionError(self.folyamat_ÉRTÉK.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Futtatás IDŐ_ÉRTÉK 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.figyelő_ÉRTÉK.connect(str(figyelő_útvonal))
            self.직렬.setblocking(False)
            self.figyelő_ÉRTÉK.sendall(b'cont\n')
            self.várakozóállapot('jkoros> ')
        except BaseException:
            self.Bezárás()
            raise

    def várakozóállapot(self, 문구, Futtatás=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_REKORD[Futtatás:]:
                return self.LOG_REKORD[Futtatás:].decode('utf-8', 'replace')
            Olvasás, _, _ = select.select([self.직렬], [], [], 0.1)
            if Olvasás:
                adat = self.직렬.recv(65536)
                if not adat: break
                self.LOG_REKORD.extend(adat)
            if self.folyamat_ÉRTÉK.poll() is not None: break
        raise AssertionError('várj_ÉRTÉK hiba_ÉRTÉK: ' + 문구 + '\n' + self.LOG_REKORD.decode('utf-8', 'replace'))

    def Parancs(self, sztring_ÉRTÉK, 기대):
        Futtatás = len(self.LOG_REKORD)
        self.직렬.sendall((sztring_ÉRTÉK + '\n').encode())
        KR = self.várakozóállapot('jkoros> ', Futtatás)
        for 문구 in 기대:
            assert 문구 in KR, (sztring_ÉRTÉK, 문구, KR)
        assert 'PANIC' not in KR, KR
        return KR

    def Bezárás(self):
        self.직렬.close()
        self.figyelő_ÉRTÉK.close()
        if self.folyamat_ÉRTÉK.poll() is None:
            self.folyamat_ÉRTÉK.terminate()
            try: self.folyamat_ÉRTÉK.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.folyamat_ÉRTÉK.kill()
                self.folyamat_ÉRTÉK.wait()
        self.folyamat_ÉRTÉK.communicate()
        self.임시.cleanup()


def 보호커널(címtár_ÉRTÉK):
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
    항목들 = ['hello=' + str(Pozíció / 'build/apps/hello.elf')]
    for Név, Tartalom_ÉRTÉK in 사례들.items():
        FORRÁS = címtár_ÉRTÉK / (Név + '.s')
        FORRÁS.write_text('.code32\n.text\n.globl _start\n_start:\n' + Tartalom_ÉRTÉK +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(címtár_ÉRTÉK / (Név + '.o')), str(FORRÁS)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozíció.parent / 'compiler/felhasználó_csatol_Navigáció.ld'),
                        '-o', str(címtár_ÉRTÉK / (Név + '.elf')), str(címtár_ÉRTÉK / (Név + '.o'))], check=True)
        항목들.append(Név + '=' + str(címtár_ÉRTÉK / (Név + '.elf')))
    informatikai_részleg_normál = bytearray((Pozíció / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    alaptalan_KR = bytearray(informatikai_részleg_normál); alaptalan_KR[0] = 0; 변형들['badelf'] = alaptalan_KR
    alaptalan_KR = bytearray(informatikai_részleg_normál); struct.pack_into('<I', alaptalan_KR, 24, 0x00100000); 변형들['badentry'] = alaptalan_KR
    alaptalan_KR = bytearray(informatikai_részleg_normál); struct.pack_into('<I', alaptalan_KR, 28, 0x7fffffff); 변형들['badtable'] = alaptalan_KR
    alaptalan_KR = bytearray(informatikai_részleg_normál); keresőtáblázat = struct.unpack_from('<I', alaptalan_KR, 28)[0]
    struct.pack_into('<I', alaptalan_KR, keresőtáblázat + 20, 0x7fffffff); 변형들['badsize'] = alaptalan_KR
    for Név, adat in 변형들.items():
        Fájl = címtár_ÉRTÉK / (Név + '.elf'); Fájl.write_bytes(adat)
        항목들.append(Név + '=' + str(Fájl))
    subprocess.run([sys.executable, str(Pozíció / 'Eszközök/BIND_végpont.py'), '-o', str(címtár_ÉRTÉK / 'apps.bin')] + 항목들, check=True)
    FORRÁS = címtár_ÉRTÉK / 'apps.s'
    FORRÁS.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(címtár_ÉRTÉK / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(címtár_ÉRTÉK / 'apps.o'), str(FORRÁS)], check=True)
    kernel_ÉRTÉK = címtár_ÉRTÉK / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Pozíció / '부팅/csatol_Navigáció.ld'), '-o', str(kernel_ÉRTÉK),
                    str(Pozíció / 'build/boot.o'), str(Pozíció / 'build/java.o'), str(Pozíció / 'build/user.o'), str(címtár_ÉRTÉK / 'apps.o')], check=True)
    return kernel_ÉRTÉK


def végrehajt_parancs():
    KR = {}
    kiszolgáló_ÉRTÉK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    kiszolgáló_ÉRTÉK.bind(('127.0.0.1', 0))
    kiszolgáló_ÉRTÉK.settimeout(0.1)
    port_ÉRTÉK = kiszolgáló_ÉRTÉK.getsockname()[1]
    KAPOTT_cikk = []
    kilép_app = threading.Event()
    def visszhang_válasz():
        while not kilép_app.is_set():
            try: adat, társ_ÉRTÉK = kiszolgáló_ÉRTÉK.recvfrom(4096)
            except socket.timeout: continue
            KAPOTT_cikk.append(adat)
            if adat != b'drop-me': kiszolgáló_ÉRTÉK.sendto(adat, társ_ÉRTÉK)
    dolgozó_ÉRTÉK = threading.Thread(target=visszhang_válasz, daemon=True)
    dolgozó_ÉRTÉK.start()
    try:
        for Altípus_ÉRTÉK in ('elf', 'iso'):
            gép = VM(Pozíció / ('build/kernel.elf' if Altípus_ÉRTÉK == 'elf' else 'build/kernel.iso'), Altípus_ÉRTÉK)
            try:
                gép.Parancs('apps', ['hello', 'udp', 'netcheck', 'stress'])
                gép.Parancs('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                gép.Parancs('run missing', ['Exit: -2'])
                gép.Parancs('net', ['NET RTL8139'])
                gép.Parancs('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Tartalom_ÉRTÉK in ('hello-network', 'odd', 'even', 'repeat-123'):
                    gép.Parancs('run udp 10.0.2.2 {} {}'.format(port_ÉRTÉK, Tartalom_ÉRTÉK), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Tartalom_ÉRTÉK.encode() in KAPOTT_cikk, 'gazda 서버에서 자료를 받지 못함'
                gép.Parancs('run stress {}'.format(port_ÉRTÉK), ['UDP STRESS PASS', 'Exit: 0'])
                gép.Parancs('run udp 10.0.2.2 {} drop-me'.format(port_ÉRTÉK), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                gép.Parancs('run hello recovered', ['arg: recovered', 'Exit: 0'])
                KR[Altípus_ÉRTÉK] = gép.LOG_REKORD.decode('utf-8', 'replace')
                print('PASS: {} felhasználó ELF/ring 3/Argumentumok/UDP gazda 왕복/IDŐ_ÉRTÉK 초과/felület 복귀'.format(Altípus_ÉRTÉK), flush=True)
            finally:
                try: gép.Parancs('net', [])
                except Exception: pass
                (Pozíció / 'build/사용자통신-last.log').write_bytes(gép.LOG_REKORD)
                gép.Bezárás()
        gép = VM(Pozíció / 'build/kernel.elf', hálózat_ÉRTÉK=False)
        try:
            gép.Parancs('net', ['NET unavailable'])
            gép.Parancs('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            gép.Parancs('run hello', ['USER MODE ring 3', 'Exit: 0'])
            KR['no_nic'] = gép.LOG_REKORD.decode()
        finally: gép.Bezárás()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            gép = VM(보호커널(Path(임시)), hálózat_ÉRTÉK=False)
            try:
                for Név, Állapot_ÉRTÉK in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    gép.Parancs('run ' + Név, ['Exit: ' + str(Állapot_ÉRTÉK)])
                    gép.Parancs('run hello', ['USER MODE ring 3', 'Exit: 0'])
                KR['protection'] = gép.LOG_REKORD.decode()
                print('PASS: felhasználó Memória_adat/hardver_port 격리, 잘못된 mutató/ELF, CPU kivétel, 무한 futam_ÉRTÉK 제한', flush=True)
            finally:
                (Pozíció / 'build/Védelem_teszt-last.log').write_bytes(gép.LOG_REKORD)
                gép.Bezárás()
    finally:
        kilép_app.set()
        dolgozó_ÉRTÉK.join(timeout=2)
        kiszolgáló_ÉRTÉK.close()
    KR['host_udp_received'] = [{'length': len(adat), 'sha256': hashlib.sha256(adat).hexdigest()} for adat in KAPOTT_cikk]
    (Pozíció / 'build/teszt_felhasználó_hálózat.json').write_text(json.dumps(KR, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    végrehajt_parancs()
