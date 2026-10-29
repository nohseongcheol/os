#!/usr/bin/env python3
"""QEMU의 stvaran_podaci CPU dozvola_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Izvrši_naredba import akcija_korijen, Naredba
from most_3de4fe3a import most_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Pokreni():
    Izlaz = akcija_korijen / 'build/verification/execution-network-review'
    Izlaz.mkdir(parents=True, exist_ok=True)
    izvješće_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((akcija_korijen / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    izvor_Datoteke = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] Argumenti) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        '통신점검': '''import java.net.*;
public class 통신점검 {
 public static void main(String[] Argumenti) throws Exception {
  Socket Spoji_se = new Socket("10.0.2.2", Integer.parseInt(Argumenti[0]));
  Spoji_se.setSoTimeout(3000);
  byte[] Tekst = "TCP 한글\\n".getBytes("UTF-8");
  Spoji_se.getOutputStream().write(Tekst);
  for (int indeks_položaja = 0; indeks_položaja < Tekst.length; indeks_položaja++)
   if (Spoji_se.getInputStream().read() != (Tekst[indeks_položaja] & 255)) throw new RuntimeException("TCP mismatch");
  Spoji_se.close();
  DatagramSocket sudionik = new DatagramSocket(); sudionik.setSoTimeout(3000);
  Tekst = "UDP 한글".getBytes("UTF-8");
  sudionik.send(new DatagramPacket(Tekst, Tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumenti[1])));
  byte[] odgovor = new byte[64]; DatagramPacket datogram = new DatagramPacket(odgovor, odgovor.length);
  sudionik.receive(datogram);
  if (datogram.getLength() != Tekst.length) throw new RuntimeException("UDP length");
  for (int indeks_položaja = 0; indeks_položaja < Tekst.length; indeks_položaja++)
   if (odgovor[indeks_položaja] != Tekst[indeks_položaja]) throw new RuntimeException("UDP mismatch");
  sudionik.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Argumenti) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket sudionik = new DatagramSocket(9301); sudionik.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Spoji_se = server_VALUE.accept(); Spoji_se.setSoTimeout(5000);
  Spoji_se.getOutputStream().write(Spoji_se.getInputStream().read() + 1);
  Spoji_se.close(); server_VALUE.close();
  byte[] podaci = new byte[64]; DatagramPacket datogram = new DatagramPacket(podaci, podaci.length);
  sudionik.receive(datogram); sudionik.send(datogram); sudionik.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ime, IZVOR in izvor_Datoteke.items():
        (Izlaz / (Ime + '.java')).write_text(IZVOR, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Izlaz)] +
                          [str(Izlaz / (Ime + '.java')) for Ime in izvor_Datoteke])
    LOG_zapis = bytearray()
    def 빈접속번호(TYPE_područje=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_područje) as Traži_VALUE:
            Traži_VALUE.bind(('127.0.0.4', 0))
            return Traži_VALUE.getsockname()[1]
    Datoteka_broj_priključka, TCP_prebaciti, UDP_prebaciti = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, most_3de4fe3a(
                Datoteka_broj_priključka, ['tcp:{}:9300'.format(TCP_prebaciti), 'udp:{}:9301'.format(UDP_prebaciti)],
                snimiti=True, domaćin_adresa='127.0.0.4') as most_VALUE:
            kontrola_put = Path(임시) / 'qmp.sock'
            Proces_VALUE = subprocess.Popen(Naredba() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrola_put)] + most_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_artikl = selectors.DefaultSelector()
            CHOOSE_artikl.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def primiti(emisija_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while emisija_VALUE not in LOG_zapis[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(emisija_VALUE) + '\n' + LOG_zapis[처음:].decode('utf-8', 'replace'))
                    for Ključ_VALUE, _ in CHOOSE_artikl.select(.05):
                        fragment_VALUE = Ključ_VALUE.fileobj.read(65536)
                        if fragment_VALUE:
                            LOG_zapis.extend(fragment_VALUE)
                return LOG_zapis[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def slati(podaci):
                Proces_VALUE.stdin.write(podaci)
                Proces_VALUE.stdin.flush()
            def ljuska(Tekst):
                print(Tekst, flush=True)
                처음 = len(LOG_zapis)
                slati((Tekst + '\n').encode())
                return primiti(처음=처음)
            primiti()
            with socket.socket(socket.AF_UNIX) as kontrola_VALUE:
                kontrola_VALUE.settimeout(10)
                kontrola_VALUE.connect(str(kontrola_put))
                tok_VALUE = kontrola_VALUE.makefile('rwb')
                json.loads(tok_VALUE.readline())
                def zahtjev(명령어, Argumenti=None):
                    podaci = {'execute': 명령어}
                    if Argumenti is not None:
                        podaci['arguments'] = Argumenti
                    tok_VALUE.write((json.dumps(podaci) + '\n').encode())
                    tok_VALUE.flush()
                    while True:
                        odgovor = json.loads(tok_VALUE.readline())
                        if 'error' in odgovor:
                            raise AssertionError(odgovor)
                        if 'return' in odgovor:
                            return odgovor['return']
                zahtjev('qmp_capabilities')
                def 권한읽기():
                    zahtjev('stop')
                    try:
                        return zahtjev('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        zahtjev('cont')
                izvješće_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in izvješće_VALUE['shell_cpu'], izvješće_VALUE['shell_cpu']
                izvješće_VALUE['initial_ps'] = ljuska('ps')
                assert 'kernel/shell' in izvješće_VALUE['initial_ps']
                izvješće_VALUE['ipconfig'] = ljuska('ipconfig')
                assert 'inet 10.0.2.15' in izvješće_VALUE['ipconfig']
                izvješće_VALUE['gateway_ping'] = ljuska('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in izvješće_VALUE['gateway_ping']
                assert 'FTP listening' in ljuska('ftpd start')
                with ftplib.FTP() as Prijenos_VALUE:
                    Prijenos_VALUE.encoding = 'utf-8'
                    Prijenos_VALUE.connect('127.0.0.4', Datoteka_broj_priključka, timeout=20)
                    Prijenos_VALUE.login()
                    for Ime in izvor_Datoteke:
                        Prijenos_VALUE.storbinary('STOR ' + Ime + '.class', io.BytesIO((Izlaz / (Ime + '.class')).read_bytes()))
                처음 = len(LOG_zapis)
                slati('java 권한점검\n'.encode())
                primiti(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    izvješće_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in izvješće_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in izvješće_VALUE['java_cpu'], izvješće_VALUE['java_cpu']
                primiti(처음=처음)
                izvješće_VALUE['after_exit_ps'] = ljuska('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', izvješće_VALUE['after_exit_ps'])
                izvješće_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ravnopravan_član_VALUE:
                    Tekst = ljuska('java 통신점검 {} {}'.format(ravnopravan_član_VALUE.TCP_prebaciti, ravnopravan_član_VALUE.UDP_prebaciti))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                    assert ravnopravan_član_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ravnopravan_član_VALUE.수신됨
                    assert not ravnopravan_član_VALUE.오류들, ravnopravan_član_VALUE.오류들
                    izvješće_VALUE['outbound_peers'] = {종류: podaci.decode() for 종류, podaci in ravnopravan_član_VALUE.수신됨.items()}
                처음 = len(LOG_zapis)
                slati('java 수신점검\n'.encode())
                primiti(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_prebaciti), timeout=5) as ravnopravan_član_VALUE:
                    ravnopravan_član_VALUE.sendall(b'A')
                    assert ravnopravan_član_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ravnopravan_član_VALUE:
                    ravnopravan_član_VALUE.settimeout(5)
                    ravnopravan_član_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_prebaciti))
                    assert ravnopravan_član_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Tekst = primiti(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                izvješće_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ljuska('terminal')
                ljuska('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_zapis)
                slati('java PrimjerProzora\n'.encode())
                primiti('GUI 예제 Pripremi: PrimjerProzora\r\n'.encode(), 처음)
                처음 = len(LOG_zapis)
                slati(bytes([30, 2, 1, 0, 0, 0, 0]))
                primiti(처음=처음)
                izvješće_VALUE['suspended_java_ps'] = ljuska('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java PrimjerProzora', izvješće_VALUE['suspended_java_ps']), izvješće_VALUE['suspended_java_ps']
                izvješće_VALUE['top'] = ljuska('top -n 1')
                assert 'java PrimjerProzora' in izvješće_VALUE['top'] and 'kernel/shell' in izvješće_VALUE['top']
                izvješće_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                izvješće_VALUE['network_trace'] = most_VALUE.zapis_praćenja
                assert not most_VALUE.GREŠKA, most_VALUE.GREŠKA
                slati(b'poweroff\n')
                assert Proces_VALUE.wait(timeout=15) == 0
                izvješće_VALUE['passed'] = True
            CHOOSE_artikl.close()
    except Exception as GREŠKA:
        izvješće_VALUE['error'] = str(GREŠKA)
        raise
    finally:
        if Proces_VALUE is not None and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:
                Proces_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_VALUE.kill()
                Proces_VALUE.wait()
        (Izlaz / 'serial.log').write_bytes(LOG_zapis)
        (Izlaz / 'report.json').write_text(json.dumps(izvješće_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Ključ_VALUE: izvješće_VALUE[Ključ_VALUE] for Ključ_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Pokreni()
