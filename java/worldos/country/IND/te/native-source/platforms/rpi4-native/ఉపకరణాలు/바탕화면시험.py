#!/usr/bin/env python3
"""వాస్తవ_డేటా RFB 클라이언트로 QEMU 창의 한글/కీ_మూల్యం/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from డెస్క్_టాప్_వీక్షణ import 정확한값
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం


def నడుపుము():
    출력결과=ప్రొజెక్ట్_మూలం/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    క్రమణం=subprocess.Popen(['python3',str(ప్రొజెక్ట్_మూలం/'ఉపకరణాలు/డెస్క్_టాప్_వీక్షణ.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(క్రమణం.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,నడుపుము=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[నడుపుము:]:
            if time.monotonic()>마감시각 or క్రమణం.poll() is not None: raise AssertionError(대화기록[నడుపుము:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                డేటా=누름값.fileobj.read(4096)
                if డేటా: 대화기록.extend(డేటా)
        return bytes(대화기록[నడుపుము:])
    try:
        까지(b'TERMINAL READY')
        పోర్ట్_సంఖ్య=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',పోర్ట్_సంఖ్య),timeout=10) as క్లయింట్:
            assert 정확한값(క్లయింట్,12)==b'RFB 003.008\n'; క్లయింట్.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(క్లయింట్,정확한값(క్లయింట్,1)[0]); క్లయింట్.sendall(b'\x01'); assert 정확한값(క్లయింట్,4)==b'\0'*4
            క్లయింట్.sendall(b'\x01'); 초기값=정확한값(క్లయింట్,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(క్లయింట్,struct.unpack('>I',초기값[20:])[0])
            క్లయింట్.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            క్లయింట్.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(చిహ్నం_మూల్యం,누르는중=True): క్లయింట్.sendall(struct.pack('>BBHI',4,int(누르는중),0,చిహ్నం_మూల్యం))
            def 글자입력(పాఠ్యము):
                for అక్షరం_డేటా in పాఠ్యము:
                    చిహ్నం=0xff0d if అక్షరం_డేటా=='\n' else ord(అక్షరం_డేటా) if ord(అక్షరం_డేటా)<256 else 0x01000000|ord(అక్షరం_డేటా)
                    누름값(చిహ్నం); 누름값(చిహ్నం,False)
            def 글쇠누르기(చిహ్నం_మూల్యం): 누름값(చిహ్నం_మూల్యం); 누름값(చిహ్నం_మూల్యం,False)
            # Start with English keys only, as delivered without a host IME.
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ఆఫ్_సెట్_మూల్యం)
            # The same composition edits UTF-8 text in the native vi editor.
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ఆఫ్_సెట్_మూల్యం)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ఆఫ్_సెట్_మూల్యం); 까지(b'jkoros-native> ',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('help ko\n')
            까지('한/영 కీ_మూల్యం, Shift+Space 또는 F9'.encode(),ఆఫ్_సెట్_మూల్యం); 까지(b'jkoros-native> ',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ఆఫ్_సెట్_మూల్యం)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            క్లిప్_బోర్డ్_మూల్యం='echo "అతికించు_మూల్యం 완료"\n'.encode(); ఆఫ్_సెట్_మూల్యం=len(대화기록)
            క్లయింట్.sendall(struct.pack('>B3xI',6,len(క్లిప్_బోర్డ్_మూల్యం))+క్లిప్_బోర్డ్_మూల్యం)
            for ఈవెంట్,_ in 준비살피미.select(.15):
                డేటా_నిరోధించు=ఈవెంట్.fileobj.read(4096)
                if డేటా_నిరోధించు: 대화기록.extend(డేటా_నిరోధించు)
            assert 'అతికించు_మూల్యం 완료'.encode() not in 대화기록[ఆఫ్_సెట్_మూల్యం:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ఆఫ్_సెట్_మూల్యం)
            క్లయింట్.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(క్లయింట్,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    పరిమాణం=struct.unpack('>I',정확한값(క్లయింట్,7)[3:])[0]; 정확한값(క్లయింట్,పరిమాణం); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(క్లయింట్,3)[1:])[0]
                for _ in range(사각형들):
                    x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు,너비값,높이값,అక్షర_సమితి=struct.unpack('>HHHHi',정확한값(క్లయింట్,12)); assert అక్షర_సమితి==0,అక్షర_సమితి
                    화소들=정확한값(క్లయింట్,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; గమ్యం_ఇమెయిల్=((Y_బటన్_సమన్వయపరుచు+안쪽순번)*640+x_నిర్దేశాంకం+순번)*3
                            빛삼원색[గమ్యం_ఇమెయిల్:గమ్యం_ఇమెయిల్+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ఆఫ్_సెట్_మూల్యం=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); క్లయింట్.sendall(struct.pack('>BBHH',5,1,576,81)); క్లయింట్.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ఆఫ్_సెట్_మూల్యం)
            assert len(대화기록)-ఆఫ్_సెట్_మూల్యం>8192,'exercise output longer than bridge status buffer'
            ఆఫ్_సెట్_మూల్యం=len(대화기록); క్లయింట్.sendall(struct.pack('>BBHH',5,1,560,63)); క్లయింట్.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); క్లయింట్.sendall(struct.pack('>BBHH',5,1,80,16)); క్లయింట్.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ఆఫ్_సెట్_మూల్యం)
            ఆఫ్_సెట్_మూల్యం=len(대화기록); క్లయింట్.sendall(struct.pack('>BBHH',5,1,80,332)); క్లయింట్.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ఆఫ్_సెట్_మూల్యం)
            నిర్ధారణ_నివేదిక.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if క్రమణం.poll() is None:
            క్రమణం.terminate()
            try: క్రమణం.wait(timeout=8)
            except subprocess.TimeoutExpired: క్రమణం.kill(); క్రమణం.wait()
        준비살피미.close(); క్రమణం.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,indent=2)+'\n')


if __name__=='__main__': నడుపుము()
