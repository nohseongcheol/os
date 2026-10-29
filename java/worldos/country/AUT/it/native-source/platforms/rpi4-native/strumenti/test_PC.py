#!/usr/bin/env python3
"""effettivo_dati RFB 클라이언트로 QEMU 창의 한글/tasto_VALORE/클립보드/마우스와 schermata 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from PC_Vista import IDENTICO_VALORE
from Esegui_comando import azione_radice


def avvia():
    output=azione_radice/'build/verification/desktop'; output.mkdir(parents=True,exist_ok=True)
    Processi=subprocess.Popen(['python3',str(azione_radice/'strumenti/PC_Vista.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Processi.stdout,selectors.EVENT_READ)
    trascrizione=bytearray(); convalida_Report={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((azione_radice/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(marcatore,avvia=0):
        scadenza_time=time.monotonic()+45
        while marcatore not in trascrizione[avvia:]:
            if time.monotonic()>scadenza_time or Processi.poll() is not None: raise AssertionError(trascrizione[avvia:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                dati=누름값.fileobj.read(4096)
                if dati: trascrizione.extend(dati)
        return bytes(trascrizione[avvia:])
    try:
        까지(b'TERMINAL READY')
        numero_di_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',trascrizione).group(1))
        with socket.create_connection(('127.0.0.1',numero_di_porta),timeout=10) as client:
            assert IDENTICO_VALORE(client,12)==b'RFB 003.008\n'; client.sendall(b'RFB 003.008\n')
            assert 1 in IDENTICO_VALORE(client,IDENTICO_VALORE(client,1)[0]); client.sendall(b'\x01'); assert IDENTICO_VALORE(client,4)==b'\0'*4
            client.sendall(b'\x01'); 초기값=IDENTICO_VALORE(client,24); assert struct.unpack('>HH',초기값[:4])==(640,480); IDENTICO_VALORE(client,struct.unpack('>I',초기값[20:])[0])
            client.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            client.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(simbolo_VALORE,누르는중=True): client.sendall(struct.pack('>BBHI',4,int(누르는중),0,simbolo_VALORE))
            def 글자입력(testo):
                for dati_di_tipo_carattere in testo:
                    simbolo=0xff0d if dati_di_tipo_carattere=='\n' else ord(dati_di_tipo_carattere) if ord(dati_di_tipo_carattere)<256 else 0x01000000|ord(dati_di_tipo_carattere)
                    누름값(simbolo); 누름값(simbolo,False)
            def 글쇠누르기(simbolo_VALORE): 누름값(simbolo_VALORE); 누름값(simbolo_VALORE,False)
            # Start with English keys only, as delivered without a host IME.
            SCARTO_VALORE=len(trascrizione); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),SCARTO_VALORE)
            # The same composition edits UTF-8 text in the native vi editor.
            SCARTO_VALORE=len(trascrizione); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',SCARTO_VALORE)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),SCARTO_VALORE); 까지(b'jkoros-native> ',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('help ko\n')
            까지('한/zero_operando tasto_VALORE, Shift+Space 또는 F9'.encode(),SCARTO_VALORE); 까지(b'jkoros-native> ',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('clear\necho "VNC 한글 input_VALORE 😀"\n'); 까지('VNC 한글 input_VALORE 😀\r\n'.encode(),SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',SCARTO_VALORE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            Appunti_VALORE='echo "incollare_VALORE 완료"\n'.encode(); SCARTO_VALORE=len(trascrizione)
            client.sendall(struct.pack('>B3xI',6,len(Appunti_VALORE))+Appunti_VALORE)
            for Evento,_ in 준비살피미.select(.15):
                blocco_di_dati=Evento.fileobj.read(4096)
                if blocco_di_dati: trascrizione.extend(blocco_di_dati)
            assert 'incollare_VALORE 완료'.encode() not in trascrizione[SCARTO_VALORE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),SCARTO_VALORE)
            client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                informativa_SMS=IDENTICO_VALORE(client,1)[0]
                if informativa_SMS==2: continue
                if informativa_SMS==3:
                    Dimensione=struct.unpack('>I',IDENTICO_VALORE(client,7)[3:])[0]; IDENTICO_VALORE(client,Dimensione); continue
                assert informativa_SMS==0,informativa_SMS
                사각형들=struct.unpack('>H',IDENTICO_VALORE(client,3)[1:])[0]
                for _ in range(사각형들):
                    coordinata_x,Y_coordinata,너비값,richiesto_altezza_VALORE,set_di_caratteri=struct.unpack('>HHHHi',IDENTICO_VALORE(client,12)); assert set_di_caratteri==0,set_di_caratteri
                    화소들=IDENTICO_VALORE(client,너비값*richiesto_altezza_VALORE*4)
                    for 안쪽순번 in range(richiesto_altezza_VALORE):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; meta_e_mail=((Y_coordinata+안쪽순번)*640+coordinata_x+순번)*3
                            빛삼원색[meta_e_mail:meta_e_mail+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (output/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(output/'vnc-terminal.png'))
            SCARTO_VALORE=len(trascrizione)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); client.sendall(struct.pack('>BBHH',5,1,576,81)); client.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',SCARTO_VALORE)
            assert len(trascrizione)-SCARTO_VALORE>8192,'exercise output longer than bridge status buffer'
            SCARTO_VALORE=len(trascrizione); client.sendall(struct.pack('>BBHH',5,1,560,63)); client.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); client.sendall(struct.pack('>BBHH',5,1,80,16)); client.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); 글자입력('gui\n'); 까지(b'GUI READY:',SCARTO_VALORE)
            SCARTO_VALORE=len(trascrizione); client.sendall(struct.pack('>BBHH',5,1,80,332)); client.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',SCARTO_VALORE)
            convalida_Report.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Processi.poll() is None:
            Processi.terminate()
            try: Processi.wait(timeout=8)
            except subprocess.TimeoutExpired: Processi.kill(); Processi.wait()
        준비살피미.close(); Processi.stdout.close()
        (output/'serial.log').write_bytes(trascrizione)
        (output/'report.json').write_text(json.dumps(convalida_Report,indent=2)+'\n')


if __name__=='__main__': avvia()
