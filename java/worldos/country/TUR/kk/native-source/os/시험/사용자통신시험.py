#!/usr/bin/env python3
"""нақты_деректер ring 3 ELF/орналастыру UDP 왕복/қорғау_мән Қате/уақыт_мән 제한/잘못된 ELF를 검증한다."""
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

Орны = Path(__file__).resolve().parents[1]


class виртуалды_машина:
    def __init__(self, Жол_2, 종류='elf', желі_мән=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        каталог_мән = Path(self.임시.name)
        self.журнал_жол = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.бақылау_мән = socket.socket(socket.AF_UNIX)
        직렬경로, бақылау_жол = каталог_мән / 'serial.sock', каталог_мән / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(бақылау_жол) + ',server,nowait']
        Команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if желі_мән else ['-net', 'none']
        Команда += ['-kernel', str(Жол_2)] if 종류 == 'elf' else ['-cdrom', str(Жол_2), '-boot', 'd']
        if 저장매체 is not None:
            Команда += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Процесс_мән = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and бақылау_жол.exists()):
                if self.Процесс_мән.poll() is not None:
                    raise AssertionError(self.Процесс_мән.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Орындау_2 уақыт_мән 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.бақылау_мән.connect(str(бақылау_жол))
            self.직렬.setblocking(False)
            self.бақылау_мән.sendall(b'cont\n')
            self.күту_күйі('jkoros> ')
        except BaseException:
            self.Жабу()
            raise

    def күту_күйі(self, 문구, Орындау_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.журнал_жол[Орындау_2:]:
                return self.журнал_жол[Орындау_2:].decode('utf-8', 'replace')
            Оқу, _, _ = select.select([self.직렬], [], [], 0.1)
            if Оқу:
                деректер = self.직렬.recv(65536)
                if not деректер: break
                self.журнал_жол.extend(деректер)
            if self.Процесс_мән.poll() is not None: break
        raise AssertionError('күте_тұрыңыз_мән қате_мән: ' + 문구 + '\n' + self.журнал_жол.decode('utf-8', 'replace'))

    def Команда(self, жол_мән_6ca8363c, 기대):
        Орындау_2 = len(self.журнал_жол)
        self.직렬.sendall((жол_мән_6ca8363c + '\n').encode())
        НӘТИЖЕ = self.күту_күйі('jkoros> ', Орындау_2)
        for 문구 in 기대:
            assert 문구 in НӘТИЖЕ, (жол_мән_6ca8363c, 문구, НӘТИЖЕ)
        assert 'PANIC' not in НӘТИЖЕ, НӘТИЖЕ
        return НӘТИЖЕ

    def Жабу(self):
        self.직렬.close()
        self.бақылау_мән.close()
        if self.Процесс_мән.poll() is None:
            self.Процесс_мән.terminate()
            try: self.Процесс_мән.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Процесс_мән.kill()
                self.Процесс_мән.wait()
        self.Процесс_мән.communicate()
        self.임시.cleanup()


def 보호커널(каталог_мән):
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
    항목들 = ['hello=' + str(Орны / 'build/apps/hello.elf')]
    for Аты, мазмұн_мән in 사례들.items():
        Неден = каталог_мән / (Аты + '.s')
        Неден.write_text('.code32\n.text\n.globl _start\n_start:\n' + мазмұн_мән +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(каталог_мән / (Аты + '.o')), str(Неден)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Орны.parent / 'compiler/пайдаланушы_Cілтеме_макет.ld'),
                        '-o', str(каталог_мән / (Аты + '.elf')), str(каталог_мән / (Аты + '.o'))], check=True)
        항목들.append(Аты + '=' + str(каталог_мән / (Аты + '.elf')))
    정상 = bytearray((Орны / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    дұрыс_емес_өлшем = bytearray(정상); дұрыс_емес_өлшем[0] = 0; 변형들['badelf'] = дұрыс_емес_өлшем
    дұрыс_емес_өлшем = bytearray(정상); struct.pack_into('<I', дұрыс_емес_өлшем, 24, 0x00100000); 변형들['badentry'] = дұрыс_емес_өлшем
    дұрыс_емес_өлшем = bytearray(정상); struct.pack_into('<I', дұрыс_емес_өлшем, 28, 0x7fffffff); 변형들['badtable'] = дұрыс_емес_өлшем
    дұрыс_емес_өлшем = bytearray(정상); Іздеу_кесте = struct.unpack_from('<I', дұрыс_емес_өлшем, 28)[0]
    struct.pack_into('<I', дұрыс_емес_өлшем, Іздеу_кесте + 20, 0x7fffffff); 변형들['badsize'] = дұрыс_емес_өлшем
    for Аты, деректер in 변형들.items():
        Файл = каталог_мән / (Аты + '.elf'); Файл.write_bytes(деректер)
        항목들.append(Аты + '=' + str(Файл))
    subprocess.run([sys.executable, str(Орны / 'Құралдар/байланыстыру_қатысушы.py'), '-o', str(каталог_мән / 'apps.bin')] + 항목들, check=True)
    Неден = каталог_мән / 'apps.s'
    Неден.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(каталог_мән / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(каталог_мән / 'apps.o'), str(Неден)], check=True)
    ядро_мән = каталог_мән / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Орны / '부팅/Cілтеме_макет.ld'), '-o', str(ядро_мән),
                    str(Орны / 'build/boot.o'), str(Орны / 'build/java.o'), str(Орны / 'build/user.o'), str(каталог_мән / 'apps.o')], check=True)
    return ядро_мән


