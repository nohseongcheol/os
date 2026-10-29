#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from اجرا_فرمان import نمایش_دادن_جذر,فرمان

def اجرا_2():
    مقصد_مقدار_مرتب_کردن=نمایش_دادن_جذر/'build/verification/windows';مقصد_مقدار_مرتب_کردن.mkdir(parents=True,exist_ok=True)
    اعتبارسنجی_گزارش={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((نمایش_دادن_جذر/'build/kernel8.img').read_bytes()).hexdigest()};واقعه_نگار_ردیف=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        داده_ها_مرتب_کردن=subprocess.Popen(فرمان()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        انتخاب_کننده_a916db4e=selectors.DefaultSelector();انتخاب_کننده_a916db4e.register(داده_ها_مرتب_کردن.stdout,selectors.EVENT_READ)
        def دستگیره_رویداد(초단위=.1):
            for 누름값,_ in انتخاب_کننده_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:واقعه_نگار_ردیف.extend(둘째값)
            assert b'PANIC:' not in واقعه_نگار_ردیف and b'HALTED' not in واقعه_نگار_ردیف,واقعه_نگار_ردیف[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            پایان_دادن_جابجایی_لایه_ای=time.monotonic()+초단위
            while 확인표시 not in واقعه_نگار_ردیف[현재위치:]:
                if time.monotonic()>پایان_دادن_جابجایی_لایه_ای or داده_ها_مرتب_کردن.poll() is not None:raise AssertionError(واقعه_نگار_ردیف[현재위치:].decode('utf-8','replace'))
                دستگیره_رویداد()
            return bytes(واقعه_نگار_ردیف[현재위치:])
        def ارسال(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(واقعه_نگار_ردیف);داده_ها_مرتب_کردن.stdin.write(둘째값);داده_ها_مرتب_کردن.stdin.flush();return 기다리기(확인표시,현재위치)
        def واسط(رشته_داده_ها):return ارسال((رشته_داده_ها+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def میانبر_مقدار(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def کلیک_دکمه(مختصات_x,دکمه_Y_مختصات):return bytes([30,1,1,مختصات_x&255,مختصات_x>>8,دکمه_Y_مختصات&255,دکمه_Y_مختصات>>8,30,1,0,مختصات_x&255,مختصات_x>>8,دکمه_Y_مختصات&255,دکمه_Y_مختصات>>8])
        def فرمان_حالت():
            داده_ها_مرتب_کردن.stdin.write(b'\x1b');داده_ها_مرتب_کردن.stdin.flush();پایان_دادن_جابجایی_لایه_ای=time.monotonic()+.2
            while time.monotonic()<پایان_دادن_جابجایی_لایه_ای:دستگیره_رویداد(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            واسط('terminal');دستگیره_رویداد(.3)
            واسط('mkdir first; cd first; export NAME=one')
            ارسال('vi 첫째.py\n'.encode(),b'NORMAL')
            ارسال('i값 = 21\nprint(مقدار * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            پایان_دادن_جابجایی_لایه_ای=time.monotonic()+3
            while time.monotonic()<پایان_دادن_جابجایی_لایه_ای:دستگیره_رویداد(.1)
            ارسال(میانبر_مقدار(1),b'TERMINAL FOCUS 2');دستگیره_رویداد(.2)
            assert b'/\r\n' in واسط('pwd')
            واسط('export NAME=two')
            ارسال('vi 둘째.txt\n'.encode(),b'NORMAL')
            ارسال('i두 번째 پنجره\n'.encode(),b'INSERT')
            ارسال(کلیک_دکمه(180,12),b'TERMINAL FOCUS 1');دستگیره_رویداد(.2)
            فرمان_حالت();ارسال(b':wq\r')
            assert b'one:/first' in واسط('echo "$NAME:$PWD"')
            assert 'مقدار = 21\r\nprint(مقدار * 2)'.encode() in واسط('cat 첫째.py')
            سنجش=واسط('python 첫째.py');assert b'42\r\n' in سنجش,سنجش
            # Close the first shell with its actual title-bar X; second editor resumes.
            ارسال(کلیک_دکمه(560,63),b'TERMINAL FOCUS 2');دستگیره_رویداد(.2)
            فرمان_حالت();ارسال(b':wq\r')
            assert b'two:/' in واسط('echo "$NAME:$PWD"')
            assert '두 번째 پنجره'.encode() in واسط('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ارسال('vi 둘째.txt\n'.encode(),b'NORMAL');ارسال(b'xu',b'NORMAL')
            ارسال(b'iX',b'INSERT');فرمان_حالت();ارسال(b':q\r',b'Unsaved')
            ارسال(b':q!\r');assert '두 번째 پنجره'.encode() in واسط('cat 둘째.txt')
            ارسال(میانبر_مقدار(1),b'TERMINAL FOCUS 1');دستگیره_رویداد(.2)
            ارسال(میانبر_مقدار(1),b'TERMINAL FOCUS 3');دستگیره_رویداد(.2)
            ارسال(میانبر_مقدار(1),b'TERMINAL FOCUS 4');دستگیره_رویداد(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            داده_ها_مرتب_کردن.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));داده_ها_مرتب_کردن.stdin.flush()
            واسط('echo DRAGGED_OK')
            ارسال('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ارسال('i저장하지 않은 داده_ها'.encode(),b'INSERT')
            ارسال(کلیک_دکمه(578,97),b'TERMINAL FOCUS 3');دستگیره_رویداد(.2)
            assert '버릴문서.txt'.encode() not in واسط('ls')
            ارسال(میانبر_مقدار(1),b'TERMINAL FOCUS 4');دستگیره_رویداد(.2)
            واسط('echo REUSED_WINDOW_OK')
            완료량=واقعه_نگار_ردیف.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            پایان_دادن_جابجایی_لایه_ای=time.monotonic()+.3
            while time.monotonic()<پایان_دادن_جابجایی_لایه_ای:دستگیره_رویداد(.05)
            with socket.socket(socket.AF_UNIX) as کد_نویسه:
                کد_نویسه.settimeout(10);کد_نویسه.connect(str(모의제어접속))
                with کد_نویسه.makefile('rwb') as فایل_ورودی:
                    json.loads(فایل_ورودی.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(مقصد_مقدار_مرتب_کردن/'four-terminals.png'),'format':'png'}}):
                        فایل_ورودی.write((json.dumps(요청값)+'\n').encode());فایل_ورودی.flush()
                        while True:
                            반환값=json.loads(فایل_ورودی.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(مقصد_مقدار_مرتب_کردن/'four-terminals.png')).convert('RGB')
            for جفت_مختصاتی,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(جفت_مختصاتی)==색상,(جفت_مختصاتی,화소들.getpixel(جفت_مختصاتی))
            واسط('echo FOUR_WINDOWS_OK')
            اعتبارسنجی_گزارش.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if داده_ها_مرتب_کردن.poll() is None:داده_ها_مرتب_کردن.terminate()
            try:داده_ها_مرتب_کردن.wait(timeout=5)
            except subprocess.TimeoutExpired:داده_ها_مرتب_کردن.kill();داده_ها_مرتب_کردن.wait()
            انتخاب_کننده_a916db4e.close();داده_ها_مرتب_کردن.stdin.close();داده_ها_مرتب_کردن.stdout.close();(مقصد_مقدار_مرتب_کردن/'serial.log').write_bytes(واقعه_نگار_ردیف);(مقصد_مقدار_مرتب_کردن/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':اجرا_2()
