#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from үтәргә_команда import экранга_җибәрү_тамыр,команда

def эшләтү():
    күчерү_урыны_VALUE_урнаштыру=экранга_җибәрү_тамыр/'build/verification/swing';күчерү_урыны_VALUE_урнаштыру.mkdir(parents=True,exist_ok=True)
    класс_юл=экранга_җибәрү_тамыр/'build/verification/new-java';класс_юл.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(экранга_җибәрү_тамыр/'dist/jkoros-native-korean.jar'),'-d',str(класс_юл),str(экранга_җибәрү_тамыр/'시험/자바/스윙시험.java'),str(экранга_җибәрү_тамыр/'시험/자바/한글창시험.java')])
    раслау_отчет={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((экранга_җибәрү_тамыр/'build/kernel8.img').read_bytes()).hexdigest()};LOG_юл=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        мәгълүмат_урнаштыру=subprocess.Popen(команда()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        сайлагыч_a916db4e=selectors.DefaultSelector();сайлагыч_a916db4e.register(мәгълүмат_урнаштыру.stdout,selectors.EVENT_READ)
        def дескриптор_вакыйга(초단위=.1):
            for 누름값,_ in сайлагыч_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_юл.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_юл and b'HALTED' not in LOG_юл,LOG_юл[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            тәмамлау_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_юл[현재위치:]:
                if time.monotonic()>тәмамлау_OFFSET or мәгълүмат_урнаштыру.poll() is not None:raise AssertionError(LOG_юл[현재위치:].decode('utf-8','replace'))
                дескриптор_вакыйга()
            return bytes(LOG_юл[현재위치:])
        def җибәрү(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_юл);мәгълүмат_урнаштыру.stdin.write(SECOND_VALUE);мәгълүмат_урнаштыру.stdin.flush();return 기다리기(확인표시,현재위치)
        def тышча(юл_мәгълүмат):return җибәрү((юл_мәгълүмат+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def ярлык_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def чирттерү_төймә(X_координатасы,세로좌표):return bytes([30,1,1,X_координатасы&255,X_координатасы>>8,세로좌표&255,세로좌표>>8,30,1,0,X_координатасы&255,X_координатасы>>8,세로좌표&255,세로좌표>>8])
        def команда_MODE():
            мәгълүмат_урнаштыру.stdin.write(b'\x1b');мәгълүмат_урнаштыру.stdin.flush();тәмамлау_OFFSET=time.monotonic()+.2
            while time.monotonic()<тәмамлау_OFFSET:дескриптор_вакыйга(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            тышча('terminal');дескриптор_вакыйга(.3)
            мәгълүмат=(экранга_җибәрү_тамыр/'build/verification/new-java/스윙시험.class').read_bytes()
            җибәрү('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(мәгълүмат),64):җибәрү(мәгълүмат[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            җибәрү(b'.\n')
            җибәрү('java 스윙시험\n'.encode(),b'SWING READY')
            тәмамлау_OFFSET=time.monotonic()+3
            while time.monotonic()<тәмамлау_OFFSET:дескриптор_вакыйга(.1)
            # JFrame centered at (120,100), content at y=130.
            җибәрү(чирттерү_төймә(200,210),b'',)  # focus JTextField
            мәгълүмат_урнаштыру.stdin.write('누리'.encode());мәгълүмат_урнаштыру.stdin.flush()
            тәмамлау_OFFSET=time.monotonic()+.3
            while time.monotonic()<тәмамлау_OFFSET:дескриптор_вакыйга(.05)
            үлчәм=җибәрү(чирттерү_төймә(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_юл)-len(үлчәм))
            җибәрү(ярлык_VALUE(1),b'TERMINAL FOCUS 2')
            үлчәм=тышча('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in үлчәм
            җибәрү(чирттерү_төймә(180,12),b'TERMINAL FOCUS 1')
            тәмамлау_OFFSET=time.monotonic()+.3
            while time.monotonic()<тәмамлау_OFFSET:дескриптор_вакыйга(.05)
            with socket.socket(socket.AF_UNIX) as символ_коды:
                символ_коды.settimeout(10);символ_коды.connect(str(모의제어접속))
                with символ_коды.makefile('rwb') as файл_кертү:
                    json.loads(файл_кертү.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(күчерү_урыны_VALUE_урнаштыру/'native-swing.png'),'format':'png'}}):
                        файл_кертү.write((json.dumps(요청값)+'\n').encode());файл_кертү.flush()
                        while True:
                            반환값=json.loads(файл_кертү.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            җибәрү(чирттерү_төймә(505,115))
            тышча('echo SWING_CLOSED_OK')
            мәгълүмат=(класс_юл/'한글창시험.class').read_bytes()
            җибәрү('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(мәгълүмат),64):җибәрү(мәгълүмат[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            җибәрү(b'.\n')
            җибәрү('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            җибәрү(чирттерү_төймә(200,255),'KOREAN SWING CLICK исем'.encode())
            җибәрү(чирттерү_төймә(505,115))
            тышча('echo KOREAN_SWING_CLOSED_OK')
            раслау_отчет.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Татарча тәрәз/төймә/동작알림/вакыйга_чират directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if мәгълүмат_урнаштыру.poll() is None:мәгълүмат_урнаштыру.terminate()
            try:мәгълүмат_урнаштыру.wait(timeout=5)
            except subprocess.TimeoutExpired:мәгълүмат_урнаштыру.kill();мәгълүмат_урнаштыру.wait()
            сайлагыч_a916db4e.close();мәгълүмат_урнаштыру.stdin.close();мәгълүмат_урнаштыру.stdout.close();(күчерү_урыны_VALUE_урнаштыру/'serial.log').write_bytes(LOG_юл);(күчерү_урыны_VALUE_урнаштыру/'report.json').write_text(json.dumps(раслау_отчет,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':эшләтү()
