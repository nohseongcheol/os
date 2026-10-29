#!/usr/bin/env python3
"""действителен_данни ring 3 ELF/хост UDP 왕복/защитавам_стойност ГРЕШКА/час_стойност 제한/잘못된 ELF를 검증한다."""
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

Позиция = Path(__file__).resolve().parents[1]


class виртуална_машина:
    def __init__(self, ПЪТ, 종류='elf', мрежа_стойност=True, Памет_среда=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        указател_стойност = Path(self.임시.name)
        self.регистрирам_запис = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_стойност = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_път = указател_стойност / 'serial.sock', указател_стойност / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_път) + ',server,nowait']
        Команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if мрежа_стойност else ['-net', 'none']
        Команда += ['-kernel', str(ПЪТ)] if 종류 == 'elf' else ['-cdrom', str(ПЪТ), '-boot', 'd']
        if Памет_среда is not None:
            Команда += ['-drive', 'file=' + str(Памет_среда) + ',format=raw,if=ide,index=0']
        self.Процес_стойност = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_път.exists()):
                if self.Процес_стойност.poll() is not None:
                    raise AssertionError(self.Процес_стойност.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Стартиране час_стойност 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_стойност.connect(str(монитор_път))
            self.직렬.setblocking(False)
            self.монитор_стойност.sendall(b'cont\n')
            self.състояние_на_изчакване('jkoros> ')
        except BaseException:
            self.Затворен()
            raise

    def състояние_на_изчакване(self, 문구, Стартиране=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.регистрирам_запис[Стартиране:]:
                return self.регистрирам_запис[Стартиране:].decode('utf-8', 'replace')
            Четене, _, _ = select.select([self.직렬], [], [], 0.1)
            if Четене:
                данни = self.직렬.recv(65536)
                if not данни: break
                self.регистрирам_запис.extend(данни)
            if self.Процес_стойност.poll() is not None: break
        raise AssertionError('почакай_стойност отказ_стойност: ' + 문구 + '\n' + self.регистрирам_запис.decode('utf-8', 'replace'))

    def Команда(self, низ_стойност, 기대):
        Стартиране = len(self.регистрирам_запис)
        self.직렬.sendall((низ_стойност + '\n').encode())
        РЕЗУЛТАТ = self.състояние_на_изчакване('jkoros> ', Стартиране)
        for 문구 in 기대:
            assert 문구 in РЕЗУЛТАТ, (низ_стойност, 문구, РЕЗУЛТАТ)
        assert 'PANIC' not in РЕЗУЛТАТ, РЕЗУЛТАТ
        return РЕЗУЛТАТ

    def Затворен(self):
        self.직렬.close()
        self.монитор_стойност.close()
        if self.Процес_стойност.poll() is None:
            self.Процес_стойност.terminate()
            try: self.Процес_стойност.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Процес_стойност.kill()
                self.Процес_стойност.wait()
        self.Процес_стойност.communicate()
        self.임시.cleanup()


def 보호커널(указател_стойност):
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
    항목들 = ['hello=' + str(Позиция / 'build/apps/hello.elf')]
    for Име, Съдържание_стойност in 사례들.items():
        ИЗТОЧНИК = указател_стойност / (Име + '.s')
        ИЗТОЧНИК.write_text('.code32\n.text\n.globl _start\n_start:\n' + Съдържание_стойност +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(указател_стойност / (Име + '.o')), str(ИЗТОЧНИК)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Позиция.parent / 'compiler/потребител_Връзка_схема.ld'),
                        '-o', str(указател_стойност / (Име + '.elf')), str(указател_стойност / (Име + '.o'))], check=True)
        항목들.append(Име + '=' + str(указател_стойност / (Име + '.elf')))
    정상 = bytearray((Позиция / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    невалиден_мярка = bytearray(정상); невалиден_мярка[0] = 0; 변형들['badelf'] = невалиден_мярка
    невалиден_мярка = bytearray(정상); struct.pack_into('<I', невалиден_мярка, 24, 0x00100000); 변형들['badentry'] = невалиден_мярка
    невалиден_мярка = bytearray(정상); struct.pack_into('<I', невалиден_мярка, 28, 0x7fffffff); 변형들['badtable'] = невалиден_мярка
    невалиден_мярка = bytearray(정상); таблица_за_справка = struct.unpack_from('<I', невалиден_мярка, 28)[0]
    struct.pack_into('<I', невалиден_мярка, таблица_за_справка + 20, 0x7fffffff); 변형들['badsize'] = невалиден_мярка
    for Име, данни in 변형들.items():
        Файл = указател_стойност / (Име + '.elf'); Файл.write_bytes(данни)
        항목들.append(Име + '=' + str(Файл))
    subprocess.run([sys.executable, str(Позиция / 'Инструменти/обвързвам_участник.py'), '-o', str(указател_стойност / 'apps.bin')] + 항목들, check=True)
    ИЗТОЧНИК = указател_стойност / 'apps.s'
    ИЗТОЧНИК.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(указател_стойност / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(указател_стойност / 'apps.o'), str(ИЗТОЧНИК)], check=True)
    ядро_стойност = указател_стойност / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Позиция / '부팅/Връзка_схема.ld'), '-o', str(ядро_стойност),
                    str(Позиция / 'build/boot.o'), str(Позиция / 'build/java.o'), str(Позиция / 'build/user.o'), str(указател_стойност / 'apps.o')], check=True)
    return ядро_стойност


