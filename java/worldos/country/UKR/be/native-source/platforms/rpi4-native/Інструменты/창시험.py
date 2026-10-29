#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from выканаць_каманда import 기준,Загад

def Выканаць():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    праверка_справаздача={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};журнал_запіс=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Загад()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектар_a916db4e=selectors.DefaultSelector();селектар_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def маркер_падзея(초단위=.1):
            for 누름값,_ in селектар_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:журнал_запіс.extend(둘째값)
            assert b'PANIC:' not in журнал_запіс and b'HALTED' not in журнал_запіс,журнал_запіс[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            скончыць_Зрух=time.monotonic()+초단위
            while 확인표시 not in журнал_запіс[현재위치:]:
                if time.monotonic()>скончыць_Зрух or 자료위치.poll() is not None:raise AssertionError(журнал_запіс[현재위치:].decode('utf-8','replace'))
                маркер_падзея()
            return bytes(журнал_запіс[현재위치:])
        def адправіць(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(журнал_запіс);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def абалонка(радок_дадзеныя):return адправіць((радок_дадзеныя+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ярлык_значэнне(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def націснуць_кнопка(каардыната_x,세로좌표):return bytes([30,1,1,каардыната_x&255,каардыната_x>>8,세로좌표&255,세로좌표>>8,30,1,0,каардыната_x&255,каардыната_x>>8,세로좌표&255,세로좌표>>8])
        def каманда_рэжым():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();скончыць_Зрух=time.monotonic()+.2
            while time.monotonic()<скончыць_Зрух:маркер_падзея(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            абалонка('terminal');маркер_падзея(.3)
            абалонка('mkdir first; cd first; export NAME=one')
            адправіць('vi 첫째.py\n'.encode(),b'NORMAL')
            адправіць('i값 = 21\nprint(значэнне * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            скончыць_Зрух=time.monotonic()+3
            while time.monotonic()<скончыць_Зрух:маркер_падзея(.1)
            адправіць(ярлык_значэнне(1),b'TERMINAL FOCUS 2');маркер_падзея(.2)
            assert b'/\r\n' in абалонка('pwd')
            абалонка('export NAME=two')
            адправіць('vi 둘째.txt\n'.encode(),b'NORMAL')
            адправіць('i두 번째 акно\n'.encode(),b'INSERT')
            адправіць(націснуць_кнопка(180,12),b'TERMINAL FOCUS 1');маркер_падзея(.2)
            каманда_рэжым();адправіць(b':wq\r')
            assert b'one:/first' in абалонка('echo "$NAME:$PWD"')
            assert 'значэнне = 21\r\nprint(значэнне * 2)'.encode() in абалонка('cat 첫째.py')
            결과=абалонка('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            адправіць(націснуць_кнопка(560,63),b'TERMINAL FOCUS 2');маркер_падзея(.2)
            каманда_рэжым();адправіць(b':wq\r')
            assert b'two:/' in абалонка('echo "$NAME:$PWD"')
            assert '두 번째 акно'.encode() in абалонка('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            адправіць('vi 둘째.txt\n'.encode(),b'NORMAL');адправіць(b'xu',b'NORMAL')
            адправіць(b'iX',b'INSERT');каманда_рэжым();адправіць(b':q\r',b'Unsaved')
            адправіць(b':q!\r');assert '두 번째 акно'.encode() in абалонка('cat 둘째.txt')
            адправіць(ярлык_значэнне(1),b'TERMINAL FOCUS 1');маркер_падзея(.2)
            адправіць(ярлык_значэнне(1),b'TERMINAL FOCUS 3');маркер_падзея(.2)
            адправіць(ярлык_значэнне(1),b'TERMINAL FOCUS 4');маркер_падзея(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            абалонка('echo DRAGGED_OK')
            адправіць('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            адправіць('i저장하지 않은 дадзеныя'.encode(),b'INSERT')
            адправіць(націснуць_кнопка(578,97),b'TERMINAL FOCUS 3');маркер_падзея(.2)
            assert '버릴문서.txt'.encode() not in абалонка('ls')
            адправіць(ярлык_значэнне(1),b'TERMINAL FOCUS 4');маркер_падзея(.2)
            абалонка('echo REUSED_WINDOW_OK')
            완료량=журнал_запіс.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            скончыць_Зрух=time.monotonic()+.3
            while time.monotonic()<скончыць_Зрух:маркер_падзея(.05)
            with socket.socket(socket.AF_UNIX) as код_сімвала:
                код_сімвала.settimeout(10);код_сімвала.connect(str(모의제어접속))
                with код_сімвала.makefile('rwb') as файл_увядзенне:
                    json.loads(файл_увядзенне.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        файл_увядзенне.write((json.dumps(요청값)+'\n').encode());файл_увядзенне.flush()
                        while True:
                            반환값=json.loads(файл_увядзенне.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for пара_каардынат,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(пара_каардынат)==색상,(пара_каардынат,화소들.getpixel(пара_каардынат))
            абалонка('echo FOUR_WINDOWS_OK')
            праверка_справаздача.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            селектар_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(журнал_запіс);(목적위치/'report.json').write_text(json.dumps(праверка_справаздача,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Выканаць()
