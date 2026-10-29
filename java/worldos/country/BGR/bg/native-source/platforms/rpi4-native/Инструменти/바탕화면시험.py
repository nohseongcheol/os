#!/usr/bin/env python3
"""действителен_данни RFB 클라이언트로 QEMU 창의 한글/Ключ_стойност/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from десктоп_Изглед import 정확한값
from изпълнявам_команда import проект_корен


def Стартиране():
    출력결과=проект_корен/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Процес=subprocess.Popen(['python3',str(проект_корен/'Инструменти/десктоп_Изглед.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процес.stdout,selectors.EVENT_READ)
    препис=bytearray(); проверка_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(маркер,Стартиране=0):
        краен_срок_час=time.monotonic()+45
        while маркер not in препис[Стартиране:]:
            if time.monotonic()>краен_срок_час or Процес.poll() is not None: raise AssertionError(препис[Стартиране:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                данни=누름값.fileobj.read(4096)
                if данни: препис.extend(данни)
        return bytes(препис[Стартиране:])
    try:
        까지(b'TERMINAL READY')
        номер_на_порт=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',препис).group(1))
        with socket.create_connection(('127.0.0.1',номер_на_порт),timeout=10) as клиент:
            assert 정확한값(клиент,12)==b'RFB 003.008\n'; клиент.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(клиент,정확한값(клиент,1)[0]); клиент.sendall(b'\x01'); assert 정확한값(клиент,4)==b'\0'*4
            клиент.sendall(b'\x01'); 초기값=정확한값(клиент,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(клиент,struct.unpack('>I',초기값[20:])[0])
            клиент.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            клиент.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(символ_стойност,누르는중=True): клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_стойност))
            def 글자입력(Текст):
                for знакови_данни in Текст:
                    символ=0xff0d if знакови_данни=='\n' else ord(знакови_данни) if ord(знакови_данни)<256 else 0x01000000|ord(знакови_данни)
                    누름값(символ); 누름값(символ,False)
            def натискам_Ключ(символ_стойност): 누름값(символ_стойност); 누름값(символ_стойност,False)
            # Start with English keys only, as delivered without a host IME.
            Изместване_стойност=len(препис); 글자입력('echo '); натискам_Ключ(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); натискам_Ключ(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('echo ')
            누름값(0xffe1); натискам_Ключ(32); 누름값(0xffe1,False)
            글자입력('dlfr'); натискам_Ключ(0xff08); натискам_Ключ(0xff08); 글자입력('fr')
            натискам_Ключ(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('echo '); натискам_Ключ(0xff31)
            글자입력('rhk rkqtk RkRnd'); натискам_Ключ(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Изместване_стойност)
            # The same composition edits UTF-8 text in the native vi editor.
            Изместване_стойност=len(препис); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Изместване_стойност)
            글자입력('i'); натискам_Ключ(0xffc6); 글자입력('gksrmf dlfr'); натискам_Ключ(0xffc6)
            натискам_Ключ(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Изместване_стойност); 까지(b'jkoros-native> ',Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('help ko\n')
            까지('한/нула_операнд Ключ_стойност, Shift+Space 또는 F9'.encode(),Изместване_стойност); 까지(b'jkoros-native> ',Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),Изместване_стойност)
            Изместване_стойност=len(препис); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Изместване_стойност)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            клипборд_стойност='echo "поставям_стойност 완료"\n'.encode(); Изместване_стойност=len(препис)
            клиент.sendall(struct.pack('>B3xI',6,len(клипборд_стойност))+клипборд_стойност)
            for Събитие,_ in 준비살피미.select(.15):
                блок_с_данни=Събитие.fileobj.read(4096)
                if блок_с_данни: препис.extend(блок_с_данни)
            assert 'поставям_стойност 완료'.encode() not in препис[Изместване_стойност:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Изместване_стойност)
            клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                предупреждение_Текст=정확한값(клиент,1)[0]
                if предупреждение_Текст==2: continue
                if предупреждение_Текст==3:
                    Размер=struct.unpack('>I',정확한값(клиент,7)[3:])[0]; 정확한값(клиент,Размер); continue
                assert предупреждение_Текст==0,предупреждение_Текст
                사각형들=struct.unpack('>H',정확한값(клиент,3)[1:])[0]
                for _ in range(사각형들):
                    x_координата,세로좌표,너비값,높이값,набор_символи=struct.unpack('>HHHHi',정확한값(клиент,12)); assert набор_символи==0,набор_символи
                    화소들=정확한값(клиент,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; местоназначение_адрес=((세로좌표+안쪽순번)*640+x_координата+순번)*3
                            빛삼원색[местоназначение_адрес:местоназначение_адрес+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            Изместване_стойност=len(препис)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Изместване_стойност)
            Изместване_стойност=len(препис); клиент.sendall(struct.pack('>BBHH',5,1,576,81)); клиент.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Изместване_стойност)
            assert len(препис)-Изместване_стойност>8192,'exercise output longer than bridge status buffer'
            Изместване_стойност=len(препис); клиент.sendall(struct.pack('>BBHH',5,1,560,63)); клиент.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Изместване_стойност)
            Изместване_стойност=len(препис); клиент.sendall(struct.pack('>BBHH',5,1,80,16)); клиент.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Изместване_стойност)
            Изместване_стойност=len(препис); 글자입력('gui\n'); 까지(b'GUI READY:',Изместване_стойност)
            Изместване_стойност=len(препис); клиент.sendall(struct.pack('>BBHH',5,1,80,332)); клиент.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Изместване_стойност)
            проверка_отчет.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Процес.poll() is None:
            Процес.terminate()
            try: Процес.wait(timeout=8)
            except subprocess.TimeoutExpired: Процес.kill(); Процес.wait()
        준비살피미.close(); Процес.stdout.close()
        (출력결과/'serial.log').write_bytes(препис)
        (출력결과/'report.json').write_text(json.dumps(проверка_отчет,indent=2)+'\n')


if __name__=='__main__': Стартиране()
