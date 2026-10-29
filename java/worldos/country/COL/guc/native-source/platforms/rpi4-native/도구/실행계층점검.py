#!/usr/bin/env python3
"""QEMU의 실제 CPU 권한, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from 실행 import 기준, aluwataaya
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def 시작():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    achikiimaajatü_ajutuu = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    원문들 = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'kusu_cheeke': '''import java.net.*;
public class kusu_cheeke {
 public static void main(String[] 인수) throws Exception {
  Socket a_ataa = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  a_ataa.setSoTimeout(3000);
  byte[] 글 = "TCP 한글\\n".getBytes("UTF-8");
  a_ataa.getOutputStream().write(글);
  for (int 자리 = 0; 자리 < 글.length; 자리++)
   if (a_ataa.getInputStream().read() != (글[자리] & 255)) throw new RuntimeException("TCP mismatch");
  a_ataa.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  글 = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(글, 글.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] 응답 = new byte[64]; DatagramPacket 전문 = new DatagramPacket(응답, 응답.length);
  종단.receive(전문);
  if (전문.getLength() != 글.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < 글.length; 자리++)
   if (응답[자리] != 글[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); 서버.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket a_ataa = 서버.accept(); a_ataa.setSoTimeout(5000);
  a_ataa.getOutputStream().write(a_ataa.getInputStream().read() + 1);
  a_ataa.close(); 서버.close();
  byte[] atijaaya = new byte[64]; DatagramPacket 전문 = new DatagramPacket(atijaaya, atijaaya.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for 이름, eejeejetülein in 원문들.items():
        (출력 / (이름 + '.java')).write_text(eejeejetülein, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (이름 + '.java')) for 이름 in 원문들])
    aa_innachikimaajatü_aparatsee = bytearray()
    def 빈접속번호(유형=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, 유형) as Achajaaya_ajutuu:
            Achajaaya_ajutuu.bind(('127.0.0.4', 0))
            return Achajaaya_ajutuu.getsockname()[1]
    파일접속번호, Pürotokoola_Aa_inmajia_Alatiriaa_outtülee, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    과정 = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(Pürotokoola_Aa_inmajia_Alatiriaa_outtülee), 'udp:{}:9301'.format(전문접속번호)],
                포착여부=True, epiajatü_ejepüsee='127.0.0.4') as 다리:
            aa_inmajia_wopu_a_ttaaleemüin = Path(임시) / 'qmp.sock'
            과정 = subprocess.Popen(aluwataaya() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(aa_inmajia_wopu_a_ttaaleemüin)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            aapawaa_apüshii = selectors.DefaultSelector()
            aapawaa_apüshii.register(과정.stdout, selectors.EVENT_READ)
            def 받기(표시=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while 표시 not in aa_innachikimaajatü_aparatsee[처음:]:
                    if time.monotonic() > 끝 or 과정.poll() is not None:
                        raise AssertionError('Missing ' + repr(표시) + '\n' + aa_innachikimaajatü_aparatsee[처음:].decode('utf-8', 'replace'))
                    for ajüttia_ajutuu, _ in aapawaa_apüshii.select(.05):
                        조각 = ajüttia_ajutuu.fileobj.read(65536)
                        if 조각:
                            aa_innachikimaajatü_aparatsee.extend(조각)
                return aa_innachikimaajatü_aparatsee[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def ajütaa(atijaaya):
                과정.stdin.write(atijaaya)
                과정.stdin.flush()
            def aluwataalapu_u(글):
                print(글, flush=True)
                처음 = len(aa_innachikimaajatü_aparatsee)
                ajütaa((글 + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as aa_inmajia_ajutuu:
                aa_inmajia_ajutuu.settimeout(10)
                aa_inmajia_ajutuu.connect(str(aa_inmajia_wopu_a_ttaaleemüin))
                palantüsü_ajutuu = aa_inmajia_ajutuu.makefile('rwb')
                json.loads(palantüsü_ajutuu.readline())
                def 요청(aluwataaya_ajutuu, 인수=None):
                    atijaaya = {'execute': aluwataaya_ajutuu}
                    if 인수 is not None:
                        atijaaya['arguments'] = 인수
                    palantüsü_ajutuu.write((json.dumps(atijaaya) + '\n').encode())
                    palantüsü_ajutuu.flush()
                    while True:
                        응답 = json.loads(palantüsü_ajutuu.readline())
                        if 'error' in 응답:
                            raise AssertionError(응답)
                        if 'return' in 응답:
                            return 응답['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                achikiimaajatü_ajutuu['shell_cpu'] = 권한읽기()
                assert 'EL1h' in achikiimaajatü_ajutuu['shell_cpu'], achikiimaajatü_ajutuu['shell_cpu']
                achikiimaajatü_ajutuu['initial_ps'] = aluwataalapu_u('ps')
                assert 'kernel/shell' in achikiimaajatü_ajutuu['initial_ps']
                achikiimaajatü_ajutuu['ipconfig'] = aluwataalapu_u('ipconfig')
                assert 'inet 10.0.2.15' in achikiimaajatü_ajutuu['ipconfig']
                achikiimaajatü_ajutuu['gateway_ping'] = aluwataalapu_u('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in achikiimaajatü_ajutuu['gateway_ping']
                assert 'FTP listening' in aluwataalapu_u('ftpd start')
                with ftplib.FTP() as alate_eraa_ajutuu:
                    alate_eraa_ajutuu.encoding = 'utf-8'
                    alate_eraa_ajutuu.connect('127.0.0.4', 파일접속번호, timeout=20)
                    alate_eraa_ajutuu.login()
                    for 이름 in 원문들:
                        alate_eraa_ajutuu.storbinary('STOR ' + 이름 + '.class', io.BytesIO((출력 / (이름 + '.class')).read_bytes()))
                처음 = len(aa_innachikimaajatü_aparatsee)
                ajütaa('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    achikiimaajatü_ajutuu['java_cpu'] = 권한읽기()
                    if 'EL0t' in achikiimaajatü_ajutuu['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in achikiimaajatü_ajutuu['java_cpu'], achikiimaajatü_ajutuu['java_cpu']
                받기(처음=처음)
                achikiimaajatü_ajutuu['after_exit_ps'] = aluwataalapu_u('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', achikiimaajatü_ajutuu['after_exit_ps'])
                achikiimaajatü_ajutuu['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as wanaawasü_ajutuu:
                    글 = aluwataalapu_u('java kusu_cheeke {} {}'.format(wanaawasü_ajutuu.Pürotokoola_Aa_inmajia_Alatiriaa_outtülee, wanaawasü_ajutuu.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in 글 and 'exit 0' in 글, 글
                    assert wanaawasü_ajutuu.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, wanaawasü_ajutuu.수신됨
                    assert not wanaawasü_ajutuu.오류들, wanaawasü_ajutuu.오류들
                    achikiimaajatü_ajutuu['outbound_peers'] = {종류: atijaaya.decode() for 종류, atijaaya in wanaawasü_ajutuu.수신됨.items()}
                처음 = len(aa_innachikimaajatü_aparatsee)
                ajütaa('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', Pürotokoola_Aa_inmajia_Alatiriaa_outtülee), timeout=5) as wanaawasü_ajutuu:
                    wanaawasü_ajutuu.sendall(b'A')
                    assert wanaawasü_ajutuu.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as wanaawasü_ajutuu:
                    wanaawasü_ajutuu.settimeout(5)
                    wanaawasü_ajutuu.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert wanaawasü_ajutuu.recvfrom(64)[0] == b'UDP-IN'
                글 = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in 글 and 'exit 0' in 글, 글
                achikiimaajatü_ajutuu['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in aluwataalapu_u('terminal')
                aluwataalapu_u('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(aa_innachikimaajatü_aparatsee)
                ajütaa('java 창예제\n'.encode())
                받기('GUI 예제 준비: 창예제\r\n'.encode(), 처음)
                처음 = len(aa_innachikimaajatü_aparatsee)
                ajütaa(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                achikiimaajatü_ajutuu['suspended_java_ps'] = aluwataalapu_u('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', achikiimaajatü_ajutuu['suspended_java_ps']), achikiimaajatü_ajutuu['suspended_java_ps']
                achikiimaajatü_ajutuu['top'] = aluwataalapu_u('top -n 1')
                assert 'java 창예제' in achikiimaajatü_ajutuu['top'] and 'kernel/shell' in achikiimaajatü_ajutuu['top']
                achikiimaajatü_ajutuu['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                achikiimaajatü_ajutuu['network_trace'] = 다리.추적기록
                assert not 다리.ajachitia, 다리.ajachitia
                ajütaa(b'poweroff\n')
                assert 과정.wait(timeout=15) == 0
                achikiimaajatü_ajutuu['passed'] = True
            aapawaa_apüshii.close()
    except Exception as ajachitia:
        achikiimaajatü_ajutuu['error'] = str(ajachitia)
        raise
    finally:
        if 과정 is not None and 과정.poll() is None:
            과정.terminate()
            try:
                과정.wait(timeout=10)
            except subprocess.TimeoutExpired:
                과정.kill()
                과정.wait()
        (출력 / 'serial.log').write_bytes(aa_innachikimaajatü_aparatsee)
        (출력 / 'report.json').write_text(json.dumps(achikiimaajatü_ajutuu, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({ajüttia_ajutuu: achikiimaajatü_ajutuu[ajüttia_ajutuu] for ajüttia_ajutuu in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    시작()
