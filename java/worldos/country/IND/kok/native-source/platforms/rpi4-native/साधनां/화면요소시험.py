#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट,आदेश

def चलोवप():
    नियुक्त_स्थान_मोल_स्थिती=प्रॉजॅक्ट_रूट/'build/verification/swing';नियुक्त_स्थान_मोल_स्थिती.mkdir(parents=True,exist_ok=True)
    वर्ग_पाथ=प्रॉजॅक्ट_रूट/'build/verification/new-java';वर्ग_पाथ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(प्रॉजॅक्ट_रूट/'dist/jkoros-native-korean.jar'),'-d',str(वर्ग_पाथ),str(प्रॉजॅक्ट_रूट/'시험/자바/스윙시험.java'),str(प्रॉजॅक्ट_रूट/'시험/자바/한글창시험.java')])
    वैधताय_अहवाल={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((प्रॉजॅक्ट_रूट/'build/kernel8.img').read_bytes()).hexdigest()};LOG_नोंद=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        डेटा_स्थिती=subprocess.Popen(आदेश()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        वेंचक_a916db4e=selectors.DefaultSelector();वेंचक_a916db4e.register(डेटा_स्थिती.stdout,selectors.EVENT_READ)
        def हँडल_प्रसंग(초단위=.1):
            for 누름값,_ in वेंचक_a916db4e.select(초단위):
                SECOND_मोल=누름값.fileobj.read(65536)
                if SECOND_मोल:LOG_नोंद.extend(SECOND_मोल)
            assert b'PANIC:' not in LOG_नोंद and b'HALTED' not in LOG_नोंद,LOG_नोंद[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            सोपोवचें_ऑफसॅट=time.monotonic()+초단위
            while 확인표시 not in LOG_नोंद[현재위치:]:
                if time.monotonic()>सोपोवचें_ऑफसॅट or डेटा_स्थिती.poll() is not None:raise AssertionError(LOG_नोंद[현재위치:].decode('utf-8','replace'))
                हँडल_प्रसंग()
            return bytes(LOG_नोंद[현재위치:])
        def धाडचें(SECOND_मोल,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_नोंद);डेटा_स्थिती.stdin.write(SECOND_मोल);डेटा_स्थिती.stdin.flush();return 기다리기(확인표시,현재위치)
        def शॅल(स्ट्रिंग_डेटा):return धाडचें((स्ट्रिंग_डेटा+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def आडवाट_मोल(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def क्लिक_करचें_बटन(x_coordinate,세로좌표):return bytes([30,1,1,x_coordinate&255,x_coordinate>>8,세로좌표&255,세로좌표>>8,30,1,0,x_coordinate&255,x_coordinate>>8,세로좌표&255,세로좌표>>8])
        def आदेश_मोड():
            डेटा_स्थिती.stdin.write(b'\x1b');डेटा_स्थिती.stdin.flush();सोपोवचें_ऑफसॅट=time.monotonic()+.2
            while time.monotonic()<सोपोवचें_ऑफसॅट:हँडल_प्रसंग(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            शॅल('terminal');हँडल_प्रसंग(.3)
            डेटा=(प्रॉजॅक्ट_रूट/'build/verification/new-java/스윙시험.class').read_bytes()
            धाडचें('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(डेटा),64):धाडचें(डेटा[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            धाडचें(b'.\n')
            धाडचें('java 스윙시험\n'.encode(),b'SWING READY')
            सोपोवचें_ऑफसॅट=time.monotonic()+3
            while time.monotonic()<सोपोवचें_ऑफसॅट:हँडल_प्रसंग(.1)
            # JFrame centered at (120,100), content at y=130.
            धाडचें(क्लिक_करचें_बटन(200,210),b'',)  # focus JTextField
            डेटा_स्थिती.stdin.write('누리'.encode());डेटा_स्थिती.stdin.flush()
            सोपोवचें_ऑफसॅट=time.monotonic()+.3
            while time.monotonic()<सोपोवचें_ऑफसॅट:हँडल_प्रसंग(.05)
            मेजप=धाडचें(क्लिक_करचें_बटन(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_नोंद)-len(मेजप))
            धाडचें(आडवाट_मोल(1),b'TERMINAL FOCUS 2')
            मेजप=शॅल('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in मेजप
            धाडचें(क्लिक_करचें_बटन(180,12),b'TERMINAL FOCUS 1')
            सोपोवचें_ऑफसॅट=time.monotonic()+.3
            while time.monotonic()<सोपोवचें_ऑफसॅट:हँडल_प्रसंग(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_कोड:
                वर्ण_कोड.settimeout(10);वर्ण_कोड.connect(str(모의제어접속))
                with वर्ण_कोड.makefile('rwb') as फायल_प्रवेश:
                    json.loads(फायल_प्रवेश.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(नियुक्त_स्थान_मोल_स्थिती/'native-swing.png'),'format':'png'}}):
                        फायल_प्रवेश.write((json.dumps(요청값)+'\n').encode());फायल_प्रवेश.flush()
                        while True:
                            반환값=json.loads(फायल_प्रवेश.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            धाडचें(क्लिक_करचें_बटन(505,115))
            शॅल('echo SWING_CLOSED_OK')
            डेटा=(वर्ग_पाथ/'한글창시험.class').read_bytes()
            धाडचें('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(डेटा),64):धाडचें(डेटा[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            धाडचें(b'.\n')
            धाडचें('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            धाडचें(क्लिक_करचें_बटन(200,255),'KOREAN SWING CLICK नांव'.encode())
            धाडचें(क्लिक_करचें_बटन(505,115))
            शॅल('echo KOREAN_SWING_CLOSED_OK')
            वैधताय_अहवाल.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 विंडो/बटन/동작알림/प्रसंग_प्रतिक्षावळ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if डेटा_स्थिती.poll() is None:डेटा_स्थिती.terminate()
            try:डेटा_स्थिती.wait(timeout=5)
            except subprocess.TimeoutExpired:डेटा_स्थिती.kill();डेटा_स्थिती.wait()
            वेंचक_a916db4e.close();डेटा_स्थिती.stdin.close();डेटा_स्थिती.stdout.close();(नियुक्त_स्थान_मोल_स्थिती/'serial.log').write_bytes(LOG_नोंद);(नियुक्त_स्थान_मोल_स्थिती/'report.json').write_text(json.dumps(वैधताय_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलोवप()
