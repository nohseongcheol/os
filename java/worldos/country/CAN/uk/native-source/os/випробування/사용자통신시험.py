#!/usr/bin/env python3
"""фактично_дані ring 3 ELF/хост UDP 왕복/захищати_значення ПОМИЛКА/час_значення 제한/잘못된 ELF를 검증한다."""
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

позиція = Path(__file__).resolve().parents[1]


class ВМ:
    def __init__(self, шлях, 종류='elf', мережа_значення=True, місце_носій=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Каталог_значення = Path(self.임시.name)
        self.журнал_запис = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монітор_значення = socket.socket(socket.AF_UNIX)
        직렬경로, монітор_шлях = Каталог_значення / 'serial.sock', Каталог_значення / 'monitor.sock'
        команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монітор_шлях) + ',server,nowait']
        команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if мережа_значення else ['-net', 'none']
        команда += ['-kernel', str(шлях)] if 종류 == 'elf' else ['-cdrom', str(шлях), '-boot', 'd']
        if місце_носій is not None:
            команда += ['-drive', 'file=' + str(місце_носій) + ',format=raw,if=ide,index=0']
        self.процес_значення = subprocess.Popen(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монітор_шлях.exists()):
                if self.процес_значення.poll() is not None:
                    raise AssertionError(self.процес_значення.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU запустити час_значення 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монітор_значення.connect(str(монітор_шлях))
            self.직렬.setblocking(False)
            self.монітор_значення.sendall(b'cont\n')
            self.стан_очікування('jkoros> ')
        except BaseException:
            self.Закрити()
            raise

    def стан_очікування(self, 문구, запустити=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.журнал_запис[запустити:]:
                return self.журнал_запис[запустити:].decode('utf-8', 'replace')
            Читання, _, _ = select.select([self.직렬], [], [], 0.1)
            if Читання:
                дані = self.직렬.recv(65536)
                if not дані: break
                self.журнал_запис.extend(дані)
            if self.процес_значення.poll() is not None: break
        raise AssertionError('хвилиноньку_панове_значення неполадка_значення: ' + 문구 + '\n' + self.журнал_запис.decode('utf-8', 'replace'))

    def команда(self, рядок_значення, 기대):
        запустити = len(self.журнал_запис)
        self.직렬.sendall((рядок_значення + '\n').encode())
        результат = self.стан_очікування('jkoros> ', запустити)
        for 문구 in 기대:
            assert 문구 in результат, (рядок_значення, 문구, результат)
        assert 'PANIC' not in результат, результат
        return результат

    def Закрити(self):
        self.직렬.close()
        self.монітор_значення.close()
        if self.процес_значення.poll() is None:
            self.процес_значення.terminate()
            try: self.процес_значення.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.процес_значення.kill()
                self.процес_значення.wait()
        self.процес_значення.communicate()
        self.임시.cleanup()


def 보호커널(Каталог_значення):
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
    항목들 = ['hello=' + str(позиція / 'build/apps/hello.elf')]
    for Назва, Вміст_значення in 사례들.items():
        вихіднийКод = Каталог_значення / (Назва + '.s')
        вихіднийКод.write_text('.code32\n.text\n.globl _start\n_start:\n' + Вміст_значення +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Каталог_значення / (Назва + '.o')), str(вихіднийКод)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(позиція.parent / 'compiler/користувач_зв_язок_Макет.ld'),
                        '-o', str(Каталог_значення / (Назва + '.elf')), str(Каталог_значення / (Назва + '.o'))], check=True)
        항목들.append(Назва + '=' + str(Каталог_значення / (Назва + '.elf')))
    정상 = bytearray((позиція / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    недійсний_КР = bytearray(정상); недійсний_КР[0] = 0; 변형들['badelf'] = недійсний_КР
    недійсний_КР = bytearray(정상); struct.pack_into('<I', недійсний_КР, 24, 0x00100000); 변형들['badentry'] = недійсний_КР
    недійсний_КР = bytearray(정상); struct.pack_into('<I', недійсний_КР, 28, 0x7fffffff); 변형들['badtable'] = недійсний_КР
    недійсний_КР = bytearray(정상); таблиця_підстановки = struct.unpack_from('<I', недійсний_КР, 28)[0]
    struct.pack_into('<I', недійсний_КР, таблиця_підстановки + 20, 0x7fffffff); 변형들['badsize'] = недійсний_КР
    for Назва, дані in 변형들.items():
        файл = Каталог_значення / (Назва + '.elf'); файл.write_bytes(дані)
        항목들.append(Назва + '=' + str(файл))
    subprocess.run([sys.executable, str(позиція / 'інструменти/зв_язувати_учасник.py'), '-o', str(Каталог_значення / 'apps.bin')] + 항목들, check=True)
    вихіднийКод = Каталог_значення / 'apps.s'
    вихіднийКод.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Каталог_значення / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Каталог_значення / 'apps.o'), str(вихіднийКод)], check=True)
    ядро_значення = Каталог_значення / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(позиція / 'запуск_машини/схема_компонування.ld'), '-o', str(ядро_значення),
                    str(позиція / 'build/boot.o'), str(позиція / 'build/java.o'), str(позиція / 'build/user.o'), str(Каталог_значення / 'apps.o')], check=True)
    return ядро_значення


