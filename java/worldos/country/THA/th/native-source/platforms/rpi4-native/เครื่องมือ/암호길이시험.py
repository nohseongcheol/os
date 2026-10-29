#!/usr/bin/env python3
"""개인 เพื่อน_e05f319b 설정을 보존하며 짧은/긴/빈 암호로 별도 커널의 SSH·VNC를 시험한다."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from ระยะไกล_การตั้งค่า import จัดเตรียม
from COSL배포 import ปลายทาง_ชื่อ, ไลบรารี

แสดง_ราก = Path(__file__).resolve().parents[1]


def เรียกใช้งาน():
    ข้อความออก = แสดง_ราก / 'build/verification/password-length'
    ข้อความออก.mkdir(parents=True, exist_ok=True)
    ส่วนตัว_การตั้งค่า = แสดง_ราก / 'build/remote/access.json'
    원래설정 = ส่วนตัว_การตั้งค่า.read_bytes()
    รายงาน_ค่า = {'passed': False, 'checks': [], 'physical_board_tested': False}
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-password-') as 임시:
            การทดสอบ_พื้นที่ทํางาน = Path(임시)
            การตั้งค่า_พาธ = การทดสอบ_พื้นที่ทํางาน / 'build/remote'
            การตั้งค่า_พาธ.mkdir(parents=True)
            การตั้งค่า_แฟ้ม = การตั้งค่า_พาธ / 'access.json'
            def 설정쓰기(ข้อมูล):
                การตั้งค่า_แฟ้ม.write_text(json.dumps(ข้อมูล, ensure_ascii=False) + '\n')
                การตั้งค่า_แฟ้ม.chmod(0o600)
            def ยืนยัน_การตั้งค่า(เชลล์, 화면):
                설정쓰기({'user': 'user', 'ssh_password': เชลล์, 'vnc_password': 화면})
                원본 = การตั้งค่า_แฟ้ม.read_bytes()
                จัดเตรียม(การทดสอบ_พื้นที่ทํางาน)
                assert การตั้งค่า_แฟ้ม.read_bytes() == 원본, 'Settings were rewritten'
                머리 = (การตั้งค่า_พาธ / 'โปรไฟล์.h').read_text()
                일치 = re.search(r'화면암호\[\] = \{([^}]+)\}', 머리)
                assert 일치 and len(일치.group(1).split(',')) == 8, 'Native VNC key must be eight bytes'
                assert (การตั้งค่า_พาธ / 'โปรไฟล์.h').stat().st_mode & 0o777 == 0o600
            for เชลล์, 화면 in [('', ''), ('a', '1'), ('1234', '1234'), ('한글', '1234567'),
                              ('a' * 15, '12345678'), ('a' * 16, '123456789'), ('a' * 256, 'v' * 1024)]:
                ยืนยัน_การตั้งค่า(เชลล์, 화면)
            รายงาน_ค่า['checks'].append('Configuration accepts empty, one-character, short, long and UTF-8 SSH passwords; VNC key has fixed storage')
            for เปลี่ยนแปลง_ค่า, รายการ_ค่า in [({'user': 'other'}, 'user'), ({'ssh_password': 1234}, 'ssh_password'),
                               ({'ssh_password': '한' * 86}, 'ssh_password'),
                               ({'vnc_password': '한글'}, 'vnc_password'), ({'vnc_password': None}, 'vnc_password')]:
                ข้อมูล = {'user': 'user', 'ssh_password': '1234', 'vnc_password': '1234'}
                ข้อมูล.update(เปลี่ยนแปลง_ค่า)
                설정쓰기(ข้อมูล)
                try:
                    จัดเตรียม(การทดสอบ_พื้นที่ทํางาน)
                except SystemExit as ข้อผิดพลาด:
                    assert รายการ_ค่า in str(ข้อผิดพลาด), 'Error did not identify its field'
                else:
                    raise AssertionError('Invalid configuration accepted: ' + รายการ_ค่า)
            รายงาน_ค่า['checks'].append('Remaining user/type/encoding/server-size errors identify the actual field')
            ตั้งค่า = json.loads((แสดง_ราก / 'build/remote/libassh-build.json').read_text())['flags']
            คอมไพเลอร์_เครื่องมือ = os.environ.get('ARM64_CC', 'clang')
            หัวต่อ = os.environ.get('ARM64_LD', 'aarch64-linux-gnu-ld')
            เก็บถาวร_เครื่องมือ = os.environ.get('ARM64_AR', 'aarch64-linux-gnu-ar')
            def ดําเนินการ_คําสั่ง(อาร์กิวเมนต์, บันทึก_สถิติ):
                subprocess.run(list(map(str, อาร์กิวเมนต์)), cwd=str(แสดง_ราก), stdout=บันทึก_สถิติ,
                               stderr=subprocess.STDOUT, check=True, timeout=240)
            for ชื่อ, เชลล์, 화면 in [('short', '1234', '1234'), ('long-vnc', 'x', 'abcdefgh-extra'), ('empty', '', '')]:
                print('Password authentication case: ' + ชื่อ, flush=True)
                ยืนยัน_การตั้งค่า(เชลล์, 화면)
                ผลลัพธ์ = ข้อความออก / ชื่อ
                ผลลัพธ์.mkdir(exist_ok=True)
                with (ผลลัพธ์ / 'build.log').open('wb') as บันทึก_สถิติ:
                    목적들 = []
                    for 원본 in sorted((แสดง_ราก / 'ระยะไกล_ค่า').glob('*.c')):
                        ปลายทาง_ค่า_a0fbc067 = การทดสอบ_พื้นที่ทํางาน / (원본.stem + '.o')
                        ดําเนินการ_คําสั่ง([คอมไพเลอร์_เครื่องมือ] + ตั้งค่า + ['-std=c11', '-DNDEBUG', '-ffunction-sections', '-fdata-sections',
                             '-I', การตั้งค่า_พาธ, '-I', แสดง_ราก / 'ระยะไกล_ค่า', '-I', แสดง_ราก / 'vendor/libassh/src',
                             '-I', แสดง_ราก / 'vendor/bearssl/inc', '-I', แสดง_ราก / 'vendor/bearssl/src',
                             '-isystem', '/usr/include/newlib', '-c', 원본, '-o', ปลายทาง_ค่า_a0fbc067], บันทึก_สถิติ)
                        목적들.append(ปลายทาง_ค่า_a0fbc067)
                    ระยะไกล_รวม = การทดสอบ_พื้นที่ทํางาน / 'libremote.a'
                    ดําเนินการ_คําสั่ง([เก็บถาวร_เครื่องมือ, 'rcs', ระยะไกล_รวม] + 목적들, บันทึก_สถิติ)
                    ดําเนินการ_คําสั่ง([หัวต่อ, '--gc-sections', '-T', แสดง_ราก / '부팅/ลิงก์_การนําทาง.ld', '-o', การทดสอบ_พื้นที่ทํางาน / 'kernel.elf'] +
                         [แสดง_ราก / 'build' / (ชื่อ + '.o') for ชื่อ in ปลายทาง_ชื่อ] + ['--start-group'] +
                         [ระยะไกล_รวม if เส้นทาง == 'remote/libremote.a' else แสดง_ราก / 'build' / เส้นทาง for เส้นทาง in ไลบรารี] + ['--end-group'], บันทึก_สถิติ)
                    ดําเนินการ_คําสั่ง([os.environ.get('ARM64_OBJCOPY', 'aarch64-linux-gnu-objcopy'), '-O', 'binary',
                         การทดสอบ_พื้นที่ทํางาน / 'kernel.elf', การทดสอบ_พื้นที่ทํางาน / 'kernel8.img'], บันทึก_สถิติ)
                with (ผลลัพธ์ / 'remote-test.log').open('wb') as บันทึก_สถิติ:
                    ดําเนินการ_คําสั่ง(['python3', แสดง_ราก / 'เครื่องมือ/การเชื่อมต่อระยะไกล_การทดสอบ.py', '--kernel', การทดสอบ_พื้นที่ทํางาน / 'kernel8.img',
                         '--access', การตั้งค่า_แฟ้ม, '--output', ผลลัพธ์], บันทึก_สถิติ)
                ตรวจสอบความถูกต้อง = json.loads((ผลลัพธ์ / 'report.json').read_text())
                assert ตรวจสอบความถูกต้อง['passed']
                รายงาน_ค่า['checks'].append(ชื่อ + ': actual OpenSSH authentication/exec and VNC authentication/framebuffer/input passed; wrong passwords rejected')
        รายงาน_ค่า['passed'] = True
    finally:
        รายงาน_ค่า['personal_settings_unchanged'] = ส่วนตัว_การตั้งค่า.read_bytes() == 원래설정
        if not รายงาน_ค่า['personal_settings_unchanged']:
            รายงาน_ค่า['passed'] = False
        รายงาน_ค่า['kernel_sha256'] = hashlib.sha256((แสดง_ราก / 'build/kernel8.img').read_bytes()).hexdigest()
        (ข้อความออก / 'report.json').write_text(json.dumps(รายงาน_ค่า, ensure_ascii=False, indent=2) + '\n')
    assert รายงาน_ค่า['personal_settings_unchanged'], 'Personal settings unexpectedly changed'
    print(json.dumps(รายงาน_ค่า, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    เรียกใช้งาน()
