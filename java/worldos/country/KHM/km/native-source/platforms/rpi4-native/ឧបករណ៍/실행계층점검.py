#!/usr/bin/env python3
"""QEMU의 ដែលពិត_ទិន្នន័យ CPU ការអនុញ្ញាត_តំលៃ, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស, ពាក្យ_បញ្ជា
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def រត់():
    លទ្ធផល = បញ្ចាំង_ឬស / 'build/verification/execution-network-review'
    លទ្ធផល.mkdir(parents=True, exist_ok=True)
    រាយការណ៍_តំលៃ = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ប្រភព_ឯកសារ = {
        'ការអនុញ្ញាត_ត្រួតពិនិត្យ': '''public class ការអនុញ្ញាត_ត្រួតពិនិត្យ {
 public static void main(String[] អាគុយម៉ង់) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'ណិតវឺក_ត្រួតពិនិត្យ': '''import java.net.*;
public class ណិតវឺក_ត្រួតពិនិត្យ {
 public static void main(String[] អាគុយម៉ង់) throws Exception {
  Socket ភ្ជាប់ = new Socket("10.0.2.2", Integer.parseInt(អាគុយម៉ង់[0]));
  ភ្ជាប់.setSoTimeout(3000);
  byte[] អត្ថបទ = "TCP 한글\\n".getBytes("UTF-8");
  ភ្ជាប់.getOutputStream().write(អត្ថបទ);
  for (int កំណត់ទីតាំង_សន្ទស្សន៏ = 0; កំណត់ទីតាំង_សន្ទស្សន៏ < អត្ថបទ.length; កំណត់ទីតាំង_សន្ទស្សន៏++)
   if (ភ្ជាប់.getInputStream().read() != (អត្ថបទ[កំណត់ទីតាំង_សន្ទស្សន៏] & 255)) throw new RuntimeException("TCP mismatch");
  ភ្ជាប់.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  អត្ថបទ = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(អត្ថបទ, អត្ថបទ.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(អាគុយម៉ង់[1])));
  byte[] ឆ្លើយតប = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ឆ្លើយតប, ឆ្លើយតប.length);
  종단.receive(전문);
  if (전문.getLength() != អត្ថបទ.length) throw new RuntimeException("UDP length");
  for (int កំណត់ទីតាំង_សន្ទស្សន៏ = 0; កំណត់ទីតាំង_សន្ទស្សន៏ < អត្ថបទ.length; កំណត់ទីតាំង_សន្ទស្សន៏++)
   if (ឆ្លើយតប[កំណត់ទីតាំង_សន្ទស្សន៏] != អត្ថបទ[កំណត់ទីតាំង_សន្ទស្សន៏]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] អាគុយម៉ង់) throws Exception {
  ServerSocket ម៉ាស៊ីនមេ_តំលៃ = new ServerSocket(9300); ម៉ាស៊ីនមេ_តំលៃ.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket ភ្ជាប់ = ម៉ាស៊ីនមេ_តំលៃ.accept(); ភ្ជាប់.setSoTimeout(5000);
  ភ្ជាប់.getOutputStream().write(ភ្ជាប់.getInputStream().read() + 1);
  ភ្ជាប់.close(); ម៉ាស៊ីនមេ_តំលៃ.close();
  byte[] ទិន្នន័យ = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ទិន្នន័យ, ទិន្នន័យ.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for ឈ្មោះ, ប្រភព in ប្រភព_ឯកសារ.items():
        (លទ្ធផល / (ឈ្មោះ + '.java')).write_text(ប្រភព, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(លទ្ធផល)] +
                          [str(លទ្ធផល / (ឈ្មោះ + '.java')) for ឈ្មោះ in ប្រភព_ឯកសារ])
    កំណត់_ហេតុ_ថត = bytearray()
    def ទទេរ_លេខរន្ធ(វាយបញ្ចូល_ប្រភេទ=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, វាយបញ្ចូល_ប្រភេទ) as រុករក_តំលៃ:
            រុករក_តំលៃ.bind(('127.0.0.4', 0))
            return រុករក_តំលៃ.getsockname()[1]
    ឯកសារ_លេខរន្ធ, ប្រូតូកូលត្រូតពិនិត្យការបញ្ជូន_ច្រក, 전문접속번호 = ទទេរ_លេខរន្ធ(), ទទេរ_លេខរន្ធ(), ទទេរ_លេខរន្ធ(socket.SOCK_DGRAM)
    ដំណើរការ_តំលៃ = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                ឯកសារ_លេខរន្ធ, ['tcp:{}:9300'.format(ប្រូតូកូលត្រូតពិនិត្យការបញ្ជូន_ច្រក), 'udp:{}:9301'.format(전문접속번호)],
                ថត=True, ហូស_អ៊ីម៉ែល='127.0.0.4') as 다리:
            អង្គបញ្ជា_ផ្លូវ = Path(임시) / 'qmp.sock'
            ដំណើរការ_តំលៃ = subprocess.Popen(ពាក្យ_បញ្ជា() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(អង្គបញ្ជា_ផ្លូវ)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ជ្រើសរើស_ធាតុ = selectors.DefaultSelector()
            ជ្រើសរើស_ធាតុ.register(ដំណើរការ_តំលៃ.stdout, selectors.EVENT_READ)
            def 받기(បង្ហាញ_តំលៃ=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while បង្ហាញ_តំលៃ not in កំណត់_ហេតុ_ថត[처음:]:
                    if time.monotonic() > 끝 or ដំណើរការ_តំលៃ.poll() is not None:
                        raise AssertionError('Missing ' + repr(បង្ហាញ_តំលៃ) + '\n' + កំណត់_ហេតុ_ថត[처음:].decode('utf-8', 'replace'))
                    for ឃី_តំលៃ, _ in ជ្រើសរើស_ធាតុ.select(.05):
                        조각 = ឃី_តំលៃ.fileobj.read(65536)
                        if 조각:
                            កំណត់_ហេតុ_ថត.extend(조각)
                return កំណត់_ហេតុ_ថត[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ផ្ញើ(ទិន្នន័យ):
                ដំណើរការ_តំលៃ.stdin.write(ទិន្នន័យ)
                ដំណើរការ_តំលៃ.stdin.flush()
            def 셸(អត្ថបទ):
                print(អត្ថបទ, flush=True)
                처음 = len(កំណត់_ហេតុ_ថត)
                ផ្ញើ((អត្ថបទ + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as អង្គបញ្ជា_តំលៃ:
                អង្គបញ្ជា_តំលៃ.settimeout(10)
                អង្គបញ្ជា_តំលៃ.connect(str(អង្គបញ្ជា_ផ្លូវ))
                ស្ទ្រីម_តំលៃ = អង្គបញ្ជា_តំលៃ.makefile('rwb')
                json.loads(ស្ទ្រីម_តំលៃ.readline())
                def 요청(ការណែនាំ_តំលៃ, អាគុយម៉ង់=None):
                    ទិន្នន័យ = {'execute': ការណែនាំ_តំលៃ}
                    if អាគុយម៉ង់ is not None:
                        ទិន្នន័យ['arguments'] = អាគុយម៉ង់
                    ស្ទ្រីម_តំលៃ.write((json.dumps(ទិន្នន័យ) + '\n').encode())
                    ស្ទ្រីម_តំលៃ.flush()
                    while True:
                        ឆ្លើយតប = json.loads(ស្ទ្រីម_តំលៃ.readline())
                        if 'error' in ឆ្លើយតប:
                            raise AssertionError(ឆ្លើយតប)
                        if 'return' in ឆ្លើយតប:
                            return ឆ្លើយតប['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                រាយការណ៍_តំលៃ['shell_cpu'] = 권한읽기()
                assert 'EL1h' in រាយការណ៍_តំលៃ['shell_cpu'], រាយការណ៍_តំលៃ['shell_cpu']
                រាយការណ៍_តំលៃ['initial_ps'] = 셸('ps')
                assert 'kernel/shell' in រាយការណ៍_តំលៃ['initial_ps']
                រាយការណ៍_តំលៃ['ipconfig'] = 셸('ipconfig')
                assert 'inet 10.0.2.15' in រាយការណ៍_តំលៃ['ipconfig']
                រាយការណ៍_តំលៃ['gateway_ping'] = 셸('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in រាយការណ៍_តំលៃ['gateway_ping']
                assert 'FTP listening' in 셸('ftpd start')
                with ftplib.FTP() as ផ្ទេរ_តំលៃ:
                    ផ្ទេរ_តំលៃ.encoding = 'utf-8'
                    ផ្ទេរ_តំលៃ.connect('127.0.0.4', ឯកសារ_លេខរន្ធ, timeout=20)
                    ផ្ទេរ_តំលៃ.login()
                    for ឈ្មោះ in ប្រភព_ឯកសារ:
                        ផ្ទេរ_តំលៃ.storbinary('STOR ' + ឈ្មោះ + '.class', io.BytesIO((លទ្ធផល / (ឈ្មោះ + '.class')).read_bytes()))
                처음 = len(កំណត់_ហេតុ_ថត)
                ផ្ញើ('java ការអនុញ្ញាត_ត្រួតពិនិត្យ\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    រាយការណ៍_តំលៃ['java_cpu'] = 권한읽기()
                    if 'EL0t' in រាយការណ៍_តំលៃ['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in រាយការណ៍_តំលៃ['java_cpu'], រាយការណ៍_តំលៃ['java_cpu']
                받기(처음=처음)
                រាយការណ៍_តំលៃ['after_exit_ps'] = 셸('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', រាយការណ៍_តំលៃ['after_exit_ps'])
                រាយការណ៍_តំលៃ['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as សិទ្ធស្មើ_តំលៃ:
                    អត្ថបទ = 셸('java ណិតវឺក_ត្រួតពិនិត្យ {} {}'.format(សិទ្ធស្មើ_តំលៃ.ប្រូតូកូលត្រូតពិនិត្យការបញ្ជូន_ច្រក, សិទ្ធស្មើ_តំលៃ.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
                    assert សិទ្ធស្មើ_តំលៃ.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, សិទ្ធស្មើ_តំលៃ.수신됨
                    assert not សិទ្ធស្មើ_តំលៃ.오류들, សិទ្ធស្មើ_តំលៃ.오류들
                    រាយការណ៍_តំលៃ['outbound_peers'] = {종류: ទិន្នន័យ.decode() for 종류, ទិន្នន័យ in សិទ្ធស្មើ_តំលៃ.수신됨.items()}
                처음 = len(កំណត់_ហេតុ_ថត)
                ផ្ញើ('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ប្រូតូកូលត្រូតពិនិត្យការបញ្ជូន_ច្រក), timeout=5) as សិទ្ធស្មើ_តំលៃ:
                    សិទ្ធស្មើ_តំលៃ.sendall(b'A')
                    assert សិទ្ធស្មើ_តំលៃ.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as សិទ្ធស្មើ_តំលៃ:
                    សិទ្ធស្មើ_តំលៃ.settimeout(5)
                    សិទ្ធស្មើ_តំលៃ.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert សិទ្ធស្មើ_តំលៃ.recvfrom(64)[0] == b'UDP-IN'
                អត្ថបទ = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
                រាយការណ៍_តំលៃ['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in 셸('terminal')
                셸('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(កំណត់_ហេតុ_ថត)
                ផ្ញើ('java 창예제\n'.encode())
                받기('GUI 예제 រៀបចំ: 창예제\r\n'.encode(), 처음)
                처음 = len(កំណត់_ហេតុ_ថត)
                ផ្ញើ(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                រាយការណ៍_តំលៃ['suspended_java_ps'] = 셸('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', រាយការណ៍_តំលៃ['suspended_java_ps']), រាយការណ៍_តំលៃ['suspended_java_ps']
                រាយការណ៍_តំលៃ['top'] = 셸('top -n 1')
                assert 'java 창예제' in រាយការណ៍_តំលៃ['top'] and 'kernel/shell' in រាយការណ៍_តំលៃ['top']
                រាយការណ៍_តំលៃ['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                រាយការណ៍_តំលៃ['network_trace'] = 다리.ត្រេស_កំណត់_ហេតុ
                assert not 다리.កំហុស, 다리.កំហុស
                ផ្ញើ(b'poweroff\n')
                assert ដំណើរការ_តំលៃ.wait(timeout=15) == 0
                រាយការណ៍_តំលៃ['passed'] = True
            ជ្រើសរើស_ធាតុ.close()
    except Exception as កំហុស:
        រាយការណ៍_តំលៃ['error'] = str(កំហុស)
        raise
    finally:
        if ដំណើរការ_តំលៃ is not None and ដំណើរការ_តំលៃ.poll() is None:
            ដំណើរការ_តំលៃ.terminate()
            try:
                ដំណើរការ_តំលៃ.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ដំណើរការ_តំលៃ.kill()
                ដំណើរការ_តំលៃ.wait()
        (លទ្ធផល / 'serial.log').write_bytes(កំណត់_ហេតុ_ថត)
        (លទ្ធផល / 'report.json').write_text(json.dumps(រាយការណ៍_តំលៃ, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ឃី_តំលៃ: រាយការណ៍_តំលៃ[ឃី_តំលៃ] for ឃី_តំលៃ in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    រត់()
