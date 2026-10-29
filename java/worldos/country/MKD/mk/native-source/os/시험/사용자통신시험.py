#!/usr/bin/env python3
"""реален_податоци ring 3 ELF/вдоми UDP 왕복/заштита_VALUE ГРЕШКА/TIME_VALUE 제한/잘못된 ELF를 검증한다."""
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

Позиција = Path(__file__).resolve().parents[1]


class виртуелен_машина:
    def __init__(self, ПАТЕКА, 종류='elf', Мрежа_VALUE=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        Именик_VALUE = Path(self.임시.name)
        self.LOG_ред = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_VALUE = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_патека = Именик_VALUE / 'serial.sock', Именик_VALUE / 'monitor.sock'
        Команда = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_патека) + ',server,nowait']
        Команда += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Мрежа_VALUE else ['-net', 'none']
        Команда += ['-kernel', str(ПАТЕКА)] if 종류 == 'elf' else ['-cdrom', str(ПАТЕКА), '-boot', 'd']
        if 저장매체 is not None:
            Команда += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Процес_VALUE = subprocess.Popen(Команда, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_патека.exists()):
                if self.Процес_VALUE.poll() is not None:
                    raise AssertionError(self.Процес_VALUE.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Изврши_2 TIME_VALUE 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_VALUE.connect(str(монитор_патека))
            self.직렬.setblocking(False)
            self.монитор_VALUE.sendall(b'cont\n')
            self.почекај_статус('jkoros> ')
        except BaseException:
            self.Затвори()
            raise

    def почекај_статус(self, 문구, Изврши_2=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.LOG_ред[Изврши_2:]:
                return self.LOG_ред[Изврши_2:].decode('utf-8', 'replace')
            Читај, _, _ = select.select([self.직렬], [], [], 0.1)
            if Читај:
                податоци = self.직렬.recv(65536)
                if not податоци: break
                self.LOG_ред.extend(податоци)
            if self.Процес_VALUE.poll() is not None: break
        raise AssertionError('почекај_VALUE неуспех_VALUE: ' + 문구 + '\n' + self.LOG_ред.decode('utf-8', 'replace'))

    def Команда(self, низа_VALUE_6ca8363c, 기대):
        Изврши_2 = len(self.LOG_ред)
        self.직렬.sendall((низа_VALUE_6ca8363c + '\n').encode())
        мерка = self.почекај_статус('jkoros> ', Изврши_2)
        for 문구 in 기대:
            assert 문구 in мерка, (низа_VALUE_6ca8363c, 문구, мерка)
        assert 'PANIC' not in мерка, мерка
        return мерка

    def Затвори(self):
        self.직렬.close()
        self.монитор_VALUE.close()
        if self.Процес_VALUE.poll() is None:
            self.Процес_VALUE.terminate()
            try: self.Процес_VALUE.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Процес_VALUE.kill()
                self.Процес_VALUE.wait()
        self.Процес_VALUE.communicate()
        self.임시.cleanup()


def 보호커널(Именик_VALUE):
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
    항목들 = ['hello=' + str(Позиција / 'build/apps/hello.elf')]
    for Име, Содржина_VALUE in 사례들.items():
        ИЗВОР = Именик_VALUE / (Име + '.s')
        ИЗВОР.write_text('.code32\n.text\n.globl _start\n_start:\n' + Содржина_VALUE +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(Именик_VALUE / (Име + '.o')), str(ИЗВОР)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Позиција.parent / 'compiler/корисник_Врска_Распоред.ld'),
                        '-o', str(Именик_VALUE / (Име + '.elf')), str(Именик_VALUE / (Име + '.o'))], check=True)
        항목들.append(Име + '=' + str(Именик_VALUE / (Име + '.elf')))
    정상 = bytearray((Позиција / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    неважечки_мерка = bytearray(정상); неважечки_мерка[0] = 0; 변형들['badelf'] = неважечки_мерка
    неважечки_мерка = bytearray(정상); struct.pack_into('<I', неважечки_мерка, 24, 0x00100000); 변형들['badentry'] = неважечки_мерка
    неважечки_мерка = bytearray(정상); struct.pack_into('<I', неважечки_мерка, 28, 0x7fffffff); 변형들['badtable'] = неважечки_мерка
    неважечки_мерка = bytearray(정상); LOOKUP_табела = struct.unpack_from('<I', неважечки_мерка, 28)[0]
    struct.pack_into('<I', неважечки_мерка, LOOKUP_табела + 20, 0x7fffffff); 변형들['badsize'] = неважечки_мерка
    for Име, податоци in 변형들.items():
        Датотека = Именик_VALUE / (Име + '.elf'); Датотека.write_bytes(податоци)
        항목들.append(Име + '=' + str(Датотека))
    subprocess.run([sys.executable, str(Позиција / 'Алатки/묶기.py'), '-o', str(Именик_VALUE / 'apps.bin')] + 항목들, check=True)
    ИЗВОР = Именик_VALUE / 'apps.s'
    ИЗВОР.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(Именик_VALUE / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(Именик_VALUE / 'apps.o'), str(ИЗВОР)], check=True)
    јадро_VALUE = Именик_VALUE / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(Позиција / '부팅/Врска_Распоред.ld'), '-o', str(јадро_VALUE),
                    str(Позиција / 'build/boot.o'), str(Позиција / 'build/java.o'), str(Позиција / 'build/user.o'), str(Именик_VALUE / 'apps.o')], check=True)
    return јадро_VALUE


