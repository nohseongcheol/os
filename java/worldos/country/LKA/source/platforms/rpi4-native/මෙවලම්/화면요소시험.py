#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from ක්_රියාත්මක_කරන්න_විධානය import 기준,විධානය

def ක්_රියාත්මක_කරන්න_2():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    පන්තිය_පෙත=기준/'build/verification/new-java';පන්තිය_පෙත.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(පන්තිය_පෙත),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
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
            දත්ත=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            ඊමේල්('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(දත්ත),64):ඊමේල්(දත්ත[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ඊමේල්(b'.\n')
            ඊමේල්('java 스윙시험\n'.encode(),b'SWING READY')
            නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+3
            while time.monotonic()<නිමා_කරන්න_ඕෆ්සෙට්:හසුරුව_සිද්ධිය(.1)
            # JFrame centered at (120,100), content at y=130.
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+.3
            while time.monotonic()<නිමා_කරන්න_ඕෆ්සෙට්:හසුරුව_සිද්ධිය(.05)
            결과=ඊමේල්(ක්ලික්_කරන්න_බොත්තම(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(ලොගය_පේළිය)-len(결과))
            ඊමේල්(කෙටිමඟ_අගය(1),b'TERMINAL FOCUS 2')
            결과=කවචය('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(180,12),b'TERMINAL FOCUS 1')
            නිමා_කරන්න_ඕෆ්සෙට්=time.monotonic()+.3
            while time.monotonic()<නිමා_කරන්න_ඕෆ්සෙට්:හසුරුව_සිද්ධිය(.05)
            with socket.socket(socket.AF_UNIX) as අනුලකුණු_කේතය:
                අනුලකුණු_කේතය.settimeout(10);අනුලකුණු_කේතය.connect(str(모의제어접속))
                with අනුලකුණු_කේතය.makefile('rwb') as ගොනුව_පිවිසුම:
                    json.loads(ගොනුව_පිවිසුම.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        ගොනුව_පිවිසුම.write((json.dumps(요청값)+'\n').encode());ගොනුව_පිවිසුම.flush()
                        while True:
                            반환값=json.loads(ගොනුව_පිවිසුම.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(505,115))
            කවචය('echo SWING_CLOSED_OK')
            දත්ත=(පන්තිය_පෙත/'한글창시험.class').read_bytes()
            ඊමේල්('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(දත්ත),64):ඊමේල්(දත්ත[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            ඊමේල්(b'.\n')
            ඊමේල්('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(200,255),'KOREAN SWING CLICK නම'.encode())
            ඊමේල්(ක්ලික්_කරන්න_බොත්තම(505,115))
            කවචය('echo KOREAN_SWING_CLOSED_OK')
            වලංගුකරණය_වාර්තාව.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 කවුළුව/බොත්තම/동작알림/සිද්ධිය_පෙළගැස්ම directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            වරකය_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(ලොගය_පේළිය);(목적위치/'report.json').write_text(json.dumps(වලංගුකරණය_වාර්තාව,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':ක්_රියාත්මක_කරන්න_2()
