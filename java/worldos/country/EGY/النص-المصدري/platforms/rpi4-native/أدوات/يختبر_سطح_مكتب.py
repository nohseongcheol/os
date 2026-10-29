#!/usr/bin/env python3
"""الفعلي_بيانات RFB 클라이언트로 QEMU 창의 한글/مفتاح_قيمة/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from سطح_مكتب_عرض import 정확한값
from ينفذ_أمر import يعرض_جذر


def تشغيل():
    الناتج=يعرض_جذر/'build/verification/desktop'; الناتج.mkdir(parents=True,exist_ok=True)
    عملية=subprocess.Popen(['python3',str(يعرض_جذر/'أدوات/سطح_مكتب_عرض.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(عملية.stdout,selectors.EVENT_READ)
    نسخة_مكتوبة=bytearray(); التحقق_من_صحة_إبلاغ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(علامة,تشغيل=0):
        موعد_نهائي_وقت=time.monotonic()+45
        while علامة not in نسخة_مكتوبة[تشغيل:]:
            if time.monotonic()>موعد_نهائي_وقت or عملية.poll() is not None: raise AssertionError(نسخة_مكتوبة[تشغيل:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                بيانات=누름값.fileobj.read(4096)
                if بيانات: نسخة_مكتوبة.extend(بيانات)
        return bytes(نسخة_مكتوبة[تشغيل:])
    try:
        까지(b'TERMINAL READY')
        رقم_المنفذ=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',نسخة_مكتوبة).group(1))
        with socket.create_connection(('127.0.0.1',رقم_المنفذ),timeout=10) as عميل:
            assert 정확한값(عميل,12)==b'RFB 003.008\n'; عميل.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(عميل,정확한값(عميل,1)[0]); عميل.sendall(b'\x01'); assert 정확한값(عميل,4)==b'\0'*4
            عميل.sendall(b'\x01'); 초기값=정확한값(عميل,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(عميل,struct.unpack('>I',초기값[20:])[0])
            عميل.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            عميل.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(رمز_قيمة,누르는중=True): عميل.sendall(struct.pack('>BBHI',4,int(누르는중),0,رمز_قيمة))
            def 글자입력(نص):
                for بيانات_الأحرف in نص:
                    رمز=0xff0d if بيانات_الأحرف=='\n' else ord(بيانات_الأحرف) if ord(بيانات_الأحرف)<256 else 0x01000000|ord(بيانات_الأحرف)
                    누름값(رمز); 누름값(رمز,False)
            def 글쇠누르기(رمز_قيمة): 누름값(رمز_قيمة); 누름값(رمز_قيمة,False)
            # Start with English keys only, as delivered without a host IME.
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),إزاحة_قيمة)
            # The same composition edits UTF-8 text in the native vi editor.
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',إزاحة_قيمة)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),إزاحة_قيمة); 까지(b'jkoros-native> ',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('help ko\n')
            까지('한/صفر_مُعامل مفتاح_قيمة, Shift+Space 또는 F9'.encode(),إزاحة_قيمة); 까지(b'jkoros-native> ',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('clear\necho "VNC 한글 إدخال_قيمة 😀"\n'); 까지('VNC 한글 إدخال_قيمة 😀\r\n'.encode(),إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',إزاحة_قيمة)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            حافظة_قيمة='echo "لصق_قيمة 완료"\n'.encode(); إزاحة_قيمة=len(نسخة_مكتوبة)
            عميل.sendall(struct.pack('>B3xI',6,len(حافظة_قيمة))+حافظة_قيمة)
            for حدث,_ in 준비살피미.select(.15):
                بيانات_حظر=حدث.fileobj.read(4096)
                if بيانات_حظر: نسخة_مكتوبة.extend(بيانات_حظر)
            assert 'لصق_قيمة 완료'.encode() not in نسخة_مكتوبة[إزاحة_قيمة:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),إزاحة_قيمة)
            عميل.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                إشعار_نص=정확한값(عميل,1)[0]
                if إشعار_نص==2: continue
                if إشعار_نص==3:
                    حجم=struct.unpack('>I',정확한값(عميل,7)[3:])[0]; 정확한값(عميل,حجم); continue
                assert إشعار_نص==0,إشعار_نص
                사각형들=struct.unpack('>H',정확한값(عميل,3)[1:])[0]
                for _ in range(사각형들):
                    الإحداثي_س,الزر_Y_إحداثيات,너비값,مطلوب_ارتفاع_قيمة,مجموعة_أحرف=struct.unpack('>HHHHi',정확한값(عميل,12)); assert مجموعة_أحرف==0,مجموعة_أحرف
                    화소들=정확한값(عميل,너비값*مطلوب_ارتفاع_قيمة*4)
                    for 안쪽순번 in range(مطلوب_ارتفاع_قيمة):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; وجهة_عنوان=((الزر_Y_إحداثيات+안쪽순번)*640+الإحداثي_س+순번)*3
                            빛삼원색[وجهة_عنوان:وجهة_عنوان+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (الناتج/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(الناتج/'vnc-terminal.png'))
            إزاحة_قيمة=len(نسخة_مكتوبة)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); عميل.sendall(struct.pack('>BBHH',5,1,576,81)); عميل.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',إزاحة_قيمة)
            assert len(نسخة_مكتوبة)-إزاحة_قيمة>8192,'exercise output longer than bridge status buffer'
            إزاحة_قيمة=len(نسخة_مكتوبة); عميل.sendall(struct.pack('>BBHH',5,1,560,63)); عميل.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); عميل.sendall(struct.pack('>BBHH',5,1,80,16)); عميل.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); 글자입력('gui\n'); 까지(b'GUI READY:',إزاحة_قيمة)
            إزاحة_قيمة=len(نسخة_مكتوبة); عميل.sendall(struct.pack('>BBHH',5,1,80,332)); عميل.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',إزاحة_قيمة)
            التحقق_من_صحة_إبلاغ.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if عملية.poll() is None:
            عملية.terminate()
            try: عملية.wait(timeout=8)
            except subprocess.TimeoutExpired: عملية.kill(); عملية.wait()
        준비살피미.close(); عملية.stdout.close()
        (الناتج/'serial.log').write_bytes(نسخة_مكتوبة)
        (الناتج/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ,indent=2)+'\n')


if __name__=='__main__': تشغيل()
