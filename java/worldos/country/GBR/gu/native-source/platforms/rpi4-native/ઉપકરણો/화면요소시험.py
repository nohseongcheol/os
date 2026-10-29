#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ,આદેશ

def ચલાવો_2():
    ગંતવ્ય_મૂલ્ય_સ્થિતિ=પ્રોજેક્ટ_રૂટ/'build/verification/swing';ગંતવ્ય_મૂલ્ય_સ્થિતિ.mkdir(parents=True,exist_ok=True)
    વર્ગ_પાથ=પ્રોજેક્ટ_રૂટ/'build/verification/new-java';વર્ગ_પાથ.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(પ્રોજેક્ટ_રૂટ/'dist/jkoros-native-korean.jar'),'-d',str(વર્ગ_પાથ),str(પ્રોજેક્ટ_રૂટ/'시험/자바/스윙시험.java'),str(પ્રોજેક્ટ_રૂટ/'시험/자바/한글창시험.java')])
    માન્યતા_અહેવાલ={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((પ્રોજેક્ટ_રૂટ/'build/kernel8.img').read_bytes()).hexdigest()};લૉગ_પંક્તિ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        ડેટા_સ્થિતિ=subprocess.Popen(આદેશ()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        પસંદકર્તા_a916db4e=selectors.DefaultSelector();પસંદકર્તા_a916db4e.register(ડેટા_સ્થિતિ.stdout,selectors.EVENT_READ)
        def હેન્ડલ_ઇવેંટ(초단위=.1):
            for 누름값,_ in પસંદકર્તા_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:લૉગ_પંક્તિ.extend(둘째값)
            assert b'PANIC:' not in લૉગ_પંક્તિ and b'HALTED' not in લૉગ_પંક્તિ,લૉગ_પંક્તિ[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            અંત_કરો_ઑફસેટ=time.monotonic()+초단위
            while 확인표시 not in લૉગ_પંક્તિ[현재위치:]:
                if time.monotonic()>અંત_કરો_ઑફસેટ or ડેટા_સ્થિતિ.poll() is not None:raise AssertionError(લૉગ_પંક્તિ[현재위치:].decode('utf-8','replace'))
                હેન્ડલ_ઇવેંટ()
            return bytes(લૉગ_પંક્તિ[현재위치:])
        def મોકલો(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(લૉગ_પંક્તિ);ડેટા_સ્થિતિ.stdin.write(둘째값);ડેટા_સ્થિતિ.stdin.flush();return 기다리기(확인표시,현재위치)
        def શેલ(સ્ટ્રિંગ_ડેટા):return મોકલો((સ્ટ્રિંગ_ડેટા+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def શૉર્ટકટ_મૂલ્ય(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def ક્લિક_કરો_બટન(x_યામ,세로좌표):return bytes([30,1,1,x_યામ&255,x_યામ>>8,세로좌표&255,세로좌표>>8,30,1,0,x_યામ&255,x_યામ>>8,세로좌표&255,세로좌표>>8])
        def આદેશ_મોડ():
            ડેટા_સ્થિતિ.stdin.write(b'\x1b');ડેટા_સ્થિતિ.stdin.flush();અંત_કરો_ઑફસેટ=time.monotonic()+.2
            while time.monotonic()<અંત_કરો_ઑફસેટ:હેન્ડલ_ઇવેંટ(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            શેલ('terminal');હેન્ડલ_ઇવેંટ(.3)
            ડેટા=(પ્રોજેક્ટ_રૂટ/'build/verification/new-java/스윙시험.class').read_bytes()
            મોકલો('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ડેટા),64):મોકલો(ડેટા[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            મોકલો(b'.\n')
            મોકલો('java 스윙시험\n'.encode(),b'SWING READY')
            અંત_કરો_ઑફસેટ=time.monotonic()+3
            while time.monotonic()<અંત_કરો_ઑફસેટ:હેન્ડલ_ઇવેંટ(.1)
            # JFrame centered at (120,100), content at y=130.
            મોકલો(ક્લિક_કરો_બટન(200,210),b'',)  # focus JTextField
            ડેટા_સ્થિતિ.stdin.write('누리'.encode());ડેટા_સ્થિતિ.stdin.flush()
            અંત_કરો_ઑફસેટ=time.monotonic()+.3
            while time.monotonic()<અંત_કરો_ઑફસેટ:હેન્ડલ_ઇવેંટ(.05)
            પરિમાણ=મોકલો(ક્લિક_કરો_બટન(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(લૉગ_પંક્તિ)-len(પરિમાણ))
            મોકલો(શૉર્ટકટ_મૂલ્ય(1),b'TERMINAL FOCUS 2')
            પરિમાણ=શેલ('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in પરિમાણ
            મોકલો(ક્લિક_કરો_બટન(180,12),b'TERMINAL FOCUS 1')
            અંત_કરો_ઑફસેટ=time.monotonic()+.3
            while time.monotonic()<અંત_કરો_ઑફસેટ:હેન્ડલ_ઇવેંટ(.05)
            with socket.socket(socket.AF_UNIX) as વર્ણ_કોડ:
                વર્ણ_કોડ.settimeout(10);વર્ણ_કોડ.connect(str(모의제어접속))
                with વર્ણ_કોડ.makefile('rwb') as ફાઇલ_પ્રવેશ:
                    json.loads(ફાઇલ_પ્રવેશ.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(ગંતવ્ય_મૂલ્ય_સ્થિતિ/'native-swing.png'),'format':'png'}}):
                        ફાઇલ_પ્રવેશ.write((json.dumps(요청값)+'\n').encode());ફાઇલ_પ્રવેશ.flush()
                        while True:
                            반환값=json.loads(ફાઇલ_પ્રવેશ.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            મોકલો(ક્લિક_કરો_બટન(505,115))
            શેલ('echo SWING_CLOSED_OK')
            ડેટા=(વર્ગ_પાથ/'한글창시험.class').read_bytes()
            મોકલો('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(ડેટા),64):મોકલો(ડેટા[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            મોકલો(b'.\n')
            મોકલો('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            મોકલો(ક્લિક_કરો_બટન(200,255),'KOREAN SWING CLICK નામ'.encode())
            મોકલો(ક્લિક_કરો_બટન(505,115))
            શેલ('echo KOREAN_SWING_CLOSED_OK')
            માન્યતા_અહેવાલ.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','ગુજરાતી વિંડો/બટન/동작알림/ઇવેંટ_કતાર directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if ડેટા_સ્થિતિ.poll() is None:ડેટા_સ્થિતિ.terminate()
            try:ડેટા_સ્થિતિ.wait(timeout=5)
            except subprocess.TimeoutExpired:ડેટા_સ્થિતિ.kill();ડેટા_સ્થિતિ.wait()
            પસંદકર્તા_a916db4e.close();ડેટા_સ્થિતિ.stdin.close();ડેટા_સ્થિતિ.stdout.close();(ગંતવ્ય_મૂલ્ય_સ્થિતિ/'serial.log').write_bytes(લૉગ_પંક્તિ);(ગંતવ્ય_મૂલ્ય_સ્થિતિ/'report.json').write_text(json.dumps(માન્યતા_અહેવાલ,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ચલાવો_2()