def орындау_пәрмен():
    НӘТИЖЕ = {}
    сервер_мән = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_мән.bind(('127.0.0.1', 0))
    сервер_мән.settimeout(0.1)
    порт_мән = сервер_мән.getsockname()[1]
    받은것 = []
    Шығу_бағдарлама = threading.Event()
    def экранға_шығару_жауап():
        while not Шығу_бағдарлама.is_set():
            try: деректер, бір_рангілі_мән = сервер_мән.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(деректер)
            if деректер != b'drop-me': сервер_мән.sendto(деректер, бір_рангілі_мән)
    일꾼 = threading.Thread(target=экранға_шығару_жауап, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            компьютер = виртуалды_машина(Орны / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                компьютер.Команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                компьютер.Команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                компьютер.Команда('run missing', ['Exit: -2'])
                компьютер.Команда('net', ['NET RTL8139'])
                компьютер.Команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for мазмұн_мән in ('hello-network', 'odd', 'even', 'repeat-123'):
                    компьютер.Команда('run udp 10.0.2.2 {} {}'.format(порт_мән, мазмұн_мән), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert мазмұн_мән.encode() in 받은것, 'орналастыру 서버에서 자료를 받지 못함'
                компьютер.Команда('run stress {}'.format(порт_мән), ['UDP STRESS PASS', 'Exit: 0'])
                компьютер.Команда('run udp 10.0.2.2 {} drop-me'.format(порт_мән), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                компьютер.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                НӘТИЖЕ[종류] = компьютер.журнал_жол.decode('utf-8', 'replace')
                print('PASS: {} пайдаланушы ELF/ring 3/Аргументтер/UDP орналастыру 왕복/уақыт_мән 초과/қоршам 복귀'.format(종류), flush=True)
            finally:
                try: компьютер.Команда('net', [])
                except Exception: pass
                (Орны / 'build/사용자통신-last.log').write_bytes(компьютер.журнал_жол)
                компьютер.Жабу()
        компьютер = виртуалды_машина(Орны / 'build/kernel.elf', желі_мән=False)
        try:
            компьютер.Команда('net', ['NET unavailable'])
            компьютер.Команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            компьютер.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            НӘТИЖЕ['no_nic'] = компьютер.журнал_жол.decode()
        finally: компьютер.Жабу()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            компьютер = виртуалды_машина(보호커널(Path(임시)), желі_мән=False)
            try:
                for Аты, күй_мән in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    компьютер.Команда('run ' + Аты, ['Exit: ' + str(күй_мән)])
                    компьютер.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                НӘТИЖЕ['protection'] = компьютер.журнал_жол.decode()
                print('PASS: пайдаланушы Жад_деректер/포트 격리, 잘못된 меңзер/ELF, CPU ерекшелік, 무한 спринт_мән 제한', flush=True)
            finally:
                (Орны / 'build/보호시험-last.log').write_bytes(компьютер.журнал_жол)
                компьютер.Жабу()
    finally:
        Шығу_бағдарлама.set()
        일꾼.join(timeout=2)
        сервер_мән.close()
    НӘТИЖЕ['host_udp_received'] = [{'length': len(деректер), 'sha256': hashlib.sha256(деректер).hexdigest()} for деректер in 받은것]
    (Орны / 'build/사용자통신시험.json').write_text(json.dumps(НӘТИЖЕ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    орындау_пәрмен()
