#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट,आदेश

def चलाउनुहोस्():
    गन्तव्य_मान_राख्नुहोस्=परियोजना_रूट/'build/verification/swing';गन्तव्य_मान_राख्नुहोस्.mkdir(parents=True,exist_ok=True)
    वर्ग_बाटो=परियोजना_रूट/'build/verification/new-java';वर्ग_बाटो.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(परियोजना_रूट/'dist/jkoros-native-korean.jar'),'-d',str(वर्ग_बाटो),str(परियोजना_रूट/'시험/자바/스윙시험.java'),str(परियोजना_रूट/'시험/자바/한글창시험.java')])
    वैधानिकता_रिपोर्ट={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((परियोजना_रूट/'build/kernel8.img').read_bytes()).hexdigest()};लग_रेकर्ड=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        लगत_राख्नुहोस्=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        चयनकर्ता_a916db4e=selectors.DefaultSelector();चयनकर्ता_a916db4e.register(लगत_राख्नुहोस्.stdout,selectors.EVENT_READ)
        def ह्यान्डल_घटना(초단위=.1):
            for 누름값,_ in चयनकर्ता_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:लग_रेकर्ड.extend(둘째값)
            assert b'PANIC:' not in लग_रेकर्ड and b'HALTED' not in लग_रेकर्ड,लग_रेकर्ड[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+초단위
            while 확인표시 not in लग_रेकर्ड[현재위치:]:
                if time.monotonic()>समाप्त_गर्नुहोस्_अफसेट or लगत_राख्नुहोस्.poll() is not None:raise AssertionError(लग_रेकर्ड[현재위치:].decode('utf-8','replace'))
                ह्यान्डल_घटना()
            return bytes(लग_रेकर्ड[현재위치:])
        def पठाउनुहोस्(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(लग_रेकर्ड);लगत_राख्नुहोस्.stdin.write(둘째값);लगत_राख्नुहोस्.stdin.flush();return 기다리기(확인표시,현재위치)
        def शेल(स्ट्रिङ_लगत):return पठाउनुहोस्((स्ट्रिङ_लगत+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def सर्टकट_मान(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def क्लिक_गर्नुहोस्_बटन(x_समन्वय,세로좌표):return bytes([30,1,1,x_समन्वय&255,x_समन्वय>>8,세로좌표&255,세로좌표>>8,30,1,0,x_समन्वय&255,x_समन्वय>>8,세로좌표&255,세로좌표>>8])
        def आदेश_मोड():
            लगत_राख्नुहोस्.stdin.write(b'\x1b');लगत_राख्नुहोस्.stdin.flush();समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+.2
            while time.monotonic()<समाप्त_गर्नुहोस्_अफसेट:ह्यान्डल_घटना(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            शेल('terminal');ह्यान्डल_घटना(.3)
            लगत=(परियोजना_रूट/'build/verification/new-java/스윙시험.class').read_bytes()
            पठाउनुहोस्('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(लगत),64):पठाउनुहोस्(लगत[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            पठाउनुहोस्(b'.\n')
            पठाउनुहोस्('java 스윙시험\n'.encode(),b'SWING READY')
            समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+3
            while time.monotonic()<समाप्त_गर्नुहोस्_अफसेट:ह्यान्डल_घटना(.1)
            # JFrame centered at (120,100), content at y=130.
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(200,210),b'',)  # focus JTextField
            लगत_राख्नुहोस्.stdin.write('누리'.encode());लगत_राख्नुहोस्.stdin.flush()
            समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+.3
            while time.monotonic()<समाप्त_गर्नुहोस्_अफसेट:ह्यान्डल_घटना(.05)
            मापन=पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(लग_रेकर्ड)-len(मापन))
            पठाउनुहोस्(सर्टकट_मान(1),b'TERMINAL FOCUS 2')
            मापन=शेल('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in मापन
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(180,12),b'TERMINAL FOCUS 1')
            समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+.3
            while time.monotonic()<समाप्त_गर्नुहोस्_अफसेट:ह्यान्डल_घटना(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_सङ्केत:
                वर्ण_सङ्केत.settimeout(10);वर्ण_सङ्केत.connect(str(모의제어접속))
                with वर्ण_सङ्केत.makefile('rwb') as फाइल_प्रविष्टि:
                    json.loads(फाइल_प्रविष्टि.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(गन्तव्य_मान_राख्नुहोस्/'native-swing.png'),'format':'png'}}):
                        फाइल_प्रविष्टि.write((json.dumps(요청값)+'\n').encode());फाइल_प्रविष्टि.flush()
                        while True:
                            반환값=json.loads(फाइल_प्रविष्टि.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(505,115))
            शेल('echo SWING_CLOSED_OK')
            लगत=(वर्ग_बाटो/'한글창시험.class').read_bytes()
            पठाउनुहोस्('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(लगत),64):पठाउनुहोस्(लगत[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            पठाउनुहोस्(b'.\n')
            पठाउनुहोस्('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(200,255),'KOREAN SWING CLICK नाम'.encode())
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(505,115))
            शेल('echo KOREAN_SWING_CLOSED_OK')
            वैधानिकता_रिपोर्ट.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','नेपाली सन्झ्याल/बटन/동작알림/घटना_लाइन directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if लगत_राख्नुहोस्.poll() is None:लगत_राख्नुहोस्.terminate()
            try:लगत_राख्नुहोस्.wait(timeout=5)
            except subprocess.TimeoutExpired:लगत_राख्नुहोस्.kill();लगत_राख्नुहोस्.wait()
            चयनकर्ता_a916db4e.close();लगत_राख्नुहोस्.stdin.close();लगत_राख्नुहोस्.stdout.close();(गन्तव्य_मान_राख्नुहोस्/'serial.log').write_bytes(लग_रेकर्ड);(गन्तव्य_मान_राख्नुहोस्/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाउनुहोस्()
