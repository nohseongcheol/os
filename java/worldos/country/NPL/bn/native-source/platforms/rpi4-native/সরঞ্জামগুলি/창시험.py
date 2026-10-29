#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল,আদেশ

def চালনা():
    গন্তব্য_মান_পদ=প্রকল্প_মূল/'build/verification/windows';গন্তব্য_মান_পদ.mkdir(parents=True,exist_ok=True)
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
            শেল('mkdir first; cd first; export NAME=one')
            পাঠান('vi 첫째.py\n'.encode(),b'NORMAL')
            পাঠান('i값 = 21\nprint(মান * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            শেষ_করা_অফসেট=time.monotonic()+3
            while time.monotonic()<শেষ_করা_অফসেট:হাতল_ঘটনা(.1)
            পাঠান(শর্টকাট_মান(1),b'TERMINAL FOCUS 2');হাতল_ঘটনা(.2)
            assert b'/\r\n' in শেল('pwd')
            শেল('export NAME=two')
            পাঠান('vi 둘째.txt\n'.encode(),b'NORMAL')
            পাঠান('i두 번째 উইন্ডো\n'.encode(),b'INSERT')
            পাঠান(ক্লিক_করা_বোতাম(180,12),b'TERMINAL FOCUS 1');হাতল_ঘটনা(.2)
            আদেশ_মোড();পাঠান(b':wq\r')
            assert b'one:/first' in শেল('echo "$NAME:$PWD"')
            assert 'মান = 21\r\nprint(মান * 2)'.encode() in শেল('cat 첫째.py')
            পরিমাপ=শেল('python 첫째.py');assert b'42\r\n' in পরিমাপ,পরিমাপ
            # Close the first shell with its actual title-bar X; second editor resumes.
            পাঠান(ক্লিক_করা_বোতাম(560,63),b'TERMINAL FOCUS 2');হাতল_ঘটনা(.2)
            আদেশ_মোড();পাঠান(b':wq\r')
            assert b'two:/' in শেল('echo "$NAME:$PWD"')
            assert '두 번째 উইন্ডো'.encode() in শেল('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            পাঠান('vi 둘째.txt\n'.encode(),b'NORMAL');পাঠান(b'xu',b'NORMAL')
            পাঠান(b'iX',b'INSERT');আদেশ_মোড();পাঠান(b':q\r',b'Unsaved')
            পাঠান(b':q!\r');assert '두 번째 উইন্ডো'.encode() in শেল('cat 둘째.txt')
            পাঠান(শর্টকাট_মান(1),b'TERMINAL FOCUS 1');হাতল_ঘটনা(.2)
            পাঠান(শর্টকাট_মান(1),b'TERMINAL FOCUS 3');হাতল_ঘটনা(.2)
            পাঠান(শর্টকাট_মান(1),b'TERMINAL FOCUS 4');হাতল_ঘটনা(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ডাটা_পদ.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ডাটা_পদ.stdin.flush()
            শেল('echo DRAGGED_OK')
            পাঠান('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            পাঠান('i저장하지 않은 ডাটা'.encode(),b'INSERT')
            পাঠান(ক্লিক_করা_বোতাম(578,97),b'TERMINAL FOCUS 3');হাতল_ঘটনা(.2)
            assert '버릴문서.txt'.encode() not in শেল('ls')
            পাঠান(শর্টকাট_মান(1),b'TERMINAL FOCUS 4');হাতল_ঘটনা(.2)
            শেল('echo REUSED_WINDOW_OK')
            완료량=লগ_সারি.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            শেষ_করা_অফসেট=time.monotonic()+.3
            while time.monotonic()<শেষ_করা_অফসেট:হাতল_ঘটনা(.05)
            with socket.socket(socket.AF_UNIX) as অক্ষর_কোড:
                অক্ষর_কোড.settimeout(10);অক্ষর_কোড.connect(str(모의제어접속))
                with অক্ষর_কোড.makefile('rwb') as ফাইল_ভুক্তি:
                    json.loads(ফাইল_ভুক্তি.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(গন্তব্য_মান_পদ/'four-terminals.png'),'format':'png'}}):
                        ফাইল_ভুক্তি.write((json.dumps(요청값)+'\n').encode());ফাইল_ভুক্তি.flush()
                        while True:
                            반환값=json.loads(ফাইল_ভুক্তি.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(গন্তব্য_মান_পদ/'four-terminals.png')).convert('RGB')
            for কোঅর্ডিনেট_পেয়ার,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(কোঅর্ডিনেট_পেয়ার)==색상,(কোঅর্ডিনেট_পেয়ার,화소들.getpixel(কোঅর্ডিনেট_পেয়ার))
            শেল('echo FOUR_WINDOWS_OK')
            বৈধকরণ_রিপোর্ট.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ডাটা_পদ.poll() is None:ডাটা_পদ.terminate()
            try:ডাটা_পদ.wait(timeout=5)
            except subprocess.TimeoutExpired:ডাটা_পদ.kill();ডাটা_পদ.wait()
            নির্বাচক_a916db4e.close();ডাটা_পদ.stdin.close();ডাটা_পদ.stdout.close();(গন্তব্য_মান_পদ/'serial.log').write_bytes(লগ_সারি);(গন্তব্য_মান_পদ/'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':চালনা()
