#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from выканаць_каманда import 기준,Загад

def Выканаць():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    клас_шлях=기준/'build/verification/new-java';клас_шлях.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(клас_шлях),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    праверка_справаздача={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};журнал_запіс=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Загад()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектар_a916db4e=selectors.DefaultSelector();селектар_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def маркер_падзея(초단위=.1):
            for 누름값,_ in селектар_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:журнал_запіс.extend(둘째값)
            assert b'PANIC:' not in журнал_запіс and b'HALTED' not in журнал_запіс,журнал_запіс[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            скончыць_Зрух=time.monotonic()+초단위
            while 확인표시 not in журнал_запіс[현재위치:]:
                if time.monotonic()>скончыць_Зрух or 자료위치.poll() is not None:raise AssertionError(журнал_запіс[현재위치:].decode('utf-8','replace'))
                маркер_падзея()
            return bytes(журнал_запіс[현재위치:])
        def адправіць(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(журнал_запіс);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def абалонка(радок_дадзеныя):return адправіць((радок_дадзеныя+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ярлык_значэнне(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def націснуць_кнопка(каардыната_x,세로좌표):return bytes([30,1,1,каардыната_x&255,каардыната_x>>8,세로좌표&255,세로좌표>>8,30,1,0,каардыната_x&255,каардыната_x>>8,세로좌표&255,세로좌표>>8])
        def каманда_рэжым():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();скончыць_Зрух=time.monotonic()+.2
            while time.monotonic()<скончыць_Зрух:маркер_падзея(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            абалонка('terminal');маркер_падзея(.3)
            дадзеныя=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            адправіць('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(дадзеныя),64):адправіць(дадзеныя[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            адправіць(b'.\n')
            адправіць('java 스윙시험\n'.encode(),b'SWING READY')
            скончыць_Зрух=time.monotonic()+3
            while time.monotonic()<скончыць_Зрух:маркер_падзея(.1)
            # JFrame centered at (120,100), content at y=130.
            адправіць(націснуць_кнопка(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            скончыць_Зрух=time.monotonic()+.3
            while time.monotonic()<скончыць_Зрух:маркер_падзея(.05)
            결과=адправіць(націснуць_кнопка(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(журнал_запіс)-len(결과))
            адправіць(ярлык_значэнне(1),b'TERMINAL FOCUS 2')
            결과=абалонка('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            адправіць(націснуць_кнопка(180,12),b'TERMINAL FOCUS 1')
            скончыць_Зрух=time.monotonic()+.3
            while time.monotonic()<скончыць_Зрух:маркер_падзея(.05)
            with socket.socket(socket.AF_UNIX) as код_сімвала:
                код_сімвала.settimeout(10);код_сімвала.connect(str(모의제어접속))
                with код_сімвала.makefile('rwb') as файл_увядзенне:
                    json.loads(файл_увядзенне.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        файл_увядзенне.write((json.dumps(요청값)+'\n').encode());файл_увядзенне.flush()
                        while True:
                            반환값=json.loads(файл_увядзенне.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            адправіць(націснуць_кнопка(505,115))
            абалонка('echo SWING_CLOSED_OK')
            дадзеныя=(клас_шлях/'한글창시험.class').read_bytes()
            адправіць('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(дадзеныя),64):адправіць(дадзеныя[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            адправіць(b'.\n')
            адправіць('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            адправіць(націснуць_кнопка(200,255),'KOREAN SWING CLICK Назва'.encode())
            адправіць(націснуць_кнопка(505,115))
            абалонка('echo KOREAN_SWING_CLOSED_OK')
            праверка_справаздача.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 акно/кнопка/동작알림/падзея_чарга directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            селектар_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(журнал_запіс);(목적위치/'report.json').write_text(json.dumps(праверка_справаздача,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Выканаць()
