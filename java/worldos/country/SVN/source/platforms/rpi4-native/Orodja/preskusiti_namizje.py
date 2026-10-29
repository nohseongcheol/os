#!/usr/bin/env python3
"""dejanski_podatki RFB 클라이언트로 QEMU 창의 한글/Ključ_VALUE/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from namizje_Pogled import EXACT_VALUE
from Izvedi_ukaz import pobuda_koren


def Zaženi():
    출력결과=pobuda_koren/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Opravilo=subprocess.Popen(['python3',str(pobuda_koren/'Orodja/namizje_Pogled.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Opravilo.stdout,selectors.EVENT_READ)
    prepis=bytearray(); preverjanje_veljavnosti_prijavi={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((pobuda_koren/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(oznaka,Zaženi=0):
        rok_čas=time.monotonic()+45
        while oznaka not in prepis[Zaženi:]:
            if time.monotonic()>rok_čas or Opravilo.poll() is not None: raise AssertionError(prepis[Zaženi:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                podatki=누름값.fileobj.read(4096)
                if podatki: prepis.extend(podatki)
        return bytes(prepis[Zaženi:])
    try:
        까지(b'TERMINAL READY')
        številka_vrat=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',prepis).group(1))
        with socket.create_connection(('127.0.0.1',številka_vrat),timeout=10) as odjemalec:
            assert EXACT_VALUE(odjemalec,12)==b'RFB 003.008\n'; odjemalec.sendall(b'RFB 003.008\n')
            assert 1 in EXACT_VALUE(odjemalec,EXACT_VALUE(odjemalec,1)[0]); odjemalec.sendall(b'\x01'); assert EXACT_VALUE(odjemalec,4)==b'\0'*4
            odjemalec.sendall(b'\x01'); 초기값=EXACT_VALUE(odjemalec,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACT_VALUE(odjemalec,struct.unpack('>I',초기값[20:])[0])
            odjemalec.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            odjemalec.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(simbol_VALUE,누르는중=True): odjemalec.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbol_VALUE))
            def 글자입력(Besedilo):
                for znakovni_podatki in Besedilo:
                    simbol=0xff0d if znakovni_podatki=='\n' else ord(znakovni_podatki) if ord(znakovni_podatki)<256 else 0x01000000|ord(znakovni_podatki)
                    누름값(simbol); 누름값(simbol,False)
            def pritisniti_Ključ(simbol_VALUE): 누름값(simbol_VALUE); 누름값(simbol_VALUE,False)
            # Start with English keys only, as delivered without a host IME.
            odmik_VALUE=len(prepis); 글자입력('echo '); pritisniti_Ključ(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); pritisniti_Ključ(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('echo ')
            누름값(0xffe1); pritisniti_Ključ(32); 누름값(0xffe1,False)
            글자입력('dlfr'); pritisniti_Ključ(0xff08); pritisniti_Ključ(0xff08); 글자입력('fr')
            pritisniti_Ključ(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('echo '); pritisniti_Ključ(0xff31)
            글자입력('rhk rkqtk RkRnd'); pritisniti_Ključ(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),odmik_VALUE)
            # The same composition edits UTF-8 text in the native vi editor.
            odmik_VALUE=len(prepis); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',odmik_VALUE)
            글자입력('i'); pritisniti_Ključ(0xffc6); 글자입력('gksrmf dlfr'); pritisniti_Ključ(0xffc6)
            pritisniti_Ključ(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),odmik_VALUE); 까지(b'jkoros-native> ',odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('help ko\n')
            까지('한/nič_operand Ključ_VALUE, Shift+Space 또는 F9'.encode(),odmik_VALUE); 까지(b'jkoros-native> ',odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),odmik_VALUE)
            odmik_VALUE=len(prepis); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',odmik_VALUE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            odložišče_VALUE='echo "prilepiti_VALUE 완료"\n'.encode(); odmik_VALUE=len(prepis)
            odjemalec.sendall(struct.pack('>B3xI',6,len(odložišče_VALUE))+odložišče_VALUE)
            for dogodek,_ in 준비살피미.select(.15):
                blok_podatkov=dogodek.fileobj.read(4096)
                if blok_podatkov: prepis.extend(blok_podatkov)
            assert 'prilepiti_VALUE 완료'.encode() not in prepis[odmik_VALUE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),odmik_VALUE)
            odjemalec.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                obvestilo_SMS=EXACT_VALUE(odjemalec,1)[0]
                if obvestilo_SMS==2: continue
                if obvestilo_SMS==3:
                    Velikost=struct.unpack('>I',EXACT_VALUE(odjemalec,7)[3:])[0]; EXACT_VALUE(odjemalec,Velikost); continue
                assert obvestilo_SMS==0,obvestilo_SMS
                사각형들=struct.unpack('>H',EXACT_VALUE(odjemalec,3)[1:])[0]
                for _ in range(사각형들):
                    koordinata_x,세로좌표,너비값,높이값,nabor_znakov=struct.unpack('>HHHHi',EXACT_VALUE(odjemalec,12)); assert nabor_znakov==0,nabor_znakov
                    화소들=EXACT_VALUE(odjemalec,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; cilj_naslov_08bbd577=((세로좌표+안쪽순번)*640+koordinata_x+순번)*3
                            빛삼원색[cilj_naslov_08bbd577:cilj_naslov_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            odmik_VALUE=len(prepis)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',odmik_VALUE)
            odmik_VALUE=len(prepis); odjemalec.sendall(struct.pack('>BBHH',5,1,576,81)); odjemalec.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',odmik_VALUE)
            assert len(prepis)-odmik_VALUE>8192,'exercise output longer than bridge status buffer'
            odmik_VALUE=len(prepis); odjemalec.sendall(struct.pack('>BBHH',5,1,560,63)); odjemalec.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',odmik_VALUE)
            odmik_VALUE=len(prepis); odjemalec.sendall(struct.pack('>BBHH',5,1,80,16)); odjemalec.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',odmik_VALUE)
            odmik_VALUE=len(prepis); 글자입력('gui\n'); 까지(b'GUI READY:',odmik_VALUE)
            odmik_VALUE=len(prepis); odjemalec.sendall(struct.pack('>BBHH',5,1,80,332)); odjemalec.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',odmik_VALUE)
            preverjanje_veljavnosti_prijavi.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Opravilo.poll() is None:
            Opravilo.terminate()
            try: Opravilo.wait(timeout=8)
            except subprocess.TimeoutExpired: Opravilo.kill(); Opravilo.wait()
        준비살피미.close(); Opravilo.stdout.close()
        (출력결과/'serial.log').write_bytes(prepis)
        (출력결과/'report.json').write_text(json.dumps(preverjanje_veljavnosti_prijavi,indent=2)+'\n')


if __name__=='__main__': Zaženi()
