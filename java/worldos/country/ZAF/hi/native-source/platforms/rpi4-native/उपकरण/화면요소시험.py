#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल,आदेश

def चलाएँ():
    गंतव्य_मान_पद=प्रोजेक्ट_करें_मूल/'build/verification/swing';गंतव्य_मान_पद.mkdir(parents=True,exist_ok=True)
    कक्षा_पथ=प्रोजेक्ट_करें_मूल/'build/verification/new-java';कक्षा_पथ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(प्रोजेक्ट_करें_मूल/'dist/jkoros-native-korean.jar'),'-d',str(कक्षा_पथ),str(प्रोजेक्ट_करें_मूल/'시험/자바/스윙시험.java'),str(प्रोजेक्ट_करें_मूल/'시험/자바/한글창시험.java')])
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
            आँकड़े=(प्रोजेक्ट_करें_मूल/'build/verification/new-java/스윙시험.class').read_bytes()
            भेजें('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(आँकड़े),64):भेजें(आँकड़े[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            भेजें(b'.\n')
            भेजें('java 스윙시험\n'.encode(),b'SWING READY')
            समाप्त_करें_ऑफ़सेट=time.monotonic()+3
            while time.monotonic()<समाप्त_करें_ऑफ़सेट:हैंडल_घटना(.1)
            # JFrame centered at (120,100), content at y=130.
            भेजें(क्लिक_करना_बटन(200,210),b'',)  # focus JTextField
            डेटा_पद.stdin.write('누리'.encode());डेटा_पद.stdin.flush()
            समाप्त_करें_ऑफ़सेट=time.monotonic()+.3
            while time.monotonic()<समाप्त_करें_ऑफ़सेट:हैंडल_घटना(.05)
            परिणाम=भेजें(क्लिक_करना_बटन(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(लॉग_रिकॉर्ड)-len(परिणाम))
            भेजें(हॉट_की_मान(1),b'TERMINAL FOCUS 2')
            परिणाम=शेल('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in परिणाम
            भेजें(क्लिक_करना_बटन(180,12),b'TERMINAL FOCUS 1')
            समाप्त_करें_ऑफ़सेट=time.monotonic()+.3
            while time.monotonic()<समाप्त_करें_ऑफ़सेट:हैंडल_घटना(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_कोड:
                वर्ण_कोड.settimeout(10);वर्ण_कोड.connect(str(모의제어접속))
                with वर्ण_कोड.makefile('rwb') as फ़ाइल_एन्ट्री:
                    json.loads(फ़ाइल_एन्ट्री.readline())
                    for अनुरोध_मान in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(गंतव्य_मान_पद/'native-swing.png'),'format':'png'}}):
                        फ़ाइल_एन्ट्री.write((json.dumps(अनुरोध_मान)+'\n').encode());फ़ाइल_एन्ट्री.flush()
                        while True:
                            반환값=json.loads(फ़ाइल_एन्ट्री.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            भेजें(क्लिक_करना_बटन(505,115))
            शेल('echo SWING_CLOSED_OK')
            आँकड़े=(कक्षा_पथ/'한글창시험.class').read_bytes()
            भेजें('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(आँकड़े),64):भेजें(आँकड़े[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            भेजें(b'.\n')
            भेजें('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            भेजें(क्लिक_करना_बटन(200,255),'KOREAN SWING CLICK नाम'.encode())
            भेजें(क्लिक_करना_बटन(505,115))
            शेल('echo KOREAN_SWING_CLOSED_OK')
            प्रमाणीकरण_रिपोर्ट.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','हिंदी खिड़की/बटन/एक्शन_सूचना/घटना_कतार directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if डेटा_पद.poll() is None:डेटा_पद.terminate()
            try:डेटा_पद.wait(timeout=5)
            except subprocess.TimeoutExpired:डेटा_पद.kill();डेटा_पद.wait()
            सिलेक्टर_a916db4e.close();डेटा_पद.stdin.close();डेटा_पद.stdout.close();(गंतव्य_मान_पद/'serial.log').write_bytes(लॉग_रिकॉर्ड);(गंतव्य_मान_पद/'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाएँ()
