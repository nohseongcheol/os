#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट,आदेश

def चलोवप():
    नियुक्त_स्थान_मोल_स्थिती=प्रॉजॅक्ट_रूट/'build/verification/windows';नियुक्त_स्थान_मोल_स्थिती.mkdir(parents=True,exist_ok=True)
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
            शॅल('mkdir first; cd first; export NAME=one')
            धाडचें('vi 첫째.py\n'.encode(),b'NORMAL')
            धाडचें('i값 = 21\nprint(मोल * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            सोपोवचें_ऑफसॅट=time.monotonic()+3
            while time.monotonic()<सोपोवचें_ऑफसॅट:हँडल_प्रसंग(.1)
            धाडचें(आडवाट_मोल(1),b'TERMINAL FOCUS 2');हँडल_प्रसंग(.2)
            assert b'/\r\n' in शॅल('pwd')
            शॅल('export NAME=two')
            धाडचें('vi 둘째.txt\n'.encode(),b'NORMAL')
            धाडचें('i두 번째 विंडो\n'.encode(),b'INSERT')
            धाडचें(क्लिक_करचें_बटन(180,12),b'TERMINAL FOCUS 1');हँडल_प्रसंग(.2)
            आदेश_मोड();धाडचें(b':wq\r')
            assert b'one:/first' in शॅल('echo "$NAME:$PWD"')
            assert 'मोल = 21\r\nprint(मोल * 2)'.encode() in शॅल('cat 첫째.py')
            मेजप=शॅल('python 첫째.py');assert b'42\r\n' in मेजप,मेजप
            # Close the first shell with its actual title-bar X; second editor resumes.
            धाडचें(क्लिक_करचें_बटन(560,63),b'TERMINAL FOCUS 2');हँडल_प्रसंग(.2)
            आदेश_मोड();धाडचें(b':wq\r')
            assert b'two:/' in शॅल('echo "$NAME:$PWD"')
            assert '두 번째 विंडो'.encode() in शॅल('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            धाडचें('vi 둘째.txt\n'.encode(),b'NORMAL');धाडचें(b'xu',b'NORMAL')
            धाडचें(b'iX',b'INSERT');आदेश_मोड();धाडचें(b':q\r',b'Unsaved')
            धाडचें(b':q!\r');assert '두 번째 विंडो'.encode() in शॅल('cat 둘째.txt')
            धाडचें(आडवाट_मोल(1),b'TERMINAL FOCUS 1');हँडल_प्रसंग(.2)
            धाडचें(आडवाट_मोल(1),b'TERMINAL FOCUS 3');हँडल_प्रसंग(.2)
            धाडचें(आडवाट_मोल(1),b'TERMINAL FOCUS 4');हँडल_प्रसंग(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            डेटा_स्थिती.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));डेटा_स्थिती.stdin.flush()
            शॅल('echo DRAGGED_OK')
            धाडचें('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            धाडचें('i저장하지 않은 डेटा'.encode(),b'INSERT')
            धाडचें(क्लिक_करचें_बटन(578,97),b'TERMINAL FOCUS 3');हँडल_प्रसंग(.2)
            assert '버릴문서.txt'.encode() not in शॅल('ls')
            धाडचें(आडवाट_मोल(1),b'TERMINAL FOCUS 4');हँडल_प्रसंग(.2)
            शॅल('echo REUSED_WINDOW_OK')
            완료량=LOG_नोंद.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            सोपोवचें_ऑफसॅट=time.monotonic()+.3
            while time.monotonic()<सोपोवचें_ऑफसॅट:हँडल_प्रसंग(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_कोड:
                वर्ण_कोड.settimeout(10);वर्ण_कोड.connect(str(모의제어접속))
                with वर्ण_कोड.makefile('rwb') as फायल_प्रवेश:
                    json.loads(फायल_प्रवेश.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(नियुक्त_स्थान_मोल_स्थिती/'four-terminals.png'),'format':'png'}}):
                        फायल_प्रवेश.write((json.dumps(요청값)+'\n').encode());फायल_प्रवेश.flush()
                        while True:
                            반환값=json.loads(फायल_प्रवेश.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(नियुक्त_स्थान_मोल_स्थिती/'four-terminals.png')).convert('RGB')
            for कॉओर्डिनेट_पॅअर,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(कॉओर्डिनेट_पॅअर)==색상,(कॉओर्डिनेट_पॅअर,화소들.getpixel(कॉओर्डिनेट_पॅअर))
            शॅल('echo FOUR_WINDOWS_OK')
            वैधताय_अहवाल.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if डेटा_स्थिती.poll() is None:डेटा_स्थिती.terminate()
            try:डेटा_स्थिती.wait(timeout=5)
            except subprocess.TimeoutExpired:डेटा_स्थिती.kill();डेटा_स्थिती.wait()
            वेंचक_a916db4e.close();डेटा_स्थिती.stdin.close();डेटा_स्थिती.stdout.close();(नियुक्त_स्थान_मोल_स्थिती/'serial.log').write_bytes(LOG_नोंद);(नियुक्त_स्थान_मोल_स्थिती/'report.json').write_text(json.dumps(वैधताय_अहवाल,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलोवप()
