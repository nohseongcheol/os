#!/usr/bin/env python3
"""faktisk_data RFB 클라이언트로 QEMU 창의 한글/tast_VÆRDI/클립보드/마우스와 skærmbillede 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from desktop_Visning import EKSAKT_VÆRDI
from Udfør_kommando import To_do_rod


def Kør_2():
    produktoutput=To_do_rod/'build/verification/desktop'; produktoutput.mkdir(parents=True,exist_ok=True)
    Proces=subprocess.Popen(['python3',str(To_do_rod/'Værktøjer/desktop_Visning.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
    afskrift=bytearray(); validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((To_do_rod/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(mærke,Kør_2=0):
        deadline_TID=time.monotonic()+45
        while mærke not in afskrift[Kør_2:]:
            if time.monotonic()>deadline_TID or Proces.poll() is not None: raise AssertionError(afskrift[Kør_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                data=누름값.fileobj.read(4096)
                if data: afskrift.extend(data)
        return bytes(afskrift[Kør_2:])
    try:
        까지(b'TERMINAL READY')
        portnummer=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',afskrift).group(1))
        with socket.create_connection(('127.0.0.1',portnummer),timeout=10) as klient:
            assert EKSAKT_VÆRDI(klient,12)==b'RFB 003.008\n'; klient.sendall(b'RFB 003.008\n')
            assert 1 in EKSAKT_VÆRDI(klient,EKSAKT_VÆRDI(klient,1)[0]); klient.sendall(b'\x01'); assert EKSAKT_VÆRDI(klient,4)==b'\0'*4
            klient.sendall(b'\x01'); 초기값=EKSAKT_VÆRDI(klient,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EKSAKT_VÆRDI(klient,struct.unpack('>I',초기값[20:])[0])
            klient.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klient.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(symbol_VÆRDI,누르는중=True): klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_VÆRDI))
            def 글자입력(Tekst):
                for tegndata in Tekst:
                    symbol=0xff0d if tegndata=='\n' else ord(tegndata) if ord(tegndata)<256 else 0x01000000|ord(tegndata)
                    누름값(symbol); 누름값(symbol,False)
            def 글쇠누르기(symbol_VÆRDI): 누름값(symbol_VÆRDI); 누름값(symbol_VÆRDI,False)
            # Start with English keys only, as delivered without a host IME.
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),FORSKYDNING_VÆRDI)
            # The same composition edits UTF-8 text in the native vi editor.
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',FORSKYDNING_VÆRDI)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),FORSKYDNING_VÆRDI); 까지(b'jkoros-native> ',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('help ko\n')
            까지('한/nul_operand tast_VÆRDI, Shift+Space 또는 F9'.encode(),FORSKYDNING_VÆRDI); 까지(b'jkoros-native> ',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('clear\necho "VNC 한글 input_VÆRDI 😀"\n'); 까지('VNC 한글 input_VÆRDI 😀\r\n'.encode(),FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',FORSKYDNING_VÆRDI)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            udklipsholder_VÆRDI='echo "sætte_ind_VÆRDI 완료"\n'.encode(); FORSKYDNING_VÆRDI=len(afskrift)
            klient.sendall(struct.pack('>B3xI',6,len(udklipsholder_VÆRDI))+udklipsholder_VÆRDI)
            for hændelse,_ in 준비살피미.select(.15):
                datablok=hændelse.fileobj.read(4096)
                if datablok: afskrift.extend(datablok)
            assert 'sætte_ind_VÆRDI 완료'.encode() not in afskrift[FORSKYDNING_VÆRDI:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),FORSKYDNING_VÆRDI)
            klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=EKSAKT_VÆRDI(klient,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Størrelse=struct.unpack('>I',EKSAKT_VÆRDI(klient,7)[3:])[0]; EKSAKT_VÆRDI(klient,Størrelse); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',EKSAKT_VÆRDI(klient,3)[1:])[0]
                for _ in range(사각형들):
                    X_koordinat,Y_koordinat,너비값,높이값,tegnsæt=struct.unpack('>HHHHi',EKSAKT_VÆRDI(klient,12)); assert tegnsæt==0,tegnsæt
                    화소들=EKSAKT_VÆRDI(klient,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; destination_mail=((Y_koordinat+안쪽순번)*640+X_koordinat+순번)*3
                            빛삼원색[destination_mail:destination_mail+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (produktoutput/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(produktoutput/'vnc-terminal.png'))
            FORSKYDNING_VÆRDI=len(afskrift)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); klient.sendall(struct.pack('>BBHH',5,1,576,81)); klient.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',FORSKYDNING_VÆRDI)
            assert len(afskrift)-FORSKYDNING_VÆRDI>8192,'exercise output longer than bridge status buffer'
            FORSKYDNING_VÆRDI=len(afskrift); klient.sendall(struct.pack('>BBHH',5,1,560,63)); klient.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); klient.sendall(struct.pack('>BBHH',5,1,80,16)); klient.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); 글자입력('gui\n'); 까지(b'GUI READY:',FORSKYDNING_VÆRDI)
            FORSKYDNING_VÆRDI=len(afskrift); klient.sendall(struct.pack('>BBHH',5,1,80,332)); klient.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',FORSKYDNING_VÆRDI)
            validering_rapport.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
        준비살피미.close(); Proces.stdout.close()
        (produktoutput/'serial.log').write_bytes(afskrift)
        (produktoutput/'report.json').write_text(json.dumps(validering_rapport,indent=2)+'\n')


if __name__=='__main__': Kør_2()
