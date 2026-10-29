#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ፈጽም_ትእዛዝ import አሳይ_ስር,ትእዛዝ

def ማስኬጃ():
    መድረሻ_እሴት_በቦታ_አስቀመጠ=አሳይ_ስር/'build/verification/windows';መድረሻ_እሴት_በቦታ_አስቀመጠ.mkdir(parents=True,exist_ok=True)
    ማረጋገጥ_ዘገባ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest()};መዝግብ_ረድፍ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ውሂብ_በቦታ_አስቀመጠ=subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        መራጭ_a916db4e=selectors.DefaultSelector();መራጭ_a916db4e.register(ውሂብ_በቦታ_አስቀመጠ.stdout,selectors.EVENT_READ)
        def እጀታ_ፍጻሜ(초단위=.1):
            for 누름값,_ in መራጭ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:መዝግብ_ረድፍ.extend(둘째값)
            assert b'PANIC:' not in መዝግብ_ረድፍ and b'HALTED' not in መዝግብ_ረድፍ,መዝግብ_ረድፍ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ጨርስ_ዝንፍ=time.monotonic()+초단위
            while 확인표시 not in መዝግብ_ረድፍ[현재위치:]:
                if time.monotonic()>ጨርስ_ዝንፍ or ውሂብ_በቦታ_አስቀመጠ.poll() is not None:raise AssertionError(መዝግብ_ረድፍ[현재위치:].decode('utf-8','replace'))
                እጀታ_ፍጻሜ()
            return bytes(መዝግብ_ረድፍ[현재위치:])
        def ላክ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(መዝግብ_ረድፍ);ውሂብ_በቦታ_አስቀመጠ.stdin.write(둘째값);ውሂብ_በቦታ_አስቀመጠ.stdin.flush();return 기다리기(확인표시,현재위치)
        def ሼል(ኅብረቁምፊ_ውሂብ):return ላክ((ኅብረቁምፊ_ውሂብ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def አቋራጭ_እሴት(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ጠቅ_አድርግ_አዝራር(ኤክስ_አስተባባሪ,세로좌표):return bytes([30,1,1,ኤክስ_አስተባባሪ&255,ኤክስ_አስተባባሪ>>8,세로좌표&255,세로좌표>>8,30,1,0,ኤክስ_አስተባባሪ&255,ኤክስ_አስተባባሪ>>8,세로좌표&255,세로좌표>>8])
        def ትእዛዝ_ሁነታ():
            ውሂብ_በቦታ_አስቀመጠ.stdin.write(b'\x1b');ውሂብ_በቦታ_አስቀመጠ.stdin.flush();ጨርስ_ዝንፍ=time.monotonic()+.2
            while time.monotonic()<ጨርስ_ዝንፍ:እጀታ_ፍጻሜ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ሼል('terminal');እጀታ_ፍጻሜ(.3)
            ሼል('mkdir first; cd first; export NAME=one')
            ላክ('vi 첫째.py\n'.encode(),b'NORMAL')
            ላክ('i값 = 21\nprint(እሴት * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ጨርስ_ዝንፍ=time.monotonic()+3
            while time.monotonic()<ጨርስ_ዝንፍ:እጀታ_ፍጻሜ(.1)
            ላክ(አቋራጭ_እሴት(1),b'TERMINAL FOCUS 2');እጀታ_ፍጻሜ(.2)
            assert b'/\r\n' in ሼል('pwd')
            ሼል('export NAME=two')
            ላክ('vi 둘째.txt\n'.encode(),b'NORMAL')
            ላክ('i두 번째 መስኮት\n'.encode(),b'INSERT')
            ላክ(ጠቅ_አድርግ_አዝራር(180,12),b'TERMINAL FOCUS 1');እጀታ_ፍጻሜ(.2)
            ትእዛዝ_ሁነታ();ላክ(b':wq\r')
            assert b'one:/first' in ሼል('echo "$NAME:$PWD"')
            assert 'እሴት = 21\r\nprint(እሴት * 2)'.encode() in ሼል('cat 첫째.py')
            ልኬት=ሼል('python 첫째.py');assert b'42\r\n' in ልኬት,ልኬት
            # Close the first shell with its actual title-bar X; second editor resumes.
            ላክ(ጠቅ_አድርግ_አዝራር(560,63),b'TERMINAL FOCUS 2');እጀታ_ፍጻሜ(.2)
            ትእዛዝ_ሁነታ();ላክ(b':wq\r')
            assert b'two:/' in ሼል('echo "$NAME:$PWD"')
            assert '두 번째 መስኮት'.encode() in ሼል('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ላክ('vi 둘째.txt\n'.encode(),b'NORMAL');ላክ(b'xu',b'NORMAL')
            ላክ(b'iX',b'INSERT');ትእዛዝ_ሁነታ();ላክ(b':q\r',b'Unsaved')
            ላክ(b':q!\r');assert '두 번째 መስኮት'.encode() in ሼል('cat 둘째.txt')
            ላክ(አቋራጭ_እሴት(1),b'TERMINAL FOCUS 1');እጀታ_ፍጻሜ(.2)
            ላክ(አቋራጭ_እሴት(1),b'TERMINAL FOCUS 3');እጀታ_ፍጻሜ(.2)
            ላክ(አቋራጭ_እሴት(1),b'TERMINAL FOCUS 4');እጀታ_ፍጻሜ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ውሂብ_በቦታ_አስቀመጠ.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ውሂብ_በቦታ_አስቀመጠ.stdin.flush()
            ሼል('echo DRAGGED_OK')
            ላክ('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ላክ('i저장하지 않은 ውሂብ'.encode(),b'INSERT')
            ላክ(ጠቅ_አድርግ_አዝራር(578,97),b'TERMINAL FOCUS 3');እጀታ_ፍጻሜ(.2)
            assert '버릴문서.txt'.encode() not in ሼል('ls')
            ላክ(አቋራጭ_እሴት(1),b'TERMINAL FOCUS 4');እጀታ_ፍጻሜ(.2)
            ሼል('echo REUSED_WINDOW_OK')
            완료량=መዝግብ_ረድፍ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ጨርስ_ዝንፍ=time.monotonic()+.3
            while time.monotonic()<ጨርስ_ዝንፍ:እጀታ_ፍጻሜ(.05)
            with socket.socket(socket.AF_UNIX) as የቁምፊ_ኮድ:
                የቁምፊ_ኮድ.settimeout(10);የቁምፊ_ኮድ.connect(str(모의제어접속))
                with የቁምፊ_ኮድ.makefile('rwb') as ፋይል_ምዝግብ:
                    json.loads(ፋይል_ምዝግብ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(መድረሻ_እሴት_በቦታ_አስቀመጠ/'four-terminals.png'),'format':'png'}}):
                        ፋይል_ምዝግብ.write((json.dumps(요청값)+'\n').encode());ፋይል_ምዝግብ.flush()
                        while True:
                            반환값=json.loads(ፋይል_ምዝግብ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(መድረሻ_እሴት_በቦታ_አስቀመጠ/'four-terminals.png')).convert('RGB')
            for መዋያ_ጥምድ,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(መዋያ_ጥምድ)==색상,(መዋያ_ጥምድ,화소들.getpixel(መዋያ_ጥምድ))
            ሼል('echo FOUR_WINDOWS_OK')
            ማረጋገጥ_ዘገባ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ውሂብ_በቦታ_አስቀመጠ.poll() is None:ውሂብ_በቦታ_አስቀመጠ.terminate()
            try:ውሂብ_በቦታ_አስቀመጠ.wait(timeout=5)
            except subprocess.TimeoutExpired:ውሂብ_በቦታ_አስቀመጠ.kill();ውሂብ_በቦታ_አስቀመጠ.wait()
            መራጭ_a916db4e.close();ውሂብ_በቦታ_አስቀመጠ.stdin.close();ውሂብ_በቦታ_አስቀመጠ.stdout.close();(መድረሻ_እሴት_በቦታ_አስቀመጠ/'serial.log').write_bytes(መዝግብ_ረድፍ);(መድረሻ_እሴት_በቦታ_አስቀመጠ/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ማስኬጃ()
