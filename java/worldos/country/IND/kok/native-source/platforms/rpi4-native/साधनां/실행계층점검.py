#!/usr/bin/env python3
"""QEMU의 प्रत्यक्ष_डेटा CPU अनुमती_मोल, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from पाळो_दिवचो_आदेश import प्रॉजॅक्ट_रूट, आदेश
from नॅटवर्क_ब्रिज import नॅटवर्क_ब्रिज
from 되돌림시험서버 import 되돌림시험서버


def चलोवप():
    출력 = प्रॉजॅक्ट_रूट / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    अहवाल_मोल = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((प्रॉजॅक्ट_रूट / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    स्त्रोत_फायली = {
        'अनुमती_तपासचें': '''public class अनुमती_तपासचें {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'नॅटवर्क_तपासचें': '''import java.net.*;
public class नॅटवर्क_तपासचें {
 public static void main(String[] 인수) throws Exception {
  Socket कनॅक्ट = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  कनॅक्ट.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  कनॅक्ट.getOutputStream().write(SMS);
  for (int स्थिती_INDEX = 0; स्थिती_INDEX < SMS.length; स्थिती_INDEX++)
   if (कनॅक्ट.getInputStream().read() != (SMS[स्थिती_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  कनॅक्ट.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] जाप_दिवप = new byte[64]; DatagramPacket 전문 = new DatagramPacket(जाप_दिवप, जाप_दिवप.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int स्थिती_INDEX = 0; स्थिती_INDEX < SMS.length; स्थिती_INDEX++)
   if (जाप_दिवप[स्थिती_INDEX] != SMS[स्थिती_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket सर्वर_मोल = new ServerSocket(9300); सर्वर_मोल.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket कनॅक्ट = सर्वर_मोल.accept(); कनॅक्ट.setSoTimeout(5000);
  कनॅक्ट.getOutputStream().write(कनॅक्ट.getInputStream().read() + 1);
  कनॅक्ट.close(); सर्वर_मोल.close();
  byte[] डेटा = new byte[64]; DatagramPacket 전문 = new DatagramPacket(डेटा, डेटा.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for नांव, स्त्रोत in स्त्रोत_फायली.items():
        (출력 / (नांव + '.java')).write_text(स्त्रोत, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (नांव + '.java')) for नांव in स्त्रोत_फायली])
    LOG_नोंद = bytearray()
    def 빈접속번호(TYPE_वर्ग=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_वर्ग) as सोद_मोल:
            सोद_मोल.bind(('127.0.0.4', 0))
            return सोद_मोल.getsockname()[1]
    파일접속번호, TCP_पोर्ट, UDP_पोर्ट = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    प्रक्रिया_मोल = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, नॅटवर्क_ब्रिज(
                파일접속번호, ['tcp:{}:9300'.format(TCP_पोर्ट), 'udp:{}:9301'.format(UDP_पोर्ट)],
                कॅप्चर=True, येजमान_नामो='127.0.0.4') as ब्रिज_मोल:
            नियंत्रण_पाथ = Path(임시) / 'qmp.sock'
            प्रक्रिया_मोल = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(नियंत्रण_पाथ)] + ब्रिज_मोल.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_आयटम = selectors.DefaultSelector()
            CHOOSE_आयटम.register(प्रक्रिया_मोल.stdout, selectors.EVENT_READ)
            def 받기(शो_मोल=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while शो_मोल not in LOG_नोंद[처음:]:
                    if time.monotonic() > 끝 or प्रक्रिया_मोल.poll() is not None:
                        raise AssertionError('Missing ' + repr(शो_मोल) + '\n' + LOG_नोंद[처음:].decode('utf-8', 'replace'))
                    for की_मोल, _ in CHOOSE_आयटम.select(.05):
                        조각 = की_मोल.fileobj.read(65536)
                        if 조각:
                            LOG_नोंद.extend(조각)
                return LOG_नोंद[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def धाडचें(डेटा):
                प्रक्रिया_मोल.stdin.write(डेटा)
                प्रक्रिया_मोल.stdin.flush()
            def शॅल(SMS):
                print(SMS, flush=True)
                처음 = len(LOG_नोंद)
                धाडचें((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as नियंत्रण_मोल:
                नियंत्रण_मोल.settimeout(10)
                नियंत्रण_मोल.connect(str(नियंत्रण_पाथ))
                Stream_मोल = नियंत्रण_मोल.makefile('rwb')
                json.loads(Stream_मोल.readline())
                def 요청(समजावणी_मोल, 인수=None):
                    डेटा = {'execute': समजावणी_मोल}
                    if 인수 is not None:
                        डेटा['arguments'] = 인수
                    Stream_मोल.write((json.dumps(डेटा) + '\n').encode())
                    Stream_मोल.flush()
                    while True:
                        जाप_दिवप = json.loads(Stream_मोल.readline())
                        if 'error' in जाप_दिवप:
                            raise AssertionError(जाप_दिवप)
                        if 'return' in जाप_दिवप:
                            return जाप_दिवप['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                अहवाल_मोल['shell_cpu'] = 권한읽기()
                assert 'EL1h' in अहवाल_मोल['shell_cpu'], अहवाल_मोल['shell_cpu']
                अहवाल_मोल['initial_ps'] = शॅल('ps')
                assert 'kernel/shell' in अहवाल_मोल['initial_ps']
                अहवाल_मोल['ipconfig'] = शॅल('ipconfig')
                assert 'inet 10.0.2.15' in अहवाल_मोल['ipconfig']
                अहवाल_मोल['gateway_ping'] = शॅल('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in अहवाल_मोल['gateway_ping']
                assert 'FTP listening' in शॅल('ftpd start')
                with ftplib.FTP() as ट्रान्सफर_मोल:
                    ट्रान्सफर_मोल.encoding = 'utf-8'
                    ट्रान्सफर_मोल.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ट्रान्सफर_मोल.login()
                    for नांव in स्त्रोत_फायली:
                        ट्रान्सफर_मोल.storbinary('STOR ' + नांव + '.class', io.BytesIO((출력 / (नांव + '.class')).read_bytes()))
                처음 = len(LOG_नोंद)
                धाडचें('java अनुमती_तपासचें\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    अहवाल_मोल['java_cpu'] = 권한읽기()
                    if 'EL0t' in अहवाल_मोल['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in अहवाल_मोल['java_cpu'], अहवाल_मोल['java_cpu']
                받기(처음=처음)
                अहवाल_मोल['after_exit_ps'] = शॅल('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', अहवाल_मोल['after_exit_ps'])
                अहवाल_मोल['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as पीयर_मोल:
                    SMS = शॅल('java नॅटवर्क_तपासचें {} {}'.format(पीयर_मोल.TCP_पोर्ट, पीयर_मोल.UDP_पोर्ट))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert पीयर_मोल.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, पीयर_मोल.수신됨
                    assert not पीयर_मोल.오류들, पीयर_मोल.오류들
                    अहवाल_मोल['outbound_peers'] = {종류: डेटा.decode() for 종류, डेटा in पीयर_मोल.수신됨.items()}
                처음 = len(LOG_नोंद)
                धाडचें('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_पोर्ट), timeout=5) as पीयर_मोल:
                    पीयर_मोल.sendall(b'A')
                    assert पीयर_मोल.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as पीयर_मोल:
                    पीयर_मोल.settimeout(5)
                    पीयर_मोल.sendto(b'UDP-IN', ('127.0.0.4', UDP_पोर्ट))
                    assert पीयर_मोल.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                अहवाल_मोल['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in शॅल('terminal')
                शॅल('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_नोंद)
                धाडचें('java 창예제\n'.encode())
                받기('GUI 예제 तयार_करचें_9ce364fc: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_नोंद)
                धाडचें(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                अहवाल_मोल['suspended_java_ps'] = शॅल('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', अहवाल_मोल['suspended_java_ps']), अहवाल_मोल['suspended_java_ps']
                अहवाल_मोल['top'] = शॅल('top -n 1')
                assert 'java 창예제' in अहवाल_मोल['top'] and 'kernel/shell' in अहवाल_मोल['top']
                अहवाल_मोल['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                अहवाल_मोल['network_trace'] = ब्रिज_मोल.추적기록
                assert not ब्रिज_मोल.चूक, ब्रिज_मोल.चूक
                धाडचें(b'poweroff\n')
                assert प्रक्रिया_मोल.wait(timeout=15) == 0
                अहवाल_मोल['passed'] = True
            CHOOSE_आयटम.close()
    except Exception as चूक:
        अहवाल_मोल['error'] = str(चूक)
        raise
    finally:
        if प्रक्रिया_मोल is not None and प्रक्रिया_मोल.poll() is None:
            प्रक्रिया_मोल.terminate()
            try:
                प्रक्रिया_मोल.wait(timeout=10)
            except subprocess.TimeoutExpired:
                प्रक्रिया_मोल.kill()
                प्रक्रिया_मोल.wait()
        (출력 / 'serial.log').write_bytes(LOG_नोंद)
        (출력 / 'report.json').write_text(json.dumps(अहवाल_मोल, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({की_मोल: अहवाल_मोल[की_मोल] for की_मोल in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    चलोवप()
