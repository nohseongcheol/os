#!/usr/bin/env python3
"""real_dades RFB 클라이언트로 QEMU 창의 한글/Clau_VALOR/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from escriptori_visualitzar import IGUAL_VALOR
from Executa_ordre import Project_rel


def Executa_2():
    출력결과=Project_rel/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Procés=subprocess.Popen(['python3',str(Project_rel/'Eines/escriptori_visualitzar.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Procés.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); validació_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_rel/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,Executa_2=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[Executa_2:]:
            if time.monotonic()>마감시각 or Procés.poll() is not None: raise AssertionError(대화기록[Executa_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                dades=누름값.fileobj.read(4096)
                if dades: 대화기록.extend(dades)
        return bytes(대화기록[Executa_2:])
    try:
        까지(b'TERMINAL READY')
        número_de_port=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',número_de_port),timeout=10) as client:
            assert IGUAL_VALOR(client,12)==b'RFB 003.008\n'; client.sendall(b'RFB 003.008\n')
            assert 1 in IGUAL_VALOR(client,IGUAL_VALOR(client,1)[0]); client.sendall(b'\x01'); assert IGUAL_VALOR(client,4)==b'\0'*4
            client.sendall(b'\x01'); 초기값=IGUAL_VALOR(client,24); assert struct.unpack('>HH',초기값[:4])==(640,480); IGUAL_VALOR(client,struct.unpack('>I',초기값[20:])[0])
            client.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            client.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(símbol_VALOR,누르는중=True): client.sendall(struct.pack('>BBHI',4,int(누르는중),0,símbol_VALOR))
            def 글자입력(SMS):
                for caràcter_dades in SMS:
                    símbol=0xff0d if caràcter_dades=='\n' else ord(caràcter_dades) if ord(caràcter_dades)<256 else 0x01000000|ord(caràcter_dades)
                    누름값(símbol); 누름값(símbol,False)
            def prémer_Clau(símbol_VALOR): 누름값(símbol_VALOR); 누름값(símbol_VALOR,False)
            # Start with English keys only, as delivered without a host IME.
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('echo '); prémer_Clau(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); prémer_Clau(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); prémer_Clau(32); 누름값(0xffe1,False)
            글자입력('dlfr'); prémer_Clau(0xff08); prémer_Clau(0xff08); 글자입력('fr')
            prémer_Clau(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('echo '); prémer_Clau(0xff31)
            글자입력('rhk rkqtk RkRnd'); prémer_Clau(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),DESPLAÇAMENT_VALOR)
            # The same composition edits UTF-8 text in the native vi editor.
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',DESPLAÇAMENT_VALOR)
            글자입력('i'); prémer_Clau(0xffc6); 글자입력('gksrmf dlfr'); prémer_Clau(0xffc6)
            prémer_Clau(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),DESPLAÇAMENT_VALOR); 까지(b'jkoros-native> ',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('help ko\n')
            까지('한/영 Clau_VALOR, Shift+Space 또는 F9'.encode(),DESPLAÇAMENT_VALOR); 까지(b'jkoros-native> ',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',DESPLAÇAMENT_VALOR)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            Porta_retalls_VALOR='echo "enganxar_VALOR 완료"\n'.encode(); DESPLAÇAMENT_VALOR=len(대화기록)
            client.sendall(struct.pack('>B3xI',6,len(Porta_retalls_VALOR))+Porta_retalls_VALOR)
            for Esdeveniment,_ in 준비살피미.select(.15):
                dades_bloquejar=Esdeveniment.fileobj.read(4096)
                if dades_bloquejar: 대화기록.extend(dades_bloquejar)
            assert 'enganxar_VALOR 완료'.encode() not in 대화기록[DESPLAÇAMENT_VALOR:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),DESPLAÇAMENT_VALOR)
            client.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=IGUAL_VALOR(client,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Mida=struct.unpack('>I',IGUAL_VALOR(client,7)[3:])[0]; IGUAL_VALOR(client,Mida); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',IGUAL_VALOR(client,3)[1:])[0]
                for _ in range(사각형들):
                    X_coordenada,Y_coordenada,너비값,높이값,joc_de_caràcters=struct.unpack('>HHHHi',IGUAL_VALOR(client,12)); assert joc_de_caràcters==0,joc_de_caràcters
                    화소들=IGUAL_VALOR(client,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; destinació_ADREÇA=((Y_coordenada+안쪽순번)*640+X_coordenada+순번)*3
                            빛삼원색[destinació_ADREÇA:destinació_ADREÇA+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            DESPLAÇAMENT_VALOR=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); client.sendall(struct.pack('>BBHH',5,1,576,81)); client.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',DESPLAÇAMENT_VALOR)
            assert len(대화기록)-DESPLAÇAMENT_VALOR>8192,'exercise output longer than bridge status buffer'
            DESPLAÇAMENT_VALOR=len(대화기록); client.sendall(struct.pack('>BBHH',5,1,560,63)); client.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); client.sendall(struct.pack('>BBHH',5,1,80,16)); client.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',DESPLAÇAMENT_VALOR)
            DESPLAÇAMENT_VALOR=len(대화기록); client.sendall(struct.pack('>BBHH',5,1,80,332)); client.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',DESPLAÇAMENT_VALOR)
            validació_informe.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Procés.poll() is None:
            Procés.terminate()
            try: Procés.wait(timeout=8)
            except subprocess.TimeoutExpired: Procés.kill(); Procés.wait()
        준비살피미.close(); Procés.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(validació_informe,indent=2)+'\n')


if __name__=='__main__': Executa_2()
