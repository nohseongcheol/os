#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from орындау_пәрмен import жоба_түбір,Команда

def Орындау_2():
    тағайындау_мән_лауазым=жоба_түбір/'build/verification/windows';тағайындау_мән_лауазым.mkdir(parents=True,exist_ok=True)
    тексерім_есеп={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((жоба_түбір/'build/kernel8.img').read_bytes()).hexdigest()};журнал_жол=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        деректер_лауазым=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектор_a916db4e=selectors.DefaultSelector();селектор_a916db4e.register(деректер_лауазым.stdout,selectors.EVENT_READ)
        def дескриптор_оқиға(초단위=.1):
            for 누름값,_ in селектор_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:журнал_жол.extend(둘째값)
            assert b'PANIC:' not in журнал_жол and b'HALTED' not in журнал_жол,журнал_жол[-2048:]
        def 기다리기(확인표시,ток_лауазым,초단위=50):
            тоқтату_жылжыту=time.monotonic()+초단위
            while 확인표시 not in журнал_жол[ток_лауазым:]:
                if time.monotonic()>тоқтату_жылжыту or деректер_лауазым.poll() is not None:raise AssertionError(журнал_жол[ток_лауазым:].decode('utf-8','replace'))
                дескриптор_оқиға()
            return bytes(журнал_жол[ток_лауазым:])
        def жіберу(둘째값,확인표시=b'jkoros-native> '):
            ток_лауазым=len(журнал_жол);деректер_лауазым.stdin.write(둘째값);деректер_лауазым.stdin.flush();return 기다리기(확인표시,ток_лауазым)
        def қоршам(жол_деректер):return жіберу((жол_деректер+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def таңбаша_мән(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def басу_түйме(x_координатасы,Y_түймешігі_координата):return bytes([30,1,1,x_координатасы&255,x_координатасы>>8,Y_түймешігі_координата&255,Y_түймешігі_координата>>8,30,1,0,x_координатасы&255,x_координатасы>>8,Y_түймешігі_координата&255,Y_түймешігі_координата>>8])
        def пәрмен_режим():
            деректер_лауазым.stdin.write(b'\x1b');деректер_лауазым.stdin.flush();тоқтату_жылжыту=time.monotonic()+.2
            while time.monotonic()<тоқтату_жылжыту:дескриптор_оқиға(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            қоршам('terminal');дескриптор_оқиға(.3)
            қоршам('mkdir first; cd first; export NAME=one')
            жіберу('vi 첫째.py\n'.encode(),b'NORMAL')
            жіберу('i값 = 21\nprint(мән * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            тоқтату_жылжыту=time.monotonic()+3
            while time.monotonic()<тоқтату_жылжыту:дескриптор_оқиға(.1)
            жіберу(таңбаша_мән(1),b'TERMINAL FOCUS 2');дескриптор_оқиға(.2)
            assert b'/\r\n' in қоршам('pwd')
            қоршам('export NAME=two')
            жіберу('vi 둘째.txt\n'.encode(),b'NORMAL')
            жіберу('i두 번째 Терезе\n'.encode(),b'INSERT')
            жіберу(басу_түйме(180,12),b'TERMINAL FOCUS 1');дескриптор_оқиға(.2)
            пәрмен_режим();жіберу(b':wq\r')
            assert b'one:/first' in қоршам('echo "$NAME:$PWD"')
            assert 'мән = 21\r\nprint(мән * 2)'.encode() in қоршам('cat 첫째.py')
            НӘТИЖЕ=қоршам('python 첫째.py');assert b'42\r\n' in НӘТИЖЕ,НӘТИЖЕ
            # Close the first shell with its actual title-bar X; second editor resumes.
            жіберу(басу_түйме(560,63),b'TERMINAL FOCUS 2');дескриптор_оқиға(.2)
            пәрмен_режим();жіберу(b':wq\r')
            assert b'two:/' in қоршам('echo "$NAME:$PWD"')
            assert '두 번째 Терезе'.encode() in қоршам('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            жіберу('vi 둘째.txt\n'.encode(),b'NORMAL');жіберу(b'xu',b'NORMAL')
            жіберу(b'iX',b'INSERT');пәрмен_режим();жіберу(b':q\r',b'Unsaved')
            жіберу(b':q!\r');assert '두 번째 Терезе'.encode() in қоршам('cat 둘째.txt')
            жіберу(таңбаша_мән(1),b'TERMINAL FOCUS 1');дескриптор_оқиға(.2)
            жіберу(таңбаша_мән(1),b'TERMINAL FOCUS 3');дескриптор_оқиға(.2)
            жіберу(таңбаша_мән(1),b'TERMINAL FOCUS 4');дескриптор_оқиға(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            деректер_лауазым.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));деректер_лауазым.stdin.flush()
            қоршам('echo DRAGGED_OK')
            жіберу('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            жіберу('i저장하지 않은 деректер'.encode(),b'INSERT')
            жіберу(басу_түйме(578,97),b'TERMINAL FOCUS 3');дескриптор_оқиға(.2)
            assert '버릴문서.txt'.encode() not in қоршам('ls')
            жіберу(таңбаша_мән(1),b'TERMINAL FOCUS 4');дескриптор_оқиға(.2)
            қоршам('echo REUSED_WINDOW_OK')
            Орындалғандар_көлем=журнал_жол.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Орындалғандар_көлем)
            # UART completion precedes the next QEMU display refresh.
            тоқтату_жылжыту=time.monotonic()+.3
            while time.monotonic()<тоқтату_жылжыту:дескриптор_оқиға(.05)
            with socket.socket(socket.AF_UNIX) as таңба_коды:
                таңба_коды.settimeout(10);таңба_коды.connect(str(모의제어접속))
                with таңба_коды.makefile('rwb') as файл_енгізу:
                    json.loads(файл_енгізу.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(тағайындау_мән_лауазым/'four-terminals.png'),'format':'png'}}):
                        файл_енгізу.write((json.dumps(요청값)+'\n').encode());файл_енгізу.flush()
                        while True:
                            반환값=json.loads(файл_енгізу.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(тағайындау_мән_лауазым/'four-terminals.png')).convert('RGB')
            for координаталар_жұбы,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(координаталар_жұбы)==색상,(координаталар_жұбы,화소들.getpixel(координаталар_жұбы))
            қоршам('echo FOUR_WINDOWS_OK')
            тексерім_есеп.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if деректер_лауазым.poll() is None:деректер_лауазым.terminate()
            try:деректер_лауазым.wait(timeout=5)
            except subprocess.TimeoutExpired:деректер_лауазым.kill();деректер_лауазым.wait()
            селектор_a916db4e.close();деректер_лауазым.stdin.close();деректер_лауазым.stdout.close();(тағайындау_мән_лауазым/'serial.log').write_bytes(журнал_жол);(тағайындау_мән_лауазым/'report.json').write_text(json.dumps(тексерім_есеп,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Орындау_2()
