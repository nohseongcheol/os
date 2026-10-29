#!/usr/bin/env python3
"""фактычны_дадзеныя ring 3 ELF/вузел UDP 왕복/ахоўваць_значэнне ПАМЫЛКА/час_значэнне 제한/잘못된 ELF를 검증한다."""
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

Пазіцыя = Path(__file__).resolve().parents[1]


class віртуальны_камп_ютар:
    def __init__(self, ШЛЯХ, 종류='elf', Сетка_значэнне=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        каталог_значэнне = Path(self.임시.name)
        self.журнал_запіс = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.манітор_значэнне = socket.socket(socket.AF_UNIX)
        직렬경로, манітор_шлях = каталог_значэнне / 'serial.sock', каталог_значэнне / 'monitor.sock'
        Загад = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(манітор_шлях) + ',server,nowait']
        Загад += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Сетка_значэнне else ['-net', 'none']
        Загад += ['-kernel', str(ШЛЯХ)] if 종류 == 'elf' else ['-cdrom', str(ШЛЯХ), '-boot', 'd']
        if 저장매체 is not None:
            Загад += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Працэс_значэнне = subprocess.Popen(Загад, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and манітор_шлях.exists()):
                if self.Працэс_значэнне.poll() is not None:
                    raise AssertionError(self.Працэс_значэнне.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Выканаць час_значэнне 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.манітор_значэнне.connect(str(манітор_шлях))
            self.직렬.setblocking(False)
            self.манітор_значэнне.sendall(b'cont\n')
            self.чакае_стан('jkoros> ')
        except BaseException:
            self.Закрыць()
            raise

    def чакае_стан(self, 문구, Выканаць=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.журнал_запіс[Выканаць:]:
                return self.журнал_запіс[Выканаць:].decode('utf-8', 'replace')
            Чытанне, _, _ = select.select([self.직렬], [], [], 0.1)
            if Чытанне:
                дадзеныя = self.직렬.recv(65536)
                if not дадзеныя: break
                self.журнал_запіс.extend(дадзеныя)
            if self.Працэс_значэнне.poll() is not None: break
        raise AssertionError('чакае_значэнне няўдача_значэнне: ' + 문구 + '\n' + self.журнал_запіс.decode('utf-8', 'replace'))

    def Загад(self, радок_значэнне, 기대):
        Выканаць = len(self.журнал_запіс)
        self.직렬.sendall((радок_значэнне + '\n').encode())
        결과 = self.чакае_стан('jkoros> ', Выканаць)
        for 문구 in 기대:
            assert 문구 in 결과, (радок_значэнне, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Закрыць(self):
        self.직렬.close()
        self.манітор_значэнне.close()
        if self.Працэс_значэнне.poll() is None:
            self.Працэс_значэнне.terminate()
            try: self.Працэс_значэнне.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Працэс_значэнне.kill()
                self.Працэс_значэнне.wait()
        self.Працэс_значэнне.communicate()
        self.임시.cleanup()


def 보호커널(каталог_значэнне):
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
    항목들 = ['hello=' + str(Пазіцыя / 'build/apps/hello.elf')]
    for Назва, кантэнт_значэнне in 사례들.items():
        КРЫНІЦА = каталог_значэнне / (Назва + '.s')
        КРЫНІЦА.write_text('.code32\n.text\n.globl _start\n_start:\n' + кантэнт_значэнне +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(каталог_значэнне / (Назва + '.o')), str(КРЫНІЦА)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Пазіцыя.parent / 'compiler/карыстальнік_сувязь_Макет.ld'),
                        '-o', str(каталог_значэнне / (Назва + '.elf')), str(каталог_значэнне / (Назва + '.o'))], check=True)
        항목들.append(Назва + '=' + str(каталог_значэнне / (Назва + '.elf')))
    정상 = bytearray((Пазіцыя / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Назва, дадзеныя in 변형들.items():
        Файл = каталог_значэнне / (Назва + '.elf'); Файл.write_bytes(дадзеныя)
        항목들.append(Назва + '=' + str(Файл))
    subprocess.run([sys.executable, str(Пазіцыя / 'Інструменты/묶기.py'), '-o', str(каталог_значэнне / 'apps.bin')] + 항목들, check=True)
    КРЫНІЦА = каталог_значэнне / 'apps.s'
    КРЫНІЦА.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(каталог_значэнне / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(каталог_значэнне / 'apps.o'), str(КРЫНІЦА)], check=True)
    ядро_значэнне = каталог_значэнне / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Пазіцыя / '부팅/сувязь_Макет.ld'), '-o', str(ядро_значэнне),
                    str(Пазіцыя / 'build/boot.o'), str(Пазіцыя / 'build/java.o'), str(Пазіцыя / 'build/user.o'), str(каталог_значэнне / 'apps.o')], check=True)
    return ядро_значэнне


