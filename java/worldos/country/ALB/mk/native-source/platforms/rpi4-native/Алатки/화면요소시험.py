#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Изврши_наредба import Project_корен,Команда

def Изврши_2():
    одредиште_VALUE_позиционирање=Project_корен/'build/verification/swing';одредиште_VALUE_позиционирање.mkdir(parents=True,exist_ok=True)
    класа_патека=Project_корен/'build/verification/new-java';класа_патека.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_корен/'dist/jkoros-native-korean.jar'),'-d',str(класа_патека),str(Project_корен/'시험/자바/스윙시험.java'),str(Project_корен/'시험/자바/한글창시험.java')])
    проверка_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_корен/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ред=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        податоци_позиционирање=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        избирач_a916db4e=selectors.DefaultSelector();избирач_a916db4e.register(податоци_позиционирање.stdout,selectors.EVENT_READ)
        def рачка_настан(초단위=.1):
            for 누름값,_ in избирач_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ред.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ред and b'HALTED' not in LOG_ред,LOG_ред[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            крај_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ред[현재위치:]:
                if time.monotonic()>крај_OFFSET or податоци_позиционирање.poll() is not None:raise AssertionError(LOG_ред[현재위치:].decode('utf-8','replace'))
                рачка_настан()
            return bytes(LOG_ред[현재위치:])
        def испрати(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ред);податоци_позиционирање.stdin.write(SECOND_VALUE);податоци_позиционирање.stdin.flush();return 기다리기(확인표시,현재위치)
        def обвивка(низа_податоци):return испрати((низа_податоци+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def брз_пристап_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def кликни_копче(координата_х,세로좌표):return bytes([30,1,1,координата_х&255,координата_х>>8,세로좌표&255,세로좌표>>8,30,1,0,координата_х&255,координата_х>>8,세로좌표&255,세로좌표>>8])
        def наредба_MODE():
            податоци_позиционирање.stdin.write(b'\x1b');податоци_позиционирање.stdin.flush();крај_OFFSET=time.monotonic()+.2
            while time.monotonic()<крај_OFFSET:рачка_настан(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            обвивка('terminal');рачка_настан(.3)
            податоци=(Project_корен/'build/verification/new-java/스윙시험.class').read_bytes()
            испрати('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(податоци),64):испрати(податоци[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            испрати(b'.\n')
            испрати('java 스윙시험\n'.encode(),b'SWING READY')
            крај_OFFSET=time.monotonic()+3
            while time.monotonic()<крај_OFFSET:рачка_настан(.1)
            # JFrame centered at (120,100), content at y=130.
            испрати(кликни_копче(200,210),b'',)  # focus JTextField
            податоци_позиционирање.stdin.write('누리'.encode());податоци_позиционирање.stdin.flush()
            крај_OFFSET=time.monotonic()+.3
            while time.monotonic()<крај_OFFSET:рачка_настан(.05)
            мерка=испрати(кликни_копче(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_ред)-len(мерка))
            испрати(брз_пристап_VALUE(1),b'TERMINAL FOCUS 2')
            мерка=обвивка('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in мерка
            испрати(кликни_копче(180,12),b'TERMINAL FOCUS 1')
            крај_OFFSET=time.monotonic()+.3
            while time.monotonic()<крај_OFFSET:рачка_настан(.05)
            with socket.socket(socket.AF_UNIX) as кодна_точка:
                кодна_точка.settimeout(10);кодна_точка.connect(str(모의제어접속))
                with кодна_точка.makefile('rwb') as датотека_внес:
                    json.loads(датотека_внес.readline())
                    for Барање_на_HTTP_VALUE in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(одредиште_VALUE_позиционирање/'native-swing.png'),'format':'png'}}):
                        датотека_внес.write((json.dumps(Барање_на_HTTP_VALUE)+'\n').encode());датотека_внес.flush()
                        while True:
                            반환값=json.loads(датотека_внес.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            испрати(кликни_копче(505,115))
            обвивка('echo SWING_CLOSED_OK')
            податоци=(класа_патека/'한글창시험.class').read_bytes()
            испрати('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(податоци),64):испрати(податоци[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            испрати(b'.\n')
            испрати('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            испрати(кликни_копче(200,255),'KOREAN SWING CLICK Име'.encode())
            испрати(кликни_копче(505,115))
            обвивка('echo KOREAN_SWING_CLOSED_OK')
            проверка_извештај.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Македонски прозорец/копче/동작알림/настан_ред_на_чекање directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if податоци_позиционирање.poll() is None:податоци_позиционирање.terminate()
            try:податоци_позиционирање.wait(timeout=5)
            except subprocess.TimeoutExpired:податоци_позиционирање.kill();податоци_позиционирање.wait()
            избирач_a916db4e.close();податоци_позиционирање.stdin.close();податоци_позиционирање.stdout.close();(одредиште_VALUE_позиционирање/'serial.log').write_bytes(LOG_ред);(одредиште_VALUE_позиционирање/'report.json').write_text(json.dumps(проверка_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Изврши_2()
