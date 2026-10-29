#!/usr/bin/env python3
"""QEMU의 iarbhír_sonraí CPU cead_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Rith_ordú import teilgean_fréamh, Ordú
from Líonra_traschóiritheoir import Líonra_traschóiritheoir
from 되돌림시험서버 import 되돌림시험서버


def Rith_2():
    Aschur = teilgean_fréamh / 'build/verification/execution-network-review'
    Aschur.mkdir(parents=True, exist_ok=True)
    tuairisc_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((teilgean_fréamh / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    foinse_Comhaid = {
        'cead_seic': '''public class cead_seic {
 public static void main(String[] Argóintí) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Líonra_seic': '''import java.net.*;
public class Líonra_seic {
 public static void main(String[] Argóintí) throws Exception {
  Socket Nasc = new Socket("10.0.2.2", Integer.parseInt(Argóintí[0]));
  Nasc.setSoTimeout(3000);
  byte[] Téacs = "TCP 한글\\n".getBytes("UTF-8");
  Nasc.getOutputStream().write(Téacs);
  for (int suíomh_INDEX = 0; suíomh_INDEX < Téacs.length; suíomh_INDEX++)
   if (Nasc.getInputStream().read() != (Téacs[suíomh_INDEX] & 255)) throw new RuntimeException("TCP mismatch");
  Nasc.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Téacs = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Téacs, Téacs.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argóintí[1])));
  byte[] freagair = new byte[64]; DatagramPacket 전문 = new DatagramPacket(freagair, freagair.length);
  종단.receive(전문);
  if (전문.getLength() != Téacs.length) throw new RuntimeException("UDP length");
  for (int suíomh_INDEX = 0; suíomh_INDEX < Téacs.length; suíomh_INDEX++)
   if (freagair[suíomh_INDEX] != Téacs[suíomh_INDEX]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Argóintí) throws Exception {
  ServerSocket freastalaí_VALUE = new ServerSocket(9300); freastalaí_VALUE.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Nasc = freastalaí_VALUE.accept(); Nasc.setSoTimeout(5000);
  Nasc.getOutputStream().write(Nasc.getInputStream().read() + 1);
  Nasc.close(); freastalaí_VALUE.close();
  byte[] sonraí = new byte[64]; DatagramPacket 전문 = new DatagramPacket(sonraí, sonraí.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ainm, FOINSE in foinse_Comhaid.items():
        (Aschur / (Ainm + '.java')).write_text(FOINSE, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Aschur)] +
                          [str(Aschur / (Ainm + '.java')) for Ainm in foinse_Comhaid])
    LOG_ró = bytearray()
    def folamh_uimhir_phoirt(TYPE_catagóir=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_catagóir) as SEARCH_VALUE:
            SEARCH_VALUE.bind(('127.0.0.4', 0))
            return SEARCH_VALUE.getsockname()[1]
    comhad_uimhir_phoirt, TCP_port, UDP_port = folamh_uimhir_phoirt(), folamh_uimhir_phoirt(), folamh_uimhir_phoirt(socket.SOCK_DGRAM)
    Próiseas_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Líonra_traschóiritheoir(
                comhad_uimhir_phoirt, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                taifead=True, óstach_ADDRESS='127.0.0.4') as traschóiritheoir_VALUE:
            rialú_cosán = Path(임시) / 'qmp.sock'
            Próiseas_VALUE = subprocess.Popen(Ordú() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(rialú_cosán)] + traschóiritheoir_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_mír = selectors.DefaultSelector()
            CHOOSE_mír.register(Próiseas_VALUE.stdout, selectors.EVENT_READ)
            def 받기(seó_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while seó_VALUE not in LOG_ró[처음:]:
                    if time.monotonic() > 끝 or Próiseas_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(seó_VALUE) + '\n' + LOG_ró[처음:].decode('utf-8', 'replace'))
                    for eochair_VALUE, _ in CHOOSE_mír.select(.05):
                        조각 = eochair_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_ró.extend(조각)
                return LOG_ró[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def seol(sonraí):
                Próiseas_VALUE.stdin.write(sonraí)
                Próiseas_VALUE.stdin.flush()
            def blaosc(Téacs):
                print(Téacs, flush=True)
                처음 = len(LOG_ró)
                seol((Téacs + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as rialú_VALUE:
                rialú_VALUE.settimeout(10)
                rialú_VALUE.connect(str(rialú_cosán))
                sruth_VALUE = rialú_VALUE.makefile('rwb')
                json.loads(sruth_VALUE.readline())
                def iarratas_HTTP(treoir_VALUE, Argóintí=None):
                    sonraí = {'execute': treoir_VALUE}
                    if Argóintí is not None:
                        sonraí['arguments'] = Argóintí
                    sruth_VALUE.write((json.dumps(sonraí) + '\n').encode())
                    sruth_VALUE.flush()
                    while True:
                        freagair = json.loads(sruth_VALUE.readline())
                        if 'error' in freagair:
                            raise AssertionError(freagair)
                        if 'return' in freagair:
                            return freagair['return']
                iarratas_HTTP('qmp_capabilities')
                def 권한읽기():
                    iarratas_HTTP('stop')
                    try:
                        return iarratas_HTTP('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        iarratas_HTTP('cont')
                tuairisc_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in tuairisc_VALUE['shell_cpu'], tuairisc_VALUE['shell_cpu']
                tuairisc_VALUE['initial_ps'] = blaosc('ps')
                assert 'kernel/shell' in tuairisc_VALUE['initial_ps']
                tuairisc_VALUE['ipconfig'] = blaosc('ipconfig')
                assert 'inet 10.0.2.15' in tuairisc_VALUE['ipconfig']
                tuairisc_VALUE['gateway_ping'] = blaosc('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in tuairisc_VALUE['gateway_ping']
                assert 'FTP listening' in blaosc('ftpd start')
                with ftplib.FTP() as traschur_VALUE:
                    traschur_VALUE.encoding = 'utf-8'
                    traschur_VALUE.connect('127.0.0.4', comhad_uimhir_phoirt, timeout=20)
                    traschur_VALUE.login()
                    for Ainm in foinse_Comhaid:
                        traschur_VALUE.storbinary('STOR ' + Ainm + '.class', io.BytesIO((Aschur / (Ainm + '.class')).read_bytes()))
                처음 = len(LOG_ró)
                seol('java cead_seic\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    tuairisc_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in tuairisc_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in tuairisc_VALUE['java_cpu'], tuairisc_VALUE['java_cpu']
                받기(처음=처음)
                tuairisc_VALUE['after_exit_ps'] = blaosc('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', tuairisc_VALUE['after_exit_ps'])
                tuairisc_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as piara_VALUE:
                    Téacs = blaosc('java Líonra_seic {} {}'.format(piara_VALUE.TCP_port, piara_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Téacs and 'exit 0' in Téacs, Téacs
                    assert piara_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, piara_VALUE.수신됨
                    assert not piara_VALUE.오류들, piara_VALUE.오류들
                    tuairisc_VALUE['outbound_peers'] = {종류: sonraí.decode() for 종류, sonraí in piara_VALUE.수신됨.items()}
                처음 = len(LOG_ró)
                seol('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as piara_VALUE:
                    piara_VALUE.sendall(b'A')
                    assert piara_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as piara_VALUE:
                    piara_VALUE.settimeout(5)
                    piara_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert piara_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Téacs = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Téacs and 'exit 0' in Téacs, Téacs
                tuairisc_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in blaosc('terminal')
                blaosc('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_ró)
                seol('java 창예제\n'.encode())
                받기('GUI 예제 Ullmhaigh: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_ró)
                seol(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                tuairisc_VALUE['suspended_java_ps'] = blaosc('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', tuairisc_VALUE['suspended_java_ps']), tuairisc_VALUE['suspended_java_ps']
                tuairisc_VALUE['top'] = blaosc('top -n 1')
                assert 'java 창예제' in tuairisc_VALUE['top'] and 'kernel/shell' in tuairisc_VALUE['top']
                tuairisc_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                tuairisc_VALUE['network_trace'] = traschóiritheoir_VALUE.rian_LOG
                assert not traschóiritheoir_VALUE.ERREÁID, traschóiritheoir_VALUE.ERREÁID
                seol(b'poweroff\n')
                assert Próiseas_VALUE.wait(timeout=15) == 0
                tuairisc_VALUE['passed'] = True
            CHOOSE_mír.close()
    except Exception as ERREÁID:
        tuairisc_VALUE['error'] = str(ERREÁID)
        raise
    finally:
        if Próiseas_VALUE is not None and Próiseas_VALUE.poll() is None:
            Próiseas_VALUE.terminate()
            try:
                Próiseas_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Próiseas_VALUE.kill()
                Próiseas_VALUE.wait()
        (Aschur / 'serial.log').write_bytes(LOG_ró)
        (Aschur / 'report.json').write_text(json.dumps(tuairisc_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({eochair_VALUE: tuairisc_VALUE[eochair_VALUE] for eochair_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Rith_2()
