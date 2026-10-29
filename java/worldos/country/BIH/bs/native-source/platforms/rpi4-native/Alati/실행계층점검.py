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

from Izvrši_komanda import projicirati_koijen, Naredba
from Mreža_most import Mreža_most
from 되돌림시험서버 import 되돌림시험서버


def Pokreni():
    Ispis = projicirati_koijen / 'build/verification/execution-network-review'
    Ispis.mkdir(parents=True, exist_ok=True)
    izvještaj_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projicirati_koijen / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    izvor_Fajlovi = {
        'dozvola_ček': '''public class dozvola_ček {
 public static void main(String[] Argumenti) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Mreža_ček': '''import java.net.*;
public class Mreža_ček {
 public static void main(String[] Argumenti) throws Exception {
  Socket Spoji_se = new Socket("10.0.2.2", Integer.parseInt(Argumenti[0]));
  Spoji_se.setSoTimeout(3000);
  byte[] Tekst = "TCP 한글\\n".getBytes("UTF-8");
  Spoji_se.getOutputStream().write(Tekst);
  for (int položaj_INDEX = 0; položaj_INDEX < Tekst.length; položaj_INDEX++)
   if (Spoji_se.getInputStream().read() != (Tekst[položaj_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Spoji_se.close();
  DatagramSocket završna_tačka = new DatagramSocket(); završna_tačka.setSoTimeout(3000);
  Tekst = "UDP 한글".getBytes("UTF-8");
  završna_tačka.send(new DatagramPacket(Tekst, Tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumenti[1])));
  byte[] odgovoriti = new byte[64]; DatagramPacket 전문 = new DatagramPacket(odgovoriti, odgovoriti.length);
  završna_tačka.receive(전문);
  if (전문.getLength() != Tekst.length) throw new RuntimeException("UDP length");
  for (int položaj_INDEX = 0; položaj_INDEX < Tekst.length; položaj_INDEX++)
   if (odgovoriti[položaj_INDEX] != Tekst[položaj_INDEX]) throw new RuntimeException("UDP mismatch");
  završna_tačka.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Argumenti) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket završna_tačka = new DatagramSocket(9301); završna_tačka.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Spoji_se = server_VALUE.accept(); Spoji_se.setSoTimeout(5000);
  Spoji_se.getOutputStream().write(Spoji_se.getInputStream().read() + 1);
  Spoji_se.close(); server_VALUE.close();
  byte[] podaci = new byte[64]; DatagramPacket 전문 = new DatagramPacket(podaci, podaci.length);
  završna_tačka.receive(전문); završna_tačka.send(전문); završna_tačka.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Naziv, IZVOR in izvor_Fajlovi.items():
        (Ispis / (Naziv + '.java')).write_text(IZVOR, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Ispis)] +
                          [str(Ispis / (Naziv + '.java')) for Naziv in izvor_Fajlovi])
    LOG_red = bytearray()
    def prazno_broj_priključka(TYPE_oblast=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_oblast) as Traži_VALUE:
            Traži_VALUE.bind(('127.0.0.4', 0))
            return Traži_VALUE.getsockname()[1]
    fajl_broj_priključka, TCP_port, UDP_port = prazno_broj_priključka(), prazno_broj_priključka(), prazno_broj_priključka(socket.SOCK_DGRAM)
    proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Mreža_most(
                fajl_broj_priključka, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                snimiti=True, organizator_adresa='127.0.0.4') as most_VALUE:
            kontrola_put = Path(임시) / 'qmp.sock'
            proces_VALUE = subprocess.Popen(Naredba() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrola_put)] + most_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_stavka = selectors.DefaultSelector()
            CHOOSE_stavka.register(proces_VALUE.stdout, selectors.EVENT_READ)
            def 받기(program_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while program_VALUE not in LOG_red[처음:]:
                    if time.monotonic() > 끝 or proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(program_VALUE) + '\n' + LOG_red[처음:].decode('utf-8', 'replace'))
                    for ključ_VALUE, _ in CHOOSE_stavka.select(.05):
                        조각 = ključ_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_red.extend(조각)
                return LOG_red[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def poslati(podaci):
                proces_VALUE.stdin.write(podaci)
                proces_VALUE.stdin.flush()
            def ljuska(Tekst):
                print(Tekst, flush=True)
                처음 = len(LOG_red)
                poslati((Tekst + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as kontrola_VALUE:
                kontrola_VALUE.settimeout(10)
                kontrola_VALUE.connect(str(kontrola_put))
                tok_VALUE = kontrola_VALUE.makefile('rwb')
                json.loads(tok_VALUE.readline())
                def HTTP_zahtjev(programska_naredba_VALUE, Argumenti=None):
                    podaci = {'execute': programska_naredba_VALUE}
                    if Argumenti is not None:
                        podaci['arguments'] = Argumenti
                    tok_VALUE.write((json.dumps(podaci) + '\n').encode())
                    tok_VALUE.flush()
                    while True:
                        odgovoriti = json.loads(tok_VALUE.readline())
                        if 'error' in odgovoriti:
                            raise AssertionError(odgovoriti)
                        if 'return' in odgovoriti:
                            return odgovoriti['return']
                HTTP_zahtjev('qmp_capabilities')
                def 권한읽기():
                    HTTP_zahtjev('stop')
                    try:
                        return HTTP_zahtjev('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        HTTP_zahtjev('cont')
                izvještaj_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in izvještaj_VALUE['shell_cpu'], izvještaj_VALUE['shell_cpu']
                izvještaj_VALUE['initial_ps'] = ljuska('ps')
                assert 'kernel/shell' in izvještaj_VALUE['initial_ps']
                izvještaj_VALUE['ipconfig'] = ljuska('ipconfig')
                assert 'inet 10.0.2.15' in izvještaj_VALUE['ipconfig']
                izvještaj_VALUE['gateway_ping'] = ljuska('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in izvještaj_VALUE['gateway_ping']
                assert 'FTP listening' in ljuska('ftpd start')
                with ftplib.FTP() as prijenos_VALUE:
                    prijenos_VALUE.encoding = 'utf-8'
                    prijenos_VALUE.connect('127.0.0.4', fajl_broj_priključka, timeout=20)
                    prijenos_VALUE.login()
                    for Naziv in izvor_Fajlovi:
                        prijenos_VALUE.storbinary('STOR ' + Naziv + '.class', io.BytesIO((Ispis / (Naziv + '.class')).read_bytes()))
                처음 = len(LOG_red)
                poslati('java dozvola_ček\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    izvještaj_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in izvještaj_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in izvještaj_VALUE['java_cpu'], izvještaj_VALUE['java_cpu']
                받기(처음=처음)
                izvještaj_VALUE['after_exit_ps'] = ljuska('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', izvještaj_VALUE['after_exit_ps'])
                izvještaj_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as peer_VALUE:
                    Tekst = ljuska('java Mreža_ček {} {}'.format(peer_VALUE.TCP_port, peer_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                    assert peer_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_VALUE.수신됨
                    assert not peer_VALUE.오류들, peer_VALUE.오류들
                    izvještaj_VALUE['outbound_peers'] = {종류: podaci.decode() for 종류, podaci in peer_VALUE.수신됨.items()}
                처음 = len(LOG_red)
                poslati('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as peer_VALUE:
                    peer_VALUE.sendall(b'A')
                    assert peer_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_VALUE:
                    peer_VALUE.settimeout(5)
                    peer_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert peer_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Tekst = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                izvještaj_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ljuska('terminal')
                ljuska('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_red)
                poslati('java 창예제\n'.encode())
                받기('GUI 예제 Pripremiti: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_red)
                poslati(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                izvještaj_VALUE['suspended_java_ps'] = ljuska('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', izvještaj_VALUE['suspended_java_ps']), izvještaj_VALUE['suspended_java_ps']
                izvještaj_VALUE['top'] = ljuska('top -n 1')
                assert 'java 창예제' in izvještaj_VALUE['top'] and 'kernel/shell' in izvještaj_VALUE['top']
                izvještaj_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                izvještaj_VALUE['network_trace'] = most_VALUE.trag_LOG
                assert not most_VALUE.GRESKA, most_VALUE.GRESKA
                poslati(b'poweroff\n')
                assert proces_VALUE.wait(timeout=15) == 0
                izvještaj_VALUE['passed'] = True
            CHOOSE_stavka.close()
    except Exception as GRESKA:
        izvještaj_VALUE['error'] = str(GRESKA)
        raise
    finally:
        if proces_VALUE is not None and proces_VALUE.poll() is None:
            proces_VALUE.terminate()
            try:
                proces_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                proces_VALUE.kill()
                proces_VALUE.wait()
        (Ispis / 'serial.log').write_bytes(LOG_red)
        (Ispis / 'report.json').write_text(json.dumps(izvještaj_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ključ_VALUE: izvještaj_VALUE[ključ_VALUE] for ključ_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Pokreni()
