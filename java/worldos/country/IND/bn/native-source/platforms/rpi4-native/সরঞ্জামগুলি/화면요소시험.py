#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল,আদেশ

def চালনা():
    গন্তব্য_মান_পদ=প্রকল্প_মূল/'build/verification/swing';গন্তব্য_মান_পদ.mkdir(parents=True,exist_ok=True)
    শ্রেণী_পথ=প্রকল্প_মূল/'build/verification/new-java';শ্রেণী_পথ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(প্রকল্প_মূল/'dist/jkoros-native-korean.jar'),'-d',str(শ্রেণী_পথ),str(প্রকল্প_মূল/'시험/자바/스윙시험.java'),str(প্রকল্প_মূল/'시험/자바/한글창시험.java')])
    বৈধকরণ_রিপোর্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((প্রকল্প_মূল/'build/kernel8.img').read_bytes()).hexdigest()};লগ_সারি=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ডাটা_পদ=subprocess.Popen(আদেশ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        নির্বাচক_a916db4e=selectors.DefaultSelector();নির্বাচক_a916db4e.register(ডাটা_পদ.stdout,selectors.EVENT_READ)
        def হাতল_ঘটনা(초단위=.1):
            for 누름값,_ in নির্বাচক_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:লগ_সারি.extend(둘째값)
            assert b'PANIC:' not in লগ_সারি and b'HALTED' not in লগ_সারি,লগ_সারি[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            শেষ_করা_অফসেট=time.monotonic()+초단위
            while 확인표시 not in লগ_সারি[현재위치:]:
                if time.monotonic()>শেষ_করা_অফসেট or ডাটা_পদ.poll() is not None:raise AssertionError(লগ_সারি[현재위치:].decode('utf-8','replace'))
                হাতল_ঘটনা()
            return bytes(লগ_সারি[현재위치:])
        def পাঠান(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(লগ_সারি);ডাটা_পদ.stdin.write(둘째값);ডাটা_পদ.stdin.flush();return 기다리기(확인표시,현재위치)
        def শেল(স্ট্রিং_ডাটা):return পাঠান((স্ট্রিং_ডাটা+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def শর্টকাট_মান(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ক্লিক_করা_বোতাম(X_বোতাম_অক্ষবিন্দু,Y_বোতাম_অক্ষবিন্দু):return bytes([30,1,1,X_বোতাম_অক্ষবিন্দু&255,X_বোতাম_অক্ষবিন্দু>>8,Y_বোতাম_অক্ষবিন্দু&255,Y_বোতাম_অক্ষবিন্দু>>8,30,1,0,X_বোতাম_অক্ষবিন্দু&255,X_বোতাম_অক্ষবিন্দু>>8,Y_বোতাম_অক্ষবিন্দু&255,Y_বোতাম_অক্ষবিন্দু>>8])
        def আদেশ_মোড():
            ডাটা_পদ.stdin.write(b'\x1b');ডাটা_পদ.stdin.flush();শেষ_করা_অফসেট=time.monotonic()+.2
            while time.monotonic()<শেষ_করা_অফসেট:হাতল_ঘটনা(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            শেল('terminal');হাতল_ঘটনা(.3)
            ডাটা=(প্রকল্প_মূল/'build/verification/new-java/스윙시험.class').read_bytes()
            পাঠান('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ডাটা),64):পাঠান(ডাটা[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            পাঠান(b'.\n')
            পাঠান('java 스윙시험\n'.encode(),b'SWING READY')
            শেষ_করা_অফসেট=time.monotonic()+3
            while time.monotonic()<শেষ_করা_অফসেট:হাতল_ঘটনা(.1)
            # JFrame centered at (120,100), content at y=130.
            পাঠান(ক্লিক_করা_বোতাম(200,210),b'',)  # focus JTextField
            ডাটা_পদ.stdin.write('누리'.encode());ডাটা_পদ.stdin.flush()
            শেষ_করা_অফসেট=time.monotonic()+.3
            while time.monotonic()<শেষ_করা_অফসেট:হাতল_ঘটনা(.05)
            পরিমাপ=পাঠান(ক্লিক_করা_বোতাম(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(লগ_সারি)-len(পরিমাপ))
            পাঠান(শর্টকাট_মান(1),b'TERMINAL FOCUS 2')
            পরিমাপ=শেল('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in পরিমাপ
            পাঠান(ক্লিক_করা_বোতাম(180,12),b'TERMINAL FOCUS 1')
            শেষ_করা_অফসেট=time.monotonic()+.3
            while time.monotonic()<শেষ_করা_অফসেট:হাতল_ঘটনা(.05)
            with socket.socket(socket.AF_UNIX) as অক্ষর_কোড:
                অক্ষর_কোড.settimeout(10);অক্ষর_কোড.connect(str(모의제어접속))
                with অক্ষর_কোড.makefile('rwb') as ফাইল_ভুক্তি:
                    json.loads(ফাইল_ভুক্তি.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(গন্তব্য_মান_পদ/'native-swing.png'),'format':'png'}}):
                        ফাইল_ভুক্তি.write((json.dumps(요청값)+'\n').encode());ফাইল_ভুক্তি.flush()
                        while True:
                            반환값=json.loads(ফাইল_ভুক্তি.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            পাঠান(ক্লিক_করা_বোতাম(505,115))
            শেল('echo SWING_CLOSED_OK')
            ডাটা=(শ্রেণী_পথ/'한글창시험.class').read_bytes()
            পাঠান('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ডাটা),64):পাঠান(ডাটা[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            পাঠান(b'.\n')
            পাঠান('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            পাঠান(ক্লিক_করা_বোতাম(200,255),'KOREAN SWING CLICK নাম'.encode())
            পাঠান(ক্লিক_করা_বোতাম(505,115))
            শেল('echo KOREAN_SWING_CLOSED_OK')
            বৈধকরণ_রিপোর্ট.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','বাংলা উইন্ডো/বোতাম/동작알림/ঘটনা_সারিবদ্ধ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ডাটা_পদ.poll() is None:ডাটা_পদ.terminate()
            try:ডাটা_পদ.wait(timeout=5)
            except subprocess.TimeoutExpired:ডাটা_পদ.kill();ডাটা_পদ.wait()
            নির্বাচক_a916db4e.close();ডাটা_পদ.stdin.close();ডাটা_পদ.stdout.close();(গন্তব্য_মান_পদ/'serial.log').write_bytes(লগ_সারি);(গন্তব্য_মান_পদ/'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':চালনা()
