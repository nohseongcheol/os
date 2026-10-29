#!/usr/bin/env python3
"""QEMU의 faktisk_data CPU tillatelse_VERDI, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Utfør_kommando import speile_rot, Kommando
from bro_3de4fe3a import bro_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Kjør_2():
    Utgang = speile_rot / 'build/verification/execution-network-review'
    Utgang.mkdir(parents=True, exist_ok=True)
    rapport_VERDI = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((speile_rot / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    kilde_Filer = {
        'rettighet_sjekk': '''public class rettighet_sjekk {
 public static void main(String[] Argumenter) {
  System.out.println("EL0_PROBE_READY");
  int nummer = 0; while (true) { nummer++; }
 }
}''',
        'nettverk_sjekk': '''import java.net.*;
public class nettverk_sjekk {
 public static void main(String[] Argumenter) throws Exception {
  Socket Koble_til = new Socket("10.0.2.2", Integer.parseInt(Argumenter[0]));
  Koble_til.setSoTimeout(3000);
  byte[] Tekst = "TCP 한글\\n".getBytes("UTF-8");
  Koble_til.getOutputStream().write(Tekst);
  for (int posisjonsindeks = 0; posisjonsindeks < Tekst.length; posisjonsindeks++)
   if (Koble_til.getInputStream().read() != (Tekst[posisjonsindeks] & 255)) throw new RuntimeException("TCP mismatch");
  Koble_til.close();
  DatagramSocket deltaker = new DatagramSocket(); deltaker.setSoTimeout(3000);
  Tekst = "UDP 한글".getBytes("UTF-8");
  deltaker.send(new DatagramPacket(Tekst, Tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumenter[1])));
  byte[] svar = new byte[64]; DatagramPacket datagram = new DatagramPacket(svar, svar.length);
  deltaker.receive(datagram);
  if (datagram.getLength() != Tekst.length) throw new RuntimeException("UDP length");
  for (int posisjonsindeks = 0; posisjonsindeks < Tekst.length; posisjonsindeks++)
   if (svar[posisjonsindeks] != Tekst[posisjonsindeks]) throw new RuntimeException("UDP mismatch");
  deltaker.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'motta_sjekk': '''import java.net.*;
public class motta_sjekk {
 public static void main(String[] Argumenter) throws Exception {
  ServerSocket server_VERDI = new ServerSocket(9300); server_VERDI.setSoTimeout(5000);
  DatagramSocket deltaker = new DatagramSocket(9301); deltaker.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Koble_til = server_VERDI.accept(); Koble_til.setSoTimeout(5000);
  Koble_til.getOutputStream().write(Koble_til.getInputStream().read() + 1);
  Koble_til.close(); server_VERDI.close();
  byte[] data = new byte[64]; DatagramPacket datagram = new DatagramPacket(data, data.length);
  deltaker.receive(datagram); deltaker.send(datagram); deltaker.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Navn, KILDE in kilde_Filer.items():
        (Utgang / (Navn + '.java')).write_text(KILDE, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Utgang)] +
                          [str(Utgang / (Navn + '.java')) for Navn in kilde_Filer])
    LOG_POST = bytearray()
    def tom_portnummer(Type_område=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Type_område) as SØK_VERDI:
            SØK_VERDI.bind(('127.0.0.4', 0))
            return SØK_VERDI.getsockname()[1]
    filport_nummer, TCP_port, UDP_port = tom_portnummer(), tom_portnummer(), tom_portnummer(socket.SOCK_DGRAM)
    Prosess_VERDI = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, bro_3de4fe3a(
                filport_nummer, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                hente=True, vert_e_post='127.0.0.4') as bro_VERDI:
            kontroll_bane = Path(임시) / 'qmp.sock'
            Prosess_VERDI = subprocess.Popen(Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontroll_bane)] + bro_VERDI.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            VELG_vare = selectors.DefaultSelector()
            VELG_vare.register(Prosess_VERDI.stdout, selectors.EVENT_READ)
            def motta(vise_VERDI_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while vise_VERDI_487749b8 not in LOG_POST[처음:]:
                    if time.monotonic() > 끝 or Prosess_VERDI.poll() is not None:
                        raise AssertionError('Missing ' + repr(vise_VERDI_487749b8) + '\n' + LOG_POST[처음:].decode('utf-8', 'replace'))
                    for tast_VERDI, _ in VELG_vare.select(.05):
                        조각 = tast_VERDI.fileobj.read(65536)
                        if 조각:
                            LOG_POST.extend(조각)
                return LOG_POST[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def sende(data):
                Prosess_VERDI.stdin.write(data)
                Prosess_VERDI.stdin.flush()
            def Shell(Tekst):
                print(Tekst, flush=True)
                처음 = len(LOG_POST)
                sende((Tekst + '\n').encode())
                return motta(처음=처음)
            motta()
            with socket.socket(socket.AF_UNIX) as kontroll_VERDI:
                kontroll_VERDI.settimeout(10)
                kontroll_VERDI.connect(str(kontroll_bane))
                strøm_VERDI = kontroll_VERDI.makefile('rwb')
                json.loads(strøm_VERDI.readline())
                def forespørsel(명령어, Argumenter=None):
                    data = {'execute': 명령어}
                    if Argumenter is not None:
                        data['arguments'] = Argumenter
                    strøm_VERDI.write((json.dumps(data) + '\n').encode())
                    strøm_VERDI.flush()
                    while True:
                        svar = json.loads(strøm_VERDI.readline())
                        if 'error' in svar:
                            raise AssertionError(svar)
                        if 'return' in svar:
                            return svar['return']
                forespørsel('qmp_capabilities')
                def 권한읽기():
                    forespørsel('stop')
                    try:
                        return forespørsel('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        forespørsel('cont')
                rapport_VERDI['shell_cpu'] = 권한읽기()
                assert 'EL1h' in rapport_VERDI['shell_cpu'], rapport_VERDI['shell_cpu']
                rapport_VERDI['initial_ps'] = Shell('ps')
                assert 'kernel/shell' in rapport_VERDI['initial_ps']
                rapport_VERDI['ipconfig'] = Shell('ipconfig')
                assert 'inet 10.0.2.15' in rapport_VERDI['ipconfig']
                rapport_VERDI['gateway_ping'] = Shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in rapport_VERDI['gateway_ping']
                assert 'FTP listening' in Shell('ftpd start')
                with ftplib.FTP() as overføre_VERDI:
                    overføre_VERDI.encoding = 'utf-8'
                    overføre_VERDI.connect('127.0.0.4', filport_nummer, timeout=20)
                    overføre_VERDI.login()
                    for Navn in kilde_Filer:
                        overføre_VERDI.storbinary('STOR ' + Navn + '.class', io.BytesIO((Utgang / (Navn + '.class')).read_bytes()))
                처음 = len(LOG_POST)
                sende('java rettighet_sjekk\n'.encode())
                motta(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    rapport_VERDI['java_cpu'] = 권한읽기()
                    if 'EL0t' in rapport_VERDI['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in rapport_VERDI['java_cpu'], rapport_VERDI['java_cpu']
                motta(처음=처음)
                rapport_VERDI['after_exit_ps'] = Shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', rapport_VERDI['after_exit_ps'])
                rapport_VERDI['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as node_VERDI_6a3b6fa7:
                    Tekst = Shell('java nettverk_sjekk {} {}'.format(node_VERDI_6a3b6fa7.TCP_port, node_VERDI_6a3b6fa7.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                    assert node_VERDI_6a3b6fa7.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, node_VERDI_6a3b6fa7.수신됨
                    assert not node_VERDI_6a3b6fa7.오류들, node_VERDI_6a3b6fa7.오류들
                    rapport_VERDI['outbound_peers'] = {종류: data.decode() for 종류, data in node_VERDI_6a3b6fa7.수신됨.items()}
                처음 = len(LOG_POST)
                sende('java motta_sjekk\n'.encode())
                motta(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as node_VERDI_6a3b6fa7:
                    node_VERDI_6a3b6fa7.sendall(b'A')
                    assert node_VERDI_6a3b6fa7.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as node_VERDI_6a3b6fa7:
                    node_VERDI_6a3b6fa7.settimeout(5)
                    node_VERDI_6a3b6fa7.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert node_VERDI_6a3b6fa7.recvfrom(64)[0] == b'UDP-IN'
                Tekst = motta(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                rapport_VERDI['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Shell('terminal')
                Shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_POST)
                sende('java Vinduseksempel\n'.encode())
                motta('GUI 예제 Forbered: Vinduseksempel\r\n'.encode(), 처음)
                처음 = len(LOG_POST)
                sende(bytes([30, 2, 1, 0, 0, 0, 0]))
                motta(처음=처음)
                rapport_VERDI['suspended_java_ps'] = Shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java Vinduseksempel', rapport_VERDI['suspended_java_ps']), rapport_VERDI['suspended_java_ps']
                rapport_VERDI['top'] = Shell('top -n 1')
                assert 'java Vinduseksempel' in rapport_VERDI['top'] and 'kernel/shell' in rapport_VERDI['top']
                rapport_VERDI['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                rapport_VERDI['network_trace'] = bro_VERDI.sporingslogg
                assert not bro_VERDI.feil, bro_VERDI.feil
                sende(b'poweroff\n')
                assert Prosess_VERDI.wait(timeout=15) == 0
                rapport_VERDI['passed'] = True
            VELG_vare.close()
    except Exception as feil:
        rapport_VERDI['error'] = str(feil)
        raise
    finally:
        if Prosess_VERDI is not None and Prosess_VERDI.poll() is None:
            Prosess_VERDI.terminate()
            try:
                Prosess_VERDI.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Prosess_VERDI.kill()
                Prosess_VERDI.wait()
        (Utgang / 'serial.log').write_bytes(LOG_POST)
        (Utgang / 'report.json').write_text(json.dumps(rapport_VERDI, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tast_VERDI: rapport_VERDI[tast_VERDI] for tast_VERDI in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Kjør_2()
