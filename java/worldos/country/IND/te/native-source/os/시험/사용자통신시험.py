#!/usr/bin/env python3
"""వాస్తవ_డేటా ring 3 ELF/హోస్ట్ UDP 왕복/రక్షించు_మూల్యం దోషం/సమయం_మూల్యం 제한/잘못된 ELF를 검증한다."""
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

స్థానము = Path(__file__).resolve().parents[1]


class వర్చువల్_యంత్రం:
    def __init__(self, పాత్, 종류='elf', నెట్_వర్క్_మూల్యం=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        సంచయని_మూల్యం = Path(self.임시.name)
        self.లాగ్_వరుస = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.మానిటర్_మూల్యం = socket.socket(socket.AF_UNIX)
        직렬경로, మానిటర్_పథం = సంచయని_మూల్యం / 'serial.sock', సంచయని_మూల్యం / 'monitor.sock'
        ఆదేశము = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(మానిటర్_పథం) + ',server,nowait']
        ఆదేశము += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if నెట్_వర్క్_మూల్యం else ['-net', 'none']
        ఆదేశము += ['-kernel', str(పాత్)] if 종류 == 'elf' else ['-cdrom', str(పాత్), '-boot', 'd']
        if 저장매체 is not None:
            ఆదేశము += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.విధానం_మూల్యం = subprocess.Popen(ఆదేశము, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and మానిటర్_పథం.exists()):
                if self.విధానం_మూల్యం.poll() is not None:
                    raise AssertionError(self.విధానం_మూల్యం.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU నడుపుము సమయం_మూల్యం 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.మానిటర్_మూల్యం.connect(str(మానిటర్_పథం))
            self.직렬.setblocking(False)
            self.మానిటర్_మూల్యం.sendall(b'cont\n')
            self.వేచియుండు_స్థితి('jkoros> ')
        except BaseException:
            self.మూసివేయి()
            raise

    def వేచియుండు_స్థితి(self, 문구, నడుపుము=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.లాగ్_వరుస[నడుపుము:]:
                return self.లాగ్_వరుస[నడుపుము:].decode('utf-8', 'replace')
            చదువు, _, _ = select.select([self.직렬], [], [], 0.1)
            if చదువు:
                డేటా = self.직렬.recv(65536)
                if not డేటా: break
                self.లాగ్_వరుస.extend(డేటా)
            if self.విధానం_మూల్యం.poll() is not None: break
        raise AssertionError('వేచియుండు_మూల్యం వైఫల్యం_మూల్యం: ' + 문구 + '\n' + self.లాగ్_వరుస.decode('utf-8', 'replace'))

    def ఆదేశము(self, అక్షరసరం_మూల్యం, 기대):
        నడుపుము = len(self.లాగ్_వరుస)
        self.직렬.sendall((అక్షరసరం_మూల్యం + '\n').encode())
        ప్రమాణం = self.వేచియుండు_స్థితి('jkoros> ', నడుపుము)
        for 문구 in 기대:
            assert 문구 in ప్రమాణం, (అక్షరసరం_మూల్యం, 문구, ప్రమాణం)
        assert 'PANIC' not in ప్రమాణం, ప్రమాణం
        return ప్రమాణం

    def మూసివేయి(self):
        self.직렬.close()
        self.మానిటర్_మూల్యం.close()
        if self.విధానం_మూల్యం.poll() is None:
            self.విధానం_మూల్యం.terminate()
            try: self.విధానం_మూల్యం.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.విధానం_మూల్యం.kill()
                self.విధానం_మూల్యం.wait()
        self.విధానం_మూల్యం.communicate()
        self.임시.cleanup()


def 보호커널(సంచయని_మూల్యం):
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
    항목들 = ['hello=' + str(స్థానము / 'build/apps/hello.elf')]
    for పేరు, విషయం_మూల్యం in 사례들.items():
        వనరు = సంచయని_మూల్యం / (పేరు + '.s')
        వనరు.write_text('.code32\n.text\n.globl _start\n_start:\n' + విషయం_మూల్యం +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(సంచయని_మూల్యం / (పేరు + '.o')), str(వనరు)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(స్థానము.parent / 'compiler/వినియోగదారు_బంధం_లేవుట్.ld'),
                        '-o', str(సంచయని_మూల్యం / (పేరు + '.elf')), str(సంచయని_మూల్యం / (పేరు + '.o'))], check=True)
        항목들.append(పేరు + '=' + str(సంచయని_మూల్యం / (పేరు + '.elf')))
    정상 = bytearray((స్థానము / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    చెల్లని_ప్రమాణం = bytearray(정상); చెల్లని_ప్రమాణం[0] = 0; 변형들['badelf'] = చెల్లని_ప్రమాణం
    చెల్లని_ప్రమాణం = bytearray(정상); struct.pack_into('<I', చెల్లని_ప్రమాణం, 24, 0x00100000); 변형들['badentry'] = చెల్లని_ప్రమాణం
    చెల్లని_ప్రమాణం = bytearray(정상); struct.pack_into('<I', చెల్లని_ప్రమాణం, 28, 0x7fffffff); 변형들['badtable'] = చెల్లని_ప్రమాణం
    చెల్లని_ప్రమాణం = bytearray(정상); అంశం_శోధన_పట్టిక = struct.unpack_from('<I', చెల్లని_ప్రమాణం, 28)[0]
    struct.pack_into('<I', చెల్లని_ప్రమాణం, అంశం_శోధన_పట్టిక + 20, 0x7fffffff); 변형들['badsize'] = చెల్లని_ప్రమాణం
    for పేరు, డేటా in 변형들.items():
        దస్త్రం = సంచయని_మూల్యం / (పేరు + '.elf'); దస్త్రం.write_bytes(డేటా)
        항목들.append(పేరు + '=' + str(దస్త్రం))
    subprocess.run([sys.executable, str(స్థానము / 'ఉపకరణాలు/묶기.py'), '-o', str(సంచయని_మూల్యం / 'apps.bin')] + 항목들, check=True)
    వనరు = సంచయని_మూల్యం / 'apps.s'
    వనరు.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(సంచయని_మూల్యం / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(సంచయని_మూల్యం / 'apps.o'), str(వనరు)], check=True)
    కెర్నల్_మూల్యం = సంచయని_మూల్యం / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(స్థానము / '부팅/బంధం_లేవుట్.ld'), '-o', str(కెర్నల్_మూల్యం),
                    str(స్థానము / 'build/boot.o'), str(స్థానము / 'build/java.o'), str(స్థానము / 'build/user.o'), str(సంచయని_మూల్యం / 'apps.o')], check=True)
    return కెర్నల్_మూల్యం


