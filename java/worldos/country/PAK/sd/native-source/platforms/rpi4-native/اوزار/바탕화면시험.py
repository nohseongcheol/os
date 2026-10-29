#!/usr/bin/env python3
"""اصلي_ڪوائف RFB 클라이언트로 QEMU 창의 한글/ڪليد_قدر/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from ڊيسڪٽاپ_منظر import 정확한값
from تعميل_ڪرڻ_حڪم import 기준


def هلائڻ():
    출력결과=기준/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    عمل_a7054519=subprocess.Popen(['python3',str(기준/'اوزار/ڊيسڪٽاپ_منظر.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(عمل_a7054519.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); ڪارگر_رپورٽ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,هلائڻ=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[هلائڻ:]:
            if time.monotonic()>마감시각 or عمل_a7054519.poll() is not None: raise AssertionError(대화기록[هلائڻ:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ڪوائف=누름값.fileobj.read(4096)
                if ڪوائف: 대화기록.extend(ڪوائف)
        return bytes(대화기록[هلائڻ:])
    try:
        까지(b'TERMINAL READY')
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',접속번호),timeout=10) as گراهڪ:
            assert 정확한값(گراهڪ,12)==b'RFB 003.008\n'; گراهڪ.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(گراهڪ,정확한값(گراهڪ,1)[0]); گراهڪ.sendall(b'\x01'); assert 정확한값(گراهڪ,4)==b'\0'*4
            گراهڪ.sendall(b'\x01'); 초기값=정확한값(گراهڪ,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(گراهڪ,struct.unpack('>I',초기값[20:])[0])
            گراهڪ.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            گراهڪ.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(نشاني_قدر,누르는중=True): گراهڪ.sendall(struct.pack('>BBHI',4,int(누르는중),0,نشاني_قدر))
            def 글자입력(متن):
                for ڪريڪٽر_ڪوائف in متن:
                    نشاني=0xff0d if ڪريڪٽر_ڪوائف=='\n' else ord(ڪريڪٽر_ڪوائف) if ord(ڪريڪٽر_ڪوائف)<256 else 0x01000000|ord(ڪريڪٽر_ڪوائف)
                    누름값(نشاني); 누름값(نشاني,False)
            def 글쇠누르기(نشاني_قدر): 누름값(نشاني_قدر); 누름값(نشاني_قدر,False)
            # Start with English keys only, as delivered without a host IME.
            آف_سيٽ_قدر=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),آف_سيٽ_قدر)
            # The same composition edits UTF-8 text in the native vi editor.
            آف_سيٽ_قدر=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',آف_سيٽ_قدر)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),آف_سيٽ_قدر); 까지(b'jkoros-native> ',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('help ko\n')
            까지('한/영 ڪليد_قدر, Shift+Space 또는 F9'.encode(),آف_سيٽ_قدر); 까지(b'jkoros-native> ',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',آف_سيٽ_قدر)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            تراشه_تختو_قدر='echo "چپڪايو_قدر 완료"\n'.encode(); آف_سيٽ_قدر=len(대화기록)
            گراهڪ.sendall(struct.pack('>B3xI',6,len(تراشه_تختو_قدر))+تراشه_تختو_قدر)
            for واقعو,_ in 준비살피미.select(.15):
                ڪوائف_بلاڪ_ڪريو=واقعو.fileobj.read(4096)
                if ڪوائف_بلاڪ_ڪريو: 대화기록.extend(ڪوائف_بلاڪ_ڪريو)
            assert 'چپڪايو_قدر 완료'.encode() not in 대화기록[آف_سيٽ_قدر:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),آف_سيٽ_قدر)
            گراهڪ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(گراهڪ,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    سائيز=struct.unpack('>I',정확한값(گراهڪ,7)[3:])[0]; 정확한값(گراهڪ,سائيز); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(گراهڪ,3)[1:])[0]
                for _ in range(사각형들):
                    x_رطبو,세로좌표,너비값,높이값,ڪيريڪٽرن_جو_سيٽ=struct.unpack('>HHHHi',정확한값(گراهڪ,12)); assert ڪيريڪٽرن_جو_سيٽ==0,ڪيريڪٽرن_جو_سيٽ
                    화소들=정확한값(گراهڪ,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; منزل_مقصود_پتو=((세로좌표+안쪽순번)*640+x_رطبو+순번)*3
                            빛삼원색[منزل_مقصود_پتو:منزل_مقصود_پتو+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            آف_سيٽ_قدر=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); گراهڪ.sendall(struct.pack('>BBHH',5,1,576,81)); گراهڪ.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',آف_سيٽ_قدر)
            assert len(대화기록)-آف_سيٽ_قدر>8192,'exercise output longer than bridge status buffer'
            آف_سيٽ_قدر=len(대화기록); گراهڪ.sendall(struct.pack('>BBHH',5,1,560,63)); گراهڪ.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); گراهڪ.sendall(struct.pack('>BBHH',5,1,80,16)); گراهڪ.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',آف_سيٽ_قدر)
            آف_سيٽ_قدر=len(대화기록); گراهڪ.sendall(struct.pack('>BBHH',5,1,80,332)); گراهڪ.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',آف_سيٽ_قدر)
            ڪارگر_رپورٽ.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if عمل_a7054519.poll() is None:
            عمل_a7054519.terminate()
            try: عمل_a7054519.wait(timeout=8)
            except subprocess.TimeoutExpired: عمل_a7054519.kill(); عمل_a7054519.wait()
        준비살피미.close(); عمل_a7054519.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(ڪارگر_رپورٽ,indent=2)+'\n')


if __name__=='__main__': هلائڻ()
