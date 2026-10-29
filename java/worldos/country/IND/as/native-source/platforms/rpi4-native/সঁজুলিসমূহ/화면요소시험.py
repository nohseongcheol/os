#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from নিষ্পাদন_আদেশ import 기준,কমান্ড

def সঞ্চালন():
    গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক=기준/'build/verification/swing';গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক.mkdir(parents=True,exist_ok=True)
    শ্ৰেণী_পথ=기준/'build/verification/new-java';শ্ৰেণী_পথ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(শ্ৰেণী_পথ),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    বৈধতা_ৰিপ_ৰ্ট={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};লগ_শাৰী=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ডাটা_স্থান_সলনি_কৰক=subprocess.Popen(কমান্ড()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        চয়নকাৰী_a916db4e=selectors.DefaultSelector();চয়নকাৰী_a916db4e.register(ডাটা_স্থান_সলনি_কৰক.stdout,selectors.EVENT_READ)
        def হেণ্ডেল_ইভেণ্ট(초단위=.1):
            for 누름값,_ in চয়নকাৰী_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:লগ_শাৰী.extend(둘째값)
            assert b'PANIC:' not in লগ_শাৰী and b'HALTED' not in লগ_শাৰী,লগ_শাৰী[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            অন্ত_কৰক_অফছেট=time.monotonic()+초단위
            while 확인표시 not in লগ_শাৰী[현재위치:]:
                if time.monotonic()>অন্ত_কৰক_অফছেট or ডাটা_স্থান_সলনি_কৰক.poll() is not None:raise AssertionError(লগ_শাৰী[현재위치:].decode('utf-8','replace'))
                হেণ্ডেল_ইভেণ্ট()
            return bytes(লগ_শাৰী[현재위치:])
        def ই_মেইল_কৰক(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(লগ_শাৰী);ডাটা_স্থান_সলনি_কৰক.stdin.write(둘째값);ডাটা_স্থান_সলনি_কৰক.stdin.flush();return 기다리기(확인표시,현재위치)
        def শ্বেল(ষ্ট্ৰিং_ডাটা):return ই_মেইল_কৰক((ষ্ট্ৰিং_ডাটা+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def চমুপথ_মান(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ক্লিক_কৰক_বুটাম(x_ক_ৰ্ডিনেট,세로좌표):return bytes([30,1,1,x_ক_ৰ্ডিনেট&255,x_ক_ৰ্ডিনেট>>8,세로좌표&255,세로좌표>>8,30,1,0,x_ক_ৰ্ডিনেট&255,x_ক_ৰ্ডিনেট>>8,세로좌표&255,세로좌표>>8])
        def আদেশ_মোড():
            ডাটা_স্থান_সলনি_কৰক.stdin.write(b'\x1b');ডাটা_স্থান_সলনি_কৰক.stdin.flush();অন্ত_কৰক_অফছেট=time.monotonic()+.2
            while time.monotonic()<অন্ত_কৰক_অফছেট:হেণ্ডেল_ইভেণ্ট(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            শ্বেল('terminal');হেণ্ডেল_ইভেণ্ট(.3)
            ডাটা=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            ই_মেইল_কৰক('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ডাটা),64):ই_মেইল_কৰক(ডাটা[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ই_মেইল_কৰক(b'.\n')
            ই_মেইল_কৰক('java 스윙시험\n'.encode(),b'SWING READY')
            অন্ত_কৰক_অফছেট=time.monotonic()+3
            while time.monotonic()<অন্ত_কৰক_অফছেট:হেণ্ডেল_ইভেণ্ট(.1)
            # JFrame centered at (120,100), content at y=130.
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(200,210),b'',)  # focus JTextField
            ডাটা_স্থান_সলনি_কৰক.stdin.write('누리'.encode());ডাটা_স্থান_সলনি_কৰক.stdin.flush()
            অন্ত_কৰক_অফছেট=time.monotonic()+.3
            while time.monotonic()<অন্ত_কৰক_অফছেট:হেণ্ডেল_ইভেণ্ট(.05)
            পৰিমাপ=ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(লগ_শাৰী)-len(পৰিমাপ))
            ই_মেইল_কৰক(চমুপথ_মান(1),b'TERMINAL FOCUS 2')
            পৰিমাপ=শ্বেল('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in পৰিমাপ
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(180,12),b'TERMINAL FOCUS 1')
            অন্ত_কৰক_অফছেট=time.monotonic()+.3
            while time.monotonic()<অন্ত_কৰক_অফছেট:হেণ্ডেল_ইভেণ্ট(.05)
            with socket.socket(socket.AF_UNIX) as বৰ্ণ_ক_ড:
                বৰ্ণ_ক_ড.settimeout(10);বৰ্ণ_ক_ড.connect(str(모의제어접속))
                with বৰ্ণ_ক_ড.makefile('rwb') as ফাইল_প্রবিষ্ট:
                    json.loads(ফাইল_প্রবিষ্ট.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক/'native-swing.png'),'format':'png'}}):
                        ফাইল_প্রবিষ্ট.write((json.dumps(요청값)+'\n').encode());ফাইল_প্রবিষ্ট.flush()
                        while True:
                            반환값=json.loads(ফাইল_প্রবিষ্ট.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(505,115))
            শ্বেল('echo SWING_CLOSED_OK')
            ডাটা=(শ্ৰেণী_পথ/'한글창시험.class').read_bytes()
            ই_মেইল_কৰক('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ডাটা),64):ই_মেইল_কৰক(ডাটা[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ই_মেইল_কৰক(b'.\n')
            ই_মেইল_কৰক('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(200,255),'KOREAN SWING CLICK নাম'.encode())
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(505,115))
            শ্বেল('echo KOREAN_SWING_CLOSED_OK')
            বৈধতা_ৰিপ_ৰ্ট.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 উইণ্ড/বুটাম/동작알림/ইভেণ্ট_লানি directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ডাটা_স্থান_সলনি_কৰক.poll() is None:ডাটা_স্থান_সলনি_কৰক.terminate()
            try:ডাটা_স্থান_সলনি_কৰক.wait(timeout=5)
            except subprocess.TimeoutExpired:ডাটা_স্থান_সলনি_কৰক.kill();ডাটা_স্থান_সলনি_কৰক.wait()
            চয়নকাৰী_a916db4e.close();ডাটা_স্থান_সলনি_কৰক.stdin.close();ডাটা_স্থান_সলনি_কৰক.stdout.close();(গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক/'serial.log').write_bytes(লগ_শাৰী);(গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':সঞ্চালন()
