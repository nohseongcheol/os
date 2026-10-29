#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ,حکم

def چلائیں():
    منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں=عکس_ڈالنا_روٹ/'build/verification/windows';منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں.mkdir(parents=True,exist_ok=True)
    توثیق_رپورٹ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((عکس_ڈالنا_روٹ/'build/kernel8.img').read_bytes()).hexdigest()};لاگ_صف=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        کوائف_پوزیشن_ٹھیک_کریں=subprocess.Popen(حکم()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        منتخب_کنندہ_a916db4e=selectors.DefaultSelector();منتخب_کنندہ_a916db4e.register(کوائف_پوزیشن_ٹھیک_کریں.stdout,selectors.EVENT_READ)
        def ہینڈل_ایونٹ(초단위=.1):
            for 누름값,_ in منتخب_کنندہ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:لاگ_صف.extend(둘째값)
            assert b'PANIC:' not in لاگ_صف and b'HALTED' not in لاگ_صف,لاگ_صف[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            اختتام_آفسٹ=time.monotonic()+초단위
            while 확인표시 not in لاگ_صف[현재위치:]:
                if time.monotonic()>اختتام_آفسٹ or کوائف_پوزیشن_ٹھیک_کریں.poll() is not None:raise AssertionError(لاگ_صف[현재위치:].decode('utf-8','replace'))
                ہینڈل_ایونٹ()
            return bytes(لاگ_صف[현재위치:])
        def بھیجیں(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(لاگ_صف);کوائف_پوزیشن_ٹھیک_کریں.stdin.write(둘째값);کوائف_پوزیشن_ٹھیک_کریں.stdin.flush();return 기다리기(확인표시,현재위치)
        def شیل(سلک_کوائف):return بھیجیں((سلک_کوائف+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def تیز_راہ_قدر(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def کلک_بٹن(ایکس_مربوط,세로좌표):return bytes([30,1,1,ایکس_مربوط&255,ایکس_مربوط>>8,세로좌표&255,세로좌표>>8,30,1,0,ایکس_مربوط&255,ایکس_مربوط>>8,세로좌표&255,세로좌표>>8])
        def حکم_موڈ():
            کوائف_پوزیشن_ٹھیک_کریں.stdin.write(b'\x1b');کوائف_پوزیشن_ٹھیک_کریں.stdin.flush();اختتام_آفسٹ=time.monotonic()+.2
            while time.monotonic()<اختتام_آفسٹ:ہینڈل_ایونٹ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            شیل('terminal');ہینڈل_ایونٹ(.3)
            شیل('mkdir first; cd first; export NAME=one')
            بھیجیں('vi 첫째.py\n'.encode(),b'NORMAL')
            بھیجیں('i값 = 21\nprint(قدر * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            اختتام_آفسٹ=time.monotonic()+3
            while time.monotonic()<اختتام_آفسٹ:ہینڈل_ایونٹ(.1)
            بھیجیں(تیز_راہ_قدر(1),b'TERMINAL FOCUS 2');ہینڈل_ایونٹ(.2)
            assert b'/\r\n' in شیل('pwd')
            شیل('export NAME=two')
            بھیجیں('vi 둘째.txt\n'.encode(),b'NORMAL')
            بھیجیں('i두 번째 ونڈو\n'.encode(),b'INSERT')
            بھیجیں(کلک_بٹن(180,12),b'TERMINAL FOCUS 1');ہینڈل_ایونٹ(.2)
            حکم_موڈ();بھیجیں(b':wq\r')
            assert b'one:/first' in شیل('echo "$NAME:$PWD"')
            assert 'قدر = 21\r\nprint(قدر * 2)'.encode() in شیل('cat 첫째.py')
            پیمائش=شیل('python 첫째.py');assert b'42\r\n' in پیمائش,پیمائش
            # Close the first shell with its actual title-bar X; second editor resumes.
            بھیجیں(کلک_بٹن(560,63),b'TERMINAL FOCUS 2');ہینڈل_ایونٹ(.2)
            حکم_موڈ();بھیجیں(b':wq\r')
            assert b'two:/' in شیل('echo "$NAME:$PWD"')
            assert '두 번째 ونڈو'.encode() in شیل('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            بھیجیں('vi 둘째.txt\n'.encode(),b'NORMAL');بھیجیں(b'xu',b'NORMAL')
            بھیجیں(b'iX',b'INSERT');حکم_موڈ();بھیجیں(b':q\r',b'Unsaved')
            بھیجیں(b':q!\r');assert '두 번째 ونڈو'.encode() in شیل('cat 둘째.txt')
            بھیجیں(تیز_راہ_قدر(1),b'TERMINAL FOCUS 1');ہینڈل_ایونٹ(.2)
            بھیجیں(تیز_راہ_قدر(1),b'TERMINAL FOCUS 3');ہینڈل_ایونٹ(.2)
            بھیجیں(تیز_راہ_قدر(1),b'TERMINAL FOCUS 4');ہینڈل_ایونٹ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            کوائف_پوزیشن_ٹھیک_کریں.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));کوائف_پوزیشن_ٹھیک_کریں.stdin.flush()
            شیل('echo DRAGGED_OK')
            بھیجیں('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            بھیجیں('i저장하지 않은 کوائف'.encode(),b'INSERT')
            بھیجیں(کلک_بٹن(578,97),b'TERMINAL FOCUS 3');ہینڈل_ایونٹ(.2)
            assert '버릴문서.txt'.encode() not in شیل('ls')
            بھیجیں(تیز_راہ_قدر(1),b'TERMINAL FOCUS 4');ہینڈل_ایونٹ(.2)
            شیل('echo REUSED_WINDOW_OK')
            완료량=لاگ_صف.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            اختتام_آفسٹ=time.monotonic()+.3
            while time.monotonic()<اختتام_آفسٹ:ہینڈل_ایونٹ(.05)
            with socket.socket(socket.AF_UNIX) as کریکٹر_ضابطہ:
                کریکٹر_ضابطہ.settimeout(10);کریکٹر_ضابطہ.connect(str(모의제어접속))
                with کریکٹر_ضابطہ.makefile('rwb') as فائل_اندراج:
                    json.loads(فائل_اندراج.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں/'four-terminals.png'),'format':'png'}}):
                        فائل_اندراج.write((json.dumps(요청값)+'\n').encode());فائل_اندراج.flush()
                        while True:
                            반환값=json.loads(فائل_اندراج.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں/'four-terminals.png')).convert('RGB')
            for معدد_جوڑا,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(معدد_جوڑا)==색상,(معدد_جوڑا,화소들.getpixel(معدد_جوڑا))
            شیل('echo FOUR_WINDOWS_OK')
            توثیق_رپورٹ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if کوائف_پوزیشن_ٹھیک_کریں.poll() is None:کوائف_پوزیشن_ٹھیک_کریں.terminate()
            try:کوائف_پوزیشن_ٹھیک_کریں.wait(timeout=5)
            except subprocess.TimeoutExpired:کوائف_پوزیشن_ٹھیک_کریں.kill();کوائف_پوزیشن_ٹھیک_کریں.wait()
            منتخب_کنندہ_a916db4e.close();کوائف_پوزیشن_ٹھیک_کریں.stdin.close();کوائف_پوزیشن_ٹھیک_کریں.stdout.close();(منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں/'serial.log').write_bytes(لاگ_صف);(منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں/'report.json').write_text(json.dumps(توثیق_رپورٹ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':چلائیں()
