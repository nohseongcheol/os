#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ක්_රියාත්මක_කරන්න_විධානය import 기준,විධානය

def ක්_රියාත්මක_කරන්න_2():
    목적위치=기준/'build/verification/windows';목적위치.mkdir(parents=True,exist_ok=True)
    වලංගුකරණය_වාර්තාව={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};ලොගය_පේළිය=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(විධානය()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        වරකය_a916db4e=selectors.DefaultSelector();වරකය_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def හසුරුව_සිද්ධිය(초단위=.1):
            for 누름값,_ in වරකය_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ලොගය_පේළිය.extend(둘째값)
            assert b'PANIC:' not in ලොගය_පේළිය and b'HALTED' not in ලොගය_පේළිය,ලොගය_පේළිය[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+초단위
            while 확인표시 not in ලොගය_පේළිය[현재위치:]:
                if time.monotonic()>නිමා_කරන්න_ඕෆ්සෙට් or 자료위치.poll() is not None:raise AssertionError(ලොගය_පේළිය[현재위치:].decode('utf-8','replace'))
                හසුරුව_සිද්ධිය()
            return bytes(ලොගය_පේළිය[현재위치:])
        def ඊමේල්(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ලොගය_පේළිය);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def කවචය(අනුලකුණු_වැල_දත්ත):return ඊමේල්((අනුලකුණු_වැල_දත්ත+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def කෙටිමඟ_අගය(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ක්ලික්_කරන්න_බොත්තම(x_ඛණ්ඩාංකය,세로좌표):return bytes([30,1,1,x_ඛණ්ඩාංකය&255,x_ඛණ්ඩාංකය>>8,세로좌표&255,세로좌표>>8,30,1,0,x_ඛණ්ඩාංකය&255,x_ඛණ්ඩාංකය>>8,세로좌표&255,세로좌표>>8])
        def විධානය_ප්_රකාරය():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+.2
            while time.monotonic()<නිමා_කරන්න_ඕෆ්සෙට්:හසුරුව_සිද්ධිය(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            කවචය('terminal');හසුරුව_සිද්ධිය(.3)
            කවචය('mkdir first; cd first; export NAME=one')
            ඊමේල්('vi 첫째.py\n'.encode(),b'NORMAL')
            ඊමේල්('i값 = 21\nprint(අගය * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+3
            while time.monotonic()<නිමා_කරන්න_ඕෆ්සෙට්:හසුරුව_සිද්ධිය(.1)
            ඊමේල්(කෙටිමඟ_අගය(1),b'TERMINAL FOCUS 2');හසුරුව_සිද්ධිය(.2)
            assert b'/\r\n' in කවචය('pwd')
            කවචය('export NAME=two')
            ඊමේල්('vi 둘째.txt\n'.encode(),b'NORMAL')
            ඊමේල්('i두 번째 කවුළුව\n'.encode(),b'INSERT')
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(180,12),b'TERMINAL FOCUS 1');හසුරුව_සිද්ධිය(.2)
            විධානය_ප්_රකාරය();ඊමේල්(b':wq\r')
            assert b'one:/first' in කවචය('echo "$NAME:$PWD"')
            assert 'අගය = 21\r\nprint(අගය * 2)'.encode() in කවචය('cat 첫째.py')
            결과=කවචය('python 첫째.py');assert b'42\r\n' in 결과,결과
            # Close the first shell with its actual title-bar X; second editor resumes.
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(560,63),b'TERMINAL FOCUS 2');හසුරුව_සිද්ධිය(.2)
            විධානය_ප්_රකාරය();ඊමේල්(b':wq\r')
            assert b'two:/' in කවචය('echo "$NAME:$PWD"')
            assert '두 번째 කවුළුව'.encode() in කවචය('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ඊමේල්('vi 둘째.txt\n'.encode(),b'NORMAL');ඊමේල්(b'xu',b'NORMAL')
            ඊමේල්(b'iX',b'INSERT');විධානය_ප්_රකාරය();ඊමේල්(b':q\r',b'Unsaved')
            ඊමේල්(b':q!\r');assert '두 번째 කවුළුව'.encode() in කවචය('cat 둘째.txt')
            ඊමේල්(කෙටිමඟ_අගය(1),b'TERMINAL FOCUS 1');හසුරුව_සිද්ධිය(.2)
            ඊමේල්(කෙටිමඟ_අගය(1),b'TERMINAL FOCUS 3');හසුරුව_සිද්ධිය(.2)
            ඊමේල්(කෙටිමඟ_අගය(1),b'TERMINAL FOCUS 4');හසුරුව_සිද්ධිය(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            자료위치.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));자료위치.stdin.flush()
            කවචය('echo DRAGGED_OK')
            ඊමේල්('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ඊමේල්('i저장하지 않은 දත්ත'.encode(),b'INSERT')
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(578,97),b'TERMINAL FOCUS 3');හසුරුව_සිද්ධිය(.2)
            assert '버릴문서.txt'.encode() not in කවචය('ls')
            ඊමේල්(කෙටිමඟ_අගය(1),b'TERMINAL FOCUS 4');හසුරුව_සිද්ධිය(.2)
            කවචය('echo REUSED_WINDOW_OK')
            완료량=ලොගය_පේළිය.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+.3
            while time.monotonic()<නිමා_කරන්න_ඕෆ්සෙට්:හසුරුව_සිද්ධිය(.05)
            with socket.socket(socket.AF_UNIX) as අනුලකුණු_කේතය:
                අනුලකුණු_කේතය.settimeout(10);අනුලකුණු_කේතය.connect(str(모의제어접속))
                with අනුලකුණු_කේතය.makefile('rwb') as ගොනුව_පිවිසුම:
                    json.loads(ගොනුව_පිවිසුම.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'four-terminals.png'),'format':'png'}}):
                        ගොනුව_පිවිසුම.write((json.dumps(요청값)+'\n').encode());ගොනුව_පිවිසුම.flush()
                        while True:
                            반환값=json.loads(ගොනුව_පිවිසුම.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(목적위치/'four-terminals.png')).convert('RGB')
            for ඛණ්ඩාංක_යුගලය,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ඛණ්ඩාංක_යුගලය)==색상,(ඛණ්ඩාංක_යුගලය,화소들.getpixel(ඛණ්ඩාංක_යුගලය))
            කවචය('echo FOUR_WINDOWS_OK')
            වලංගුකරණය_වාර්තාව.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            වරකය_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ලොගය_පේළිය);(목적위치/'report.json').write_text(json.dumps(වලංගුකරණය_වාර්තාව,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ක්_රියාත්මක_කරන්න_2()
