#!/usr/bin/env python3
"""QEMU의 rzeczywisty_dane CPU pozwolenie_WARTOŚĆ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Wykonaj_polecenie import Project_korzeń, polecenie
from mostek_3de4fe3a import mostek_3de4fe3a
from echo_warunki_początkowe import echo_warunki_początkowe


def Uruchom_2():
    pozycja_wyjścia = Project_korzeń / 'build/verification/execution-network-review'
    pozycja_wyjścia.mkdir(parents=True, exist_ok=True)
    Raport_WARTOŚĆ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_korzeń / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    źródło_Files = {
        'uprawnienie_czek': '''public class uprawnienie_czek {
 public static void main(String[] argumenty) {
  System.out.println("EL0_PROBE_READY");
  int identyfikator = 0; while (true) { identyfikator++; }
 }
}''',
        'sieć_czek': '''import java.net.*;
public class sieć_czek {
 public static void main(String[] argumenty) throws Exception {
  Socket Połącz = new Socket("10.0.2.2", Integer.parseInt(argumenty[0]));
  Połącz.setSoTimeout(3000);
  byte[] tekst = "TCP 한글\\n".getBytes("UTF-8");
  Połącz.getOutputStream().write(tekst);
  for (int indeks_pozycji = 0; indeks_pozycji < tekst.length; indeks_pozycji++)
   if (Połącz.getInputStream().read() != (tekst[indeks_pozycji] & 255)) throw new RuntimeException("TCP mismatch");
  Połącz.close();
  DatagramSocket uczestnik = new DatagramSocket(); uczestnik.setSoTimeout(3000);
  tekst = "UDP 한글".getBytes("UTF-8");
  uczestnik.send(new DatagramPacket(tekst, tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumenty[1])));
  byte[] odpowiedź = new byte[64]; DatagramPacket datagram = new DatagramPacket(odpowiedź, odpowiedź.length);
  uczestnik.receive(datagram);
  if (datagram.getLength() != tekst.length) throw new RuntimeException("UDP length");
  for (int indeks_pozycji = 0; indeks_pozycji < tekst.length; indeks_pozycji++)
   if (odpowiedź[indeks_pozycji] != tekst[indeks_pozycji]) throw new RuntimeException("UDP mismatch");
  uczestnik.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'odbierać_czek': '''import java.net.*;
public class odbierać_czek {
 public static void main(String[] argumenty) throws Exception {
  ServerSocket serwer_WARTOŚĆ = new ServerSocket(9300); serwer_WARTOŚĆ.setSoTimeout(5000);
  DatagramSocket uczestnik = new DatagramSocket(9301); uczestnik.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Połącz = serwer_WARTOŚĆ.accept(); Połącz.setSoTimeout(5000);
  Połącz.getOutputStream().write(Połącz.getInputStream().read() + 1);
  Połącz.close(); serwer_WARTOŚĆ.close();
  byte[] dane = new byte[64]; DatagramPacket datagram = new DatagramPacket(dane, dane.length);
  uczestnik.receive(datagram); uczestnik.send(datagram); uczestnik.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nazwa, plik_źródłowy in źródło_Files.items():
        (pozycja_wyjścia / (Nazwa + '.java')).write_text(plik_źródłowy, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(pozycja_wyjścia)] +
                          [str(pozycja_wyjścia / (Nazwa + '.java')) for Nazwa in źródło_Files])
    LOG_zapis = bytearray()
    def 빈접속번호(TYP_obszar=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYP_obszar) as Search_WARTOŚĆ:
            Search_WARTOŚĆ.bind(('127.0.0.4', 0))
            return Search_WARTOŚĆ.getsockname()[1]
    port_plików_identyfikator, port_TCP, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proces_WARTOŚĆ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, mostek_3de4fe3a(
                port_plików_identyfikator, ['tcp:{}:9300'.format(port_TCP), 'udp:{}:9301'.format(UDP_port)],
                Capture=True, host_ADRES='127.0.0.4') as mostek_WARTOŚĆ:
            kontrola_ścieżka = Path(임시) / 'qmp.sock'
            Proces_WARTOŚĆ = subprocess.Popen(polecenie() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrola_ścieżka)] + mostek_WARTOŚĆ.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            WYBIERZ_towar = selectors.DefaultSelector()
            WYBIERZ_towar.register(Proces_WARTOŚĆ.stdout, selectors.EVENT_READ)
            def odbierać(program_WARTOŚĆ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while program_WARTOŚĆ not in LOG_zapis[처음:]:
                    if time.monotonic() > 끝 or Proces_WARTOŚĆ.poll() is not None:
                        raise AssertionError('Missing ' + repr(program_WARTOŚĆ) + '\n' + LOG_zapis[처음:].decode('utf-8', 'replace'))
                    for Klucz_WARTOŚĆ, _ in WYBIERZ_towar.select(.05):
                        fragment_WARTOŚĆ_652d4b53 = Klucz_WARTOŚĆ.fileobj.read(65536)
                        if fragment_WARTOŚĆ_652d4b53:
                            LOG_zapis.extend(fragment_WARTOŚĆ_652d4b53)
                return LOG_zapis[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def wysłać(dane):
                Proces_WARTOŚĆ.stdin.write(dane)
                Proces_WARTOŚĆ.stdin.flush()
            def powłoka(tekst):
                print(tekst, flush=True)
                처음 = len(LOG_zapis)
                wysłać((tekst + '\n').encode())
                return odbierać(처음=처음)
            odbierać()
            with socket.socket(socket.AF_UNIX) as kontrola_WARTOŚĆ:
                kontrola_WARTOŚĆ.settimeout(10)
                kontrola_WARTOŚĆ.connect(str(kontrola_ścieżka))
                Stream_WARTOŚĆ = kontrola_WARTOŚĆ.makefile('rwb')
                json.loads(Stream_WARTOŚĆ.readline())
                def żądanie(instrukcja_WARTOŚĆ, argumenty=None):
                    dane = {'execute': instrukcja_WARTOŚĆ}
                    if argumenty is not None:
                        dane['arguments'] = argumenty
                    Stream_WARTOŚĆ.write((json.dumps(dane) + '\n').encode())
                    Stream_WARTOŚĆ.flush()
                    while True:
                        odpowiedź = json.loads(Stream_WARTOŚĆ.readline())
                        if 'error' in odpowiedź:
                            raise AssertionError(odpowiedź)
                        if 'return' in odpowiedź:
                            return odpowiedź['return']
                żądanie('qmp_capabilities')
                def uprawnienie_do_odczytu():
                    żądanie('stop')
                    try:
                        return żądanie('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        żądanie('cont')
                Raport_WARTOŚĆ['shell_cpu'] = uprawnienie_do_odczytu()
                assert 'EL1h' in Raport_WARTOŚĆ['shell_cpu'], Raport_WARTOŚĆ['shell_cpu']
                Raport_WARTOŚĆ['initial_ps'] = powłoka('ps')
                assert 'kernel/shell' in Raport_WARTOŚĆ['initial_ps']
                Raport_WARTOŚĆ['ipconfig'] = powłoka('ipconfig')
                assert 'inet 10.0.2.15' in Raport_WARTOŚĆ['ipconfig']
                Raport_WARTOŚĆ['gateway_ping'] = powłoka('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Raport_WARTOŚĆ['gateway_ping']
                assert 'FTP listening' in powłoka('ftpd start')
                with ftplib.FTP() as transfer_WARTOŚĆ:
                    transfer_WARTOŚĆ.encoding = 'utf-8'
                    transfer_WARTOŚĆ.connect('127.0.0.4', port_plików_identyfikator, timeout=20)
                    transfer_WARTOŚĆ.login()
                    for Nazwa in źródło_Files:
                        transfer_WARTOŚĆ.storbinary('STOR ' + Nazwa + '.class', io.BytesIO((pozycja_wyjścia / (Nazwa + '.class')).read_bytes()))
                처음 = len(LOG_zapis)
                wysłać('java uprawnienie_czek\n'.encode())
                odbierać(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Raport_WARTOŚĆ['java_cpu'] = uprawnienie_do_odczytu()
                    if 'EL0t' in Raport_WARTOŚĆ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Raport_WARTOŚĆ['java_cpu'], Raport_WARTOŚĆ['java_cpu']
                odbierać(처음=처음)
                Raport_WARTOŚĆ['after_exit_ps'] = powłoka('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Raport_WARTOŚĆ['after_exit_ps'])
                Raport_WARTOŚĆ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with echo_warunki_początkowe() as węzeł_równorzędny_WARTOŚĆ:
                    tekst = powłoka('java sieć_czek {} {}'.format(węzeł_równorzędny_WARTOŚĆ.port_TCP, węzeł_równorzędny_WARTOŚĆ.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in tekst and 'exit 0' in tekst, tekst
                    assert węzeł_równorzędny_WARTOŚĆ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, węzeł_równorzędny_WARTOŚĆ.수신됨
                    assert not węzeł_równorzędny_WARTOŚĆ.오류들, węzeł_równorzędny_WARTOŚĆ.오류들
                    Raport_WARTOŚĆ['outbound_peers'] = {Rodzaj_WARTOŚĆ: dane.decode() for Rodzaj_WARTOŚĆ, dane in węzeł_równorzędny_WARTOŚĆ.수신됨.items()}
                처음 = len(LOG_zapis)
                wysłać('java odbierać_czek\n'.encode())
                odbierać(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', port_TCP), timeout=5) as węzeł_równorzędny_WARTOŚĆ:
                    węzeł_równorzędny_WARTOŚĆ.sendall(b'A')
                    assert węzeł_równorzędny_WARTOŚĆ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as węzeł_równorzędny_WARTOŚĆ:
                    węzeł_równorzędny_WARTOŚĆ.settimeout(5)
                    węzeł_równorzędny_WARTOŚĆ.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert węzeł_równorzędny_WARTOŚĆ.recvfrom(64)[0] == b'UDP-IN'
                tekst = odbierać(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in tekst and 'exit 0' in tekst, tekst
                Raport_WARTOŚĆ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in powłoka('terminal')
                powłoka('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_zapis)
                wysłać('java PrzykładOkna\n'.encode())
                odbierać('GUI 예제 Przygotuj: PrzykładOkna\r\n'.encode(), 처음)
                처음 = len(LOG_zapis)
                wysłać(bytes([30, 2, 1, 0, 0, 0, 0]))
                odbierać(처음=처음)
                Raport_WARTOŚĆ['suspended_java_ps'] = powłoka('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java PrzykładOkna', Raport_WARTOŚĆ['suspended_java_ps']), Raport_WARTOŚĆ['suspended_java_ps']
                Raport_WARTOŚĆ['top'] = powłoka('top -n 1')
                assert 'java PrzykładOkna' in Raport_WARTOŚĆ['top'] and 'kernel/shell' in Raport_WARTOŚĆ['top']
                Raport_WARTOŚĆ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Raport_WARTOŚĆ['network_trace'] = mostek_WARTOŚĆ.dziennik_śledzenia
                assert not mostek_WARTOŚĆ.błąd, mostek_WARTOŚĆ.błąd
                wysłać(b'poweroff\n')
                assert Proces_WARTOŚĆ.wait(timeout=15) == 0
                Raport_WARTOŚĆ['passed'] = True
            WYBIERZ_towar.close()
    except Exception as błąd:
        Raport_WARTOŚĆ['error'] = str(błąd)
        raise
    finally:
        if Proces_WARTOŚĆ is not None and Proces_WARTOŚĆ.poll() is None:
            Proces_WARTOŚĆ.terminate()
            try:
                Proces_WARTOŚĆ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_WARTOŚĆ.kill()
                Proces_WARTOŚĆ.wait()
        (pozycja_wyjścia / 'serial.log').write_bytes(LOG_zapis)
        (pozycja_wyjścia / 'report.json').write_text(json.dumps(Raport_WARTOŚĆ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Klucz_WARTOŚĆ: Raport_WARTOŚĆ[Klucz_WARTOŚĆ] for Klucz_WARTOŚĆ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Uruchom_2()
