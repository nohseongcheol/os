#!/usr/bin/env python3
"""kgonthe_data ring 3 ELF/go_nea_ditirelo UDP 왕복/šireletša_boleng Phošo/시간 제한/잘못된 ELF를 검증한다."""
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


class sethalwa_motšhene:
    def __init__(self, Tsejana, 종류='elf', Netweke_boleng=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        lelokelelo_boleng = Path(self.임시.name)
        self.pego_rei = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.mmonithara_boleng = socket.socket(socket.AF_UNIX)
        직렬경로, mmonithara_tsela = lelokelelo_boleng / 'serial.sock', lelokelelo_boleng / 'monitor.sock'
        Taelo = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(mmonithara_tsela) + ',server,nowait']
        Taelo += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Netweke_boleng else ['-net', 'none']
        Taelo += ['-kernel', str(Tsejana)] if 종류 == 'elf' else ['-cdrom', str(Tsejana), '-boot', 'd']
        if 저장매체 is not None:
            Taelo += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.tiragalo_boleng = subprocess.Popen(Taelo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and mmonithara_tsela.exists()):
                if self.tiragalo_boleng.poll() is not None:
                    raise AssertionError(self.tiragalo_boleng.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Diriša 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.mmonithara_boleng.connect(str(mmonithara_tsela))
            self.직렬.setblocking(False)
            self.mmonithara_boleng.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Tswalela()
            raise

    def 기다림(self, 문구, Diriša=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.pego_rei[Diriša:]:
                return self.pego_rei[Diriša:].decode('utf-8', 'replace')
            Bala, _, _ = select.select([self.직렬], [], [], 0.1)
            if Bala:
                data = self.직렬.recv(65536)
                if not data: break
                self.pego_rei.extend(data)
            if self.tiragalo_boleng.poll() is not None: break
        raise AssertionError('대기 go_palelwa_boleng: ' + 문구 + '\n' + self.pego_rei.decode('utf-8', 'replace'))

    def Taelo(self, molokoloko_boleng, 기대):
        Diriša = len(self.pego_rei)
        self.직렬.sendall((molokoloko_boleng + '\n').encode())
        결과 = self.기다림('jkoros> ', Diriša)
        for 문구 in 기대:
            assert 문구 in 결과, (molokoloko_boleng, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Tswalela(self):
        self.직렬.close()
        self.mmonithara_boleng.close()
        if self.tiragalo_boleng.poll() is None:
            self.tiragalo_boleng.terminate()
            try: self.tiragalo_boleng.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.tiragalo_boleng.kill()
                self.tiragalo_boleng.wait()
        self.tiragalo_boleng.communicate()
        self.임시.cleanup()


def 보호커널(lelokelelo_boleng):
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
    for Leina, Diteng_boleng in 사례들.items():
        mohlodi = lelokelelo_boleng / (Leina + '.s')
        mohlodi.write_text('.code32\n.text\n.globl _start\n_start:\n' + Diteng_boleng +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(lelokelelo_boleng / (Leina + '.o')), str(mohlodi)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/mošomiši_linke_Sebopego.ld'),
                        '-o', str(lelokelelo_boleng / (Leina + '.elf')), str(lelokelelo_boleng / (Leina + '.o'))], check=True)
        항목들.append(Leina + '=' + str(lelokelelo_boleng / (Leina + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Leina, data in 변형들.items():
        Faele = lelokelelo_boleng / (Leina + '.elf'); Faele.write_bytes(data)
        항목들.append(Leina + '=' + str(Faele))
    subprocess.run([sys.executable, str(위치 / 'Ditholosi/묶기.py'), '-o', str(lelokelelo_boleng / 'apps.bin')] + 항목들, check=True)
    mohlodi = lelokelelo_boleng / 'apps.s'
    mohlodi.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(lelokelelo_boleng / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(lelokelelo_boleng / 'apps.o'), str(mohlodi)], check=True)
    khenele_boleng = lelokelelo_boleng / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/linke_Sebopego.ld'), '-o', str(khenele_boleng),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(lelokelelo_boleng / 'apps.o')], check=True)
    return khenele_boleng


def phethagatša_taelo():
    결과 = {}
    seba_boleng = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seba_boleng.bind(('127.0.0.1', 0))
    seba_boleng.settimeout(0.1)
    phote_boleng = seba_boleng.getsockname()[1]
    받은것 = []
    Etšwa_tirišo = threading.Event()
    def 되보내기():
        while not Etšwa_tirišo.is_set():
            try: data, sedirišwa_sa_legoro_le_tee_boleng = seba_boleng.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(data)
            if data != b'drop-me': seba_boleng.sendto(data, sedirišwa_sa_legoro_le_tee_boleng)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            motšhene = sethalwa_motšhene(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                motšhene.Taelo('apps', ['hello', 'udp', 'netcheck', 'stress'])
                motšhene.Taelo('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                motšhene.Taelo('run missing', ['Exit: -2'])
                motšhene.Taelo('net', ['NET RTL8139'])
                motšhene.Taelo('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Diteng_boleng in ('hello-network', 'odd', 'even', 'repeat-123'):
                    motšhene.Taelo('run udp 10.0.2.2 {} {}'.format(phote_boleng, Diteng_boleng), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Diteng_boleng.encode() in 받은것, 'go_nea_ditirelo 서버에서 자료를 받지 못함'
                motšhene.Taelo('run stress {}'.format(phote_boleng), ['UDP STRESS PASS', 'Exit: 0'])
                motšhene.Taelo('run udp 10.0.2.2 {} drop-me'.format(phote_boleng), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                motšhene.Taelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = motšhene.pego_rei.decode('utf-8', 'replace')
                print('PASS: {} mošomiši ELF/ring 3/인수/UDP go_nea_ditirelo 왕복/시간 초과/šele 복귀'.format(종류), flush=True)
            finally:
                try: motšhene.Taelo('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(motšhene.pego_rei)
                motšhene.Tswalela()
        motšhene = sethalwa_motšhene(위치 / 'build/kernel.elf', Netweke_boleng=False)
        try:
            motšhene.Taelo('net', ['NET unavailable'])
            motšhene.Taelo('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            motšhene.Taelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = motšhene.pego_rei.decode()
        finally: motšhene.Tswalela()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            motšhene = sethalwa_motšhene(보호커널(Path(임시)), Netweke_boleng=False)
            try:
                for Leina, boemo_boleng in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    motšhene.Taelo('run ' + Leina, ['Exit: ' + str(boemo_boleng)])
                    motšhene.Taelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = motšhene.pego_rei.decode()
                print('PASS: mošomiši memori_data/포트 격리, 잘못된 sešupi/ELF, CPU 예외, 무한 poeletšo_boleng 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(motšhene.pego_rei)
                motšhene.Tswalela()
    finally:
        Etšwa_tirišo.set()
        일꾼.join(timeout=2)
        seba_boleng.close()
    결과['host_udp_received'] = [{'length': len(data), 'sha256': hashlib.sha256(data).hexdigest()} for data in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    phethagatša_taelo()
