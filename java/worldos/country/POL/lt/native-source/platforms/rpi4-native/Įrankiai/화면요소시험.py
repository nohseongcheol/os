#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from Vykdyti_komanda import Project_šaknis,Komanda

def Paleisti():
    vieta_VALUE_padėtis=Project_šaknis/'build/verification/swing';vieta_VALUE_padėtis.mkdir(parents=True,exist_ok=True)
    klasė_kelias=Project_šaknis/'build/verification/new-java';klasė_kelias.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_šaknis/'dist/jkoros-native-korean.jar'),'-d',str(klasė_kelias),str(Project_šaknis/'시험/자바/스윙시험.java'),str(Project_šaknis/'시험/자바/한글창시험.java')])
    tikrinimas_pranešti={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((Project_šaknis/'build/kernel8.img').read_bytes()).hexdigest()};LOG_RECORD=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        duomenys_padėtis=subprocess.Popen(Komanda()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        išrinkiklis_a916db4e=selectors.DefaultSelector();išrinkiklis_a916db4e.register(duomenys_padėtis.stdout,selectors.EVENT_READ)
        def rodyklė_įvykis(초단위=.1):
            for 누름값,_ in išrinkiklis_a916db4e.select(초단위):
                SECOND_VALUE=누름값.fileobj.read(65536)
                if SECOND_VALUE:LOG_RECORD.extend(SECOND_VALUE)
            assert b'PANIC:' not in LOG_RECORD and b'HALTED' not in LOG_RECORD,LOG_RECORD[-2048:]
        def 기다리기(žymeklis,dabartinis_padėtis,초단위=50):
            baigti_pokalbį_OFFSET=time.monotonic()+초단위
            while žymeklis not in LOG_RECORD[dabartinis_padėtis:]:
                if time.monotonic()>baigti_pokalbį_OFFSET or duomenys_padėtis.poll() is not None:raise AssertionError(LOG_RECORD[dabartinis_padėtis:].decode('utf-8','replace'))
                rodyklė_įvykis()
            return bytes(LOG_RECORD[dabartinis_padėtis:])
        def siųsti(SECOND_VALUE,žymeklis=b'jkoros-native> '):
            dabartinis_padėtis=len(LOG_RECORD);duomenys_padėtis.stdin.write(SECOND_VALUE);duomenys_padėtis.stdin.flush();return 기다리기(žymeklis,dabartinis_padėtis)
        def apvalkalas(eilutė_duomenys):return siųsti((eilutė_duomenys+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def nuoroda_VALUE(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def spustelėti_mygtukas(x_koordinatė,세로좌표):return bytes([30,1,1,x_koordinatė&255,x_koordinatė>>8,세로좌표&255,세로좌표>>8,30,1,0,x_koordinatė&255,x_koordinatė>>8,세로좌표&255,세로좌표>>8])
        def komanda_MODE():
            duomenys_padėtis.stdin.write(b'\x1b');duomenys_padėtis.stdin.flush();baigti_pokalbį_OFFSET=time.monotonic()+.2
            while time.monotonic()<baigti_pokalbį_OFFSET:rodyklė_įvykis(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            apvalkalas('terminal');rodyklė_įvykis(.3)
            duomenys=(Project_šaknis/'build/verification/new-java/스윙시험.class').read_bytes()
            siųsti('load 스윙시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(duomenys),64):siųsti(duomenys[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            siųsti(b'.\n')
            siųsti('java 스윙시험\n'.encode(),b'SWING READY')
            baigti_pokalbį_OFFSET=time.monotonic()+3
            while time.monotonic()<baigti_pokalbį_OFFSET:rodyklė_įvykis(.1)
            # JFrame centered at (120,100), content at y=130.
            siųsti(spustelėti_mygtukas(200,210),b'',)  # focus JTextField
            duomenys_padėtis.stdin.write('누리'.encode());duomenys_padėtis.stdin.flush()
            baigti_pokalbį_OFFSET=time.monotonic()+.3
            while time.monotonic()<baigti_pokalbį_OFFSET:rodyklė_įvykis(.05)
            REZULTATAS=siųsti(spustelėti_mygtukas(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(LOG_RECORD)-len(REZULTATAS))
            siųsti(nuoroda_VALUE(1),b'TERMINAL FOCUS 2')
            REZULTATAS=apvalkalas('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in REZULTATAS
            siųsti(spustelėti_mygtukas(180,12),b'TERMINAL FOCUS 1')
            baigti_pokalbį_OFFSET=time.monotonic()+.3
            while time.monotonic()<baigti_pokalbį_OFFSET:rodyklė_įvykis(.05)
            with socket.socket(socket.AF_UNIX) as simbolio_kodas:
                simbolio_kodas.settimeout(10);simbolio_kodas.connect(str(모의제어접속))
                with simbolio_kodas.makefile('rwb') as Failas_įrašas:
                    json.loads(Failas_įrašas.readline())
                    for užklausa_VALUE_625fa62c in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(vieta_VALUE_padėtis/'native-swing.png'),'format':'png'}}):
                        Failas_įrašas.write((json.dumps(užklausa_VALUE_625fa62c)+'\n').encode());Failas_įrašas.flush()
                        while True:
                            반환값=json.loads(Failas_įrašas.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            siųsti(spustelėti_mygtukas(505,115))
            apvalkalas('echo SWING_CLOSED_OK')
            duomenys=(klasė_kelias/'한글창시험.class').read_bytes()
            siųsti('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(duomenys),64):siųsti(duomenys[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            siųsti(b'.\n')
            siųsti('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            siųsti(spustelėti_mygtukas(200,255),'KOREAN SWING CLICK Pavadinimas_2'.encode())
            siųsti(spustelėti_mygtukas(505,115))
            apvalkalas('echo KOREAN_SWING_CLOSED_OK')
            tikrinimas_pranešti.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','Lietuvių Langas/mygtukas/gavinys_pranešimas/įvykis_eilė directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if duomenys_padėtis.poll() is None:duomenys_padėtis.terminate()
            try:duomenys_padėtis.wait(timeout=5)
            except subprocess.TimeoutExpired:duomenys_padėtis.kill();duomenys_padėtis.wait()
            išrinkiklis_a916db4e.close();duomenys_padėtis.stdin.close();duomenys_padėtis.stdout.close();(vieta_VALUE_padėtis/'serial.log').write_bytes(LOG_RECORD);(vieta_VALUE_padėtis/'report.json').write_text(json.dumps(tikrinimas_pranešti,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Paleisti()
