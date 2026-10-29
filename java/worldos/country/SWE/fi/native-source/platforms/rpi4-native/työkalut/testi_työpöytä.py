#!/usr/bin/env python3
"""todellinen_data RFB 클라이언트로 QEMU 창의 한글/Avain_ARVO/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from työpöytä_Näkymä import VERTAA_ARVO
from Suorita_komento import aloite_juuri


def Suorita_2():
    tulos=aloite_juuri/'build/verification/desktop'; tulos.mkdir(parents=True,exist_ok=True)
    Prosessi=subprocess.Popen(['python3',str(aloite_juuri/'työkalut/työpöytä_Näkymä.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Prosessi.stdout,selectors.EVENT_READ)
    transkriptio=bytearray(); vahvistus_raportti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((aloite_juuri/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(merkintä,Suorita_2=0):
        määräaika_AIKA=time.monotonic()+45
        while merkintä not in transkriptio[Suorita_2:]:
            if time.monotonic()>määräaika_AIKA or Prosessi.poll() is not None: raise AssertionError(transkriptio[Suorita_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                data=누름값.fileobj.read(4096)
                if data: transkriptio.extend(data)
        return bytes(transkriptio[Suorita_2:])
    try:
        까지(b'TERMINAL READY')
        portin_numero=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkriptio).group(1))
        with socket.create_connection(('127.0.0.1',portin_numero),timeout=10) as asiakas:
            assert VERTAA_ARVO(asiakas,12)==b'RFB 003.008\n'; asiakas.sendall(b'RFB 003.008\n')
            assert 1 in VERTAA_ARVO(asiakas,VERTAA_ARVO(asiakas,1)[0]); asiakas.sendall(b'\x01'); assert VERTAA_ARVO(asiakas,4)==b'\0'*4
            asiakas.sendall(b'\x01'); 초기값=VERTAA_ARVO(asiakas,24); assert struct.unpack('>HH',초기값[:4])==(640,480); VERTAA_ARVO(asiakas,struct.unpack('>I',초기값[20:])[0])
            asiakas.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            asiakas.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(symboli_ARVO,누르는중=True): asiakas.sendall(struct.pack('>BBHI',4,int(누르는중),0,symboli_ARVO))
            def 글자입력(teksti):
                for merkkitiedot in teksti:
                    symboli=0xff0d if merkkitiedot=='\n' else ord(merkkitiedot) if ord(merkkitiedot)<256 else 0x01000000|ord(merkkitiedot)
                    누름값(symboli); 누름값(symboli,False)
            def paina_Avain(symboli_ARVO): 누름값(symboli_ARVO); 누름값(symboli_ARVO,False)
            # Start with English keys only, as delivered without a host IME.
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('echo '); paina_Avain(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); paina_Avain(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('echo ')
            누름값(0xffe1); paina_Avain(32); 누름값(0xffe1,False)
            글자입력('dlfr'); paina_Avain(0xff08); paina_Avain(0xff08); 글자입력('fr')
            paina_Avain(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('echo '); paina_Avain(0xff31)
            글자입력('rhk rkqtk RkRnd'); paina_Avain(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),SIIRTYMÄ_ARVO)
            # The same composition edits UTF-8 text in the native vi editor.
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',SIIRTYMÄ_ARVO)
            글자입력('i'); paina_Avain(0xffc6); 글자입력('gksrmf dlfr'); paina_Avain(0xffc6)
            paina_Avain(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),SIIRTYMÄ_ARVO); 까지(b'jkoros-native> ',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('help ko\n')
            까지('한/nolla_operandi Avain_ARVO, Shift+Space 또는 F9'.encode(),SIIRTYMÄ_ARVO); 까지(b'jkoros-native> ',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('clear\necho "VNC 한글 syöte_ARVO 😀"\n'); 까지('VNC 한글 syöte_ARVO 😀\r\n'.encode(),SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',SIIRTYMÄ_ARVO)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            leikepöytä_ARVO='echo "liitä_ARVO_8e45bfbb 완료"\n'.encode(); SIIRTYMÄ_ARVO=len(transkriptio)
            asiakas.sendall(struct.pack('>B3xI',6,len(leikepöytä_ARVO))+leikepöytä_ARVO)
            for Tapahtuma,_ in 준비살피미.select(.15):
                tietolohko=Tapahtuma.fileobj.read(4096)
                if tietolohko: transkriptio.extend(tietolohko)
            assert 'liitä_ARVO_8e45bfbb 완료'.encode() not in transkriptio[SIIRTYMÄ_ARVO:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),SIIRTYMÄ_ARVO)
            asiakas.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=VERTAA_ARVO(asiakas,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Koko=struct.unpack('>I',VERTAA_ARVO(asiakas,7)[3:])[0]; VERTAA_ARVO(asiakas,Koko); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',VERTAA_ARVO(asiakas,3)[1:])[0]
                for _ in range(사각형들):
                    x_koordinaatti,Y_koordinaatti,너비값,높이값,merkistö=struct.unpack('>HHHHi',VERTAA_ARVO(asiakas,12)); assert merkistö==0,merkistö
                    화소들=VERTAA_ARVO(asiakas,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; kohde_OSOITE_08bbd577=((Y_koordinaatti+안쪽순번)*640+x_koordinaatti+순번)*3
                            빛삼원색[kohde_OSOITE_08bbd577:kohde_OSOITE_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (tulos/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(tulos/'vnc-terminal.png'))
            SIIRTYMÄ_ARVO=len(transkriptio)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); asiakas.sendall(struct.pack('>BBHH',5,1,576,81)); asiakas.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',SIIRTYMÄ_ARVO)
            assert len(transkriptio)-SIIRTYMÄ_ARVO>8192,'exercise output longer than bridge status buffer'
            SIIRTYMÄ_ARVO=len(transkriptio); asiakas.sendall(struct.pack('>BBHH',5,1,560,63)); asiakas.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); asiakas.sendall(struct.pack('>BBHH',5,1,80,16)); asiakas.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); 글자입력('gui\n'); 까지(b'GUI READY:',SIIRTYMÄ_ARVO)
            SIIRTYMÄ_ARVO=len(transkriptio); asiakas.sendall(struct.pack('>BBHH',5,1,80,332)); asiakas.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',SIIRTYMÄ_ARVO)
            vahvistus_raportti.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Prosessi.poll() is None:
            Prosessi.terminate()
            try: Prosessi.wait(timeout=8)
            except subprocess.TimeoutExpired: Prosessi.kill(); Prosessi.wait()
        준비살피미.close(); Prosessi.stdout.close()
        (tulos/'serial.log').write_bytes(transkriptio)
        (tulos/'report.json').write_text(json.dumps(vahvistus_raportti,indent=2)+'\n')


if __name__=='__main__': Suorita_2()
