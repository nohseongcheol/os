#!/usr/bin/env python3
"""QEMU의 go_iawn_data CPU hawl_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Gweithredu_gorchymyn import prosiect_gwraidd, Gorchymyn
from Rhwydwaith_pont import Rhwydwaith_pont
from 되돌림시험서버 import 되돌림시험서버


def Gweithredu_2():
    Allbwn = prosiect_gwraidd / 'build/verification/execution-network-review'
    Allbwn.mkdir(parents=True, exist_ok=True)
    adrodd_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((prosiect_gwraidd / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ffynhonnell_Ffeil = {
        'hawl_gwirio': '''public class hawl_gwirio {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Rhwydwaith_gwirio': '''import java.net.*;
public class Rhwydwaith_gwirio {
 public static void main(String[] 인수) throws Exception {
  Socket Cysylltu = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Cysylltu.setSoTimeout(3000);
  byte[] Testun = "TCP 한글\\n".getBytes("UTF-8");
  Cysylltu.getOutputStream().write(Testun);
  for (int safle_INDEX = 0; safle_INDEX < Testun.length; safle_INDEX++)
   if (Cysylltu.getInputStream().read() != (Testun[safle_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Cysylltu.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Testun = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Testun, Testun.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] ateb = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ateb, ateb.length);
  종단.receive(전문);
  if (전문.getLength() != Testun.length) throw new RuntimeException("UDP length");
  for (int safle_INDEX = 0; safle_INDEX < Testun.length; safle_INDEX++)
   if (ateb[safle_INDEX] != Testun[safle_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket gweinydd_VALUE = new ServerSocket(9300); gweinydd_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Cysylltu = gweinydd_VALUE.accept(); Cysylltu.setSoTimeout(5000);
  Cysylltu.getOutputStream().write(Cysylltu.getInputStream().read() + 1);
  Cysylltu.close(); gweinydd_VALUE.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Enw, FFYNHONNELL in ffynhonnell_Ffeil.items():
        (Allbwn / (Enw + '.java')).write_text(FFYNHONNELL, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Allbwn)] +
                          [str(Allbwn / (Enw + '.java')) for Enw in ffynhonnell_Ffeil])
    LOG_rhes = bytearray()
    def gwag_rhif_porth(TYPE_ardal=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_ardal) as SEARCH_VALUE:
            SEARCH_VALUE.bind(('127.0.0.4', 0))
            return SEARCH_VALUE.getsockname()[1]
    ffeil_rhif_porth, TCP_porth, UDP_porth = gwag_rhif_porth(), gwag_rhif_porth(), gwag_rhif_porth(socket.SOCK_DGRAM)
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Rhwydwaith_pont(
                ffeil_rhif_porth, ['tcp:{}:9300'.format(TCP_porth), 'udp:{}:9301'.format(UDP_porth)],
                recordio=True, lletya_ADDRESS='127.0.0.4') as pont_VALUE:
            rheoli_llwybr = Path(임시) / 'qmp.sock'
            Proses_VALUE = subprocess.Popen(Gorchymyn() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(rheoli_llwybr)] + pont_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            dewis_eitem = selectors.DefaultSelector()
            dewis_eitem.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def 받기(sioe_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while sioe_VALUE not in LOG_rhes[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(sioe_VALUE) + '\n' + LOG_rhes[처음:].decode('utf-8', 'replace'))
                    for bysell_VALUE, _ in dewis_eitem.select(.05):
                        조각 = bysell_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_rhes.extend(조각)
                return LOG_rhes[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def anfon(data):
                Proses_VALUE.stdin.write(data)
                Proses_VALUE.stdin.flush()
            def cragen(Testun):
                print(Testun, flush=True)
                처음 = len(LOG_rhes)
                anfon((Testun + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as rheoli_VALUE:
                rheoli_VALUE.settimeout(10)
                rheoli_VALUE.connect(str(rheoli_llwybr))
                ffrwd_VALUE = rheoli_VALUE.makefile('rwb')
                json.loads(ffrwd_VALUE.readline())
                def cais_HTTP(cyfarwyddyd_VALUE, 인수=None):
                    data = {'execute': cyfarwyddyd_VALUE}
                    if 인수 is not None:
                        data['arguments'] = 인수
                    ffrwd_VALUE.write((json.dumps(data) + '\n').encode())
                    ffrwd_VALUE.flush()
                    while True:
                        ateb = json.loads(ffrwd_VALUE.readline())
                        if 'error' in ateb:
                            raise AssertionError(ateb)
                        if 'return' in ateb:
                            return ateb['return']
                cais_HTTP('qmp_capabilities')
                def 권한읽기():
                    cais_HTTP('stop')
                    try:
                        return cais_HTTP('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        cais_HTTP('cont')
                adrodd_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in adrodd_VALUE['shell_cpu'], adrodd_VALUE['shell_cpu']
                adrodd_VALUE['initial_ps'] = cragen('ps')
                assert 'kernel/shell' in adrodd_VALUE['initial_ps']
                adrodd_VALUE['ipconfig'] = cragen('ipconfig')
                assert 'inet 10.0.2.15' in adrodd_VALUE['ipconfig']
                adrodd_VALUE['gateway_ping'] = cragen('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in adrodd_VALUE['gateway_ping']
                assert 'FTP listening' in cragen('ftpd start')
                with ftplib.FTP() as trosglwyddo_VALUE:
                    trosglwyddo_VALUE.encoding = 'utf-8'
                    trosglwyddo_VALUE.connect('127.0.0.4', ffeil_rhif_porth, timeout=20)
                    trosglwyddo_VALUE.login()
                    for Enw in ffynhonnell_Ffeil:
                        trosglwyddo_VALUE.storbinary('STOR ' + Enw + '.class', io.BytesIO((Allbwn / (Enw + '.class')).read_bytes()))
                처음 = len(LOG_rhes)
                anfon('java hawl_gwirio\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    adrodd_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in adrodd_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in adrodd_VALUE['java_cpu'], adrodd_VALUE['java_cpu']
                받기(처음=처음)
                adrodd_VALUE['after_exit_ps'] = cragen('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', adrodd_VALUE['after_exit_ps'])
                adrodd_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as cymar_VALUE:
                    Testun = cragen('java Rhwydwaith_gwirio {} {}'.format(cymar_VALUE.TCP_porth, cymar_VALUE.UDP_porth))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Testun and 'exit 0' in Testun, Testun
                    assert cymar_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, cymar_VALUE.수신됨
                    assert not cymar_VALUE.오류들, cymar_VALUE.오류들
                    adrodd_VALUE['outbound_peers'] = {종류: data.decode() for 종류, data in cymar_VALUE.수신됨.items()}
                처음 = len(LOG_rhes)
                anfon('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_porth), timeout=5) as cymar_VALUE:
                    cymar_VALUE.sendall(b'A')
                    assert cymar_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as cymar_VALUE:
                    cymar_VALUE.settimeout(5)
                    cymar_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_porth))
                    assert cymar_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Testun = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Testun and 'exit 0' in Testun, Testun
                adrodd_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in cragen('terminal')
                cragen('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_rhes)
                anfon('java 창예제\n'.encode())
                받기('GUI 예제 Paratoi: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_rhes)
                anfon(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                adrodd_VALUE['suspended_java_ps'] = cragen('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', adrodd_VALUE['suspended_java_ps']), adrodd_VALUE['suspended_java_ps']
                adrodd_VALUE['top'] = cragen('top -n 1')
                assert 'java 창예제' in adrodd_VALUE['top'] and 'kernel/shell' in adrodd_VALUE['top']
                adrodd_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                adrodd_VALUE['network_trace'] = pont_VALUE.olrhain_LOG
                assert not pont_VALUE.Gwall, pont_VALUE.Gwall
                anfon(b'poweroff\n')
                assert Proses_VALUE.wait(timeout=15) == 0
                adrodd_VALUE['passed'] = True
            dewis_eitem.close()
    except Exception as Gwall:
        adrodd_VALUE['error'] = str(Gwall)
        raise
    finally:
        if Proses_VALUE is not None and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:
                Proses_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proses_VALUE.kill()
                Proses_VALUE.wait()
        (Allbwn / 'serial.log').write_bytes(LOG_rhes)
        (Allbwn / 'report.json').write_text(json.dumps(adrodd_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({bysell_VALUE: adrodd_VALUE[bysell_VALUE] for bysell_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Gweithredu_2()
