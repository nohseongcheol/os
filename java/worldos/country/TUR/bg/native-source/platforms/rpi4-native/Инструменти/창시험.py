#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from изпълнявам_команда import проект_корен,Команда

def Стартиране():
    местоназначение_стойност_позиция=проект_корен/'build/verification/windows';местоназначение_стойност_позиция.mkdir(parents=True,exist_ok=True)
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
            обвивка('mkdir first; cd first; export NAME=one')
            изпращам('vi 첫째.py\n'.encode(),b'NORMAL')
            изпращам('i값 = 21\nprint(стойност * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            прекратяване_на_повикването_Изместване=time.monotonic()+3
            while time.monotonic()<прекратяване_на_повикването_Изместване:манипулатор_събитие(.1)
            изпращам(пряк_път_стойност(1),b'TERMINAL FOCUS 2');манипулатор_събитие(.2)
            assert b'/\r\n' in обвивка('pwd')
            обвивка('export NAME=two')
            изпращам('vi 둘째.txt\n'.encode(),b'NORMAL')
            изпращам('i두 번째 Прозорец\n'.encode(),b'INSERT')
            изпращам(кликвам_бутон(180,12),b'TERMINAL FOCUS 1');манипулатор_събитие(.2)
            команда_режим();изпращам(b':wq\r')
            assert b'one:/first' in обвивка('echo "$NAME:$PWD"')
            assert 'стойност = 21\r\nprint(стойност * 2)'.encode() in обвивка('cat 첫째.py')
            РЕЗУЛТАТ=обвивка('python 첫째.py');assert b'42\r\n' in РЕЗУЛТАТ,РЕЗУЛТАТ
            # Close the first shell with its actual title-bar X; second editor resumes.
            изпращам(кликвам_бутон(560,63),b'TERMINAL FOCUS 2');манипулатор_събитие(.2)
            команда_режим();изпращам(b':wq\r')
            assert b'two:/' in обвивка('echo "$NAME:$PWD"')
            assert '두 번째 Прозорец'.encode() in обвивка('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            изпращам('vi 둘째.txt\n'.encode(),b'NORMAL');изпращам(b'xu',b'NORMAL')
            изпращам(b'iX',b'INSERT');команда_режим();изпращам(b':q\r',b'Unsaved')
            изпращам(b':q!\r');assert '두 번째 Прозорец'.encode() in обвивка('cat 둘째.txt')
            изпращам(пряк_път_стойност(1),b'TERMINAL FOCUS 1');манипулатор_събитие(.2)
            изпращам(пряк_път_стойност(1),b'TERMINAL FOCUS 3');манипулатор_събитие(.2)
            изпращам(пряк_път_стойност(1),b'TERMINAL FOCUS 4');манипулатор_събитие(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            данни_позиция.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));данни_позиция.stdin.flush()
            обвивка('echo DRAGGED_OK')
            изпращам('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            изпращам('i저장하지 않은 данни'.encode(),b'INSERT')
            изпращам(кликвам_бутон(578,97),b'TERMINAL FOCUS 3');манипулатор_събитие(.2)
            assert '버릴문서.txt'.encode() not in обвивка('ls')
            изпращам(пряк_път_стойност(1),b'TERMINAL FOCUS 4');манипулатор_събитие(.2)
            обвивка('echo REUSED_WINDOW_OK')
            Завършени_количество=регистрирам_запис.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Завършени_количество)
            # UART completion precedes the next QEMU display refresh.
            прекратяване_на_повикването_Изместване=time.monotonic()+.3
            while time.monotonic()<прекратяване_на_повикването_Изместване:манипулатор_събитие(.05)
            with socket.socket(socket.AF_UNIX) as знаков_код:
                знаков_код.settimeout(10);знаков_код.connect(str(모의제어접속))
                with знаков_код.makefile('rwb') as Файл_запис:
                    json.loads(Файл_запис.readline())
                    for искане_стойност in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(местоназначение_стойност_позиция/'four-terminals.png'),'format':'png'}}):
                        Файл_запис.write((json.dumps(искане_стойност)+'\n').encode());Файл_запис.flush()
                        while True:
                            반환값=json.loads(Файл_запис.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(местоназначение_стойност_позиция/'four-terminals.png')).convert('RGB')
            for координатна_двойка,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(координатна_двойка)==색상,(координатна_двойка,화소들.getpixel(координатна_двойка))
            обвивка('echo FOUR_WINDOWS_OK')
            проверка_отчет.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if данни_позиция.poll() is None:данни_позиция.terminate()
            try:данни_позиция.wait(timeout=5)
            except subprocess.TimeoutExpired:данни_позиция.kill();данни_позиция.wait()
            свързан_елемент_за_избор_a916db4e.close();данни_позиция.stdin.close();данни_позиция.stdout.close();(местоназначение_стойност_позиция/'serial.log').write_bytes(регистрирам_запис);(местоназначение_стойност_позиция/'report.json').write_text(json.dumps(проверка_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Стартиране()
