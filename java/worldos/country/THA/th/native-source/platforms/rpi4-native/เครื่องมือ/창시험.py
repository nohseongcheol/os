#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ดําเนินการ_คําสั่ง import แสดง_ราก,คําสั่ง

def เรียกใช้งาน():
    ปลายทาง_ค่า_ตําแหน่ง=แสดง_ราก/'build/verification/windows';ปลายทาง_ค่า_ตําแหน่ง.mkdir(parents=True,exist_ok=True)
    การตรวจสอบความถูกต้อง_รายงาน={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest()};บันทึก_สถิติ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ข้อมูล_ตําแหน่ง=subprocess.Popen(คําสั่ง()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ตัวเลือก_a916db4e=selectors.DefaultSelector();ตัวเลือก_a916db4e.register(ข้อมูล_ตําแหน่ง.stdout,selectors.EVENT_READ)
        def จุดจับ_กิจกรรม(초단위=.1):
            for 누름값,_ in ตัวเลือก_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:บันทึก_สถิติ.extend(둘째값)
            assert b'PANIC:' not in บันทึก_สถิติ and b'HALTED' not in บันทึก_สถิติ,บันทึก_สถิติ[-2048:]
        def 기다리기(มาร์กเกอร์,ปัจจุบัน_ตําแหน่ง,초단위=50):
            สิ้นสุดการโทร_ออฟเซต=time.monotonic()+초단위
            while มาร์กเกอร์ not in บันทึก_สถิติ[ปัจจุบัน_ตําแหน่ง:]:
                if time.monotonic()>สิ้นสุดการโทร_ออฟเซต or ข้อมูล_ตําแหน่ง.poll() is not None:raise AssertionError(บันทึก_สถิติ[ปัจจุบัน_ตําแหน่ง:].decode('utf-8','replace'))
                จุดจับ_กิจกรรม()
            return bytes(บันทึก_สถิติ[ปัจจุบัน_ตําแหน่ง:])
        def ส่ง(둘째값,มาร์กเกอร์=b'jkoros-native> '):
            ปัจจุบัน_ตําแหน่ง=len(บันทึก_สถิติ);ข้อมูล_ตําแหน่ง.stdin.write(둘째값);ข้อมูล_ตําแหน่ง.stdin.flush();return 기다리기(มาร์กเกอร์,ปัจจุบัน_ตําแหน่ง)
        def เชลล์(สตริง_ข้อมูล):return ส่ง((สตริง_ข้อมูล+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ทางลัด_ค่า(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def คลิก_ปุ่ม(พิกัดแกน_x,세로좌표):return bytes([30,1,1,พิกัดแกน_x&255,พิกัดแกน_x>>8,세로좌표&255,세로좌표>>8,30,1,0,พิกัดแกน_x&255,พิกัดแกน_x>>8,세로좌표&255,세로좌표>>8])
        def คําสั่ง_โหมด():
            ข้อมูล_ตําแหน่ง.stdin.write(b'\x1b');ข้อมูล_ตําแหน่ง.stdin.flush();สิ้นสุดการโทร_ออฟเซต=time.monotonic()+.2
            while time.monotonic()<สิ้นสุดการโทร_ออฟเซต:จุดจับ_กิจกรรม(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            เชลล์('terminal');จุดจับ_กิจกรรม(.3)
            เชลล์('mkdir first; cd first; export NAME=one')
            ส่ง('vi 첫째.py\n'.encode(),b'NORMAL')
            ส่ง('i값 = 21\nprint(ค่า * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            สิ้นสุดการโทร_ออฟเซต=time.monotonic()+3
            while time.monotonic()<สิ้นสุดการโทร_ออฟเซต:จุดจับ_กิจกรรม(.1)
            ส่ง(ทางลัด_ค่า(1),b'TERMINAL FOCUS 2');จุดจับ_กิจกรรม(.2)
            assert b'/\r\n' in เชลล์('pwd')
            เชลล์('export NAME=two')
            ส่ง('vi 둘째.txt\n'.encode(),b'NORMAL')
            ส่ง('i두 번째 หน้าต่าง\n'.encode(),b'INSERT')
            ส่ง(คลิก_ปุ่ม(180,12),b'TERMINAL FOCUS 1');จุดจับ_กิจกรรม(.2)
            คําสั่ง_โหมด();ส่ง(b':wq\r')
            assert b'one:/first' in เชลล์('echo "$NAME:$PWD"')
            assert 'ค่า = 21\r\nprint(ค่า * 2)'.encode() in เชลล์('cat 첫째.py')
            ผลลัพธ์=เชลล์('python 첫째.py');assert b'42\r\n' in ผลลัพธ์,ผลลัพธ์
            # Close the first shell with its actual title-bar X; second editor resumes.
            ส่ง(คลิก_ปุ่ม(560,63),b'TERMINAL FOCUS 2');จุดจับ_กิจกรรม(.2)
            คําสั่ง_โหมด();ส่ง(b':wq\r')
            assert b'two:/' in เชลล์('echo "$NAME:$PWD"')
            assert '두 번째 หน้าต่าง'.encode() in เชลล์('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ส่ง('vi 둘째.txt\n'.encode(),b'NORMAL');ส่ง(b'xu',b'NORMAL')
            ส่ง(b'iX',b'INSERT');คําสั่ง_โหมด();ส่ง(b':q\r',b'Unsaved')
            ส่ง(b':q!\r');assert '두 번째 หน้าต่าง'.encode() in เชลล์('cat 둘째.txt')
            ส่ง(ทางลัด_ค่า(1),b'TERMINAL FOCUS 1');จุดจับ_กิจกรรม(.2)
            ส่ง(ทางลัด_ค่า(1),b'TERMINAL FOCUS 3');จุดจับ_กิจกรรม(.2)
            ส่ง(ทางลัด_ค่า(1),b'TERMINAL FOCUS 4');จุดจับ_กิจกรรม(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ข้อมูล_ตําแหน่ง.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ข้อมูล_ตําแหน่ง.stdin.flush()
            เชลล์('echo DRAGGED_OK')
            ส่ง('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ส่ง('i저장하지 않은 ข้อมูล'.encode(),b'INSERT')
            ส่ง(คลิก_ปุ่ม(578,97),b'TERMINAL FOCUS 3');จุดจับ_กิจกรรม(.2)
            assert '버릴문서.txt'.encode() not in เชลล์('ls')
            ส่ง(ทางลัด_ค่า(1),b'TERMINAL FOCUS 4');จุดจับ_กิจกรรม(.2)
            เชลล์('echo REUSED_WINDOW_OK')
            เสร็จสมบูรณ์_จํานวน=บันทึก_สถิติ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',เสร็จสมบูรณ์_จํานวน)
            # UART completion precedes the next QEMU display refresh.
            สิ้นสุดการโทร_ออฟเซต=time.monotonic()+.3
            while time.monotonic()<สิ้นสุดการโทร_ออฟเซต:จุดจับ_กิจกรรม(.05)
            with socket.socket(socket.AF_UNIX) as รหัสอักขระ:
                รหัสอักขระ.settimeout(10);รหัสอักขระ.connect(str(모의제어접속))
                with รหัสอักขระ.makefile('rwb') as แฟ้ม_รายการ_3d0c1245:
                    json.loads(แฟ้ม_รายการ_3d0c1245.readline())
                    for คําขอ_ค่า in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ปลายทาง_ค่า_ตําแหน่ง/'four-terminals.png'),'format':'png'}}):
                        แฟ้ม_รายการ_3d0c1245.write((json.dumps(คําขอ_ค่า)+'\n').encode());แฟ้ม_รายการ_3d0c1245.flush()
                        while True:
                            반환값=json.loads(แฟ้ม_รายการ_3d0c1245.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ปลายทาง_ค่า_ตําแหน่ง/'four-terminals.png')).convert('RGB')
            for คู่พิกัด,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(คู่พิกัด)==색상,(คู่พิกัด,화소들.getpixel(คู่พิกัด))
            เชลล์('echo FOUR_WINDOWS_OK')
            การตรวจสอบความถูกต้อง_รายงาน.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ข้อมูล_ตําแหน่ง.poll() is None:ข้อมูล_ตําแหน่ง.terminate()
            try:ข้อมูล_ตําแหน่ง.wait(timeout=5)
            except subprocess.TimeoutExpired:ข้อมูล_ตําแหน่ง.kill();ข้อมูล_ตําแหน่ง.wait()
            ตัวเลือก_a916db4e.close();ข้อมูล_ตําแหน่ง.stdin.close();ข้อมูล_ตําแหน่ง.stdout.close();(ปลายทาง_ค่า_ตําแหน่ง/'serial.log').write_bytes(บันทึก_สถิติ);(ปลายทาง_ค่า_ตําแหน่ง/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':เรียกใช้งาน()
