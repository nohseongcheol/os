#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import 기준,aluwataaya

def 시작():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    anaajiaakua_ipa_achikiimaajatü={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};aa_innachikimaajatü_aparatsee=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(aluwataaya()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(자료위치.stdout,selectors.EVENT_READ)
        def aapaaya_kasachiki(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:aa_innachikimaajatü_aparatsee.extend(둘째값)
            assert b'PANIC:' not in aa_innachikimaajatü_aparatsee and b'HALTED' not in aa_innachikimaajatü_aparatsee,aa_innachikimaajatü_aparatsee[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in aa_innachikimaajatü_aparatsee[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(aa_innachikimaajatü_aparatsee[현재위치:].decode('utf-8','replace'))
                aapaaya_kasachiki()
            return bytes(aa_innachikimaajatü_aparatsee[현재위치:])
        def ajütaa(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(aa_innachikimaajatü_aparatsee);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def aluwataalapu_u(kaleena_atijaaya):return ajütaa((kaleena_atijaaya+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def a_ttaaya_uwatuale_e_ajutuu(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def aküliküjaa_ajüttülee(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def aluwataaya_akua_ipaa():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:aapaaya_kasachiki(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            aluwataalapu_u('terminal');aapaaya_kasachiki(.3)
            aluwataalapu_u('mkdir first; cd first; export NAME=one')
            ajütaa('vi 첫째.py\n'.encode(),b'NORMAL')
            ajütaa('i값 = 21\nprint(ajutuu * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:aapaaya_kasachiki(.1)
            ajütaa(a_ttaaya_uwatuale_e_ajutuu(1),b'TERMINAL FOCUS 2');aapaaya_kasachiki(.2)
            assert b'/\r\n' in aluwataalapu_u('pwd')
            aluwataalapu_u('export NAME=two')
            ajütaa('vi 둘째.txt\n'.encode(),b'NORMAL')
            ajütaa('i두 번째 analaaya\n'.encode(),b'INSERT')
            ajütaa(aküliküjaa_ajüttülee(180,12),b'TERMINAL FOCUS 1');aapaaya_kasachiki(.2)
            aluwataaya_akua_ipaa();ajütaa(b':wq\r')
            assert b'one:/first' in aluwataalapu_u('echo "$NAME:$PWD"')
            assert 'ajutuu = 21\r\nprint(ajutuu * 2)'.encode() in aluwataalapu_u('cat 첫째.py')
            결과=aluwataalapu_u('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            ajütaa(aküliküjaa_ajüttülee(560,63),b'TERMINAL FOCUS 2');aapaaya_kasachiki(.2)
            aluwataaya_akua_ipaa();ajütaa(b':wq\r')
            assert b'two:/' in aluwataalapu_u('echo "$NAME:$PWD"')
            assert '두 번째 analaaya'.encode() in aluwataalapu_u('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ajütaa('vi 둘째.txt\n'.encode(),b'NORMAL');ajütaa(b'xu',b'NORMAL')
            ajütaa(b'iX',b'INSERT');aluwataaya_akua_ipaa();ajütaa(b':q\r',b'Unsaved')
            ajütaa(b':q!\r');assert '두 번째 analaaya'.encode() in aluwataalapu_u('cat 둘째.txt')
            ajütaa(a_ttaaya_uwatuale_e_ajutuu(1),b'TERMINAL FOCUS 1');aapaaya_kasachiki(.2)
            ajütaa(a_ttaaya_uwatuale_e_ajutuu(1),b'TERMINAL FOCUS 3');aapaaya_kasachiki(.2)
            ajütaa(a_ttaaya_uwatuale_e_ajutuu(1),b'TERMINAL FOCUS 4');aapaaya_kasachiki(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            aluwataalapu_u('echo DRAGGED_OK')
            ajütaa('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ajütaa('i저장하지 않은 atijaaya'.encode(),b'INSERT')
            ajütaa(aküliküjaa_ajüttülee(578,97),b'TERMINAL FOCUS 3');aapaaya_kasachiki(.2)
            assert '버릴문서.txt'.encode() not in aluwataalapu_u('ls')
            ajütaa(a_ttaaya_uwatuale_e_ajutuu(1),b'TERMINAL FOCUS 4');aapaaya_kasachiki(.2)
            aluwataalapu_u('echo REUSED_WINDOW_OK')
            완료량=aa_innachikimaajatü_aparatsee.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:aapaaya_kasachiki(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as anaajaalaa_ekeroliaa:
                    json.loads(anaajaalaa_ekeroliaa.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        anaajaalaa_ekeroliaa.write((json.dumps(요청값)+'\n').encode());anaajaalaa_ekeroliaa.flush()
                        while True:
                            반환값=json.loads(anaajaalaa_ekeroliaa.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for piamasü_ayaawatülee,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(piamasü_ayaawatülee)==색상,(piamasü_ayaawatülee,화소들.getpixel(piamasü_ayaawatülee))
            aluwataalapu_u('echo FOUR_WINDOWS_OK')
            anaajiaakua_ipa_achikiimaajatü.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            선택기.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(aa_innachikimaajatü_aparatsee);(목적위치/'report.json').write_text(json.dumps(anaajiaakua_ipa_achikiimaajatü,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':시작()
