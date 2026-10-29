#!/usr/bin/env python3
"""tényleges_adat RFB 클라이언트로 QEMU 창의 한글/Kulcs_ÉRTÉK/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from Asztal_Nézet import AZONOS_ÉRTÉK
from végrehajt_parancs import teendő_gyök


def Futtatás():
    kimenet=teendő_gyök/'build/verification/desktop'; kimenet.mkdir(parents=True,exist_ok=True)
    Folyamat=subprocess.Popen(['python3',str(teendő_gyök/'Eszközök/Asztal_Nézet.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Folyamat.stdout,selectors.EVENT_READ)
    átirat=bytearray(); ellenőrzés_jelent={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((teendő_gyök/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(jelölő,Futtatás=0):
        határidő_IDŐ=time.monotonic()+45
        while jelölő not in átirat[Futtatás:]:
            if time.monotonic()>határidő_IDŐ or Folyamat.poll() is not None: raise AssertionError(átirat[Futtatás:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                adat=누름값.fileobj.read(4096)
                if adat: átirat.extend(adat)
        return bytes(átirat[Futtatás:])
    try:
        까지(b'TERMINAL READY')
        portszám=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',átirat).group(1))
        with socket.create_connection(('127.0.0.1',portszám),timeout=10) as kliens:
            assert AZONOS_ÉRTÉK(kliens,12)==b'RFB 003.008\n'; kliens.sendall(b'RFB 003.008\n')
            assert 1 in AZONOS_ÉRTÉK(kliens,AZONOS_ÉRTÉK(kliens,1)[0]); kliens.sendall(b'\x01'); assert AZONOS_ÉRTÉK(kliens,4)==b'\0'*4
            kliens.sendall(b'\x01'); 초기값=AZONOS_ÉRTÉK(kliens,24); assert struct.unpack('>HH',초기값[:4])==(640,480); AZONOS_ÉRTÉK(kliens,struct.unpack('>I',초기값[20:])[0])
            kliens.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            kliens.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(szimbólum_ÉRTÉK,누르는중=True): kliens.sendall(struct.pack('>BBHI',4,int(누르는중),0,szimbólum_ÉRTÉK))
            def 글자입력(Szöveg):
                for karakteres_adat in Szöveg:
                    szimbólum=0xff0d if karakteres_adat=='\n' else ord(karakteres_adat) if ord(karakteres_adat)<256 else 0x01000000|ord(karakteres_adat)
                    누름값(szimbólum); 누름값(szimbólum,False)
            def 글쇠누르기(szimbólum_ÉRTÉK): 누름값(szimbólum_ÉRTÉK); 누름값(szimbólum_ÉRTÉK,False)
            # Start with English keys only, as delivered without a host IME.
            Ofszet_ÉRTÉK=len(átirat); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Ofszet_ÉRTÉK)
            # The same composition edits UTF-8 text in the native vi editor.
            Ofszet_ÉRTÉK=len(átirat); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Ofszet_ÉRTÉK)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Ofszet_ÉRTÉK); 까지(b'jkoros-native> ',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('help ko\n')
            까지('한/nulla_operandus Kulcs_ÉRTÉK, Shift+Space 또는 F9'.encode(),Ofszet_ÉRTÉK); 까지(b'jkoros-native> ',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('clear\necho "VNC 한글 bevitel_ÉRTÉK 😀"\n'); 까지('VNC 한글 bevitel_ÉRTÉK 😀\r\n'.encode(),Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Ofszet_ÉRTÉK)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            vágólap_ÉRTÉK='echo "beilleszt_ÉRTÉK 완료"\n'.encode(); Ofszet_ÉRTÉK=len(átirat)
            kliens.sendall(struct.pack('>B3xI',6,len(vágólap_ÉRTÉK))+vágólap_ÉRTÉK)
            for Esemény,_ in 준비살피미.select(.15):
                adatblokk=Esemény.fileobj.read(4096)
                if adatblokk: átirat.extend(adatblokk)
            assert 'beilleszt_ÉRTÉK 완료'.encode() not in átirat[Ofszet_ÉRTÉK:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Ofszet_ÉRTÉK)
            kliens.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                alapelv_SMS=AZONOS_ÉRTÉK(kliens,1)[0]
                if alapelv_SMS==2: continue
                if alapelv_SMS==3:
                    Méret=struct.unpack('>I',AZONOS_ÉRTÉK(kliens,7)[3:])[0]; AZONOS_ÉRTÉK(kliens,Méret); continue
                assert alapelv_SMS==0,alapelv_SMS
                사각형들=struct.unpack('>H',AZONOS_ÉRTÉK(kliens,3)[1:])[0]
                for _ in range(사각형들):
                    x_koordináta,Y_koordináta,너비값,높이값,karakterkészlet=struct.unpack('>HHHHi',AZONOS_ÉRTÉK(kliens,12)); assert karakterkészlet==0,karakterkészlet
                    화소들=AZONOS_ÉRTÉK(kliens,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; cél_CÍM_08bbd577=((Y_koordináta+안쪽순번)*640+x_koordináta+순번)*3
                            빛삼원색[cél_CÍM_08bbd577:cél_CÍM_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (kimenet/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(kimenet/'vnc-terminal.png'))
            Ofszet_ÉRTÉK=len(átirat)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); kliens.sendall(struct.pack('>BBHH',5,1,576,81)); kliens.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Ofszet_ÉRTÉK)
            assert len(átirat)-Ofszet_ÉRTÉK>8192,'exercise output longer than bridge status buffer'
            Ofszet_ÉRTÉK=len(átirat); kliens.sendall(struct.pack('>BBHH',5,1,560,63)); kliens.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); kliens.sendall(struct.pack('>BBHH',5,1,80,16)); kliens.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); 글자입력('gui\n'); 까지(b'GUI READY:',Ofszet_ÉRTÉK)
            Ofszet_ÉRTÉK=len(átirat); kliens.sendall(struct.pack('>BBHH',5,1,80,332)); kliens.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Ofszet_ÉRTÉK)
            ellenőrzés_jelent.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Folyamat.poll() is None:
            Folyamat.terminate()
            try: Folyamat.wait(timeout=8)
            except subprocess.TimeoutExpired: Folyamat.kill(); Folyamat.wait()
        준비살피미.close(); Folyamat.stdout.close()
        (kimenet/'serial.log').write_bytes(átirat)
        (kimenet/'report.json').write_text(json.dumps(ellenőrzés_jelent,indent=2)+'\n')


if __name__=='__main__': Futtatás()
