#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Utfør_kommando import spegle_rot,Kommando

def Køyr_2():
    mål_VALUE_plassere=spegle_rot/'build/verification/windows';mål_VALUE_plassere.mkdir(parents=True,exist_ok=True)
    validering_rapport={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((spegle_rot/'build/kernel8.img').read_bytes()).hexdigest()};LOG_rad=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_plassere=subprocess.Popen(Kommando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        veljar_a916db4e=selectors.DefaultSelector();veljar_a916db4e.register(data_plassere.stdout,selectors.EVENT_READ)
        def handtak_hending(초단위=.1):
            for 누름값,_ in veljar_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_rad.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_rad and b'HALTED' not in LOG_rad,LOG_rad[-2048:]
        def 기다리기(확인표시,betalt_plassere,초단위=50):
            avslutte_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_rad[betalt_plassere:]:
                if time.monotonic()>avslutte_OFFSET or data_plassere.poll() is not None:raise AssertionError(LOG_rad[betalt_plassere:].decode('utf-8','replace'))
                handtak_hending()
            return bytes(LOG_rad[betalt_plassere:])
        def sende(SECOND_VALUE,확인표시=b'jkoros-native> '):
            betalt_plassere=len(LOG_rad);data_plassere.stdin.write(SECOND_VALUE);data_plassere.stdin.flush();return 기다리기(확인표시,betalt_plassere)
        def grensesnitt(streng_data):return sende((streng_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def snarveg_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klikk_knapp(x_koordinat,Y_koordinat):return bytes([30,1,1,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8,30,1,0,x_koordinat&255,x_koordinat>>8,Y_koordinat&255,Y_koordinat>>8])
        def kommando_MODE():
            data_plassere.stdin.write(b'\x1b');data_plassere.stdin.flush();avslutte_OFFSET=time.monotonic()+.2
            while time.monotonic()<avslutte_OFFSET:handtak_hending(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            grensesnitt('terminal');handtak_hending(.3)
            grensesnitt('mkdir first; cd first; export NAME=one')
            sende('vi 첫째.py\n'.encode(),b'NORMAL')
            sende('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            avslutte_OFFSET=time.monotonic()+3
            while time.monotonic()<avslutte_OFFSET:handtak_hending(.1)
            sende(snarveg_VALUE(1),b'TERMINAL FOCUS 2');handtak_hending(.2)
            assert b'/\r\n' in grensesnitt('pwd')
            grensesnitt('export NAME=two')
            sende('vi 둘째.txt\n'.encode(),b'NORMAL')
            sende('i두 번째 vindauge\n'.encode(),b'INSERT')
            sende(klikk_knapp(180,12),b'TERMINAL FOCUS 1');handtak_hending(.2)
            kommando_MODE();sende(b':wq\r')
            assert b'one:/first' in grensesnitt('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in grensesnitt('cat 첫째.py')
            forretningsmål=grensesnitt('python 첫째.py');assert b'42\r\n' in forretningsmål,forretningsmål
            # Close the first shell with its actual title-bar X; second editor resumes.
            sende(klikk_knapp(560,63),b'TERMINAL FOCUS 2');handtak_hending(.2)
            kommando_MODE();sende(b':wq\r')
            assert b'two:/' in grensesnitt('echo "$NAME:$PWD"')
            assert '두 번째 vindauge'.encode() in grensesnitt('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            sende('vi 둘째.txt\n'.encode(),b'NORMAL');sende(b'xu',b'NORMAL')
            sende(b'iX',b'INSERT');kommando_MODE();sende(b':q\r',b'Unsaved')
            sende(b':q!\r');assert '두 번째 vindauge'.encode() in grensesnitt('cat 둘째.txt')
            sende(snarveg_VALUE(1),b'TERMINAL FOCUS 1');handtak_hending(.2)
            sende(snarveg_VALUE(1),b'TERMINAL FOCUS 3');handtak_hending(.2)
            sende(snarveg_VALUE(1),b'TERMINAL FOCUS 4');handtak_hending(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_plassere.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_plassere.stdin.flush()
            grensesnitt('echo DRAGGED_OK')
            sende('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            sende('i저장하지 않은 data'.encode(),b'INSERT')
            sende(klikk_knapp(578,97),b'TERMINAL FOCUS 3');handtak_hending(.2)
            assert '버릴문서.txt'.encode() not in grensesnitt('ls')
            sende(snarveg_VALUE(1),b'TERMINAL FOCUS 4');handtak_hending(.2)
            grensesnitt('echo REUSED_WINDOW_OK')
            완료량=LOG_rad.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            avslutte_OFFSET=time.monotonic()+.3
            while time.monotonic()<avslutte_OFFSET:handtak_hending(.05)
            with socket.socket(socket.AF_UNIX) as teiknkode:
                teiknkode.settimeout(10);teiknkode.connect(str(모의제어접속))
                with teiknkode.makefile('rwb') as fil_oppføring:
                    json.loads(fil_oppføring.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(mål_VALUE_plassere/'four-terminals.png'),'format':'png'}}):
                        fil_oppføring.write((json.dumps(요청값)+'\n').encode());fil_oppføring.flush()
                        while True:
                            반환값=json.loads(fil_oppføring.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(mål_VALUE_plassere/'four-terminals.png')).convert('RGB')
            for koordinatpar,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinatpar)==색상,(koordinatpar,화소들.getpixel(koordinatpar))
            grensesnitt('echo FOUR_WINDOWS_OK')
            validering_rapport.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_plassere.poll() is None:data_plassere.terminate()
            try:data_plassere.wait(timeout=5)
            except subprocess.TimeoutExpired:data_plassere.kill();data_plassere.wait()
            veljar_a916db4e.close();data_plassere.stdin.close();data_plassere.stdout.close();(mål_VALUE_plassere/'serial.log').write_bytes(LOG_rad);(mål_VALUE_plassere/'report.json').write_text(json.dumps(validering_rapport,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Køyr_2()
