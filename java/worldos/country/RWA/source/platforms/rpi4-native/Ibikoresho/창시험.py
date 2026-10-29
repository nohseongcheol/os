#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from gukora_ibwiriza import 기준,Icyo_wifuza

def ihuriro():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    iyemeza_raporo={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};kubika_umurongo=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Icyo_wifuza()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        muhitamo_a916db4e=selectors.DefaultSelector();muhitamo_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def umukondo_icyabaye(초단위=.1):
            for 누름값,_ in muhitamo_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:kubika_umurongo.extend(둘째값)
            assert b'PANIC:' not in kubika_umurongo and b'HALTED' not in kubika_umurongo,kubika_umurongo[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            kurangiza_Ofuseti=time.monotonic()+초단위
            while 확인표시 not in kubika_umurongo[현재위치:]:
                if time.monotonic()>kurangiza_Ofuseti or 자료위치.poll() is not None:raise AssertionError(kubika_umurongo[현재위치:].decode('utf-8','replace'))
                umukondo_icyabaye()
            return bytes(kubika_umurongo[현재위치:])
        def kohereza(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(kubika_umurongo);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def insomamabwiriza(igicenteruro_amakurushingiro):return kohereza((igicenteruro_amakurushingiro+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ihinanzira_agaciro(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def gukanda_buto(Ihuza_rya_x,세로좌표):return bytes([30,1,1,Ihuza_rya_x&255,Ihuza_rya_x>>8,세로좌표&255,세로좌표>>8,30,1,0,Ihuza_rya_x&255,Ihuza_rya_x>>8,세로좌표&255,세로좌표>>8])
        def ibwiriza_uburyo():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();kurangiza_Ofuseti=time.monotonic()+.2
            while time.monotonic()<kurangiza_Ofuseti:umukondo_icyabaye(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            insomamabwiriza('terminal');umukondo_icyabaye(.3)
            insomamabwiriza('mkdir first; cd first; export NAME=one')
            kohereza('vi 첫째.py\n'.encode(),b'NORMAL')
            kohereza('i값 = 21\nprint(agaciro * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            kurangiza_Ofuseti=time.monotonic()+3
            while time.monotonic()<kurangiza_Ofuseti:umukondo_icyabaye(.1)
            kohereza(ihinanzira_agaciro(1),b'TERMINAL FOCUS 2');umukondo_icyabaye(.2)
            assert b'/\r\n' in insomamabwiriza('pwd')
            insomamabwiriza('export NAME=two')
            kohereza('vi 둘째.txt\n'.encode(),b'NORMAL')
            kohereza('i두 번째 idirishya\n'.encode(),b'INSERT')
            kohereza(gukanda_buto(180,12),b'TERMINAL FOCUS 1');umukondo_icyabaye(.2)
            ibwiriza_uburyo();kohereza(b':wq\r')
            assert b'one:/first' in insomamabwiriza('echo "$NAME:$PWD"')
            assert 'agaciro = 21\r\nprint(agaciro * 2)'.encode() in insomamabwiriza('cat 첫째.py')
            결과=insomamabwiriza('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            kohereza(gukanda_buto(560,63),b'TERMINAL FOCUS 2');umukondo_icyabaye(.2)
            ibwiriza_uburyo();kohereza(b':wq\r')
            assert b'two:/' in insomamabwiriza('echo "$NAME:$PWD"')
            assert '두 번째 idirishya'.encode() in insomamabwiriza('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            kohereza('vi 둘째.txt\n'.encode(),b'NORMAL');kohereza(b'xu',b'NORMAL')
            kohereza(b'iX',b'INSERT');ibwiriza_uburyo();kohereza(b':q\r',b'Unsaved')
            kohereza(b':q!\r');assert '두 번째 idirishya'.encode() in insomamabwiriza('cat 둘째.txt')
            kohereza(ihinanzira_agaciro(1),b'TERMINAL FOCUS 1');umukondo_icyabaye(.2)
            kohereza(ihinanzira_agaciro(1),b'TERMINAL FOCUS 3');umukondo_icyabaye(.2)
            kohereza(ihinanzira_agaciro(1),b'TERMINAL FOCUS 4');umukondo_icyabaye(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            insomamabwiriza('echo DRAGGED_OK')
            kohereza('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            kohereza('i저장하지 않은 amakurushingiro'.encode(),b'INSERT')
            kohereza(gukanda_buto(578,97),b'TERMINAL FOCUS 3');umukondo_icyabaye(.2)
            assert '버릴문서.txt'.encode() not in insomamabwiriza('ls')
            kohereza(ihinanzira_agaciro(1),b'TERMINAL FOCUS 4');umukondo_icyabaye(.2)
            insomamabwiriza('echo REUSED_WINDOW_OK')
            완료량=kubika_umurongo.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            kurangiza_Ofuseti=time.monotonic()+.3
            while time.monotonic()<kurangiza_Ofuseti:umukondo_icyabaye(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as dosiye_icyinjizwa:
                    json.loads(dosiye_icyinjizwa.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        dosiye_icyinjizwa.write((json.dumps(요청값)+'\n').encode());dosiye_icyinjizwa.flush()
                        while True:
                            반환값=json.loads(dosiye_icyinjizwa.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for inyabubiri_y_indangakadomo,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(inyabubiri_y_indangakadomo)==색상,(inyabubiri_y_indangakadomo,화소들.getpixel(inyabubiri_y_indangakadomo))
            insomamabwiriza('echo FOUR_WINDOWS_OK')
            iyemeza_raporo.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            muhitamo_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(kubika_umurongo);(목적위치/'report.json').write_text(json.dumps(iyemeza_raporo,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ihuriro()