def అమలు_చేయి_ఆదేశం():
    ప్రమాణం = {}
    సర్వర్_మూల్యం = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    సర్వర్_మూల్యం.bind(('127.0.0.1', 0))
    సర్వర్_మూల్యం.settimeout(0.1)
    పోర్టు_మూల్యం = సర్వర్_మూల్యం.getsockname()[1]
    받은것 = []
    నిష్క్రమణ_అనువర్తనం = threading.Event()
    def 되보내기():
        while not నిష్క్రమణ_అనువర్తనం.is_set():
            try: డేటా, పియర్_మూల్యం = సర్వర్_మూల్యం.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(డేటా)
            if డేటా != b'drop-me': సర్వర్_మూల్యం.sendto(డేటా, పియర్_మూల్యం)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            యంత్రం = వర్చువల్_యంత్రం(స్థానము / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                యంత్రం.ఆదేశము('apps', ['hello', 'udp', 'netcheck', 'stress'])
                యంత్రం.ఆదేశము('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                యంత్రం.ఆదేశము('run missing', ['Exit: -2'])
                యంత్రం.ఆదేశము('net', ['NET RTL8139'])
                యంత్రం.ఆదేశము('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for విషయం_మూల్యం in ('hello-network', 'odd', 'even', 'repeat-123'):
                    యంత్రం.ఆదేశము('run udp 10.0.2.2 {} {}'.format(పోర్టు_మూల్యం, విషయం_మూల్యం), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert విషయం_మూల్యం.encode() in 받은것, 'హోస్ట్ 서버에서 자료를 받지 못함'
                యంత్రం.ఆదేశము('run stress {}'.format(పోర్టు_మూల్యం), ['UDP STRESS PASS', 'Exit: 0'])
                యంత్రం.ఆదేశము('run udp 10.0.2.2 {} drop-me'.format(పోర్టు_మూల్యం), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                యంత్రం.ఆదేశము('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ప్రమాణం[종류] = యంత్రం.లాగ్_వరుస.decode('utf-8', 'replace')
                print('PASS: {} వినియోగదారు ELF/ring 3/인수/UDP హోస్ట్ 왕복/సమయం_మూల్యం 초과/షెల్ 복귀'.format(종류), flush=True)
            finally:
                try: యంత్రం.ఆదేశము('net', [])
                except Exception: pass
                (స్థానము / 'build/사용자통신-last.log').write_bytes(యంత్రం.లాగ్_వరుస)
                యంత్రం.మూసివేయి()
        యంత్రం = వర్చువల్_యంత్రం(స్థానము / 'build/kernel.elf', నెట్_వర్క్_మూల్యం=False)
        try:
            యంత్రం.ఆదేశము('net', ['NET unavailable'])
            యంత్రం.ఆదేశము('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            యంత్రం.ఆదేశము('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ప్రమాణం['no_nic'] = యంత్రం.లాగ్_వరుస.decode()
        finally: యంత్రం.మూసివేయి()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            యంత్రం = వర్చువల్_యంత్రం(보호커널(Path(임시)), నెట్_వర్క్_మూల్యం=False)
            try:
                for పేరు, స్థితి_మూల్యం in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    యంత్రం.ఆదేశము('run ' + పేరు, ['Exit: ' + str(స్థితి_మూల్యం)])
                    యంత్రం.ఆదేశము('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ప్రమాణం['protection'] = యంత్రం.లాగ్_వరుస.decode()
                print('PASS: వినియోగదారు మెమరీ_డేటా/포트 격리, 잘못된 పాయింటర్/ELF, CPU మినహాయింపు, 무한 పునరావృతం_మూల్యం 제한', flush=True)
            finally:
                (స్థానము / 'build/보호시험-last.log').write_bytes(యంత్రం.లాగ్_వరుస)
                యంత్రం.మూసివేయి()
    finally:
        నిష్క్రమణ_అనువర్తనం.set()
        일꾼.join(timeout=2)
        సర్వర్_మూల్యం.close()
    ప్రమాణం['host_udp_received'] = [{'length': len(డేటా), 'sha256': hashlib.sha256(డేటా).hexdigest()} for డేటా in 받은것]
    (స్థానము / 'build/사용자통신시험.json').write_text(json.dumps(ప్రమాణం, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    అమలు_చేయి_ఆదేశం()
