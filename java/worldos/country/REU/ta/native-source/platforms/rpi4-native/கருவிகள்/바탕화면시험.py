#!/usr/bin/env python3
"""அசல்_தரவு RFB 클라이언트로 QEMU 창의 한글/சாவி_மதிப்பு/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from டெஸ்க்டாப்_காட்சி import 정확한값
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்


def செயல்படுத்துக():
    출력결과=திட்டப்பணி_மூலம்/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    செயல்பாடு=subprocess.Popen(['python3',str(திட்டப்பணி_மூலம்/'கருவிகள்/டெஸ்க்டாப்_காட்சி.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(செயல்பாடு.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); செல்லுபடியாக்கம்_அறிக்கை={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,செயல்படுத்துக=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[செயல்படுத்துக:]:
            if time.monotonic()>마감시각 or செயல்பாடு.poll() is not None: raise AssertionError(대화기록[செயல்படுத்துக:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                தரவு=누름값.fileobj.read(4096)
                if தரவு: 대화기록.extend(தரவு)
        return bytes(대화기록[செயல்படுத்துக:])
    try:
        까지(b'TERMINAL READY')
        முனைய_எண்=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',முனைய_எண்),timeout=10) as பயனகம்:
            assert 정확한값(பயனகம்,12)==b'RFB 003.008\n'; பயனகம்.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(பயனகம்,정확한값(பயனகம்,1)[0]); பயனகம்.sendall(b'\x01'); assert 정확한값(பயனகம்,4)==b'\0'*4
            பயனகம்.sendall(b'\x01'); 초기값=정확한값(பயனகம்,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(பயனகம்,struct.unpack('>I',초기값[20:])[0])
            பயனகம்.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            பயனகம்.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(சின்னம்_மதிப்பு,누르는중=True): பயனகம்.sendall(struct.pack('>BBHI',4,int(누르는중),0,சின்னம்_மதிப்பு))
            def 글자입력(உரை):
                for எழுத்துருத்_தரவு in உரை:
                    சின்னம்=0xff0d if எழுத்துருத்_தரவு=='\n' else ord(எழுத்துருத்_தரவு) if ord(எழுத்துருத்_தரவு)<256 else 0x01000000|ord(எழுத்துருத்_தரவு)
                    누름값(சின்னம்); 누름값(சின்னம்,False)
            def 글쇠누르기(சின்னம்_மதிப்பு): 누름값(சின்னம்_மதிப்பு); 누름값(சின்னம்_மதிப்பு,False)
            # Start with English keys only, as delivered without a host IME.
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ஆஃப்செட்_மதிப்பு)
            # The same composition edits UTF-8 text in the native vi editor.
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ஆஃப்செட்_மதிப்பு)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ஆஃப்செட்_மதிப்பு); 까지(b'jkoros-native> ',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('help ko\n')
            까지('한/영 சாவி_மதிப்பு, Shift+Space 또는 F9'.encode(),ஆஃப்செட்_மதிப்பு); 까지(b'jkoros-native> ',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ஆஃப்செட்_மதிப்பு)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            நகலகம்_மதிப்பு='echo "ஒட்டு_மதிப்பு 완료"\n'.encode(); ஆஃப்செட்_மதிப்பு=len(대화기록)
            பயனகம்.sendall(struct.pack('>B3xI',6,len(நகலகம்_மதிப்பு))+நகலகம்_மதிப்பு)
            for நிகழ்வு,_ in 준비살피미.select(.15):
                தரவு_தடு=நிகழ்வு.fileobj.read(4096)
                if தரவு_தடு: 대화기록.extend(தரவு_தடு)
            assert 'ஒட்டு_மதிப்பு 완료'.encode() not in 대화기록[ஆஃப்செட்_மதிப்பு:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ஆஃப்செட்_மதிப்பு)
            பயனகம்.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(பயனகம்,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    அளவு=struct.unpack('>I',정확한값(பயனகம்,7)[3:])[0]; 정확한값(பயனகம்,அளவு); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(பயனகம்,3)[1:])[0]
                for _ in range(사각형들):
                    x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு,너비값,높이값,எழுத்துக்குறி_குழு=struct.unpack('>HHHHi',정확한값(பயனகம்,12)); assert எழுத்துக்குறி_குழு==0,எழுத்துக்குறி_குழு
                    화소들=정확한값(பயனகம்,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; இலக்கு_முகவரி_08bbd577=((Y_பொத்தான்_அச்சுத்_தொகுப்பு+안쪽순번)*640+x_ஒத்ததரமுள்ளது+순번)*3
                            빛삼원색[இலக்கு_முகவரி_08bbd577:இலக்கு_முகவரி_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ஆஃப்செட்_மதிப்பு=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); பயனகம்.sendall(struct.pack('>BBHH',5,1,576,81)); பயனகம்.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ஆஃப்செட்_மதிப்பு)
            assert len(대화기록)-ஆஃப்செட்_மதிப்பு>8192,'exercise output longer than bridge status buffer'
            ஆஃப்செட்_மதிப்பு=len(대화기록); பயனகம்.sendall(struct.pack('>BBHH',5,1,560,63)); பயனகம்.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); பயனகம்.sendall(struct.pack('>BBHH',5,1,80,16)); பயனகம்.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ஆஃப்செட்_மதிப்பு)
            ஆஃப்செட்_மதிப்பு=len(대화기록); பயனகம்.sendall(struct.pack('>BBHH',5,1,80,332)); பயனகம்.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ஆஃப்செட்_மதிப்பு)
            செல்லுபடியாக்கம்_அறிக்கை.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if செயல்பாடு.poll() is None:
            செயல்பாடு.terminate()
            try: செயல்பாடு.wait(timeout=8)
            except subprocess.TimeoutExpired: செயல்பாடு.kill(); செயல்பாடு.wait()
        준비살피미.close(); செயல்பாடு.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,indent=2)+'\n')


if __name__=='__main__': செயல்படுத்துக()
