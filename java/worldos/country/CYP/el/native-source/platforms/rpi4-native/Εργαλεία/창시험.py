#!/usr/bin/env python3
"""Actual EL0 vi, independently preserved terminal sessions and process snapshots."""
import hashlib,json,re,selectors,socket,subprocess,tempfile,time
from pathlib import Path
from εκτελώ_εντολή import έργο_ρίζα,Εντολή

def Εκτέλεση_2():
    προορισμός_τιμή_θέση=έργο_ρίζα/'build/verification/windows';προορισμός_τιμή_θέση.mkdir(parents=True,exist_ok=True)
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
            κέλυφος('mkdir first; cd first; export NAME=one')
            στέλνω('vi 첫째.py\n'.encode(),b'NORMAL')
            στέλνω('i값 = 21\nprint(τιμή * 2)\n'.encode(),b'INSERT')
            # A live editor survives the old two-second deadline and can be suspended.
            Τελική_οντότητα_Υπέρθεση=time.monotonic()+3
            while time.monotonic()<Τελική_οντότητα_Υπέρθεση:δείκτης_χειρισμού_συμβάν(.1)
            στέλνω(συντόμευση_τιμή(1),b'TERMINAL FOCUS 2');δείκτης_χειρισμού_συμβάν(.2)
            assert b'/\r\n' in κέλυφος('pwd')
            κέλυφος('export NAME=two')
            στέλνω('vi 둘째.txt\n'.encode(),b'NORMAL')
            στέλνω('i두 번째 Παράθυρο\n'.encode(),b'INSERT')
            στέλνω(κλικ_κουμπί(180,12),b'TERMINAL FOCUS 1');δείκτης_χειρισμού_συμβάν(.2)
            εντολή_λειτουργία();στέλνω(b':wq\r')
            assert b'one:/first' in κέλυφος('echo "$NAME:$PWD"')
            assert 'τιμή = 21\r\nprint(τιμή * 2)'.encode() in κέλυφος('cat 첫째.py')
            μέτρηση=κέλυφος('python 첫째.py');assert b'42\r\n' in μέτρηση,μέτρηση
            # Close the first shell with its actual title-bar X; second editor resumes.
            στέλνω(κλικ_κουμπί(560,63),b'TERMINAL FOCUS 2');δείκτης_χειρισμού_συμβάν(.2)
            εντολή_λειτουργία();στέλνω(b':wq\r')
            assert b'two:/' in κέλυφος('echo "$NAME:$PWD"')
            assert '두 번째 Παράθυρο'.encode() in κέλυφος('cat 둘째.txt')
            # Edit persisted text, undo, refuse an unsaved quit, then explicitly discard.
            στέλνω('vi 둘째.txt\n'.encode(),b'NORMAL');στέλνω(b'xu',b'NORMAL')
            στέλνω(b'iX',b'INSERT');εντολή_λειτουργία();στέλνω(b':q\r',b'Unsaved')
            στέλνω(b':q!\r');assert '두 번째 Παράθυρο'.encode() in κέλυφος('cat 둘째.txt')
            στέλνω(συντόμευση_τιμή(1),b'TERMINAL FOCUS 1');δείκτης_χειρισμού_συμβάν(.2)
            στέλνω(συντόμευση_τιμή(1),b'TERMINAL FOCUS 3');δείκτης_χειρισμού_συμβάν(.2)
            στέλνω(συντόμευση_τιμή(1),b'TERMINAL FOCUS 4');δείκτης_χειρισμού_συμβάν(.2)
            # Drag the fourth terminal, then close a running editor with unsaved text.
            δεδομένα_θέση.stdin.write(bytes([30,1,1,200,0,116,0,30,1,1,170,0,96,0,30,1,0,170,0,96,0]));δεδομένα_θέση.stdin.flush()
            κέλυφος('echo DRAGGED_OK')
            στέλνω('vi 버릴문서.txt\n'.encode(),b'NORMAL')
            στέλνω('i저장하지 않은 δεδομένα'.encode(),b'INSERT')
            στέλνω(κλικ_κουμπί(578,97),b'TERMINAL FOCUS 3');δείκτης_χειρισμού_συμβάν(.2)
            assert '버릴문서.txt'.encode() not in κέλυφος('ls')
            στέλνω(συντόμευση_τιμή(1),b'TERMINAL FOCUS 4');δείκτης_χειρισμού_συμβάν(.2)
            κέλυφος('echo REUSED_WINDOW_OK')
            Ολοκληρωμένες_ποσό=καταγράφω_ρεκόρ.rfind(b'\r\n__DONE__\r\n')+len(b'\r\n__DONE__\r\n')
            기다리기(b'jkoros-native> ',Ολοκληρωμένες_ποσό)
            # UART completion precedes the next QEMU display refresh.
            Τελική_οντότητα_Υπέρθεση=time.monotonic()+.3
            while time.monotonic()<Τελική_οντότητα_Υπέρθεση:δείκτης_χειρισμού_συμβάν(.05)
            with socket.socket(socket.AF_UNIX) as σημείο_κώδικα:
                σημείο_κώδικα.settimeout(10);σημείο_κώδικα.connect(str(모의제어접속))
                with σημείο_κώδικα.makefile('rwb') as Αρχείο_καταχώρηση:
                    json.loads(Αρχείο_καταχώρηση.readline())
                    for αίτηση_τιμή in ({'execute':'qmp_capabilities'},{'execute':'screendump','arguments':{'filename':str(προορισμός_τιμή_θέση/'four-terminals.png'),'format':'png'}}):
                        Αρχείο_καταχώρηση.write((json.dumps(αίτηση_τιμή)+'\n').encode());Αρχείο_καταχώρηση.flush()
                        while True:
                            반환값=json.loads(Αρχείο_καταχώρηση.readline())
                            if 'error' in 반환값:raise AssertionError(반환값)
                            if 'return' in 반환값:break
            from PIL import Image
            화소들=Image.open(str(προορισμός_τιμή_θέση/'four-terminals.png')).convert('RGB')
            for ζεύγος_συντεταγμένων,색상 in [((12,48),(56,68,96)),((590,66),(56,68,96)),((44,84),(56,68,96)),((60,102),(32,80,144))]:
                assert 화소들.getpixel(ζεύγος_συντεταγμένων)==색상,(ζεύγος_συντεταγμένων,화소들.getpixel(ζεύγος_συντεταγμένων))
            κέλυφος('echo FOUR_WINDOWS_OK')
            επικύρωση_έκθεση.update(passed=True,checks=['EL0 UTF-8 vi create/save/edit/undo/unsaved quit/discard','interactive editor survives 3 seconds','two suspended vi instances preserve memory/registers and independent cwd/env','dragged title-bar X terminates unsaved vi, frees process, and permits window reuse','four native terminal windows','Korean Python identifiers compile and run after vi save'])
            print('PASS: native four-window desktop, independent shells, suspended EL0 vi, Korean coding')
        finally:
            if δεδομένα_θέση.poll() is None:δεδομένα_θέση.terminate()
            try:δεδομένα_θέση.wait(timeout=5)
            except subprocess.TimeoutExpired:δεδομένα_θέση.kill();δεδομένα_θέση.wait()
            επιλογέας_a916db4e.close();δεδομένα_θέση.stdin.close();δεδομένα_θέση.stdout.close();(προορισμός_τιμή_θέση/'serial.log').write_bytes(καταγράφω_ρεκόρ);(προορισμός_τιμή_θέση/'report.json').write_text(json.dumps(επικύρωση_έκθεση,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':Εκτέλεση_2()
