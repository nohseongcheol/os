#!/usr/bin/env python3
"""واقعی_داده_ها RFB 클라이언트로 QEMU 창의 한글/کلید_مقدار/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from رایانه_نما import 정확한값
from اجرا_فرمان import نمایش_دادن_جذر


def اجرا_2():
    출력결과=نمایش_دادن_جذر/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    فرآیند=subprocess.Popen(['python3',str(نمایش_دادن_جذر/'ابزارها/رایانه_نما.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(فرآیند.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); اعتبارسنجی_گزارش={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,اجرا_2=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[اجرا_2:]:
            if time.monotonic()>마감시각 or فرآیند.poll() is not None: raise AssertionError(대화기록[اجرا_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                داده_ها=누름값.fileobj.read(4096)
                if داده_ها: 대화기록.extend(داده_ها)
        return bytes(대화기록[اجرا_2:])
    try:
        까지(b'TERMINAL READY')
        شماره_درگاه=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',شماره_درگاه),timeout=10) as سرویس_گیرنده:
            assert 정확한값(سرویس_گیرنده,12)==b'RFB 003.008\n'; سرویس_گیرنده.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(سرویس_گیرنده,정확한값(سرویس_گیرنده,1)[0]); سرویس_گیرنده.sendall(b'\x01'); assert 정확한값(سرویس_گیرنده,4)==b'\0'*4
            سرویس_گیرنده.sendall(b'\x01'); 초기값=정확한값(سرویس_گیرنده,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(سرویس_گیرنده,struct.unpack('>I',초기값[20:])[0])
            سرویس_گیرنده.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            سرویس_گیرنده.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(نماد_مقدار,누르는중=True): سرویس_گیرنده.sendall(struct.pack('>BBHI',4,int(누르는중),0,نماد_مقدار))
            def 글자입력(متن):
                for نویسه_داده_ها in متن:
                    نماد=0xff0d if نویسه_داده_ها=='\n' else ord(نویسه_داده_ها) if ord(نویسه_داده_ها)<256 else 0x01000000|ord(نویسه_داده_ها)
                    누름값(نماد); 누름값(نماد,False)
            def فشار_دادن_کلید(نماد_مقدار): 누름값(نماد_مقدار); 누름값(نماد_مقدار,False)
            # Start with English keys only, as delivered without a host IME.
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('echo '); فشار_دادن_کلید(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); فشار_دادن_کلید(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); فشار_دادن_کلید(32); 누름값(0xffe1,False)
            글자입력('dlfr'); فشار_دادن_کلید(0xff08); فشار_دادن_کلید(0xff08); 글자입력('fr')
            فشار_دادن_کلید(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('echo '); فشار_دادن_کلید(0xff31)
            글자입력('rhk rkqtk RkRnd'); فشار_دادن_کلید(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),جابجایی_لایه_ای_مقدار)
            # The same composition edits UTF-8 text in the native vi editor.
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',جابجایی_لایه_ای_مقدار)
            글자입력('i'); فشار_دادن_کلید(0xffc6); 글자입력('gksrmf dlfr'); فشار_دادن_کلید(0xffc6)
            فشار_دادن_کلید(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),جابجایی_لایه_ای_مقدار); 까지(b'jkoros-native> ',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('help ko\n')
            까지('한/영 کلید_مقدار, Shift+Space 또는 F9'.encode(),جابجایی_لایه_ای_مقدار); 까지(b'jkoros-native> ',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',جابجایی_لایه_ای_مقدار)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            کلیپ_بورد_مقدار='echo "جای_گذاری_مقدار 완료"\n'.encode(); جابجایی_لایه_ای_مقدار=len(대화기록)
            سرویس_گیرنده.sendall(struct.pack('>B3xI',6,len(کلیپ_بورد_مقدار))+کلیپ_بورد_مقدار)
            for رویداد,_ in 준비살피미.select(.15):
                داده_ها_مسدود_کردن=رویداد.fileobj.read(4096)
                if داده_ها_مسدود_کردن: 대화기록.extend(داده_ها_مسدود_کردن)
            assert 'جای_گذاری_مقدار 완료'.encode() not in 대화기록[جابجایی_لایه_ای_مقدار:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),جابجایی_لایه_ای_مقدار)
            سرویس_گیرنده.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(سرویس_گیرنده,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    اندازه=struct.unpack('>I',정확한값(سرویس_گیرنده,7)[3:])[0]; 정확한값(سرویس_گیرنده,اندازه); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(سرویس_گیرنده,3)[1:])[0]
                for _ in range(사각형들):
                    مختصات_x,دکمه_Y_مختصات,너비값,높이값,مجموعه_نویسه_ها=struct.unpack('>HHHHi',정확한값(سرویس_گیرنده,12)); assert مجموعه_نویسه_ها==0,مجموعه_نویسه_ها
                    화소들=정확한값(سرویس_گیرنده,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; مقصد_آدرس=((دکمه_Y_مختصات+안쪽순번)*640+مختصات_x+순번)*3
                            빛삼원색[مقصد_آدرس:مقصد_آدرس+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            جابجایی_لایه_ای_مقدار=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,1,576,81)); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',جابجایی_لایه_ای_مقدار)
            assert len(대화기록)-جابجایی_لایه_ای_مقدار>8192,'exercise output longer than bridge status buffer'
            جابجایی_لایه_ای_مقدار=len(대화기록); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,1,560,63)); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,1,80,16)); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',جابجایی_لایه_ای_مقدار)
            جابجایی_لایه_ای_مقدار=len(대화기록); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,1,80,332)); سرویس_گیرنده.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',جابجایی_لایه_ای_مقدار)
            اعتبارسنجی_گزارش.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if فرآیند.poll() is None:
            فرآیند.terminate()
            try: فرآیند.wait(timeout=8)
            except subprocess.TimeoutExpired: فرآیند.kill(); فرآیند.wait()
        준비살피미.close(); فرآیند.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,indent=2)+'\n')


if __name__=='__main__': اجرا_2()
