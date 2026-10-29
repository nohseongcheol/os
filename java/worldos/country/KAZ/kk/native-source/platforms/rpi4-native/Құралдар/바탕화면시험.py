#!/usr/bin/env python3
"""нақты_деректер RFB 클라이언트로 QEMU 창의 한글/Кілт_мән/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from үстелдік_Көрініс import 정확한값
from орындау_пәрмен import жоба_түбір


def Орындау_2():
    출력결과=жоба_түбір/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Үрдіс=subprocess.Popen(['python3',str(жоба_түбір/'Құралдар/үстелдік_Көрініс.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Үрдіс.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); тексерім_есеп={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,Орындау_2=0):
        ең_соңғы_мерзім_уақыт=time.monotonic()+45
        while 확인표시 not in 대화기록[Орындау_2:]:
            if time.monotonic()>ең_соңғы_мерзім_уақыт or Үрдіс.poll() is not None: raise AssertionError(대화기록[Орындау_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                деректер=누름값.fileobj.read(4096)
                if деректер: 대화기록.extend(деректер)
        return bytes(대화기록[Орындау_2:])
    try:
        까지(b'TERMINAL READY')
        порт_нөмірі=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',порт_нөмірі),timeout=10) as клиент:
            assert 정확한값(клиент,12)==b'RFB 003.008\n'; клиент.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(клиент,정확한값(клиент,1)[0]); клиент.sendall(b'\x01'); assert 정확한값(клиент,4)==b'\0'*4
            клиент.sendall(b'\x01'); 초기값=정확한값(клиент,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(клиент,struct.unpack('>I',초기값[20:])[0])
            клиент.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            клиент.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(символ_мән,누르는중=True): клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_мән))
            def 글자입력(Мәтін):
                for символдық_деректер in Мәтін:
                    символ=0xff0d if символдық_деректер=='\n' else ord(символдық_деректер) if ord(символдық_деректер)<256 else 0x01000000|ord(символдық_деректер)
                    누름값(символ); 누름값(символ,False)
            def басу_Кілт(символ_мән): 누름값(символ_мән); 누름값(символ_мән,False)
            # Start with English keys only, as delivered without a host IME.
            жылжыту_мән_450fc799=len(대화기록); 글자입력('echo '); басу_Кілт(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); басу_Кілт(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); басу_Кілт(32); 누름값(0xffe1,False)
            글자입력('dlfr'); басу_Кілт(0xff08); басу_Кілт(0xff08); 글자입력('fr')
            басу_Кілт(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('echo '); басу_Кілт(0xff31)
            글자입력('rhk rkqtk RkRnd'); басу_Кілт(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),жылжыту_мән_450fc799)
            # The same composition edits UTF-8 text in the native vi editor.
            жылжыту_мән_450fc799=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',жылжыту_мән_450fc799)
            글자입력('i'); басу_Кілт(0xffc6); 글자입력('gksrmf dlfr'); басу_Кілт(0xffc6)
            басу_Кілт(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),жылжыту_мән_450fc799); 까지(b'jkoros-native> ',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('help ko\n')
            까지('한/영 Кілт_мән, Shift+Space 또는 F9'.encode(),жылжыту_мән_450fc799); 까지(b'jkoros-native> ',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',жылжыту_мән_450fc799)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            аралық_сақтағыш_мән='echo "қою_мән 완료"\n'.encode(); жылжыту_мән_450fc799=len(대화기록)
            клиент.sendall(struct.pack('>B3xI',6,len(аралық_сақтағыш_мән))+аралық_сақтағыш_мән)
            for Оқиға,_ in 준비살피미.select(.15):
                деректер_блогы=Оқиға.fileobj.read(4096)
                if деректер_блогы: 대화기록.extend(деректер_блогы)
            assert 'қою_мән 완료'.encode() not in 대화기록[жылжыту_мән_450fc799:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),жылжыту_мән_450fc799)
            клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(клиент,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Өлшемі=struct.unpack('>I',정확한값(клиент,7)[3:])[0]; 정확한값(клиент,Өлшемі); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(клиент,3)[1:])[0]
                for _ in range(사각형들):
                    x_координатасы,Y_түймешігі_координата,너비값,높이값,таңбалар_жиыны=struct.unpack('>HHHHi',정확한값(клиент,12)); assert таңбалар_жиыны==0,таңбалар_жиыны
                    화소들=정확한값(клиент,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; тағайындау_мекенжай=((Y_түймешігі_координата+안쪽순번)*640+x_координатасы+순번)*3
                            빛삼원색[тағайындау_мекенжай:тағайындау_мекенжай+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            жылжыту_мән_450fc799=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); клиент.sendall(struct.pack('>BBHH',5,1,576,81)); клиент.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',жылжыту_мән_450fc799)
            assert len(대화기록)-жылжыту_мән_450fc799>8192,'exercise output longer than bridge status buffer'
            жылжыту_мән_450fc799=len(대화기록); клиент.sendall(struct.pack('>BBHH',5,1,560,63)); клиент.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); клиент.sendall(struct.pack('>BBHH',5,1,80,16)); клиент.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',жылжыту_мән_450fc799)
            жылжыту_мән_450fc799=len(대화기록); клиент.sendall(struct.pack('>BBHH',5,1,80,332)); клиент.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',жылжыту_мән_450fc799)
            тексерім_есеп.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Үрдіс.poll() is None:
            Үрдіс.terminate()
            try: Үрдіс.wait(timeout=8)
            except subprocess.TimeoutExpired: Үрдіс.kill(); Үрдіс.wait()
        준비살피미.close(); Үрдіс.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(тексерім_есеп,indent=2)+'\n')


if __name__=='__main__': Орындау_2()
