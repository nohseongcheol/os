#!/usr/bin/env python3
"""skutočný_údaje RFB 클라이언트로 QEMU 창의 한글/Kľúč_VALUE/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from počítač_zobraziť import EXACT_VALUE
from Vykonať_príkaz import akcia_koreň


def Spustiť_2():
    출력결과=akcia_koreň/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Proces=subprocess.Popen(['python3',str(akcia_koreň/'Nástroje/počítač_zobraziť.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
    prepis=bytearray(); overenie_správa={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akcia_koreň/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(fixka,Spustiť_2=0):
        termín_čas=time.monotonic()+45
        while fixka not in prepis[Spustiť_2:]:
            if time.monotonic()>termín_čas or Proces.poll() is not None: raise AssertionError(prepis[Spustiť_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                údaje=누름값.fileobj.read(4096)
                if údaje: prepis.extend(údaje)
        return bytes(prepis[Spustiť_2:])
    try:
        까지(b'TERMINAL READY')
        číslo_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',prepis).group(1))
        with socket.create_connection(('127.0.0.1',číslo_portu),timeout=10) as klient:
            assert EXACT_VALUE(klient,12)==b'RFB 003.008\n'; klient.sendall(b'RFB 003.008\n')
            assert 1 in EXACT_VALUE(klient,EXACT_VALUE(klient,1)[0]); klient.sendall(b'\x01'); assert EXACT_VALUE(klient,4)==b'\0'*4
            klient.sendall(b'\x01'); 초기값=EXACT_VALUE(klient,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACT_VALUE(klient,struct.unpack('>I',초기값[20:])[0])
            klient.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klient.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(symbol_VALUE,누르는중=True): klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_VALUE))
            def 글자입력(Spracovanie_textu):
                for znakové_údaje in Spracovanie_textu:
                    symbol=0xff0d if znakové_údaje=='\n' else ord(znakové_údaje) if ord(znakové_údaje)<256 else 0x01000000|ord(znakové_údaje)
                    누름값(symbol); 누름값(symbol,False)
            def 글쇠누르기(symbol_VALUE): 누름값(symbol_VALUE); 누름값(symbol_VALUE,False)
            # Start with English keys only, as delivered without a host IME.
            Posun_VALUE=len(prepis); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Posun_VALUE)
            # The same composition edits UTF-8 text in the native vi editor.
            Posun_VALUE=len(prepis); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Posun_VALUE)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Posun_VALUE); 까지(b'jkoros-native> ',Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('help ko\n')
            까지('한/영 Kľúč_VALUE, Shift+Space 또는 F9'.encode(),Posun_VALUE); 까지(b'jkoros-native> ',Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('clear\necho "VNC 한글 vstup_VALUE 😀"\n'); 까지('VNC 한글 vstup_VALUE 😀\r\n'.encode(),Posun_VALUE)
            Posun_VALUE=len(prepis); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Posun_VALUE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            Schránka_VALUE='echo "prilepiť_VALUE 완료"\n'.encode(); Posun_VALUE=len(prepis)
            klient.sendall(struct.pack('>B3xI',6,len(Schránka_VALUE))+Schránka_VALUE)
            for Udalosť,_ in 준비살피미.select(.15):
                blok_údajov=Udalosť.fileobj.read(4096)
                if blok_údajov: prepis.extend(blok_údajov)
            assert 'prilepiť_VALUE 완료'.encode() not in prepis[Posun_VALUE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Posun_VALUE)
            klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                upozornenie_SMS=EXACT_VALUE(klient,1)[0]
                if upozornenie_SMS==2: continue
                if upozornenie_SMS==3:
                    Veľkosť=struct.unpack('>I',EXACT_VALUE(klient,7)[3:])[0]; EXACT_VALUE(klient,Veľkosť); continue
                assert upozornenie_SMS==0,upozornenie_SMS
                사각형들=struct.unpack('>H',EXACT_VALUE(klient,3)[1:])[0]
                for _ in range(사각형들):
                    X_súradnica,Y_súradnica,너비값,높이값,tabuľka_znakov=struct.unpack('>HHHHi',EXACT_VALUE(klient,12)); assert tabuľka_znakov==0,tabuľka_znakov
                    화소들=EXACT_VALUE(klient,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; cieľ_adresa_08bbd577=((Y_súradnica+안쪽순번)*640+X_súradnica+순번)*3
                            빛삼원색[cieľ_adresa_08bbd577:cieľ_adresa_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            Posun_VALUE=len(prepis)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Posun_VALUE)
            Posun_VALUE=len(prepis); klient.sendall(struct.pack('>BBHH',5,1,576,81)); klient.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Posun_VALUE)
            assert len(prepis)-Posun_VALUE>8192,'exercise output longer than bridge status buffer'
            Posun_VALUE=len(prepis); klient.sendall(struct.pack('>BBHH',5,1,560,63)); klient.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Posun_VALUE)
            Posun_VALUE=len(prepis); klient.sendall(struct.pack('>BBHH',5,1,80,16)); klient.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Posun_VALUE)
            Posun_VALUE=len(prepis); 글자입력('gui\n'); 까지(b'GUI READY:',Posun_VALUE)
            Posun_VALUE=len(prepis); klient.sendall(struct.pack('>BBHH',5,1,80,332)); klient.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Posun_VALUE)
            overenie_správa.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
        준비살피미.close(); Proces.stdout.close()
        (출력결과/'serial.log').write_bytes(prepis)
        (출력결과/'report.json').write_text(json.dumps(overenie_správa,indent=2)+'\n')


if __name__=='__main__': Spustiť_2()
