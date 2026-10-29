#!/usr/bin/env python3
"""QEMU의 ನಿಜವಾದ_ಡೇಟಾ CPU ಅನುಮತಿ_ಮೌಲ್ಯ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ಪೂರೈಸು_ಆದೇಶ import ಬಿಂಬಿಸು_ಮೂಲ, ಆಜ್ಞೆ
from ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ import ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ
from 되돌림시험서버 import 되돌림시험서버


def ಚಲಾಯಿಸು_2():
    ಔಟ್_ಪುಟ್ = ಬಿಂಬಿಸು_ಮೂಲ / 'build/verification/execution-network-review'
    ಔಟ್_ಪುಟ್.mkdir(parents=True, exist_ok=True)
    ವರದಿ_ಮೌಲ್ಯ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ಬಿಂಬಿಸು_ಮೂಲ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ಮೂಲ_ಫೈಲ್_ಗಳು = {
        'ಅನುಮತಿ_ಚೆಕ್': '''public class ಅನುಮತಿ_ಚೆಕ್ {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ನೆಟ್_ವರ್ಕ್_ಚೆಕ್': '''import java.net.*;
public class ನೆಟ್_ವರ್ಕ್_ಚೆಕ್ {
 public static void main(String[] 인수) throws Exception {
  Socket ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.setSoTimeout(3000);
  byte[] ಪಠ್ಯ = "TCP 한글\\n".getBytes("UTF-8");
  ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getOutputStream().write(ಪಠ್ಯ);
  for (int ಹುದ್ದೆ_ಪದಸೂಚಿ = 0; ಹುದ್ದೆ_ಪದಸೂಚಿ < ಪಠ್ಯ.length; ಹುದ್ದೆ_ಪದಸೂಚಿ++)
   if (ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getInputStream().read() != (ಪಠ್ಯ[ಹುದ್ದೆ_ಪದಸೂಚಿ] & 255)) throw new RuntimeException("TCP mismatch");
  ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ಪಠ್ಯ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ಪಠ್ಯ, ಪಠ್ಯ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] ಪ್ರತ್ಯುತ್ತರ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ಪ್ರತ್ಯುತ್ತರ, ಪ್ರತ್ಯುತ್ತರ.length);
  종단.receive(전문);
  if (전문.getLength() != ಪಠ್ಯ.length) throw new RuntimeException("UDP length");
  for (int ಹುದ್ದೆ_ಪದಸೂಚಿ = 0; ಹುದ್ದೆ_ಪದಸೂಚಿ < ಪಠ್ಯ.length; ಹುದ್ದೆ_ಪದಸೂಚಿ++)
   if (ಪ್ರತ್ಯುತ್ತರ[ಹುದ್ದೆ_ಪದಸೂಚಿ] != ಪಠ್ಯ[ಹುದ್ದೆ_ಪದಸೂಚಿ]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket ಸರ್ವರ್_ಮೌಲ್ಯ = new ServerSocket(9300); ಸರ್ವರ್_ಮೌಲ್ಯ.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು = ಸರ್ವರ್_ಮೌಲ್ಯ.accept(); ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.setSoTimeout(5000);
  ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getOutputStream().write(ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.getInputStream().read() + 1);
  ಸಂಪರ್ಕ_ಕಲ್ಪಿಸು.close(); ಸರ್ವರ್_ಮೌಲ್ಯ.close();
  byte[] ಡೇಟಾ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ಡೇಟಾ, ಡೇಟಾ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ಹೆಸರು, ಮೂಲ in ಮೂಲ_ಫೈಲ್_ಗಳು.items():
        (ಔಟ್_ಪುಟ್ / (ಹೆಸರು + '.java')).write_text(ಮೂಲ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ಔಟ್_ಪುಟ್)] +
                          [str(ಔಟ್_ಪುಟ್ / (ಹೆಸರು + '.java')) for ಹೆಸರು in ಮೂಲ_ಫೈಲ್_ಗಳು])
    ಲಾಗ್_ದಾಖಲೆ = bytearray()
    def ಖಾಲಿ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ(ಪ್ರಕಾರ_ವರ್ಗ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ಪ್ರಕಾರ_ವರ್ಗ) as ಶೋಧ_ಮೌಲ್ಯ:
            ಶೋಧ_ಮೌಲ್ಯ.bind(('127.0.0.4', 0))
            return ಶೋಧ_ಮೌಲ್ಯ.getsockname()[1]
    ಫೈಲ್_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, ಪ್ರಸಾರ_ನಿಯಂತ್ರಣ_ಪ್ರೊಟೋಕಾಲ್_ಪೋರ್ಟ್, 전문접속번호 = ಖಾಲಿ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ(), ಖಾಲಿ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ(), ಖಾಲಿ_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ(socket.SOCK_DGRAM)
    ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ನೆಟ್_ವರ್ಕ್_ಸೇತುವೆ(
                ಫೈಲ್_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, ['tcp:{}:9300'.format(ಪ್ರಸಾರ_ನಿಯಂತ್ರಣ_ಪ್ರೊಟೋಕಾಲ್_ಪೋರ್ಟ್), 'udp:{}:9301'.format(전문접속번호)],
                ಸೆರೆಹಿಡಿ=True, ಹೋಸ್ಟ್_ಇಮೇಲ್='127.0.0.4') as ಸೇತುವೆ_ಮೌಲ್ಯ:
            ನಿಯಂತ್ರಣ_ಹಾದಿ = Path(임시) / 'qmp.sock'
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ = subprocess.Popen(ಆಜ್ಞೆ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ನಿಯಂತ್ರಣ_ಹಾದಿ)] + ಸೇತುವೆ_ಮೌಲ್ಯ.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ಆರಿಸು_ಅಂಶ = selectors.DefaultSelector()
            ಆರಿಸು_ಅಂಶ.register(ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdout, selectors.EVENT_READ)
            def 받기(ಶೋ_ಮೌಲ್ಯ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ಶೋ_ಮೌಲ್ಯ not in ಲಾಗ್_ದಾಖಲೆ[처음:]:
                    if time.monotonic() > 끝 or ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ಶೋ_ಮೌಲ್ಯ) + '\n' + ಲಾಗ್_ದಾಖಲೆ[처음:].decode('utf-8', 'replace'))
                    for ಕೀ_ಮೌಲ್ಯ, _ in ಆರಿಸು_ಅಂಶ.select(.05):
                        조각 = ಕೀ_ಮೌಲ್ಯ.fileobj.read(65536)
                        if 조각:
                            ಲಾಗ್_ದಾಖಲೆ.extend(조각)
                return ಲಾಗ್_ದಾಖಲೆ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ಕಳುಹಿಸಿ(ಡೇಟಾ):
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.write(ಡೇಟಾ)
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.stdin.flush()
            def ಶೆಲ್(ಪಠ್ಯ):
                print(ಪಠ್ಯ, flush=True)
                처음 = len(ಲಾಗ್_ದಾಖಲೆ)
                ಕಳುಹಿಸಿ((ಪಠ್ಯ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ:
                ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ.settimeout(10)
                ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ.connect(str(ನಿಯಂತ್ರಣ_ಹಾದಿ))
                ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ = ನಿಯಂತ್ರಣ_ಮೌಲ್ಯ.makefile('rwb')
                json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline())
                def 요청(ಸೂಚನೆ_ಮೌಲ್ಯ, 인수=None):
                    ಡೇಟಾ = {'execute': ಸೂಚನೆ_ಮೌಲ್ಯ}
                    if 인수 is not None:
                        ಡೇಟಾ['arguments'] = 인수
                    ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.write((json.dumps(ಡೇಟಾ) + '\n').encode())
                    ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.flush()
                    while True:
                        ಪ್ರತ್ಯುತ್ತರ = json.loads(ಸ್ಟ್ರೀಮ್_ಮೌಲ್ಯ.readline())
                        if 'error' in ಪ್ರತ್ಯುತ್ತರ:
                            raise AssertionError(ಪ್ರತ್ಯುತ್ತರ)
                        if 'return' in ಪ್ರತ್ಯುತ್ತರ:
                            return ಪ್ರತ್ಯುತ್ತರ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ವರದಿ_ಮೌಲ್ಯ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ವರದಿ_ಮೌಲ್ಯ['shell_cpu'], ವರದಿ_ಮೌಲ್ಯ['shell_cpu']
                ವರದಿ_ಮೌಲ್ಯ['initial_ps'] = ಶೆಲ್('ps')
                assert 'kernel/shell' in ವರದಿ_ಮೌಲ್ಯ['initial_ps']
                ವರದಿ_ಮೌಲ್ಯ['ipconfig'] = ಶೆಲ್('ipconfig')
                assert 'inet 10.0.2.15' in ವರದಿ_ಮೌಲ್ಯ['ipconfig']
                ವರದಿ_ಮೌಲ್ಯ['gateway_ping'] = ಶೆಲ್('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ವರದಿ_ಮೌಲ್ಯ['gateway_ping']
                assert 'FTP listening' in ಶೆಲ್('ftpd start')
                with ftplib.FTP() as ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ:
                    ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.encoding = 'utf-8'
                    ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.connect('127.0.0.4', ಫೈಲ್_ಪೋರ್ಟ್_ಸಂಖ್ಯೆ, timeout=20)
                    ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.login()
                    for ಹೆಸರು in ಮೂಲ_ಫೈಲ್_ಗಳು:
                        ವರ್ಗಾವಣೆ_ಮೌಲ್ಯ.storbinary('STOR ' + ಹೆಸರು + '.class', io.BytesIO((ಔಟ್_ಪುಟ್ / (ಹೆಸರು + '.class')).read_bytes()))
                처음 = len(ಲಾಗ್_ದಾಖಲೆ)
                ಕಳುಹಿಸಿ('java ಅನುಮತಿ_ಚೆಕ್\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ವರದಿ_ಮೌಲ್ಯ['java_cpu'] = 권한읽기()
                    if 'EL0t' in ವರದಿ_ಮೌಲ್ಯ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ವರದಿ_ಮೌಲ್ಯ['java_cpu'], ವರದಿ_ಮೌಲ್ಯ['java_cpu']
                받기(처음=처음)
                ವರದಿ_ಮೌಲ್ಯ['after_exit_ps'] = ಶೆಲ್('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ವರದಿ_ಮೌಲ್ಯ['after_exit_ps'])
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ಪೀರ್_ಮೌಲ್ಯ:
                    ಪಠ್ಯ = ಶೆಲ್('java ನೆಟ್_ವರ್ಕ್_ಚೆಕ್ {} {}'.format(ಪೀರ್_ಮೌಲ್ಯ.ಪ್ರಸಾರ_ನಿಯಂತ್ರಣ_ಪ್ರೊಟೋಕಾಲ್_ಪೋರ್ಟ್, ಪೀರ್_ಮೌಲ್ಯ.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
                    assert ಪೀರ್_ಮೌಲ್ಯ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ಪೀರ್_ಮೌಲ್ಯ.수신됨
                    assert not ಪೀರ್_ಮೌಲ್ಯ.오류들, ಪೀರ್_ಮೌಲ್ಯ.오류들
                    ವರದಿ_ಮೌಲ್ಯ['outbound_peers'] = {종류: ಡೇಟಾ.decode() for 종류, ಡೇಟಾ in ಪೀರ್_ಮೌಲ್ಯ.수신됨.items()}
                처음 = len(ಲಾಗ್_ದಾಖಲೆ)
                ಕಳುಹಿಸಿ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ಪ್ರಸಾರ_ನಿಯಂತ್ರಣ_ಪ್ರೊಟೋಕಾಲ್_ಪೋರ್ಟ್), timeout=5) as ಪೀರ್_ಮೌಲ್ಯ:
                    ಪೀರ್_ಮೌಲ್ಯ.sendall(b'A')
                    assert ಪೀರ್_ಮೌಲ್ಯ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ಪೀರ್_ಮೌಲ್ಯ:
                    ಪೀರ್_ಮೌಲ್ಯ.settimeout(5)
                    ಪೀರ್_ಮೌಲ್ಯ.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ಪೀರ್_ಮೌಲ್ಯ.recvfrom(64)[0] == b'UDP-IN'
                ಪಠ್ಯ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ಪಠ್ಯ and 'exit 0' in ಪಠ್ಯ, ಪಠ್ಯ
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ಶೆಲ್('terminal')
                ಶೆಲ್('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ಲಾಗ್_ದಾಖಲೆ)
                ಕಳುಹಿಸಿ('java 창예제\n'.encode())
                받기('GUI 예제 ಸಿದ್ಧಪಡಿಸು: 창예제\r\n'.encode(), 처음)
                처음 = len(ಲಾಗ್_ದಾಖಲೆ)
                ಕಳುಹಿಸಿ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ವರದಿ_ಮೌಲ್ಯ['suspended_java_ps'] = ಶೆಲ್('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ವರದಿ_ಮೌಲ್ಯ['suspended_java_ps']), ವರದಿ_ಮೌಲ್ಯ['suspended_java_ps']
                ವರದಿ_ಮೌಲ್ಯ['top'] = ಶೆಲ್('top -n 1')
                assert 'java 창예제' in ವರದಿ_ಮೌಲ್ಯ['top'] and 'kernel/shell' in ವರದಿ_ಮೌಲ್ಯ['top']
                ವರದಿ_ಮೌಲ್ಯ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ವರದಿ_ಮೌಲ್ಯ['network_trace'] = ಸೇತುವೆ_ಮೌಲ್ಯ.ಟ್ರೇಸ್_ಲಾಗ್
                assert not ಸೇತುವೆ_ಮೌಲ್ಯ.ದೋಷ, ಸೇತುವೆ_ಮೌಲ್ಯ.ದೋಷ
                ಕಳುಹಿಸಿ(b'poweroff\n')
                assert ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=15) == 0
                ವರದಿ_ಮೌಲ್ಯ['passed'] = True
            ಆರಿಸು_ಅಂಶ.close()
    except Exception as ದೋಷ:
        ವರದಿ_ಮೌಲ್ಯ['error'] = str(ದೋಷ)
        raise
    finally:
        if ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ is not None and ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.poll() is None:
            ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.terminate()
            try:
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.kill()
                ಪ್ರಕ್ರಿಯೆ_ಮೌಲ್ಯ.wait()
        (ಔಟ್_ಪುಟ್ / 'serial.log').write_bytes(ಲಾಗ್_ದಾಖಲೆ)
        (ಔಟ್_ಪುಟ್ / 'report.json').write_text(json.dumps(ವರದಿ_ಮೌಲ್ಯ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ಕೀ_ಮೌಲ್ಯ: ವರದಿ_ಮೌಲ್ಯ[ಕೀ_ಮೌಲ್ಯ] for ಕೀ_ಮೌಲ್ಯ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ಚಲಾಯಿಸು_2()
