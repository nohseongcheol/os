#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ,આદેશ

def ચલાવો_2():
    ગંતવ્ય_મૂલ્ય_સ્થિતિ=પ્રોજેક્ટ_રૂટ/'build/verification/windows';ગંતવ્ય_મૂલ્ય_સ્થિતિ.mkdir(parents=True,exist_ok=True)
    માન્યતા_અહેવાલ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest()};લૉગ_પંક્તિ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ડેટા_સ્થિતિ=subprocess.Popen(આદેશ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        પસંદકર્તા_a916db4e=selectors.DefaultSelector();પસંદકર્તા_a916db4e.register(ડેટા_સ્થિતિ.stdout,selectors.EVENT_READ)
        def હેન્ડલ_ઇવેંટ(초단위=.1):
            for 누름값,_ in પસંદકર્તા_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:લૉગ_પંક્તિ.extend(둘째값)
            assert b'PANIC:' not in લૉગ_પંક્તિ and b'HALTED' not in લૉગ_પંક્તિ,લૉગ_પંક્તિ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            અંત_કરો_ઑફસેટ=time.monotonic()+초단위
            while 확인표시 not in લૉગ_પંક્તિ[현재위치:]:
                if time.monotonic()>અંત_કરો_ઑફસેટ or ડેટા_સ્થિતિ.poll() is not None:raise AssertionError(લૉગ_પંક્તિ[현재위치:].decode('utf-8','replace'))
                હેન્ડલ_ઇવેંટ()
            return bytes(લૉગ_પંક્તિ[현재위치:])
        def મોકલો(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(લૉગ_પંક્તિ);ડેટા_સ્થિતિ.stdin.write(둘째값);ડેટા_સ્થિતિ.stdin.flush();return 기다리기(확인표시,현재위치)
        def શેલ(સ્ટ્રિંગ_ડેટા):return મોકલો((સ્ટ્રિંગ_ડેટા+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def શૉર્ટકટ_મૂલ્ય(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ક્લિક_કરો_બટન(x_યામ,세로좌표):return bytes([30,1,1,x_યામ&255,x_યામ>>8,세로좌표&255,세로좌표>>8,30,1,0,x_યામ&255,x_યામ>>8,세로좌표&255,세로좌표>>8])
        def આદેશ_મોડ():
            ડેટા_સ્થિતિ.stdin.write(b'\x1b');ડેટા_સ્થિતિ.stdin.flush();અંત_કરો_ઑફસેટ=time.monotonic()+.2
            while time.monotonic()<અંત_કરો_ઑફસેટ:હેન્ડલ_ઇવેંટ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            શેલ('terminal');હેન્ડલ_ઇવેંટ(.3)
            શેલ('mkdir first; cd first; export NAME=one')
            મોકલો('vi 첫째.py\n'.encode(),b'NORMAL')
            મોકલો('i값 = 21\nprint(મૂલ્ય * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            અંત_કરો_ઑફસેટ=time.monotonic()+3
            while time.monotonic()<અંત_કરો_ઑફસેટ:હેન્ડલ_ઇવેંટ(.1)
            મોકલો(શૉર્ટકટ_મૂલ્ય(1),b'TERMINAL FOCUS 2');હેન્ડલ_ઇવેંટ(.2)
            assert b'/\r\n' in શેલ('pwd')
            શેલ('export NAME=two')
            મોકલો('vi 둘째.txt\n'.encode(),b'NORMAL')
            મોકલો('i두 번째 વિંડો\n'.encode(),b'INSERT')
            મોકલો(ક્લિક_કરો_બટન(180,12),b'TERMINAL FOCUS 1');હેન્ડલ_ઇવેંટ(.2)
            આદેશ_મોડ();મોકલો(b':wq\r')
            assert b'one:/first' in શેલ('echo "$NAME:$PWD"')
            assert 'મૂલ્ય = 21\r\nprint(મૂલ્ય * 2)'.encode() in શેલ('cat 첫째.py')
            પરિમાણ=શેલ('python 첫째.py');assert b'42\r\n' in પરિમાણ,પરિમાણ
            # Close the first shell with its actual title-bar X; second editor resumes.
            મોકલો(ક્લિક_કરો_બટન(560,63),b'TERMINAL FOCUS 2');હેન્ડલ_ઇવેંટ(.2)
            આદેશ_મોડ();મોકલો(b':wq\r')
            assert b'two:/' in શેલ('echo "$NAME:$PWD"')
            assert '두 번째 વિંડો'.encode() in શેલ('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            મોકલો('vi 둘째.txt\n'.encode(),b'NORMAL');મોકલો(b'xu',b'NORMAL')
            મોકલો(b'iX',b'INSERT');આદેશ_મોડ();મોકલો(b':q\r',b'Unsaved')
            મોકલો(b':q!\r');assert '두 번째 વિંડો'.encode() in શેલ('cat 둘째.txt')
            મોકલો(શૉર્ટકટ_મૂલ્ય(1),b'TERMINAL FOCUS 1');હેન્ડલ_ઇવેંટ(.2)
            મોકલો(શૉર્ટકટ_મૂલ્ય(1),b'TERMINAL FOCUS 3');હેન્ડલ_ઇવેંટ(.2)
            મોકલો(શૉર્ટકટ_મૂલ્ય(1),b'TERMINAL FOCUS 4');હેન્ડલ_ઇવેંટ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ડેટા_સ્થિતિ.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ડેટા_સ્થિતિ.stdin.flush()
            શેલ('echo DRAGGED_OK')
            મોકલો('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            મોકલો('i저장하지 않은 ડેટા'.encode(),b'INSERT')
            મોકલો(ક્લિક_કરો_બટન(578,97),b'TERMINAL FOCUS 3');હેન્ડલ_ઇવેંટ(.2)
            assert '버릴문서.txt'.encode() not in શેલ('ls')
            મોકલો(શૉર્ટકટ_મૂલ્ય(1),b'TERMINAL FOCUS 4');હેન્ડલ_ઇવેંટ(.2)
            શેલ('echo REUSED_WINDOW_OK')
            완료량=લૉગ_પંક્તિ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            અંત_કરો_ઑફસેટ=time.monotonic()+.3
            while time.monotonic()<અંત_કરો_ઑફસેટ:હેન્ડલ_ઇવેંટ(.05)
            with socket.socket(socket.AF_UNIX) as વર્ણ_કોડ:
                વર્ણ_કોડ.settimeout(10);વર્ણ_કોડ.connect(str(모의제어접속))
                with વર્ણ_કોડ.makefile('rwb') as ફાઇલ_પ્રવેશ:
                    json.loads(ફાઇલ_પ્રવેશ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ગંતવ્ય_મૂલ્ય_સ્થિતિ/'four-terminals.png'),'format':'png'}}):
                        ફાઇલ_પ્રવેશ.write((json.dumps(요청값)+'\n').encode());ફાઇલ_પ્રવેશ.flush()
                        while True:
                            반환값=json.loads(ફાઇલ_પ્રવેશ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ગંતવ્ય_મૂલ્ય_સ્થિતિ/'four-terminals.png')).convert('RGB')
            for યામ_જોડ,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(યામ_જોડ)==색상,(યામ_જોડ,화소들.getpixel(યામ_જોડ))
            શેલ('echo FOUR_WINDOWS_OK')
            માન્યતા_અહેવાલ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ડેટા_સ્થિતિ.poll() is None:ડેટા_સ્થિતિ.terminate()
            try:ડેટા_સ્થિતિ.wait(timeout=5)
            except subprocess.TimeoutExpired:ડેટા_સ્થિતિ.kill();ડેટા_સ્થિતિ.wait()
            પસંદકર્તા_a916db4e.close();ડેટા_સ્થિતિ.stdin.close();ડેટા_સ્થિતિ.stdout.close();(ગંતવ્ય_મૂલ્ય_સ્થિતિ/'serial.log').write_bytes(લૉગ_પંક્તિ);(ગંતવ્ય_મૂલ્ય_સ્થિતિ/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ચલાવો_2()
