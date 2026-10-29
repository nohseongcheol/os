#!/usr/bin/env python3
"""πραγματικός_δεδομένα QEMU/VNC에서 화면 Μέγεθος·όριο_τιμή·Παράθυρο μετακινώ_τιμή_83b651b8·Swing·언어별 그리기를 검사한다."""
import ftplib
import hashlib
import io
import json
import re
import selectors
import socket
import struct
import subprocess
import time
from PIL import Image
from υπολογιστής_Προβολή import 정확한값
from εκτελώ_εντολή import έργο_ρίζα


def ανάλυση_δοκιμή(너비, ύψος_τιμή, μέτρηση_διαδρομή):
    with socket.socket() as 임시:
        임시.bind(('127.0.0.1', 0)); αριθμός_θύρας = 임시.getsockname()[1]
    αλλάζω_μέγεθος_μήνυμα = '{}x{}'.format(너비, ύψος_τιμή)
    διεργασία_τιμή = subprocess.Popen(['python3', str(έργο_ρίζα/'Εργαλεία/εκτελώ_εντολή.py'), '--desktop', '--network', '--port', '0',
        '--ftp-port', str(αριθμός_θύρας), '--resolution', αλλάζω_μέγεθος_μήνυμα], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
    επιλογέας_a916db4e = selectors.DefaultSelector(); επιλογέας_a916db4e.register(διεργασία_τιμή.stdout, selectors.EVENT_READ)
    καταγράφω_ρεκόρ = bytearray(); απομακρυσμένος_τιμή = None; Μεταφορά_τιμή = None

    def 기다리기(εμφανίζω_τιμή, Εκτέλεση_2=0):
        προθεσμία_τιμή = time.monotonic() + 60
        while εμφανίζω_τιμή not in καταγράφω_ρεκόρ[Εκτέλεση_2:]:
            if time.monotonic() > προθεσμία_τιμή or διεργασία_τιμή.poll() is not None or b'HALTED' in καταγράφω_ρεκόρ or b'PANIC:' in καταγράφω_ρεκόρ:
                raise AssertionError(καταγράφω_ρεκόρ[Εκτέλεση_2:].decode('utf-8', 'replace'))
            for Συμβάν, _ in επιλογέας_a916db4e.select(.1):
                δεδομένα = Συμβάν.fileobj.read(65536)
                if δεδομένα: καταγράφω_ρεκόρ.extend(δεδομένα)
        return καταγράφω_ρεκόρ[Εκτέλεση_2:].decode('utf-8', 'replace')

    def κλικ_κουμπί(σύμβολο, 눌림=True): απομακρυσμένος_τιμή.sendall(struct.pack('>BBHI', 4, int(눌림), 0, σύμβολο))

    def αποστολή_μηνύματος(Κείμενο):
        Εκτέλεση_2 = len(καταγράφω_ρεκόρ)
        for χαρακτήρας_τιμή in Κείμενο:
            σύμβολο = 0xff0d if χαρακτήρας_τιμή == '\n' else ord(χαρακτήρας_τιμή) if ord(χαρακτήρας_τιμή) < 256 else 0x1000000 | ord(χαρακτήρας_τιμή)
            κλικ_κουμπί(σύμβολο); κλικ_κουμπί(σύμβολο, False)
        return Εκτέλεση_2

    def κέλυφος(Κείμενο): return 기다리기(b'\r\n__RESOLUTION_DONE__\r\n', αποστολή_μηνύματος(Κείμενο+'; echo __RESOLUTION_DONE__\n'))

    def 가리키기(가로, τομέας_θέση, 눌림): απομακρυσμένος_τιμή.sendall(struct.pack('>BBHH', 5, 눌림, 가로, τομέας_θέση))

    def κλικ_τιμή(가로, τομέας_θέση): 가리키기(가로, τομέας_θέση, 1); 가리키기(가로, τομέας_θέση, 0)

    def 화상():
        # 비증분 요청의 모든 사각형을 합친다. 각 화소의 stride도 πραγματικός_δεδομένα 너비를 쓴다.
        απομακρυσμένος_τιμή.sendall(struct.pack('>BBHHHH', 3, 0, 0, 0, 너비, ύψος_τιμή))
        σχέδιο_τιμή = Image.new('RGB', (너비, ύψος_τιμή)); περιοχή_τιμή_9285603e = 0
        while True:
            종류 = 정확한값(απομακρυσμένος_τιμή, 1)[0]
            if 종류 == 2: continue
            if 종류 == 3:
                διάρκεια_τιμή = struct.unpack('>I', 정확한값(απομακρυσμένος_τιμή, 7)[3:])[0]; 정확한값(απομακρυσμένος_τιμή, διάρκεια_τιμή); continue
            assert 종류 == 0, 종류
            개수 = struct.unpack('>H', 정확한값(απομακρυσμένος_τιμή, 3)[1:])[0]
            for _ in range(개수):
                가로, τομέας_θέση, 폭, διάρκεια_τιμή, κωδικοποίηση_τιμή = struct.unpack('>HHHHi', 정확한값(απομακρυσμένος_τιμή, 12))
                assert κωδικοποίηση_τιμή == 0 and 가로+폭 <= 너비 and τομέας_θέση+διάρκεια_τιμή <= ύψος_τιμή
                σχέδιο_τιμή.paste(Image.frombytes('RGB', (폭, διάρκεια_τιμή), 정확한값(απομακρυσμένος_τιμή, 폭*διάρκεια_τιμή*4), 'raw', 'BGRX'), (가로, τομέας_θέση))
                περιοχή_τιμή_9285603e += 폭*διάρκεια_τιμή
            if περιοχή_τιμή_9285603e:
                assert περιοχή_τιμή_9285603e == 너비*ύψος_τιμή, περιοχή_τιμή_9285603e
                return σχέδιο_τιμή

    def 화소확인(συντονισμός_τιμή, 색):
        προθεσμία_τιμή = time.monotonic()+10
        while True:
            σχέδιο_τιμή = 화상()
            if σχέδιο_τιμή.getpixel(συντονισμός_τιμή) == 색: return σχέδιο_τιμή
            if time.monotonic() > προθεσμία_τιμή: raise AssertionError((συντονισμός_τιμή, σχέδιο_τιμή.getpixel(συντονισμός_τιμή), 색))

    def ανεβάζω_Αρχεία(Όνομα, δεδομένα): Μεταφορά_τιμή.storbinary('STOR '+Όνομα, io.BytesIO(δεδομένα))

    try:
        기다리기(b'TERMINAL READY')
        assert ('FRAMEBUFFER PASS '+αλλάζω_μέγεθος_μήνυμα+' RGB32').encode() in καταγράφω_ρεκόρ
        print('BOOT:', αλλάζω_μέγεθος_μήνυμα, flush=True)
        원격번호 = int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)', καταγράφω_ρεκόρ).group(1))
        απομακρυσμένος_τιμή = socket.create_connection(('127.0.0.1', 원격번호), timeout=20)
        assert 정확한값(απομακρυσμένος_τιμή, 12) == b'RFB 003.008\n'; απομακρυσμένος_τιμή.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(απομακρυσμένος_τιμή, 정확한값(απομακρυσμένος_τιμή, 1)[0]); απομακρυσμένος_τιμή.sendall(b'\x01')
        assert 정확한값(απομακρυσμένος_τιμή, 4) == b'\0'*4; απομακρυσμένος_τιμή.sendall(b'\x01')
        αρχική_κατάσταση = 정확한값(απομακρυσμένος_τιμή, 24); assert struct.unpack('>HH', αρχική_κατάσταση[:4]) == (너비, ύψος_τιμή)
        정확한값(απομακρυσμένος_τιμή, struct.unpack('>I', αρχική_κατάσταση[20:])[0])
        απομακρυσμένος_τιμή.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x', 32, 24, 0, 1, 255, 255, 255, 16, 8, 0))
        απομακρυσμένος_τιμή.sendall(struct.pack('>BBHi', 2, 0, 1, 0))
        화소확인((너비-1, ύψος_τιμή-1), (24, 32, 48))
        # 화면 오른쪽 아래까지 이동한다. 이전 640×480 όριο_τιμή 밖에서 X를 누른다.
        가리키기(40, 60, 1); 가리키기(너비-568+28, ύψος_τιμή-360+12, 1); 가리키기(너비-568+28, ύψος_τιμή-360+12, 0)
        화소확인((너비-568, ύψος_τιμή-360), (32, 80, 144))
        Εκτέλεση_2 = len(καταγράφω_ρεκόρ); κλικ_τιμή(너비-20, ύψος_τιμή-345); 기다리기(b'TERMINAL FOCUS 1', Εκτέλεση_2)
        화소확인((너비-568, ύψος_τιμή-360), (24, 32, 48))
        Εκτέλεση_2 = len(καταγράφω_ρεκόρ); κλικ_τιμή(80, 16); 기다리기(b'TERMINAL FOCUS 1', Εκτέλεση_2)
        κέλυφος('ftpd start')
        Μεταφορά_τιμή = ftplib.FTP(); Μεταφορά_τιμή.encoding = 'utf-8'; Μεταφορά_τιμή.connect('127.0.0.1', αριθμός_θύρας, timeout=20); Μεταφορά_τιμή.login()
        # C όριο_τιμή 검사는 32비트 unsigned 음수 μετατρέπω_τιμή·απόσπασμα 밖·빈 사각형을 포함한다.
        ΠΗΓΗ = '''#include <화면규약.h>
#include <파일규약.h>
int main(void) {
    unsigned 너비=화면너비(), ύψος_τιμή=화면높이();
    if(너비!=WIDTH || ύψος_τιμή!=HEIGHT) return 1;
    if(Σχεδίαση_ορθογώνιο(너비,ύψος_τιμή,0,0,0)) return 2;
    if(Σχεδίαση_ορθογώνιο(너비,ύψος_τιμή-1,1,1,0)!=-22) return 3;
    if(Σχεδίαση_ορθογώνιο(너비-1,ύψος_τιμή,1,1,0)!=-22) return 4;
    if(Σχεδίαση_ορθογώνιο(-1,0,1,1,0)!=-22) return 5;
    if(Σχεδίαση_ορθογώνιο(0,0,-1,1,0)!=-22) return 6;
    if(Σχεδίαση_ορθογώνιο(너비-1,ύψος_τιμή-1,1,1,0x332211)) return 7;
    εγγράφω_Αρχείο_δεδομένα(1,"C RESOLUTION PASS\\n",18);
    그림기다리기(); return 0;
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ύψος_τιμή))
        ανεβάζω_Αρχεία('화면시험.c', ΠΗΓΗ.encode())
        assert 'exit 0' in κέλυφος('cc /화면시험.c -o /화면시험')
        기다리기(b'C RESOLUTION PASS', αποστολή_μηνύματος('run /화면시험\n'))
        화소확인((너비-1, ύψος_τιμή-1), (17, 34, 51))
        기다리기(b'jkoros-native> ', αποστολή_μηνύματος('q'))
        ΠΗΓΗ = '''from ελληνικά import 화면크기, Σχεδίαση_ορθογώνιο, 그림기다리기, Έξοδος, σφάλμα_συστήματος
