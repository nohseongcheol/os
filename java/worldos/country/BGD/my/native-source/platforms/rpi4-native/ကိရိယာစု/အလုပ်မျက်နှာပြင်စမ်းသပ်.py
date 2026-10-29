#!/usr/bin/env python3
"""တကယ့်ဒေတာ RFB 클라이언트로 QEMU 창의 한글/သော့တန်ဖိုး/클립보드/마우스와 မျက်နှာပြင် 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from အလုပ်မျက်နှာပြင်ရှုမြင်ရာ import 정확한값
from စက်မောင်း import စီမံကိန်းအမြစ်


def လုပ်ဆောင်():
    출력결과=စီမံကိန်းအမြစ်/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    실행과정=subprocess.Popen(['python3',str(စီမံကိန်းအမြစ်/'ကိရိယာစု/အလုပ်မျက်နှာပြင်ရှုမြင်ရာ.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(실행과정.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); 검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,လုပ်ဆောင်=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[လုပ်ဆောင်:]:
            if time.monotonic()>마감시각 or 실행과정.poll() is not None: raise AssertionError(대화기록[လုပ်ဆောင်:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ဒေတာ=누름값.fileobj.read(4096)
                if ဒေတာ: 대화기록.extend(ဒေတာ)
        return bytes(대화기록[လုပ်ဆောင်:])
    try:
        까지(b'TERMINAL READY')
        ဆက်သွယ်ပေါက်ကိန်း=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',ဆက်သွယ်ပေါက်ကိန်း),timeout=10) as လက်ခံစက်:
            assert 정확한값(လက်ခံစက်,12)==b'RFB 003.008\n'; လက်ခံစက်.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(လက်ခံစက်,정확한값(လက်ခံစက်,1)[0]); လက်ခံစက်.sendall(b'\x01'); assert 정확한값(လက်ခံစက်,4)==b'\0'*4
            လက်ခံစက်.sendall(b'\x01'); အစဦးတန်ဖိုး=정확한값(လက်ခံစက်,24); assert struct.unpack('>HH',အစဦးတန်ဖိုး[:4])==(640,480); 정확한값(လက်ခံစက်,struct.unpack('>I',အစဦးတန်ဖိုး[20:])[0])
            လက်ခံစက်.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            လက်ခံစက်.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(သင်္ကေတတန်ဖိုး,누르는중=True): လက်ခံစက်.sendall(struct.pack('>BBHI',4,int(누르는중),0,သင်္ကေတတန်ဖိုး))
            def 글자입력(စာသား):
                for အက္ခရာဒေတာ in စာသား:
                    သင်္ကေတ=0xff0d if အက္ခရာဒေတာ=='\n' else ord(အက္ခရာဒေတာ) if ord(အက္ခရာဒေတာ)<256 else 0x01000000|ord(အက္ခရာဒေတာ)
                    누름값(သင်္ကေတ); 누름값(သင်္ကေတ,False)
            def 글쇠누르기(သင်္ကေတတန်ဖိုး): 누름값(သင်္ကေတတန်ဖိုး); 누름값(သင်္ကေတတန်ဖိုး,False)
            # Start with English keys only, as delivered without a host IME.
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),အရွေ့တန်ဖိုး)
            # The same composition edits UTF-8 text in the native vi editor.
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('vi ဟန်ဂုအဝင်.txt\n'); 까지(b'NORMAL',အရွေ့တန်ဖိုး)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('cat ဟန်ဂုအဝင်.txt\n')
            까지('한글 읽'.encode(),အရွေ့တန်ဖိုး); 까지(b'jkoros-native> ',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('help ko\n')
            까지('한/သုညတွက်ချက်ခံ သော့တန်ဖိုး, Shift+Space 또는 F9'.encode(),အရွေ့တန်ဖိုး); 까지(b'jkoros-native> ',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('clear\necho "VNC 한글 ဝင်ဒေတာ 😀"\n'); 까지('VNC 한글 ဝင်ဒေတာ 😀\r\n'.encode(),အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',အရွေ့တန်ဖိုး)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            붙임판='echo "붙여넣기 ဖြစ်သောအပြည့်အစုံ"\n'.encode(); အရွေ့တန်ဖိုး=len(대화기록)
            လက်ခံစက်.sendall(struct.pack('>B3xI',6,len(붙임판))+붙임판)
            for ဖြစ်ရပ်,_ in 준비살피미.select(.15):
                ဒေတာအတုံး=ဖြစ်ရပ်.fileobj.read(4096)
                if ဒေတာအတုံး: 대화기록.extend(ဒေတာအတုံး)
            assert '붙여넣기 ဖြစ်သောအပြည့်အစုံ'.encode() not in 대화기록[အရွေ့တန်ဖိုး:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 ဖြစ်သောအပြည့်အစုံ\r\njkoros-native> '.encode(),အရွေ့တန်ဖိုး)
            လက်ခံစက်.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(လက်ခံစက်,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    အရွယ်=struct.unpack('>I',정확한값(လက်ခံစက်,7)[3:])[0]; 정확한값(လက်ခံစက်,အရွယ်); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(လက်ခံစက်,3)[1:])[0]
                for _ in range(사각형들):
                    xတည်နေရာအမှတ်,yတည်နေရာအမှတ်,너비값,높이값,အက္ခရာကုဒ်စနစ်=struct.unpack('>HHHHi',정확한값(လက်ခံစက်,12)); assert အက္ခရာကုဒ်စနစ်==0,အက္ခရာကုဒ်စနစ်
                    화소들=정확한값(လက်ခံစက်,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for အစဉ်အမှတ် in range(너비값):
                            မူရင်းလိပ်စာ=(안쪽순번*너비값+အစဉ်အမှတ်)*4; ဦးတည်ရာလိပ်စာ=((yတည်နေရာအမှတ်+안쪽순번)*640+xတည်နေရာအမှတ်+အစဉ်အမှတ်)*3
                            빛삼원색[ဦးတည်ရာလိပ်စာ:ဦးတည်ရာလိပ်စာ+3]=bytes((화소들[မူရင်းလိပ်စာ+2],화소들[မူရင်းလိပ်စာ+1],화소들[မူရင်းလိပ်စာ]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            အရွေ့တန်ဖိုး=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); လက်ခံစက်.sendall(struct.pack('>BBHH',5,1,576,81)); လက်ခံစက်.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',အရွေ့တန်ဖိုး)
            assert len(대화기록)-အရွေ့တန်ဖိုး>8192,'exercise output longer than bridge status buffer'
            အရွေ့တန်ဖိုး=len(대화기록); လက်ခံစက်.sendall(struct.pack('>BBHH',5,1,560,63)); လက်ခံစက်.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); လက်ခံစက်.sendall(struct.pack('>BBHH',5,1,80,16)); လက်ခံစက်.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',အရွေ့တန်ဖိုး)
            အရွေ့တန်ဖိုး=len(대화기록); လက်ခံစက်.sendall(struct.pack('>BBHH',5,1,80,332)); လက်ခံစက်.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',အရွေ့တန်ဖိုး)
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


if __name__=='__main__': လုပ်ဆောင်()
