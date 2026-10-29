#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล ring 3 ELF/โฮสต์ UDP 왕복/ป้องกัน_ค่า ข้อผิดพลาด/ค่าเวลา 제한/잘못된 ELF를 검증한다."""
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

ตําแหน่ง = Path(__file__).resolve().parents[1]


class เครื่องเสมือน:
    def __init__(self, เส้นทาง, 종류='elf', เครือข่าย_ค่า=True, ที่เก็บ_กลาง=None):
        self.임시 = tempfile.TemporaryDirectory(prefix='jkoros-user-test-')
        ไดเรกทอรี_ค่า = Path(self.임시.name)
        self.บันทึก_สถิติ = bytearray()
        self.직렬 = socket.socket(socket.AF_UNIX)
        self.จอภาพ_ค่า = socket.socket(socket.AF_UNIX)
        직렬경로, จอภาพ_พาธ = ไดเรกทอรี_ค่า / 'serial.sock', ไดเรกทอรี_ค่า / 'monitor.sock'
        คําสั่ง = ['qemu-system-i386', '-m', '64M', '-display', 'none', '-no-reboot', '-S',
                '-serial', 'unix:' + str(직렬경로) + ',server,nowait',
                '-monitor', 'unix:' + str(จอภาพ_พาธ) + ',server,nowait']
        คําสั่ง += ['-netdev', 'user,id=net0', '-device', 'rtl8139,netdev=net0'] if เครือข่าย_ค่า else ['-net', 'none']
        คําสั่ง += ['-kernel', str(เส้นทาง)] if 종류 == 'elf' else ['-cdrom', str(เส้นทาง), '-boot', 'd']
        if ที่เก็บ_กลาง is not None:
            คําสั่ง += ['-drive', 'file=' + str(ที่เก็บ_กลาง) + ',format=raw,if=ide,index=0']
        self.กระบวนการ_ค่า = subprocess.Popen(คําสั่ง, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            끝 = time.monotonic() + 10
            while not (직렬경로.exists() and จอภาพ_พาธ.exists()):
                if self.กระบวนการ_ค่า.poll() is not None:
                    raise AssertionError(self.กระบวนการ_ค่า.stderr.read().decode())
                if time.monotonic() > 끝: raise AssertionError('QEMU เรียกใช้งาน ค่าเวลา 초과')
                time.sleep(0.03)
            self.직렬.connect(str(직렬경로))
            self.จอภาพ_ค่า.connect(str(จอภาพ_พาธ))
            self.직렬.setblocking(False)
            self.จอภาพ_ค่า.sendall(b'cont\n')
            self.ภาวะรอ('jkoros> ')
        except BaseException:
            self.ปิด()
            raise

    def ภาวะรอ(self, 문구, เรียกใช้งาน=0, 제한=15):
        끝 = time.monotonic() + 제한
        while time.monotonic() < 끝:
            if 문구.encode() in self.บันทึก_สถิติ[เรียกใช้งาน:]:
                return self.บันทึก_สถิติ[เรียกใช้งาน:].decode('utf-8', 'replace')
            อ่าน, _, _ = select.select([self.직렬], [], [], 0.1)
            if อ่าน:
                ข้อมูล = self.직렬.recv(65536)
                if not ข้อมูล: break
                self.บันทึก_สถิติ.extend(ข้อมูล)
            if self.กระบวนการ_ค่า.poll() is not None: break
        raise AssertionError('รอเดี๋ยว_ค่า ความล้มเหลว_ค่า: ' + 문구 + '\n' + self.บันทึก_สถิติ.decode('utf-8', 'replace'))

    def คําสั่ง(self, สตริง_ค่า, 기대):
        เรียกใช้งาน = len(self.บันทึก_สถิติ)
        self.직렬.sendall((สตริง_ค่า + '\n').encode())
        ผลลัพธ์ = self.ภาวะรอ('jkoros> ', เรียกใช้งาน)
        for 문구 in 기대:
            assert 문구 in ผลลัพธ์, (สตริง_ค่า, 문구, ผลลัพธ์)
        assert 'PANIC' not in ผลลัพธ์, ผลลัพธ์
        return ผลลัพธ์

    def ปิด(self):
        self.직렬.close()
        self.จอภาพ_ค่า.close()
        if self.กระบวนการ_ค่า.poll() is None:
            self.กระบวนการ_ค่า.terminate()
            try: self.กระบวนการ_ค่า.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.กระบวนการ_ค่า.kill()
                self.กระบวนการ_ค่า.wait()
        self.กระบวนการ_ค่า.communicate()
        self.임시.cleanup()


def 보호커널(ไดเรกทอรี_ค่า):
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
    항목들 = ['hello=' + str(ตําแหน่ง / 'build/apps/hello.elf')]
    for ชื่อ, เนื้อหา_ค่า in 사례들.items():
        รหัสต้นฉบับ = ไดเรกทอรี_ค่า / (ชื่อ + '.s')
        รหัสต้นฉบับ.write_text('.code32\n.text\n.globl _start\n_start:\n' + เนื้อหา_ค่า +
                       '\nmovl $99,%ebx\nxorl %eax,%eax\nint $0x80\n.section .note.GNU-stack,"",@progbits\n')
        subprocess.run(['as', '--32', '-o', str(ไดเรกทอรี_ค่า / (ชื่อ + '.o')), str(รหัสต้นฉบับ)], check=True)
        subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ตําแหน่ง.parent / 'compiler/ผู้ใช้_ลิงก์_การนําทาง.ld'),
                        '-o', str(ไดเรกทอรี_ค่า / (ชื่อ + '.elf')), str(ไดเรกทอรี_ค่า / (ชื่อ + '.o'))], check=True)
        항목들.append(ชื่อ + '=' + str(ไดเรกทอรี_ค่า / (ชื่อ + '.elf')))
    정상 = bytearray((ตําแหน่ง / 'build/apps/hello.elf').read_bytes())
    변형들 = {}
    ไม่ถูกต้อง_เมตริก = bytearray(정상); ไม่ถูกต้อง_เมตริก[0] = 0; 변형들['badelf'] = ไม่ถูกต้อง_เมตริก
    ไม่ถูกต้อง_เมตริก = bytearray(정상); struct.pack_into('<I', ไม่ถูกต้อง_เมตริก, 24, 0x00100000); 변형들['badentry'] = ไม่ถูกต้อง_เมตริก
    ไม่ถูกต้อง_เมตริก = bytearray(정상); struct.pack_into('<I', ไม่ถูกต้อง_เมตริก, 28, 0x7fffffff); 변형들['badtable'] = ไม่ถูกต้อง_เมตริก
    ไม่ถูกต้อง_เมตริก = bytearray(정상); การค้นหา_ตาราง = struct.unpack_from('<I', ไม่ถูกต้อง_เมตริก, 28)[0]
    struct.pack_into('<I', ไม่ถูกต้อง_เมตริก, การค้นหา_ตาราง + 20, 0x7fffffff); 변형들['badsize'] = ไม่ถูกต้อง_เมตริก
    for ชื่อ, ข้อมูล in 변형들.items():
        แฟ้ม = ไดเรกทอรี_ค่า / (ชื่อ + '.elf'); แฟ้ม.write_bytes(ข้อมูล)
        항목들.append(ชื่อ + '=' + str(แฟ้ม))
    subprocess.run([sys.executable, str(ตําแหน่ง / 'เครื่องมือ/ผูก_ปลายทาง.py'), '-o', str(ไดเรกทอรี_ค่า / 'apps.bin')] + 항목들, check=True)
    รหัสต้นฉบับ = ไดเรกทอรี_ค่า / 'apps.s'
    รหัสต้นฉบับ.write_text('.section .rodata.apps,"a"\n.globl app_blob_start,app_blob_end\napp_blob_start:\n.incbin "' +
                   str(ไดเรกทอรี_ค่า / 'apps.bin') + '"\napp_blob_end:\n.section .note.GNU-stack,"",@progbits\n')
    subprocess.run(['as', '--32', '-o', str(ไดเรกทอรี_ค่า / 'apps.o'), str(รหัสต้นฉบับ)], check=True)
    เคอร์เนล_ค่า = ไดเรกทอรี_ค่า / 'kernel.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-T', str(ตําแหน่ง / '부팅/ลิงก์_การนําทาง.ld'), '-o', str(เคอร์เนล_ค่า),
                    str(ตําแหน่ง / 'build/boot.o'), str(ตําแหน่ง / 'build/java.o'), str(ตําแหน่ง / 'build/user.o'), str(ไดเรกทอรี_ค่า / 'apps.o')], check=True)
    return เคอร์เนล_ค่า


