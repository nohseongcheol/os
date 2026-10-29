#!/usr/bin/env python3
"""stvarni_podaci RFB 클라이언트로 QEMU 창의 한글/Ključ_VALUE/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from desktop_Prikaz import EXACT_VALUE
from Izvrši_komanda import radnja_koren


def koristiti():
    출력결과=radnja_koren/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Proces=subprocess.Popen(['python3',str(radnja_koren/'Alatke/desktop_Prikaz.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
    transkript=bytearray(); provera_valjanosti_izveštaj={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((radnja_koren/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(označivač,koristiti=0):
        krajnji_rok_TIME=time.monotonic()+45
        while označivač not in transkript[koristiti:]:
            if time.monotonic()>krajnji_rok_TIME or Proces.poll() is not None: raise AssertionError(transkript[koristiti:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                podaci=누름값.fileobj.read(4096)
                if podaci: transkript.extend(podaci)
        return bytes(transkript[koristiti:])
    try:
        까지(b'TERMINAL READY')
        broj_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkript).group(1))
        with socket.create_connection(('127.0.0.1',broj_porta),timeout=10) as klijent:
            assert EXACT_VALUE(klijent,12)==b'RFB 003.008\n'; klijent.sendall(b'RFB 003.008\n')
            assert 1 in EXACT_VALUE(klijent,EXACT_VALUE(klijent,1)[0]); klijent.sendall(b'\x01'); assert EXACT_VALUE(klijent,4)==b'\0'*4
            klijent.sendall(b'\x01'); 초기값=EXACT_VALUE(klijent,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACT_VALUE(klijent,struct.unpack('>I',초기값[20:])[0])
            klijent.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klijent.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(simbol_VALUE,누르는중=True): klijent.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
            def 글자입력(SMS):
                for znakovni_podaci in SMS:
                    simbol=0xff0d if znakovni_podaci=='\n' else ord(znakovni_podaci) if ord(znakovni_podaci)<256 else 0x01000000|ord(znakovni_podaci)
                    누름값(simbol); 누름값(simbol,False)
            def pritisnuti_Ključ(simbol_VALUE): 누름값(simbol_VALUE); 누름값(simbol_VALUE,False)
            # Start with English keys only, as delivered without a host IME.
            Pomak_VALUE=len(transkript); 글자입력('echo '); pritisnuti_Ključ(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); pritisnuti_Ključ(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('echo ')
            누름값(0xffe1); pritisnuti_Ključ(32); 누름값(0xffe1,False)
            글자입력('dlfr'); pritisnuti_Ključ(0xff08); pritisnuti_Ključ(0xff08); 글자입력('fr')
            pritisnuti_Ključ(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('echo '); pritisnuti_Ključ(0xff31)
            글자입력('rhk rkqtk RkRnd'); pritisnuti_Ključ(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Pomak_VALUE)
            # The same composition edits UTF-8 text in the native vi editor.
            Pomak_VALUE=len(transkript); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Pomak_VALUE)
            글자입력('i'); pritisnuti_Ključ(0xffc6); 글자입력('gksrmf dlfr'); pritisnuti_Ključ(0xffc6)
            pritisnuti_Ključ(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Pomak_VALUE); 까지(b'jkoros-native> ',Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('help ko\n')
            까지('한/nula_operand Ključ_VALUE, Shift+Space 또는 F9'.encode(),Pomak_VALUE); 까지(b'jkoros-native> ',Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),Pomak_VALUE)
            Pomak_VALUE=len(transkript); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Pomak_VALUE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            međuspremnik_VALUE='echo "nalepiti_VALUE 완료"\n'.encode(); Pomak_VALUE=len(transkript)
            klijent.sendall(struct.pack('>B3xI',6,len(međuspremnik_VALUE))+međuspremnik_VALUE)
            for događaj,_ in 준비살피미.select(.15):
                blok_podataka=događaj.fileobj.read(4096)
                if blok_podataka: transkript.extend(blok_podataka)
            assert 'nalepiti_VALUE 완료'.encode() not in transkript[Pomak_VALUE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Pomak_VALUE)
            klijent.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                obaveštavanje_SMS=EXACT_VALUE(klijent,1)[0]
                if obaveštavanje_SMS==2: continue
                if obaveštavanje_SMS==3:
                    promeniti_veličinu=struct.unpack('>I',EXACT_VALUE(klijent,7)[3:])[0]; EXACT_VALUE(klijent,promeniti_veličinu); continue
                assert obaveštavanje_SMS==0,obaveštavanje_SMS
                사각형들=struct.unpack('>H',EXACT_VALUE(klijent,3)[1:])[0]
                for _ in range(사각형들):
                    x_koordinata,세로좌표,너비값,높이값,skup_znakova=struct.unpack('>HHHHi',EXACT_VALUE(klijent,12)); assert skup_znakova==0,skup_znakova
                    화소들=EXACT_VALUE(klijent,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; odredište_adresa=((세로좌표+안쪽순번)*640+x_koordinata+순번)*3
                            빛삼원색[odredište_adresa:odredište_adresa+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            Pomak_VALUE=len(transkript)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Pomak_VALUE)
            Pomak_VALUE=len(transkript); klijent.sendall(struct.pack('>BBHH',5,1,576,81)); klijent.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Pomak_VALUE)
            assert len(transkript)-Pomak_VALUE>8192,'exercise output longer than bridge status buffer'
            Pomak_VALUE=len(transkript); klijent.sendall(struct.pack('>BBHH',5,1,560,63)); klijent.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Pomak_VALUE)
            Pomak_VALUE=len(transkript); klijent.sendall(struct.pack('>BBHH',5,1,80,16)); klijent.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Pomak_VALUE)
            Pomak_VALUE=len(transkript); 글자입력('gui\n'); 까지(b'GUI READY:',Pomak_VALUE)
            Pomak_VALUE=len(transkript); klijent.sendall(struct.pack('>BBHH',5,1,80,332)); klijent.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Pomak_VALUE)
            provera_valjanosti_izveštaj.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
        준비살피미.close(); Proces.stdout.close()
        (출력결과/'serial.log').write_bytes(transkript)
        (출력결과/'report.json').write_text(json.dumps(provera_valjanosti_izveštaj,indent=2)+'\n')


if __name__=='__main__': koristiti()
