#!/usr/bin/env python3
"""QEMU의 raun_gögn CPU leyfi_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from keyra_skipun import verk_rót, Skipun
from Net_brú import Net_brú
from 되돌림시험서버 import 되돌림시험서버


def Keyra_2():
    úttak = verk_rót / 'build/verification/execution-network-review'
    úttak.mkdir(parents=True, exist_ok=True)
    skrá_VALUE_ddf2aaf3 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((verk_rót / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    uppruni_Skrár = {
        'heimild_athuga': '''public class heimild_athuga {
 public static void main(String[] Viðföng) {
  System.out.println("EL0_PROBE_READY");
  int númer = 0; while (true) { númer++; }
 }
}''',
        'Net_athuga': '''import java.net.*;
public class Net_athuga {
 public static void main(String[] Viðföng) throws Exception {
  Socket Tengjast = new Socket("10.0.2.2", Integer.parseInt(Viðföng[0]));
  Tengjast.setSoTimeout(3000);
  byte[] Texti = "TCP 한글\\n".getBytes("UTF-8");
  Tengjast.getOutputStream().write(Texti);
  for (int staða_INDEX = 0; staða_INDEX < Texti.length; staða_INDEX++)
   if (Tengjast.getInputStream().read() != (Texti[staða_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Tengjast.close();
  DatagramSocket endastöð = new DatagramSocket(); endastöð.setSoTimeout(3000);
  Texti = "UDP 한글".getBytes("UTF-8");
  endastöð.send(new DatagramPacket(Texti, Texti.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Viðföng[1])));
  byte[] svara = new byte[64]; DatagramPacket 전문 = new DatagramPacket(svara, svara.length);
  endastöð.receive(전문);
  if (전문.getLength() != Texti.length) throw new RuntimeException("UDP length");
  for (int staða_INDEX = 0; staða_INDEX < Texti.length; staða_INDEX++)
   if (svara[staða_INDEX] != Texti[staða_INDEX]) throw new RuntimeException("UDP mismatch");
  endastöð.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Viðföng) throws Exception {
  ServerSocket þjónn_VALUE = new ServerSocket(9300); þjónn_VALUE.setSoTimeout(5000);
  DatagramSocket endastöð = new DatagramSocket(9301); endastöð.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Tengjast = þjónn_VALUE.accept(); Tengjast.setSoTimeout(5000);
  Tengjast.getOutputStream().write(Tengjast.getInputStream().read() + 1);
  Tengjast.close(); þjónn_VALUE.close();
  byte[] gögn = new byte[64]; DatagramPacket 전문 = new DatagramPacket(gögn, gögn.length);
  endastöð.receive(전문); endastöð.send(전문); endastöð.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Heiti, Uppruni in uppruni_Skrár.items():
        (úttak / (Heiti + '.java')).write_text(Uppruni, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(úttak)] +
                          [str(úttak / (Heiti + '.java')) for Heiti in uppruni_Skrár])
    LOG_lína = bytearray()
    def autt_tengisnúmer(TYPE_tegund=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_tegund) as Leit_VALUE:
            Leit_VALUE.bind(('127.0.0.4', 0))
            return Leit_VALUE.getsockname()[1]
    skrá_tengisnúmer, TCP_gátt, UDP_gátt = autt_tengisnúmer(), autt_tengisnúmer(), autt_tengisnúmer(socket.SOCK_DGRAM)
    Ferli_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Net_brú(
                skrá_tengisnúmer, ['tcp:{}:9300'.format(TCP_gátt), 'udp:{}:9301'.format(UDP_gátt)],
                fanga=True, hýsa_slóð='127.0.0.4') as brú_VALUE:
            stýring_slóð = Path(임시) / 'qmp.sock'
            Ferli_VALUE = subprocess.Popen(Skipun() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(stýring_slóð)] + brú_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            velja_vara = selectors.DefaultSelector()
            velja_vara.register(Ferli_VALUE.stdout, selectors.EVENT_READ)
            def 받기(sýna_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while sýna_VALUE not in LOG_lína[처음:]:
                    if time.monotonic() > 끝 or Ferli_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(sýna_VALUE) + '\n' + LOG_lína[처음:].decode('utf-8', 'replace'))
                    for Lykill_VALUE, _ in velja_vara.select(.05):
                        조각 = Lykill_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_lína.extend(조각)
                return LOG_lína[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def senda(gögn):
                Ferli_VALUE.stdin.write(gögn)
                Ferli_VALUE.stdin.flush()
            def skel(Texti):
                print(Texti, flush=True)
                처음 = len(LOG_lína)
                senda((Texti + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as stýring_VALUE:
                stýring_VALUE.settimeout(10)
                stýring_VALUE.connect(str(stýring_slóð))
                Stream_VALUE = stýring_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def 요청(skipun_VALUE, Viðföng=None):
                    gögn = {'execute': skipun_VALUE}
                    if Viðföng is not None:
                        gögn['arguments'] = Viðföng
                    Stream_VALUE.write((json.dumps(gögn) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        svara = json.loads(Stream_VALUE.readline())
                        if 'error' in svara:
                            raise AssertionError(svara)
                        if 'return' in svara:
                            return svara['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                skrá_VALUE_ddf2aaf3['shell_cpu'] = 권한읽기()
                assert 'EL1h' in skrá_VALUE_ddf2aaf3['shell_cpu'], skrá_VALUE_ddf2aaf3['shell_cpu']
                skrá_VALUE_ddf2aaf3['initial_ps'] = skel('ps')
                assert 'kernel/shell' in skrá_VALUE_ddf2aaf3['initial_ps']
                skrá_VALUE_ddf2aaf3['ipconfig'] = skel('ipconfig')
                assert 'inet 10.0.2.15' in skrá_VALUE_ddf2aaf3['ipconfig']
                skrá_VALUE_ddf2aaf3['gateway_ping'] = skel('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in skrá_VALUE_ddf2aaf3['gateway_ping']
                assert 'FTP listening' in skel('ftpd start')
                with ftplib.FTP() as flytja_VALUE:
                    flytja_VALUE.encoding = 'utf-8'
                    flytja_VALUE.connect('127.0.0.4', skrá_tengisnúmer, timeout=20)
                    flytja_VALUE.login()
                    for Heiti in uppruni_Skrár:
                        flytja_VALUE.storbinary('STOR ' + Heiti + '.class', io.BytesIO((úttak / (Heiti + '.class')).read_bytes()))
                처음 = len(LOG_lína)
                senda('java heimild_athuga\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    skrá_VALUE_ddf2aaf3['java_cpu'] = 권한읽기()
                    if 'EL0t' in skrá_VALUE_ddf2aaf3['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in skrá_VALUE_ddf2aaf3['java_cpu'], skrá_VALUE_ddf2aaf3['java_cpu']
                받기(처음=처음)
                skrá_VALUE_ddf2aaf3['after_exit_ps'] = skel('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', skrá_VALUE_ddf2aaf3['after_exit_ps'])
                skrá_VALUE_ddf2aaf3['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as jafningi_VALUE:
                    Texti = skel('java Net_athuga {} {}'.format(jafningi_VALUE.TCP_gátt, jafningi_VALUE.UDP_gátt))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Texti and 'exit 0' in Texti, Texti
                    assert jafningi_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, jafningi_VALUE.수신됨
                    assert not jafningi_VALUE.오류들, jafningi_VALUE.오류들
                    skrá_VALUE_ddf2aaf3['outbound_peers'] = {종류: gögn.decode() for 종류, gögn in jafningi_VALUE.수신됨.items()}
                처음 = len(LOG_lína)
                senda('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_gátt), timeout=5) as jafningi_VALUE:
                    jafningi_VALUE.sendall(b'A')
                    assert jafningi_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as jafningi_VALUE:
                    jafningi_VALUE.settimeout(5)
                    jafningi_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_gátt))
                    assert jafningi_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Texti = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Texti and 'exit 0' in Texti, Texti
                skrá_VALUE_ddf2aaf3['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in skel('terminal')
                skel('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_lína)
                senda('java Gluggadæmi\n'.encode())
                받기('GUI 예제 Undirbúa: Gluggadæmi\r\n'.encode(), 처음)
                처음 = len(LOG_lína)
                senda(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                skrá_VALUE_ddf2aaf3['suspended_java_ps'] = skel('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java Gluggadæmi', skrá_VALUE_ddf2aaf3['suspended_java_ps']), skrá_VALUE_ddf2aaf3['suspended_java_ps']
                skrá_VALUE_ddf2aaf3['top'] = skel('top -n 1')
                assert 'java Gluggadæmi' in skrá_VALUE_ddf2aaf3['top'] and 'kernel/shell' in skrá_VALUE_ddf2aaf3['top']
                skrá_VALUE_ddf2aaf3['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                skrá_VALUE_ddf2aaf3['network_trace'] = brú_VALUE.spor_LOG
                assert not brú_VALUE.Villa, brú_VALUE.Villa
                senda(b'poweroff\n')
                assert Ferli_VALUE.wait(timeout=15) == 0
                skrá_VALUE_ddf2aaf3['passed'] = True
            velja_vara.close()
    except Exception as Villa:
        skrá_VALUE_ddf2aaf3['error'] = str(Villa)
        raise
    finally:
        if Ferli_VALUE is not None and Ferli_VALUE.poll() is None:
            Ferli_VALUE.terminate()
            try:
                Ferli_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Ferli_VALUE.kill()
                Ferli_VALUE.wait()
        (úttak / 'serial.log').write_bytes(LOG_lína)
        (úttak / 'report.json').write_text(json.dumps(skrá_VALUE_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Lykill_VALUE: skrá_VALUE_ddf2aaf3[Lykill_VALUE] for Lykill_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Keyra_2()
