#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Изврши_команда import пројектовати_корен,Наредба

def Покрени():
    одредиште_вриједност_позиција=пројектовати_корен/'build/verification/swing';одредиште_вриједност_позиција.mkdir(parents=True,exist_ok=True)
    класа_пут=пројектовати_корен/'build/verification/new-java';класа_пут.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(пројектовати_корен/'dist/jkoros-native-korean.jar'),'-d',str(класа_пут),str(пројектовати_корен/'시험/자바/스윙시험.java'),str(пројектовати_корен/'시험/자바/한글창시험.java')])
    провјера_извештај={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((пројектовати_корен/'build/kernel8.img').read_bytes()).hexdigest()};евиденција_ред=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        подаци_позиција=subprocess.Popen(Наредба()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        бирач_a916db4e=selectors.DefaultSelector();бирач_a916db4e.register(подаци_позиција.stdout,selectors.EVENT_READ)
        def хватиште_догађај(초단위=.1):
            for 누름값,_ in бирач_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:евиденција_ред.extend(둘째값)
            assert b'PANIC:' not in евиденција_ред and b'HALTED' not in евиденција_ред,евиденција_ред[-2048:]
        def 기다리기(확인표시,актуелно_позиција,초단위=50):
            завршити_Помак=time.monotonic()+초단위
            while 확인표시 not in евиденција_ред[актуелно_позиција:]:
                if time.monotonic()>завршити_Помак or подаци_позиција.poll() is not None:raise AssertionError(евиденција_ред[актуелно_позиција:].decode('utf-8','replace'))
                хватиште_догађај()
            return bytes(евиденција_ред[актуелно_позиција:])
        def послати(둘째값,확인표시=b'jkoros-native> '):
            актуелно_позиција=len(евиденција_ред);подаци_позиција.stdin.write(둘째값);подаци_позиција.stdin.flush();return 기다리기(확인표시,актуелно_позиција)
        def љуска(ниска_подаци):return послати((ниска_подаци+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def пречица_вриједност(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def клик_дугме(x_координата,дугме_Y_координата):return bytes([30,1,1,x_координата&255,x_координата>>8,дугме_Y_координата&255,дугме_Y_координата>>8,30,1,0,x_координата&255,x_координата>>8,дугме_Y_координата&255,дугме_Y_координата>>8])
        def команда_мод():
            подаци_позиција.stdin.write(b'\x1b');подаци_позиција.stdin.flush();завршити_Помак=time.monotonic()+.2
            while time.monotonic()<завршити_Помак:хватиште_догађај(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            љуска('terminal');хватиште_догађај(.3)
            подаци=(пројектовати_корен/'build/verification/new-java/스윙시험.class').read_bytes()
            послати('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(подаци),64):послати(подаци[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            послати(b'.\n')
            послати('java 스윙시험\n'.encode(),b'SWING READY')
            завршити_Помак=time.monotonic()+3
            while time.monotonic()<завршити_Помак:хватиште_догађај(.1)
            # JFrame centered at (120,100), content at y=130.
            послати(клик_дугме(200,210),b'',)  # focus JTextField
            подаци_позиција.stdin.write('누리'.encode());подаци_позиција.stdin.flush()
            завршити_Помак=time.monotonic()+.3
            while time.monotonic()<завршити_Помак:хватиште_догађај(.05)
            ИСХОД=послати(клик_дугме(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(евиденција_ред)-len(ИСХОД))
            послати(пречица_вриједност(1),b'TERMINAL FOCUS 2')
            ИСХОД=љуска('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in ИСХОД
            послати(клик_дугме(180,12),b'TERMINAL FOCUS 1')
            завршити_Помак=time.monotonic()+.3
            while time.monotonic()<завршити_Помак:хватиште_догађај(.05)
            with socket.socket(socket.AF_UNIX) as кôд_знака:
                кôд_знака.settimeout(10);кôд_знака.connect(str(모의제어접속))
                with кôд_знака.makefile('rwb') as фајл_унос:
                    json.loads(фајл_унос.readline())
                    for захтев_вриједност in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(одредиште_вриједност_позиција/'native-swing.png'),'format':'png'}}):
                        фајл_унос.write((json.dumps(захтев_вриједност)+'\n').encode());фајл_унос.flush()
                        while True:
                            반환값=json.loads(фајл_унос.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            послати(клик_дугме(505,115))
            љуска('echo SWING_CLOSED_OK')
            подаци=(класа_пут/'한글창시험.class').read_bytes()
            послати('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(подаци),64):послати(подаци[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            послати(b'.\n')
            послати('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            послати(клик_дугме(200,255),'KOREAN SWING CLICK Назив'.encode())
            послати(клик_дугме(505,115))
            љуска('echo KOREAN_SWING_CLOSED_OK')
            провјера_извештај.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 Прозор/дугме/동작알림/догађај_редослед directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if подаци_позиција.poll() is None:подаци_позиција.terminate()
            try:подаци_позиција.wait(timeout=5)
            except subprocess.TimeoutExpired:подаци_позиција.kill();подаци_позиција.wait()
            бирач_a916db4e.close();подаци_позиција.stdin.close();подаци_позиција.stdout.close();(одредиште_вриједност_позиција/'serial.log').write_bytes(евиденција_ред);(одредиште_вриједност_позиција/'report.json').write_text(json.dumps(провјера_извештај,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Покрени()
