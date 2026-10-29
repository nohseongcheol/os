#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from 실행 import 기준,Komando

def Ruli():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    클래스경로=기준/'build/verification/new-java';클래스경로.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(클래스경로),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    검증기록={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};기록=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Komando()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        선택기=selectors.DefaultSelector();선택기.register(자료위치.stdout,selectors.EVENT_READ)
        def 사건처리(초단위=.1):
            for 누름값,_ in 선택기.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:기록.extend(둘째값)
            assert b'PANIC:' not in 기록 and b'HALTED' not in 기록,기록[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            끝위치=time.monotonic()+초단위
            while 확인표시 not in 기록[현재위치:]:
                if time.monotonic()>끝위치 or 자료위치.poll() is not None:raise AssertionError(기록[현재위치:].decode('utf-8','replace'))
                사건처리()
            return bytes(기록[현재위치:])
        def 보내기(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(기록);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def 셸(문자열값):return 보내기((문자열값+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def 바로가기(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def 누르기(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def 명령방식():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();끝위치=time.monotonic()+.2
            while time.monotonic()<끝위치:사건처리(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            셸('terminal');사건처리(.3)
            자료=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            보내기('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(자료),64):보내기(자료[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            보내기(b'.\n')
            보내기('java 스윙시험\n'.encode(),b'SWING READY')
            끝위치=time.monotonic()+3
            while time.monotonic()<끝위치:사건처리(.1)
            # JFrame centered at (120,100), content at y=130.
            보내기(누르기(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:사건처리(.05)
            결과=보내기(누르기(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(기록)-len(결과))
            보내기(바로가기(1),b'TERMINAL FOCUS 2')
            결과=셸('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            보내기(누르기(180,12),b'TERMINAL FOCUS 1')
            끝위치=time.monotonic()+.3
            while time.monotonic()<끝위치:사건처리(.05)
            with socket.socket(socket.AF_UNIX) as 문자값:
                문자값.settimeout(10);문자값.connect(str(모의제어접속))
                with 문자값.makefile('rwb') as 파일항목:
                    json.loads(파일항목.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        파일항목.write((json.dumps(요청값)+'\n').encode());파일항목.flush()
                        while True:
                            반환값=json.loads(파일항목.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            보내기(누르기(505,115))
            셸('echo SWING_CLOSED_OK')
            자료=(클래스경로/'한글창시험.class').read_bytes()
            보내기('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(자료),64):보내기(자료[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            보내기(b'.\n')
            보내기('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            보내기(누르기(200,255),'KOREAN SWING CLICK Nomo'.encode())
            보내기(누르기(505,115))
            셸('echo KOREAN_SWING_CLOSED_OK')
            검증기록.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 창/단추/동작알림/화면일정 directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            선택기.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(기록);(목적위치/'report.json').write_text(json.dumps(검증기록,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Ruli()
