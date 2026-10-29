#!/usr/bin/env python3
"""QEMU의 aktual_të_dhëna CPU leje_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from zbatoj_komandë import Project_rrënjë, Komanda
from rrjet_urë import rrjet_urë
from 되돌림시험서버 import 되돌림시험서버


def Ekzekuto():
    출력 = Project_rrënjë / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    raport_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_rrënjë / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    burim_Skedarët = {
        'leje_çek': '''public class leje_çek {
 public static void main(String[] Argumente) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'rrjet_çek': '''import java.net.*;
public class rrjet_çek {
 public static void main(String[] Argumente) throws Exception {
  Socket Lidhu = new Socket("10.0.2.2", Integer.parseInt(Argumente[0]));
  Lidhu.setSoTimeout(3000);
  byte[] Teksti = "TCP 한글\\n".getBytes("UTF-8");
  Lidhu.getOutputStream().write(Teksti);
  for (int pozicioni_INDEX = 0; pozicioni_INDEX < Teksti.length; pozicioni_INDEX++)
   if (Lidhu.getInputStream().read() != (Teksti[pozicioni_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Lidhu.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Teksti = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Teksti, Teksti.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumente[1])));
  byte[] replikë = new byte[64]; DatagramPacket 전문 = new DatagramPacket(replikë, replikë.length);
  종단.receive(전문);
  if (전문.getLength() != Teksti.length) throw new RuntimeException("UDP length");
  for (int pozicioni_INDEX = 0; pozicioni_INDEX < Teksti.length; pozicioni_INDEX++)
   if (replikë[pozicioni_INDEX] != Teksti[pozicioni_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Argumente) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Lidhu = server_VALUE.accept(); Lidhu.setSoTimeout(5000);
  Lidhu.getOutputStream().write(Lidhu.getInputStream().read() + 1);
  Lidhu.close(); server_VALUE.close();
  byte[] të_dhëna = new byte[64]; DatagramPacket 전문 = new DatagramPacket(të_dhëna, të_dhëna.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Emër, BURIMI in burim_Skedarët.items():
        (출력 / (Emër + '.java')).write_text(BURIMI, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Emër + '.java')) for Emër in burim_Skedarët])
    LOG_RECORD = bytearray()
    def bosh_numri_i_portës(TYPE_kategori=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_kategori) as Kërkim_VALUE:
            Kërkim_VALUE.bind(('127.0.0.4', 0))
            return Kërkim_VALUE.getsockname()[1]
    skedar_numri_i_portës, TCP_portë, UDP_portë = bosh_numri_i_portës(), bosh_numri_i_portës(), bosh_numri_i_portës(socket.SOCK_DGRAM)
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, rrjet_urë(
                skedar_numri_i_portës, ['tcp:{}:9300'.format(TCP_portë), 'udp:{}:9301'.format(UDP_portë)],
                kap=True, pritës_email='127.0.0.4') as urë_VALUE:
            kontroll_shteg = Path(임시) / 'qmp.sock'
            Proces_VALUE = subprocess.Popen(Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontroll_shteg)] + urë_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_njësi = selectors.DefaultSelector()
            CHOOSE_njësi.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def 받기(shfaq_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while shfaq_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(shfaq_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for tast_VALUE, _ in CHOOSE_njësi.select(.05):
                        조각 = tast_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def dërgoj(të_dhëna):
                Proces_VALUE.stdin.write(të_dhëna)
                Proces_VALUE.stdin.flush()
            def pasues(Teksti):
                print(Teksti, flush=True)
                처음 = len(LOG_RECORD)
                dërgoj((Teksti + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as kontroll_VALUE:
                kontroll_VALUE.settimeout(10)
                kontroll_VALUE.connect(str(kontroll_shteg))
                Stream_VALUE = kontroll_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def 요청(instruksion_VALUE, Argumente=None):
                    të_dhëna = {'execute': instruksion_VALUE}
                    if Argumente is not None:
                        të_dhëna['arguments'] = Argumente
                    Stream_VALUE.write((json.dumps(të_dhëna) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        replikë = json.loads(Stream_VALUE.readline())
                        if 'error' in replikë:
                            raise AssertionError(replikë)
                        if 'return' in replikë:
                            return replikë['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                raport_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in raport_VALUE['shell_cpu'], raport_VALUE['shell_cpu']
                raport_VALUE['initial_ps'] = pasues('ps')
                assert 'kernel/shell' in raport_VALUE['initial_ps']
                raport_VALUE['ipconfig'] = pasues('ipconfig')
                assert 'inet 10.0.2.15' in raport_VALUE['ipconfig']
                raport_VALUE['gateway_ping'] = pasues('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in raport_VALUE['gateway_ping']
                assert 'FTP listening' in pasues('ftpd start')
                with ftplib.FTP() as transferim_VALUE:
                    transferim_VALUE.encoding = 'utf-8'
                    transferim_VALUE.connect('127.0.0.4', skedar_numri_i_portës, timeout=20)
                    transferim_VALUE.login()
                    for Emër in burim_Skedarët:
                        transferim_VALUE.storbinary('STOR ' + Emër + '.class', io.BytesIO((출력 / (Emër + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                dërgoj('java leje_çek\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    raport_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in raport_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in raport_VALUE['java_cpu'], raport_VALUE['java_cpu']
                받기(처음=처음)
                raport_VALUE['after_exit_ps'] = pasues('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', raport_VALUE['after_exit_ps'])
                raport_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as homolog_VALUE:
                    Teksti = pasues('java rrjet_çek {} {}'.format(homolog_VALUE.TCP_portë, homolog_VALUE.UDP_portë))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Teksti and 'exit 0' in Teksti, Teksti
                    assert homolog_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, homolog_VALUE.수신됨
                    assert not homolog_VALUE.오류들, homolog_VALUE.오류들
                    raport_VALUE['outbound_peers'] = {종류: të_dhëna.decode() for 종류, të_dhëna in homolog_VALUE.수신됨.items()}
                처음 = len(LOG_RECORD)
                dërgoj('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_portë), timeout=5) as homolog_VALUE:
                    homolog_VALUE.sendall(b'A')
                    assert homolog_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as homolog_VALUE:
                    homolog_VALUE.settimeout(5)
                    homolog_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_portë))
                    assert homolog_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Teksti = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Teksti and 'exit 0' in Teksti, Teksti
                raport_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in pasues('terminal')
                pasues('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                dërgoj('java 창예제\n'.encode())
                받기('GUI 예제 Përgatit: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                dërgoj(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                raport_VALUE['suspended_java_ps'] = pasues('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', raport_VALUE['suspended_java_ps']), raport_VALUE['suspended_java_ps']
                raport_VALUE['top'] = pasues('top -n 1')
                assert 'java 창예제' in raport_VALUE['top'] and 'kernel/shell' in raport_VALUE['top']
                raport_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                raport_VALUE['network_trace'] = urë_VALUE.gjurmë_LOG
                assert not urë_VALUE.GABIM, urë_VALUE.GABIM
                dërgoj(b'poweroff\n')
                assert Proces_VALUE.wait(timeout=15) == 0
                raport_VALUE['passed'] = True
            CHOOSE_njësi.close()
    except Exception as GABIM:
        raport_VALUE['error'] = str(GABIM)
        raise
    finally:
        if Proces_VALUE is not None and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:
                Proces_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_VALUE.kill()
                Proces_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_RECORD)
        (출력 / 'report.json').write_text(json.dumps(raport_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tast_VALUE: raport_VALUE[tast_VALUE] for tast_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Ekzekuto()
