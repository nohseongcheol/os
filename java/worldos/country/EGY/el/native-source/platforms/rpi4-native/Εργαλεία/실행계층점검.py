#!/usr/bin/env python3
"""QEMU의 πραγματικός_δεδομένα CPU άδεια_τιμή, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
import ftplib
import hashlib
import io
import json
from pathlib import Path
import re
import selectors
import socket
import subprocess
import tempfile
import time

from εκτελώ_εντολή import έργο_ρίζα, Εντολή
from γέφυρα_3de4fe3a import γέφυρα_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Εκτέλεση_2():
    Έξοδος = έργο_ρίζα / 'build/verification/execution-network-review'
    Έξοδος.mkdir(parents=True, exist_ok=True)
    έκθεση_τιμή = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((έργο_ρίζα / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    προέλευση_Αρχεία = {
        'δικαίωμα_ελέγχω': '''public class δικαίωμα_ελέγχω {
 public static void main(String[] Παράμετροι) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'δίκτυο_ελέγχω': '''import java.net.*;
public class δίκτυο_ελέγχω {
 public static void main(String[] Παράμετροι) throws Exception {
  Socket Σύνδεση = new Socket("10.0.2.2", Integer.parseInt(Παράμετροι[0]));
  Σύνδεση.setSoTimeout(3000);
  byte[] Κείμενο = "TCP 한글\\n".getBytes("UTF-8");
  Σύνδεση.getOutputStream().write(Κείμενο);
  for (int δείκτης_θέσης = 0; δείκτης_θέσης < Κείμενο.length; δείκτης_θέσης++)
   if (Σύνδεση.getInputStream().read() != (Κείμενο[δείκτης_θέσης] & 255)) throw new RuntimeException("TCP mismatch");
  Σύνδεση.close();
  DatagramSocket τελικό_σημείο = new DatagramSocket(); τελικό_σημείο.setSoTimeout(3000);
  Κείμενο = "UDP 한글".getBytes("UTF-8");
  τελικό_σημείο.send(new DatagramPacket(Κείμενο, Κείμενο.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Παράμετροι[1])));
  byte[] απαντώ = new byte[64]; DatagramPacket αυτοδύναμο_πακέτο = new DatagramPacket(απαντώ, απαντώ.length);
  τελικό_σημείο.receive(αυτοδύναμο_πακέτο);
  if (αυτοδύναμο_πακέτο.getLength() != Κείμενο.length) throw new RuntimeException("UDP length");
  for (int δείκτης_θέσης = 0; δείκτης_θέσης < Κείμενο.length; δείκτης_θέσης++)
   if (απαντώ[δείκτης_θέσης] != Κείμενο[δείκτης_θέσης]) throw new RuntimeException("UDP mismatch");
  τελικό_σημείο.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'λαμβάνω_ελέγχω': '''import java.net.*;
public class λαμβάνω_ελέγχω {
 public static void main(String[] Παράμετροι) throws Exception {
  ServerSocket διακομιστής_τιμή = new ServerSocket(9300); διακομιστής_τιμή.setSoTimeout(5000);
  DatagramSocket τελικό_σημείο = new DatagramSocket(9301); τελικό_σημείο.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Σύνδεση = διακομιστής_τιμή.accept(); Σύνδεση.setSoTimeout(5000);
  Σύνδεση.getOutputStream().write(Σύνδεση.getInputStream().read() + 1);
  Σύνδεση.close(); διακομιστής_τιμή.close();
  byte[] δεδομένα = new byte[64]; DatagramPacket αυτοδύναμο_πακέτο = new DatagramPacket(δεδομένα, δεδομένα.length);
  τελικό_σημείο.receive(αυτοδύναμο_πακέτο); τελικό_σημείο.send(αυτοδύναμο_πακέτο); τελικό_σημείο.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Όνομα, ΠΗΓΗ in προέλευση_Αρχεία.items():
        (Έξοδος / (Όνομα + '.java')).write_text(ΠΗΓΗ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Έξοδος)] +
                          [str(Έξοδος / (Όνομα + '.java')) for Όνομα in προέλευση_Αρχεία])
    καταγράφω_ρεκόρ = bytearray()
    def 빈접속번호(Τύπος_περιοχή=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Τύπος_περιοχή) as αναζητώ_τιμή:
            αναζητώ_τιμή.bind(('127.0.0.4', 0))
            return αναζητώ_τιμή.getsockname()[1]
    Αρχείο_αριθμός_θύρας, θύρα_TCP, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    διεργασία_τιμή = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, γέφυρα_3de4fe3a(
                Αρχείο_αριθμός_θύρας, ['tcp:{}:9300'.format(θύρα_TCP), 'udp:{}:9301'.format(전문접속번호)],
                δεσμεύω=True, φιλοξενώ_διεύθυνση='127.0.0.4') as γέφυρα_τιμή:
            έλεγχος_διαδρομή = Path(임시) / 'qmp.sock'
            διεργασία_τιμή = subprocess.Popen(Εντολή() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(έλεγχος_διαδρομή)] + γέφυρα_τιμή.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            επιλέγω_στοιχείο = selectors.DefaultSelector()
            επιλέγω_στοιχείο.register(διεργασία_τιμή.stdout, selectors.EVENT_READ)
            def λαμβάνω(εμφανίζω_τιμή=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while εμφανίζω_τιμή not in καταγράφω_ρεκόρ[처음:]:
                    if time.monotonic() > 끝 or διεργασία_τιμή.poll() is not None:
                        raise AssertionError('Missing ' + repr(εμφανίζω_τιμή) + '\n' + καταγράφω_ρεκόρ[처음:].decode('utf-8', 'replace'))
                    for Κλειδί_τιμή, _ in επιλέγω_στοιχείο.select(.05):
                        조각 = Κλειδί_τιμή.fileobj.read(65536)
                        if 조각:
                            καταγράφω_ρεκόρ.extend(조각)
                return καταγράφω_ρεκόρ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def στέλνω(δεδομένα):
                διεργασία_τιμή.stdin.write(δεδομένα)
                διεργασία_τιμή.stdin.flush()
            def κέλυφος(Κείμενο):
                print(Κείμενο, flush=True)
                처음 = len(καταγράφω_ρεκόρ)
                στέλνω((Κείμενο + '\n').encode())
                return λαμβάνω(처음=처음)
            λαμβάνω()
            with socket.socket(socket.AF_UNIX) as έλεγχος_τιμή:
                έλεγχος_τιμή.settimeout(10)
                έλεγχος_τιμή.connect(str(έλεγχος_διαδρομή))
                ροή_τιμή = έλεγχος_τιμή.makefile('rwb')
                json.loads(ροή_τιμή.readline())
                def αίτηση(명령어, Παράμετροι=None):
                    δεδομένα = {'execute': 명령어}
                    if Παράμετροι is not None:
                        δεδομένα['arguments'] = Παράμετροι
                    ροή_τιμή.write((json.dumps(δεδομένα) + '\n').encode())
                    ροή_τιμή.flush()
                    while True:
                        απαντώ = json.loads(ροή_τιμή.readline())
                        if 'error' in απαντώ:
                            raise AssertionError(απαντώ)
                        if 'return' in απαντώ:
                            return απαντώ['return']
                αίτηση('qmp_capabilities')
                def 권한읽기():
                    αίτηση('stop')
                    try:
                        return αίτηση('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        αίτηση('cont')
                έκθεση_τιμή['shell_cpu'] = 권한읽기()
                assert 'EL1h' in έκθεση_τιμή['shell_cpu'], έκθεση_τιμή['shell_cpu']
                έκθεση_τιμή['initial_ps'] = κέλυφος('ps')
                assert 'kernel/shell' in έκθεση_τιμή['initial_ps']
                έκθεση_τιμή['ipconfig'] = κέλυφος('ipconfig')
                assert 'inet 10.0.2.15' in έκθεση_τιμή['ipconfig']
                έκθεση_τιμή['gateway_ping'] = κέλυφος('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in έκθεση_τιμή['gateway_ping']
                assert 'FTP listening' in κέλυφος('ftpd start')
                with ftplib.FTP() as Μεταφορά_τιμή:
                    Μεταφορά_τιμή.encoding = 'utf-8'
                    Μεταφορά_τιμή.connect('127.0.0.4', Αρχείο_αριθμός_θύρας, timeout=20)
                    Μεταφορά_τιμή.login()
                    for Όνομα in προέλευση_Αρχεία:
                        Μεταφορά_τιμή.storbinary('STOR ' + Όνομα + '.class', io.BytesIO((Έξοδος / (Όνομα + '.class')).read_bytes()))
                처음 = len(καταγράφω_ρεκόρ)
                στέλνω('java δικαίωμα_ελέγχω\n'.encode())
                λαμβάνω(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    έκθεση_τιμή['java_cpu'] = 권한읽기()
                    if 'EL0t' in έκθεση_τιμή['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in έκθεση_τιμή['java_cpu'], έκθεση_τιμή['java_cpu']
                λαμβάνω(처음=처음)
                έκθεση_τιμή['after_exit_ps'] = κέλυφος('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', έκθεση_τιμή['after_exit_ps'])
                έκθεση_τιμή['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ομότιμος_τιμή:
                    Κείμενο = κέλυφος('java δίκτυο_ελέγχω {} {}'.format(ομότιμος_τιμή.θύρα_TCP, ομότιμος_τιμή.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
                    assert ομότιμος_τιμή.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ομότιμος_τιμή.수신됨
                    assert not ομότιμος_τιμή.오류들, ομότιμος_τιμή.오류들
                    έκθεση_τιμή['outbound_peers'] = {종류: δεδομένα.decode() for 종류, δεδομένα in ομότιμος_τιμή.수신됨.items()}
                처음 = len(καταγράφω_ρεκόρ)
                στέλνω('java λαμβάνω_ελέγχω\n'.encode())
                λαμβάνω(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', θύρα_TCP), timeout=5) as ομότιμος_τιμή:
                    ομότιμος_τιμή.sendall(b'A')
                    assert ομότιμος_τιμή.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ομότιμος_τιμή:
                    ομότιμος_τιμή.settimeout(5)
                    ομότιμος_τιμή.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ομότιμος_τιμή.recvfrom(64)[0] == b'UDP-IN'
                Κείμενο = λαμβάνω(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Κείμενο and 'exit 0' in Κείμενο, Κείμενο
                έκθεση_τιμή['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in κέλυφος('terminal')
                κέλυφος('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(καταγράφω_ρεκόρ)
                στέλνω('java ΠαράδειγμαΠαραθύρου\n'.encode())
                λαμβάνω('GUI 예제 Προετοίμασε: ΠαράδειγμαΠαραθύρου\r\n'.encode(), 처음)
                처음 = len(καταγράφω_ρεκόρ)
                στέλνω(bytes([30, 2, 1, 0, 0, 0, 0]))
                λαμβάνω(처음=처음)
                έκθεση_τιμή['suspended_java_ps'] = κέλυφος('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java ΠαράδειγμαΠαραθύρου', έκθεση_τιμή['suspended_java_ps']), έκθεση_τιμή['suspended_java_ps']
                έκθεση_τιμή['top'] = κέλυφος('top -n 1')
                assert 'java ΠαράδειγμαΠαραθύρου' in έκθεση_τιμή['top'] and 'kernel/shell' in έκθεση_τιμή['top']
                έκθεση_τιμή['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                έκθεση_τιμή['network_trace'] = γέφυρα_τιμή.αρχείο_καταγραφής_ανίχνευσης
                assert not γέφυρα_τιμή.ΣΦΑΛΜΑ, γέφυρα_τιμή.ΣΦΑΛΜΑ
                στέλνω(b'poweroff\n')
                assert διεργασία_τιμή.wait(timeout=15) == 0
                έκθεση_τιμή['passed'] = True
            επιλέγω_στοιχείο.close()
    except Exception as ΣΦΑΛΜΑ:
        έκθεση_τιμή['error'] = str(ΣΦΑΛΜΑ)
        raise
    finally:
        if διεργασία_τιμή is not None and διεργασία_τιμή.poll() is None:
            διεργασία_τιμή.terminate()
            try:
                διεργασία_τιμή.wait(timeout=10)
            except subprocess.TimeoutExpired:
                διεργασία_τιμή.kill()
                διεργασία_τιμή.wait()
        (Έξοδος / 'serial.log').write_bytes(καταγράφω_ρεκόρ)
        (Έξοδος / 'report.json').write_text(json.dumps(έκθεση_τιμή, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Κλειδί_τιμή: έκθεση_τιμή[Κλειδί_τιμή] for Κλειδί_τιμή in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Εκτέλεση_2()
