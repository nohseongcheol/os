#!/usr/bin/env python3
"""фактик_мәгълүмат ring 3 ELF/хост UDP 왕복/саклау_VALUE Хата/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

урнаштыру = Path(__file__).resolve().parents[1]


class виртуаль_машина:
    def __init__(self, Yul, 종류='elf', Челтәр_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        каталог_VALUE = Path(self.임시.name)
        self.LOG_юл = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_юл = каталог_VALUE / 'serial.sock', каталог_VALUE / 'monitor.sock'
        команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_юл) + ',server,nowait']
        команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Челтәр_VALUE else ['-net', 'none']
        команда += ['-kernel', str(Yul)] if 종류 == 'elf' else ['-cdrom', str(Yul), '-boot', 'd']
        if 저장매체 is not None:
            команда += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Процесс_VALUE = subprocess.Popen(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_юл.exists()):
                if self.Процесс_VALUE.poll() is not None:
                    raise AssertionError(self.Процесс_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU эшләтү TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_VALUE.connect(str(монитор_юл))
            self.직렬.setblocking(False)
            self.монитор_VALUE.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Yap()
            raise

    def 기다림(self, 문구, эшләтү=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_юл[эшләтү:]:
                return self.LOG_юл[эшләтү:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                мәгълүмат = self.직렬.recv(65536)
                if not мәгълүмат: break
                self.LOG_юл.extend(мәгълүмат)
            if self.Процесс_VALUE.poll() is not None: break
        raise AssertionError('대기 эштән_туктау_VALUE: ' + 문구 + '\n' + self.LOG_юл.decode('utf-8', 'replace'))

    def команда(self, юл_VALUE_6ca8363c, 기대):
        эшләтү = len(self.LOG_юл)
        self.직렬.sendall((юл_VALUE_6ca8363c + '\n').encode())
        үлчәм = self.기다림('jkoros> ', эшләтү)
        for 문구 in 기대:
            assert 문구 in үлчәм, (юл_VALUE_6ca8363c, 문구, үлчәм)
        assert 'PANIC' not in үлчәм, үлчәм
        return үлчәм

    def Yap(self):
        self.직렬.close()
        self.монитор_VALUE.close()
        if self.Процесс_VALUE.poll() is None:
            self.Процесс_VALUE.terminate()
            try: self.Процесс_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Процесс_VALUE.kill()
                self.Процесс_VALUE.wait()
        self.Процесс_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(каталог_VALUE):
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
    항목들 = ['hello=' + str(урнаштыру / 'build/apps/hello.elf')]
    for исем, Эчтәлек_VALUE in 사례들.items():
        чыганак = каталог_VALUE / (исем + '.s')
        чыганак.write_text('.code32\n.text\n.globl _start\n_start:\n' + Эчтәлек_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(каталог_VALUE / (исем + '.o')), str(чыганак)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(урнаштыру.parent / 'compiler/кулланучы_бәйләү_план.ld'),
                        '-o', str(каталог_VALUE / (исем + '.elf')), str(каталог_VALUE / (исем + '.o'))], check=True)
        항목들.append(исем + '=' + str(каталог_VALUE / (исем + '.elf')))
    정상 = bytearray((урнаштыру / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    дөрес_булмаган_үлчәм = bytearray(정상); дөрес_булмаган_үлчәм[0] = 0; 변형들['badelf'] = дөрес_булмаган_үлчәм
    дөрес_булмаган_үлчәм = bytearray(정상); struct.pack_into('<I', дөрес_булмаган_үлчәм, 24, 0x00100000); 변형들['badentry'] = дөрес_булмаган_үлчәм
    дөрес_булмаган_үлчәм = bytearray(정상); struct.pack_into('<I', дөрес_булмаган_үлчәм, 28, 0x7fffffff); 변형들['badtable'] = дөрес_булмаган_үлчәм
    дөрес_булмаган_үлчәм = bytearray(정상); Эзләү_таблица = struct.unpack_from('<I', дөрес_булмаган_үлчәм, 28)[0]
    struct.pack_into('<I', дөрес_булмаган_үлчәм, Эзләү_таблица + 20, 0x7fffffff); 변형들['badsize'] = дөрес_булмаган_үлчәм
    for исем, мәгълүмат in 변형들.items():
        Birem = каталог_VALUE / (исем + '.elf'); Birem.write_bytes(мәгълүмат)
        항목들.append(исем + '=' + str(Birem))
    subprocess.run([sys.executable, str(урнаштыру / 'Кораллар/묶기.py'), '-o', str(каталог_VALUE / 'apps.bin')] + 항목들, check=True)
    чыганак = каталог_VALUE / 'apps.s'
    чыганак.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(каталог_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(каталог_VALUE / 'apps.o'), str(чыганак)], check=True)
    төш_VALUE = каталог_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(урнаштыру / '부팅/бәйләү_план.ld'), '-o', str(төш_VALUE),
                    str(урнаштыру / 'build/boot.o'), str(урнаштыру / 'build/java.o'), str(урнаштыру / 'build/user.o'), str(каталог_VALUE / 'apps.o')], check=True)
    return төш_VALUE


def үтәргә_команда():
    үлчәм = {}
    сервер_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_VALUE.bind(('127.0.0.1', 0))
    сервер_VALUE.settimeout(0.1)
    порт_VALUE = сервер_VALUE.getsockname()[1]
    RECEIVED_элемент = []
    Чыгу_кушымта = threading.Event()
    def 되보내기():
        while not Чыгу_кушымта.is_set():
            try: мәгълүмат, тиңдәш_VALUE = сервер_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_элемент.append(мәгълүмат)
            if мәгълүмат != b'drop-me': сервер_VALUE.sendto(мәгълүмат, тиңдәш_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуаль_машина(урнаштыру / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                машина.команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                машина.команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                машина.команда('run missing', ['Exit: -2'])
                машина.команда('net', ['NET RTL8139'])
                машина.команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Эчтәлек_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    машина.команда('run udp 10.0.2.2 {} {}'.format(порт_VALUE, Эчтәлек_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Эчтәлек_VALUE.encode() in RECEIVED_элемент, 'хост 서버에서 자료를 받지 못함'
                машина.команда('run stress {}'.format(порт_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                машина.команда('run udp 10.0.2.2 {} drop-me'.format(порт_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                машина.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                үлчәм[종류] = машина.LOG_юл.decode('utf-8', 'replace')
                print('PASS: {} кулланучы ELF/ring 3/인수/UDP хост 왕복/TIME_VALUE 초과/тышча 복귀'.format(종류), flush=True)
            finally:
                try: машина.команда('net', [])
                except Exception: pass
                (урнаштыру / 'build/사용자통신-last.log').write_bytes(машина.LOG_юл)
                машина.Yap()
        машина = виртуаль_машина(урнаштыру / 'build/kernel.elf', Челтәр_VALUE=False)
        try:
            машина.команда('net', ['NET unavailable'])
            машина.команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            машина.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            үлчәм['no_nic'] = машина.LOG_юл.decode()
        finally: машина.Yap()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            машина = виртуаль_машина(보호커널(Path(임시)), Челтәр_VALUE=False)
            try:
                for исем, халәт_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    машина.команда('run ' + исем, ['Exit: ' + str(халәт_VALUE)])
                    машина.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                үлчәм['protection'] = машина.LOG_юл.decode()
                print('PASS: кулланучы Хәтер_мәгълүмат/포트 격리, 잘못된 күрсәткеч/ELF, CPU 예외, 무한 итерация_VALUE 제한', flush=True)
            finally:
                (урнаштыру / 'build/보호시험-last.log').write_bytes(машина.LOG_юл)
                машина.Yap()
    finally:
        Чыгу_кушымта.set()
        일꾼.join(timeout=2)
        сервер_VALUE.close()
    үлчәм['host_udp_received'] = [{'length': len(мәгълүмат), 'sha256': hashlib.sha256(мәгълүмат).hexdigest()} for мәгълүмат in RECEIVED_элемент]
    (урнаштыру / 'build/사용자통신시험.json').write_text(json.dumps(үлчәм, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    үтәргә_команда()
