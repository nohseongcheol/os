#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from gnìomhaich_àithne import tilg_freumh,àithne

def ruith():
    ceann_uidhe_VALUE_suidhich=tilg_freumh/'build/verification/windows';ceann_uidhe_VALUE_suidhich.mkdir(parents=True,exist_ok=True)
    dearbhadh_aithisg={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((tilg_freumh/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ràgh=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        dàta_suidhich=subprocess.Popen(àithne()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        roghnaichear_a916db4e=selectors.DefaultSelector();roghnaichear_a916db4e.register(dàta_suidhich.stdout,selectors.EVENT_READ)
        def làmhrachan_tachartas(초단위=.1):
            for 누름값,_ in roghnaichear_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ràgh.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ràgh and b'HALTED' not in LOG_ràgh,LOG_ràgh[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            crìochnaich_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ràgh[현재위치:]:
                if time.monotonic()>crìochnaich_OFFSET or dàta_suidhich.poll() is not None:raise AssertionError(LOG_ràgh[현재위치:].decode('utf-8','replace'))
                làmhrachan_tachartas()
            return bytes(LOG_ràgh[현재위치:])
        def cuir(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ràgh);dàta_suidhich.stdin.write(SECOND_VALUE);dàta_suidhich.stdin.flush();return 기다리기(확인표시,현재위치)
        def slige(sreang_dàta):return cuir((sreang_dàta+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ath_ghoirid_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def briog_putan(co_chomharra_x,세로좌표):return bytes([30,1,1,co_chomharra_x&255,co_chomharra_x>>8,세로좌표&255,세로좌표>>8,30,1,0,co_chomharra_x&255,co_chomharra_x>>8,세로좌표&255,세로좌표>>8])
        def àithne_MODE():
            dàta_suidhich.stdin.write(b'\x1b');dàta_suidhich.stdin.flush();crìochnaich_OFFSET=time.monotonic()+.2
            while time.monotonic()<crìochnaich_OFFSET:làmhrachan_tachartas(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            slige('terminal');làmhrachan_tachartas(.3)
            slige('mkdir first; cd first; export NAME=one')
            cuir('vi 첫째.py\n'.encode(),b'NORMAL')
            cuir('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            crìochnaich_OFFSET=time.monotonic()+3
            while time.monotonic()<crìochnaich_OFFSET:làmhrachan_tachartas(.1)
            cuir(ath_ghoirid_VALUE(1),b'TERMINAL FOCUS 2');làmhrachan_tachartas(.2)
            assert b'/\r\n' in slige('pwd')
            slige('export NAME=two')
            cuir('vi 둘째.txt\n'.encode(),b'NORMAL')
            cuir('i두 번째 uinneag\n'.encode(),b'INSERT')
            cuir(briog_putan(180,12),b'TERMINAL FOCUS 1');làmhrachan_tachartas(.2)
            àithne_MODE();cuir(b':wq\r')
            assert b'one:/first' in slige('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in slige('cat 첫째.py')
            tomhas=slige('python 첫째.py');assert b'42\r\n' in tomhas,tomhas
            # Close the first shell with its actual title-bar X; second editor resumes.
            cuir(briog_putan(560,63),b'TERMINAL FOCUS 2');làmhrachan_tachartas(.2)
            àithne_MODE();cuir(b':wq\r')
            assert b'two:/' in slige('echo "$NAME:$PWD"')
            assert '두 번째 uinneag'.encode() in slige('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            cuir('vi 둘째.txt\n'.encode(),b'NORMAL');cuir(b'xu',b'NORMAL')
            cuir(b'iX',b'INSERT');àithne_MODE();cuir(b':q\r',b'Unsaved')
            cuir(b':q!\r');assert '두 번째 uinneag'.encode() in slige('cat 둘째.txt')
            cuir(ath_ghoirid_VALUE(1),b'TERMINAL FOCUS 1');làmhrachan_tachartas(.2)
            cuir(ath_ghoirid_VALUE(1),b'TERMINAL FOCUS 3');làmhrachan_tachartas(.2)
            cuir(ath_ghoirid_VALUE(1),b'TERMINAL FOCUS 4');làmhrachan_tachartas(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            dàta_suidhich.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));dàta_suidhich.stdin.flush()
            slige('echo DRAGGED_OK')
            cuir('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            cuir('i저장하지 않은 dàta'.encode(),b'INSERT')
            cuir(briog_putan(578,97),b'TERMINAL FOCUS 3');làmhrachan_tachartas(.2)
            assert '버릴문서.txt'.encode() not in slige('ls')
            cuir(ath_ghoirid_VALUE(1),b'TERMINAL FOCUS 4');làmhrachan_tachartas(.2)
            slige('echo REUSED_WINDOW_OK')
            완료량=LOG_ràgh.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            crìochnaich_OFFSET=time.monotonic()+.3
            while time.monotonic()<crìochnaich_OFFSET:làmhrachan_tachartas(.05)
            with socket.socket(socket.AF_UNIX) as còd_a_charactair:
                còd_a_charactair.settimeout(10);còd_a_charactair.connect(str(모의제어접속))
                with còd_a_charactair.makefile('rwb') as faidhle_cur_a_steach:
                    json.loads(faidhle_cur_a_steach.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ceann_uidhe_VALUE_suidhich/'four-terminals.png'),'format':'png'}}):
                        faidhle_cur_a_steach.write((json.dumps(요청값)+'\n').encode());faidhle_cur_a_steach.flush()
                        while True:
                            반환값=json.loads(faidhle_cur_a_steach.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ceann_uidhe_VALUE_suidhich/'four-terminals.png')).convert('RGB')
            for càraid_àireimh,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(càraid_àireimh)==색상,(càraid_àireimh,화소들.getpixel(càraid_àireimh))
            slige('echo FOUR_WINDOWS_OK')
            dearbhadh_aithisg.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if dàta_suidhich.poll() is None:dàta_suidhich.terminate()
            try:dàta_suidhich.wait(timeout=5)
            except subprocess.TimeoutExpired:dàta_suidhich.kill();dàta_suidhich.wait()
            roghnaichear_a916db4e.close();dàta_suidhich.stdin.close();dàta_suidhich.stdout.close();(ceann_uidhe_VALUE_suidhich/'serial.log').write_bytes(LOG_ràgh);(ceann_uidhe_VALUE_suidhich/'report.json').write_text(json.dumps(dearbhadh_aithisg,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ruith()
