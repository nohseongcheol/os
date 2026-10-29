#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from bajarmoq_buyruq import Project_ildiz,Buyruq

def Bajarish():
    ko_chirish_joyi_VALUE_holat=Project_ildiz/'build/verification/windows';ko_chirish_joyi_VALUE_holat.mkdir(parents=True,exist_ok=True)
    tasdiq_hisobot={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_ildiz/'build/kernel8.img').read_bytes()).hexdigest()};LOG_satr=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ma_lumotlar_holat=subprocess.Popen(Buyruq()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        tanlagich_a916db4e=selectors.DefaultSelector();tanlagich_a916db4e.register(ma_lumotlar_holat.stdout,selectors.EVENT_READ)
        def deskriptor_hodisa(초단위=.1):
            for 누름값,_ in tanlagich_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_satr.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_satr and b'HALTED' not in LOG_satr,LOG_satr[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            to_xtatmoq_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_satr[현재위치:]:
                if time.monotonic()>to_xtatmoq_OFFSET or ma_lumotlar_holat.poll() is not None:raise AssertionError(LOG_satr[현재위치:].decode('utf-8','replace'))
                deskriptor_hodisa()
            return bytes(LOG_satr[현재위치:])
        def yuborish(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_satr);ma_lumotlar_holat.stdin.write(SECOND_VALUE);ma_lumotlar_holat.stdin.flush();return 기다리기(확인표시,현재위치)
        def qobiq(satr_ma_lumotlar):return yuborish((satr_ma_lumotlar+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def yorliq_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def chertmoq_tugma(x_koordinata,Y_tugmasi_koordinat):return bytes([30,1,1,x_koordinata&255,x_koordinata>>8,Y_tugmasi_koordinat&255,Y_tugmasi_koordinat>>8,30,1,0,x_koordinata&255,x_koordinata>>8,Y_tugmasi_koordinat&255,Y_tugmasi_koordinat>>8])
        def buyruq_MODE():
            ma_lumotlar_holat.stdin.write(b'\x1b');ma_lumotlar_holat.stdin.flush();to_xtatmoq_OFFSET=time.monotonic()+.2
            while time.monotonic()<to_xtatmoq_OFFSET:deskriptor_hodisa(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            qobiq('terminal');deskriptor_hodisa(.3)
            qobiq('mkdir first; cd first; export NAME=one')
            yuborish('vi 첫째.py\n'.encode(),b'NORMAL')
            yuborish('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            to_xtatmoq_OFFSET=time.monotonic()+3
            while time.monotonic()<to_xtatmoq_OFFSET:deskriptor_hodisa(.1)
            yuborish(yorliq_VALUE(1),b'TERMINAL FOCUS 2');deskriptor_hodisa(.2)
            assert b'/\r\n' in qobiq('pwd')
            qobiq('export NAME=two')
            yuborish('vi 둘째.txt\n'.encode(),b'NORMAL')
            yuborish('i두 번째 oyna\n'.encode(),b'INSERT')
            yuborish(chertmoq_tugma(180,12),b'TERMINAL FOCUS 1');deskriptor_hodisa(.2)
            buyruq_MODE();yuborish(b':wq\r')
            assert b'one:/first' in qobiq('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in qobiq('cat 첫째.py')
            o_lchov=qobiq('python 첫째.py');assert b'42\r\n' in o_lchov,o_lchov
            # Close the first shell with its actual title-bar X; second editor resumes.
            yuborish(chertmoq_tugma(560,63),b'TERMINAL FOCUS 2');deskriptor_hodisa(.2)
            buyruq_MODE();yuborish(b':wq\r')
            assert b'two:/' in qobiq('echo "$NAME:$PWD"')
            assert '두 번째 oyna'.encode() in qobiq('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            yuborish('vi 둘째.txt\n'.encode(),b'NORMAL');yuborish(b'xu',b'NORMAL')
            yuborish(b'iX',b'INSERT');buyruq_MODE();yuborish(b':q\r',b'Unsaved')
            yuborish(b':q!\r');assert '두 번째 oyna'.encode() in qobiq('cat 둘째.txt')
            yuborish(yorliq_VALUE(1),b'TERMINAL FOCUS 1');deskriptor_hodisa(.2)
            yuborish(yorliq_VALUE(1),b'TERMINAL FOCUS 3');deskriptor_hodisa(.2)
            yuborish(yorliq_VALUE(1),b'TERMINAL FOCUS 4');deskriptor_hodisa(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ma_lumotlar_holat.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ma_lumotlar_holat.stdin.flush()
            qobiq('echo DRAGGED_OK')
            yuborish('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            yuborish('i저장하지 않은 ma_lumotlar'.encode(),b'INSERT')
            yuborish(chertmoq_tugma(578,97),b'TERMINAL FOCUS 3');deskriptor_hodisa(.2)
            assert '버릴문서.txt'.encode() not in qobiq('ls')
            yuborish(yorliq_VALUE(1),b'TERMINAL FOCUS 4');deskriptor_hodisa(.2)
            qobiq('echo REUSED_WINDOW_OK')
            완료량=LOG_satr.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            to_xtatmoq_OFFSET=time.monotonic()+.3
            while time.monotonic()<to_xtatmoq_OFFSET:deskriptor_hodisa(.05)
            with socket.socket(socket.AF_UNIX) as belgi_kodi:
                belgi_kodi.settimeout(10);belgi_kodi.connect(str(모의제어접속))
                with belgi_kodi.makefile('rwb') as fayl_kiritish:
                    json.loads(fayl_kiritish.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ko_chirish_joyi_VALUE_holat/'four-terminals.png'),'format':'png'}}):
                        fayl_kiritish.write((json.dumps(요청값)+'\n').encode());fayl_kiritish.flush()
                        while True:
                            반환값=json.loads(fayl_kiritish.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ko_chirish_joyi_VALUE_holat/'four-terminals.png')).convert('RGB')
            for koordinatalar_jufti,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koordinatalar_jufti)==색상,(koordinatalar_jufti,화소들.getpixel(koordinatalar_jufti))
            qobiq('echo FOUR_WINDOWS_OK')
            tasdiq_hisobot.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ma_lumotlar_holat.poll() is None:ma_lumotlar_holat.terminate()
            try:ma_lumotlar_holat.wait(timeout=5)
            except subprocess.TimeoutExpired:ma_lumotlar_holat.kill();ma_lumotlar_holat.wait()
            tanlagich_a916db4e.close();ma_lumotlar_holat.stdin.close();ma_lumotlar_holat.stdout.close();(ko_chirish_joyi_VALUE_holat/'serial.log').write_bytes(LOG_satr);(ko_chirish_joyi_VALUE_holat/'report.json').write_text(json.dumps(tasdiq_hisobot,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Bajarish()
