#!/usr/bin/env python3
"""dearbh_dàta RFB 클라이언트로 QEMU 창의 한글/Iuchair_VALUE/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from deasg_seall import EXACT_VALUE
from gnìomhaich_àithne import tilg_freumh


def ruith():
    출력결과=tilg_freumh/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    Pròiseas=subprocess.Popen(['python3',str(tilg_freumh/'innealan/deasg_seall.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(Pròiseas.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); dearbhadh_aithisg={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,ruith=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[ruith:]:
            if time.monotonic()>마감시각 or Pròiseas.poll() is not None: raise AssertionError(대화기록[ruith:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                dàta=누름값.fileobj.read(4096)
                if dàta: 대화기록.extend(dàta)
        return bytes(대화기록[ruith:])
    try:
        까지(b'TERMINAL READY')
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',접속번호),timeout=10) as cliant:
            assert EXACT_VALUE(cliant,12)==b'RFB 003.008\n'; cliant.sendall(b'RFB 003.008\n')
            assert 1 in EXACT_VALUE(cliant,EXACT_VALUE(cliant,1)[0]); cliant.sendall(b'\x01'); assert EXACT_VALUE(cliant,4)==b'\0'*4
            cliant.sendall(b'\x01'); 초기값=EXACT_VALUE(cliant,24); assert struct.unpack('>HH',초기값[:4])==(640,480); EXACT_VALUE(cliant,struct.unpack('>I',초기값[20:])[0])
            cliant.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            cliant.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(samhla_VALUE,누르는중=True): cliant.sendall(struct.pack('>BBHI',4,int(누르는중),0,samhla_VALUE))
            def 글자입력(SMS):
                for caractar_dàta in SMS:
                    samhla=0xff0d if caractar_dàta=='\n' else ord(caractar_dàta) if ord(caractar_dàta)<256 else 0x01000000|ord(caractar_dàta)
                    누름값(samhla); 누름값(samhla,False)
            def 글쇠누르기(samhla_VALUE): 누름값(samhla_VALUE); 누름값(samhla_VALUE,False)
            # Start with English keys only, as delivered without a host IME.
            OFFSET_VALUE=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),OFFSET_VALUE)
            # The same composition edits UTF-8 text in the native vi editor.
            OFFSET_VALUE=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',OFFSET_VALUE)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),OFFSET_VALUE); 까지(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('help ko\n')
            까지('한/영 Iuchair_VALUE, Shift+Space 또는 F9'.encode(),OFFSET_VALUE); 까지(b'jkoros-native> ',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',OFFSET_VALUE)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            bòrd_stòraidh_VALUE='echo "cuir_ann_VALUE 완료"\n'.encode(); OFFSET_VALUE=len(대화기록)
            cliant.sendall(struct.pack('>B3xI',6,len(bòrd_stòraidh_VALUE))+bòrd_stòraidh_VALUE)
            for tachartas,_ in 준비살피미.select(.15):
                dàta_bac=tachartas.fileobj.read(4096)
                if dàta_bac: 대화기록.extend(dàta_bac)
            assert 'cuir_ann_VALUE 완료'.encode() not in 대화기록[OFFSET_VALUE:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),OFFSET_VALUE)
            cliant.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=EXACT_VALUE(cliant,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    atharraich_am_meud=struct.unpack('>I',EXACT_VALUE(cliant,7)[3:])[0]; EXACT_VALUE(cliant,atharraich_am_meud); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',EXACT_VALUE(cliant,3)[1:])[0]
                for _ in range(사각형들):
                    co_chomharra_x,세로좌표,너비값,높이값,seata_charactaran=struct.unpack('>HHHHi',EXACT_VALUE(cliant,12)); assert seata_charactaran==0,seata_charactaran
                    화소들=EXACT_VALUE(cliant,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; ceann_uidhe_ADDRESS=((세로좌표+안쪽순번)*640+co_chomharra_x+순번)*3
                            빛삼원색[ceann_uidhe_ADDRESS:ceann_uidhe_ADDRESS+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            OFFSET_VALUE=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); cliant.sendall(struct.pack('>BBHH',5,1,576,81)); cliant.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',OFFSET_VALUE)
            assert len(대화기록)-OFFSET_VALUE>8192,'exercise output longer than bridge status buffer'
            OFFSET_VALUE=len(대화기록); cliant.sendall(struct.pack('>BBHH',5,1,560,63)); cliant.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); cliant.sendall(struct.pack('>BBHH',5,1,80,16)); cliant.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',OFFSET_VALUE)
            OFFSET_VALUE=len(대화기록); cliant.sendall(struct.pack('>BBHH',5,1,80,332)); cliant.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',OFFSET_VALUE)
            dearbhadh_aithisg.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if Pròiseas.poll() is None:
            Pròiseas.terminate()
            try: Pròiseas.wait(timeout=8)
            except subprocess.TimeoutExpired: Pròiseas.kill(); Pròiseas.wait()
        준비살피미.close(); Pròiseas.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(dearbhadh_aithisg,indent=2)+'\n')


if __name__=='__main__': ruith()
