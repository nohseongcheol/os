#!/usr/bin/env python3
"""фактично_дані RFB 클라이언트로 QEMU 창의 한글/Ключ_значення/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from настільний_Вигляд import 정확한값
from Виконати_команда import Дії_корінь


def запустити():
    출력결과=Дії_корінь/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Процеси=subprocess.Popen(['python3',str(Дії_корінь/'інструменти/настільний_Вигляд.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Процеси.stdout,selectors.EVENT_READ)
    транскрипт=bytearray(); перевірка_звіт={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(маркер,запустити=0):
        крайнiй_термін_час=time.monotonic()+45
        while маркер not in транскрипт[запустити:]:
            if time.monotonic()>крайнiй_термін_час or Процеси.poll() is not None: raise AssertionError(транскрипт[запустити:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                дані=누름값.fileobj.read(4096)
                if дані: транскрипт.extend(дані)
        return bytes(транскрипт[запустити:])
    try:
        까지(b'TERMINAL READY')
        номер_порту=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',транскрипт).group(1))
        with socket.create_connection(('127.0.0.1',номер_порту),timeout=10) as клієнт:
            assert 정확한값(клієнт,12)==b'RFB 003.008\n'; клієнт.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(клієнт,정확한값(клієнт,1)[0]); клієнт.sendall(b'\x01'); assert 정확한값(клієнт,4)==b'\0'*4
            клієнт.sendall(b'\x01'); 초기값=정확한값(клієнт,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(клієнт,struct.unpack('>I',초기값[20:])[0])
            клієнт.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            клієнт.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(символ_значення,누르는중=True): клієнт.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_значення))
            def 글자입력(текст):
                for символьні_дані in текст:
                    символ=0xff0d if символьні_дані=='\n' else ord(символьні_дані) if ord(символьні_дані)<256 else 0x01000000|ord(символьні_дані)
                    누름값(символ); 누름값(символ,False)
            def натиснути_Ключ(символ_значення): 누름값(символ_значення); 누름값(символ_значення,False)
            # Start with English keys only, as delivered without a host IME.
            Зміщена_копія_значення=len(транскрипт); 글자입력('echo '); натиснути_Ключ(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); натиснути_Ключ(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('echo ')
            누름값(0xffe1); натиснути_Ключ(32); 누름값(0xffe1,False)
            글자입력('dlfr'); натиснути_Ключ(0xff08); натиснути_Ключ(0xff08); 글자입력('fr')
            натиснути_Ключ(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('echo '); натиснути_Ключ(0xff31)
            글자입력('rhk rkqtk RkRnd'); натиснути_Ключ(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),Зміщена_копія_значення)
            # The same composition edits UTF-8 text in the native vi editor.
            Зміщена_копія_значення=len(транскрипт); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',Зміщена_копія_значення)
            글자입력('i'); натиснути_Ключ(0xffc6); 글자입력('gksrmf dlfr'); натиснути_Ключ(0xffc6)
            натиснути_Ключ(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),Зміщена_копія_значення); 까지(b'jkoros-native> ',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('help ko\n')
            까지('한/нуль_операнд Ключ_значення, Shift+Space 또는 F9'.encode(),Зміщена_копія_значення); 까지(b'jkoros-native> ',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',Зміщена_копія_значення)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            буфер_обміну_значення='echo "вставляти_значення 완료"\n'.encode(); Зміщена_копія_значення=len(транскрипт)
            клієнт.sendall(struct.pack('>B3xI',6,len(буфер_обміну_значення))+буфер_обміну_значення)
            for Подія,_ in 준비살피미.select(.15):
                блок_даних=Подія.fileobj.read(4096)
                if блок_даних: транскрипт.extend(блок_даних)
            assert 'вставляти_значення 완료'.encode() not in транскрипт[Зміщена_копія_значення:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),Зміщена_копія_значення)
            клієнт.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                повідомлення_Текст=정확한값(клієнт,1)[0]
                if повідомлення_Текст==2: continue
                if повідомлення_Текст==3:
                    Розмір=struct.unpack('>I',정확한값(клієнт,7)[3:])[0]; 정확한값(клієнт,Розмір); continue
                assert повідомлення_Текст==0,повідомлення_Текст
                사각형들=struct.unpack('>H',정확한값(клієнт,3)[1:])[0]
                for _ in range(사각형들):
                    координата_X,세로좌표,너비값,높이값,набір_символів=struct.unpack('>HHHHi',정확한값(клієнт,12)); assert набір_символів==0,набір_символів
                    화소들=정확한값(клієнт,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; місце_адреса=((세로좌표+안쪽순번)*640+координата_X+순번)*3
                            빛삼원색[місце_адреса:місце_адреса+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            Зміщена_копія_значення=len(транскрипт)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); клієнт.sendall(struct.pack('>BBHH',5,1,576,81)); клієнт.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',Зміщена_копія_значення)
            assert len(транскрипт)-Зміщена_копія_значення>8192,'exercise output longer than bridge status buffer'
            Зміщена_копія_значення=len(транскрипт); клієнт.sendall(struct.pack('>BBHH',5,1,560,63)); клієнт.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); клієнт.sendall(struct.pack('>BBHH',5,1,80,16)); клієнт.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); 글자입력('gui\n'); 까지(b'GUI READY:',Зміщена_копія_значення)
            Зміщена_копія_значення=len(транскрипт); клієнт.sendall(struct.pack('>BBHH',5,1,80,332)); клієнт.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',Зміщена_копія_значення)
            перевірка_звіт.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Процеси.poll() is None:
            Процеси.terminate()
            try: Процеси.wait(timeout=8)
            except subprocess.TimeoutExpired: Процеси.kill(); Процеси.wait()
        준비살피미.close(); Процеси.stdout.close()
        (출력결과/'serial.log').write_bytes(транскрипт)
        (출력결과/'report.json').write_text(json.dumps(перевірка_звіт,indent=2)+'\n')


if __name__=='__main__': запустити()
