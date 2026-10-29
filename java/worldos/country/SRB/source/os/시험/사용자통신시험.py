#!/usr/bin/env python3
"""стваран_подаци ring 3 ELF/хост UDP 왕복/заштитити_вриједност ГРЕШКА/време_вриједност 제한/잘못된 ELF를 검증한다."""
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

Положај = Path(__file__).resolve().parents[1]


class виртуелно_рачунар:
    def __init__(self, ПУТАЊА, 종류='elf', Мрежа_вриједност=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        именик_вриједност = Path(self.임시.name)
        self.евиденција_ред = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_вриједност = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_пут = именик_вриједност / 'serial.sock', именик_вриједност / 'monitor.sock'
        Наредба = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_пут) + ',server,nowait']
        Наредба += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Мрежа_вриједност else ['-net', 'none']
        Наредба += ['-kernel', str(ПУТАЊА)] if 종류 == 'elf' else ['-cdrom', str(ПУТАЊА), '-boot', 'd']
        if 저장매체 is not None:
            Наредба += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Процес_вриједност = subprocess.Popen(Наредба, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_пут.exists()):
                if self.Процес_вриједност.poll() is not None:
                    raise AssertionError(self.Процес_вриједност.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Покрени време_вриједност 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_вриједност.connect(str(монитор_пут))
            self.직렬.setblocking(False)
            self.монитор_вриједност.sendall(b'cont\n')
            self.чекај_стање('jkoros> ')
        except BaseException:
            self.Затворен()
            raise

    def чекај_стање(self, 문구, Покрени=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.евиденција_ред[Покрени:]:
                return self.евиденција_ред[Покрени:].decode('utf-8', 'replace')
            Чита, _, _ = select.select([self.직렬], [], [], 0.1)
            if Чита:
                подаци = self.직렬.recv(65536)
                if not подаци: break
                self.евиденција_ред.extend(подаци)
            if self.Процес_вриједност.poll() is not None: break
        raise AssertionError('чекај_вриједност неуспјех_вриједност: ' + 문구 + '\n' + self.евиденција_ред.decode('utf-8', 'replace'))

    def Наредба(self, ниска_вриједност, 기대):
        Покрени = len(self.евиденција_ред)
        self.직렬.sendall((ниска_вриједност + '\n').encode())
        ИСХОД = self.чекај_стање('jkoros> ', Покрени)
        for 문구 in 기대:
            assert 문구 in ИСХОД, (ниска_вриједност, 문구, ИСХОД)
        assert 'PANIC' not in ИСХОД, ИСХОД
        return ИСХОД

    def Затворен(self):
        self.직렬.close()
        self.монитор_вриједност.close()
        if self.Процес_вриједност.poll() is None:
            self.Процес_вриједност.terminate()
            try: self.Процес_вриједност.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Процес_вриједност.kill()
                self.Процес_вриједност.wait()
        self.Процес_вриједност.communicate()
        self.임시.cleanup()


def 보호커널(именик_вриједност):
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
    항목들 = ['hello=' + str(Положај / 'build/apps/hello.elf')]
    for Назив, Садржај_вриједност in 사례들.items():
        ИЗВОР = именик_вриједност / (Назив + '.s')
        ИЗВОР.write_text('.code32\n.text\n.globl _start\n_start:\n' + Садржај_вриједност +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(именик_вриједност / (Назив + '.o')), str(ИЗВОР)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Положај.parent / 'compiler/корисник_Веза_изглед.ld'),
                        '-o', str(именик_вриједност / (Назив + '.elf')), str(именик_вриједност / (Назив + '.o'))], check=True)
        항목들.append(Назив + '=' + str(именик_вриједност / (Назив + '.elf')))
    정상 = bytearray((Положај / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    неважеће_мера = bytearray(정상); неважеће_мера[0] = 0; 변형들['badelf'] = неважеће_мера
    неважеће_мера = bytearray(정상); struct.pack_into('<I', неважеће_мера, 24, 0x00100000); 변형들['badentry'] = неважеће_мера
    неважеће_мера = bytearray(정상); struct.pack_into('<I', неважеће_мера, 28, 0x7fffffff); 변형들['badtable'] = неважеће_мера
    неважеће_мера = bytearray(정상); Претрага_табела = struct.unpack_from('<I', неважеће_мера, 28)[0]
    struct.pack_into('<I', неважеће_мера, Претрага_табела + 20, 0x7fffffff); 변형들['badsize'] = неважеће_мера
    for Назив, подаци in 변형들.items():
        Датотека = именик_вриједност / (Назив + '.elf'); Датотека.write_bytes(подаци)
        항목들.append(Назив + '=' + str(Датотека))
    subprocess.run([sys.executable, str(Положај / 'Алатке/повезати_крајња_тачка.py'), '-o', str(именик_вриједност / 'apps.bin')] + 항목들, check=True)
    ИЗВОР = именик_вриједност / 'apps.s'
    ИЗВОР.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(именик_вриједност / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(именик_вриједност / 'apps.o'), str(ИЗВОР)], check=True)
    језгро_вриједност = именик_вриједност / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Положај / '부팅/Веза_изглед.ld'), '-o', str(језгро_вриједност),
                    str(Положај / 'build/boot.o'), str(Положај / 'build/java.o'), str(Положај / 'build/user.o'), str(именик_вриједност / 'apps.o')], check=True)
    return језгро_вриједност


