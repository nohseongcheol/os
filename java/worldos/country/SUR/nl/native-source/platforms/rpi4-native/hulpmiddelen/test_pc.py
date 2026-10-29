#!/usr/bin/env python3
"""werkelijk_gegevens RFB 클라이언트로 QEMU 창의 한글/toets_WAARDE/클립보드/마우스와 scherm 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from pc_Weergave import GELIJK_WAARDE
from Uitvoeren_opdracht import Taken_wortel


def starten():
    uitvoer=Taken_wortel/'build/verification/desktop'; uitvoer.mkdir(parents=True,exist_ok=True)
    Proces=subprocess.Popen(['python3',str(Taken_wortel/'hulpmiddelen/pc_Weergave.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
    transcriptie=bytearray(); validatie_Rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Taken_wortel/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(markering,starten=0):
        deadline_TIJD=time.monotonic()+45
        while markering not in transcriptie[starten:]:
            if time.monotonic()>deadline_TIJD or Proces.poll() is not None: raise AssertionError(transcriptie[starten:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                gegevens=누름값.fileobj.read(4096)
                if gegevens: transcriptie.extend(gegevens)
        return bytes(transcriptie[starten:])
    try:
        까지(b'TERMINAL READY')
        poortnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcriptie).group(1))
        with socket.create_connection(('127.0.0.1',poortnummer),timeout=10) as client:
            assert GELIJK_WAARDE(client,12)==b'RFB 003.008\n'; client.sendall(b'RFB 003.008\n')
            assert 1 in GELIJK_WAARDE(client,GELIJK_WAARDE(client,1)[0]); client.sendall(b'\x01'); assert GELIJK_WAARDE(client,4)==b'\0'*4
            client.sendall(b'\x01'); 초기값=GELIJK_WAARDE(client,24); assert struct.unpack('>HH',초기값[:4])==(640,480); GELIJK_WAARDE(client,struct.unpack('>I',초기값[20:])[0])
            client.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            client.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(symbool_WAARDE,누르는중=True): client.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbool_WAARDE))
            def 글자입력(tekst):
                for tekengegevens in tekst:
                    symbool=0xff0d if tekengegevens=='\n' else ord(tekengegevens) if ord(tekengegevens)<256 else 0x01000000|ord(tekengegevens)
                    누름값(symbool); 누름값(symbool,False)
            def 글쇠누르기(symbool_WAARDE): 누름값(symbool_WAARDE); 누름값(symbool_WAARDE,False)
            # Start with English keys only, as delivered without a host IME.
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),VERSCHUIVING_WAARDE)
            # The same composition edits UTF-8 text in the native vi editor.
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',VERSCHUIVING_WAARDE)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),VERSCHUIVING_WAARDE); 까지(b'jkoros-native> ',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('help ko\n')
            까지('한/nul_operand toets_WAARDE, Shift+Space 또는 F9'.encode(),VERSCHUIVING_WAARDE); 까지(b'jkoros-native> ',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('clear\necho "VNC 한글 invoer_WAARDE 😀"\n'); 까지('VNC 한글 invoer_WAARDE 😀\r\n'.encode(),VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',VERSCHUIVING_WAARDE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            klembord_WAARDE='echo "plakken_WAARDE 완료"\n'.encode(); VERSCHUIVING_WAARDE=len(transcriptie)
            client.sendall(struct.pack('>B3xI',6,len(klembord_WAARDE))+klembord_WAARDE)
            for Gebeurtenis,_ in 준비살피미.select(.15):
                gegevensblok=Gebeurtenis.fileobj.read(4096)
                if gegevensblok: transcriptie.extend(gegevensblok)
            assert 'plakken_WAARDE 완료'.encode() not in transcriptie[VERSCHUIVING_WAARDE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),VERSCHUIVING_WAARDE)
            client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                kennisgeving_sms=GELIJK_WAARDE(client,1)[0]
                if kennisgeving_sms==2: continue
                if kennisgeving_sms==3:
                    Grootte=struct.unpack('>I',GELIJK_WAARDE(client,7)[3:])[0]; GELIJK_WAARDE(client,Grootte); continue
                assert kennisgeving_sms==0,kennisgeving_sms
                사각형들=struct.unpack('>H',GELIJK_WAARDE(client,3)[1:])[0]
                for _ in range(사각형들):
                    x_coördinaat,Y_coördinaat,너비값,aangevraagd_hoogte_WAARDE,tekenset=struct.unpack('>HHHHi',GELIJK_WAARDE(client,12)); assert tekenset==0,tekenset
                    화소들=GELIJK_WAARDE(client,너비값*aangevraagd_hoogte_WAARDE*4)
                    for 안쪽순번 in range(aangevraagd_hoogte_WAARDE):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; doel_ADRES_08bbd577=((Y_coördinaat+안쪽순번)*640+x_coördinaat+순번)*3
                            빛삼원색[doel_ADRES_08bbd577:doel_ADRES_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (uitvoer/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(uitvoer/'vnc-terminal.png'))
            VERSCHUIVING_WAARDE=len(transcriptie)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); client.sendall(struct.pack('>BBHH',5,1,576,81)); client.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',VERSCHUIVING_WAARDE)
            assert len(transcriptie)-VERSCHUIVING_WAARDE>8192,'exercise output longer than bridge status buffer'
            VERSCHUIVING_WAARDE=len(transcriptie); client.sendall(struct.pack('>BBHH',5,1,560,63)); client.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); client.sendall(struct.pack('>BBHH',5,1,80,16)); client.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); 글자입력('gui\n'); 까지(b'GUI READY:',VERSCHUIVING_WAARDE)
            VERSCHUIVING_WAARDE=len(transcriptie); client.sendall(struct.pack('>BBHH',5,1,80,332)); client.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',VERSCHUIVING_WAARDE)
            validatie_Rapport.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
        준비살피미.close(); Proces.stdout.close()
        (uitvoer/'serial.log').write_bytes(transcriptie)
        (uitvoer/'report.json').write_text(json.dumps(validatie_Rapport,indent=2)+'\n')


if __name__=='__main__': starten()
