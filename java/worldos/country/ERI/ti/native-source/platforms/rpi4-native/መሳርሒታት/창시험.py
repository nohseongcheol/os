#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ተግብር_ትእዛዝ import 기준,ትእዛዝ

def ኣኺድ():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    ምርግጋፅ_ጸብጻብ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};ምዝጉብ_ሪጋ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        መራፂ_a916db4e=selectors.DefaultSelector();መራፂ_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def መትሓዚ_ፍጻመ(초단위=.1):
            for 누름값,_ in መራፂ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ምዝጉብ_ሪጋ.extend(둘째값)
            assert b'PANIC:' not in ምዝጉብ_ሪጋ and b'HALTED' not in ምዝጉብ_ሪጋ,ምዝጉብ_ሪጋ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ኣቑም_ሽፋን=time.monotonic()+초단위
            while 확인표시 not in ምዝጉብ_ሪጋ[현재위치:]:
                if time.monotonic()>ኣቑም_ሽፋን or 자료위치.poll() is not None:raise AssertionError(ምዝጉብ_ሪጋ[현재위치:].decode('utf-8','replace'))
                መትሓዚ_ፍጻመ()
            return bytes(ምዝጉብ_ሪጋ[현재위치:])
        def ለኣኽ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ምዝጉብ_ሪጋ);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def ሽፋን(ሕብረ_ቁምፊ_ሓበሬታ):return ለኣኽ((ሕብረ_ቁምፊ_ሓበሬታ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ኣቋራጭ_ዋጋ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ጠዉቕ_መጠወቒ(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def ትእዛዝ_ኹነት():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();ኣቑም_ሽፋን=time.monotonic()+.2
            while time.monotonic()<ኣቑም_ሽፋን:መትሓዚ_ፍጻመ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ሽፋን('terminal');መትሓዚ_ፍጻመ(.3)
            ሽፋን('mkdir first; cd first; export NAME=one')
            ለኣኽ('vi 첫째.py\n'.encode(),b'NORMAL')
            ለኣኽ('i값 = 21\nprint(ዋጋ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ኣቑም_ሽፋን=time.monotonic()+3
            while time.monotonic()<ኣቑም_ሽፋን:መትሓዚ_ፍጻመ(.1)
            ለኣኽ(ኣቋራጭ_ዋጋ(1),b'TERMINAL FOCUS 2');መትሓዚ_ፍጻመ(.2)
            assert b'/\r\n' in ሽፋን('pwd')
            ሽፋን('export NAME=two')
            ለኣኽ('vi 둘째.txt\n'.encode(),b'NORMAL')
            ለኣኽ('i두 번째 መስኮት\n'.encode(),b'INSERT')
            ለኣኽ(ጠዉቕ_መጠወቒ(180,12),b'TERMINAL FOCUS 1');መትሓዚ_ፍጻመ(.2)
            ትእዛዝ_ኹነት();ለኣኽ(b':wq\r')
            assert b'one:/first' in ሽፋን('echo "$NAME:$PWD"')
            assert 'ዋጋ = 21\r\nprint(ዋጋ * 2)'.encode() in ሽፋን('cat 첫째.py')
            결과=ሽፋን('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            ለኣኽ(ጠዉቕ_መጠወቒ(560,63),b'TERMINAL FOCUS 2');መትሓዚ_ፍጻመ(.2)
            ትእዛዝ_ኹነት();ለኣኽ(b':wq\r')
            assert b'two:/' in ሽፋን('echo "$NAME:$PWD"')
            assert '두 번째 መስኮት'.encode() in ሽፋን('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ለኣኽ('vi 둘째.txt\n'.encode(),b'NORMAL');ለኣኽ(b'xu',b'NORMAL')
            ለኣኽ(b'iX',b'INSERT');ትእዛዝ_ኹነት();ለኣኽ(b':q\r',b'Unsaved')
            ለኣኽ(b':q!\r');assert '두 번째 መስኮት'.encode() in ሽፋን('cat 둘째.txt')
            ለኣኽ(ኣቋራጭ_ዋጋ(1),b'TERMINAL FOCUS 1');መትሓዚ_ፍጻመ(.2)
            ለኣኽ(ኣቋራጭ_ዋጋ(1),b'TERMINAL FOCUS 3');መትሓዚ_ፍጻመ(.2)
            ለኣኽ(ኣቋራጭ_ዋጋ(1),b'TERMINAL FOCUS 4');መትሓዚ_ፍጻመ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            ሽፋን('echo DRAGGED_OK')
            ለኣኽ('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ለኣኽ('i저장하지 않은 ሓበሬታ'.encode(),b'INSERT')
            ለኣኽ(ጠዉቕ_መጠወቒ(578,97),b'TERMINAL FOCUS 3');መትሓዚ_ፍጻመ(.2)
            assert '버릴문서.txt'.encode() not in ሽፋን('ls')
            ለኣኽ(ኣቋራጭ_ዋጋ(1),b'TERMINAL FOCUS 4');መትሓዚ_ፍጻመ(.2)
            ሽፋን('echo REUSED_WINDOW_OK')
            완료량=ምዝጉብ_ሪጋ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ኣቑም_ሽፋን=time.monotonic()+.3
            while time.monotonic()<ኣቑም_ሽፋን:መትሓዚ_ፍጻመ(.05)
            with socket.socket(socket.AF_UNIX) as ኮድ_ፊደል:
                ኮድ_ፊደል.settimeout(10);ኮድ_ፊደል.connect(str(모의제어접속))
                with ኮድ_ፊደል.makefile('rwb') as ፋይል_ምእታው:
                    json.loads(ፋይል_ምእታው.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        ፋይል_ምእታው.write((json.dumps(요청값)+'\n').encode());ፋይል_ምእታው.flush()
                        while True:
                            반환값=json.loads(ፋይል_ምእታው.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for ጸምዲ_ኣማራዱ,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ጸምዲ_ኣማራዱ)==색상,(ጸምዲ_ኣማራዱ,화소들.getpixel(ጸምዲ_ኣማራዱ))
            ሽፋን('echo FOUR_WINDOWS_OK')
            ምርግጋፅ_ጸብጻብ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            መራፂ_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ምዝጉብ_ሪጋ);(목적위치/'report.json').write_text(json.dumps(ምርግጋፅ_ጸብጻብ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ኣኺድ()
