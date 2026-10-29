#!/usr/bin/env python3
"""real_dados RFB 클라이언트로 QEMU 창의 한글/Chave_VALOR/클립보드/마우스와 tela 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from desktop_Exibir import EXATO_VALOR
from Executar_comando import ação_raiz


def iniciar():
    saída=ação_raiz/'build/verification/desktop'; saída.mkdir(parents=True,exist_ok=True)
    Processo=subprocess.Popen(['python3',str(ação_raiz/'ferramentas/desktop_Exibir.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Processo.stdout,selectors.EVENT_READ)
    transcrição=bytearray(); validação_relatar={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ação_raiz/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(favorito,iniciar=0):
        data_limite_time=time.monotonic()+45
        while favorito not in transcrição[iniciar:]:
            if time.monotonic()>data_limite_time or Processo.poll() is not None: raise AssertionError(transcrição[iniciar:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                dados=누름값.fileobj.read(4096)
                if dados: transcrição.extend(dados)
        return bytes(transcrição[iniciar:])
    try:
        까지(b'TERMINAL READY')
        número_da_porta=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',transcrição).group(1))
        with socket.create_connection(('127.0.0.1',número_da_porta),timeout=10) as cliente:
            assert EXATO_VALOR(cliente,12)==b'RFB 003.008\n'; cliente.sendall(b'RFB 003.008\n')
            assert 1 in EXATO_VALOR(cliente,EXATO_VALOR(cliente,1)[0]); cliente.sendall(b'\x01'); assert EXATO_VALOR(cliente,4)==b'\0'*4
            cliente.sendall(b'\x01'); 초기값=EXATO_VALOR(cliente,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXATO_VALOR(cliente,struct.unpack('>I',초기값[20:])[0])
            cliente.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            cliente.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(símbolo_VALOR,누르는중=True): cliente.sendall(struct.pack('>BBHI',4,int(누르는중),0,símbolo_VALOR))
            def 글자입력(texto):
                for dados_de_caractere in texto:
                    símbolo=0xff0d if dados_de_caractere=='\n' else ord(dados_de_caractere) if ord(dados_de_caractere)<256 else 0x01000000|ord(dados_de_caractere)
                    누름값(símbolo); 누름값(símbolo,False)
            def 글쇠누르기(símbolo_VALOR): 누름값(símbolo_VALOR); 누름값(símbolo_VALOR,False)
            # Start with English keys only, as delivered without a host IME.
            DESLOC_VALOR=len(transcrição); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),DESLOC_VALOR)
            # The same composition edits UTF-8 text in the native vi editor.
            DESLOC_VALOR=len(transcrição); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',DESLOC_VALOR)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),DESLOC_VALOR); 까지(b'jkoros-native> ',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('help ko\n')
            까지('한/zero_operando Chave_VALOR, Shift+Space 또는 F9'.encode(),DESLOC_VALOR); 까지(b'jkoros-native> ',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('clear\necho "VNC 한글 entrada_VALOR 😀"\n'); 까지('VNC 한글 entrada_VALOR 😀\r\n'.encode(),DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',DESLOC_VALOR)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            área_de_transferência_VALOR='echo "colar_VALOR 완료"\n'.encode(); DESLOC_VALOR=len(transcrição)
            cliente.sendall(struct.pack('>B3xI',6,len(área_de_transferência_VALOR))+área_de_transferência_VALOR)
            for Evento,_ in 준비살피미.select(.15):
                bloco_de_dados=Evento.fileobj.read(4096)
                if bloco_de_dados: transcrição.extend(bloco_de_dados)
            assert 'colar_VALOR 완료'.encode() not in transcrição[DESLOC_VALOR:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),DESLOC_VALOR)
            cliente.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                aviso_SMS=EXATO_VALOR(cliente,1)[0]
                if aviso_SMS==2: continue
                if aviso_SMS==3:
                    Tamanho=struct.unpack('>I',EXATO_VALOR(cliente,7)[3:])[0]; EXATO_VALOR(cliente,Tamanho); continue
                assert aviso_SMS==0,aviso_SMS
                사각형들=struct.unpack('>H',EXATO_VALOR(cliente,3)[1:])[0]
                for _ in range(사각형들):
                    coordenada_X,Y_coordenada,너비값,solicitado_altura_VALOR,conjunto_de_caracteres=struct.unpack('>HHHHi',EXATO_VALOR(cliente,12)); assert conjunto_de_caracteres==0,conjunto_de_caracteres
                    화소들=EXATO_VALOR(cliente,너비값*solicitado_altura_VALOR*4)
                    for 안쪽순번 in range(solicitado_altura_VALOR):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; destino_email=((Y_coordenada+안쪽순번)*640+coordenada_X+순번)*3
                            빛삼원색[destino_email:destino_email+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (saída/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(saída/'vnc-terminal.png'))
            DESLOC_VALOR=len(transcrição)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); cliente.sendall(struct.pack('>BBHH',5,1,576,81)); cliente.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',DESLOC_VALOR)
            assert len(transcrição)-DESLOC_VALOR>8192,'exercise output longer than bridge status buffer'
            DESLOC_VALOR=len(transcrição); cliente.sendall(struct.pack('>BBHH',5,1,560,63)); cliente.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); cliente.sendall(struct.pack('>BBHH',5,1,80,16)); cliente.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); 글자입력('gui\n'); 까지(b'GUI READY:',DESLOC_VALOR)
            DESLOC_VALOR=len(transcrição); cliente.sendall(struct.pack('>BBHH',5,1,80,332)); cliente.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',DESLOC_VALOR)
            validação_relatar.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Processo.poll() is None:
            Processo.terminate()
            try: Processo.wait(timeout=8)
            except subprocess.TimeoutExpired: Processo.kill(); Processo.wait()
        준비살피미.close(); Processo.stdout.close()
        (saída/'serial.log').write_bytes(transcrição)
        (saída/'report.json').write_text(json.dumps(validação_relatar,indent=2)+'\n')


if __name__=='__main__': iniciar()
