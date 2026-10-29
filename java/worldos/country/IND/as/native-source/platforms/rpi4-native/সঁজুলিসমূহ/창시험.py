#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from নিষ্পাদন_আদেশ import 기준,কমান্ড

def সঞ্চালন():
    গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক=기준/'build/verification/windows';গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক.mkdir(parents=True,exist_ok=True)
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
            শ্বেল('mkdir first; cd first; export NAME=one')
            ই_মেইল_কৰক('vi 첫째.py\n'.encode(),b'NORMAL')
            ই_মেইল_কৰক('i값 = 21\nprint(মান * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            অন্ত_কৰক_অফছেট=time.monotonic()+3
            while time.monotonic()<অন্ত_কৰক_অফছেট:হেণ্ডেল_ইভেণ্ট(.1)
            ই_মেইল_কৰক(চমুপথ_মান(1),b'TERMINAL FOCUS 2');হেণ্ডেল_ইভেণ্ট(.2)
            assert b'/\r\n' in শ্বেল('pwd')
            শ্বেল('export NAME=two')
            ই_মেইল_কৰক('vi 둘째.txt\n'.encode(),b'NORMAL')
            ই_মেইল_কৰক('i두 번째 উইণ্ড\n'.encode(),b'INSERT')
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(180,12),b'TERMINAL FOCUS 1');হেণ্ডেল_ইভেণ্ট(.2)
            আদেশ_মোড();ই_মেইল_কৰক(b':wq\r')
            assert b'one:/first' in শ্বেল('echo "$NAME:$PWD"')
            assert 'মান = 21\r\nprint(মান * 2)'.encode() in শ্বেল('cat 첫째.py')
            পৰিমাপ=শ্বেল('python 첫째.py');assert b'42\r\n' in পৰিমাপ,পৰিমাপ
            # Close the first shell with its actual title-bar X; second editor resumes.
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(560,63),b'TERMINAL FOCUS 2');হেণ্ডেল_ইভেণ্ট(.2)
            আদেশ_মোড();ই_মেইল_কৰক(b':wq\r')
            assert b'two:/' in শ্বেল('echo "$NAME:$PWD"')
            assert '두 번째 উইণ্ড'.encode() in শ্বেল('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ই_মেইল_কৰক('vi 둘째.txt\n'.encode(),b'NORMAL');ই_মেইল_কৰক(b'xu',b'NORMAL')
            ই_মেইল_কৰক(b'iX',b'INSERT');আদেশ_মোড();ই_মেইল_কৰক(b':q\r',b'Unsaved')
            ই_মেইল_কৰক(b':q!\r');assert '두 번째 উইণ্ড'.encode() in শ্বেল('cat 둘째.txt')
            ই_মেইল_কৰক(চমুপথ_মান(1),b'TERMINAL FOCUS 1');হেণ্ডেল_ইভেণ্ট(.2)
            ই_মেইল_কৰক(চমুপথ_মান(1),b'TERMINAL FOCUS 3');হেণ্ডেল_ইভেণ্ট(.2)
            ই_মেইল_কৰক(চমুপথ_মান(1),b'TERMINAL FOCUS 4');হেণ্ডেল_ইভেণ্ট(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ডাটা_স্থান_সলনি_কৰক.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ডাটা_স্থান_সলনি_কৰক.stdin.flush()
            শ্বেল('echo DRAGGED_OK')
            ই_মেইল_কৰক('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ই_মেইল_কৰক('i저장하지 않은 ডাটা'.encode(),b'INSERT')
            ই_মেইল_কৰক(ক্লিক_কৰক_বুটাম(578,97),b'TERMINAL FOCUS 3');হেণ্ডেল_ইভেণ্ট(.2)
            assert '버릴문서.txt'.encode() not in শ্বেল('ls')
            ই_মেইল_কৰক(চমুপথ_মান(1),b'TERMINAL FOCUS 4');হেণ্ডেল_ইভেণ্ট(.2)
            শ্বেল('echo REUSED_WINDOW_OK')
            완료량=লগ_শাৰী.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            অন্ত_কৰক_অফছেট=time.monotonic()+.3
            while time.monotonic()<অন্ত_কৰক_অফছেট:হেণ্ডেল_ইভেণ্ট(.05)
            with socket.socket(socket.AF_UNIX) as বৰ্ণ_ক_ড:
                বৰ্ণ_ক_ড.settimeout(10);বৰ্ণ_ক_ড.connect(str(모의제어접속))
                with বৰ্ণ_ক_ড.makefile('rwb') as ফাইল_প্রবিষ্ট:
                    json.loads(ফাইল_প্রবিষ্ট.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক/'four-terminals.png'),'format':'png'}}):
                        ফাইল_প্রবিষ্ট.write((json.dumps(요청값)+'\n').encode());ফাইল_প্রবিষ্ট.flush()
                        while True:
                            반환값=json.loads(ফাইল_প্রবিষ্ট.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক/'four-terminals.png')).convert('RGB')
            for সমন্বয়_যুগল,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(সমন্বয়_যুগল)==색상,(সমন্বয়_যুগল,화소들.getpixel(সমন্বয়_যুগল))
            শ্বেল('echo FOUR_WINDOWS_OK')
            বৈধতা_ৰিপ_ৰ্ট.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ডাটা_স্থান_সলনি_কৰক.poll() is None:ডাটা_স্থান_সলনি_কৰক.terminate()
            try:ডাটা_স্থান_সলনি_কৰক.wait(timeout=5)
            except subprocess.TimeoutExpired:ডাটা_স্থান_সলনি_কৰক.kill();ডাটা_স্থান_সলনি_কৰক.wait()
            চয়নকাৰী_a916db4e.close();ডাটা_স্থান_সলনি_কৰক.stdin.close();ডাটা_স্থান_সলনি_কৰক.stdout.close();(গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক/'serial.log').write_bytes(লগ_শাৰী);(গন্তব্য_স্থান_মান_স্থান_সলনি_কৰক/'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':সঞ্চালন()