def ดําเนินการ_คําสั่ง():
    ผลลัพธ์ = {}
    เซิร์ฟเวอร์_ค่า = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    เซิร์ฟเวอร์_ค่า.bind(('127.0.0.1', 0))
    เซิร์ฟเวอร์_ค่า.settimeout(0.1)
    แปลง_ค่า = เซิร์ฟเวอร์_ค่า.getsockname()[1]
    받은것 = []
    ออก_แอป = threading.Event()
    def 되보내기():
        while not ออก_แอป.is_set():
            try: ข้อมูล, ชั้น_ค่า = เซิร์ฟเวอร์_ค่า.recvfrom(4096)
            except socket.timeout: continue
            받은것.append(ข้อมูล)
            if ข้อมูล != b'drop-me': เซิร์ฟเวอร์_ค่า.sendto(ข้อมูล, ชั้น_ค่า)
    ผู้ปฏิบัติงาน_ค่า = threading.Thread(target=되보내기, daemon=True)
    ผู้ปฏิบัติงาน_ค่า.start()
    try:
        for 종류 in ('elf', 'iso'):
            เครื่อง = เครื่องเสมือน(ตําแหน่ง / ('build/kernel.elf' if 종류 == 'elf' else 'build/kernel.iso'), 종류)
            try:
                เครื่อง.คําสั่ง('apps', ['hello', 'udp', 'netcheck', 'stress'])
                เครื่อง.คําสั่ง('run hello first second', ['separate Java ELF', 'USER MODE ring 3', 'arg: first', 'arg: second', 'Exit: 0'])
                เครื่อง.คําสั่ง('run missing', ['Exit: -2'])
                เครื่อง.คําสั่ง('net', ['NET RTL8139'])
                เครื่อง.คําสั่ง('run netcheck', ['UDP API CHECK PASS', 'Exit: 0'])
                for เนื้อหา_ค่า in ('hello-network', 'odd', 'even', 'repeat-123'):
                    เครื่อง.คําสั่ง('run udp 10.0.2.2 {} {}'.format(แปลง_ค่า, เนื้อหา_ค่า), ['UDP SENT', 'UDP ECHO PASS', 'Exit: 0'])
                    assert เนื้อหา_ค่า.encode() in 받은것, 'โฮสต์ 서버에서 자료를 받지 못함'
                เครื่อง.คําสั่ง('run stress {}'.format(แปลง_ค่า), ['UDP STRESS PASS', 'Exit: 0'])
                เครื่อง.คําสั่ง('run udp 10.0.2.2 {} drop-me'.format(แปลง_ค่า), ['UDP SENT', 'UDP RECEIVE TIMEOUT/ERROR', 'Exit: 5'])
                เครื่อง.คําสั่ง('run hello recovered', ['arg: recovered', 'Exit: 0'])
                ผลลัพธ์[종류] = เครื่อง.บันทึก_สถิติ.decode('utf-8', 'replace')
                print('PASS: {} ผู้ใช้ ELF/ring 3/อาร์กิวเมนต์/UDP โฮสต์ 왕복/ค่าเวลา 초과/เชลล์ 복귀'.format(종류), flush=True)
            finally:
                try: เครื่อง.คําสั่ง('net', [])
                except Exception: pass
                (ตําแหน่ง / 'build/사용자통신-last.log').write_bytes(เครื่อง.บันทึก_สถิติ)
                เครื่อง.ปิด()
        เครื่อง = เครื่องเสมือน(ตําแหน่ง / 'build/kernel.elf', เครือข่าย_ค่า=False)
        try:
            เครื่อง.คําสั่ง('net', ['NET unavailable'])
            เครื่อง.คําสั่ง('run udp 10.0.2.2 9 hello', ['UDP OPEN FAILED', 'Exit: 3'])
            เครื่อง.คําสั่ง('run hello', ['USER MODE ring 3', 'Exit: 0'])
            ผลลัพธ์['no_nic'] = เครื่อง.บันทึก_สถิติ.decode()
        finally: เครื่อง.ปิด()
        with tempfile.TemporaryDirectory(prefix='jkoros-protection-test-') as 임시:
            เครื่อง = เครื่องเสมือน(보호커널(Path(임시)), เครือข่าย_ค่า=False)
            try:
                for ชื่อ, สถานะ_ค่า in [('badmem', 142), ('badport', 141), ('badptr', 0), ('badfile', 0), ('fault', 134),
                                   ('spin', 124), ('badelf', -8), ('badentry', -8), ('badtable', -8), ('badsize', -8)]:
                    เครื่อง.คําสั่ง('run ' + ชื่อ, ['Exit: ' + str(สถานะ_ค่า)])
                    เครื่อง.คําสั่ง('run hello', ['USER MODE ring 3', 'Exit: 0'])
                ผลลัพธ์['protection'] = เครื่อง.บันทึก_สถิติ.decode()
                print('PASS: ผู้ใช้ ความจํา_ข้อมูล/ฮาร์ดแวร์_แปลง 격리, 잘못된 ตัวชี้/ELF, CPU ข้อยกเว้น, 무한 สปรินต์_ค่า 제한', flush=True)
            finally:
                (ตําแหน่ง / 'build/การป้องกัน_การทดสอบ-last.log').write_bytes(เครื่อง.บันทึก_สถิติ)
                เครื่อง.ปิด()
    finally:
        ออก_แอป.set()
        ผู้ปฏิบัติงาน_ค่า.join(timeout=2)
        เซิร์ฟเวอร์_ค่า.close()
    ผลลัพธ์['host_udp_received'] = [{'length': len(ข้อมูล), 'sha256': hashlib.sha256(ข้อมูล).hexdigest()} for ข้อมูล in 받은것]
    (ตําแหน่ง / 'build/การทดสอบ_ผู้ใช้_เครือข่าย.json').write_text(json.dumps(ผลลัพธ์, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    ดําเนินการ_คําสั่ง()
