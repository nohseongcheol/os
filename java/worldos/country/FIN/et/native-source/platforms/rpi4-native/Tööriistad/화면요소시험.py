#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Täida_käsk import Project_juur,Käsk

def Käivita_2():
    sihtkoht_VALUE_ametikoht=Project_juur/'build/verification/swing';sihtkoht_VALUE_ametikoht.mkdir(parents=True,exist_ok=True)
    tund_tee=Project_juur/'build/verification/new-java';tund_tee.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_juur/'dist/jkoros-native-korean.jar'),'-d',str(tund_tee),str(Project_juur/'시험/자바/스윙시험.java'),str(Project_juur/'시험/자바/한글창시험.java')])
    kinnitamine_aruanne={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_juur/'build/kernel8.img').read_bytes()).hexdigest()};LOG_kirje=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        andmed_ametikoht=subprocess.Popen(Käsk()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        valija_a916db4e=selectors.DefaultSelector();valija_a916db4e.register(andmed_ametikoht.stdout,selectors.EVENT_READ)
        def pide_sündmus(초단위=.1):
            for 누름값,_ in valija_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_kirje.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_kirje and b'HALTED' not in LOG_kirje,LOG_kirje[-2048:]
        def 기다리기(marker,tähtaja_piires_ametikoht,초단위=50):
            lõpeta_kõne_nihe=time.monotonic()+초단위
            while marker not in LOG_kirje[tähtaja_piires_ametikoht:]:
                if time.monotonic()>lõpeta_kõne_nihe or andmed_ametikoht.poll() is not None:raise AssertionError(LOG_kirje[tähtaja_piires_ametikoht:].decode('utf-8','replace'))
                pide_sündmus()
            return bytes(LOG_kirje[tähtaja_piires_ametikoht:])
        def saatma(SECOND_VALUE,marker=b'jkoros-native> '):
            tähtaja_piires_ametikoht=len(LOG_kirje);andmed_ametikoht.stdin.write(SECOND_VALUE);andmed_ametikoht.stdin.flush();return 기다리기(marker,tähtaja_piires_ametikoht)
        def kest(string_andmed):return saatma((string_andmed+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def otsetee_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def klõps_nupp(가로좌표,세로좌표):return bytes([30,1,1,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8,30,1,0,가로좌표&255,가로좌표>>8,세로좌표&255,세로좌표>>8])
        def käsk_MODE():
            andmed_ametikoht.stdin.write(b'\x1b');andmed_ametikoht.stdin.flush();lõpeta_kõne_nihe=time.monotonic()+.2
            while time.monotonic()<lõpeta_kõne_nihe:pide_sündmus(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            kest('terminal');pide_sündmus(.3)
            andmed=(Project_juur/'build/verification/new-java/스윙시험.class').read_bytes()
            saatma('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(andmed),64):saatma(andmed[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            saatma(b'.\n')
            saatma('java 스윙시험\n'.encode(),b'SWING READY')
            lõpeta_kõne_nihe=time.monotonic()+3
            while time.monotonic()<lõpeta_kõne_nihe:pide_sündmus(.1)
            # JFrame centered at (120,100), content at y=130.
            saatma(klõps_nupp(200,210),b'',)  # focus JTextField
            andmed_ametikoht.stdin.write('누리'.encode());andmed_ametikoht.stdin.flush()
            lõpeta_kõne_nihe=time.monotonic()+.3
            while time.monotonic()<lõpeta_kõne_nihe:pide_sündmus(.05)
            TULEMUS=saatma(klõps_nupp(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_kirje)-len(TULEMUS))
            saatma(otsetee_VALUE(1),b'TERMINAL FOCUS 2')
            TULEMUS=kest('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in TULEMUS
            saatma(klõps_nupp(180,12),b'TERMINAL FOCUS 1')
            lõpeta_kõne_nihe=time.monotonic()+.3
            while time.monotonic()<lõpeta_kõne_nihe:pide_sündmus(.05)
            with socket.socket(socket.AF_UNIX) as koodipunkt:
                koodipunkt.settimeout(10);koodipunkt.connect(str(모의제어접속))
                with koodipunkt.makefile('rwb') as Fail_kirje:
                    json.loads(Fail_kirje.readline())
                    for päring_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(sihtkoht_VALUE_ametikoht/'native-swing.png'),'format':'png'}}):
                        Fail_kirje.write((json.dumps(päring_VALUE_625fa62c)+'\n').encode());Fail_kirje.flush()
                        while True:
                            반환값=json.loads(Fail_kirje.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            saatma(klõps_nupp(505,115))
            kest('echo SWING_CLOSED_OK')
            andmed=(tund_tee/'한글창시험.class').read_bytes()
            saatma('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(andmed),64):saatma(andmed[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            saatma(b'.\n')
            saatma('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            saatma(klõps_nupp(200,255),'KOREAN SWING CLICK Nimi_2'.encode())
            saatma(klõps_nupp(505,115))
            kest('echo KOREAN_SWING_CLOSED_OK')
            kinnitamine_aruanne.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Eesti aken/nupp/Toiming_teatamine/sündmus_järjekord directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if andmed_ametikoht.poll() is None:andmed_ametikoht.terminate()
            try:andmed_ametikoht.wait(timeout=5)
            except subprocess.TimeoutExpired:andmed_ametikoht.kill();andmed_ametikoht.wait()
            valija_a916db4e.close();andmed_ametikoht.stdin.close();andmed_ametikoht.stdout.close();(sihtkoht_VALUE_ametikoht/'serial.log').write_bytes(LOG_kirje);(sihtkoht_VALUE_ametikoht/'report.json').write_text(json.dumps(kinnitamine_aruanne,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Käivita_2()
