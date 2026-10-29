#!/usr/bin/env python3
"""QEMU의 వాస్తవ_డేటా CPU అనుమతి_మూల్యం, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం, ఆదేశము
from నెట్_వర్క్_బ్రిడ్జ్ import నెట్_వర్క్_బ్రిడ్జ్
from 되돌림시험서버 import 되돌림시험서버


def నడుపుము():
    అవుట్పుట్ = ప్రొజెక్ట్_మూలం / 'build/verification/execution-network-review'
    అవుట్పుట్.mkdir(parents=True, exist_ok=True)
    నివేదిక_మూల్యం = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    మూలం_ఫైల్_లు = {
        'అనుమతి_తనిఖీ': '''public class అనుమతి_తనిఖీ {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'నెట్_వర్క్_తనిఖీ': '''import java.net.*;
public class నెట్_వర్క్_తనిఖీ {
 public static void main(String[] 인수) throws Exception {
  Socket కనెక్టుచేయి = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  కనెక్టుచేయి.setSoTimeout(3000);
  byte[] పాఠ్యము = "TCP 한글\\n".getBytes("UTF-8");
  కనెక్టుచేయి.getOutputStream().write(పాఠ్యము);
  for (int స్థాయి_సూచీ = 0; స్థాయి_సూచీ < పాఠ్యము.length; స్థాయి_సూచీ++)
   if (కనెక్టుచేయి.getInputStream().read() != (పాఠ్యము[స్థాయి_సూచీ] & 255)) throw new RuntimeException("TCP mismatch");
  కనెక్టుచేయి.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  పాఠ్యము = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(పాఠ్యము, పాఠ్యము.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] ప్రత్యుత్తరం_ఇవ్వు = new byte[64]; DatagramPacket 전문 = new DatagramPacket(ప్రత్యుత్తరం_ఇవ్వు, ప్రత్యుత్తరం_ఇవ్వు.length);
  종단.receive(전문);
  if (전문.getLength() != పాఠ్యము.length) throw new RuntimeException("UDP length");
  for (int స్థాయి_సూచీ = 0; స్థాయి_సూచీ < పాఠ్యము.length; స్థాయి_సూచీ++)
   if (ప్రత్యుత్తరం_ఇవ్వు[స్థాయి_సూచీ] != పాఠ్యము[స్థాయి_సూచీ]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket సర్వర్_మూల్యం = new ServerSocket(9300); సర్వర్_మూల్యం.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket కనెక్టుచేయి = సర్వర్_మూల్యం.accept(); కనెక్టుచేయి.setSoTimeout(5000);
  కనెక్టుచేయి.getOutputStream().write(కనెక్టుచేయి.getInputStream().read() + 1);
  కనెక్టుచేయి.close(); సర్వర్_మూల్యం.close();
  byte[] డేటా = new byte[64]; DatagramPacket 전문 = new DatagramPacket(డేటా, డేటా.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for పేరు, వనరు in మూలం_ఫైల్_లు.items():
        (అవుట్పుట్ / (పేరు + '.java')).write_text(వనరు, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(అవుట్పుట్)] +
                          [str(అవుట్పుట్ / (పేరు + '.java')) for పేరు in మూలం_ఫైల్_లు])
    లాగ్_వరుస = bytearray()
    def ఖాళీ_పోర్ట్_సంఖ్య(టైప్_చేయండి_వర్గం=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, టైప్_చేయండి_వర్గం) as శోధన_మూల్యం:
            శోధన_మూల్యం.bind(('127.0.0.4', 0))
            return శోధన_మూల్యం.getsockname()[1]
    ఫైలు_పోర్ట్_సంఖ్య, ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు, 전문접속번호 = ఖాళీ_పోర్ట్_సంఖ్య(), ఖాళీ_పోర్ట్_సంఖ్య(), ఖాళీ_పోర్ట్_సంఖ్య(socket.SOCK_DGRAM)
    విధానం_మూల్యం = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, నెట్_వర్క్_బ్రిడ్జ్(
                ఫైలు_పోర్ట్_సంఖ్య, ['tcp:{}:9300'.format(ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు), 'udp:{}:9301'.format(전문접속번호)],
                సంగ్రహణ=True, హోస్ట్_ఇమెయిల్='127.0.0.4') as బ్రిడ్జ్_మూల్యం:
            నియంత్రణ_పథం = Path(임시) / 'qmp.sock'
            విధానం_మూల్యం = subprocess.Popen(ఆదేశము() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(నియంత్రణ_పథం)] + బ్రిడ్జ్_మూల్యం.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ఎంచు_అంశం = selectors.DefaultSelector()
            ఎంచు_అంశం.register(విధానం_మూల్యం.stdout, selectors.EVENT_READ)
            def 받기(చూపించు_మూల్యం=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while చూపించు_మూల్యం not in లాగ్_వరుస[처음:]:
                    if time.monotonic() > 끝 or విధానం_మూల్యం.poll() is not None:
                        raise AssertionError('Missing ' + repr(చూపించు_మూల్యం) + '\n' + లాగ్_వరుస[처음:].decode('utf-8', 'replace'))
                    for కీ_మూల్యం, _ in ఎంచు_అంశం.select(.05):
                        조각 = కీ_మూల్యం.fileobj.read(65536)
                        if 조각:
                            లాగ్_వరుస.extend(조각)
                return లాగ్_వరుస[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def పంపు(డేటా):
                విధానం_మూల్యం.stdin.write(డేటా)
                విధానం_మూల్యం.stdin.flush()
            def షెల్(పాఠ్యము):
                print(పాఠ్యము, flush=True)
                처음 = len(లాగ్_వరుస)
                పంపు((పాఠ్యము + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as నియంత్రణ_మూల్యం:
                నియంత్రణ_మూల్యం.settimeout(10)
                నియంత్రణ_మూల్యం.connect(str(నియంత్రణ_పథం))
                ధార_మూల్యం = నియంత్రణ_మూల్యం.makefile('rwb')
                json.loads(ధార_మూల్యం.readline())
                def 요청(సూచన_మూల్యం, 인수=None):
                    డేటా = {'execute': సూచన_మూల్యం}
                    if 인수 is not None:
                        డేటా['arguments'] = 인수
                    ధార_మూల్యం.write((json.dumps(డేటా) + '\n').encode())
                    ధార_మూల్యం.flush()
                    while True:
                        ప్రత్యుత్తరం_ఇవ్వు = json.loads(ధార_మూల్యం.readline())
                        if 'error' in ప్రత్యుత్తరం_ఇవ్వు:
                            raise AssertionError(ప్రత్యుత్తరం_ఇవ్వు)
                        if 'return' in ప్రత్యుత్తరం_ఇవ్వు:
                            return ప్రత్యుత్తరం_ఇవ్వు['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                నివేదిక_మూల్యం['shell_cpu'] = 권한읽기()
                assert 'EL1h' in నివేదిక_మూల్యం['shell_cpu'], నివేదిక_మూల్యం['shell_cpu']
                నివేదిక_మూల్యం['initial_ps'] = షెల్('ps')
                assert 'kernel/shell' in నివేదిక_మూల్యం['initial_ps']
                నివేదిక_మూల్యం['ipconfig'] = షెల్('ipconfig')
                assert 'inet 10.0.2.15' in నివేదిక_మూల్యం['ipconfig']
                నివేదిక_మూల్యం['gateway_ping'] = షెల్('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in నివేదిక_మూల్యం['gateway_ping']
                assert 'FTP listening' in షెల్('ftpd start')
                with ftplib.FTP() as బదిలీ_మూల్యం:
                    బదిలీ_మూల్యం.encoding = 'utf-8'
                    బదిలీ_మూల్యం.connect('127.0.0.4', ఫైలు_పోర్ట్_సంఖ్య, timeout=20)
                    బదిలీ_మూల్యం.login()
                    for పేరు in మూలం_ఫైల్_లు:
                        బదిలీ_మూల్యం.storbinary('STOR ' + పేరు + '.class', io.BytesIO((అవుట్పుట్ / (పేరు + '.class')).read_bytes()))
                처음 = len(లాగ్_వరుస)
                పంపు('java అనుమతి_తనిఖీ\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    నివేదిక_మూల్యం['java_cpu'] = 권한읽기()
                    if 'EL0t' in నివేదిక_మూల్యం['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in నివేదిక_మూల్యం['java_cpu'], నివేదిక_మూల్యం['java_cpu']
                받기(처음=처음)
                నివేదిక_మూల్యం['after_exit_ps'] = షెల్('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', నివేదిక_మూల్యం['after_exit_ps'])
                నివేదిక_మూల్యం['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as పియర్_మూల్యం:
                    పాఠ్యము = షెల్('java నెట్_వర్క్_తనిఖీ {} {}'.format(పియర్_మూల్యం.ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు, పియర్_మూల్యం.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
                    assert పియర్_మూల్యం.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, పియర్_మూల్యం.수신됨
                    assert not పియర్_మూల్యం.오류들, పియర్_మూల్యం.오류들
                    నివేదిక_మూల్యం['outbound_peers'] = {종류: డేటా.decode() for 종류, డేటా in పియర్_మూల్యం.수신됨.items()}
                처음 = len(లాగ్_వరుస)
                పంపు('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు), timeout=5) as పియర్_మూల్యం:
                    పియర్_మూల్యం.sendall(b'A')
                    assert పియర్_మూల్యం.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as పియర్_మూల్యం:
                    పియర్_మూల్యం.settimeout(5)
                    పియర్_మూల్యం.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert పియర్_మూల్యం.recvfrom(64)[0] == b'UDP-IN'
                పాఠ్యము = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
                నివేదిక_మూల్యం['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in షెల్('terminal')
                షెల్('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(లాగ్_వరుస)
                పంపు('java 창예제\n'.encode())
                받기('GUI 예제 సిద్ధం_చేయు: 창예제\r\n'.encode(), 처음)
                처음 = len(లాగ్_వరుస)
                పంపు(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                నివేదిక_మూల్యం['suspended_java_ps'] = షెల్('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', నివేదిక_మూల్యం['suspended_java_ps']), నివేదిక_మూల్యం['suspended_java_ps']
                నివేదిక_మూల్యం['top'] = షెల్('top -n 1')
                assert 'java 창예제' in నివేదిక_మూల్యం['top'] and 'kernel/shell' in నివేదిక_మూల్యం['top']
                నివేదిక_మూల్యం['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                నివేదిక_మూల్యం['network_trace'] = బ్రిడ్జ్_మూల్యం.జాడ_లాగ్
                assert not బ్రిడ్జ్_మూల్యం.దోషం, బ్రిడ్జ్_మూల్యం.దోషం
                పంపు(b'poweroff\n')
                assert విధానం_మూల్యం.wait(timeout=15) == 0
                నివేదిక_మూల్యం['passed'] = True
            ఎంచు_అంశం.close()
    except Exception as దోషం:
        నివేదిక_మూల్యం['error'] = str(దోషం)
        raise
    finally:
        if విధానం_మూల్యం is not None and విధానం_మూల్యం.poll() is None:
            విధానం_మూల్యం.terminate()
            try:
                విధానం_మూల్యం.wait(timeout=10)
            except subprocess.TimeoutExpired:
                విధానం_మూల్యం.kill()
                విధానం_మూల్యం.wait()
        (అవుట్పుట్ / 'serial.log').write_bytes(లాగ్_వరుస)
        (అవుట్పుట్ / 'report.json').write_text(json.dumps(నివేదిక_మూల్యం, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({కీ_మూల్యం: నివేదిక_మూల్యం[కీ_మూల్యం] for కీ_మూల్యం in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    నడుపుము()
