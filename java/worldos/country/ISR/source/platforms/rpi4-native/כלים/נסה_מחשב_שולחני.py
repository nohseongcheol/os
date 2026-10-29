#!/usr/bin/env python3
"""בפועל_נתונים RFB 클라이언트로 QEMU 창의 한글/מקש_ערך/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from מחשב_שולחני_הצג import 정확한값
from לבצע_פקודה import לשקף_בסיס


def הפעלה():
    פלט=לשקף_בסיס/'build/verification/desktop'; פלט.mkdir(parents=True,exist_ok=True)
    תהליך=subprocess.Popen(['python3',str(לשקף_בסיס/'כלים/מחשב_שולחני_הצג.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(תהליך.stdout,selectors.EVENT_READ)
    תמליל=bytearray(); אימות_דוח={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((לשקף_בסיס/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(סמן,הפעלה=0):
        תאריך_יעד_זמן=time.monotonic()+45
        while סמן not in תמליל[הפעלה:]:
            if time.monotonic()>תאריך_יעד_זמן or תהליך.poll() is not None: raise AssertionError(תמליל[הפעלה:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                נתונים=누름값.fileobj.read(4096)
                if נתונים: תמליל.extend(נתונים)
        return bytes(תמליל[הפעלה:])
    try:
        까지(b'TERMINAL READY')
        מספר_יציאה=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',תמליל).group(1))
        with socket.create_connection(('127.0.0.1',מספר_יציאה),timeout=10) as לקוח:
            assert 정확한값(לקוח,12)==b'RFB 003.008\n'; לקוח.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(לקוח,정확한값(לקוח,1)[0]); לקוח.sendall(b'\x01'); assert 정확한값(לקוח,4)==b'\0'*4
            לקוח.sendall(b'\x01'); 초기값=정확한값(לקוח,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(לקוח,struct.unpack('>I',초기값[20:])[0])
            לקוח.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            לקוח.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(סימן_ערך,누르는중=True): לקוח.sendall(struct.pack('>BBHI',4,int(누르는중),0,סימן_ערך))
            def 글자입력(טקסט):
                for נתוני_תווים in טקסט:
                    סימן=0xff0d if נתוני_תווים=='\n' else ord(נתוני_תווים) if ord(נתוני_תווים)<256 else 0x01000000|ord(נתוני_תווים)
                    누름값(סימן); 누름값(סימן,False)
            def 글쇠누르기(סימן_ערך): 누름값(סימן_ערך); 누름값(סימן_ערך,False)
            # Start with English keys only, as delivered without a host IME.
            היסט_ערך=len(תמליל); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),היסט_ערך)
            # The same composition edits UTF-8 text in the native vi editor.
            היסט_ערך=len(תמליל); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',היסט_ערך)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),היסט_ערך); 까지(b'jkoros-native> ',היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('help ko\n')
            까지('한/אפס_אופרנד מקש_ערך, Shift+Space 또는 F9'.encode(),היסט_ערך); 까지(b'jkoros-native> ',היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('clear\necho "VNC 한글 קלט_ערך 😀"\n'); 까지('VNC 한글 קלט_ערך 😀\r\n'.encode(),היסט_ערך)
            היסט_ערך=len(תמליל); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',היסט_ערך)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            לוח_ערך='echo "הדבק_ערך 완료"\n'.encode(); היסט_ערך=len(תמליל)
            לקוח.sendall(struct.pack('>B3xI',6,len(לוח_ערך))+לוח_ערך)
            for אירוע,_ in 준비살피미.select(.15):
                נתונים_בלוק=אירוע.fileobj.read(4096)
                if נתונים_בלוק: תמליל.extend(נתונים_בלוק)
            assert 'הדבק_ערך 완료'.encode() not in תמליל[היסט_ערך:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),היסט_ערך)
            לקוח.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                הודעה_טקסט=정확한값(לקוח,1)[0]
                if הודעה_טקסט==2: continue
                if הודעה_טקסט==3:
                    גודל=struct.unpack('>I',정확한값(לקוח,7)[3:])[0]; 정확한값(לקוח,גודל); continue
                assert הודעה_טקסט==0,הודעה_טקסט
                사각형들=struct.unpack('>H',정확한값(לקוח,3)[1:])[0]
                for _ in range(사각형들):
                    קואורדינטת_x,세로좌표,너비값,נדרש_גובה_ערך,ערכת_תווים=struct.unpack('>HHHHi',정확한값(לקוח,12)); assert ערכת_תווים==0,ערכת_תווים
                    화소들=정확한값(לקוח,너비값*נדרש_גובה_ערך*4)
                    for 안쪽순번 in range(נדרש_גובה_ערך):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; יעד_למען_08bbd577=((세로좌표+안쪽순번)*640+קואורדינטת_x+순번)*3
                            빛삼원색[יעד_למען_08bbd577:יעד_למען_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (פלט/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(פלט/'vnc-terminal.png'))
            היסט_ערך=len(תמליל)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',היסט_ערך)
            היסט_ערך=len(תמליל); לקוח.sendall(struct.pack('>BBHH',5,1,576,81)); לקוח.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',היסט_ערך)
            assert len(תמליל)-היסט_ערך>8192,'exercise output longer than bridge status buffer'
            היסט_ערך=len(תמליל); לקוח.sendall(struct.pack('>BBHH',5,1,560,63)); לקוח.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',היסט_ערך)
            היסט_ערך=len(תמליל); לקוח.sendall(struct.pack('>BBHH',5,1,80,16)); לקוח.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',היסט_ערך)
            היסט_ערך=len(תמליל); 글자입력('gui\n'); 까지(b'GUI READY:',היסט_ערך)
            היסט_ערך=len(תמליל); לקוח.sendall(struct.pack('>BBHH',5,1,80,332)); לקוח.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',היסט_ערך)
            אימות_דוח.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if תהליך.poll() is None:
            תהליך.terminate()
            try: תהליך.wait(timeout=8)
            except subprocess.TimeoutExpired: תהליך.kill(); תהליך.wait()
        준비살피미.close(); תהליך.stdout.close()
        (פלט/'serial.log').write_bytes(תמליל)
        (פלט/'report.json').write_text(json.dumps(אימות_דוח,indent=2)+'\n')


if __name__=='__main__': הפעלה()
