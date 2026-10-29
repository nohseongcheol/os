#!/usr/bin/env python3
"""QEMU의 ھەقىقىي_مەلۇمات CPU ئىجازەت_قىممىتى, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز, بۇيرۇق
from تور_كۆۋرۈك import تور_كۆۋرۈك
from 되돌림시험서버 import 되돌림시험서버


def ئىجرا_قىل_2():
    چىقار = كۆرسىتىش_يىلتىز / 'build/verification/execution-network-review'
    چىقار.mkdir(parents=True, exist_ok=True)
    خەۋەر_قىممىتى = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    مەنبە_ھۆججەت = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] ئۆزگەرگۈچىلەر) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'تور_تەكشۈرۈش': '''import java.net.*;
public class تور_تەكشۈرۈش {
 public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
  Socket ئۇلا = new Socket("10.0.2.2", Integer.parseInt(ئۆزگەرگۈچىلەر[0]));
  ئۇلا.setSoTimeout(3000);
  byte[] تېكىست = "TCP 한글\\n".getBytes("UTF-8");
  ئۇلا.getOutputStream().write(تېكىست);
  for (int ئورۇنلاشتۇرۇش_ئىندېكس = 0; ئورۇنلاشتۇرۇش_ئىندېكس < تېكىست.length; ئورۇنلاشتۇرۇش_ئىندېكس++)
   if (ئۇلا.getInputStream().read() != (تېكىست[ئورۇنلاشتۇرۇش_ئىندېكس] & 255)) throw new RuntimeException("TCP mismatch");
  ئۇلا.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  تېكىست = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(تېكىست, تېكىست.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(ئۆزگەرگۈچىلەر[1])));
  byte[] جاۋابلاش = new byte[64]; DatagramPacket 전문 = new DatagramPacket(جاۋابلاش, جاۋابلاش.length);
  종단.receive(전문);
  if (전문.getLength() != تېكىست.length) throw new RuntimeException("UDP length");
  for (int ئورۇنلاشتۇرۇش_ئىندېكس = 0; ئورۇنلاشتۇرۇش_ئىندېكس < تېكىست.length; ئورۇنلاشتۇرۇش_ئىندېكس++)
   if (جاۋابلاش[ئورۇنلاشتۇرۇش_ئىندېكس] != تېكىست[ئورۇنلاشتۇرۇش_ئىندېكس]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception {
  ServerSocket مۇلازىمىتېر_قىممىتى = new ServerSocket(9300); مۇلازىمىتېر_قىممىتى.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ئۇلا = مۇلازىمىتېر_قىممىتى.accept(); ئۇلا.setSoTimeout(5000);
  ئۇلا.getOutputStream().write(ئۇلا.getInputStream().read() + 1);
  ئۇلا.close(); مۇلازىمىتېر_قىممىتى.close();
  byte[] مەلۇمات = new byte[64]; DatagramPacket 전문 = new DatagramPacket(مەلۇمات, مەلۇمات.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ئاتى, مەنبە in مەنبە_ھۆججەت.items():
        (چىقار / (ئاتى + '.java')).write_text(مەنبە, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(چىقار)] +
                          [str(چىقار / (ئاتى + '.java')) for ئاتى in مەنبە_ھۆججەت])
    خاتىرە_قۇر = bytearray()
    def 빈접속번호(تىپ_تۈر=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, تىپ_تۈر) as ئىزدەش_قىممىتى:
            ئىزدەش_قىممىتى.bind(('127.0.0.4', 0))
            return ئىزدەش_قىممىتى.getsockname()[1]
    파일접속번호, يەتكۈزۈش_كونترول_كېلىشىمى_ئېغىز, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    جەريان_قىممىتى = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, تور_كۆۋرۈك(
                파일접속번호, ['tcp:{}:9300'.format(يەتكۈزۈش_كونترول_كېلىشىمى_ئېغىز), 'udp:{}:9301'.format(전문접속번호)],
                تۇتۇش=True, باقار_ئادرېس='127.0.0.4') as كۆۋرۈك_قىممىتى:
            كونترول_يول = Path(임시) / 'qmp.sock'
            جەريان_قىممىتى = subprocess.Popen(بۇيرۇق() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(كونترول_يول)] + كۆۋرۈك_قىممىتى.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            تاللىماق_تۈر = selectors.DefaultSelector()
            تاللىماق_تۈر.register(جەريان_قىممىتى.stdout, selectors.EVENT_READ)
            def 받기(كۆرسەتمەك_قىممىتى=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while كۆرسەتمەك_قىممىتى not in خاتىرە_قۇر[처음:]:
                    if time.monotonic() > 끝 or جەريان_قىممىتى.poll() is not None:
                        raise AssertionError('Missing ' + repr(كۆرسەتمەك_قىممىتى) + '\n' + خاتىرە_قۇر[처음:].decode('utf-8', 'replace'))
                    for ئاچقۇچ_قىممىتى, _ in تاللىماق_تۈر.select(.05):
                        조각 = ئاچقۇچ_قىممىتى.fileobj.read(65536)
                        if 조각:
                            خاتىرە_قۇر.extend(조각)
                return خاتىرە_قۇر[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ئەۋەتمەك(مەلۇمات):
                جەريان_قىممىتى.stdin.write(مەلۇمات)
                جەريان_قىممىتى.stdin.flush()
            def قاپ(تېكىست):
                print(تېكىست, flush=True)
                처음 = len(خاتىرە_قۇر)
                ئەۋەتمەك((تېكىست + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as كونترول_قىممىتى:
                كونترول_قىممىتى.settimeout(10)
                كونترول_قىممىتى.connect(str(كونترول_يول))
                ئېقىم_قىممىتى = كونترول_قىممىتى.makefile('rwb')
                json.loads(ئېقىم_قىممىتى.readline())
                def 요청(بۇيرۇق_قىممىتى, ئۆزگەرگۈچىلەر=None):
                    مەلۇمات = {'execute': بۇيرۇق_قىممىتى}
                    if ئۆزگەرگۈچىلەر is not None:
                        مەلۇمات['arguments'] = ئۆزگەرگۈچىلەر
                    ئېقىم_قىممىتى.write((json.dumps(مەلۇمات) + '\n').encode())
                    ئېقىم_قىممىتى.flush()
                    while True:
                        جاۋابلاش = json.loads(ئېقىم_قىممىتى.readline())
                        if 'error' in جاۋابلاش:
                            raise AssertionError(جاۋابلاش)
                        if 'return' in جاۋابلاش:
                            return جاۋابلاش['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                خەۋەر_قىممىتى['shell_cpu'] = 권한읽기()
                assert 'EL1h' in خەۋەر_قىممىتى['shell_cpu'], خەۋەر_قىممىتى['shell_cpu']
                خەۋەر_قىممىتى['initial_ps'] = قاپ('ps')
                assert 'kernel/shell' in خەۋەر_قىممىتى['initial_ps']
                خەۋەر_قىممىتى['ipconfig'] = قاپ('ipconfig')
                assert 'inet 10.0.2.15' in خەۋەر_قىممىتى['ipconfig']
                خەۋەر_قىممىتى['gateway_ping'] = قاپ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in خەۋەر_قىممىتى['gateway_ping']
                assert 'FTP listening' in قاپ('ftpd start')
                with ftplib.FTP() as يوللاش_قىممىتى_630ba093:
                    يوللاش_قىممىتى_630ba093.encoding = 'utf-8'
                    يوللاش_قىممىتى_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    يوللاش_قىممىتى_630ba093.login()
                    for ئاتى in مەنبە_ھۆججەت:
                        يوللاش_قىممىتى_630ba093.storbinary('STOR ' + ئاتى + '.class', io.BytesIO((چىقار / (ئاتى + '.class')).read_bytes()))
                처음 = len(خاتىرە_قۇر)
                ئەۋەتمەك('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    خەۋەر_قىممىتى['java_cpu'] = 권한읽기()
                    if 'EL0t' in خەۋەر_قىممىتى['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in خەۋەر_قىممىتى['java_cpu'], خەۋەر_قىممىتى['java_cpu']
                받기(처음=처음)
                خەۋەر_قىممىتى['after_exit_ps'] = قاپ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', خەۋەر_قىممىتى['after_exit_ps'])
                خەۋەر_قىممىتى['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as باراۋەرلىك_قىممىتى:
                    تېكىست = قاپ('java تور_تەكشۈرۈش {} {}'.format(باراۋەرلىك_قىممىتى.يەتكۈزۈش_كونترول_كېلىشىمى_ئېغىز, باراۋەرلىك_قىممىتى.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in تېكىست and 'exit 0' in تېكىست, تېكىست
                    assert باراۋەرلىك_قىممىتى.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, باراۋەرلىك_قىممىتى.수신됨
                    assert not باراۋەرلىك_قىممىتى.오류들, باراۋەرلىك_قىممىتى.오류들
                    خەۋەر_قىممىتى['outbound_peers'] = {종류: مەلۇمات.decode() for 종류, مەلۇمات in باراۋەرلىك_قىممىتى.수신됨.items()}
                처음 = len(خاتىرە_قۇر)
                ئەۋەتمەك('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', يەتكۈزۈش_كونترول_كېلىشىمى_ئېغىز), timeout=5) as باراۋەرلىك_قىممىتى:
                    باراۋەرلىك_قىممىتى.sendall(b'A')
                    assert باراۋەرلىك_قىممىتى.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as باراۋەرلىك_قىممىتى:
                    باراۋەرلىك_قىممىتى.settimeout(5)
                    باراۋەرلىك_قىممىتى.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert باراۋەرلىك_قىممىتى.recvfrom(64)[0] == b'UDP-IN'
                تېكىست = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in تېكىست and 'exit 0' in تېكىست, تېكىست
                خەۋەر_قىممىتى['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in قاپ('terminal')
                قاپ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(خاتىرە_قۇر)
                ئەۋەتمەك('java 창예제\n'.encode())
                받기('GUI 예제 تەييارلىماق: 창예제\r\n'.encode(), 처음)
                처음 = len(خاتىرە_قۇر)
                ئەۋەتمەك(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                خەۋەر_قىممىتى['suspended_java_ps'] = قاپ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', خەۋەر_قىممىتى['suspended_java_ps']), خەۋەر_قىممىتى['suspended_java_ps']
                خەۋەر_قىممىتى['top'] = قاپ('top -n 1')
                assert 'java 창예제' in خەۋەر_قىممىتى['top'] and 'kernel/shell' in خەۋەر_قىممىتى['top']
                خەۋەر_قىممىتى['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                خەۋەر_قىممىتى['network_trace'] = كۆۋرۈك_قىممىتى.추적기록
                assert not كۆۋرۈك_قىممىتى.خاتالىق, كۆۋرۈك_قىممىتى.خاتالىق
                ئەۋەتمەك(b'poweroff\n')
                assert جەريان_قىممىتى.wait(timeout=15) == 0
                خەۋەر_قىممىتى['passed'] = True
            تاللىماق_تۈر.close()
    except Exception as خاتالىق:
        خەۋەر_قىممىتى['error'] = str(خاتالىق)
        raise
    finally:
        if جەريان_قىممىتى is not None and جەريان_قىممىتى.poll() is None:
            جەريان_قىممىتى.terminate()
            try:
                جەريان_قىممىتى.wait(timeout=10)
            except subprocess.TimeoutExpired:
                جەريان_قىممىتى.kill()
                جەريان_قىممىتى.wait()
        (چىقار / 'serial.log').write_bytes(خاتىرە_قۇر)
        (چىقار / 'report.json').write_text(json.dumps(خەۋەر_قىممىتى, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ئاچقۇچ_قىممىتى: خەۋەر_قىممىتى[ئاچقۇچ_قىممىتى] for ئاچقۇچ_قىممىتى in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ئىجرا_قىل_2()
