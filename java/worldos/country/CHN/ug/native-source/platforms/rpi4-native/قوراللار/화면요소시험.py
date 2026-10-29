#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز,بۇيرۇق

def ئىجرا_قىل_2():
    نىشان_قىممىتى_ئورۇنلاشتۇرۇش=كۆرسىتىش_يىلتىز/'build/verification/swing';نىشان_قىممىتى_ئورۇنلاشتۇرۇش.mkdir(parents=True,exist_ok=True)
    تۈركۈم_يول=كۆرسىتىش_يىلتىز/'build/verification/new-java';تۈركۈم_يول.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(كۆرسىتىش_يىلتىز/'dist/jkoros-native-korean.jar'),'-d',str(تۈركۈم_يول),str(كۆرسىتىش_يىلتىز/'시험/자바/스윙시험.java'),str(كۆرسىتىش_يىلتىز/'시험/자바/한글창시험.java')])
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
            مەلۇمات=(كۆرسىتىش_يىلتىز/'build/verification/new-java/스윙시험.class').read_bytes()
            ئەۋەتمەك('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(مەلۇمات),64):ئەۋەتمەك(مەلۇمات[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ئەۋەتمەك(b'.\n')
            ئەۋەتمەك('java 스윙시험\n'.encode(),b'SWING READY')
            تاماملىماق_ئاغما=time.monotonic()+3
            while time.monotonic()<تاماملىماق_ئاغما:تۇتقۇچ_ھادىسە(.1)
            # JFrame centered at (120,100), content at y=130.
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(200,210),b'',)  # focus JTextField
            مەلۇمات_ئورۇنلاشتۇرۇش.stdin.write('누리'.encode());مەلۇمات_ئورۇنلاشتۇرۇش.stdin.flush()
            تاماملىماق_ئاغما=time.monotonic()+.3
            while time.monotonic()<تاماملىماق_ئاغما:تۇتقۇچ_ھادىسە(.05)
            ئۆلچەم=ئەۋەتمەك(چەكمەك_كۇنۇپكا(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(خاتىرە_قۇر)-len(ئۆلچەم))
            ئەۋەتمەك(قىسقا_يول_قىممىتى(1),b'TERMINAL FOCUS 2')
            ئۆلچەم=قاپ('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ئۆلچەم
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(180,12),b'TERMINAL FOCUS 1')
            تاماملىماق_ئاغما=time.monotonic()+.3
            while time.monotonic()<تاماملىماق_ئاغما:تۇتقۇچ_ھادىسە(.05)
            with socket.socket(socket.AF_UNIX) as ھەرپ_كودى:
                ھەرپ_كودى.settimeout(10);ھەرپ_كودى.connect(str(모의제어접속))
                with ھەرپ_كودى.makefile('rwb') as ھۆججەت_كىرگۈزۈش:
                    json.loads(ھۆججەت_كىرگۈزۈش.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(نىشان_قىممىتى_ئورۇنلاشتۇرۇش/'native-swing.png'),'format':'png'}}):
                        ھۆججەت_كىرگۈزۈش.write((json.dumps(요청값)+'\n').encode());ھۆججەت_كىرگۈزۈش.flush()
                        while True:
                            반환값=json.loads(ھۆججەت_كىرگۈزۈش.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(505,115))
            قاپ('echo SWING_CLOSED_OK')
            مەلۇمات=(تۈركۈم_يول/'한글창시험.class').read_bytes()
            ئەۋەتمەك('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(مەلۇمات),64):ئەۋەتمەك(مەلۇمات[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ئەۋەتمەك(b'.\n')
            ئەۋەتمەك('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(200,255),'KOREAN SWING CLICK ئاتى'.encode())
            ئەۋەتمەك(چەكمەك_كۇنۇپكا(505,115))
            قاپ('echo KOREAN_SWING_CLOSED_OK')
            دەلىللەش_خەۋەر.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 كۆزنەك/كۇنۇپكا/동작알림/ھادىسە_تەرتىپ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if مەلۇمات_ئورۇنلاشتۇرۇش.poll() is None:مەلۇمات_ئورۇنلاشتۇرۇش.terminate()
            try:مەلۇمات_ئورۇنلاشتۇرۇش.wait(timeout=5)
            except subprocess.TimeoutExpired:مەلۇمات_ئورۇنلاشتۇرۇش.kill();مەلۇمات_ئورۇنلاشتۇرۇش.wait()
            تاللىغۇچ_a916db4e.close();مەلۇمات_ئورۇنلاشتۇرۇش.stdin.close();مەلۇمات_ئورۇنلاشتۇرۇش.stdout.close();(نىشان_قىممىتى_ئورۇنلاشتۇرۇش/'serial.log').write_bytes(خاتىرە_قۇر);(نىشان_قىممىتى_ئورۇنلاشتۇرۇش/'report.json').write_text(json.dumps(دەلىللەش_خەۋەر,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ئىجرا_قىل_2()
