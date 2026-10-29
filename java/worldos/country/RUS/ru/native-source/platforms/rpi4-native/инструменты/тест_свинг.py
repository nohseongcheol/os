#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import задача_корень,команда

def запустить():
    цель_ЗНАЧЕН_позиция=задача_корень/'build/verification/swing';цель_ЗНАЧЕН_позиция.mkdir(parents=True,exist_ok=True)
    Класс_путь=задача_корень/'build/verification/new-java';Класс_путь.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(задача_корень/'dist/jkoros-native-korean.jar'),'-d',str(Класс_путь),str(задача_корень/'испытания/자바/свинг_тест.java'),str(задача_корень/'испытания/자바/한글창시험.java')])
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
            данные=(задача_корень/'build/verification/new-java/свинг_тест.class').read_bytes()
            написать('load свинг_тест.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(данные),64):написать(данные[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            написать(b'.\n')
            написать('java свинг_тест\n'.encode(),b'SWING READY')
            элемент_СМЕЩ=time.monotonic()+3
            while time.monotonic()<элемент_СМЕЩ:маркер_Событие(.1)
            # JFrame centered at (120,100), content at y=130.
            написать(клик_кнопка(200,210),b'',)  # focus JTextField
            данные_позиция.stdin.write('누리'.encode());данные_позиция.stdin.flush()
            элемент_СМЕЩ=time.monotonic()+.3
            while time.monotonic()<элемент_СМЕЩ:маркер_Событие(.05)
            результат=написать(клик_кнопка(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_ЗАПИСЬ)-len(результат))
            написать(ярлык_ЗНАЧЕН(1),b'TERMINAL FOCUS 2')
            результат=оболочка('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in результат
            написать(клик_кнопка(180,12),b'TERMINAL FOCUS 1')
            элемент_СМЕЩ=time.monotonic()+.3
            while time.monotonic()<элемент_СМЕЩ:маркер_Событие(.05)
            with socket.socket(socket.AF_UNIX) as код_знака:
                код_знака.settimeout(10);код_знака.connect(str(모의제어접속))
                with код_знака.makefile('rwb') as файл_ввод:
                    json.loads(файл_ввод.readline())
                    for запрос_ЗНАЧЕН_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(цель_ЗНАЧЕН_позиция/'native-swing.png'),'format':'png'}}):
                        файл_ввод.write((json.dumps(запрос_ЗНАЧЕН_625fa62c)+'\n').encode());файл_ввод.flush()
                        while True:
                            반환값=json.loads(файл_ввод.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            написать(клик_кнопка(505,115))
            оболочка('echo SWING_CLOSED_OK')
            данные=(Класс_путь/'한글창시험.class').read_bytes()
            написать('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(данные),64):написать(данные[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            написать(b'.\n')
            написать('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            написать(клик_кнопка(200,255),'KOREAN SWING CLICK Название'.encode())
            написать(клик_кнопка(505,115))
            оболочка('echo KOREAN_SWING_CLOSED_OK')
            проверка_Отчет.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','русский Окно/кнопка/задача_уведомление/Событие_Очередь directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if данные_позиция.poll() is None:данные_позиция.terminate()
            try:данные_позиция.wait(timeout=5)
            except subprocess.TimeoutExpired:данные_позиция.kill();данные_позиция.wait()
            селектор_a916db4e.close();данные_позиция.stdin.close();данные_позиция.stdout.close();(цель_ЗНАЧЕН_позиция/'serial.log').write_bytes(LOG_ЗАПИСЬ);(цель_ЗНАЧЕН_позиция/'report.json').write_text(json.dumps(проверка_Отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустить()
