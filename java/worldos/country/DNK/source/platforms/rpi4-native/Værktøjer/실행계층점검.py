#!/usr/bin/env python3
"""QEMU의 faktisk_data CPU rettighed_VÆRDI, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Udfør_kommando import To_do_rod, Kommando
from bro_3de4fe3a import bro_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Kør_2():
    Udgang = To_do_rod / 'build/verification/execution-network-review'
    Udgang.mkdir(parents=True, exist_ok=True)
    rapport_VÆRDI = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((To_do_rod / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    kilde_Filer = {
        'rettighed_check': '''public class rettighed_check {
 public static void main(String[] Argumenter) {
  System.out.println("EL0_PROBE_READY");
  int tal = 0; while (true) { tal++; }
 }
}''',
        'netværk_check': '''import java.net.*;
public class netværk_check {
 public static void main(String[] Argumenter) throws Exception {
  Socket Tilslut = new Socket("10.0.2.2", Integer.parseInt(Argumenter[0]));
  Tilslut.setSoTimeout(3000);
  byte[] Tekst = "TCP 한글\\n".getBytes("UTF-8");
  Tilslut.getOutputStream().write(Tekst);
  for (int positionsindeks = 0; positionsindeks < Tekst.length; positionsindeks++)
   if (Tilslut.getInputStream().read() != (Tekst[positionsindeks] & 255)) throw new RuntimeException("TCP mismatch");
  Tilslut.close();
  DatagramSocket slutpunkt = new DatagramSocket(); slutpunkt.setSoTimeout(3000);
  Tekst = "UDP 한글".getBytes("UTF-8");
  slutpunkt.send(new DatagramPacket(Tekst, Tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumenter[1])));
  byte[] svar = new byte[64]; DatagramPacket datagram = new DatagramPacket(svar, svar.length);
  slutpunkt.receive(datagram);
  if (datagram.getLength() != Tekst.length) throw new RuntimeException("UDP length");
  for (int positionsindeks = 0; positionsindeks < Tekst.length; positionsindeks++)
   if (svar[positionsindeks] != Tekst[positionsindeks]) throw new RuntimeException("UDP mismatch");
  slutpunkt.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'modtage_check': '''import java.net.*;
public class modtage_check {
 public static void main(String[] Argumenter) throws Exception {
  ServerSocket server_VÆRDI = new ServerSocket(9300); server_VÆRDI.setSoTimeout(5000);
  DatagramSocket slutpunkt = new DatagramSocket(9301); slutpunkt.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Tilslut = server_VÆRDI.accept(); Tilslut.setSoTimeout(5000);
  Tilslut.getOutputStream().write(Tilslut.getInputStream().read() + 1);
  Tilslut.close(); server_VÆRDI.close();
  byte[] data = new byte[64]; DatagramPacket datagram = new DatagramPacket(data, data.length);
  slutpunkt.receive(datagram); slutpunkt.send(datagram); slutpunkt.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Navn, KILDE in kilde_Filer.items():
        (Udgang / (Navn + '.java')).write_text(KILDE, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Udgang)] +
                          [str(Udgang / (Navn + '.java')) for Navn in kilde_Filer])
    LOG_post = bytearray()
    def 빈접속번호(Type_område=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Type_område) as SØG_VÆRDI:
            SØG_VÆRDI.bind(('127.0.0.4', 0))
            return SØG_VÆRDI.getsockname()[1]
    filport_tal, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proces_VÆRDI = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, bro_3de4fe3a(
                filport_tal, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                optage=True, vært_mail='127.0.0.4') as bro_VÆRDI:
            kontrol_sti = Path(임시) / 'qmp.sock'
            Proces_VÆRDI = subprocess.Popen(Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrol_sti)] + bro_VÆRDI.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            VÆLG_vare = selectors.DefaultSelector()
            VÆLG_vare.register(Proces_VÆRDI.stdout, selectors.EVENT_READ)
            def modtage(vise_VÆRDI=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while vise_VÆRDI not in LOG_post[처음:]:
                    if time.monotonic() > 끝 or Proces_VÆRDI.poll() is not None:
                        raise AssertionError('Missing ' + repr(vise_VÆRDI) + '\n' + LOG_post[처음:].decode('utf-8', 'replace'))
                    for tast_VÆRDI, _ in VÆLG_vare.select(.05):
                        조각 = tast_VÆRDI.fileobj.read(65536)
                        if 조각:
                            LOG_post.extend(조각)
                return LOG_post[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def maile(data):
                Proces_VÆRDI.stdin.write(data)
                Proces_VÆRDI.stdin.flush()
            def Shell(Tekst):
                print(Tekst, flush=True)
                처음 = len(LOG_post)
                maile((Tekst + '\n').encode())
                return modtage(처음=처음)
            modtage()
            with socket.socket(socket.AF_UNIX) as kontrol_VÆRDI:
                kontrol_VÆRDI.settimeout(10)
                kontrol_VÆRDI.connect(str(kontrol_sti))
                strøm_VÆRDI = kontrol_VÆRDI.makefile('rwb')
                json.loads(strøm_VÆRDI.readline())
                def anmodning(명령어, Argumenter=None):
                    data = {'execute': 명령어}
                    if Argumenter is not None:
                        data['arguments'] = Argumenter
                    strøm_VÆRDI.write((json.dumps(data) + '\n').encode())
                    strøm_VÆRDI.flush()
                    while True:
                        svar = json.loads(strøm_VÆRDI.readline())
                        if 'error' in svar:
                            raise AssertionError(svar)
                        if 'return' in svar:
                            return svar['return']
                anmodning('qmp_capabilities')
                def læserettigheder():
                    anmodning('stop')
                    try:
                        return anmodning('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        anmodning('cont')
                rapport_VÆRDI['shell_cpu'] = læserettigheder()
                assert 'EL1h' in rapport_VÆRDI['shell_cpu'], rapport_VÆRDI['shell_cpu']
                rapport_VÆRDI['initial_ps'] = Shell('ps')
                assert 'kernel/shell' in rapport_VÆRDI['initial_ps']
                rapport_VÆRDI['ipconfig'] = Shell('ipconfig')
                assert 'inet 10.0.2.15' in rapport_VÆRDI['ipconfig']
                rapport_VÆRDI['gateway_ping'] = Shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in rapport_VÆRDI['gateway_ping']
                assert 'FTP listening' in Shell('ftpd start')
                with ftplib.FTP() as overføre_VÆRDI:
                    overføre_VÆRDI.encoding = 'utf-8'
                    overføre_VÆRDI.connect('127.0.0.4', filport_tal, timeout=20)
                    overføre_VÆRDI.login()
                    for Navn in kilde_Filer:
                        overføre_VÆRDI.storbinary('STOR ' + Navn + '.class', io.BytesIO((Udgang / (Navn + '.class')).read_bytes()))
                처음 = len(LOG_post)
                maile('java rettighed_check\n'.encode())
                modtage(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    rapport_VÆRDI['java_cpu'] = læserettigheder()
                    if 'EL0t' in rapport_VÆRDI['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in rapport_VÆRDI['java_cpu'], rapport_VÆRDI['java_cpu']
                modtage(처음=처음)
                rapport_VÆRDI['after_exit_ps'] = Shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', rapport_VÆRDI['after_exit_ps'])
                rapport_VÆRDI['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as peer_VÆRDI:
                    Tekst = Shell('java netværk_check {} {}'.format(peer_VÆRDI.TCP_port, peer_VÆRDI.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                    assert peer_VÆRDI.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_VÆRDI.수신됨
                    assert not peer_VÆRDI.오류들, peer_VÆRDI.오류들
                    rapport_VÆRDI['outbound_peers'] = {종류: data.decode() for 종류, data in peer_VÆRDI.수신됨.items()}
                처음 = len(LOG_post)
                maile('java modtage_check\n'.encode())
                modtage(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as peer_VÆRDI:
                    peer_VÆRDI.sendall(b'A')
                    assert peer_VÆRDI.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_VÆRDI:
                    peer_VÆRDI.settimeout(5)
                    peer_VÆRDI.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert peer_VÆRDI.recvfrom(64)[0] == b'UDP-IN'
                Tekst = modtage(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                rapport_VÆRDI['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Shell('terminal')
                Shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_post)
                maile('java Vindueseksempel\n'.encode())
                modtage('GUI 예제 Tilrettelæg: Vindueseksempel\r\n'.encode(), 처음)
                처음 = len(LOG_post)
                maile(bytes([30, 2, 1, 0, 0, 0, 0]))
                modtage(처음=처음)
                rapport_VÆRDI['suspended_java_ps'] = Shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java Vindueseksempel', rapport_VÆRDI['suspended_java_ps']), rapport_VÆRDI['suspended_java_ps']
                rapport_VÆRDI['top'] = Shell('top -n 1')
                assert 'java Vindueseksempel' in rapport_VÆRDI['top'] and 'kernel/shell' in rapport_VÆRDI['top']
                rapport_VÆRDI['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                rapport_VÆRDI['network_trace'] = bro_VÆRDI.sporingslogfil
                assert not bro_VÆRDI.fejl, bro_VÆRDI.fejl
                maile(b'poweroff\n')
                assert Proces_VÆRDI.wait(timeout=15) == 0
                rapport_VÆRDI['passed'] = True
            VÆLG_vare.close()
    except Exception as fejl:
        rapport_VÆRDI['error'] = str(fejl)
        raise
    finally:
        if Proces_VÆRDI is not None and Proces_VÆRDI.poll() is None:
            Proces_VÆRDI.terminate()
            try:
                Proces_VÆRDI.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_VÆRDI.kill()
                Proces_VÆRDI.wait()
        (Udgang / 'serial.log').write_bytes(LOG_post)
        (Udgang / 'report.json').write_text(json.dumps(rapport_VÆRDI, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tast_VÆRDI: rapport_VÆRDI[tast_VÆRDI] for tast_VÆRDI in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Kør_2()
