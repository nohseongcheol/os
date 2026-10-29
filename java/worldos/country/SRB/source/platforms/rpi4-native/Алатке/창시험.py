#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Изврши_команда import пројектовати_корен,Наредба

def Покрени():
    одредиште_вриједност_позиција=пројектовати_корен/'build/verification/windows';одредиште_вриједност_позиција.mkdir(parents=True,exist_ok=True)
    провјера_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest()};евиденција_ред=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        подаци_позиција=subprocess.Popen(Наредба()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        бирач_a916db4e=selectors.DefaultSelector();бирач_a916db4e.register(подаци_позиција.stdout,selectors.EVENT_READ)
        def хватиште_догађај(초단위=.1):
            for 누름값,_ in бирач_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:евиденција_ред.extend(둘째값)
            assert b'PANIC:' not in евиденција_ред and b'HALTED' not in евиденција_ред,евиденција_ред[-2048:]
        def 기다리기(확인표시,актуелно_позиција,초단위=50):
            завршити_Помак=time.monotonic()+초단위
            while 확인표시 not in евиденција_ред[актуелно_позиција:]:
                if time.monotonic()>завршити_Помак or подаци_позиција.poll() is not None:raise AssertionError(евиденција_ред[актуелно_позиција:].decode('utf-8','replace'))
                хватиште_догађај()
            return bytes(евиденција_ред[актуелно_позиција:])
        def послати(둘째값,확인표시=b'jkoros-native> '):
            актуелно_позиција=len(евиденција_ред);подаци_позиција.stdin.write(둘째값);подаци_позиција.stdin.flush();return 기다리기(확인표시,актуелно_позиција)
        def љуска(ниска_подаци):return послати((ниска_подаци+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def пречица_вриједност(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def клик_дугме(x_координата,дугме_Y_координата):return bytes([30,1,1,x_координата&255,x_координата>>8,дугме_Y_координата&255,дугме_Y_координата>>8,30,1,0,x_координата&255,x_координата>>8,дугме_Y_координата&255,дугме_Y_координата>>8])
        def команда_мод():
            подаци_позиција.stdin.write(b'\x1b');подаци_позиција.stdin.flush();завршити_Помак=time.monotonic()+.2
            while time.monotonic()<завршити_Помак:хватиште_догађај(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            љуска('terminal');хватиште_догађај(.3)
            љуска('mkdir first; cd first; export NAME=one')
            послати('vi 첫째.py\n'.encode(),b'NORMAL')
            послати('i값 = 21\nprint(вриједност * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            завршити_Помак=time.monotonic()+3
            while time.monotonic()<завршити_Помак:хватиште_догађај(.1)
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 2');хватиште_догађај(.2)
            assert b'/\r\n' in љуска('pwd')
            љуска('export NAME=two')
            послати('vi 둘째.txt\n'.encode(),b'NORMAL')
            послати('i두 번째 Прозор\n'.encode(),b'INSERT')
            послати(клик_дугме(180,12),b'TERMINAL FOCUS 1');хватиште_догађај(.2)
            команда_мод();послати(b':wq\r')
            assert b'one:/first' in љуска('echo "$NAME:$PWD"')
            assert 'вриједност = 21\r\nprint(вриједност * 2)'.encode() in љуска('cat 첫째.py')
            ИСХОД=љуска('python 첫째.py');assert b'42\r\n' in ИСХОД,ИСХОД
            # Close the first shell with its actual title-bar X; second editor resumes.
            послати(клик_дугме(560,63),b'TERMINAL FOCUS 2');хватиште_догађај(.2)
            команда_мод();послати(b':wq\r')
            assert b'two:/' in љуска('echo "$NAME:$PWD"')
            assert '두 번째 Прозор'.encode() in љуска('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            послати('vi 둘째.txt\n'.encode(),b'NORMAL');послати(b'xu',b'NORMAL')
            послати(b'iX',b'INSERT');команда_мод();послати(b':q\r',b'Unsaved')
            послати(b':q!\r');assert '두 번째 Прозор'.encode() in љуска('cat 둘째.txt')
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 1');хватиште_догађај(.2)
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 3');хватиште_догађај(.2)
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 4');хватиште_догађај(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            подаци_позиција.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));подаци_позиција.stdin.flush()
            љуска('echo DRAGGED_OK')
            послати('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            послати('i저장하지 않은 подаци'.encode(),b'INSERT')
            послати(клик_дугме(578,97),b'TERMINAL FOCUS 3');хватиште_догађај(.2)
            assert '버릴문서.txt'.encode() not in љуска('ls')
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 4');хватиште_догађај(.2)
            љуска('echo REUSED_WINDOW_OK')
            Довршено_износ=евиденција_ред.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Довршено_износ)
            # UART completion precedes the next QEMU display refresh.
            завршити_Помак=time.monotonic()+.3
            while time.monotonic()<завршити_Помак:хватиште_догађај(.05)
            with socket.socket(socket.AF_UNIX) as кôд_знака:
                кôд_знака.settimeout(10);кôд_знака.connect(str(모의제어접속))
                with кôд_знака.makefile('rwb') as фајл_унос:
                    json.loads(фајл_унос.readline())
                    for захтев_вриједност in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(одредиште_вриједност_позиција/'four-terminals.png'),'format':'png'}}):
                        фајл_унос.write((json.dumps(захтев_вриједност)+'\n').encode());фајл_унос.flush()
                        while True:
                            반환값=json.loads(фајл_унос.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(одредиште_вриједност_позиција/'four-terminals.png')).convert('RGB')
            for координатни_пар,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(координатни_пар)==색상,(координатни_пар,화소들.getpixel(координатни_пар))
            љуска('echo FOUR_WINDOWS_OK')
            провјера_извештај.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if подаци_позиција.poll() is None:подаци_позиција.terminate()
            try:подаци_позиција.wait(timeout=5)
            except subprocess.TimeoutExpired:подаци_позиција.kill();подаци_позиција.wait()
            бирач_a916db4e.close();подаци_позиција.stdin.close();подаци_позиција.stdout.close();(одредиште_вриједност_позиција/'serial.log').write_bytes(евиденција_ред);(одредиште_вриједност_позиција/'report.json').write_text(json.dumps(провјера_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Покрени()
