#!/usr/bin/env python3
"""фактический_данные ring 3 ELF/узел UDP 왕복/защитить_ЗНАЧЕН ошибка/значение_времени 제한/잘못된 ELF를 검증한다."""
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

позиция = Path(__file__).resolve().parents[1]


class VM:
    def __init__(self, путь, Вид_ЗНАЧЕН='elf', сеть_ЗНАЧЕН=True, Память_средний=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Каталог_ЗНАЧЕН = Path(self.임시.name)
        self.LOG_ЗАПИСЬ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_ЗНАЧЕН = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_путь = Каталог_ЗНАЧЕН / 'serial.sock', Каталог_ЗНАЧЕН / 'monitor.sock'
        команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_путь) + ',server,nowait']
        команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if сеть_ЗНАЧЕН else ['-net', 'none']
        команда += ['-kernel', str(путь)] if Вид_ЗНАЧЕН == 'elf' else ['-cdrom', str(путь), '-boot', 'd']
        if Память_средний is not None:
            команда += ['-drive', 'file=' + str(Память_средний) + ',format=raw,if=ide,index=0']
        self.Процесс_ЗНАЧЕН = subprocess.Popen(команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_путь.exists()):
                if self.Процесс_ЗНАЧЕН.poll() is not None:
                    raise AssertionError(self.Процесс_ЗНАЧЕН.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU запустить значение_времени 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_ЗНАЧЕН.connect(str(монитор_путь))
            self.직렬.setblocking(False)
            self.монитор_ЗНАЧЕН.sendall(b'cont\n')
            self.состояние_ожидания('jkoros> ')
        except BaseException:
            self.Закрыть()
            raise

    def состояние_ожидания(self, 문구, запустить=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_ЗАПИСЬ[запустить:]:
                return self.LOG_ЗАПИСЬ[запустить:].decode('utf-8', 'replace')
            Чтение, _, _ = select.select([self.직렬], [], [], 0.1)
            if Чтение:
                данные = self.직렬.recv(65536)
                if not данные: break
                self.LOG_ЗАПИСЬ.extend(данные)
            if self.Процесс_ЗНАЧЕН.poll() is not None: break
        raise AssertionError('минутку_ЗНАЧЕН сбой_ЗНАЧЕН: ' + 문구 + '\n' + self.LOG_ЗАПИСЬ.decode('utf-8', 'replace'))

    def команда(self, строка_ЗНАЧЕН, 기대):
        запустить = len(self.LOG_ЗАПИСЬ)
        self.직렬.sendall((строка_ЗНАЧЕН + '\n').encode())
        результат = self.состояние_ожидания('jkoros> ', запустить)
        for 문구 in 기대:
            assert 문구 in результат, (строка_ЗНАЧЕН, 문구, результат)
        assert 'PANIC' not in результат, результат
        return результат

    def Закрыть(self):
        self.직렬.close()
        self.монитор_ЗНАЧЕН.close()
        if self.Процесс_ЗНАЧЕН.poll() is None:
            self.Процесс_ЗНАЧЕН.terminate()
            try: self.Процесс_ЗНАЧЕН.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Процесс_ЗНАЧЕН.kill()
                self.Процесс_ЗНАЧЕН.wait()
        self.Процесс_ЗНАЧЕН.communicate()
        self.임시.cleanup()


def 보호커널(Каталог_ЗНАЧЕН):
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
    항목들 = ['hello=' + str(позиция / 'build/apps/hello.elf')]
    for Название, контент_ЗНАЧЕН in 사례들.items():
        исходныйКод = Каталог_ЗНАЧЕН / (Название + '.s')
        исходныйКод.write_text('.code32\n.text\n.globl _start\n_start:\n' + контент_ЗНАЧЕН +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Каталог_ЗНАЧЕН / (Название + '.o')), str(исходныйКод)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(позиция.parent / 'compiler/пользователь_канал_Макет.ld'),
                        '-o', str(Каталог_ЗНАЧЕН / (Название + '.elf')), str(Каталог_ЗНАЧЕН / (Название + '.o'))], check=True)
        항목들.append(Название + '=' + str(Каталог_ЗНАЧЕН / (Название + '.elf')))
    ИТ_службы_обычный = bytearray((позиция / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    неверный_KR = bytearray(ИТ_службы_обычный); неверный_KR[0] = 0; 변형들['badelf'] = неверный_KR
    неверный_KR = bytearray(ИТ_службы_обычный); struct.pack_into('<I', неверный_KR, 24, 0x00100000); 변형들['badentry'] = неверный_KR
    неверный_KR = bytearray(ИТ_службы_обычный); struct.pack_into('<I', неверный_KR, 28, 0x7fffffff); 변형들['badtable'] = неверный_KR
    неверный_KR = bytearray(ИТ_службы_обычный); таблица_подстановки = struct.unpack_from('<I', неверный_KR, 28)[0]
    struct.pack_into('<I', неверный_KR, таблица_подстановки + 20, 0x7fffffff); 변형들['badsize'] = неверный_KR
    for Название, данные in 변형들.items():
        файл = Каталог_ЗНАЧЕН / (Название + '.elf'); файл.write_bytes(данные)
        항목들.append(Название + '=' + str(файл))
    subprocess.run([sys.executable, str(позиция / 'инструменты/BIND_участник.py'), '-o', str(Каталог_ЗНАЧЕН / 'apps.bin')] + 항목들, check=True)
    исходныйКод = Каталог_ЗНАЧЕН / 'apps.s'
    исходныйКод.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Каталог_ЗНАЧЕН / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Каталог_ЗНАЧЕН / 'apps.o'), str(исходныйКод)], check=True)
    ядро_ЗНАЧЕН = Каталог_ЗНАЧЕН / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(позиция / 'запуск_машины/схема_компоновки.ld'), '-o', str(ядро_ЗНАЧЕН),
                    str(позиция / 'build/boot.o'), str(позиция / 'build/java.o'), str(позиция / 'build/user.o'), str(Каталог_ЗНАЧЕН / 'apps.o')], check=True)
    return ядро_ЗНАЧЕН


