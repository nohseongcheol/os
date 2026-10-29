#!/usr/bin/env python3
"""verklig_data RFB 클라이언트로 QEMU 창의 한글/Nyckel_värde/클립보드/마우스와 skärmbild 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from Dator_vy import EXAKT_värde
from köra_kommando import åtgärd_rot


def Kör():
    utleverans=åtgärd_rot/'build/verification/desktop'; utleverans.mkdir(parents=True,exist_ok=True)
    Process=subprocess.Popen(['python3',str(åtgärd_rot/'verktyg/Dator_vy.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Process.stdout,selectors.EVENT_READ)
    avskrift=bytearray(); validering_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((åtgärd_rot/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(markör_8b722c5f,Kör=0):
        måldatum_tid=time.monotonic()+45
        while markör_8b722c5f not in avskrift[Kör:]:
            if time.monotonic()>måldatum_tid or Process.poll() is not None: raise AssertionError(avskrift[Kör:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                data=누름값.fileobj.read(4096)
                if data: avskrift.extend(data)
        return bytes(avskrift[Kör:])
    try:
        까지(b'TERMINAL READY')
        portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',avskrift).group(1))
        with socket.create_connection(('127.0.0.1',portnummer),timeout=10) as klient:
            assert EXAKT_värde(klient,12)==b'RFB 003.008\n'; klient.sendall(b'RFB 003.008\n')
            assert 1 in EXAKT_värde(klient,EXAKT_värde(klient,1)[0]); klient.sendall(b'\x01'); assert EXAKT_värde(klient,4)==b'\0'*4
            klient.sendall(b'\x01'); 초기값=EXAKT_värde(klient,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXAKT_värde(klient,struct.unpack('>I',초기값[20:])[0])
            klient.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klient.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(symbol_värde,누르는중=True): klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_värde))
            def 글자입력(text):
                for teckendata in text:
                    symbol=0xff0d if teckendata=='\n' else ord(teckendata) if ord(teckendata)<256 else 0x01000000|ord(teckendata)
                    누름값(symbol); 누름값(symbol,False)
            def tryck_Nyckel(symbol_värde): 누름값(symbol_värde); 누름값(symbol_värde,False)
            # Start with English keys only, as delivered without a host IME.
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('echo '); tryck_Nyckel(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); tryck_Nyckel(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('echo ')
            누름값(0xffe1); tryck_Nyckel(32); 누름값(0xffe1,False)
            글자입력('dlfr'); tryck_Nyckel(0xff08); tryck_Nyckel(0xff08); 글자입력('fr')
            tryck_Nyckel(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('echo '); tryck_Nyckel(0xff31)
            글자입력('rhk rkqtk RkRnd'); tryck_Nyckel(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),FÖRSKJUTNING_värde)
            # The same composition edits UTF-8 text in the native vi editor.
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',FÖRSKJUTNING_värde)
            글자입력('i'); tryck_Nyckel(0xffc6); 글자입력('gksrmf dlfr'); tryck_Nyckel(0xffc6)
            tryck_Nyckel(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),FÖRSKJUTNING_värde); 까지(b'jkoros-native> ',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('help ko\n')
            까지('한/noll_operand Nyckel_värde, Shift+Space 또는 F9'.encode(),FÖRSKJUTNING_värde); 까지(b'jkoros-native> ',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('clear\necho "VNC 한글 indata_värde 😀"\n'); 까지('VNC 한글 indata_värde 😀\r\n'.encode(),FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',FÖRSKJUTNING_värde)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            Urklipp_värde='echo "klistra_in_värde 완료"\n'.encode(); FÖRSKJUTNING_värde=len(avskrift)
            klient.sendall(struct.pack('>B3xI',6,len(Urklipp_värde))+Urklipp_värde)
            for Händelse,_ in 준비살피미.select(.15):
                datablock=Händelse.fileobj.read(4096)
                if datablock: avskrift.extend(datablock)
            assert 'klistra_in_värde 완료'.encode() not in avskrift[FÖRSKJUTNING_värde:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),FÖRSKJUTNING_värde)
            klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=EXAKT_värde(klient,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Storlek=struct.unpack('>I',EXAKT_värde(klient,7)[3:])[0]; EXAKT_värde(klient,Storlek); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',EXAKT_värde(klient,3)[1:])[0]
                for _ in range(사각형들):
                    x_koordinat,Y_koordinat,너비값,높이값,teckenuppsättning=struct.unpack('>HHHHi',EXAKT_värde(klient,12)); assert teckenuppsättning==0,teckenuppsättning
                    화소들=EXAKT_värde(klient,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; mål_ADRESS_08bbd577=((Y_koordinat+안쪽순번)*640+x_koordinat+순번)*3
                            빛삼원색[mål_ADRESS_08bbd577:mål_ADRESS_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (utleverans/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(utleverans/'vnc-terminal.png'))
            FÖRSKJUTNING_värde=len(avskrift)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); klient.sendall(struct.pack('>BBHH',5,1,576,81)); klient.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',FÖRSKJUTNING_värde)
            assert len(avskrift)-FÖRSKJUTNING_värde>8192,'exercise output longer than bridge status buffer'
            FÖRSKJUTNING_värde=len(avskrift); klient.sendall(struct.pack('>BBHH',5,1,560,63)); klient.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); klient.sendall(struct.pack('>BBHH',5,1,80,16)); klient.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); 글자입력('gui\n'); 까지(b'GUI READY:',FÖRSKJUTNING_värde)
            FÖRSKJUTNING_värde=len(avskrift); klient.sendall(struct.pack('>BBHH',5,1,80,332)); klient.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',FÖRSKJUTNING_värde)
            validering_Rapport.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Process.poll() is None:
            Process.terminate()
            try: Process.wait(timeout=8)
            except subprocess.TimeoutExpired: Process.kill(); Process.wait()
        준비살피미.close(); Process.stdout.close()
        (utleverans/'serial.log').write_bytes(avskrift)
        (utleverans/'report.json').write_text(json.dumps(validering_Rapport,indent=2)+'\n')


if __name__=='__main__': Kör()
