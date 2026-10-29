#!/usr/bin/env python3
"""QEMU의 faktiki_verilənlər CPU icazə_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from icra_etmək_əmr import Project_kök, Əmr
from Şəbəkə_körpü import Şəbəkə_körpü
from 되돌림시험서버 import 되돌림시험서버


def İcra_Et():
    출력 = Project_kök / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    hesabat_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_kök / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    mənbə_Fayllar = {
        'icazə_çek': '''public class icazə_çek {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Şəbəkə_çek': '''import java.net.*;
public class Şəbəkə_çek {
 public static void main(String[] 인수) throws Exception {
  Socket Bağlan = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Bağlan.setSoTimeout(3000);
  byte[] Mətn = "TCP 한글\\n".getBytes("UTF-8");
  Bağlan.getOutputStream().write(Mətn);
  for (int yerinə_qoymaq_INDEX = 0; yerinə_qoymaq_INDEX < Mətn.length; yerinə_qoymaq_INDEX++)
   if (Bağlan.getInputStream().read() != (Mətn[yerinə_qoymaq_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Bağlan.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Mətn = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Mətn, Mətn.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] cavab = new byte[64]; DatagramPacket 전문 = new DatagramPacket(cavab, cavab.length);
  종단.receive(전문);
  if (전문.getLength() != Mətn.length) throw new RuntimeException("UDP length");
  for (int yerinə_qoymaq_INDEX = 0; yerinə_qoymaq_INDEX < Mətn.length; yerinə_qoymaq_INDEX++)
   if (cavab[yerinə_qoymaq_INDEX] != Mətn[yerinə_qoymaq_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Bağlan = server_VALUE.accept(); Bağlan.setSoTimeout(5000);
  Bağlan.getOutputStream().write(Bağlan.getInputStream().read() + 1);
  Bağlan.close(); server_VALUE.close();
  byte[] verilənlər = new byte[64]; DatagramPacket 전문 = new DatagramPacket(verilənlər, verilənlər.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ad, QAYNAQ in mənbə_Fayllar.items():
        (출력 / (Ad + '.java')).write_text(QAYNAQ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Ad + '.java')) for Ad in mənbə_Fayllar])
    LOG_yaz = bytearray()
    def 빈접속번호(TYPE_sahə=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_sahə) as SEARCH_VALUE:
            SEARCH_VALUE.bind(('127.0.0.4', 0))
            return SEARCH_VALUE.getsockname()[1]
    파일접속번호, TCP_port, UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proses_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Şəbəkə_körpü(
                파일접속번호, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                çəkmək=True, host_ünvan='127.0.0.4') as körpü_VALUE:
            nəzarət_yol = Path(임시) / 'qmp.sock'
            Proses_VALUE = subprocess.Popen(Əmr() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(nəzarət_yol)] + körpü_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_element = selectors.DefaultSelector()
            CHOOSE_element.register(Proses_VALUE.stdout, selectors.EVENT_READ)
            def 받기(göstərmək_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while göstərmək_VALUE not in LOG_yaz[처음:]:
                    if time.monotonic() > 끝 or Proses_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(göstərmək_VALUE) + '\n' + LOG_yaz[처음:].decode('utf-8', 'replace'))
                    for Açar_VALUE, _ in CHOOSE_element.select(.05):
                        조각 = Açar_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_yaz.extend(조각)
                return LOG_yaz[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def göndərmək(verilənlər):
                Proses_VALUE.stdin.write(verilənlər)
                Proses_VALUE.stdin.flush()
            def örtük(Mətn):
                print(Mətn, flush=True)
                처음 = len(LOG_yaz)
                göndərmək((Mətn + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as nəzarət_VALUE:
                nəzarət_VALUE.settimeout(10)
                nəzarət_VALUE.connect(str(nəzarət_yol))
                axın_VALUE = nəzarət_VALUE.makefile('rwb')
                json.loads(axın_VALUE.readline())
                def HTTP_sorğusu(təlimat_VALUE, 인수=None):
                    verilənlər = {'execute': təlimat_VALUE}
                    if 인수 is not None:
                        verilənlər['arguments'] = 인수
                    axın_VALUE.write((json.dumps(verilənlər) + '\n').encode())
                    axın_VALUE.flush()
                    while True:
                        cavab = json.loads(axın_VALUE.readline())
                        if 'error' in cavab:
                            raise AssertionError(cavab)
                        if 'return' in cavab:
                            return cavab['return']
                HTTP_sorğusu('qmp_capabilities')
                def 권한읽기():
                    HTTP_sorğusu('stop')
                    try:
                        return HTTP_sorğusu('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        HTTP_sorğusu('cont')
                hesabat_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in hesabat_VALUE['shell_cpu'], hesabat_VALUE['shell_cpu']
                hesabat_VALUE['initial_ps'] = örtük('ps')
                assert 'kernel/shell' in hesabat_VALUE['initial_ps']
                hesabat_VALUE['ipconfig'] = örtük('ipconfig')
                assert 'inet 10.0.2.15' in hesabat_VALUE['ipconfig']
                hesabat_VALUE['gateway_ping'] = örtük('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in hesabat_VALUE['gateway_ping']
                assert 'FTP listening' in örtük('ftpd start')
                with ftplib.FTP() as ötürmə_VALUE:
                    ötürmə_VALUE.encoding = 'utf-8'
                    ötürmə_VALUE.connect('127.0.0.4', 파일접속번호, timeout=20)
                    ötürmə_VALUE.login()
                    for Ad in mənbə_Fayllar:
                        ötürmə_VALUE.storbinary('STOR ' + Ad + '.class', io.BytesIO((출력 / (Ad + '.class')).read_bytes()))
                처음 = len(LOG_yaz)
                göndərmək('java icazə_çek\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    hesabat_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in hesabat_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in hesabat_VALUE['java_cpu'], hesabat_VALUE['java_cpu']
                받기(처음=처음)
                hesabat_VALUE['after_exit_ps'] = örtük('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', hesabat_VALUE['after_exit_ps'])
                hesabat_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as eynisəviyyəli_VALUE:
                    Mətn = örtük('java Şəbəkə_çek {} {}'.format(eynisəviyyəli_VALUE.TCP_port, eynisəviyyəli_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Mətn and 'exit 0' in Mətn, Mətn
                    assert eynisəviyyəli_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, eynisəviyyəli_VALUE.수신됨
                    assert not eynisəviyyəli_VALUE.오류들, eynisəviyyəli_VALUE.오류들
                    hesabat_VALUE['outbound_peers'] = {종류: verilənlər.decode() for 종류, verilənlər in eynisəviyyəli_VALUE.수신됨.items()}
                처음 = len(LOG_yaz)
                göndərmək('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as eynisəviyyəli_VALUE:
                    eynisəviyyəli_VALUE.sendall(b'A')
                    assert eynisəviyyəli_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as eynisəviyyəli_VALUE:
                    eynisəviyyəli_VALUE.settimeout(5)
                    eynisəviyyəli_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert eynisəviyyəli_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Mətn = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Mətn and 'exit 0' in Mətn, Mətn
                hesabat_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in örtük('terminal')
                örtük('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_yaz)
                göndərmək('java 창예제\n'.encode())
                받기('GUI 예제 Hazırla: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_yaz)
                göndərmək(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                hesabat_VALUE['suspended_java_ps'] = örtük('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', hesabat_VALUE['suspended_java_ps']), hesabat_VALUE['suspended_java_ps']
                hesabat_VALUE['top'] = örtük('top -n 1')
                assert 'java 창예제' in hesabat_VALUE['top'] and 'kernel/shell' in hesabat_VALUE['top']
                hesabat_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                hesabat_VALUE['network_trace'] = körpü_VALUE.iz_LOG
                assert not körpü_VALUE.XƏTA, körpü_VALUE.XƏTA
                göndərmək(b'poweroff\n')
                assert Proses_VALUE.wait(timeout=15) == 0
                hesabat_VALUE['passed'] = True
            CHOOSE_element.close()
    except Exception as XƏTA:
        hesabat_VALUE['error'] = str(XƏTA)
        raise
    finally:
        if Proses_VALUE is not None and Proses_VALUE.poll() is None:
            Proses_VALUE.terminate()
            try:
                Proses_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proses_VALUE.kill()
                Proses_VALUE.wait()
        (출력 / 'serial.log').write_bytes(LOG_yaz)
        (출력 / 'report.json').write_text(json.dumps(hesabat_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Açar_VALUE: hesabat_VALUE[Açar_VALUE] for Açar_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    İcra_Et()
