#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Виконати_команда import Дії_корінь,команда

def запустити():
    місце_значення_посада=Дії_корінь/'build/verification/swing';місце_значення_посада.mkdir(parents=True,exist_ok=True)
    Клас_шлях=Дії_корінь/'build/verification/new-java';Клас_шлях.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Дії_корінь/'dist/jkoros-native-korean.jar'),'-d',str(Клас_шлях),str(Дії_корінь/'випробування/자바/스윙시험.java'),str(Дії_корінь/'випробування/자바/한글창시험.java')])
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
            дані=(Дії_корінь/'build/verification/new-java/스윙시험.class').read_bytes()
            надсилати('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(дані),64):надсилати(дані[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            надсилати(b'.\n')
            надсилати('java 스윙시험\n'.encode(),b'SWING READY')
            завершити_виклик_Зміщена_копія=time.monotonic()+3
            while time.monotonic()<завершити_виклик_Зміщена_копія:маркер_подія(.1)
            # JFrame centered at (120,100), content at y=130.
            надсилати(клік_кнопка(200,210),b'',)  # focus JTextField
            дані_посада.stdin.write('누리'.encode());дані_посада.stdin.flush()
            завершити_виклик_Зміщена_копія=time.monotonic()+.3
            while time.monotonic()<завершити_виклик_Зміщена_копія:маркер_подія(.05)
            результат=надсилати(клік_кнопка(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(журнал_запис)-len(результат))
            надсилати(ярлик_значення(1),b'TERMINAL FOCUS 2')
            результат=оболонка('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in результат
            надсилати(клік_кнопка(180,12),b'TERMINAL FOCUS 1')
            завершити_виклик_Зміщена_копія=time.monotonic()+.3
            while time.monotonic()<завершити_виклик_Зміщена_копія:маркер_подія(.05)
            with socket.socket(socket.AF_UNIX) as код_символу:
                код_символу.settimeout(10);код_символу.connect(str(모의제어접속))
                with код_символу.makefile('rwb') as Файл_запис:
                    json.loads(Файл_запис.readline())
                    for запит_значення_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(місце_значення_посада/'native-swing.png'),'format':'png'}}):
                        Файл_запис.write((json.dumps(запит_значення_625fa62c)+'\n').encode());Файл_запис.flush()
                        while True:
                            반환값=json.loads(Файл_запис.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            надсилати(клік_кнопка(505,115))
            оболонка('echo SWING_CLOSED_OK')
            дані=(Клас_шлях/'한글창시험.class').read_bytes()
            надсилати('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(дані),64):надсилати(дані[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            надсилати(b'.\n')
            надсилати('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            надсилати(клік_кнопка(200,255),'KOREAN SWING CLICK Назва'.encode())
            надсилати(клік_кнопка(505,115))
            оболонка('echo KOREAN_SWING_CLOSED_OK')
            перевірка_звіт.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','українська Вікно/кнопка/Дія_повідомлення/подія_черга directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if дані_посада.poll() is None:дані_посада.terminate()
            try:дані_посада.wait(timeout=5)
            except subprocess.TimeoutExpired:дані_посада.kill();дані_посада.wait()
            селектор_a916db4e.close();дані_посада.stdin.close();дані_посада.stdout.close();(місце_значення_посада/'serial.log').write_bytes(журнал_запис);(місце_значення_посада/'report.json').write_text(json.dumps(перевірка_звіт,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':запустити()
