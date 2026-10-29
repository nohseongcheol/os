#!/usr/bin/env python3
"""faktinis_duomenys RFB 클라이언트로 QEMU 창의 한글/Raktas_VALUE/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from darbalaukis_rodyti import EXACT_VALUE
from Vykdyti_komanda import Project_šaknis


def Paleisti():
    išeiga=Project_šaknis/'build/verification/desktop'; išeiga.mkdir(parents=True,exist_ok=True)
    Procesas=subprocess.Popen(['python3',str(Project_šaknis/'Įrankiai/darbalaukis_rodyti.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Procesas.stdout,selectors.EVENT_READ)
    transkribavimas=bytearray(); tikrinimas_pranešti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(žymeklis,Paleisti=0):
        terminas_TIME=time.monotonic()+45
        while žymeklis not in transkribavimas[Paleisti:]:
            if time.monotonic()>terminas_TIME or Procesas.poll() is not None: raise AssertionError(transkribavimas[Paleisti:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                duomenys=누름값.fileobj.read(4096)
                if duomenys: transkribavimas.extend(duomenys)
        return bytes(transkribavimas[Paleisti:])
    try:
        까지(b'TERMINAL READY')
        prievado_numeris=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkribavimas).group(1))
        with socket.create_connection(('127.0.0.1',prievado_numeris),timeout=10) as klientas:
            assert EXACT_VALUE(klientas,12)==b'RFB 003.008\n'; klientas.sendall(b'RFB 003.008\n')
            assert 1 in EXACT_VALUE(klientas,EXACT_VALUE(klientas,1)[0]); klientas.sendall(b'\x01'); assert EXACT_VALUE(klientas,4)==b'\0'*4
            klientas.sendall(b'\x01'); 초기값=EXACT_VALUE(klientas,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACT_VALUE(klientas,struct.unpack('>I',초기값[20:])[0])
            klientas.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klientas.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(simbolis_VALUE,누르는중=True): klientas.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbolis_VALUE))
            def 글자입력(Tekstas):
                for simbolių_duomenys in Tekstas:
                    simbolis=0xff0d if simbolių_duomenys=='\n' else ord(simbolių_duomenys) if ord(simbolių_duomenys)<256 else 0x01000000|ord(simbolių_duomenys)
                    누름값(simbolis); 누름값(simbolis,False)
            def paspausti_Raktas(simbolis_VALUE): 누름값(simbolis_VALUE); 누름값(simbolis_VALUE,False)
            # Start with English keys only, as delivered without a host IME.
            OFFSET_VALUE=len(transkribavimas); 글자입력('echo '); paspausti_Raktas(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); paspausti_Raktas(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('echo ')
            누름값(0xffe1); paspausti_Raktas(32); 누름값(0xffe1,False)
            글자입력('dlfr'); paspausti_Raktas(0xff08); paspausti_Raktas(0xff08); 글자입력('fr')
            paspausti_Raktas(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('echo '); paspausti_Raktas(0xff31)
            글자입력('rhk rkqtk RkRnd'); paspausti_Raktas(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),OFFSET_VALUE)
            # The same composition edits UTF-8 text in the native vi editor.
            OFFSET_VALUE=len(transkribavimas); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',OFFSET_VALUE)
            글자입력('i'); paspausti_Raktas(0xffc6); 글자입력('gksrmf dlfr'); paspausti_Raktas(0xffc6)
            paspausti_Raktas(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),OFFSET_VALUE); 까지(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('help ko\n')
            까지('한/nulis_operandas Raktas_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE); 까지(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',OFFSET_VALUE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            mainų_sritis_VALUE='echo "Įklijuoti_VALUE 완료"\n'.encode(); OFFSET_VALUE=len(transkribavimas)
            klientas.sendall(struct.pack('>B3xI',6,len(mainų_sritis_VALUE))+mainų_sritis_VALUE)
            for Įvykis,_ in 준비살피미.select(.15):
                duomenų_blokas=Įvykis.fileobj.read(4096)
                if duomenų_blokas: transkribavimas.extend(duomenų_blokas)
            assert 'Įklijuoti_VALUE 완료'.encode() not in transkribavimas[OFFSET_VALUE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),OFFSET_VALUE)
            klientas.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                pranešimas_SMS=EXACT_VALUE(klientas,1)[0]
                if pranešimas_SMS==2: continue
                if pranešimas_SMS==3:
                    Dydis=struct.unpack('>I',EXACT_VALUE(klientas,7)[3:])[0]; EXACT_VALUE(klientas,Dydis); continue
                assert pranešimas_SMS==0,pranešimas_SMS
                사각형들=struct.unpack('>H',EXACT_VALUE(klientas,3)[1:])[0]
                for _ in range(사각형들):
                    x_koordinatė,세로좌표,너비값,높이값,simbolių_rinkinys=struct.unpack('>HHHHi',EXACT_VALUE(klientas,12)); assert simbolių_rinkinys==0,simbolių_rinkinys
                    화소들=EXACT_VALUE(klientas,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; vieta_ADDRESS=((세로좌표+안쪽순번)*640+x_koordinatė+순번)*3
                            빛삼원색[vieta_ADDRESS:vieta_ADDRESS+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (išeiga/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(išeiga/'vnc-terminal.png'))
            OFFSET_VALUE=len(transkribavimas)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); klientas.sendall(struct.pack('>BBHH',5,1,576,81)); klientas.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',OFFSET_VALUE)
            assert len(transkribavimas)-OFFSET_VALUE>8192,'exercise output longer than bridge status buffer'
            OFFSET_VALUE=len(transkribavimas); klientas.sendall(struct.pack('>BBHH',5,1,560,63)); klientas.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); klientas.sendall(struct.pack('>BBHH',5,1,80,16)); klientas.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); 글자입력('gui\n'); 까지(b'GUI READY:',OFFSET_VALUE)
            OFFSET_VALUE=len(transkribavimas); klientas.sendall(struct.pack('>BBHH',5,1,80,332)); klientas.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',OFFSET_VALUE)
            tikrinimas_pranešti.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Procesas.poll() is None:
            Procesas.terminate()
            try: Procesas.wait(timeout=8)
            except subprocess.TimeoutExpired: Procesas.kill(); Procesas.wait()
        준비살피미.close(); Procesas.stdout.close()
        (išeiga/'serial.log').write_bytes(transkribavimas)
        (išeiga/'report.json').write_text(json.dumps(tikrinimas_pranešti,indent=2)+'\n')


if __name__=='__main__': Paleisti()
