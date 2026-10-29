#!/usr/bin/env python3
"""QEMU의 वास्तविक_लगत CPU अनुमति_मान, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from कार्यान्वयन_गर्नुहोस्_आदेश import परियोजना_रूट, आदेश
from सञ्जाल_ब्रिज import सञ्जाल_ब्रिज
from 되돌림시험서버 import 되돌림시험서버


def चलाउनुहोस्():
    출력 = परियोजना_रूट / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    रिपोर्ट_मान = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((परियोजना_रूट / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    स्रोत_फाइलहरू = {
        'अनुमति_चेक': '''public class अनुमति_चेक {
 public static void main(String[] तर्क) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'सञ्जाल_चेक': '''import java.net.*;
public class सञ्जाल_चेक {
 public static void main(String[] तर्क) throws Exception {
  Socket जडान = new Socket("10.0.2.2", Integer.parseInt(तर्क[0]));
  जडान.setSoTimeout(3000);
  byte[] पाठ = "TCP 한글\\n".getBytes("UTF-8");
  जडान.getOutputStream().write(पाठ);
  for (int राख्नुहोस्_अनुक्रमणिका = 0; राख्नुहोस्_अनुक्रमणिका < पाठ.length; राख्नुहोस्_अनुक्रमणिका++)
   if (जडान.getInputStream().read() != (पाठ[राख्नुहोस्_अनुक्रमणिका] & 255)) throw new RuntimeException("TCP mismatch");
  जडान.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  पाठ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(पाठ, पाठ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(तर्क[1])));
  byte[] जवाफ_दिनुहोस् = new byte[64]; DatagramPacket 전문 = new DatagramPacket(जवाफ_दिनुहोस्, जवाफ_दिनुहोस्.length);
  종단.receive(전문);
  if (전문.getLength() != पाठ.length) throw new RuntimeException("UDP length");
  for (int राख्नुहोस्_अनुक्रमणिका = 0; राख्नुहोस्_अनुक्रमणिका < पाठ.length; राख्नुहोस्_अनुक्रमणिका++)
   if (जवाफ_दिनुहोस्[राख्नुहोस्_अनुक्रमणिका] != पाठ[राख्नुहोस्_अनुक्रमणिका]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] तर्क) throws Exception {
  ServerSocket सर्भर_मान = new ServerSocket(9300); सर्भर_मान.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket जडान = सर्भर_मान.accept(); जडान.setSoTimeout(5000);
  जडान.getOutputStream().write(जडान.getInputStream().read() + 1);
  जडान.close(); सर्भर_मान.close();
  byte[] लगत = new byte[64]; DatagramPacket 전문 = new DatagramPacket(लगत, लगत.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for नाम, स्रोत in स्रोत_फाइलहरू.items():
        (출력 / (नाम + '.java')).write_text(स्रोत, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (नाम + '.java')) for नाम in स्रोत_फाइलहरू])
    लग_रेकर्ड = bytearray()
    def 빈접속번호(प्रकार_कोटि=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, प्रकार_कोटि) as खोज_मान:
            खोज_मान.bind(('127.0.0.4', 0))
            return खोज_मान.getsockname()[1]
    파일접속번호, टिसिपी_पोर्ट, युडिपी_पोर्ट = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    प्रक्रिया_मान = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, सञ्जाल_ब्रिज(
                파일접속번호, ['tcp:{}:9300'.format(टिसिपी_पोर्ट), 'udp:{}:9301'.format(युडिपी_पोर्ट)],
                क्यापचर=True, होस्ट_ठेगाना='127.0.0.4') as ब्रिज_मान:
            नियन्त्रण_बाटो = Path(임시) / 'qmp.sock'
            प्रक्रिया_मान = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(नियन्त्रण_बाटो)] + ब्रिज_मान.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            छान्नुहोस्_वस्तु = selectors.DefaultSelector()
            छान्नुहोस्_वस्तु.register(प्रक्रिया_मान.stdout, selectors.EVENT_READ)
            def 받기(शो_मान=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while शो_मान not in लग_रेकर्ड[처음:]:
                    if time.monotonic() > 끝 or प्रक्रिया_मान.poll() is not None:
                        raise AssertionError('Missing ' + repr(शो_मान) + '\n' + लग_रेकर्ड[처음:].decode('utf-8', 'replace'))
                    for कुञ्जी_मान, _ in छान्नुहोस्_वस्तु.select(.05):
                        조각 = कुञ्जी_मान.fileobj.read(65536)
                        if 조각:
                            लग_रेकर्ड.extend(조각)
                return लग_रेकर्ड[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def पठाउनुहोस्(लगत):
                प्रक्रिया_मान.stdin.write(लगत)
                प्रक्रिया_मान.stdin.flush()
            def शेल(पाठ):
                print(पाठ, flush=True)
                처음 = len(लग_रेकर्ड)
                पठाउनुहोस्((पाठ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as नियन्त्रण_मान:
                नियन्त्रण_मान.settimeout(10)
                नियन्त्रण_मान.connect(str(नियन्त्रण_बाटो))
                प्रवाह_मान = नियन्त्रण_मान.makefile('rwb')
                json.loads(प्रवाह_मान.readline())
                def 요청(निर्देशन_मान, तर्क=None):
                    लगत = {'execute': निर्देशन_मान}
                    if तर्क is not None:
                        लगत['arguments'] = तर्क
                    प्रवाह_मान.write((json.dumps(लगत) + '\n').encode())
                    प्रवाह_मान.flush()
                    while True:
                        जवाफ_दिनुहोस् = json.loads(प्रवाह_मान.readline())
                        if 'error' in जवाफ_दिनुहोस्:
                            raise AssertionError(जवाफ_दिनुहोस्)
                        if 'return' in जवाफ_दिनुहोस्:
                            return जवाफ_दिनुहोस्['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                रिपोर्ट_मान['shell_cpu'] = 권한읽기()
                assert 'EL1h' in रिपोर्ट_मान['shell_cpu'], रिपोर्ट_मान['shell_cpu']
                रिपोर्ट_मान['initial_ps'] = शेल('ps')
                assert 'kernel/shell' in रिपोर्ट_मान['initial_ps']
                रिपोर्ट_मान['ipconfig'] = शेल('ipconfig')
                assert 'inet 10.0.2.15' in रिपोर्ट_मान['ipconfig']
                रिपोर्ट_मान['gateway_ping'] = शेल('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in रिपोर्ट_मान['gateway_ping']
                assert 'FTP listening' in शेल('ftpd start')
                with ftplib.FTP() as ट्रान्सफर_मान:
                    ट्रान्सफर_मान.encoding = 'utf-8'
                    ट्रान्सफर_मान.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ट्रान्सफर_मान.login()
                    for नाम in स्रोत_फाइलहरू:
                        ट्रान्सफर_मान.storbinary('STOR ' + नाम + '.class', io.BytesIO((출력 / (नाम + '.class')).read_bytes()))
                처음 = len(लग_रेकर्ड)
                पठाउनुहोस्('java अनुमति_चेक\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    रिपोर्ट_मान['java_cpu'] = 권한읽기()
                    if 'EL0t' in रिपोर्ट_मान['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in रिपोर्ट_मान['java_cpu'], रिपोर्ट_मान['java_cpu']
                받기(처음=처음)
                रिपोर्ट_मान['after_exit_ps'] = शेल('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', रिपोर्ट_मान['after_exit_ps'])
                रिपोर्ट_मान['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as समान_मान:
                    पाठ = शेल('java सञ्जाल_चेक {} {}'.format(समान_मान.टिसिपी_पोर्ट, समान_मान.युडिपी_पोर्ट))
                    assert 'OUTBOUND_TCP_UDP_PASS' in पाठ and 'exit 0' in पाठ, पाठ
                    assert समान_मान.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, समान_मान.수신됨
                    assert not समान_मान.오류들, समान_मान.오류들
                    रिपोर्ट_मान['outbound_peers'] = {종류: लगत.decode() for 종류, लगत in समान_मान.수신됨.items()}
                처음 = len(लग_रेकर्ड)
                पठाउनुहोस्('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', टिसिपी_पोर्ट), timeout=5) as समान_मान:
                    समान_मान.sendall(b'A')
                    assert समान_मान.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as समान_मान:
                    समान_मान.settimeout(5)
                    समान_मान.sendto(b'UDP-IN', ('127.0.0.4', युडिपी_पोर्ट))
                    assert समान_मान.recvfrom(64)[0] == b'UDP-IN'
                पाठ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in पाठ and 'exit 0' in पाठ, पाठ
                रिपोर्ट_मान['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in शेल('terminal')
                शेल('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(लग_रेकर्ड)
                पठाउनुहोस्('java झ्यालउदाहरण\n'.encode())
                받기('GUI 예제 तयार_गर्नुहोस्: झ्यालउदाहरण\r\n'.encode(), 처음)
                처음 = len(लग_रेकर्ड)
                पठाउनुहोस्(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                रिपोर्ट_मान['suspended_java_ps'] = शेल('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java झ्यालउदाहरण', रिपोर्ट_मान['suspended_java_ps']), रिपोर्ट_मान['suspended_java_ps']
                रिपोर्ट_मान['top'] = शेल('top -n 1')
                assert 'java झ्यालउदाहरण' in रिपोर्ट_मान['top'] and 'kernel/shell' in रिपोर्ट_मान['top']
                रिपोर्ट_मान['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                रिपोर्ट_मान['network_trace'] = ब्रिज_मान.추적기록
                assert not ब्रिज_मान.त्रुटि, ब्रिज_मान.त्रुटि
                पठाउनुहोस्(b'poweroff\n')
                assert प्रक्रिया_मान.wait(timeout=15) == 0
                रिपोर्ट_मान['passed'] = True
            छान्नुहोस्_वस्तु.close()
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
        (출력 / 'serial.log').write_bytes(लग_रेकर्ड)
        (출력 / 'report.json').write_text(json.dumps(रिपोर्ट_मान, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({कुञ्जी_मान: रिपोर्ट_मान[कुञ्जी_मान] for कुञ्जी_मान in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    चलाउनुहोस्()
