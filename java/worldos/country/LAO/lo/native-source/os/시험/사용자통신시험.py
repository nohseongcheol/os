#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ ring 3 ELF/ໂຮສ UDP 왕복/ປົກປ້ອງ_ຄ່າ ຂໍ້ຜິດພາດ/ເວລາ_ຄ່າ 제한/잘못된 ELF를 검증한다."""
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

ຈັດຕໍາແຫນ່ງ = Path(__file__).resolve().parents[1]


class ຈໍາລອງ_ເຄື່ອງຈັກ:
    def __init__(self, ທາງໂຄຈອນ, 종류='elf', ເຄືອຂ່າຍ_ຄ່າ=True, 저장매체=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ກຸ່ມຂໍ້ມູນ_ຄ່າ = Path(self.임시.name)
        self.ບັນທຶກ_ແຖວ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.ຫນ້າຈໍ_ຄ່າ = socket.socket(socket.AF_UNIX)
        직렬경로, ຫນ້າຈໍ_ທາງໂຄຈອນ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'serial.sock', ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'monitor.sock'
        ຄໍາສັ່ງ_1f12b8e2 = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(ຫນ້າຈໍ_ທາງໂຄຈອນ) + ',server,nowait']
        ຄໍາສັ່ງ_1f12b8e2 += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if ເຄືອຂ່າຍ_ຄ່າ else ['-net', 'none']
        ຄໍາສັ່ງ_1f12b8e2 += ['-kernel', str(ທາງໂຄຈອນ)] if 종류 == 'elf' else ['-cdrom', str(ທາງໂຄຈອນ), '-boot', 'd']
        if 저장매체 is not None:
            ຄໍາສັ່ງ_1f12b8e2 += ['-drive', 'file=' + str(저장매체) + ',format=raw,if=ide,index=0']
        self.ຂະ_ບວນ_ການ_ຄ່າ = subprocess.Popen(ຄໍາສັ່ງ_1f12b8e2, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and ຫນ້າຈໍ_ທາງໂຄຈອນ.exists()):
                if self.ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None:
                    raise AssertionError(self.ຂະ_ບວນ_ການ_ຄ່າ.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU ແລ່ນ ເວລາ_ຄ່າ 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.ຫນ້າຈໍ_ຄ່າ.connect(str(ຫນ້າຈໍ_ທາງໂຄຈອນ))
            self.직렬.setblocking(False)
            self.ຫນ້າຈໍ_ຄ່າ.sendall(b'cont\n')
            self.ລໍຖ້າ_ສະຖານະ('jkoros> ')
        except BaseException:
            self.ປິດ()
            raise

    def ລໍຖ້າ_ສະຖານະ(self, 문구, ແລ່ນ=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.ບັນທຶກ_ແຖວ[ແລ່ນ:]:
                return self.ບັນທຶກ_ແຖວ[ແລ່ນ:].decode('utf-8', 'replace')
            읽기, _, _ = select.select([self.직렬], [], [], 0.1)
            if 읽기:
                ຂໍ້ມູນ = self.직렬.recv(65536)
                if not ຂໍ້ມູນ: break
                self.ບັນທຶກ_ແຖວ.extend(ຂໍ້ມູນ)
            if self.ຂະ_ບວນ_ການ_ຄ່າ.poll() is not None: break
        raise AssertionError('ລໍຖ້າ_ຄ່າ ຫຼົ້ມເຫຼວ_ຄ່າ: ' + 문구 + '\n' + self.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace'))

    def ຄໍາສັ່ງ_1f12b8e2(self, ສະຕຣິງ_ຄ່າ, 기대):
        ແລ່ນ = len(self.ບັນທຶກ_ແຖວ)
        self.직렬.sendall((ສະຕຣິງ_ຄ່າ + '\n').encode())
        ມາດຕະການ = self.ລໍຖ້າ_ສະຖານະ('jkoros> ', ແລ່ນ)
        for 문구 in 기대:
            assert 문구 in ມາດຕະການ, (ສະຕຣິງ_ຄ່າ, 문구, ມາດຕະການ)
        assert 'PANIC' not in ມາດຕະການ, ມາດຕະການ
        return ມາດຕະການ

    def ປິດ(self):
        self.직렬.close()
        self.ຫນ້າຈໍ_ຄ່າ.close()
        if self.ຂະ_ບວນ_ການ_ຄ່າ.poll() is None:
            self.ຂະ_ບວນ_ການ_ຄ່າ.terminate()
            try: self.ຂະ_ບວນ_ການ_ຄ່າ.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.ຂະ_ບວນ_ການ_ຄ່າ.kill()
                self.ຂະ_ບວນ_ການ_ຄ່າ.wait()
        self.ຂະ_ບວນ_ການ_ຄ່າ.communicate()
        self.임시.cleanup()


def 보호커널(ກຸ່ມຂໍ້ມູນ_ຄ່າ):
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
    항목들 = ['hello=' + str(ຈັດຕໍາແຫນ່ງ / 'build/apps/hello.elf')]
    for ຊື່, ເນື້ອໃນ_ຄ່າ_cb0f2404 in 사례들.items():
        ແຫຼ່ງທີ່ມາ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.s')
        ແຫຼ່ງທີ່ມາ.write_text('.code32\n.text\n.globl _start\n_start:\n' + ເນື້ອໃນ_ຄ່າ_cb0f2404 +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.o')), str(ແຫຼ່ງທີ່ມາ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ຈັດຕໍາແຫນ່ງ.parent / 'compiler/ຜູ້ໃຊ້_ລິ້ງ_ຮູບແບບ.ld'),
                        '-o', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.elf')), str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.o'))], check=True)
        항목들.append(ຊື່ + '=' + str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.elf')))
    정상 = bytearray((ຈັດຕໍາແຫນ່ງ / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ໃຊ້ບໍ່ໄດ້_ມາດຕະການ = bytearray(정상); ໃຊ້ບໍ່ໄດ້_ມາດຕະການ[0] = 0; 변형들['badelf'] = ໃຊ້ບໍ່ໄດ້_ມາດຕະການ
    ໃຊ້ບໍ່ໄດ້_ມາດຕະການ = bytearray(정상); struct.pack_into('<I', ໃຊ້ບໍ່ໄດ້_ມາດຕະການ, 24, 0x00100000); 변형들['badentry'] = ໃຊ້ບໍ່ໄດ້_ມາດຕະການ
    ໃຊ້ບໍ່ໄດ້_ມາດຕະການ = bytearray(정상); struct.pack_into('<I', ໃຊ້ບໍ່ໄດ້_ມາດຕະການ, 28, 0x7fffffff); 변형들['badtable'] = ໃຊ້ບໍ່ໄດ້_ມາດຕະການ
    ໃຊ້ບໍ່ໄດ້_ມາດຕະການ = bytearray(정상); ຄົ້ນຫາ_ຕາຕະລາງ = struct.unpack_from('<I', ໃຊ້ບໍ່ໄດ້_ມາດຕະການ, 28)[0]
    struct.pack_into('<I', ໃຊ້ບໍ່ໄດ້_ມາດຕະການ, ຄົ້ນຫາ_ຕາຕະລາງ + 20, 0x7fffffff); 변형들['badsize'] = ໃຊ້ບໍ່ໄດ້_ມາດຕະການ
    for ຊື່, ຂໍ້ມູນ in 변형들.items():
        ຟາຍ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / (ຊື່ + '.elf'); ຟາຍ.write_bytes(ຂໍ້ມູນ)
        항목들.append(ຊື່ + '=' + str(ຟາຍ))
    subprocess.run([sys.executable, str(ຈັດຕໍາແຫນ່ງ / 'ເຄື່ອງມື/묶기.py'), '-o', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'apps.bin')] + 항목들, check=True)
    ແຫຼ່ງທີ່ມາ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'apps.s'
    ແຫຼ່ງທີ່ມາ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'apps.o'), str(ແຫຼ່ງທີ່ມາ)], check=True)
    ແກນກາງ_ຄ່າ = ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ຈັດຕໍາແຫນ່ງ / '부팅/ລິ້ງ_ຮູບແບບ.ld'), '-o', str(ແກນກາງ_ຄ່າ),
                    str(ຈັດຕໍາແຫນ່ງ / 'build/boot.o'), str(ຈັດຕໍາແຫນ່ງ / 'build/java.o'), str(ຈັດຕໍາແຫນ່ງ / 'build/user.o'), str(ກຸ່ມຂໍ້ມູນ_ຄ່າ / 'apps.o')], check=True)
    return ແກນກາງ_ຄ່າ


def ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ():
    ມາດຕະການ = {}
    서버 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    서버.bind(('127.0.0.1', 0))
    서버.settimeout(0.1)
    ຜອດ_ຄ່າ = 서버.getsockname()[1]
    받은것 = []
    ອອກ_ແອັບ = threading.Event()
    def 되보내기():
        while not ອອກ_ແອັບ.is_set():
            try: ຂໍ້ມູນ, ລຸ້ນດຽວກັນ_ຄ່າ = 서버.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ຂໍ້ມູນ)
            if ຂໍ້ມູນ != b'drop-me': 서버.sendto(ຂໍ້ມູນ, ລຸ້ນດຽວກັນ_ຄ່າ)
    일꾼 = threading.Thread(target=되보내기, daemon=True)
    일꾼.start()
    try:
        for 종류 in ('elf', 'iso'):
            ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('apps', ['hello', 'udp', 'netcheck', 'stress'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run missing', ['Exit: -2'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('net', ['NET RTL8139'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for ເນື້ອໃນ_ຄ່າ_cb0f2404 in ('hello-network', 'odd', 'even', 'repeat-123'):
                    ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run udp 10.0.2.2 {} {}'.format(ຜອດ_ຄ່າ, ເນື້ອໃນ_ຄ່າ_cb0f2404), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert ເນື້ອໃນ_ຄ່າ_cb0f2404.encode() in 받은것, 'ໂຮສ 서버에서 자료를 받지 못함'
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run stress {}'.format(ຜອດ_ຄ່າ), ['UDP STRESS PASS', 'Exit: 0'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run udp 10.0.2.2 {} drop-me'.format(ຜອດ_ຄ່າ), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ມາດຕະການ[종류] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode('utf-8', 'replace')
                print('PASS: {} ຜູ້ໃຊ້ ELF/ring 3/인수/UDP ໂຮສ 왕복/ເວລາ_ຄ່າ 초과/ເຊລ 복귀'.format(종류), flush=True)
            finally:
                try: ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('net', [])
                except Exception: pass
                (ຈັດຕໍາແຫນ່ງ / 'build/사용자통신-last.log').write_bytes(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
                ເຄື່ອງຈັກ.ປິດ()
        ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(ຈັດຕໍາແຫນ່ງ / 'build/kernel.elf', ເຄືອຂ່າຍ_ຄ່າ=False)
        try:
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('net', ['NET unavailable'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ມາດຕະການ['no_nic'] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode()
        finally: ເຄື່ອງຈັກ.ປິດ()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            ເຄື່ອງຈັກ = ຈໍາລອງ_ເຄື່ອງຈັກ(보호커널(Path(임시)), ເຄືອຂ່າຍ_ຄ່າ=False)
            try:
                for ຊື່, ສະຖານະ_ຄ່າ in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run ' + ຊື່, ['Exit: ' + str(ສະຖານະ_ຄ່າ)])
                    ເຄື່ອງຈັກ.ຄໍາສັ່ງ_1f12b8e2('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ມາດຕະການ['protection'] = ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ.decode()
                print('PASS: ຜູ້ໃຊ້ ຄວາມຈໍາ_ຂໍ້ມູນ/포트 격리, 잘못된 ລູກສອນເມົ້າ/ELF, CPU ຂໍ້ຍົກເວັ້ນ, 무한 ສະປຣິນ_ຄ່າ 제한', flush=True)
            finally:
                (ຈັດຕໍາແຫນ່ງ / 'build/보호시험-last.log').write_bytes(ເຄື່ອງຈັກ.ບັນທຶກ_ແຖວ)
                ເຄື່ອງຈັກ.ປິດ()
    finally:
        ອອກ_ແອັບ.set()
        일꾼.join(timeout=2)
        서버.close()
    ມາດຕະການ['host_udp_received'] = [{'length': len(ຂໍ້ມູນ), 'sha256': hashlib.sha256(ຂໍ້ມູນ).hexdigest()} for ຂໍ້ມູນ in 받은것]
    (ຈັດຕໍາແຫນ່ງ / 'build/사용자통신시험.json').write_text(json.dumps(ມາດຕະການ, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ()
