#!/usr/bin/env python3
"""QEMU의 todellinen_data CPU lupa_ARVO, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Suorita_komento import aloite_juuri, komento
from silta_3de4fe3a import silta_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Suorita_2():
    tulostuspaikka = aloite_juuri / 'build/verification/execution-network-review'
    tulostuspaikka.mkdir(parents=True, exist_ok=True)
    raportti_ARVO = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((aloite_juuri / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    lähde_Files = {
        'oikeus_sekki': '''public class oikeus_sekki {
 public static void main(String[] argumentit) {
  System.out.println("EL0_PROBE_READY");
  int numero = 0; while (true) { numero++; }
 }
}''',
        'verkko_sekki': '''import java.net.*;
public class verkko_sekki {
 public static void main(String[] argumentit) throws Exception {
  Socket Yhdistä = new Socket("10.0.2.2", Integer.parseInt(argumentit[0]));
  Yhdistä.setSoTimeout(3000);
  byte[] teksti = "TCP 한글\\n".getBytes("UTF-8");
  Yhdistä.getOutputStream().write(teksti);
  for (int sijainti = 0; sijainti < teksti.length; sijainti++)
   if (Yhdistä.getInputStream().read() != (teksti[sijainti] & 255)) throw new RuntimeException("TCP mismatch");
  Yhdistä.close();
  DatagramSocket päätepiste = new DatagramSocket(); päätepiste.setSoTimeout(3000);
  teksti = "UDP 한글".getBytes("UTF-8");
  päätepiste.send(new DatagramPacket(teksti, teksti.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumentit[1])));
  byte[] palaute = new byte[64]; DatagramPacket datagrammi = new DatagramPacket(palaute, palaute.length);
  päätepiste.receive(datagrammi);
  if (datagrammi.getLength() != teksti.length) throw new RuntimeException("UDP length");
  for (int sijainti = 0; sijainti < teksti.length; sijainti++)
   if (palaute[sijainti] != teksti[sijainti]) throw new RuntimeException("UDP mismatch");
  päätepiste.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'saada_sekki': '''import java.net.*;
public class saada_sekki {
 public static void main(String[] argumentit) throws Exception {
  ServerSocket palvelin_ARVO = new ServerSocket(9300); palvelin_ARVO.setSoTimeout(5000);
  DatagramSocket päätepiste = new DatagramSocket(9301); päätepiste.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Yhdistä = palvelin_ARVO.accept(); Yhdistä.setSoTimeout(5000);
  Yhdistä.getOutputStream().write(Yhdistä.getInputStream().read() + 1);
  Yhdistä.close(); palvelin_ARVO.close();
  byte[] data = new byte[64]; DatagramPacket datagrammi = new DatagramPacket(data, data.length);
  päätepiste.receive(datagrammi); päätepiste.send(datagrammi); päätepiste.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nimi, lähdetiedosto in lähde_Files.items():
        (tulostuspaikka / (Nimi + '.java')).write_text(lähdetiedosto, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(tulostuspaikka)] +
                          [str(tulostuspaikka / (Nimi + '.java')) for Nimi in lähde_Files])
    LOG_TIETUE = bytearray()
    def 빈접속번호(TYYPPI_alue=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYYPPI_alue) as Hae_ARVO:
            Hae_ARVO.bind(('127.0.0.4', 0))
            return Hae_ARVO.getsockname()[1]
    tiedostoportti_numero, TCP_portti, UDP_portti = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    prosessi_ARVO = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, silta_3de4fe3a(
                tiedostoportti_numero, ['tcp:{}:9300'.format(TCP_portti), 'udp:{}:9301'.format(UDP_portti)],
                siepata=True, isäntä_OSOITE='127.0.0.4') as silta_ARVO:
            ohjain_polku = Path(임시) / 'qmp.sock'
            prosessi_ARVO = subprocess.Popen(komento() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ohjain_polku)] + silta_ARVO.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            valita_kohde = selectors.DefaultSelector()
            valita_kohde.register(prosessi_ARVO.stdout, selectors.EVENT_READ)
            def saada(näyttää_ARVO=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while näyttää_ARVO not in LOG_TIETUE[처음:]:
                    if time.monotonic() > 끝 or prosessi_ARVO.poll() is not None:
                        raise AssertionError('Missing ' + repr(näyttää_ARVO) + '\n' + LOG_TIETUE[처음:].decode('utf-8', 'replace'))
                    for Avain_ARVO, _ in valita_kohde.select(.05):
                        조각 = Avain_ARVO.fileobj.read(65536)
                        if 조각:
                            LOG_TIETUE.extend(조각)
                return LOG_TIETUE[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def lähettää(data):
                prosessi_ARVO.stdin.write(data)
                prosessi_ARVO.stdin.flush()
            def liittymä(teksti):
                print(teksti, flush=True)
                처음 = len(LOG_TIETUE)
                lähettää((teksti + '\n').encode())
                return saada(처음=처음)
            saada()
            with socket.socket(socket.AF_UNIX) as ohjain_ARVO:
                ohjain_ARVO.settimeout(10)
                ohjain_ARVO.connect(str(ohjain_polku))
                virta_ARVO = ohjain_ARVO.makefile('rwb')
                json.loads(virta_ARVO.readline())
                def pyyntö(käsky_ARVO, argumentit=None):
                    data = {'execute': käsky_ARVO}
                    if argumentit is not None:
                        data['arguments'] = argumentit
                    virta_ARVO.write((json.dumps(data) + '\n').encode())
                    virta_ARVO.flush()
                    while True:
                        palaute = json.loads(virta_ARVO.readline())
                        if 'error' in palaute:
                            raise AssertionError(palaute)
                        if 'return' in palaute:
                            return palaute['return']
                pyyntö('qmp_capabilities')
                def lukuoikeus():
                    pyyntö('stop')
                    try:
                        return pyyntö('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        pyyntö('cont')
                raportti_ARVO['shell_cpu'] = lukuoikeus()
                assert 'EL1h' in raportti_ARVO['shell_cpu'], raportti_ARVO['shell_cpu']
                raportti_ARVO['initial_ps'] = liittymä('ps')
                assert 'kernel/shell' in raportti_ARVO['initial_ps']
                raportti_ARVO['ipconfig'] = liittymä('ipconfig')
                assert 'inet 10.0.2.15' in raportti_ARVO['ipconfig']
                raportti_ARVO['gateway_ping'] = liittymä('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in raportti_ARVO['gateway_ping']
                assert 'FTP listening' in liittymä('ftpd start')
                with ftplib.FTP() as Siirrä_ARVO:
                    Siirrä_ARVO.encoding = 'utf-8'
                    Siirrä_ARVO.connect('127.0.0.4', tiedostoportti_numero, timeout=20)
                    Siirrä_ARVO.login()
                    for Nimi in lähde_Files:
                        Siirrä_ARVO.storbinary('STOR ' + Nimi + '.class', io.BytesIO((tulostuspaikka / (Nimi + '.class')).read_bytes()))
                처음 = len(LOG_TIETUE)
                lähettää('java oikeus_sekki\n'.encode())
                saada(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    raportti_ARVO['java_cpu'] = lukuoikeus()
                    if 'EL0t' in raportti_ARVO['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in raportti_ARVO['java_cpu'], raportti_ARVO['java_cpu']
                saada(처음=처음)
                raportti_ARVO['after_exit_ps'] = liittymä('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', raportti_ARVO['after_exit_ps'])
                raportti_ARVO['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as vertaissolmu_ARVO:
                    teksti = liittymä('java verkko_sekki {} {}'.format(vertaissolmu_ARVO.TCP_portti, vertaissolmu_ARVO.UDP_portti))
                    assert 'OUTBOUND_TCP_UDP_PASS' in teksti and 'exit 0' in teksti, teksti
                    assert vertaissolmu_ARVO.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, vertaissolmu_ARVO.수신됨
                    assert not vertaissolmu_ARVO.오류들, vertaissolmu_ARVO.오류들
                    raportti_ARVO['outbound_peers'] = {종류: data.decode() for 종류, data in vertaissolmu_ARVO.수신됨.items()}
                처음 = len(LOG_TIETUE)
                lähettää('java saada_sekki\n'.encode())
                saada(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_portti), timeout=5) as vertaissolmu_ARVO:
                    vertaissolmu_ARVO.sendall(b'A')
                    assert vertaissolmu_ARVO.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as vertaissolmu_ARVO:
                    vertaissolmu_ARVO.settimeout(5)
                    vertaissolmu_ARVO.sendto(b'UDP-IN', ('127.0.0.4', UDP_portti))
                    assert vertaissolmu_ARVO.recvfrom(64)[0] == b'UDP-IN'
                teksti = saada(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in teksti and 'exit 0' in teksti, teksti
                raportti_ARVO['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in liittymä('terminal')
                liittymä('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_TIETUE)
                lähettää('java Ikkunaesimerkki\n'.encode())
                saada('GUI 예제 Valmistele: Ikkunaesimerkki\r\n'.encode(), 처음)
                처음 = len(LOG_TIETUE)
                lähettää(bytes([30, 2, 1, 0, 0, 0, 0]))
                saada(처음=처음)
                raportti_ARVO['suspended_java_ps'] = liittymä('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java Ikkunaesimerkki', raportti_ARVO['suspended_java_ps']), raportti_ARVO['suspended_java_ps']
                raportti_ARVO['top'] = liittymä('top -n 1')
                assert 'java Ikkunaesimerkki' in raportti_ARVO['top'] and 'kernel/shell' in raportti_ARVO['top']
                raportti_ARVO['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                raportti_ARVO['network_trace'] = silta_ARVO.tapahtumaloki
                assert not silta_ARVO.VIRHE, silta_ARVO.VIRHE
                lähettää(b'poweroff\n')
                assert prosessi_ARVO.wait(timeout=15) == 0
                raportti_ARVO['passed'] = True
            valita_kohde.close()
    except Exception as VIRHE:
        raportti_ARVO['error'] = str(VIRHE)
        raise
    finally:
        if prosessi_ARVO is not None and prosessi_ARVO.poll() is None:
            prosessi_ARVO.terminate()
            try:
                prosessi_ARVO.wait(timeout=10)
            except subprocess.TimeoutExpired:
                prosessi_ARVO.kill()
                prosessi_ARVO.wait()
        (tulostuspaikka / 'serial.log').write_bytes(LOG_TIETUE)
        (tulostuspaikka / 'report.json').write_text(json.dumps(raportti_ARVO, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Avain_ARVO: raportti_ARVO[Avain_ARVO] for Avain_ARVO in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Suorita_2()
