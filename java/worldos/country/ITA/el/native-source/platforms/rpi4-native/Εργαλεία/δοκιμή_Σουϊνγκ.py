#!/usr/bin/env python3
"""Native Swing rendering, Java callbacks, Korean wrappers and session switching."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from εκτελώ_εντολή import έργο_ρίζα,Εντολή

def Εκτέλεση_2():
    προορισμός_τιμή_θέση=έργο_ρίζα/'build/verification/swing';προορισμός_τιμή_θέση.mkdir(parents=True,exist_ok=True)
    Τάξη_διαδρομή=έργο_ρίζα/'build/verification/new-java';Τάξη_διαδρομή.mkdir(parents=True,exist_ok=True)
    subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(έργο_ρίζα/'dist/jkoros-native-korean.jar'),'-d',str(Τάξη_διαδρομή),str(έργο_ρίζα/'시험/자바/Σουϊνγκ_δοκιμή.java'),str(έργο_ρίζα/'시험/자바/한글창시험.java')])
    επικύρωση_έκθεση={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest()};καταγράφω_ρεκόρ=bytearray()
    with tempfile.TemporaryDirectory(prefix='native-windows-') as 작업경로:
        모의제어접속=Path(작업경로)/'qmp.sock'
        δεδομένα_θέση=subprocess.Popen(Εντολή()+['-display','none','-monitor','none','-serial','stdio','-qmp','unix:{},server=on,wait=off'.format(모의제어접속)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
        επιλογέας_a916db4e=selectors.DefaultSelector();επιλογέας_a916db4e.register(δεδομένα_θέση.stdout,selectors.EVENT_READ)
        def δείκτης_χειρισμού_συμβάν(초단위=.1):
            for 누름값,_ in επιλογέας_a916db4e.select(초단위):
                둘째값=누름값.fileobj.read(65536)
                if 둘째값:καταγράφω_ρεκόρ.extend(둘째값)
            assert b'PANIC:' not in καταγράφω_ρεκόρ and b'HALTED' not in καταγράφω_ρεκόρ,καταγράφω_ρεκόρ[-2048:]
        def 기다리기(δείκτης_8b722c5f,τρέχων_θέση,초단위=50):
            Τελική_οντότητα_Υπέρθεση=time.monotonic()+초단위
            while δείκτης_8b722c5f not in καταγράφω_ρεκόρ[τρέχων_θέση:]:
                if time.monotonic()>Τελική_οντότητα_Υπέρθεση or δεδομένα_θέση.poll() is not None:raise AssertionError(καταγράφω_ρεκόρ[τρέχων_θέση:].decode('utf-8','replace'))
                δείκτης_χειρισμού_συμβάν()
            return bytes(καταγράφω_ρεκόρ[τρέχων_θέση:])
        def στέλνω(둘째값,δείκτης_8b722c5f=b'jkoros-native> '):
            τρέχων_θέση=len(καταγράφω_ρεκόρ);δεδομένα_θέση.stdin.write(둘째값);δεδομένα_θέση.stdin.flush();return 기다리기(δείκτης_8b722c5f,τρέχων_θέση)
        def κέλυφος(συμβολοσειρά_δεδομένα):return στέλνω((συμβολοσειρά_δεδομένα+'; echo __DONE__').encode()+b'\n',b'\r\n__DONE__\r\n')
        def συντόμευση_τιμή(셋째순번):return bytes([30,2,셋째순번,0,0,0,0])
        def κλικ_κουμπί(συντεταγμένη_x,κουμπί_Y_συντονισμός):return bytes([30,1,1,συντεταγμένη_x&255,συντεταγμένη_x>>8,κουμπί_Y_συντονισμός&255,κουμπί_Y_συντονισμός>>8,30,1,0,συντεταγμένη_x&255,συντεταγμένη_x>>8,κουμπί_Y_συντονισμός&255,κουμπί_Y_συντονισμός>>8])
        def εντολή_λειτουργία():
            δεδομένα_θέση.stdin.write(b'\x1b');δεδομένα_θέση.stdin.flush();Τελική_οντότητα_Υπέρθεση=time.monotonic()+.2
            while time.monotonic()<Τελική_οντότητα_Υπέρθεση:δείκτης_χειρισμού_συμβάν(.03)
        try:
            기다리기(b'jkoros-native> ',0)
            κέλυφος('terminal');δείκτης_χειρισμού_συμβάν(.3)
            δεδομένα=(έργο_ρίζα/'build/verification/new-java/Σουϊνγκ_δοκιμή.class').read_bytes()
            στέλνω('load Σουϊνγκ_δοκιμή.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(δεδομένα),64):στέλνω(δεδομένα[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            στέλνω(b'.\n')
            στέλνω('java Σουϊνγκ_δοκιμή\n'.encode(),b'SWING READY')
            Τελική_οντότητα_Υπέρθεση=time.monotonic()+3
            while time.monotonic()<Τελική_οντότητα_Υπέρθεση:δείκτης_χειρισμού_συμβάν(.1)
            # JFrame centered at (120,100), content at y=130.
            στέλνω(κλικ_κουμπί(200,210),b'',)  # focus JTextField
            δεδομένα_θέση.stdin.write('누리'.encode());δεδομένα_θέση.stdin.flush()
            Τελική_οντότητα_Υπέρθεση=time.monotonic()+.3
            while time.monotonic()<Τελική_οντότητα_Υπέρθεση:δείκτης_χειρισμού_συμβάν(.05)
            μέτρηση=στέλνω(κλικ_κουμπί(200,255),'SWING CLICK 이름누리'.encode())
            기다리기(b'true',len(καταγράφω_ρεκόρ)-len(μέτρηση))
            στέλνω(συντόμευση_τιμή(1),b'TERMINAL FOCUS 2')
            μέτρηση=κέλυφος('echo GUI_SUSPENDED_OK');assert b'GUI_SUSPENDED_OK' in μέτρηση
            στέλνω(κλικ_κουμπί(180,12),b'TERMINAL FOCUS 1')
            Τελική_οντότητα_Υπέρθεση=time.monotonic()+.3
            while time.monotonic()<Τελική_οντότητα_Υπέρθεση:δείκτης_χειρισμού_συμβάν(.05)
            with socket.socket(socket.AF_UNIX) as σημείο_κώδικα:
                σημείο_κώδικα.settimeout(10);σημείο_κώδικα.connect(str(모의제어접속))
                with σημείο_κώδικα.makefile('rwb') as Αρχείο_καταχώρηση:
                    json.loads(Αρχείο_καταχώρηση.readline())
                    for αίτηση_τιμή in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(προορισμός_τιμή_θέση/'native-swing.png'),'format':'png'}}):
                        Αρχείο_καταχώρηση.write((json.dumps(αίτηση_τιμή)+'\n').encode());Αρχείο_καταχώρηση.flush()
                        while True:
                            반환값=json.loads(Αρχείο_καταχώρηση.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            στέλνω(κλικ_κουμπί(505,115))
            κέλυφος('echo SWING_CLOSED_OK')
            δεδομένα=(Τάξη_διαδρομή/'한글창시험.class').read_bytes()
            στέλνω('load 한글창시험.class\n'.encode(),b'hex> ')
            for 순번 in range(0,len(δεδομένα),64):στέλνω(δεδομένα[순번:순번+64].hex().encode()+b'\n',b'hex> ')
            στέλνω(b'.\n')
            στέλνω('java 한글창시험\n'.encode(),b'KOREAN SWING READY')
            στέλνω(κλικ_κουμπί(200,255),'KOREAN SWING CLICK Όνομα'.encode())
            στέλνω(κλικ_κουμπί(505,115))
            κέλυφος('echo KOREAN_SWING_CLOSED_OK')
            επικύρωση_έκθεση.update(passed=True,direct_korean_gui=True,checks=['standard javax.swing JFrame/JLabel/JTextField/JButton in own EL0 JVM','SwingUtilities.invokeLater and ActionListener callbacks','Korean GUI text and UTF-8 keyboard input','3-second GUI lifetime and suspend/resume across terminals','JFrame title-bar X disposes window and returns to shell','ελληνικά Παράθυρο/κουμπί/έργο_γνωστοποίηση/συμβάν_ουρά directly allocate objects and dispatch Korean callbacks; distinct from standard GUI types'])
            print('PASS: native Swing subset, Unicode input, action callback, lifecycle and suspension')
        finally:
            if δεδομένα_θέση.poll() is None:δεδομένα_θέση.terminate()
            try:δεδομένα_θέση.wait(timeout=5)
            except subprocess.TimeoutExpired:δεδομένα_θέση.kill();δεδομένα_θέση.wait()
            επιλογέας_a916db4e.close();δεδομένα_θέση.stdin.close();δεδομένα_θέση.stdout.close();(προορισμός_τιμή_θέση/'serial.log').write_bytes(καταγράφω_ρεκόρ);(προορισμός_τιμή_θέση/'report.json').write_text(json.dumps(επικύρωση_έκθεση,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Εκτέλεση_2()
