#!/usr/bin/env python3
"""QEMU의 stvarni_podaci CPU dozvola_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Izvrši_komanda import radnja_koren, komanda
from mrežni_most import mrežni_most
from 되돌림시험서버 import 되돌림시험서버


def koristiti():
    출력 = radnja_koren / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    izveštaj_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((radnja_koren / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    izvor_Datoteke = {
        'dozvola_proveriti': '''public class dozvola_proveriti {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Mreža_proveriti': '''import java.net.*;
public class Mreža_proveriti {
 public static void main(String[] 인수) throws Exception {
  Socket veze = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  veze.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  veze.getOutputStream().write(SMS);
  for (int indeks_pozicije = 0; indeks_pozicije < SMS.length; indeks_pozicije++)
   if (veze.getInputStream().read() != (SMS[indeks_pozicije] & 255)) throw new RuntimeException("TCP mismatch");
  veze.close();
  DatagramSocket učesnik = new DatagramSocket(); učesnik.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  učesnik.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] odgovor = new byte[64]; DatagramPacket datagram = new DatagramPacket(odgovor, odgovor.length);
  učesnik.receive(datagram);
  if (datagram.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int indeks_pozicije = 0; indeks_pozicije < SMS.length; indeks_pozicije++)
   if (odgovor[indeks_pozicije] != SMS[indeks_pozicije]) throw new RuntimeException("UDP mismatch");
  učesnik.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'primiti_proveriti': '''import java.net.*;
public class primiti_proveriti {
 public static void main(String[] 인수) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket učesnik = new DatagramSocket(9301); učesnik.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket veze = server_VALUE.accept(); veze.setSoTimeout(5000);
  veze.getOutputStream().write(veze.getInputStream().read() + 1);
  veze.close(); server_VALUE.close();
  byte[] podaci = new byte[64]; DatagramPacket datagram = new DatagramPacket(podaci, podaci.length);
  učesnik.receive(datagram); učesnik.send(datagram); učesnik.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ime, izvor in izvor_Datoteke.items():
        (출력 / (ime + '.java')).write_text(izvor, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (ime + '.java')) for ime in izvor_Datoteke])
    LOG_snimi = bytearray()
    def 빈접속번호(tip_oblast=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, tip_oblast) as SEARCH_VALUE:
            SEARCH_VALUE.bind(('127.0.0.4', 0))
            return SEARCH_VALUE.getsockname()[1]
    Datoteka_broj_porta, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, mrežni_most(
                Datoteka_broj_porta, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                uhvatiti=True, host_adresa='127.0.0.4') as most_VALUE:
            kontrola_putanja = Path(임시) / 'qmp.sock'
            Proces_VALUE = subprocess.Popen(komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrola_putanja)] + most_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_stavka = selectors.DefaultSelector()
            CHOOSE_stavka.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def primiti(emisija_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while emisija_VALUE not in LOG_snimi[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(emisija_VALUE) + '\n' + LOG_snimi[처음:].decode('utf-8', 'replace'))
                    for Ključ_VALUE, _ in CHOOSE_stavka.select(.05):
                        조각 = Ključ_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_snimi.extend(조각)
                return LOG_snimi[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def poslati(podaci):
                Proces_VALUE.stdin.write(podaci)
                Proces_VALUE.stdin.flush()
            def ljuska(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_snimi)
                poslati((SMS + '\n').encode())
                return primiti(처음=처음)
            primiti()
            with socket.socket(socket.AF_UNIX) as kontrola_VALUE:
                kontrola_VALUE.settimeout(10)
                kontrola_VALUE.connect(str(kontrola_putanja))
                tok_VALUE = kontrola_VALUE.makefile('rwb')
                json.loads(tok_VALUE.readline())
                def zahtev(명령어, 인수=None):
                    podaci = {'execute': 명령어}
                    if 인수 is not None:
                        podaci['arguments'] = 인수
                    tok_VALUE.write((json.dumps(podaci) + '\n').encode())
                    tok_VALUE.flush()
                    while True:
                        odgovor = json.loads(tok_VALUE.readline())
                        if 'error' in odgovor:
                            raise AssertionError(odgovor)
                        if 'return' in odgovor:
                            return odgovor['return']
                zahtev('qmp_capabilities')
                def 권한읽기():
                    zahtev('stop')
                    try:
                        return zahtev('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        zahtev('cont')
                izveštaj_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in izveštaj_VALUE['shell_cpu'], izveštaj_VALUE['shell_cpu']
                izveštaj_VALUE['initial_ps'] = ljuska('ps')
                assert 'kernel/shell' in izveštaj_VALUE['initial_ps']
                izveštaj_VALUE['ipconfig'] = ljuska('ipconfig')
                assert 'inet 10.0.2.15' in izveštaj_VALUE['ipconfig']
                izveštaj_VALUE['gateway_ping'] = ljuska('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in izveštaj_VALUE['gateway_ping']
                assert 'FTP listening' in ljuska('ftpd start')
                with ftplib.FTP() as prenos_VALUE:
                    prenos_VALUE.encoding = 'utf-8'
                    prenos_VALUE.connect('127.0.0.4', Datoteka_broj_porta, timeout=20)
                    prenos_VALUE.login()
                    for ime in izvor_Datoteke:
                        prenos_VALUE.storbinary('STOR ' + ime + '.class', io.BytesIO((출력 / (ime + '.class')).read_bytes()))
                처음 = len(LOG_snimi)
                poslati('java dozvola_proveriti\n'.encode())
                primiti(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    izveštaj_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in izveštaj_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in izveštaj_VALUE['java_cpu'], izveštaj_VALUE['java_cpu']
                primiti(처음=처음)
                izveštaj_VALUE['after_exit_ps'] = ljuska('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', izveštaj_VALUE['after_exit_ps'])
                izveštaj_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ravnopravni_uređaj_VALUE:
                    SMS = ljuska('java Mreža_proveriti {} {}'.format(ravnopravni_uređaj_VALUE.TCP_port, ravnopravni_uređaj_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert ravnopravni_uređaj_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ravnopravni_uređaj_VALUE.수신됨
                    assert not ravnopravni_uređaj_VALUE.오류들, ravnopravni_uređaj_VALUE.오류들
                    izveštaj_VALUE['outbound_peers'] = {종류: podaci.decode() for 종류, podaci in ravnopravni_uređaj_VALUE.수신됨.items()}
                처음 = len(LOG_snimi)
                poslati('java primiti_proveriti\n'.encode())
                primiti(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as ravnopravni_uređaj_VALUE:
                    ravnopravni_uređaj_VALUE.sendall(b'A')
                    assert ravnopravni_uređaj_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ravnopravni_uređaj_VALUE:
                    ravnopravni_uređaj_VALUE.settimeout(5)
                    ravnopravni_uređaj_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert ravnopravni_uređaj_VALUE.recvfrom(64)[0] == b'UDP-IN'
                SMS = primiti(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                izveštaj_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ljuska('terminal')
                ljuska('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_snimi)
                poslati('java 창예제\n'.encode())
                primiti('GUI 예제 Pripremi: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_snimi)
                poslati(bytes([30, 2, 1, 0, 0, 0, 0]))
                primiti(처음=처음)
                izveštaj_VALUE['suspended_java_ps'] = ljuska('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', izveštaj_VALUE['suspended_java_ps']), izveštaj_VALUE['suspended_java_ps']
                izveštaj_VALUE['top'] = ljuska('top -n 1')
                assert 'java 창예제' in izveštaj_VALUE['top'] and 'kernel/shell' in izveštaj_VALUE['top']
                izveštaj_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                izveštaj_VALUE['network_trace'] = most_VALUE.evidencija_praćenja
                assert not most_VALUE.greška, most_VALUE.greška
                poslati(b'poweroff\n')
                assert Proces_VALUE.wait(timeout=15) == 0
                izveštaj_VALUE['passed'] = True
            CHOOSE_stavka.close()
    except Exception as greška:
        izveštaj_VALUE['error'] = str(greška)
        raise
    finally:
        if Proces_VALUE is not None and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:
                Proces_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_VALUE.kill()
                Proces_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_snimi)
        (출력 / 'report.json').write_text(json.dumps(izveštaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Ključ_VALUE: izveštaj_VALUE[Ključ_VALUE] for Ključ_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    koristiti()
