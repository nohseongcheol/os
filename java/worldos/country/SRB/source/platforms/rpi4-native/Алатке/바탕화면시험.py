#!/usr/bin/env python3
"""стваран_подаци RFB 클라이언트로 QEMU 창의 한글/Кључ_вриједност/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from десктоп_Приказ import 정확한값
from Изврши_команда import пројектовати_корен


def Покрени():
    출력결과=пројектовати_корен/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Процес=subprocess.Popen(['python3',str(пројектовати_корен/'Алатке/десктоп_Приказ.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процес.stdout,selectors.EVENT_READ)
    транскрипт=bytearray(); провјера_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,Покрени=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in транскрипт[Покрени:]:
            if time.monotonic()>마감시각 or Процес.poll() is not None: raise AssertionError(транскрипт[Покрени:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                подаци=누름값.fileobj.read(4096)
                if подаци: транскрипт.extend(подаци)
        return bytes(транскрипт[Покрени:])
    try:
        까지(b'TERMINAL READY')
        број_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',транскрипт).group(1))
        with socket.create_connection(('127.0.0.1',број_порта),timeout=10) as клијент:
            assert 정확한값(клијент,12)==b'RFB 003.008\n'; клијент.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(клијент,정확한값(клијент,1)[0]); клијент.sendall(b'\x01'); assert 정확한값(клијент,4)==b'\0'*4
            клијент.sendall(b'\x01'); 초기값=정확한값(клијент,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(клијент,struct.unpack('>I',초기값[20:])[0])
            клијент.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            клијент.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(симбол_вриједност,누르는중=True): клијент.sendall(struct.pack('>BBHI',4,int(누르는중),0,симбол_вриједност))
            def 글자입력(Текст):
                for знак_подаци in Текст:
                    симбол=0xff0d if знак_подаци=='\n' else ord(знак_подаци) if ord(знак_подаци)<256 else 0x01000000|ord(знак_подаци)
                    누름값(симбол); 누름값(симбол,False)
            def отиснути_Кључ(симбол_вриједност): 누름값(симбол_вриједност); 누름값(симбол_вриједност,False)
            # Start with English keys only, as delivered without a host IME.
            Помак_вриједност=len(транскрипт); 글자입력('echo '); отиснути_Кључ(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); отиснути_Кључ(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('echo ')
            누름값(0xffe1); отиснути_Кључ(32); 누름값(0xffe1,False)
            글자입력('dlfr'); отиснути_Кључ(0xff08); отиснути_Кључ(0xff08); 글자입력('fr')
            отиснути_Кључ(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('echo '); отиснути_Кључ(0xff31)
            글자입력('rhk rkqtk RkRnd'); отиснути_Кључ(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Помак_вриједност)
            # The same composition edits UTF-8 text in the native vi editor.
            Помак_вриједност=len(транскрипт); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Помак_вриједност)
            글자입력('i'); отиснути_Кључ(0xffc6); 글자입력('gksrmf dlfr'); отиснути_Кључ(0xffc6)
            отиснути_Кључ(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Помак_вриједност); 까지(b'jkoros-native> ',Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('help ko\n')
            까지('한/영 Кључ_вриједност, Shift+Space 또는 F9'.encode(),Помак_вриједност); 까지(b'jkoros-native> ',Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),Помак_вриједност)
            Помак_вриједност=len(транскрипт); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Помак_вриједност)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            међуспремник_вриједност='echo "залијепити_вриједност 완료"\n'.encode(); Помак_вриједност=len(транскрипт)
            клијент.sendall(struct.pack('>B3xI',6,len(међуспремник_вриједност))+међуспремник_вриједност)
            for Догађај,_ in 준비살피미.select(.15):
                подаци_блокирај=Догађај.fileobj.read(4096)
                if подаци_блокирај: транскрипт.extend(подаци_блокирај)
            assert 'залијепити_вриједност 완료'.encode() not in транскрипт[Помак_вриједност:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Помак_вриједност)
            клијент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(клијент,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Величина=struct.unpack('>I',정확한값(клијент,7)[3:])[0]; 정확한값(клијент,Величина); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(клијент,3)[1:])[0]
                for _ in range(사각형들):
                    x_координата,дугме_Y_координата,너비값,높이값,скуп_знакова=struct.unpack('>HHHHi',정확한값(клијент,12)); assert скуп_знакова==0,скуп_знакова
                    화소들=정확한값(клијент,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; одредиште_адреса=((дугме_Y_координата+안쪽순번)*640+x_координата+순번)*3
                            빛삼원색[одредиште_адреса:одредиште_адреса+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            Помак_вриједност=len(транскрипт)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Помак_вриједност)
            Помак_вриједност=len(транскрипт); клијент.sendall(struct.pack('>BBHH',5,1,576,81)); клијент.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Помак_вриједност)
            assert len(транскрипт)-Помак_вриједност>8192,'exercise output longer than bridge status buffer'
            Помак_вриједност=len(транскрипт); клијент.sendall(struct.pack('>BBHH',5,1,560,63)); клијент.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Помак_вриједност)
            Помак_вриједност=len(транскрипт); клијент.sendall(struct.pack('>BBHH',5,1,80,16)); клијент.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Помак_вриједност)
            Помак_вриједност=len(транскрипт); 글자입력('gui\n'); 까지(b'GUI READY:',Помак_вриједност)
            Помак_вриједност=len(транскрипт); клијент.sendall(struct.pack('>BBHH',5,1,80,332)); клијент.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Помак_вриједност)
            провјера_извештај.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Процес.poll() is None:
            Процес.terminate()
            try: Процес.wait(timeout=8)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
        준비살피미.close(); Процес.stdout.close()
        (출력결과/'serial.log').write_bytes(транскрипт)
        (출력결과/'report.json').write_text(json.dumps(провјера_извештај,indent=2)+'\n')


if __name__=='__main__': Покрени()
