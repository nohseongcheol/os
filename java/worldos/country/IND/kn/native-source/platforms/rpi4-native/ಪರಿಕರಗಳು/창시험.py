#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ,ಆಜ್ಞೆ

def ಚಲಾಯಿಸು_2():
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/windows';ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ.mkdir(parents=True,exist_ok=True)
    ದೃಢೀಕರಣ_ವರದಿ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest()};ಲಾಗ್_ದಾಖಲೆ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ಡೇಟಾ_ಹುದ್ದೆ=subprocess.Popen(ಆಜ್ಞೆ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ಸೆಲೆಕ್ಟರ್_a916db4e=selectors.DefaultSelector();ಸೆಲೆಕ್ಟರ್_a916db4e.register(ಡೇಟಾ_ಹುದ್ದೆ.stdout,selectors.EVENT_READ)
        def ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(초단위=.1):
            for 누름값,_ in ಸೆಲೆಕ್ಟರ್_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ಲಾಗ್_ದಾಖಲೆ.extend(둘째값)
            assert b'PANIC:' not in ಲಾಗ್_ದಾಖಲೆ and b'HALTED' not in ಲಾಗ್_ದಾಖಲೆ,ಲಾಗ್_ದಾಖಲೆ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+초단위
            while 확인표시 not in ಲಾಗ್_ದಾಖಲೆ[현재위치:]:
                if time.monotonic()>ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್ or ಡೇಟಾ_ಹುದ್ದೆ.poll() is not None:raise AssertionError(ಲಾಗ್_ದಾಖಲೆ[현재위치:].decode('utf-8','replace'))
                ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ()
            return bytes(ಲಾಗ್_ದಾಖಲೆ[현재위치:])
        def ಕಳುಹಿಸಿ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ಲಾಗ್_ದಾಖಲೆ);ಡೇಟಾ_ಹುದ್ದೆ.stdin.write(둘째값);ಡೇಟಾ_ಹುದ್ದೆ.stdin.flush();return 기다리기(확인표시,현재위치)
        def ಶೆಲ್(ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ):return ಕಳುಹಿಸಿ((ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ):return bytes([30,1,1,x_ಸಮಭಾಜಕ&255,x_ಸಮಭಾಜಕ>>8,Y_ಬಟನ್_ಸಮನ್ವಯ&255,Y_ಬಟನ್_ಸಮನ್ವಯ>>8,30,1,0,x_ಸಮಭಾಜಕ&255,x_ಸಮಭಾಜಕ>>8,Y_ಬಟನ್_ಸಮನ್ವಯ&255,Y_ಬಟನ್_ಸಮನ್ವಯ>>8])
        def ಆದೇಶ_ಮೋಡ್():
            ಡೇಟಾ_ಹುದ್ದೆ.stdin.write(b'\x1b');ಡೇಟಾ_ಹುದ್ದೆ.stdin.flush();ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+.2
            while time.monotonic()<ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್:ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ಶೆಲ್('terminal');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.3)
            ಶೆಲ್('mkdir first; cd first; export NAME=one')
            ಕಳುಹಿಸಿ('vi 첫째.py\n'.encode(),b'NORMAL')
            ಕಳುಹಿಸಿ('i값 = 21\nprint(ಮೌಲ್ಯ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+3
            while time.monotonic()<ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್:ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.1)
            ಕಳುಹಿಸಿ(ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(1),b'TERMINAL FOCUS 2');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            assert b'/\r\n' in ಶೆಲ್('pwd')
            ಶೆಲ್('export NAME=two')
            ಕಳುಹಿಸಿ('vi 둘째.txt\n'.encode(),b'NORMAL')
            ಕಳುಹಿಸಿ('i두 번째 ವಿಂಡೋ\n'.encode(),b'INSERT')
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(180,12),b'TERMINAL FOCUS 1');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            ಆದೇಶ_ಮೋಡ್();ಕಳುಹಿಸಿ(b':wq\r')
            assert b'one:/first' in ಶೆಲ್('echo "$NAME:$PWD"')
            assert 'ಮೌಲ್ಯ = 21\r\nprint(ಮೌಲ್ಯ * 2)'.encode() in ಶೆಲ್('cat 첫째.py')
            ಮಾಪನ=ಶೆಲ್('python 첫째.py');assert b'42\r\n' in ಮಾಪನ,ಮಾಪನ
            # Close the first shell with its actual title-bar X; second editor resumes.
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(560,63),b'TERMINAL FOCUS 2');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            ಆದೇಶ_ಮೋಡ್();ಕಳುಹಿಸಿ(b':wq\r')
            assert b'two:/' in ಶೆಲ್('echo "$NAME:$PWD"')
            assert '두 번째 ವಿಂಡೋ'.encode() in ಶೆಲ್('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ಕಳುಹಿಸಿ('vi 둘째.txt\n'.encode(),b'NORMAL');ಕಳುಹಿಸಿ(b'xu',b'NORMAL')
            ಕಳುಹಿಸಿ(b'iX',b'INSERT');ಆದೇಶ_ಮೋಡ್();ಕಳುಹಿಸಿ(b':q\r',b'Unsaved')
            ಕಳುಹಿಸಿ(b':q!\r');assert '두 번째 ವಿಂಡೋ'.encode() in ಶೆಲ್('cat 둘째.txt')
            ಕಳುಹಿಸಿ(ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(1),b'TERMINAL FOCUS 1');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            ಕಳುಹಿಸಿ(ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(1),b'TERMINAL FOCUS 3');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            ಕಳುಹಿಸಿ(ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(1),b'TERMINAL FOCUS 4');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ಡೇಟಾ_ಹುದ್ದೆ.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ಡೇಟಾ_ಹುದ್ದೆ.stdin.flush()
            ಶೆಲ್('echo DRAGGED_OK')
            ಕಳುಹಿಸಿ('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ಕಳುಹಿಸಿ('i저장하지 않은 ಡೇಟಾ'.encode(),b'INSERT')
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(578,97),b'TERMINAL FOCUS 3');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            assert '버릴문서.txt'.encode() not in ಶೆಲ್('ls')
            ಕಳುಹಿಸಿ(ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(1),b'TERMINAL FOCUS 4');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.2)
            ಶೆಲ್('echo REUSED_WINDOW_OK')
            완료량=ಲಾಗ್_ದಾಖಲೆ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+.3
            while time.monotonic()<ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್:ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.05)
            with socket.socket(socket.AF_UNIX) as ಅಕ್ಷರ_ಕೋಡ್:
                ಅಕ್ಷರ_ಕೋಡ್.settimeout(10);ಅಕ್ಷರ_ಕೋಡ್.connect(str(모의제어접속))
                with ಅಕ್ಷರ_ಕೋಡ್.makefile('rwb') as ಫೈಲ್_ನಮೂದು:
                    json.loads(ಫೈಲ್_ನಮೂದು.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ/'four-terminals.png'),'format':'png'}}):
                        ಫೈಲ್_ನಮೂದು.write((json.dumps(요청값)+'\n').encode());ಫೈಲ್_ನಮೂದು.flush()
                        while True:
                            반환값=json.loads(ಫೈಲ್_ನಮೂದು.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ/'four-terminals.png')).convert('RGB')
            for ಕೊ_ಆರ್ಡಿನೆಟ್_ಪೇರ್,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ಕೊ_ಆರ್ಡಿನೆಟ್_ಪೇರ್)==색상,(ಕೊ_ಆರ್ಡಿನೆಟ್_ಪೇರ್,화소들.getpixel(ಕೊ_ಆರ್ಡಿನೆಟ್_ಪೇರ್))
            ಶೆಲ್('echo FOUR_WINDOWS_OK')
            ದೃಢೀಕರಣ_ವರದಿ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ಡೇಟಾ_ಹುದ್ದೆ.poll() is None:ಡೇಟಾ_ಹುದ್ದೆ.terminate()
            try:ಡೇಟಾ_ಹುದ್ದೆ.wait(timeout=5)
            except subprocess.TimeoutExpired:ಡೇಟಾ_ಹುದ್ದೆ.kill();ಡೇಟಾ_ಹುದ್ದೆ.wait()
            ಸೆಲೆಕ್ಟರ್_a916db4e.close();ಡೇಟಾ_ಹುದ್ದೆ.stdin.close();ಡೇಟಾ_ಹುದ್ದೆ.stdout.close();(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ/'serial.log').write_bytes(ಲಾಗ್_ದಾಖಲೆ);(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ಚಲಾಯಿಸು_2()
