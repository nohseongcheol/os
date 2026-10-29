#!/usr/bin/env python3
"""QEMU의 ulwazi_ngokwenzekile_imininingwane CPU imvume_inani, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from yenza_umyalo import 기준, Umlayelo
from iNethiwekhi_ibhuloho import iNethiwekhi_ibhuloho
from 되돌림시험서버 import 되돌림시험서버


def Sebenzisa():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    umbiko_inani = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    umthombo_Amafayela = {
        'imvume_hlola': '''public class imvume_hlola {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'iNethiwekhi_hlola': '''import java.net.*;
public class iNethiwekhi_hlola {
 public static void main(String[] 인수) throws Exception {
  Socket Xhumanisa = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Xhumanisa.setSoTimeout(3000);
  byte[] Itekisi = "TCP 한글\\n".getBytes("UTF-8");
  Xhumanisa.getOutputStream().write(Itekisi);
  for (int 자리 = 0; 자리 < Itekisi.length; 자리++)
   if (Xhumanisa.getInputStream().read() != (Itekisi[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Xhumanisa.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Itekisi = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Itekisi, Itekisi.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] phendula = new byte[64]; DatagramPacket 전문 = new DatagramPacket(phendula, phendula.length);
  종단.receive(전문);
  if (전문.getLength() != Itekisi.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Itekisi.length; 자리++)
   if (phendula[자리] != Itekisi[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket Iseva_inani = new ServerSocket(9300); Iseva_inani.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Xhumanisa = Iseva_inani.accept(); Xhumanisa.setSoTimeout(5000);
  Xhumanisa.getOutputStream().write(Xhumanisa.getInputStream().read() + 1);
  Xhumanisa.close(); Iseva_inani.close();
  byte[] imininingwane = new byte[64]; DatagramPacket 전문 = new DatagramPacket(imininingwane, imininingwane.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Igama, umthombo in umthombo_Amafayela.items():
        (출력 / (Igama + '.java')).write_text(umthombo, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Igama + '.java')) for Igama in umthombo_Amafayela])
    loga_umugqa = bytearray()
    def 빈접속번호(thayipha_umunxa=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, thayipha_umunxa) as Bheka_inani:
            Bheka_inani.bind(('127.0.0.4', 0))
            return Bheka_inani.getsockname()[1]
    파일접속번호, i_TCP_intuba, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Inqubo_inani = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, iNethiwekhi_ibhuloho(
                파일접속번호, ['tcp:{}:9300'.format(i_TCP_intuba), 'udp:{}:9301'.format(전문접속번호)],
                thwebula=True, singatha_ikheli='127.0.0.4') as ibhuloho_inani:
            isilawuli_umzila = Path(임시) / 'qmp.sock'
            Inqubo_inani = subprocess.Popen(Umlayelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(isilawuli_umzila)] + ibhuloho_inani.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            khetha_utho = selectors.DefaultSelector()
            khetha_utho.register(Inqubo_inani.stdout, selectors.EVENT_READ)
            def 받기(khombisa_inani=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while khombisa_inani not in loga_umugqa[처음:]:
                    if time.monotonic() > 끝 or Inqubo_inani.poll() is not None:
                        raise AssertionError('Missing ' + repr(khombisa_inani) + '\n' + loga_umugqa[처음:].decode('utf-8', 'replace'))
                    for inkomba_inani, _ in khetha_utho.select(.05):
                        조각 = inkomba_inani.fileobj.read(65536)
                        if 조각:
                            loga_umugqa.extend(조각)
                return loga_umugqa[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def Thumela(imininingwane):
                Inqubo_inani.stdin.write(imininingwane)
                Inqubo_inani.stdin.flush()
            def isihumushi_miyalelo(Itekisi):
                print(Itekisi, flush=True)
                처음 = len(loga_umugqa)
                Thumela((Itekisi + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as isilawuli_inani:
                isilawuli_inani.settimeout(10)
                isilawuli_inani.connect(str(isilawuli_umzila))
                Stream_inani = isilawuli_inani.makefile('rwb')
                json.loads(Stream_inani.readline())
                def 요청(umyalelo_inani, 인수=None):
                    imininingwane = {'execute': umyalelo_inani}
                    if 인수 is not None:
                        imininingwane['arguments'] = 인수
                    Stream_inani.write((json.dumps(imininingwane) + '\n').encode())
                    Stream_inani.flush()
                    while True:
                        phendula = json.loads(Stream_inani.readline())
                        if 'error' in phendula:
                            raise AssertionError(phendula)
                        if 'return' in phendula:
                            return phendula['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                umbiko_inani['shell_cpu'] = 권한읽기()
                assert 'EL1h' in umbiko_inani['shell_cpu'], umbiko_inani['shell_cpu']
                umbiko_inani['initial_ps'] = isihumushi_miyalelo('ps')
                assert 'kernel/shell' in umbiko_inani['initial_ps']
                umbiko_inani['ipconfig'] = isihumushi_miyalelo('ipconfig')
                assert 'inet 10.0.2.15' in umbiko_inani['ipconfig']
                umbiko_inani['gateway_ping'] = isihumushi_miyalelo('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in umbiko_inani['gateway_ping']
                assert 'FTP listening' in isihumushi_miyalelo('ftpd start')
                with ftplib.FTP() as dlulisa_inani_630ba093:
                    dlulisa_inani_630ba093.encoding = 'utf-8'
                    dlulisa_inani_630ba093.connect('127.0.0.4', 파일접속번호, timeout=20)
                    dlulisa_inani_630ba093.login()
                    for Igama in umthombo_Amafayela:
                        dlulisa_inani_630ba093.storbinary('STOR ' + Igama + '.class', io.BytesIO((출력 / (Igama + '.class')).read_bytes()))
                처음 = len(loga_umugqa)
                Thumela('java imvume_hlola\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    umbiko_inani['java_cpu'] = 권한읽기()
                    if 'EL0t' in umbiko_inani['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in umbiko_inani['java_cpu'], umbiko_inani['java_cpu']
                받기(처음=처음)
                umbiko_inani['after_exit_ps'] = isihumushi_miyalelo('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', umbiko_inani['after_exit_ps'])
                umbiko_inani['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as untanga_inani:
                    Itekisi = isihumushi_miyalelo('java iNethiwekhi_hlola {} {}'.format(untanga_inani.i_TCP_intuba, untanga_inani.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Itekisi and 'exit 0' in Itekisi, Itekisi
                    assert untanga_inani.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, untanga_inani.수신됨
                    assert not untanga_inani.오류들, untanga_inani.오류들
                    umbiko_inani['outbound_peers'] = {종류: imininingwane.decode() for 종류, imininingwane in untanga_inani.수신됨.items()}
                처음 = len(loga_umugqa)
                Thumela('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', i_TCP_intuba), timeout=5) as untanga_inani:
                    untanga_inani.sendall(b'A')
                    assert untanga_inani.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as untanga_inani:
                    untanga_inani.settimeout(5)
                    untanga_inani.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert untanga_inani.recvfrom(64)[0] == b'UDP-IN'
                Itekisi = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Itekisi and 'exit 0' in Itekisi, Itekisi
                umbiko_inani['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in isihumushi_miyalelo('terminal')
                isihumushi_miyalelo('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(loga_umugqa)
                Thumela('java 창예제\n'.encode())
                받기('GUI 예제 Hlela: 창예제\r\n'.encode(), 처음)
                처음 = len(loga_umugqa)
                Thumela(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                umbiko_inani['suspended_java_ps'] = isihumushi_miyalelo('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', umbiko_inani['suspended_java_ps']), umbiko_inani['suspended_java_ps']
                umbiko_inani['top'] = isihumushi_miyalelo('top -n 1')
                assert 'java 창예제' in umbiko_inani['top'] and 'kernel/shell' in umbiko_inani['top']
                umbiko_inani['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                umbiko_inani['network_trace'] = ibhuloho_inani.ithreyisi_loga
                assert not ibhuloho_inani.Iphutha, ibhuloho_inani.Iphutha
                Thumela(b'poweroff\n')
                assert Inqubo_inani.wait(timeout=15) == 0
                umbiko_inani['passed'] = True
            khetha_utho.close()
    except Exception as Iphutha:
        umbiko_inani['error'] = str(Iphutha)
        raise
    finally:
        if Inqubo_inani is not None and Inqubo_inani.poll() is None:
            Inqubo_inani.terminate()
            try:
                Inqubo_inani.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Inqubo_inani.kill()
                Inqubo_inani.wait()
        (출력 / 'serial.log').write_bytes(loga_umugqa)
        (출력 / 'report.json').write_text(json.dumps(umbiko_inani, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({inkomba_inani: umbiko_inani[inkomba_inani] for inkomba_inani in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Sebenzisa()
