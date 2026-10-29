#!/usr/bin/env python3
"""фактический_данные RFB 클라이언트로 QEMU 창의 한글/Ключ_ЗНАЧЕН/클립보드/마우스와 экран 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from компьютер_Вид import СОВПАД_ЗНАЧЕН
from 실행 import задача_корень


def запустить():
    выход=задача_корень/'build/verification/desktop'; выход.mkdir(parents=True,exist_ok=True)
    Процесс=subprocess.Popen(['python3',str(задача_корень/'инструменты/компьютер_Вид.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    готовность_монитор=selectors.DefaultSelector(); готовность_монитор.register(Процесс.stdout,selectors.EVENT_READ)
    расшифровка=bytearray(); проверка_Отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(метка,запустить=0):
        крайний_срок_ВРЕМЯ=time.monotonic()+45
        while метка not in расшифровка[запустить:]:
            if time.monotonic()>крайний_срок_ВРЕМЯ or Процесс.poll() is not None: raise AssertionError(расшифровка[запустить:].decode('utf-8','replace'))
            for 누름값,_ in готовность_монитор.select(.1):
                данные=누름값.fileobj.read(4096)
                if данные: расшифровка.extend(данные)
        return bytes(расшифровка[запустить:])
    try:
        까지(b'TERMINAL READY')
        номер_порта=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',расшифровка).group(1))
        with socket.create_connection(('127.0.0.1',номер_порта),timeout=10) as клиент:
            assert СОВПАД_ЗНАЧЕН(клиент,12)==b'RFB 003.008\n'; клиент.sendall(b'RFB 003.008\n')
            assert 1 in СОВПАД_ЗНАЧЕН(клиент,СОВПАД_ЗНАЧЕН(клиент,1)[0]); клиент.sendall(b'\x01'); assert СОВПАД_ЗНАЧЕН(клиент,4)==b'\0'*4
            клиент.sendall(b'\x01'); 초기값=СОВПАД_ЗНАЧЕН(клиент,24); assert struct.unpack('>HH',초기값[:4])==(640,480); СОВПАД_ЗНАЧЕН(клиент,struct.unpack('>I',초기값[20:])[0])
            клиент.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            клиент.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(символ_ЗНАЧЕН,누르는중=True): клиент.sendall(struct.pack('>BBHI',4,int(누르는중),0,символ_ЗНАЧЕН))
            def 글자입력(текст):
                for символьные_данные in текст:
                    символ=0xff0d if символьные_данные=='\n' else ord(символьные_данные) if ord(символьные_данные)<256 else 0x01000000|ord(символьные_данные)
                    누름값(символ); 누름값(символ,False)
            def 글쇠누르기(символ_ЗНАЧЕН): 누름값(символ_ЗНАЧЕН); 누름값(символ_ЗНАЧЕН,False)
            # Start with English keys only, as delivered without a host IME.
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),СМЕЩ_ЗНАЧЕН)
            # The same composition edits UTF-8 text in the native vi editor.
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',СМЕЩ_ЗНАЧЕН)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),СМЕЩ_ЗНАЧЕН); 까지(b'jkoros-native> ',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('help ko\n')
            까지('한/нуль_операнд Ключ_ЗНАЧЕН, Shift+Space 또는 F9'.encode(),СМЕЩ_ЗНАЧЕН); 까지(b'jkoros-native> ',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('clear\necho "VNC 한글 входные_данные_ЗНАЧЕН 😀"\n'); 까지('VNC 한글 входные_данные_ЗНАЧЕН 😀\r\n'.encode(),СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',СМЕЩ_ЗНАЧЕН)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            буфер_обмена_ЗНАЧЕН='echo "вставить_ЗНАЧЕН 완료"\n'.encode(); СМЕЩ_ЗНАЧЕН=len(расшифровка)
            клиент.sendall(struct.pack('>B3xI',6,len(буфер_обмена_ЗНАЧЕН))+буфер_обмена_ЗНАЧЕН)
            for Событие,_ in готовность_монитор.select(.15):
                блок_данных=Событие.fileobj.read(4096)
                if блок_данных: расшифровка.extend(блок_данных)
            assert 'вставить_ЗНАЧЕН 완료'.encode() not in расшифровка[СМЕЩ_ЗНАЧЕН:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),СМЕЩ_ЗНАЧЕН)
            клиент.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                уведомление_SMS=СОВПАД_ЗНАЧЕН(клиент,1)[0]
                if уведомление_SMS==2: continue
                if уведомление_SMS==3:
                    Размер=struct.unpack('>I',СОВПАД_ЗНАЧЕН(клиент,7)[3:])[0]; СОВПАД_ЗНАЧЕН(клиент,Размер); continue
                assert уведомление_SMS==0,уведомление_SMS
                사각형들=struct.unpack('>H',СОВПАД_ЗНАЧЕН(клиент,3)[1:])[0]
                for _ in range(사각형들):
                    координата_X,Y_координата,너비값,높이값,кодировка=struct.unpack('>HHHHi',СОВПАД_ЗНАЧЕН(клиент,12)); assert кодировка==0,кодировка
                    화소들=СОВПАД_ЗНАЧЕН(клиент,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; цель_АДРЕС_08bbd577=((Y_координата+안쪽순번)*640+координата_X+순번)*3
                            빛삼원색[цель_АДРЕС_08bbd577:цель_АДРЕС_08bbd577+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (выход/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(выход/'vnc-terminal.png'))
            СМЕЩ_ЗНАЧЕН=len(расшифровка)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); клиент.sendall(struct.pack('>BBHH',5,1,576,81)); клиент.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',СМЕЩ_ЗНАЧЕН)
            assert len(расшифровка)-СМЕЩ_ЗНАЧЕН>8192,'exercise output longer than bridge status buffer'
            СМЕЩ_ЗНАЧЕН=len(расшифровка); клиент.sendall(struct.pack('>BBHH',5,1,560,63)); клиент.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); клиент.sendall(struct.pack('>BBHH',5,1,80,16)); клиент.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); 글자입력('gui\n'); 까지(b'GUI READY:',СМЕЩ_ЗНАЧЕН)
            СМЕЩ_ЗНАЧЕН=len(расшифровка); клиент.sendall(struct.pack('>BBHH',5,1,80,332)); клиент.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',СМЕЩ_ЗНАЧЕН)
            проверка_Отчет.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Процесс.poll() is None:
            Процесс.terminate()
            try: Процесс.wait(timeout=8)
            except subprocess.TimeoutExpired: Процесс.kill(); Процесс.wait()
        готовность_монитор.close(); Процесс.stdout.close()
        (выход/'serial.log').write_bytes(расшифровка)
        (выход/'report.json').write_text(json.dumps(проверка_Отчет,indent=2)+'\n')


if __name__=='__main__': запустить()
