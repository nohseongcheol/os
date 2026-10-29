#!/usr/bin/env python3
"""QEMU의 اصل_کوائف CPU اجازت_قدر, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ, حکم
from نیٹ_ورک_برج import نیٹ_ورک_برج
from 되돌림시험서버 import 되돌림시험서버


def چلائیں():
    اخراج_کا_مقام = عکس_ڈالنا_روٹ / 'build/verification/execution-network-review'
    اخراج_کا_مقام.mkdir(parents=True, exist_ok=True)
    رپورٹ_قدر = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ماخذ_فائلیں = {
        'اجازت_پڑتال_کریں': '''public class اجازت_پڑتال_کریں {
 public static void main(String[] دلائل) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'نیٹ_ورک_پڑتال_کریں': '''import java.net.*;
public class نیٹ_ورک_پڑتال_کریں {
 public static void main(String[] دلائل) throws Exception {
  Socket متصل_ہوں = new Socket("10.0.2.2", Integer.parseInt(دلائل[0]));
  متصل_ہوں.setSoTimeout(3000);
  byte[] متن = "TCP 한글\\n".getBytes("UTF-8");
  متصل_ہوں.getOutputStream().write(متن);
  for (int پوزیشن_ٹھیک_کریں_اشاریہ = 0; پوزیشن_ٹھیک_کریں_اشاریہ < متن.length; پوزیشن_ٹھیک_کریں_اشاریہ++)
   if (متصل_ہوں.getInputStream().read() != (متن[پوزیشن_ٹھیک_کریں_اشاریہ] & 255)) throw new RuntimeException("TCP mismatch");
  متصل_ہوں.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  متن = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(متن, متن.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(دلائل[1])));
  byte[] جواب_دیں = new byte[64]; DatagramPacket 전문 = new DatagramPacket(جواب_دیں, جواب_دیں.length);
  종단.receive(전문);
  if (전문.getLength() != متن.length) throw new RuntimeException("UDP length");
  for (int پوزیشن_ٹھیک_کریں_اشاریہ = 0; پوزیشن_ٹھیک_کریں_اشاریہ < متن.length; پوزیشن_ٹھیک_کریں_اشاریہ++)
   if (جواب_دیں[پوزیشن_ٹھیک_کریں_اشاریہ] != متن[پوزیشن_ٹھیک_کریں_اشاریہ]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] دلائل) throws Exception {
  ServerSocket سرور_قدر = new ServerSocket(9300); سرور_قدر.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket متصل_ہوں = سرور_قدر.accept(); متصل_ہوں.setSoTimeout(5000);
  متصل_ہوں.getOutputStream().write(متصل_ہوں.getInputStream().read() + 1);
  متصل_ہوں.close(); سرور_قدر.close();
  byte[] کوائف = new byte[64]; DatagramPacket 전문 = new DatagramPacket(کوائف, کوائف.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for نام, ماخذ_فائل in ماخذ_فائلیں.items():
        (اخراج_کا_مقام / (نام + '.java')).write_text(ماخذ_فائل, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(اخراج_کا_مقام)] +
                          [str(اخراج_کا_مقام / (نام + '.java')) for نام in ماخذ_فائلیں])
    لاگ_صف = bytearray()
    def خالی_دہانہ_نمبر(ٹائپ_کریں_زمرہ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ٹائپ_کریں_زمرہ) as تلاش_قدر:
            تلاش_قدر.bind(('127.0.0.4', 0))
            return تلاش_قدر.getsockname()[1]
    فائل_دہانہ_نمبر, ٹرانسمشن_کنٹرول_پروٹوکول_پورٹ, 전문접속번호 = خالی_دہانہ_نمبر(), خالی_دہانہ_نمبر(), خالی_دہانہ_نمبر(socket.SOCK_DGRAM)
    عمل_قدر = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, نیٹ_ورک_برج(
                فائل_دہانہ_نمبر, ['tcp:{}:9300'.format(ٹرانسمشن_کنٹرول_پروٹوکول_پورٹ), 'udp:{}:9301'.format(전문접속번호)],
                کیپچر_کریں=True, میزبان_پتہ='127.0.0.4') as برج_قدر:
            کنٹرول_راہ = Path(임시) / 'qmp.sock'
            عمل_قدر = subprocess.Popen(حکم() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(کنٹرول_راہ)] + برج_قدر.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            انتخاب_کریں_شے = selectors.DefaultSelector()
            انتخاب_کریں_شے.register(عمل_قدر.stdout, selectors.EVENT_READ)
            def 받기(دکھانا_قدر=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while دکھانا_قدر not in لاگ_صف[처음:]:
                    if time.monotonic() > 끝 or عمل_قدر.poll() is not None:
                        raise AssertionError('Missing ' + repr(دکھانا_قدر) + '\n' + لاگ_صف[처음:].decode('utf-8', 'replace'))
                    for کلید_قدر, _ in انتخاب_کریں_شے.select(.05):
                        조각 = کلید_قدر.fileobj.read(65536)
                        if 조각:
                            لاگ_صف.extend(조각)
                return لاگ_صف[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def بھیجیں(کوائف):
                عمل_قدر.stdin.write(کوائف)
                عمل_قدر.stdin.flush()
            def شیل(متن):
                print(متن, flush=True)
                처음 = len(لاگ_صف)
                بھیجیں((متن + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as کنٹرول_قدر:
                کنٹرول_قدر.settimeout(10)
                کنٹرول_قدر.connect(str(کنٹرول_راہ))
                بہاؤ_قدر = کنٹرول_قدر.makefile('rwb')
                json.loads(بہاؤ_قدر.readline())
                def 요청(ہدایت_قدر, دلائل=None):
                    کوائف = {'execute': ہدایت_قدر}
                    if دلائل is not None:
                        کوائف['arguments'] = دلائل
                    بہاؤ_قدر.write((json.dumps(کوائف) + '\n').encode())
                    بہاؤ_قدر.flush()
                    while True:
                        جواب_دیں = json.loads(بہاؤ_قدر.readline())
                        if 'error' in جواب_دیں:
                            raise AssertionError(جواب_دیں)
                        if 'return' in جواب_دیں:
                            return جواب_دیں['return']
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
                    منتقلی_قدر.connect('127.0.0.4', فائل_دہانہ_نمبر, timeout=20)
                    منتقلی_قدر.login()
                    for نام in ماخذ_فائلیں:
                        منتقلی_قدر.storbinary('STOR ' + نام + '.class', io.BytesIO((اخراج_کا_مقام / (نام + '.class')).read_bytes()))
                처음 = len(لاگ_صف)
                بھیجیں('java اجازت_پڑتال_کریں\n'.encode())
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
                with 되돌림시험서버() as ساتھی_قدر:
                    متن = شیل('java نیٹ_ورک_پڑتال_کریں {} {}'.format(ساتھی_قدر.ٹرانسمشن_کنٹرول_پروٹوکول_پورٹ, ساتھی_قدر.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                    assert ساتھی_قدر.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ساتھی_قدر.수신됨
                    assert not ساتھی_قدر.오류들, ساتھی_قدر.오류들
                    رپورٹ_قدر['outbound_peers'] = {종류: کوائف.decode() for 종류, کوائف in ساتھی_قدر.수신됨.items()}
                처음 = len(لاگ_صف)
                بھیجیں('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ٹرانسمشن_کنٹرول_پروٹوکول_پورٹ), timeout=5) as ساتھی_قدر:
                    ساتھی_قدر.sendall(b'A')
                    assert ساتھی_قدر.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ساتھی_قدر:
                    ساتھی_قدر.settimeout(5)
                    ساتھی_قدر.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ساتھی_قدر.recvfrom(64)[0] == b'UDP-IN'
                متن = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                رپورٹ_قدر['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in شیل('terminal')
                شیل('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(لاگ_صف)
                بھیجیں('java کھڑکیمثال\n'.encode())
                받기('GUI 예제 تیار_کریں: کھڑکیمثال\r\n'.encode(), 처음)
                처음 = len(لاگ_صف)
                بھیجیں(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                رپورٹ_قدر['suspended_java_ps'] = شیل('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java کھڑکیمثال', رپورٹ_قدر['suspended_java_ps']), رپورٹ_قدر['suspended_java_ps']
                رپورٹ_قدر['top'] = شیل('top -n 1')
                assert 'java کھڑکیمثال' in رپورٹ_قدر['top'] and 'kernel/shell' in رپورٹ_قدر['top']
                رپورٹ_قدر['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                رپورٹ_قدر['network_trace'] = برج_قدر.ٹریس_لاگ
                assert not برج_قدر.غلطی, برج_قدر.غلطی
                بھیجیں(b'poweroff\n')
                assert عمل_قدر.wait(timeout=15) == 0
                رپورٹ_قدر['passed'] = True
            انتخاب_کریں_شے.close()
    except Exception as غلطی:
        رپورٹ_قدر['error'] = str(غلطی)
        raise
    finally:
        if عمل_قدر is not None and عمل_قدر.poll() is None:
            عمل_قدر.terminate()
            try:
                عمل_قدر.wait(timeout=10)
            except subprocess.TimeoutExpired:
                عمل_قدر.kill()
                عمل_قدر.wait()
        (اخراج_کا_مقام / 'serial.log').write_bytes(لاگ_صف)
        (اخراج_کا_مقام / 'report.json').write_text(json.dumps(رپورٹ_قدر, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({کلید_قدر: رپورٹ_قدر[کلید_قدر] for کلید_قدر in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    چلائیں()
