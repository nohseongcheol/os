#!/usr/bin/env python3
"""QEMU의 প্রকৃত_ডাটা CPU অনুমতি_মান, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from কার্যকর_করুন_আদেশ import প্রকল্প_মূল, আদেশ
from নেটওয়ার্ক_ব্রিজ import নেটওয়ার্ক_ব্রিজ
from 되돌림시험서버 import 되돌림시험서버


def চালনা():
    নির্গম = প্রকল্প_মূল / 'build/verification/execution-network-review'
    নির্গম.mkdir(parents=True, exist_ok=True)
    রিপোর্ট_মান = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((প্রকল্প_মূল / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    উত্স_ফাইলগুলি = {
        'অনুমতি_চেক': '''public class অনুমতি_চেক {
 public static void main(String[] আর্গুমেন্ট_তালিকা) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'নেটওয়ার্ক_চেক': '''import java.net.*;
public class নেটওয়ার্ক_চেক {
 public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception {
  Socket সংযোগ_স্থাপনা = new Socket("10.0.2.2", Integer.parseInt(আর্গুমেন্ট_তালিকা[0]));
  সংযোগ_স্থাপনা.setSoTimeout(3000);
  byte[] পাঠ = "TCP 한글\\n".getBytes("UTF-8");
  সংযোগ_স্থাপনা.getOutputStream().write(পাঠ);
  for (int পদ_সূচি = 0; পদ_সূচি < পাঠ.length; পদ_সূচি++)
   if (সংযোগ_স্থাপনা.getInputStream().read() != (পাঠ[পদ_সূচি] & 255)) throw new RuntimeException("TCP mismatch");
  সংযোগ_স্থাপনা.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  পাঠ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(পাঠ, পাঠ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(আর্গুমেন্ট_তালিকা[1])));
  byte[] উত্তর_দিন = new byte[64]; DatagramPacket 전문 = new DatagramPacket(উত্তর_দিন, উত্তর_দিন.length);
  종단.receive(전문);
  if (전문.getLength() != পাঠ.length) throw new RuntimeException("UDP length");
  for (int পদ_সূচি = 0; পদ_সূচি < পাঠ.length; পদ_সূচি++)
   if (উত্তর_দিন[পদ_সূচি] != পাঠ[পদ_সূচি]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception {
  ServerSocket সার্ভার_মান = new ServerSocket(9300); সার্ভার_মান.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket সংযোগ_স্থাপনা = সার্ভার_মান.accept(); সংযোগ_স্থাপনা.setSoTimeout(5000);
  সংযোগ_স্থাপনা.getOutputStream().write(সংযোগ_স্থাপনা.getInputStream().read() + 1);
  সংযোগ_স্থাপনা.close(); সার্ভার_মান.close();
  byte[] ডাটা = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ডাটা, ডাটা.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for নাম, উৎস_নথি in উত্স_ফাইলগুলি.items():
        (নির্গম / (নাম + '.java')).write_text(উৎস_নথি, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(নির্গম)] +
                          [str(নির্গম / (নাম + '.java')) for নাম in উত্স_ফাইলগুলি])
    লগ_সারি = bytearray()
    def খালি_পোর্ট_নম্বর(টাইপ_করুন_বিভাগ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, টাইপ_করুন_বিভাগ) as দেখুন_মান:
            দেখুন_মান.bind(('127.0.0.4', 0))
            return দেখুন_মান.getsockname()[1]
    ফাইল_পোর্ট_নম্বর, ট্রান্সমিশন_কন্ট্রোল_প্রটোকল_পোর্ট, 전문접속번호 = খালি_পোর্ট_নম্বর(), খালি_পোর্ট_নম্বর(), খালি_পোর্ট_নম্বর(socket.SOCK_DGRAM)
    প্রসেসর_মান = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, নেটওয়ার্ক_ব্রিজ(
                ফাইল_পোর্ট_নম্বর, ['tcp:{}:9300'.format(ট্রান্সমিশন_কন্ট্রোল_প্রটোকল_পোর্ট), 'udp:{}:9301'.format(전문접속번호)],
                ক্যাপচার=True, হোস্ট_ইমেইল='127.0.0.4') as ব্রিজ_মান:
            নিয়ন্ত্রণ_পথ = Path(임시) / 'qmp.sock'
            প্রসেসর_মান = subprocess.Popen(আদেশ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(নিয়ন্ত্রণ_পথ)] + ব্রিজ_মান.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            চয়ন_করা_দফা = selectors.DefaultSelector()
            চয়ন_করা_দফা.register(প্রসেসর_মান.stdout, selectors.EVENT_READ)
            def 받기(শো_মান=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while শো_মান not in লগ_সারি[처음:]:
                    if time.monotonic() > 끝 or প্রসেসর_মান.poll() is not None:
                        raise AssertionError('Missing ' + repr(শো_মান) + '\n' + লগ_সারি[처음:].decode('utf-8', 'replace'))
                    for কী_মান, _ in চয়ন_করা_দফা.select(.05):
                        조각 = কী_মান.fileobj.read(65536)
                        if 조각:
                            লগ_সারি.extend(조각)
                return লগ_সারি[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def পাঠান(ডাটা):
                প্রসেসর_মান.stdin.write(ডাটা)
                প্রসেসর_মান.stdin.flush()
            def শেল(পাঠ):
                print(পাঠ, flush=True)
                처음 = len(লগ_সারি)
                পাঠান((পাঠ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as নিয়ন্ত্রণ_মান:
                নিয়ন্ত্রণ_মান.settimeout(10)
                নিয়ন্ত্রণ_মান.connect(str(নিয়ন্ত্রণ_পথ))
                প্রবাহ_মান = নিয়ন্ত্রণ_মান.makefile('rwb')
                json.loads(প্রবাহ_মান.readline())
                def 요청(নির্দেশ_মান, আর্গুমেন্ট_তালিকা=None):
                    ডাটা = {'execute': নির্দেশ_মান}
                    if আর্গুমেন্ট_তালিকা is not None:
                        ডাটা['arguments'] = আর্গুমেন্ট_তালিকা
                    প্রবাহ_মান.write((json.dumps(ডাটা) + '\n').encode())
                    প্রবাহ_মান.flush()
                    while True:
                        উত্তর_দিন = json.loads(প্রবাহ_মান.readline())
                        if 'error' in উত্তর_দিন:
                            raise AssertionError(উত্তর_দিন)
                        if 'return' in উত্তর_দিন:
                            return উত্তর_দিন['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                রিপোর্ট_মান['shell_cpu'] = 권한읽기()
                assert 'EL1h' in রিপোর্ট_মান['shell_cpu'], রিপোর্ট_মান['shell_cpu']
                রিপোর্ট_মান['initial_ps'] = শেল('ps')
                assert 'kernel/shell' in রিপোর্ট_মান['initial_ps']
                রিপোর্ট_মান['ipconfig'] = শেল('ipconfig')
                assert 'inet 10.0.2.15' in রিপোর্ট_মান['ipconfig']
                রিপোর্ট_মান['gateway_ping'] = শেল('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in রিপোর্ট_মান['gateway_ping']
                assert 'FTP listening' in শেল('ftpd start')
                with ftplib.FTP() as স্থানান্তর_মান:
                    স্থানান্তর_মান.encoding = 'utf-8'
                    স্থানান্তর_মান.connect('127.0.0.4', ফাইল_পোর্ট_নম্বর, timeout=20)
                    স্থানান্তর_মান.login()
                    for নাম in উত্স_ফাইলগুলি:
                        স্থানান্তর_মান.storbinary('STOR ' + নাম + '.class', io.BytesIO((নির্গম / (নাম + '.class')).read_bytes()))
                처음 = len(লগ_সারি)
                পাঠান('java অনুমতি_চেক\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    রিপোর্ট_মান['java_cpu'] = 권한읽기()
                    if 'EL0t' in রিপোর্ট_মান['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in রিপোর্ট_মান['java_cpu'], রিপোর্ট_মান['java_cpu']
                받기(처음=처음)
                রিপোর্ট_মান['after_exit_ps'] = শেল('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', রিপোর্ট_মান['after_exit_ps'])
                রিপোর্ট_মান['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as পিয়ার_মান:
                    পাঠ = শেল('java নেটওয়ার্ক_চেক {} {}'.format(পিয়ার_মান.ট্রান্সমিশন_কন্ট্রোল_প্রটোকল_পোর্ট, পিয়ার_মান.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in পাঠ and 'exit 0' in পাঠ, পাঠ
                    assert পিয়ার_মান.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, পিয়ার_মান.수신됨
                    assert not পিয়ার_মান.오류들, পিয়ার_মান.오류들
                    রিপোর্ট_মান['outbound_peers'] = {종류: ডাটা.decode() for 종류, ডাটা in পিয়ার_মান.수신됨.items()}
                처음 = len(লগ_সারি)
                পাঠান('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ট্রান্সমিশন_কন্ট্রোল_প্রটোকল_পোর্ট), timeout=5) as পিয়ার_মান:
                    পিয়ার_মান.sendall(b'A')
                    assert পিয়ার_মান.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as পিয়ার_মান:
                    পিয়ার_মান.settimeout(5)
                    পিয়ার_মান.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert পিয়ার_মান.recvfrom(64)[0] == b'UDP-IN'
                পাঠ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in পাঠ and 'exit 0' in পাঠ, পাঠ
                রিপোর্ট_মান['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in শেল('terminal')
                শেল('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(লগ_সারি)
                পাঠান('java জানালানমুনা\n'.encode())
                받기('GUI 예제 প্রস্তুত_করুন: জানালানমুনা\r\n'.encode(), 처음)
                처음 = len(লগ_সারি)
                পাঠান(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                রিপোর্ট_মান['suspended_java_ps'] = শেল('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java জানালানমুনা', রিপোর্ট_মান['suspended_java_ps']), রিপোর্ট_মান['suspended_java_ps']
                রিপোর্ট_মান['top'] = শেল('top -n 1')
                assert 'java জানালানমুনা' in রিপোর্ট_মান['top'] and 'kernel/shell' in রিপোর্ট_মান['top']
                রিপোর্ট_মান['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                রিপোর্ট_মান['network_trace'] = ব্রিজ_মান.ট্রেস_লগ
                assert not ব্রিজ_মান.ত্রুটি, ব্রিজ_মান.ত্রুটি
                পাঠান(b'poweroff\n')
                assert প্রসেসর_মান.wait(timeout=15) == 0
                রিপোর্ট_মান['passed'] = True
            চয়ন_করা_দফা.close()
    except Exception as ত্রুটি:
        রিপোর্ট_মান['error'] = str(ত্রুটি)
        raise
    finally:
        if প্রসেসর_মান is not None and প্রসেসর_মান.poll() is None:
            প্রসেসর_মান.terminate()
            try:
                প্রসেসর_মান.wait(timeout=10)
            except subprocess.TimeoutExpired:
                প্রসেসর_মান.kill()
                প্রসেসর_মান.wait()
        (নির্গম / 'serial.log').write_bytes(লগ_সারি)
        (নির্গম / 'report.json').write_text(json.dumps(রিপোর্ট_মান, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({কী_মান: রিপোর্ট_মান[কী_মান] for কী_মান in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    চালনা()
