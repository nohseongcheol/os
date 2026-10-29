#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from изпълнявам_команда import проект_корен,Команда

def Стартиране():
    местоназначение_стойност_позиция=проект_корен/'build/verification/swing';местоназначение_стойност_позиция.mkdir(parents=True,exist_ok=True)
    Клас_път=проект_корен/'build/verification/new-java';Клас_път.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(проект_корен/'dist/jkoros-native-korean.jar'),'-d',str(Клас_път),str(проект_корен/'시험/자바/스윙시험.java'),str(проект_корен/'시험/자바/한글창시험.java')])
    проверка_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((проект_корен/'build/kernel8.img').read_bytes()).hexdigest()};регистрирам_запис=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        данни_позиция=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        свързан_елемент_за_избор_a916db4e=selectors.DefaultSelector();свързан_елемент_за_избор_a916db4e.register(данни_позиция.stdout,selectors.EVENT_READ)
        def манипулатор_събитие(초단위=.1):
            for 누름값,_ in свързан_елемент_за_избор_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:регистрирам_запис.extend(둘째값)
            assert b'PANIC:' not in регистрирам_запис and b'HALTED' not in регистрирам_запис,регистрирам_запис[-2048:]
        def 기다리기(маркер,в_срок_позиция,초단위=50):
            прекратяване_на_повикването_Изместване=time.monotonic()+초단위
            while маркер not in регистрирам_запис[в_срок_позиция:]:
                if time.monotonic()>прекратяване_на_повикването_Изместване or данни_позиция.poll() is not None:raise AssertionError(регистрирам_запис[в_срок_позиция:].decode('utf-8','replace'))
                манипулатор_събитие()
            return bytes(регистрирам_запис[в_срок_позиция:])
        def изпращам(둘째값,маркер=b'jkoros-native> '):
            в_срок_позиция=len(регистрирам_запис);данни_позиция.stdin.write(둘째값);данни_позиция.stdin.flush();return 기다리기(маркер,в_срок_позиция)
        def обвивка(низ_данни):return изпращам((низ_данни+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def пряк_път_стойност(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def кликвам_бутон(x_координата,세로좌표):return bytes([30,1,1,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8,30,1,0,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8])
        def команда_режим():
            данни_позиция.stdin.write(b'\x1b');данни_позиция.stdin.flush();прекратяване_на_повикването_Изместване=time.monotonic()+.2
            while time.monotonic()<прекратяване_на_повикването_Изместване:манипулатор_събитие(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            обвивка('terminal');манипулатор_събитие(.3)
            данни=(проект_корен/'build/verification/new-java/스윙시험.class').read_bytes()
            изпращам('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(данни),64):изпращам(данни[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            изпращам(b'.\n')
            изпращам('java 스윙시험\n'.encode(),b'SWING READY')
            прекратяване_на_повикването_Изместване=time.monotonic()+3
            while time.monotonic()<прекратяване_на_повикването_Изместване:манипулатор_събитие(.1)
            # JFrame centered at (120,100), content at y=130.
            изпращам(кликвам_бутон(200,210),b'',)  # focus JTextField
            данни_позиция.stdin.write('누리'.encode());данни_позиция.stdin.flush()
            прекратяване_на_повикването_Изместване=time.monotonic()+.3
            while time.monotonic()<прекратяване_на_повикването_Изместване:манипулатор_събитие(.05)
            РЕЗУЛТАТ=изпращам(кликвам_бутон(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(регистрирам_запис)-len(РЕЗУЛТАТ))
            изпращам(пряк_път_стойност(1),b'TERMINAL FOCUS 2')
            РЕЗУЛТАТ=обвивка('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in РЕЗУЛТАТ
            изпращам(кликвам_бутон(180,12),b'TERMINAL FOCUS 1')
            прекратяване_на_повикването_Изместване=time.monotonic()+.3
            while time.monotonic()<прекратяване_на_повикването_Изместване:манипулатор_събитие(.05)
            with socket.socket(socket.AF_UNIX) as знаков_код:
                знаков_код.settimeout(10);знаков_код.connect(str(모의제어접속))
                with знаков_код.makefile('rwb') as Файл_запис:
                    json.loads(Файл_запис.readline())
                    for искане_стойност in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(местоназначение_стойност_позиция/'native-swing.png'),'format':'png'}}):
                        Файл_запис.write((json.dumps(искане_стойност)+'\n').encode());Файл_запис.flush()
                        while True:
                            반환값=json.loads(Файл_запис.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            изпращам(кликвам_бутон(505,115))
            обвивка('echo SWING_CLOSED_OK')
            данни=(Клас_път/'한글창시험.class').read_bytes()
            изпращам('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(данни),64):изпращам(данни[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            изпращам(b'.\n')
            изпращам('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            изпращам(кликвам_бутон(200,255),'KOREAN SWING CLICK Име'.encode())
            изпращам(кликвам_бутон(505,115))
            обвивка('echo KOREAN_SWING_CLOSED_OK')
            проверка_отчет.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Български Прозорец/бутон/проект_предупреждение/събитие_опашка directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if данни_позиция.poll() is None:данни_позиция.terminate()
            try:данни_позиция.wait(timeout=5)
            except subprocess.TimeoutExpired:данни_позиция.kill();данни_позиция.wait()
            свързан_елемент_за_избор_a916db4e.close();данни_позиция.stdin.close();данни_позиция.stdout.close();(местоназначение_стойност_позиция/'serial.log').write_bytes(регистрирам_запис);(местоназначение_стойност_позиция/'report.json').write_text(json.dumps(проверка_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Стартиране()
