#!/usr/bin/env python3
"""ನಿಜವಾದ_ಡೇಟಾ RFB 클라이언트로 QEMU 창의 한글/ಕೀ_ಮೌಲ್ಯ/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ import 정확한값
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ


def ಚಲಾಯಿಸು_2():
    출력결과=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    ಪ್ರಕ್ರಿಯೆ=subprocess.Popen(['python3',str(ಬಿಂಬಿಸು_ಮೂಲ/'ಪರಿಕರಗಳು/ಡೆಸ್ಕ್_ಟಾಪ್_ವೀಕ್ಷಣೆ.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(ಪ್ರಕ್ರಿಯೆ.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); ದೃಢೀಕರಣ_ವರದಿ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,ಚಲಾಯಿಸು_2=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[ಚಲಾಯಿಸು_2:]:
            if time.monotonic()>마감시각 or ಪ್ರಕ್ರಿಯೆ.poll() is not None: raise AssertionError(대화기록[ಚಲಾಯಿಸು_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ಡೇಟಾ=누름값.fileobj.read(4096)
                if ಡೇಟಾ: 대화기록.extend(ಡೇಟಾ)
        return bytes(대화기록[ಚಲಾಯಿಸು_2:])
    try:
        까지(b'TERMINAL READY')
        ಪೋರ್ಟ್_ಸಂಖ್ಯೆ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',ಪೋರ್ಟ್_ಸಂಖ್ಯೆ),timeout=10) as ಕ್ಲೈಂಟ್:
            assert 정확한값(ಕ್ಲೈಂಟ್,12)==b'RFB 003.008\n'; ಕ್ಲೈಂಟ್.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(ಕ್ಲೈಂಟ್,정확한값(ಕ್ಲೈಂಟ್,1)[0]); ಕ್ಲೈಂಟ್.sendall(b'\x01'); assert 정확한값(ಕ್ಲೈಂಟ್,4)==b'\0'*4
            ಕ್ಲೈಂಟ್.sendall(b'\x01'); 초기값=정확한값(ಕ್ಲೈಂಟ್,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(ಕ್ಲೈಂಟ್,struct.unpack('>I',초기값[20:])[0])
            ಕ್ಲೈಂಟ್.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(ಚಿಹ್ನೆ_ಮೌಲ್ಯ,누르는중=True): ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHI',4,int(누르는중),0,ಚಿಹ್ನೆ_ಮೌಲ್ಯ))
            def 글자입력(ಪಠ್ಯ):
                for ಅಕ್ಷರ_ಡೇಟಾ in ಪಠ್ಯ:
                    ಚಿಹ್ನೆ=0xff0d if ಅಕ್ಷರ_ಡೇಟಾ=='\n' else ord(ಅಕ್ಷರ_ಡೇಟಾ) if ord(ಅಕ್ಷರ_ಡೇಟಾ)<256 else 0x01000000|ord(ಅಕ್ಷರ_ಡೇಟಾ)
                    누름값(ಚಿಹ್ನೆ); 누름값(ಚಿಹ್ನೆ,False)
            def 글쇠누르기(ಚಿಹ್ನೆ_ಮೌಲ್ಯ): 누름값(ಚಿಹ್ನೆ_ಮೌಲ್ಯ); 누름값(ಚಿಹ್ನೆ_ಮೌಲ್ಯ,False)
            # Start with English keys only, as delivered without a host IME.
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            # The same composition edits UTF-8 text in the native vi editor.
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ); 까지(b'jkoros-native> ',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('help ko\n')
            까지('한/영 ಕೀ_ಮೌಲ್ಯ, Shift+Space 또는 F9'.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ); 까지(b'jkoros-native> ',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ='echo "ಅಂಟಿಸು_ಮೌಲ್ಯ 완료"\n'.encode(); ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록)
            ಕ್ಲೈಂಟ್.sendall(struct.pack('>B3xI',6,len(ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ))+ಕ್ಲಿಪ್_ಬೋರ್ಡ್_ಮೌಲ್ಯ)
            for ಸಂಗತಿ,_ in 준비살피미.select(.15):
                ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು=ಸಂಗತಿ.fileobj.read(4096)
                if ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು: 대화기록.extend(ಡೇಟಾ_ನಿರ್ಬಂಧಿಸು)
            assert 'ಅಂಟಿಸು_ಮೌಲ್ಯ 완료'.encode() not in 대화기록[ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(ಕ್ಲೈಂಟ್,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    ಗಾತ್ರ=struct.unpack('>I',정확한값(ಕ್ಲೈಂಟ್,7)[3:])[0]; 정확한값(ಕ್ಲೈಂಟ್,ಗಾತ್ರ); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(ಕ್ಲೈಂಟ್,3)[1:])[0]
                for _ in range(사각형들):
                    x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ,너비값,높이값,ಅಕ್ಷರ_ಸಮೂಹ=struct.unpack('>HHHHi',정확한값(ಕ್ಲೈಂಟ್,12)); assert ಅಕ್ಷರ_ಸಮೂಹ==0,ಅಕ್ಷರ_ಸಮೂಹ
                    화소들=정확한값(ಕ್ಲೈಂಟ್,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; ಗಮ್ಯಸ್ಥಾನ_ಇಮೇಲ್=((Y_ಬಟನ್_ಸಮನ್ವಯ+안쪽순번)*640+x_ಸಮಭಾಜಕ+순번)*3
                            빛삼원색[ಗಮ್ಯಸ್ಥಾನ_ಇಮೇಲ್:ಗಮ್ಯಸ್ಥಾನ_ಇಮೇಲ್+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,1,576,81)); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            assert len(대화기록)-ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ>8192,'exercise output longer than bridge status buffer'
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,1,560,63)); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,1,80,16)); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ=len(대화기록); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,1,80,332)); ಕ್ಲೈಂಟ್.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ)
            ದೃಢೀಕರಣ_ವರದಿ.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if ಪ್ರಕ್ರಿಯೆ.poll() is None:
            ಪ್ರಕ್ರಿಯೆ.terminate()
            try: ಪ್ರಕ್ರಿಯೆ.wait(timeout=8)
            except subprocess.TimeoutExpired: ಪ್ರಕ್ರಿಯೆ.kill(); ಪ್ರಕ್ರಿಯೆ.wait()
        준비살피미.close(); ಪ್ರಕ್ರಿಯೆ.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,indent=2)+'\n')


if __name__=='__main__': ಚಲಾಯಿಸು_2()
