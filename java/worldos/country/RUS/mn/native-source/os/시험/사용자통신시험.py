#!/usr/bin/env python3
"""бодит_өгөгдөл ring 3 ELF/хост UDP 왕복/хамгаалах_утга Алдаа/시간 제한/잘못된 ELF를 검증한다."""
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

위치 = Path(__file__).resolve().parents[1]


class виртуал_компьютер:
    def __init__(self, ЗАМ, 종류='elf', Сүлжээ_утга=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        лавлах_утга = Path(self.임시.name)
        self.бичих_мөр_6e8b375a = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.хяналтын_төхөөрөмж_утга = socket.socket(socket.AF_UNIX)
        직렬경로, хяналтын_төхөөрөмж_зам = лавлах_утга / 'serial.sock', лавлах_утга / 'monitor.sock'
        Тушаал = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(хяналтын_төхөөрөмж_зам) + ',server,nowait']
        Тушаал += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Сүлжээ_утга else ['-net', 'none']
        Тушаал += ['-kernel', str(ЗАМ)] if 종류 == 'elf' else ['-cdrom', str(ЗАМ), '-boot', 'd']
        if 저장매체 is not None:
            Тушаал += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.үйл_явц_утга = subprocess.Popen(Тушаал, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and хяналтын_төхөөрөмж_зам.exists()):
                if self.үйл_явц_утга.poll() is not None:
                    raise AssertionError(self.үйл_явц_утга.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Ажиллуулах 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.хяналтын_төхөөрөмж_утга.connect(str(хяналтын_төхөөрөмж_зам))
            self.직렬.setblocking(False)
            self.хяналтын_төхөөрөмж_утга.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Хаах()
            raise

    def 기다림(self, 문구, Ажиллуулах=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.бичих_мөр_6e8b375a[Ажиллуулах:]:
                return self.бичих_мөр_6e8b375a[Ажиллуулах:].decode('utf-8', 'replace')
            Унших, _, _ = select.select([self.직렬], [], [], 0.1)
            if Унших:
                өгөгдөл = self.직렬.recv(65536)
                if not өгөгдөл: break
                self.бичих_мөр_6e8b375a.extend(өгөгдөл)
            if self.үйл_явц_утга.poll() is not None: break
        raise AssertionError('대기 гэмтэл_утга: ' + 문구 + '\n' + self.бичих_мөр_6e8b375a.decode('utf-8', 'replace'))

    def Тушаал(self, мөр_утга_6ca8363c, 기대):
        Ажиллуулах = len(self.бичих_мөр_6e8b375a)
        self.직렬.sendall((мөр_утга_6ca8363c + '\n').encode())
        결과 = self.기다림('jkoros> ', Ажиллуулах)
        for 문구 in 기대:
            assert 문구 in 결과, (мөр_утга_6ca8363c, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Хаах(self):
        self.직렬.close()
        self.хяналтын_төхөөрөмж_утга.close()
        if self.үйл_явц_утга.poll() is None:
            self.үйл_явц_утга.terminate()
            try: self.үйл_явц_утга.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.үйл_явц_утга.kill()
                self.үйл_явц_утга.wait()
        self.үйл_явц_утга.communicate()
        self.임시.cleanup()


def 보호커널(лавлах_утга):
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
    항목들 = ['hello=' + str(위치 / 'build/apps/hello.elf')]
    for Нэр, Агуулга_утга in 사례들.items():
        ЭХ = лавлах_утга / (Нэр + '.s')
        ЭХ.write_text('.code32\n.text\n.globl _start\n_start:\n' + Агуулга_утга +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(лавлах_утга / (Нэр + '.o')), str(ЭХ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/хэрэглэгч_Холбох_Бүдүүвч.ld'),
                        '-o', str(лавлах_утга / (Нэр + '.elf')), str(лавлах_утга / (Нэр + '.o'))], check=True)
        항목들.append(Нэр + '=' + str(лавлах_утга / (Нэр + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Нэр, өгөгдөл in 변형들.items():
        Файл = лавлах_утга / (Нэр + '.elf'); Файл.write_bytes(өгөгдөл)
        항목들.append(Нэр + '=' + str(Файл))
    subprocess.run([sys.executable, str(위치 / 'Хэрэгслүүд/묶기.py'), '-o', str(лавлах_утга / 'apps.bin')] + 항목들, check=True)
    ЭХ = лавлах_утга / 'apps.s'
    ЭХ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(лавлах_утга / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(лавлах_утга / 'apps.o'), str(ЭХ)], check=True)
    кернел_утга = лавлах_утга / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Холбох_Бүдүүвч.ld'), '-o', str(кернел_утга),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(лавлах_утга / 'apps.o')], check=True)
    return кернел_утга


def Гүйцэтгэх_команд():
    결과 = {}
    сервер_утга = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_утга.bind(('127.0.0.1', 0))
    сервер_утга.settimeout(0.1)
    порт_утга = сервер_утга.getsockname()[1]
    받은것 = []
    Гарах_програм = threading.Event()
    def 되보내기():
        while not Гарах_програм.is_set():
            try: өгөгдөл, ижил_түвшин_утга = сервер_утга.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(өгөгдөл)
            if өгөгдөл != b'drop-me': сервер_утга.sendto(өгөгдөл, ижил_түвшин_утга)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            компьютер = виртуал_компьютер(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                компьютер.Тушаал('apps', ['hello', 'udp', 'netcheck', 'stress'])
                компьютер.Тушаал('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                компьютер.Тушаал('run missing', ['Exit: -2'])
                компьютер.Тушаал('net', ['NET RTL8139'])
                компьютер.Тушаал('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Агуулга_утга in ('hello-network', 'odd', 'even', 'repeat-123'):
                    компьютер.Тушаал('run udp 10.0.2.2 {} {}'.format(порт_утга, Агуулга_утга), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Агуулга_утга.encode() in 받은것, 'хост 서버에서 자료를 받지 못함'
                компьютер.Тушаал('run stress {}'.format(порт_утга), ['UDP STRESS PASS', 'Exit: 0'])
                компьютер.Тушаал('run udp 10.0.2.2 {} drop-me'.format(порт_утга), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                компьютер.Тушаал('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = компьютер.бичих_мөр_6e8b375a.decode('utf-8', 'replace')
                print('PASS: {} хэрэглэгч ELF/ring 3/인수/UDP хост 왕복/시간 초과/бүрхүүл 복귀'.format(종류), flush=True)
            finally:
                try: компьютер.Тушаал('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(компьютер.бичих_мөр_6e8b375a)
                компьютер.Хаах()
        компьютер = виртуал_компьютер(위치 / 'build/kernel.elf', Сүлжээ_утга=False)
        try:
            компьютер.Тушаал('net', ['NET unavailable'])
            компьютер.Тушаал('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            компьютер.Тушаал('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = компьютер.бичих_мөр_6e8b375a.decode()
        finally: компьютер.Хаах()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            компьютер = виртуал_компьютер(보호커널(Path(임시)), Сүлжээ_утга=False)
            try:
                for Нэр, төлөв_утга in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    компьютер.Тушаал('run ' + Нэр, ['Exit: ' + str(төлөв_утга)])
                    компьютер.Тушаал('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = компьютер.бичих_мөр_6e8b375a.decode()
                print('PASS: хэрэглэгч санах_ой_өгөгдөл/포트 격리, 잘못된 заагч/ELF, CPU 예외, 무한 давталт_утга 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(компьютер.бичих_мөр_6e8b375a)
                компьютер.Хаах()
    finally:
        Гарах_програм.set()
        일꾼.join(timeout=2)
        сервер_утга.close()
    결과['host_udp_received'] = [{'length': len(өгөгдөл), 'sha256': hashlib.sha256(өгөгдөл).hexdigest()} for өгөгдөл in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    Гүйцэтгэх_команд()