def Виконати_команда():
    результат = {}
    сервер_значення = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_значення.bind(('127.0.0.1', 0))
    сервер_значення.settimeout(0.1)
    порт_значення = сервер_значення.getsockname()[1]
    받은것 = []
    Вийти_програма = threading.Event()
    def відлуння_відповідь():
        while not Вийти_програма.is_set():
            try: дані, точка_значення = сервер_значення.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(дані)
            if дані != b'drop-me': сервер_значення.sendto(дані, точка_значення)
    일꾼 = threading.Thread(target=відлуння_відповідь, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            комп_ютер = ВМ(позиція / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                комп_ютер.команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                комп_ютер.команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                комп_ютер.команда('run missing', ['Exit: -2'])
                комп_ютер.команда('net', ['NET RTL8139'])
                комп_ютер.команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Вміст_значення in ('hello-network', 'odd', 'even', 'repeat-123'):
                    комп_ютер.команда('run udp 10.0.2.2 {} {}'.format(порт_значення, Вміст_значення), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Вміст_значення.encode() in 받은것, 'хост 서버에서 자료를 받지 못함'
                комп_ютер.команда('run stress {}'.format(порт_значення), ['UDP STRESS PASS', 'Exit: 0'])
                комп_ютер.команда('run udp 10.0.2.2 {} drop-me'.format(порт_значення), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                комп_ютер.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                результат[종류] = комп_ютер.журнал_запис.decode('utf-8', 'replace')
                print('PASS: {} простір_користувача ELF/ring 3/аргументи/UDP хост 왕복/час_значення 초과/оболонка 복귀'.format(종류), flush=True)
            finally:
                try: комп_ютер.команда('net', [])
                except Exception: pass
                (позиція / 'build/사용자통신-last.log').write_bytes(комп_ютер.журнал_запис)
                комп_ютер.Закрити()
        комп_ютер = ВМ(позиція / 'build/kernel.elf', мережа_значення=False)
        try:
            комп_ютер.команда('net', ['NET unavailable'])
            комп_ютер.команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            комп_ютер.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            результат['no_nic'] = комп_ютер.журнал_запис.decode()
        finally: комп_ютер.Закрити()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            комп_ютер = ВМ(보호커널(Path(임시)), мережа_значення=False)
            try:
                for Назва, Стан_значення in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    комп_ютер.команда('run ' + Назва, ['Exit: ' + str(Стан_значення)])
                    комп_ютер.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                результат['protection'] = комп_ютер.журнал_запис.decode()
                print('PASS: простір_користувача Пам_ять_дані/обладнання_порт 격리, 잘못된 курсор/ELF, CPU виняток, 무한 спринт_значення 제한', flush=True)
            finally:
                (позиція / 'build/보호시험-last.log').write_bytes(комп_ютер.журнал_запис)
                комп_ютер.Закрити()
    finally:
        Вийти_програма.set()
        일꾼.join(timeout=2)
        сервер_значення.close()
    результат['host_udp_received'] = [{'length': len(дані), 'sha256': hashlib.sha256(дані).hexdigest()} for дані in 받은것]
    (позиція / 'build/사용자통신시험.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Виконати_команда()
