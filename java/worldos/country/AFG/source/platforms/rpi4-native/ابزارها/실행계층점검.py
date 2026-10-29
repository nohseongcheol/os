#!/usr/bin/env python3
"""QEMU의 واقعی_داده_ها CPU مجوز_مقدار, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from اجرا_فرمان import نمایش_دادن_جذر, فرمان
from شبکه_پل import شبکه_پل
from 되돌림시험서버 import 되돌림시험서버


def اجرا_2():
    خروجی = نمایش_دادن_جذر / 'build/verification/execution-network-review'
    خروجی.mkdir(parents=True, exist_ok=True)
    گزارش_مقدار = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    منبع_فایل = {
        'مجوز_بررسی': '''public class مجوز_بررسی {
 public static void main(String[] نشانوندها) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'شبکه_بررسی': '''import java.net.*;
public class شبکه_بررسی {
 public static void main(String[] نشانوندها) throws Exception {
  Socket اتصال = new Socket("10.0.2.2", Integer.parseInt(نشانوندها[0]));
  اتصال.setSoTimeout(3000);
  byte[] متن = "TCP 한글\\n".getBytes("UTF-8");
  اتصال.getOutputStream().write(متن);
  for (int مرتب_کردن_فهرست = 0; مرتب_کردن_فهرست < متن.length; مرتب_کردن_فهرست++)
   if (اتصال.getInputStream().read() != (متن[مرتب_کردن_فهرست] & 255)) throw new RuntimeException("TCP mismatch");
  اتصال.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  متن = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(متن, متن.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(نشانوندها[1])));
  byte[] پاسخ_دادن = new byte[64]; DatagramPacket 전문 = new DatagramPacket(پاسخ_دادن, پاسخ_دادن.length);
  종단.receive(전문);
  if (전문.getLength() != متن.length) throw new RuntimeException("UDP length");
  for (int مرتب_کردن_فهرست = 0; مرتب_کردن_فهرست < متن.length; مرتب_کردن_فهرست++)
   if (پاسخ_دادن[مرتب_کردن_فهرست] != متن[مرتب_کردن_فهرست]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] نشانوندها) throws Exception {
  ServerSocket سرور_مقدار = new ServerSocket(9300); سرور_مقدار.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket اتصال = سرور_مقدار.accept(); اتصال.setSoTimeout(5000);
  اتصال.getOutputStream().write(اتصال.getInputStream().read() + 1);
  اتصال.close(); سرور_مقدار.close();
  byte[] داده_ها = new byte[64]; DatagramPacket 전문 = new DatagramPacket(داده_ها, داده_ها.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for نام, مبداء in منبع_فایل.items():
        (خروجی / (نام + '.java')).write_text(مبداء, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(خروجی)] +
                          [str(خروجی / (نام + '.java')) for نام in منبع_فایل])
    واقعه_نگار_ردیف = bytearray()
    def خالی_شماره_درگاه(تایپ_کردن_دسته=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, تایپ_کردن_دسته) as جستجو_مقدار:
            جستجو_مقدار.bind(('127.0.0.4', 0))
            return جستجو_مقدار.getsockname()[1]
    فایل_شماره_درگاه, پروتکل_کنترل_مخابره_تبدیل, پروتکل_داده_نگار_کاربر_تبدیل = خالی_شماره_درگاه(), خالی_شماره_درگاه(), خالی_شماره_درگاه(socket.SOCK_DGRAM)
    فرآیند_مقدار = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, شبکه_پل(
                فایل_شماره_درگاه, ['tcp:{}:9300'.format(پروتکل_کنترل_مخابره_تبدیل), 'udp:{}:9301'.format(پروتکل_داده_نگار_کاربر_تبدیل)],
                ضبط_کردن=True, میزبان_آدرس='127.0.0.4') as پل_مقدار:
            کنترل_مسیر = Path(임시) / 'qmp.sock'
            فرآیند_مقدار = subprocess.Popen(فرمان() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(کنترل_مسیر)] + پل_مقدار.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            انتخاب_کردن_مورد = selectors.DefaultSelector()
            انتخاب_کردن_مورد.register(فرآیند_مقدار.stdout, selectors.EVENT_READ)
            def 받기(نمایش_مقدار=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while نمایش_مقدار not in واقعه_نگار_ردیف[처음:]:
                    if time.monotonic() > 끝 or فرآیند_مقدار.poll() is not None:
                        raise AssertionError('Missing ' + repr(نمایش_مقدار) + '\n' + واقعه_نگار_ردیف[처음:].decode('utf-8', 'replace'))
                    for کلید_مقدار, _ in انتخاب_کردن_مورد.select(.05):
                        조각 = کلید_مقدار.fileobj.read(65536)
                        if 조각:
                            واقعه_نگار_ردیف.extend(조각)
                return واقعه_نگار_ردیف[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ارسال(داده_ها):
                فرآیند_مقدار.stdin.write(داده_ها)
                فرآیند_مقدار.stdin.flush()
            def واسط(متن):
                print(متن, flush=True)
                처음 = len(واقعه_نگار_ردیف)
                ارسال((متن + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as کنترل_مقدار:
                کنترل_مقدار.settimeout(10)
                کنترل_مقدار.connect(str(کنترل_مسیر))
                جریان_مقدار = کنترل_مقدار.makefile('rwb')
                json.loads(جریان_مقدار.readline())
                def 요청(دستورالعمل_مقدار, نشانوندها=None):
                    داده_ها = {'execute': دستورالعمل_مقدار}
                    if نشانوندها is not None:
                        داده_ها['arguments'] = نشانوندها
                    جریان_مقدار.write((json.dumps(داده_ها) + '\n').encode())
                    جریان_مقدار.flush()
                    while True:
                        پاسخ_دادن = json.loads(جریان_مقدار.readline())
                        if 'error' in پاسخ_دادن:
                            raise AssertionError(پاسخ_دادن)
                        if 'return' in پاسخ_دادن:
                            return پاسخ_دادن['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                گزارش_مقدار['shell_cpu'] = 권한읽기()
                assert 'EL1h' in گزارش_مقدار['shell_cpu'], گزارش_مقدار['shell_cpu']
                گزارش_مقدار['initial_ps'] = واسط('ps')
                assert 'kernel/shell' in گزارش_مقدار['initial_ps']
                گزارش_مقدار['ipconfig'] = واسط('ipconfig')
                assert 'inet 10.0.2.15' in گزارش_مقدار['ipconfig']
                گزارش_مقدار['gateway_ping'] = واسط('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in گزارش_مقدار['gateway_ping']
                assert 'FTP listening' in واسط('ftpd start')
                with ftplib.FTP() as انتقال_مقدار_630ba093:
                    انتقال_مقدار_630ba093.encoding = 'utf-8'
                    انتقال_مقدار_630ba093.connect('127.0.0.4', فایل_شماره_درگاه, timeout=20)
                    انتقال_مقدار_630ba093.login()
                    for نام in منبع_فایل:
                        انتقال_مقدار_630ba093.storbinary('STOR ' + نام + '.class', io.BytesIO((خروجی / (نام + '.class')).read_bytes()))
                처음 = len(واقعه_نگار_ردیف)
                ارسال('java مجوز_بررسی\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    گزارش_مقدار['java_cpu'] = 권한읽기()
                    if 'EL0t' in گزارش_مقدار['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in گزارش_مقدار['java_cpu'], گزارش_مقدار['java_cpu']
                받기(처음=처음)
                گزارش_مقدار['after_exit_ps'] = واسط('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', گزارش_مقدار['after_exit_ps'])
                گزارش_مقدار['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as مشابه_مقدار:
                    متن = واسط('java شبکه_بررسی {} {}'.format(مشابه_مقدار.پروتکل_کنترل_مخابره_تبدیل, مشابه_مقدار.پروتکل_داده_نگار_کاربر_تبدیل))
                    assert 'OUTBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                    assert مشابه_مقدار.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, مشابه_مقدار.수신됨
                    assert not مشابه_مقدار.오류들, مشابه_مقدار.오류들
                    گزارش_مقدار['outbound_peers'] = {종류: داده_ها.decode() for 종류, داده_ها in مشابه_مقدار.수신됨.items()}
                처음 = len(واقعه_نگار_ردیف)
                ارسال('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', پروتکل_کنترل_مخابره_تبدیل), timeout=5) as مشابه_مقدار:
                    مشابه_مقدار.sendall(b'A')
                    assert مشابه_مقدار.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as مشابه_مقدار:
                    مشابه_مقدار.settimeout(5)
                    مشابه_مقدار.sendto(b'UDP-IN', ('127.0.0.4', پروتکل_داده_نگار_کاربر_تبدیل))
                    assert مشابه_مقدار.recvfrom(64)[0] == b'UDP-IN'
                متن = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in متن and 'exit 0' in متن, متن
                گزارش_مقدار['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in واسط('terminal')
                واسط('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(واقعه_نگار_ردیف)
                ارسال('java نمونهپنجره\n'.encode())
                받기('GUI 예제 آماده_کردن: نمونهپنجره\r\n'.encode(), 처음)
                처음 = len(واقعه_نگار_ردیف)
                ارسال(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                گزارش_مقدار['suspended_java_ps'] = واسط('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java نمونهپنجره', گزارش_مقدار['suspended_java_ps']), گزارش_مقدار['suspended_java_ps']
                گزارش_مقدار['top'] = واسط('top -n 1')
                assert 'java نمونهپنجره' in گزارش_مقدار['top'] and 'kernel/shell' in گزارش_مقدار['top']
                گزارش_مقدار['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                گزارش_مقدار['network_trace'] = پل_مقدار.اثر_ماتریس_واقعه_نگار
                assert not پل_مقدار.خطا, پل_مقدار.خطا
                ارسال(b'poweroff\n')
                assert فرآیند_مقدار.wait(timeout=15) == 0
                گزارش_مقدار['passed'] = True
            انتخاب_کردن_مورد.close()
    except Exception as خطا:
        گزارش_مقدار['error'] = str(خطا)
        raise
    finally:
        if فرآیند_مقدار is not None and فرآیند_مقدار.poll() is None:
            فرآیند_مقدار.terminate()
            try:
                فرآیند_مقدار.wait(timeout=10)
            except subprocess.TimeoutExpired:
                فرآیند_مقدار.kill()
                فرآیند_مقدار.wait()
        (خروجی / 'serial.log').write_bytes(واقعه_نگار_ردیف)
        (خروجی / 'report.json').write_text(json.dumps(گزارش_مقدار, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({کلید_مقدار: گزارش_مقدار[کلید_مقدار] for کلید_مقدار in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    اجرا_2()
