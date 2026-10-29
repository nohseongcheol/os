#!/usr/bin/env python3
"""QEMU의 რეალური_მონაცემები CPU ნებართვა_მნიშვნელობა, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from შესრულება_ბრძანება import პროეცირება_ფესვი, ბრძანება
from ქსელი_ხიდი import ქსელი_ხიდი
from 되돌림시험서버 import 되돌림시험서버


def გაშვება():
    출력 = პროეცირება_ფესვი / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ანგარიში_მნიშვნელობა = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((პროეცირება_ფესვი / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    წყარო_ფაილები = {
        'ნებართვა_შემოწმება': '''public class ნებართვა_შემოწმება {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ქსელი_შემოწმება': '''import java.net.*;
public class ქსელი_შემოწმება {
 public static void main(String[] 인수) throws Exception {
  Socket დაკავშირება = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  დაკავშირება.setSoTimeout(3000);
  byte[] ტექსტი = "TCP 한글\\n".getBytes("UTF-8");
  დაკავშირება.getOutputStream().write(ტექსტი);
  for (int პოზიცია_ინდექსი = 0; პოზიცია_ინდექსი < ტექსტი.length; პოზიცია_ინდექსი++)
   if (დაკავშირება.getInputStream().read() != (ტექსტი[პოზიცია_ინდექსი] & 255)) throw new RuntimeException("TCP mismatch");
  დაკავშირება.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  ტექსტი = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(ტექსტი, ტექსტი.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] პასუხი = new byte[64]; DatagramPacket 전문 = new DatagramPacket(პასუხი, პასუხი.length);
  종단.receive(전문);
  if (전문.getLength() != ტექსტი.length) throw new RuntimeException("UDP length");
  for (int პოზიცია_ინდექსი = 0; პოზიცია_ინდექსი < ტექსტი.length; პოზიცია_ინდექსი++)
   if (პასუხი[პოზიცია_ინდექსი] != ტექსტი[პოზიცია_ინდექსი]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket სერვერი_მნიშვნელობა = new ServerSocket(9300); სერვერი_მნიშვნელობა.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket დაკავშირება = სერვერი_მნიშვნელობა.accept(); დაკავშირება.setSoTimeout(5000);
  დაკავშირება.getOutputStream().write(დაკავშირება.getInputStream().read() + 1);
  დაკავშირება.close(); სერვერი_მნიშვნელობა.close();
  byte[] მონაცემები = new byte[64]; DatagramPacket 전문 = new DatagramPacket(მონაცემები, მონაცემები.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for სახელი, წყარო in წყარო_ფაილები.items():
        (출력 / (სახელი + '.java')).write_text(წყარო, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (სახელი + '.java')) for სახელი in წყარო_ფაილები])
    ჟურნალი_ჩაწერა = bytearray()
    def 빈접속번호(აკრეფა_კატეგორია=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, აკრეფა_კატეგორია) as ძებნა_მნიშვნელობა:
            ძებნა_მნიშვნელობა.bind(('127.0.0.4', 0))
            return ძებნა_მნიშვნელობა.getsockname()[1]
    파일접속번호, გადაცემის_მართვის_პროტოკოლი_პორტი, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    პროცესი_მნიშვნელობა = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, ქსელი_ხიდი(
                파일접속번호, ['tcp:{}:9300'.format(გადაცემის_მართვის_პროტოკოლი_პორტი), 'udp:{}:9301'.format(전문접속번호)],
                გადაღება=True, მასპინძელი_მისამართი='127.0.0.4') as ხიდი_მნიშვნელობა:
            მართვა_მდებარეობა = Path(임시) / 'qmp.sock'
            პროცესი_მნიშვნელობა = subprocess.Popen(ბრძანება() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(მართვა_მდებარეობა)] + ხიდი_მნიშვნელობა.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            არჩევა_ელემენტი = selectors.DefaultSelector()
            არჩევა_ელემენტი.register(პროცესი_მნიშვნელობა.stdout, selectors.EVENT_READ)
            def 받기(ჩვენება_მნიშვნელობა=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while ჩვენება_მნიშვნელობა not in ჟურნალი_ჩაწერა[처음:]:
                    if time.monotonic() > 끝 or პროცესი_მნიშვნელობა.poll() is not None:
                        raise AssertionError('Missing ' + repr(ჩვენება_მნიშვნელობა) + '\n' + ჟურნალი_ჩაწერა[처음:].decode('utf-8', 'replace'))
                    for კლავიში_მნიშვნელობა, _ in არჩევა_ელემენტი.select(.05):
                        조각 = კლავიში_მნიშვნელობა.fileobj.read(65536)
                        if 조각:
                            ჟურნალი_ჩაწერა.extend(조각)
                return ჟურნალი_ჩაწერა[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def გაგზავნა(მონაცემები):
                პროცესი_მნიშვნელობა.stdin.write(მონაცემები)
                პროცესი_მნიშვნელობა.stdin.flush()
            def გარემო(ტექსტი):
                print(ტექსტი, flush=True)
                처음 = len(ჟურნალი_ჩაწერა)
                გაგზავნა((ტექსტი + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as მართვა_მნიშვნელობა:
                მართვა_მნიშვნელობა.settimeout(10)
                მართვა_მნიშვნელობა.connect(str(მართვა_მდებარეობა))
                ნაკადი_მნიშვნელობა = მართვა_მნიშვნელობა.makefile('rwb')
                json.loads(ნაკადი_მნიშვნელობა.readline())
                def 요청(ინსტრუქცია_მნიშვნელობა, 인수=None):
                    მონაცემები = {'execute': ინსტრუქცია_მნიშვნელობა}
                    if 인수 is not None:
                        მონაცემები['arguments'] = 인수
                    ნაკადი_მნიშვნელობა.write((json.dumps(მონაცემები) + '\n').encode())
                    ნაკადი_მნიშვნელობა.flush()
                    while True:
                        პასუხი = json.loads(ნაკადი_მნიშვნელობა.readline())
                        if 'error' in პასუხი:
                            raise AssertionError(პასუხი)
                        if 'return' in პასუხი:
                            return პასუხი['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ანგარიში_მნიშვნელობა['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ანგარიში_მნიშვნელობა['shell_cpu'], ანგარიში_მნიშვნელობა['shell_cpu']
                ანგარიში_მნიშვნელობა['initial_ps'] = გარემო('ps')
                assert 'kernel/shell' in ანგარიში_მნიშვნელობა['initial_ps']
                ანგარიში_მნიშვნელობა['ipconfig'] = გარემო('ipconfig')
                assert 'inet 10.0.2.15' in ანგარიში_მნიშვნელობა['ipconfig']
                ანგარიში_მნიშვნელობა['gateway_ping'] = გარემო('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ანგარიში_მნიშვნელობა['gateway_ping']
                assert 'FTP listening' in გარემო('ftpd start')
                with ftplib.FTP() as გადატანა_მნიშვნელობა_630ba093:
                    გადატანა_მნიშვნელობა_630ba093.encoding = 'utf-8'
                    გადატანა_მნიშვნელობა_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    გადატანა_მნიშვნელობა_630ba093.login()
                    for სახელი in წყარო_ფაილები:
                        გადატანა_მნიშვნელობა_630ba093.storbinary('STOR ' + სახელი + '.class', io.BytesIO((출력 / (სახელი + '.class')).read_bytes()))
                처음 = len(ჟურნალი_ჩაწერა)
                გაგზავნა('java ნებართვა_შემოწმება\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ანგარიში_მნიშვნელობა['java_cpu'] = 권한읽기()
                    if 'EL0t' in ანგარიში_მნიშვნელობა['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ანგარიში_მნიშვნელობა['java_cpu'], ანგარიში_მნიშვნელობა['java_cpu']
                받기(처음=처음)
                ანგარიში_მნიშვნელობა['after_exit_ps'] = გარემო('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ანგარიში_მნიშვნელობა['after_exit_ps'])
                ანგარიში_მნიშვნელობა['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as კვანძი_მნიშვნელობა_6a3b6fa7:
                    ტექსტი = გარემო('java ქსელი_შემოწმება {} {}'.format(კვანძი_მნიშვნელობა_6a3b6fa7.გადაცემის_მართვის_პროტოკოლი_პორტი, კვანძი_მნიშვნელობა_6a3b6fa7.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
                    assert კვანძი_მნიშვნელობა_6a3b6fa7.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, კვანძი_მნიშვნელობა_6a3b6fa7.수신됨
                    assert not კვანძი_მნიშვნელობა_6a3b6fa7.오류들, კვანძი_მნიშვნელობა_6a3b6fa7.오류들
                    ანგარიში_მნიშვნელობა['outbound_peers'] = {종류: მონაცემები.decode() for 종류, მონაცემები in კვანძი_მნიშვნელობა_6a3b6fa7.수신됨.items()}
                처음 = len(ჟურნალი_ჩაწერა)
                გაგზავნა('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', გადაცემის_მართვის_პროტოკოლი_პორტი), timeout=5) as კვანძი_მნიშვნელობა_6a3b6fa7:
                    კვანძი_მნიშვნელობა_6a3b6fa7.sendall(b'A')
                    assert კვანძი_მნიშვნელობა_6a3b6fa7.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as კვანძი_მნიშვნელობა_6a3b6fa7:
                    კვანძი_მნიშვნელობა_6a3b6fa7.settimeout(5)
                    კვანძი_მნიშვნელობა_6a3b6fa7.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert კვანძი_მნიშვნელობა_6a3b6fa7.recvfrom(64)[0] == b'UDP-IN'
                ტექსტი = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in ტექსტი and 'exit 0' in ტექსტი, ტექსტი
                ანგარიში_მნიშვნელობა['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in გარემო('terminal')
                გარემო('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ჟურნალი_ჩაწერა)
                გაგზავნა('java 창예제\n'.encode())
                받기('GUI 예제 მომზადება: 창예제\r\n'.encode(), 처음)
                처음 = len(ჟურნალი_ჩაწერა)
                გაგზავნა(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ანგარიში_მნიშვნელობა['suspended_java_ps'] = გარემო('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ანგარიში_მნიშვნელობა['suspended_java_ps']), ანგარიში_მნიშვნელობა['suspended_java_ps']
                ანგარიში_მნიშვნელობა['top'] = გარემო('top -n 1')
                assert 'java 창예제' in ანგარიში_მნიშვნელობა['top'] and 'kernel/shell' in ანგარიში_მნიშვნელობა['top']
                ანგარიში_მნიშვნელობა['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ანგარიში_მნიშვნელობა['network_trace'] = ხიდი_მნიშვნელობა.추적기록
                assert not ხიდი_მნიშვნელობა.შეცდომა, ხიდი_მნიშვნელობა.შეცდომა
                გაგზავნა(b'poweroff\n')
                assert პროცესი_მნიშვნელობა.wait(timeout=15) == 0
                ანგარიში_მნიშვნელობა['passed'] = True
            არჩევა_ელემენტი.close()
    except Exception as შეცდომა:
        ანგარიში_მნიშვნელობა['error'] = str(შეცდომა)
        raise
    finally:
        if პროცესი_მნიშვნელობა is not None and პროცესი_მნიშვნელობა.poll() is None:
            პროცესი_მნიშვნელობა.terminate()
            try:
                პროცესი_მნიშვნელობა.wait(timeout=10)
            except subprocess.TimeoutExpired:
                პროცესი_მნიშვნელობა.kill()
                პროცესი_მნიშვნელობა.wait()
        (출력 / 'serial.log').write_bytes(ჟურნალი_ჩაწერა)
        (출력 / 'report.json').write_text(json.dumps(ანგარიში_მნიშვნელობა, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({კლავიში_მნიშვნელობა: ანგარიში_მნიშვნელობა[კლავიში_მნიშვნელობა] for კლავიში_მნიშვნელობა in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    გაშვება()
