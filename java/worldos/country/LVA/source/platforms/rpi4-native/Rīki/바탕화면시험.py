#!/usr/bin/env python3
"""faktisks_dati RFB 클라이언트로 QEMU 창의 한글/Atslēga_VALUE/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from dators_Skats import EXACT_VALUE
from Izpildīt_komanda import Project_sakne


def Palaist():
    ražojums=Project_sakne/'build/verification/desktop'; ražojums.mkdir(parents=True,exist_ok=True)
    Process=subprocess.Popen(['python3',str(Project_sakne/'Rīki/dators_Skats.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Process.stdout,selectors.EVENT_READ)
    transkripcija=bytearray(); validācija_ziņot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_sakne/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(marķieris,Palaist=0):
        izpildes_termiņš_TIME=time.monotonic()+45
        while marķieris not in transkripcija[Palaist:]:
            if time.monotonic()>izpildes_termiņš_TIME or Process.poll() is not None: raise AssertionError(transkripcija[Palaist:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                dati=누름값.fileobj.read(4096)
                if dati: transkripcija.extend(dati)
        return bytes(transkripcija[Palaist:])
    try:
        까지(b'TERMINAL READY')
        porta_numurs=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transkripcija).group(1))
        with socket.create_connection(('127.0.0.1',porta_numurs),timeout=10) as klients:
            assert EXACT_VALUE(klients,12)==b'RFB 003.008\n'; klients.sendall(b'RFB 003.008\n')
            assert 1 in EXACT_VALUE(klients,EXACT_VALUE(klients,1)[0]); klients.sendall(b'\x01'); assert EXACT_VALUE(klients,4)==b'\0'*4
            klients.sendall(b'\x01'); 초기값=EXACT_VALUE(klients,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACT_VALUE(klients,struct.unpack('>I',초기값[20:])[0])
            klients.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            klients.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(simbols_VALUE,누르는중=True): klients.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbols_VALUE))
            def 글자입력(Teksts):
                for rakstzīmju_dati in Teksts:
                    simbols=0xff0d if rakstzīmju_dati=='\n' else ord(rakstzīmju_dati) if ord(rakstzīmju_dati)<256 else 0x01000000|ord(rakstzīmju_dati)
                    누름값(simbols); 누름값(simbols,False)
            def nospiest_Atslēga(simbols_VALUE): 누름값(simbols_VALUE); 누름값(simbols_VALUE,False)
            # Start with English keys only, as delivered without a host IME.
            Nobīde_VALUE=len(transkripcija); 글자입력('echo '); nospiest_Atslēga(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); nospiest_Atslēga(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('echo ')
            누름값(0xffe1); nospiest_Atslēga(32); 누름값(0xffe1,False)
            글자입력('dlfr'); nospiest_Atslēga(0xff08); nospiest_Atslēga(0xff08); 글자입력('fr')
            nospiest_Atslēga(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('echo '); nospiest_Atslēga(0xff31)
            글자입력('rhk rkqtk RkRnd'); nospiest_Atslēga(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Nobīde_VALUE)
            # The same composition edits UTF-8 text in the native vi editor.
            Nobīde_VALUE=len(transkripcija); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Nobīde_VALUE)
            글자입력('i'); nospiest_Atslēga(0xffc6); 글자입력('gksrmf dlfr'); nospiest_Atslēga(0xffc6)
            nospiest_Atslēga(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Nobīde_VALUE); 까지(b'jkoros-native> ',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('help ko\n')
            까지('한/nulle_operands Atslēga_VALUE, Shift+Space 또는 F9'.encode(),Nobīde_VALUE); 까지(b'jkoros-native> ',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Nobīde_VALUE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            starpliktuve_VALUE='echo "ielīmēt_VALUE 완료"\n'.encode(); Nobīde_VALUE=len(transkripcija)
            klients.sendall(struct.pack('>B3xI',6,len(starpliktuve_VALUE))+starpliktuve_VALUE)
            for Notikums,_ in 준비살피미.select(.15):
                datu_bloks=Notikums.fileobj.read(4096)
                if datu_bloks: transkripcija.extend(datu_bloks)
            assert 'ielīmēt_VALUE 완료'.encode() not in transkripcija[Nobīde_VALUE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Nobīde_VALUE)
            klients.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                informēšana_SMS=EXACT_VALUE(klients,1)[0]
                if informēšana_SMS==2: continue
                if informēšana_SMS==3:
                    Izmērs=struct.unpack('>I',EXACT_VALUE(klients,7)[3:])[0]; EXACT_VALUE(klients,Izmērs); continue
                assert informēšana_SMS==0,informēšana_SMS
                사각형들=struct.unpack('>H',EXACT_VALUE(klients,3)[1:])[0]
                for _ in range(사각형들):
                    x_koordināta,세로좌표,너비값,높이값,rakstzīmju_kopa=struct.unpack('>HHHHi',EXACT_VALUE(klients,12)); assert rakstzīmju_kopa==0,rakstzīmju_kopa
                    화소들=EXACT_VALUE(klients,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; mērķis_adrese_08bbd577=((세로좌표+안쪽순번)*640+x_koordināta+순번)*3
                            빛삼원색[mērķis_adrese_08bbd577:mērķis_adrese_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (ražojums/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(ražojums/'vnc-terminal.png'))
            Nobīde_VALUE=len(transkripcija)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); klients.sendall(struct.pack('>BBHH',5,1,576,81)); klients.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Nobīde_VALUE)
            assert len(transkripcija)-Nobīde_VALUE>8192,'exercise output longer than bridge status buffer'
            Nobīde_VALUE=len(transkripcija); klients.sendall(struct.pack('>BBHH',5,1,560,63)); klients.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); klients.sendall(struct.pack('>BBHH',5,1,80,16)); klients.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); 글자입력('gui\n'); 까지(b'GUI READY:',Nobīde_VALUE)
            Nobīde_VALUE=len(transkripcija); klients.sendall(struct.pack('>BBHH',5,1,80,332)); klients.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Nobīde_VALUE)
            validācija_ziņot.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Process.poll() is None:
            Process.terminate()
            try: Process.wait(timeout=8)
            except subprocess.TimeoutExpired: Process.kill(); Process.wait()
        준비살피미.close(); Process.stdout.close()
        (ražojums/'serial.log').write_bytes(transkripcija)
        (ražojums/'report.json').write_text(json.dumps(validācija_ziņot,indent=2)+'\n')


if __name__=='__main__': Palaist()
