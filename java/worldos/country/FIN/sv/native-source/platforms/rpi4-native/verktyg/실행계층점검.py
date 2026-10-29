#!/usr/bin/env python3
"""QEMU의 verklig_data CPU behörighet_värde, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from köra_kommando import åtgärd_rot, kommando
from brygga_3de4fe3a import brygga_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Kör():
    utmatningsposition = åtgärd_rot / 'build/verification/execution-network-review'
    utmatningsposition.mkdir(parents=True, exist_ok=True)
    Rapport_värde = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((åtgärd_rot / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    källa_Filer = {
        'behörighet_check': '''public class behörighet_check {
 public static void main(String[] argument) {
  System.out.println("EL0_PROBE_READY");
  int nummer = 0; while (true) { nummer++; }
 }
}''',
        'nätverk_check': '''import java.net.*;
public class nätverk_check {
 public static void main(String[] argument) throws Exception {
  Socket Anslut = new Socket("10.0.2.2", Integer.parseInt(argument[0]));
  Anslut.setSoTimeout(3000);
  byte[] text = "TCP 한글\\n".getBytes("UTF-8");
  Anslut.getOutputStream().write(text);
  for (int positionsindex = 0; positionsindex < text.length; positionsindex++)
   if (Anslut.getInputStream().read() != (text[positionsindex] & 255)) throw new RuntimeException("TCP mismatch");
  Anslut.close();
  DatagramSocket deltagare = new DatagramSocket(); deltagare.setSoTimeout(3000);
  text = "UDP 한글".getBytes("UTF-8");
  deltagare.send(new DatagramPacket(text, text.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argument[1])));
  byte[] svara = new byte[64]; DatagramPacket datagram = new DatagramPacket(svara, svara.length);
  deltagare.receive(datagram);
  if (datagram.getLength() != text.length) throw new RuntimeException("UDP length");
  for (int positionsindex = 0; positionsindex < text.length; positionsindex++)
   if (svara[positionsindex] != text[positionsindex]) throw new RuntimeException("UDP mismatch");
  deltagare.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'få_check': '''import java.net.*;
public class få_check {
 public static void main(String[] argument) throws Exception {
  ServerSocket server_värde = new ServerSocket(9300); server_värde.setSoTimeout(5000);
  DatagramSocket deltagare = new DatagramSocket(9301); deltagare.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Anslut = server_värde.accept(); Anslut.setSoTimeout(5000);
  Anslut.getOutputStream().write(Anslut.getInputStream().read() + 1);
  Anslut.close(); server_värde.close();
  byte[] data = new byte[64]; DatagramPacket datagram = new DatagramPacket(data, data.length);
  deltagare.receive(datagram); deltagare.send(datagram); deltagare.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Namn, källfil in källa_Filer.items():
        (utmatningsposition / (Namn + '.java')).write_text(källfil, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(utmatningsposition)] +
                          [str(utmatningsposition / (Namn + '.java')) for Namn in källa_Filer])
    LOG_POST = bytearray()
    def 빈접속번호(Typ_område=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Typ_område) as SÖK_värde:
            SÖK_värde.bind(('127.0.0.4', 0))
            return SÖK_värde.getsockname()[1]
    filport_nummer, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Process_värde = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, brygga_3de4fe3a(
                filport_nummer, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                Capture=True, värd_ADRESS='127.0.0.4') as brygga_värde:
            kontroll_väg = Path(임시) / 'qmp.sock'
            Process_värde = subprocess.Popen(kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontroll_väg)] + brygga_värde.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            VÄLJ_objekt = selectors.DefaultSelector()
            VÄLJ_objekt.register(Process_värde.stdout, selectors.EVENT_READ)
            def få(visa_värde=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while visa_värde not in LOG_POST[처음:]:
                    if time.monotonic() > 끝 or Process_värde.poll() is not None:
                        raise AssertionError('Missing ' + repr(visa_värde) + '\n' + LOG_POST[처음:].decode('utf-8', 'replace'))
                    for Nyckel_värde, _ in VÄLJ_objekt.select(.05):
                        조각 = Nyckel_värde.fileobj.read(65536)
                        if 조각:
                            LOG_POST.extend(조각)
                return LOG_POST[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def skicka(data):
                Process_värde.stdin.write(data)
                Process_värde.stdin.flush()
            def Shell(text):
                print(text, flush=True)
                처음 = len(LOG_POST)
                skicka((text + '\n').encode())
                return få(처음=처음)
            få()
            with socket.socket(socket.AF_UNIX) as kontroll_värde:
                kontroll_värde.settimeout(10)
                kontroll_värde.connect(str(kontroll_väg))
                flöde_värde = kontroll_värde.makefile('rwb')
                json.loads(flöde_värde.readline())
                def begäran(instruktion_värde, argument=None):
                    data = {'execute': instruktion_värde}
                    if argument is not None:
                        data['arguments'] = argument
                    flöde_värde.write((json.dumps(data) + '\n').encode())
                    flöde_värde.flush()
                    while True:
                        svara = json.loads(flöde_värde.readline())
                        if 'error' in svara:
                            raise AssertionError(svara)
                        if 'return' in svara:
                            return svara['return']
                begäran('qmp_capabilities')
                def läsbehörighet():
                    begäran('stop')
                    try:
                        return begäran('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        begäran('cont')
                Rapport_värde['shell_cpu'] = läsbehörighet()
                assert 'EL1h' in Rapport_värde['shell_cpu'], Rapport_värde['shell_cpu']
                Rapport_värde['initial_ps'] = Shell('ps')
                assert 'kernel/shell' in Rapport_värde['initial_ps']
                Rapport_värde['ipconfig'] = Shell('ipconfig')
                assert 'inet 10.0.2.15' in Rapport_värde['ipconfig']
                Rapport_värde['gateway_ping'] = Shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Rapport_värde['gateway_ping']
                assert 'FTP listening' in Shell('ftpd start')
                with ftplib.FTP() as Överför_värde:
                    Överför_värde.encoding = 'utf-8'
                    Överför_värde.connect('127.0.0.4', filport_nummer, timeout=20)
                    Överför_värde.login()
                    for Namn in källa_Filer:
                        Överför_värde.storbinary('STOR ' + Namn + '.class', io.BytesIO((utmatningsposition / (Namn + '.class')).read_bytes()))
                처음 = len(LOG_POST)
                skicka('java behörighet_check\n'.encode())
                få(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Rapport_värde['java_cpu'] = läsbehörighet()
                    if 'EL0t' in Rapport_värde['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Rapport_värde['java_cpu'], Rapport_värde['java_cpu']
                få(처음=처음)
                Rapport_värde['after_exit_ps'] = Shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Rapport_värde['after_exit_ps'])
                Rapport_värde['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as peer_värde:
                    text = Shell('java nätverk_check {} {}'.format(peer_värde.TCP_port, peer_värde.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in text and 'exit 0' in text, text
                    assert peer_värde.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_värde.수신됨
                    assert not peer_värde.오류들, peer_värde.오류들
                    Rapport_värde['outbound_peers'] = {variant_värde: data.decode() for variant_värde, data in peer_värde.수신됨.items()}
                처음 = len(LOG_POST)
                skicka('java få_check\n'.encode())
                få(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as peer_värde:
                    peer_värde.sendall(b'A')
                    assert peer_värde.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_värde:
                    peer_värde.settimeout(5)
                    peer_värde.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert peer_värde.recvfrom(64)[0] == b'UDP-IN'
                text = få(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in text and 'exit 0' in text, text
                Rapport_värde['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Shell('terminal')
                Shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_POST)
                skicka('java Fönsterexempel\n'.encode())
                få('GUI 예제 Förbereda: Fönsterexempel\r\n'.encode(), 처음)
                처음 = len(LOG_POST)
                skicka(bytes([30, 2, 1, 0, 0, 0, 0]))
                få(처음=처음)
                Rapport_värde['suspended_java_ps'] = Shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java Fönsterexempel', Rapport_värde['suspended_java_ps']), Rapport_värde['suspended_java_ps']
                Rapport_värde['top'] = Shell('top -n 1')
                assert 'java Fönsterexempel' in Rapport_värde['top'] and 'kernel/shell' in Rapport_värde['top']
                Rapport_värde['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Rapport_värde['network_trace'] = brygga_värde.spårningslogg
                assert not brygga_värde.fel, brygga_värde.fel
                skicka(b'poweroff\n')
                assert Process_värde.wait(timeout=15) == 0
                Rapport_värde['passed'] = True
            VÄLJ_objekt.close()
    except Exception as fel:
        Rapport_värde['error'] = str(fel)
        raise
    finally:
        if Process_värde is not None and Process_värde.poll() is None:
            Process_värde.terminate()
            try:
                Process_värde.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Process_värde.kill()
                Process_värde.wait()
        (utmatningsposition / 'serial.log').write_bytes(LOG_POST)
        (utmatningsposition / 'report.json').write_text(json.dumps(Rapport_värde, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Nyckel_värde: Rapport_värde[Nyckel_värde] for Nyckel_värde in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Kör()
