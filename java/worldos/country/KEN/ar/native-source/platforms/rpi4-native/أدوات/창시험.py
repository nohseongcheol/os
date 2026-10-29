#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ينفذ_أمر import يعرض_جذر,أمر

def تشغيل():
    وجهة_قيمة_منصب=يعرض_جذر/'build/verification/windows';وجهة_قيمة_منصب.mkdir(parents=True,exist_ok=True)
    التحقق_من_صحة_إبلاغ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((يعرض_جذر/'build/kernel8.img').read_bytes()).hexdigest()};سجل_سجل=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        بيانات_منصب=subprocess.Popen(أمر()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        محدد_a916db4e=selectors.DefaultSelector();محدد_a916db4e.register(بيانات_منصب.stdout,selectors.EVENT_READ)
        def مؤشر_حدث(초단위=.1):
            for 누름값,_ in محدد_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:سجل_سجل.extend(둘째값)
            assert b'PANIC:' not in سجل_سجل and b'HALTED' not in سجل_سجل,سجل_سجل[-2048:]
        def 기다리기(علامة,حديث_منصب,초단위=50):
            إنهاء_مكالمة_إزاحة=time.monotonic()+초단위
            while علامة not in سجل_سجل[حديث_منصب:]:
                if time.monotonic()>إنهاء_مكالمة_إزاحة or بيانات_منصب.poll() is not None:raise AssertionError(سجل_سجل[حديث_منصب:].decode('utf-8','replace'))
                مؤشر_حدث()
            return bytes(سجل_سجل[حديث_منصب:])
        def يرسل(둘째값,علامة=b'jkoros-native> '):
            حديث_منصب=len(سجل_سجل);بيانات_منصب.stdin.write(둘째값);بيانات_منصب.stdin.flush();return 기다리기(علامة,حديث_منصب)
        def 셸(سلسلة_بيانات):return يرسل((سلسلة_بيانات+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def اختصار_قيمة(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def نقرة_زر(الإحداثي_س,الزر_Y_إحداثيات):return bytes([30,1,1,الإحداثي_س&255,الإحداثي_س>>8,الزر_Y_إحداثيات&255,الزر_Y_إحداثيات>>8,30,1,0,الإحداثي_س&255,الإحداثي_س>>8,الزر_Y_إحداثيات&255,الزر_Y_إحداثيات>>8])
        def أمر_الوضع():
            بيانات_منصب.stdin.write(b'\x1b');بيانات_منصب.stdin.flush();إنهاء_مكالمة_إزاحة=time.monotonic()+.2
            while time.monotonic()<إنهاء_مكالمة_إزاحة:مؤشر_حدث(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            셸('terminal');مؤشر_حدث(.3)
            셸('mkdir first; cd first; export NAME=one')
            يرسل('vi 첫째.py\n'.encode(),b'NORMAL')
            يرسل('i값 = 21\nprint(قيمة * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            إنهاء_مكالمة_إزاحة=time.monotonic()+3
            while time.monotonic()<إنهاء_مكالمة_إزاحة:مؤشر_حدث(.1)
            يرسل(اختصار_قيمة(1),b'TERMINAL FOCUS 2');مؤشر_حدث(.2)
            assert b'/\r\n' in 셸('pwd')
            셸('export NAME=two')
            يرسل('vi 둘째.txt\n'.encode(),b'NORMAL')
            يرسل('i두 번째 نافذة\n'.encode(),b'INSERT')
            يرسل(نقرة_زر(180,12),b'TERMINAL FOCUS 1');مؤشر_حدث(.2)
            أمر_الوضع();يرسل(b':wq\r')
            assert b'one:/first' in 셸('echo "$NAME:$PWD"')
            assert 'قيمة = 21\r\nprint(قيمة * 2)'.encode() in 셸('cat 첫째.py')
            نتيجة=셸('python 첫째.py');assert b'42\r\n' in نتيجة,نتيجة
            # Close the first shell with its actual title-bar X; second editor resumes.
            يرسل(نقرة_زر(560,63),b'TERMINAL FOCUS 2');مؤشر_حدث(.2)
            أمر_الوضع();يرسل(b':wq\r')
            assert b'two:/' in 셸('echo "$NAME:$PWD"')
            assert '두 번째 نافذة'.encode() in 셸('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            يرسل('vi 둘째.txt\n'.encode(),b'NORMAL');يرسل(b'xu',b'NORMAL')
            يرسل(b'iX',b'INSERT');أمر_الوضع();يرسل(b':q\r',b'Unsaved')
            يرسل(b':q!\r');assert '두 번째 نافذة'.encode() in 셸('cat 둘째.txt')
            يرسل(اختصار_قيمة(1),b'TERMINAL FOCUS 1');مؤشر_حدث(.2)
            يرسل(اختصار_قيمة(1),b'TERMINAL FOCUS 3');مؤشر_حدث(.2)
            يرسل(اختصار_قيمة(1),b'TERMINAL FOCUS 4');مؤشر_حدث(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            بيانات_منصب.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));بيانات_منصب.stdin.flush()
            셸('echo DRAGGED_OK')
            يرسل('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            يرسل('i저장하지 않은 بيانات'.encode(),b'INSERT')
            يرسل(نقرة_زر(578,97),b'TERMINAL FOCUS 3');مؤشر_حدث(.2)
            assert '버릴문서.txt'.encode() not in 셸('ls')
            يرسل(اختصار_قيمة(1),b'TERMINAL FOCUS 4');مؤشر_حدث(.2)
            셸('echo REUSED_WINDOW_OK')
            مكتمل_مبلغ=سجل_سجل.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',مكتمل_مبلغ)
            # UART completion precedes the next QEMU display refresh.
            إنهاء_مكالمة_إزاحة=time.monotonic()+.3
            while time.monotonic()<إنهاء_مكالمة_إزاحة:مؤشر_حدث(.05)
            with socket.socket(socket.AF_UNIX) as رمز_الحرف:
                رمز_الحرف.settimeout(10);رمز_الحرف.connect(str(모의제어접속))
                with رمز_الحرف.makefile('rwb') as ملف_إدخال_3d0c1245:
                    json.loads(ملف_إدخال_3d0c1245.readline())
                    for طلب_قيمة in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(وجهة_قيمة_منصب/'four-terminals.png'),'format':'png'}}):
                        ملف_إدخال_3d0c1245.write((json.dumps(طلب_قيمة)+'\n').encode());ملف_إدخال_3d0c1245.flush()
                        while True:
                            반환값=json.loads(ملف_إدخال_3d0c1245.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(وجهة_قيمة_منصب/'four-terminals.png')).convert('RGB')
            for زوج_إحداثيات,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(زوج_إحداثيات)==색상,(زوج_إحداثيات,화소들.getpixel(زوج_إحداثيات))
            셸('echo FOUR_WINDOWS_OK')
            التحقق_من_صحة_إبلاغ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if بيانات_منصب.poll() is None:بيانات_منصب.terminate()
            try:بيانات_منصب.wait(timeout=5)
            except subprocess.TimeoutExpired:بيانات_منصب.kill();بيانات_منصب.wait()
            محدد_a916db4e.close();بيانات_منصب.stdin.close();بيانات_منصب.stdout.close();(وجهة_قيمة_منصب/'serial.log').write_bytes(سجل_سجل);(وجهة_قيمة_منصب/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':تشغيل()
