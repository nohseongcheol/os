#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from စက်မောင်း import စီမံကိန်းအမြစ်,အမိန့်

def လုပ်ဆောင်():
    ဦးတည်ရာတန်ဖိုးနေရာ=စီမံကိန်းအမြစ်/'build/verification/windows';ဦးတည်ရာတန်ဖိုးနေရာ.mkdir(parents=True,exist_ok=True)
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((စီမံကိန်းအမြစ်/'build/kernel8.img').read_bytes()).hexdigest()};မှတ်တမ်းမှတ်တမ်းတစ်ခု=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as လုပ်ဆောင်လမ်း:
        모의제어접속=Path(လုပ်ဆောင်လမ်း)/'qmp.sock'
        ဒေတာနေရာ=subprocess.Popen(အမိန့်()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(ဒေတာနေရာ.stdout,selectors.EVENT_READ)
        def ကိုင်တွယ်ရာဖြစ်ရပ်(စက္ကန့်ယူနစ်=.1):
            for 누름값,_ in 선택기.select(စက္ကန့်ယူနစ်):
                ဒုတိယတန်ဖိုး=누름값.fileobj.read(65536)
                if ဒုတိယတန်ဖိုး:မှတ်တမ်းမှတ်တမ်းတစ်ခု.extend(ဒုတိယတန်ဖိုး)
            assert b'PANIC:' not in မှတ်တမ်းမှတ်တမ်းတစ်ခု and b'HALTED' not in မှတ်တမ်းမှတ်တမ်းတစ်ခု,မှတ်တမ်းမှတ်တမ်းတစ်ခု[-2048:]
        def စောင့်(확인표시,လက်ရှိနေရာ,စက္ကန့်ယူနစ်=50):
            အဆုံးအရွေ့=time.monotonic()+စက္ကန့်ယူနစ်
            while 확인표시 not in မှတ်တမ်းမှတ်တမ်းတစ်ခု[လက်ရှိနေရာ:]:
                if time.monotonic()>အဆုံးအရွေ့ or ဒေတာနေရာ.poll() is not None:raise AssertionError(မှတ်တမ်းမှတ်တမ်းတစ်ခု[လက်ရှိနေရာ:].decode('utf-8','replace'))
                ကိုင်တွယ်ရာဖြစ်ရပ်()
            return bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု[လက်ရှိနေရာ:])
        def ပို့(ဒုတိယတန်ဖိုး,확인표시=b'jkoros-native> '):
            လက်ရှိနေရာ=len(မှတ်တမ်းမှတ်တမ်းတစ်ခု);ဒေတာနေရာ.stdin.write(ဒုတိယတန်ဖိုး);ဒေတာနေရာ.stdin.flush();return စောင့်(확인표시,လက်ရှိနေရာ)
        def အမိန့်ဝင်း(အက္ခရာစဉ်ဒေတာ):return ပို့((အက္ခရာစဉ်ဒေတာ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def 바로가기(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def 누르기(xတည်နေရာအမှတ်,yတည်နေရာအမှတ်):return bytes([30,1,1,xတည်နေရာအမှတ်&255,xတည်နေရာအမှတ်>>8,yတည်နေရာအမှတ်&255,yတည်နေရာအမှတ်>>8,30,1,0,xတည်နေရာအမှတ်&255,xတည်နေရာအမှတ်>>8,yတည်နေရာအမှတ်&255,yတည်နေရာအမှတ်>>8])
        def အမိန့်နည်းစနစ်():
            ဒေတာနေရာ.stdin.write(b'\x1b');ဒေတာနေရာ.stdin.flush();အဆုံးအရွေ့=time.monotonic()+.2
            while time.monotonic()<အဆုံးအရွေ့:ကိုင်တွယ်ရာဖြစ်ရပ်(.03)
        try:
            စောင့်(b'jkoros-native> ',0)
            အမိန့်ဝင်း('terminal');ကိုင်တွယ်ရာဖြစ်ရပ်(.3)
            အမိန့်ဝင်း('mkdir first; cd first; export NAME=one')
            ပို့('vi ပထမအစဉ်.py\n'.encode(),b'NORMAL')
            ပို့('i값 = 21\nprint(တန်ဖိုး * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            အဆုံးအရွေ့=time.monotonic()+3
            while time.monotonic()<အဆုံးအရွေ့:ကိုင်တွယ်ရာဖြစ်ရပ်(.1)
            ပို့(바로가기(1),b'TERMINAL FOCUS 2');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            assert b'/\r\n' in အမိန့်ဝင်း('pwd')
            အမိန့်ဝင်း('export NAME=two')
            ပို့('vi ဒုတိယအစဉ်.txt\n'.encode(),b'NORMAL')
            ပို့('i두 번째 ဝင်း\n'.encode(),b'INSERT')
            ပို့(누르기(180,12),b'TERMINAL FOCUS 1');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            အမိန့်နည်းစနစ်();ပို့(b':wq\r')
            assert b'one:/first' in အမိန့်ဝင်း('echo "$NAME:$PWD"')
            assert 'တန်ဖိုး = 21\r\nprint(တန်ဖိုး * 2)'.encode() in အမိန့်ဝင်း('cat ပထမအစဉ်.py')
            ရလဒ်=အမိန့်ဝင်း('python ပထမအစဉ်.py');assert b'42\r\n' in ရလဒ်,ရလဒ်
            # Close the first shell with its actual title-bar X; second editor resumes.
            ပို့(누르기(560,63),b'TERMINAL FOCUS 2');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            အမိန့်နည်းစနစ်();ပို့(b':wq\r')
            assert b'two:/' in အမိန့်ဝင်း('echo "$NAME:$PWD"')
            assert '두 번째 ဝင်း'.encode() in အမိန့်ဝင်း('cat ဒုတိယအစဉ်.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ပို့('vi ဒုတိယအစဉ်.txt\n'.encode(),b'NORMAL');ပို့(b'xu',b'NORMAL')
            ပို့(b'iX',b'INSERT');အမိန့်နည်းစနစ်();ပို့(b':q\r',b'Unsaved')
            ပို့(b':q!\r');assert '두 번째 ဝင်း'.encode() in အမိန့်ဝင်း('cat ဒုတိယအစဉ်.txt')
            ပို့(바로가기(1),b'TERMINAL FOCUS 1');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            ပို့(바로가기(1),b'TERMINAL FOCUS 3');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            ပို့(바로가기(1),b'TERMINAL FOCUS 4');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ဒေတာနေရာ.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ဒေတာနေရာ.stdin.flush()
            အမိန့်ဝင်း('echo DRAGGED_OK')
            ပို့('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ပို့('i저장하지 않은 ဒေတာ'.encode(),b'INSERT')
            ပို့(누르기(578,97),b'TERMINAL FOCUS 3');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            assert '버릴문서.txt'.encode() not in အမိန့်ဝင်း('ls')
            ပို့(바로가기(1),b'TERMINAL FOCUS 4');ကိုင်တွယ်ရာဖြစ်ရပ်(.2)
            အမိန့်ဝင်း('echo REUSED_WINDOW_OK')
            완료량=မှတ်တမ်းမှတ်တမ်းတစ်ခု.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            စောင့်(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            အဆုံးအရွေ့=time.monotonic()+.3
            while time.monotonic()<အဆုံးအရွေ့:ကိုင်တွယ်ရာဖြစ်ရပ်(.05)
            with socket.socket(socket.AF_UNIX) as အက္ခရာကုဒ်:
                အက္ခရာကုဒ်.settimeout(10);အက္ခရာကုဒ်.connect(str(모의제어접속))
                with အက္ခရာကုဒ်.makefile('rwb') as ဖိုင်အချက်:
                    json.loads(ဖိုင်အချက်.readline())
                    for တောင်းဆိုချက်တန်ဖိုး in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ဦးတည်ရာတန်ဖိုးနေရာ/'four-terminals.png'),'format':'png'}}):
                        ဖိုင်အချက်.write((json.dumps(တောင်းဆိုချက်တန်ဖိုး)+'\n').encode());ဖိုင်အချက်.flush()
                        while True:
                            ပြန်ပေးတန်ဖိုး=json.loads(ဖိုင်အချက်.readline())
                            if 'error' in ပြန်ပေးတန်ဖိုး:raise AssertionError(ပြန်ပေးတန်ဖိုး)
                            if 'return' in ပြန်ပေးတန်ဖိုး:break
            from PIL import Image
            화소들=Image.open(str(ဦးတည်ရာတန်ဖိုးနေရာ/'four-terminals.png')).convert('RGB')
            for 좌표쌍,ပုံမှတ်အရောင် in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(좌표쌍)==ပုံမှတ်အရောင်,(좌표쌍,화소들.getpixel(좌표쌍))
            အမိန့်ဝင်း('echo FOUR_WINDOWS_OK')
            검증기록.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ဒေတာနေရာ.poll() is None:ဒေတာနေရာ.terminate()
            try:ဒေတာနေရာ.wait(timeout=5)
            except subprocess.TimeoutExpired:ဒေတာနေရာ.kill();ဒေတာနေရာ.wait()
            선택기.close();ဒေတာနေရာ.stdin.close();ဒေတာနေရာ.stdout.close();(ဦးတည်ရာတန်ဖိုးနေရာ/'serial.log').write_bytes(မှတ်တမ်းမှတ်တမ်းတစ်ခု);(ဦးတည်ရာတန်ဖိုးနေရာ/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':လုပ်ဆောင်()
