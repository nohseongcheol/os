#!/usr/bin/env python3
"""QEMU의 gangan_détà CPU Ìyànda_iye, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ṣiṣẹ́_àṣẹ import 기준, Àṣẹ
from Alásopọ̀_afará import Alásopọ̀_afará
from 되돌림시험서버 import 되돌림시험서버


def Rọ́ọ̀nù():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ìjábọ̀_iye = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    orísun_Àwọn_fáìlì = {
        'ìgbaniláàyè_ṣàyẹ̀wò': '''public class ìgbaniláàyè_ṣàyẹ̀wò {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Alásopọ̀_ṣàyẹ̀wò': '''import java.net.*;
public class Alásopọ̀_ṣàyẹ̀wò {
 public static void main(String[] 인수) throws Exception {
  Socket Darapọ̀ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Darapọ̀.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  Darapọ̀.getOutputStream().write(SMS);
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (Darapọ̀.getInputStream().read() != (SMS[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Darapọ̀.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] Fèsì = new byte[64]; DatagramPacket 전문 = new DatagramPacket(Fèsì, Fèsì.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (Fèsì[자리] != SMS[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket apèsè_iye = new ServerSocket(9300); apèsè_iye.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Darapọ̀ = apèsè_iye.accept(); Darapọ̀.setSoTimeout(5000);
  Darapọ̀.getOutputStream().write(Darapọ̀.getInputStream().read() + 1);
  Darapọ̀.close(); apèsè_iye.close();
  byte[] détà = new byte[64]; DatagramPacket 전문 = new DatagramPacket(détà, détà.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Orúkọ, orísun in orísun_Àwọn_fáìlì.items():
        (출력 / (Orúkọ + '.java')).write_text(orísun, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Orúkọ + '.java')) for Orúkọ in orísun_Àwọn_fáìlì])
    àkọsílẹ̀_ìṣe_ìlà_ìbú = bytearray()
    def 빈접속번호(irú_ìsọ̀rí=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, irú_ìsọ̀rí) as wákiri_iye:
            wákiri_iye.bind(('127.0.0.4', 0))
            return wákiri_iye.getsockname()[1]
    파일접속번호, TCP_ojú, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Ìlànà_iye = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Alásopọ̀_afará(
                파일접속번호, ['tcp:{}:9300'.format(TCP_ojú), 'udp:{}:9301'.format(전문접속번호)],
                gbàwòránsílẹ̀=True, olùpèsè_àdírẹ́ẹ̀sì='127.0.0.4') as afará_iye:
            ìdarí_ọ̀nà = Path(임시) / 'qmp.sock'
            Ìlànà_iye = subprocess.Popen(Àṣẹ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ìdarí_ọ̀nà)] + afará_iye.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            yan_wúnrẹ̀n = selectors.DefaultSelector()
            yan_wúnrẹ̀n.register(Ìlànà_iye.stdout, selectors.EVENT_READ)
            def 받기(ṣàfihàn_iye=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ṣàfihàn_iye not in àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:]:
                    if time.monotonic() > 끝 or Ìlànà_iye.poll() is not None:
                        raise AssertionError('Missing ' + repr(ṣàfihàn_iye) + '\n' + àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:].decode('utf-8', 'replace'))
                    for bọ́tìnnì_iye, _ in yan_wúnrẹ̀n.select(.05):
                        조각 = bọ́tìnnì_iye.fileobj.read(65536)
                        if 조각:
                            àkọsílẹ̀_ìṣe_ìlà_ìbú.extend(조각)
                return àkọsílẹ̀_ìṣe_ìlà_ìbú[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def í_meèlì(détà):
                Ìlànà_iye.stdin.write(détà)
                Ìlànà_iye.stdin.flush()
            def ṣẹ́ẹ̀lì(SMS):
                print(SMS, flush=True)
                처음 = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                í_meèlì((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ìdarí_iye:
                ìdarí_iye.settimeout(10)
                ìdarí_iye.connect(str(ìdarí_ọ̀nà))
                Stream_iye = ìdarí_iye.makefile('rwb')
                json.loads(Stream_iye.readline())
                def 요청(ìtọ́sọ́nà_iye, 인수=None):
                    détà = {'execute': ìtọ́sọ́nà_iye}
                    if 인수 is not None:
                        détà['arguments'] = 인수
                    Stream_iye.write((json.dumps(détà) + '\n').encode())
                    Stream_iye.flush()
                    while True:
                        Fèsì = json.loads(Stream_iye.readline())
                        if 'error' in Fèsì:
                            raise AssertionError(Fèsì)
                        if 'return' in Fèsì:
                            return Fèsì['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ìjábọ̀_iye['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ìjábọ̀_iye['shell_cpu'], ìjábọ̀_iye['shell_cpu']
                ìjábọ̀_iye['initial_ps'] = ṣẹ́ẹ̀lì('ps')
                assert 'kernel/shell' in ìjábọ̀_iye['initial_ps']
                ìjábọ̀_iye['ipconfig'] = ṣẹ́ẹ̀lì('ipconfig')
                assert 'inet 10.0.2.15' in ìjábọ̀_iye['ipconfig']
                ìjábọ̀_iye['gateway_ping'] = ṣẹ́ẹ̀lì('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ìjábọ̀_iye['gateway_ping']
                assert 'FTP listening' in ṣẹ́ẹ̀lì('ftpd start')
                with ftplib.FTP() as ṣàgbélọ_iye:
                    ṣàgbélọ_iye.encoding = 'utf-8'
                    ṣàgbélọ_iye.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ṣàgbélọ_iye.login()
                    for Orúkọ in orísun_Àwọn_fáìlì:
                        ṣàgbélọ_iye.storbinary('STOR ' + Orúkọ + '.class', io.BytesIO((출력 / (Orúkọ + '.class')).read_bytes()))
                처음 = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                í_meèlì('java ìgbaniláàyè_ṣàyẹ̀wò\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ìjábọ̀_iye['java_cpu'] = 권한읽기()
                    if 'EL0t' in ìjábọ̀_iye['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ìjábọ̀_iye['java_cpu'], ìjábọ̀_iye['java_cpu']
                받기(처음=처음)
                ìjábọ̀_iye['after_exit_ps'] = ṣẹ́ẹ̀lì('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ìjábọ̀_iye['after_exit_ps'])
                ìjábọ̀_iye['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ọ̀gbà_iye:
                    SMS = ṣẹ́ẹ̀lì('java Alásopọ̀_ṣàyẹ̀wò {} {}'.format(ọ̀gbà_iye.TCP_ojú, ọ̀gbà_iye.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert ọ̀gbà_iye.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ọ̀gbà_iye.수신됨
                    assert not ọ̀gbà_iye.오류들, ọ̀gbà_iye.오류들
                    ìjábọ̀_iye['outbound_peers'] = {종류: détà.decode() for 종류, détà in ọ̀gbà_iye.수신됨.items()}
                처음 = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                í_meèlì('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_ojú), timeout=5) as ọ̀gbà_iye:
                    ọ̀gbà_iye.sendall(b'A')
                    assert ọ̀gbà_iye.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ọ̀gbà_iye:
                    ọ̀gbà_iye.settimeout(5)
                    ọ̀gbà_iye.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ọ̀gbà_iye.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                ìjábọ̀_iye['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ṣẹ́ẹ̀lì('terminal')
                ṣẹ́ẹ̀lì('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                í_meèlì('java 창예제\n'.encode())
                받기('GUI 예제 gbaradì: 창예제\r\n'.encode(), 처음)
                처음 = len(àkọsílẹ̀_ìṣe_ìlà_ìbú)
                í_meèlì(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ìjábọ̀_iye['suspended_java_ps'] = ṣẹ́ẹ̀lì('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ìjábọ̀_iye['suspended_java_ps']), ìjábọ̀_iye['suspended_java_ps']
                ìjábọ̀_iye['top'] = ṣẹ́ẹ̀lì('top -n 1')
                assert 'java 창예제' in ìjábọ̀_iye['top'] and 'kernel/shell' in ìjábọ̀_iye['top']
                ìjábọ̀_iye['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ìjábọ̀_iye['network_trace'] = afará_iye.àròpọ̀_mátirísì_adọ́gbaníhà_àkọsílẹ̀_ìṣe
                assert not afará_iye.àṣìṣe, afará_iye.àṣìṣe
                í_meèlì(b'poweroff\n')
                assert Ìlànà_iye.wait(timeout=15) == 0
                ìjábọ̀_iye['passed'] = True
            yan_wúnrẹ̀n.close()
    except Exception as àṣìṣe:
        ìjábọ̀_iye['error'] = str(àṣìṣe)
        raise
    finally:
        if Ìlànà_iye is not None and Ìlànà_iye.poll() is None:
            Ìlànà_iye.terminate()
            try:
                Ìlànà_iye.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Ìlànà_iye.kill()
                Ìlànà_iye.wait()
        (출력 / 'serial.log').write_bytes(àkọsílẹ̀_ìṣe_ìlà_ìbú)
        (출력 / 'report.json').write_text(json.dumps(ìjábọ̀_iye, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({bọ́tìnnì_iye: ìjábọ̀_iye[bọ́tìnnì_iye] for bọ́tìnnì_iye in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Rọ́ọ̀nù()
