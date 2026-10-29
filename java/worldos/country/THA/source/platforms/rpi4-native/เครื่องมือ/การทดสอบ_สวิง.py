#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ดําเนินการ_คําสั่ง import แสดง_ราก,คําสั่ง

def เรียกใช้งาน():
    ปลายทาง_ค่า_ตําแหน่ง=แสดง_ราก/'build/verification/swing';ปลายทาง_ค่า_ตําแหน่ง.mkdir(parents=True,exist_ok=True)
    คลาส_พาธ=แสดง_ราก/'build/verification/new-java';คลาส_พาธ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(แสดง_ราก/'dist/jkoros-native-korean.jar'),'-d',str(คลาส_พาธ),str(แสดง_ราก/'시험/자바/สวิง_การทดสอบ.java'),str(แสดง_ราก/'시험/자바/한글창시험.java')])
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
            ข้อมูล=(แสดง_ราก/'build/verification/new-java/สวิง_การทดสอบ.class').read_bytes()
            ส่ง('load สวิง_การทดสอบ.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ข้อมูล),64):ส่ง(ข้อมูล[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ส่ง(b'.\n')
            ส่ง('java สวิง_การทดสอบ\n'.encode(),b'SWING READY')
            สิ้นสุดการโทร_ออฟเซต=time.monotonic()+3
            while time.monotonic()<สิ้นสุดการโทร_ออฟเซต:จุดจับ_กิจกรรม(.1)
            # JFrame centered at (120,100), content at y=130.
            ส่ง(คลิก_ปุ่ม(200,210),b'',)  # focus JTextField
            ข้อมูล_ตําแหน่ง.stdin.write('누리'.encode());ข้อมูล_ตําแหน่ง.stdin.flush()
            สิ้นสุดการโทร_ออฟเซต=time.monotonic()+.3
            while time.monotonic()<สิ้นสุดการโทร_ออฟเซต:จุดจับ_กิจกรรม(.05)
            ผลลัพธ์=ส่ง(คลิก_ปุ่ม(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(บันทึก_สถิติ)-len(ผลลัพธ์))
            ส่ง(ทางลัด_ค่า(1),b'TERMINAL FOCUS 2')
            ผลลัพธ์=เชลล์('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ผลลัพธ์
            ส่ง(คลิก_ปุ่ม(180,12),b'TERMINAL FOCUS 1')
            สิ้นสุดการโทร_ออฟเซต=time.monotonic()+.3
            while time.monotonic()<สิ้นสุดการโทร_ออฟเซต:จุดจับ_กิจกรรม(.05)
            with socket.socket(socket.AF_UNIX) as รหัสอักขระ:
                รหัสอักขระ.settimeout(10);รหัสอักขระ.connect(str(모의제어접속))
                with รหัสอักขระ.makefile('rwb') as แฟ้ม_รายการ_3d0c1245:
                    json.loads(แฟ้ม_รายการ_3d0c1245.readline())
                    for คําขอ_ค่า in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ปลายทาง_ค่า_ตําแหน่ง/'native-swing.png'),'format':'png'}}):
                        แฟ้ม_รายการ_3d0c1245.write((json.dumps(คําขอ_ค่า)+'\n').encode());แฟ้ม_รายการ_3d0c1245.flush()
                        while True:
                            반환값=json.loads(แฟ้ม_รายการ_3d0c1245.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ส่ง(คลิก_ปุ่ม(505,115))
            เชลล์('echo SWING_CLOSED_OK')
            ข้อมูล=(คลาส_พาธ/'한글창시험.class').read_bytes()
            ส่ง('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ข้อมูล),64):ส่ง(ข้อมูล[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ส่ง(b'.\n')
            ส่ง('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ส่ง(คลิก_ปุ่ม(200,255),'KOREAN SWING CLICK ชื่อ'.encode())
            ส่ง(คลิก_ปุ่ม(505,115))
            เชลล์('echo KOREAN_SWING_CLOSED_OK')
            การตรวจสอบความถูกต้อง_รายงาน.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','ไทย หน้าต่าง/ปุ่ม/แอคชัน_ข้อสังเกต/กิจกรรม_คิว directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ข้อมูล_ตําแหน่ง.poll() is None:ข้อมูล_ตําแหน่ง.terminate()
            try:ข้อมูล_ตําแหน่ง.wait(timeout=5)
            except subprocess.TimeoutExpired:ข้อมูล_ตําแหน่ง.kill();ข้อมูล_ตําแหน่ง.wait()
            ตัวเลือก_a916db4e.close();ข้อมูล_ตําแหน่ง.stdin.close();ข้อมูล_ตําแหน่ง.stdout.close();(ปลายทาง_ค่า_ตําแหน่ง/'serial.log').write_bytes(บันทึก_สถิติ);(ปลายทาง_ค่า_ตําแหน่ง/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':เรียกใช้งาน()
