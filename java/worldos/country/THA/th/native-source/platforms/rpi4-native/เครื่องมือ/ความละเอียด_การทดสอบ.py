#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล QEMU/VNC에서 화면 ขนาด·경계·หน้าต่าง ขยับ_ค่า·Swing·언어별 그리기를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from เดสก์ท็อป_ดู import 정확한값
from ดําเนินการ_คําสั่ง import แสดง_ราก


def ความละเอียด_การทดสอบ(너비, 높이, เมตริก_พาธ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); หมายเลขพอร์ต = 임시.getsockname()[1]
    ขนาด_ข้อความ = '{}x{}'.format(너비, 높이)
    กระบวนการ_ค่า = subprocess.Popen(['python3', str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_คําสั่ง.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(หมายเลขพอร์ต), '--resolution', ขนาด_ข้อความ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ตัวเลือก_a916db4e = selectors.DefaultSelector(); ตัวเลือก_a916db4e.register(กระบวนการ_ค่า.stdout, selectors.EVENT_READ)
    บันทึก_สถิติ = bytearray(); ระยะไกล_ค่า = None; โอน_ค่า = None

    def 기다리기(แสดง_ค่า, เรียกใช้งาน=0):
        วันครบกําหนด_ค่า = time.monotonic() + 60
        while แสดง_ค่า not in บันทึก_สถิติ[เรียกใช้งาน:]:
            if time.monotonic() > วันครบกําหนด_ค่า or กระบวนการ_ค่า.poll() is not None or b'HALTED' in บันทึก_สถิติ or b'PANIC:' in บันทึก_สถิติ:
                raise AssertionError(บันทึก_สถิติ[เรียกใช้งาน:].decode('utf-8', 'replace'))
            for เหตุการณ์, _ in ตัวเลือก_a916db4e.select(.1):
                ข้อมูล = เหตุการณ์.fileobj.read(65536)
                if ข้อมูล: บันทึก_สถิติ.extend(ข้อมูล)
        return บันทึก_สถิติ[เรียกใช้งาน:].decode('utf-8', 'replace')

    def คลิก_ปุ่ม(สัญลักษณ์, 눌림=True): ระยะไกล_ค่า.sendall(struct.pack('>BBHI', 4, int(눌림), 0, สัญลักษณ์))

    def ส่ง_SMS(ข้อความ):
        เรียกใช้งาน = len(บันทึก_สถิติ)
        for อักขระ_ค่า in ข้อความ:
            สัญลักษณ์ = 0xff0d if อักขระ_ค่า == '\n' else ord(อักขระ_ค่า) if ord(อักขระ_ค่า) < 256 else 0x1000000 | ord(อักขระ_ค่า)
            คลิก_ปุ่ม(สัญลักษณ์); คลิก_ปุ่ม(สัญลักษณ์, False)
        return เรียกใช้งาน

    def เชลล์(ข้อความ): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', ส่ง_SMS(ข้อความ+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, แนวตั้ง_ตําแหน่ง, 눌림): ระยะไกล_ค่า.sendall(struct.pack('>BBHH', 5, 눌림, 가로, แนวตั้ง_ตําแหน่ง))

    def คลิก_ค่า(가로, แนวตั้ง_ตําแหน่ง): 가리키기(가로, แนวตั้ง_ตําแหน่ง, 1); 가리키기(가로, แนวตั้ง_ตําแหน่ง, 0)

    def บิตแมป_รูป():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 ค่าจริง_ข้อมูล 너비를 쓴다.
        ระยะไกล_ค่า.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, 높이))
        รูปวาด_ค่า = Image.new('RGB', (너비, 높이)); ประเภท_ค่า_9285603e = 0
        while True:
            종류 = 정확한값(ระยะไกล_ค่า, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                길이 = struct.unpack('>I', 정확한값(ระยะไกล_ค่า, 7)[3:])[0]; 정확한값(ระยะไกล_ค่า, 길이); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(ระยะไกล_ค่า, 3)[1:])[0]
            for _ in range(개수):
                가로, แนวตั้ง_ตําแหน่ง, 폭, 길이, การเข้ารหัส_ค่า = struct.unpack('>HHHHi', 정확한값(ระยะไกล_ค่า, 12))
                assert การเข้ารหัส_ค่า == 0 and 가로+폭 <= 너비 and แนวตั้ง_ตําแหน่ง+길이 <= 높이
                รูปวาด_ค่า.paste(Image.frombytes('RGB', (폭, 길이), 정확한값(ระยะไกล_ค่า, 폭*길이*4), 'raw', 'BGRX'), (가로, แนวตั้ง_ตําแหน่ง))
                ประเภท_ค่า_9285603e += 폭*길이
            if ประเภท_ค่า_9285603e:
                assert ประเภท_ค่า_9285603e == 너비*높이, ประเภท_ค่า_9285603e
                return รูปวาด_ค่า

    def เช็ค_พิกเซล(좌표, 색):
        วันครบกําหนด_ค่า = time.monotonic()+10
        while True:
            รูปวาด_ค่า = บิตแมป_รูป()
            if รูปวาด_ค่า.getpixel(좌표) == 색: return รูปวาด_ค่า
            if time.monotonic() > วันครบกําหนด_ค่า: raise AssertionError((좌표, รูปวาด_ค่า.getpixel(좌표), 색))

    def อัปโหลด_ไฟล์(ชื่อ, ข้อมูล): โอน_ค่า.storbinary('STOR '+ชื่อ, io.BytesIO(ข้อมูล))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+ขนาด_ข้อความ+' RGB32').encode() in บันทึก_สถิติ
        print('BOOT:', ขนาด_ข้อความ, flush=True)
        ระยะไกล_หมายเลข = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', บันทึก_สถิติ).group(1))
        ระยะไกล_ค่า = socket.create_connection(('127.0.0.1', ระยะไกล_หมายเลข), timeout=20)
        assert 정확한값(ระยะไกล_ค่า, 12) == b'RFB 003.008\n'; ระยะไกล_ค่า.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ระยะไกล_ค่า, 정확한값(ระยะไกล_ค่า, 1)[0]); ระยะไกล_ค่า.sendall(b'\x01')
        assert 정확한값(ระยะไกล_ค่า, 4) == b'\0'*4; ระยะไกล_ค่า.sendall(b'\x01')
        สภาวะเริ่มต้น = 정확한값(ระยะไกล_ค่า, 24); assert struct.unpack('>HH', สภาวะเริ่มต้น[:4]) == (너비, 높이)
        정확한값(ระยะไกล_ค่า, struct.unpack('>I', สภาวะเริ่มต้น[20:])[0])
        ระยะไกล_ค่า.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        ระยะไกล_ค่า.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        เช็ค_พิกเซล((너비-1, 높이-1), (24, 32, 48))
        # 화면 สิทธิ์ 아래까지 이동한다. 이전 640×480 경계 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, 높이-360+12, 1); 가리키기(너비-568+28, 높이-360+12, 0)
        เช็ค_พิกเซล((너비-568, 높이-360), (32, 80, 144))
        เรียกใช้งาน = len(บันทึก_สถิติ); คลิก_ค่า(너비-20, 높이-345); 기다리기(b'TERMINAL FOCUS 1', เรียกใช้งาน)
        เช็ค_พิกเซล((너비-568, 높이-360), (24, 32, 48))
        เรียกใช้งาน = len(บันทึก_สถิติ); คลิก_ค่า(80, 16); 기다리기(b'TERMINAL FOCUS 1', เรียกใช้งาน)
        เชลล์('ftpd start')
        โอน_ค่า = ftplib.FTP(); โอน_ค่า.encoding = 'utf-8'; โอน_ค่า.connect('127.0.0.1', หมายเลขพอร์ต, timeout=20); โอน_ค่า.login()
        # C 경계 검사는 32비트 unsigned 음수 แปลง_ค่า_4633b7f3·คลิป 밖·빈 사각형을 포함한다.
        รหัสต้นฉบับ = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), 높이=화면높이();
    if(너비!=WIDTH || 높이!=HEIGHT) return 1;
    if(วาด_สี่เหลี่ยมผืนผ้า(너비,높이,0,0,0)) return 2;
    if(วาด_สี่เหลี่ยมผืนผ้า(너비,높이-1,1,1,0)!=-22) return 3;
    if(วาด_สี่เหลี่ยมผืนผ้า(너비-1,높이,1,1,0)!=-22) return 4;
    if(วาด_สี่เหลี่ยมผืนผ้า(-1,0,1,1,0)!=-22) return 5;
    if(วาด_สี่เหลี่ยมผืนผ้า(0,0,-1,1,0)!=-22) return 6;
    if(วาด_สี่เหลี่ยมผืนผ้า(너비-1,높이-1,1,1,0x332211)) return 7;
    파일자료쓰기(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        อัปโหลด_ไฟล์('화면시험.c', รหัสต้นฉบับ.encode())
        assert 'exit 0' in เชลล์('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', ส่ง_SMS('run /화면시험\n'))
        เช็ค_พิกเซล((너비-1, 높이-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', ส่ง_SMS('q'))
        รหัสต้นฉบับ = '''from ไทย import 화면크기, วาด_สี่เหลี่ยมผืนผ้า, 그림기다리기, ข้อความออก, ระบบ_ข้อผิดพลาด
너비, 높이 = 화면크기()
assert (너비, 높이) == (WIDTH, HEIGHT)
try:
    วาด_สี่เหลี่ยมผืนผ้า(너비, 높이-1, 1, 1, 0)
    raise AssertionError("boundary")
except ระบบ_ข้อผิดพลาด as ข้อผิดพลาด:
    assert ข้อผิดพลาด.ดัชนี == 22
วาด_สี่เหลี่ยมผืนผ้า(너비-1, 높이-1, 1, 1, 0x665544)
ข้อความออก("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        อัปโหลด_ไฟล์('화면시험.py', รหัสต้นฉบับ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', ส่ง_SMS('python /화면시험.py\n'))
        เช็ค_พิกเซล((너비-1, 높이-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', ส่ง_SMS('q'))
        รหัสต้นฉบับ = '''import ไทย.เอง.*;
public class ความละเอียด_การทดสอบ {
    public static void main(String[] อาร์กิวเมนต์) {
        int 너비=화면.너비(), 높이=화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) throw new สถานะ_ข้อยกเว้น("ขนาด");
        try { 화면.สี่เหลี่ยมผืนผ้า(너비,높이-1,1,1,0); throw new สถานะ_ข้อยกเว้น("คลิป"); }
        catch (ไม่ถูกต้อง_อาร์กิวเมนต์_ข้อยกเว้น ข้อผิดพลาด) { }
        화면.ลบ_รายการ(0x302018);
        화면.สี่เหลี่ยมผืนผ้า(너비-1,높이-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        # ข้อยกเว้น 처리는 โฮสต์ javac 결과를 เอง JVM에 올려 검사한다.
        경계원문 = เมตริก_พาธ/'해상도경계시험.java'
        경계원문.write_text(รหัสต้นฉบับ.replace('class ความละเอียด_การทดสอบ', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(แสดง_ราก/'dist/jkoros-native-korean.jar'), '-d', str(เมตริก_พาธ), str(경계원문)])
        อัปโหลด_ไฟล์('해상도경계시험.class', (เมตริก_พาธ/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', ส่ง_SMS('java 해상도경계시험\n'))
        เช็ค_พิกเซล((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ส่ง_SMS('q'))
        # 게스트 javac의 สนับสนุน_ค่า 문법으로 ขนาด คิวรี_ค่า·ลบ_รายการ·다섯 อาร์กิวเมนต์ 그리기를 컴파일한다.
        รหัสต้นฉบับ = '''public class ความละเอียด_การทดสอบ {
    public static void main(String[] อาร์กิวเมนต์) {
        int 너비=ไทย.เอง.화면.너비();
        int 높이=ไทย.เอง.화면.높이();
        if (너비!=WIDTH || 높이!=HEIGHT) return;
        ไทย.เอง.화면.ลบ_รายการ(3153944);
        ไทย.เอง.화면.สี่เหลี่ยมผืนผ้า(너비-1,높이-1,1,1,10061943);
        ไทย.เอง.ข้อความออก.줄쓰기("JAVA RESOLUTION PASS");
        ไทย.เอง.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(높이))
        อัปโหลด_ไฟล์('ความละเอียด_การทดสอบ.java', รหัสต้นฉบับ.encode())
        ผลลัพธ์ = เชลล์('javac ความละเอียด_การทดสอบ.java'); assert 'exit 0' in ผลลัพธ์, ผลลัพธ์
        기다리기(b'JAVA RESOLUTION PASS', ส่ง_SMS('java ความละเอียด_การทดสอบ\n'))
        เช็ค_พิกเซล((너비-1, 높이-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', ส่ง_SMS('q'))
        อัปโหลด_ไฟล์('สวิง_การทดสอบ.class', (เมตริก_พาธ/'สวิง_การทดสอบ.class').read_bytes())
        기다리기(b'SWING READY', ส่ง_SMS('java สวิง_การทดสอบ\n'))
        가로, แนวตั้ง_ตําแหน่ง = (너비-400)//2, (높이-280)//2
        รูปวาด_ค่า = เช็ค_พิกเซล((가로, แนวตั้ง_ตําแหน่ง), (32, 80, 144))
        รูปวาด_ค่า.save(str(เมตริก_พาธ/(ขนาด_ข้อความ+'.png')))
        เรียกใช้งาน = len(บันทึก_สถิติ); คลิก_ค่า(가로+80, แนวตั้ง_ตําแหน่ง+155)
        기다리기('SWING CLICK ชื่อ'.encode(), เรียกใช้งาน)
        เรียกใช้งาน = len(บันทึก_สถิติ); คลิก_ค่า(가로+385, แนวตั้ง_ตําแหน่ง+15); 기다리기(b'jkoros-native> ', เรียกใช้งาน)
        assert 'AFTER_RESOLUTION' in เชลล์('echo AFTER_RESOLUTION')
        print('PASS:', ขนาด_ข้อความ, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if โอน_ค่า: โอน_ค่า.close()
        if ระยะไกล_ค่า: ระยะไกล_ค่า.close()
        if กระบวนการ_ค่า.poll() is None:
            กระบวนการ_ค่า.terminate()
            try: กระบวนการ_ค่า.wait(timeout=8)
            except subprocess.TimeoutExpired: กระบวนการ_ค่า.kill(); กระบวนการ_ค่า.wait()
        ตัวเลือก_a916db4e.close(); กระบวนการ_ค่า.stdout.close()
        (เมตริก_พาธ/(ขนาด_ข้อความ+'.log')).write_bytes(บันทึก_สถิติ)


def เรียกใช้งาน():
    เมตริก_พาธ = แสดง_ราก/'build/verification/resolution'; เมตริก_พาธ.mkdir(parents=True, exist_ok=True)
    บันทึก_สถิติ = {'passed': False, 'kernel_sha256': hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for ไม่ถูกต้อง_ค่า in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            ผลลัพธ์ = subprocess.run(['python3', str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_คําสั่ง.py'), '--resolution', ไม่ถูกต้อง_ค่า], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert ผลลัพธ์.returncode == 2 and b'--resolution' in ผลลัพธ์.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(เมตริก_พาธ), str(แสดง_ราก/'시험/자바/สวิง_การทดสอบ.java')])
        for 너비, 높이 in ((1920,1080), (1280,720), (640,480)):
            ความละเอียด_การทดสอบ(너비, 높이, เมตริก_พาธ); บันทึก_สถิติ['resolutions'].append([너비, 높이])
        บันทึก_สถิติ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (เมตริก_พาธ/'report.json').write_text(json.dumps(บันทึก_สถิติ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': เรียกใช้งาน()
