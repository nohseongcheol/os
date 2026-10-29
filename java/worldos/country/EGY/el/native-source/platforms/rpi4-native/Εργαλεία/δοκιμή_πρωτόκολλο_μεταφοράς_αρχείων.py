#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from γέφυρα_3de4fe3a import γέφυρα_3de4fe3a
from εκτελώ_εντολή import έργο_ρίζα, Εντολή
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Εκτέλεση_2():
    μέτρηση_δεδομένα = έργο_ρίζα / 'build/verification/ftp'; μέτρηση_δεδομένα.mkdir(parents=True, exist_ok=True)
    επικύρωση_έκθεση = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((έργο_ρίζα / 'build/kernel8.img').read_bytes()).hexdigest()}
    μεταγραφή = bytearray()
    자바원문 = μέτρηση_δεδομένα / 'δοκιμή_πακέτο.java'
    자바원문.write_text('public class δοκιμή_πακέτο { public static void main(String[] Παράμετροι) throws Exception { ελληνικά.ίδιο.Έξοδος.εγγράφω_γραμμή("JAR εκτελώ_εντολή: " + Παράμετροι[0]); ελληνικά.ίδιο.Αρχείο.Εγγραφή("jar.txt", "ίδιο πυρήνας_τιμή Αρχείο"); ελληνικά.ίδιο.Έξοδος.εγγράφω_γραμμή(ελληνικά.ίδιο.Αρχείο.Ανάγνωση("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(έργο_ρίζα/'build/java-library/classes'), '-d', str(μέτρηση_δεδομένα), str(자바원문)])
    Αρχειοθήκη = io.BytesIO()
    with zipfile.ZipFile(Αρχειοθήκη, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: δοκιμή_πακέτο\r\n\r\n')
        자바꾸러미.write(str(μέτρηση_δεδομένα/'δοκιμή_πακέτο.class'), 'δοκιμή_πακέτο.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); αριθμός_θύρας = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); διακομιστής_ροή_θύρα = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); διακομιστής_αυτοδύναμο_πακέτο_θύρα = 임시자원.getsockname()[1]
    with γέφυρα_3de4fe3a(αριθμός_θύρας, ['tcp:{}:9300'.format(διακομιστής_ροή_θύρα), 'udp:{}:9301'.format(διακομιστής_αυτοδύναμο_πακέτο_θύρα)], δεσμεύω=True) as γέφυρα:
        Διεργασία = subprocess.Popen(Εντολή() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + γέφυρα.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        επιλογέας = selectors.DefaultSelector(); επιλογέας.register(Διεργασία.stdout, selectors.EVENT_READ)
        def λαμβάνω_μήνυμα(δείκτης_8b722c5f=b'jkoros-native> ', εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ=60):
            δεδομένα = bytearray(); Τελική_οντότητα_Υπέρθεση = time.monotonic() + εκτέλεση_ΤΕΛΟΣ_ΧΡΟΝΟΥ
            while δείκτης_8b722c5f not in δεδομένα:
                if time.monotonic() > Τελική_οντότητα_Υπέρθεση or Διεργασία.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + δεδομένα.decode('utf-8', 'replace'))
                for 누름값, _ in επιλογέας.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: δεδομένα.extend(조각); μεταγραφή.extend(조각)
                if b'PANIC:' in δεδομένα or b'FAIL ' in δεδομένα: raise AssertionError(δεδομένα)
            return δεδομένα.decode('utf-8', 'replace').replace('\r\n', '\n')
        def κέλυφος(Γραμμή):
            Διεργασία.stdin.write(Γραμμή.encode() + b'\n'); Διεργασία.stdin.flush(); return λαμβάνω_μήνυμα()
        try:
            λαμβάνω_μήνυμα(); assert 'FTP listening' in κέλυφος('ftpd start')
            μεταφορά_αρχείων_σύνδεση = ftplib.FTP(); μεταφορά_αρχείων_σύνδεση.encoding = 'utf-8'; μεταφορά_αρχείων_σύνδεση.connect('127.0.0.1', αριθμός_θύρας, timeout=20); μεταφορά_αρχείων_σύνδεση.login()
            ωφέλιμο_φορτίο_δεδομένα = bytes(range(256)) * 32
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR binary.dat', io.BytesIO(ωφέλιμο_φορτίο_δεδομένα))
            μέτρηση = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR binary.dat', μέτρηση.extend)
            assert μέτρηση == ωφέλιμο_φορτίο_δεδομένα; assert μεταφορά_αρχείων_σύνδεση.size('binary.dat') == len(ωφέλιμο_φορτίο_δεδομένα)
            επικύρωση_έκθεση['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in κέλυφος('cat 한글.txt')
            assert '한글.txt' in μεταφορά_αρχείων_σύνδεση.nlst()
            assert dict(μεταφορά_αρχείων_σύνδεση.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            επικύρωση_έκθεση['checks'].append('UTF-8 filename and content visible in guest shell')
            try: μεταφορά_αρχείων_σύνδεση.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            μέτρηση = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR binary.dat', μέτρηση.extend); assert μέτρηση == ωφέλιμο_φορτίο_δεδομένα
            επικύρωση_έκθεση['checks'].append('oversized replacement rejected; previous file preserved')
            with μεταφορά_αρχείων_σύνδεση.transfercmd('STOR pending.txt') as ανεβάζω_Αρχεία:
                # A control command must not change the active upload's destination.
                assert μεταφορά_αρχείων_σύνδεση.size('binary.dat') == len(ωφέλιμο_φορτίο_δεδομένα)
                ανεβάζω_Αρχεία.sendall(b'UPLOAD TARGET PRESERVED')
            assert μεταφορά_αρχείων_σύνδεση.voidresp().startswith('226')
            μέτρηση = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR pending.txt', μέτρηση.extend)
            assert μέτρηση == b'UPLOAD TARGET PRESERVED'
            μέτρηση = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR binary.dat', μέτρηση.extend)
            assert μέτρηση == ωφέλιμο_φορτίο_δεδομένα
            μεταφορά_αρχείων_σύνδεση.delete('pending.txt')
            επικύρωση_έκθεση['checks'].append('interleaved SIZE cannot change the active STOR destination')
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 인사.jar', io.BytesIO(Αρχειοθήκη.getvalue()))
            Κείμενο = κέλυφος('java -jar 인사.jar 누리')
            assert 'JAR εκτελώ_εντολή: 누리' in Κείμενο and 'ίδιο πυρήνας_τιμή Αρχείο' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            Κείμενο = κέλυφος('./인사.jar 세상')
            assert 'JAR εκτελώ_εντολή: 세상' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            επικύρωση_έκθεση['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct δεδομένα { int 수; double 비율; };\nint Διαχείριση_ενημερώσεων_λογισμικού_τιμή(int n) { return n ? n + Διαχείριση_ενημερώσεων_λογισμικού_τιμή(n-1) : 0; }\nint main(void) { struct δεδομένα τιμή = {Διαχείριση_ενημερώσεων_λογισμικού_τιμή(10), 1.25}; if (τιμή.수 != 55 || τιμή.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ανοίγω_Αρχείο("cc.txt", 읽고쓰기 | 없으면만들기 | περικοπή_Περιεχόμενα, 0600); if (문서 < 0) return 1; εγγράφω_Αρχείο_δεδομένα(문서, 인사, sizeof(인사)-1); κλείνω_Αρχείο(문서); εγγράφω_Αρχείο_δεδομένα(1, 인사, sizeof(인사)-1); return 0; }\n'
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Κείμενο = κέλυφος('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            Κείμενο = κέλυφος('run 한글.elf'); assert 'CC NATIVE PASS' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            assert 'CC NATIVE PASS' in κέλυφος('cat cc.txt')
            εκτελέσιμο = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR 한글.elf', εκτελέσιμο.extend)
            assert εκτελέσιμο[:4] == b'\x7fELF' and εκτελέσιμο[18:20] == b'\xb7\x00'
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR παρουσία_τιμή.elf', io.BytesIO(εκτελέσιμο)); Κείμενο = κέλυφος('run παρουσία_τιμή.elf'); assert 'CC NATIVE PASS' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR εκτελώ_εντολή', io.BytesIO(εκτελέσιμο)); Κείμενο=κέλυφος('./εκτελώ_εντολή');assert 'CC NATIVE PASS' in Κείμενο and 'exit 0' in Κείμενο,Κείμενο
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR Όνομα.txt', io.BytesIO(εκτελέσιμο)); Κείμενο=κέλυφος('./Όνομα.txt');assert 'CC NATIVE PASS' in Κείμενο and 'exit 0' in Κείμενο,Κείμενο
            κέλυφος('rm εκτελώ_εντολή Όνομα.txt')
            επικύρωση_έκθεση['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            κέλυφος('rm binary.dat 한글.txt 한글.c 한글.elf παρουσία_τιμή.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(μέτρηση_δεδομένα/'linux-reference')
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Κείμενο=κέλυφος('./리눅스인사');assert 'exit -8' in Κείμενο,Κείμενο
            Κείμενο=κέλυφος('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Κείμενο,Κείμενο
            assert 'LINUX ELF FILE IO' in κέλυφος('cat linux.txt')
            μεταφορά_αρχείων_σύνδεση.delete('리눅스인사');μεταφορά_αρχείων_σύνδεση.delete('linux.txt')
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in κέλυφος('./거짓.elf');μεταφορά_αρχείων_σύνδεση.delete('거짓.elf')
            επικύρωση_έκθεση['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as ηχώ_διακομιστής_καταχώρηση:
                통신원문 = μέτρηση_δεδομένα/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Σύνδεση = ελληνικά.ίδιο.연결통신.Σύνδεση("10.0.2.2", Integer.parseInt(args[0]));
 Σύνδεση.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ΠΗΓΗ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ΠΗΓΗ.length;i++) if (Σύνδεση.getInputStream().read() != (ΠΗΓΗ[i]&255)) throw new RuntimeException("TCP mismatch");
 Σύνδεση.close();
 DatagramSocket τελικό_σημείο = ελληνικά.ίδιο.통신.Άνοιγμα(0); ελληνικά.ίδιο.통신.ΤΕΛΟΣ_ΧΡΟΝΟΥ(τελικό_σημείο, 500);
 ελληνικά.ίδιο.통신.στέλνω(τελικό_σημείο, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!ελληνικά.ίδιο.통신.λαμβάνω(τελικό_σημείο).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 τελικό_σημείο.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(έργο_ρίζα/'build/java-library/classes'),'-d',str(μέτρηση_δεδομένα),str(통신원문)])
                μεταφορά_αρχείων_σύνδεση.storbinary('STOR 바깥통신.class', io.BytesIO((μέτρηση_δεδομένα/'바깥통신.class').read_bytes()))
                Κείμενο = κέλυφος('java 바깥통신 {} {}'.format(ηχώ_διακομιστής_καταχώρηση.θύρα_TCP, ηχώ_διακομιστής_καταχώρηση.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Κείμενο and '10.0.2.2' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
                assert ηχώ_διακομιστής_καταχώρηση.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, ηχώ_διακομιστής_καταχώρηση.수신됨
                assert not ηχώ_διακομιστής_καταχώρηση.오류들, ηχώ_διακομιστής_καταχώρηση.오류들
            επικύρωση_έκθεση['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            μεταφορά_αρχείων_σύνδεση.delete('바깥통신.class')
            διακομιστής_προέλευση=μέτρηση_δεδομένα/'διακομιστής_δοκιμή.java'
            διακομιστής_προέλευση.write_text('''import java.net.*; public class διακομιστής_δοκιμή {
 public static void main(String[] args) throws Exception {
  ServerSocket διακομιστής_τιμή = new ServerSocket(9300); DatagramSocket τελικό_σημείο = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket Επισκέπτης_τιμή = διακομιστής_τιμή.accept();
  Επισκέπτης_τιμή.getOutputStream().write(Επισκέπτης_τιμή.getInputStream().read()+1); Επισκέπτης_τιμή.close(); διακομιστής_τιμή.close();
  byte[] Περιεχόμενο_τιμή = new byte[8]; DatagramPacket αυτοδύναμο_πακέτο = new DatagramPacket(Περιεχόμενο_τιμή, Περιεχόμενο_τιμή.length); τελικό_σημείο.receive(αυτοδύναμο_πακέτο);
  τελικό_σημείο.send(αυτοδύναμο_πακέτο); τελικό_σημείο.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(μέτρηση_δεδομένα),str(διακομιστής_προέλευση)])
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR διακομιστής_δοκιμή.class',io.BytesIO((μέτρηση_δεδομένα/'διακομιστής_δοκιμή.class').read_bytes()))
            Διεργασία.stdin.write('java διακομιστής_δοκιμή\n'.encode());Διεργασία.stdin.flush();λαμβάνω_μήνυμα(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',διακομιστής_ροή_θύρα),timeout=5) as ομότιμος_τιμή:
                ομότιμος_τιμή.sendall(b'A');assert ομότιμος_τιμή.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ομότιμος_τιμή:
                ομότιμος_τιμή.settimeout(5);ομότιμος_τιμή.sendto(b'UDP-IN',('127.0.0.1',διακομιστής_αυτοδύναμο_πακέτο_θύρα));assert ομότιμος_τιμή.recvfrom(512)[0]==b'UDP-IN'
            Κείμενο=λαμβάνω_μήνυμα();assert 'INBOUND TCP UDP PASS' in Κείμενο and 'exit 0' in Κείμενο,Κείμενο
            επικύρωση_έκθεση['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            μεταφορά_αρχείων_σύνδεση.delete('διακομιστής_δοκιμή.class')
            명령열 = 'public class 빛 { public static void main(String[] Παράμετροι) throws Exception { int Διαχείριση_ενημερώσεων_λογισμικού_τιμή = 0; int 수 = 1; while (수 <= 10) { Διαχείριση_ενημερώσεων_λογισμικού_τιμή = Διαχείριση_ενημερώσεων_λογισμικού_τιμή + 수; 수 = 수 + 1; } ελληνικά.ίδιο.Έξοδος.수쓰기(Διαχείριση_ενημερώσεων_λογισμικού_τιμή); ελληνικά.ίδιο.Αρχείο.Εγγραφή("aot.txt", "한글 AOT Αρχείο 😀"); ελληνικά.ίδιο.Έξοδος.εγγράφω_γραμμή(ελληνικά.ίδιο.Αρχείο.Ανάγνωση("aot.txt")); } }'
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Κείμενο = κέλυφος('javac 빛.java'); assert 'exit 0' in Κείμενο and 'Compiled:' in Κείμενο, Κείμενο
            Κείμενο = κέλυφος('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            Κείμενο = κέλυφος('run 빛.elf'); assert '\n55\n' in Κείμενο and '한글 AOT Αρχείο 😀' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            εγγενής = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR 빛.elf', εγγενής.extend)
            Κείμενο = κέλυφος('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Κείμενο and 'unsupported' in Κείμενο, Κείμενο
            보존자료 = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR 빛.elf', 보존자료.extend); assert εγγενής == 보존자료
            바이트코드 = bytearray(); μεταφορά_αρχείων_σύνδεση.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Κείμενο = κέλυφος('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            Κείμενο = κέλυφος('run 빛.elf'); assert '\n55\n' in Κείμενο and '한글 AOT Αρχείο 😀' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
            επικύρωση_έκθεση['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            επικύρωση_έκθεση['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            στατικός_προέλευση=μέτρηση_δεδομένα/'στατικός_δοκιμή.java'
            στατικός_προέλευση.write_text('''public class στατικός_δοκιμή {
 static int έργο_ρίζα = 3;
 static int Διαχείριση_ενημερώσεων_λογισμικού_τιμή(int n) { return n == 0 ? 0 : n + Διαχείριση_ενημερώσεων_λογισμικού_τιμή(n-1); }
 public static void main(String[] Παράμετροι) {
  int[] τιμή = new int[] {έργο_ρίζα, Διαχείριση_ενημερώσεων_λογισμικού_τιμή(10)};
  System.out.println(τιμή[0] + τιμή[1]); System.out.println(Παράμετροι[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(μέτρηση_δεδομένα),str(στατικός_προέλευση)])
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR στατικός_δοκιμή.class',io.BytesIO((μέτρηση_δεδομένα/'στατικός_δοκιμή.class').read_bytes()))
            Κείμενο=κέλυφος('jaot στατικός_δοκιμή.class -o στατικός_δοκιμή.elf');assert 'exit 0' in Κείμενο,Κείμενο
            Κείμενο=κέλυφος('run στατικός_δοκιμή.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Κείμενο,Κείμενο
            μεταφορά_αρχείων_σύνδεση.delete('στατικός_δοκιμή.class');μεταφορά_αρχείων_σύνδεση.delete('στατικός_δοκιμή.elf')
            επικύρωση_έκθεση['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Αρχειοθήκη.getvalue());손상자료[14]^=1
            μεταφορά_αρχείων_σύνδεση.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Κείμενο=κέλυφος('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Κείμενο,Κείμενο
            επικύρωση_έκθεση['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            μεταφορά_αρχείων_σύνδεση.quit(); assert 'FTP stopped' in κέλυφος('ftpd stop')
            assert not γέφυρα.ΣΦΑΛΜΑ, γέφυρα.ΣΦΑΛΜΑ
            επικύρωση_έκθεση.update(passed=True, frames_to_guest=γέφυρα.커널수신틀수, frames_from_guest=γέφυρα.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in επιλογέας.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: μεταγραφή.extend(조각)
            γέφυρα.Παύση_συμβάν.set()
            Διεργασία.terminate()
            try: Διεργασία.wait(timeout=5)
            except subprocess.TimeoutExpired: Διεργασία.kill(); Διεργασία.wait()
            επιλογέας.close(); Διεργασία.stdin.close(); Διεργασία.stdout.close()
            επικύρωση_έκθεση['bridge_error'] = γέφυρα.ΣΦΑΛΜΑ
            επικύρωση_έκθεση['frames_to_guest'] = γέφυρα.커널수신틀수; επικύρωση_έκθεση['frames_from_guest'] = γέφυρα.커널발신틀수
            (μέτρηση_δεδομένα/'packets.json').write_text(json.dumps(γέφυρα.αρχείο_καταγραφής_ανίχνευσης,indent=2)+'\n')
            (μέτρηση_δεδομένα / 'serial.log').write_bytes(μεταγραφή)
            (μέτρηση_δεδομένα / 'report.json').write_text(json.dumps(επικύρωση_έκθεση, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Εκτέλεση_2()
