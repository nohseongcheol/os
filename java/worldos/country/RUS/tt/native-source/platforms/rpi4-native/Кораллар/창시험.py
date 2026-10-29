#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from үтәргә_команда import экранга_җибәрү_тамыр,команда

def эшләтү():
    күчерү_урыны_VALUE_урнаштыру=экранга_җибәрү_тамыр/'build/verification/windows';күчерү_урыны_VALUE_урнаштыру.mkdir(parents=True,exist_ok=True)
    раслау_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest()};LOG_юл=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        мәгълүмат_урнаштыру=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        сайлагыч_a916db4e=selectors.DefaultSelector();сайлагыч_a916db4e.register(мәгълүмат_урнаштыру.stdout,selectors.EVENT_READ)
        def дескриптор_вакыйга(초단위=.1):
            for 누름값,_ in сайлагыч_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_юл.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_юл and b'HALTED' not in LOG_юл,LOG_юл[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            тәмамлау_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_юл[현재위치:]:
                if time.monotonic()>тәмамлау_OFFSET or мәгълүмат_урнаштыру.poll() is not None:raise AssertionError(LOG_юл[현재위치:].decode('utf-8','replace'))
                дескриптор_вакыйга()
            return bytes(LOG_юл[현재위치:])
        def җибәрү(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_юл);мәгълүмат_урнаштыру.stdin.write(SECOND_VALUE);мәгълүмат_урнаштыру.stdin.flush();return 기다리기(확인표시,현재위치)
        def тышча(юл_мәгълүмат):return җибәрү((юл_мәгълүмат+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ярлык_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def чирттерү_төймә(X_координатасы,세로좌표):return bytes([30,1,1,X_координатасы&255,X_координатасы>>8,세로좌표&255,세로좌표>>8,30,1,0,X_координатасы&255,X_координатасы>>8,세로좌표&255,세로좌표>>8])
        def команда_MODE():
            мәгълүмат_урнаштыру.stdin.write(b'\x1b');мәгълүмат_урнаштыру.stdin.flush();тәмамлау_OFFSET=time.monotonic()+.2
            while time.monotonic()<тәмамлау_OFFSET:дескриптор_вакыйга(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            тышча('terminal');дескриптор_вакыйга(.3)
            тышча('mkdir first; cd first; export NAME=one')
            җибәрү('vi 첫째.py\n'.encode(),b'NORMAL')
            җибәрү('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            тәмамлау_OFFSET=time.monotonic()+3
            while time.monotonic()<тәмамлау_OFFSET:дескриптор_вакыйга(.1)
            җибәрү(ярлык_VALUE(1),b'TERMINAL FOCUS 2');дескриптор_вакыйга(.2)
            assert b'/\r\n' in тышча('pwd')
            тышча('export NAME=two')
            җибәрү('vi 둘째.txt\n'.encode(),b'NORMAL')
            җибәрү('i두 번째 тәрәз\n'.encode(),b'INSERT')
            җибәрү(чирттерү_төймә(180,12),b'TERMINAL FOCUS 1');дескриптор_вакыйга(.2)
            команда_MODE();җибәрү(b':wq\r')
            assert b'one:/first' in тышча('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in тышча('cat 첫째.py')
            үлчәм=тышча('python 첫째.py');assert b'42\r\n' in үлчәм,үлчәм
            # Close the first shell with its actual title-bar X; second editor resumes.
            җибәрү(чирттерү_төймә(560,63),b'TERMINAL FOCUS 2');дескриптор_вакыйга(.2)
            команда_MODE();җибәрү(b':wq\r')
            assert b'two:/' in тышча('echo "$NAME:$PWD"')
            assert '두 번째 тәрәз'.encode() in тышча('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            җибәрү('vi 둘째.txt\n'.encode(),b'NORMAL');җибәрү(b'xu',b'NORMAL')
            җибәрү(b'iX',b'INSERT');команда_MODE();җибәрү(b':q\r',b'Unsaved')
            җибәрү(b':q!\r');assert '두 번째 тәрәз'.encode() in тышча('cat 둘째.txt')
            җибәрү(ярлык_VALUE(1),b'TERMINAL FOCUS 1');дескриптор_вакыйга(.2)
            җибәрү(ярлык_VALUE(1),b'TERMINAL FOCUS 3');дескриптор_вакыйга(.2)
            җибәрү(ярлык_VALUE(1),b'TERMINAL FOCUS 4');дескриптор_вакыйга(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            мәгълүмат_урнаштыру.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));мәгълүмат_урнаштыру.stdin.flush()
            тышча('echo DRAGGED_OK')
            җибәрү('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            җибәрү('i저장하지 않은 мәгълүмат'.encode(),b'INSERT')
            җибәрү(чирттерү_төймә(578,97),b'TERMINAL FOCUS 3');дескриптор_вакыйга(.2)
            assert '버릴문서.txt'.encode() not in тышча('ls')
            җибәрү(ярлык_VALUE(1),b'TERMINAL FOCUS 4');дескриптор_вакыйга(.2)
            тышча('echo REUSED_WINDOW_OK')
            완료량=LOG_юл.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            тәмамлау_OFFSET=time.monotonic()+.3
            while time.monotonic()<тәмамлау_OFFSET:дескриптор_вакыйга(.05)
            with socket.socket(socket.AF_UNIX) as символ_коды:
                символ_коды.settimeout(10);символ_коды.connect(str(모의제어접속))
                with символ_коды.makefile('rwb') as файл_кертү:
                    json.loads(файл_кертү.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(күчерү_урыны_VALUE_урнаштыру/'four-terminals.png'),'format':'png'}}):
                        файл_кертү.write((json.dumps(요청값)+'\n').encode());файл_кертү.flush()
                        while True:
                            반환값=json.loads(файл_кертү.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(күчерү_урыны_VALUE_урнаштыру/'four-terminals.png')).convert('RGB')
            for координатлар_пары,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(координатлар_пары)==색상,(координатлар_пары,화소들.getpixel(координатлар_пары))
            тышча('echo FOUR_WINDOWS_OK')
            раслау_отчет.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if мәгълүмат_урнаштыру.poll() is None:мәгълүмат_урнаштыру.terminate()
            try:мәгълүмат_урнаштыру.wait(timeout=5)
            except subprocess.TimeoutExpired:мәгълүмат_урнаштыру.kill();мәгълүмат_урнаштыру.wait()
            сайлагыч_a916db4e.close();мәгълүмат_урнаштыру.stdin.close();мәгълүмат_урнаштыру.stdout.close();(күчерү_урыны_VALUE_урнаштыру/'serial.log').write_bytes(LOG_юл);(күчерү_урыны_VALUE_урнаштыру/'report.json').write_text(json.dumps(раслау_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':эшләтү()
