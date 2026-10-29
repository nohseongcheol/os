#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
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
from pathlib import Path
from เดสก์ท็อป_ดู import 정확한값
from 예제되돌림서버 import 되돌림서버
from ดําเนินการ_คําสั่ง import แสดง_ราก


def การทดสอบ_ภาษา(ภาษา,되돌림서버항목,เมตริก_ข้อมูล):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));การถ่ายโอนแฟ้ม_หมายเลขพอร์ต=임시자원.getsockname()[1]
    โพรเซส=subprocess.Popen(['python3',str(แสดง_ราก/'เครื่องมือ/ดําเนินการ_คําสั่ง.py'),'--desktop','--network','--port','0','--ftp-port',str(การถ่ายโอนแฟ้ม_หมายเลขพอร์ต)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    ตัวเลือก_582fe3b9=selectors.DefaultSelector();ตัวเลือก_582fe3b9.register(โพรเซส.stdout,selectors.EVENT_READ)
    การถอดความ=bytearray();ไคลเอ็นต์=None;การถ่ายโอนแฟ้ม_เพื่อน=None
    def รับ_อีเมล(มาร์กเกอร์,เรียกใช้งาน=0):
        สิ้นสุดการโทร_ออฟเซต=time.monotonic()+60
        while มาร์กเกอร์ not in การถอดความ[เรียกใช้งาน:]:
            if time.monotonic()>สิ้นสุดการโทร_ออฟเซต or โพรเซส.poll() is not None:raise AssertionError(การถอดความ[เรียกใช้งาน:].decode('utf-8','replace'))
            for 누름값,_ in ตัวเลือก_582fe3b9.select(.1):
                ข้อมูล=누름값.fileobj.read(65536)
                if ข้อมูล:การถอดความ.extend(ข้อมูล)
        return การถอดความ[เรียกใช้งาน:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(สัญลักษณ์_ค่า,누르는중=True):ไคลเอ็นต์.sendall(struct.pack('>BBHI',4,int(누르는중),0,สัญลักษณ์_ค่า))
    def เริ่ม_ออฟเซต(บรรทัด):
        เรียกใช้งาน=len(การถอดความ)
        for รหัสอักขระ in บรรทัด+'\n':
            สัญลักษณ์_ค่า=0xff0d if รหัสอักขระ=='\n' else ord(รหัสอักขระ) if ord(รหัสอักขระ)<256 else 0x1000000|ord(รหัสอักขระ)
            누름값(สัญลักษณ์_ค่า);누름값(สัญลักษณ์_ค่า,False)
        return เรียกใช้งาน
    def เชลล์(บรรทัด):return รับ_อีเมล(b'jkoros-native> ',เริ่ม_ออฟเซต(บรรทัด))
    def ดําเนินการ_คําสั่ง(บรรทัด,예상결과):
        ข้อความ=เชลล์(บรรทัด);assert 예상결과 in ข้อความ and 'exit 0' in ข้อความ,(บรรทัด,ข้อความ)
        return ข้อความ
    def 화소들():
        ไคลเอ็นต์.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            ประเภท_ค่า=정확한값(ไคลเอ็นต์,1)[0]
            if ประเภท_ค่า==2:continue
            if ประเภท_ค่า==3:
                개수=struct.unpack('>I',정확한값(ไคลเอ็นต์,7)[3:])[0];정확한값(ไคลเอ็นต์,개수);continue
            assert ประเภท_ค่า==0,ประเภท_ค่า
            항목수=struct.unpack('>H',정확한값(ไคลเอ็นต์,3)[1:])[0]
            for _ in range(항목수):
                พิกัดแกน_x,세로좌표,너비값,높이값,ชุดอักขระ=struct.unpack('>HHHHi',정확한값(ไคลเอ็นต์,12));assert ชุดอักขระ==0,ชุดอักขระ
                ข้อมูล=정확한값(ไคลเอ็นต์,너비값*높이값*4)
                for แถว_ตําแหน่ง in range(높이값):
                    for คอลัมน์_ตําแหน่ง in range(너비값):
                        원본자료=(แถว_ตําแหน่ง*너비값+คอลัมน์_ตําแหน่ง)*4;เป้าหมาย=((세로좌표+แถว_ตําแหน่ง)*640+พิกัดแกน_x+คอลัมน์_ตําแหน่ง)*3
                        빛삼원색[เป้าหมาย:เป้าหมาย+3]=bytes((ข้อมูล[원본자료+2],ข้อมูล[원본자료+1],ข้อมูล[원본자료]))
            if 항목수:return 빛삼원색
    try:
        รับ_อีเมล(b'TERMINAL READY');รับ_อีเมล(b'jkoros-native> ',การถอดความ.rfind(b'TERMINAL READY'))
        หมายเลขพอร์ต=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',การถอดความ).group(1))
        ไคลเอ็นต์=socket.create_connection(('127.0.0.1',หมายเลขพอร์ต),timeout=10)
        assert 정확한값(ไคลเอ็นต์,12)==b'RFB 003.008\n';ไคลเอ็นต์.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(ไคลเอ็นต์,정확한값(ไคลเอ็นต์,1)[0]);ไคลเอ็นต์.sendall(b'\x01');assert 정확한값(ไคลเอ็นต์,4)==b'\0'*4
        ไคลเอ็นต์.sendall(b'\x01');초기값=정확한값(ไคลเอ็นต์,24);정확한값(ไคลเอ็นต์,struct.unpack('>I',초기값[20:])[0])
        ไคลเอ็นต์.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        ไคลเอ็นต์.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in เชลล์('ftpd start')
        การถ่ายโอนแฟ้ม_เพื่อน=ftplib.FTP();การถ่ายโอนแฟ้ม_เพื่อน.encoding='utf-8';การถ่ายโอนแฟ้ม_เพื่อน.connect('127.0.0.1',การถ่ายโอนแฟ้ม_หมายเลขพอร์ต,timeout=20);การถ่ายโอนแฟ้ม_เพื่อน.login()
        ส่วนข้อมูล_ข้อมูล=('GUI와 FTP 동시 ใช้_ค่า '+ภาษา+' 😀\n').encode()
        การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 함께.txt',io.BytesIO(ส่วนข้อมูล_ข้อมูล))
        assert ส่วนข้อมูล_ข้อมูล.decode().strip() in เชลล์('cat /함께.txt')
        받은수=bytearray();การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ส่วนข้อมูล_ข้อมูล;การถ่ายโอนแฟ้ม_เพื่อน.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        ส่ง_รายการ=เชลล์('ls /example')
        assert all(ชื่อ in ส่ง_รายการ for ชื่อ in ('java/','c/','python/','README.md')),ส่ง_รายการ
        if ภาษา=='java':
            รวม_ไฟล์กํากับ=json.loads((แสดง_ราก/'build/examples/manifest.json').read_text())
            for เส้นทาง,จุดเข้าใช้งาน in รวม_ไฟล์กํากับ.items():
                เชลล์('cp '+เส้นทาง+' /example-check.bin')
                เนื้อหา_ค่า=bytearray();การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR example-check.bin',เนื้อหา_ค่า.extend)
                assert len(เนื้อหา_ค่า)==จุดเข้าใช้งาน['bytes'] and hashlib.sha256(เนื้อหา_ค่า).hexdigest()==จุดเข้าใช้งาน['sha256'],เส้นทาง
            การถ่ายโอนแฟ้ม_เพื่อน.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            ไบนารี=bytes(range(256))*64
            การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR boundary.bin',io.BytesIO(ไบนารี))
            เนื้อหา_ค่า=bytearray();การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR boundary.bin',เนื้อหา_ค่า.extend)
            assert เนื้อหา_ค่า==ไบนารี and 'boundary.bin' in การถ่ายโอนแฟ้ม_เพื่อน.nlst()
            เชลล์('cp /boundary.bin /boundary-copy.bin')
            เนื้อหา_ค่า=bytearray();การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR boundary-copy.bin',เนื้อหา_ค่า.extend)
            assert เนื้อหา_ค่า==ไบนารี
            การถ่ายโอนแฟ้ม_เพื่อน.delete('boundary.bin');การถ่ายโอนแฟ้ม_เพื่อน.delete('boundary-copy.bin')
        assert 'พิมพ์' in เชลล์('ls /example/'+ภาษา)
        เชลล์('cd /example/'+ภาษา)
        ชื่อ_ตาราง={'java':'JAVA','c':'C','python':'PYTHON'}[ภาษา]
        예상파일=ชื่อ_ตาราง+' แฟ้ม: 한글 ข้อมูล 😀\n'
        if ภาษา=='java':
            ดําเนินการ_คําสั่ง('javac พิมพ์.java','Compiled:');ดําเนินการ_คําสั่ง('java พิมพ์','JAVA ข้อความออก: 안녕하세요 😀')
            ดําเนินการ_คําสั่ง('javac 파일예제.java','Compiled:');ดําเนินการ_คําสั่ง('java 파일예제',예상파일)
            ดําเนินการ_คําสั่ง('java เครือข่าย {} {}'.format(되돌림서버항목.연결접속번호,되돌림서버항목.전문접속번호),'JAVA 네트워크 ยืนยัน: TCP UDP 한글')
            กราฟิก_คําสั่ง='java วาดภาพ'
        elif ภาษา=='c':
            for ชื่อ,전달값,예상결과 in [('ข้อความออก','', 'C ข้อความออก: 안녕하세요 😀'),('แฟ้ม','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'C 네트워크 ยืนยัน: UDP 한글')]:
                ดําเนินการ_คําสั่ง('cc '+ชื่อ+'예제.c -o ดําเนินการ_คําสั่ง','Compiled native ARM64 ELF:')
                ดําเนินการ_คําสั่ง('./ดําเนินการ_คําสั่ง'+전달값,예상결과)
            ดําเนินการ_คําสั่ง('cc วาดภาพ.c -o ดําเนินการ_คําสั่ง','Compiled native ARM64 ELF:');กราฟิก_คําสั่ง='./ดําเนินการ_คําสั่ง'
        else:
            for ชื่อ,전달값,예상결과 in [('ข้อความออก','','PYTHON ข้อความออก: 안녕하세요 😀'),('แฟ้ม','',예상파일),
                    ('네트워크',' '+str(되돌림서버항목.전문접속번호),'PYTHON 네트워크 ยืนยัน: UDP 한글')]:
                ดําเนินการ_คําสั่ง('python '+ชื่อ+'예제.py'+전달값,예상결과)
            กราฟิก_คําสั่ง='python วาดภาพ.py'
        เริ่ม_รูปวาด=เริ่ม_ออฟเซต(กราฟิก_คําสั่ง)
        ข้อความ=รับ_อีเมล('그림을 확인한 ย้อนกลับ_ค่า Enter를 누르세요.\r\n'.encode(),เริ่ม_รูปวาด)
        assert ชื่อ_ตาราง+' 그래픽: 빨강 초록 파랑' in ข้อความ and 'exit 0' not in ข้อความ,ข้อความ
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        การถ่ายโอนแฟ้ม_เพื่อน.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';การถ่ายโอนแฟ้ม_เพื่อน.delete('도중.txt')
        빛삼원색=화소들()
        for 세로좌표,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            ออฟเซต_ค่า=(세로좌표*640+610)*3;assert tuple(빛삼원색[ออฟเซต_ค่า:ออฟเซต_ค่า+3])==색상,(ภาษา,세로좌표,tuple(빛삼원색[ออฟเซต_ค่า:ออฟเซต_ค่า+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(เมตริก_ข้อมูล/(ภาษา+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in รับ_อีเมล(b'jkoros-native> ',เริ่ม_รูปวาด)
        if ภาษา=='java':
            เริ่ม_หน้าต่าง=เริ่ม_ออฟเซต('java 창예제')
            รับ_อีเมล('GUI 예제 จัดเตรียม: 창예제'.encode(),เริ่ม_หน้าต่าง)
            def คลิก_ค่า(가로,แนวตั้ง_ตําแหน่ง):
                for ปุ่ม in (1,0):ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,ปุ่ม,가로,แนวตั้ง_ตําแหน่ง))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            คลิก_ค่า(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for อักขระ_ค่า in '한글':누름값(0x1000000|ord(อักขระ_ค่า));누름값(0x1000000|ord(อักขระ_ค่า),False)
            for 횟수 in (1,2):
                เรียกใช้งาน=len(การถอดความ);คลิก_ค่า(180,242)
                รับ_อีเมล(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),เรียกใช้งาน)
            time.sleep(.3)
            หน้าต่าง_รูปวาด=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=หน้าต่าง_รูปวาด.crop((110,272,530,300)).tobytes()
            หน้าต่าง_รูปวาด.save(str(เมตริก_ข้อมูล/'java-swing.png'))
            เรียกใช้งาน=len(การถอดความ);คลิก_ค่า(535,105)
            assert 'exit 0' in รับ_อีเมล(b'jkoros-native> ',เรียกใช้งาน)
        # Download the guest-created bytes through FTP in the same GUI VM.
        แฟ้ม_รายการ_ชื่อ={'java':'java.txt','c':'c.txt','python':'python.txt'}[ภาษา]
        เชลล์('cp '+แฟ้ม_รายการ_ชื่อ+' /ตรวจสอบความถูกต้อง.txt')
        받은수=bytearray();การถ่ายโอนแฟ้ม_เพื่อน.retrbinary('RETR ตรวจสอบความถูกต้อง.txt',받은수.extend);assert 받은수==예상파일.encode()
        เชลล์('echo preserved > พิมพ์.'+('py' if ภาษา=='python' else ภาษา))
        assert 'EXAMPLES READY' in เชลล์('example '+ภาษา)
        assert '\npreserved\n' in เชลล์('cat พิมพ์.'+('py' if ภาษา=='python' else ภาษา))
        assert '한/ศูนย์_ตัวถูกดําเนินการ คีย์_ค่า, Shift+Space 또는 F9' in เชลล์('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in เชลล์('echo GUI NETWORK TOGETHER')
        การถ่ายโอนแฟ้ม_เพื่อน.quit();การถ่ายโอนแฟ้ม_เพื่อน=None;assert 'FTP stopped' in เชลล์('ftpd stop')
        print('PASS '+ภาษา+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if การถ่ายโอนแฟ้ม_เพื่อน:
            try:การถ่ายโอนแฟ้ม_เพื่อน.close()
            except OSError:pass
        if ไคลเอ็นต์:ไคลเอ็นต์.close()
        โพรเซส.terminate()
        try:โพรเซส.wait(timeout=8)
        except subprocess.TimeoutExpired:โพรเซส.kill();โพรเซส.wait()
        ตัวเลือก_582fe3b9.close();โพรเซส.stdout.close();(เมตริก_ข้อมูล/(ภาษา+'-serial.log')).write_bytes(การถอดความ)


def เรียกใช้งาน():
    เมตริก_ข้อมูล=แสดง_ราก/'build/verification/examples';เมตริก_ข้อมูล.mkdir(parents=True,exist_ok=True)
    การตรวจสอบความถูกต้อง_รายงาน={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with 되돌림서버() as 되돌림서버항목:
            for ภาษา in ('java','c','python'):
                การทดสอบ_ภาษา(ภาษา,되돌림서버항목,เมตริก_ข้อมูล);การตรวจสอบความถูกต้อง_รายงาน['languages'].append(ภาษา)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert 되돌림서버항목.수신됨==[(ประเภท_ค่า,ข้อมูล.encode()) for ประเภท_ค่า,ข้อมูล in 예상결과],되돌림서버항목.수신됨
            การตรวจสอบความถูกต้อง_รายงาน['host_network_payloads']=[{'protocol':ประเภท_ค่า,'text':ข้อมูล.decode()} for ประเภท_ค่า,ข้อมูล in 되돌림서버항목.수신됨]
        การตรวจสอบความถูกต้อง_รายงาน.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(เมตริก_ข้อมูล/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':เรียกใช้งาน()
