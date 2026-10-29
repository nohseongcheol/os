#!/usr/bin/env python3
"""воқеӣ_иттилоот ring 3 ELF/мизбон UDP 왕복/муҳофизат_кардан_қимат Хато/시간 제한/잘못된 ELF를 검증한다."""
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


class виртуалӣ_компютер:
    def __init__(self, масир, 종류='elf', Шабака_қимат=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        директория_қимат = Path(self.임시.name)
        self.сабт_кардан_сабт = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.монитор_қимат = socket.socket(socket.AF_UNIX)
        직렬경로, монитор_масир = директория_қимат / 'serial.sock', директория_қимат / 'monitor.sock'
        фармон = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(монитор_масир) + ',server,nowait']
        фармон += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Шабака_қимат else ['-net', 'none']
        фармон += ['-kernel', str(масир)] if 종류 == 'elf' else ['-cdrom', str(масир), '-boot', 'd']
        if 저장매체 is not None:
            фармон += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Раванд_қимат = subprocess.Popen(фармон, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and монитор_масир.exists()):
                if self.Раванд_қимат.poll() is not None:
                    raise AssertionError(self.Раванд_қимат.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU порча 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.монитор_қимат.connect(str(монитор_масир))
            self.직렬.setblocking(False)
            self.монитор_қимат.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Пӯшидан()
            raise

    def 기다림(self, 문구, порча=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.сабт_кардан_сабт[порча:]:
                return self.сабт_кардан_сабт[порча:].decode('utf-8', 'replace')
            Хондан, _, _ = select.select([self.직렬], [], [], 0.1)
            if Хондан:
                иттилоот = self.직렬.recv(65536)
                if not иттилоот: break
                self.сабт_кардан_сабт.extend(иттилоот)
            if self.Раванд_қимат.poll() is not None: break
        raise AssertionError('대기 нокомӣ_қимат: ' + 문구 + '\n' + self.сабт_кардан_сабт.decode('utf-8', 'replace'))

    def фармон(self, сатр_қимат_6ca8363c, 기대):
        порча = len(self.сабт_кардан_сабт)
        self.직렬.sendall((сатр_қимат_6ca8363c + '\n').encode())
        결과 = self.기다림('jkoros> ', порча)
        for 문구 in 기대:
            assert 문구 in 결과, (сатр_қимат_6ca8363c, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Пӯшидан(self):
        self.직렬.close()
        self.монитор_қимат.close()
        if self.Раванд_қимат.poll() is None:
            self.Раванд_қимат.terminate()
            try: self.Раванд_қимат.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Раванд_қимат.kill()
                self.Раванд_қимат.wait()
        self.Раванд_қимат.communicate()
        self.임시.cleanup()


def 보호커널(директория_қимат):
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
    for Ном, Мӯҳтаво_қимат in 사례들.items():
        манбаъ = директория_қимат / (Ном + '.s')
        манбаъ.write_text('.code32\n.text\n.globl _start\n_start:\n' + Мӯҳтаво_қимат +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(директория_қимат / (Ном + '.o')), str(манбаъ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/корбар_Пайванд_Тарҳбандӣ.ld'),
                        '-o', str(директория_қимат / (Ном + '.elf')), str(директория_қимат / (Ном + '.o'))], check=True)
        항목들.append(Ном + '=' + str(директория_қимат / (Ном + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Ном, иттилоот in 변형들.items():
        Файл = директория_қимат / (Ном + '.elf'); Файл.write_bytes(иттилоот)
        항목들.append(Ном + '=' + str(Файл))
    subprocess.run([sys.executable, str(위치 / 'Абзорҳо/묶기.py'), '-o', str(директория_қимат / 'apps.bin')] + 항목들, check=True)
    манбаъ = директория_қимат / 'apps.s'
    манбаъ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(директория_қимат / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(директория_қимат / 'apps.o'), str(манбаъ)], check=True)
    ҳаста_қимат = директория_қимат / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Пайванд_Тарҳбандӣ.ld'), '-o', str(ҳаста_қимат),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(директория_қимат / 'apps.o')], check=True)
    return ҳаста_қимат


def иҷро_кардан_фармон():
    결과 = {}
    сервер_қимат = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    сервер_қимат.bind(('127.0.0.1', 0))
    сервер_қимат.settimeout(0.1)
    порт_қимат = сервер_қимат.getsockname()[1]
    받은것 = []
    Баромад_барнома = threading.Event()
    def 되보내기():
        while not Баромад_барнома.is_set():
            try: иттилоот, ҳамсон_қимат = сервер_қимат.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(иттилоот)
            if иттилоот != b'drop-me': сервер_қимат.sendto(иттилоот, ҳамсон_қимат)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            компютер = виртуалӣ_компютер(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                компютер.фармон('apps', ['hello', 'udp', 'netcheck', 'stress'])
                компютер.фармон('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                компютер.фармон('run missing', ['Exit: -2'])
                компютер.фармон('net', ['NET RTL8139'])
                компютер.фармон('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Мӯҳтаво_қимат in ('hello-network', 'odd', 'even', 'repeat-123'):
                    компютер.фармон('run udp 10.0.2.2 {} {}'.format(порт_қимат, Мӯҳтаво_қимат), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Мӯҳтаво_қимат.encode() in 받은것, 'мизбон 서버에서 자료를 받지 못함'
                компютер.фармон('run stress {}'.format(порт_қимат), ['UDP STRESS PASS', 'Exit: 0'])
                компютер.фармон('run udp 10.0.2.2 {} drop-me'.format(порт_қимат), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                компютер.фармон('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = компютер.сабт_кардан_сабт.decode('utf-8', 'replace')
                print('PASS: {} корбар ELF/ring 3/인수/UDP мизбон 왕복/시간 초과/восит 복귀'.format(종류), flush=True)
            finally:
                try: компютер.фармон('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(компютер.сабт_кардан_сабт)
                компютер.Пӯшидан()
        компютер = виртуалӣ_компютер(위치 / 'build/kernel.elf', Шабака_қимат=False)
        try:
            компютер.фармон('net', ['NET unavailable'])
            компютер.фармон('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            компютер.фармон('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = компютер.сабт_кардан_сабт.decode()
        finally: компютер.Пӯшидан()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            компютер = виртуалӣ_компютер(보호커널(Path(임시)), Шабака_қимат=False)
            try:
                for Ном, вазъият_қимат in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    компютер.фармон('run ' + Ном, ['Exit: ' + str(вазъият_қимат)])
                    компютер.фармон('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = компютер.сабт_кардан_сабт.decode()
                print('PASS: корбар ҳофиза_иттилоот/포트 격리, 잘못된 курсор/ELF, CPU 예외, 무한 такрор_қимат 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(компютер.сабт_кардан_сабт)
                компютер.Пӯшидан()
    finally:
        Баромад_барнома.set()
        일꾼.join(timeout=2)
        сервер_қимат.close()
    결과['host_udp_received'] = [{'length': len(иттилоот), 'sha256': hashlib.sha256(иттилоот).hexdigest()} for иттилоот in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    иҷро_кардан_фармон()
