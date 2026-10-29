#!/usr/bin/env python3
"""QEMU의 තථ්_ය_දත්ත CPU අවසරය_අගය, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ක්_රියාත්මක_කරන්න_විධානය import 기준, විධානය
from ජාලය_පාලම import ජාලය_පාලම
from 되돌림시험서버 import 되돌림시험서버


def ක්_රියාත්මක_කරන්න_2():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    වාර්තාව_අගය = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    මූලය_ගොනු = {
        'අවසරය_චෙක්පත': '''public class අවසරය_චෙක්පත {
 public static void main(String[] විස්තාරක) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ජාලය_චෙක්පත': '''import java.net.*;
public class ජාලය_චෙක්පත {
 public static void main(String[] විස්තාරක) throws Exception {
  Socket සම්බන්ද_වන්න = new Socket("10.0.2.2", Integer.parseInt(විස්තාරක[0]));
  සම්බන්ද_වන්න.setSoTimeout(3000);
  byte[] පෙළ = "TCP 한글\\n".getBytes("UTF-8");
  සම්බන්ද_වන්න.getOutputStream().write(පෙළ);
  for (int 자리 = 0; 자리 < පෙළ.length; 자리++)
   if (සම්බන්ද_වන්න.getInputStream().read() != (පෙළ[자리] & 255)) throw new RuntimeException("TCP mismatch");
  සම්බන්ද_වන්න.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  පෙළ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(පෙළ, පෙළ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(විස්තාරක[1])));
  byte[] පිළිතුරු_දෙන්න = new byte[64]; DatagramPacket 전문 = new DatagramPacket(පිළිතුරු_දෙන්න, පිළිතුරු_දෙන්න.length);
  종단.receive(전문);
  if (전문.getLength() != පෙළ.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < පෙළ.length; 자리++)
   if (පිළිතුරු_දෙන්න[자리] != පෙළ[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] විස්තාරක) throws Exception {
  ServerSocket සේවාදායකය_අගය = new ServerSocket(9300); සේවාදායකය_අගය.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket සම්බන්ද_වන්න = සේවාදායකය_අගය.accept(); සම්බන්ද_වන්න.setSoTimeout(5000);
  සම්බන්ද_වන්න.getOutputStream().write(සම්බන්ද_වන්න.getInputStream().read() + 1);
  සම්බන්ද_වන්න.close(); සේවාදායකය_අගය.close();
  byte[] දත්ත = new byte[64]; DatagramPacket 전문 = new DatagramPacket(දත්ත, දත්ත.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for නම, මූලය in මූලය_ගොනු.items():
        (출력 / (නම + '.java')).write_text(මූලය, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (නම + '.java')) for නම in මූලය_ගොනු])
    ලොගය_පේළිය = bytearray()
    def 빈접속번호(ටයිප්_කරන්න_ප්_රවර්ගය=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ටයිප්_කරන්න_ප්_රවර්ගය) as සෙවීම_අගය:
            සෙවීම_අගය.bind(('127.0.0.4', 0))
            return සෙවීම_අගය.getsockname()[1]
    파일접속번호, සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    ක්_රියාවලිය_අගය = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ජාලය_පාලම(
                파일접속번호, ['tcp:{}:9300'.format(සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට), 'udp:{}:9301'.format(전문접속번호)],
                ග්_රහණය=True, ධාරකය_යොමුව='127.0.0.4') as පාලම_අගය:
            පාලකය_පෙත = Path(임시) / 'qmp.sock'
            ක්_රියාවලිය_අගය = subprocess.Popen(විධානය() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(පාලකය_පෙත)] + පාලම_අගය.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            තෝරන්න_අයිතමය = selectors.DefaultSelector()
            තෝරන්න_අයිතමය.register(ක්_රියාවලිය_අගය.stdout, selectors.EVENT_READ)
            def 받기(දර්ශනය_අගය=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while දර්ශනය_අගය not in ලොගය_පේළිය[처음:]:
                    if time.monotonic() > 끝 or ක්_රියාවලිය_අගය.poll() is not None:
                        raise AssertionError('Missing ' + repr(දර්ශනය_අගය) + '\n' + ලොගය_පේළිය[처음:].decode('utf-8', 'replace'))
                    for යතුර_අගය, _ in තෝරන්න_අයිතමය.select(.05):
                        조각 = යතුර_අගය.fileobj.read(65536)
                        if 조각:
                            ලොගය_පේළිය.extend(조각)
                return ලොගය_පේළිය[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ඊමේල්(දත්ත):
                ක්_රියාවලිය_අගය.stdin.write(දත්ත)
                ක්_රියාවලිය_අගය.stdin.flush()
            def කවචය(පෙළ):
                print(පෙළ, flush=True)
                처음 = len(ලොගය_පේළිය)
                ඊමේල්((පෙළ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as පාලකය_අගය:
                පාලකය_අගය.settimeout(10)
                පාලකය_අගය.connect(str(පාලකය_පෙත))
                දහර_අගය = පාලකය_අගය.makefile('rwb')
                json.loads(දහර_අගය.readline())
                def 요청(උපදෙස_අගය, විස්තාරක=None):
                    දත්ත = {'execute': උපදෙස_අගය}
                    if විස්තාරක is not None:
                        දත්ත['arguments'] = විස්තාරක
                    දහර_අගය.write((json.dumps(දත්ත) + '\n').encode())
                    දහර_අගය.flush()
                    while True:
                        පිළිතුරු_දෙන්න = json.loads(දහර_අගය.readline())
                        if 'error' in පිළිතුරු_දෙන්න:
                            raise AssertionError(පිළිතුරු_දෙන්න)
                        if 'return' in පිළිතුරු_දෙන්න:
                            return පිළිතුරු_දෙන්න['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                වාර්තාව_අගය['shell_cpu'] = 권한읽기()
                assert 'EL1h' in වාර්තාව_අගය['shell_cpu'], වාර්තාව_අගය['shell_cpu']
                වාර්තාව_අගය['initial_ps'] = කවචය('ps')
                assert 'kernel/shell' in වාර්තාව_අගය['initial_ps']
                වාර්තාව_අගය['ipconfig'] = කවචය('ipconfig')
                assert 'inet 10.0.2.15' in වාර්තාව_අගය['ipconfig']
                වාර්තාව_අගය['gateway_ping'] = කවචය('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in වාර්තාව_අගය['gateway_ping']
                assert 'FTP listening' in කවචය('ftpd start')
                with ftplib.FTP() as මාරුව_අගය:
                    මාරුව_අගය.encoding = 'utf-8'
                    මාරුව_අගය.connect('127.0.0.4', 파일접속번호, timeout=20)
                    මාරුව_අගය.login()
                    for නම in මූලය_ගොනු:
                        මාරුව_අගය.storbinary('STOR ' + නම + '.class', io.BytesIO((출력 / (නම + '.class')).read_bytes()))
                처음 = len(ලොගය_පේළිය)
                ඊමේල්('java අවසරය_චෙක්පත\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    වාර්තාව_අගය['java_cpu'] = 권한읽기()
                    if 'EL0t' in වාර්තාව_අගය['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in වාර්තාව_අගය['java_cpu'], වාර්තාව_අගය['java_cpu']
                받기(처음=처음)
                වාර්තාව_අගය['after_exit_ps'] = කවචය('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', වාර්තාව_අගය['after_exit_ps'])
                වාර්තාව_අගය['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as සමානයා_අගය:
                    පෙළ = කවචය('java ජාලය_චෙක්පත {} {}'.format(සමානයා_අගය.සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට, සමානයා_අගය.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in පෙළ and 'exit 0' in පෙළ, පෙළ
                    assert සමානයා_අගය.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, සමානයා_අගය.수신됨
                    assert not සමානයා_අගය.오류들, සමානයා_අගය.오류들
                    වාර්තාව_අගය['outbound_peers'] = {종류: දත්ත.decode() for 종류, දත්ත in සමානයා_අගය.수신됨.items()}
                처음 = len(ලොගය_පේළිය)
                ඊමේල්('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට), timeout=5) as සමානයා_අගය:
                    සමානයා_අගය.sendall(b'A')
                    assert සමානයා_අගය.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as සමානයා_අගය:
                    සමානයා_අගය.settimeout(5)
                    සමානයා_අගය.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert සමානයා_අගය.recvfrom(64)[0] == b'UDP-IN'
                පෙළ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in පෙළ and 'exit 0' in පෙළ, පෙළ
                වාර්තාව_අගය['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in කවචය('terminal')
                කවචය('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ලොගය_පේළිය)
                ඊමේල්('java 창예제\n'.encode())
                받기('GUI 예제 පිළියෙල_කරන්න: 창예제\r\n'.encode(), 처음)
                처음 = len(ලොගය_පේළිය)
                ඊමේල්(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                වාර්තාව_අගය['suspended_java_ps'] = කවචය('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', වාර්තාව_අගය['suspended_java_ps']), වාර්තාව_අගය['suspended_java_ps']
                වාර්තාව_අගය['top'] = කවචය('top -n 1')
                assert 'java 창예제' in වාර්තාව_අගය['top'] and 'kernel/shell' in වාර්තාව_අගය['top']
                වාර්තාව_අගය['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                වාර්තාව_අගය['network_trace'] = පාලම_අගය.추적기록
                assert not පාලම_අගය.දෝෂය, පාලම_අගය.දෝෂය
                ඊමේල්(b'poweroff\n')
                assert ක්_රියාවලිය_අගය.wait(timeout=15) == 0
                වාර්තාව_අගය['passed'] = True
            තෝරන්න_අයිතමය.close()
    except Exception as දෝෂය:
        වාර්තාව_අගය['error'] = str(දෝෂය)
        raise
    finally:
        if ක්_රියාවලිය_අගය is not None and ක්_රියාවලිය_අගය.poll() is None:
            ක්_රියාවලිය_අගය.terminate()
            try:
                ක්_රියාවලිය_අගය.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ක්_රියාවලිය_අගය.kill()
                ක්_රියාවලිය_අගය.wait()
        (출력 / 'serial.log').write_bytes(ලොගය_පේළිය)
        (출력 / 'report.json').write_text(json.dumps(වාර්තාව_අගය, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({යතුර_අගය: වාර්තාව_අගය[යතුර_අගය] for යතුර_අගය in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ක්_රියාත්මක_කරන්න_2()