너비, ύψος_τιμή = 화면크기()
assert (너비, ύψος_τιμή) == (WIDTH, HEIGHT)
try:
    Σχεδίαση_ορθογώνιο(너비, ύψος_τιμή-1, 1, 1, 0)
    raise AssertionError("boundary")
except σφάλμα_συστήματος as ΣΦΑΛΜΑ:
    assert ΣΦΑΛΜΑ.Ευρετήριο == 22
Σχεδίαση_ορθογώνιο(너비-1, ύψος_τιμή-1, 1, 1, 0x665544)
Έξοδος("PYTHON RESOLUTION PASS")
그림기다리기()
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ύψος_τιμή))
        ανεβάζω_Αρχεία('화면시험.py', ΠΗΓΗ.encode())
        기다리기(b'PYTHON RESOLUTION PASS', αποστολή_μηνύματος('python /화면시험.py\n'))
        화소확인((너비-1, ύψος_τιμή-1), (68, 85, 102))
        기다리기(b'jkoros-native> ', αποστολή_μηνύματος('q'))
        ΠΗΓΗ = '''import ελληνικά.ίδιο.*;
public class ανάλυση_δοκιμή {
    public static void main(String[] Παράμετροι) {
        int 너비=화면.너비(), ύψος_τιμή=화면.ύψος_τιμή();
        if (너비!=WIDTH || ύψος_τιμή!=HEIGHT) throw new Κατάσταση_εξαίρεση("Μέγεθος");
        try { 화면.ορθογώνιο(너비,ύψος_τιμή-1,1,1,0); throw new Κατάσταση_εξαίρεση("απόσπασμα"); }
        catch (άκυρος_όρισμα_εξαίρεση ΣΦΑΛΜΑ) { }
        화면.διαγράφω_καταχώρηση(0x302018);
        화면.ορθογώνιο(너비-1,ύψος_τιμή-1,1,1,0x998877);
        System.out.println("JAVA RESOLUTION PASS");
        화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ύψος_τιμή))
        # εξαίρεση 처리는 φιλοξενώ javac 결과를 ίδιο JVM에 올려 검사한다.
        όριο_προέλευση = μέτρηση_διαδρομή/'해상도경계시험.java'
        όριο_προέλευση.write_text(ΠΗΓΗ.replace('class ανάλυση_δοκιμή', 'class 해상도경계시험'))
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(έργο_ρίζα/'dist/jkoros-native-korean.jar'), '-d', str(μέτρηση_διαδρομή), str(όριο_προέλευση)])
        ανεβάζω_Αρχεία('해상도경계시험.class', (μέτρηση_διαδρομή/'해상도경계시험.class').read_bytes())
        기다리기(b'JAVA RESOLUTION PASS', αποστολή_μηνύματος('java 해상도경계시험\n'))
        화소확인((너비-1, ύψος_τιμή-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', αποστολή_μηνύματος('q'))
        # 게스트 javac의 στήριγμα_τιμή 문법으로 Μέγεθος ερώτημα_τιμή·διαγράφω_καταχώρηση·다섯 Παράμετροι 그리기를 컴파일한다.
        ΠΗΓΗ = '''public class ανάλυση_δοκιμή {
    public static void main(String[] Παράμετροι) {
        int 너비=ελληνικά.ίδιο.화면.너비();
        int ύψος_τιμή=ελληνικά.ίδιο.화면.ύψος_τιμή();
        if (너비!=WIDTH || ύψος_τιμή!=HEIGHT) return;
        ελληνικά.ίδιο.화면.διαγράφω_καταχώρηση(3153944);
        ελληνικά.ίδιο.화면.ορθογώνιο(너비-1,ύψος_τιμή-1,1,1,10061943);
        ελληνικά.ίδιο.Έξοδος.εγγράφω_γραμμή("JAVA RESOLUTION PASS");
        ελληνικά.ίδιο.화면.기다리기();
    }
}
'''.replace('WIDTH', str(너비)).replace('HEIGHT', str(ύψος_τιμή))
        ανεβάζω_Αρχεία('ανάλυση_δοκιμή.java', ΠΗΓΗ.encode())
        μέτρηση = κέλυφος('javac ανάλυση_δοκιμή.java'); assert 'exit 0' in μέτρηση, μέτρηση
        기다리기(b'JAVA RESOLUTION PASS', αποστολή_μηνύματος('java ανάλυση_δοκιμή\n'))
        화소확인((너비-1, ύψος_τιμή-1), (119, 136, 153))
        기다리기(b'jkoros-native> ', αποστολή_μηνύματος('q'))
        ανεβάζω_Αρχεία('Σουϊνγκ_δοκιμή.class', (μέτρηση_διαδρομή/'Σουϊνγκ_δοκιμή.class').read_bytes())
        기다리기(b'SWING READY', αποστολή_μηνύματος('java Σουϊνγκ_δοκιμή\n'))
        가로, τομέας_θέση = (너비-400)//2, (ύψος_τιμή-280)//2
        σχέδιο_τιμή = 화소확인((가로, τομέας_θέση), (32, 80, 144))
        σχέδιο_τιμή.save(str(μέτρηση_διαδρομή/(αλλάζω_μέγεθος_μήνυμα+'.png')))
        Εκτέλεση_2 = len(καταγράφω_ρεκόρ); κλικ_τιμή(가로+80, τομέας_θέση+155)
        기다리기('SWING CLICK Όνομα'.encode(), Εκτέλεση_2)
        Εκτέλεση_2 = len(καταγράφω_ρεκόρ); κλικ_τιμή(가로+385, τομέας_θέση+15); 기다리기(b'jkoros-native> ', Εκτέλεση_2)
        assert 'AFTER_RESOLUTION' in κέλυφος('echo AFTER_RESOLUTION')
        print('PASS:', αλλάζω_μέγεθος_μήνυμα, 'RGB32, VNC, terminal drag/close, C/Python/Java bounds, centered Swing callbacks', flush=True)
    finally:
        if Μεταφορά_τιμή: Μεταφορά_τιμή.close()
        if απομακρυσμένος_τιμή: απομακρυσμένος_τιμή.close()
        if διεργασία_τιμή.poll() is None:
            διεργασία_τιμή.terminate()
            try: διεργασία_τιμή.wait(timeout=8)
            except subprocess.TimeoutExpired: διεργασία_τιμή.kill(); διεργασία_τιμή.wait()
        επιλογέας_a916db4e.close(); διεργασία_τιμή.stdout.close()
        (μέτρηση_διαδρομή/(αλλάζω_μέγεθος_μήνυμα+'.log')).write_bytes(καταγράφω_ρεκόρ)


def Εκτέλεση_2():
    μέτρηση_διαδρομή = έργο_ρίζα/'build/verification/resolution'; μέτρηση_διαδρομή.mkdir(parents=True, exist_ok=True)
    καταγράφω_ρεκόρ = {'passed': False, 'kernel_sha256': hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(), 'resolutions': []}
    try:
        for άκυρος_τιμή in ('0x0', '639x480', '1920x1081', '1921x1080', '1920*1080'):
            μέτρηση = subprocess.run(['python3', str(έργο_ρίζα/'Εργαλεία/εκτελώ_εντολή.py'), '--resolution', άκυρος_τιμή], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            assert μέτρηση.returncode == 2 and b'--resolution' in μέτρηση.stderr
        subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(μέτρηση_διαδρομή), str(έργο_ρίζα/'시험/자바/Σουϊνγκ_δοκιμή.java')])
        for 너비, ύψος_τιμή in ((1920,1080), (1280,720), (640,480)):
            ανάλυση_δοκιμή(너비, ύψος_τιμή, μέτρηση_διαδρομή); καταγράφω_ρεκόρ['resolutions'].append([너비, ύψος_τιμή])
        καταγράφω_ρεκόρ.update(passed=True, linux_loaded=False, physical_board_tested=False,
            checks=['RFB actual geometry and full-frame RGB32 pixels', 'terminal drag and close at bottom right',
                    'guest cc/javac and Python: Korean size API, last pixel, rejected out-of-bounds drawing',
                    'Swing centered placement, button callback and X', 'desktop and FTP networking together', 'invalid CLI sizes rejected'])
    finally:
        (μέτρηση_διαδρομή/'report.json').write_text(json.dumps(καταγράφω_ρεκόρ, ensure_ascii=False, indent=2)+'\n')


if __name__ == '__main__': Εκτέλεση_2()
