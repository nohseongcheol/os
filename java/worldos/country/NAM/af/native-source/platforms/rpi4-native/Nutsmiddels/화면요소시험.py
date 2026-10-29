#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from uitvoer_bevel import Project_wortel,Opdrag

def Loop():
    bestemming_VALUE_plaas=Project_wortel/'build/verification/swing';bestemming_VALUE_plaas.mkdir(parents=True,exist_ok=True)
    Klas_pad=Project_wortel/'build/verification/new-java';Klas_pad.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_wortel/'dist/jkoros-native-korean.jar'),'-d',str(Klas_pad),str(Project_wortel/'시험/자바/스윙시험.java'),str(Project_wortel/'시험/자바/한글창시험.java')])
    validering_verslag={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_wortel/'build/kernel8.img').read_bytes()).hexdigest()};LOG_ry=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        data_plaas=subprocess.Popen(Opdrag()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        selekteerder_a916db4e=selectors.DefaultSelector();selekteerder_a916db4e.register(data_plaas.stdout,selectors.EVENT_READ)
        def handvatsel_gebeurtenis(초단위=.1):
            for 누름값,_ in selekteerder_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_ry.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_ry and b'HALTED' not in LOG_ry,LOG_ry[-2048:]
        def 기다리기(확인표시,현재위치,초단위=50):
            beëindig_OFFSET=time.monotonic()+초단위
            while 확인표시 not in LOG_ry[현재위치:]:
                if time.monotonic()>beëindig_OFFSET or data_plaas.poll() is not None:raise AssertionError(LOG_ry[현재위치:].decode('utf-8','replace'))
                handvatsel_gebeurtenis()
            return bytes(LOG_ry[현재위치:])
        def e_pos(SECOND_VALUE,확인표시=b'jkoros-native> '):
            현재위치=len(LOG_ry);data_plaas.stdin.write(SECOND_VALUE);data_plaas.stdin.flush();return 기다리기(확인표시,현재위치)
        def dop(string_data):return e_pos((string_data+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def kortpad_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klik_knoppie(x_koördinaat,Y_koördinaat):return bytes([30,1,1,x_koördinaat&255,x_koördinaat>>8,Y_koördinaat&255,Y_koördinaat>>8,30,1,0,x_koördinaat&255,x_koördinaat>>8,Y_koördinaat&255,Y_koördinaat>>8])
        def bevel_MODE():
            data_plaas.stdin.write(b'\x1b');data_plaas.stdin.flush();beëindig_OFFSET=time.monotonic()+.2
            while time.monotonic()<beëindig_OFFSET:handvatsel_gebeurtenis(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            dop('terminal');handvatsel_gebeurtenis(.3)
            data=(Project_wortel/'build/verification/new-java/스윙시험.class').read_bytes()
            e_pos('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):e_pos(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            e_pos(b'.\n')
            e_pos('java 스윙시험\n'.encode(),b'SWING READY')
            beëindig_OFFSET=time.monotonic()+3
            while time.monotonic()<beëindig_OFFSET:handvatsel_gebeurtenis(.1)
            # JFrame centered at (120,100), content at y=130.
            e_pos(klik_knoppie(200,210),b'',)  # focus JTextField
            data_plaas.stdin.write('누리'.encode());data_plaas.stdin.flush()
            beëindig_OFFSET=time.monotonic()+.3
            while time.monotonic()<beëindig_OFFSET:handvatsel_gebeurtenis(.05)
            maatreël=e_pos(klik_knoppie(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_ry)-len(maatreël))
            e_pos(kortpad_VALUE(1),b'TERMINAL FOCUS 2')
            maatreël=dop('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in maatreël
            e_pos(klik_knoppie(180,12),b'TERMINAL FOCUS 1')
            beëindig_OFFSET=time.monotonic()+.3
            while time.monotonic()<beëindig_OFFSET:handvatsel_gebeurtenis(.05)
            with socket.socket(socket.AF_UNIX) as karakterkode:
                karakterkode.settimeout(10);karakterkode.connect(str(모의제어접속))
                with karakterkode.makefile('rwb') as lêer_inskrywing:
                    json.loads(lêer_inskrywing.readline())
                    for 요청값 in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(bestemming_VALUE_plaas/'native-swing.png'),'format':'png'}}):
                        lêer_inskrywing.write((json.dumps(요청값)+'\n').encode());lêer_inskrywing.flush()
                        while True:
                            반환값=json.loads(lêer_inskrywing.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            e_pos(klik_knoppie(505,115))
            dop('echo SWING_CLOSED_OK')
            data=(Klas_pad/'한글창시험.class').read_bytes()
            e_pos('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(data),64):e_pos(data[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            e_pos(b'.\n')
            e_pos('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            e_pos(klik_knoppie(200,255),'KOREAN SWING CLICK Naam'.encode())
            e_pos(klik_knoppie(505,115))
            dop('echo KOREAN_SWING_CLOSED_OK')
            validering_verslag.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','한국어 venster/knoppie/동작알림/gebeurtenis_tou directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if data_plaas.poll() is None:data_plaas.terminate()
            try:data_plaas.wait(timeout=5)
            except subprocess.TimeoutExpired:data_plaas.kill();data_plaas.wait()
            selekteerder_a916db4e.close();data_plaas.stdin.close();data_plaas.stdout.close();(bestemming_VALUE_plaas/'serial.log').write_bytes(LOG_ry);(bestemming_VALUE_plaas/'report.json').write_text(json.dumps(validering_verslag,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Loop()
