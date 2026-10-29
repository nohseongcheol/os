#!/usr/bin/env python3
"""QEMU의 ਅਸਲ_ਸਮੱਗਰੀ CPU ਆਗਿਆ_ਕੀਮਤ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ਅਮਲ_ਕਰੋ_ਆਦੇਸ਼ import ਪ੍ਰੋਜੈਕਟ_ਰੂਟ, ਕਮਾਂਡ
from ਨੈਟਵਰਕ_ਬਰਿਜ import ਨੈਟਵਰਕ_ਬਰਿਜ
from 되돌림시험서버 import 되돌림시험서버


def ਚਲਾਓ_2():
    ਆਉਟਪੁੱਟ = ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/verification/execution-network-review'
    ਆਉਟਪੁੱਟ.mkdir(parents=True, exist_ok=True)
    ਵਿਵਰਨ_ਕੀਮਤ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ਪ੍ਰੋਜੈਕਟ_ਰੂਟ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ਸਰੋਤ_ਫ਼ਾਈਲਾਂ = {
        'ਇਜਾਜ਼ਤ_ਚੈਕ_ਕਰੋ': '''public class ਇਜਾਜ਼ਤ_ਚੈਕ_ਕਰੋ {
 public static void main(String[] ਆਰਗੂਮੈਂਟ) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ਨੈਟਵਰਕ_ਚੈਕ_ਕਰੋ': '''import java.net.*;
public class ਨੈਟਵਰਕ_ਚੈਕ_ਕਰੋ {
 public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
  Socket ਕੁਨੈਕਸ਼ਨ_ਕਰੋ = new Socket("10.0.2.2", Integer.parseInt(ਆਰਗੂਮੈਂਟ[0]));
  ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.setSoTimeout(3000);
  byte[] ਟੈਕਸਟ = "TCP 한글\\n".getBytes("UTF-8");
  ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getOutputStream().write(ਟੈਕਸਟ);
  for (int ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ < ਟੈਕਸਟ.length; ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ++)
   if (ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getInputStream().read() != (ਟੈਕਸਟ[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ] & 255)) throw new RuntimeException("TCP mismatch");
  ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ਟੈਕਸਟ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ਟੈਕਸਟ, ਟੈਕਸਟ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(ਆਰਗੂਮੈਂਟ[1])));
  byte[] ਜਵਾਬ_ਦਿਓ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ਜਵਾਬ_ਦਿਓ, ਜਵਾਬ_ਦਿਓ.length);
  종단.receive(전문);
  if (전문.getLength() != ਟੈਕਸਟ.length) throw new RuntimeException("UDP length");
  for (int ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ = 0; ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ < ਟੈਕਸਟ.length; ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ++)
   if (ਜਵਾਬ_ਦਿਓ[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ] != ਟੈਕਸਟ[ਸਥਿਤੀ_ਬਦਲੋ_ਅਨੁਕ੍ਰਮਣਿਕਾ]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] ਆਰਗੂਮੈਂਟ) throws Exception {
  ServerSocket ਸਰਵਰ_ਕੀਮਤ = new ServerSocket(9300); ਸਰਵਰ_ਕੀਮਤ.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ਕੁਨੈਕਸ਼ਨ_ਕਰੋ = ਸਰਵਰ_ਕੀਮਤ.accept(); ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.setSoTimeout(5000);
  ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getOutputStream().write(ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.getInputStream().read() + 1);
  ਕੁਨੈਕਸ਼ਨ_ਕਰੋ.close(); ਸਰਵਰ_ਕੀਮਤ.close();
  byte[] ਸਮੱਗਰੀ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ਸਮੱਗਰੀ, ਸਮੱਗਰੀ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ਨਾਂ, ਸਰੋਤ in ਸਰੋਤ_ਫ਼ਾਈਲਾਂ.items():
        (ਆਉਟਪੁੱਟ / (ਨਾਂ + '.java')).write_text(ਸਰੋਤ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ਆਉਟਪੁੱਟ)] +
                          [str(ਆਉਟਪੁੱਟ / (ਨਾਂ + '.java')) for ਨਾਂ in ਸਰੋਤ_ਫ਼ਾਈਲਾਂ])
    ਲੌਗ_ਕਤਾਰ = bytearray()
    def 빈접속번호(ਟਾਈਪ_ਕਰੋ_ਸ਼੍ਰੇਣੀ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ਟਾਈਪ_ਕਰੋ_ਸ਼੍ਰੇਣੀ) as ਖੋਜ_ਕੀਮਤ:
            ਖੋਜ_ਕੀਮਤ.bind(('127.0.0.4', 0))
            return ਖੋਜ_ਕੀਮਤ.getsockname()[1]
    파일접속번호, ਸੰਚਾਰ_ਰੋਕ_ਤਰੀਕਾ_ਪੋਰਟ, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    ਕਾਰਵਾਈ_ਕੀਮਤ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ਨੈਟਵਰਕ_ਬਰਿਜ(
                파일접속번호, ['tcp:{}:9300'.format(ਸੰਚਾਰ_ਰੋਕ_ਤਰੀਕਾ_ਪੋਰਟ), 'udp:{}:9301'.format(전문접속번호)],
                ਪਕੜਨਾ=True, ਹੋਸਟ_ਪਤਾ='127.0.0.4') as ਬਰਿਜ_ਕੀਮਤ:
            ਨਿਯੰਤਰਣ_ਰਸਤਾ = Path(임시) / 'qmp.sock'
            ਕਾਰਵਾਈ_ਕੀਮਤ = subprocess.Popen(ਕਮਾਂਡ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(ਨਿਯੰਤਰਣ_ਰਸਤਾ)] + ਬਰਿਜ_ਕੀਮਤ.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ਚੁਣੋ_ਆਇਟਮ = selectors.DefaultSelector()
            ਚੁਣੋ_ਆਇਟਮ.register(ਕਾਰਵਾਈ_ਕੀਮਤ.stdout, selectors.EVENT_READ)
            def 받기(ਸ਼ੋਅ_ਕੀਮਤ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ਸ਼ੋਅ_ਕੀਮਤ not in ਲੌਗ_ਕਤਾਰ[처음:]:
                    if time.monotonic() > 끝 or ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is not None:
                        raise AssertionError('Missing ' + repr(ਸ਼ੋਅ_ਕੀਮਤ) + '\n' + ਲੌਗ_ਕਤਾਰ[처음:].decode('utf-8', 'replace'))
                    for ਕੀ_ਕੀਮਤ, _ in ਚੁਣੋ_ਆਇਟਮ.select(.05):
                        조각 = ਕੀ_ਕੀਮਤ.fileobj.read(65536)
                        if 조각:
                            ਲੌਗ_ਕਤਾਰ.extend(조각)
                return ਲੌਗ_ਕਤਾਰ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ਈਮੇਲ(ਸਮੱਗਰੀ):
                ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.write(ਸਮੱਗਰੀ)
                ਕਾਰਵਾਈ_ਕੀਮਤ.stdin.flush()
            def ਸ਼ੈਲ(ਟੈਕਸਟ):
                print(ਟੈਕਸਟ, flush=True)
                처음 = len(ਲੌਗ_ਕਤਾਰ)
                ਈਮੇਲ((ਟੈਕਸਟ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as ਨਿਯੰਤਰਣ_ਕੀਮਤ:
                ਨਿਯੰਤਰਣ_ਕੀਮਤ.settimeout(10)
                ਨਿਯੰਤਰਣ_ਕੀਮਤ.connect(str(ਨਿਯੰਤਰਣ_ਰਸਤਾ))
                ਸਟ੍ਰੀਮ_ਕੀਮਤ = ਨਿਯੰਤਰਣ_ਕੀਮਤ.makefile('rwb')
                json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline())
                def 요청(ਨਿਰਦੇਸ਼_ਕੀਮਤ, ਆਰਗੂਮੈਂਟ=None):
                    ਸਮੱਗਰੀ = {'execute': ਨਿਰਦੇਸ਼_ਕੀਮਤ}
                    if ਆਰਗੂਮੈਂਟ is not None:
                        ਸਮੱਗਰੀ['arguments'] = ਆਰਗੂਮੈਂਟ
                    ਸਟ੍ਰੀਮ_ਕੀਮਤ.write((json.dumps(ਸਮੱਗਰੀ) + '\n').encode())
                    ਸਟ੍ਰੀਮ_ਕੀਮਤ.flush()
                    while True:
                        ਜਵਾਬ_ਦਿਓ = json.loads(ਸਟ੍ਰੀਮ_ਕੀਮਤ.readline())
                        if 'error' in ਜਵਾਬ_ਦਿਓ:
                            raise AssertionError(ਜਵਾਬ_ਦਿਓ)
                        if 'return' in ਜਵਾਬ_ਦਿਓ:
                            return ਜਵਾਬ_ਦਿਓ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ਵਿਵਰਨ_ਕੀਮਤ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ਵਿਵਰਨ_ਕੀਮਤ['shell_cpu'], ਵਿਵਰਨ_ਕੀਮਤ['shell_cpu']
                ਵਿਵਰਨ_ਕੀਮਤ['initial_ps'] = ਸ਼ੈਲ('ps')
                assert 'kernel/shell' in ਵਿਵਰਨ_ਕੀਮਤ['initial_ps']
                ਵਿਵਰਨ_ਕੀਮਤ['ipconfig'] = ਸ਼ੈਲ('ipconfig')
                assert 'inet 10.0.2.15' in ਵਿਵਰਨ_ਕੀਮਤ['ipconfig']
                ਵਿਵਰਨ_ਕੀਮਤ['gateway_ping'] = ਸ਼ੈਲ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ਵਿਵਰਨ_ਕੀਮਤ['gateway_ping']
                assert 'FTP listening' in ਸ਼ੈਲ('ftpd start')
                with ftplib.FTP() as ਸਥਾਂਨਤਰ_ਕੀਮਤ:
                    ਸਥਾਂਨਤਰ_ਕੀਮਤ.encoding = 'utf-8'
                    ਸਥਾਂਨਤਰ_ਕੀਮਤ.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ਸਥਾਂਨਤਰ_ਕੀਮਤ.login()
                    for ਨਾਂ in ਸਰੋਤ_ਫ਼ਾਈਲਾਂ:
                        ਸਥਾਂਨਤਰ_ਕੀਮਤ.storbinary('STOR ' + ਨਾਂ + '.class', io.BytesIO((ਆਉਟਪੁੱਟ / (ਨਾਂ + '.class')).read_bytes()))
                처음 = len(ਲੌਗ_ਕਤਾਰ)
                ਈਮੇਲ('java ਇਜਾਜ਼ਤ_ਚੈਕ_ਕਰੋ\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ਵਿਵਰਨ_ਕੀਮਤ['java_cpu'] = 권한읽기()
                    if 'EL0t' in ਵਿਵਰਨ_ਕੀਮਤ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ਵਿਵਰਨ_ਕੀਮਤ['java_cpu'], ਵਿਵਰਨ_ਕੀਮਤ['java_cpu']
                받기(처음=처음)
                ਵਿਵਰਨ_ਕੀਮਤ['after_exit_ps'] = ਸ਼ੈਲ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ਵਿਵਰਨ_ਕੀਮਤ['after_exit_ps'])
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ਪਿਅਰ_ਕੀਮਤ:
                    ਟੈਕਸਟ = ਸ਼ੈਲ('java ਨੈਟਵਰਕ_ਚੈਕ_ਕਰੋ {} {}'.format(ਪਿਅਰ_ਕੀਮਤ.ਸੰਚਾਰ_ਰੋਕ_ਤਰੀਕਾ_ਪੋਰਟ, ਪਿਅਰ_ਕੀਮਤ.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
                    assert ਪਿਅਰ_ਕੀਮਤ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ਪਿਅਰ_ਕੀਮਤ.수신됨
                    assert not ਪਿਅਰ_ਕੀਮਤ.오류들, ਪਿਅਰ_ਕੀਮਤ.오류들
                    ਵਿਵਰਨ_ਕੀਮਤ['outbound_peers'] = {종류: ਸਮੱਗਰੀ.decode() for 종류, ਸਮੱਗਰੀ in ਪਿਅਰ_ਕੀਮਤ.수신됨.items()}
                처음 = len(ਲੌਗ_ਕਤਾਰ)
                ਈਮੇਲ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ਸੰਚਾਰ_ਰੋਕ_ਤਰੀਕਾ_ਪੋਰਟ), timeout=5) as ਪਿਅਰ_ਕੀਮਤ:
                    ਪਿਅਰ_ਕੀਮਤ.sendall(b'A')
                    assert ਪਿਅਰ_ਕੀਮਤ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ਪਿਅਰ_ਕੀਮਤ:
                    ਪਿਅਰ_ਕੀਮਤ.settimeout(5)
                    ਪਿਅਰ_ਕੀਮਤ.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ਪਿਅਰ_ਕੀਮਤ.recvfrom(64)[0] == b'UDP-IN'
                ਟੈਕਸਟ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ਟੈਕਸਟ and 'exit 0' in ਟੈਕਸਟ, ਟੈਕਸਟ
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ਸ਼ੈਲ('terminal')
                ਸ਼ੈਲ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ਲੌਗ_ਕਤਾਰ)
                ਈਮੇਲ('java 창예제\n'.encode())
                받기('GUI 예제 ਤਿਆਰ_ਕਰੋ: 창예제\r\n'.encode(), 처음)
                처음 = len(ਲੌਗ_ਕਤਾਰ)
                ਈਮੇਲ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ਵਿਵਰਨ_ਕੀਮਤ['suspended_java_ps'] = ਸ਼ੈਲ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ਵਿਵਰਨ_ਕੀਮਤ['suspended_java_ps']), ਵਿਵਰਨ_ਕੀਮਤ['suspended_java_ps']
                ਵਿਵਰਨ_ਕੀਮਤ['top'] = ਸ਼ੈਲ('top -n 1')
                assert 'java 창예제' in ਵਿਵਰਨ_ਕੀਮਤ['top'] and 'kernel/shell' in ਵਿਵਰਨ_ਕੀਮਤ['top']
                ਵਿਵਰਨ_ਕੀਮਤ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ਵਿਵਰਨ_ਕੀਮਤ['network_trace'] = ਬਰਿਜ_ਕੀਮਤ.ਟਰੇਸ_ਲੌਗ
                assert not ਬਰਿਜ_ਕੀਮਤ.ਗਲਤੀ, ਬਰਿਜ_ਕੀਮਤ.ਗਲਤੀ
                ਈਮੇਲ(b'poweroff\n')
                assert ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=15) == 0
                ਵਿਵਰਨ_ਕੀਮਤ['passed'] = True
            ਚੁਣੋ_ਆਇਟਮ.close()
    except Exception as ਗਲਤੀ:
        ਵਿਵਰਨ_ਕੀਮਤ['error'] = str(ਗਲਤੀ)
        raise
    finally:
        if ਕਾਰਵਾਈ_ਕੀਮਤ is not None and ਕਾਰਵਾਈ_ਕੀਮਤ.poll() is None:
            ਕਾਰਵਾਈ_ਕੀਮਤ.terminate()
            try:
                ਕਾਰਵਾਈ_ਕੀਮਤ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ਕਾਰਵਾਈ_ਕੀਮਤ.kill()
                ਕਾਰਵਾਈ_ਕੀਮਤ.wait()
        (ਆਉਟਪੁੱਟ / 'serial.log').write_bytes(ਲੌਗ_ਕਤਾਰ)
        (ਆਉਟਪੁੱਟ / 'report.json').write_text(json.dumps(ਵਿਵਰਨ_ਕੀਮਤ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ਕੀ_ਕੀਮਤ: ਵਿਵਰਨ_ਕੀਮਤ[ਕੀ_ਕੀਮਤ] for ਕੀ_ਕੀਮਤ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ਚਲਾਓ_2()
