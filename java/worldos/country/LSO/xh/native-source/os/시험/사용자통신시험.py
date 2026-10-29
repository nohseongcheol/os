#!/usr/bin/env python3
"""eyona_yenzekileyo_iingcombolo ring 3 ELF/umsingathi UDP 왕복/khusela_ixabiso Impazamo/시간 제한/잘못된 ELF를 검증한다."""
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


class enembonakalo_yenyani_umatshini:
    def __init__(self, INDLELA, 종류='elf', Inethiwekhi_ixabiso=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        isalathisi_ixabiso_e5561a2b = Path(self.임시.name)
        self.ilog_umqolo = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.imonitha_ixabiso = socket.socket(socket.AF_UNIX)
        직렬경로, imonitha_indlela = isalathisi_ixabiso_e5561a2b / 'serial.sock', isalathisi_ixabiso_e5561a2b / 'monitor.sock'
        Umyalelo = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(imonitha_indlela) + ',server,nowait']
        Umyalelo += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if Inethiwekhi_ixabiso else ['-net', 'none']
        Umyalelo += ['-kernel', str(INDLELA)] if 종류 == 'elf' else ['-cdrom', str(INDLELA), '-boot', 'd']
        if 저장매체 is not None:
            Umyalelo += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.Inkqubo_ixabiso = subprocess.Popen(Umyalelo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and imonitha_indlela.exists()):
                if self.Inkqubo_ixabiso.poll() is not None:
                    raise AssertionError(self.Inkqubo_ixabiso.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU Phumeza 시간 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.imonitha_ixabiso.connect(str(imonitha_indlela))
            self.직렬.setblocking(False)
            self.imonitha_ixabiso.sendall(b'cont\n')
            self.기다림('jkoros> ')
        except BaseException:
            self.Vala()
            raise

    def 기다림(self, 문구, Phumeza=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ilog_umqolo[Phumeza:]:
                return self.ilog_umqolo[Phumeza:].decode('utf-8', 'replace')
            Funda, _, _ = select.select([self.직렬], [], [], 0.1)
            if Funda:
                iingcombolo = self.직렬.recv(65536)
                if not iingcombolo: break
                self.ilog_umqolo.extend(iingcombolo)
            if self.Inkqubo_ixabiso.poll() is not None: break
        raise AssertionError('대기 ukungaphumeleli_ixabiso: ' + 문구 + '\n' + self.ilog_umqolo.decode('utf-8', 'replace'))

    def Umyalelo(self, uluhlu_lweekharektha_ixabiso, 기대):
        Phumeza = len(self.ilog_umqolo)
        self.직렬.sendall((uluhlu_lweekharektha_ixabiso + '\n').encode())
        결과 = self.기다림('jkoros> ', Phumeza)
        for 문구 in 기대:
            assert 문구 in 결과, (uluhlu_lweekharektha_ixabiso, 문구, 결과)
        assert 'PANIC' not in 결과, 결과
        return 결과

    def Vala(self):
        self.직렬.close()
        self.imonitha_ixabiso.close()
        if self.Inkqubo_ixabiso.poll() is None:
            self.Inkqubo_ixabiso.terminate()
            try: self.Inkqubo_ixabiso.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.Inkqubo_ixabiso.kill()
                self.Inkqubo_ixabiso.wait()
        self.Inkqubo_ixabiso.communicate()
        self.임시.cleanup()


def 보호커널(isalathisi_ixabiso_e5561a2b):
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
    for Igama, Isiqulatho_ixabiso in 사례들.items():
        UMTHOMBO = isalathisi_ixabiso_e5561a2b / (Igama + '.s')
        UMTHOMBO.write_text('.code32\n.text\n.globl _start\n_start:\n' + Isiqulatho_ixabiso +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(isalathisi_ixabiso_e5561a2b / (Igama + '.o')), str(UMTHOMBO)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치.parent / 'compiler/umsebenzisi_Ilinki_ubume.ld'),
                        '-o', str(isalathisi_ixabiso_e5561a2b / (Igama + '.elf')), str(isalathisi_ixabiso_e5561a2b / (Igama + '.o'))], check=True)
        항목들.append(Igama + '=' + str(isalathisi_ixabiso_e5561a2b / (Igama + '.elf')))
    정상 = bytearray((위치 / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    잘못 = bytearray(정상); 잘못[0] = 0; 변형들['badelf'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 24, 0x00100000); 변형들['badentry'] = 잘못
    잘못 = bytearray(정상); struct.pack_into('<I', 잘못, 28, 0x7fffffff); 변형들['badtable'] = 잘못
    잘못 = bytearray(정상); 표 = struct.unpack_from('<I', 잘못, 28)[0]
    struct.pack_into('<I', 잘못, 표 + 20, 0x7fffffff); 변형들['badsize'] = 잘못
    for Igama, iingcombolo in 변형들.items():
        iFayili = isalathisi_ixabiso_e5561a2b / (Igama + '.elf'); iFayili.write_bytes(iingcombolo)
        항목들.append(Igama + '=' + str(iFayili))
    subprocess.run([sys.executable, str(위치 / 'Izixhobo/묶기.py'), '-o', str(isalathisi_ixabiso_e5561a2b / 'apps.bin')] + 항목들, check=True)
    UMTHOMBO = isalathisi_ixabiso_e5561a2b / 'apps.s'
    UMTHOMBO.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(isalathisi_ixabiso_e5561a2b / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(isalathisi_ixabiso_e5561a2b / 'apps.o'), str(UMTHOMBO)], check=True)
    ikheneli_ixabiso = isalathisi_ixabiso_e5561a2b / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(위치 / '부팅/Ilinki_ubume.ld'), '-o', str(ikheneli_ixabiso),
                    str(위치 / 'build/boot.o'), str(위치 / 'build/java.o'), str(위치 / 'build/user.o'), str(isalathisi_ixabiso_e5561a2b / 'apps.o')], check=True)
    return ikheneli_ixabiso


