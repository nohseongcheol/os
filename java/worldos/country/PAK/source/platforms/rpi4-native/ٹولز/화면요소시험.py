#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ,حکم

def چلائیں():
    منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں=عکس_ڈالنا_روٹ/'build/verification/swing';منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں.mkdir(parents=True,exist_ok=True)
    صنف_راہ=عکس_ڈالنا_روٹ/'build/verification/new-java';صنف_راہ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(عکس_ڈالنا_روٹ/'dist/jkoros-native-korean.jar'),'-d',str(صنف_راہ),str(عکس_ڈالنا_روٹ/'시험/자바/스윙시험.java'),str(عکس_ڈالنا_روٹ/'시험/자바/한글창시험.java')])
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
            کوائف=(عکس_ڈالنا_روٹ/'build/verification/new-java/스윙시험.class').read_bytes()
            بھیجیں('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(کوائف),64):بھیجیں(کوائف[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            بھیجیں(b'.\n')
            بھیجیں('java 스윙시험\n'.encode(),b'SWING READY')
            اختتام_آفسٹ=time.monotonic()+3
            while time.monotonic()<اختتام_آفسٹ:ہینڈل_ایونٹ(.1)
            # JFrame centered at (120,100), content at y=130.
            بھیجیں(کلک_بٹن(200,210),b'',)  # focus JTextField
            کوائف_پوزیشن_ٹھیک_کریں.stdin.write('누리'.encode());کوائف_پوزیشن_ٹھیک_کریں.stdin.flush()
            اختتام_آفسٹ=time.monotonic()+.3
            while time.monotonic()<اختتام_آفسٹ:ہینڈل_ایونٹ(.05)
            پیمائش=بھیجیں(کلک_بٹن(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(لاگ_صف)-len(پیمائش))
            بھیجیں(تیز_راہ_قدر(1),b'TERMINAL FOCUS 2')
            پیمائش=شیل('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in پیمائش
            بھیجیں(کلک_بٹن(180,12),b'TERMINAL FOCUS 1')
            اختتام_آفسٹ=time.monotonic()+.3
            while time.monotonic()<اختتام_آفسٹ:ہینڈل_ایونٹ(.05)
            with socket.socket(socket.AF_UNIX) as کریکٹر_ضابطہ:
                کریکٹر_ضابطہ.settimeout(10);کریکٹر_ضابطہ.connect(str(모의제어접속))
                with کریکٹر_ضابطہ.makefile('rwb') as فائل_اندراج:
                    json.loads(فائل_اندراج.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں/'native-swing.png'),'format':'png'}}):
                        فائل_اندراج.write((json.dumps(요청값)+'\n').encode());فائل_اندراج.flush()
                        while True:
                            반환값=json.loads(فائل_اندراج.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            بھیجیں(کلک_بٹن(505,115))
            شیل('echo SWING_CLOSED_OK')
            کوائف=(صنف_راہ/'한글창시험.class').read_bytes()
            بھیجیں('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(کوائف),64):بھیجیں(کوائف[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            بھیجیں(b'.\n')
            بھیجیں('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            بھیجیں(کلک_بٹن(200,255),'KOREAN SWING CLICK نام'.encode())
            بھیجیں(کلک_بٹن(505,115))
            شیل('echo KOREAN_SWING_CLOSED_OK')
            توثیق_رپورٹ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','اردو ونڈو/بٹن/동작알림/ایونٹ_قطار directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if کوائف_پوزیشن_ٹھیک_کریں.poll() is None:کوائف_پوزیشن_ٹھیک_کریں.terminate()
            try:کوائف_پوزیشن_ٹھیک_کریں.wait(timeout=5)
            except subprocess.TimeoutExpired:کوائف_پوزیشن_ٹھیک_کریں.kill();کوائف_پوزیشن_ٹھیک_کریں.wait()
            منتخب_کنندہ_a916db4e.close();کوائف_پوزیشن_ٹھیک_کریں.stdin.close();کوائف_پوزیشن_ٹھیک_کریں.stdout.close();(منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں/'serial.log').write_bytes(لاگ_صف);(منزل_مقصود_قدر_پوزیشن_ٹھیک_کریں/'report.json').write_text(json.dumps(توثیق_رپورٹ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':چلائیں()
