#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from phethagatša_taelo import 기준,Taelo

def Diriša():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    tiišetšo_pego={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};pego_rei=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Taelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        sekgethi_a916db4e=selectors.DefaultSelector();sekgethi_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def tshwaro_tiragalo(초단위=.1):
            for 누름값,_ in sekgethi_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:pego_rei.extend(둘째값)
            assert b'PANIC:' not in pego_rei and b'HALTED' not in pego_rei,pego_rei[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            fetša_E_Šetšego=time.monotonic()+초단위
            while 확인표시 not in pego_rei[현재위치:]:
                if time.monotonic()>fetša_E_Šetšego or 자료위치.poll() is not None:raise AssertionError(pego_rei[현재위치:].decode('utf-8','replace'))
                tshwaro_tiragalo()
            return bytes(pego_rei[현재위치:])
        def Romela(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(pego_rei);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def šele(molokoloko_data):return Romela((molokoloko_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def kgaoletšo_boleng(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klika_konope(kamano_ya_x,세로좌표):return bytes([30,1,1,kamano_ya_x&255,kamano_ya_x>>8,세로좌표&255,세로좌표>>8,30,1,0,kamano_ya_x&255,kamano_ya_x>>8,세로좌표&255,세로좌표>>8])
        def taelo_mokgwa():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();fetša_E_Šetšego=time.monotonic()+.2
            while time.monotonic()<fetša_E_Šetšego:tshwaro_tiragalo(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            šele('terminal');tshwaro_tiragalo(.3)
            šele('mkdir first; cd first; export NAME=one')
            Romela('vi 첫째.py\n'.encode(),b'NORMAL')
            Romela('i값 = 21\nprint(boleng * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            fetša_E_Šetšego=time.monotonic()+3
            while time.monotonic()<fetša_E_Šetšego:tshwaro_tiragalo(.1)
            Romela(kgaoletšo_boleng(1),b'TERMINAL FOCUS 2');tshwaro_tiragalo(.2)
            assert b'/\r\n' in šele('pwd')
            šele('export NAME=two')
            Romela('vi 둘째.txt\n'.encode(),b'NORMAL')
            Romela('i두 번째 lefastere\n'.encode(),b'INSERT')
            Romela(klika_konope(180,12),b'TERMINAL FOCUS 1');tshwaro_tiragalo(.2)
            taelo_mokgwa();Romela(b':wq\r')
            assert b'one:/first' in šele('echo "$NAME:$PWD"')
            assert 'boleng = 21\r\nprint(boleng * 2)'.encode() in šele('cat 첫째.py')
            결과=šele('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            Romela(klika_konope(560,63),b'TERMINAL FOCUS 2');tshwaro_tiragalo(.2)
            taelo_mokgwa();Romela(b':wq\r')
            assert b'two:/' in šele('echo "$NAME:$PWD"')
            assert '두 번째 lefastere'.encode() in šele('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            Romela('vi 둘째.txt\n'.encode(),b'NORMAL');Romela(b'xu',b'NORMAL')
            Romela(b'iX',b'INSERT');taelo_mokgwa();Romela(b':q\r',b'Unsaved')
            Romela(b':q!\r');assert '두 번째 lefastere'.encode() in šele('cat 둘째.txt')
            Romela(kgaoletšo_boleng(1),b'TERMINAL FOCUS 1');tshwaro_tiragalo(.2)
            Romela(kgaoletšo_boleng(1),b'TERMINAL FOCUS 3');tshwaro_tiragalo(.2)
            Romela(kgaoletšo_boleng(1),b'TERMINAL FOCUS 4');tshwaro_tiragalo(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            šele('echo DRAGGED_OK')
            Romela('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            Romela('i저장하지 않은 data'.encode(),b'INSERT')
            Romela(klika_konope(578,97),b'TERMINAL FOCUS 3');tshwaro_tiragalo(.2)
            assert '버릴문서.txt'.encode() not in šele('ls')
            Romela(kgaoletšo_boleng(1),b'TERMINAL FOCUS 4');tshwaro_tiragalo(.2)
            šele('echo REUSED_WINDOW_OK')
            완료량=pego_rei.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            fetša_E_Šetšego=time.monotonic()+.3
            while time.monotonic()<fetša_E_Šetšego:tshwaro_tiragalo(.05)
            with socket.socket(socket.AF_UNIX) as khouto_ya_tlhaka:
                khouto_ya_tlhaka.settimeout(10);khouto_ya_tlhaka.connect(str(모의제어접속))
                with khouto_ya_tlhaka.makefile('rwb') as faele_go_tsenya_tshedimošo:
                    json.loads(faele_go_tsenya_tshedimošo.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        faele_go_tsenya_tshedimošo.write((json.dumps(요청값)+'\n').encode());faele_go_tsenya_tshedimošo.flush()
                        while True:
                            반환값=json.loads(faele_go_tsenya_tshedimošo.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for para_ya_papetšo,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(para_ya_papetšo)==색상,(para_ya_papetšo,화소들.getpixel(para_ya_papetšo))
            šele('echo FOUR_WINDOWS_OK')
            tiišetšo_pego.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            sekgethi_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(pego_rei);(목적위치/'report.json').write_text(json.dumps(tiišetšo_pego,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Diriša()
