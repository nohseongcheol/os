#!/usr/bin/env python3
"""ຕົວ_ຈິງ_ຂໍ້ມູນ RFB 클라이언트로 QEMU 창의 한글/ກະແຈ_ຄ່າ/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from ເດັສທັອບ_ເບິ່ງ import 정확한값
from ປະ_ຕິ_ບັດ_ຄໍາສັ່ງ import ໂຄງ_ການ_ເລກຮາກ


def ແລ່ນ():
    출력결과=ໂຄງ_ການ_ເລກຮາກ/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    ຂະ_ບວນ_ການ=subprocess.Popen(['python3',str(ໂຄງ_ການ_ເລກຮາກ/'ເຄື່ອງມື/ເດັສທັອບ_ເບິ່ງ.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(ຂະ_ບວນ_ການ.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); ໃຊ້ໄດ້_ລາຍງານ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ໂຄງ_ການ_ເລກຮາກ/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,ແລ່ນ=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[ແລ່ນ:]:
            if time.monotonic()>마감시각 or ຂະ_ບວນ_ການ.poll() is not None: raise AssertionError(대화기록[ແລ່ນ:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ຂໍ້ມູນ=누름값.fileobj.read(4096)
                if ຂໍ້ມູນ: 대화기록.extend(ຂໍ້ມູນ)
        return bytes(대화기록[ແລ່ນ:])
    try:
        까지(b'TERMINAL READY')
        ຫມາຍເລກພອດ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',ຫມາຍເລກພອດ),timeout=10) as ລູກຂ່າຍ:
            assert 정확한값(ລູກຂ່າຍ,12)==b'RFB 003.008\n'; ລູກຂ່າຍ.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(ລູກຂ່າຍ,정확한값(ລູກຂ່າຍ,1)[0]); ລູກຂ່າຍ.sendall(b'\x01'); assert 정확한값(ລູກຂ່າຍ,4)==b'\0'*4
            ລູກຂ່າຍ.sendall(b'\x01'); 초기값=정확한값(ລູກຂ່າຍ,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(ລູກຂ່າຍ,struct.unpack('>I',초기값[20:])[0])
            ລູກຂ່າຍ.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            ລູກຂ່າຍ.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(ສັນຍາລັກ_ຄ່າ,누르는중=True): ລູກຂ່າຍ.sendall(struct.pack('>BBHI',4,int(누르는중),0,ສັນຍາລັກ_ຄ່າ))
            def 글자입력(ຂໍ້ຄວາມ):
                for ຕົວອັກສອນ_ຂໍ້ມູນ in ຂໍ້ຄວາມ:
                    ສັນຍາລັກ=0xff0d if ຕົວອັກສອນ_ຂໍ້ມູນ=='\n' else ord(ຕົວອັກສອນ_ຂໍ້ມູນ) if ord(ຕົວອັກສອນ_ຂໍ້ມູນ)<256 else 0x01000000|ord(ຕົວອັກສອນ_ຂໍ້ມູນ)
                    누름값(ສັນຍາລັກ); 누름값(ສັນຍາລັກ,False)
            def 글쇠누르기(ສັນຍາລັກ_ຄ່າ): 누름값(ສັນຍາລັກ_ຄ່າ); 누름값(ສັນຍາລັກ_ຄ່າ,False)
            # Start with English keys only, as delivered without a host IME.
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ອອບເຊັດ_ຄ່າ)
            # The same composition edits UTF-8 text in the native vi editor.
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ອອບເຊັດ_ຄ່າ)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ອອບເຊັດ_ຄ່າ); 까지(b'jkoros-native> ',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('help ko\n')
            까지('한/영 ກະແຈ_ຄ່າ, Shift+Space 또는 F9'.encode(),ອອບເຊັດ_ຄ່າ); 까지(b'jkoros-native> ',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ອອບເຊັດ_ຄ່າ)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            ຄລິບບອດ_ຄ່າ='echo "ວາງ_ຄ່າ 완료"\n'.encode(); ອອບເຊັດ_ຄ່າ=len(대화기록)
            ລູກຂ່າຍ.sendall(struct.pack('>B3xI',6,len(ຄລິບບອດ_ຄ່າ))+ຄລິບບອດ_ຄ່າ)
            for ງານ,_ in 준비살피미.select(.15):
                ຂໍ້ມູນ_ບລັອກ=ງານ.fileobj.read(4096)
                if ຂໍ້ມູນ_ບລັອກ: 대화기록.extend(ຂໍ້ມູນ_ບລັອກ)
            assert 'ວາງ_ຄ່າ 완료'.encode() not in 대화기록[ອອບເຊັດ_ຄ່າ:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ອອບເຊັດ_ຄ່າ)
            ລູກຂ່າຍ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(ລູກຂ່າຍ,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    ຂະ_ຫນາດ=struct.unpack('>I',정확한값(ລູກຂ່າຍ,7)[3:])[0]; 정확한값(ລູກຂ່າຍ,ຂະ_ຫນາດ); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(ລູກຂ່າຍ,3)[1:])[0]
                for _ in range(사각형들):
                    ຈຸດ_ພິ_ກັດ_x,ປຸ່ມ_Y_ຈຸດປະສານ,너비값,높이값,ຊຸດ_ຕົວ_ອັກ_ສອນ=struct.unpack('>HHHHi',정확한값(ລູກຂ່າຍ,12)); assert ຊຸດ_ຕົວ_ອັກ_ສອນ==0,ຊຸດ_ຕົວ_ອັກ_ສອນ
                    화소들=정확한값(ລູກຂ່າຍ,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; ປາຍທາງ_ອີເມວ=((ປຸ່ມ_Y_ຈຸດປະສານ+안쪽순번)*640+ຈຸດ_ພິ_ກັດ_x+순번)*3
                            빛삼원색[ປາຍທາງ_ອີເມວ:ປາຍທາງ_ອີເມວ+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ອອບເຊັດ_ຄ່າ=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,1,576,81)); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ອອບເຊັດ_ຄ່າ)
            assert len(대화기록)-ອອບເຊັດ_ຄ່າ>8192,'exercise output longer than bridge status buffer'
            ອອບເຊັດ_ຄ່າ=len(대화기록); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,1,560,63)); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,1,80,16)); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ອອບເຊັດ_ຄ່າ)
            ອອບເຊັດ_ຄ່າ=len(대화기록); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,1,80,332)); ລູກຂ່າຍ.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ອອບເຊັດ_ຄ່າ)
            ໃຊ້ໄດ້_ລາຍງານ.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if ຂະ_ບວນ_ການ.poll() is None:
            ຂະ_ບວນ_ການ.terminate()
            try: ຂະ_ບວນ_ການ.wait(timeout=8)
            except subprocess.TimeoutExpired: ຂະ_ບວນ_ການ.kill(); ຂະ_ບວນ_ການ.wait()
        준비살피미.close(); ຂະ_ບວນ_ການ.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(ໃຊ້ໄດ້_ລາຍງານ,indent=2)+'\n')


if __name__=='__main__': ແລ່ນ()