def Изврши_наредба():
    мерка = {}
    сервер_VALUE = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_VALUE.bind(('127.0.0.1', 0))
    сервер_VALUE.settimeout(0.1)
    порта_VALUE = сервер_VALUE.getsockname()[1]
    RECEIVED_ставка = []
    Излез_програма = threading.Event()
    def 되보내기():
        while not Излез_програма.is_set():
            try: податоци, рамноправен_уред_VALUE = сервер_VALUE.recvfrom(4096)
            except socket.timeout: continue
            RECEIVED_ставка.append(податоци)
            if податоци != b'drop-me': сервер_VALUE.sendto(податоци, рамноправен_уред_VALUE)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            машина = виртуелен_машина(Позиција / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                машина.Команда('apps', ['hello', 'udp', 'netcheck', 'stress'])
                машина.Команда('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                машина.Команда('run missing', ['Exit: -2'])
                машина.Команда('net', ['NET RTL8139'])
                машина.Команда('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Содржина_VALUE in ('hello-network', 'odd', 'even', 'repeat-123'):
                    машина.Команда('run udp 10.0.2.2 {} {}'.format(порта_VALUE, Содржина_VALUE), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Содржина_VALUE.encode() in RECEIVED_ставка, 'вдоми 서버에서 자료를 받지 못함'
                машина.Команда('run stress {}'.format(порта_VALUE), ['UDP STRESS PASS', 'Exit: 0'])
                машина.Команда('run udp 10.0.2.2 {} drop-me'.format(порта_VALUE), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                машина.Команда('run hello recovered', ['arg: recovered', 'Exit: 0'])
                мерка[종류] = машина.LOG_ред.decode('utf-8', 'replace')
                print('PASS: {} корисник ELF/ring 3/Аргументи/UDP вдоми 왕복/TIME_VALUE 초과/обвивка 복귀'.format(종류), flush=True)
            finally:
                try: машина.Команда('net', [])
                except Exception: pass
                (Позиција / 'build/사용자통신-last.log').write_bytes(машина.LOG_ред)
                машина.Затвори()
        машина = виртуелен_машина(Позиција / 'build/kernel.elf', Мрежа_VALUE=False)
        try:
            машина.Команда('net', ['NET unavailable'])
            машина.Команда('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            машина.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
            мерка['no_nic'] = машина.LOG_ред.decode()
        finally: машина.Затвори()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            машина = виртуелен_машина(보호커널(Path(임시)), Мрежа_VALUE=False)
            try:
                for Име, статус_VALUE in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    машина.Команда('run ' + Име, ['Exit: ' + str(статус_VALUE)])
                    машина.Команда('run hello', ['USER MODE ring 3', 'Exit: 0'])
                мерка['protection'] = машина.LOG_ред.decode()
                print('PASS: корисник Меморија_податоци/포트 격리, 잘못된 покажувач/ELF, CPU исклучок, 무한 повторување_VALUE 제한', flush=True)
            finally:
                (Позиција / 'build/보호시험-last.log').write_bytes(машина.LOG_ред)
                машина.Затвори()
    finally:
        Излез_програма.set()
        일꾼.join(timeout=2)
        сервер_VALUE.close()
    мерка['host_udp_received'] = [{'length': len(податоци), 'sha256': hashlib.sha256(податоци).hexdigest()} for податоци in RECEIVED_ставка]
    (Позиција / 'build/사용자통신시험.json').write_text(json.dumps(мерка, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Изврши_наредба()
