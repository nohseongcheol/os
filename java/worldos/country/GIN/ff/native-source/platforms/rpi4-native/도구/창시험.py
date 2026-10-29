#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import 기준,ginol

def huutoraade():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    teeŋtingol_ciimtol={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};suurnal_winndande=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(ginol()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(자료위치.stdout,selectors.EVENT_READ)
        def jaggoode_saɗteende(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:suurnal_winndande.extend(둘째값)
            assert b'PANIC:' not in suurnal_winndande and b'HALTED' not in suurnal_winndande,suurnal_winndande[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in suurnal_winndande[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(suurnal_winndande[현재위치:].decode('utf-8','replace'))
                jaggoode_saɗteende()
            return bytes(suurnal_winndande[현재위치:])
        def neldude(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(suurnal_winndande);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def laalagal(ɓoggol_keɓe):return neldude((ɓoggol_keɓe+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def sodorde_njaru(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def dobaade_feɗoode(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def ginol_modd():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:jaggoode_saɗteende(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            laalagal('terminal');jaggoode_saɗteende(.3)
            laalagal('mkdir first; cd first; export NAME=one')
            neldude('vi 첫째.py\n'.encode(),b'NORMAL')
            neldude('i값 = 21\nprint(njaru * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:jaggoode_saɗteende(.1)
            neldude(sodorde_njaru(1),b'TERMINAL FOCUS 2');jaggoode_saɗteende(.2)
            assert b'/\r\n' in laalagal('pwd')
            laalagal('export NAME=two')
            neldude('vi 둘째.txt\n'.encode(),b'NORMAL')
            neldude('i두 번째 falanteere\n'.encode(),b'INSERT')
            neldude(dobaade_feɗoode(180,12),b'TERMINAL FOCUS 1');jaggoode_saɗteende(.2)
            ginol_modd();neldude(b':wq\r')
            assert b'one:/first' in laalagal('echo "$NAME:$PWD"')
            assert 'njaru = 21\r\nprint(njaru * 2)'.encode() in laalagal('cat 첫째.py')
            결과=laalagal('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            neldude(dobaade_feɗoode(560,63),b'TERMINAL FOCUS 2');jaggoode_saɗteende(.2)
            ginol_modd();neldude(b':wq\r')
            assert b'two:/' in laalagal('echo "$NAME:$PWD"')
            assert '두 번째 falanteere'.encode() in laalagal('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            neldude('vi 둘째.txt\n'.encode(),b'NORMAL');neldude(b'xu',b'NORMAL')
            neldude(b'iX',b'INSERT');ginol_modd();neldude(b':q\r',b'Unsaved')
            neldude(b':q!\r');assert '두 번째 falanteere'.encode() in laalagal('cat 둘째.txt')
            neldude(sodorde_njaru(1),b'TERMINAL FOCUS 1');jaggoode_saɗteende(.2)
            neldude(sodorde_njaru(1),b'TERMINAL FOCUS 3');jaggoode_saɗteende(.2)
            neldude(sodorde_njaru(1),b'TERMINAL FOCUS 4');jaggoode_saɗteende(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            laalagal('echo DRAGGED_OK')
            neldude('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            neldude('i저장하지 않은 keɓe'.encode(),b'INSERT')
            neldude(dobaade_feɗoode(578,97),b'TERMINAL FOCUS 3');jaggoode_saɗteende(.2)
            assert '버릴문서.txt'.encode() not in laalagal('ls')
            neldude(sodorde_njaru(1),b'TERMINAL FOCUS 4');jaggoode_saɗteende(.2)
            laalagal('echo REUSED_WINDOW_OK')
            완료량=suurnal_winndande.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:jaggoode_saɗteende(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as fiilde_naatnugol:
                    json.loads(fiilde_naatnugol.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        fiilde_naatnugol.write((json.dumps(요청값)+'\n').encode());fiilde_naatnugol.flush()
                        while True:
                            반환값=json.loads(fiilde_naatnugol.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for 좌표쌍,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(좌표쌍)==색상,(좌표쌍,화소들.getpixel(좌표쌍))
            laalagal('echo FOUR_WINDOWS_OK')
            teeŋtingol_ciimtol.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            선택기.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(suurnal_winndande);(목적위치/'report.json').write_text(json.dumps(teeŋtingol_ciimtol,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':huutoraade()
