#!/usr/bin/env python3
"""πραγματικός_δεδομένα OpenSSH 클라이언트와 RFB 클라이언트로 게스트 서비스를 검증한다."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import struct
import subprocess
import tempfile
import threading
import time
import selectors
from Crypto.Cipher import DES
from εκτελώ_εντολή import έργο_ρίζα, Εντολή
from γέφυρα_3de4fe3a import γέφυρα_3de4fe3a


def Εκτέλεση_2():
    ανάλυση_48ee4b1b = argparse.ArgumentParser(description=__doc__)
    ανάλυση_48ee4b1b.add_argument('--kernel', type=Path, default=έργο_ρίζα / 'build/kernel8.img')
    ανάλυση_48ee4b1b.add_argument('--access', type=Path, default=έργο_ρίζα / 'build/remote/access.json')
    ανάλυση_48ee4b1b.add_argument('--output', type=Path, default=έργο_ρίζα / 'build/verification/native-remote')
    Παράμετροι = ανάλυση_48ee4b1b.parse_args()
    Έξοδος = Παράμετροι.output
    Έξοδος.mkdir(parents=True, exist_ok=True)
    Ρυθμίσεις = json.loads(Παράμετροι.access.read_text())
    έκθεση_τιμή = {'passed': False, 'physical_board_tested': False, 'linux_loaded': False,
          'kernel_sha256': hashlib.sha256(Παράμετροι.kernel.read_bytes()).hexdigest(), 'checks': []}
    def 빈포트():
        with socket.socket() as Σύνδεση:
            Σύνδεση.bind(('127.0.0.5', 0))
            return Σύνδεση.getsockname()[1]
    κέλυφος_θύρα, 화면포트, Αρχείο_θύρα = 빈포트(), 빈포트(), 빈포트()
    καταγράφω_ρεκόρ = bytearray()
    διεργασία_τιμή = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-remote-') as 임시, γέφυρα_3de4fe3a(Αρχείο_θύρα,
                ['tcp:{}:22'.format(κέλυφος_θύρα), 'tcp:{}:5900'.format(화면포트)], φιλοξενώ_διεύθυνση='127.0.0.5') as γέφυρα_τιμή:
            실행인수 = Εντολή()
            실행인수[실행인수.index('-kernel') + 1] = str(Παράμετροι.kernel.resolve())
            διεργασία_τιμή = subprocess.Popen(실행인수 + ['-display','none','-monitor','none','-serial','stdio'] + γέφυρα_τιμή.전달인수(),
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            def 수집():
                while True:
                    δεδομένα = διεργασία_τιμή.stdout.read(4096)
                    if not δεδομένα: break
                    καταγράφω_ρεκόρ.extend(δεδομένα)
            νήμα_τιμή = threading.Thread(target=수집, daemon=True)
            νήμα_τιμή.start()
            def κατάσταση_αναμονής(λέξη_μήνυμα, 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while λέξη_μήνυμα not in καταγράφω_ρεκόρ[처음:]:
                    if time.monotonic()>끝 or διεργασία_τιμή.poll() is not None:
                        raise AssertionError('Missing '+repr(λέξη_μήνυμα)+'\n'+καταγράφω_ρεκόρ[처음:].decode('utf-8','replace'))
                    time.sleep(.02)
            κατάσταση_αναμονής(b'jkoros-native> ')
            βοηθητική_εφαρμογή_τιμή = Path(임시)/'askpass'
            βοηθητική_εφαρμογή_τιμή.write_text('#!/usr/bin/python3\nimport os\nprint(os.environ["JKOROS_TEST_PASSWORD"])\n')
            βοηθητική_εφαρμογή_τιμή.chmod(0o700)
            περιβάλλον_5d36e09c = dict(os.environ, DISPLAY=':999', SSH_ASKPASS=str(βοηθητική_εφαρμογή_τιμή), SSH_ASKPASS_REQUIRE='force')
            def ασφαλής_κέλυφος(κωδικός_πρόσβασης_τιμή, 명령어, προσαρτώ_καταχώρηση=()):
                περιβάλλον_5d36e09c['JKOROS_TEST_PASSWORD']=κωδικός_πρόσβασης_τιμή
                Παράμετροι=['ssh','-v']+list(προσαρτώ_καταχώρηση)+['-p',str(κέλυφος_θύρα),'-o','StrictHostKeyChecking=no','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                    '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1',
                    '-o','ConnectTimeout=20','user@127.0.0.5',명령어]
                μέτρηση=subprocess.run(Παράμετροι,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    env=περιβάλλον_5d36e09c,start_new_session=True,timeout=50)
                return μέτρηση
            μέτρηση=ασφαλής_κέλυφος('!' + Ρυθμίσεις['ssh_password'], 'echo SHOULD_NOT_RUN')
            (Έξοδος/'ssh-rejected.log').write_bytes(μέτρηση.stderr)
            assert μέτρηση.returncode!=0 and b'Permission denied' in μέτρηση.stderr and b'SHOULD_NOT_RUN' not in καταγράφω_ρεκόρ, μέτρηση.stderr
            έκθεση_τιμή['checks'].append('SSH incorrect password rejected')
            time.sleep(.5)
            μέτρηση=ασφαλής_κέλυφος(Ρυθμίσεις['ssh_password'], 'echo SSH_NATIVE_PASS')
            (Έξοδος/'ssh.log').write_bytes(μέτρηση.stderr)
            (Έξοδος/'ssh-output.txt').write_bytes(μέτρηση.stdout)
            assert μέτρηση.returncode==0 and b'SSH_NATIVE_PASS' in μέτρηση.stdout, (μέτρηση.returncode,μέτρηση.stdout,μέτρηση.stderr)
            έκθεση_τιμή['checks'].append('OpenSSH password authentication and native shell exec')
            assert b'cipher: aes128-ctr MAC: hmac-sha2-256' in μέτρηση.stderr, μέτρηση.stderr
            έκθεση_τιμή['checks'].append('Negotiated allowlisted AES-CTR / HMAC-SHA256')
            print('SSH authentication / exec PASS',flush=True)
            time.sleep(.3)
            μέτρηση=ασφαλής_κέλυφος(Ρυθμίσεις['ssh_password'], 'cd /example/java; java ΠαράδειγμαΕξόδου; cd /')
            assert μέτρηση.returncode==0 and 'JAVA Έξοδος: 안녕하세요 😀'.encode() in μέτρηση.stdout,μέτρηση.stdout
            έκθεση_τιμή['checks'].append('SSH executes EL0 Java example with UTF-8 output')
            time.sleep(.3)
            μέτρηση=ασφαλής_κέλυφος(Ρυθμίσεις['ssh_password'], 'missing_remote_command')
            assert μέτρηση.returncode==127,μέτρηση.returncode
            έκθεση_τιμή['checks'].append('SSH nonzero command exit status')
            time.sleep(.3)
            μέτρηση=ασφαλής_κέλυφος(Ρυθμίσεις['ssh_password'], 'cat /example/java/ΠαράδειγμαΠαραθύρου.java', ('-o', 'RekeyLimit=1K'))
            (Έξοδος/'ssh-rekey.log').write_bytes(μέτρηση.stderr)
            assert μέτρηση.returncode==0 and 'class ΠαράδειγμαΠαραθύρου'.encode() in μέτρηση.stdout, (μέτρηση.returncode,μέτρηση.stdout,μέτρηση.stderr)
            assert μέτρηση.stderr.count(b'SSH2_MSG_NEWKEYS received')>=2, μέτρηση.stderr
            έκθεση_τιμή['checks'].append('OpenSSH rekey during native command output')
            time.sleep(.3)
            대화인수=['ssh','-tt','-p',str(κέλυφος_θύρα),'-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(Path(임시)/'known_hosts'),
                '-o','PreferredAuthentications=password','-o','PubkeyAuthentication=no','-o','NumberOfPasswordPrompts=1','user@127.0.0.5']
            αλληλεπιδραστικός_περίοδος_λειτουργίας=subprocess.Popen(대화인수,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=περιβάλλον_5d36e09c,start_new_session=True,bufsize=0)
            μεταγραφή=bytearray();επιλογή_τιμή=selectors.DefaultSelector();επιλογή_τιμή.register(αλληλεπιδραστικός_περίοδος_λειτουργίας.stdout,selectors.EVENT_READ)
            def 대화읽기(εμφανίζω_τιμή):
                προθεσμία_τιμή=time.monotonic()+30
                while εμφανίζω_τιμή not in μεταγραφή:
                    if time.monotonic()>προθεσμία_τιμή or αλληλεπιδραστικός_περίοδος_λειτουργίας.poll() is not None:raise AssertionError('SSH interactive missing '+repr(εμφανίζω_τιμή)+' '+repr(bytes(μεταγραφή)))
                    for καταχώρηση_τιμή,_ in επιλογή_τιμή.select(.1):
                        조각=καταχώρηση_τιμή.fileobj.read(4096)
                        if 조각:μεταγραφή.extend(조각)
            try:
                대화읽기(b'shared native console')
                αλληλεπιδραστικός_περίοδος_λειτουργίας.stdin.write(b'echo SSH_INTERACTIVE_PASS\r');αλληλεπιδραστικός_περίοδος_λειτουργίας.stdin.flush();대화읽기(b'\r\nSSH_INTERACTIVE_PASS\r\n')
                αλληλεπιδραστικός_περίοδος_λειτουργίας.stdin.write(b'\x04');αλληλεπιδραστικός_περίοδος_λειτουργίας.stdin.flush();나머지,ΣΦΑΛΜΑ=αλληλεπιδραστικός_περίοδος_λειτουργίας.communicate(timeout=15)
                assert αλληλεπιδραστικός_περίοδος_λειτουργίας.returncode==0 and b'PTY allocation request failed' not in ΣΦΑΛΜΑ,(αλληλεπιδραστικός_περίοδος_λειτουργίας.returncode,ΣΦΑΛΜΑ)
                (Έξοδος/'ssh-interactive.txt').write_bytes(μεταγραφή+나머지)
            finally:
                επιλογή_τιμή.close()
                if αλληλεπιδραστικός_περίοδος_λειτουργίας.poll() is None:αλληλεπιδραστικός_περίοδος_λειτουργίας.kill();αλληλεπιδραστικός_περίοδος_λειτουργίας.wait()
            έκθεση_τιμή['checks'].append('SSH interactive terminal request, command, Ctrl-D disconnect')
            def 정확히(Σύνδεση, 수):
                δεδομένα=bytearray()
                while len(δεδομένα)<수:
                    τμήμα_τιμή=Σύνδεση.recv(수-len(δεδομένα))
                    if not τμήμα_τιμή: raise AssertionError('RFB EOF')
                    δεδομένα.extend(τμήμα_τιμή)
                return bytes(δεδομένα)
            def 화면인증(κωδικός_πρόσβασης_τιμή):
                Σύνδεση=socket.create_connection(('127.0.0.5',화면포트),10);Σύνδεση.settimeout(30)
                assert 정확히(Σύνδεση,12)==b'RFB 003.008\n'
                Σύνδεση.sendall(b'RFB 003.008\n');assert 정확히(Σύνδεση,2)==b'\x01\x02'
                Σύνδεση.sendall(b'\x02');πρόκληση_τιμή=정확히(Σύνδεση,16)
                είσοδος_κωδικός_πρόσβασης=κωδικός_πρόσβασης_τιμή.encode('ascii')[:8].ljust(8, b'\0')
                열쇠=bytes(int('{:08b}'.format(수)[::-1],2) for 수 in είσοδος_κωδικός_πρόσβασης)
                Σύνδεση.sendall(DES.new(열쇠,DES.MODE_ECB).encrypt(πρόκληση_τιμή))
                Κατάσταση_τιμή=struct.unpack('!I',정확히(Σύνδεση,4))[0]
                return Σύνδεση,Κατάσταση_τιμή
            άκυρος_κωδικός_πρόσβασης='!' if not Ρυθμίσεις['vnc_password'].startswith('!') else '?'
            Σύνδεση,Κατάσταση_τιμή=화면인증(άκυρος_κωδικός_πρόσβασης);assert Κατάσταση_τιμή==1;Σύνδεση.close();time.sleep(.6)
            έκθεση_τιμή['checks'].append('VNC incorrect password rejected')
            Σύνδεση,Κατάσταση_τιμή=화면인증(Ρυθμίσεις['vnc_password']);assert Κατάσταση_τιμή==0
            with Σύνδεση:
                Σύνδεση.sendall(b'\x01');αρχική_κατάσταση=정확히(Σύνδεση,24);너비,ύψος_τιμή=struct.unpack('!HH',αρχική_κατάσταση[:4]);Όνομα=정확히(Σύνδεση,struct.unpack('!I',αρχική_κατάσταση[20:24])[0])
                assert (너비,ύψος_τιμή)==(640,480) and b'jkoros native'==Όνομα
                def 화면(προσαυξάνω_βήμα=0):
                    Σύνδεση.sendall(struct.pack('!BBHHHH',3,προσαυξάνω_βήμα,0,0,너비,ύψος_τιμή));머리=정확히(Σύνδεση,4);수=struct.unpack('!H',머리[2:])[0];σύνολο_τιμή=0
                    σχέδιο_τιμή=bytearray(너비*ύψος_τιμή*4)
                    for _ in range(수):
                        συντεταγμένη_x,κουμπί_Y_συντονισμός,영역너비,περιοχή_ύψος,μέθοδος_λειτουργία=struct.unpack('!HHHHi',정확히(Σύνδεση,12));assert μέθοδος_λειτουργία==0 and συντεταγμένη_x+영역너비<=너비 and κουμπί_Y_συντονισμός+περιοχή_ύψος<=ύψος_τιμή
                        화소=정확히(Σύνδεση,영역너비*περιοχή_ύψος*4);σύνολο_τιμή+=len(화소)
                        for Γραμμή in range(περιοχή_ύψος):σχέδιο_τιμή[((κουμπί_Y_συντονισμός+Γραμμή)*너비+συντεταγμένη_x)*4:((κουμπί_Y_συντονισμός+Γραμμή)*너비+συντεταγμένη_x+영역너비)*4]=화소[Γραμμή*영역너비*4:(Γραμμή+1)*영역너비*4]
                    if not προσαυξάνω_βήμα:
                        from PIL import Image
                        Image.frombytes('RGB',(너비,ύψος_τιμή),bytes(σχέδιο_τιμή),'raw','BGRX').save(str(Έξοδος/'native-vnc.png'))
                    return 수,σύνολο_τιμή
                수,σύνολο_τιμή=화면();assert 수>0 and σύνολο_τιμή==너비*ύψος_τιμή*4
                έκθεση_τιμή['checks'].append('Native framebuffer RFB full update {} bytes'.format(σύνολο_τιμή))
                수,σύνολο_τιμή=화면(1);assert σύνολο_τιμή<너비*ύψος_τιμή*4
                έκθεση_τιμή['checks'].append('RFB incremental update')
                처음=len(καταγράφω_ρεκόρ)
                for χαρακτήρας_τιμή in 'echo VNC_NATIVE_PASS\r':
                    σύμβολο=0xff0d if χαρακτήρας_τιμή=='\r' else ord(χαρακτήρας_τιμή)
                    Σύνδεση.sendall(struct.pack('!BBHI',4,1,0,σύμβολο));Σύνδεση.sendall(struct.pack('!BBHI',4,0,0,σύμβολο))
                κατάσταση_αναμονής(b'VNC_NATIVE_PASS',처음)
                έκθεση_τιμή['checks'].append('Authenticated VNC keyboard executes guest shell command')
                def Κλειδί_μολυβιά(σύμβολο,누름=1):Σύνδεση.sendall(struct.pack('!BBHI',4,누름,0,σύμβολο))
                처음=len(καταγράφω_ρεκόρ)
                for χαρακτήρας_τιμή in 'echo ':Κλειδί_μολυβιά(ord(χαρακτήρας_τιμή))
                Κλειδί_μολυβιά(0xffc6)
                for χαρακτήρας_τιμή in 'gksrmf':Κλειδί_μολυβιά(ord(χαρακτήρας_τιμή))
                Κλειδί_μολυβιά(0xffc6);Κλειδί_μολυβιά(0xff0d)
                κατάσταση_αναμονής('\r\n한글\r\n'.encode(),처음)
                έκθεση_τιμή['checks'].append('Native VNC F9 two-set Hangul composition')
                Σύνδεση.sendall(struct.pack('!BBHH',5,0,120,100))
                έκθεση_τιμή['checks'].append('VNC pointer input accepted')
            διεργασία_τιμή.stdin.write(b'poweroff\n');διεργασία_τιμή.stdin.flush();διεργασία_τιμή.wait(timeout=15);assert διεργασία_τιμή.returncode==0
            έκθεση_τιμή['passed']=True
    finally:
        if διεργασία_τιμή and διεργασία_τιμή.poll() is None:
            διεργασία_τιμή.terminate()
            try: διεργασία_τιμή.wait(timeout=5)
            except subprocess.TimeoutExpired: διεργασία_τιμή.kill();διεργασία_τιμή.wait()
        (Έξοδος/'serial.log').write_bytes(καταγράφω_ρεκόρ)
        (Έξοδος/'report.json').write_text(json.dumps(έκθεση_τιμή,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(έκθεση_τιμή,ensure_ascii=False,indent=2))


if __name__=='__main__': Εκτέλεση_2()