def изпълнявам_команда():
    РЕЗУЛТАТ = {}
    сървър_стойност = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сървър_стойност.bind(('127.0.0.1', 0))
    сървър_стойност.settimeout(0.1)
    порт_стойност = сървър_стойност.getsockname()[1]
    받은것 = []
    Изход_програма = threading.Event()
    def Ехо_отговор():
        while not Изход_програма.is_set():
            try: данни, крайно_устройство_стойност = сървър_стойност.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(данни)
            if данни != b'drop-me': сървър_стойност.sendto(данни, крайно_устройство_стойност)
    일꾼 = threading.Thread(target=Ехо_отговор, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуална_машина(Позиция / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                машина.Команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                машина.Команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                машина.Команда('run missing', ['Exit: -2'])
                машина.Команда('net', ['NET RTL8139'])
                машина.Команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Съдържание_стойност in ('hello-network', 'odd', 'even', 'repeat-123'):
                    машина.Команда('run udp 10.0.2.2 {} {}'.format(порт_стойност, Съдържание_стойност), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Съдържание_стойност.encode() in 받은것, 'хост 서버에서 자료를 받지 못함'
                машина.Команда('run stress {}'.format(порт_стойност), ['UDP STRESS PASS', 'Exit: 0'])
                машина.Команда('run udp 10.0.2.2 {} drop-me'.format(порт_стойност), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                машина.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                РЕЗУЛТАТ[종류] = машина.регистрирам_запис.decode('utf-8', 'replace')
                print('PASS: {} потребител ELF/ring 3/Параметри/UDP хост 왕복/час_стойност 초과/обвивка 복귀'.format(종류), flush=True)
            finally:
                try: машина.Команда('net', [])
                except Exception: pass
                (Позиция / 'build/사용자통신-last.log').write_bytes(машина.регистрирам_запис)
                машина.Затворен()
        машина = виртуална_машина(Позиция / 'build/kernel.elf', мрежа_стойност=False)
        try:
            машина.Команда('net', ['NET unavailable'])
            машина.Команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            машина.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            РЕЗУЛТАТ['no_nic'] = машина.регистрирам_запис.decode()
        finally: машина.Затворен()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            машина = виртуална_машина(보호커널(Path(임시)), мрежа_стойност=False)
            try:
                for Име, Състояние_стойност in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    машина.Команда('run ' + Име, ['Exit: ' + str(Състояние_стойност)])
                    машина.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                РЕЗУЛТАТ['protection'] = машина.регистрирам_запис.decode()
                print('PASS: потребител Памет_данни/포트 격리, 잘못된 показалец/ELF, CPU изключение, 무한 спринт_стойност 제한', flush=True)
            finally:
                (Позиция / 'build/보호시험-last.log').write_bytes(машина.регистрирам_запис)
                машина.Затворен()
    finally:
        Изход_програма.set()
        일꾼.join(timeout=2)
        сървър_стойност.close()
    РЕЗУЛТАТ['host_udp_received'] = [{'length': len(данни), 'sha256': hashlib.sha256(данни).hexdigest()} for данни in 받은것]
    (Позиция / 'build/사용자통신시험.json').write_text(json.dumps(РЕЗУЛТАТ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    изпълнявам_команда()
