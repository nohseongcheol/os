#!/usr/bin/env python3
"""QEMU의 વાસ્તવિક_ડેટા CPU અનુમતિ_મૂલ્ય, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from અમલ_કરો_આદેશ import પ્રોજેક્ટ_રૂટ, આદેશ
from નેટવર્ક_બ્રિજ import નેટવર્ક_બ્રિજ
from 되돌림시험서버 import 되돌림시험서버


def ચલાવો_2():
    આઉટપુટ = પ્રોજેક્ટ_રૂટ / 'build/verification/execution-network-review'
    આઉટપુટ.mkdir(parents=True, exist_ok=True)
    અહેવાલ_મૂલ્ય = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((પ્રોજેક્ટ_રૂટ / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    સ્રોત_ફાઇલો = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] દલીલો) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'નેટવર્ક_તપાસો': '''import java.net.*;
public class નેટવર્ક_તપાસો {
 public static void main(String[] દલીલો) throws Exception {
  Socket સંપર્ક_કરો = new Socket("10.0.2.2", Integer.parseInt(દલીલો[0]));
  સંપર્ક_કરો.setSoTimeout(3000);
  byte[] લખાણ = "TCP 한글\\n".getBytes("UTF-8");
  સંપર્ક_કરો.getOutputStream().write(લખાણ);
  for (int સ્થિતિ_અનુક્રમણિકા = 0; સ્થિતિ_અનુક્રમણિકા < લખાણ.length; સ્થિતિ_અનુક્રમણિકા++)
   if (સંપર્ક_કરો.getInputStream().read() != (લખાણ[સ્થિતિ_અનુક્રમણિકા] & 255)) throw new RuntimeException("TCP mismatch");
  સંપર્ક_કરો.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  લખાણ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(લખાણ, લખાણ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(દલીલો[1])));
  byte[] જવાબ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(જવાબ, જવાબ.length);
  종단.receive(전문);
  if (전문.getLength() != લખાણ.length) throw new RuntimeException("UDP length");
  for (int સ્થિતિ_અનુક્રમણિકા = 0; સ્થિતિ_અનુક્રમણિકા < લખાણ.length; સ્થિતિ_અનુક્રમણિકા++)
   if (જવાબ[સ્થિતિ_અનુક્રમણિકા] != લખાણ[સ્થિતિ_અનુક્રમણિકા]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] દલીલો) throws Exception {
  ServerSocket સર્વર_મૂલ્ય = new ServerSocket(9300); સર્વર_મૂલ્ય.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket સંપર્ક_કરો = સર્વર_મૂલ્ય.accept(); સંપર્ક_કરો.setSoTimeout(5000);
  સંપર્ક_કરો.getOutputStream().write(સંપર્ક_કરો.getInputStream().read() + 1);
  સંપર્ક_કરો.close(); સર્વર_મૂલ્ય.close();
  byte[] ડેટા = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ડેટા, ડેટા.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for નામ, સ્રોત in સ્રોત_ફાઇલો.items():
        (આઉટપુટ / (નામ + '.java')).write_text(સ્રોત, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(આઉટપુટ)] +
                          [str(આઉટપુટ / (નામ + '.java')) for નામ in સ્રોત_ફાઇલો])
    લૉગ_પંક્તિ = bytearray()
    def ખાલી_પોર્ટ_નંબર(લખો_શ્રેણી=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, લખો_શ્રેણી) as શોધ_મૂલ્ય:
            શોધ_મૂલ્ય.bind(('127.0.0.4', 0))
            return શોધ_મૂલ્ય.getsockname()[1]
    ફાઇલ_પોર્ટ_નંબર, પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ, 전문접속번호 = ખાલી_પોર્ટ_નંબર(), ખાલી_પોર્ટ_નંબર(), ખાલી_પોર્ટ_નંબર(socket.SOCK_DGRAM)
    પ્રક્રિયા_મૂલ્ય = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, નેટવર્ક_બ્રિજ(
                ફાઇલ_પોર્ટ_નંબર, ['tcp:{}:9300'.format(પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ), 'udp:{}:9301'.format(전문접속번호)],
                કૅપ્ચર_કરો=True, હોસ્ટ_સરનામું='127.0.0.4') as બ્રિજ_મૂલ્ય:
            નિયંત્રણ_પાથ = Path(임시) / 'qmp.sock'
            પ્રક્રિયા_મૂલ્ય = subprocess.Popen(આદેશ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(નિયંત્રણ_પાથ)] + બ્રિજ_મૂલ્ય.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            પસંદ_કરો_આઇટમ = selectors.DefaultSelector()
            પસંદ_કરો_આઇટમ.register(પ્રક્રિયા_મૂલ્ય.stdout, selectors.EVENT_READ)
            def 받기(શૉ_મૂલ્ય=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while શૉ_મૂલ્ય not in લૉગ_પંક્તિ[처음:]:
                    if time.monotonic() > 끝 or પ્રક્રિયા_મૂલ્ય.poll() is not None:
                        raise AssertionError('Missing ' + repr(શૉ_મૂલ્ય) + '\n' + લૉગ_પંક્તિ[처음:].decode('utf-8', 'replace'))
                    for કી_મૂલ્ય, _ in પસંદ_કરો_આઇટમ.select(.05):
                        조각 = કી_મૂલ્ય.fileobj.read(65536)
                        if 조각:
                            લૉગ_પંક્તિ.extend(조각)
                return લૉગ_પંક્તિ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def મોકલો(ડેટા):
                પ્રક્રિયા_મૂલ્ય.stdin.write(ડેટા)
                પ્રક્રિયા_મૂલ્ય.stdin.flush()
            def શેલ(લખાણ):
                print(લખાણ, flush=True)
                처음 = len(લૉગ_પંક્તિ)
                મોકલો((લખાણ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as નિયંત્રણ_મૂલ્ય:
                નિયંત્રણ_મૂલ્ય.settimeout(10)
                નિયંત્રણ_મૂલ્ય.connect(str(નિયંત્રણ_પાથ))
                સ્ટ્રીમ_મૂલ્ય = નિયંત્રણ_મૂલ્ય.makefile('rwb')
                json.loads(સ્ટ્રીમ_મૂલ્ય.readline())
                def 요청(સૂચના_મૂલ્ય, દલીલો=None):
                    ડેટા = {'execute': સૂચના_મૂલ્ય}
                    if દલીલો is not None:
                        ડેટા['arguments'] = દલીલો
                    સ્ટ્રીમ_મૂલ્ય.write((json.dumps(ડેટા) + '\n').encode())
                    સ્ટ્રીમ_મૂલ્ય.flush()
                    while True:
                        જવાબ = json.loads(સ્ટ્રીમ_મૂલ્ય.readline())
                        if 'error' in જવાબ:
                            raise AssertionError(જવાબ)
                        if 'return' in જવાબ:
                            return જવાબ['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                અહેવાલ_મૂલ્ય['shell_cpu'] = 권한읽기()
                assert 'EL1h' in અહેવાલ_મૂલ્ય['shell_cpu'], અહેવાલ_મૂલ્ય['shell_cpu']
                અહેવાલ_મૂલ્ય['initial_ps'] = શેલ('ps')
                assert 'kernel/shell' in અહેવાલ_મૂલ્ય['initial_ps']
                અહેવાલ_મૂલ્ય['ipconfig'] = શેલ('ipconfig')
                assert 'inet 10.0.2.15' in અહેવાલ_મૂલ્ય['ipconfig']
                અહેવાલ_મૂલ્ય['gateway_ping'] = શેલ('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in અહેવાલ_મૂલ્ય['gateway_ping']
                assert 'FTP listening' in શેલ('ftpd start')
                with ftplib.FTP() as સ્થાનાંતર_મૂલ્ય:
                    સ્થાનાંતર_મૂલ્ય.encoding = 'utf-8'
                    સ્થાનાંતર_મૂલ્ય.connect('127.0.0.4', ફાઇલ_પોર્ટ_નંબર, timeout=20)
                    સ્થાનાંતર_મૂલ્ય.login()
                    for નામ in સ્રોત_ફાઇલો:
                        સ્થાનાંતર_મૂલ્ય.storbinary('STOR ' + નામ + '.class', io.BytesIO((આઉટપુટ / (નામ + '.class')).read_bytes()))
                처음 = len(લૉગ_પંક્તિ)
                મોકલો('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    અહેવાલ_મૂલ્ય['java_cpu'] = 권한읽기()
                    if 'EL0t' in અહેવાલ_મૂલ્ય['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in અહેવાલ_મૂલ્ય['java_cpu'], અહેવાલ_મૂલ્ય['java_cpu']
                받기(처음=처음)
                અહેવાલ_મૂલ્ય['after_exit_ps'] = શેલ('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', અહેવાલ_મૂલ્ય['after_exit_ps'])
                અહેવાલ_મૂલ્ય['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as પીઅર_મૂલ્ય:
                    લખાણ = શેલ('java નેટવર્ક_તપાસો {} {}'.format(પીઅર_મૂલ્ય.પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ, પીઅર_મૂલ્ય.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in લખાણ and 'exit 0' in લખાણ, લખાણ
                    assert પીઅર_મૂલ્ય.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, પીઅર_મૂલ્ય.수신됨
                    assert not પીઅર_મૂલ્ય.오류들, પીઅર_મૂલ્ય.오류들
                    અહેવાલ_મૂલ્ય['outbound_peers'] = {종류: ડેટા.decode() for 종류, ડેટા in પીઅર_મૂલ્ય.수신됨.items()}
                처음 = len(લૉગ_પંક્તિ)
                મોકલો('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', પ્રસારણ_નિયંત્રણ_પ્રોટોકૉલ_પૉર્ટ), timeout=5) as પીઅર_મૂલ્ય:
                    પીઅર_મૂલ્ય.sendall(b'A')
                    assert પીઅર_મૂલ્ય.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as પીઅર_મૂલ્ય:
                    પીઅર_મૂલ્ય.settimeout(5)
                    પીઅર_મૂલ્ય.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert પીઅર_મૂલ્ય.recvfrom(64)[0] == b'UDP-IN'
                લખાણ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in લખાણ and 'exit 0' in લખાણ, લખાણ
                અહેવાલ_મૂલ્ય['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in શેલ('terminal')
                શેલ('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(લૉગ_પંક્તિ)
                મોકલો('java 창예제\n'.encode())
                받기('GUI 예제 તૈયાર_કરો: 창예제\r\n'.encode(), 처음)
                처음 = len(લૉગ_પંક્તિ)
                મોકલો(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                અહેવાલ_મૂલ્ય['suspended_java_ps'] = શેલ('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', અહેવાલ_મૂલ્ય['suspended_java_ps']), અહેવાલ_મૂલ્ય['suspended_java_ps']
                અહેવાલ_મૂલ્ય['top'] = શેલ('top -n 1')
                assert 'java 창예제' in અહેવાલ_મૂલ્ય['top'] and 'kernel/shell' in અહેવાલ_મૂલ્ય['top']
                અહેવાલ_મૂલ્ય['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                અહેવાલ_મૂલ્ય['network_trace'] = બ્રિજ_મૂલ્ય.ટ્રૅસ_લૉગ
                assert not બ્રિજ_મૂલ્ય.ભૂલ, બ્રિજ_મૂલ્ય.ભૂલ
                મોકલો(b'poweroff\n')
                assert પ્રક્રિયા_મૂલ્ય.wait(timeout=15) == 0
                અહેવાલ_મૂલ્ય['passed'] = True
            પસંદ_કરો_આઇટમ.close()
    except Exception as ભૂલ:
        અહેવાલ_મૂલ્ય['error'] = str(ભૂલ)
        raise
    finally:
        if પ્રક્રિયા_મૂલ્ય is not None and પ્રક્રિયા_મૂલ્ય.poll() is None:
            પ્રક્રિયા_મૂલ્ય.terminate()
            try:
                પ્રક્રિયા_મૂલ્ય.wait(timeout=10)
            except subprocess.TimeoutExpired:
                પ્રક્રિયા_મૂલ્ય.kill()
                પ્રક્રિયા_મૂલ્ય.wait()
        (આઉટપુટ / 'serial.log').write_bytes(લૉગ_પંક્તિ)
        (આઉટપુટ / 'report.json').write_text(json.dumps(અહેવાલ_મૂલ્ય, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({કી_મૂલ્ય: અહેવાલ_મૂલ્ય[કી_મૂલ્ય] for કી_મૂલ્ય in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ચલાવો_2()
