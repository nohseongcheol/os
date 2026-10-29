#!/usr/bin/env python3
"""Run all examples in the real combined VNC + SLIP/FTP native VM."""
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
from pathlib import Path
from υπολογιστής_Προβολή import 정확한값
from 예제되돌림서버 import ηχώ_Διακομιστές
from εκτελώ_εντολή import έργο_ρίζα


def δοκιμή_Γλώσσα(Γλώσσα,ηχώ_διακομιστής_καταχώρηση,μέτρηση_δεδομένα):
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1',0));μεταφορά_αρχείων_αριθμός_θύρας=임시자원.getsockname()[1]
    Διεργασία=subprocess.Popen(['python3',str(έργο_ρίζα/'Εργαλεία/εκτελώ_εντολή.py'),'--desktop','--network','--port','0','--ftp-port',str(μεταφορά_αρχείων_αριθμός_θύρας)],
        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
    επιλογέας=selectors.DefaultSelector();επιλογέας.register(Διεργασία.stdout,selectors.EVENT_READ)
    μεταγραφή=bytearray();πελάτης=None;μεταφορά_αρχείων_σύνδεση=None
    def λαμβάνω_μήνυμα(δείκτης_8b722c5f,Εκτέλεση_2=0):
        Τελική_οντότητα_Υπέρθεση=time.monotonic()+60
        while δείκτης_8b722c5f not in μεταγραφή[Εκτέλεση_2:]:
            if time.monotonic()>Τελική_οντότητα_Υπέρθεση or Διεργασία.poll() is not None:raise AssertionError(μεταγραφή[Εκτέλεση_2:].decode('utf-8','replace'))
            for 누름값,_ in επιλογέας.select(.1):
                δεδομένα=누름값.fileobj.read(65536)
                if δεδομένα:μεταγραφή.extend(δεδομένα)
        return μεταγραφή[Εκτέλεση_2:].decode('utf-8','replace').replace('\r\n','\n')
    def 누름값(σύμβολο_τιμή,누르는중=True):πελάτης.sendall(struct.pack('>BBHI',4,int(누르는중),0,σύμβολο_τιμή))
    def αρχή_Υπέρθεση(Γραμμή):
        Εκτέλεση_2=len(μεταγραφή)
        for σημείο_κώδικα in Γραμμή+'\n':
            σύμβολο_τιμή=0xff0d if σημείο_κώδικα=='\n' else ord(σημείο_κώδικα) if ord(σημείο_κώδικα)<256 else 0x1000000|ord(σημείο_κώδικα)
            누름값(σύμβολο_τιμή);누름값(σύμβολο_τιμή,False)
        return Εκτέλεση_2
    def κέλυφος(Γραμμή):return λαμβάνω_μήνυμα(b'jkoros-native> ',αρχή_Υπέρθεση(Γραμμή))
    def εκτελώ_εντολή(Γραμμή,예상결과):
        Κείμενο=κέλυφος(Γραμμή);assert 예상결과 in Κείμενο and 'exit 0' in Κείμενο,(Γραμμή,Κείμενο)
        return Κείμενο
    def 화소들():
        πελάτης.sendall(struct.pack('>BBHHHH',3,0,0,0,640,480))
        빛삼원색=bytearray(640*480*3)
        while True:
            περιοχή_τιμή=정확한값(πελάτης,1)[0]
            if περιοχή_τιμή==2:continue
            if περιοχή_τιμή==3:
                개수=struct.unpack('>I',정확한값(πελάτης,7)[3:])[0];정확한값(πελάτης,개수);continue
            assert περιοχή_τιμή==0,περιοχή_τιμή
            항목수=struct.unpack('>H',정확한값(πελάτης,3)[1:])[0]
            for _ in range(항목수):
                συντεταγμένη_x,κουμπί_Y_συντονισμός,너비값,ζητήθηκε_ύψος_τιμή,σύνολο_χαρακτήρων=struct.unpack('>HHHHi',정확한값(πελάτης,12));assert σύνολο_χαρακτήρων==0,σύνολο_χαρακτήρων
                δεδομένα=정확한값(πελάτης,너비값*ζητήθηκε_ύψος_τιμή*4)
                for σειρά_θέση in range(ζητήθηκε_ύψος_τιμή):
                    for στήλη_θέση in range(너비값):
                        원본자료=(σειρά_θέση*너비값+στήλη_θέση)*4;τιμή_στόχος=((κουμπί_Y_συντονισμός+σειρά_θέση)*640+συντεταγμένη_x+στήλη_θέση)*3
                        빛삼원색[τιμή_στόχος:τιμή_στόχος+3]=bytes((δεδομένα[원본자료+2],δεδομένα[원본자료+1],δεδομένα[원본자료]))
            if 항목수:return 빛삼원색
    try:
        λαμβάνω_μήνυμα(b'TERMINAL READY');λαμβάνω_μήνυμα(b'jkoros-native> ',μεταγραφή.rfind(b'TERMINAL READY'))
        αριθμός_θύρας=int(re.search(rb'DESKTOP VNC 127.0.0.1:(\d+)',μεταγραφή).group(1))
        πελάτης=socket.create_connection(('127.0.0.1',αριθμός_θύρας),timeout=10)
        assert 정확한값(πελάτης,12)==b'RFB 003.008\n';πελάτης.sendall(b'RFB 003.008\n')
        assert 1 in 정확한값(πελάτης,정확한값(πελάτης,1)[0]);πελάτης.sendall(b'\x01');assert 정확한값(πελάτης,4)==b'\0'*4
        πελάτης.sendall(b'\x01');초기값=정확한값(πελάτης,24);정확한값(πελάτης,struct.unpack('>I',초기값[20:])[0])
        πελάτης.sendall(b'\0\0\0\0'+struct.pack('>BBBBHHHBBB3x',32,24,0,1,255,255,255,16,8,0))
        πελάτης.sendall(struct.pack('>BBHi',2,0,1,0))
        assert 'FTP listening' in κέλυφος('ftpd start')
        μεταφορά_αρχείων_σύνδεση=ftplib.FTP();μεταφορά_αρχείων_σύνδεση.encoding='utf-8';μεταφορά_αρχείων_σύνδεση.connect('127.0.0.1',μεταφορά_αρχείων_αριθμός_θύρας,timeout=20);μεταφορά_αρχείων_σύνδεση.login()
        ωφέλιμο_φορτίο_δεδομένα=('GUI와 FTP 동시 χρήση_τιμή '+Γλώσσα+' 😀\n').encode()
        μεταφορά_αρχείων_σύνδεση.storbinary('STOR 함께.txt',io.BytesIO(ωφέλιμο_φορτίο_δεδομένα))
        assert ωφέλιμο_φορτίο_δεδομένα.decode().strip() in κέλυφος('cat /함께.txt')
        받은수=bytearray();μεταφορά_αρχείων_σύνδεση.retrbinary('RETR 함께.txt',받은수.extend);assert 받은수==ωφέλιμο_φορτίο_δεδομένα;μεταφορά_αρχείων_σύνδεση.delete('함께.txt')
        # No installation command: every language and the manual exist at boot.
        στέλνω_Λίστα=κέλυφος('ls /example')
        assert all(Όνομα in στέλνω_Λίστα for Όνομα in ('java/','c/','python/','README.md')),στέλνω_Λίστα
        if Γλώσσα=='java':
            πακέτο_διακήρυξη=json.loads((έργο_ρίζα/'build/examples/manifest.json').read_text())
            for ΔΙΑΔΡΟΜΗ,σημείο_εισόδου in πακέτο_διακήρυξη.items():
                κέλυφος('cp '+ΔΙΑΔΡΟΜΗ+' /example-check.bin')
                Περιεχόμενο_τιμή=bytearray();μεταφορά_αρχείων_σύνδεση.retrbinary('RETR example-check.bin',Περιεχόμενο_τιμή.extend)
                assert len(Περιεχόμενο_τιμή)==σημείο_εισόδου['bytes'] and hashlib.sha256(Περιεχόμενο_τιμή).hexdigest()==σημείο_εισόδου['sha256'],ΔΙΑΔΡΟΜΗ
            μεταφορά_αρχείων_σύνδεση.delete('example-check.bin')
            # Exercise packed file bytes, the last byte of a full file, and root
            # FTP listing for file slots above the former 16-entry limit.
            δυαδικός=bytes(range(256))*64
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR boundary.bin',io.BytesIO(δυαδικός))
            Περιεχόμενο_τιμή=bytearray();μεταφορά_αρχείων_σύνδεση.retrbinary('RETR boundary.bin',Περιεχόμενο_τιμή.extend)
            assert Περιεχόμενο_τιμή==δυαδικός and 'boundary.bin' in μεταφορά_αρχείων_σύνδεση.nlst()
            κέλυφος('cp /boundary.bin /boundary-copy.bin')
            Περιεχόμενο_τιμή=bytearray();μεταφορά_αρχείων_σύνδεση.retrbinary('RETR boundary-copy.bin',Περιεχόμενο_τιμή.extend)
            assert Περιεχόμενο_τιμή==δυαδικός
            μεταφορά_αρχείων_σύνδεση.delete('boundary.bin');μεταφορά_αρχείων_σύνδεση.delete('boundary-copy.bin')
        assert 'ΠαράδειγμαΕξόδου' in κέλυφος('ls /example/'+Γλώσσα)
        κέλυφος('cd /example/'+Γλώσσα)
        όνομα_πίνακας={'java':'JAVA','c':'C','python':'PYTHON'}[Γλώσσα]
        예상파일=όνομα_πίνακας+' Αρχείο: 한글 δεδομένα 😀\n'
        if Γλώσσα=='java':
            εκτελώ_εντολή('javac ΠαράδειγμαΕξόδου.java','Compiled:');εκτελώ_εντολή('java ΠαράδειγμαΕξόδου','JAVA Έξοδος: 안녕하세요 😀')
            εκτελώ_εντολή('javac ΠαράδειγμαΑρχείου.java','Compiled:');εκτελώ_εντολή('java ΠαράδειγμαΑρχείου',예상파일)
            εκτελώ_εντολή('java ΠαράδειγμαΔικτύου {} {}'.format(ηχώ_διακομιστής_καταχώρηση.θύρα_TCP,ηχώ_διακομιστής_καταχώρηση.전문접속번호),'JAVA 네트워크 επαληθεύω: TCP UDP 한글')
            γραφικά_εντολή='java ΠαράδειγμαΣχεδίου'
        elif Γλώσσα=='c':
            for Όνομα,전달값,예상결과 in [('Έξοδος','', 'C Έξοδος: 안녕하세요 😀'),('Αρχείο','',예상파일),
                    ('네트워크',' '+str(ηχώ_διακομιστής_καταχώρηση.전문접속번호),'C 네트워크 επαληθεύω: UDP 한글')]:
                εκτελώ_εντολή('cc '+Όνομα+'예제.c -o εκτελώ_εντολή','Compiled native ARM64 ELF:')
                εκτελώ_εντολή('./εκτελώ_εντολή'+전달값,예상결과)
            εκτελώ_εντολή('cc ΠαράδειγμαΣχεδίου.c -o εκτελώ_εντολή','Compiled native ARM64 ELF:');γραφικά_εντολή='./εκτελώ_εντολή'
        else:
            for Όνομα,전달값,예상결과 in [('Έξοδος','','PYTHON Έξοδος: 안녕하세요 😀'),('Αρχείο','',예상파일),
                    ('네트워크',' '+str(ηχώ_διακομιστής_καταχώρηση.전문접속번호),'PYTHON 네트워크 επαληθεύω: UDP 한글')]:
                εκτελώ_εντολή('python '+Όνομα+'예제.py'+전달값,예상결과)
            γραφικά_εντολή='python ΠαράδειγμαΣχεδίου.py'
        αρχή_σχέδιο=αρχή_Υπέρθεση(γραφικά_εντολή)
        Κείμενο=λαμβάνω_μήνυμα('그림을 확인한 Πίσω_τιμή Enter를 누르세요.\r\n'.encode(),αρχή_σχέδιο)
        assert όνομα_πίνακας+' 그래픽: 빨강 초록 파랑' in Κείμενο and 'exit 0' not in Κείμενο,Κείμενο
        # While EL0 waits for GUI input, kernel FTP must continue serving data.
        μεταφορά_αρχείων_σύνδεση.storbinary('STOR 도중.txt',io.BytesIO(b'FTP DURING GRAPHICS'))
        받은수=bytearray();μεταφορά_αρχείων_σύνδεση.retrbinary('RETR 도중.txt',받은수.extend);assert 받은수==b'FTP DURING GRAPHICS';μεταφορά_αρχείων_σύνδεση.delete('도중.txt')
        빛삼원색=화소들()
        for κουμπί_Y_συντονισμός,색상 in [(410,(255,0,0)),(435,(0,255,0)),(460,(0,0,255))]:
            Υπέρθεση_τιμή=(κουμπί_Y_συντονισμός*640+610)*3;assert tuple(빛삼원색[Υπέρθεση_τιμή:Υπέρθεση_τιμή+3])==색상,(Γλώσσα,κουμπί_Y_συντονισμός,tuple(빛삼원색[Υπέρθεση_τιμή:Υπέρθεση_τιμή+3]))
        from PIL import Image
        Image.frombytes('RGB',(640,480),bytes(빛삼원색)).save(str(μέτρηση_δεδομένα/(Γλώσσα+'-graphics.png')))
        누름값(0xff0d);누름값(0xff0d,False)
        assert 'exit 0' in λαμβάνω_μήνυμα(b'jkoros-native> ',αρχή_σχέδιο)
        if Γλώσσα=='java':
            αρχή_Παράθυρο=αρχή_Υπέρθεση('java ΠαράδειγμαΠαραθύρου')
            λαμβάνω_μήνυμα('GUI 예제 Προετοίμασε: ΠαράδειγμαΠαραθύρου'.encode(),αρχή_Παράθυρο)
            def κλικ_τιμή(가로,τομέας_θέση):
                for κουμπί in (1,0):πελάτης.sendall(struct.pack('>BBHH',5,κουμπί,가로,τομέας_θέση))
            time.sleep(.3)
            이전그림=Image.frombytes('RGB',(640,480),bytes(화소들()))
            κλικ_τιμή(160,196)
            for _ in range(2):누름값(0xff08);누름값(0xff08,False)
            for χαρακτήρας_τιμή in '한글':누름값(0x1000000|ord(χαρακτήρας_τιμή));누름값(0x1000000|ord(χαρακτήρας_τιμή),False)
            for 횟수 in (1,2):
                Εκτέλεση_2=len(μεταγραφή);κλικ_τιμή(180,242)
                λαμβάνω_μήνυμα(('GUI 인사: 안녕하세요, 한글님! ('+str(횟수)+')').encode(),Εκτέλεση_2)
            time.sleep(.3)
            Παράθυρο_σχέδιο=Image.frombytes('RGB',(640,480),bytes(화소들()))
            assert 이전그림.crop((110,272,530,300)).tobytes()!=Παράθυρο_σχέδιο.crop((110,272,530,300)).tobytes()
            Παράθυρο_σχέδιο.save(str(μέτρηση_δεδομένα/'java-swing.png'))
            Εκτέλεση_2=len(μεταγραφή);κλικ_τιμή(535,105)
            assert 'exit 0' in λαμβάνω_μήνυμα(b'jkoros-native> ',Εκτέλεση_2)
        # Download the guest-created bytes through FTP in the same GUI VM.
        Αρχείο_καταχώρηση_όνομα={'java':'java.txt','c':'c.txt','python':'python.txt'}[Γλώσσα]
        κέλυφος('cp '+Αρχείο_καταχώρηση_όνομα+' /επικυρώνω.txt')
        받은수=bytearray();μεταφορά_αρχείων_σύνδεση.retrbinary('RETR επικυρώνω.txt',받은수.extend);assert 받은수==예상파일.encode()
        κέλυφος('echo preserved > ΠαράδειγμαΕξόδου.'+('py' if Γλώσσα=='python' else Γλώσσα))
        assert 'EXAMPLES READY' in κέλυφος('example '+Γλώσσα)
        assert '\npreserved\n' in κέλυφος('cat ΠαράδειγμαΕξόδου.'+('py' if Γλώσσα=='python' else Γλώσσα))
        assert '한/μηδέν_τελεστέος Κλειδί_τιμή, Shift+Space 또는 F9' in κέλυφος('help ko')
        # VNC input remains usable while the FTP control/data connections are active.
        assert 'GUI NETWORK TOGETHER' in κέλυφος('echo GUI NETWORK TOGETHER')
        μεταφορά_αρχείων_σύνδεση.quit();μεταφορά_αρχείων_σύνδεση=None;assert 'FTP stopped' in κέλυφος('ftpd stop')
        print('PASS '+Γλώσσα+': Korean output, file bytes, external network and framebuffer in desktop+network VM',flush=True)
    finally:
        if μεταφορά_αρχείων_σύνδεση:
            try:μεταφορά_αρχείων_σύνδεση.close()
            except OSError:pass
        if πελάτης:πελάτης.close()
        Διεργασία.terminate()
        try:Διεργασία.wait(timeout=8)
        except subprocess.TimeoutExpired:Διεργασία.kill();Διεργασία.wait()
        επιλογέας.close();Διεργασία.stdout.close();(μέτρηση_δεδομένα/(Γλώσσα+'-serial.log')).write_bytes(μεταγραφή)


def Εκτέλεση_2():
    μέτρηση_δεδομένα=έργο_ρίζα/'build/verification/examples';μέτρηση_δεδομένα.mkdir(parents=True,exist_ok=True)
    επικύρωση_έκθεση={'passed':False,'linux_loaded':False,'kernel_sha256':hashlib.sha256((έργο_ρίζα/'build/kernel8.img').read_bytes()).hexdigest(),'languages':[]}
    try:
        with ηχώ_Διακομιστές() as ηχώ_διακομιστής_καταχώρηση:
            for Γλώσσα in ('java','c','python'):
                δοκιμή_Γλώσσα(Γλώσσα,ηχώ_διακομιστής_καταχώρηση,μέτρηση_δεδομένα);επικύρωση_έκθεση['languages'].append(Γλώσσα)
            예상결과=[('tcp','JAVA TCP 한글\n'),('udp','JAVA UDP 한글'),('udp','C UDP 한글'),('udp','PYTHON UDP 한글')]
            assert ηχώ_διακομιστής_καταχώρηση.수신됨==[(περιοχή_τιμή,δεδομένα.encode()) for περιοχή_τιμή,δεδομένα in 예상결과],ηχώ_διακομιστής_καταχώρηση.수신됨
            επικύρωση_έκθεση['host_network_payloads']=[{'protocol':περιοχή_τιμή,'text':δεδομένα.decode()} for περιοχή_τιμή,δεδομένα in ηχώ_διακομιστής_καταχώρηση.수신됨]
        επικύρωση_έκθεση.update(passed=True,examples_executed=13,graphics_pixel_checks=9,
                      swing_example_korean_input_button_label_and_close=True,
                      same_vm_vnc_and_ftp=True,ftp_while_graphics_waits=True,guest_examples_preserve_existing_files=True,
                      examples_present_at_boot=True,all_embedded_file_hashes_match=True,
                      full_16k_binary_copy_and_ftp_listing_above_slot_16=True)
    finally:(μέτρηση_δεδομένα/'report.json').write_text(json.dumps(επικύρωση_έκθεση,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':Εκτέλεση_2()
