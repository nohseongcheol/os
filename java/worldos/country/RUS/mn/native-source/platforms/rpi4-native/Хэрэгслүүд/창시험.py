#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Гүйцэтгэх_команд import 기준,Тушаал

def Ажиллуулах():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    баталгаажуулалт_тайлан={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};бичих_мөр_6e8b375a=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Тушаал()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        сонгогч_a916db4e=selectors.DefaultSelector();сонгогч_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def барих_үйлдэл(초단위=.1):
            for 누름값,_ in сонгогч_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:бичих_мөр_6e8b375a.extend(둘째값)
            assert b'PANIC:' not in бичих_мөр_6e8b375a and b'HALTED' not in бичих_мөр_6e8b375a,бичих_мөр_6e8b375a[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            дуусгах_Оффсет=time.monotonic()+초단위
            while 확인표시 not in бичих_мөр_6e8b375a[현재위치:]:
                if time.monotonic()>дуусгах_Оффсет or 자료위치.poll() is not None:raise AssertionError(бичих_мөр_6e8b375a[현재위치:].decode('utf-8','replace'))
                барих_үйлдэл()
            return bytes(бичих_мөр_6e8b375a[현재위치:])
        def илгээх(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(бичих_мөр_6e8b375a);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def бүрхүүл(мөр_өгөгдөл):return илгээх((мөр_өгөгдөл+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def файлын_холбоос_утга(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def товших_товч(х_координат,세로좌표):return bytes([30,1,1,х_координат&255,х_координат>>8,세로좌표&255,세로좌표>>8,30,1,0,х_координат&255,х_координат>>8,세로좌표&255,세로좌표>>8])
        def команд_горим():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();дуусгах_Оффсет=time.monotonic()+.2
            while time.monotonic()<дуусгах_Оффсет:барих_үйлдэл(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            бүрхүүл('terminal');барих_үйлдэл(.3)
            бүрхүүл('mkdir first; cd first; export NAME=one')
            илгээх('vi 첫째.py\n'.encode(),b'NORMAL')
            илгээх('i값 = 21\nprint(утга * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            дуусгах_Оффсет=time.monotonic()+3
            while time.monotonic()<дуусгах_Оффсет:барих_үйлдэл(.1)
            илгээх(файлын_холбоос_утга(1),b'TERMINAL FOCUS 2');барих_үйлдэл(.2)
            assert b'/\r\n' in бүрхүүл('pwd')
            бүрхүүл('export NAME=two')
            илгээх('vi 둘째.txt\n'.encode(),b'NORMAL')
            илгээх('i두 번째 цонх\n'.encode(),b'INSERT')
            илгээх(товших_товч(180,12),b'TERMINAL FOCUS 1');барих_үйлдэл(.2)
            команд_горим();илгээх(b':wq\r')
            assert b'one:/first' in бүрхүүл('echo "$NAME:$PWD"')
            assert 'утга = 21\r\nprint(утга * 2)'.encode() in бүрхүүл('cat 첫째.py')
            결과=бүрхүүл('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            илгээх(товших_товч(560,63),b'TERMINAL FOCUS 2');барих_үйлдэл(.2)
            команд_горим();илгээх(b':wq\r')
            assert b'two:/' in бүрхүүл('echo "$NAME:$PWD"')
            assert '두 번째 цонх'.encode() in бүрхүүл('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            илгээх('vi 둘째.txt\n'.encode(),b'NORMAL');илгээх(b'xu',b'NORMAL')
            илгээх(b'iX',b'INSERT');команд_горим();илгээх(b':q\r',b'Unsaved')
            илгээх(b':q!\r');assert '두 번째 цонх'.encode() in бүрхүүл('cat 둘째.txt')
            илгээх(файлын_холбоос_утга(1),b'TERMINAL FOCUS 1');барих_үйлдэл(.2)
            илгээх(файлын_холбоос_утга(1),b'TERMINAL FOCUS 3');барих_үйлдэл(.2)
            илгээх(файлын_холбоос_утга(1),b'TERMINAL FOCUS 4');барих_үйлдэл(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            бүрхүүл('echo DRAGGED_OK')
            илгээх('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            илгээх('i저장하지 않은 өгөгдөл'.encode(),b'INSERT')
            илгээх(товших_товч(578,97),b'TERMINAL FOCUS 3');барих_үйлдэл(.2)
            assert '버릴문서.txt'.encode() not in бүрхүүл('ls')
            илгээх(файлын_холбоос_утга(1),b'TERMINAL FOCUS 4');барих_үйлдэл(.2)
            бүрхүүл('echo REUSED_WINDOW_OK')
            완료량=бичих_мөр_6e8b375a.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            дуусгах_Оффсет=time.monotonic()+.3
            while time.monotonic()<дуусгах_Оффсет:барих_үйлдэл(.05)
            with socket.socket(socket.AF_UNIX) as тэмдэгтийн_код:
                тэмдэгтийн_код.settimeout(10);тэмдэгтийн_код.connect(str(모의제어접속))
                with тэмдэгтийн_код.makefile('rwb') as файл_оролт:
                    json.loads(файл_оролт.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        файл_оролт.write((json.dumps(요청값)+'\n').encode());файл_оролт.flush()
                        while True:
                            반환값=json.loads(файл_оролт.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for координатын_хослол,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(координатын_хослол)==색상,(координатын_хослол,화소들.getpixel(координатын_хослол))
            бүрхүүл('echo FOUR_WINDOWS_OK')
            баталгаажуулалт_тайлан.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            сонгогч_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(бичих_мөр_6e8b375a);(목적위치/'report.json').write_text(json.dumps(баталгаажуулалт_тайлан,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Ажиллуулах()
