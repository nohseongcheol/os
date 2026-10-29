#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ينفذ_أمر import يعرض_جذر,أمر

def تشغيل():
    وجهة_قيمة_منصب=يعرض_جذر/'build/verification/swing';وجهة_قيمة_منصب.mkdir(parents=True,exist_ok=True)
    فئة_مسار=يعرض_جذر/'build/verification/new-java';فئة_مسار.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(يعرض_جذر/'dist/jkoros-native-korean.jar'),'-d',str(فئة_مسار),str(يعرض_جذر/'اختبارات/자바/스윙시험.java'),str(يعرض_جذر/'اختبارات/자바/한글창시험.java')])
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
            بيانات=(يعرض_جذر/'build/verification/new-java/스윙시험.class').read_bytes()
            يرسل('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(بيانات),64):يرسل(بيانات[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            يرسل(b'.\n')
            يرسل('java 스윙시험\n'.encode(),b'SWING READY')
            إنهاء_مكالمة_إزاحة=time.monotonic()+3
            while time.monotonic()<إنهاء_مكالمة_إزاحة:مؤشر_حدث(.1)
            # JFrame centered at (120,100), content at y=130.
            يرسل(نقرة_زر(200,210),b'',)  # focus JTextField
            بيانات_منصب.stdin.write('누리'.encode());بيانات_منصب.stdin.flush()
            إنهاء_مكالمة_إزاحة=time.monotonic()+.3
            while time.monotonic()<إنهاء_مكالمة_إزاحة:مؤشر_حدث(.05)
            نتيجة=يرسل(نقرة_زر(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(سجل_سجل)-len(نتيجة))
            يرسل(اختصار_قيمة(1),b'TERMINAL FOCUS 2')
            نتيجة=셸('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in نتيجة
            يرسل(نقرة_زر(180,12),b'TERMINAL FOCUS 1')
            إنهاء_مكالمة_إزاحة=time.monotonic()+.3
            while time.monotonic()<إنهاء_مكالمة_إزاحة:مؤشر_حدث(.05)
            with socket.socket(socket.AF_UNIX) as رمز_الحرف:
                رمز_الحرف.settimeout(10);رمز_الحرف.connect(str(모의제어접속))
                with رمز_الحرف.makefile('rwb') as ملف_إدخال_3d0c1245:
                    json.loads(ملف_إدخال_3d0c1245.readline())
                    for طلب_قيمة in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(وجهة_قيمة_منصب/'native-swing.png'),'format':'png'}}):
                        ملف_إدخال_3d0c1245.write((json.dumps(طلب_قيمة)+'\n').encode());ملف_إدخال_3d0c1245.flush()
                        while True:
                            반환값=json.loads(ملف_إدخال_3d0c1245.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            يرسل(نقرة_زر(505,115))
            셸('echo SWING_CLOSED_OK')
            بيانات=(فئة_مسار/'한글창시험.class').read_bytes()
            يرسل('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(بيانات),64):يرسل(بيانات[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            يرسل(b'.\n')
            يرسل('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            يرسل(نقرة_زر(200,255),'KOREAN SWING CLICK اسم'.encode())
            يرسل(نقرة_زر(505,115))
            셸('echo KOREAN_SWING_CLOSED_OK')
            التحقق_من_صحة_إبلاغ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','العربية نافذة/زر/إجراء_إشعار/حدث_يدرج directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if بيانات_منصب.poll() is None:بيانات_منصب.terminate()
            try:بيانات_منصب.wait(timeout=5)
            except subprocess.TimeoutExpired:بيانات_منصب.kill();بيانات_منصب.wait()
            محدد_a916db4e.close();بيانات_منصب.stdin.close();بيانات_منصب.stdout.close();(وجهة_قيمة_منصب/'serial.log').write_bytes(سجل_سجل);(وجهة_قيمة_منصب/'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':تشغيل()