def выканаць_каманда():
    결과 = {}
    сервер_значэнне = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_значэнне.bind(('127.0.0.1', 0))
    сервер_значэнне.settimeout(0.1)
    порт_значэнне = сервер_значэнне.getsockname()[1]
    받은것 = []
    Выхад_праграма = threading.Event()
    def 되보내기():
        while not Выхад_праграма.is_set():
            try: дадзеныя, аднарангавы_значэнне = сервер_значэнне.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(дадзеныя)
            if дадзеныя != b'drop-me': сервер_значэнне.sendto(дадзеныя, аднарангавы_значэнне)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            камп_ютар = віртуальны_камп_ютар(Пазіцыя / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                камп_ютар.Загад('apps', ['hello', 'udp', 'netcheck', 'stress'])
                камп_ютар.Загад('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                камп_ютар.Загад('run missing', ['Exit: -2'])
                камп_ютар.Загад('net', ['NET RTL8139'])
                камп_ютар.Загад('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for кантэнт_значэнне in ('hello-network', 'odd', 'even', 'repeat-123'):
                    камп_ютар.Загад('run udp 10.0.2.2 {} {}'.format(порт_значэнне, кантэнт_значэнне), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert кантэнт_значэнне.encode() in 받은것, 'вузел 서버에서 자료를 받지 못함'
                камп_ютар.Загад('run stress {}'.format(порт_значэнне), ['UDP STRESS PASS', 'Exit: 0'])
                камп_ютар.Загад('run udp 10.0.2.2 {} drop-me'.format(порт_значэнне), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                камп_ютар.Загад('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = камп_ютар.журнал_запіс.decode('utf-8', 'replace')
                print('PASS: {} карыстальнік ELF/ring 3/인수/UDP вузел 왕복/час_значэнне 초과/абалонка 복귀'.format(종류), flush=True)
            finally:
                try: камп_ютар.Загад('net', [])
                except Exception: pass
                (Пазіцыя / 'build/사용자통신-last.log').write_bytes(камп_ютар.журнал_запіс)
                камп_ютар.Закрыць()
        камп_ютар = віртуальны_камп_ютар(Пазіцыя / 'build/kernel.elf', Сетка_значэнне=False)
        try:
            камп_ютар.Загад('net', ['NET unavailable'])
            камп_ютар.Загад('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            камп_ютар.Загад('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = камп_ютар.журнал_запіс.decode()
        finally: камп_ютар.Закрыць()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            камп_ютар = віртуальны_камп_ютар(보호커널(Path(임시)), Сетка_значэнне=False)
            try:
                for Назва, стан_значэнне in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    камп_ютар.Загад('run ' + Назва, ['Exit: ' + str(стан_значэнне)])
                    камп_ютар.Загад('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = камп_ютар.журнал_запіс.decode()
                print('PASS: карыстальнік памяць_дадзеныя/포트 격리, 잘못된 указальнік/ELF, CPU выключэнне, 무한 спрынт_значэнне 제한', flush=True)
            finally:
                (Пазіцыя / 'build/보호시험-last.log').write_bytes(камп_ютар.журнал_запіс)
                камп_ютар.Закрыць()
    finally:
        Выхад_праграма.set()
        일꾼.join(timeout=2)
        сервер_значэнне.close()
    결과['host_udp_received'] = [{'length': len(дадзеныя), 'sha256': hashlib.sha256(дадзеныя).hexdigest()} for дадзеныя in 받은것]
    (Пазіцыя / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    выканаць_каманда()
