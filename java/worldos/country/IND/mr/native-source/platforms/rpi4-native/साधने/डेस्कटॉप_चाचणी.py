#!/usr/bin/env python3
"""वास्तविक_डेटा RFB 클라이언트로 QEMU 창의 한글/कळ_मूल्य/클립보드/마우스와 पडदा 전송을 검사한다."""
import hashlib
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from pathlib import Path
from डेस्कटॉप_दृश्य import तंतोतंत_मूल्य
from आज्ञा_कार्यवाही_करा import प्रोजेक्ट_मूळ


def सुरू_करा():
    प्रदान=प्रोजेक्ट_मूळ/'build/verification/desktop'; प्रदान.mkdir(parents=True,exist_ok=True)
    प्रक्रिया=subprocess.Popen(['python3',str(प्रोजेक्ट_मूळ/'साधने/डेस्कटॉप_दृश्य.py'),'--port','0'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    सज्जता_मॉनिटर=selectors.DefaultSelector(); सज्जता_मॉनिटर.register(प्रक्रिया.stdout,selectors.EVENT_READ)
    सत्रलेख=bytearray(); पडताळणी_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_मूळ/'build/kernel8.img').read_bytes()).hexdigest()}
    def पर्यंत(खूण,सुरू_करा=0):
        अंतिमवेळ_वेळ=time.monotonic()+45
        while खूण not in सत्रलेख[सुरू_करा:]:
            if time.monotonic()>अंतिमवेळ_वेळ or प्रक्रिया.poll() is not None: raise AssertionError(सत्रलेख[सुरू_करा:].decode('utf-8','replace'))
            for दाबलेले_मूल्य,_ in सज्जता_मॉनिटर.select(.1):
                डेटा=दाबलेले_मूल्य.fileobj.read(4096)
                if डेटा: सत्रलेख.extend(डेटा)
        return bytes(सत्रलेख[सुरू_करा:])
    try:
        पर्यंत(b'TERMINAL READY')
        पोर्ट_नंबर=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',सत्रलेख).group(1))
        with socket.create_connection(('127.0.0.1',पोर्ट_नंबर),timeout=10) as क्लायंट:
            assert तंतोतंत_मूल्य(क्लायंट,12)==b'RFB 003.008\n'; क्लायंट.sendall(b'RFB 003.008\n')
            assert 1 in तंतोतंत_मूल्य(क्लायंट,तंतोतंत_मूल्य(क्लायंट,1)[0]); क्लायंट.sendall(b'\x01'); assert तंतोतंत_मूल्य(क्लायंट,4)==b'\0'*4
            क्लायंट.sendall(b'\x01'); प्रारंभिक_मूल्य=तंतोतंत_मूल्य(क्लायंट,24); assert struct.unpack('>HH',प्रारंभिक_मूल्य[:4])==(640,480); तंतोतंत_मूल्य(क्लायंट,struct.unpack('>I',प्रारंभिक_मूल्य[20:])[0])
            क्लायंट.sendall(b'\x00\x00\x00\x00'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
            क्लायंट.sendall(struct.pack('>BBHi',2,0,1,0))
            def दाबलेले_मूल्य(चिन्ह_मूल्य,आहे_दाबणे=True): क्लायंट.sendall(struct.pack('>BBHI',4,int(आहे_दाबणे),0,चिन्ह_मूल्य))
            def टंकित_वर्ण(पाठ्य):
                for वर्ण_डेटा in पाठ्य:
                    चिन्ह=0xff0d if वर्ण_डेटा=='\n' else ord(वर्ण_डेटा) if ord(वर्ण_डेटा)<256 else 0x01000000|ord(वर्ण_डेटा)
                    दाबलेले_मूल्य(चिन्ह); दाबलेले_मूल्य(चिन्ह,False)
            def दाबा_कळ(चिन्ह_मूल्य): दाबलेले_मूल्य(चिन्ह_मूल्य); दाबलेले_मूल्य(चिन्ह_मूल्य,False)
            # Start with English keys only, as delivered without a host IME.
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('echo '); दाबा_कळ(0xffc6)
            टंकित_वर्ण('dkssudgktpdy gksrmf'); दाबा_कळ(0xffc6); टंकित_वर्ण('\n')
            पर्यंत('\r\n안녕하세요 한글\r\njkoros-native> '.encode(),ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('echo ')
            दाबलेले_मूल्य(0xffe1); दाबा_कळ(32); दाबलेले_मूल्य(0xffe1,False)
            टंकित_वर्ण('dlfr'); दाबा_कळ(0xff08); दाबा_कळ(0xff08); टंकित_वर्ण('fr')
            दाबा_कळ(0xff31); टंकित_वर्ण(' EN\n')
            पर्यंत('\r\n읽 EN\r\njkoros-native> '.encode(),ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('echo '); दाबा_कळ(0xff31)
            टंकित_वर्ण('rhk rkqtk RkRnd'); दाबा_कळ(0xff31); टंकित_वर्ण('\n')
            पर्यंत('\r\n과 갑사 까꿍\r\njkoros-native> '.encode(),ऑफसेट_मूल्य)
            # The same composition edits UTF-8 text in the native vi editor.
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('vi हांगुल_आदान.txt\n'); पर्यंत(b'NORMAL',ऑफसेट_मूल्य)
            टंकित_वर्ण('i'); दाबा_कळ(0xffc6); टंकित_वर्ण('gksrmf dlfr'); दाबा_कळ(0xffc6)
            दाबा_कळ(0xff1b); टंकित_वर्ण(':wq\n'); पर्यंत(b'jkoros-native> ',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('cat हांगुल_आदान.txt\n')
            पर्यंत('한글 읽'.encode(),ऑफसेट_मूल्य); पर्यंत(b'jkoros-native> ',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('help ko\n')
            पर्यंत('한/शून्य_संकार्य कळ_मूल्य, Shift+Space 또는 F9'.encode(),ऑफसेट_मूल्य); पर्यंत(b'jkoros-native> ',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('clear\necho "VNC 한글 आदान_मूल्य 😀"\n'); पर्यंत('VNC 한글 आदान_मूल्य 😀\r\n'.encode(),ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); दाबलेले_मूल्य(0xffe3); दाबलेले_मूल्य(ord('u')); दाबलेले_मूल्य(ord('u'),False); दाबलेले_मूल्य(0xffe3,False); टंकित_वर्ण('echo CONTROL_OK\n'); पर्यंत(b'\r\nCONTROL_OK\r\n',ऑफसेट_मूल्य)
            # A shared clipboard is not a paste command. Require explicit Ctrl+Shift+V.
            क्लिपबोर्ड_मूल्य='echo "चिकटवा_मूल्य आहे_पूर्ण"\n'.encode(); ऑफसेट_मूल्य=len(सत्रलेख)
            क्लायंट.sendall(struct.pack('>B3xI',6,len(क्लिपबोर्ड_मूल्य))+क्लिपबोर्ड_मूल्य)
            for इव्हेंट,_ in सज्जता_मॉनिटर.select(.15):
                डेटा_अवरोधित_करा=इव्हेंट.fileobj.read(4096)
                if डेटा_अवरोधित_करा: सत्रलेख.extend(डेटा_अवरोधित_करा)
            assert 'चिकटवा_मूल्य आहे_पूर्ण'.encode() not in सत्रलेख[ऑफसेट_मूल्य:]
            दाबलेले_मूल्य(0xffe3); दाबलेले_मूल्य(0xffe1); दाबलेले_मूल्य(ord('v')); दाबलेले_मूल्य(ord('v'),False); दाबलेले_मूल्य(0xffe1,False); दाबलेले_मूल्य(0xffe3,False)
            # The prompt follows the guest's terminal redraw after command completion.
            पर्यंत('\r\n붙여넣기 आहे_पूर्ण\r\njkoros-native> '.encode(),ऑफसेट_मूल्य)
            क्लायंट.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
            रेड_ग्रीन_ब्ल्यू_रंग=bytearray(640*480*3); पाहिलेले_नोंदी=False
            while not पाहिलेले_नोंदी:
                सूचना_मजकूर=तंतोतंत_मूल्य(क्लायंट,1)[0]
                if सूचना_मजकूर==2: continue
                if सूचना_मजकूर==3:
                    आकार=struct.unpack('>I',तंतोतंत_मूल्य(क्लायंट,7)[3:])[0]; तंतोतंत_मूल्य(क्लायंट,आकार); continue
                assert सूचना_मजकूर==0,सूचना_मजकूर
                आयत_यादी=struct.unpack('>H',तंतोतंत_मूल्य(क्लायंट,3)[1:])[0]
                for _ in range(आयत_यादी):
                    आडवे_समन्वयीत,उभे_समन्वयीत,मागितलेले_रुंदी_मूल्य,मागितलेले_उंची_मूल्य,वर्ण_संच=struct.unpack('>HHHHi',तंतोतंत_मूल्य(क्लायंट,12)); assert वर्ण_संच==0,वर्ण_संच
                    चित्रबिंदू_यादी=तंतोतंत_मूल्य(क्लायंट,मागितलेले_रुंदी_मूल्य*मागितलेले_उंची_मूल्य*4)
                    for आंतरिक_संयोग_क्रमांक in range(मागितलेले_उंची_मूल्य):
                        for क्रमांक_अनुक्रमणिका in range(मागितलेले_रुंदी_मूल्य):
                            मूळ_पत्ता_4c9bece9=(आंतरिक_संयोग_क्रमांक*मागितलेले_रुंदी_मूल्य+क्रमांक_अनुक्रमणिका)*4; गंतव्यस्थान_पत्ता=((उभे_समन्वयीत+आंतरिक_संयोग_क्रमांक)*640+आडवे_समन्वयीत+क्रमांक_अनुक्रमणिका)*3
                            रेड_ग्रीन_ब्ल्यू_रंग[गंतव्यस्थान_पत्ता:गंतव्यस्थान_पत्ता+3]=bytes((चित्रबिंदू_यादी[मूळ_पत्ता_4c9bece9+2],चित्रबिंदू_यादी[मूळ_पत्ता_4c9bece9+1],चित्रबिंदू_यादी[मूळ_पत्ता_4c9bece9]))
                    पाहिलेले_नोंदी=True
            assert रेड_ग्रीन_ब्ल्यू_रंग[(48*640+12)*3:(48*640+12)*3+3]==bytes((32,80,144))
            (प्रदान/'vnc-terminal.ppm').write_bytes(b'P6\n640 480\n255\n'+रेड_ग्रीन_ब्ल्यू_रंग)
            from PIL import Image
            Image.frombytes('RGB',(640,480),bytes(रेड_ग्रीन_ब्ल्यू_रंग)).save(str(प्रदान/'vnc-terminal.png'))
            ऑफसेट_मूल्य=len(सत्रलेख)
            दाबलेले_मूल्य(0xffe3); दाबलेले_मूल्य(0xffe1); दाबलेले_मूल्य(ord('t')); दाबलेले_मूल्य(ord('t'),False); दाबलेले_मूल्य(0xffe1,False); दाबलेले_मूल्य(0xffe3,False)
            पर्यंत(b'TERMINAL FOCUS 2',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('echo SECOND_VNC_WINDOW\n'); पर्यंत(b'\r\nSECOND_VNC_WINDOW\r\n',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); क्लायंट.sendall(struct.pack('>BBHH',5,1,576,81)); क्लायंट.sendall(struct.pack('>BBHH',5,0,576,81)); पर्यंत(b'TERMINAL FOCUS 1',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('python -c \'print("x"*9000)\'\n'); पर्यंत(b'\r\njkoros-native> ',ऑफसेट_मूल्य)
            assert len(सत्रलेख)-ऑफसेट_मूल्य>8192,'exercise output longer than bridge status buffer'
            ऑफसेट_मूल्य=len(सत्रलेख); क्लायंट.sendall(struct.pack('>BBHH',5,1,560,63)); क्लायंट.sendall(struct.pack('>BBHH',5,0,560,63)); पर्यंत(b'TERMINAL FOCUS 1',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); क्लायंट.sendall(struct.pack('>BBHH',5,1,80,16)); क्लायंट.sendall(struct.pack('>BBHH',5,0,80,16)); पर्यंत(b'TERMINAL FOCUS 1',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('echo REOPENED_VNC_WINDOW\n'); पर्यंत(b'\r\nREOPENED_VNC_WINDOW\r\n',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); टंकित_वर्ण('gui\n'); पर्यंत(b'GUI READY:',ऑफसेट_मूल्य)
            ऑफसेट_मूल्य=len(सत्रलेख); क्लायंट.sendall(struct.pack('>BBHH',5,1,80,332)); क्लायंट.sendall(struct.pack('>BBHH',5,0,80,332)); पर्यंत(b'TERMINAL READY',ऑफसेट_मूल्य)
            पडताळणी_अहवाल.update(passed=True,checks=['RFB 3.8 handshake and actual 640x480 raw framebuffer','F9, Shift+Space and Hangul toggle: ASCII two-set keys compose Korean in shell and vi','compound vowels/finals, resyllabification and composition Backspace','help ko lists implemented shortcuts','Unicode Hangul/emoji keysyms -> guest shell','Ctrl modifiers and explicit clipboard paste; no clipboard auto-execution','Ctrl+Shift+T creates second native terminal, mouse X closes it','mouse close after 9 KiB output, desktop new-terminal button and legacy launcher button'])
        print('PASS: actual VNC keyboard/Unicode/paste/mouse/framebuffer -> native terminal')
    finally:
        if प्रक्रिया.poll() is None:
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=8)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
        सज्जता_मॉनिटर.close(); प्रक्रिया.stdout.close()
        (प्रदान/'serial.log').write_bytes(सत्रलेख)
        (प्रदान/'report.json').write_text(json.dumps(पडताळणी_अहवाल,indent=2)+'\n')


if __name__=='__main__': सुरू_करा()
