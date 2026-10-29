#!/usr/bin/env python3
"""tegelik_andmed RFB 클라이언트로 QEMU 창의 한글/Võti_VALUE/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from töölaud_Kuva import EXACT_VALUE
from Täida_käsk import Project_juur


def Käivita_2():
    toodang=Project_juur/'build/verification/desktop'; toodang.mkdir(parents=True,exist_ok=True)
    Protsess=subprocess.Popen(['python3',str(Project_juur/'Tööriistad/töölaud_Kuva.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Protsess.stdout,selectors.EVENT_READ)
    transkriptsioon=bytearray(); kinnitamine_aruanne={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(marker,Käivita_2=0):
        tähtaeg_Aeg=time.monotonic()+45
        while marker not in transkriptsioon[Käivita_2:]:
            if time.monotonic()>tähtaeg_Aeg or Protsess.poll() is not None: raise AssertionError(transkriptsioon[Käivita_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                andmed=누름값.fileobj.read(4096)
                if andmed: transkriptsioon.extend(andmed)
        return bytes(transkriptsioon[Käivita_2:])
    try:
        까지(b'TERMINAL READY')
        pordinumber=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkriptsioon).group(1))
        with socket.create_connection(('127.0.0.1',pordinumber),timeout=10) as klient:
            assert EXACT_VALUE(klient,12)==b'RFB 003.008\n'; klient.sendall(b'RFB 003.008\n')
            assert 1 in EXACT_VALUE(klient,EXACT_VALUE(klient,1)[0]); klient.sendall(b'\x01'); assert EXACT_VALUE(klient,4)==b'\0'*4
            klient.sendall(b'\x01'); 초기값=EXACT_VALUE(klient,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACT_VALUE(klient,struct.unpack('>I',초기값[20:])[0])
            klient.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klient.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(sümbol_VALUE,누르는중=True): klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,sümbol_VALUE))
            def 글자입력(Tekst):
                for tähemärgiandmed in Tekst:
                    sümbol=0xff0d if tähemärgiandmed=='\n' else ord(tähemärgiandmed) if ord(tähemärgiandmed)<256 else 0x01000000|ord(tähemärgiandmed)
                    누름값(sümbol); 누름값(sümbol,False)
            def vajutama_Võti(sümbol_VALUE): 누름값(sümbol_VALUE); 누름값(sümbol_VALUE,False)
            # Start with English keys only, as delivered without a host IME.
            nihe_VALUE=len(transkriptsioon); 글자입력('echo '); vajutama_Võti(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); vajutama_Võti(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('echo ')
            누름값(0xffe1); vajutama_Võti(32); 누름값(0xffe1,False)
            글자입력('dlfr'); vajutama_Võti(0xff08); vajutama_Võti(0xff08); 글자입력('fr')
            vajutama_Võti(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('echo '); vajutama_Võti(0xff31)
            글자입력('rhk rkqtk RkRnd'); vajutama_Võti(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),nihe_VALUE)
            # The same composition edits UTF-8 text in the native vi editor.
            nihe_VALUE=len(transkriptsioon); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',nihe_VALUE)
            글자입력('i'); vajutama_Võti(0xffc6); 글자입력('gksrmf dlfr'); vajutama_Võti(0xffc6)
            vajutama_Võti(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),nihe_VALUE); 까지(b'jkoros-native> ',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('help ko\n')
            까지('한/null_operand Võti_VALUE, Shift+Space 또는 F9'.encode(),nihe_VALUE); 까지(b'jkoros-native> ',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',nihe_VALUE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            lõikelaud_VALUE='echo "kleepima_VALUE 완료"\n'.encode(); nihe_VALUE=len(transkriptsioon)
            klient.sendall(struct.pack('>B3xI',6,len(lõikelaud_VALUE))+lõikelaud_VALUE)
            for Sündmus,_ in 준비살피미.select(.15):
                andmeplokk=Sündmus.fileobj.read(4096)
                if andmeplokk: transkriptsioon.extend(andmeplokk)
            assert 'kleepima_VALUE 완료'.encode() not in transkriptsioon[nihe_VALUE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),nihe_VALUE)
            klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                teatamine_SMS=EXACT_VALUE(klient,1)[0]
                if teatamine_SMS==2: continue
                if teatamine_SMS==3:
                    Suurus=struct.unpack('>I',EXACT_VALUE(klient,7)[3:])[0]; EXACT_VALUE(klient,Suurus); continue
                assert teatamine_SMS==0,teatamine_SMS
                사각형들=struct.unpack('>H',EXACT_VALUE(klient,3)[1:])[0]
                for _ in range(사각형들):
                    가로좌표,세로좌표,너비값,높이값,märgistik=struct.unpack('>HHHHi',EXACT_VALUE(klient,12)); assert märgistik==0,märgistik
                    화소들=EXACT_VALUE(klient,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; sihtkoht_ADDRESS=((세로좌표+안쪽순번)*640+가로좌표+순번)*3
                            빛삼원색[sihtkoht_ADDRESS:sihtkoht_ADDRESS+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (toodang/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(toodang/'vnc-terminal.png'))
            nihe_VALUE=len(transkriptsioon)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); klient.sendall(struct.pack('>BBHH',5,1,576,81)); klient.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',nihe_VALUE)
            assert len(transkriptsioon)-nihe_VALUE>8192,'exercise output longer than bridge status buffer'
            nihe_VALUE=len(transkriptsioon); klient.sendall(struct.pack('>BBHH',5,1,560,63)); klient.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); klient.sendall(struct.pack('>BBHH',5,1,80,16)); klient.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); 글자입력('gui\n'); 까지(b'GUI READY:',nihe_VALUE)
            nihe_VALUE=len(transkriptsioon); klient.sendall(struct.pack('>BBHH',5,1,80,332)); klient.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',nihe_VALUE)
            kinnitamine_aruanne.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Protsess.poll() is None:
            Protsess.terminate()
            try: Protsess.wait(timeout=8)
            except subprocess.TimeoutExpired: Protsess.kill(); Protsess.wait()
        준비살피미.close(); Protsess.stdout.close()
        (toodang/'serial.log').write_bytes(transkriptsioon)
        (toodang/'report.json').write_text(json.dumps(kinnitamine_aruanne,indent=2)+'\n')


if __name__=='__main__': Käivita_2()