def 실행():
    результат = {}
    сервер_ЗНАЧЕН = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_ЗНАЧЕН.bind(('127.0.0.1', 0))
    сервер_ЗНАЧЕН.settimeout(0.1)
    порт_ЗНАЧЕН = сервер_ЗНАЧЕН.getsockname()[1]
    ПОЛУЧЕНО_товар = []
    Выход_программа = threading.Event()
    def вывод_на_экран_ответ():
        while not Выход_программа.is_set():
            try: данные, одноранговый_ЗНАЧЕН = сервер_ЗНАЧЕН.recvfrom(4096)
            except socket.timeout: continue
            ПОЛУЧЕНО_товар.append(данные)
            if данные != b'drop-me': сервер_ЗНАЧЕН.sendto(данные, одноранговый_ЗНАЧЕН)
    работник_ЗНАЧЕН = threading.Thread(target=вывод_на_экран_ответ, daemon=True)
    работник_ЗНАЧЕН.start()
    try:
        for Вид_ЗНАЧЕН in ('elf', 'iso'):
            компьютер_5eb260fa = VM(позиция / ('build/kernel.elf' if Вид_ЗНАЧЕН == 'elf' else 'build/kernel.iso'), Вид_ЗНАЧЕН)
            try:
                компьютер_5eb260fa.команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                компьютер_5eb260fa.команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                компьютер_5eb260fa.команда('run missing', ['Exit: -2'])
                компьютер_5eb260fa.команда('net', ['NET RTL8139'])
                компьютер_5eb260fa.команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for контент_ЗНАЧЕН in ('hello-network', 'odd', 'even', 'repeat-123'):
                    компьютер_5eb260fa.команда('run udp 10.0.2.2 {} {}'.format(порт_ЗНАЧЕН, контент_ЗНАЧЕН), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert контент_ЗНАЧЕН.encode() in ПОЛУЧЕНО_товар, 'узел 서버에서 자료를 받지 못함'
                компьютер_5eb260fa.команда('run stress {}'.format(порт_ЗНАЧЕН), ['UDP STRESS PASS', 'Exit: 0'])
                компьютер_5eb260fa.команда('run udp 10.0.2.2 {} drop-me'.format(порт_ЗНАЧЕН), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                компьютер_5eb260fa.команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                результат[Вид_ЗНАЧЕН] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode('utf-8', 'replace')
                print('PASS: {} пространство_пользователя ELF/ring 3/аргументы/UDP узел 왕복/значение_времени 초과/оболочка 복귀'.format(Вид_ЗНАЧЕН), flush=True)
            finally:
                try: компьютер_5eb260fa.команда('net', [])
                except Exception: pass
                (позиция / 'build/사용자통신-last.log').write_bytes(компьютер_5eb260fa.LOG_ЗАПИСЬ)
                компьютер_5eb260fa.Закрыть()
        компьютер_5eb260fa = VM(позиция / 'build/kernel.elf', сеть_ЗНАЧЕН=False)
        try:
            компьютер_5eb260fa.команда('net', ['NET unavailable'])
            компьютер_5eb260fa.команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            компьютер_5eb260fa.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            результат['no_nic'] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode()
        finally: компьютер_5eb260fa.Закрыть()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            компьютер_5eb260fa = VM(보호커널(Path(임시)), сеть_ЗНАЧЕН=False)
            try:
                for Название, Состояние_ЗНАЧЕН in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    компьютер_5eb260fa.команда('run ' + Название, ['Exit: ' + str(Состояние_ЗНАЧЕН)])
                    компьютер_5eb260fa.команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                результат['protection'] = компьютер_5eb260fa.LOG_ЗАПИСЬ.decode()
                print('PASS: пространство_пользователя Память_данные/аппаратный_порт 격리, 잘못된 указатель/ELF, CPU исключение, 무한 спринт_ЗНАЧЕН 제한', flush=True)
            finally:
                (позиция / 'build/Защита_тест-last.log').write_bytes(компьютер_5eb260fa.LOG_ЗАПИСЬ)
                компьютер_5eb260fa.Закрыть()
    finally:
        Выход_программа.set()
        работник_ЗНАЧЕН.join(timeout=2)
        сервер_ЗНАЧЕН.close()
    результат['host_udp_received'] = [{'length': len(данные), 'sha256': hashlib.sha256(данные).hexdigest()} for данные in ПОЛУЧЕНО_товар]
    (позиция / 'build/тест_пользователь_сеть.json').write_text(json.dumps(результат, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    실행()
