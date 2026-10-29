#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from نفاذ_کرو_حکم import 기준,حکم

def چلاؤ():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    جواز_دہی_رپورٹ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};لاگ_صف=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(حکم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        منتخب_کرنڑ_آلا_a916db4e=selectors.DefaultSelector();منتخب_کرنڑ_آلا_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def نبٹنا_واقعہ(초단위=.1):
            for 누름값,_ in منتخب_کرنڑ_آلا_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:لاگ_صف.extend(둘째값)
            assert b'PANIC:' not in لاگ_صف and b'HALTED' not in لاگ_صف,لاگ_صف[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ختم_کرو_آف_سیٹ=time.monotonic()+초단위
            while 확인표시 not in لاگ_صف[현재위치:]:
                if time.monotonic()>ختم_کرو_آف_سیٹ or 자료위치.poll() is not None:raise AssertionError(لاگ_صف[현재위치:].decode('utf-8','replace'))
                نبٹنا_واقعہ()
            return bytes(لاگ_صف[현재위치:])
        def بھیجو(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(لاگ_صف);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def شیل(سٹرنگ_کوائف):return بھیجو((سٹرنگ_کوائف+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def تیز_راہ_قدر(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def کلک_کرو_بٹن(x_محدد,세로좌표):return bytes([30,1,1,x_محدد&255,x_محدد>>8,세로좌표&255,세로좌표>>8,30,1,0,x_محدد&255,x_محدد>>8,세로좌표&255,세로좌표>>8])
        def حکم_موڈ():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();ختم_کرو_آف_سیٹ=time.monotonic()+.2
            while time.monotonic()<ختم_کرو_آف_سیٹ:نبٹنا_واقعہ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            شیل('terminal');نبٹنا_واقعہ(.3)
            شیل('mkdir first; cd first; export NAME=one')
            بھیجو('vi 첫째.py\n'.encode(),b'NORMAL')
            بھیجو('i값 = 21\nprint(قدر * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ختم_کرو_آف_سیٹ=time.monotonic()+3
            while time.monotonic()<ختم_کرو_آف_سیٹ:نبٹنا_واقعہ(.1)
            بھیجو(تیز_راہ_قدر(1),b'TERMINAL FOCUS 2');نبٹنا_واقعہ(.2)
            assert b'/\r\n' in شیل('pwd')
            شیل('export NAME=two')
            بھیجو('vi 둘째.txt\n'.encode(),b'NORMAL')
            بھیجو('i두 번째 کھڑکی\n'.encode(),b'INSERT')
            بھیجو(کلک_کرو_بٹن(180,12),b'TERMINAL FOCUS 1');نبٹنا_واقعہ(.2)
            حکم_موڈ();بھیجو(b':wq\r')
            assert b'one:/first' in شیل('echo "$NAME:$PWD"')
            assert 'قدر = 21\r\nprint(قدر * 2)'.encode() in شیل('cat 첫째.py')
            결과=شیل('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            بھیجو(کلک_کرو_بٹن(560,63),b'TERMINAL FOCUS 2');نبٹنا_واقعہ(.2)
            حکم_موڈ();بھیجو(b':wq\r')
            assert b'two:/' in شیل('echo "$NAME:$PWD"')
            assert '두 번째 کھڑکی'.encode() in شیل('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            بھیجو('vi 둘째.txt\n'.encode(),b'NORMAL');بھیجو(b'xu',b'NORMAL')
            بھیجو(b'iX',b'INSERT');حکم_موڈ();بھیجو(b':q\r',b'Unsaved')
            بھیجو(b':q!\r');assert '두 번째 کھڑکی'.encode() in شیل('cat 둘째.txt')
            بھیجو(تیز_راہ_قدر(1),b'TERMINAL FOCUS 1');نبٹنا_واقعہ(.2)
            بھیجو(تیز_راہ_قدر(1),b'TERMINAL FOCUS 3');نبٹنا_واقعہ(.2)
            بھیجو(تیز_راہ_قدر(1),b'TERMINAL FOCUS 4');نبٹنا_واقعہ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            شیل('echo DRAGGED_OK')
            بھیجو('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            بھیجو('i저장하지 않은 کوائف'.encode(),b'INSERT')
            بھیجو(کلک_کرو_بٹن(578,97),b'TERMINAL FOCUS 3');نبٹنا_واقعہ(.2)
            assert '버릴문서.txt'.encode() not in شیل('ls')
            بھیجو(تیز_راہ_قدر(1),b'TERMINAL FOCUS 4');نبٹنا_واقعہ(.2)
            شیل('echo REUSED_WINDOW_OK')
            완료량=لاگ_صف.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ختم_کرو_آف_سیٹ=time.monotonic()+.3
            while time.monotonic()<ختم_کرو_آف_سیٹ:نبٹنا_واقعہ(.05)
            with socket.socket(socket.AF_UNIX) as کیریکٹر_کوڈ:
                کیریکٹر_کوڈ.settimeout(10);کیریکٹر_کوڈ.connect(str(모의제어접속))
                with کیریکٹر_کوڈ.makefile('rwb') as فائل_داخلہ:
                    json.loads(فائل_داخلہ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        فائل_داخلہ.write((json.dumps(요청값)+'\n').encode());فائل_داخلہ.flush()
                        while True:
                            반환값=json.loads(فائل_داخلہ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for محددات_دی_جوڑی,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(محددات_دی_جوڑی)==색상,(محددات_دی_جوڑی,화소들.getpixel(محددات_دی_جوڑی))
            شیل('echo FOUR_WINDOWS_OK')
            جواز_دہی_رپورٹ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            منتخب_کرنڑ_آلا_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(لاگ_صف);(목적위치/'report.json').write_text(json.dumps(جواز_دہی_رپورٹ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':چلاؤ()
