#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز,بۇيرۇق

def ئىجرا_قىل_2():
    نىشان_قىممىتى_ئورۇنلاشتۇرۇش=كۆرسىتىش_يىلتىز/'build/verification/windows';نىشان_قىممىتى_ئورۇنلاشتۇرۇش.mkdir(parents=True,exist_ok=True)
    دەلىللەش_خەۋەر={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((كۆرسىتىش_يىلتىز/'build/kernel8.img').read_bytes()).hexdigest()};خاتىرە_قۇر=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        مەلۇمات_ئورۇنلاشتۇرۇش=subprocess.Popen(بۇيرۇق()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        تاللىغۇچ_a916db4e=selectors.DefaultSelector();تاللىغۇچ_a916db4e.register(مەلۇمات_ئورۇنلاشتۇرۇش.stdout,selectors.EVENT_READ)
        def تۇتقۇچ_ھادىسە(초단위=.1):
            for 누름값,_ in تاللىغۇچ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:خاتىرە_قۇر.extend(둘째값)
            assert b'PANIC:' not in خاتىرە_قۇر and b'HALTED' not in خاتىرە_قۇر,خاتىرە_قۇر[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            تاماملىماق_ئاغما=time.monotonic()+초단위
            while 확인표시 not in خاتىرە_قۇر[현재위치:]:
                if time.monotonic()>تاماملىماق_ئاغما or مەلۇمات_ئورۇنلاشتۇرۇش.poll() is not None:raise AssertionError(خاتىرە_قۇر[현재위치:].decode('utf-8','replace'))
                تۇتقۇچ_ھادىسە()
            return bytes(خاتىرە_قۇر[현재위치:])
        def ئەۋەتمەك(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(خاتىرە_قۇر);مەلۇمات_ئورۇنلاشتۇرۇش.stdin.write(둘째값);مەلۇمات_ئورۇنلاشتۇرۇش.stdin.flush();return 기다리기(확인표시,현재위치)
        def قاپ(ھەرپ_تىزمىسى_مەلۇمات):return ئەۋەتمەك((ھەرپ_تىزمىسى_مەلۇمات+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def قىسقا_يول_قىممىتى(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def چەكمەك_كۇنۇپكا(x_كوردىنات,세로좌표):return bytes([30,1,1,x_كوردىنات&255,x_كوردىنات>>8,세로좌표&255,세로좌표>>8,30,1,0,x_كوردىنات&255,x_كوردىنات>>8,세로좌표&255,세로좌표>>8])
        def بۇيرۇق_ھالەت():
            مەلۇمات_ئورۇنلاشتۇرۇش.stdin.write(b'\x1b');مەلۇمات_ئورۇنلاشتۇرۇش.stdin.flush();تاماملىماق_ئاغما=time.monotonic()+.2
            while time.monotonic()<تاماملىماق_ئاغما:تۇتقۇچ_ھادىسە(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            قاپ('terminal');تۇتقۇچ_ھادىسە(.3)
            قاپ('mkdir first; cd first; export NAME=one')
            ئەۋەتمەك('vi 첫째.py\n'.encode(),b'NORMAL')
            ئەۋەتمەك('i값 = 21\nprint(قىممىتى * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            تاماملىماق_ئاغما=time.monotonic()+3
            while time.monotonic()<تاماملىماق_ئاغما:تۇتقۇچ_ھادىسە(.1)
            ئەۋەتمەك(قىسقا_يول_قىممىتى(1),b'TERMINAL FOCUS 2');تۇتقۇچ_ھادىسە(.2)
            assert b'/\r\n' in قاپ('pwd')
            قاپ('export NAME=two')
            ئەۋەتمەك('vi 둘째.txt\n'.encode(),b'NORMAL')
            ئەۋەتمەك('i두 번째 كۆزنەك\n'.encode(),b'INSERT')
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(180,12),b'TERMINAL FOCUS 1');تۇتقۇچ_ھادىسە(.2)
            بۇيرۇق_ھالەت();ئەۋەتمەك(b':wq\r')
            assert b'one:/first' in قاپ('echo "$NAME:$PWD"')
            assert 'قىممىتى = 21\r\nprint(قىممىتى * 2)'.encode() in قاپ('cat 첫째.py')
            ئۆلچەم=قاپ('python 첫째.py');assert b'42\r\n' in ئۆلچەم,ئۆلچەم
            # Close the first shell with its actual title-bar X; second editor resumes.
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(560,63),b'TERMINAL FOCUS 2');تۇتقۇچ_ھادىسە(.2)
            بۇيرۇق_ھالەت();ئەۋەتمەك(b':wq\r')
            assert b'two:/' in قاپ('echo "$NAME:$PWD"')
            assert '두 번째 كۆزنەك'.encode() in قاپ('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ئەۋەتمەك('vi 둘째.txt\n'.encode(),b'NORMAL');ئەۋەتمەك(b'xu',b'NORMAL')
            ئەۋەتمەك(b'iX',b'INSERT');بۇيرۇق_ھالەت();ئەۋەتمەك(b':q\r',b'Unsaved')
            ئەۋەتمەك(b':q!\r');assert '두 번째 كۆزنەك'.encode() in قاپ('cat 둘째.txt')
            ئەۋەتمەك(قىسقا_يول_قىممىتى(1),b'TERMINAL FOCUS 1');تۇتقۇچ_ھادىسە(.2)
            ئەۋەتمەك(قىسقا_يول_قىممىتى(1),b'TERMINAL FOCUS 3');تۇتقۇچ_ھادىسە(.2)
            ئەۋەتمەك(قىسقا_يول_قىممىتى(1),b'TERMINAL FOCUS 4');تۇتقۇچ_ھادىسە(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            مەلۇمات_ئورۇنلاشتۇرۇش.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));مەلۇمات_ئورۇنلاشتۇرۇش.stdin.flush()
            قاپ('echo DRAGGED_OK')
            ئەۋەتمەك('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ئەۋەتمەك('i저장하지 않은 مەلۇمات'.encode(),b'INSERT')
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(578,97),b'TERMINAL FOCUS 3');تۇتقۇچ_ھادىسە(.2)
            assert '버릴문서.txt'.encode() not in قاپ('ls')
            ئەۋەتمەك(قىسقا_يول_قىممىتى(1),b'TERMINAL FOCUS 4');تۇتقۇچ_ھادىسە(.2)
            قاپ('echo REUSED_WINDOW_OK')
            완료량=خاتىرە_قۇر.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            تاماملىماق_ئاغما=time.monotonic()+.3
            while time.monotonic()<تاماملىماق_ئاغما:تۇتقۇچ_ھادىسە(.05)
            with socket.socket(socket.AF_UNIX) as ھەرپ_كودى:
                ھەرپ_كودى.settimeout(10);ھەرپ_كودى.connect(str(모의제어접속))
                with ھەرپ_كودى.makefile('rwb') as ھۆججەت_كىرگۈزۈش:
                    json.loads(ھۆججەت_كىرگۈزۈش.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(نىشان_قىممىتى_ئورۇنلاشتۇرۇش/'four-terminals.png'),'format':'png'}}):
                        ھۆججەت_كىرگۈزۈش.write((json.dumps(요청값)+'\n').encode());ھۆججەت_كىرگۈزۈش.flush()
                        while True:
                            반환값=json.loads(ھۆججەت_كىرگۈزۈش.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(نىشان_قىممىتى_ئورۇنلاشتۇرۇش/'four-terminals.png')).convert('RGB')
            for جۈپ_كوردىنات,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(جۈپ_كوردىنات)==색상,(جۈپ_كوردىنات,화소들.getpixel(جۈپ_كوردىنات))
            قاپ('echo FOUR_WINDOWS_OK')
            دەلىللەش_خەۋەر.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if مەلۇمات_ئورۇنلاشتۇرۇش.poll() is None:مەلۇمات_ئورۇنلاشتۇرۇش.terminate()
            try:مەلۇمات_ئورۇنلاشتۇرۇش.wait(timeout=5)
            except subprocess.TimeoutExpired:مەلۇمات_ئورۇنلاشتۇرۇش.kill();مەلۇمات_ئورۇنلاشتۇرۇش.wait()
            تاللىغۇچ_a916db4e.close();مەلۇمات_ئورۇنلاشتۇرۇش.stdin.close();مەلۇمات_ئورۇنلاشتۇرۇش.stdout.close();(نىشان_قىممىتى_ئورۇنلاشتۇرۇش/'serial.log').write_bytes(خاتىرە_قۇر);(نىشان_قىممىتى_ئورۇنلاشتۇرۇش/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ئىجرا_قىل_2()
