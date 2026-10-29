#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍,ନିର୍ଦ୍ଦେଶ

def ଚଳାନ୍ତୁ():
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/windows';ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି.mkdir(parents=True,exist_ok=True)
    ବୈଧକରଣ_ରିପୋର୍ଟ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/kernel8.img').read_bytes()).hexdigest()};ଲଗ୍_ଧାଡ଼ି=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ଡାଟା_ସ୍ଥିତି=subprocess.Popen(ନିର୍ଦ୍ଦେଶ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ଚୟନକାରୀ_a916db4e=selectors.DefaultSelector();ଚୟନକାରୀ_a916db4e.register(ଡାଟା_ସ୍ଥିତି.stdout,selectors.EVENT_READ)
        def ହାଣ୍ଡେଲ୍_ଘଟଣା(초단위=.1):
            for 누름값,_ in ଚୟନକାରୀ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ଲଗ୍_ଧାଡ଼ି.extend(둘째값)
            assert b'PANIC:' not in ଲଗ୍_ଧାଡ଼ି and b'HALTED' not in ଲଗ୍_ଧାଡ଼ି,ଲଗ୍_ଧାଡ଼ି[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+초단위
            while 확인표시 not in ଲଗ୍_ଧାଡ଼ି[현재위치:]:
                if time.monotonic()>ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍ or ଡାଟା_ସ୍ଥିତି.poll() is not None:raise AssertionError(ଲଗ୍_ଧାଡ଼ି[현재위치:].decode('utf-8','replace'))
                ହାଣ୍ଡେଲ୍_ଘଟଣା()
            return bytes(ଲଗ୍_ଧାଡ଼ି[현재위치:])
        def ପଠାନ୍ତୁ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ଲଗ୍_ଧାଡ଼ି);ଡାଟା_ସ୍ଥିତି.stdin.write(둘째값);ଡାଟା_ସ୍ଥିତି.stdin.flush();return 기다리기(확인표시,현재위치)
        def ଖୋଳ(ଷ୍ଟ୍ରିଂ_ଡାଟା):return ପଠାନ୍ତୁ((ଷ୍ଟ୍ରିଂ_ଡାଟା+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ସର୍ଟକଟ୍_ମୂଲ୍ୟ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def କ୍ଲିକ୍_କରିବା_ବଟନ୍(x_ସଂଯୋଜନ,세로좌표):return bytes([30,1,1,x_ସଂଯୋଜନ&255,x_ସଂଯୋଜନ>>8,세로좌표&255,세로좌표>>8,30,1,0,x_ସଂଯୋଜନ&255,x_ସଂଯୋଜନ>>8,세로좌표&255,세로좌표>>8])
        def ନିର୍ଦ୍ଦେଶ_ମୋଡ୍():
            ଡାଟା_ସ୍ଥିତି.stdin.write(b'\x1b');ଡାଟା_ସ୍ଥିତି.stdin.flush();ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+.2
            while time.monotonic()<ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍:ହାଣ୍ଡେଲ୍_ଘଟଣା(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ଖୋଳ('terminal');ହାଣ୍ଡେଲ୍_ଘଟଣା(.3)
            ଖୋଳ('mkdir first; cd first; export NAME=one')
            ପଠାନ୍ତୁ('vi 첫째.py\n'.encode(),b'NORMAL')
            ପଠାନ୍ତୁ('i값 = 21\nprint(ମୂଲ୍ୟ * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+3
            while time.monotonic()<ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍:ହାଣ୍ଡେଲ୍_ଘଟଣା(.1)
            ପଠାନ୍ତୁ(ସର୍ଟକଟ୍_ମୂଲ୍ୟ(1),b'TERMINAL FOCUS 2');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            assert b'/\r\n' in ଖୋଳ('pwd')
            ଖୋଳ('export NAME=two')
            ପଠାନ୍ତୁ('vi 둘째.txt\n'.encode(),b'NORMAL')
            ପଠାନ୍ତୁ('i두 번째 ଓ୍ୱିଣ୍ଡୋ\n'.encode(),b'INSERT')
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(180,12),b'TERMINAL FOCUS 1');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            ନିର୍ଦ୍ଦେଶ_ମୋଡ୍();ପଠାନ୍ତୁ(b':wq\r')
            assert b'one:/first' in ଖୋଳ('echo "$NAME:$PWD"')
            assert 'ମୂଲ୍ୟ = 21\r\nprint(ମୂଲ୍ୟ * 2)'.encode() in ଖୋଳ('cat 첫째.py')
            ମାପ=ଖୋଳ('python 첫째.py');assert b'42\r\n' in ମାପ,ମାପ
            # Close the first shell with its actual title-bar X; second editor resumes.
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(560,63),b'TERMINAL FOCUS 2');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            ନିର୍ଦ୍ଦେଶ_ମୋଡ୍();ପଠାନ୍ତୁ(b':wq\r')
            assert b'two:/' in ଖୋଳ('echo "$NAME:$PWD"')
            assert '두 번째 ଓ୍ୱିଣ୍ଡୋ'.encode() in ଖୋଳ('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            ପଠାନ୍ତୁ('vi 둘째.txt\n'.encode(),b'NORMAL');ପଠାନ୍ତୁ(b'xu',b'NORMAL')
            ପଠାନ୍ତୁ(b'iX',b'INSERT');ନିର୍ଦ୍ଦେଶ_ମୋଡ୍();ପଠାନ୍ତୁ(b':q\r',b'Unsaved')
            ପଠାନ୍ତୁ(b':q!\r');assert '두 번째 ଓ୍ୱିଣ୍ଡୋ'.encode() in ଖୋଳ('cat 둘째.txt')
            ପଠାନ୍ତୁ(ସର୍ଟକଟ୍_ମୂଲ୍ୟ(1),b'TERMINAL FOCUS 1');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            ପଠାନ୍ତୁ(ସର୍ଟକଟ୍_ମୂଲ୍ୟ(1),b'TERMINAL FOCUS 3');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            ପଠାନ୍ତୁ(ସର୍ଟକଟ୍_ମୂଲ୍ୟ(1),b'TERMINAL FOCUS 4');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            ଡାଟା_ସ୍ଥିତି.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));ଡାଟା_ସ୍ଥିତି.stdin.flush()
            ଖୋଳ('echo DRAGGED_OK')
            ପଠାନ୍ତୁ('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            ପଠାନ୍ତୁ('i저장하지 않은 ଡାଟା'.encode(),b'INSERT')
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(578,97),b'TERMINAL FOCUS 3');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            assert '버릴문서.txt'.encode() not in ଖୋଳ('ls')
            ପଠାନ୍ତୁ(ସର୍ଟକଟ୍_ମୂଲ୍ୟ(1),b'TERMINAL FOCUS 4');ହାଣ୍ଡେଲ୍_ଘଟଣା(.2)
            ଖୋଳ('echo REUSED_WINDOW_OK')
            완료량=ଲଗ୍_ଧାଡ଼ି.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',완료량)
            # UART completion precedes the next QEMU display refresh.
            ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+.3
            while time.monotonic()<ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍:ହାଣ୍ଡେଲ୍_ଘଟଣା(.05)
            with socket.socket(socket.AF_UNIX) as ବର୍ଣ୍ଣ_କୋଡ଼୍:
                ବର୍ଣ୍ଣ_କୋଡ଼୍.settimeout(10);ବର୍ଣ୍ଣ_କୋଡ଼୍.connect(str(모의제어접속))
                with ବର୍ଣ୍ଣ_କୋଡ଼୍.makefile('rwb') as ଫାଇଲ୍_ଏଣ୍ଟ୍ରି:
                    json.loads(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି/'four-terminals.png'),'format':'png'}}):
                        ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.write((json.dumps(요청값)+'\n').encode());ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.flush()
                        while True:
                            반환값=json.loads(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି/'four-terminals.png')).convert('RGB')
            for ସଂଯୋଜନ_ଯୁଗ୍ମ,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ସଂଯୋଜନ_ଯୁଗ୍ମ)==색상,(ସଂଯୋଜନ_ଯୁଗ୍ମ,화소들.getpixel(ସଂଯୋଜନ_ଯୁଗ୍ମ))
            ଖୋଳ('echo FOUR_WINDOWS_OK')
            ବୈଧକରଣ_ରିପୋର୍ଟ.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if ଡାଟା_ସ୍ଥିତି.poll() is None:ଡାଟା_ସ୍ଥିତି.terminate()
            try:ଡାଟା_ସ୍ଥିତି.wait(timeout=5)
            except subprocess.TimeoutExpired:ଡାଟା_ସ୍ଥିତି.kill();ଡାଟା_ସ୍ଥିତି.wait()
            ଚୟନକାରୀ_a916db4e.close();ଡାଟା_ସ୍ଥିତି.stdin.close();ଡାଟା_ସ୍ଥିତି.stdout.close();(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି/'serial.log').write_bytes(ଲଗ୍_ଧାଡ଼ି);(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ଚଳାନ୍ତୁ()
