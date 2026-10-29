#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล QEMU/VNC에서 เทอร์มินัล 모서리 ลาก_ค่า·ตัวชี้·동적 อักขระ_ค่า 칸·แก้ไข_ค่า เนื้อหา_ค่า 보존를 검사한다."""
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


def 창크기시험(너비, 높이, เมตริก_พาธ):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); หมายเลขพอร์ต = 임시.getsockname()[1]
    ขนาด_ข้อความ = '{}x{}'.format(너비, 높이)
    กระบวนการ_ค่า = subprocess.Popen(['python3', str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_คําสั่ง.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(หมายเลขพอร์ต), '--resolution', ขนาด_ข้อความ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    ตัวเลือก_a916db4e = selectors.DefaultSelector(); ตัวเลือก_a916db4e.register(กระบวนการ_ค่า.stdout, selectors.EVENT_READ)
    บันทึก_สถิติ = bytearray(); ระยะไกล_ค่า = None; โอน_ค่า = None; ตัวชี้_ที่ซ่อน=[False]

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

    def เชลล์(ข้อความ): return 기다리기(b'\r\n__RESIZE_DONE__\r\n', ส่ง_SMS(ข้อความ+'; echo __RESIZE_DONE__\n'))

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
                if การเข้ารหัส_ค่า == -239:
                    assert 폭==0 and 길이==0, 'remote cursor must be hidden'
                    ตัวชี้_ที่ซ่อน[0]=True
                    continue
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
        ระยะไกล_ค่า.sendall(struct.pack('>BBHii', 2, 0, 2, 0, -239))
        เช็ค_พิกเซล((너비-1, 높이-1), (24, 32, 48))
        def 숨고르기(초=.25):
            끝=time.monotonic()+초
            while time.monotonic()<끝:
                for เหตุการณ์,_ in ตัวเลือก_a916db4e.select(.02):
                    ข้อมูล=เหตุการณ์.fileobj.read(65536)
                    if ข้อมูล:บันทึก_สถิติ.extend(ข้อมูล)
        หน้าต่าง=[12,48,568,360]
        def ยืนยัน_ขนาด():
            คอลัมน์_ค่า,แถว_ค่า=(หน้าต่าง[2]-24)//8,(หน้าต่าง[3]-56)//16
            ข้อความ=เชลล์('terminal size')
            assert 'TERMINAL SIZE {}x{}\r\n'.format(คอลัมน์_ค่า,แถว_ค่า) in ข้อความ,ข้อความ
            # ค่าจริง_ข้อมูล หน้าต่าง 테두리: 단지 ขนาด คิวรี_ค่า 값만 바뀐 것이 아닌지 확인한다.
            가리키기(너비-1,10,0);숨고르기()
            เช็ค_พิกเซล((หน้าต่าง[0],หน้าต่าง[1]),(32,80,144))
            รูปวาด_ค่า=เช็ค_พิกเซล((หน้าต่าง[0]+หน้าต่าง[2]-1,หน้าต่าง[1]+หน้าต่าง[3]-1),(39,49,64))
            return รูปวาด_ค่า
        def 모서리(방향):
            return (หน้าต่าง[0]+(3 if 방향 in (1,3) else หน้าต่าง[2]-4),หน้าต่าง[1]+(3 if 방향<=2 else หน้าต่าง[3]-4))
        def ปรับขนาด_ลาก(방향,차이,ปุ่ม=1):
            가,세=모서리(방향);가리키기(가,세,0);숨고르기()
            # 대각선 양방향 화살표의 흰 선과 반대 방향의 빈 점을 확인한다.
            흰점=(가-7 if 방향 in (1,4) else 가+7,세-7)
            เช็ค_พิกเซล(흰점,(255,255,255))
            가리키기(가,세,ปุ่ม)
            끝가=max(0,min(너비-1,가+차이[0]));สิ้นสุดการโทร_แนวตั้ง=max(0,min(높이-1,세+차이[1]))
            가리키기(끝가,สิ้นสุดการโทร_แนวตั้ง,ปุ่ม);가리키기(끝가,สิ้นสุดการโทร_แนวตั้ง,0);숨고르기()
            if ปุ่ม==1:
                왼,위,폭,길이=หน้าต่าง;สิทธิ์_ค่า_1766ca81,아래=왼+폭,위+길이
                if 방향 in (1,3):왼=max(0,min(สิทธิ์_ค่า_1766ca81-360,왼+끝가-가))
                else:สิทธิ์_ค่า_1766ca81=max(왼+360,min(너비,สิทธิ์_ค่า_1766ca81+끝가-가))
                if 방향<=2:위=max(34,min(아래-216,위+สิ้นสุดการโทร_แนวตั้ง-세))
                else:아래=max(위+216,min(높이,아래+สิ้นสุดการโทร_แนวตั้ง-세))
                หน้าต่าง[:]=[왼,위,สิทธิ์_ค่า_1766ca81-왼,아래-위]
        ยืนยัน_ขนาด();assert ตัวชี้_ที่ซ่อน[0]
        ปรับขนาด_ลาก(4,(-100,-60),4);ยืนยัน_ขนาด() # สิทธิ์ 버튼은 크기를 바꾸지 않는다.
        for 방향,차이 in ((4,(-120,-80)),(1,(24,16)),(2,(40,16)),(3,(24,32))):
            ปรับขนาด_ลาก(방향,차이);ยืนยัน_ขนาด()
        # 입력 중인 긴 한글 명령은 줄바꿈/가로 스크롤과 무관하게 그대로 실행된다.
        긴글='크기가 바뀌어도 입력한 한글 명령이 그대로 남습니다 '*3
        ส่ง_SMS("echo '"+긴글+"'");숨고르기()
        ปรับขนาด_ลาก(4,(-1000,-1000));assert หน้าต่าง[2:]==[360,216]
        ปรับขนาด_ลาก(4,(너비,높이))
        เรียกใช้งาน=ส่ง_SMS('\n');기다리기(('\r\n'+긴글+'\r\n').encode(),เรียกใช้งาน);ยืนยัน_ขนาด()
        # vi가 แก้ไข_ค่า 중에 화면 크기를 ลองอีกครั้ง_ค่า 읽고, 저장하지 않은 한글도 유지한다.
        เชลล์('ftpd start')
        โอน_ค่า=ftplib.FTP();โอน_ค่า.encoding='utf-8';โอน_ค่า.connect('127.0.0.1',หมายเลขพอร์ต,timeout=20);โอน_ค่า.login()
        기다리기(b'NORMAL',ส่ง_SMS('vi /크기자료.txt\n'))
        기다리기(b'INSERT',ส่ง_SMS('i미저장 한글 ข้อมูล\n'));숨고르기()
        ปรับขนาด_ลาก(4,(-너비,-높이))
        # ANSI แถว_ค่า 이동에 새 แถว_ค่า 수가 나타나는지, 한 글자도 입력하지 않고 확인한다.
        assert ('\x1b[{};1H'.format((หน้าต่าง[3]-56)//16)).encode() in บันทึก_สถิติ[-4096:]
        ส่ง_SMS('작은 창에서도 이어 เขียน\n');숨고르기()
        ปรับขนาด_ลาก(4,(너비,높이))
        ส่ง_SMS('큰 창에서도 이어 เขียน\n');숨고르기()
        คลิก_ปุ่ม(0xff1b);คลิก_ปุ่ม(0xff1b,False);숨고르기()
        기다리기(b'jkoros-native> ',ส่ง_SMS(':wq\n'))
        เนื้อหา_ค่า=bytearray();โอน_ค่า.retrbinary('RETR 크기자료.txt',เนื้อหา_ค่า.extend)
        assert เนื้อหา_ค่า=='미저장 한글 ข้อมูล\n작은 창에서도 이어 เขียน\n큰 창에서도 이어 เขียน\n'.encode(),เนื้อหา_ค่า
        ยืนยัน_ขนาด().save(str(เมตริก_พาธ/(ขนาด_ข้อความ+'-large.png')))
        # 두 번째 창은 ค่าเริ่มต้น ขนาด, ลองอีกครั้ง_ค่า 첫 창을 고르면 앞에서 바꾼 크기가 유지된다.
        เรียกใช้งาน=len(บันทึก_สถิติ);คลิก_ค่า(70,16);기다리기(b'TERMINAL FOCUS 2',เรียกใช้งาน)
        assert 'TERMINAL SIZE 68x19' in เชลล์('terminal size')
        เรียกใช้งาน=len(บันทึก_สถิติ);คลิก_ค่า(180,16);기다리기(b'TERMINAL FOCUS 1',เรียกใช้งาน);ยืนยัน_ขนาด()
        ปรับขนาด_ลาก(4,(-너비,-높이));ยืนยัน_ขนาด().save(str(เมตริก_พาธ/(ขนาด_ข้อความ+'-small.png')))
        # ขนาด เปลี่ยนแปลง_ค่า ย้อนกลับ_ค่า X 닫기도 새로운 สิทธิ์ 가장자리를 사용한다.
        เรียกใช้งาน=len(บันทึก_สถิติ);คลิก_ค่า(หน้าต่าง[0]+หน้าต่าง[2]-20,หน้าต่าง[1]+15);기다리기(b'TERMINAL FOCUS 2',เรียกใช้งาน)
        assert 'RESIZE CLOSED' in เชลล์('echo RESIZE CLOSED')
        print('PASS:',ขนาด_ข้อความ,'four corners, left drag, cursor, limits, live shell/vi, independent windows',flush=True)
    finally:
        if โอน_ค่า:โอน_ค่า.close()
        if ระยะไกล_ค่า:ระยะไกล_ค่า.close()
        if กระบวนการ_ค่า.poll() is None:
            กระบวนการ_ค่า.terminate()
            try:กระบวนการ_ค่า.wait(timeout=8)
            except subprocess.TimeoutExpired:กระบวนการ_ค่า.kill();กระบวนการ_ค่า.wait()
        ตัวเลือก_a916db4e.close();กระบวนการ_ค่า.stdout.close();(เมตริก_พาธ/(ขนาด_ข้อความ+'.log')).write_bytes(บันทึก_สถิติ)


def เรียกใช้งาน():
    เมตริก_พาธ=แสดง_ราก/'build/verification/resize';เมตริก_พาธ.mkdir(parents=True,exist_ok=True)
    บันทึก_สถิติ={'passed':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),'resolutions':[]}
    try:
        for 너비,높이 in ((640,480),(1920,1080)):
            창크기시험(너비,높이,เมตริก_พาธ);บันทึก_สถิติ['resolutions'].append([너비,높이])
        บันทึก_สถิติ.update(passed=True,checks=['native diagonal cursor pixels and hidden RFB cursor','all four corners use left drag; right drag ignored',
            'minimum/maximum geometry and current text rows/columns','long Korean shell input and unsaved vi text preserved',
            'vi redraws during idle resize','per-window geometry and resized X close'])
    finally:(เมตริก_พาธ/'report.json').write_text(json.dumps(บันทึก_สถิติ,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':เรียกใช้งาน()
