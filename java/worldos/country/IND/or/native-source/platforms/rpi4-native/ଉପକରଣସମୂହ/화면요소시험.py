#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍,ନିର୍ଦ୍ଦେଶ

def ଚଳାନ୍ତୁ():
    ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/swing';ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି.mkdir(parents=True,exist_ok=True)
    ଶ୍ରେଣୀ_ପଥ=ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/new-java';ଶ୍ରେଣୀ_ପଥ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'dist/jkoros-native-korean.jar'),'-d',str(ଶ୍ରେଣୀ_ପଥ),str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시험/자바/스윙시험.java'),str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'시험/자바/한글창시험.java')])
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
            ଡାଟା=(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/verification/new-java/스윙시험.class').read_bytes()
            ପଠାନ୍ତୁ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ଡାଟା),64):ପଠାନ୍ତୁ(ଡାଟା[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ପଠାନ୍ତୁ(b'.\n')
            ପଠାନ୍ତୁ('java 스윙시험\n'.encode(),b'SWING READY')
            ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+3
            while time.monotonic()<ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍:ହାଣ୍ଡେଲ୍_ଘଟଣା(.1)
            # JFrame centered at (120,100), content at y=130.
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(200,210),b'',)  # focus JTextField
            ଡାଟା_ସ୍ଥିତି.stdin.write('누리'.encode());ଡାଟା_ସ୍ଥିତି.stdin.flush()
            ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+.3
            while time.monotonic()<ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍:ହାଣ୍ଡେଲ୍_ଘଟଣା(.05)
            ମାପ=ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ଲଗ୍_ଧାଡ଼ି)-len(ମାପ))
            ପଠାନ୍ତୁ(ସର୍ଟକଟ୍_ମୂଲ୍ୟ(1),b'TERMINAL FOCUS 2')
            ମାପ=ଖୋଳ('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ମାପ
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(180,12),b'TERMINAL FOCUS 1')
            ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍=time.monotonic()+.3
            while time.monotonic()<ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍:ହାଣ୍ଡେଲ୍_ଘଟଣା(.05)
            with socket.socket(socket.AF_UNIX) as ବର୍ଣ୍ଣ_କୋଡ଼୍:
                ବର୍ଣ୍ଣ_କୋଡ଼୍.settimeout(10);ବର୍ଣ୍ଣ_କୋଡ଼୍.connect(str(모의제어접속))
                with ବର୍ଣ୍ଣ_କୋଡ଼୍.makefile('rwb') as ଫାଇଲ୍_ଏଣ୍ଟ୍ରି:
                    json.loads(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି/'native-swing.png'),'format':'png'}}):
                        ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.write((json.dumps(요청값)+'\n').encode());ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.flush()
                        while True:
                            반환값=json.loads(ଫାଇଲ୍_ଏଣ୍ଟ୍ରି.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(505,115))
            ଖୋଳ('echo SWING_CLOSED_OK')
            ଡାଟା=(ଶ୍ରେଣୀ_ପଥ/'한글창시험.class').read_bytes()
            ପଠାନ୍ତୁ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ଡାଟା),64):ପଠାନ୍ତୁ(ଡାଟା[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ପଠାନ୍ତୁ(b'.\n')
            ପଠାନ୍ତୁ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(200,255),'KOREAN SWING CLICK ନାମ'.encode())
            ପଠାନ୍ତୁ(କ୍ଲିକ୍_କରିବା_ବଟନ୍(505,115))
            ଖୋଳ('echo KOREAN_SWING_CLOSED_OK')
            ବୈଧକରଣ_ରିପୋର୍ଟ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 ଓ୍ୱିଣ୍ଡୋ/ବଟନ୍/동작알림/ଘଟଣା_ପ୍ରତିଧାଡ଼ି directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ଡାଟା_ସ୍ଥିତି.poll() is None:ଡାଟା_ସ୍ଥିତି.terminate()
            try:ଡାଟା_ସ୍ଥିତି.wait(timeout=5)
            except subprocess.TimeoutExpired:ଡାଟା_ସ୍ଥିତି.kill();ଡାଟା_ସ୍ଥିତି.wait()
            ଚୟନକାରୀ_a916db4e.close();ଡାଟା_ସ୍ଥିତି.stdin.close();ଡାଟା_ସ୍ଥିତି.stdout.close();(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି/'serial.log').write_bytes(ଲଗ୍_ଧାଡ଼ି);(ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ_ସ୍ଥିତି/'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ଚଳାନ୍ତୁ()
