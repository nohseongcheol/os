#!/usr/bin/env python3
"""QEMU의 werkelijk_gegevens CPU machtiging_WAARDE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Uitvoeren_opdracht import Taken_wortel, opdracht
from brug_3de4fe3a import brug_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def starten():
    tekstuitvoer = Taken_wortel / 'build/verification/execution-network-review'
    tekstuitvoer.mkdir(parents=True, exist_ok=True)
    Rapport_WAARDE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Taken_wortel / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    bron_Files = {
        'machtiging_cheque': '''public class machtiging_cheque {
 public static void main(String[] argumenten) {
  System.out.println("EL0_PROBE_READY");
  int nummer = 0; while (true) { nummer++; }
 }
}''',
        'net_cheque': '''import java.net.*;
public class net_cheque {
 public static void main(String[] argumenten) throws Exception {
  Socket Verbinden = new Socket("10.0.2.2", Integer.parseInt(argumenten[0]));
  Verbinden.setSoTimeout(3000);
  byte[] tekst = "TCP 한글\\n".getBytes("UTF-8");
  Verbinden.getOutputStream().write(tekst);
  for (int plaatsingsindex = 0; plaatsingsindex < tekst.length; plaatsingsindex++)
   if (Verbinden.getInputStream().read() != (tekst[plaatsingsindex] & 255)) throw new RuntimeException("TCP mismatch");
  Verbinden.close();
  DatagramSocket eindpunt = new DatagramSocket(); eindpunt.setSoTimeout(3000);
  tekst = "UDP 한글".getBytes("UTF-8");
  eindpunt.send(new DatagramPacket(tekst, tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumenten[1])));
  byte[] reactie = new byte[64]; DatagramPacket datagram = new DatagramPacket(reactie, reactie.length);
  eindpunt.receive(datagram);
  if (datagram.getLength() != tekst.length) throw new RuntimeException("UDP length");
  for (int plaatsingsindex = 0; plaatsingsindex < tekst.length; plaatsingsindex++)
   if (reactie[plaatsingsindex] != tekst[plaatsingsindex]) throw new RuntimeException("UDP mismatch");
  eindpunt.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'ontvangen_cheque': '''import java.net.*;
public class ontvangen_cheque {
 public static void main(String[] argumenten) throws Exception {
  ServerSocket server_WAARDE = new ServerSocket(9300); server_WAARDE.setSoTimeout(5000);
  DatagramSocket eindpunt = new DatagramSocket(9301); eindpunt.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Verbinden = server_WAARDE.accept(); Verbinden.setSoTimeout(5000);
  Verbinden.getOutputStream().write(Verbinden.getInputStream().read() + 1);
  Verbinden.close(); server_WAARDE.close();
  byte[] gegevens = new byte[64]; DatagramPacket datagram = new DatagramPacket(gegevens, gegevens.length);
  eindpunt.receive(datagram); eindpunt.send(datagram); eindpunt.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Naam, broncode in bron_Files.items():
        (tekstuitvoer / (Naam + '.java')).write_text(broncode, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tekstuitvoer)] +
                          [str(tekstuitvoer / (Naam + '.java')) for Naam in bron_Files])
    LOG_RECORD = bytearray()
    def leeg_poortnummer(TYPE_gebied=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_gebied) as Search_WAARDE:
            Search_WAARDE.bind(('127.0.0.4', 0))
            return Search_WAARDE.getsockname()[1]
    bestandspoort_nummer, TCP_poort, UDP_poort = leeg_poortnummer(), leeg_poortnummer(), leeg_poortnummer(socket.SOCK_DGRAM)
    Proces_WAARDE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, brug_3de4fe3a(
                bestandspoort_nummer, ['tcp:{}:9300'.format(TCP_poort), 'udp:{}:9301'.format(UDP_poort)],
                Capture=True, host_ADRES='127.0.0.4') as brug_WAARDE:
            controle_pad = Path(임시) / 'qmp.sock'
            Proces_WAARDE = subprocess.Popen(opdracht() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(controle_pad)] + brug_WAARDE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            KIEZEN_item = selectors.DefaultSelector()
            KIEZEN_item.register(Proces_WAARDE.stdout, selectors.EVENT_READ)
            def ontvangen(weergeven_WAARDE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while weergeven_WAARDE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_WAARDE.poll() is not None:
                        raise AssertionError('Missing ' + repr(weergeven_WAARDE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for toets_WAARDE, _ in KIEZEN_item.select(.05):
                        조각 = toets_WAARDE.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def e_mailen(gegevens):
                Proces_WAARDE.stdin.write(gegevens)
                Proces_WAARDE.stdin.flush()
            def Shell(tekst):
                print(tekst, flush=True)
                처음 = len(LOG_RECORD)
                e_mailen((tekst + '\n').encode())
                return ontvangen(처음=처음)
            ontvangen()
            with socket.socket(socket.AF_UNIX) as controle_WAARDE:
                controle_WAARDE.settimeout(10)
                controle_WAARDE.connect(str(controle_pad))
                Stream_WAARDE = controle_WAARDE.makefile('rwb')
                json.loads(Stream_WAARDE.readline())
                def aanvraag(instructie_WAARDE, argumenten=None):
                    gegevens = {'execute': instructie_WAARDE}
                    if argumenten is not None:
                        gegevens['arguments'] = argumenten
                    Stream_WAARDE.write((json.dumps(gegevens) + '\n').encode())
                    Stream_WAARDE.flush()
                    while True:
                        reactie = json.loads(Stream_WAARDE.readline())
                        if 'error' in reactie:
                            raise AssertionError(reactie)
                        if 'return' in reactie:
                            return reactie['return']
                aanvraag('qmp_capabilities')
                def leesmachtiging():
                    aanvraag('stop')
                    try:
                        return aanvraag('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        aanvraag('cont')
                Rapport_WAARDE['shell_cpu'] = leesmachtiging()
                assert 'EL1h' in Rapport_WAARDE['shell_cpu'], Rapport_WAARDE['shell_cpu']
                Rapport_WAARDE['initial_ps'] = Shell('ps')
                assert 'kernel/shell' in Rapport_WAARDE['initial_ps']
                Rapport_WAARDE['ipconfig'] = Shell('ipconfig')
                assert 'inet 10.0.2.15' in Rapport_WAARDE['ipconfig']
                Rapport_WAARDE['gateway_ping'] = Shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Rapport_WAARDE['gateway_ping']
                assert 'FTP listening' in Shell('ftpd start')
                with ftplib.FTP() as transfer_WAARDE:
                    transfer_WAARDE.encoding = 'utf-8'
                    transfer_WAARDE.connect('127.0.0.4', bestandspoort_nummer, timeout=20)
                    transfer_WAARDE.login()
                    for Naam in bron_Files:
                        transfer_WAARDE.storbinary('STOR ' + Naam + '.class', io.BytesIO((tekstuitvoer / (Naam + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                e_mailen('java machtiging_cheque\n'.encode())
                ontvangen(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Rapport_WAARDE['java_cpu'] = leesmachtiging()
                    if 'EL0t' in Rapport_WAARDE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Rapport_WAARDE['java_cpu'], Rapport_WAARDE['java_cpu']
                ontvangen(처음=처음)
                Rapport_WAARDE['after_exit_ps'] = Shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Rapport_WAARDE['after_exit_ps'])
                Rapport_WAARDE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as peer_WAARDE:
                    tekst = Shell('java net_cheque {} {}'.format(peer_WAARDE.TCP_poort, peer_WAARDE.UDP_poort))
                    assert 'OUTBOUND_TCP_UDP_PASS' in tekst and 'exit 0' in tekst, tekst
                    assert peer_WAARDE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_WAARDE.수신됨
                    assert not peer_WAARDE.오류들, peer_WAARDE.오류들
                    Rapport_WAARDE['outbound_peers'] = {soort_WAARDE: gegevens.decode() for soort_WAARDE, gegevens in peer_WAARDE.수신됨.items()}
                처음 = len(LOG_RECORD)
                e_mailen('java ontvangen_cheque\n'.encode())
                ontvangen(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_poort), timeout=5) as peer_WAARDE:
                    peer_WAARDE.sendall(b'A')
                    assert peer_WAARDE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_WAARDE:
                    peer_WAARDE.settimeout(5)
                    peer_WAARDE.sendto(b'UDP-IN', ('127.0.0.4', UDP_poort))
                    assert peer_WAARDE.recvfrom(64)[0] == b'UDP-IN'
                tekst = ontvangen(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in tekst and 'exit 0' in tekst, tekst
                Rapport_WAARDE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Shell('terminal')
                Shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                e_mailen('java Venstervoorbeeld\n'.encode())
                ontvangen('GUI 예제 Bereid_voor: Venstervoorbeeld\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                e_mailen(bytes([30, 2, 1, 0, 0, 0, 0]))
                ontvangen(처음=처음)
                Rapport_WAARDE['suspended_java_ps'] = Shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java Venstervoorbeeld', Rapport_WAARDE['suspended_java_ps']), Rapport_WAARDE['suspended_java_ps']
                Rapport_WAARDE['top'] = Shell('top -n 1')
                assert 'java Venstervoorbeeld' in Rapport_WAARDE['top'] and 'kernel/shell' in Rapport_WAARDE['top']
                Rapport_WAARDE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Rapport_WAARDE['network_trace'] = brug_WAARDE.traceerlogboek
                assert not brug_WAARDE.fout, brug_WAARDE.fout
                e_mailen(b'poweroff\n')
                assert Proces_WAARDE.wait(timeout=15) == 0
                Rapport_WAARDE['passed'] = True
            KIEZEN_item.close()
    except Exception as fout:
        Rapport_WAARDE['error'] = str(fout)
        raise
    finally:
        if Proces_WAARDE is not None and Proces_WAARDE.poll() is None:
            Proces_WAARDE.terminate()
            try:
                Proces_WAARDE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_WAARDE.kill()
                Proces_WAARDE.wait()
        (tekstuitvoer / 'serial.log').write_bytes(LOG_RECORD)
        (tekstuitvoer / 'report.json').write_text(json.dumps(Rapport_WAARDE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({toets_WAARDE: Rapport_WAARDE[toets_WAARDE] for toets_WAARDE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    starten()
