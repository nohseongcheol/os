#!/usr/bin/env python3
"""ਅਸਲ_ਸਮੱਗਰੀ RFB 클라이언트로 QEMU 창의 한글/ਕੀ_ਕੀਮਤ/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼ import 정확한값
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ


def ਚਲਾਓ_2():
    출력결과=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    ਪਰੋਸੈੱਸ=subprocess.Popen(['python3',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'ਸਾਧਨ/ਡੈਸਕਟੌਪ_ਦ੍ਰਿਸ਼.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    준비살피미=selectors.DefaultSelector(); 준비살피미.register(ਪਰੋਸੈੱਸ.stdout,selectors.EVENT_READ)
    대화기록=bytearray(); ਮਾਨਤਾ_ਵਿਵਰਨ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(확인표시,ਚਲਾਓ_2=0):
        마감시각=time.monotonic()+45
        while 확인표시 not in 대화기록[ਚਲਾਓ_2:]:
            if time.monotonic()>마감시각 or ਪਰੋਸੈੱਸ.poll() is not None: raise AssertionError(대화기록[ਚਲਾਓ_2:].decode('utf-8','replace'))
            for 누름값,_ in 준비살피미.select(.1):
                ਸਮੱਗਰੀ=누름값.fileobj.read(4096)
                if ਸਮੱਗਰੀ: 대화기록.extend(ਸਮੱਗਰੀ)
        return bytes(대화기록[ਚਲਾਓ_2:])
    try:
        까지(b'TERMINAL READY')
        접속번호=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',대화기록).group(1))
        with socket.create_connection(('127.0.0.1',접속번호),timeout=10) as ਗਾਹਕ:
            assert 정확한값(ਗਾਹਕ,12)==b'RFB 003.008\n'; ਗਾਹਕ.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(ਗਾਹਕ,정확한값(ਗਾਹਕ,1)[0]); ਗਾਹਕ.sendall(b'\x01'); assert 정확한값(ਗਾਹਕ,4)==b'\0'*4
            ਗਾਹਕ.sendall(b'\x01'); 초기값=정확한값(ਗਾਹਕ,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(ਗਾਹਕ,struct.unpack('>I',초기값[20:])[0])
            ਗਾਹਕ.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            ਗਾਹਕ.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(ਪ੍ਰਤੀਕ_ਕੀਮਤ,누르는중=True): ਗਾਹਕ.sendall(struct.pack('>BBHI',4,int(누르는중),0,ਪ੍ਰਤੀਕ_ਕੀਮਤ))
            def 글자입력(ਟੈਕਸਟ):
                for ਵਰਣ_ਸਮੱਗਰੀ in ਟੈਕਸਟ:
                    ਪ੍ਰਤੀਕ=0xff0d if ਵਰਣ_ਸਮੱਗਰੀ=='\n' else ord(ਵਰਣ_ਸਮੱਗਰੀ) if ord(ਵਰਣ_ਸਮੱਗਰੀ)<256 else 0x01000000|ord(ਵਰਣ_ਸਮੱਗਰੀ)
                    누름값(ਪ੍ਰਤੀਕ); 누름값(ਪ੍ਰਤੀਕ,False)
            def 글쇠누르기(ਪ੍ਰਤੀਕ_ਕੀਮਤ): 누름값(ਪ੍ਰਤੀਕ_ਕੀਮਤ); 누름값(ਪ੍ਰਤੀਕ_ਕੀਮਤ,False)
            # Start with English keys only, as delivered without a host IME.
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('echo '); 글쇠누르기(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); 글쇠누르기(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('echo ')
            누름값(0xffe1); 글쇠누르기(32); 누름값(0xffe1,False)
            글자입력('dlfr'); 글쇠누르기(0xff08); 글쇠누르기(0xff08); 글자입력('fr')
            글쇠누르기(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('echo '); 글쇠누르기(0xff31)
            글자입력('rhk rkqtk RkRnd'); 글쇠누르기(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            # The same composition edits UTF-8 text in the native vi editor.
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ਔਫਸੈਟ_ਕੀਮਤ)
            글자입력('i'); 글쇠누르기(0xffc6); 글자입력('gksrmf dlfr'); 글쇠누르기(0xffc6)
            글쇠누르기(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ਔਫਸੈਟ_ਕੀਮਤ); 까지(b'jkoros-native> ',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('help ko\n')
            까지('한/영 ਕੀ_ਕੀਮਤ, Shift+Space 또는 F9'.encode(),ਔਫਸੈਟ_ਕੀਮਤ); 까지(b'jkoros-native> ',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ਔਫਸੈਟ_ਕੀਮਤ)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            ਕਲਿਪਬੋਰਡ_ਕੀਮਤ='echo "ਚਿਪਕਾਊਣਾ_ਕੀਮਤ 완료"\n'.encode(); ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록)
            ਗਾਹਕ.sendall(struct.pack('>B3xI',6,len(ਕਲਿਪਬੋਰਡ_ਕੀਮਤ))+ਕਲਿਪਬੋਰਡ_ਕੀਮਤ)
            for ਇਵੈਂਟ,_ in 준비살피미.select(.15):
                ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ=ਇਵੈਂਟ.fileobj.read(4096)
                if ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ: 대화기록.extend(ਸਮੱਗਰੀ_ਬਲੌਕ_ਕਰੋ)
            assert 'ਚਿਪਕਾਊਣਾ_ਕੀਮਤ 완료'.encode() not in 대화기록[ਔਫਸੈਟ_ਕੀਮਤ:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ਔਫਸੈਟ_ਕੀਮਤ)
            ਗਾਹਕ.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                알림문=정확한값(ਗਾਹਕ,1)[0]
                if 알림문==2: continue
                if 알림문==3:
                    ਆਕਾਰ=struct.unpack('>I',정확한값(ਗਾਹਕ,7)[3:])[0]; 정확한값(ਗਾਹਕ,ਆਕਾਰ); continue
                assert 알림문==0,알림문
                사각형들=struct.unpack('>H',정확한값(ਗਾਹਕ,3)[1:])[0]
                for _ in range(사각형들):
                    x_ਕੌਔਰਡੀਨੇਟ,세로좌표,너비값,높이값,ਵਰਣ_ਸੈਟ=struct.unpack('>HHHHi',정확한값(ਗਾਹਕ,12)); assert ਵਰਣ_ਸੈਟ==0,ਵਰਣ_ਸੈਟ
                    화소들=정확한값(ਗਾਹਕ,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; ਮੰਜਿਲ_ਪਤਾ=((세로좌표+안쪽순번)*640+x_ਕੌਔਰਡੀਨੇਟ+순번)*3
                            빛삼원색[ਮੰਜਿਲ_ਪਤਾ:ਮੰਜਿਲ_ਪਤਾ+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,1,576,81)); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ਔਫਸੈਟ_ਕੀਮਤ)
            assert len(대화기록)-ਔਫਸੈਟ_ਕੀਮਤ>8192,'exercise output longer than bridge status buffer'
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,1,560,63)); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,1,80,16)); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); 글자입력('gui\n'); 까지(b'GUI READY:',ਔਫਸੈਟ_ਕੀਮਤ)
            ਔਫਸੈਟ_ਕੀਮਤ=len(대화기록); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,1,80,332)); ਗਾਹਕ.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ਔਫਸੈਟ_ਕੀਮਤ)
            ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if ਪਰੋਸੈੱਸ.poll() is None:
            ਪਰੋਸੈੱਸ.terminate()
            try: ਪਰੋਸੈੱਸ.wait(timeout=8)
            except subprocess.TimeoutExpired: ਪਰੋਸੈੱਸ.kill(); ਪਰੋਸੈੱਸ.wait()
        준비살피미.close(); ਪਰੋਸੈੱਸ.stdout.close()
        (출력결과/'serial.log').write_bytes(대화기록)
        (출력결과/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,indent=2)+'\n')


if __name__=='__main__': ਚਲਾਓ_2()
