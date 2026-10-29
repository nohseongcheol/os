#!/usr/bin/env python3
"""QEMU의 ڕاستەکی_دەیتا CPU ڕێپێدان_نرخ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from جێبەجێکردن_فەرمان import 기준, فەرمان
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def ڕادان():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ڕاپۆرت_نرخ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ژێدەر_فایله_کان = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'تۆڕ_پشکنین': '''import java.net.*;
public class تۆڕ_پشکنین {
 public static void main(String[] 인수) throws Exception {
  Socket لكاندن = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  لكاندن.setSoTimeout(3000);
  byte[] دەق = "TCP 한글\\n".getBytes("UTF-8");
  لكاندن.getOutputStream().write(دەق);
  for (int 자리 = 0; 자리 < دەق.length; 자리++)
   if (لكاندن.getInputStream().read() != (دەق[자리] & 255)) throw new RuntimeException("TCP mismatch");
  لكاندن.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  دەق = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(دەق, دەق.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] وەڵامدانەوه = new byte[64]; DatagramPacket 전문 = new DatagramPacket(وەڵامدانەوه, وەڵامدانەوه.length);
  종단.receive(전문);
  if (전문.getLength() != دەق.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < دەق.length; 자리++)
   if (وەڵامدانەوه[자리] != دەق[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket ڕاژەکار_نرخ = new ServerSocket(9300); ڕاژەکار_نرخ.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket لكاندن = ڕاژەکار_نرخ.accept(); لكاندن.setSoTimeout(5000);
  لكاندن.getOutputStream().write(لكاندن.getInputStream().read() + 1);
  لكاندن.close(); ڕاژەکار_نرخ.close();
  byte[] دەیتا = new byte[64]; DatagramPacket 전문 = new DatagramPacket(دەیتا, دەیتا.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ناو, ژێدەر in ژێدەر_فایله_کان.items():
        (출력 / (ناو + '.java')).write_text(ژێدەر, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (ناو + '.java')) for ناو in ژێدەر_فایله_کان])
    تۆمار_ڕزن = bytearray()
    def 빈접속번호(چاپکردن_پۆل=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, چاپکردن_پۆل) as گەڕان_نرخ:
            گەڕان_نرخ.bind(('127.0.0.4', 0))
            return گەڕان_نرخ.getsockname()[1]
    파일접속번호, TCP_دەرگا, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    پرۆسە_نرخ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_دەرگا), 'udp:{}:9301'.format(전문접속번호)],
                تۆمارکردن=True, جێدەر_ناونیشان='127.0.0.4') as 다리:
            کۆنترۆڵ_گوزەر = Path(임시) / 'qmp.sock'
            پرۆسە_نرخ = subprocess.Popen(فەرمان() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(کۆنترۆڵ_گوزەر)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            هەڵبژاردن_ئایتم = selectors.DefaultSelector()
            هەڵبژاردن_ئایتم.register(پرۆسە_نرخ.stdout, selectors.EVENT_READ)
            def 받기(نیشاندان_نرخ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while نیشاندان_نرخ not in تۆمار_ڕزن[처음:]:
                    if time.monotonic() > 끝 or پرۆسە_نرخ.poll() is not None:
                        raise AssertionError('Missing ' + repr(نیشاندان_نرخ) + '\n' + تۆمار_ڕزن[처음:].decode('utf-8', 'replace'))
                    for کلیل_نرخ, _ in هەڵبژاردن_ئایتم.select(.05):
                        조각 = کلیل_نرخ.fileobj.read(65536)
                        if 조각:
                            تۆمار_ڕزن.extend(조각)
                return تۆمار_ڕزن[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ناردن(دەیتا):
                پرۆسە_نرخ.stdin.write(دەیتا)
                پرۆسە_نرخ.stdin.flush()
            def توێکڵ(دەق):
                print(دەق, flush=True)
                처음 = len(تۆمار_ڕزن)
                ناردن((دەق + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as کۆنترۆڵ_نرخ:
                کۆنترۆڵ_نرخ.settimeout(10)
                کۆنترۆڵ_نرخ.connect(str(کۆنترۆڵ_گوزەر))
                Stream_نرخ = کۆنترۆڵ_نرخ.makefile('rwb')
                json.loads(Stream_نرخ.readline())
                def 요청(ڕێنمایی_نرخ, 인수=None):
                    دەیتا = {'execute': ڕێنمایی_نرخ}
                    if 인수 is not None:
                        دەیتا['arguments'] = 인수
                    Stream_نرخ.write((json.dumps(دەیتا) + '\n').encode())
                    Stream_نرخ.flush()
                    while True:
                        وەڵامدانەوه = json.loads(Stream_نرخ.readline())
                        if 'error' in وەڵامدانەوه:
                            raise AssertionError(وەڵامدانەوه)
                        if 'return' in وەڵامدانەوه:
                            return وەڵامدانەوه['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ڕاپۆرت_نرخ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ڕاپۆرت_نرخ['shell_cpu'], ڕاپۆرت_نرخ['shell_cpu']
                ڕاپۆرت_نرخ['initial_ps'] = توێکڵ('ps')
                assert 'kernel/shell' in ڕاپۆرت_نرخ['initial_ps']
                ڕاپۆرت_نرخ['ipconfig'] = توێکڵ('ipconfig')
                assert 'inet 10.0.2.15' in ڕاپۆرت_نرخ['ipconfig']
                ڕاپۆرت_نرخ['gateway_ping'] = توێکڵ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ڕاپۆرت_نرخ['gateway_ping']
                assert 'FTP listening' in توێکڵ('ftpd start')
                with ftplib.FTP() as گواستنەوە_نرخ_630ba093:
                    گواستنەوە_نرخ_630ba093.encoding = 'utf-8'
                    گواستنەوە_نرخ_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    گواستنەوە_نرخ_630ba093.login()
                    for ناو in ژێدەر_فایله_کان:
                        گواستنەوە_نرخ_630ba093.storbinary('STOR ' + ناو + '.class', io.BytesIO((출력 / (ناو + '.class')).read_bytes()))
                처음 = len(تۆمار_ڕزن)
                ناردن('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ڕاپۆرت_نرخ['java_cpu'] = 권한읽기()
                    if 'EL0t' in ڕاپۆرت_نرخ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ڕاپۆرت_نرخ['java_cpu'], ڕاپۆرت_نرخ['java_cpu']
                받기(처음=처음)
                ڕاپۆرت_نرخ['after_exit_ps'] = توێکڵ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ڕاپۆرت_نرخ['after_exit_ps'])
                ڕاپۆرت_نرخ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as هاوتا_نرخ:
                    دەق = توێکڵ('java تۆڕ_پشکنین {} {}'.format(هاوتا_نرخ.TCP_دەرگا, هاوتا_نرخ.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in دەق and 'exit 0' in دەق, دەق
                    assert هاوتا_نرخ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, هاوتا_نرخ.수신됨
                    assert not هاوتا_نرخ.오류들, هاوتا_نرخ.오류들
                    ڕاپۆرت_نرخ['outbound_peers'] = {종류: دەیتا.decode() for 종류, دەیتا in هاوتا_نرخ.수신됨.items()}
                처음 = len(تۆمار_ڕزن)
                ناردن('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_دەرگا), timeout=5) as هاوتا_نرخ:
                    هاوتا_نرخ.sendall(b'A')
                    assert هاوتا_نرخ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as هاوتا_نرخ:
                    هاوتا_نرخ.settimeout(5)
                    هاوتا_نرخ.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert هاوتا_نرخ.recvfrom(64)[0] == b'UDP-IN'
                دەق = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in دەق and 'exit 0' in دەق, دەق
                ڕاپۆرت_نرخ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in توێکڵ('terminal')
                توێکڵ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(تۆمار_ڕزن)
                ناردن('java 창예제\n'.encode())
                받기('GUI 예제 ئامادە_کردن_9ce364fc: 창예제\r\n'.encode(), 처음)
                처음 = len(تۆمار_ڕزن)
                ناردن(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ڕاپۆرت_نرخ['suspended_java_ps'] = توێکڵ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ڕاپۆرت_نرخ['suspended_java_ps']), ڕاپۆرت_نرخ['suspended_java_ps']
                ڕاپۆرت_نرخ['top'] = توێکڵ('top -n 1')
                assert 'java 창예제' in ڕاپۆرت_نرخ['top'] and 'kernel/shell' in ڕاپۆرت_نرخ['top']
                ڕاپۆرت_نرخ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ڕاپۆرت_نرخ['network_trace'] = 다리.추적기록
                assert not 다리.هەڵە, 다리.هەڵە
                ناردن(b'poweroff\n')
                assert پرۆسە_نرخ.wait(timeout=15) == 0
                ڕاپۆرت_نرخ['passed'] = True
            هەڵبژاردن_ئایتم.close()
    except Exception as هەڵە:
        ڕاپۆرت_نرخ['error'] = str(هەڵە)
        raise
    finally:
        if پرۆسە_نرخ is not None and پرۆسە_نرخ.poll() is None:
            پرۆسە_نرخ.terminate()
            try:
                پرۆسە_نرخ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                پرۆسە_نرخ.kill()
                پرۆسە_نرخ.wait()
        (출력 / 'serial.log').write_bytes(تۆمار_ڕزن)
        (출력 / 'report.json').write_text(json.dumps(ڕاپۆرت_نرخ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({کلیل_نرخ: ڕاپۆرت_نرخ[کلیل_نرخ] for کلیل_نرخ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ڕادان()
