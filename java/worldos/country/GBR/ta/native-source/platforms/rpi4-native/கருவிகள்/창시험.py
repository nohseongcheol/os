#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம்,கட்டளை

def செயல்படுத்துக():
    இலக்கு_மதிப்பு_நிலை=திட்டப்பணி_மூலம்/'build/verification/windows';இலக்கு_மதிப்பு_நிலை.mkdir(parents=True,exist_ok=True)
    செல்லுபடியாக்கம்_அறிக்கை={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((திட்டப்பணி_மூலம்/'build/kernel8.img').read_bytes()).hexdigest()};பதிவு_பதிவு=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        தரவு_நிலை=subprocess.Popen(கட்டளை()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        தேர்வி_a916db4e=selectors.DefaultSelector();தேர்வி_a916db4e.register(தரவு_நிலை.stdout,selectors.EVENT_READ)
        def நடத்தி_நிகழ்வு(초단위=.1):
            for 누름값,_ in தேர்வி_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:பதிவு_பதிவு.extend(둘째값)
            assert b'PANIC:' not in பதிவு_பதிவு and b'HALTED' not in பதிவு_பதிவு,பதிவு_பதிவு[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            முடி_ஆஃப்செட்=time.monotonic()+초단위
            while 확인표시 not in பதிவு_பதிவு[현재위치:]:
                if time.monotonic()>முடி_ஆஃப்செட் or தரவு_நிலை.poll() is not None:raise AssertionError(பதிவு_பதிவு[현재위치:].decode('utf-8','replace'))
                நடத்தி_நிகழ்வு()
            return bytes(பதிவு_பதிவு[현재위치:])
        def அனுப்பு(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(பதிவு_பதிவு);தரவு_நிலை.stdin.write(둘째값);தரவு_நிலை.stdin.flush();return 기다리기(확인표시,현재위치)
        def கூடு(சரம்_தரவு):return அனுப்பு((சரம்_தரவு+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def குறுக்குவழி_மதிப்பு(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def கிளிக்_செய்_பொத்தான்(x_ஒத்ததரமுள்ளது,Y_பொத்தான்_அச்சுத்_தொகுப்பு):return bytes([30,1,1,x_ஒத்ததரமுள்ளது&255,x_ஒத்ததரமுள்ளது>>8,Y_பொத்தான்_அச்சுத்_தொகுப்பு&255,Y_பொத்தான்_அச்சுத்_தொகுப்பு>>8,30,1,0,x_ஒத்ததரமுள்ளது&255,x_ஒத்ததரமுள்ளது>>8,Y_பொத்தான்_அச்சுத்_தொகுப்பு&255,Y_பொத்தான்_அச்சுத்_தொகுப்பு>>8])
        def கட்டளை_பயன்முறை():
            தரவு_நிலை.stdin.write(b'\x1b');தரவு_நிலை.stdin.flush();முடி_ஆஃப்செட்=time.monotonic()+.2
            while time.monotonic()<முடி_ஆஃப்செட்:நடத்தி_நிகழ்வு(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            கூடு('terminal');நடத்தி_நிகழ்வு(.3)
            கூடு('mkdir first; cd first; export NAME=one')
            அனுப்பு('vi 첫째.py\n'.encode(),b'NORMAL')
            அனுப்பு('i값 = 21\nprint(மதிப்பு * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            முடி_ஆஃப்செட்=time.monotonic()+3
            while time.monotonic()<முடி_ஆஃப்செட்:நடத்தி_நிகழ்வு(.1)
            அனுப்பு(குறுக்குவழி_மதிப்பு(1),b'TERMINAL FOCUS 2');நடத்தி_நிகழ்வு(.2)
            assert b'/\r\n' in கூடு('pwd')
            கூடு('export NAME=two')
            அனுப்பு('vi 둘째.txt\n'.encode(),b'NORMAL')
            அனுப்பு('i두 번째 சாளரம்\n'.encode(),b'INSERT')
            அனுப்பு(கிளிக்_செய்_பொத்தான்(180,12),b'TERMINAL FOCUS 1');நடத்தி_நிகழ்வு(.2)
            கட்டளை_பயன்முறை();அனுப்பு(b':wq\r')
            assert b'one:/first' in கூடு('echo "$NAME:$PWD"')
            assert 'மதிப்பு = 21\r\nprint(மதிப்பு * 2)'.encode() in கூடு('cat 첫째.py')
            அளவிடக்கூடியது=கூடு('python 첫째.py');assert b'42\r\n' in அளவிடக்கூடியது,அளவிடக்கூடியது
            # Close the first shell with its actual title-bar X; second editor resumes.
            அனுப்பு(கிளிக்_செய்_பொத்தான்(560,63),b'TERMINAL FOCUS 2');நடத்தி_நிகழ்வு(.2)
            கட்டளை_பயன்முறை();அனுப்பு(b':wq\r')
            assert b'two:/' in கூடு('echo "$NAME:$PWD"')
            assert '두 번째 சாளரம்'.encode() in கூடு('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            அனுப்பு('vi 둘째.txt\n'.encode(),b'NORMAL');அனுப்பு(b'xu',b'NORMAL')
            அனுப்பு(b'iX',b'INSERT');கட்டளை_பயன்முறை();அனுப்பு(b':q\r',b'Unsaved')
            அனுப்பு(b':q!\r');assert '두 번째 சாளரம்'.encode() in கூடு('cat 둘째.txt')
            அனுப்பு(குறுக்குவழி_மதிப்பு(1),b'TERMINAL FOCUS 1');நடத்தி_நிகழ்வு(.2)
            அனுப்பு(குறுக்குவழி_மதிப்பு(1),b'TERMINAL FOCUS 3');நடத்தி_நிகழ்வு(.2)
            அனுப்பு(குறுக்குவழி_மதிப்பு(1),b'TERMINAL FOCUS 4');நடத்தி_நிகழ்வு(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            தரவு_நிலை.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));தரவு_நிலை.stdin.flush()
            கூடு('echo DRAGGED_OK')
            அனுப்பு('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            அனுப்பு('i저장하지 않은 தரவு'.encode(),b'INSERT')
            அனுப்பு(கிளிக்_செய்_பொத்தான்(578,97),b'TERMINAL FOCUS 3');நடத்தி_நிகழ்வு(.2)
            assert '버릴문서.txt'.encode() not in கூடு('ls')
            அனுப்பு(குறுக்குவழி_மதிப்பு(1),b'TERMINAL FOCUS 4');நடத்தி_நிகழ்வு(.2)
            கூடு('echo REUSED_WINDOW_OK')
            완료량=பதிவு_பதிவு.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            முடி_ஆஃப்செட்=time.monotonic()+.3
            while time.monotonic()<முடி_ஆஃப்செட்:நடத்தி_நிகழ்வு(.05)
            with socket.socket(socket.AF_UNIX) as எழுத்துக்குறி_குறியீடு:
                எழுத்துக்குறி_குறியீடு.settimeout(10);எழுத்துக்குறி_குறியீடு.connect(str(모의제어접속))
                with எழுத்துக்குறி_குறியீடு.makefile('rwb') as கோப்பு_உள்ளீடு:
                    json.loads(கோப்பு_உள்ளீடு.readline())
                    for HTTP_வேண்டுதல்_மதிப்பு in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(இலக்கு_மதிப்பு_நிலை/'four-terminals.png'),'format':'png'}}):
                        கோப்பு_உள்ளீடு.write((json.dumps(HTTP_வேண்டுதல்_மதிப்பு)+'\n').encode());கோப்பு_உள்ளீடு.flush()
                        while True:
                            반환값=json.loads(கோப்பு_உள்ளீடு.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(இலக்கு_மதிப்பு_நிலை/'four-terminals.png')).convert('RGB')
            for அச்சுத்_தொகுப்பு_ஜோடி,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(அச்சுத்_தொகுப்பு_ஜோடி)==색상,(அச்சுத்_தொகுப்பு_ஜோடி,화소들.getpixel(அச்சுத்_தொகுப்பு_ஜோடி))
            கூடு('echo FOUR_WINDOWS_OK')
            செல்லுபடியாக்கம்_அறிக்கை.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if தரவு_நிலை.poll() is None:தரவு_நிலை.terminate()
            try:தரவு_நிலை.wait(timeout=5)
            except subprocess.TimeoutExpired:தரவு_நிலை.kill();தரவு_நிலை.wait()
            தேர்வி_a916db4e.close();தரவு_நிலை.stdin.close();தரவு_நிலை.stdout.close();(இலக்கு_மதிப்பு_நிலை/'serial.log').write_bytes(பதிவு_பதிவு);(இலக்கு_மதிப்பு_நிலை/'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':செயல்படுத்துக()
