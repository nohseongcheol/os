#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ýerine_ýetir_buýruk import 기준,buýruk

def Bitir():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    barlag_hasabat={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};hasaba_alyş_setir=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(buýruk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        saýlaýjy_a916db4e=selectors.DefaultSelector();saýlaýjy_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def ryçag_waka(초단위=.1):
            for 누름값,_ in saýlaýjy_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:hasaba_alyş_setir.extend(둘째값)
            assert b'PANIC:' not in hasaba_alyş_setir and b'HALTED' not in hasaba_alyş_setir,hasaba_alyş_setir[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            tamamla_Süýşüriş=time.monotonic()+초단위
            while 확인표시 not in hasaba_alyş_setir[현재위치:]:
                if time.monotonic()>tamamla_Süýşüriş or 자료위치.poll() is not None:raise AssertionError(hasaba_alyş_setir[현재위치:].decode('utf-8','replace'))
                ryçag_waka()
            return bytes(hasaba_alyş_setir[현재위치:])
        def iber(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(hasaba_alyş_setir);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def gabyjak(setir_maglumat):return iber((setir_maglumat+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ýarlyk_baha(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def bas_düwme(x_koordinatasy,세로좌표):return bytes([30,1,1,x_koordinatasy&255,x_koordinatasy>>8,세로좌표&255,세로좌표>>8,30,1,0,x_koordinatasy&255,x_koordinatasy>>8,세로좌표&255,세로좌표>>8])
        def buýruk_reje():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();tamamla_Süýşüriş=time.monotonic()+.2
            while time.monotonic()<tamamla_Süýşüriş:ryçag_waka(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            gabyjak('terminal');ryçag_waka(.3)
            gabyjak('mkdir first; cd first; export NAME=one')
            iber('vi 첫째.py\n'.encode(),b'NORMAL')
            iber('i값 = 21\nprint(baha * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            tamamla_Süýşüriş=time.monotonic()+3
            while time.monotonic()<tamamla_Süýşüriş:ryçag_waka(.1)
            iber(ýarlyk_baha(1),b'TERMINAL FOCUS 2');ryçag_waka(.2)
            assert b'/\r\n' in gabyjak('pwd')
            gabyjak('export NAME=two')
            iber('vi 둘째.txt\n'.encode(),b'NORMAL')
            iber('i두 번째 penjire\n'.encode(),b'INSERT')
            iber(bas_düwme(180,12),b'TERMINAL FOCUS 1');ryçag_waka(.2)
            buýruk_reje();iber(b':wq\r')
            assert b'one:/first' in gabyjak('echo "$NAME:$PWD"')
            assert 'baha = 21\r\nprint(baha * 2)'.encode() in gabyjak('cat 첫째.py')
            결과=gabyjak('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            iber(bas_düwme(560,63),b'TERMINAL FOCUS 2');ryçag_waka(.2)
            buýruk_reje();iber(b':wq\r')
            assert b'two:/' in gabyjak('echo "$NAME:$PWD"')
            assert '두 번째 penjire'.encode() in gabyjak('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            iber('vi 둘째.txt\n'.encode(),b'NORMAL');iber(b'xu',b'NORMAL')
            iber(b'iX',b'INSERT');buýruk_reje();iber(b':q\r',b'Unsaved')
            iber(b':q!\r');assert '두 번째 penjire'.encode() in gabyjak('cat 둘째.txt')
            iber(ýarlyk_baha(1),b'TERMINAL FOCUS 1');ryçag_waka(.2)
            iber(ýarlyk_baha(1),b'TERMINAL FOCUS 3');ryçag_waka(.2)
            iber(ýarlyk_baha(1),b'TERMINAL FOCUS 4');ryçag_waka(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            gabyjak('echo DRAGGED_OK')
            iber('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            iber('i저장하지 않은 maglumat'.encode(),b'INSERT')
            iber(bas_düwme(578,97),b'TERMINAL FOCUS 3');ryçag_waka(.2)
            assert '버릴문서.txt'.encode() not in gabyjak('ls')
            iber(ýarlyk_baha(1),b'TERMINAL FOCUS 4');ryçag_waka(.2)
            gabyjak('echo REUSED_WINDOW_OK')
            완료량=hasaba_alyş_setir.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            tamamla_Süýşüriş=time.monotonic()+.3
            while time.monotonic()<tamamla_Süýşüriş:ryçag_waka(.05)
            with socket.socket(socket.AF_UNIX) as nyşanyň_kody:
                nyşanyň_kody.settimeout(10);nyşanyň_kody.connect(str(모의제어접속))
                with nyşanyň_kody.makefile('rwb') as faýl_girizmeklik:
                    json.loads(faýl_girizmeklik.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        faýl_girizmeklik.write((json.dumps(요청값)+'\n').encode());faýl_girizmeklik.flush()
                        while True:
                            반환값=json.loads(faýl_girizmeklik.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for koordinata_jübüti,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinata_jübüti)==색상,(koordinata_jübüti,화소들.getpixel(koordinata_jübüti))
            gabyjak('echo FOUR_WINDOWS_OK')
            barlag_hasabat.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            saýlaýjy_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(hasaba_alyş_setir);(목적위치/'report.json').write_text(json.dumps(barlag_hasabat,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bitir()
