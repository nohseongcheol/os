#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import задача_корень,команда

def запустить():
    цель_ЗНАЧЕН_позиция=задача_корень/'build/verification/windows';цель_ЗНАЧЕН_позиция.mkdir(parents=True,exist_ok=True)
    проверка_Отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((задача_корень/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ЗАПИСЬ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        данные_позиция=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектор_a916db4e=selectors.DefaultSelector();селектор_a916db4e.register(данные_позиция.stdout,selectors.EVENT_READ)
        def маркер_Событие(초단위=.1):
            for 누름값,_ in селектор_a916db4e.select(초단위):
                СЕКУНДЫ_ЗНАЧЕН=누름값.fileobj.read(65536)
                if СЕКУНДЫ_ЗНАЧЕН:LOG_ЗАПИСЬ.extend(СЕКУНДЫ_ЗНАЧЕН)
            assert b'PANIC:' not in LOG_ЗАПИСЬ and b'HALTED' not in LOG_ЗАПИСЬ,LOG_ЗАПИСЬ[-2048:]
        def 기다리기(метка,текущий_позиция,초단위=50):
            элемент_СМЕЩ=time.monotonic()+초단위
            while метка not in LOG_ЗАПИСЬ[текущий_позиция:]:
                if time.monotonic()>элемент_СМЕЩ or данные_позиция.poll() is not None:raise AssertionError(LOG_ЗАПИСЬ[текущий_позиция:].decode('utf-8','replace'))
                маркер_Событие()
            return bytes(LOG_ЗАПИСЬ[текущий_позиция:])
        def написать(СЕКУНДЫ_ЗНАЧЕН,метка=b'jkoros-native> '):
            текущий_позиция=len(LOG_ЗАПИСЬ);данные_позиция.stdin.write(СЕКУНДЫ_ЗНАЧЕН);данные_позиция.stdin.flush();return 기다리기(метка,текущий_позиция)
        def оболочка(строка_данные):return написать((строка_данные+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ярлык_ЗНАЧЕН(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def клик_кнопка(координата_X,Y_координата):return bytes([30,1,1,координата_X&255,координата_X>>8,Y_координата&255,Y_координата>>8,30,1,0,координата_X&255,координата_X>>8,Y_координата&255,Y_координата>>8])
        def 명령방식():
            данные_позиция.stdin.write(b'\x1b');данные_позиция.stdin.flush();элемент_СМЕЩ=time.monotonic()+.2
            while time.monotonic()<элемент_СМЕЩ:маркер_Событие(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            оболочка('terminal');маркер_Событие(.3)
            оболочка('mkdir first; cd first; export NAME=one')
            написать('vi 첫째.py\n'.encode(),b'NORMAL')
            написать('i값 = 21\nprint(ЗНАЧЕН * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            элемент_СМЕЩ=time.monotonic()+3
            while time.monotonic()<элемент_СМЕЩ:маркер_Событие(.1)
            написать(ярлык_ЗНАЧЕН(1),b'TERMINAL FOCUS 2');маркер_Событие(.2)
            assert b'/\r\n' in оболочка('pwd')
            оболочка('export NAME=two')
            написать('vi 둘째.txt\n'.encode(),b'NORMAL')
            написать('i두 번째 Окно\n'.encode(),b'INSERT')
            написать(клик_кнопка(180,12),b'TERMINAL FOCUS 1');маркер_Событие(.2)
            명령방식();написать(b':wq\r')
            assert b'one:/first' in оболочка('echo "$NAME:$PWD"')
            assert 'ЗНАЧЕН = 21\r\nprint(ЗНАЧЕН * 2)'.encode() in оболочка('cat 첫째.py')
            результат=оболочка('python 첫째.py');assert b'42\r\n' in результат,результат
            # Close the first shell with its actual title-bar X; second editor resumes.
            написать(клик_кнопка(560,63),b'TERMINAL FOCUS 2');маркер_Событие(.2)
            명령방식();написать(b':wq\r')
            assert b'two:/' in оболочка('echo "$NAME:$PWD"')
            assert '두 번째 Окно'.encode() in оболочка('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            написать('vi 둘째.txt\n'.encode(),b'NORMAL');написать(b'xu',b'NORMAL')
            написать(b'iX',b'INSERT');명령방식();написать(b':q\r',b'Unsaved')
            написать(b':q!\r');assert '두 번째 Окно'.encode() in оболочка('cat 둘째.txt')
            написать(ярлык_ЗНАЧЕН(1),b'TERMINAL FOCUS 1');маркер_Событие(.2)
            написать(ярлык_ЗНАЧЕН(1),b'TERMINAL FOCUS 3');маркер_Событие(.2)
            написать(ярлык_ЗНАЧЕН(1),b'TERMINAL FOCUS 4');маркер_Событие(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            данные_позиция.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));данные_позиция.stdin.flush()
            оболочка('echo DRAGGED_OK')
            написать('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            написать('i저장하지 않은 данные'.encode(),b'INSERT')
            написать(клик_кнопка(578,97),b'TERMINAL FOCUS 3');маркер_Событие(.2)
            assert '버릴문서.txt'.encode() not in оболочка('ls')
            написать(ярлык_ЗНАЧЕН(1),b'TERMINAL FOCUS 4');маркер_Событие(.2)
            оболочка('echo REUSED_WINDOW_OK')
            завершено_объем=LOG_ЗАПИСЬ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',завершено_объем)
            # UART completion precedes the next QEMU display refresh.
            элемент_СМЕЩ=time.monotonic()+.3
            while time.monotonic()<элемент_СМЕЩ:маркер_Событие(.05)
            with socket.socket(socket.AF_UNIX) as код_знака:
                код_знака.settimeout(10);код_знака.connect(str(모의제어접속))
                with код_знака.makefile('rwb') as файл_ввод:
                    json.loads(файл_ввод.readline())
                    for запрос_ЗНАЧЕН_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(цель_ЗНАЧЕН_позиция/'four-terminals.png'),'format':'png'}}):
                        файл_ввод.write((json.dumps(запрос_ЗНАЧЕН_625fa62c)+'\n').encode());файл_ввод.flush()
                        while True:
                            반환값=json.loads(файл_ввод.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(цель_ЗНАЧЕН_позиция/'four-terminals.png')).convert('RGB')
            for пара_координат,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(пара_координат)==색상,(пара_координат,화소들.getpixel(пара_координат))
            оболочка('echo FOUR_WINDOWS_OK')
            проверка_Отчет.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if данные_позиция.poll() is None:данные_позиция.terminate()
            try:данные_позиция.wait(timeout=5)
            except subprocess.TimeoutExpired:данные_позиция.kill();данные_позиция.wait()
            селектор_a916db4e.close();данные_позиция.stdin.close();данные_позиция.stdout.close();(цель_ЗНАЧЕН_позиция/'serial.log').write_bytes(LOG_ЗАПИСЬ);(цель_ЗНАЧЕН_позиция/'report.json').write_text(json.dumps(проверка_Отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустить()
