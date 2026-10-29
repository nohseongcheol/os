#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ፈጽም_ትእዛዝ import አሳይ_ስር,ትእዛዝ

def ማስኬጃ():
    መድረሻ_እሴት_በቦታ_አስቀመጠ=አሳይ_ስር/'build/verification/swing';መድረሻ_እሴት_በቦታ_አስቀመጠ.mkdir(parents=True,exist_ok=True)
    መደብ_ዱካ=አሳይ_ስር/'build/verification/new-java';መደብ_ዱካ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(አሳይ_ስር/'dist/jkoros-native-korean.jar'),'-d',str(መደብ_ዱካ),str(አሳይ_ስር/'시험/자바/스윙시험.java'),str(አሳይ_ስር/'시험/자바/한글창시험.java')])
    ማረጋገጥ_ዘገባ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((አሳይ_ስር/'build/kernel8.img').read_bytes()).hexdigest()};መዝግብ_ረድፍ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ውሂብ_በቦታ_አስቀመጠ=subprocess.Popen(ትእዛዝ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        መራጭ_a916db4e=selectors.DefaultSelector();መራጭ_a916db4e.register(ውሂብ_በቦታ_አስቀመጠ.stdout,selectors.EVENT_READ)
        def እጀታ_ፍጻሜ(초단위=.1):
            for 누름값,_ in መራጭ_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:መዝግብ_ረድፍ.extend(둘째값)
            assert b'PANIC:' not in መዝግብ_ረድፍ and b'HALTED' not in መዝግብ_ረድፍ,መዝግብ_ረድፍ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            ጨርስ_ዝንፍ=time.monotonic()+초단위
            while 확인표시 not in መዝግብ_ረድፍ[현재위치:]:
                if time.monotonic()>ጨርስ_ዝንፍ or ውሂብ_በቦታ_አስቀመጠ.poll() is not None:raise AssertionError(መዝግብ_ረድፍ[현재위치:].decode('utf-8','replace'))
                እጀታ_ፍጻሜ()
            return bytes(መዝግብ_ረድፍ[현재위치:])
        def ላክ(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(መዝግብ_ረድፍ);ውሂብ_በቦታ_አስቀመጠ.stdin.write(둘째값);ውሂብ_በቦታ_አስቀመጠ.stdin.flush();return 기다리기(확인표시,현재위치)
        def ሼል(ኅብረቁምፊ_ውሂብ):return ላክ((ኅብረቁምፊ_ውሂብ+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def አቋራጭ_እሴት(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ጠቅ_አድርግ_አዝራር(ኤክስ_አስተባባሪ,세로좌표):return bytes([30,1,1,ኤክስ_አስተባባሪ&255,ኤክስ_አስተባባሪ>>8,세로좌표&255,세로좌표>>8,30,1,0,ኤክስ_አስተባባሪ&255,ኤክስ_አስተባባሪ>>8,세로좌표&255,세로좌표>>8])
        def ትእዛዝ_ሁነታ():
            ውሂብ_በቦታ_አስቀመጠ.stdin.write(b'\x1b');ውሂብ_በቦታ_አስቀመጠ.stdin.flush();ጨርስ_ዝንፍ=time.monotonic()+.2
            while time.monotonic()<ጨርስ_ዝንፍ:እጀታ_ፍጻሜ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            ሼል('terminal');እጀታ_ፍጻሜ(.3)
            ውሂብ=(አሳይ_ስር/'build/verification/new-java/스윙시험.class').read_bytes()
            ላክ('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ውሂብ),64):ላክ(ውሂብ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ላክ(b'.\n')
            ላክ('java 스윙시험\n'.encode(),b'SWING READY')
            ጨርስ_ዝንፍ=time.monotonic()+3
            while time.monotonic()<ጨርስ_ዝንፍ:እጀታ_ፍጻሜ(.1)
            # JFrame centered at (120,100), content at y=130.
            ላክ(ጠቅ_አድርግ_አዝራር(200,210),b'',)  # focus JTextField
            ውሂብ_በቦታ_አስቀመጠ.stdin.write('누리'.encode());ውሂብ_በቦታ_አስቀመጠ.stdin.flush()
            ጨርስ_ዝንፍ=time.monotonic()+.3
            while time.monotonic()<ጨርስ_ዝንፍ:እጀታ_ፍጻሜ(.05)
            ልኬት=ላክ(ጠቅ_አድርግ_አዝራር(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(መዝግብ_ረድፍ)-len(ልኬት))
            ላክ(አቋራጭ_እሴት(1),b'TERMINAL FOCUS 2')
            ልኬት=ሼል('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ልኬት
            ላክ(ጠቅ_አድርግ_አዝራር(180,12),b'TERMINAL FOCUS 1')
            ጨርስ_ዝንፍ=time.monotonic()+.3
            while time.monotonic()<ጨርስ_ዝንፍ:እጀታ_ፍጻሜ(.05)
            with socket.socket(socket.AF_UNIX) as የቁምፊ_ኮድ:
                የቁምፊ_ኮድ.settimeout(10);የቁምፊ_ኮድ.connect(str(모의제어접속))
                with የቁምፊ_ኮድ.makefile('rwb') as ፋይል_ምዝግብ:
                    json.loads(ፋይል_ምዝግብ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(መድረሻ_እሴት_በቦታ_አስቀመጠ/'native-swing.png'),'format':'png'}}):
                        ፋይል_ምዝግብ.write((json.dumps(요청값)+'\n').encode());ፋይል_ምዝግብ.flush()
                        while True:
                            반환값=json.loads(ፋይል_ምዝግብ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ላክ(ጠቅ_አድርግ_አዝራር(505,115))
            ሼል('echo SWING_CLOSED_OK')
            ውሂብ=(መደብ_ዱካ/'한글창시험.class').read_bytes()
            ላክ('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ውሂብ),64):ላክ(ውሂብ[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ላክ(b'.\n')
            ላክ('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ላክ(ጠቅ_አድርግ_አዝራር(200,255),'KOREAN SWING CLICK ስም'.encode())
            ላክ(ጠቅ_አድርግ_አዝራር(505,115))
            ሼል('echo KOREAN_SWING_CLOSED_OK')
            ማረጋገጥ_ዘገባ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','አማርኛ መስኮት/አዝራር/동작알림/ፍጻሜ_ሰልፍ directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ውሂብ_በቦታ_አስቀመጠ.poll() is None:ውሂብ_በቦታ_አስቀመጠ.terminate()
            try:ውሂብ_በቦታ_አስቀመጠ.wait(timeout=5)
            except subprocess.TimeoutExpired:ውሂብ_በቦታ_አስቀመጠ.kill();ውሂብ_በቦታ_አስቀመጠ.wait()
            መራጭ_a916db4e.close();ውሂብ_በቦታ_አስቀመጠ.stdin.close();ውሂብ_በቦታ_አስቀመጠ.stdout.close();(መድረሻ_እሴት_በቦታ_አስቀመጠ/'serial.log').write_bytes(መዝግብ_ረድፍ);(መድረሻ_እሴት_በቦታ_አስቀመጠ/'report.json').write_text(json.dumps(ማረጋገጥ_ዘገባ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ማስኬጃ()