def ukwenza_umyalelo():
    결과 = {}
    iseva_ixabiso = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    iseva_ixabiso.bind(('127.0.0.1', 0))
    iseva_ixabiso.settimeout(0.1)
    iphothi_ixabiso = iseva_ixabiso.getsockname()[1]
    받은것 = []
    phuma_inkqubo = threading.Event()
    def 되보내기():
        while not phuma_inkqubo.is_set():
            try: iingcombolo, untanga_ixabiso = iseva_ixabiso.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(iingcombolo)
            if iingcombolo != b'drop-me': iseva_ixabiso.sendto(iingcombolo, untanga_ixabiso)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            umatshini = enembonakalo_yenyani_umatshini(위치 / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                umatshini.Umyalelo('apps', ['hello', 'udp', 'netcheck', 'stress'])
                umatshini.Umyalelo('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                umatshini.Umyalelo('run missing', ['Exit: -2'])
                umatshini.Umyalelo('net', ['NET RTL8139'])
                umatshini.Umyalelo('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for Isiqulatho_ixabiso in ('hello-network', 'odd', 'even', 'repeat-123'):
                    umatshini.Umyalelo('run udp 10.0.2.2 {} {}'.format(iphothi_ixabiso, Isiqulatho_ixabiso), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert Isiqulatho_ixabiso.encode() in 받은것, 'umsingathi 서버에서 자료를 받지 못함'
                umatshini.Umyalelo('run stress {}'.format(iphothi_ixabiso), ['UDP STRESS PASS', 'Exit: 0'])
                umatshini.Umyalelo('run udp 10.0.2.2 {} drop-me'.format(iphothi_ixabiso), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                umatshini.Umyalelo('run hello recovered', ['arg: recovered', 'Exit: 0'])
                결과[종류] = umatshini.ilog_umqolo.decode('utf-8', 'replace')
                print('PASS: {} umsebenzisi ELF/ring 3/인수/UDP umsingathi 왕복/시간 초과/isiniki_myalelo 복귀'.format(종류), flush=True)
            finally:
                try: umatshini.Umyalelo('net', [])
                except Exception: pass
                (위치 / 'build/사용자통신-last.log').write_bytes(umatshini.ilog_umqolo)
                umatshini.Vala()
        umatshini = enembonakalo_yenyani_umatshini(위치 / 'build/kernel.elf', Inethiwekhi_ixabiso=False)
        try:
            umatshini.Umyalelo('net', ['NET unavailable'])
            umatshini.Umyalelo('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            umatshini.Umyalelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
            결과['no_nic'] = umatshini.ilog_umqolo.decode()
        finally: umatshini.Vala()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            umatshini = enembonakalo_yenyani_umatshini(보호커널(Path(임시)), Inethiwekhi_ixabiso=False)
            try:
                for Igama, imo_ixabiso in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    umatshini.Umyalelo('run ' + Igama, ['Exit: ' + str(imo_ixabiso)])
                    umatshini.Umyalelo('run hello', ['USER MODE ring 3', 'Exit: 0'])
                결과['protection'] = umatshini.ilog_umqolo.decode()
                print('PASS: umsebenzisi imemori_iingcombolo/포트 격리, 잘못된 isalathisi/ELF, CPU 예외, 무한 uniko_lomyalelo_omnye_ixabiso 제한', flush=True)
            finally:
                (위치 / 'build/보호시험-last.log').write_bytes(umatshini.ilog_umqolo)
                umatshini.Vala()
    finally:
        phuma_inkqubo.set()
        일꾼.join(timeout=2)
        iseva_ixabiso.close()
    결과['host_udp_received'] = [{'length': len(iingcombolo), 'sha256': hashlib.sha256(iingcombolo).hexdigest()} for iingcombolo in 받은것]
    (위치 / 'build/사용자통신시험.json').write_text(json.dumps(결과, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ukwenza_umyalelo()
