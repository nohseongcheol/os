#!/usr/bin/env python3
"""વાસ્તવિક_ડેટા RFB 클라이언트로 QEMU 창의 한글/કી_મૂલ્ય/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from ડેસ્કટૉપ_જુઓ import 정확한값
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ


def ચલાવો_2():
    출력결과=પ્રોજેક્ટ_રૂટ/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    પ્રક્રિયા=subprocess.Popen(['python3',str(પ્રોજેક્ટ_રૂટ/'ઉપકરણો/ડેસ્કટૉપ_જુઓ.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(પ્રક્રિયા.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); માન્યતા_અહેવાલ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,ચલાવો_2=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[ચલાવો_2:]:
            if time.monotonic()>마감시각 or પ્રક્રિયા.poll() is not None: raise AssertionError(대화기록[ચલાવો_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ડેટા=누름값.fileobj.read(4096)
                if ડેટા: 대화기록.extend(ડેટા)
        return bytes(대화기록[ચલાવો_2:])
    try:
        까지(b'TERMINAL READY')
        પોર્ટ_નંબર=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',પોર્ટ_નંબર),timeout=10) as ક્લાયંટ:
            assert 정확한값(ક્લાયંટ,12)==b'RFB 003.008\n'; ક્લાયંટ.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(ક્લાયંટ,정확한값(ક્લાયંટ,1)[0]); ક્લાયંટ.sendall(b'\x01'); assert 정확한값(ક્લાયંટ,4)==b'\0'*4
            ક્લાયંટ.sendall(b'\x01'); 초기값=정확한값(ક્લાયંટ,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(ક્લાયંટ,struct.unpack('>I',초기값[20:])[0])
            ક્લાયંટ.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            ક્લાયંટ.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(પ્રતીક_મૂલ્ય,누르는중=True): ક્લાયંટ.sendall(struct.pack('>BBHI',4,int(누르는중),0,પ્રતીક_મૂલ્ય))
            def 글자입력(લખાણ):
                for વર્ણ_ડેટા in લખાણ:
                    પ્રતીક=0xff0d if વર્ણ_ડેટા=='\n' else ord(વર્ણ_ડેટા) if ord(વર્ણ_ડેટા)<256 else 0x01000000|ord(વર્ણ_ડેટા)
                    누름값(પ્રતીક); 누름값(પ્રતીક,False)
            def 글쇠누르기(પ્રતીક_મૂલ્ય): 누름값(પ્રતીક_મૂલ્ય); 누름값(પ્રતીક_મૂલ્ય,False)
            # Start with English keys only, as delivered without a host IME.
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ઑફસેટ_મૂલ્ય)
            # The same composition edits UTF-8 text in the native vi editor.
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ઑફસેટ_મૂલ્ય)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ઑફસેટ_મૂલ્ય); 까지(b'jkoros-native> ',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('help ko\n')
            까지('한/영 કી_મૂલ્ય, Shift+Space 또는 F9'.encode(),ઑફસેટ_મૂલ્ય); 까지(b'jkoros-native> ',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ઑફસેટ_મૂલ્ય)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            ક્લિપબોર્ડ_મૂલ્ય='echo "ચોંટાડો_મૂલ્ય 완료"\n'.encode(); ઑફસેટ_મૂલ્ય=len(대화기록)
            ક્લાયંટ.sendall(struct.pack('>B3xI',6,len(ક્લિપબોર્ડ_મૂલ્ય))+ક્લિપબોર્ડ_મૂલ્ય)
            for ઇવેંટ,_ in 준비살피미.select(.15):
                ડેટા_અવરોધિત_કરો=ઇવેંટ.fileobj.read(4096)
                if ડેટા_અવરોધિત_કરો: 대화기록.extend(ડેટા_અવરોધિત_કરો)
            assert 'ચોંટાડો_મૂલ્ય 완료'.encode() not in 대화기록[ઑફસેટ_મૂલ્ય:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ઑફસેટ_મૂલ્ય)
            ક્લાયંટ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(ક્લાયંટ,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    માપ=struct.unpack('>I',정확한값(ક્લાયંટ,7)[3:])[0]; 정확한값(ક્લાયંટ,માપ); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(ક્લાયંટ,3)[1:])[0]
                for _ in range(사각형들):
                    x_યામ,세로좌표,너비값,높이값,વર્ણ_સેટ=struct.unpack('>HHHHi',정확한값(ક્લાયંટ,12)); assert વર્ણ_સેટ==0,વર્ણ_સેટ
                    화소들=정확한값(ક્લાયંટ,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; ગંતવ્ય_સરનામું=((세로좌표+안쪽순번)*640+x_યામ+순번)*3
                            빛삼원색[ગંતવ્ય_સરનામું:ગંતવ્ય_સરનામું+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ઑફસેટ_મૂલ્ય=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); ક્લાયંટ.sendall(struct.pack('>BBHH',5,1,576,81)); ક્લાયંટ.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ઑફસેટ_મૂલ્ય)
            assert len(대화기록)-ઑફસેટ_મૂલ્ય>8192,'exercise output longer than bridge status buffer'
            ઑફસેટ_મૂલ્ય=len(대화기록); ક્લાયંટ.sendall(struct.pack('>BBHH',5,1,560,63)); ક્લાયંટ.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); ક્લાયંટ.sendall(struct.pack('>BBHH',5,1,80,16)); ક્લાયંટ.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ઑફસેટ_મૂલ્ય)
            ઑફસેટ_મૂલ્ય=len(대화기록); ક્લાયંટ.sendall(struct.pack('>BBHH',5,1,80,332)); ક્લાયંટ.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ઑફસેટ_મૂલ્ય)
            માન્યતા_અહેવાલ.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if પ્રક્રિયા.poll() is None:
            પ્રક્રિયા.terminate()
            try: પ્રક્રિયા.wait(timeout=8)
            except subprocess.TimeoutExpired: પ્રક્રિયા.kill(); પ્રક્રિયા.wait()
        준비살피미.close(); પ્રક્રિયા.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,indent=2)+'\n')


if __name__=='__main__': ચલાવો_2()