def Изврши_команда():
    ИСХОД = {}
    сервер_вриједност = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_вриједност.bind(('127.0.0.1', 0))
    сервер_вриједност.settimeout(0.1)
    порт_вриједност = сервер_вриједност.getsockname()[1]
    받은것 = []
    Излаз_програм = threading.Event()
    def 되보내기():
        while not Излаз_програм.is_set():
            try: подаци, 상대 = сервер_вриједност.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(подаци)
            if подаци != b'drop-me': сервер_вриједност.sendto(подаци, 상대)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            рачунар = виртуелно_рачунар(Положај / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                рачунар.Наредба('apps', ['hello', 'udp', 'netcheck', 'stress'])
                рачунар.Наредба('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                рачунар.Наредба('run missing', ['Exit: -2'])
                рачунар.Наредба('net', ['NET RTL8139'])
                рачунар.Наредба('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Садржај_вриједност in ('hello-network', 'odd', 'even', 'repeat-123'):
                    рачунар.Наредба('run udp 10.0.2.2 {} {}'.format(порт_вриједност, Садржај_вриједност), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Садржај_вриједност.encode() in 받은것, 'хост 서버에서 자료를 받지 못함'
                рачунар.Наредба('run stress {}'.format(порт_вриједност), ['UDP STRESS PASS', 'Exit: 0'])
                рачунар.Наредба('run udp 10.0.2.2 {} drop-me'.format(порт_вриједност), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                рачунар.Наредба('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ИСХОД[종류] = рачунар.евиденција_ред.decode('utf-8', 'replace')
                print('PASS: {} корисник ELF/ring 3/Аргументи/UDP хост 왕복/време_вриједност 초과/љуска 복귀'.format(종류), flush=True)
            finally:
                try: рачунар.Наредба('net', [])
                except Exception: pass
                (Положај / 'build/사용자통신-last.log').write_bytes(рачунар.евиденција_ред)
                рачунар.Затворен()
        рачунар = виртуелно_рачунар(Положај / 'build/kernel.elf', Мрежа_вриједност=False)
        try:
            рачунар.Наредба('net', ['NET unavailable'])
            рачунар.Наредба('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            рачунар.Наредба('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ИСХОД['no_nic'] = рачунар.евиденција_ред.decode()
        finally: рачунар.Затворен()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            рачунар = виртуелно_рачунар(보호커널(Path(임시)), Мрежа_вриједност=False)
            try:
                for Назив, стање_вриједност in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    рачунар.Наредба('run ' + Назив, ['Exit: ' + str(стање_вриједност)])
                    рачунар.Наредба('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ИСХОД['protection'] = рачунар.евиденција_ред.decode()
                print('PASS: корисник Меморија_подаци/포트 격리, 잘못된 показивач/ELF, CPU изузетак, 무한 спринт_вриједност 제한', flush=True)
            finally:
                (Положај / 'build/보호시험-last.log').write_bytes(рачунар.евиденција_ред)
                рачунар.Затворен()
    finally:
        Излаз_програм.set()
        일꾼.join(timeout=2)
        сервер_вриједност.close()
    ИСХОД['host_udp_received'] = [{'length': len(подаци), 'sha256': hashlib.sha256(подаци).hexdigest()} for подаци in 받은것]
    (Положај / 'build/사용자통신시험.json').write_text(json.dumps(ИСХОД, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Изврши_команда()
