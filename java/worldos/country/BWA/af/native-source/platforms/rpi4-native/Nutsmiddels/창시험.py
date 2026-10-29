#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from uitvoer_bevel import Project_wortel,Opdrag

def Loop():
    bestemming_VALUE_plaas=Project_wortel/'build/verification/windows';bestemming_VALUE_plaas.mkdir(parents=True,exist_ok=True)
    validering_verslag={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ry=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_plaas=subprocess.Popen(Opdrag()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selekteerder_a916db4e=selectors.DefaultSelector();selekteerder_a916db4e.register(data_plaas.stdout,selectors.EVENT_READ)
        def handvatsel_gebeurtenis(초단위=.1):
            for 누름값,_ in selekteerder_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ry.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ry and b'HALTED' not in LOG_ry,LOG_ry[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            beëindig_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ry[현재위치:]:
                if time.monotonic()>beëindig_OFFSET or data_plaas.poll() is not None:raise AssertionError(LOG_ry[현재위치:].decode('utf-8','replace'))
                handvatsel_gebeurtenis()
            return bytes(LOG_ry[현재위치:])
        def e_pos(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ry);data_plaas.stdin.write(SECOND_VALUE);data_plaas.stdin.flush();return 기다리기(확인표시,현재위치)
        def dop(string_data):return e_pos((string_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def kortpad_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_knoppie(x_koördinaat,Y_koördinaat):return bytes([30,1,1,x_koördinaat&255,x_koördinaat>>8,Y_koördinaat&255,Y_koördinaat>>8,30,1,0,x_koördinaat&255,x_koördinaat>>8,Y_koördinaat&255,Y_koördinaat>>8])
        def bevel_MODE():
            data_plaas.stdin.write(b'\x1b');data_plaas.stdin.flush();beëindig_OFFSET=time.monotonic()+.2
            while time.monotonic()<beëindig_OFFSET:handvatsel_gebeurtenis(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            dop('terminal');handvatsel_gebeurtenis(.3)
            dop('mkdir first; cd first; export NAME=one')
            e_pos('vi 첫째.py\n'.encode(),b'NORMAL')
            e_pos('i값 = 21\nprint(VALUE * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            beëindig_OFFSET=time.monotonic()+3
            while time.monotonic()<beëindig_OFFSET:handvatsel_gebeurtenis(.1)
            e_pos(kortpad_VALUE(1),b'TERMINAL FOCUS 2');handvatsel_gebeurtenis(.2)
            assert b'/\r\n' in dop('pwd')
            dop('export NAME=two')
            e_pos('vi 둘째.txt\n'.encode(),b'NORMAL')
            e_pos('i두 번째 venster\n'.encode(),b'INSERT')
            e_pos(klik_knoppie(180,12),b'TERMINAL FOCUS 1');handvatsel_gebeurtenis(.2)
            bevel_MODE();e_pos(b':wq\r')
            assert b'one:/first' in dop('echo "$NAME:$PWD"')
            assert 'VALUE = 21\r\nprint(VALUE * 2)'.encode() in dop('cat 첫째.py')
            maatreël=dop('python 첫째.py');assert b'42\r\n' in maatreël,maatreël
            # Close the first shell with its actual title-bar X; second editor resumes.
            e_pos(klik_knoppie(560,63),b'TERMINAL FOCUS 2');handvatsel_gebeurtenis(.2)
            bevel_MODE();e_pos(b':wq\r')
            assert b'two:/' in dop('echo "$NAME:$PWD"')
            assert '두 번째 venster'.encode() in dop('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            e_pos('vi 둘째.txt\n'.encode(),b'NORMAL');e_pos(b'xu',b'NORMAL')
            e_pos(b'iX',b'INSERT');bevel_MODE();e_pos(b':q\r',b'Unsaved')
            e_pos(b':q!\r');assert '두 번째 venster'.encode() in dop('cat 둘째.txt')
            e_pos(kortpad_VALUE(1),b'TERMINAL FOCUS 1');handvatsel_gebeurtenis(.2)
            e_pos(kortpad_VALUE(1),b'TERMINAL FOCUS 3');handvatsel_gebeurtenis(.2)
            e_pos(kortpad_VALUE(1),b'TERMINAL FOCUS 4');handvatsel_gebeurtenis(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            data_plaas.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));data_plaas.stdin.flush()
            dop('echo DRAGGED_OK')
            e_pos('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            e_pos('i저장하지 않은 data'.encode(),b'INSERT')
            e_pos(klik_knoppie(578,97),b'TERMINAL FOCUS 3');handvatsel_gebeurtenis(.2)
            assert '버릴문서.txt'.encode() not in dop('ls')
            e_pos(kortpad_VALUE(1),b'TERMINAL FOCUS 4');handvatsel_gebeurtenis(.2)
            dop('echo REUSED_WINDOW_OK')
            완료량=LOG_ry.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            beëindig_OFFSET=time.monotonic()+.3
            while time.monotonic()<beëindig_OFFSET:handvatsel_gebeurtenis(.05)
            with socket.socket(socket.AF_UNIX) as karakterkode:
                karakterkode.settimeout(10);karakterkode.connect(str(모의제어접속))
                with karakterkode.makefile('rwb') as lêer_inskrywing:
                    json.loads(lêer_inskrywing.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(bestemming_VALUE_plaas/'four-terminals.png'),'format':'png'}}):
                        lêer_inskrywing.write((json.dumps(요청값)+'\n').encode());lêer_inskrywing.flush()
                        while True:
                            반환값=json.loads(lêer_inskrywing.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(bestemming_VALUE_plaas/'four-terminals.png')).convert('RGB')
            for koördinaatpaar,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(koördinaatpaar)==색상,(koördinaatpaar,화소들.getpixel(koördinaatpaar))
            dop('echo FOUR_WINDOWS_OK')
            validering_verslag.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if data_plaas.poll() is None:data_plaas.terminate()
            try:data_plaas.wait(timeout=5)
            except subprocess.TimeoutExpired:data_plaas.kill();data_plaas.wait()
            selekteerder_a916db4e.close();data_plaas.stdin.close();data_plaas.stdout.close();(bestemming_VALUE_plaas/'serial.log').write_bytes(LOG_ry);(bestemming_VALUE_plaas/'report.json').write_text(json.dumps(validering_verslag,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Loop()
