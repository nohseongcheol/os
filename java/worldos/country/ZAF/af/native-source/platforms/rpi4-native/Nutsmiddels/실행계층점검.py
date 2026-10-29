#!/usr/bin/env python3
"""QEMU의 werklik_data CPU toestemming_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from uitvoer_bevel import Project_wortel, Opdrag
from Netwerk_brug import Netwerk_brug
from 되돌림시험서버 import 되돌림시험서버


def Loop():
    Afvoer = Project_wortel / 'build/verification/execution-network-review'
    Afvoer.mkdir(parents=True, exist_ok=True)
    verslag_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_wortel / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    bron_Lêers = {
        'toestemming_tjek': '''public class toestemming_tjek {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Netwerk_tjek': '''import java.net.*;
public class Netwerk_tjek {
 public static void main(String[] 인수) throws Exception {
  Socket Koppel = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Koppel.setSoTimeout(3000);
  byte[] Teks = "TCP 한글\\n".getBytes("UTF-8");
  Koppel.getOutputStream().write(Teks);
  for (int plaas_INDEX = 0; plaas_INDEX < Teks.length; plaas_INDEX++)
   if (Koppel.getInputStream().read() != (Teks[plaas_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Koppel.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Teks = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Teks, Teks.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] antwoord = new byte[64]; DatagramPacket 전문 = new DatagramPacket(antwoord, antwoord.length);
  종단.receive(전문);
  if (전문.getLength() != Teks.length) throw new RuntimeException("UDP length");
  for (int plaas_INDEX = 0; plaas_INDEX < Teks.length; plaas_INDEX++)
   if (antwoord[plaas_INDEX] != Teks[plaas_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket bediener_VALUE = new ServerSocket(9300); bediener_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Koppel = bediener_VALUE.accept(); Koppel.setSoTimeout(5000);
  Koppel.getOutputStream().write(Koppel.getInputStream().read() + 1);
  Koppel.close(); bediener_VALUE.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Naam, Bron in bron_Lêers.items():
        (Afvoer / (Naam + '.java')).write_text(Bron, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Afvoer)] +
                          [str(Afvoer / (Naam + '.java')) for Naam in bron_Lêers])
    LOG_ry = bytearray()
    def 빈접속번호(TYPE_kategorie=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_kategorie) as Soek_VALUE:
            Soek_VALUE.bind(('127.0.0.4', 0))
            return Soek_VALUE.getsockname()[1]
    파일접속번호, TCP_ombou, GDP_Gebruikersdatagramprotokol_ombou = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Netwerk_brug(
                파일접속번호, ['tcp:{}:9300'.format(TCP_ombou), 'udp:{}:9301'.format(GDP_Gebruikersdatagramprotokol_ombou)],
                lê_vas=True, hou_adres='127.0.0.4') as brug_VALUE:
            kontrole_pad = Path(임시) / 'qmp.sock'
            Proses_VALUE = subprocess.Popen(Opdrag() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrole_pad)] + brug_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            kies_item = selectors.DefaultSelector()
            kies_item.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def 받기(wys_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while wys_VALUE not in LOG_ry[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(wys_VALUE) + '\n' + LOG_ry[처음:].decode('utf-8', 'replace'))
                    for Sleutel_VALUE, _ in kies_item.select(.05):
                        조각 = Sleutel_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_ry.extend(조각)
                return LOG_ry[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def e_pos(data):
                Proses_VALUE.stdin.write(data)
                Proses_VALUE.stdin.flush()
            def dop(Teks):
                print(Teks, flush=True)
                처음 = len(LOG_ry)
                e_pos((Teks + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as kontrole_VALUE:
                kontrole_VALUE.settimeout(10)
                kontrole_VALUE.connect(str(kontrole_pad))
                Stream_VALUE = kontrole_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def 요청(instruksie_VALUE, 인수=None):
                    data = {'execute': instruksie_VALUE}
                    if 인수 is not None:
                        data['arguments'] = 인수
                    Stream_VALUE.write((json.dumps(data) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        antwoord = json.loads(Stream_VALUE.readline())
                        if 'error' in antwoord:
                            raise AssertionError(antwoord)
                        if 'return' in antwoord:
                            return antwoord['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                verslag_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in verslag_VALUE['shell_cpu'], verslag_VALUE['shell_cpu']
                verslag_VALUE['initial_ps'] = dop('ps')
                assert 'kernel/shell' in verslag_VALUE['initial_ps']
                verslag_VALUE['ipconfig'] = dop('ipconfig')
                assert 'inet 10.0.2.15' in verslag_VALUE['ipconfig']
                verslag_VALUE['gateway_ping'] = dop('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in verslag_VALUE['gateway_ping']
                assert 'FTP listening' in dop('ftpd start')
                with ftplib.FTP() as oordra_VALUE:
                    oordra_VALUE.encoding = 'utf-8'
                    oordra_VALUE.connect('127.0.0.4', 파일접속번호, timeout=20)
                    oordra_VALUE.login()
                    for Naam in bron_Lêers:
                        oordra_VALUE.storbinary('STOR ' + Naam + '.class', io.BytesIO((Afvoer / (Naam + '.class')).read_bytes()))
                처음 = len(LOG_ry)
                e_pos('java toestemming_tjek\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    verslag_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in verslag_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in verslag_VALUE['java_cpu'], verslag_VALUE['java_cpu']
                받기(처음=처음)
                verslag_VALUE['after_exit_ps'] = dop('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', verslag_VALUE['after_exit_ps'])
                verslag_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as portuur_VALUE:
                    Teks = dop('java Netwerk_tjek {} {}'.format(portuur_VALUE.TCP_ombou, portuur_VALUE.GDP_Gebruikersdatagramprotokol_ombou))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Teks and 'exit 0' in Teks, Teks
                    assert portuur_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, portuur_VALUE.수신됨
                    assert not portuur_VALUE.오류들, portuur_VALUE.오류들
                    verslag_VALUE['outbound_peers'] = {종류: data.decode() for 종류, data in portuur_VALUE.수신됨.items()}
                처음 = len(LOG_ry)
                e_pos('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_ombou), timeout=5) as portuur_VALUE:
                    portuur_VALUE.sendall(b'A')
                    assert portuur_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as portuur_VALUE:
                    portuur_VALUE.settimeout(5)
                    portuur_VALUE.sendto(b'UDP-IN', ('127.0.0.4', GDP_Gebruikersdatagramprotokol_ombou))
                    assert portuur_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Teks = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Teks and 'exit 0' in Teks, Teks
                verslag_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in dop('terminal')
                dop('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_ry)
                e_pos('java 창예제\n'.encode())
                받기('GUI 예제 Maak_gereed: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_ry)
                e_pos(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                verslag_VALUE['suspended_java_ps'] = dop('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', verslag_VALUE['suspended_java_ps']), verslag_VALUE['suspended_java_ps']
                verslag_VALUE['top'] = dop('top -n 1')
                assert 'java 창예제' in verslag_VALUE['top'] and 'kernel/shell' in verslag_VALUE['top']
                verslag_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                verslag_VALUE['network_trace'] = brug_VALUE.spoor_LOG
                assert not brug_VALUE.Fout, brug_VALUE.Fout
                e_pos(b'poweroff\n')
                assert Proses_VALUE.wait(timeout=15) == 0
                verslag_VALUE['passed'] = True
            kies_item.close()
    except Exception as Fout:
        verslag_VALUE['error'] = str(Fout)
        raise
    finally:
        if Proses_VALUE is not None and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:
                Proses_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proses_VALUE.kill()
                Proses_VALUE.wait()
        (Afvoer / 'serial.log').write_bytes(LOG_ry)
        (Afvoer / 'report.json').write_text(json.dumps(verslag_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Sleutel_VALUE: verslag_VALUE[Sleutel_VALUE] for Sleutel_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Loop()
