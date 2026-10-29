#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from نفاذ_کرو_حکم import 기준,حکم

def چلاؤ():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    درجہ_راہ=기준/'build/verification/new-java';درجہ_راہ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(درجہ_راہ),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
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
            کوائف=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            بھیجو('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(کوائف),64):بھیجو(کوائف[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            بھیجو(b'.\n')
            بھیجو('java 스윙시험\n'.encode(),b'SWING READY')
            ختم_کرو_آف_سیٹ=time.monotonic()+3
            while time.monotonic()<ختم_کرو_آف_سیٹ:نبٹنا_واقعہ(.1)
            # JFrame centered at (120,100), content at y=130.
            بھیجو(کلک_کرو_بٹن(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            ختم_کرو_آف_سیٹ=time.monotonic()+.3
            while time.monotonic()<ختم_کرو_آف_سیٹ:نبٹنا_واقعہ(.05)
            결과=بھیجو(کلک_کرو_بٹن(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(لاگ_صف)-len(결과))
            بھیجو(تیز_راہ_قدر(1),b'TERMINAL FOCUS 2')
            결과=شیل('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            بھیجو(کلک_کرو_بٹن(180,12),b'TERMINAL FOCUS 1')
            ختم_کرو_آف_سیٹ=time.monotonic()+.3
            while time.monotonic()<ختم_کرو_آف_سیٹ:نبٹنا_واقعہ(.05)
            with socket.socket(socket.AF_UNIX) as کیریکٹر_کوڈ:
                کیریکٹر_کوڈ.settimeout(10);کیریکٹر_کوڈ.connect(str(모의제어접속))
                with کیریکٹر_کوڈ.makefile('rwb') as فائل_داخلہ:
                    json.loads(فائل_داخلہ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        فائل_داخلہ.write((json.dumps(요청값)+'\n').encode());فائل_داخلہ.flush()
                        while True:
                            반환값=json.loads(فائل_داخلہ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            بھیجو(کلک_کرو_بٹن(505,115))
            شیل('echo SWING_CLOSED_OK')
            کوائف=(درجہ_راہ/'한글창시험.class').read_bytes()
            بھیجو('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(کوائف),64):بھیجو(کوائف[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            بھیجو(b'.\n')
            بھیجو('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            بھیجو(کلک_کرو_بٹن(200,255),'KOREAN SWING CLICK ناں'.encode())
            بھیجو(کلک_کرو_بٹن(505,115))
            شیل('echo KOREAN_SWING_CLOSED_OK')
            جواز_دہی_رپورٹ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 کھڑکی/بٹن/동작알림/واقعہ_قطار directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            منتخب_کرنڑ_آلا_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(لاگ_صف);(목적위치/'report.json').write_text(json.dumps(جواز_دہی_رپورٹ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':چلاؤ()
