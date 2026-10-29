#!/usr/bin/env python3
"""ǹdịnezie_datà ring 3 ELF/usu UDP 왕복/nchedo_valuu mmejọ/시간 제한/잘못된 ELF를 검증한다."""
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


class kendìnuchè_ngwa_komputa:
    def __init__(self, ụzọ_ozi, 종류='elf', Netwọọkụ_valuu=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        dàịrektrị_valuu = Path(self.임시.name)
        self.ndekọ_NDEKỌ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.enyo_kọmputà_valuu = socket.socket(socket.AF_UNIX)
        직렬경로, enyo_kọmputà_ụzọ_ozi = dàịrektrị_valuu / 'serial.sock', dàịrektrị_valuu / 'monitor.sock'
        Ntiiwu = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(enyo_kọmputà_ụzọ_ozi) + ',server,nowait']
        Ntiiwu += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Netwọọkụ_valuu else ['-net', 'none']
        Ntiiwu += ['-kernel', str(ụzọ_ozi)] if 종류 == 'elf' else ['-cdrom', str(ụzọ_ozi), '-boot', 'd']
        if 저장매체 is not None:
            Ntiiwu += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ùsòrò_valuu_6712bde7 = subprocess.Popen(Ntiiwu, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and enyo_kọmputà_ụzọ_ozi.exists()):
                if self.ùsòrò_valuu_6712bde7.poll() is not None:
                    raise AssertionError(self.ùsòrò_valuu_6712bde7.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Bido 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.enyo_kọmputà_valuu.connect(str(enyo_kọmputà_ụzọ_ozi))
            self.직렬.setblocking(False)
            self.enyo_kọmputà_valuu.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Mechie()
            raise

    def 기다림(self, 문구, Bido=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ndekọ_NDEKỌ[Bido:]:
                return self.ndekọ_NDEKỌ[Bido:].decode('utf-8', 'replace')
            Wepụta_ọzi, _, _ = select.select([self.직렬], [], [], 0.1)
            if Wepụta_ọzi:
                datà = self.직렬.recv(65536)
                if not datà: break
                self.ndekọ_NDEKỌ.extend(datà)
            if self.ùsòrò_valuu_6712bde7.poll() is not None: break
        raise AssertionError('대기 ọdịdà_valuu: ' + 문구 + '\n' + self.ndekọ_NDEKỌ.decode('utf-8', 'replace'))

    def Ntiiwu(self, ùsòròokwū_valuu, 기대):
        Bido = len(self.ndekọ_NDEKỌ)
        self.직렬.sendall((ùsòròokwū_valuu + '\n').encode())
        결과 = self.기다림('jkoros> ', Bido)
        for 문구 in 기대:
            assert 문구 in 결과, (ùsòròokwū_valuu, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Mechie(self):
        self.직렬.close()
        self.enyo_kọmputà_valuu.close()
        if self.ùsòrò_valuu_6712bde7.poll() is None:
            self.ùsòrò_valuu_6712bde7.terminate()
            try: self.ùsòrò_valuu_6712bde7.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ùsòrò_valuu_6712bde7.kill()
                self.ùsòrò_valuu_6712bde7.wait()
        self.ùsòrò_valuu_6712bde7.communicate()
        self.임시.cleanup()


def 보호커널(dàịrektrị_valuu):
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
    for Aha, ndịnà_valuu in 사례들.items():
        ebensìbịa = dàịrektrị_valuu / (Aha + '.s')
        ebensìbịa.write_text('.code32\n.text\n.globl _start\n_start:\n' + ndịnà_valuu +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(dàịrektrị_valuu / (Aha + '.o')), str(ebensìbịa)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/òjìàrụ_Njikọ_Nhàzi.ld'),
                        '-o', str(dàịrektrị_valuu / (Aha + '.elf')), str(dàịrektrị_valuu / (Aha + '.o'))], check=True)
        항목들.append(Aha + '=' + str(dàịrektrị_valuu / (Aha + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Aha, datà in 변형들.items():
        Faịlụ = dàịrektrị_valuu / (Aha + '.elf'); Faịlụ.write_bytes(datà)
        항목들.append(Aha + '=' + str(Faịlụ))
    subprocess.run([sys.executable, str(위치 / 'Ngwaọrụ/묶기.py'), '-o', str(dàịrektrị_valuu / 'apps.bin')] + 항목들, check=True)
    ebensìbịa = dàịrektrị_valuu / 'apps.s'
    ebensìbịa.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(dàịrektrị_valuu / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(dàịrektrị_valuu / 'apps.o'), str(ebensìbịa)], check=True)
    mkpụrụobī_kọmpùta_valuu = dàịrektrị_valuu / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Njikọ_Nhàzi.ld'), '-o', str(mkpụrụobī_kọmpùta_valuu),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(dàịrektrị_valuu / 'apps.o')], check=True)
    return mkpụrụobī_kọmpùta_valuu


def mee_nnyemiwu():
    결과 = {}
    savà_valuu = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    savà_valuu.bind(('127.0.0.1', 0))
    savà_valuu.settimeout(0.1)
    pọọt_valuu = savà_valuu.getsockname()[1]
    받은것 = []
    pụọ_app = threading.Event()
    def 되보내기():
        while not pụọ_app.is_set():
            try: datà, ibè_valuu = savà_valuu.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(datà)
            if datà != b'drop-me': savà_valuu.sendto(datà, ibè_valuu)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ngwa_komputa.Ntiiwu('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ngwa_komputa.Ntiiwu('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ngwa_komputa.Ntiiwu('run missing', ['Exit: -2'])
                ngwa_komputa.Ntiiwu('net', ['NET RTL8139'])
                ngwa_komputa.Ntiiwu('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ndịnà_valuu in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ngwa_komputa.Ntiiwu('run udp 10.0.2.2 {} {}'.format(pọọt_valuu, ndịnà_valuu), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ndịnà_valuu.encode() in 받은것, 'usu 서버에서 자료를 받지 못함'
                ngwa_komputa.Ntiiwu('run stress {}'.format(pọọt_valuu), ['UDP STRESS PASS', 'Exit: 0'])
                ngwa_komputa.Ntiiwu('run udp 10.0.2.2 {} drop-me'.format(pọọt_valuu), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ngwa_komputa.Ntiiwu('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = ngwa_komputa.ndekọ_NDEKỌ.decode('utf-8', 'replace')
                print('PASS: {} òjìàrụ ELF/ring 3/인수/UDP usu 왕복/시간 초과/nkọwannyemiwu 복귀'.format(종류), flush=True)
            finally:
                try: ngwa_komputa.Ntiiwu('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(ngwa_komputa.ndekọ_NDEKỌ)
                ngwa_komputa.Mechie()
        ngwa_komputa = kendìnuchè_ngwa_komputa(위치 / 'build/kernel.elf', Netwọọkụ_valuu=False)
        try:
            ngwa_komputa.Ntiiwu('net', ['NET unavailable'])
            ngwa_komputa.Ntiiwu('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ngwa_komputa.Ntiiwu('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = ngwa_komputa.ndekọ_NDEKỌ.decode()
        finally: ngwa_komputa.Mechie()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ngwa_komputa = kendìnuchè_ngwa_komputa(보호커널(Path(임시)), Netwọọkụ_valuu=False)
            try:
                for Aha, ọnọdụ_valuu in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ngwa_komputa.Ntiiwu('run ' + Aha, ['Exit: ' + str(ọnọdụ_valuu)])
                    ngwa_komputa.Ntiiwu('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = ngwa_komputa.ndekọ_NDEKỌ.decode()
                print('PASS: òjìàrụ memọrị_datà/ngwaike_pọọt 격리, 잘못된 nrụaka/ELF, CPU 예외, 무한 memmekwa_valuu 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(ngwa_komputa.ndekọ_NDEKỌ)
                ngwa_komputa.Mechie()
    finally:
        pụọ_app.set()
        일꾼.join(timeout=2)
        savà_valuu.close()
    결과['host_udp_received'] = [{'length': len(datà), 'sha256': hashlib.sha256(datà).hexdigest()} for datà in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    mee_nnyemiwu()
