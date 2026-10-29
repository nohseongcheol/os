#!/usr/bin/env python3
"""QEMU의 ትኽክለኛ_ሓበሬታ CPU ፍቓድ_ዋጋ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ተግብር_ትእዛዝ import 기준, ትእዛዝ
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def ኣኺድ():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ጸብጻብ_ዋጋ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ምንጪ_ፋይላት = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ማሕበራዊ_ኔትወርክ_ፈትሽ': '''import java.net.*;
public class ማሕበራዊ_ኔትወርክ_ፈትሽ {
 public static void main(String[] 인수) throws Exception {
  Socket ኣላግብ = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ኣላግብ.setSoTimeout(3000);
  byte[] ጽሑፍ = "TCP 한글\\n".getBytes("UTF-8");
  ኣላግብ.getOutputStream().write(ጽሑፍ);
  for (int 자리 = 0; 자리 < ጽሑፍ.length; 자리++)
   if (ኣላግብ.getInputStream().read() != (ጽሑፍ[자리] & 255)) throw new RuntimeException("TCP mismatch");
  ኣላግብ.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ጽሑፍ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ጽሑፍ, ጽሑፍ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] መልስ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(መልስ, መልስ.length);
  종단.receive(전문);
  if (전문.getLength() != ጽሑፍ.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < ጽሑፍ.length; 자리++)
   if (መልስ[자리] != ጽሑፍ[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket ኣገልጋሊ_ዋጋ = new ServerSocket(9300); ኣገልጋሊ_ዋጋ.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ኣላግብ = ኣገልጋሊ_ዋጋ.accept(); ኣላግብ.setSoTimeout(5000);
  ኣላግብ.getOutputStream().write(ኣላግብ.getInputStream().read() + 1);
  ኣላግብ.close(); ኣገልጋሊ_ዋጋ.close();
  byte[] ሓበሬታ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ሓበሬታ, ሓበሬታ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ሽም, ምንጪ in ምንጪ_ፋይላት.items():
        (출력 / (ሽም + '.java')).write_text(ምንጪ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (ሽም + '.java')) for ሽም in ምንጪ_ፋይላት])
    ምዝጉብ_ሪጋ = bytearray()
    def 빈접속번호(ዓይነት_መደብ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ዓይነት_መደብ) as አለሻ_ዋጋ:
            አለሻ_ዋጋ.bind(('127.0.0.4', 0))
            return አለሻ_ዋጋ.getsockname()[1]
    파일접속번호, ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    መስርሕ_ዋጋ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ), 'udp:{}:9301'.format(전문접속번호)],
                ቕረጽ=True, አዐንግድ_ኣድራሻ='127.0.0.4') as 다리:
            ቁጽጽር_መገዲ = Path(임시) / 'qmp.sock'
            መስርሕ_ዋጋ = subprocess.Popen(ትእዛዝ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ቁጽጽር_መገዲ)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ምረጽ_ውልቀ_ነገር = selectors.DefaultSelector()
            ምረጽ_ውልቀ_ነገር.register(መስርሕ_ዋጋ.stdout, selectors.EVENT_READ)
            def 받기(ኣርእይ_ዋጋ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ኣርእይ_ዋጋ not in ምዝጉብ_ሪጋ[처음:]:
                    if time.monotonic() > 끝 or መስርሕ_ዋጋ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ኣርእይ_ዋጋ) + '\n' + ምዝጉብ_ሪጋ[처음:].decode('utf-8', 'replace'))
                    for መፍትሕ_ዋጋ, _ in ምረጽ_ውልቀ_ነገር.select(.05):
                        조각 = መፍትሕ_ዋጋ.fileobj.read(65536)
                        if 조각:
                            ምዝጉብ_ሪጋ.extend(조각)
                return ምዝጉብ_ሪጋ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ለኣኽ(ሓበሬታ):
                መስርሕ_ዋጋ.stdin.write(ሓበሬታ)
                መስርሕ_ዋጋ.stdin.flush()
            def ሽፋን(ጽሑፍ):
                print(ጽሑፍ, flush=True)
                처음 = len(ምዝጉብ_ሪጋ)
                ለኣኽ((ጽሑፍ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ቁጽጽር_ዋጋ:
                ቁጽጽር_ዋጋ.settimeout(10)
                ቁጽጽር_ዋጋ.connect(str(ቁጽጽር_መገዲ))
                ወሓዚ_ዋጋ = ቁጽጽር_ዋጋ.makefile('rwb')
                json.loads(ወሓዚ_ዋጋ.readline())
                def 요청(መምርሒ_ዋጋ, 인수=None):
                    ሓበሬታ = {'execute': መምርሒ_ዋጋ}
                    if 인수 is not None:
                        ሓበሬታ['arguments'] = 인수
                    ወሓዚ_ዋጋ.write((json.dumps(ሓበሬታ) + '\n').encode())
                    ወሓዚ_ዋጋ.flush()
                    while True:
                        መልስ = json.loads(ወሓዚ_ዋጋ.readline())
                        if 'error' in መልስ:
                            raise AssertionError(መልስ)
                        if 'return' in መልስ:
                            return መልስ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ጸብጻብ_ዋጋ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ጸብጻብ_ዋጋ['shell_cpu'], ጸብጻብ_ዋጋ['shell_cpu']
                ጸብጻብ_ዋጋ['initial_ps'] = ሽፋን('ps')
                assert 'kernel/shell' in ጸብጻብ_ዋጋ['initial_ps']
                ጸብጻብ_ዋጋ['ipconfig'] = ሽፋን('ipconfig')
                assert 'inet 10.0.2.15' in ጸብጻብ_ዋጋ['ipconfig']
                ጸብጻብ_ዋጋ['gateway_ping'] = ሽፋን('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ጸብጻብ_ዋጋ['gateway_ping']
                assert 'FTP listening' in ሽፋን('ftpd start')
                with ftplib.FTP() as ምስጋር_ዋጋ:
                    ምስጋር_ዋጋ.encoding = 'utf-8'
                    ምስጋር_ዋጋ.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ምስጋር_ዋጋ.login()
                    for ሽም in ምንጪ_ፋይላት:
                        ምስጋር_ዋጋ.storbinary('STOR ' + ሽም + '.class', io.BytesIO((출력 / (ሽም + '.class')).read_bytes()))
                처음 = len(ምዝጉብ_ሪጋ)
                ለኣኽ('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ጸብጻብ_ዋጋ['java_cpu'] = 권한읽기()
                    if 'EL0t' in ጸብጻብ_ዋጋ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ጸብጻብ_ዋጋ['java_cpu'], ጸብጻብ_ዋጋ['java_cpu']
                받기(처음=처음)
                ጸብጻብ_ዋጋ['after_exit_ps'] = ሽፋን('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ጸብጻብ_ዋጋ['after_exit_ps'])
                ጸብጻብ_ዋጋ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as መዘና_ዋጋ:
                    ጽሑፍ = ሽፋን('java ማሕበራዊ_ኔትወርክ_ፈትሽ {} {}'.format(መዘና_ዋጋ.ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ, መዘና_ዋጋ.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
                    assert መዘና_ዋጋ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, መዘና_ዋጋ.수신됨
                    assert not መዘና_ዋጋ.오류들, መዘና_ዋጋ.오류들
                    ጸብጻብ_ዋጋ['outbound_peers'] = {종류: ሓበሬታ.decode() for 종류, ሓበሬታ in መዘና_ዋጋ.수신됨.items()}
                처음 = len(ምዝጉብ_ሪጋ)
                ለኣኽ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ናይ_መተሓላላፊ_ተቖጻጻሪ_ፕሮቶኮል_ወደብ), timeout=5) as መዘና_ዋጋ:
                    መዘና_ዋጋ.sendall(b'A')
                    assert መዘና_ዋጋ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as መዘና_ዋጋ:
                    መዘና_ዋጋ.settimeout(5)
                    መዘና_ዋጋ.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert መዘና_ዋጋ.recvfrom(64)[0] == b'UDP-IN'
                ጽሑፍ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ጽሑፍ and 'exit 0' in ጽሑፍ, ጽሑፍ
                ጸብጻብ_ዋጋ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ሽፋን('terminal')
                ሽፋን('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ምዝጉብ_ሪጋ)
                ለኣኽ('java 창예제\n'.encode())
                받기('GUI 예제 ኣዳልው: 창예제\r\n'.encode(), 처음)
                처음 = len(ምዝጉብ_ሪጋ)
                ለኣኽ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ጸብጻብ_ዋጋ['suspended_java_ps'] = ሽፋን('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ጸብጻብ_ዋጋ['suspended_java_ps']), ጸብጻብ_ዋጋ['suspended_java_ps']
                ጸብጻብ_ዋጋ['top'] = ሽፋን('top -n 1')
                assert 'java 창예제' in ጸብጻብ_ዋጋ['top'] and 'kernel/shell' in ጸብጻብ_ዋጋ['top']
                ጸብጻብ_ዋጋ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ጸብጻብ_ዋጋ['network_trace'] = 다리.추적기록
                assert not 다리.ጌጋ, 다리.ጌጋ
                ለኣኽ(b'poweroff\n')
                assert መስርሕ_ዋጋ.wait(timeout=15) == 0
                ጸብጻብ_ዋጋ['passed'] = True
            ምረጽ_ውልቀ_ነገር.close()
    except Exception as ጌጋ:
        ጸብጻብ_ዋጋ['error'] = str(ጌጋ)
        raise
    finally:
        if መስርሕ_ዋጋ is not None and መስርሕ_ዋጋ.poll() is None:
            መስርሕ_ዋጋ.terminate()
            try:
                መስርሕ_ዋጋ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                መስርሕ_ዋጋ.kill()
                መስርሕ_ዋጋ.wait()
        (출력 / 'serial.log').write_bytes(ምዝጉብ_ሪጋ)
        (출력 / 'report.json').write_text(json.dumps(ጸብጻብ_ዋጋ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({መፍትሕ_ዋጋ: ጸብጻብ_ዋጋ[መፍትሕ_ዋጋ] for መፍትሕ_ዋጋ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ኣኺድ()
