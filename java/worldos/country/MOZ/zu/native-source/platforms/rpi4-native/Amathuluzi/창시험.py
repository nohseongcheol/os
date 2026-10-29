#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from yenza_umyalo import 기준,Umlayelo

def Sebenzisa():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    ukufakazisa_umbiko={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};loga_umugqa=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Umlayelo()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        isiqoki_a916db4e=selectors.DefaultSelector();isiqoki_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def isibambo_isigameko(초단위=.1):
            for 누름값,_ in isiqoki_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:loga_umugqa.extend(둘째값)
            assert b'PANIC:' not in loga_umugqa and b'HALTED' not in loga_umugqa,loga_umugqa[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            yekisa_I_ofisethi=time.monotonic()+초단위
            while 확인표시 not in loga_umugqa[현재위치:]:
                if time.monotonic()>yekisa_I_ofisethi or 자료위치.poll() is not None:raise AssertionError(loga_umugqa[현재위치:].decode('utf-8','replace'))
                isibambo_isigameko()
            return bytes(loga_umugqa[현재위치:])
        def Thumela(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(loga_umugqa);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def isihumushi_miyalelo(uchunge_imininingwane):return Thumela((uchunge_imininingwane+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ukunqamulela_inani(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def qhafaza_inkinobho(okuxhumanisa_u_x,세로좌표):return bytes([30,1,1,okuxhumanisa_u_x&255,okuxhumanisa_u_x>>8,세로좌표&255,세로좌표>>8,30,1,0,okuxhumanisa_u_x&255,okuxhumanisa_u_x>>8,세로좌표&255,세로좌표>>8])
        def umyalo_inqubo():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();yekisa_I_ofisethi=time.monotonic()+.2
            while time.monotonic()<yekisa_I_ofisethi:isibambo_isigameko(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            isihumushi_miyalelo('terminal');isibambo_isigameko(.3)
            isihumushi_miyalelo('mkdir first; cd first; export NAME=one')
            Thumela('vi 첫째.py\n'.encode(),b'NORMAL')
            Thumela('i값 = 21\nprint(inani * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            yekisa_I_ofisethi=time.monotonic()+3
            while time.monotonic()<yekisa_I_ofisethi:isibambo_isigameko(.1)
            Thumela(ukunqamulela_inani(1),b'TERMINAL FOCUS 2');isibambo_isigameko(.2)
            assert b'/\r\n' in isihumushi_miyalelo('pwd')
            isihumushi_miyalelo('export NAME=two')
            Thumela('vi 둘째.txt\n'.encode(),b'NORMAL')
            Thumela('i두 번째 ifasitela\n'.encode(),b'INSERT')
            Thumela(qhafaza_inkinobho(180,12),b'TERMINAL FOCUS 1');isibambo_isigameko(.2)
            umyalo_inqubo();Thumela(b':wq\r')
            assert b'one:/first' in isihumushi_miyalelo('echo "$NAME:$PWD"')
            assert 'inani = 21\r\nprint(inani * 2)'.encode() in isihumushi_miyalelo('cat 첫째.py')
            결과=isihumushi_miyalelo('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            Thumela(qhafaza_inkinobho(560,63),b'TERMINAL FOCUS 2');isibambo_isigameko(.2)
            umyalo_inqubo();Thumela(b':wq\r')
            assert b'two:/' in isihumushi_miyalelo('echo "$NAME:$PWD"')
            assert '두 번째 ifasitela'.encode() in isihumushi_miyalelo('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            Thumela('vi 둘째.txt\n'.encode(),b'NORMAL');Thumela(b'xu',b'NORMAL')
            Thumela(b'iX',b'INSERT');umyalo_inqubo();Thumela(b':q\r',b'Unsaved')
            Thumela(b':q!\r');assert '두 번째 ifasitela'.encode() in isihumushi_miyalelo('cat 둘째.txt')
            Thumela(ukunqamulela_inani(1),b'TERMINAL FOCUS 1');isibambo_isigameko(.2)
            Thumela(ukunqamulela_inani(1),b'TERMINAL FOCUS 3');isibambo_isigameko(.2)
            Thumela(ukunqamulela_inani(1),b'TERMINAL FOCUS 4');isibambo_isigameko(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            isihumushi_miyalelo('echo DRAGGED_OK')
            Thumela('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            Thumela('i저장하지 않은 imininingwane'.encode(),b'INSERT')
            Thumela(qhafaza_inkinobho(578,97),b'TERMINAL FOCUS 3');isibambo_isigameko(.2)
            assert '버릴문서.txt'.encode() not in isihumushi_miyalelo('ls')
            Thumela(ukunqamulela_inani(1),b'TERMINAL FOCUS 4');isibambo_isigameko(.2)
            isihumushi_miyalelo('echo REUSED_WINDOW_OK')
            완료량=loga_umugqa.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            yekisa_I_ofisethi=time.monotonic()+.3
            while time.monotonic()<yekisa_I_ofisethi:isibambo_isigameko(.05)
            with socket.socket(socket.AF_UNIX) as ikhodi_yohlamvu:
                ikhodi_yohlamvu.settimeout(10);ikhodi_yohlamvu.connect(str(모의제어접속))
                with ikhodi_yohlamvu.makefile('rwb') as ifayela_okufakwayo:
                    json.loads(ifayela_okufakwayo.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        ifayela_okufakwayo.write((json.dumps(요청값)+'\n').encode());ifayela_okufakwayo.flush()
                        while True:
                            반환값=json.loads(ifayela_okufakwayo.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for ichashaza_kugrafu,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ichashaza_kugrafu)==색상,(ichashaza_kugrafu,화소들.getpixel(ichashaza_kugrafu))
            isihumushi_miyalelo('echo FOUR_WINDOWS_OK')
            ukufakazisa_umbiko.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            isiqoki_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(loga_umugqa);(목적위치/'report.json').write_text(json.dumps(ukufakazisa_umbiko,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Sebenzisa()
