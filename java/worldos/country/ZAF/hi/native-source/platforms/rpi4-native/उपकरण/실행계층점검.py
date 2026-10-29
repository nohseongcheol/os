#!/usr/bin/env python3
"""QEMU의 वास्तविक_डेटा CPU अनुमति_मान, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल, आदेश
from ब्रिज_3de4fe3a import ब्रिज_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def चलाएँ():
    निर्गम = प्रोजेक्ट_करें_मूल / 'build/verification/execution-network-review'
    निर्गम.mkdir(parents=True, exist_ok=True)
    रिपोर्ट_मान = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    स्रोत_फ़ाइलें = {
        'अनुमति_जाँचें': '''public class अनुमति_जाँचें {
 public static void main(String[] तर्क) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'नेटवर्क_जाँचें': '''import java.net.*;
public class नेटवर्क_जाँचें {
 public static void main(String[] तर्क) throws Exception {
  Socket जोड़ना = new Socket("10.0.2.2", Integer.parseInt(तर्क[0]));
  जोड़ना.setSoTimeout(3000);
  byte[] पाठ = "TCP 한글\\n".getBytes("UTF-8");
  जोड़ना.getOutputStream().write(पाठ);
  for (int पद_इंडेक्स = 0; पद_इंडेक्स < पाठ.length; पद_इंडेक्स++)
   if (जोड़ना.getInputStream().read() != (पाठ[पद_इंडेक्स] & 255)) throw new RuntimeException("TCP mismatch");
  जोड़ना.close();
  DatagramSocket एंडपॉइंट = new DatagramSocket(); एंडपॉइंट.setSoTimeout(3000);
  पाठ = "UDP 한글".getBytes("UTF-8");
  एंडपॉइंट.send(new DatagramPacket(पाठ, पाठ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(तर्क[1])));
  byte[] उत्तर = new byte[64]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(उत्तर, उत्तर.length);
  एंडपॉइंट.receive(स्वतंत्रसंदेश);
  if (स्वतंत्रसंदेश.getLength() != पाठ.length) throw new RuntimeException("UDP length");
  for (int पद_इंडेक्स = 0; पद_इंडेक्स < पाठ.length; पद_इंडेक्स++)
   if (उत्तर[पद_इंडेक्स] != पाठ[पद_इंडेक्स]) throw new RuntimeException("UDP mismatch");
  एंडपॉइंट.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] तर्क) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); 서버.setSoTimeout(5000);
  DatagramSocket एंडपॉइंट = new DatagramSocket(9301); एंडपॉइंट.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket जोड़ना = 서버.accept(); जोड़ना.setSoTimeout(5000);
  जोड़ना.getOutputStream().write(जोड़ना.getInputStream().read() + 1);
  जोड़ना.close(); 서버.close();
  byte[] आँकड़े = new byte[64]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(आँकड़े, आँकड़े.length);
  एंडपॉइंट.receive(स्वतंत्रसंदेश); एंडपॉइंट.send(स्वतंत्रसंदेश); एंडपॉइंट.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for नाम, स्रोत in स्रोत_फ़ाइलें.items():
        (निर्गम / (नाम + '.java')).write_text(स्रोत, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(निर्गम)] +
                          [str(निर्गम / (नाम + '.java')) for नाम in स्रोत_फ़ाइलें])
    लॉग_रिकॉर्ड = bytearray()
    def 빈접속번호(लिखें_श्रेणी=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, लिखें_श्रेणी) as खोज_मान:
            खोज_मान.bind(('127.0.0.4', 0))
            return खोज_मान.getsockname()[1]
    फ़ाइल_पोर्ट_संख्या, 연결접속번호, यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    प्रक्रिया_मान = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ब्रिज_3de4fe3a(
                फ़ाइल_पोर्ट_संख्या, ['tcp:{}:9300'.format(연결접속번호), 'udp:{}:9301'.format(यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट)],
                कैप्चर_करें=True, आयोजक_पता='127.0.0.4') as ब्रिज_मान:
            नियंत्रण_पथ = Path(임시) / 'qmp.sock'
            प्रक्रिया_मान = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(नियंत्रण_पथ)] + ब्रिज_मान.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            चुनें_आइटम = selectors.DefaultSelector()
            चुनें_आइटम.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
            def 받기(शो_मान=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while शो_मान not in लॉग_रिकॉर्ड[처음:]:
                    if time.monotonic() > 끝 or प्रक्रिया_मान.poll() is not None:
                        raise AssertionError('Missing ' + repr(शो_मान) + '\n' + लॉग_रिकॉर्ड[처음:].decode('utf-8', 'replace'))
                    for कुंजी_मान, _ in चुनें_आइटम.select(.05):
                        조각 = कुंजी_मान.fileobj.read(65536)
                        if 조각:
                            लॉग_रिकॉर्ड.extend(조각)
                return लॉग_रिकॉर्ड[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def भेजें(आँकड़े):
                प्रक्रिया_मान.stdin.write(आँकड़े)
                प्रक्रिया_मान.stdin.flush()
            def शेल(पाठ):
                print(पाठ, flush=True)
                처음 = len(लॉग_रिकॉर्ड)
                भेजें((पाठ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as नियंत्रण_मान:
                नियंत्रण_मान.settimeout(10)
                नियंत्रण_मान.connect(str(नियंत्रण_पथ))
                स्ट्रीम_मान = नियंत्रण_मान.makefile('rwb')
                json.loads(स्ट्रीम_मान.readline())
                def अनुरोध(명령어, तर्क=None):
                    आँकड़े = {'execute': 명령어}
                    if तर्क is not None:
                        आँकड़े['arguments'] = तर्क
                    स्ट्रीम_मान.write((json.dumps(आँकड़े) + '\n').encode())
                    स्ट्रीम_मान.flush()
                    while True:
                        उत्तर = json.loads(स्ट्रीम_मान.readline())
                        if 'error' in उत्तर:
                            raise AssertionError(उत्तर)
                        if 'return' in उत्तर:
                            return उत्तर['return']
                अनुरोध('qmp_capabilities')
                def पढें_अनुमति():
                    अनुरोध('stop')
                    try:
                        return अनुरोध('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        अनुरोध('cont')
                रिपोर्ट_मान['shell_cpu'] = पढें_अनुमति()
                assert 'EL1h' in रिपोर्ट_मान['shell_cpu'], रिपोर्ट_मान['shell_cpu']
                रिपोर्ट_मान['initial_ps'] = शेल('ps')
                assert 'kernel/shell' in रिपोर्ट_मान['initial_ps']
                रिपोर्ट_मान['ipconfig'] = शेल('ipconfig')
                assert 'inet 10.0.2.15' in रिपोर्ट_मान['ipconfig']
                रिपोर्ट_मान['gateway_ping'] = शेल('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in रिपोर्ट_मान['gateway_ping']
                assert 'FTP listening' in शेल('ftpd start')
                with ftplib.FTP() as हस्तांतरण_मान:
                    हस्तांतरण_मान.encoding = 'utf-8'
                    हस्तांतरण_मान.connect('127.0.0.4', फ़ाइल_पोर्ट_संख्या, timeout=20)
                    हस्तांतरण_मान.login()
                    for नाम in स्रोत_फ़ाइलें:
                        हस्तांतरण_मान.storbinary('STOR ' + नाम + '.class', io.BytesIO((निर्गम / (नाम + '.class')).read_bytes()))
                처음 = len(लॉग_रिकॉर्ड)
                भेजें('java अनुमति_जाँचें\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    रिपोर्ट_मान['java_cpu'] = पढें_अनुमति()
                    if 'EL0t' in रिपोर्ट_मान['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in रिपोर्ट_मान['java_cpu'], रिपोर्ट_मान['java_cpu']
                받기(처음=처음)
                रिपोर्ट_मान['after_exit_ps'] = शेल('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', रिपोर्ट_मान['after_exit_ps'])
                रिपोर्ट_मान['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as पीअर_मान:
                    पाठ = शेल('java नेटवर्क_जाँचें {} {}'.format(पीअर_मान.연결접속번호, पीअर_मान.यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट))
                    assert 'OUTBOUND_TCP_UDP_PASS' in पाठ and 'exit 0' in पाठ, पाठ
                    assert पीअर_मान.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, पीअर_मान.수신됨
                    assert not पीअर_मान.오류들, पीअर_मान.오류들
                    रिपोर्ट_मान['outbound_peers'] = {종류: आँकड़े.decode() for 종류, आँकड़े in पीअर_मान.수신됨.items()}
                처음 = len(लॉग_रिकॉर्ड)
                भेजें('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', 연결접속번호), timeout=5) as पीअर_मान:
                    पीअर_मान.sendall(b'A')
                    assert पीअर_मान.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as पीअर_मान:
                    पीअर_मान.settimeout(5)
                    पीअर_मान.sendto(b'UDP-IN', ('127.0.0.4', यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट))
                    assert पीअर_मान.recvfrom(64)[0] == b'UDP-IN'
                पाठ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in पाठ and 'exit 0' in पाठ, पाठ
                रिपोर्ट_मान['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in शेल('terminal')
                शेल('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(लॉग_रिकॉर्ड)
                भेजें('java खिड़कीउदाहरण\n'.encode())
                받기('GUI 예제 준비: खिड़कीउदाहरण\r\n'.encode(), 처음)
                처음 = len(लॉग_रिकॉर्ड)
                भेजें(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                रिपोर्ट_मान['suspended_java_ps'] = शेल('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java खिड़कीउदाहरण', रिपोर्ट_मान['suspended_java_ps']), रिपोर्ट_मान['suspended_java_ps']
                रिपोर्ट_मान['top'] = शेल('top -n 1')
                assert 'java खिड़कीउदाहरण' in रिपोर्ट_मान['top'] and 'kernel/shell' in रिपोर्ट_मान['top']
                रिपोर्ट_मान['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                रिपोर्ट_मान['network_trace'] = ब्रिज_मान.ट्रेस_लॉग
                assert not ब्रिज_मान.त्रुटि, ब्रिज_मान.त्रुटि
                भेजें(b'poweroff\n')
                assert प्रक्रिया_मान.wait(timeout=15) == 0
                रिपोर्ट_मान['passed'] = True
            चुनें_आइटम.close()
    except Exception as त्रुटि:
        रिपोर्ट_मान['error'] = str(त्रुटि)
        raise
    finally:
        if प्रक्रिया_मान is not None and प्रक्रिया_मान.poll() is None:
            प्रक्रिया_मान.terminate()
            try:
                प्रक्रिया_मान.wait(timeout=10)
            except subprocess.TimeoutExpired:
                प्रक्रिया_मान.kill()
                प्रक्रिया_मान.wait()
        (निर्गम / 'serial.log').write_bytes(लॉग_रिकॉर्ड)
        (निर्गम / 'report.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({कुंजी_मान: रिपोर्ट_मान[कुंजी_मान] for कुंजी_मान in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    चलाएँ()
