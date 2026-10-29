#!/usr/bin/env python3
"""QEMU의 اصلی_کوائف CPU اجازت_قدر, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from نفاذ_کرو_حکم import 기준, حکم
from نیٹ_ورک_برج import نیٹ_ورک_برج
from 되돌림시험서버 import 되돌림시험서버


def چلاؤ():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    رپورٹ_قدر = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ماخذ_فائلاں = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'نیٹ_ورک_پڑتال': '''import java.net.*;
public class نیٹ_ورک_پڑتال {
 public static void main(String[] 인수) throws Exception {
  Socket جڑو = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  جڑو.setSoTimeout(3000);
  byte[] متن = "TCP 한글\\n".getBytes("UTF-8");
  جڑو.getOutputStream().write(متن);
  for (int 자리 = 0; 자리 < متن.length; 자리++)
   if (جڑو.getInputStream().read() != (متن[자리] & 255)) throw new RuntimeException("TCP mismatch");
  جڑو.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  متن = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(متن, متن.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] جواب_دیوؤ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(جواب_دیوؤ, جواب_دیوؤ.length);
  종단.receive(전문);
  if (전문.getLength() != متن.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < متن.length; 자리++)
   if (جواب_دیوؤ[자리] != متن[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket سرور_قدر = new ServerSocket(9300); سرور_قدر.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket جڑو = سرور_قدر.accept(); جڑو.setSoTimeout(5000);
  جڑو.getOutputStream().write(جڑو.getInputStream().read() + 1);
  جڑو.close(); سرور_قدر.close();
  byte[] کوائف = new byte[64]; DatagramPacket 전문 = new DatagramPacket(کوائف, کوائف.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ناں, ماخذ in ماخذ_فائلاں.items():
        (출력 / (ناں + '.java')).write_text(ماخذ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (ناں + '.java')) for ناں in ماخذ_فائلاں])
    لاگ_صف = bytearray()
    def 빈접속번호(ٹائپ_کرو_زمرہ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ٹائپ_کرو_زمرہ) as تلاش_قدر:
            تلاش_قدر.bind(('127.0.0.4', 0))
            return تلاش_قدر.getsockname()[1]
    파일접속번호, ٹرانسمشن_کنٹرول_پروٹوکول_دہانہ, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    عمل_قدر = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, نیٹ_ورک_برج(
                파일접속번호, ['tcp:{}:9300'.format(ٹرانسمشن_کنٹرول_پروٹوکول_دہانہ), 'udp:{}:9301'.format(전문접속번호)],
                کھیچو=True, مہمان_پتا='127.0.0.4') as برج_قدر:
            کنٹرول_راہ = Path(임시) / 'qmp.sock'
            عمل_قدر = subprocess.Popen(حکم() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(کنٹرول_راہ)] + برج_قدر.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            انتخاب_کرو_شے = selectors.DefaultSelector()
            انتخاب_کرو_شے.register(عمل_قدر.stdout, selectors.EVENT_READ)
            def 받기(نمایش_کرو_قدر=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while نمایش_کرو_قدر not in لاگ_صف[처음:]:
                    if time.monotonic() > 끝 or عمل_قدر.poll() is not None:
                        raise AssertionError('Missing ' + repr(نمایش_کرو_قدر) + '\n' + لاگ_صف[처음:].decode('utf-8', 'replace'))
                    for کلید_قدر, _ in انتخاب_کرو_شے.select(.05):
                        조각 = کلید_قدر.fileobj.read(65536)
                        if 조각:
                            لاگ_صف.extend(조각)
                return لاگ_صف[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def بھیجو(کوائف):
                عمل_قدر.stdin.write(کوائف)
                عمل_قدر.stdin.flush()
            def شیل(متن):
                print(متن, flush=True)
                처음 = len(لاگ_صف)
                بھیجو((متن + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as کنٹرول_قدر:
                کنٹرول_قدر.settimeout(10)
                کنٹرول_قدر.connect(str(کنٹرول_راہ))
                سٹریم_قدر = کنٹرول_قدر.makefile('rwb')
                json.loads(سٹریم_قدر.readline())
                def 요청(ہدایت_قدر, 인수=None):
                    کوائف = {'execute': ہدایت_قدر}
                    if 인수 is not None:
                        کوائف['arguments'] = 인수
                    سٹریم_قدر.write((json.dumps(کوائف) + '\n').encode())
                    سٹریم_قدر.flush()
                    while True:
                        جواب_دیوؤ = json.loads(سٹریم_قدر.readline())
                        if 'error' in جواب_دیوؤ:
                            raise AssertionError(جواب_دیوؤ)
                        if 'return' in جواب_دیوؤ:
                            return جواب_دیوؤ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                رپورٹ_قدر['shell_cpu'] = 권한읽기()
                assert 'EL1h' in رپورٹ_قدر['shell_cpu'], رپورٹ_قدر['shell_cpu']
                رپورٹ_قدر['initial_ps'] = شیل('ps')
                assert 'kernel/shell' in رپورٹ_قدر['initial_ps']
                رپورٹ_قدر['ipconfig'] = شیل('ipconfig')
                assert 'inet 10.0.2.15' in رپورٹ_قدر['ipconfig']
                رپورٹ_قدر['gateway_ping'] = شیل('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in رپورٹ_قدر['gateway_ping']
                assert 'FTP listening' in شیل('ftpd start')
                with ftplib.FTP() as منتقلی_قدر:
                    منتقلی_قدر.encoding = 'utf-8'
                    منتقلی_قدر.connect('127.0.0.4', 파일접속번호, timeout=20)
                    منتقلی_قدر.login()
                    for ناں in ماخذ_فائلاں:
                        منتقلی_قدر.storbinary('STOR ' + ناں + '.class', io.BytesIO((출력 / (ناں + '.class')).read_bytes()))
                처음 = len(لاگ_صف)
                بھیجو('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    رپورٹ_قدر['java_cpu'] = 권한읽기()
                    if 'EL0t' in رپورٹ_قدر['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in رپورٹ_قدر['java_cpu'], رپورٹ_قدر['java_cpu']
                받기(처음=처음)
                رپورٹ_قدر['after_exit_ps'] = شیل('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', رپورٹ_قدر['after_exit_ps'])
                رپورٹ_قدر['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ہم_سر_قدر:
                    متن = شیل('java نیٹ_ورک_پڑتال {} {}'.format(ہم_سر_قدر.ٹرانسمشن_کنٹرول_پروٹوکول_دہانہ, ہم_سر_قدر.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                    assert ہم_سر_قدر.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ہم_سر_قدر.수신됨
                    assert not ہم_سر_قدر.오류들, ہم_سر_قدر.오류들
                    رپورٹ_قدر['outbound_peers'] = {종류: کوائف.decode() for 종류, کوائف in ہم_سر_قدر.수신됨.items()}
                처음 = len(لاگ_صف)
                بھیجو('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ٹرانسمشن_کنٹرول_پروٹوکول_دہانہ), timeout=5) as ہم_سر_قدر:
                    ہم_سر_قدر.sendall(b'A')
                    assert ہم_سر_قدر.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ہم_سر_قدر:
                    ہم_سر_قدر.settimeout(5)
                    ہم_سر_قدر.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ہم_سر_قدر.recvfrom(64)[0] == b'UDP-IN'
                متن = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                رپورٹ_قدر['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in شیل('terminal')
                شیل('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(لاگ_صف)
                بھیجو('java 창예제\n'.encode())
                받기('GUI 예제 تیاری_کرو: 창예제\r\n'.encode(), 처음)
                처음 = len(لاگ_صف)
                بھیجو(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                رپورٹ_قدر['suspended_java_ps'] = شیل('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', رپورٹ_قدر['suspended_java_ps']), رپورٹ_قدر['suspended_java_ps']
                رپورٹ_قدر['top'] = شیل('top -n 1')
                assert 'java 창예제' in رپورٹ_قدر['top'] and 'kernel/shell' in رپورٹ_قدر['top']
                رپورٹ_قدر['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                رپورٹ_قدر['network_trace'] = برج_قدر.추적기록
                assert not برج_قدر.نقص, برج_قدر.نقص
                بھیجو(b'poweroff\n')
                assert عمل_قدر.wait(timeout=15) == 0
                رپورٹ_قدر['passed'] = True
            انتخاب_کرو_شے.close()
    except Exception as نقص:
        رپورٹ_قدر['error'] = str(نقص)
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
        (출력 / 'report.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({کلید_قدر: رپورٹ_قدر[کلید_قدر] for کلید_قدر in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    چلاؤ()
