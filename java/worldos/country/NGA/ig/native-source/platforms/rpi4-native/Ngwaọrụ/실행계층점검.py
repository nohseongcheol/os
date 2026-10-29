#!/usr/bin/env python3
"""QEMU의 ǹdịnezie_datà CPU ikikere_valuu, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from mee_nnyemiwu import 기준, Ntiiwu
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def Bido():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    akụkọ_valuu = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    ebensìbịa_Ndi_ọbọakwụkwọ = {
        'ikikere_cheèk': '''public class ikikere_cheèk {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Netwọọkụ_cheèk': '''import java.net.*;
public class Netwọọkụ_cheèk {
 public static void main(String[] 인수) throws Exception {
  Socket Banye = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Banye.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  Banye.getOutputStream().write(SMS);
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (Banye.getInputStream().read() != (SMS[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Banye.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] nzaghachi = new byte[64]; DatagramPacket 전문 = new DatagramPacket(nzaghachi, nzaghachi.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (nzaghachi[자리] != SMS[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket savà_valuu = new ServerSocket(9300); savà_valuu.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Banye = savà_valuu.accept(); Banye.setSoTimeout(5000);
  Banye.getOutputStream().write(Banye.getInputStream().read() + 1);
  Banye.close(); savà_valuu.close();
  byte[] datà = new byte[64]; DatagramPacket 전문 = new DatagramPacket(datà, datà.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Aha, ebensìbịa in ebensìbịa_Ndi_ọbọakwụkwọ.items():
        (출력 / (Aha + '.java')).write_text(ebensìbịa, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Aha + '.java')) for Aha in ebensìbịa_Ndi_ọbọakwụkwọ])
    ndekọ_NDEKỌ = bytearray()
    def 빈접속번호(pinye_otu=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, pinye_otu) as Chọọ_valuu:
            Chọọ_valuu.bind(('127.0.0.4', 0))
            return Chọọ_valuu.getsockname()[1]
    파일접속번호, TCP_pọọt, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    ùsòrò_valuu_6712bde7 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_pọọt), 'udp:{}:9301'.format(전문접속번호)],
                See=True, usu_àdreèsì='127.0.0.4') as 다리:
            njizi_ụzọ_ozi = Path(임시) / 'qmp.sock'
            ùsòrò_valuu_6712bde7 = subprocess.Popen(Ntiiwu() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(njizi_ụzọ_ozi)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            họrọ_ihe = selectors.DefaultSelector()
            họrọ_ihe.register(ùsòrò_valuu_6712bde7.stdout, selectors.EVENT_READ)
            def 받기(gòsi_valuu=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while gòsi_valuu not in ndekọ_NDEKỌ[처음:]:
                    if time.monotonic() > 끝 or ùsòrò_valuu_6712bde7.poll() is not None:
                        raise AssertionError('Missing ' + repr(gòsi_valuu) + '\n' + ndekọ_NDEKỌ[처음:].decode('utf-8', 'replace'))
                    for ọtụgwo_valuu, _ in họrọ_ihe.select(.05):
                        조각 = ọtụgwo_valuu.fileobj.read(65536)
                        if 조각:
                            ndekọ_NDEKỌ.extend(조각)
                return ndekọ_NDEKỌ[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def zìga(datà):
                ùsòrò_valuu_6712bde7.stdin.write(datà)
                ùsòrò_valuu_6712bde7.stdin.flush()
            def nkọwannyemiwu(SMS):
                print(SMS, flush=True)
                처음 = len(ndekọ_NDEKỌ)
                zìga((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as njizi_valuu:
                njizi_valuu.settimeout(10)
                njizi_valuu.connect(str(njizi_ụzọ_ozi))
                agịrị_valuu = njizi_valuu.makefile('rwb')
                json.loads(agịrị_valuu.readline())
                def 요청(okwunkụzi_valuu, 인수=None):
                    datà = {'execute': okwunkụzi_valuu}
                    if 인수 is not None:
                        datà['arguments'] = 인수
                    agịrị_valuu.write((json.dumps(datà) + '\n').encode())
                    agịrị_valuu.flush()
                    while True:
                        nzaghachi = json.loads(agịrị_valuu.readline())
                        if 'error' in nzaghachi:
                            raise AssertionError(nzaghachi)
                        if 'return' in nzaghachi:
                            return nzaghachi['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                akụkọ_valuu['shell_cpu'] = 권한읽기()
                assert 'EL1h' in akụkọ_valuu['shell_cpu'], akụkọ_valuu['shell_cpu']
                akụkọ_valuu['initial_ps'] = nkọwannyemiwu('ps')
                assert 'kernel/shell' in akụkọ_valuu['initial_ps']
                akụkọ_valuu['ipconfig'] = nkọwannyemiwu('ipconfig')
                assert 'inet 10.0.2.15' in akụkọ_valuu['ipconfig']
                akụkọ_valuu['gateway_ping'] = nkọwannyemiwu('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in akụkọ_valuu['gateway_ping']
                assert 'FTP listening' in nkọwannyemiwu('ftpd start')
                with ftplib.FTP() as dògharịa_valuu:
                    dògharịa_valuu.encoding = 'utf-8'
                    dògharịa_valuu.connect('127.0.0.4', 파일접속번호, timeout=20)
                    dògharịa_valuu.login()
                    for Aha in ebensìbịa_Ndi_ọbọakwụkwọ:
                        dògharịa_valuu.storbinary('STOR ' + Aha + '.class', io.BytesIO((출력 / (Aha + '.class')).read_bytes()))
                처음 = len(ndekọ_NDEKỌ)
                zìga('java ikikere_cheèk\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    akụkọ_valuu['java_cpu'] = 권한읽기()
                    if 'EL0t' in akụkọ_valuu['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in akụkọ_valuu['java_cpu'], akụkọ_valuu['java_cpu']
                받기(처음=처음)
                akụkọ_valuu['after_exit_ps'] = nkọwannyemiwu('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', akụkọ_valuu['after_exit_ps'])
                akụkọ_valuu['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as ibè_valuu:
                    SMS = nkọwannyemiwu('java Netwọọkụ_cheèk {} {}'.format(ibè_valuu.TCP_pọọt, ibè_valuu.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert ibè_valuu.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, ibè_valuu.수신됨
                    assert not ibè_valuu.오류들, ibè_valuu.오류들
                    akụkọ_valuu['outbound_peers'] = {종류: datà.decode() for 종류, datà in ibè_valuu.수신됨.items()}
                처음 = len(ndekọ_NDEKỌ)
                zìga('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_pọọt), timeout=5) as ibè_valuu:
                    ibè_valuu.sendall(b'A')
                    assert ibè_valuu.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ibè_valuu:
                    ibè_valuu.settimeout(5)
                    ibè_valuu.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert ibè_valuu.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                akụkọ_valuu['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in nkọwannyemiwu('terminal')
                nkọwannyemiwu('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ndekọ_NDEKỌ)
                zìga('java 창예제\n'.encode())
                받기('GUI 예제 Kwado: 창예제\r\n'.encode(), 처음)
                처음 = len(ndekọ_NDEKỌ)
                zìga(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                akụkọ_valuu['suspended_java_ps'] = nkọwannyemiwu('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', akụkọ_valuu['suspended_java_ps']), akụkọ_valuu['suspended_java_ps']
                akụkọ_valuu['top'] = nkọwannyemiwu('top -n 1')
                assert 'java 창예제' in akụkọ_valuu['top'] and 'kernel/shell' in akụkọ_valuu['top']
                akụkọ_valuu['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                akụkọ_valuu['network_trace'] = 다리.추적기록
                assert not 다리.mmejọ, 다리.mmejọ
                zìga(b'poweroff\n')
                assert ùsòrò_valuu_6712bde7.wait(timeout=15) == 0
                akụkọ_valuu['passed'] = True
            họrọ_ihe.close()
    except Exception as mmejọ:
        akụkọ_valuu['error'] = str(mmejọ)
        raise
    finally:
        if ùsòrò_valuu_6712bde7 is not None and ùsòrò_valuu_6712bde7.poll() is None:
            ùsòrò_valuu_6712bde7.terminate()
            try:
                ùsòrò_valuu_6712bde7.wait(timeout=10)
            except subprocess.TimeoutExpired:
                ùsòrò_valuu_6712bde7.kill()
                ùsòrò_valuu_6712bde7.wait()
        (출력 / 'serial.log').write_bytes(ndekọ_NDEKỌ)
        (출력 / 'report.json').write_text(json.dumps(akụkọ_valuu, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ọtụgwo_valuu: akụkọ_valuu[ọtụgwo_valuu] for ọtụgwo_valuu in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Bido()
