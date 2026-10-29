#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल,आदेश

def चलाएँ():
    गंतव्य_मान_पद=प्रोजेक्ट_करें_मूल/'build/verification/windows';गंतव्य_मान_पद.mkdir(parents=True,exist_ok=True)
    प्रमाणीकरण_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रोजेक्ट_करें_मूल/'build/kernel8.img').read_bytes()).hexdigest()};लॉग_रिकॉर्ड=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        डेटा_पद=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        सिलेक्टर_a916db4e=selectors.DefaultSelector();सिलेक्टर_a916db4e.register(डेटा_पद.stdout,selectors.EVENT_READ)
        def हैंडल_घटना(초단위=.1):
            for 누름값,_ in सिलेक्टर_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:लॉग_रिकॉर्ड.extend(둘째값)
            assert b'PANIC:' not in लॉग_रिकॉर्ड and b'HALTED' not in लॉग_रिकॉर्ड,लॉग_रिकॉर्ड[-2048:]
        def 기다리기(मार्कर,अद्यतित_पद,초단위=50):
            समाप्त_करें_ऑफ़सेट=time.monotonic()+초단위
            while मार्कर not in लॉग_रिकॉर्ड[अद्यतित_पद:]:
                if time.monotonic()>समाप्त_करें_ऑफ़सेट or डेटा_पद.poll() is not None:raise AssertionError(लॉग_रिकॉर्ड[अद्यतित_पद:].decode('utf-8','replace'))
                हैंडल_घटना()
            return bytes(लॉग_रिकॉर्ड[अद्यतित_पद:])
        def भेजें(둘째값,मार्कर=b'jkoros-native> '):
            अद्यतित_पद=len(लॉग_रिकॉर्ड);डेटा_पद.stdin.write(둘째값);डेटा_पद.stdin.flush();return 기다리기(मार्कर,अद्यतित_पद)
        def शेल(स्ट्रिंग_डेटा):return भेजें((स्ट्रिंग_डेटा+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def हॉट_की_मान(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def क्लिक_करना_बटन(x_निर्देशांक,세로좌표):return bytes([30,1,1,x_निर्देशांक&255,x_निर्देशांक>>8,세로좌표&255,세로좌표>>8,30,1,0,x_निर्देशांक&255,x_निर्देशांक>>8,세로좌표&255,세로좌표>>8])
        def आदेश_मोड():
            डेटा_पद.stdin.write(b'\x1b');डेटा_पद.stdin.flush();समाप्त_करें_ऑफ़सेट=time.monotonic()+.2
            while time.monotonic()<समाप्त_करें_ऑफ़सेट:हैंडल_घटना(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            शेल('terminal');हैंडल_घटना(.3)
            शेल('mkdir first; cd first; export NAME=one')
            भेजें('vi 첫째.py\n'.encode(),b'NORMAL')
            भेजें('i값 = 21\nprint(मान * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            समाप्त_करें_ऑफ़सेट=time.monotonic()+3
            while time.monotonic()<समाप्त_करें_ऑफ़सेट:हैंडल_घटना(.1)
            भेजें(हॉट_की_मान(1),b'TERMINAL FOCUS 2');हैंडल_घटना(.2)
            assert b'/\r\n' in शेल('pwd')
            शेल('export NAME=two')
            भेजें('vi 둘째.txt\n'.encode(),b'NORMAL')
            भेजें('i두 번째 खिड़की\n'.encode(),b'INSERT')
            भेजें(क्लिक_करना_बटन(180,12),b'TERMINAL FOCUS 1');हैंडल_घटना(.2)
            आदेश_मोड();भेजें(b':wq\r')
            assert b'one:/first' in शेल('echo "$NAME:$PWD"')
            assert 'मान = 21\r\nprint(मान * 2)'.encode() in शेल('cat 첫째.py')
            परिणाम=शेल('python 첫째.py');assert b'42\r\n' in परिणाम,परिणाम
            # Close the first shell with its actual title-bar X; second editor resumes.
            भेजें(क्लिक_करना_बटन(560,63),b'TERMINAL FOCUS 2');हैंडल_घटना(.2)
            आदेश_मोड();भेजें(b':wq\r')
            assert b'two:/' in शेल('echo "$NAME:$PWD"')
            assert '두 번째 खिड़की'.encode() in शेल('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            भेजें('vi 둘째.txt\n'.encode(),b'NORMAL');भेजें(b'xu',b'NORMAL')
            भेजें(b'iX',b'INSERT');आदेश_मोड();भेजें(b':q\r',b'Unsaved')
            भेजें(b':q!\r');assert '두 번째 खिड़की'.encode() in शेल('cat 둘째.txt')
            भेजें(हॉट_की_मान(1),b'TERMINAL FOCUS 1');हैंडल_घटना(.2)
            भेजें(हॉट_की_मान(1),b'TERMINAL FOCUS 3');हैंडल_घटना(.2)
            भेजें(हॉट_की_मान(1),b'TERMINAL FOCUS 4');हैंडल_घटना(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            डेटा_पद.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));डेटा_पद.stdin.flush()
            शेल('echo DRAGGED_OK')
            भेजें('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            भेजें('i저장하지 않은 आँकड़े'.encode(),b'INSERT')
            भेजें(क्लिक_करना_बटन(578,97),b'TERMINAL FOCUS 3');हैंडल_घटना(.2)
            assert '버릴문서.txt'.encode() not in शेल('ls')
            भेजें(हॉट_की_मान(1),b'TERMINAL FOCUS 4');हैंडल_घटना(.2)
            शेल('echo REUSED_WINDOW_OK')
            पूर्ण_राशि=लॉग_रिकॉर्ड.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',पूर्ण_राशि)
            # UART completion precedes the next QEMU display refresh.
            समाप्त_करें_ऑफ़सेट=time.monotonic()+.3
            while time.monotonic()<समाप्त_करें_ऑफ़सेट:हैंडल_घटना(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_कोड:
                वर्ण_कोड.settimeout(10);वर्ण_कोड.connect(str(모의제어접속))
                with वर्ण_कोड.makefile('rwb') as फ़ाइल_एन्ट्री:
                    json.loads(फ़ाइल_एन्ट्री.readline())
                    for अनुरोध_मान in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(गंतव्य_मान_पद/'four-terminals.png'),'format':'png'}}):
                        फ़ाइल_एन्ट्री.write((json.dumps(अनुरोध_मान)+'\n').encode());फ़ाइल_एन्ट्री.flush()
                        while True:
                            반환값=json.loads(फ़ाइल_एन्ट्री.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(गंतव्य_मान_पद/'four-terminals.png')).convert('RGB')
            for समन्वय_जोड़ी,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(समन्वय_जोड़ी)==색상,(समन्वय_जोड़ी,화소들.getpixel(समन्वय_जोड़ी))
            शेल('echo FOUR_WINDOWS_OK')
            प्रमाणीकरण_रिपोर्ट.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if डेटा_पद.poll() is None:डेटा_पद.terminate()
            try:डेटा_पद.wait(timeout=5)
            except subprocess.TimeoutExpired:डेटा_पद.kill();डेटा_पद.wait()
            सिलेक्टर_a916db4e.close();डेटा_पद.stdin.close();डेटा_पद.stdout.close();(गंतव्य_मान_पद/'serial.log').write_bytes(लॉग_रिकॉर्ड);(गंतव्य_मान_पद/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाएँ()
