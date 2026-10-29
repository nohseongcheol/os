#!/usr/bin/env python3
"""QEMU의 വാസ്തവമായ_ഡാറ്റാ CPU അനുമതി_മൂല്യം, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from നടപ്പാക്കുക_കമാന്_ഡ് import പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം, ആജ്ഞ
from നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ് import നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്
from 되돌림시험서버 import 되돌림시험서버


def നടപ്പിലാക്കുക():
    ഫലം = പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/verification/execution-network-review'
    ഫലം.mkdir(parents=True, exist_ok=True)
    నివేదిక_മൂല്യം = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((പ്രൊജക്റ്റ്_ചെയ്യുക_വർഗ്ഗമൂലം / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ഉറവിടം_ഫയലുകൾ = {
        'അനുമതി_ചെക്ക്': '''public class അനുമതി_ചെക്ക് {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'നെറ്റ്_വർക്ക്_ചെക്ക്': '''import java.net.*;
public class നെറ്റ്_വർക്ക്_ചെക്ക് {
 public static void main(String[] 인수) throws Exception {
  Socket കണക്ടു്_ചെയ്യുക = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  കണക്ടു്_ചെയ്യുക.setSoTimeout(3000);
  byte[] പദാവലി = "TCP 한글\\n".getBytes("UTF-8");
  കണക്ടു്_ചെയ്യുക.getOutputStream().write(പദാവലി);
  for (int പദവി_സൂചിക = 0; പദവി_സൂചിക < പദാവലി.length; പദവി_സൂചിക++)
   if (കണക്ടു്_ചെയ്യുക.getInputStream().read() != (പദാവലി[പദവി_സൂചിക] & 255)) throw new RuntimeException("TCP mismatch");
  കണക്ടു്_ചെയ്യുക.close();
  DatagramSocket അവസാനബിന്ദു = new DatagramSocket(); അവസാനബിന്ദു.setSoTimeout(3000);
  പദാവലി = "UDP 한글".getBytes("UTF-8");
  അവസാനബിന്ദു.send(new DatagramPacket(പദാവലി, പദാവലി.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] മറുപടി_നൽകുക = new byte[64]; DatagramPacket 전문 = new DatagramPacket(മറുപടി_നൽകുക, മറുപടി_നൽകുക.length);
  അവസാനബിന്ദു.receive(전문);
  if (전문.getLength() != പദാവലി.length) throw new RuntimeException("UDP length");
  for (int പദവി_സൂചിക = 0; പദവി_സൂചിക < പദാവലി.length; പദവി_സൂചിക++)
   if (മറുപടി_നൽകുക[പദവി_സൂചിക] != പദാവലി[പദവി_സൂചിക]) throw new RuntimeException("UDP mismatch");
  അവസാനബിന്ദു.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket സെര്_വര്_മൂല്യം = new ServerSocket(9300); സെര്_വര്_മൂല്യം.setSoTimeout(5000);
  DatagramSocket അവസാനബിന്ദു = new DatagramSocket(9301); അവസാനബിന്ദു.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket കണക്ടു്_ചെയ്യുക = സെര്_വര്_മൂല്യം.accept(); കണക്ടു്_ചെയ്യുക.setSoTimeout(5000);
  കണക്ടു്_ചെയ്യുക.getOutputStream().write(കണക്ടു്_ചെയ്യുക.getInputStream().read() + 1);
  കണക്ടു്_ചെയ്യുക.close(); സെര്_വര്_മൂല്യം.close();
  byte[] ഡാറ്റാ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ഡാറ്റാ, ഡാറ്റാ.length);
  അവസാനബിന്ദു.receive(전문); അവസാനബിന്ദു.send(전문); അവസാനബിന്ദു.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for പേരു്, ഉറവിടം in ഉറവിടം_ഫയലുകൾ.items():
        (ഫലം / (പേരു് + '.java')).write_text(ഉറവിടം, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(ഫലം)] +
                          [str(ഫലം / (പേരു് + '.java')) for പേരു് in ഉറവിടം_ഫയലുകൾ])
    ലോഗ്_രേഖ = bytearray()
    def ശൂന്യം_പോര്_ട്ട്_നമ്പര്(ടൈപ്പ്_ചെയ്യുക_വകുപ്പ്=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ടൈപ്പ്_ചെയ്യുക_വകുപ്പ്) as തിരയൽ_മൂല്യം:
            തിരയൽ_മൂല്യം.bind(('127.0.0.4', 0))
            return തിരയൽ_മൂല്യം.getsockname()[1]
    ഫയല്_പോര്_ട്ട്_നമ്പര്, ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്, 전문접속번호 = ശൂന്യം_പോര്_ട്ട്_നമ്പര്(), ശൂന്യം_പോര്_ട്ട്_നമ്പര്(), ശൂന്യം_പോര്_ട്ട്_നമ്പര്(socket.SOCK_DGRAM)
    പ്രോസസ്_മൂല്യം = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, നെറ്റ്_വർക്ക്_ബ്രിഡ്_ജ്(
                ഫയല്_പോര്_ട്ട്_നമ്പര്, ['tcp:{}:9300'.format(ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്), 'udp:{}:9301'.format(전문접속번호)],
                ക്യാപ്_ചർ_ചെയ്യുക=True, ഹോസ്റ്റ്_ഇമെയിൽ='127.0.0.4') as ബ്രിഡ്_ജ്_മൂല്യം:
            നിയന്ത്രണം_പാത = Path(임시) / 'qmp.sock'
            പ്രോസസ്_മൂല്യം = subprocess.Popen(ആജ്ഞ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(നിയന്ത്രണം_പാത)] + ബ്രിഡ്_ജ്_മൂല്യം.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            നോക്കിയെടുക്കുക_ഇനം = selectors.DefaultSelector()
            നോക്കിയെടുക്കുക_ഇനം.register(പ്രോസസ്_മൂല്യം.stdout, selectors.EVENT_READ)
            def 받기(പ്രദർശനം_മൂല്യം=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while പ്രദർശനം_മൂല്യം not in ലോഗ്_രേഖ[처음:]:
                    if time.monotonic() > 끝 or പ്രോസസ്_മൂല്യം.poll() is not None:
                        raise AssertionError('Missing ' + repr(പ്രദർശനം_മൂല്യം) + '\n' + ലോഗ്_രേഖ[처음:].decode('utf-8', 'replace'))
                    for കീ_മൂല്യം, _ in നോക്കിയെടുക്കുക_ഇനം.select(.05):
                        조각 = കീ_മൂല്യം.fileobj.read(65536)
                        if 조각:
                            ലോഗ്_രേഖ.extend(조각)
                return ലോഗ്_രേഖ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def അയയ്ക്കുക(ഡാറ്റാ):
                പ്രോസസ്_മൂല്യം.stdin.write(ഡാറ്റാ)
                പ്രോസസ്_മൂല്യം.stdin.flush()
            def ഷെല്(പദാവലി):
                print(പദാവലി, flush=True)
                처음 = len(ലോഗ്_രേഖ)
                അയയ്ക്കുക((പദാവലി + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as നിയന്ത്രണം_മൂല്യം:
                നിയന്ത്രണം_മൂല്യം.settimeout(10)
                നിയന്ത്രണം_മൂല്യം.connect(str(നിയന്ത്രണം_പാത))
                സ്ട്രീം_മൂല്യം = നിയന്ത്രണം_മൂല്യം.makefile('rwb')
                json.loads(സ്ട്രീം_മൂല്യം.readline())
                def HTTP_അപേക്ഷ(നിര്_ദേശം_മൂല്യം, 인수=None):
                    ഡാറ്റാ = {'execute': നിര്_ദേശം_മൂല്യം}
                    if 인수 is not None:
                        ഡാറ്റാ['arguments'] = 인수
                    സ്ട്രീം_മൂല്യം.write((json.dumps(ഡാറ്റാ) + '\n').encode())
                    സ്ട്രീം_മൂല്യം.flush()
                    while True:
                        മറുപടി_നൽകുക = json.loads(സ്ട്രീം_മൂല്യം.readline())
                        if 'error' in മറുപടി_നൽകുക:
                            raise AssertionError(മറുപടി_നൽകുക)
                        if 'return' in മറുപടി_നൽകുക:
                            return മറുപടി_നൽകുക['return']
                HTTP_അപേക്ഷ('qmp_capabilities')
                def 권한읽기():
                    HTTP_അപേക്ഷ('stop')
                    try:
                        return HTTP_അപേക്ഷ('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        HTTP_അപേക്ഷ('cont')
                నివేదిక_മൂല്യം['shell_cpu'] = 권한읽기()
                assert 'EL1h' in నివేదిక_മൂല്യം['shell_cpu'], నివేదిక_മൂല്യം['shell_cpu']
                నివేదిక_മൂല്യം['initial_ps'] = ഷെല്('ps')
                assert 'kernel/shell' in నివేదిక_മൂല്യം['initial_ps']
                నివేదిక_മൂല്യം['ipconfig'] = ഷെല്('ipconfig')
                assert 'inet 10.0.2.15' in నివేదిక_മൂല്യം['ipconfig']
                నివేదిక_മൂല്യം['gateway_ping'] = ഷെല്('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in నివేదిక_മൂല്യം['gateway_ping']
                assert 'FTP listening' in ഷെല്('ftpd start')
                with ftplib.FTP() as കൈമാറുക_മൂല്യം_630ba093:
                    കൈമാറുക_മൂല്യം_630ba093.encoding = 'utf-8'
                    കൈമാറുക_മൂല്യം_630ba093.connect('127.0.0.4', ഫയല്_പോര്_ട്ട്_നമ്പര്, timeout=20)
                    കൈമാറുക_മൂല്യം_630ba093.login()
                    for പേരു് in ഉറവിടം_ഫയലുകൾ:
                        കൈമാറുക_മൂല്യം_630ba093.storbinary('STOR ' + പേരു് + '.class', io.BytesIO((ഫലം / (പേരു് + '.class')).read_bytes()))
                처음 = len(ലോഗ്_രേഖ)
                അയയ്ക്കുക('java അനുമതി_ചെക്ക്\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    నివేదిక_മൂല്യം['java_cpu'] = 권한읽기()
                    if 'EL0t' in నివేదిక_മൂല്യം['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in నివేదిక_മൂല്യം['java_cpu'], నివేదిక_മൂല്യം['java_cpu']
                받기(처음=처음)
                నివేదిక_മൂല്യം['after_exit_ps'] = ഷെല്('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', నివేదిక_മൂല്യം['after_exit_ps'])
                నివేదిక_മൂല്യം['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as പീര്_മൂല്യം:
                    പദാവലി = ഷെല്('java നെറ്റ്_വർക്ക്_ചെക്ക് {} {}'.format(പീര്_മൂല്യം.ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്, പീര്_മൂല്യം.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
                    assert പീര്_മൂല്യം.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, പീര്_മൂല്യം.수신됨
                    assert not പീര്_മൂല്യം.오류들, പീര്_മൂല്യം.오류들
                    నివేదిక_മൂല്യം['outbound_peers'] = {종류: ഡാറ്റാ.decode() for 종류, ഡാറ്റാ in പീര്_മൂല്യം.수신됨.items()}
                처음 = len(ലോഗ്_രേഖ)
                അയയ്ക്കുക('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ട്രാന്_സ്_മിഷന്_കണ്_ട്രോള്_പ്രോട്ടോക്കോള്_പോര്_ട്ട്), timeout=5) as പീര്_മൂല്യം:
                    പീര്_മൂല്യം.sendall(b'A')
                    assert പീര്_മൂല്യം.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as പീര്_മൂല്യം:
                    പീര്_മൂല്യം.settimeout(5)
                    പീര്_മൂല്യം.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert പീര്_മൂല്യം.recvfrom(64)[0] == b'UDP-IN'
                പദാവലി = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in പദാവലി and 'exit 0' in പദാവലി, പദാവലി
                నివేదిక_മൂല്യം['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in ഷെല്('terminal')
                ഷെല്('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ലോഗ്_രേഖ)
                അയയ്ക്കുക('java 창예제\n'.encode())
                받기('GUI 예제 തയ്യാറാക്കുക: 창예제\r\n'.encode(), 처음)
                처음 = len(ലോഗ്_രേഖ)
                അയയ്ക്കുക(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                నివేదిక_മൂല്യം['suspended_java_ps'] = ഷെല്('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', నివేదిక_മൂല്യം['suspended_java_ps']), నివేదిక_മൂല്യം['suspended_java_ps']
                నివేదిక_മൂല്യം['top'] = ഷെല്('top -n 1')
                assert 'java 창예제' in నివేదిక_മൂല്യം['top'] and 'kernel/shell' in నివేదిక_മൂല്യം['top']
                నివేదిక_മൂല്യം['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                నివేదిక_മൂല്യം['network_trace'] = ബ്രിഡ്_ജ്_മൂല്യം.ട്രെയ്സ്_ലോഗ്
                assert not ബ്രിഡ്_ജ്_മൂല്യം.പിശക്, ബ്രിഡ്_ജ്_മൂല്യം.പിശക്
                അയയ്ക്കുക(b'poweroff\n')
                assert പ്രോസസ്_മൂല്യം.wait(timeout=15) == 0
                నివేదిక_മൂല്യം['passed'] = True
            നോക്കിയെടുക്കുക_ഇനം.close()
    except Exception as പിശക്:
        నివేదిక_മൂല്യം['error'] = str(പിശക്)
        raise
    finally:
        if പ്രോസസ്_മൂല്യം is not None and പ്രോസസ്_മൂല്യം.poll() is None:
            പ്രോസസ്_മൂല്യം.terminate()
            try:
                പ്രോസസ്_മൂല്യം.wait(timeout=10)
            except subprocess.TimeoutExpired:
                പ്രോസസ്_മൂല്യം.kill()
                പ്രോസസ്_മൂല്യം.wait()
        (ഫലം / 'serial.log').write_bytes(ലോഗ്_രേഖ)
        (ഫലം / 'report.json').write_text(json.dumps(నివేదిక_മൂല്യം, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({കീ_മൂല്യം: నివేదిక_മൂല്യം[കീ_മൂല്യം] for കീ_മൂല്യം in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    നടപ്പിലാക്കുക()
