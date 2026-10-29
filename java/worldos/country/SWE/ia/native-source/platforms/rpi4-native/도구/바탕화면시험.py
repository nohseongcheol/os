#!/usr/bin/env python3
"""실제 RFB 클라이언트로 QEMU 창의 한글/키/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from 바탕화면 import 정확한값
from 실행 import 기준


def Exeque():
    출력결과=기준/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    실행과정=subprocess.Popen(['python3',str(기준/'도구/바탕화면.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(실행과정.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); 검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,Exeque=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[Exeque:]:
            if time.monotonic()>마감시각 or 실행과정.poll() is not None: raise AssertionError(대화기록[Exeque:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                자료=누름값.fileobj.read(4096)
                if 자료: 대화기록.extend(자료)
        return bytes(대화기록[Exeque:])
    try:
        까지(b'TERMINAL READY')
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',접속번호),timeout=10) as 접속자:
            assert 정확한값(접속자,12)==b'RFB 003.008\n'; 접속자.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(접속자,정확한값(접속자,1)[0]); 접속자.sendall(b'\x01'); assert 정확한값(접속자,4)==b'\0'*4
            접속자.sendall(b'\x01'); 초기값=정확한값(접속자,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(접속자,struct.unpack('>I',초기값[20:])[0])
            접속자.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            접속자.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(심볼,누르는중=True): 접속자.sendall(struct.pack('>BBHI',4,int(누르는중),0,심볼))
            def 글자입력(texto):
                for 글자값 in texto:
                    기호=0xff0d if 글자값=='\n' else ord(글자값) if ord(글자값)<256 else 0x01000000|ord(글자값)
                    누름값(기호); 누름값(기호,False)
            def 글쇠누르기(심볼): 누름값(심볼); 누름값(심볼,False)
            # Start with English keys only, as delivered without a host IME.
            변위=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),변위)
            변위=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),변위)
            변위=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),변위)
            # The same composition edits UTF-8 text in the native vi editor.
            변위=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',변위)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',변위)
            변위=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),변위); 까지(b'jkoros-native> ',변위)
            변위=len(대화기록); 글자입력('help ko\n')
            까지('한/영 키, Shift+Space 또는 F9'.encode(),변위); 까지(b'jkoros-native> ',변위)
            변위=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),변위)
            변위=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',변위)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            붙임판='echo "붙여넣기 완료"\n'.encode(); 변위=len(대화기록)
            접속자.sendall(struct.pack('>B3xI',6,len(붙임판))+붙임판)
            for 사건,_ in 준비살피미.select(.15):
                자료덩이=사건.fileobj.read(4096)
                if 자료덩이: 대화기록.extend(자료덩이)
            assert '붙여넣기 완료'.encode() not in 대화기록[변위:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),변위)
            접속자.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(접속자,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Grandor=struct.unpack('>I',정확한값(접속자,7)[3:])[0]; 정확한값(접속자,Grandor); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(접속자,3)[1:])[0]
                for _ in range(사각형들):
                    가로좌표,세로좌표,너비값,높이값,문자부호=struct.unpack('>HHHHi',정확한값(접속자,12)); assert 문자부호==0,문자부호
                    화소들=정확한값(접속자,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; 목적주소=((세로좌표+안쪽순번)*640+가로좌표+순번)*3
                            빛삼원색[목적주소:목적주소+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            변위=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',변위)
            변위=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',변위)
            변위=len(대화기록); 접속자.sendall(struct.pack('>BBHH',5,1,576,81)); 접속자.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',변위)
            변위=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',변위)
            assert len(대화기록)-변위>8192,'exercise output longer than bridge status buffer'
            변위=len(대화기록); 접속자.sendall(struct.pack('>BBHH',5,1,560,63)); 접속자.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',변위)
            변위=len(대화기록); 접속자.sendall(struct.pack('>BBHH',5,1,80,16)); 접속자.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',변위)
            변위=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',변위)
            변위=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',변위)
            변위=len(대화기록); 접속자.sendall(struct.pack('>BBHH',5,1,80,332)); 접속자.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',변위)
            검증기록.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if 실행과정.poll() is None:
            실행과정.terminate()
            try: 실행과정.wait(timeout=8)
            except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
        준비살피미.close(); 실행과정.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(검증기록,indent=2)+'\n')


if __name__=='__main__': Exeque()
