#!/usr/bin/env python3
"""gangan_détà ring 3 ELF/olùpèsè UDP 왕복/dáàbòbò_iye àṣìṣe/시간 제한/잘못된 ELF를 검증한다."""
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


class àfojúunúṣe_maṣíìnì:
    def __init__(self, ọ̀nà, 종류='elf', Alásopọ̀_iye=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        àkójọpọ̀_fáìlì_iye = Path(self.임시.name)
        self.àkọsílẹ̀_ìṣe_ìlà_ìbú = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.aṣàfihàn_iye = socket.socket(socket.AF_UNIX)
        직렬경로, aṣàfihàn_ọ̀nà = àkójọpọ̀_fáìlì_iye / 'serial.sock', àkójọpọ̀_fáìlì_iye / 'monitor.sock'
        Àṣẹ = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(aṣàfihàn_ọ̀nà) + ',server,nowait']
        Àṣẹ += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Alásopọ̀_iye else ['-net', 'none']
        Àṣẹ += ['-kernel', str(ọ̀nà)] if 종류 == 'elf' else ['-cdrom', str(ọ̀nà), '-boot', 'd']
        if 저장매체 is not None:
            Àṣẹ += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Ìlànà_iye = subprocess.Popen(Àṣẹ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and aṣàfihàn_ọ̀nà.exists()):
                if self.Ìlànà_iye.poll() is not None:
                    raise AssertionError(self.Ìlànà_iye.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Rọ́ọ̀nù 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.aṣàfihàn_iye.connect(str(aṣàfihàn_ọ̀nà))
            self.직렬.setblocking(False)
            self.aṣàfihàn_iye.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Ti()
            raise

    def 기다림(self, 문구, Rọ́ọ̀nù=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:]:
                return self.àkọsílẹ̀_ìṣe_ìlà_ìbú[Rọ́ọ̀nù:].decode('utf-8', 'replace')
            Kàá, _, _ = select.select([self.직렬], [], [], 0.1)
            if Kàá:
                détà = self.직렬.recv(65536)
                if not détà: break
                self.àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(détà)
            if self.Ìlànà_iye.poll() is not None: break
        raise AssertionError('대기 ìkùnà_iye: ' + 문구 + '\n' + self.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace'))

    def Àṣẹ(self, fọ́nrán_iye, 기대):
        Rọ́ọ̀nù = len(self.àkọsílẹ̀_ìṣe_ìlà_ìbú)
        self.직렬.sendall((fọ́nrán_iye + '\n').encode())
        결과 = self.기다림('jkoros> ', Rọ́ọ̀nù)
        for 문구 in 기대:
            assert 문구 in 결과, (fọ́nrán_iye, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Ti(self):
        self.직렬.close()
        self.aṣàfihàn_iye.close()
        if self.Ìlànà_iye.poll() is None:
            self.Ìlànà_iye.terminate()
            try: self.Ìlànà_iye.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Ìlànà_iye.kill()
                self.Ìlànà_iye.wait()
        self.Ìlànà_iye.communicate()
        self.임시.cleanup()


def 보호커널(àkójọpọ̀_fáìlì_iye):
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
    for Orúkọ, Àkóónú_iye in 사례들.items():
        orísun = àkójọpọ̀_fáìlì_iye / (Orúkọ + '.s')
        orísun.write_text('.code32\n.text\n.globl _start\n_start:\n' + Àkóónú_iye +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(àkójọpọ̀_fáìlì_iye / (Orúkọ + '.o')), str(orísun)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/aṣàmúlò_ṣàsopọ̀_ètò_ìrísí.ld'),
                        '-o', str(àkójọpọ̀_fáìlì_iye / (Orúkọ + '.elf')), str(àkójọpọ̀_fáìlì_iye / (Orúkọ + '.o'))], check=True)
        항목들.append(Orúkọ + '=' + str(àkójọpọ̀_fáìlì_iye / (Orúkọ + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Orúkọ, détà in 변형들.items():
        Fáìlì = àkójọpọ̀_fáìlì_iye / (Orúkọ + '.elf'); Fáìlì.write_bytes(détà)
        항목들.append(Orúkọ + '=' + str(Fáìlì))
    subprocess.run([sys.executable, str(위치 / 'Àwọn_irinṣẹ́/묶기.py'), '-o', str(àkójọpọ̀_fáìlì_iye / 'apps.bin')] + 항목들, check=True)
    orísun = àkójọpọ̀_fáìlì_iye / 'apps.s'
    orísun.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(àkójọpọ̀_fáìlì_iye / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(àkójọpọ̀_fáìlì_iye / 'apps.o'), str(orísun)], check=True)
    kánẹ́ẹ̀lì_iye = àkójọpọ̀_fáìlì_iye / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/ṣàsopọ̀_ètò_ìrísí.ld'), '-o', str(kánẹ́ẹ̀lì_iye),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(àkójọpọ̀_fáìlì_iye / 'apps.o')], check=True)
    return kánẹ́ẹ̀lì_iye


def ṣiṣẹ́_àṣẹ():
    결과 = {}
    apèsè_iye = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    apèsè_iye.bind(('127.0.0.1', 0))
    apèsè_iye.settimeout(0.1)
    ojú_iye = apèsè_iye.getsockname()[1]
    받은것 = []
    jáde_àtòjọ_ètò = threading.Event()
    def 되보내기():
        while not jáde_àtòjọ_ètò.is_set():
            try: détà, ọ̀gbà_iye = apèsè_iye.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(détà)
            if détà != b'drop-me': apèsè_iye.sendto(détà, ọ̀gbà_iye)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                maṣíìnì.Àṣẹ('apps', ['hello', 'udp', 'netcheck', 'stress'])
                maṣíìnì.Àṣẹ('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                maṣíìnì.Àṣẹ('run missing', ['Exit: -2'])
                maṣíìnì.Àṣẹ('net', ['NET RTL8139'])
                maṣíìnì.Àṣẹ('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Àkóónú_iye in ('hello-network', 'odd', 'even', 'repeat-123'):
                    maṣíìnì.Àṣẹ('run udp 10.0.2.2 {} {}'.format(ojú_iye, Àkóónú_iye), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Àkóónú_iye.encode() in 받은것, 'olùpèsè 서버에서 자료를 받지 못함'
                maṣíìnì.Àṣẹ('run stress {}'.format(ojú_iye), ['UDP STRESS PASS', 'Exit: 0'])
                maṣíìnì.Àṣẹ('run udp 10.0.2.2 {} drop-me'.format(ojú_iye), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                maṣíìnì.Àṣẹ('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode('utf-8', 'replace')
                print('PASS: {} aṣàmúlò ELF/ring 3/인수/UDP olùpèsè 왕복/시간 초과/ṣẹ́ẹ̀lì 복귀'.format(종류), flush=True)
            finally:
                try: maṣíìnì.Àṣẹ('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
                maṣíìnì.Ti()
        maṣíìnì = àfojúunúṣe_maṣíìnì(위치 / 'build/kernel.elf', Alásopọ̀_iye=False)
        try:
            maṣíìnì.Àṣẹ('net', ['NET unavailable'])
            maṣíìnì.Àṣẹ('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            maṣíìnì.Àṣẹ('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode()
        finally: maṣíìnì.Ti()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            maṣíìnì = àfojúunúṣe_maṣíìnì(보호커널(Path(임시)), Alásopọ̀_iye=False)
            try:
                for Orúkọ, ipò_iye in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    maṣíìnì.Àṣẹ('run ' + Orúkọ, ['Exit: ' + str(ipò_iye)])
                    maṣíìnì.Àṣẹ('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú.decode()
                print('PASS: aṣàmúlò ibi_ìpamọ́_détà/ohun_èlò_alárídìmú_ojú 격리, 잘못된 ìtọ́ka/ELF, CPU 예외, 무한 àṣetúnṣe_iye 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(maṣíìnì.àkọsílẹ̀_ìṣe_ìlà_ìbú)
                maṣíìnì.Ti()
    finally:
        jáde_àtòjọ_ètò.set()
        일꾼.join(timeout=2)
        apèsè_iye.close()
    결과['host_udp_received'] = [{'length': len(détà), 'sha256': hashlib.sha256(détà).hexdigest()} for détà in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ṣiṣẹ́_àṣẹ()
