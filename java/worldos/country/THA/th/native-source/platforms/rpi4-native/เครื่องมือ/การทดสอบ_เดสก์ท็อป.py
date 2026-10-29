#!/usr/bin/env python3
"""ค่าจริง_ข้อมูล RFB 클라이언트로 QEMU 창의 한글/คีย์_ค่า/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from เดสก์ท็อป_ดู import 정확한값
from ดําเนินการ_คําสั่ง import แสดง_ราก


def เรียกใช้งาน():
    ผลผลิต=แสดง_ราก/'build/verification/desktop'; ผลผลิต.mkdir(parents=True,exist_ok=True)
    โพรเซส=subprocess.Popen(['python3',str(แสดง_ราก/'เครื่องมือ/เดสก์ท็อป_ดู.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(โพรเซส.stdout,selectors.EVENT_READ)
    การถอดความ=bytearray(); การตรวจสอบความถูกต้อง_รายงาน={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((แสดง_ราก/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(มาร์กเกอร์,เรียกใช้งาน=0):
        วันครบกําหนด_เวลา=time.monotonic()+45
        while มาร์กเกอร์ not in การถอดความ[เรียกใช้งาน:]:
            if time.monotonic()>วันครบกําหนด_เวลา or โพรเซส.poll() is not None: raise AssertionError(การถอดความ[เรียกใช้งาน:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ข้อมูล=누름값.fileobj.read(4096)
                if ข้อมูล: การถอดความ.extend(ข้อมูล)
        return bytes(การถอดความ[เรียกใช้งาน:])
    try:
        까지(b'TERMINAL READY')
        หมายเลขพอร์ต=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',การถอดความ).group(1))
        with socket.create_connection(('127.0.0.1',หมายเลขพอร์ต),timeout=10) as ไคลเอ็นต์:
            assert 정확한값(ไคลเอ็นต์,12)==b'RFB 003.008\n'; ไคลเอ็นต์.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(ไคลเอ็นต์,정확한값(ไคลเอ็นต์,1)[0]); ไคลเอ็นต์.sendall(b'\x01'); assert 정확한값(ไคลเอ็นต์,4)==b'\0'*4
            ไคลเอ็นต์.sendall(b'\x01'); 초기값=정확한값(ไคลเอ็นต์,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(ไคลเอ็นต์,struct.unpack('>I',초기값[20:])[0])
            ไคลเอ็นต์.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            ไคลเอ็นต์.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(สัญลักษณ์_ค่า,누르는중=True): ไคลเอ็นต์.sendall(struct.pack('>BBHI',4,int(누르는중),0,สัญลักษณ์_ค่า))
            def 글자입력(ข้อความ):
                for ข้อมูลอักขระ in ข้อความ:
                    สัญลักษณ์=0xff0d if ข้อมูลอักขระ=='\n' else ord(ข้อมูลอักขระ) if ord(ข้อมูลอักขระ)<256 else 0x01000000|ord(ข้อมูลอักขระ)
                    누름값(สัญลักษณ์); 누름값(สัญลักษณ์,False)
            def กด_คีย์(สัญลักษณ์_ค่า): 누름값(สัญลักษณ์_ค่า); 누름값(สัญลักษณ์_ค่า,False)
            # Start with English keys only, as delivered without a host IME.
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('echo '); กด_คีย์(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); กด_คีย์(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('echo ')
            누름값(0xffe1); กด_คีย์(32); 누름값(0xffe1,False)
            글자입력('dlfr'); กด_คีย์(0xff08); กด_คีย์(0xff08); 글자입력('fr')
            กด_คีย์(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('echo '); กด_คีย์(0xff31)
            글자입력('rhk rkqtk RkRnd'); กด_คีย์(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ออฟเซต_ค่า)
            # The same composition edits UTF-8 text in the native vi editor.
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ออฟเซต_ค่า)
            글자입력('i'); กด_คีย์(0xffc6); 글자입력('gksrmf dlfr'); กด_คีย์(0xffc6)
            กด_คีย์(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ออฟเซต_ค่า); 까지(b'jkoros-native> ',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('help ko\n')
            까지('한/ศูนย์_ตัวถูกดําเนินการ คีย์_ค่า, Shift+Space 또는 F9'.encode(),ออฟเซต_ค่า); 까지(b'jkoros-native> ',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ออฟเซต_ค่า)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            คลิปบอร์ด_ค่า='echo "วาง_ค่า 완료"\n'.encode(); ออฟเซต_ค่า=len(การถอดความ)
            ไคลเอ็นต์.sendall(struct.pack('>B3xI',6,len(คลิปบอร์ด_ค่า))+คลิปบอร์ด_ค่า)
            for เหตุการณ์,_ in 준비살피미.select(.15):
                ข้อมูล_บล็อก=เหตุการณ์.fileobj.read(4096)
                if ข้อมูล_บล็อก: การถอดความ.extend(ข้อมูล_บล็อก)
            assert 'วาง_ค่า 완료'.encode() not in การถอดความ[ออฟเซต_ค่า:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ออฟเซต_ค่า)
            ไคลเอ็นต์.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                ข้อสังเกต_ข้อความ=정확한값(ไคลเอ็นต์,1)[0]
                if ข้อสังเกต_ข้อความ==2: continue
                if ข้อสังเกต_ข้อความ==3:
                    ขนาด=struct.unpack('>I',정확한값(ไคลเอ็นต์,7)[3:])[0]; 정확한값(ไคลเอ็นต์,ขนาด); continue
                assert ข้อสังเกต_ข้อความ==0,ข้อสังเกต_ข้อความ
                사각형들=struct.unpack('>H',정확한값(ไคลเอ็นต์,3)[1:])[0]
                for _ in range(사각형들):
                    พิกัดแกน_x,세로좌표,너비값,높이값,ชุดอักขระ=struct.unpack('>HHHHi',정확한값(ไคลเอ็นต์,12)); assert ชุดอักขระ==0,ชุดอักขระ
                    화소들=정확한값(ไคลเอ็นต์,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; ปลายทาง_อีเมล=((세로좌표+안쪽순번)*640+พิกัดแกน_x+순번)*3
                            빛삼원색[ปลายทาง_อีเมล:ปลายทาง_อีเมล+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (ผลผลิต/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ผลผลิต/'vnc-terminal.png'))
            ออฟเซต_ค่า=len(การถอดความ)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,1,576,81)); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ออฟเซต_ค่า)
            assert len(การถอดความ)-ออฟเซต_ค่า>8192,'exercise output longer than bridge status buffer'
            ออฟเซต_ค่า=len(การถอดความ); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,1,560,63)); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,1,80,16)); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); 글자입력('gui\n'); 까지(b'GUI READY:',ออฟเซต_ค่า)
            ออฟเซต_ค่า=len(การถอดความ); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,1,80,332)); ไคลเอ็นต์.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ออฟเซต_ค่า)
            การตรวจสอบความถูกต้อง_รายงาน.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if โพรเซส.poll() is None:
            โพรเซส.terminate()
            try: โพรเซส.wait(timeout=8)
            except subprocess.TimeoutExpired: โพรเซส.kill(); โพรเซส.wait()
        준비살피미.close(); โพรเซส.stdout.close()
        (ผลผลิต/'serial.log').write_bytes(การถอดความ)
        (ผลผลิต/'report.json').write_text(json.dumps(การตรวจสอบความถูกต้อง_รายงาน,indent=2)+'\n')


if __name__=='__main__': เรียกใช้งาน()
