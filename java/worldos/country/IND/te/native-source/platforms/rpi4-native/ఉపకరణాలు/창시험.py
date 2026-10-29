#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం,ఆదేశము

def నడుపుము():
    గమ్యం_మూల్యం_స్థాయి=ప్రొజెక్ట్_మూలం/'build/verification/windows';గమ్యం_మూల్యం_స్థాయి.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ప్రొజెక్ట్_మూలం/'build/kernel8.img').read_bytes()).hexdigest()};లాగ్_వరుస=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        డేటా_స్థాయి=subprocess.Popen(ఆదేశము()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        సెలక్టర్_a916db4e=selectors.DefaultSelector();సెలక్టర్_a916db4e.register(డేటా_స్థాయి.stdout,selectors.EVENT_READ)
        def నిర్వాహకం_ఈవెంట్(초단위=.1):
            for 누름값,_ in సెలక్టర్_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:లాగ్_వరుస.extend(둘째값)
            assert b'PANIC:' not in లాగ్_వరుస and b'HALTED' not in లాగ్_వరుస,లాగ్_వరుస[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ముగించు_ఆఫ్_సెట్=time.monotonic()+초단위
            while 확인표시 not in లాగ్_వరుస[현재위치:]:
                if time.monotonic()>ముగించు_ఆఫ్_సెట్ or డేటా_స్థాయి.poll() is not None:raise AssertionError(లాగ్_వరుస[현재위치:].decode('utf-8','replace'))
                నిర్వాహకం_ఈవెంట్()
            return bytes(లాగ్_వరుస[현재위치:])
        def పంపు(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(లాగ్_వరుస);డేటా_స్థాయి.stdin.write(둘째값);డేటా_స్థాయి.stdin.flush();return 기다리기(확인표시,현재위치)
        def షెల్(అక్షరసరం_డేటా):return పంపు((అక్షరసరం_డేటా+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def సత్వరమార్గం_మూల్యం(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def క్లిక్_చెయండి_బటన్(x_నిర్దేశాంకం,Y_బటన్_సమన్వయపరుచు):return bytes([30,1,1,x_నిర్దేశాంకం&255,x_నిర్దేశాంకం>>8,Y_బటన్_సమన్వయపరుచు&255,Y_బటన్_సమన్వయపరుచు>>8,30,1,0,x_నిర్దేశాంకం&255,x_నిర్దేశాంకం>>8,Y_బటన్_సమన్వయపరుచు&255,Y_బటన్_సమన్వయపరుచు>>8])
        def ఆదేశం_మోడ్():
            డేటా_స్థాయి.stdin.write(b'\x1b');డేటా_స్థాయి.stdin.flush();ముగించు_ఆఫ్_సెట్=time.monotonic()+.2
            while time.monotonic()<ముగించు_ఆఫ్_సెట్:నిర్వాహకం_ఈవెంట్(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            షెల్('terminal');నిర్వాహకం_ఈవెంట్(.3)
            షెల్('mkdir first; cd first; export NAME=one')
            పంపు('vi 첫째.py\n'.encode(),b'NORMAL')
            పంపు('i값 = 21\nprint(మూల్యం * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ముగించు_ఆఫ్_సెట్=time.monotonic()+3
            while time.monotonic()<ముగించు_ఆఫ్_సెట్:నిర్వాహకం_ఈవెంట్(.1)
            పంపు(సత్వరమార్గం_మూల్యం(1),b'TERMINAL FOCUS 2');నిర్వాహకం_ఈవెంట్(.2)
            assert b'/\r\n' in షెల్('pwd')
            షెల్('export NAME=two')
            పంపు('vi 둘째.txt\n'.encode(),b'NORMAL')
            పంపు('i두 번째 విండో\n'.encode(),b'INSERT')
            పంపు(క్లిక్_చెయండి_బటన్(180,12),b'TERMINAL FOCUS 1');నిర్వాహకం_ఈవెంట్(.2)
            ఆదేశం_మోడ్();పంపు(b':wq\r')
            assert b'one:/first' in షెల్('echo "$NAME:$PWD"')
            assert 'మూల్యం = 21\r\nprint(మూల్యం * 2)'.encode() in షెల్('cat 첫째.py')
            ప్రమాణం=షెల్('python 첫째.py');assert b'42\r\n' in ప్రమాణం,ప్రమాణం
            # Close the first shell with its actual title-bar X; second editor resumes.
            పంపు(క్లిక్_చెయండి_బటన్(560,63),b'TERMINAL FOCUS 2');నిర్వాహకం_ఈవెంట్(.2)
            ఆదేశం_మోడ్();పంపు(b':wq\r')
            assert b'two:/' in షెల్('echo "$NAME:$PWD"')
            assert '두 번째 విండో'.encode() in షెల్('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            పంపు('vi 둘째.txt\n'.encode(),b'NORMAL');పంపు(b'xu',b'NORMAL')
            పంపు(b'iX',b'INSERT');ఆదేశం_మోడ్();పంపు(b':q\r',b'Unsaved')
            పంపు(b':q!\r');assert '두 번째 విండో'.encode() in షెల్('cat 둘째.txt')
            పంపు(సత్వరమార్గం_మూల్యం(1),b'TERMINAL FOCUS 1');నిర్వాహకం_ఈవెంట్(.2)
            పంపు(సత్వరమార్గం_మూల్యం(1),b'TERMINAL FOCUS 3');నిర్వాహకం_ఈవెంట్(.2)
            పంపు(సత్వరమార్గం_మూల్యం(1),b'TERMINAL FOCUS 4');నిర్వాహకం_ఈవెంట్(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            డేటా_స్థాయి.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));డేటా_స్థాయి.stdin.flush()
            షెల్('echo DRAGGED_OK')
            పంపు('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            పంపు('i저장하지 않은 డేటా'.encode(),b'INSERT')
            పంపు(క్లిక్_చెయండి_బటన్(578,97),b'TERMINAL FOCUS 3');నిర్వాహకం_ఈవెంట్(.2)
            assert '버릴문서.txt'.encode() not in షెల్('ls')
            పంపు(సత్వరమార్గం_మూల్యం(1),b'TERMINAL FOCUS 4');నిర్వాహకం_ఈవెంట్(.2)
            షెల్('echo REUSED_WINDOW_OK')
            완료량=లాగ్_వరుస.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ముగించు_ఆఫ్_సెట్=time.monotonic()+.3
            while time.monotonic()<ముగించు_ఆఫ్_సెట్:నిర్వాహకం_ఈవెంట్(.05)
            with socket.socket(socket.AF_UNIX) as అక్షర_కోడ్:
                అక్షర_కోడ్.settimeout(10);అక్షర_కోడ్.connect(str(모의제어접속))
                with అక్షర_కోడ్.makefile('rwb') as ఫైలు_ప్రవేశం:
                    json.loads(ఫైలు_ప్రవేశం.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(గమ్యం_మూల్యం_స్థాయి/'four-terminals.png'),'format':'png'}}):
                        ఫైలు_ప్రవేశం.write((json.dumps(요청값)+'\n').encode());ఫైలు_ప్రవేశం.flush()
                        while True:
                            반환값=json.loads(ఫైలు_ప్రవేశం.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(గమ్యం_మూల్యం_స్థాయి/'four-terminals.png')).convert('RGB')
            for నిర్దేశాంక_జంట,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(నిర్దేశాంక_జంట)==색상,(నిర్దేశాంక_జంట,화소들.getpixel(నిర్దేశాంక_జంట))
            షెల్('echo FOUR_WINDOWS_OK')
            నిర్ధారణ_నివేదిక.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if డేటా_స్థాయి.poll() is None:డేటా_స్థాయి.terminate()
            try:డేటా_స్థాయి.wait(timeout=5)
            except subprocess.TimeoutExpired:డేటా_స్థాయి.kill();డేటా_స్థాయి.wait()
            సెలక్టర్_a916db4e.close();డేటా_స్థాయి.stdin.close();డేటా_స్థాయి.stdout.close();(గమ్యం_మూల్యం_స్థాయి/'serial.log').write_bytes(లాగ్_వరుస);(గమ్యం_మూల్యం_స్థాయి/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':నడుపుము()
