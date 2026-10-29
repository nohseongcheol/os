#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from اجرا_فرمان import نمایش_دادن_جذر,فرمان

def اجرا_2():
    مقصد_مقدار_مرتب_کردن=نمایش_دادن_جذر/'build/verification/swing';مقصد_مقدار_مرتب_کردن.mkdir(parents=True,exist_ok=True)
    کلاس_مسیر=نمایش_دادن_جذر/'build/verification/new-java';کلاس_مسیر.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(نمایش_دادن_جذر/'dist/jkoros-native-korean.jar'),'-d',str(کلاس_مسیر),str(نمایش_دادن_جذر/'시험/자바/스윙시험.java'),str(نمایش_دادن_جذر/'시험/자바/한글창시험.java')])
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
            داده_ها=(نمایش_دادن_جذر/'build/verification/new-java/스윙시험.class').read_bytes()
            ارسال('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(داده_ها),64):ارسال(داده_ها[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ارسال(b'.\n')
            ارسال('java 스윙시험\n'.encode(),b'SWING READY')
            پایان_دادن_جابجایی_لایه_ای=time.monotonic()+3
            while time.monotonic()<پایان_دادن_جابجایی_لایه_ای:دستگیره_رویداد(.1)
            # JFrame centered at (120,100), content at y=130.
            ارسال(کلیک_دکمه(200,210),b'',)  # focus JTextField
            داده_ها_مرتب_کردن.stdin.write('누리'.encode());داده_ها_مرتب_کردن.stdin.flush()
            پایان_دادن_جابجایی_لایه_ای=time.monotonic()+.3
            while time.monotonic()<پایان_دادن_جابجایی_لایه_ای:دستگیره_رویداد(.05)
            سنجش=ارسال(کلیک_دکمه(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(واقعه_نگار_ردیف)-len(سنجش))
            ارسال(میانبر_مقدار(1),b'TERMINAL FOCUS 2')
            سنجش=واسط('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in سنجش
            ارسال(کلیک_دکمه(180,12),b'TERMINAL FOCUS 1')
            پایان_دادن_جابجایی_لایه_ای=time.monotonic()+.3
            while time.monotonic()<پایان_دادن_جابجایی_لایه_ای:دستگیره_رویداد(.05)
            with socket.socket(socket.AF_UNIX) as کد_نویسه:
                کد_نویسه.settimeout(10);کد_نویسه.connect(str(모의제어접속))
                with کد_نویسه.makefile('rwb') as فایل_ورودی:
                    json.loads(فایل_ورودی.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(مقصد_مقدار_مرتب_کردن/'native-swing.png'),'format':'png'}}):
                        فایل_ورودی.write((json.dumps(요청값)+'\n').encode());فایل_ورودی.flush()
                        while True:
                            반환값=json.loads(فایل_ورودی.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ارسال(کلیک_دکمه(505,115))
            واسط('echo SWING_CLOSED_OK')
            داده_ها=(کلاس_مسیر/'한글창시험.class').read_bytes()
            ارسال('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(داده_ها),64):ارسال(داده_ها[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ارسال(b'.\n')
            ارسال('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ارسال(کلیک_دکمه(200,255),'KOREAN SWING CLICK نام'.encode())
            ارسال(کلیک_دکمه(505,115))
            واسط('echo KOREAN_SWING_CLOSED_OK')
            اعتبارسنجی_گزارش.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','فارسی پنجره/دکمه/동작알림/رویداد_صف directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if داده_ها_مرتب_کردن.poll() is None:داده_ها_مرتب_کردن.terminate()
            try:داده_ها_مرتب_کردن.wait(timeout=5)
            except subprocess.TimeoutExpired:داده_ها_مرتب_کردن.kill();داده_ها_مرتب_کردن.wait()
            انتخاب_کننده_a916db4e.close();داده_ها_مرتب_کردن.stdin.close();داده_ها_مرتب_کردن.stdout.close();(مقصد_مقدار_مرتب_کردن/'serial.log').write_bytes(واقعه_نگار_ردیف);(مقصد_مقدار_مرتب_کردن/'report.json').write_text(json.dumps(اعتبارسنجی_گزارش,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':اجرا_2()
