#!/usr/bin/env python3
"""QEMU의 tegelik_andmed CPU luba_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Täida_käsk import Project_juur, Käsk
from sild_3de4fe3a import sild_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Käivita_2():
    Väljund = Project_juur / 'build/verification/execution-network-review'
    Väljund.mkdir(parents=True, exist_ok=True)
    aruanne_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_juur / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    lähe_Failid = {
        'luba_tšekk': '''public class luba_tšekk {
 public static void main(String[] Argumendid) {
  System.out.println("EL0_PROBE_READY");
  int number = 0; while (true) { number++; }
 }
}''',
        'võrk_tšekk': '''import java.net.*;
public class võrk_tšekk {
 public static void main(String[] Argumendid) throws Exception {
  Socket Ühendu = new Socket("10.0.2.2", Integer.parseInt(Argumendid[0]));
  Ühendu.setSoTimeout(3000);
  byte[] Tekst = "TCP 한글\\n".getBytes("UTF-8");
  Ühendu.getOutputStream().write(Tekst);
  for (int asukohaindeks = 0; asukohaindeks < Tekst.length; asukohaindeks++)
   if (Ühendu.getInputStream().read() != (Tekst[asukohaindeks] & 255)) throw new RuntimeException("TCP mismatch");
  Ühendu.close();
  DatagramSocket osaleja = new DatagramSocket(); osaleja.setSoTimeout(3000);
  Tekst = "UDP 한글".getBytes("UTF-8");
  osaleja.send(new DatagramPacket(Tekst, Tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumendid[1])));
  byte[] vastus = new byte[64]; DatagramPacket datagramm = new DatagramPacket(vastus, vastus.length);
  osaleja.receive(datagramm);
  if (datagramm.getLength() != Tekst.length) throw new RuntimeException("UDP length");
  for (int asukohaindeks = 0; asukohaindeks < Tekst.length; asukohaindeks++)
   if (vastus[asukohaindeks] != Tekst[asukohaindeks]) throw new RuntimeException("UDP mismatch");
  osaleja.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'saama_tšekk': '''import java.net.*;
public class saama_tšekk {
 public static void main(String[] Argumendid) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket osaleja = new DatagramSocket(9301); osaleja.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Ühendu = server_VALUE.accept(); Ühendu.setSoTimeout(5000);
  Ühendu.getOutputStream().write(Ühendu.getInputStream().read() + 1);
  Ühendu.close(); server_VALUE.close();
  byte[] andmed = new byte[64]; DatagramPacket datagramm = new DatagramPacket(andmed, andmed.length);
  osaleja.receive(datagramm); osaleja.send(datagramm); osaleja.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Nimi_2, ALLIKAS in lähe_Failid.items():
        (Väljund / (Nimi_2 + '.java')).write_text(ALLIKAS, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Väljund)] +
                          [str(Väljund / (Nimi_2 + '.java')) for Nimi_2 in lähe_Failid])
    LOG_kirje = bytearray()
    def 빈접속번호(TYPE_ala=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_ala) as Otsi_VALUE:
            Otsi_VALUE.bind(('127.0.0.4', 0))
            return Otsi_VALUE.getsockname()[1]
    Fail_pordinumber, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Joonis_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, sild_3de4fe3a(
                Fail_pordinumber, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                hõivama=True, host_ADDRESS='127.0.0.4') as sild_VALUE:
            meede_tee = Path(임시) / 'qmp.sock'
            Joonis_VALUE = subprocess.Popen(Käsk() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(meede_tee)] + sild_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_kaup = selectors.DefaultSelector()
            CHOOSE_kaup.register(Joonis_VALUE.stdout, selectors.EVENT_READ)
            def saama(saade_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while saade_VALUE not in LOG_kirje[처음:]:
                    if time.monotonic() > 끝 or Joonis_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(saade_VALUE) + '\n' + LOG_kirje[처음:].decode('utf-8', 'replace'))
                    for Võti_VALUE, _ in CHOOSE_kaup.select(.05):
                        조각 = Võti_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_kirje.extend(조각)
                return LOG_kirje[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def saatma(andmed):
                Joonis_VALUE.stdin.write(andmed)
                Joonis_VALUE.stdin.flush()
            def kest(Tekst):
                print(Tekst, flush=True)
                처음 = len(LOG_kirje)
                saatma((Tekst + '\n').encode())
                return saama(처음=처음)
            saama()
            with socket.socket(socket.AF_UNIX) as meede_VALUE:
                meede_VALUE.settimeout(10)
                meede_VALUE.connect(str(meede_tee))
                voog_VALUE = meede_VALUE.makefile('rwb')
                json.loads(voog_VALUE.readline())
                def päring(명령어, Argumendid=None):
                    andmed = {'execute': 명령어}
                    if Argumendid is not None:
                        andmed['arguments'] = Argumendid
                    voog_VALUE.write((json.dumps(andmed) + '\n').encode())
                    voog_VALUE.flush()
                    while True:
                        vastus = json.loads(voog_VALUE.readline())
                        if 'error' in vastus:
                            raise AssertionError(vastus)
                        if 'return' in vastus:
                            return vastus['return']
                päring('qmp_capabilities')
                def 권한읽기():
                    päring('stop')
                    try:
                        return päring('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        päring('cont')
                aruanne_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in aruanne_VALUE['shell_cpu'], aruanne_VALUE['shell_cpu']
                aruanne_VALUE['initial_ps'] = kest('ps')
                assert 'kernel/shell' in aruanne_VALUE['initial_ps']
                aruanne_VALUE['ipconfig'] = kest('ipconfig')
                assert 'inet 10.0.2.15' in aruanne_VALUE['ipconfig']
                aruanne_VALUE['gateway_ping'] = kest('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in aruanne_VALUE['gateway_ping']
                assert 'FTP listening' in kest('ftpd start')
                with ftplib.FTP() as Edasta_VALUE:
                    Edasta_VALUE.encoding = 'utf-8'
                    Edasta_VALUE.connect('127.0.0.4', Fail_pordinumber, timeout=20)
                    Edasta_VALUE.login()
                    for Nimi_2 in lähe_Failid:
                        Edasta_VALUE.storbinary('STOR ' + Nimi_2 + '.class', io.BytesIO((Väljund / (Nimi_2 + '.class')).read_bytes()))
                처음 = len(LOG_kirje)
                saatma('java luba_tšekk\n'.encode())
                saama(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    aruanne_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in aruanne_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in aruanne_VALUE['java_cpu'], aruanne_VALUE['java_cpu']
                saama(처음=처음)
                aruanne_VALUE['after_exit_ps'] = kest('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', aruanne_VALUE['after_exit_ps'])
                aruanne_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as partner_VALUE:
                    Tekst = kest('java võrk_tšekk {} {}'.format(partner_VALUE.TCP_port, partner_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                    assert partner_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, partner_VALUE.수신됨
                    assert not partner_VALUE.오류들, partner_VALUE.오류들
                    aruanne_VALUE['outbound_peers'] = {종류: andmed.decode() for 종류, andmed in partner_VALUE.수신됨.items()}
                처음 = len(LOG_kirje)
                saatma('java saama_tšekk\n'.encode())
                saama(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as partner_VALUE:
                    partner_VALUE.sendall(b'A')
                    assert partner_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as partner_VALUE:
                    partner_VALUE.settimeout(5)
                    partner_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert partner_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Tekst = saama(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                aruanne_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in kest('terminal')
                kest('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_kirje)
                saatma('java AknaNäide\n'.encode())
                saama('GUI 예제 Ettevalmistamine: AknaNäide\r\n'.encode(), 처음)
                처음 = len(LOG_kirje)
                saatma(bytes([30, 2, 1, 0, 0, 0, 0]))
                saama(처음=처음)
                aruanne_VALUE['suspended_java_ps'] = kest('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java AknaNäide', aruanne_VALUE['suspended_java_ps']), aruanne_VALUE['suspended_java_ps']
                aruanne_VALUE['top'] = kest('top -n 1')
                assert 'java AknaNäide' in aruanne_VALUE['top'] and 'kernel/shell' in aruanne_VALUE['top']
                aruanne_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                aruanne_VALUE['network_trace'] = sild_VALUE.jälituslogi
                assert not sild_VALUE.VIGA, sild_VALUE.VIGA
                saatma(b'poweroff\n')
                assert Joonis_VALUE.wait(timeout=15) == 0
                aruanne_VALUE['passed'] = True
            CHOOSE_kaup.close()
    except Exception as VIGA:
        aruanne_VALUE['error'] = str(VIGA)
        raise
    finally:
        if Joonis_VALUE is not None and Joonis_VALUE.poll() is None:
            Joonis_VALUE.terminate()
            try:
                Joonis_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Joonis_VALUE.kill()
                Joonis_VALUE.wait()
        (Väljund / 'serial.log').write_bytes(LOG_kirje)
        (Väljund / 'report.json').write_text(json.dumps(aruanne_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Võti_VALUE: aruanne_VALUE[Võti_VALUE] for Võti_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Käivita_2()
