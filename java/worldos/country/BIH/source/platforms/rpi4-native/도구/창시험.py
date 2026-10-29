#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import 기준,команда

def 시작():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    провјера_извјештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};дневник_рада_ред=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(자료위치.stdout,selectors.EVENT_READ)
        def хватиште_догађај(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:дневник_рада_ред.extend(둘째값)
            assert b'PANIC:' not in дневник_рада_ред and b'HALTED' not in дневник_рада_ред,дневник_рада_ред[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in дневник_рада_ред[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(дневник_рада_ред[현재위치:].decode('utf-8','replace'))
                хватиште_догађај()
            return bytes(дневник_рада_ред[현재위치:])
        def послати(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(дневник_рада_ред);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def љуска(стринг_подаци):return послати((стринг_подаци+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def пречица_вриједност(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def кликнути_дугме(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def команда_мод():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:хватиште_догађај(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            љуска('terminal');хватиште_догађај(.3)
            љуска('mkdir first; cd first; export NAME=one')
            послати('vi 첫째.py\n'.encode(),b'NORMAL')
            послати('i값 = 21\nprint(вриједност * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:хватиште_догађај(.1)
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 2');хватиште_догађај(.2)
            assert b'/\r\n' in љуска('pwd')
            љуска('export NAME=two')
            послати('vi 둘째.txt\n'.encode(),b'NORMAL')
            послати('i두 번째 прозор\n'.encode(),b'INSERT')
            послати(кликнути_дугме(180,12),b'TERMINAL FOCUS 1');хватиште_догађај(.2)
            команда_мод();послати(b':wq\r')
            assert b'one:/first' in љуска('echo "$NAME:$PWD"')
            assert 'вриједност = 21\r\nprint(вриједност * 2)'.encode() in љуска('cat 첫째.py')
            결과=љуска('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            послати(кликнути_дугме(560,63),b'TERMINAL FOCUS 2');хватиште_догађај(.2)
            команда_мод();послати(b':wq\r')
            assert b'two:/' in љуска('echo "$NAME:$PWD"')
            assert '두 번째 прозор'.encode() in љуска('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            послати('vi 둘째.txt\n'.encode(),b'NORMAL');послати(b'xu',b'NORMAL')
            послати(b'iX',b'INSERT');команда_мод();послати(b':q\r',b'Unsaved')
            послати(b':q!\r');assert '두 번째 прозор'.encode() in љуска('cat 둘째.txt')
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 1');хватиште_догађај(.2)
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 3');хватиште_догађај(.2)
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 4');хватиште_догађај(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            љуска('echo DRAGGED_OK')
            послати('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            послати('i저장하지 않은 подаци'.encode(),b'INSERT')
            послати(кликнути_дугме(578,97),b'TERMINAL FOCUS 3');хватиште_догађај(.2)
            assert '버릴문서.txt'.encode() not in љуска('ls')
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 4');хватиште_догађај(.2)
            љуска('echo REUSED_WINDOW_OK')
            완료량=дневник_рада_ред.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:хватиште_догађај(.05)
            with socket.socket(socket.AF_UNIX) as кôд_знака:
                кôд_знака.settimeout(10);кôд_знака.connect(str(모의제어접속))
                with кôд_знака.makefile('rwb') as фајл_унос:
                    json.loads(фајл_унос.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        фајл_унос.write((json.dumps(요청값)+'\n').encode());фајл_унос.flush()
                        while True:
                            반환값=json.loads(фајл_унос.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for Координатни_пар,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(Координатни_пар)==색상,(Координатни_пар,화소들.getpixel(Координатни_пар))
            љуска('echo FOUR_WINDOWS_OK')
            провјера_извјештај.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            선택기.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(дневник_рада_ред);(목적위치/'report.json').write_text(json.dumps(провјера_извјештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':시작()
