#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from diragatsa_Taelo import 기준,Taelo

def dirisa():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    netefatso_pego={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};rekota_mola=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Taelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        setlhophi_a916db4e=selectors.DefaultSelector();setlhophi_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def mokgwakamogelo_tiragalo(초단위=.1):
            for 누름값,_ in setlhophi_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:rekota_mola.extend(둘째값)
            assert b'PANIC:' not in rekota_mola and b'HALTED' not in rekota_mola,rekota_mola[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            kgaola_Baya_ka_Tekatekanyo=time.monotonic()+초단위
            while 확인표시 not in rekota_mola[현재위치:]:
                if time.monotonic()>kgaola_Baya_ka_Tekatekanyo or 자료위치.poll() is not None:raise AssertionError(rekota_mola[현재위치:].decode('utf-8','replace'))
                mokgwakamogelo_tiragalo()
            return bytes(rekota_mola[현재위치:])
        def romela(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(rekota_mola);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def setlhalosataelo(dikwalwa_tshedimosetso):return romela((dikwalwa_tshedimosetso+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def tlhabanyetso_Boleng(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def tobetsa_konopo(kgokagano_ya_x,세로좌표):return bytes([30,1,1,kgokagano_ya_x&255,kgokagano_ya_x>>8,세로좌표&255,세로좌표>>8,30,1,0,kgokagano_ya_x&255,kgokagano_ya_x>>8,세로좌표&255,세로좌표>>8])
        def Taelo_mokgwa():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();kgaola_Baya_ka_Tekatekanyo=time.monotonic()+.2
            while time.monotonic()<kgaola_Baya_ka_Tekatekanyo:mokgwakamogelo_tiragalo(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            setlhalosataelo('terminal');mokgwakamogelo_tiragalo(.3)
            setlhalosataelo('mkdir first; cd first; export NAME=one')
            romela('vi 첫째.py\n'.encode(),b'NORMAL')
            romela('i값 = 21\nprint(Boleng * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            kgaola_Baya_ka_Tekatekanyo=time.monotonic()+3
            while time.monotonic()<kgaola_Baya_ka_Tekatekanyo:mokgwakamogelo_tiragalo(.1)
            romela(tlhabanyetso_Boleng(1),b'TERMINAL FOCUS 2');mokgwakamogelo_tiragalo(.2)
            assert b'/\r\n' in setlhalosataelo('pwd')
            setlhalosataelo('export NAME=two')
            romela('vi 둘째.txt\n'.encode(),b'NORMAL')
            romela('i두 번째 fensetere\n'.encode(),b'INSERT')
            romela(tobetsa_konopo(180,12),b'TERMINAL FOCUS 1');mokgwakamogelo_tiragalo(.2)
            Taelo_mokgwa();romela(b':wq\r')
            assert b'one:/first' in setlhalosataelo('echo "$NAME:$PWD"')
            assert 'Boleng = 21\r\nprint(Boleng * 2)'.encode() in setlhalosataelo('cat 첫째.py')
            결과=setlhalosataelo('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            romela(tobetsa_konopo(560,63),b'TERMINAL FOCUS 2');mokgwakamogelo_tiragalo(.2)
            Taelo_mokgwa();romela(b':wq\r')
            assert b'two:/' in setlhalosataelo('echo "$NAME:$PWD"')
            assert '두 번째 fensetere'.encode() in setlhalosataelo('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            romela('vi 둘째.txt\n'.encode(),b'NORMAL');romela(b'xu',b'NORMAL')
            romela(b'iX',b'INSERT');Taelo_mokgwa();romela(b':q\r',b'Unsaved')
            romela(b':q!\r');assert '두 번째 fensetere'.encode() in setlhalosataelo('cat 둘째.txt')
            romela(tlhabanyetso_Boleng(1),b'TERMINAL FOCUS 1');mokgwakamogelo_tiragalo(.2)
            romela(tlhabanyetso_Boleng(1),b'TERMINAL FOCUS 3');mokgwakamogelo_tiragalo(.2)
            romela(tlhabanyetso_Boleng(1),b'TERMINAL FOCUS 4');mokgwakamogelo_tiragalo(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            setlhalosataelo('echo DRAGGED_OK')
            romela('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            romela('i저장하지 않은 tshedimosetso'.encode(),b'INSERT')
            romela(tobetsa_konopo(578,97),b'TERMINAL FOCUS 3');mokgwakamogelo_tiragalo(.2)
            assert '버릴문서.txt'.encode() not in setlhalosataelo('ls')
            romela(tlhabanyetso_Boleng(1),b'TERMINAL FOCUS 4');mokgwakamogelo_tiragalo(.2)
            setlhalosataelo('echo REUSED_WINDOW_OK')
            완료량=rekota_mola.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            kgaola_Baya_ka_Tekatekanyo=time.monotonic()+.3
            while time.monotonic()<kgaola_Baya_ka_Tekatekanyo:mokgwakamogelo_tiragalo(.05)
            with socket.socket(socket.AF_UNIX) as khoutuletshwao:
                khoutuletshwao.settimeout(10);khoutuletshwao.connect(str(모의제어접속))
                with khoutuletshwao.makefile('rwb') as faele_tsenyo:
                    json.loads(faele_tsenyo.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        faele_tsenyo.write((json.dumps(요청값)+'\n').encode());faele_tsenyo.flush()
                        while True:
                            반환값=json.loads(faele_tsenyo.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for sebedi_sa_dintlhakopanyi,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(sebedi_sa_dintlhakopanyi)==색상,(sebedi_sa_dintlhakopanyi,화소들.getpixel(sebedi_sa_dintlhakopanyi))
            setlhalosataelo('echo FOUR_WINDOWS_OK')
            netefatso_pego.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            setlhophi_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(rekota_mola);(목적위치/'report.json').write_text(json.dumps(netefatso_pego,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':dirisa()
