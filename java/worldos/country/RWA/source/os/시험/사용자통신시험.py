#!/usr/bin/env python3
"""nyakuri_amakurushingiro ring 3 ELF/gucumbikira UDP 왕복/kurinda_agaciro IKOSA/시간 제한/잘못된 ELF를 검증한다."""
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


class kidafatika_imashini:
    def __init__(self, Inzira, 종류='elf', Urusobemiyoboro_agaciro=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ububiko_agaciro_e5561a2b = Path(self.임시.name)
        self.kubika_umurongo = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.mugaragaza_agaciro = socket.socket(socket.AF_UNIX)
        직렬경로, mugaragaza_inzira = ububiko_agaciro_e5561a2b / 'serial.sock', ububiko_agaciro_e5561a2b / 'monitor.sock'
        Icyo_wifuza = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(mugaragaza_inzira) + ',server,nowait']
        Icyo_wifuza += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Urusobemiyoboro_agaciro else ['-net', 'none']
        Icyo_wifuza += ['-kernel', str(Inzira)] if 종류 == 'elf' else ['-cdrom', str(Inzira), '-boot', 'd']
        if 저장매체 is not None:
            Icyo_wifuza += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Inzira_agaciro = subprocess.Popen(Icyo_wifuza, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and mugaragaza_inzira.exists()):
                if self.Inzira_agaciro.poll() is not None:
                    raise AssertionError(self.Inzira_agaciro.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ihuriro 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.mugaragaza_agaciro.connect(str(mugaragaza_inzira))
            self.직렬.setblocking(False)
            self.mugaragaza_agaciro.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Gufunga()
            raise

    def 기다림(self, 문구, ihuriro=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.kubika_umurongo[ihuriro:]:
                return self.kubika_umurongo[ihuriro:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                amakurushingiro = self.직렬.recv(65536)
                if not amakurushingiro: break
                self.kubika_umurongo.extend(amakurushingiro)
            if self.Inzira_agaciro.poll() is not None: break
        raise AssertionError('대기 kudakora_agaciro: ' + 문구 + '\n' + self.kubika_umurongo.decode('utf-8', 'replace'))

    def Icyo_wifuza(self, igicenteruro_agaciro, 기대):
        ihuriro = len(self.kubika_umurongo)
        self.직렬.sendall((igicenteruro_agaciro + '\n').encode())
        결과 = self.기다림('jkoros> ', ihuriro)
        for 문구 in 기대:
            assert 문구 in 결과, (igicenteruro_agaciro, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Gufunga(self):
        self.직렬.close()
        self.mugaragaza_agaciro.close()
        if self.Inzira_agaciro.poll() is None:
            self.Inzira_agaciro.terminate()
            try: self.Inzira_agaciro.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Inzira_agaciro.kill()
                self.Inzira_agaciro.wait()
        self.Inzira_agaciro.communicate()
        self.임시.cleanup()


def 보호커널(ububiko_agaciro_e5561a2b):
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
    for Izina, Ibirimo_agaciro in 사례들.items():
        Inkomoko = ububiko_agaciro_e5561a2b / (Izina + '.s')
        Inkomoko.write_text('.code32\n.text\n.globl _start\n_start:\n' + Ibirimo_agaciro +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ububiko_agaciro_e5561a2b / (Izina + '.o')), str(Inkomoko)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/ukoresha_Ihuza_Imimerere.ld'),
                        '-o', str(ububiko_agaciro_e5561a2b / (Izina + '.elf')), str(ububiko_agaciro_e5561a2b / (Izina + '.o'))], check=True)
        항목들.append(Izina + '=' + str(ububiko_agaciro_e5561a2b / (Izina + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Izina, amakurushingiro in 변형들.items():
        Idosiye = ububiko_agaciro_e5561a2b / (Izina + '.elf'); Idosiye.write_bytes(amakurushingiro)
        항목들.append(Izina + '=' + str(Idosiye))
    subprocess.run([sys.executable, str(위치 / 'Ibikoresho/묶기.py'), '-o', str(ububiko_agaciro_e5561a2b / 'apps.bin')] + 항목들, check=True)
    Inkomoko = ububiko_agaciro_e5561a2b / 'apps.s'
    Inkomoko.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ububiko_agaciro_e5561a2b / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ububiko_agaciro_e5561a2b / 'apps.o'), str(Inkomoko)], check=True)
    intima_agaciro = ububiko_agaciro_e5561a2b / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Ihuza_Imimerere.ld'), '-o', str(intima_agaciro),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(ububiko_agaciro_e5561a2b / 'apps.o')], check=True)
    return intima_agaciro


def gukora_ibwiriza():
    결과 = {}
    seriveri_agaciro = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seriveri_agaciro.bind(('127.0.0.1', 0))
    seriveri_agaciro.settimeout(0.1)
    poti_agaciro = seriveri_agaciro.getsockname()[1]
    받은것 = []
    gusohoka_porogaramu = threading.Event()
    def 되보내기():
        while not gusohoka_porogaramu.is_set():
            try: amakurushingiro, Mugenzi_agaciro = seriveri_agaciro.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(amakurushingiro)
            if amakurushingiro != b'drop-me': seriveri_agaciro.sendto(amakurushingiro, Mugenzi_agaciro)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            imashini = kidafatika_imashini(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                imashini.Icyo_wifuza('apps', ['hello', 'udp', 'netcheck', 'stress'])
                imashini.Icyo_wifuza('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                imashini.Icyo_wifuza('run missing', ['Exit: -2'])
                imashini.Icyo_wifuza('net', ['NET RTL8139'])
                imashini.Icyo_wifuza('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Ibirimo_agaciro in ('hello-network', 'odd', 'even', 'repeat-123'):
                    imashini.Icyo_wifuza('run udp 10.0.2.2 {} {}'.format(poti_agaciro, Ibirimo_agaciro), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Ibirimo_agaciro.encode() in 받은것, 'gucumbikira 서버에서 자료를 받지 못함'
                imashini.Icyo_wifuza('run stress {}'.format(poti_agaciro), ['UDP STRESS PASS', 'Exit: 0'])
                imashini.Icyo_wifuza('run udp 10.0.2.2 {} drop-me'.format(poti_agaciro), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                imashini.Icyo_wifuza('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = imashini.kubika_umurongo.decode('utf-8', 'replace')
                print('PASS: {} ukoresha ELF/ring 3/인수/UDP gucumbikira 왕복/시간 초과/insomamabwiriza 복귀'.format(종류), flush=True)
            finally:
                try: imashini.Icyo_wifuza('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(imashini.kubika_umurongo)
                imashini.Gufunga()
        imashini = kidafatika_imashini(위치 / 'build/kernel.elf', Urusobemiyoboro_agaciro=False)
        try:
            imashini.Icyo_wifuza('net', ['NET unavailable'])
            imashini.Icyo_wifuza('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            imashini.Icyo_wifuza('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = imashini.kubika_umurongo.decode()
        finally: imashini.Gufunga()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            imashini = kidafatika_imashini(보호커널(Path(임시)), Urusobemiyoboro_agaciro=False)
            try:
                for Izina, imimerere_agaciro in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    imashini.Icyo_wifuza('run ' + Izina, ['Exit: ' + str(imimerere_agaciro)])
                    imashini.Icyo_wifuza('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = imashini.kubika_umurongo.decode()
                print('PASS: ukoresha ububiko_amakurushingiro/포트 격리, 잘못된 mwerekana/ELF, CPU 예외, 무한 isubiramo_agaciro 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(imashini.kubika_umurongo)
                imashini.Gufunga()
    finally:
        gusohoka_porogaramu.set()
        일꾼.join(timeout=2)
        seriveri_agaciro.close()
    결과['host_udp_received'] = [{'length': len(amakurushingiro), 'sha256': hashlib.sha256(amakurushingiro).hexdigest()} for amakurushingiro in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    gukora_ibwiriza()
