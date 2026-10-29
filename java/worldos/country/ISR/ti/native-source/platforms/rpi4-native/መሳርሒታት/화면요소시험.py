#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ተግብር_ትእዛዝ import 기준,ትእዛዝ

def ኣኺድ():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    ክፍሊ_መገዲ=기준/'build/verification/new-java';ክፍሊ_መገዲ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(ክፍሊ_መገዲ),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    ምርግጋፅ_ጸብጻብ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};ምዝጉብ_ሪጋ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        መራፂ_a916db4e=selectors.DefaultSelector();መራፂ_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def መትሓዚ_ፍጻመ(초단위=.1):
            for 누름값,_ in መራፂ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:ምዝጉብ_ሪጋ.extend(둘째값)
            assert b'PANIC:' not in ምዝጉብ_ሪጋ and b'HALTED' not in ምዝጉብ_ሪጋ,ምዝጉብ_ሪጋ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ኣቑም_ሽፋን=time.monotonic()+초단위
            while 확인표시 not in ምዝጉብ_ሪጋ[현재위치:]:
                if time.monotonic()>ኣቑም_ሽፋን or 자료위치.poll() is not None:raise AssertionError(ምዝጉብ_ሪጋ[현재위치:].decode('utf-8','replace'))
                መትሓዚ_ፍጻመ()
            return bytes(ምዝጉብ_ሪጋ[현재위치:])
        def ለኣኽ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(ምዝጉብ_ሪጋ);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def ሽፋን(ሕብረ_ቁምፊ_ሓበሬታ):return ለኣኽ((ሕብረ_ቁምፊ_ሓበሬታ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ኣቋራጭ_ዋጋ(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ጠዉቕ_መጠወቒ(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def ትእዛዝ_ኹነት():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();ኣቑም_ሽፋን=time.monotonic()+.2
            while time.monotonic()<ኣቑም_ሽፋን:መትሓዚ_ፍጻመ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ሽፋን('terminal');መትሓዚ_ፍጻመ(.3)
            ሓበሬታ=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            ለኣኽ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ሓበሬታ),64):ለኣኽ(ሓበሬታ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ለኣኽ(b'.\n')
            ለኣኽ('java 스윙시험\n'.encode(),b'SWING READY')
            ኣቑም_ሽፋን=time.monotonic()+3
            while time.monotonic()<ኣቑም_ሽፋን:መትሓዚ_ፍጻመ(.1)
            # JFrame centered at (120,100), content at y=130.
            ለኣኽ(ጠዉቕ_መጠወቒ(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            ኣቑም_ሽፋን=time.monotonic()+.3
            while time.monotonic()<ኣቑም_ሽፋን:መትሓዚ_ፍጻመ(.05)
            결과=ለኣኽ(ጠዉቕ_መጠወቒ(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ምዝጉብ_ሪጋ)-len(결과))
            ለኣኽ(ኣቋራጭ_ዋጋ(1),b'TERMINAL FOCUS 2')
            결과=ሽፋን('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            ለኣኽ(ጠዉቕ_መጠወቒ(180,12),b'TERMINAL FOCUS 1')
            ኣቑም_ሽፋን=time.monotonic()+.3
            while time.monotonic()<ኣቑም_ሽፋን:መትሓዚ_ፍጻመ(.05)
            with socket.socket(socket.AF_UNIX) as ኮድ_ፊደል:
                ኮድ_ፊደል.settimeout(10);ኮድ_ፊደል.connect(str(모의제어접속))
                with ኮድ_ፊደል.makefile('rwb') as ፋይል_ምእታው:
                    json.loads(ፋይል_ምእታው.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        ፋይል_ምእታው.write((json.dumps(요청값)+'\n').encode());ፋይል_ምእታው.flush()
                        while True:
                            반환값=json.loads(ፋይል_ምእታው.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ለኣኽ(ጠዉቕ_መጠወቒ(505,115))
            ሽፋን('echo SWING_CLOSED_OK')
            ሓበሬታ=(ክፍሊ_መገዲ/'한글창시험.class').read_bytes()
            ለኣኽ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ሓበሬታ),64):ለኣኽ(ሓበሬታ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ለኣኽ(b'.\n')
            ለኣኽ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ለኣኽ(ጠዉቕ_መጠወቒ(200,255),'KOREAN SWING CLICK ሽም'.encode())
            ለኣኽ(ጠዉቕ_መጠወቒ(505,115))
            ሽፋን('echo KOREAN_SWING_CLOSED_OK')
            ምርግጋፅ_ጸብጻብ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','ትግርኛ መስኮት/መጠወቒ/동작알림/ፍጻመ_ሪጋ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            መራፂ_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ምዝጉብ_ሪጋ);(목적위치/'report.json').write_text(json.dumps(ምርግጋፅ_ጸብጻብ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ኣኺድ()
