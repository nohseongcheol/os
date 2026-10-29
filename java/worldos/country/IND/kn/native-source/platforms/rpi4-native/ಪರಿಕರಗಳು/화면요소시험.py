#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ,ಆಜ್ಞೆ

def ಚಲಾಯಿಸು_2():
    ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/swing';ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ.mkdir(parents=True,exist_ok=True)
    ವರ್ಗ_ಹಾದಿ=ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/new-java';ವರ್ಗ_ಹಾದಿ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ಬಿಂಬಿಸು_ಮೂಲ/'dist/jkoros-native-korean.jar'),'-d',str(ವರ್ಗ_ಹಾದಿ),str(ಬಿಂಬಿಸು_ಮೂಲ/'시험/자바/스윙시험.java'),str(ಬಿಂಬಿಸು_ಮೂಲ/'시험/자바/한글창시험.java')])
    ದೃಢೀಕರಣ_ವರದಿ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ/'build/kernel8.img').read_bytes()).hexdigest()};ಲಾಗ್_ದಾಖಲೆ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ಡೇಟಾ_ಹುದ್ದೆ=subprocess.Popen(ಆಜ್ಞೆ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        ಸೆಲೆಕ್ಟರ್_a916db4e=selectors.DefaultSelector();ಸೆಲೆಕ್ಟರ್_a916db4e.register(ಡೇಟಾ_ಹುದ್ದೆ.stdout,selectors.EVENT_READ)
        def ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(초단위=.1):
            for 누름값,_ in ಸೆಲೆಕ್ಟರ್_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ಲಾಗ್_ದಾಖಲೆ.extend(둘째값)
            assert b'PANIC:' not in ಲಾಗ್_ದಾಖಲೆ and b'HALTED' not in ಲಾಗ್_ದಾಖಲೆ,ಲಾಗ್_ದಾಖಲೆ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+초단위
            while 확인표시 not in ಲಾಗ್_ದಾಖಲೆ[현재위치:]:
                if time.monotonic()>ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್ or ಡೇಟಾ_ಹುದ್ದೆ.poll() is not None:raise AssertionError(ಲಾಗ್_ದಾಖಲೆ[현재위치:].decode('utf-8','replace'))
                ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ()
            return bytes(ಲಾಗ್_ದಾಖಲೆ[현재위치:])
        def ಕಳುಹಿಸಿ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ಲಾಗ್_ದಾಖಲೆ);ಡೇಟಾ_ಹುದ್ದೆ.stdin.write(둘째값);ಡೇಟಾ_ಹುದ್ದೆ.stdin.flush();return 기다리기(확인표시,현재위치)
        def ಶೆಲ್(ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ):return ಕಳುಹಿಸಿ((ಸ್ಟ್ರಿಂಗ್_ಡೇಟಾ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(x_ಸಮಭಾಜಕ,Y_ಬಟನ್_ಸಮನ್ವಯ):return bytes([30,1,1,x_ಸಮಭಾಜಕ&255,x_ಸಮಭಾಜಕ>>8,Y_ಬಟನ್_ಸಮನ್ವಯ&255,Y_ಬಟನ್_ಸಮನ್ವಯ>>8,30,1,0,x_ಸಮಭಾಜಕ&255,x_ಸಮಭಾಜಕ>>8,Y_ಬಟನ್_ಸಮನ್ವಯ&255,Y_ಬಟನ್_ಸಮನ್ವಯ>>8])
        def ಆದೇಶ_ಮೋಡ್():
            ಡೇಟಾ_ಹುದ್ದೆ.stdin.write(b'\x1b');ಡೇಟಾ_ಹುದ್ದೆ.stdin.flush();ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+.2
            while time.monotonic()<ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್:ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ಶೆಲ್('terminal');ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.3)
            ಡೇಟಾ=(ಬಿಂಬಿಸು_ಮೂಲ/'build/verification/new-java/스윙시험.class').read_bytes()
            ಕಳುಹಿಸಿ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ಡೇಟಾ),64):ಕಳುಹಿಸಿ(ಡೇಟಾ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ಕಳುಹಿಸಿ(b'.\n')
            ಕಳುಹಿಸಿ('java 스윙시험\n'.encode(),b'SWING READY')
            ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+3
            while time.monotonic()<ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್:ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.1)
            # JFrame centered at (120,100), content at y=130.
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(200,210),b'',)  # focus JTextField
            ಡೇಟಾ_ಹುದ್ದೆ.stdin.write('누리'.encode());ಡೇಟಾ_ಹುದ್ದೆ.stdin.flush()
            ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+.3
            while time.monotonic()<ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್:ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.05)
            ಮಾಪನ=ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ಲಾಗ್_ದಾಖಲೆ)-len(ಮಾಪನ))
            ಕಳುಹಿಸಿ(ಕಿರುಹಾದಿ_ಮೌಲ್ಯ(1),b'TERMINAL FOCUS 2')
            ಮಾಪನ=ಶೆಲ್('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ಮಾಪನ
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(180,12),b'TERMINAL FOCUS 1')
            ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್=time.monotonic()+.3
            while time.monotonic()<ಅಂತ್ಯಗೊಳಿಸು_ಆಫ್_ಸೆಟ್:ಹ್ಯಾಂಡಲ್_ಸಂಗತಿ(.05)
            with socket.socket(socket.AF_UNIX) as ಅಕ್ಷರ_ಕೋಡ್:
                ಅಕ್ಷರ_ಕೋಡ್.settimeout(10);ಅಕ್ಷರ_ಕೋಡ್.connect(str(모의제어접속))
                with ಅಕ್ಷರ_ಕೋಡ್.makefile('rwb') as ಫೈಲ್_ನಮೂದು:
                    json.loads(ಫೈಲ್_ನಮೂದು.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ/'native-swing.png'),'format':'png'}}):
                        ಫೈಲ್_ನಮೂದು.write((json.dumps(요청값)+'\n').encode());ಫೈಲ್_ನಮೂದು.flush()
                        while True:
                            반환값=json.loads(ಫೈಲ್_ನಮೂದು.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(505,115))
            ಶೆಲ್('echo SWING_CLOSED_OK')
            ಡೇಟಾ=(ವರ್ಗ_ಹಾದಿ/'한글창시험.class').read_bytes()
            ಕಳುಹಿಸಿ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ಡೇಟಾ),64):ಕಳುಹಿಸಿ(ಡೇಟಾ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ಕಳುಹಿಸಿ(b'.\n')
            ಕಳುಹಿಸಿ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(200,255),'KOREAN SWING CLICK ಹೆಸರು'.encode())
            ಕಳುಹಿಸಿ(ಕ್ಲಿಕ್_ಮಾಡಿ_ಬಟನ್(505,115))
            ಶೆಲ್('echo KOREAN_SWING_CLOSED_OK')
            ದೃಢೀಕರಣ_ವರದಿ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','ಕನ್ನಡ ವಿಂಡೋ/ಬಟನ್/동작알림/ಸಂಗತಿ_ಸರದಿ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ಡೇಟಾ_ಹುದ್ದೆ.poll() is None:ಡೇಟಾ_ಹುದ್ದೆ.terminate()
            try:ಡೇಟಾ_ಹುದ್ದೆ.wait(timeout=5)
            except subprocess.TimeoutExpired:ಡೇಟಾ_ಹುದ್ದೆ.kill();ಡೇಟಾ_ಹುದ್ದೆ.wait()
            ಸೆಲೆಕ್ಟರ್_a916db4e.close();ಡೇಟಾ_ಹುದ್ದೆ.stdin.close();ಡೇಟಾ_ಹುದ್ದೆ.stdout.close();(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ/'serial.log').write_bytes(ಲಾಗ್_ದಾಖಲೆ);(ಗಮ್ಯಸ್ಥಾನ_ಮೌಲ್ಯ_ಹುದ್ದೆ/'report.json').write_text(json.dumps(ದೃಢೀಕರಣ_ವರದಿ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ಚಲಾಯಿಸು_2()
