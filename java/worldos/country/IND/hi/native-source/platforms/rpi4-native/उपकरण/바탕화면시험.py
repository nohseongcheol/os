#!/usr/bin/env python3
"""वास्तविक_डेटा RFB 클라이언트로 QEMU 창의 한글/कुंजी_मान/클립보드/마우스와 화면 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from डेस्कटॉप_दृश्य import 정확한값
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल


def चलाएँ():
    출력결과=प्रोजेक्ट_करें_मूल/'build/verification/desktop'; 출력결과.mkdir(parents=True,exist_ok=True)
    प्रक्रिया=subprocess.Popen(['python3',str(प्रोजेक्ट_करें_मूल/'उपकरण/डेस्कटॉप_दृश्य.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    तैयारी_मॉनीटर=selectors.DefaultSelector(); तैयारी_मॉनीटर.register(प्रक्रिया.stdout,selectors.EVENT_READ)
    बोला_गया_पाठ=bytearray(); प्रमाणीकरण_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest()}
    def 까지(मार्कर,चलाएँ=0):
        अंति_म_समय_सीमा_समय=time.monotonic()+45
        while मार्कर not in बोला_गया_पाठ[चलाएँ:]:
            if time.monotonic()>अंति_म_समय_सीमा_समय or प्रक्रिया.poll() is not None: raise AssertionError(बोला_गया_पाठ[चलाएँ:].decode('utf-8','replace'))
            for 누름값,_ in तैयारी_मॉनीटर.select(.1):
                आँकड़े=누름값.fileobj.read(4096)
                if आँकड़े: बोला_गया_पाठ.extend(आँकड़े)
        return bytes(बोला_गया_पाठ[चलाएँ:])
    try:
        까지(b'TERMINAL READY')
        पोर्ट_संख्या=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',बोला_गया_पाठ).group(1))
        with socket.create_connection(('127.0.0.1',पोर्ट_संख्या),timeout=10) as क्लायंट:
            assert 정확한값(क्लायंट,12)==b'RFB 003.008\n'; क्लायंट.sendall(b'RFB 003.008\n')
            assert 1 in 정확한값(क्लायंट,정확한값(क्लायंट,1)[0]); क्लायंट.sendall(b'\x01'); assert 정확한값(क्लायंट,4)==b'\0'*4
            क्लायंट.sendall(b'\x01'); 초기값=정확한값(क्लायंट,24); assert struct.unpack('>HH',초기값[:4])==(640,480); 정확한값(क्लायंट,struct.unpack('>I',초기값[20:])[0])
            क्लायंट.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            क्लायंट.sendall(struct.pack('>BBHi',2,0,1,0))
            def 누름값(प्रतीक_मान,누르는중=True): क्लायंट.sendall(struct.pack('>BBHI',4,int(누르는중),0,प्रतीक_मान))
            def 글자입력(पाठ):
                for वर्ण_डेटा in पाठ:
                    प्रतीक=0xff0d if वर्ण_डेटा=='\n' else ord(वर्ण_डेटा) if ord(वर्ण_डेटा)<256 else 0x01000000|ord(वर्ण_डेटा)
                    누름값(प्रतीक); 누름값(प्रतीक,False)
            def दबाएँ_कुंजी(प्रतीक_मान): 누름값(प्रतीक_मान); 누름값(प्रतीक_मान,False)
            # Start with English keys only, as delivered without a host IME.
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('echo '); दबाएँ_कुंजी(0xffc6)
            글자입력('dkssudgktpdy gksrmf'); दबाएँ_कुंजी(0xffc6); 글자입력('\n')
            까지('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('echo ')
            누름값(0xffe1); दबाएँ_कुंजी(32); 누름값(0xffe1,False)
            글자입력('dlfr'); दबाएँ_कुंजी(0xff08); दबाएँ_कुंजी(0xff08); 글자입력('fr')
            दबाएँ_कुंजी(0xff31); 글자입력(' EN\n')
            까지('\r\n읽 EN\r\njkoros-native> '.encode(),ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('echo '); दबाएँ_कुंजी(0xff31)
            글자입력('rhk rkqtk RkRnd'); दबाएँ_कुंजी(0xff31); 글자입력('\n')
            까지('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ऑफ़सेट_मान)
            # The same composition edits UTF-8 text in the native vi editor.
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('vi 한글입력.txt\n'); 까지(b'NORMAL',ऑफ़सेट_मान)
            글자입력('i'); दबाएँ_कुंजी(0xffc6); 글자입력('gksrmf dlfr'); दबाएँ_कुंजी(0xffc6)
            दबाएँ_कुंजी(0xff1b); 글자입력(':wq\n'); 까지(b'jkoros-native> ',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('cat 한글입력.txt\n')
            까지('한글 읽'.encode(),ऑफ़सेट_मान); 까지(b'jkoros-native> ',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('help ko\n')
            까지('한/शून्य_ऑपरेंड कुंजी_मान, Shift+Space 또는 F9'.encode(),ऑफ़सेट_मान); 까지(b'jkoros-native> ',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('clear\necho "VNC 한글 입력 😀"\n'); 까지('VNC 한글 입력 😀\r\n'.encode(),ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 누름값(0xffe3); 누름값(ord('u')); 누름값(ord('u'),False); 누름값(0xffe3,False); 글자입력('echo CONTROL_OK\n'); 까지(b'\r\nCONTROL_OK\r\n',ऑफ़सेट_मान)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            क्लिपबोर्ड_मान='echo "चिपकाएँ_मान 완료"\n'.encode(); ऑफ़सेट_मान=len(बोला_गया_पाठ)
            क्लायंट.sendall(struct.pack('>B3xI',6,len(क्लिपबोर्ड_मान))+क्लिपबोर्ड_मान)
            for घटना,_ in तैयारी_मॉनीटर.select(.15):
                डेटा_ब्_लॉक=घटना.fileobj.read(4096)
                if डेटा_ब्_लॉक: बोला_गया_पाठ.extend(डेटा_ब्_लॉक)
            assert 'चिपकाएँ_मान 완료'.encode() not in बोला_गया_पाठ[ऑफ़सेट_मान:]
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('v')); 누름값(ord('v'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            까지('\r\n붙여넣기 완료\r\njkoros-native> '.encode(),ऑफ़सेट_मान)
            क्लायंट.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            빛삼원색=bytearray(640*480*3); 본항목들=False
            while not 본항목들:
                सूचना_पाठ=정확한값(क्लायंट,1)[0]
                if सूचना_पाठ==2: continue
                if सूचना_पाठ==3:
                    आकार=struct.unpack('>I',정확한값(क्लायंट,7)[3:])[0]; 정확한값(क्लायंट,आकार); continue
                assert सूचना_पाठ==0,सूचना_पाठ
                사각형들=struct.unpack('>H',정확한값(क्लायंट,3)[1:])[0]
                for _ in range(사각형들):
                    x_निर्देशांक,세로좌표,너비값,높이값,वर्ण_सेट=struct.unpack('>HHHHi',정확한값(क्लायंट,12)); assert वर्ण_सेट==0,वर्ण_सेट
                    화소들=정확한값(क्लायंट,너비값*높이값*4)
                    for 안쪽순번 in range(높이값):
                        for 순번 in range(너비값):
                            원본주소=(안쪽순번*너비값+순번)*4; गंतव्य_पता=((세로좌표+안쪽순번)*640+x_निर्देशांक+순번)*3
                            빛삼원색[गंतव्य_पता:गंतव्य_पता+3]=bytes((화소들[원본주소+2],화소들[원본주소+1],화소들[원본주소]))
                    본항목들=True
            assert 빛삼원색[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (출력결과/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+빛삼원색)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(출력결과/'vnc-terminal.png'))
            ऑफ़सेट_मान=len(बोला_गया_पाठ)
            누름값(0xffe3); 누름값(0xffe1); 누름값(ord('t')); 누름값(ord('t'),False); 누름값(0xffe1,False); 누름값(0xffe3,False)
            까지(b'TERMINAL FOCUS 2',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('echo SECOND_VNC_WINDOW\n'); 까지(b'\r\nSECOND_VNC_WINDOW\r\n',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); क्लायंट.sendall(struct.pack('>BBHH',5,1,576,81)); क्लायंट.sendall(struct.pack('>BBHH',5,0,576,81)); 까지(b'TERMINAL FOCUS 1',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('python -c \'print("x"*9000)\'\n'); 까지(b'\r\njkoros-native> ',ऑफ़सेट_मान)
            assert len(बोला_गया_पाठ)-ऑफ़सेट_मान>8192,'exercise output longer than bridge status buffer'
            ऑफ़सेट_मान=len(बोला_गया_पाठ); क्लायंट.sendall(struct.pack('>BBHH',5,1,560,63)); क्लायंट.sendall(struct.pack('>BBHH',5,0,560,63)); 까지(b'TERMINAL FOCUS 1',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); क्लायंट.sendall(struct.pack('>BBHH',5,1,80,16)); क्लायंट.sendall(struct.pack('>BBHH',5,0,80,16)); 까지(b'TERMINAL FOCUS 1',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('echo REOPENED_VNC_WINDOW\n'); 까지(b'\r\nREOPENED_VNC_WINDOW\r\n',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); 글자입력('gui\n'); 까지(b'GUI READY:',ऑफ़सेट_मान)
            ऑफ़सेट_मान=len(बोला_गया_पाठ); क्लायंट.sendall(struct.pack('>BBHH',5,1,80,332)); क्लायंट.sendall(struct.pack('>BBHH',5,0,80,332)); 까지(b'TERMINAL READY',ऑफ़सेट_मान)
            प्रमाणीकरण_रिपोर्ट.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if प्रक्रिया.poll() is None:
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=8)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
        तैयारी_मॉनीटर.close(); प्रक्रिया.stdout.close()
        (출력결과/'serial.log').write_bytes(बोला_गया_पाठ)
        (출력결과/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,indent=2)+'\n')


if __name__=='__main__': चलाएँ()
