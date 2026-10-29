#!/usr/bin/env python3
"""QEMU의 totoo_data CPU pahintulot_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Mag_execute_utos import Project_root, utos
from Network_bridge import Network_bridge
from 되돌림시험서버 import 되돌림시험서버


def run():
    출력 = Project_root / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ulat_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_root / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    pinagmulan_Mga_File = {
        'pahintulot_tseke': '''public class pahintulot_tseke {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Network_tseke': '''import java.net.*;
public class Network_tseke {
 public static void main(String[] 인수) throws Exception {
  Socket CONNECT = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  CONNECT.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  CONNECT.getOutputStream().write(SMS);
  for (int posisyon_INDEX = 0; posisyon_INDEX < SMS.length; posisyon_INDEX++)
   if (CONNECT.getInputStream().read() != (SMS[posisyon_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  CONNECT.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] tumugon = new byte[64]; DatagramPacket 전문 = new DatagramPacket(tumugon, tumugon.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int posisyon_INDEX = 0; posisyon_INDEX < SMS.length; posisyon_INDEX++)
   if (tumugon[posisyon_INDEX] != SMS[posisyon_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket CONNECT = server_VALUE.accept(); CONNECT.setSoTimeout(5000);
  CONNECT.getOutputStream().write(CONNECT.getInputStream().read() + 1);
  CONNECT.close(); server_VALUE.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for pangalan, pinagmulan in pinagmulan_Mga_File.items():
        (출력 / (pangalan + '.java')).write_text(pinagmulan, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (pangalan + '.java')) for pangalan in pinagmulan_Mga_File])
    LOG_hanay = bytearray()
    def walang_laman_numero_ng_port(TYPE_kategorya=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_kategorya) as SEARCH_VALUE:
            SEARCH_VALUE.bind(('127.0.0.4', 0))
            return SEARCH_VALUE.getsockname()[1]
    file_numero_ng_port, TCP_port, UDP_port = walang_laman_numero_ng_port(), walang_laman_numero_ng_port(), walang_laman_numero_ng_port(socket.SOCK_DGRAM)
    Proseso_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Network_bridge(
                file_numero_ng_port, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                mag_capture=True, host_email='127.0.0.4') as bridge_VALUE:
            control_path = Path(임시) / 'qmp.sock'
            Proseso_VALUE = subprocess.Popen(utos() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(control_path)] + bridge_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_item = selectors.DefaultSelector()
            CHOOSE_item.register(Proseso_VALUE.stdout, selectors.EVENT_READ)
            def 받기(ipakita_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ipakita_VALUE not in LOG_hanay[처음:]:
                    if time.monotonic() > 끝 or Proseso_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(ipakita_VALUE) + '\n' + LOG_hanay[처음:].decode('utf-8', 'replace'))
                    for key_VALUE, _ in CHOOSE_item.select(.05):
                        조각 = key_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_hanay.extend(조각)
                return LOG_hanay[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def i_email(data):
                Proseso_VALUE.stdin.write(data)
                Proseso_VALUE.stdin.flush()
            def shell(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_hanay)
                i_email((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as control_VALUE:
                control_VALUE.settimeout(10)
                control_VALUE.connect(str(control_path))
                Stream_VALUE = control_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def 요청(instruksiyon_VALUE, 인수=None):
                    data = {'execute': instruksiyon_VALUE}
                    if 인수 is not None:
                        data['arguments'] = 인수
                    Stream_VALUE.write((json.dumps(data) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        tumugon = json.loads(Stream_VALUE.readline())
                        if 'error' in tumugon:
                            raise AssertionError(tumugon)
                        if 'return' in tumugon:
                            return tumugon['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ulat_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ulat_VALUE['shell_cpu'], ulat_VALUE['shell_cpu']
                ulat_VALUE['initial_ps'] = shell('ps')
                assert 'kernel/shell' in ulat_VALUE['initial_ps']
                ulat_VALUE['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in ulat_VALUE['ipconfig']
                ulat_VALUE['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ulat_VALUE['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as lipat_VALUE:
                    lipat_VALUE.encoding = 'utf-8'
                    lipat_VALUE.connect('127.0.0.4', file_numero_ng_port, timeout=20)
                    lipat_VALUE.login()
                    for pangalan in pinagmulan_Mga_File:
                        lipat_VALUE.storbinary('STOR ' + pangalan + '.class', io.BytesIO((출력 / (pangalan + '.class')).read_bytes()))
                처음 = len(LOG_hanay)
                i_email('java pahintulot_tseke\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ulat_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in ulat_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ulat_VALUE['java_cpu'], ulat_VALUE['java_cpu']
                받기(처음=처음)
                ulat_VALUE['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ulat_VALUE['after_exit_ps'])
                ulat_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as peer_VALUE:
                    SMS = shell('java Network_tseke {} {}'.format(peer_VALUE.TCP_port, peer_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert peer_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, peer_VALUE.수신됨
                    assert not peer_VALUE.오류들, peer_VALUE.오류들
                    ulat_VALUE['outbound_peers'] = {종류: data.decode() for 종류, data in peer_VALUE.수신됨.items()}
                처음 = len(LOG_hanay)
                i_email('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as peer_VALUE:
                    peer_VALUE.sendall(b'A')
                    assert peer_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as peer_VALUE:
                    peer_VALUE.settimeout(5)
                    peer_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert peer_VALUE.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                ulat_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_hanay)
                i_email('java 창예제\n'.encode())
                받기('GUI 예제 Ihanda: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_hanay)
                i_email(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ulat_VALUE['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ulat_VALUE['suspended_java_ps']), ulat_VALUE['suspended_java_ps']
                ulat_VALUE['top'] = shell('top -n 1')
                assert 'java 창예제' in ulat_VALUE['top'] and 'kernel/shell' in ulat_VALUE['top']
                ulat_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ulat_VALUE['network_trace'] = bridge_VALUE.trace_LOG
                assert not bridge_VALUE.error, bridge_VALUE.error
                i_email(b'poweroff\n')
                assert Proseso_VALUE.wait(timeout=15) == 0
                ulat_VALUE['passed'] = True
            CHOOSE_item.close()
    except Exception as error:
        ulat_VALUE['error'] = str(error)
        raise
    finally:
        if Proseso_VALUE is not None and Proseso_VALUE.poll() is None:
            Proseso_VALUE.terminate()
            try:
                Proseso_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proseso_VALUE.kill()
                Proseso_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_hanay)
        (출력 / 'report.json').write_text(json.dumps(ulat_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({key_VALUE: ulat_VALUE[key_VALUE] for key_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    run()
