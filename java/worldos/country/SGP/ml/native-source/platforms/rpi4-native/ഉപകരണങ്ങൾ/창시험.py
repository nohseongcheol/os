#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം,ആജ്ഞ

def നടപ്പിലാക്കുക():
    ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി=പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/verification/windows';ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി.mkdir(parents=True,exist_ok=True)
    నిర్ధారణ_నివేదిక={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം/'build/kernel8.img').read_bytes()).hexdigest()};ലോഗ്_രേഖ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ഡാറ്റാ_പദവി=subprocess.Popen(ആജ്ഞ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        సెలక్టర్_a916db4e=selectors.DefaultSelector();సెలక్టర్_a916db4e.register(ഡാറ്റാ_പദവി.stdout,selectors.EVENT_READ)
        def കൈകാര്യംചെയ്യല്_ഇവന്റ്(초단위=.1):
            for 누름값,_ in సెలక్టర్_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ലോഗ്_രേഖ.extend(둘째값)
            assert b'PANIC:' not in ലോഗ്_രേഖ and b'HALTED' not in ലോഗ്_രേഖ,ലോഗ്_രേഖ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+초단위
            while 확인표시 not in ലോഗ്_രേഖ[현재위치:]:
                if time.monotonic()>അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ് or ഡാറ്റാ_പദവി.poll() is not None:raise AssertionError(ലോഗ്_രേഖ[현재위치:].decode('utf-8','replace'))
                കൈകാര്യംചെയ്യല്_ഇവന്റ്()
            return bytes(ലോഗ്_രേഖ[현재위치:])
        def അയയ്ക്കുക(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ലോഗ്_രേഖ);ഡാറ്റാ_പദവി.stdin.write(둘째값);ഡാറ്റാ_പദവി.stdin.flush();return 기다리기(확인표시,현재위치)
        def ഷെല്(സ്ട്രിംഗ്_ഡാറ്റാ):return അയയ്ക്കുക((സ്ട്രിംഗ്_ഡാറ്റാ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def എളുപ്പവഴി_മൂല്യം(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(x_ഏകോപനം,Y_ബട്ടൺ_ഏകോപനം):return bytes([30,1,1,x_ഏകോപനം&255,x_ഏകോപനം>>8,Y_ബട്ടൺ_ഏകോപനം&255,Y_ബട്ടൺ_ഏകോപനം>>8,30,1,0,x_ഏകോപനം&255,x_ഏകോപനം>>8,Y_ബട്ടൺ_ഏകോപനം&255,Y_ബട്ടൺ_ഏകോപനം>>8])
        def കമാന്_ഡ്_മോഡ്():
            ഡാറ്റാ_പദവി.stdin.write(b'\x1b');ഡാറ്റാ_പദവി.stdin.flush();അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+.2
            while time.monotonic()<അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്:കൈകാര്യംചെയ്യല്_ഇവന്റ്(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ഷെല്('terminal');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.3)
            ഷെല്('mkdir first; cd first; export NAME=one')
            അയയ്ക്കുക('vi 첫째.py\n'.encode(),b'NORMAL')
            അയയ്ക്കുക('i값 = 21\nprint(മൂല്യം * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+3
            while time.monotonic()<അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്:കൈകാര്യംചെയ്യല്_ഇവന്റ്(.1)
            അയയ്ക്കുക(എളുപ്പവഴി_മൂല്യം(1),b'TERMINAL FOCUS 2');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            assert b'/\r\n' in ഷെല്('pwd')
            ഷെല്('export NAME=two')
            അയയ്ക്കുക('vi 둘째.txt\n'.encode(),b'NORMAL')
            അയയ്ക്കുക('i두 번째 ജാലകം\n'.encode(),b'INSERT')
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(180,12),b'TERMINAL FOCUS 1');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            കമാന്_ഡ്_മോഡ്();അയയ്ക്കുക(b':wq\r')
            assert b'one:/first' in ഷെല്('echo "$NAME:$PWD"')
            assert 'മൂല്യം = 21\r\nprint(മൂല്യം * 2)'.encode() in ഷെല്('cat 첫째.py')
            അളവ്=ഷെല്('python 첫째.py');assert b'42\r\n' in അളവ്,അളവ്
            # Close the first shell with its actual title-bar X; second editor resumes.
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(560,63),b'TERMINAL FOCUS 2');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            കമാന്_ഡ്_മോഡ്();അയയ്ക്കുക(b':wq\r')
            assert b'two:/' in ഷെല്('echo "$NAME:$PWD"')
            assert '두 번째 ജാലകം'.encode() in ഷെല്('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            അയയ്ക്കുക('vi 둘째.txt\n'.encode(),b'NORMAL');അയയ്ക്കുക(b'xu',b'NORMAL')
            അയയ്ക്കുക(b'iX',b'INSERT');കമാന്_ഡ്_മോഡ്();അയയ്ക്കുക(b':q\r',b'Unsaved')
            അയയ്ക്കുക(b':q!\r');assert '두 번째 ജാലകം'.encode() in ഷെല്('cat 둘째.txt')
            അയയ്ക്കുക(എളുപ്പവഴി_മൂല്യം(1),b'TERMINAL FOCUS 1');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            അയയ്ക്കുക(എളുപ്പവഴി_മൂല്യം(1),b'TERMINAL FOCUS 3');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            അയയ്ക്കുക(എളുപ്പവഴി_മൂല്യം(1),b'TERMINAL FOCUS 4');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ഡാറ്റാ_പദവി.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ഡാറ്റാ_പദവി.stdin.flush()
            ഷെല്('echo DRAGGED_OK')
            അയയ്ക്കുക('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            അയയ്ക്കുക('i저장하지 않은 ഡാറ്റാ'.encode(),b'INSERT')
            അയയ്ക്കുക(ക്ലിക്ക്_ചെയ്യുക_ബട്ടണ്(578,97),b'TERMINAL FOCUS 3');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            assert '버릴문서.txt'.encode() not in ഷെല്('ls')
            അയയ്ക്കുക(എളുപ്പവഴി_മൂല്യം(1),b'TERMINAL FOCUS 4');കൈകാര്യംചെയ്യല്_ഇവന്റ്(.2)
            ഷെല്('echo REUSED_WINDOW_OK')
            완료량=ലോഗ്_രേഖ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്=time.monotonic()+.3
            while time.monotonic()<അവസാനിപ്പിക്കുക_ഓഫ്_സെറ്റ്:കൈകാര്യംചെയ്യല്_ഇവന്റ്(.05)
            with socket.socket(socket.AF_UNIX) as പ്രതീകകോഡ്:
                പ്രതീകകോഡ്.settimeout(10);പ്രതീകകോഡ്.connect(str(모의제어접속))
                with പ്രതീകകോഡ്.makefile('rwb') as ഫയല്_എന്_ട്രി:
                    json.loads(ഫയല്_എന്_ട്രി.readline())
                    for HTTP_അപേക്ഷ_മൂല്യം in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി/'four-terminals.png'),'format':'png'}}):
                        ഫയല്_എന്_ട്രി.write((json.dumps(HTTP_അപേക്ഷ_മൂല്യം)+'\n').encode());ഫയല്_എന്_ട്രി.flush()
                        while True:
                            반환값=json.loads(ഫയല്_എന്_ട്രി.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി/'four-terminals.png')).convert('RGB')
            for കോര്_ഡിനേറ്റ്_പെയര്,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(കോര്_ഡിനേറ്റ്_പെയര്)==색상,(കോര്_ഡിനേറ്റ്_പെയര്,화소들.getpixel(കോര്_ഡിനേറ്റ്_പെയര്))
            ഷെല്('echo FOUR_WINDOWS_OK')
            నిర్ధారణ_నివేదిక.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ഡാറ്റാ_പദവി.poll() is None:ഡാറ്റാ_പദവി.terminate()
            try:ഡാറ്റാ_പദവി.wait(timeout=5)
            except subprocess.TimeoutExpired:ഡാറ്റാ_പദവി.kill();ഡാറ്റാ_പദവി.wait()
            సెలక్టర్_a916db4e.close();ഡാറ്റാ_പദവി.stdin.close();ഡാറ്റാ_പദവി.stdout.close();(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി/'serial.log').write_bytes(ലോഗ്_രേഖ);(ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം_പദവി/'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':നടപ്പിലാക്കുക()
