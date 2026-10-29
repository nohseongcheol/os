#!/usr/bin/env python3
"""QEMU의 liteew_mbir CPU sañ_sañ_xëyma, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from def_ndigel import 기준, ndigel
from mbaal_poŋ import mbaal_poŋ
from 되돌림시험서버 import 되돌림시험서버


def daw():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    tënk_xëyma = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    Cosaan_Fisiye_yi = {
        '권한점검': '''public class 권한점검 {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'mbaal_sek': '''import java.net.*;
public class mbaal_sek {
 public static void main(String[] 인수) throws Exception {
  Socket JOKKOO = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  JOKKOO.setSoTimeout(3000);
  byte[] Tekst = "TCP 한글\\n".getBytes("UTF-8");
  JOKKOO.getOutputStream().write(Tekst);
  for (int 자리 = 0; 자리 < Tekst.length; 자리++)
   if (JOKKOO.getInputStream().read() != (Tekst[자리] & 255)) throw new RuntimeException("TCP mismatch");
  JOKKOO.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Tekst = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Tekst, Tekst.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] tontu = new byte[64]; DatagramPacket 전문 = new DatagramPacket(tontu, tontu.length);
  종단.receive(전문);
  if (전문.getLength() != Tekst.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Tekst.length; 자리++)
   if (tontu[자리] != Tekst[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket dëggu_xëyma = new ServerSocket(9300); dëggu_xëyma.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket JOKKOO = dëggu_xëyma.accept(); JOKKOO.setSoTimeout(5000);
  JOKKOO.getOutputStream().write(JOKKOO.getInputStream().read() + 1);
  JOKKOO.close(); dëggu_xëyma.close();
  byte[] mbir = new byte[64]; DatagramPacket 전문 = new DatagramPacket(mbir, mbir.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for tur_253d1510, Cosaan in Cosaan_Fisiye_yi.items():
        (출력 / (tur_253d1510 + '.java')).write_text(Cosaan, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (tur_253d1510 + '.java')) for tur_253d1510 in Cosaan_Fisiye_yi])
    làq_Dënk = bytearray()
    def 빈접속번호(xeet_ngiir=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, xeet_ngiir) as Wut_xëyma:
            Wut_xëyma.bind(('127.0.0.4', 0))
            return Wut_xëyma.getsockname()[1]
    파일접속번호, TCP_jël, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    yokkute_xëyma = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, mbaal_poŋ(
                파일접속번호, ['tcp:{}:9300'.format(TCP_jël), 'udp:{}:9301'.format(전문접속번호)],
                jël=True, dalal_dëkkuwaay='127.0.0.4') as poŋ_xëyma:
            Saytu_doxinu_ordinateur_Yoonu_jëmale = Path(임시) / 'qmp.sock'
            yokkute_xëyma = subprocess.Popen(ndigel() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(Saytu_doxinu_ordinateur_Yoonu_jëmale)] + poŋ_xëyma.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            Tànn_ëmbeef = selectors.DefaultSelector()
            Tànn_ëmbeef.register(yokkute_xëyma.stdout, selectors.EVENT_READ)
            def 받기(féeñal_xëyma=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while féeñal_xëyma not in làq_Dënk[처음:]:
                    if time.monotonic() > 끝 or yokkute_xëyma.poll() is not None:
                        raise AssertionError('Missing ' + repr(féeñal_xëyma) + '\n' + làq_Dënk[처음:].decode('utf-8', 'replace'))
                    for kër_xëyma, _ in Tànn_ëmbeef.select(.05):
                        조각 = kër_xëyma.fileobj.read(65536)
                        if 조각:
                            làq_Dënk.extend(조각)
                return làq_Dënk[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def Yónnee(mbir):
                yokkute_xëyma.stdin.write(mbir)
                yokkute_xëyma.stdin.flush()
            def Wëreef(Tekst):
                print(Tekst, flush=True)
                처음 = len(làq_Dënk)
                Yónnee((Tekst + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as Saytu_doxinu_ordinateur_xëyma:
                Saytu_doxinu_ordinateur_xëyma.settimeout(10)
                Saytu_doxinu_ordinateur_xëyma.connect(str(Saytu_doxinu_ordinateur_Yoonu_jëmale))
                dawal_xëyma = Saytu_doxinu_ordinateur_xëyma.makefile('rwb')
                json.loads(dawal_xëyma.readline())
                def 요청(ndigal_xëyma, 인수=None):
                    mbir = {'execute': ndigal_xëyma}
                    if 인수 is not None:
                        mbir['arguments'] = 인수
                    dawal_xëyma.write((json.dumps(mbir) + '\n').encode())
                    dawal_xëyma.flush()
                    while True:
                        tontu = json.loads(dawal_xëyma.readline())
                        if 'error' in tontu:
                            raise AssertionError(tontu)
                        if 'return' in tontu:
                            return tontu['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                tënk_xëyma['shell_cpu'] = 권한읽기()
                assert 'EL1h' in tënk_xëyma['shell_cpu'], tënk_xëyma['shell_cpu']
                tënk_xëyma['initial_ps'] = Wëreef('ps')
                assert 'kernel/shell' in tënk_xëyma['initial_ps']
                tënk_xëyma['ipconfig'] = Wëreef('ipconfig')
                assert 'inet 10.0.2.15' in tënk_xëyma['ipconfig']
                tënk_xëyma['gateway_ping'] = Wëreef('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in tënk_xëyma['gateway_ping']
                assert 'FTP listening' in Wëreef('ftpd start')
                with ftplib.FTP() as toxal_xëyma_630ba093:
                    toxal_xëyma_630ba093.encoding = 'utf-8'
                    toxal_xëyma_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    toxal_xëyma_630ba093.login()
                    for tur_253d1510 in Cosaan_Fisiye_yi:
                        toxal_xëyma_630ba093.storbinary('STOR ' + tur_253d1510 + '.class', io.BytesIO((출력 / (tur_253d1510 + '.class')).read_bytes()))
                처음 = len(làq_Dënk)
                Yónnee('java 권한점검\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    tënk_xëyma['java_cpu'] = 권한읽기()
                    if 'EL0t' in tënk_xëyma['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in tënk_xëyma['java_cpu'], tënk_xëyma['java_cpu']
                받기(처음=처음)
                tënk_xëyma['after_exit_ps'] = Wëreef('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', tënk_xëyma['after_exit_ps'])
                tënk_xëyma['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as Nàttangoo_xëyma:
                    Tekst = Wëreef('java mbaal_sek {} {}'.format(Nàttangoo_xëyma.TCP_jël, Nàttangoo_xëyma.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                    assert Nàttangoo_xëyma.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, Nàttangoo_xëyma.수신됨
                    assert not Nàttangoo_xëyma.오류들, Nàttangoo_xëyma.오류들
                    tënk_xëyma['outbound_peers'] = {종류: mbir.decode() for 종류, mbir in Nàttangoo_xëyma.수신됨.items()}
                처음 = len(làq_Dënk)
                Yónnee('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_jël), timeout=5) as Nàttangoo_xëyma:
                    Nàttangoo_xëyma.sendall(b'A')
                    assert Nàttangoo_xëyma.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Nàttangoo_xëyma:
                    Nàttangoo_xëyma.settimeout(5)
                    Nàttangoo_xëyma.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert Nàttangoo_xëyma.recvfrom(64)[0] == b'UDP-IN'
                Tekst = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekst and 'exit 0' in Tekst, Tekst
                tënk_xëyma['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Wëreef('terminal')
                Wëreef('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(làq_Dënk)
                Yónnee('java 창예제\n'.encode())
                받기('GUI 예제 jël_matuwaay: 창예제\r\n'.encode(), 처음)
                처음 = len(làq_Dënk)
                Yónnee(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                tënk_xëyma['suspended_java_ps'] = Wëreef('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', tënk_xëyma['suspended_java_ps']), tënk_xëyma['suspended_java_ps']
                tënk_xëyma['top'] = Wëreef('top -n 1')
                assert 'java 창예제' in tënk_xëyma['top'] and 'kernel/shell' in tënk_xëyma['top']
                tënk_xëyma['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                tënk_xëyma['network_trace'] = poŋ_xëyma.추적기록
                assert not poŋ_xëyma.njumte, poŋ_xëyma.njumte
                Yónnee(b'poweroff\n')
                assert yokkute_xëyma.wait(timeout=15) == 0
                tënk_xëyma['passed'] = True
            Tànn_ëmbeef.close()
    except Exception as njumte:
        tënk_xëyma['error'] = str(njumte)
        raise
    finally:
        if yokkute_xëyma is not None and yokkute_xëyma.poll() is None:
            yokkute_xëyma.terminate()
            try:
                yokkute_xëyma.wait(timeout=10)
            except subprocess.TimeoutExpired:
                yokkute_xëyma.kill()
                yokkute_xëyma.wait()
        (출력 / 'serial.log').write_bytes(làq_Dënk)
        (출력 / 'report.json').write_text(json.dumps(tënk_xëyma, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({kër_xëyma: tënk_xëyma[kër_xëyma] for kër_xëyma in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    daw()
