#!/usr/bin/env python3
"""რეალური_მონაცემები RFB 클라이언트로 QEMU 창의 한글/კლავიში_მნიშვნელობა/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from სამუშაო_დაფა_ხედი import 정확한값
from შესრულება_ბრძანება import პროეცირება_ფესვი


def გაშვება():
    출력결과=პროეცირება_ფესვი/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    პროცესი=subprocess.Popen(['python3',str(პროეცირება_ფესვი/'ხელსაწყოები/სამუშაო_დაფა_ხედი.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(პროცესი.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); გადამოწმება_ანგარიში={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((პროეცირება_ფესვი/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,გაშვება=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[გაშვება:]:
            if time.monotonic()>마감시각 or პროცესი.poll() is not None: raise AssertionError(대화기록[გაშვება:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                მონაცემები=누름값.fileobj.read(4096)
                if მონაცემები: 대화기록.extend(მონაცემები)
        return bytes(대화기록[გაშვება:])
    try:
        까지(b'TERMINAL READY')
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',접속번호),timeout=10) as კლიენტი:
            assert 정확한값(კლიენტი,12)==b'RFB 003.008\n'; კლიენტი.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(კლიენტი,정확한값(კლიენტი,1)[0]); კლიენტი.sendall(b'\x01'); assert 정확한값(კლიენტი,4)==b'\0'*4
            კლიენტი.sendall(b'\x01'); 초기값=정확한값(კლიენტი,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(კლიენტი,struct.unpack('>I',초기값[20:])[0])
            კლიენტი.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            კლიენტი.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(სიმბოლო_მნიშვნელობა,누르는중=True): კლიენტი.sendall(struct.pack('>BBHI',4,int(누르는중),0,სიმბოლო_მნიშვნელობა))
            def 글자입력(ტექსტი):
                for სიმბოლო_მონაცემები_4d9f8719 in ტექსტი:
                    სიმბოლო=0xff0d if სიმბოლო_მონაცემები_4d9f8719=='\n' else ord(სიმბოლო_მონაცემები_4d9f8719) if ord(სიმბოლო_მონაცემები_4d9f8719)<256 else 0x01000000|ord(სიმბოლო_მონაცემები_4d9f8719)
                    누름값(სიმბოლო); 누름값(სიმბოლო,False)
            def დაჭერა_კლავიში(სიმბოლო_მნიშვნელობა): 누름값(სიმბოლო_მნიშვნელობა); 누름값(სიმბოლო_მნიშვნელობა,False)
            # Start with English keys only, as delivered without a host IME.
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('echo '); დაჭერა_კლავიში(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); დაჭერა_კლავიში(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); დაჭერა_კლავიში(32); 누름값(0xffe1,False)
            글자입력('dlfr'); დაჭერა_კლავიში(0xff08); დაჭერა_კლავიში(0xff08); 글자입력('fr')
            დაჭერა_კლავიში(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('echo '); დაჭერა_კლავიში(0xff31)
            글자입력('rhk rkqtk RkRnd'); დაჭერა_კლავიში(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ოფსეტი_მნიშვნელობა)
            # The same composition edits UTF-8 text in the native vi editor.
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ოფსეტი_მნიშვნელობა)
            글자입력('i'); დაჭერა_კლავიში(0xffc6); 글자입력('gksrmf dlfr'); დაჭერა_კლავიში(0xffc6)
            დაჭერა_კლავიში(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ოფსეტი_მნიშვნელობა); 까지(b'jkoros-native> ',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('help ko\n')
            까지('한/영 კლავიში_მნიშვნელობა, Shift+Space 또는 F9'.encode(),ოფსეტი_მნიშვნელობა); 까지(b'jkoros-native> ',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ოფსეტი_მნიშვნელობა)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            გაცვლის_ბუფერი_მნიშვნელობა='echo "ჩასმა_მნიშვნელობა 완료"\n'.encode(); ოფსეტი_მნიშვნელობა=len(대화기록)
            კლიენტი.sendall(struct.pack('>B3xI',6,len(გაცვლის_ბუფერი_მნიშვნელობა))+გაცვლის_ბუფერი_მნიშვნელობა)
            for მოვლენა,_ in 준비살피미.select(.15):
                მონაცემები_დაბლოკვა=მოვლენა.fileobj.read(4096)
                if მონაცემები_დაბლოკვა: 대화기록.extend(მონაცემები_დაბლოკვა)
            assert 'ჩასმა_მნიშვნელობა 완료'.encode() not in 대화기록[ოფსეტი_მნიშვნელობა:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ოფსეტი_მნიშვნელობა)
            კლიენტი.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(კლიენტი,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    ზომა=struct.unpack('>I',정확한값(კლიენტი,7)[3:])[0]; 정확한값(კლიენტი,ზომა); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(კლიენტი,3)[1:])[0]
                for _ in range(사각형들):
                    x_კოორდინატა,Y_ღილაკი_კოორდინატი,너비값,높이값,კოდირება=struct.unpack('>HHHHi',정확한값(კლიენტი,12)); assert კოდირება==0,კოდირება
                    화소들=정확한값(კლიენტი,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; მიმართულება_მისამართი=((Y_ღილაკი_კოორდინატი+안쪽순번)*640+x_კოორდინატა+순번)*3
                            빛삼원색[მიმართულება_მისამართი:მიმართულება_მისამართი+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ოფსეტი_მნიშვნელობა=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); კლიენტი.sendall(struct.pack('>BBHH',5,1,576,81)); კლიენტი.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ოფსეტი_მნიშვნელობა)
            assert len(대화기록)-ოფსეტი_მნიშვნელობა>8192,'exercise output longer than bridge status buffer'
            ოფსეტი_მნიშვნელობა=len(대화기록); კლიენტი.sendall(struct.pack('>BBHH',5,1,560,63)); კლიენტი.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); კლიენტი.sendall(struct.pack('>BBHH',5,1,80,16)); კლიენტი.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ოფსეტი_მნიშვნელობა)
            ოფსეტი_მნიშვნელობა=len(대화기록); კლიენტი.sendall(struct.pack('>BBHH',5,1,80,332)); კლიენტი.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ოფსეტი_მნიშვნელობა)
            გადამოწმება_ანგარიში.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if პროცესი.poll() is None:
            პროცესი.terminate()
            try: პროცესი.wait(timeout=8)
            except subprocess.TimeoutExpired: პროცესი.kill(); პროცესი.wait()
        준비살피미.close(); პროცესი.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(გადამოწმება_ანგარიში,indent=2)+'\n')


if __name__=='__main__': გაშვება()
