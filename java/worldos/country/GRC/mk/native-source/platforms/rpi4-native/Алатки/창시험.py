#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Изврши_наредба import Project_корен,Команда

def Изврши_2():
    одредиште_VALUE_позиционирање=Project_корен/'build/verification/windows';одредиште_VALUE_позиционирање.mkdir(parents=True,exist_ok=True)
    проверка_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ред=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        податоци_позиционирање=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        избирач_a916db4e=selectors.DefaultSelector();избирач_a916db4e.register(податоци_позиционирање.stdout,selectors.EVENT_READ)
        def рачка_настан(초단위=.1):
            for 누름값,_ in избирач_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ред.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ред and b'HALTED' not in LOG_ред,LOG_ред[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            крај_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ред[현재위치:]:
                if time.monotonic()>крај_OFFSET or податоци_позиционирање.poll() is not None:raise AssertionError(LOG_ред[현재위치:].decode('utf-8','replace'))
                рачка_настан()
            return bytes(LOG_ред[현재위치:])
        def испрати(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ред);податоци_позиционирање.stdin.write(SECOND_VALUE);податоци_позиционирање.stdin.flush();return 기다리기(확인표시,현재위치)
        def обвивка(низа_податоци):return испрати((низа_податоци+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def брз_пристап_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def кликни_копче(координата_х,세로좌표):return bytes([30,1,1,координата_х&255,координата_х>>8,세로좌표&255,세로좌표>>8,30,1,0,координата_х&255,координата_х>>8,세로좌표&255,세로좌표>>8])
        def наредба_MODE():
            податоци_позиционирање.stdin.write(b'\x1b');податоци_позиционирање.stdin.flush();крај_OFFSET=time.monotonic()+.2
            while time.monotonic()<крај_OFFSET:рачка_настан(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            обвивка('terminal');рачка_настан(.3)
            обвивка('mkdir first; cd first; export NAME=one')
            испрати('vi 첫째.py\n'.encode(),b'NORMAL')
            испрати('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            крај_OFFSET=time.monotonic()+3
            while time.monotonic()<крај_OFFSET:рачка_настан(.1)
            испрати(брз_пристап_VALUE(1),b'TERMINAL FOCUS 2');рачка_настан(.2)
            assert b'/\r\n' in обвивка('pwd')
            обвивка('export NAME=two')
            испрати('vi 둘째.txt\n'.encode(),b'NORMAL')
            испрати('i두 번째 прозорец\n'.encode(),b'INSERT')
            испрати(кликни_копче(180,12),b'TERMINAL FOCUS 1');рачка_настан(.2)
            наредба_MODE();испрати(b':wq\r')
            assert b'one:/first' in обвивка('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in обвивка('cat 첫째.py')
            мерка=обвивка('python 첫째.py');assert b'42\r\n' in мерка,мерка
            # Close the first shell with its actual title-bar X; second editor resumes.
            испрати(кликни_копче(560,63),b'TERMINAL FOCUS 2');рачка_настан(.2)
            наредба_MODE();испрати(b':wq\r')
            assert b'two:/' in обвивка('echo "$NAME:$PWD"')
            assert '두 번째 прозорец'.encode() in обвивка('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            испрати('vi 둘째.txt\n'.encode(),b'NORMAL');испрати(b'xu',b'NORMAL')
            испрати(b'iX',b'INSERT');наредба_MODE();испрати(b':q\r',b'Unsaved')
            испрати(b':q!\r');assert '두 번째 прозорец'.encode() in обвивка('cat 둘째.txt')
            испрати(брз_пристап_VALUE(1),b'TERMINAL FOCUS 1');рачка_настан(.2)
            испрати(брз_пристап_VALUE(1),b'TERMINAL FOCUS 3');рачка_настан(.2)
            испрати(брз_пристап_VALUE(1),b'TERMINAL FOCUS 4');рачка_настан(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            податоци_позиционирање.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));податоци_позиционирање.stdin.flush()
            обвивка('echo DRAGGED_OK')
            испрати('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            испрати('i저장하지 않은 податоци'.encode(),b'INSERT')
            испрати(кликни_копче(578,97),b'TERMINAL FOCUS 3');рачка_настан(.2)
            assert '버릴문서.txt'.encode() not in обвивка('ls')
            испрати(брз_пристап_VALUE(1),b'TERMINAL FOCUS 4');рачка_настан(.2)
            обвивка('echo REUSED_WINDOW_OK')
            완료량=LOG_ред.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            крај_OFFSET=time.monotonic()+.3
            while time.monotonic()<крај_OFFSET:рачка_настан(.05)
            with socket.socket(socket.AF_UNIX) as кодна_точка:
                кодна_точка.settimeout(10);кодна_точка.connect(str(모의제어접속))
                with кодна_точка.makefile('rwb') as датотека_внес:
                    json.loads(датотека_внес.readline())
                    for Барање_на_HTTP_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(одредиште_VALUE_позиционирање/'four-terminals.png'),'format':'png'}}):
                        датотека_внес.write((json.dumps(Барање_на_HTTP_VALUE)+'\n').encode());датотека_внес.flush()
                        while True:
                            반환값=json.loads(датотека_внес.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(одредиште_VALUE_позиционирање/'four-terminals.png')).convert('RGB')
            for координативен_пар,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(координативен_пар)==색상,(координативен_пар,화소들.getpixel(координативен_пар))
            обвивка('echo FOUR_WINDOWS_OK')
            проверка_извештај.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if податоци_позиционирање.poll() is None:податоци_позиционирање.terminate()
            try:податоци_позиционирање.wait(timeout=5)
            except subprocess.TimeoutExpired:податоци_позиционирање.kill();податоци_позиционирање.wait()
            избирач_a916db4e.close();податоци_позиционирање.stdin.close();податоци_позиционирање.stdout.close();(одредиште_VALUE_позиционирање/'serial.log').write_bytes(LOG_ред);(одредиште_VALUE_позиционирање/'report.json').write_text(json.dumps(проверка_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Изврши_2()
