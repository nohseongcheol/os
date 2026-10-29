#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट,आदेश

def चलाउनुहोस्():
    गन्तव्य_मान_राख्नुहोस्=परियोजना_रूट/'build/verification/windows';गन्तव्य_मान_राख्नुहोस्.mkdir(parents=True,exist_ok=True)
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
            शेल('mkdir first; cd first; export NAME=one')
            पठाउनुहोस्('vi 첫째.py\n'.encode(),b'NORMAL')
            पठाउनुहोस्('i값 = 21\nprint(मान * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+3
            while time.monotonic()<समाप्त_गर्नुहोस्_अफसेट:ह्यान्डल_घटना(.1)
            पठाउनुहोस्(सर्टकट_मान(1),b'TERMINAL FOCUS 2');ह्यान्डल_घटना(.2)
            assert b'/\r\n' in शेल('pwd')
            शेल('export NAME=two')
            पठाउनुहोस्('vi 둘째.txt\n'.encode(),b'NORMAL')
            पठाउनुहोस्('i두 번째 सन्झ्याल\n'.encode(),b'INSERT')
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(180,12),b'TERMINAL FOCUS 1');ह्यान्डल_घटना(.2)
            आदेश_मोड();पठाउनुहोस्(b':wq\r')
            assert b'one:/first' in शेल('echo "$NAME:$PWD"')
            assert 'मान = 21\r\nprint(मान * 2)'.encode() in शेल('cat 첫째.py')
            मापन=शेल('python 첫째.py');assert b'42\r\n' in मापन,मापन
            # Close the first shell with its actual title-bar X; second editor resumes.
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(560,63),b'TERMINAL FOCUS 2');ह्यान्डल_घटना(.2)
            आदेश_मोड();पठाउनुहोस्(b':wq\r')
            assert b'two:/' in शेल('echo "$NAME:$PWD"')
            assert '두 번째 सन्झ्याल'.encode() in शेल('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            पठाउनुहोस्('vi 둘째.txt\n'.encode(),b'NORMAL');पठाउनुहोस्(b'xu',b'NORMAL')
            पठाउनुहोस्(b'iX',b'INSERT');आदेश_मोड();पठाउनुहोस्(b':q\r',b'Unsaved')
            पठाउनुहोस्(b':q!\r');assert '두 번째 सन्झ्याल'.encode() in शेल('cat 둘째.txt')
            पठाउनुहोस्(सर्टकट_मान(1),b'TERMINAL FOCUS 1');ह्यान्डल_घटना(.2)
            पठाउनुहोस्(सर्टकट_मान(1),b'TERMINAL FOCUS 3');ह्यान्डल_घटना(.2)
            पठाउनुहोस्(सर्टकट_मान(1),b'TERMINAL FOCUS 4');ह्यान्डल_घटना(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            लगत_राख्नुहोस्.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));लगत_राख्नुहोस्.stdin.flush()
            शेल('echo DRAGGED_OK')
            पठाउनुहोस्('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            पठाउनुहोस्('i저장하지 않은 लगत'.encode(),b'INSERT')
            पठाउनुहोस्(क्लिक_गर्नुहोस्_बटन(578,97),b'TERMINAL FOCUS 3');ह्यान्डल_घटना(.2)
            assert '버릴문서.txt'.encode() not in शेल('ls')
            पठाउनुहोस्(सर्टकट_मान(1),b'TERMINAL FOCUS 4');ह्यान्डल_घटना(.2)
            शेल('echo REUSED_WINDOW_OK')
            완료량=लग_रेकर्ड.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            समाप्त_गर्नुहोस्_अफसेट=time.monotonic()+.3
            while time.monotonic()<समाप्त_गर्नुहोस्_अफसेट:ह्यान्डल_घटना(.05)
            with socket.socket(socket.AF_UNIX) as वर्ण_सङ्केत:
                वर्ण_सङ्केत.settimeout(10);वर्ण_सङ्केत.connect(str(모의제어접속))
                with वर्ण_सङ्केत.makefile('rwb') as फाइल_प्रविष्टि:
                    json.loads(फाइल_प्रविष्टि.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(गन्तव्य_मान_राख्नुहोस्/'four-terminals.png'),'format':'png'}}):
                        फाइल_प्रविष्टि.write((json.dumps(요청값)+'\n').encode());फाइल_प्रविष्टि.flush()
                        while True:
                            반환값=json.loads(फाइल_प्रविष्टि.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(गन्तव्य_मान_राख्नुहोस्/'four-terminals.png')).convert('RGB')
            for समन्वय_गर्ने_जोडी,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(समन्वय_गर्ने_जोडी)==색상,(समन्वय_गर्ने_जोडी,화소들.getpixel(समन्वय_गर्ने_जोडी))
            शेल('echo FOUR_WINDOWS_OK')
            वैधानिकता_रिपोर्ट.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if लगत_राख्नुहोस्.poll() is None:लगत_राख्नुहोस्.terminate()
            try:लगत_राख्नुहोस्.wait(timeout=5)
            except subprocess.TimeoutExpired:लगत_राख्नुहोस्.kill();लगत_राख्नुहोस्.wait()
            चयनकर्ता_a916db4e.close();लगत_राख्नुहोस्.stdin.close();लगत_राख्नुहोस्.stdout.close();(गन्तव्य_मान_राख्नुहोस्/'serial.log').write_bytes(लग_रेकर्ड);(गन्तव्य_मान_राख्नुहोस्/'report.json').write_text(json.dumps(वैधानिकता_रिपोर्ट,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':चलाउनुहोस्()
