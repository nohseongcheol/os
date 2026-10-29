#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Виконати_команда import Дії_корінь,команда

def запустити():
    місце_значення_посада=Дії_корінь/'build/verification/windows';місце_значення_посада.mkdir(parents=True,exist_ok=True)
    перевірка_звіт={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Дії_корінь/'build/kernel8.img').read_bytes()).hexdigest()};журнал_запис=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        дані_посада=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектор_a916db4e=selectors.DefaultSelector();селектор_a916db4e.register(дані_посада.stdout,selectors.EVENT_READ)
        def маркер_подія(초단위=.1):
            for 누름값,_ in селектор_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:журнал_запис.extend(둘째값)
            assert b'PANIC:' not in журнал_запис and b'HALTED' not in журнал_запис,журнал_запис[-2048:]
        def 기다리기(маркер,чинний_посада,초단위=50):
            завершити_виклик_Зміщена_копія=time.monotonic()+초단위
            while маркер not in журнал_запис[чинний_посада:]:
                if time.monotonic()>завершити_виклик_Зміщена_копія or дані_посада.poll() is not None:raise AssertionError(журнал_запис[чинний_посада:].decode('utf-8','replace'))
                маркер_подія()
            return bytes(журнал_запис[чинний_посада:])
        def надсилати(둘째값,маркер=b'jkoros-native> '):
            чинний_посада=len(журнал_запис);дані_посада.stdin.write(둘째값);дані_посада.stdin.flush();return 기다리기(маркер,чинний_посада)
        def оболонка(рядок_дані):return надсилати((рядок_дані+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ярлик_значення(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def клік_кнопка(координата_X,세로좌표):return bytes([30,1,1,координата_X&255,координата_X>>8,세로좌표&255,세로좌표>>8,30,1,0,координата_X&255,координата_X>>8,세로좌표&255,세로좌표>>8])
        def команда_режим():
            дані_посада.stdin.write(b'\x1b');дані_посада.stdin.flush();завершити_виклик_Зміщена_копія=time.monotonic()+.2
            while time.monotonic()<завершити_виклик_Зміщена_копія:маркер_подія(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            оболонка('terminal');маркер_подія(.3)
            оболонка('mkdir first; cd first; export NAME=one')
            надсилати('vi 첫째.py\n'.encode(),b'NORMAL')
            надсилати('i값 = 21\nprint(значення * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            завершити_виклик_Зміщена_копія=time.monotonic()+3
            while time.monotonic()<завершити_виклик_Зміщена_копія:маркер_подія(.1)
            надсилати(ярлик_значення(1),b'TERMINAL FOCUS 2');маркер_подія(.2)
            assert b'/\r\n' in оболонка('pwd')
            оболонка('export NAME=two')
            надсилати('vi 둘째.txt\n'.encode(),b'NORMAL')
            надсилати('i두 번째 Вікно\n'.encode(),b'INSERT')
            надсилати(клік_кнопка(180,12),b'TERMINAL FOCUS 1');маркер_подія(.2)
            команда_режим();надсилати(b':wq\r')
            assert b'one:/first' in оболонка('echo "$NAME:$PWD"')
            assert 'значення = 21\r\nprint(значення * 2)'.encode() in оболонка('cat 첫째.py')
            результат=оболонка('python 첫째.py');assert b'42\r\n' in результат,результат
            # Close the first shell with its actual title-bar X; second editor resumes.
            надсилати(клік_кнопка(560,63),b'TERMINAL FOCUS 2');маркер_подія(.2)
            команда_режим();надсилати(b':wq\r')
            assert b'two:/' in оболонка('echo "$NAME:$PWD"')
            assert '두 번째 Вікно'.encode() in оболонка('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            надсилати('vi 둘째.txt\n'.encode(),b'NORMAL');надсилати(b'xu',b'NORMAL')
            надсилати(b'iX',b'INSERT');команда_режим();надсилати(b':q\r',b'Unsaved')
            надсилати(b':q!\r');assert '두 번째 Вікно'.encode() in оболонка('cat 둘째.txt')
            надсилати(ярлик_значення(1),b'TERMINAL FOCUS 1');маркер_подія(.2)
            надсилати(ярлик_значення(1),b'TERMINAL FOCUS 3');маркер_подія(.2)
            надсилати(ярлик_значення(1),b'TERMINAL FOCUS 4');маркер_подія(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            дані_посада.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));дані_посада.stdin.flush()
            оболонка('echo DRAGGED_OK')
            надсилати('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            надсилати('i저장하지 않은 дані'.encode(),b'INSERT')
            надсилати(клік_кнопка(578,97),b'TERMINAL FOCUS 3');маркер_подія(.2)
            assert '버릴문서.txt'.encode() not in оболонка('ls')
            надсилати(ярлик_значення(1),b'TERMINAL FOCUS 4');маркер_подія(.2)
            оболонка('echo REUSED_WINDOW_OK')
            Виконано_сума=журнал_запис.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Виконано_сума)
            # UART completion precedes the next QEMU display refresh.
            завершити_виклик_Зміщена_копія=time.monotonic()+.3
            while time.monotonic()<завершити_виклик_Зміщена_копія:маркер_подія(.05)
            with socket.socket(socket.AF_UNIX) as код_символу:
                код_символу.settimeout(10);код_символу.connect(str(모의제어접속))
                with код_символу.makefile('rwb') as Файл_запис:
                    json.loads(Файл_запис.readline())
                    for запит_значення_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(місце_значення_посада/'four-terminals.png'),'format':'png'}}):
                        Файл_запис.write((json.dumps(запит_значення_625fa62c)+'\n').encode());Файл_запис.flush()
                        while True:
                            반환값=json.loads(Файл_запис.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(місце_значення_посада/'four-terminals.png')).convert('RGB')
            for пара_координат,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(пара_координат)==색상,(пара_координат,화소들.getpixel(пара_координат))
            оболонка('echo FOUR_WINDOWS_OK')
            перевірка_звіт.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if дані_посада.poll() is None:дані_посада.terminate()
            try:дані_посада.wait(timeout=5)
            except subprocess.TimeoutExpired:дані_посада.kill();дані_посада.wait()
            селектор_a916db4e.close();дані_посада.stdin.close();дані_посада.stdout.close();(місце_значення_посада/'serial.log').write_bytes(журнал_запис);(місце_значення_посада/'report.json').write_text(json.dumps(перевірка_звіт,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустити()
