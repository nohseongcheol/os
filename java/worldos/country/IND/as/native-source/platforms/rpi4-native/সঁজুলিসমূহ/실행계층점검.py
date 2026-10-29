#!/usr/bin/env python3
"""QEMU의 প্ৰকৃত_ডাটা CPU অনুমতি_মান, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from নিষ্পাদন_আদেশ import 기준, কমান্ড
from নেটৱৰ্ক_ব্ৰীজ import নেটৱৰ্ক_ব্ৰীজ
from 되돌림시험서버 import 되돌림시험서버


def সঞ্চালন():
    নিৰ্গম = 기준 / 'build/verification/execution-network-review'
    নিৰ্গম.mkdir(parents=True, exist_ok=True)
    ৰিপ_ৰ্ট_মান = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    উৎস_ফাইলসমূহ = {
        'অনুমতি_পৰীক্ষণ': '''public class অনুমতি_পৰীক্ষণ {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'নেটৱৰ্ক_পৰীক্ষণ': '''import java.net.*;
public class নেটৱৰ্ক_পৰীক্ষণ {
 public static void main(String[] 인수) throws Exception {
  Socket সংযোগ_স্থাপনা = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  সংযোগ_স্থাপনা.setSoTimeout(3000);
  byte[] টেক্সট = "TCP 한글\\n".getBytes("UTF-8");
  সংযোগ_স্থাপনা.getOutputStream().write(টেক্সট);
  for (int স্থান_সলনি_কৰক_ইনডেক্স = 0; স্থান_সলনি_কৰক_ইনডেক্স < টেক্সট.length; স্থান_সলনি_কৰক_ইনডেক্স++)
   if (সংযোগ_স্থাপনা.getInputStream().read() != (টেক্সট[স্থান_সলনি_কৰক_ইনডেক্স] & 255)) throw new RuntimeException("TCP mismatch");
  সংযোগ_স্থাপনা.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  টেক্সট = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(টেক্সট, টেক্সট.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] প্ৰত্যুত্তৰ_দিয়ক = new byte[64]; DatagramPacket 전문 = new DatagramPacket(প্ৰত্যুত্তৰ_দিয়ক, প্ৰত্যুত্তৰ_দিয়ক.length);
  종단.receive(전문);
  if (전문.getLength() != টেক্সট.length) throw new RuntimeException("UDP length");
  for (int স্থান_সলনি_কৰক_ইনডেক্স = 0; স্থান_সলনি_কৰক_ইনডেক্স < টেক্সট.length; স্থান_সলনি_কৰক_ইনডেক্স++)
   if (প্ৰত্যুত্তৰ_দিয়ক[স্থান_সলনি_কৰক_ইনডেক্স] != টেক্সট[স্থান_সলনি_কৰক_ইনডেক্স]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket ছাৰ্ভাৰ_মান = new ServerSocket(9300); ছাৰ্ভাৰ_মান.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket সংযোগ_স্থাপনা = ছাৰ্ভাৰ_মান.accept(); সংযোগ_স্থাপনা.setSoTimeout(5000);
  সংযোগ_স্থাপনা.getOutputStream().write(সংযোগ_স্থাপনা.getInputStream().read() + 1);
  সংযোগ_স্থাপনা.close(); ছাৰ্ভাৰ_মান.close();
  byte[] ডাটা = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ডাটা, ডাটা.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for নাম, উৎস in উৎস_ফাইলসমূহ.items():
        (নিৰ্গম / (নাম + '.java')).write_text(উৎস, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(নিৰ্গম)] +
                          [str(নিৰ্গম / (নাম + '.java')) for নাম in উৎস_ফাইলসমূহ])
    লগ_শাৰী = bytearray()
    def 빈접속번호(প্ৰকাৰ_বর্গ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, প্ৰকাৰ_বর্গ) as অনুসন্ধান_মান:
            অনুসন্ধান_মান.bind(('127.0.0.4', 0))
            return অনুসন্ধান_মান.getsockname()[1]
    파일접속번호, প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    প্ৰক্ৰিয়া_মান = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, নেটৱৰ্ক_ব্ৰীজ(
                파일접속번호, ['tcp:{}:9300'.format(প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট), 'udp:{}:9301'.format(전문접속번호)],
                কেপচাৰ=True, হ_ষ্ট_ঠিকনা='127.0.0.4') as ব্ৰীজ_মান:
            নিয়ন্ত্রণ_পথ = Path(임시) / 'qmp.sock'
            প্ৰক্ৰিয়া_মান = subprocess.Popen(কমান্ড() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(নিয়ন্ত্রণ_পথ)] + ব্ৰীজ_মান.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            পচন্দ_কৰক_আইটেম = selectors.DefaultSelector()
            পচন্দ_কৰক_আইটেম.register(প্ৰক্ৰিয়া_মান.stdout, selectors.EVENT_READ)
            def 받기(শ্ব_মান=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while শ্ব_মান not in লগ_শাৰী[처음:]:
                    if time.monotonic() > 끝 or প্ৰক্ৰিয়া_মান.poll() is not None:
                        raise AssertionError('Missing ' + repr(শ্ব_মান) + '\n' + লগ_শাৰী[처음:].decode('utf-8', 'replace'))
                    for কী_মান, _ in পচন্দ_কৰক_আইটেম.select(.05):
                        조각 = কী_মান.fileobj.read(65536)
                        if 조각:
                            লগ_শাৰী.extend(조각)
                return লগ_শাৰী[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ই_মেইল_কৰক(ডাটা):
                প্ৰক্ৰিয়া_মান.stdin.write(ডাটা)
                প্ৰক্ৰিয়া_মান.stdin.flush()
            def শ্বেল(টেক্সট):
                print(টেক্সট, flush=True)
                처음 = len(লগ_শাৰী)
                ই_মেইল_কৰক((টেক্সট + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as নিয়ন্ত্রণ_মান:
                নিয়ন্ত্রণ_মান.settimeout(10)
                নিয়ন্ত্রণ_মান.connect(str(নিয়ন্ত্রণ_পথ))
                ষ্ট্ৰিম_মান = নিয়ন্ত্রণ_মান.makefile('rwb')
                json.loads(ষ্ট্ৰিম_মান.readline())
                def 요청(নিৰ্দেশনা_মান, 인수=None):
                    ডাটা = {'execute': নিৰ্দেশনা_মান}
                    if 인수 is not None:
                        ডাটা['arguments'] = 인수
                    ষ্ট্ৰিম_মান.write((json.dumps(ডাটা) + '\n').encode())
                    ষ্ট্ৰিম_মান.flush()
                    while True:
                        প্ৰত্যুত্তৰ_দিয়ক = json.loads(ষ্ট্ৰিম_মান.readline())
                        if 'error' in প্ৰত্যুত্তৰ_দিয়ক:
                            raise AssertionError(প্ৰত্যুত্তৰ_দিয়ক)
                        if 'return' in প্ৰত্যুত্তৰ_দিয়ক:
                            return প্ৰত্যুত্তৰ_দিয়ক['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ৰিপ_ৰ্ট_মান['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ৰিপ_ৰ্ট_মান['shell_cpu'], ৰিপ_ৰ্ট_মান['shell_cpu']
                ৰিপ_ৰ্ট_মান['initial_ps'] = শ্বেল('ps')
                assert 'kernel/shell' in ৰিপ_ৰ্ট_মান['initial_ps']
                ৰিপ_ৰ্ট_মান['ipconfig'] = শ্বেল('ipconfig')
                assert 'inet 10.0.2.15' in ৰিপ_ৰ্ট_মান['ipconfig']
                ৰিপ_ৰ্ট_মান['gateway_ping'] = শ্বেল('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ৰিপ_ৰ্ট_মান['gateway_ping']
                assert 'FTP listening' in শ্বেল('ftpd start')
                with ftplib.FTP() as স্থানান্তৰণ_মান:
                    স্থানান্তৰণ_মান.encoding = 'utf-8'
                    স্থানান্তৰণ_মান.connect('127.0.0.4', 파일접속번호, timeout=20)
                    স্থানান্তৰণ_মান.login()
                    for নাম in উৎস_ফাইলসমূহ:
                        স্থানান্তৰণ_মান.storbinary('STOR ' + নাম + '.class', io.BytesIO((নিৰ্গম / (নাম + '.class')).read_bytes()))
                처음 = len(লগ_শাৰী)
                ই_মেইল_কৰক('java অনুমতি_পৰীক্ষণ\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ৰিপ_ৰ্ট_মান['java_cpu'] = 권한읽기()
                    if 'EL0t' in ৰিপ_ৰ্ট_মান['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ৰিপ_ৰ্ট_মান['java_cpu'], ৰিপ_ৰ্ট_মান['java_cpu']
                받기(처음=처음)
                ৰিপ_ৰ্ট_মান['after_exit_ps'] = শ্বেল('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ৰিপ_ৰ্ট_মান['after_exit_ps'])
                ৰিপ_ৰ্ট_মান['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as পীয়েৰ_মান:
                    টেক্সট = শ্বেল('java নেটৱৰ্ক_পৰীক্ষণ {} {}'.format(পীয়েৰ_মান.প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট, পীয়েৰ_মান.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
                    assert পীয়েৰ_মান.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, পীয়েৰ_মান.수신됨
                    assert not পীয়েৰ_মান.오류들, পীয়েৰ_মান.오류들
                    ৰিপ_ৰ্ট_মান['outbound_peers'] = {종류: ডাটা.decode() for 종류, ডাটা in পীয়েৰ_মান.수신됨.items()}
                처음 = len(লগ_শাৰী)
                ই_মেইল_কৰক('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট), timeout=5) as পীয়েৰ_মান:
                    পীয়েৰ_মান.sendall(b'A')
                    assert পীয়েৰ_মান.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as পীয়েৰ_মান:
                    পীয়েৰ_মান.settimeout(5)
                    পীয়েৰ_মান.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert পীয়েৰ_মান.recvfrom(64)[0] == b'UDP-IN'
                টেক্সট = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
                ৰিপ_ৰ্ট_মান['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in শ্বেল('terminal')
                শ্বেল('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(লগ_শাৰী)
                ই_মেইল_কৰক('java 창예제\n'.encode())
                받기('GUI 예제 প্ৰস্তুত_কৰক: 창예제\r\n'.encode(), 처음)
                처음 = len(লগ_শাৰী)
                ই_মেইল_কৰক(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ৰিপ_ৰ্ট_মান['suspended_java_ps'] = শ্বেল('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ৰিপ_ৰ্ট_মান['suspended_java_ps']), ৰিপ_ৰ্ট_মান['suspended_java_ps']
                ৰিপ_ৰ্ট_মান['top'] = শ্বেল('top -n 1')
                assert 'java 창예제' in ৰিপ_ৰ্ট_মান['top'] and 'kernel/shell' in ৰিপ_ৰ্ট_মান['top']
                ৰিপ_ৰ্ট_মান['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ৰিপ_ৰ্ট_মান['network_trace'] = ব্ৰীজ_মান.ট্ৰেচ_লগ
                assert not ব্ৰীজ_মান.ত্ৰুটি, ব্ৰীজ_মান.ত্ৰুটি
                ই_মেইল_কৰক(b'poweroff\n')
                assert প্ৰক্ৰিয়া_মান.wait(timeout=15) == 0
                ৰিপ_ৰ্ট_মান['passed'] = True
            পচন্দ_কৰক_আইটেম.close()
    except Exception as ত্ৰুটি:
        ৰিপ_ৰ্ট_মান['error'] = str(ত্ৰুটি)
        raise
    finally:
        if প্ৰক্ৰিয়া_মান is not None and প্ৰক্ৰিয়া_মান.poll() is None:
            প্ৰক্ৰিয়া_মান.terminate()
            try:
                প্ৰক্ৰিয়া_মান.wait(timeout=10)
            except subprocess.TimeoutExpired:
                প্ৰক্ৰিয়া_মান.kill()
                প্ৰক্ৰিয়া_মান.wait()
        (নিৰ্গম / 'serial.log').write_bytes(লগ_শাৰী)
        (নিৰ্গম / 'report.json').write_text(json.dumps(ৰিপ_ৰ্ট_মান, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({কী_মান: ৰিপ_ৰ্ট_মান[কী_মান] for কী_মান in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    সঞ্চালন()
