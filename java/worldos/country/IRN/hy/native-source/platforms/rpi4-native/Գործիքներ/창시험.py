#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from կատարել_հրաման import արձակել_արմատ,Հրահանգ

def Գործարկել():
    նպատակակետ_արժեք_դիրք=արձակել_արմատ/'build/verification/windows';նպատակակետ_արժեք_դիրք.mkdir(parents=True,exist_ok=True)
    վավերացում_զեկույց={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((արձակել_արմատ/'build/kernel8.img').read_bytes()).hexdigest()};մատյան_տող=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        տվյալ_դիրք=subprocess.Popen(Հրահանգ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ընտրիչ_a916db4e=selectors.DefaultSelector();ընտրիչ_a916db4e.register(տվյալ_դիրք.stdout,selectors.EVENT_READ)
        def բռնակ_միջոցառում(초단위=.1):
            for 누름값,_ in ընտրիչ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:մատյան_տող.extend(둘째값)
            assert b'PANIC:' not in մատյան_տող and b'HALTED' not in մատյան_տող,մատյան_տող[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            վերջացնել_Տեղաշարժում=time.monotonic()+초단위
            while 확인표시 not in մատյան_տող[현재위치:]:
                if time.monotonic()>վերջացնել_Տեղաշարժում or տվյալ_դիրք.poll() is not None:raise AssertionError(մատյան_տող[현재위치:].decode('utf-8','replace'))
                բռնակ_միջոցառում()
            return bytes(մատյան_տող[현재위치:])
        def ուղարկել(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(մատյան_տող);տվյալ_դիրք.stdin.write(둘째값);տվյալ_դիրք.stdin.flush();return 기다리기(확인표시,현재위치)
        def խեցի(տող_տվյալ):return ուղարկել((տող_տվյալ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def դյուրանցում_արժեք(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def կտտացնել_կոճակ(x_կոորդինատ,세로좌표):return bytes([30,1,1,x_կոորդինատ&255,x_կոորդինատ>>8,세로좌표&255,세로좌표>>8,30,1,0,x_կոորդինատ&255,x_կոորդինատ>>8,세로좌표&255,세로좌표>>8])
        def հրաման_կերպ():
            տվյալ_դիրք.stdin.write(b'\x1b');տվյալ_դիրք.stdin.flush();վերջացնել_Տեղաշարժում=time.monotonic()+.2
            while time.monotonic()<վերջացնել_Տեղաշարժում:բռնակ_միջոցառում(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            խեցի('terminal');բռնակ_միջոցառում(.3)
            խեցի('mkdir first; cd first; export NAME=one')
            ուղարկել('vi 첫째.py\n'.encode(),b'NORMAL')
            ուղարկել('i값 = 21\nprint(արժեք * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            վերջացնել_Տեղաշարժում=time.monotonic()+3
            while time.monotonic()<վերջացնել_Տեղաշարժում:բռնակ_միջոցառում(.1)
            ուղարկել(դյուրանցում_արժեք(1),b'TERMINAL FOCUS 2');բռնակ_միջոցառում(.2)
            assert b'/\r\n' in խեցի('pwd')
            խեցի('export NAME=two')
            ուղարկել('vi 둘째.txt\n'.encode(),b'NORMAL')
            ուղարկել('i두 번째 պատուհան\n'.encode(),b'INSERT')
            ուղարկել(կտտացնել_կոճակ(180,12),b'TERMINAL FOCUS 1');բռնակ_միջոցառում(.2)
            հրաման_կերպ();ուղարկել(b':wq\r')
            assert b'one:/first' in խեցի('echo "$NAME:$PWD"')
            assert 'արժեք = 21\r\nprint(արժեք * 2)'.encode() in խեցի('cat 첫째.py')
            չափ=խեցի('python 첫째.py');assert b'42\r\n' in չափ,չափ
            # Close the first shell with its actual title-bar X; second editor resumes.
            ուղարկել(կտտացնել_կոճակ(560,63),b'TERMINAL FOCUS 2');բռնակ_միջոցառում(.2)
            հրաման_կերպ();ուղարկել(b':wq\r')
            assert b'two:/' in խեցի('echo "$NAME:$PWD"')
            assert '두 번째 պատուհան'.encode() in խեցի('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ուղարկել('vi 둘째.txt\n'.encode(),b'NORMAL');ուղարկել(b'xu',b'NORMAL')
            ուղարկել(b'iX',b'INSERT');հրաման_կերպ();ուղարկել(b':q\r',b'Unsaved')
            ուղարկել(b':q!\r');assert '두 번째 պատուհան'.encode() in խեցի('cat 둘째.txt')
            ուղարկել(դյուրանցում_արժեք(1),b'TERMINAL FOCUS 1');բռնակ_միջոցառում(.2)
            ուղարկել(դյուրանցում_արժեք(1),b'TERMINAL FOCUS 3');բռնակ_միջոցառում(.2)
            ուղարկել(դյուրանցում_արժեք(1),b'TERMINAL FOCUS 4');բռնակ_միջոցառում(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            տվյալ_դիրք.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));տվյալ_դիրք.stdin.flush()
            խեցի('echo DRAGGED_OK')
            ուղարկել('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ուղարկել('i저장하지 않은 տվյալ'.encode(),b'INSERT')
            ուղարկել(կտտացնել_կոճակ(578,97),b'TERMINAL FOCUS 3');բռնակ_միջոցառում(.2)
            assert '버릴문서.txt'.encode() not in խեցի('ls')
            ուղարկել(դյուրանցում_արժեք(1),b'TERMINAL FOCUS 4');բռնակ_միջոցառում(.2)
            խեցի('echo REUSED_WINDOW_OK')
            완료량=մատյան_տող.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            վերջացնել_Տեղաշարժում=time.monotonic()+.3
            while time.monotonic()<վերջացնել_Տեղաշարժում:բռնակ_միջոցառում(.05)
            with socket.socket(socket.AF_UNIX) as գրանշանի_կոդ:
                գրանշանի_կոդ.settimeout(10);գրանշանի_կոդ.connect(str(모의제어접속))
                with գրանշանի_կոդ.makefile('rwb') as նիշք_մուտքագրում:
                    json.loads(նիշք_մուտքագրում.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(նպատակակետ_արժեք_դիրք/'four-terminals.png'),'format':'png'}}):
                        նիշք_մուտքագրում.write((json.dumps(요청값)+'\n').encode());նիշք_մուտքագրում.flush()
                        while True:
                            반환값=json.loads(նիշք_մուտքագրում.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(նպատակակետ_արժեք_դիրք/'four-terminals.png')).convert('RGB')
            for դիրքացույցների_զույգ,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(դիրքացույցների_զույգ)==색상,(դիրքացույցների_զույգ,화소들.getpixel(դիրքացույցների_զույգ))
            խեցի('echo FOUR_WINDOWS_OK')
            վավերացում_զեկույց.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if տվյալ_դիրք.poll() is None:տվյալ_դիրք.terminate()
            try:տվյալ_դիրք.wait(timeout=5)
            except subprocess.TimeoutExpired:տվյալ_դիրք.kill();տվյալ_դիրք.wait()
            ընտրիչ_a916db4e.close();տվյալ_դիրք.stdin.close();տվյալ_դիրք.stdout.close();(նպատակակետ_արժեք_դիրք/'serial.log').write_bytes(մատյան_տող);(նպատակակետ_արժեք_դիրք/'report.json').write_text(json.dumps(վավերացում_զեկույց,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Գործարկել()
