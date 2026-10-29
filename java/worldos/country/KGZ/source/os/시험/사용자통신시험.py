#!/usr/bin/env python3
"""актуалдуу_берилмелер ring 3 ELF/кабылдоо UDP 왕복/коргоо_маани Ката/시간 제한/잘못된 ELF를 검증한다."""
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

Турган_жери = Path(__file__).resolve().parents[1]


class виртуалдык_машина:
    def __init__(self, ЖОЛ, 종류='elf', Желе_маани=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        каталог_маани = Path(self.임시.name)
        self.жазуу_катар = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_маани = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_жол = каталог_маани / 'serial.sock', каталог_маани / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_жол) + ',server,nowait']
        Команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Желе_маани else ['-net', 'none']
        Команда += ['-kernel', str(ЖОЛ)] if 종류 == 'elf' else ['-cdrom', str(ЖОЛ), '-boot', 'd']
        if 저장매체 is not None:
            Команда += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Процесс_маани = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_жол.exists()):
                if self.Процесс_маани.poll() is not None:
                    raise AssertionError(self.Процесс_маани.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Жүргүзүү 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_маани.connect(str(монитор_жол))
            self.직렬.setblocking(False)
            self.монитор_маани.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Жабуу()
            raise

    def 기다림(self, 문구, Жүргүзүү=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.жазуу_катар[Жүргүзүү:]:
                return self.жазуу_катар[Жүргүзүү:].decode('utf-8', 'replace')
            Окуу, _, _ = select.select([self.직렬], [], [], 0.1)
            if Окуу:
                берилмелер = self.직렬.recv(65536)
                if not берилмелер: break
                self.жазуу_катар.extend(берилмелер)
            if self.Процесс_маани.poll() is not None: break
        raise AssertionError('대기 натыйжасыз_маани: ' + 문구 + '\n' + self.жазуу_катар.decode('utf-8', 'replace'))

    def Команда(self, сап_маани, 기대):
        Жүргүзүү = len(self.жазуу_катар)
        self.직렬.sendall((сап_маани + '\n').encode())
        결과 = self.기다림('jkoros> ', Жүргүзүү)
        for 문구 in 기대:
            assert 문구 in 결과, (сап_маани, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Жабуу(self):
        self.직렬.close()
        self.монитор_маани.close()
        if self.Процесс_маани.poll() is None:
            self.Процесс_маани.terminate()
            try: self.Процесс_маани.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Процесс_маани.kill()
                self.Процесс_маани.wait()
        self.Процесс_маани.communicate()
        self.임시.cleanup()


def 보호커널(каталог_маани):
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
    항목들 = ['hello=' + str(Турган_жери / 'build/apps/hello.elf')]
    for Аты, Мазмун_маани in 사례들.items():
        Булак = каталог_маани / (Аты + '.s')
        Булак.write_text('.code32\n.text\n.globl _start\n_start:\n' + Мазмун_маани +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(каталог_маани / (Аты + '.o')), str(Булак)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Турган_жери.parent / 'compiler/колдонуучу_Шилтеме_түзүлүш.ld'),
                        '-o', str(каталог_маани / (Аты + '.elf')), str(каталог_маани / (Аты + '.o'))], check=True)
        항목들.append(Аты + '=' + str(каталог_маани / (Аты + '.elf')))
    정상 = bytearray((Турган_жери / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Аты, берилмелер in 변형들.items():
        Файл = каталог_маани / (Аты + '.elf'); Файл.write_bytes(берилмелер)
        항목들.append(Аты + '=' + str(Файл))
    subprocess.run([sys.executable, str(Турган_жери / 'Куралдар/묶기.py'), '-o', str(каталог_маани / 'apps.bin')] + 항목들, check=True)
    Булак = каталог_маани / 'apps.s'
    Булак.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(каталог_маани / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(каталог_маани / 'apps.o'), str(Булак)], check=True)
    өзөк_маани = каталог_маани / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Турган_жери / '부팅/Шилтеме_түзүлүш.ld'), '-o', str(өзөк_маани),
                    str(Турган_жери / 'build/boot.o'), str(Турган_жери / 'build/java.o'), str(Турган_жери / 'build/user.o'), str(каталог_маани / 'apps.o')], check=True)
    return өзөк_маани


def аткаруу_буйрук():
    결과 = {}
    сервер_маани = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_маани.bind(('127.0.0.1', 0))
    сервер_маани.settimeout(0.1)
    порт_маани = сервер_маани.getsockname()[1]
    받은것 = []
    Чыгуу_програм = threading.Event()
    def 되보내기():
        while not Чыгуу_програм.is_set():
            try: берилмелер, бирдей_маани = сервер_маани.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(берилмелер)
            if берилмелер != b'drop-me': сервер_маани.sendto(берилмелер, бирдей_маани)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуалдык_машина(Турган_жери / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                машина.Команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                машина.Команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                машина.Команда('run missing', ['Exit: -2'])
                машина.Команда('net', ['NET RTL8139'])
                машина.Команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Мазмун_маани in ('hello-network', 'odd', 'even', 'repeat-123'):
                    машина.Команда('run udp 10.0.2.2 {} {}'.format(порт_маани, Мазмун_маани), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Мазмун_маани.encode() in 받은것, 'кабылдоо 서버에서 자료를 받지 못함'
                машина.Команда('run stress {}'.format(порт_маани), ['UDP STRESS PASS', 'Exit: 0'])
                машина.Команда('run udp 10.0.2.2 {} drop-me'.format(порт_маани), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                машина.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = машина.жазуу_катар.decode('utf-8', 'replace')
                print('PASS: {} колдонуучу ELF/ring 3/인수/UDP кабылдоо 왕복/시간 초과/сырты 복귀'.format(종류), flush=True)
            finally:
                try: машина.Команда('net', [])
                except Exception: pass
                (Турган_жери / 'build/사용자통신-last.log').write_bytes(машина.жазуу_катар)
                машина.Жабуу()
        машина = виртуалдык_машина(Турган_жери / 'build/kernel.elf', Желе_маани=False)
        try:
            машина.Команда('net', ['NET unavailable'])
            машина.Команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            машина.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = машина.жазуу_катар.decode()
        finally: машина.Жабуу()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            машина = виртуалдык_машина(보호커널(Path(임시)), Желе_маани=False)
            try:
                for Аты, абал_маани in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    машина.Команда('run ' + Аты, ['Exit: ' + str(абал_маани)])
                    машина.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = машина.жазуу_катар.decode()
                print('PASS: колдонуучу эс_берилмелер/포트 격리, 잘못된 көрсөткүч/ELF, CPU 예외, 무한 итерация_маани 제한', flush=True)
            finally:
                (Турган_жери / 'build/보호시험-last.log').write_bytes(машина.жазуу_катар)
                машина.Жабуу()
    finally:
        Чыгуу_програм.set()
        일꾼.join(timeout=2)
        сервер_маани.close()
    결과['host_udp_received'] = [{'length': len(берилмелер), 'sha256': hashlib.sha256(берилмелер).hexdigest()} for берилмелер in 받은것]
    (Турган_жери / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    аткаруу_буйрук()
