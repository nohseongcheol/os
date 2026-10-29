#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import 기준,piqujijjut

def 시작():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    naammannirainiq_unikkaaq={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};papattivik_sanimukutaak=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(piqujijjut()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(자료위치.stdout,selectors.EVENT_READ)
        def nuuttarut_piniku(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:papattivik_sanimukutaak.extend(둘째값)
            assert b'PANIC:' not in papattivik_sanimukutaak and b'HALTED' not in papattivik_sanimukutaak,papattivik_sanimukutaak[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in papattivik_sanimukutaak[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(papattivik_sanimukutaak[현재위치:].decode('utf-8','replace'))
                nuuttarut_piniku()
            return bytes(papattivik_sanimukutaak[현재위치:])
        def nassiutili(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(papattivik_sanimukutaak);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def piqujijjutiliriji(qimiaq_titiqqat):return nassiutili((qimiaq_titiqqat+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def nangarut_atuutilik(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def naqilli_tikkuagaq(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def piqujijjut_mode():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:nuuttarut_piniku(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            piqujijjutiliriji('terminal');nuuttarut_piniku(.3)
            piqujijjutiliriji('mkdir first; cd first; export NAME=one')
            nassiutili('vi 첫째.py\n'.encode(),b'NORMAL')
            nassiutili('i값 = 21\nprint(atuutilik * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:nuuttarut_piniku(.1)
            nassiutili(nangarut_atuutilik(1),b'TERMINAL FOCUS 2');nuuttarut_piniku(.2)
            assert b'/\r\n' in piqujijjutiliriji('pwd')
            piqujijjutiliriji('export NAME=two')
            nassiutili('vi 둘째.txt\n'.encode(),b'NORMAL')
            nassiutili('i두 번째 igalaangujaq\n'.encode(),b'INSERT')
            nassiutili(naqilli_tikkuagaq(180,12),b'TERMINAL FOCUS 1');nuuttarut_piniku(.2)
            piqujijjut_mode();nassiutili(b':wq\r')
            assert b'one:/first' in piqujijjutiliriji('echo "$NAME:$PWD"')
            assert 'atuutilik = 21\r\nprint(atuutilik * 2)'.encode() in piqujijjutiliriji('cat 첫째.py')
            결과=piqujijjutiliriji('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            nassiutili(naqilli_tikkuagaq(560,63),b'TERMINAL FOCUS 2');nuuttarut_piniku(.2)
            piqujijjut_mode();nassiutili(b':wq\r')
            assert b'two:/' in piqujijjutiliriji('echo "$NAME:$PWD"')
            assert '두 번째 igalaangujaq'.encode() in piqujijjutiliriji('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            nassiutili('vi 둘째.txt\n'.encode(),b'NORMAL');nassiutili(b'xu',b'NORMAL')
            nassiutili(b'iX',b'INSERT');piqujijjut_mode();nassiutili(b':q\r',b'Unsaved')
            nassiutili(b':q!\r');assert '두 번째 igalaangujaq'.encode() in piqujijjutiliriji('cat 둘째.txt')
            nassiutili(nangarut_atuutilik(1),b'TERMINAL FOCUS 1');nuuttarut_piniku(.2)
            nassiutili(nangarut_atuutilik(1),b'TERMINAL FOCUS 3');nuuttarut_piniku(.2)
            nassiutili(nangarut_atuutilik(1),b'TERMINAL FOCUS 4');nuuttarut_piniku(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            piqujijjutiliriji('echo DRAGGED_OK')
            nassiutili('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            nassiutili('i저장하지 않은 titiqqat'.encode(),b'INSERT')
            nassiutili(naqilli_tikkuagaq(578,97),b'TERMINAL FOCUS 3');nuuttarut_piniku(.2)
            assert '버릴문서.txt'.encode() not in piqujijjutiliriji('ls')
            nassiutili(nangarut_atuutilik(1),b'TERMINAL FOCUS 4');nuuttarut_piniku(.2)
            piqujijjutiliriji('echo REUSED_WINDOW_OK')
            완료량=papattivik_sanimukutaak.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:nuuttarut_piniku(.05)
            with socket.socket(socket.AF_UNIX) as immikkuuqtumut_nalunaikkut:
                immikkuuqtumut_nalunaikkut.settimeout(10);immikkuuqtumut_nalunaikkut.connect(str(모의제어접속))
                with immikkuuqtumut_nalunaikkut.makefile('rwb') as ini_Iliniku:
                    json.loads(ini_Iliniku.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        ini_Iliniku.write((json.dumps(요청값)+'\n').encode());ini_Iliniku.flush()
                        while True:
                            반환값=json.loads(ini_Iliniku.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for illugiik,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(illugiik)==색상,(illugiik,화소들.getpixel(illugiik))
            piqujijjutiliriji('echo FOUR_WINDOWS_OK')
            naammannirainiq_unikkaaq.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            선택기.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(papattivik_sanimukutaak);(목적위치/'report.json').write_text(json.dumps(naammannirainiq_unikkaaq,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':시작()
