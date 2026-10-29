#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from аткаруу_буйрук import 기준,Команда

def Жүргүзүү():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    ырастоо_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};жазуу_катар=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектор_a916db4e=selectors.DefaultSelector();селектор_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def тутка_окуя(초단위=.1):
            for 누름값,_ in селектор_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:жазуу_катар.extend(둘째값)
            assert b'PANIC:' not in жазуу_катар and b'HALTED' not in жазуу_катар,жазуу_катар[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            аяктоо_Жылбышуу=time.monotonic()+초단위
            while 확인표시 not in жазуу_катар[현재위치:]:
                if time.monotonic()>аяктоо_Жылбышуу or 자료위치.poll() is not None:raise AssertionError(жазуу_катар[현재위치:].decode('utf-8','replace'))
                тутка_окуя()
            return bytes(жазуу_катар[현재위치:])
        def жөнөтүү(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(жазуу_катар);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def сырты(сап_берилмелер):return жөнөтүү((сап_берилмелер+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def тез_чакыргыч_маани(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def баскылоо_баскыч(x_координата,세로좌표):return bytes([30,1,1,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8,30,1,0,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8])
        def буйрук_режим():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();аяктоо_Жылбышуу=time.monotonic()+.2
            while time.monotonic()<аяктоо_Жылбышуу:тутка_окуя(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            сырты('terminal');тутка_окуя(.3)
            сырты('mkdir first; cd first; export NAME=one')
            жөнөтүү('vi 첫째.py\n'.encode(),b'NORMAL')
            жөнөтүү('i값 = 21\nprint(маани * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            аяктоо_Жылбышуу=time.monotonic()+3
            while time.monotonic()<аяктоо_Жылбышуу:тутка_окуя(.1)
            жөнөтүү(тез_чакыргыч_маани(1),b'TERMINAL FOCUS 2');тутка_окуя(.2)
            assert b'/\r\n' in сырты('pwd')
            сырты('export NAME=two')
            жөнөтүү('vi 둘째.txt\n'.encode(),b'NORMAL')
            жөнөтүү('i두 번째 терезе\n'.encode(),b'INSERT')
            жөнөтүү(баскылоо_баскыч(180,12),b'TERMINAL FOCUS 1');тутка_окуя(.2)
            буйрук_режим();жөнөтүү(b':wq\r')
            assert b'one:/first' in сырты('echo "$NAME:$PWD"')
            assert 'маани = 21\r\nprint(маани * 2)'.encode() in сырты('cat 첫째.py')
            결과=сырты('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            жөнөтүү(баскылоо_баскыч(560,63),b'TERMINAL FOCUS 2');тутка_окуя(.2)
            буйрук_режим();жөнөтүү(b':wq\r')
            assert b'two:/' in сырты('echo "$NAME:$PWD"')
            assert '두 번째 терезе'.encode() in сырты('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            жөнөтүү('vi 둘째.txt\n'.encode(),b'NORMAL');жөнөтүү(b'xu',b'NORMAL')
            жөнөтүү(b'iX',b'INSERT');буйрук_режим();жөнөтүү(b':q\r',b'Unsaved')
            жөнөтүү(b':q!\r');assert '두 번째 терезе'.encode() in сырты('cat 둘째.txt')
            жөнөтүү(тез_чакыргыч_маани(1),b'TERMINAL FOCUS 1');тутка_окуя(.2)
            жөнөтүү(тез_чакыргыч_маани(1),b'TERMINAL FOCUS 3');тутка_окуя(.2)
            жөнөтүү(тез_чакыргыч_маани(1),b'TERMINAL FOCUS 4');тутка_окуя(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            сырты('echo DRAGGED_OK')
            жөнөтүү('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            жөнөтүү('i저장하지 않은 берилмелер'.encode(),b'INSERT')
            жөнөтүү(баскылоо_баскыч(578,97),b'TERMINAL FOCUS 3');тутка_окуя(.2)
            assert '버릴문서.txt'.encode() not in сырты('ls')
            жөнөтүү(тез_чакыргыч_маани(1),b'TERMINAL FOCUS 4');тутка_окуя(.2)
            сырты('echo REUSED_WINDOW_OK')
            완료량=жазуу_катар.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            аяктоо_Жылбышуу=time.monotonic()+.3
            while time.monotonic()<аяктоо_Жылбышуу:тутка_окуя(.05)
            with socket.socket(socket.AF_UNIX) as символ_коду:
                символ_коду.settimeout(10);символ_коду.connect(str(모의제어접속))
                with символ_коду.makefile('rwb') as файл_киргизме_жазуу:
                    json.loads(файл_киргизме_жазуу.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        файл_киргизме_жазуу.write((json.dumps(요청값)+'\n').encode());файл_киргизме_жазуу.flush()
                        while True:
                            반환값=json.loads(файл_киргизме_жазуу.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for координаттар_жубу,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(координаттар_жубу)==색상,(координаттар_жубу,화소들.getpixel(координаттар_жубу))
            сырты('echo FOUR_WINDOWS_OK')
            ырастоо_отчет.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            селектор_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(жазуу_катар);(목적위치/'report.json').write_text(json.dumps(ырастоо_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Жүргүзүү()
