#!/usr/bin/env python3
"""QEMU의 ପ୍ରକୃତ_ଡାଟା CPU ଅନୁମତି_ମୂଲ୍ୟ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, ନିର୍ଦ୍ଦେଶ
from ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍ import ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍
from 되돌림시험서버 import 되돌림시험서버


def ଚଳାନ୍ତୁ():
    ନିର୍ଗମ = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification/execution-network-review'
    ନିର୍ଗମ.mkdir(parents=True, exist_ok=True)
    ରିପୋର୍ଟ_ମୂଲ୍ୟ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ଉତ୍ସ_ଫାଇଲ୍_ଗୁଡିକ = {
        'ଅନୁମତି_ପରୀକ୍ଷିତ': '''public class ଅନୁମତି_ପରୀକ୍ଷିତ {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ନେଟ୍_ୱାର୍କ୍_ପରୀକ୍ଷିତ': '''import java.net.*;
public class ନେଟ୍_ୱାର୍କ୍_ପରୀକ୍ଷିତ {
 public static void main(String[] 인수) throws Exception {
  Socket ସଂଯୋଗ_କରନ୍ତୁ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ସଂଯୋଗ_କରନ୍ତୁ.setSoTimeout(3000);
  byte[] ପାଠ୍ଯ = "TCP 한글\\n".getBytes("UTF-8");
  ସଂଯୋଗ_କରନ୍ତୁ.getOutputStream().write(ପାଠ୍ଯ);
  for (int ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା = 0; ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା < ପାଠ୍ଯ.length; ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା++)
   if (ସଂଯୋଗ_କରନ୍ତୁ.getInputStream().read() != (ପାଠ୍ଯ[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା] & 255)) throw new RuntimeException("TCP mismatch");
  ସଂଯୋଗ_କରନ୍ତୁ.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ପାଠ୍ଯ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ପାଠ୍ଯ, ପାଠ୍ଯ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ, ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ.length);
  종단.receive(전문);
  if (전문.getLength() != ପାଠ୍ଯ.length) throw new RuntimeException("UDP length");
  for (int ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା = 0; ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା < ପାଠ୍ଯ.length; ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା++)
   if (ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା] != ପାଠ୍ଯ[ସ୍ଥିତି_ଅନୁକ୍ରମଣିକା]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket ସର୍ଭର୍_ମୂଲ୍ୟ = new ServerSocket(9300); ସର୍ଭର୍_ମୂଲ୍ୟ.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ସଂଯୋଗ_କରନ୍ତୁ = ସର୍ଭର୍_ମୂଲ୍ୟ.accept(); ସଂଯୋଗ_କରନ୍ତୁ.setSoTimeout(5000);
  ସଂଯୋଗ_କରନ୍ତୁ.getOutputStream().write(ସଂଯୋଗ_କରନ୍ତୁ.getInputStream().read() + 1);
  ସଂଯୋଗ_କରନ୍ତୁ.close(); ସର୍ଭର୍_ମୂଲ୍ୟ.close();
  byte[] ଡାଟା = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ଡାଟା, ଡାଟା.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ନାମ, ଉତ୍ସ in ଉତ୍ସ_ଫାଇଲ୍_ଗୁଡିକ.items():
        (ନିର୍ଗମ / (ନାମ + '.java')).write_text(ଉତ୍ସ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ନିର୍ଗମ)] +
                          [str(ନିର୍ଗମ / (ନାମ + '.java')) for ନାମ in ଉତ୍ସ_ଫାଇଲ୍_ଗୁଡିକ])
    ଲଗ୍_ଧାଡ଼ି = bytearray()
    def ଖାଲି_ପୋର୍ଟ୍_ନମ୍ଵର୍(ଟାଇପ୍_କରିବା_ବର୍ଗ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ଟାଇପ୍_କରିବା_ବର୍ଗ) as ସନ୍ଧାନ_ମୂଲ୍ୟ:
            ସନ୍ଧାନ_ମୂଲ୍ୟ.bind(('127.0.0.4', 0))
            return ସନ୍ଧାନ_ମୂଲ୍ୟ.getsockname()[1]
    ଫାଇଲ୍_ପୋର୍ଟ୍_ନମ୍ଵର୍, ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ, 전문접속번호 = ଖାଲି_ପୋର୍ଟ୍_ନମ୍ଵର୍(), ଖାଲି_ପୋର୍ଟ୍_ନମ୍ଵର୍(), ଖାଲି_ପୋର୍ଟ୍_ନମ୍ଵର୍(socket.SOCK_DGRAM)
    ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍(
                ଫାଇଲ୍_ପୋର୍ଟ୍_ନମ୍ଵର୍, ['tcp:{}:9300'.format(ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ), 'udp:{}:9301'.format(전문접속번호)],
                କ୍ୟାପଚର୍_କରିବା=True, ଆୟୋଜକ_ଠିକଣା='127.0.0.4') as ବ୍ରିଜ୍_ମୂଲ୍ୟ:
            ନିୟନ୍ତ୍ରଣ_ପଥ = Path(임시) / 'qmp.sock'
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ = subprocess.Popen(ନିର୍ଦ୍ଦେଶ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ନିୟନ୍ତ୍ରଣ_ପଥ)] + ବ୍ରିଜ୍_ମୂଲ୍ୟ.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ମନୋନୟନ_ଆଇଟମ୍ = selectors.DefaultSelector()
            ମନୋନୟନ_ଆଇଟମ୍.register(ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdout, selectors.EVENT_READ)
            def 받기(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ not in ଲଗ୍_ଧାଡ଼ି[처음:]:
                    if time.monotonic() > 끝 or ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ପ୍ରଦର୍ଶନ_କରିବା_ମୂଲ୍ୟ) + '\n' + ଲଗ୍_ଧାଡ଼ି[처음:].decode('utf-8', 'replace'))
                    for କୀ_ମୂଲ୍ୟ, _ in ମନୋନୟନ_ଆଇଟମ୍.select(.05):
                        조각 = କୀ_ମୂଲ୍ୟ.fileobj.read(65536)
                        if 조각:
                            ଲଗ୍_ଧାଡ଼ି.extend(조각)
                return ଲଗ୍_ଧାଡ଼ି[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ପଠାନ୍ତୁ(ଡାଟା):
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.write(ଡାଟା)
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.stdin.flush()
            def ଖୋଳ(ପାଠ୍ଯ):
                print(ପାଠ୍ଯ, flush=True)
                처음 = len(ଲଗ୍_ଧାଡ଼ି)
                ପଠାନ୍ତୁ((ପାଠ୍ଯ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ:
                ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ.settimeout(10)
                ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ.connect(str(ନିୟନ୍ତ୍ରଣ_ପଥ))
                ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ = ନିୟନ୍ତ୍ରଣ_ମୂଲ୍ୟ.makefile('rwb')
                json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline())
                def 요청(ପରାମର୍ଶ_ମୂଲ୍ୟ, 인수=None):
                    ଡାଟା = {'execute': ପରାମର୍ଶ_ମୂଲ୍ୟ}
                    if 인수 is not None:
                        ଡାଟା['arguments'] = 인수
                    ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.write((json.dumps(ଡାଟା) + '\n').encode())
                    ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.flush()
                    while True:
                        ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ = json.loads(ଷ୍ଟ୍ରିମ୍_ମୂଲ୍ୟ.readline())
                        if 'error' in ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ:
                            raise AssertionError(ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ)
                        if 'return' in ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ:
                            return ପ୍ରତ୍ୟୁତ୍ତର_କରନ୍ତୁ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['shell_cpu'], ରିପୋର୍ଟ_ମୂଲ୍ୟ['shell_cpu']
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['initial_ps'] = ଖୋଳ('ps')
                assert 'kernel/shell' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['initial_ps']
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['ipconfig'] = ଖୋଳ('ipconfig')
                assert 'inet 10.0.2.15' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['ipconfig']
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['gateway_ping'] = ଖୋଳ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['gateway_ping']
                assert 'FTP listening' in ଖୋଳ('ftpd start')
                with ftplib.FTP() as ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ:
                    ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.encoding = 'utf-8'
                    ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.connect('127.0.0.4', ଫାଇଲ୍_ପୋର୍ଟ୍_ନମ୍ଵର୍, timeout=20)
                    ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.login()
                    for ନାମ in ଉତ୍ସ_ଫାଇଲ୍_ଗୁଡିକ:
                        ସ୍ଥାନାନ୍ତର_ମୂଲ୍ୟ.storbinary('STOR ' + ନାମ + '.class', io.BytesIO((ନିର୍ଗମ / (ନାମ + '.class')).read_bytes()))
                처음 = len(ଲଗ୍_ଧାଡ଼ି)
                ପଠାନ୍ତୁ('java ଅନୁମତି_ପରୀକ୍ଷିତ\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ରିପୋର୍ଟ_ମୂଲ୍ୟ['java_cpu'] = 권한읽기()
                    if 'EL0t' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['java_cpu'], ରିପୋର୍ଟ_ମୂଲ୍ୟ['java_cpu']
                받기(처음=처음)
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['after_exit_ps'] = ଖୋଳ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ରିପୋର୍ଟ_ମୂଲ୍ୟ['after_exit_ps'])
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ସମକକ୍ଷ_ମୂଲ୍ୟ:
                    ପାଠ୍ଯ = ଖୋଳ('java ନେଟ୍_ୱାର୍କ୍_ପରୀକ୍ଷିତ {} {}'.format(ସମକକ୍ଷ_ମୂଲ୍ୟ.ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ, ସମକକ୍ଷ_ମୂଲ୍ୟ.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
                    assert ସମକକ୍ଷ_ମୂଲ୍ୟ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ସମକକ୍ଷ_ମୂଲ୍ୟ.수신됨
                    assert not ସମକକ୍ଷ_ମୂଲ୍ୟ.오류들, ସମକକ୍ଷ_ମୂଲ୍ୟ.오류들
                    ରିପୋର୍ଟ_ମୂଲ୍ୟ['outbound_peers'] = {종류: ଡାଟା.decode() for 종류, ଡାଟା in ସମକକ୍ଷ_ମୂଲ୍ୟ.수신됨.items()}
                처음 = len(ଲଗ୍_ଧାଡ଼ି)
                ପଠାନ୍ତୁ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ), timeout=5) as ସମକକ୍ଷ_ମୂଲ୍ୟ:
                    ସମକକ୍ଷ_ମୂଲ୍ୟ.sendall(b'A')
                    assert ସମକକ୍ଷ_ମୂଲ୍ୟ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ସମକକ୍ଷ_ମୂଲ୍ୟ:
                    ସମକକ୍ଷ_ମୂଲ୍ୟ.settimeout(5)
                    ସମକକ୍ଷ_ମୂଲ୍ୟ.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ସମକକ୍ଷ_ମୂଲ୍ୟ.recvfrom(64)[0] == b'UDP-IN'
                ପାଠ୍ଯ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ଖୋଳ('terminal')
                ଖୋଳ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ଲଗ୍_ଧାଡ଼ି)
                ପଠାନ୍ତୁ('java 창예제\n'.encode())
                받기('GUI 예제 ପ୍ରସ୍ତୁତ: 창예제\r\n'.encode(), 처음)
                처음 = len(ଲଗ୍_ଧାଡ଼ି)
                ପଠାନ୍ତୁ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['suspended_java_ps'] = ଖୋଳ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ରିପୋର୍ଟ_ମୂଲ୍ୟ['suspended_java_ps']), ରିପୋର୍ଟ_ମୂଲ୍ୟ['suspended_java_ps']
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['top'] = ଖୋଳ('top -n 1')
                assert 'java 창예제' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['top'] and 'kernel/shell' in ରିପୋର୍ଟ_ମୂଲ୍ୟ['top']
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['network_trace'] = ବ୍ରିଜ୍_ମୂଲ୍ୟ.ଚିହ୍ନଟ_ଲଗ୍
                assert not ବ୍ରିଜ୍_ମୂଲ୍ୟ.ତ୍ରୁଟି, ବ୍ରିଜ୍_ମୂଲ୍ୟ.ତ୍ରୁଟି
                ପଠାନ୍ତୁ(b'poweroff\n')
                assert ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=15) == 0
                ରିପୋର୍ଟ_ମୂଲ୍ୟ['passed'] = True
            ମନୋନୟନ_ଆଇଟମ୍.close()
    except Exception as ତ୍ରୁଟି:
        ରିପୋର୍ଟ_ମୂଲ୍ୟ['error'] = str(ତ୍ରୁଟି)
        raise
    finally:
        if ପ୍ରୋସେସ୍_ମୂଲ୍ୟ is not None and ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.poll() is None:
            ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.terminate()
            try:
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.kill()
                ପ୍ରୋସେସ୍_ମୂଲ୍ୟ.wait()
        (ନିର୍ଗମ / 'serial.log').write_bytes(ଲଗ୍_ଧାଡ଼ି)
        (ନିର୍ଗମ / 'report.json').write_text(json.dumps(ରିପୋର୍ଟ_ମୂଲ୍ୟ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({କୀ_ମୂଲ୍ୟ: ରିପୋର୍ଟ_ମୂଲ୍ୟ[କୀ_ମୂଲ୍ୟ] for କୀ_ମୂଲ୍ୟ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ଚଳାନ୍ତୁ()
