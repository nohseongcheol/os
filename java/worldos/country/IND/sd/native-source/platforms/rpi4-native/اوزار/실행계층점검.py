#!/usr/bin/env python3
"""QEMU의 اصلي_ڪوائف CPU اجازت_قدر, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from تعميل_ڪرڻ_حڪم import 기준, حڪم
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def هلائڻ():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    رپورٽ_قدر = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ماخذ_فائلون = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'نيٽ_ورڪ_پڙتال_ڪريو': '''import java.net.*;
public class نيٽ_ورڪ_پڙتال_ڪريو {
 public static void main(String[] 인수) throws Exception {
  Socket ڪنيڪٽ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ڪنيڪٽ.setSoTimeout(3000);
  byte[] متن = "TCP 한글\\n".getBytes("UTF-8");
  ڪنيڪٽ.getOutputStream().write(متن);
  for (int 자리 = 0; 자리 < متن.length; 자리++)
   if (ڪنيڪٽ.getInputStream().read() != (متن[자리] & 255)) throw new RuntimeException("TCP mismatch");
  ڪنيڪٽ.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  متن = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(متن, متن.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] جواب_ڏيو = new byte[64]; DatagramPacket 전문 = new DatagramPacket(جواب_ڏيو, جواب_ڏيو.length);
  종단.receive(전문);
  if (전문.getLength() != متن.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < متن.length; 자리++)
   if (جواب_ڏيو[자리] != متن[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket سرور_قدر = new ServerSocket(9300); سرور_قدر.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ڪنيڪٽ = سرور_قدر.accept(); ڪنيڪٽ.setSoTimeout(5000);
  ڪنيڪٽ.getOutputStream().write(ڪنيڪٽ.getInputStream().read() + 1);
  ڪنيڪٽ.close(); سرور_قدر.close();
  byte[] ڪوائف = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ڪوائف, ڪوائف.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for نالو, ماخذ in ماخذ_فائلون.items():
        (출력 / (نالو + '.java')).write_text(ماخذ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (نالو + '.java')) for نالو in ماخذ_فائلون])
    لاگ_صف = bytearray()
    def 빈접속번호(قسم_قسم=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, قسم_قسم) as ڳولا_قدر:
            ڳولا_قدر.bind(('127.0.0.4', 0))
            return ڳولا_قدر.getsockname()[1]
    파일접속번호, ٽرانسمشن_ڪنٽرول_پروٽوڪول_پورٽ, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    عمل_قدر = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(ٽرانسمشن_ڪنٽرول_پروٽوڪول_پورٽ), 'udp:{}:9301'.format(전문접속번호)],
                ڪيپچر=True, مهمان_پتو='127.0.0.4') as 다리:
            ڪنٽرول_راههه = Path(임시) / 'qmp.sock'
            عمل_قدر = subprocess.Popen(حڪم() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ڪنٽرول_راههه)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            چونڊ_ڪريو_شي = selectors.DefaultSelector()
            چونڊ_ڪريو_شي.register(عمل_قدر.stdout, selectors.EVENT_READ)
            def 받기(نمائش_ڪريو_قدر=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while نمائش_ڪريو_قدر not in لاگ_صف[처음:]:
                    if time.monotonic() > 끝 or عمل_قدر.poll() is not None:
                        raise AssertionError('Missing ' + repr(نمائش_ڪريو_قدر) + '\n' + لاگ_صف[처음:].decode('utf-8', 'replace'))
                    for ڪليد_قدر, _ in چونڊ_ڪريو_شي.select(.05):
                        조각 = ڪليد_قدر.fileobj.read(65536)
                        if 조각:
                            لاگ_صف.extend(조각)
                return لاگ_صف[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def اي_ميل(ڪوائف):
                عمل_قدر.stdin.write(ڪوائف)
                عمل_قدر.stdin.flush()
            def شيل(متن):
                print(متن, flush=True)
                처음 = len(لاگ_صف)
                اي_ميل((متن + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ڪنٽرول_قدر:
                ڪنٽرول_قدر.settimeout(10)
                ڪنٽرول_قدر.connect(str(ڪنٽرول_راههه))
                اسٽريم_قدر = ڪنٽرول_قدر.makefile('rwb')
                json.loads(اسٽريم_قدر.readline())
                def 요청(هدايت_قدر, 인수=None):
                    ڪوائف = {'execute': هدايت_قدر}
                    if 인수 is not None:
                        ڪوائف['arguments'] = 인수
                    اسٽريم_قدر.write((json.dumps(ڪوائف) + '\n').encode())
                    اسٽريم_قدر.flush()
                    while True:
                        جواب_ڏيو = json.loads(اسٽريم_قدر.readline())
                        if 'error' in جواب_ڏيو:
                            raise AssertionError(جواب_ڏيو)
                        if 'return' in جواب_ڏيو:
                            return جواب_ڏيو['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                رپورٽ_قدر['shell_cpu'] = 권한읽기()
                assert 'EL1h' in رپورٽ_قدر['shell_cpu'], رپورٽ_قدر['shell_cpu']
                رپورٽ_قدر['initial_ps'] = شيل('ps')
                assert 'kernel/shell' in رپورٽ_قدر['initial_ps']
                رپورٽ_قدر['ipconfig'] = شيل('ipconfig')
                assert 'inet 10.0.2.15' in رپورٽ_قدر['ipconfig']
                رپورٽ_قدر['gateway_ping'] = شيل('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in رپورٽ_قدر['gateway_ping']
                assert 'FTP listening' in شيل('ftpd start')
                with ftplib.FTP() as منتقلي_قدر:
                    منتقلي_قدر.encoding = 'utf-8'
                    منتقلي_قدر.connect('127.0.0.4', 파일접속번호, timeout=20)
                    منتقلي_قدر.login()
                    for نالو in ماخذ_فائلون:
                        منتقلي_قدر.storbinary('STOR ' + نالو + '.class', io.BytesIO((출력 / (نالو + '.class')).read_bytes()))
                처음 = len(لاگ_صف)
                اي_ميل('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    رپورٽ_قدر['java_cpu'] = 권한읽기()
                    if 'EL0t' in رپورٽ_قدر['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in رپورٽ_قدر['java_cpu'], رپورٽ_قدر['java_cpu']
                받기(처음=처음)
                رپورٽ_قدر['after_exit_ps'] = شيل('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', رپورٽ_قدر['after_exit_ps'])
                رپورٽ_قدر['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as همعصر_قدر:
                    متن = شيل('java نيٽ_ورڪ_پڙتال_ڪريو {} {}'.format(همعصر_قدر.ٽرانسمشن_ڪنٽرول_پروٽوڪول_پورٽ, همعصر_قدر.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                    assert همعصر_قدر.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, همعصر_قدر.수신됨
                    assert not همعصر_قدر.오류들, همعصر_قدر.오류들
                    رپورٽ_قدر['outbound_peers'] = {종류: ڪوائف.decode() for 종류, ڪوائف in همعصر_قدر.수신됨.items()}
                처음 = len(لاگ_صف)
                اي_ميل('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ٽرانسمشن_ڪنٽرول_پروٽوڪول_پورٽ), timeout=5) as همعصر_قدر:
                    همعصر_قدر.sendall(b'A')
                    assert همعصر_قدر.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as همعصر_قدر:
                    همعصر_قدر.settimeout(5)
                    همعصر_قدر.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert همعصر_قدر.recvfrom(64)[0] == b'UDP-IN'
                متن = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                رپورٽ_قدر['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in شيل('terminal')
                شيل('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(لاگ_صف)
                اي_ميل('java 창예제\n'.encode())
                받기('GUI 예제 تياري_ڪريو: 창예제\r\n'.encode(), 처음)
                처음 = len(لاگ_صف)
                اي_ميل(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                رپورٽ_قدر['suspended_java_ps'] = شيل('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', رپورٽ_قدر['suspended_java_ps']), رپورٽ_قدر['suspended_java_ps']
                رپورٽ_قدر['top'] = شيل('top -n 1')
                assert 'java 창예제' in رپورٽ_قدر['top'] and 'kernel/shell' in رپورٽ_قدر['top']
                رپورٽ_قدر['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                رپورٽ_قدر['network_trace'] = 다리.추적기록
                assert not 다리.نقص, 다리.نقص
                اي_ميل(b'poweroff\n')
                assert عمل_قدر.wait(timeout=15) == 0
                رپورٽ_قدر['passed'] = True
            چونڊ_ڪريو_شي.close()
    except Exception as نقص:
        رپورٽ_قدر['error'] = str(نقص)
        raise
    finally:
        if عمل_قدر is not None and عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try:
                عمل_قدر.wait(timeout=10)
            except subprocess.TimeoutExpired:
                عمل_قدر.kill()
                عمل_قدر.wait()
        (출력 / 'serial.log').write_bytes(لاگ_صف)
        (출력 / 'report.json').write_text(json.dumps(رپورٽ_قدر, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ڪليد_قدر: رپورٽ_قدر[ڪليد_قدر] for ڪليد_قدر in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    هلائڻ()
