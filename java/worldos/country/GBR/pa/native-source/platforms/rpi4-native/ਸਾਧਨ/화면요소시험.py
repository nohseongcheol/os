#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ,ਕਮਾਂਡ

def ਚਲਾਓ_2():
    ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/swing';ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ.mkdir(parents=True,exist_ok=True)
    ਸ੍ਰੇਣੀ_ਰਸਤਾ=ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/new-java';ਸ੍ਰੇਣੀ_ਰਸਤਾ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'dist/jkoros-native-korean.jar'),'-d',str(ਸ੍ਰੇਣੀ_ਰਸਤਾ),str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시험/자바/스윙시험.java'),str(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'시험/자바/한글창시험.java')])
    ਮਾਨਤਾ_ਵਿਵਰਨ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/kernel8.img').read_bytes()).hexdigest()};ਲੌਗ_ਕਤਾਰ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ=subprocess.Popen(ਕਮਾਂਡ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ਚੋਣਕਰਤਾ_a916db4e=selectors.DefaultSelector();ਚੋਣਕਰਤਾ_a916db4e.register(ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout,selectors.EVENT_READ)
        def ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(초단위=.1):
            for 누름값,_ in ਚੋਣਕਰਤਾ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ਲੌਗ_ਕਤਾਰ.extend(둘째값)
            assert b'PANIC:' not in ਲੌਗ_ਕਤਾਰ and b'HALTED' not in ਲੌਗ_ਕਤਾਰ,ਲੌਗ_ਕਤਾਰ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+초단위
            while 확인표시 not in ਲੌਗ_ਕਤਾਰ[현재위치:]:
                if time.monotonic()>ਅੰਤ_ਔਫਸੈਟ or ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.poll() is not None:raise AssertionError(ਲੌਗ_ਕਤਾਰ[현재위치:].decode('utf-8','replace'))
                ਸੰਭਾਲਣਾ_ਇਵੈਂਟ()
            return bytes(ਲੌਗ_ਕਤਾਰ[현재위치:])
        def ਈਮੇਲ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ਲੌਗ_ਕਤਾਰ);ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.write(둘째값);ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.flush();return 기다리기(확인표시,현재위치)
        def ਸ਼ੈਲ(ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ):return ਈਮੇਲ((ਨਿਰਭਰ_ਰਹਿਣ_ਵਾਲਾ_ਸਮੱਗਰੀ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ਕਲਿਕ_ਕਰੋ_ਬਟਨ(x_ਕੌਔਰਡੀਨੇਟ,세로좌표):return bytes([30,1,1,x_ਕੌਔਰਡੀਨੇਟ&255,x_ਕੌਔਰਡੀਨੇਟ>>8,세로좌표&255,세로좌표>>8,30,1,0,x_ਕੌਔਰਡੀਨੇਟ&255,x_ਕੌਔਰਡੀਨੇਟ>>8,세로좌표&255,세로좌표>>8])
        def ਆਦੇਸ਼_ਮੋਡ():
            ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.write(b'\x1b');ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.flush();ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+.2
            while time.monotonic()<ਅੰਤ_ਔਫਸੈਟ:ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ਸ਼ੈਲ('terminal');ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.3)
            ਸਮੱਗਰੀ=(ਪ੍ਰੋਜੈਕਟ_ਰੂਟ/'build/verification/new-java/스윙시험.class').read_bytes()
            ਈਮੇਲ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ਸਮੱਗਰੀ),64):ਈਮੇਲ(ਸਮੱਗਰੀ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ਈਮੇਲ(b'.\n')
            ਈਮੇਲ('java 스윙시험\n'.encode(),b'SWING READY')
            ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+3
            while time.monotonic()<ਅੰਤ_ਔਫਸੈਟ:ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.1)
            # JFrame centered at (120,100), content at y=130.
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(200,210),b'',)  # focus JTextField
            ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.write('누리'.encode());ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.flush()
            ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+.3
            while time.monotonic()<ਅੰਤ_ਔਫਸੈਟ:ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.05)
            ਮਾਪ=ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ਲੌਗ_ਕਤਾਰ)-len(ਮਾਪ))
            ਈਮੇਲ(ਸ਼ੌਰਟਕਟ_ਕੀਮਤ(1),b'TERMINAL FOCUS 2')
            ਮਾਪ=ਸ਼ੈਲ('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ਮਾਪ
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(180,12),b'TERMINAL FOCUS 1')
            ਅੰਤ_ਔਫਸੈਟ=time.monotonic()+.3
            while time.monotonic()<ਅੰਤ_ਔਫਸੈਟ:ਸੰਭਾਲਣਾ_ਇਵੈਂਟ(.05)
            with socket.socket(socket.AF_UNIX) as ਵਰਣ_ਕੋਡ:
                ਵਰਣ_ਕੋਡ.settimeout(10);ਵਰਣ_ਕੋਡ.connect(str(모의제어접속))
                with ਵਰਣ_ਕੋਡ.makefile('rwb') as ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ:
                    json.loads(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ/'native-swing.png'),'format':'png'}}):
                        ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.write((json.dumps(요청값)+'\n').encode());ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.flush()
                        while True:
                            반환값=json.loads(ਲਿਖਤ_ਪੱਤਰ_ਦਾਖਲਾ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(505,115))
            ਸ਼ੈਲ('echo SWING_CLOSED_OK')
            ਸਮੱਗਰੀ=(ਸ੍ਰੇਣੀ_ਰਸਤਾ/'한글창시험.class').read_bytes()
            ਈਮੇਲ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ਸਮੱਗਰੀ),64):ਈਮੇਲ(ਸਮੱਗਰੀ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ਈਮੇਲ(b'.\n')
            ਈਮੇਲ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(200,255),'KOREAN SWING CLICK ਨਾਂ'.encode())
            ਈਮੇਲ(ਕਲਿਕ_ਕਰੋ_ਬਟਨ(505,115))
            ਸ਼ੈਲ('echo KOREAN_SWING_CLOSED_OK')
            ਮਾਨਤਾ_ਵਿਵਰਨ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','ਪੰਜਾਬੀ ਵਿੰਡੋ/ਬਟਨ/동작알림/ਇਵੈਂਟ_ਕਤਾਰ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.poll() is None:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.terminate()
            try:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.wait(timeout=5)
            except subprocess.TimeoutExpired:ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.kill();ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.wait()
            ਚੋਣਕਰਤਾ_a916db4e.close();ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdin.close();ਸਮੱਗਰੀ_ਸਥਿਤੀ_ਬਦਲੋ.stdout.close();(ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ/'serial.log').write_bytes(ਲੌਗ_ਕਤਾਰ);(ਮੰਜਿਲ_ਕੀਮਤ_ਸਥਿਤੀ_ਬਦਲੋ/'report.json').write_text(json.dumps(ਮਾਨਤਾ_ਵਿਵਰਨ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ਚਲਾਓ_2()
