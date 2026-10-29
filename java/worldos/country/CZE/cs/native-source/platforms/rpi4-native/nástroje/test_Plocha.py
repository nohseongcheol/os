#!/usr/bin/env python3
"""skutečný_data RFB 클라이언트로 QEMU 창의 한글/Klíč_HODNOTA/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from Plocha_pohled import STEJNÉ_HODNOTA
from Provést_příkaz import akce_kořen


def Spustit_2():
    výstup=akce_kořen/'build/verification/desktop'; výstup.mkdir(parents=True,exist_ok=True)
    Proces=subprocess.Popen(['python3',str(akce_kořen/'nástroje/Plocha_pohled.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proces.stdout,selectors.EVENT_READ)
    přepis=bytearray(); ověření_Zpráva={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((akce_kořen/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(značka,Spustit_2=0):
        konečný_termín_ČAS=time.monotonic()+45
        while značka not in přepis[Spustit_2:]:
            if time.monotonic()>konečný_termín_ČAS or Proces.poll() is not None: raise AssertionError(přepis[Spustit_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                data=누름값.fileobj.read(4096)
                if data: přepis.extend(data)
        return bytes(přepis[Spustit_2:])
    try:
        까지(b'TERMINAL READY')
        číslo_portu=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',přepis).group(1))
        with socket.create_connection(('127.0.0.1',číslo_portu),timeout=10) as klient:
            assert STEJNÉ_HODNOTA(klient,12)==b'RFB 003.008\n'; klient.sendall(b'RFB 003.008\n')
            assert 1 in STEJNÉ_HODNOTA(klient,STEJNÉ_HODNOTA(klient,1)[0]); klient.sendall(b'\x01'); assert STEJNÉ_HODNOTA(klient,4)==b'\0'*4
            klient.sendall(b'\x01'); 초기값=STEJNÉ_HODNOTA(klient,24); assert struct.unpack('>HH',초기값[:4])==(640,480); STEJNÉ_HODNOTA(klient,struct.unpack('>I',초기값[20:])[0])
            klient.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klient.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(symbol_HODNOTA,누르는중=True): klient.sendall(struct.pack('>BBHI',4,int(누르는중),0,symbol_HODNOTA))
            def 글자입력(text):
                for textová_data in text:
                    symbol=0xff0d if textová_data=='\n' else ord(textová_data) if ord(textová_data)<256 else 0x01000000|ord(textová_data)
                    누름값(symbol); 누름값(symbol,False)
            def 글쇠누르기(symbol_HODNOTA): 누름값(symbol_HODNOTA); 누름값(symbol_HODNOTA,False)
            # Start with English keys only, as delivered without a host IME.
            POSUN_HODNOTA=len(přepis); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),POSUN_HODNOTA)
            # The same composition edits UTF-8 text in the native vi editor.
            POSUN_HODNOTA=len(přepis); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',POSUN_HODNOTA)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),POSUN_HODNOTA); 까지(b'jkoros-native> ',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('help ko\n')
            까지('한/nula_operand Klíč_HODNOTA, Shift+Space 또는 F9'.encode(),POSUN_HODNOTA); 까지(b'jkoros-native> ',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('clear\necho "VNC 한글 vstup_HODNOTA 😀"\n'); 까지('VNC 한글 vstup_HODNOTA 😀\r\n'.encode(),POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',POSUN_HODNOTA)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            schránka_HODNOTA='echo "vložit_HODNOTA 완료"\n'.encode(); POSUN_HODNOTA=len(přepis)
            klient.sendall(struct.pack('>B3xI',6,len(schránka_HODNOTA))+schránka_HODNOTA)
            for Události,_ in 준비살피미.select(.15):
                datový_blok=Události.fileobj.read(4096)
                if datový_blok: přepis.extend(datový_blok)
            assert 'vložit_HODNOTA 완료'.encode() not in přepis[POSUN_HODNOTA:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),POSUN_HODNOTA)
            klient.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                povinnost_zvěřejnit_SMS=STEJNÉ_HODNOTA(klient,1)[0]
                if povinnost_zvěřejnit_SMS==2: continue
                if povinnost_zvěřejnit_SMS==3:
                    Velikost=struct.unpack('>I',STEJNÉ_HODNOTA(klient,7)[3:])[0]; STEJNÉ_HODNOTA(klient,Velikost); continue
                assert povinnost_zvěřejnit_SMS==0,povinnost_zvěřejnit_SMS
                사각형들=struct.unpack('>H',STEJNÉ_HODNOTA(klient,3)[1:])[0]
                for _ in range(사각형들):
                    souřadnice_x,Y_souřadnice,너비값,vyžádáno_výška_HODNOTA,znaková_sada=struct.unpack('>HHHHi',STEJNÉ_HODNOTA(klient,12)); assert znaková_sada==0,znaková_sada
                    화소들=STEJNÉ_HODNOTA(klient,너비값*vyžádáno_výška_HODNOTA*4)
                    for 안쪽순번 in range(vyžádáno_výška_HODNOTA):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; cíl_ODKAZ_08bbd577=((Y_souřadnice+안쪽순번)*640+souřadnice_x+순번)*3
                            빛삼원색[cíl_ODKAZ_08bbd577:cíl_ODKAZ_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (výstup/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(výstup/'vnc-terminal.png'))
            POSUN_HODNOTA=len(přepis)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); klient.sendall(struct.pack('>BBHH',5,1,576,81)); klient.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',POSUN_HODNOTA)
            assert len(přepis)-POSUN_HODNOTA>8192,'exercise output longer than bridge status buffer'
            POSUN_HODNOTA=len(přepis); klient.sendall(struct.pack('>BBHH',5,1,560,63)); klient.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); klient.sendall(struct.pack('>BBHH',5,1,80,16)); klient.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); 글자입력('gui\n'); 까지(b'GUI READY:',POSUN_HODNOTA)
            POSUN_HODNOTA=len(přepis); klient.sendall(struct.pack('>BBHH',5,1,80,332)); klient.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',POSUN_HODNOTA)
            ověření_Zpráva.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Proces.poll() is None:
            Proces.terminate()
            try: Proces.wait(timeout=8)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
        준비살피미.close(); Proces.stdout.close()
        (výstup/'serial.log').write_bytes(přepis)
        (výstup/'report.json').write_text(json.dumps(ověření_Zpráva,indent=2)+'\n')


if __name__=='__main__': Spustit_2()
