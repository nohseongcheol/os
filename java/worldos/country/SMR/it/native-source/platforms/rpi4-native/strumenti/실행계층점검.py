#!/usr/bin/env python3
"""QEMU의 effettivo_dati CPU privilegio_VALORE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Esegui_comando import azione_radice, comando
from bridge_3de4fe3a import bridge_3de4fe3a
from eco_schermo_fixture import eco_schermo_fixture


def avvia():
    uscitaTesto = azione_radice / 'build/verification/execution-network-review'
    uscitaTesto.mkdir(parents=True, exist_ok=True)
    Report_VALORE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((azione_radice / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    fonte_File = {
        'privilegio_assegno': '''public class privilegio_assegno {
 public static void main(String[] argomenti) {
  System.out.println("EL0_PROBE_READY");
  int numero = 0; while (true) { numero++; }
 }
}''',
        'rete_assegno': '''import java.net.*;
public class rete_assegno {
 public static void main(String[] argomenti) throws Exception {
  Socket Connetti = new Socket("10.0.2.2", Integer.parseInt(argomenti[0]));
  Connetti.setSoTimeout(3000);
  byte[] testo = "TCP 한글\\n".getBytes("UTF-8");
  Connetti.getOutputStream().write(testo);
  for (int funzione_INDICE = 0; funzione_INDICE < testo.length; funzione_INDICE++)
   if (Connetti.getInputStream().read() != (testo[funzione_INDICE] & 255)) throw new RuntimeException("TCP mismatch");
  Connetti.close();
  DatagramSocket endpoint = new DatagramSocket(); endpoint.setSoTimeout(3000);
  testo = "UDP 한글".getBytes("UTF-8");
  endpoint.send(new DatagramPacket(testo, testo.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argomenti[1])));
  byte[] replica = new byte[64]; DatagramPacket datagramma = new DatagramPacket(replica, replica.length);
  endpoint.receive(datagramma);
  if (datagramma.getLength() != testo.length) throw new RuntimeException("UDP length");
  for (int funzione_INDICE = 0; funzione_INDICE < testo.length; funzione_INDICE++)
   if (replica[funzione_INDICE] != testo[funzione_INDICE]) throw new RuntimeException("UDP mismatch");
  endpoint.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'ricevere_assegno': '''import java.net.*;
public class ricevere_assegno {
 public static void main(String[] argomenti) throws Exception {
  ServerSocket server_VALORE = new ServerSocket(9300); server_VALORE.setSoTimeout(5000);
  DatagramSocket endpoint = new DatagramSocket(9301); endpoint.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Connetti = server_VALORE.accept(); Connetti.setSoTimeout(5000);
  Connetti.getOutputStream().write(Connetti.getInputStream().read() + 1);
  Connetti.close(); server_VALORE.close();
  byte[] dati = new byte[64]; DatagramPacket datagramma = new DatagramPacket(dati, dati.length);
  endpoint.receive(datagramma); endpoint.send(datagramma); endpoint.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nome, codiceSorgente in fonte_File.items():
        (uscitaTesto / (Nome + '.java')).write_text(codiceSorgente, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(uscitaTesto)] +
                          [str(uscitaTesto / (Nome + '.java')) for Nome in fonte_File])
    LOG_riga = bytearray()
    def vuota_numero_di_porta(TIPO_area=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TIPO_area) as Cerca_VALORE:
            Cerca_VALORE.bind(('127.0.0.4', 0))
            return Cerca_VALORE.getsockname()[1]
    porta_file_numero, porta_TCP, UDP_porta = vuota_numero_di_porta(), vuota_numero_di_porta(), vuota_numero_di_porta(socket.SOCK_DGRAM)
    Processi_VALORE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, bridge_3de4fe3a(
                porta_file_numero, ['tcp:{}:9300'.format(porta_TCP), 'udp:{}:9301'.format(UDP_porta)],
                acquisire=True, ID_host='127.0.0.4') as bridge_VALORE:
            controllo_percorso = Path(임시) / 'qmp.sock'
            Processi_VALORE = subprocess.Popen(comando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(controllo_percorso)] + bridge_VALORE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            SCEGLI_articolo = selectors.DefaultSelector()
            SCEGLI_articolo.register(Processi_VALORE.stdout, selectors.EVENT_READ)
            def ricevere(mostrare_VALORE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while mostrare_VALORE not in LOG_riga[처음:]:
                    if time.monotonic() > 끝 or Processi_VALORE.poll() is not None:
                        raise AssertionError('Missing ' + repr(mostrare_VALORE) + '\n' + LOG_riga[처음:].decode('utf-8', 'replace'))
                    for tasto_VALORE, _ in SCEGLI_articolo.select(.05):
                        blocco_VALORE_652d4b53 = tasto_VALORE.fileobj.read(65536)
                        if blocco_VALORE_652d4b53:
                            LOG_riga.extend(blocco_VALORE_652d4b53)
                return LOG_riga[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def inviare(dati):
                Processi_VALORE.stdin.write(dati)
                Processi_VALORE.stdin.flush()
            def Shell(testo):
                print(testo, flush=True)
                처음 = len(LOG_riga)
                inviare((testo + '\n').encode())
                return ricevere(처음=처음)
            ricevere()
            with socket.socket(socket.AF_UNIX) as controllo_VALORE:
                controllo_VALORE.settimeout(10)
                controllo_VALORE.connect(str(controllo_percorso))
                Stream_VALORE = controllo_VALORE.makefile('rwb')
                json.loads(Stream_VALORE.readline())
                def richiesta(istruzione_VALORE_4c26ea1b, argomenti=None):
                    dati = {'execute': istruzione_VALORE_4c26ea1b}
                    if argomenti is not None:
                        dati['arguments'] = argomenti
                    Stream_VALORE.write((json.dumps(dati) + '\n').encode())
                    Stream_VALORE.flush()
                    while True:
                        replica = json.loads(Stream_VALORE.readline())
                        if 'error' in replica:
                            raise AssertionError(replica)
                        if 'return' in replica:
                            return replica['return']
                richiesta('qmp_capabilities')
                def autorizzazione_di_lettura():
                    richiesta('stop')
                    try:
                        return richiesta('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        richiesta('cont')
                Report_VALORE['shell_cpu'] = autorizzazione_di_lettura()
                assert 'EL1h' in Report_VALORE['shell_cpu'], Report_VALORE['shell_cpu']
                Report_VALORE['initial_ps'] = Shell('ps')
                assert 'kernel/shell' in Report_VALORE['initial_ps']
                Report_VALORE['ipconfig'] = Shell('ipconfig')
                assert 'inet 10.0.2.15' in Report_VALORE['ipconfig']
                Report_VALORE['gateway_ping'] = Shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Report_VALORE['gateway_ping']
                assert 'FTP listening' in Shell('ftpd start')
                with ftplib.FTP() as trasferire_VALORE:
                    trasferire_VALORE.encoding = 'utf-8'
                    trasferire_VALORE.connect('127.0.0.4', porta_file_numero, timeout=20)
                    trasferire_VALORE.login()
                    for Nome in fonte_File:
                        trasferire_VALORE.storbinary('STOR ' + Nome + '.class', io.BytesIO((uscitaTesto / (Nome + '.class')).read_bytes()))
                처음 = len(LOG_riga)
                inviare('java privilegio_assegno\n'.encode())
                ricevere(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Report_VALORE['java_cpu'] = autorizzazione_di_lettura()
                    if 'EL0t' in Report_VALORE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Report_VALORE['java_cpu'], Report_VALORE['java_cpu']
                ricevere(처음=처음)
                Report_VALORE['after_exit_ps'] = Shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Report_VALORE['after_exit_ps'])
                Report_VALORE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with eco_schermo_fixture() as peer_VALORE:
                    testo = Shell('java rete_assegno {} {}'.format(peer_VALORE.porta_TCP, peer_VALORE.UDP_porta))
                    assert 'OUTBOUND_TCP_UDP_PASS' in testo and 'exit 0' in testo, testo
                    assert peer_VALORE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_VALORE.수신됨
                    assert not peer_VALORE.오류들, peer_VALORE.오류들
                    Report_VALORE['outbound_peers'] = {Kind_VALORE: dati.decode() for Kind_VALORE, dati in peer_VALORE.수신됨.items()}
                처음 = len(LOG_riga)
                inviare('java ricevere_assegno\n'.encode())
                ricevere(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', porta_TCP), timeout=5) as peer_VALORE:
                    peer_VALORE.sendall(b'A')
                    assert peer_VALORE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_VALORE:
                    peer_VALORE.settimeout(5)
                    peer_VALORE.sendto(b'UDP-IN', ('127.0.0.4', UDP_porta))
                    assert peer_VALORE.recvfrom(64)[0] == b'UDP-IN'
                testo = ricevere(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in testo and 'exit 0' in testo, testo
                Report_VALORE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Shell('terminal')
                Shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_riga)
                inviare('java EsempioFinestra\n'.encode())
                ricevere('GUI 예제 Prepara: EsempioFinestra\r\n'.encode(), 처음)
                처음 = len(LOG_riga)
                inviare(bytes([30, 2, 1, 0, 0, 0, 0]))
                ricevere(처음=처음)
                Report_VALORE['suspended_java_ps'] = Shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java EsempioFinestra', Report_VALORE['suspended_java_ps']), Report_VALORE['suspended_java_ps']
                Report_VALORE['top'] = Shell('top -n 1')
                assert 'java EsempioFinestra' in Report_VALORE['top'] and 'kernel/shell' in Report_VALORE['top']
                Report_VALORE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Report_VALORE['network_trace'] = bridge_VALORE.log_di_analisi
                assert not bridge_VALORE.errore, bridge_VALORE.errore
                inviare(b'poweroff\n')
                assert Processi_VALORE.wait(timeout=15) == 0
                Report_VALORE['passed'] = True
            SCEGLI_articolo.close()
    except Exception as errore:
        Report_VALORE['error'] = str(errore)
        raise
    finally:
        if Processi_VALORE is not None and Processi_VALORE.poll() is None:
            Processi_VALORE.terminate()
            try:
                Processi_VALORE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Processi_VALORE.kill()
                Processi_VALORE.wait()
        (uscitaTesto / 'serial.log').write_bytes(LOG_riga)
        (uscitaTesto / 'report.json').write_text(json.dumps(Report_VALORE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tasto_VALORE: Report_VALORE[tasto_VALORE] for tasto_VALORE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    avvia()
