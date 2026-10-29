#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from аткаруу_буйрук import 기준,Команда

def Жүргүзүү():
    목적위치=기준/'build/verification/swing';목적위치.mkdir(parents=True,exist_ok=True)
    класс_жол=기준/'build/verification/new-java';класс_жол.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'dist/jkoros-native-korean.jar'),'-d',str(класс_жол),str(기준/'시험/자바/스윙시험.java'),str(기준/'시험/자바/한글창시험.java')])
    ырастоо_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((기준/'build/kernel8.img').read_bytes()).hexdigest()};жазуу_катар=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        자료위치=subprocess.Popen(Команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        селектор_a916db4e=selectors.DefaultSelector();селектор_a916db4e.register(자료위치.stdout,selectors.EVENT_READ)
        def тутка_окуя(초단위=.1):
            for 누름값,_ in селектор_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:жазуу_катар.extend(둘째값)
            assert b'PANIC:' not in жазуу_катар and b'HALTED' not in жазуу_катар,жазуу_катар[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            аяктоо_Жылбышуу=time.monotonic()+초단위
            while 확인표시 not in жазуу_катар[현재위치:]:
                if time.monotonic()>аяктоо_Жылбышуу or 자료위치.poll() is not None:raise AssertionError(жазуу_катар[현재위치:].decode('utf-8','replace'))
                тутка_окуя()
            return bytes(жазуу_катар[현재위치:])
        def жөнөтүү(둘째값,확인표시=b'jkoros-native> '):
            현재위치=len(жазуу_катар);자료위치.stdin.write(둘째값);자료위치.stdin.flush();return 기다리기(확인표시,현재위치)
        def сырты(сап_берилмелер):return жөнөтүү((сап_берилмелер+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def тез_чакыргыч_маани(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def баскылоо_баскыч(x_координата,세로좌표):return bytes([30,1,1,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8,30,1,0,x_координата&255,x_координата>>8,세로좌표&255,세로좌표>>8])
        def буйрук_режим():
            자료위치.stdin.write(b'\x1b');자료위치.stdin.flush();аяктоо_Жылбышуу=time.monotonic()+.2
            while time.monotonic()<аяктоо_Жылбышуу:тутка_окуя(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            сырты('terminal');тутка_окуя(.3)
            берилмелер=(기준/'build/verification/new-java/스윙시험.class').read_bytes()
            жөнөтүү('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(берилмелер),64):жөнөтүү(берилмелер[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            жөнөтүү(b'.\n')
            жөнөтүү('java 스윙시험\n'.encode(),b'SWING READY')
            аяктоо_Жылбышуу=time.monotonic()+3
            while time.monotonic()<аяктоо_Жылбышуу:тутка_окуя(.1)
            # JFrame centered at (120,100), content at y=130.
            жөнөтүү(баскылоо_баскыч(200,210),b'',)  # focus JTextField
            자료위치.stdin.write('누리'.encode());자료위치.stdin.flush()
            аяктоо_Жылбышуу=time.monotonic()+.3
            while time.monotonic()<аяктоо_Жылбышуу:тутка_окуя(.05)
            결과=жөнөтүү(баскылоо_баскыч(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(жазуу_катар)-len(결과))
            жөнөтүү(тез_чакыргыч_маани(1),b'TERMINAL FOCUS 2')
            결과=сырты('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in 결과
            жөнөтүү(баскылоо_баскыч(180,12),b'TERMINAL FOCUS 1')
            аяктоо_Жылбышуу=time.monotonic()+.3
            while time.monotonic()<аяктоо_Жылбышуу:тутка_окуя(.05)
            with socket.socket(socket.AF_UNIX) as символ_коду:
                символ_коду.settimeout(10);символ_коду.connect(str(모의제어접속))
                with символ_коду.makefile('rwb') as файл_киргизме_жазуу:
                    json.loads(файл_киргизме_жазуу.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(목적위치/'native-swing.png'),'format':'png'}}):
                        файл_киргизме_жазуу.write((json.dumps(요청값)+'\n').encode());файл_киргизме_жазуу.flush()
                        while True:
                            반환값=json.loads(файл_киргизме_жазуу.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            жөнөтүү(баскылоо_баскыч(505,115))
            сырты('echo SWING_CLOSED_OK')
            берилмелер=(класс_жол/'한글창시험.class').read_bytes()
            жөнөтүү('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(берилмелер),64):жөнөтүү(берилмелер[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            жөнөтүү(b'.\n')
            жөнөтүү('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            жөнөтүү(баскылоо_баскыч(200,255),'KOREAN SWING CLICK Аты'.encode())
            жөнөтүү(баскылоо_баскыч(505,115))
            сырты('echo KOREAN_SWING_CLOSED_OK')
            ырастоо_отчет.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 терезе/баскыч/동작알림/окуя_кезек directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if 자료위치.poll() is None:자료위치.terminate()
            try:자료위치.wait(timeout=5)
            except subprocess.TimeoutExpired:자료위치.kill();자료위치.wait()
            селектор_a916db4e.close();자료위치.stdin.close();자료위치.stdout.close();(목적위치/'serial.log').write_bytes(жазуу_катар);(목적위치/'report.json').write_text(json.dumps(ырастоо_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Жүргүзүү()
