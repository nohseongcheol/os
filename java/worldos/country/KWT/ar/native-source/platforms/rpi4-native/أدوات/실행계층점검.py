#!/usr/bin/env python3
"""QEMU의 الفعلي_بيانات CPU إذن_قيمة, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ينفذ_أمر import يعرض_جذر, أمر
from جسر_3de4fe3a import جسر_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def تشغيل():
    مخرجات = يعرض_جذر / 'build/verification/execution-network-review'
    مخرجات.mkdir(parents=True, exist_ok=True)
    إبلاغ_قيمة = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((يعرض_جذر / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    مصدر_الملفات = {
        'إذن_شيك': '''public class إذن_شيك {
 public static void main(String[] وسائط) {
  System.out.println("EL0_PROBE_READY");
  int رقم = 0; while (true) { رقم++; }
 }
}''',
        'شبكة_شيك': '''import java.net.*;
public class شبكة_شيك {
 public static void main(String[] وسائط) throws Exception {
  Socket اتصال = new Socket("10.0.2.2", Integer.parseInt(وسائط[0]));
  اتصال.setSoTimeout(3000);
  byte[] نص = "TCP 한글\\n".getBytes("UTF-8");
  اتصال.getOutputStream().write(نص);
  for (int منصب_فهرس = 0; منصب_فهرس < نص.length; منصب_فهرس++)
   if (اتصال.getInputStream().read() != (نص[منصب_فهرس] & 255)) throw new RuntimeException("TCP mismatch");
  اتصال.close();
  DatagramSocket المشارك = new DatagramSocket(); المشارك.setSoTimeout(3000);
  نص = "UDP 한글".getBytes("UTF-8");
  المشارك.send(new DatagramPacket(نص, نص.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(وسائط[1])));
  byte[] رد = new byte[64]; DatagramPacket رزمةمستقلة = new DatagramPacket(رد, رد.length);
  المشارك.receive(رزمةمستقلة);
  if (رزمةمستقلة.getLength() != نص.length) throw new RuntimeException("UDP length");
  for (int منصب_فهرس = 0; منصب_فهرس < نص.length; منصب_فهرس++)
   if (رد[منصب_فهرس] != نص[منصب_فهرس]) throw new RuntimeException("UDP mismatch");
  المشارك.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'يستلم_شيك': '''import java.net.*;
public class يستلم_شيك {
 public static void main(String[] وسائط) throws Exception {
  ServerSocket خادم_قيمة = new ServerSocket(9300); خادم_قيمة.setSoTimeout(5000);
  DatagramSocket المشارك = new DatagramSocket(9301); المشارك.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket اتصال = خادم_قيمة.accept(); اتصال.setSoTimeout(5000);
  اتصال.getOutputStream().write(اتصال.getInputStream().read() + 1);
  اتصال.close(); خادم_قيمة.close();
  byte[] بيانات = new byte[64]; DatagramPacket رزمةمستقلة = new DatagramPacket(بيانات, بيانات.length);
  المشارك.receive(رزمةمستقلة); المشارك.send(رزمةمستقلة); المشارك.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for اسم, مصدر in مصدر_الملفات.items():
        (مخرجات / (اسم + '.java')).write_text(مصدر, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(مخرجات)] +
                          [str(مخرجات / (اسم + '.java')) for اسم in مصدر_الملفات])
    سجل_سجل = bytearray()
    def فارغ_رقم_المنفذ(نوع_فئة=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, نوع_فئة) as بحث_قيمة:
            بحث_قيمة.bind(('127.0.0.4', 0))
            return بحث_قيمة.getsockname()[1]
    منفذ_الملف_رقم, TCP_منفذ, بروتوكول_مخطط_بيانات_المستخدم_منفذ = فارغ_رقم_المنفذ(), فارغ_رقم_المنفذ(), فارغ_رقم_المنفذ(socket.SOCK_DGRAM)
    عملية_قيمة = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, جسر_3de4fe3a(
                منفذ_الملف_رقم, ['tcp:{}:9300'.format(TCP_منفذ), 'udp:{}:9301'.format(بروتوكول_مخطط_بيانات_المستخدم_منفذ)],
                يسجل=True, مضيف_عنوان='127.0.0.4') as جسر_قيمة:
            تحكم_مسار = Path(임시) / 'qmp.sock'
            عملية_قيمة = subprocess.Popen(أمر() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(تحكم_مسار)] + جسر_قيمة.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            يختار_عنصر = selectors.DefaultSelector()
            يختار_عنصر.register(عملية_قيمة.stdout, selectors.EVENT_READ)
            def يستلم(عرض_قيمة_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while عرض_قيمة_487749b8 not in سجل_سجل[처음:]:
                    if time.monotonic() > 끝 or عملية_قيمة.poll() is not None:
                        raise AssertionError('Missing ' + repr(عرض_قيمة_487749b8) + '\n' + سجل_سجل[처음:].decode('utf-8', 'replace'))
                    for مفتاح_قيمة, _ in يختار_عنصر.select(.05):
                        조각 = مفتاح_قيمة.fileobj.read(65536)
                        if 조각:
                            سجل_سجل.extend(조각)
                return سجل_سجل[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def يرسل(بيانات):
                عملية_قيمة.stdin.write(بيانات)
                عملية_قيمة.stdin.flush()
            def 셸(نص):
                print(نص, flush=True)
                처음 = len(سجل_سجل)
                يرسل((نص + '\n').encode())
                return يستلم(처음=처음)
            يستلم()
            with socket.socket(socket.AF_UNIX) as تحكم_قيمة:
                تحكم_قيمة.settimeout(10)
                تحكم_قيمة.connect(str(تحكم_مسار))
                بث_قيمة = تحكم_قيمة.makefile('rwb')
                json.loads(بث_قيمة.readline())
                def طلب(تعليمة_قيمة, وسائط=None):
                    بيانات = {'execute': تعليمة_قيمة}
                    if وسائط is not None:
                        بيانات['arguments'] = وسائط
                    بث_قيمة.write((json.dumps(بيانات) + '\n').encode())
                    بث_قيمة.flush()
                    while True:
                        رد = json.loads(بث_قيمة.readline())
                        if 'error' in رد:
                            raise AssertionError(رد)
                        if 'return' in رد:
                            return رد['return']
                طلب('qmp_capabilities')
                def إذن_القراءة():
                    طلب('stop')
                    try:
                        return طلب('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        طلب('cont')
                إبلاغ_قيمة['shell_cpu'] = إذن_القراءة()
                assert 'EL1h' in إبلاغ_قيمة['shell_cpu'], إبلاغ_قيمة['shell_cpu']
                إبلاغ_قيمة['initial_ps'] = 셸('ps')
                assert 'kernel/shell' in إبلاغ_قيمة['initial_ps']
                إبلاغ_قيمة['ipconfig'] = 셸('ipconfig')
                assert 'inet 10.0.2.15' in إبلاغ_قيمة['ipconfig']
                إبلاغ_قيمة['gateway_ping'] = 셸('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in إبلاغ_قيمة['gateway_ping']
                assert 'FTP listening' in 셸('ftpd start')
                with ftplib.FTP() as نقل_قيمة_630ba093:
                    نقل_قيمة_630ba093.encoding = 'utf-8'
                    نقل_قيمة_630ba093.connect('127.0.0.4', منفذ_الملف_رقم, timeout=20)
                    نقل_قيمة_630ba093.login()
                    for اسم in مصدر_الملفات:
                        نقل_قيمة_630ba093.storbinary('STOR ' + اسم + '.class', io.BytesIO((مخرجات / (اسم + '.class')).read_bytes()))
                처음 = len(سجل_سجل)
                يرسل('java إذن_شيك\n'.encode())
                يستلم(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    إبلاغ_قيمة['java_cpu'] = إذن_القراءة()
                    if 'EL0t' in إبلاغ_قيمة['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in إبلاغ_قيمة['java_cpu'], إبلاغ_قيمة['java_cpu']
                يستلم(처음=처음)
                إبلاغ_قيمة['after_exit_ps'] = 셸('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', إبلاغ_قيمة['after_exit_ps'])
                إبلاغ_قيمة['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as نظير_قيمة:
                    نص = 셸('java شبكة_شيك {} {}'.format(نظير_قيمة.TCP_منفذ, نظير_قيمة.بروتوكول_مخطط_بيانات_المستخدم_منفذ))
                    assert 'OUTBOUND_TCP_UDP_PASS' in نص and 'exit 0' in نص, نص
                    assert نظير_قيمة.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, نظير_قيمة.수신됨
                    assert not نظير_قيمة.오류들, نظير_قيمة.오류들
                    إبلاغ_قيمة['outbound_peers'] = {종류: بيانات.decode() for 종류, بيانات in نظير_قيمة.수신됨.items()}
                처음 = len(سجل_سجل)
                يرسل('java يستلم_شيك\n'.encode())
                يستلم(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_منفذ), timeout=5) as نظير_قيمة:
                    نظير_قيمة.sendall(b'A')
                    assert نظير_قيمة.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as نظير_قيمة:
                    نظير_قيمة.settimeout(5)
                    نظير_قيمة.sendto(b'UDP-IN', ('127.0.0.4', بروتوكول_مخطط_بيانات_المستخدم_منفذ))
                    assert نظير_قيمة.recvfrom(64)[0] == b'UDP-IN'
                نص = يستلم(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in نص and 'exit 0' in نص, نص
                إبلاغ_قيمة['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in 셸('terminal')
                셸('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(سجل_سجل)
                يرسل('java مثالنافذة\n'.encode())
                يستلم('GUI 예제 إعداد: مثالنافذة\r\n'.encode(), 처음)
                처음 = len(سجل_سجل)
                يرسل(bytes([30, 2, 1, 0, 0, 0, 0]))
                يستلم(처음=처음)
                إبلاغ_قيمة['suspended_java_ps'] = 셸('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java مثالنافذة', إبلاغ_قيمة['suspended_java_ps']), إبلاغ_قيمة['suspended_java_ps']
                إبلاغ_قيمة['top'] = 셸('top -n 1')
                assert 'java مثالنافذة' in إبلاغ_قيمة['top'] and 'kernel/shell' in إبلاغ_قيمة['top']
                إبلاغ_قيمة['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                إبلاغ_قيمة['network_trace'] = جسر_قيمة.سجل_التتبّع
                assert not جسر_قيمة.خطأ, جسر_قيمة.خطأ
                يرسل(b'poweroff\n')
                assert عملية_قيمة.wait(timeout=15) == 0
                إبلاغ_قيمة['passed'] = True
            يختار_عنصر.close()
    except Exception as خطأ:
        إبلاغ_قيمة['error'] = str(خطأ)
        raise
    finally:
        if عملية_قيمة is not None and عملية_قيمة.poll() is None:
            عملية_قيمة.terminate()
            try:
                عملية_قيمة.wait(timeout=10)
            except subprocess.TimeoutExpired:
                عملية_قيمة.kill()
                عملية_قيمة.wait()
        (مخرجات / 'serial.log').write_bytes(سجل_سجل)
        (مخرجات / 'report.json').write_text(json.dumps(إبلاغ_قيمة, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({مفتاح_قيمة: إبلاغ_قيمة[مفتاح_قيمة] for مفتاح_قيمة in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    تشغيل()
