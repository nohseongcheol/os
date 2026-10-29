#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ,ਕਮਾਂਡ

def ਚਲਾਓ_2():
    ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/windows';ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ.mkdir(parents=True,exist_ok=True)
    ਮਾਨਤਾ_ਵਿਵਰਨ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest()};ਲੌਗ_ਕਤਾਰ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ=subprocess.Popen(ਕਮਾਂਡ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ਚੋਣਕਰਤਾ_a916db4e=selectors.DefaultSelector();ਚੋਣਕਰਤਾ_a916db4e.register(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout,selectors.EVENT_READ)
        def ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(초단위=.1):
            for 누름값,_ in ਚੋਣਕਰਤਾ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ਲੌਗ_ਕਤਾਰ.extend(둘째값)
            assert b'PANIC:' not in ਲੌਗ_ਕਤਾਰ and b'HALTED' not in ਲੌਗ_ਕਤਾਰ,ਲੌਗ_ਕਤਾਰ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+초단위
            while 확인표시 not in ਲੌਗ_ਕਤਾਰ[현재위치:]:
                if time.monotonic()>ਅੰਤ_ਔਫਸੈਟ or ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.poll() is not None:raise AssertionError(ਲੌਗ_ਕਤਾਰ[현재위치:].decode('utf-8','replace'))
                ਸੰਭਾਲਣਾ_ਇਵੈਂਟ()
            return bytes(ਲੌਗ_ਕਤਾਰ[현재위치:])
        def ਈਮੇਲ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ਲੌਗ_ਕਤਾਰ);ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.write(둘째값);ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.flush();return 기다리기(확인표시,현재위치)
        def ਸ਼ੈਲ(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ):return ਈਮੇਲ((ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ਕਲਿਕ_ਕਰੋ_ਬਟਨ(x_ਕੌਔਰਡੀਨੇਟ,세로좌표):return bytes([30,1,1,x_ਕੌਔਰਡੀਨੇਟ&255,x_ਕੌਔਰਡੀਨੇਟ>>8,세로좌표&255,세로좌표>>8,30,1,0,x_ਕੌਔਰਡੀਨੇਟ&255,x_ਕੌਔਰਡੀਨੇਟ>>8,세로좌표&255,세로좌표>>8])
        def ਆਦੇਸ਼_ਮੋਡ():
            ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.write(b'\x1b');ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.flush();ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+.2
            while time.monotonic()<ਅੰਤ_ਔਫਸੈਟ:ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ਸ਼ੈਲ('terminal');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.3)
            ਸ਼ੈਲ('mkdir first; cd first; export NAME=one')
            ਈਮੇਲ('vi 첫째.py\n'.encode(),b'NORMAL')
            ਈਮੇਲ('i값 = 21\nprint(ਕੀਮਤ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+3
            while time.monotonic()<ਅੰਤ_ਔਫਸੈਟ:ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.1)
            ਈਮੇਲ(ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(1),b'TERMINAL FOCUS 2');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            assert b'/\r\n' in ਸ਼ੈਲ('pwd')
            ਸ਼ੈਲ('export NAME=two')
            ਈਮੇਲ('vi 둘째.txt\n'.encode(),b'NORMAL')
            ਈਮੇਲ('i두 번째 ਵਿੰਡੋ\n'.encode(),b'INSERT')
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(180,12),b'TERMINAL FOCUS 1');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            ਆਦੇਸ਼_ਮੋਡ();ਈਮੇਲ(b':wq\r')
            assert b'one:/first' in ਸ਼ੈਲ('echo "$NAME:$PWD"')
            assert 'ਕੀਮਤ = 21\r\nprint(ਕੀਮਤ * 2)'.encode() in ਸ਼ੈਲ('cat 첫째.py')
            ਮਾਪ=ਸ਼ੈਲ('python 첫째.py');assert b'42\r\n' in ਮਾਪ,ਮਾਪ
            # Close the first shell with its actual title-bar X; second editor resumes.
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(560,63),b'TERMINAL FOCUS 2');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            ਆਦੇਸ਼_ਮੋਡ();ਈਮੇਲ(b':wq\r')
            assert b'two:/' in ਸ਼ੈਲ('echo "$NAME:$PWD"')
            assert '두 번째 ਵਿੰਡੋ'.encode() in ਸ਼ੈਲ('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ਈਮੇਲ('vi 둘째.txt\n'.encode(),b'NORMAL');ਈਮੇਲ(b'xu',b'NORMAL')
            ਈਮੇਲ(b'iX',b'INSERT');ਆਦੇਸ਼_ਮੋਡ();ਈਮੇਲ(b':q\r',b'Unsaved')
            ਈਮੇਲ(b':q!\r');assert '두 번째 ਵਿੰਡੋ'.encode() in ਸ਼ੈਲ('cat 둘째.txt')
            ਈਮੇਲ(ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(1),b'TERMINAL FOCUS 1');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            ਈਮੇਲ(ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(1),b'TERMINAL FOCUS 3');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            ਈਮੇਲ(ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(1),b'TERMINAL FOCUS 4');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.flush()
            ਸ਼ੈਲ('echo DRAGGED_OK')
            ਈਮੇਲ('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ਈਮੇਲ('i저장하지 않은 ਸਮੱਗਰੀ'.encode(),b'INSERT')
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(578,97),b'TERMINAL FOCUS 3');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            assert '버릴문서.txt'.encode() not in ਸ਼ੈਲ('ls')
            ਈਮੇਲ(ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(1),b'TERMINAL FOCUS 4');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.2)
            ਸ਼ੈਲ('echo REUSED_WINDOW_OK')
            완료량=ਲੌਗ_ਕਤਾਰ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+.3
            while time.monotonic()<ਅੰਤ_ਔਫਸੈਟ:ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.05)
            with socket.socket(socket.AF_UNIX) as ਵਰਣ_ਕੋਡ:
                ਵਰਣ_ਕੋਡ.settimeout(10);ਵਰਣ_ਕੋਡ.connect(str(모의제어접속))
                with ਵਰਣ_ਕੋਡ.makefile('rwb') as ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ:
                    json.loads(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ/'four-terminals.png'),'format':'png'}}):
                        ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.write((json.dumps(요청값)+'\n').encode());ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.flush()
                        while True:
                            반환값=json.loads(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ/'four-terminals.png')).convert('RGB')
            for ਕੋਔਰਡੀਨੇਟ_ਪੇਅਰ,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ਕੋਔਰਡੀਨੇਟ_ਪੇਅਰ)==색상,(ਕੋਔਰਡੀਨੇਟ_ਪੇਅਰ,화소들.getpixel(ਕੋਔਰਡੀਨੇਟ_ਪੇਅਰ))
            ਸ਼ੈਲ('echo FOUR_WINDOWS_OK')
            ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.poll() is None:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.terminate()
            try:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.wait(timeout=5)
            except subprocess.TimeoutExpired:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.kill();ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.wait()
            ਚੋਣਕਰਤਾ_a916db4e.close();ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.close();ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout.close();(ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ/'serial.log').write_bytes(ਲੌਗ_ਕਤਾਰ);(ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ਚਲਾਓ_2()
