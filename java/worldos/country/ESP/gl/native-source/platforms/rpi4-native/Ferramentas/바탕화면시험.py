#!/usr/bin/env python3
"""real_datos RFB 클라이언트로 QEMU 창의 한글/Chave_VALOR/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from escritorio_ver import EXACTO_VALOR
from executar_comando import Project_raíz


def Executar_2():
    출력결과=Project_raíz/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Proceso=subprocess.Popen(['python3',str(Project_raíz/'Ferramentas/escritorio_ver.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Proceso.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); validación_informe={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_raíz/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,Executar_2=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[Executar_2:]:
            if time.monotonic()>마감시각 or Proceso.poll() is not None: raise AssertionError(대화기록[Executar_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                datos=누름값.fileobj.read(4096)
                if datos: 대화기록.extend(datos)
        return bytes(대화기록[Executar_2:])
    try:
        까지(b'TERMINAL READY')
        número_do_porto=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',número_do_porto),timeout=10) as cliente:
            assert EXACTO_VALOR(cliente,12)==b'RFB 003.008\n'; cliente.sendall(b'RFB 003.008\n')
            assert 1 in EXACTO_VALOR(cliente,EXACTO_VALOR(cliente,1)[0]); cliente.sendall(b'\x01'); assert EXACTO_VALOR(cliente,4)==b'\0'*4
            cliente.sendall(b'\x01'); 초기값=EXACTO_VALOR(cliente,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACTO_VALOR(cliente,struct.unpack('>I',초기값[20:])[0])
            cliente.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            cliente.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(símbolo_VALOR,누르는중=True): cliente.sendall(struct.pack('>BBHI',4,int(누르는중),0,símbolo_VALOR))
            def 글자입력(Texto):
                for carácter_datos in Texto:
                    símbolo=0xff0d if carácter_datos=='\n' else ord(carácter_datos) if ord(carácter_datos)<256 else 0x01000000|ord(carácter_datos)
                    누름값(símbolo); 누름값(símbolo,False)
            def pulsar_Chave(símbolo_VALOR): 누름값(símbolo_VALOR); 누름값(símbolo_VALOR,False)
            # Start with English keys only, as delivered without a host IME.
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('echo '); pulsar_Chave(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); pulsar_Chave(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); pulsar_Chave(32); 누름값(0xffe1,False)
            글자입력('dlfr'); pulsar_Chave(0xff08); pulsar_Chave(0xff08); 글자입력('fr')
            pulsar_Chave(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('echo '); pulsar_Chave(0xff31)
            글자입력('rhk rkqtk RkRnd'); pulsar_Chave(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),DESPRAZAMENTO_VALOR)
            # The same composition edits UTF-8 text in the native vi editor.
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',DESPRAZAMENTO_VALOR)
            글자입력('i'); pulsar_Chave(0xffc6); 글자입력('gksrmf dlfr'); pulsar_Chave(0xffc6)
            pulsar_Chave(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),DESPRAZAMENTO_VALOR); 까지(b'jkoros-native> ',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('help ko\n')
            까지('한/영 Chave_VALOR, Shift+Space 또는 F9'.encode(),DESPRAZAMENTO_VALOR); 까지(b'jkoros-native> ',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',DESPRAZAMENTO_VALOR)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            portapapeis_VALOR='echo "pegar_VALOR 완료"\n'.encode(); DESPRAZAMENTO_VALOR=len(대화기록)
            cliente.sendall(struct.pack('>B3xI',6,len(portapapeis_VALOR))+portapapeis_VALOR)
            for Evento,_ in 준비살피미.select(.15):
                datos_bloquear=Evento.fileobj.read(4096)
                if datos_bloquear: 대화기록.extend(datos_bloquear)
            assert 'pegar_VALOR 완료'.encode() not in 대화기록[DESPRAZAMENTO_VALOR:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),DESPRAZAMENTO_VALOR)
            cliente.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=EXACTO_VALOR(cliente,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    Tamaño=struct.unpack('>I',EXACTO_VALOR(cliente,7)[3:])[0]; EXACTO_VALOR(cliente,Tamaño); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',EXACTO_VALOR(cliente,3)[1:])[0]
                for _ in range(사각형들):
                    X_coordenada,Y_coordenada,너비값,높이값,conxunto_de_caracteres=struct.unpack('>HHHHi',EXACTO_VALOR(cliente,12)); assert conxunto_de_caracteres==0,conxunto_de_caracteres
                    화소들=EXACTO_VALOR(cliente,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; destino_ENDEREZO=((Y_coordenada+안쪽순번)*640+X_coordenada+순번)*3
                            빛삼원색[destino_ENDEREZO:destino_ENDEREZO+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            DESPRAZAMENTO_VALOR=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); cliente.sendall(struct.pack('>BBHH',5,1,576,81)); cliente.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',DESPRAZAMENTO_VALOR)
            assert len(대화기록)-DESPRAZAMENTO_VALOR>8192,'exercise output longer than bridge status buffer'
            DESPRAZAMENTO_VALOR=len(대화기록); cliente.sendall(struct.pack('>BBHH',5,1,560,63)); cliente.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); cliente.sendall(struct.pack('>BBHH',5,1,80,16)); cliente.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',DESPRAZAMENTO_VALOR)
            DESPRAZAMENTO_VALOR=len(대화기록); cliente.sendall(struct.pack('>BBHH',5,1,80,332)); cliente.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',DESPRAZAMENTO_VALOR)
            validación_informe.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Proceso.poll() is None:
            Proceso.terminate()
            try: Proceso.wait(timeout=8)
            except subprocess.TimeoutExpired: Proceso.kill(); Proceso.wait()
        준비살피미.close(); Proceso.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(validación_informe,indent=2)+'\n')


if __name__=='__main__': Executar_2()
