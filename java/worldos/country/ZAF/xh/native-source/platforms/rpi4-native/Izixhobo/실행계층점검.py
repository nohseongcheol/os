#!/usr/bin/env python3
"""QEMU의 eyona_yenzekileyo_iingcombolo CPU imvume_ixabiso, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ukwenza_umyalelo import 기준, Umyalelo
from Inethiwekhi_ibhulorho import Inethiwekhi_ibhulorho
from 되돌림시험서버 import 되돌림시험서버


def Phumeza():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ingxelo_ixabiso_ddf2aaf3 = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    umthombo_Iifayile = {
        'imvume_jonga': '''public class imvume_jonga {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Inethiwekhi_jonga': '''import java.net.*;
public class Inethiwekhi_jonga {
 public static void main(String[] 인수) throws Exception {
  Socket Nxulumanisa = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Nxulumanisa.setSoTimeout(3000);
  byte[] Umbhalo = "TCP 한글\\n".getBytes("UTF-8");
  Nxulumanisa.getOutputStream().write(Umbhalo);
  for (int 자리 = 0; 자리 < Umbhalo.length; 자리++)
   if (Nxulumanisa.getInputStream().read() != (Umbhalo[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Nxulumanisa.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Umbhalo = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Umbhalo, Umbhalo.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] phendula = new byte[64]; DatagramPacket 전문 = new DatagramPacket(phendula, phendula.length);
  종단.receive(전문);
  if (전문.getLength() != Umbhalo.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Umbhalo.length; 자리++)
   if (phendula[자리] != Umbhalo[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket iseva_ixabiso = new ServerSocket(9300); iseva_ixabiso.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Nxulumanisa = iseva_ixabiso.accept(); Nxulumanisa.setSoTimeout(5000);
  Nxulumanisa.getOutputStream().write(Nxulumanisa.getInputStream().read() + 1);
  Nxulumanisa.close(); iseva_ixabiso.close();
  byte[] iingcombolo = new byte[64]; DatagramPacket 전문 = new DatagramPacket(iingcombolo, iingcombolo.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Igama, UMTHOMBO in umthombo_Iifayile.items():
        (출력 / (Igama + '.java')).write_text(UMTHOMBO, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Igama + '.java')) for Igama in umthombo_Iifayile])
    ilog_umqolo = bytearray()
    def 빈접속번호(uhlobo_udidi=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, uhlobo_udidi) as Khangela_ixabiso:
            Khangela_ixabiso.bind(('127.0.0.4', 0))
            return Khangela_ixabiso.getsockname()[1]
    파일접속번호, i_TCP_iphothi, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Inkqubo_ixabiso = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Inethiwekhi_ibhulorho(
                파일접속번호, ['tcp:{}:9300'.format(i_TCP_iphothi), 'udp:{}:9301'.format(전문접속번호)],
                bamba=True, umsingathi_idilesi='127.0.0.4') as ibhulorho_ixabiso:
            isilawuli_indlela = Path(임시) / 'qmp.sock'
            Inkqubo_ixabiso = subprocess.Popen(Umyalelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(isilawuli_indlela)] + ibhulorho_ixabiso.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            khetha_into = selectors.DefaultSelector()
            khetha_into.register(Inkqubo_ixabiso.stdout, selectors.EVENT_READ)
            def 받기(bonisa_ixabiso=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while bonisa_ixabiso not in ilog_umqolo[처음:]:
                    if time.monotonic() > 끝 or Inkqubo_ixabiso.poll() is not None:
                        raise AssertionError('Missing ' + repr(bonisa_ixabiso) + '\n' + ilog_umqolo[처음:].decode('utf-8', 'replace'))
                    for iqhosha_ixabiso, _ in khetha_into.select(.05):
                        조각 = iqhosha_ixabiso.fileobj.read(65536)
                        if 조각:
                            ilog_umqolo.extend(조각)
                return ilog_umqolo[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def thumela(iingcombolo):
                Inkqubo_ixabiso.stdin.write(iingcombolo)
                Inkqubo_ixabiso.stdin.flush()
            def isiniki_myalelo(Umbhalo):
                print(Umbhalo, flush=True)
                처음 = len(ilog_umqolo)
                thumela((Umbhalo + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as isilawuli_ixabiso:
                isilawuli_ixabiso.settimeout(10)
                isilawuli_ixabiso.connect(str(isilawuli_indlela))
                Stream_ixabiso = isilawuli_ixabiso.makefile('rwb')
                json.loads(Stream_ixabiso.readline())
                def 요청(umyalelo_ixabiso, 인수=None):
                    iingcombolo = {'execute': umyalelo_ixabiso}
                    if 인수 is not None:
                        iingcombolo['arguments'] = 인수
                    Stream_ixabiso.write((json.dumps(iingcombolo) + '\n').encode())
                    Stream_ixabiso.flush()
                    while True:
                        phendula = json.loads(Stream_ixabiso.readline())
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
                ingxelo_ixabiso_ddf2aaf3['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ingxelo_ixabiso_ddf2aaf3['shell_cpu'], ingxelo_ixabiso_ddf2aaf3['shell_cpu']
                ingxelo_ixabiso_ddf2aaf3['initial_ps'] = isiniki_myalelo('ps')
                assert 'kernel/shell' in ingxelo_ixabiso_ddf2aaf3['initial_ps']
                ingxelo_ixabiso_ddf2aaf3['ipconfig'] = isiniki_myalelo('ipconfig')
                assert 'inet 10.0.2.15' in ingxelo_ixabiso_ddf2aaf3['ipconfig']
                ingxelo_ixabiso_ddf2aaf3['gateway_ping'] = isiniki_myalelo('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ingxelo_ixabiso_ddf2aaf3['gateway_ping']
                assert 'FTP listening' in isiniki_myalelo('ftpd start')
                with ftplib.FTP() as gqithisela_ixabiso:
                    gqithisela_ixabiso.encoding = 'utf-8'
                    gqithisela_ixabiso.connect('127.0.0.4', 파일접속번호, timeout=20)
                    gqithisela_ixabiso.login()
                    for Igama in umthombo_Iifayile:
                        gqithisela_ixabiso.storbinary('STOR ' + Igama + '.class', io.BytesIO((출력 / (Igama + '.class')).read_bytes()))
                처음 = len(ilog_umqolo)
                thumela('java imvume_jonga\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ingxelo_ixabiso_ddf2aaf3['java_cpu'] = 권한읽기()
                    if 'EL0t' in ingxelo_ixabiso_ddf2aaf3['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ingxelo_ixabiso_ddf2aaf3['java_cpu'], ingxelo_ixabiso_ddf2aaf3['java_cpu']
                받기(처음=처음)
                ingxelo_ixabiso_ddf2aaf3['after_exit_ps'] = isiniki_myalelo('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ingxelo_ixabiso_ddf2aaf3['after_exit_ps'])
                ingxelo_ixabiso_ddf2aaf3['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as untanga_ixabiso:
                    Umbhalo = isiniki_myalelo('java Inethiwekhi_jonga {} {}'.format(untanga_ixabiso.i_TCP_iphothi, untanga_ixabiso.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
                    assert untanga_ixabiso.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, untanga_ixabiso.수신됨
                    assert not untanga_ixabiso.오류들, untanga_ixabiso.오류들
                    ingxelo_ixabiso_ddf2aaf3['outbound_peers'] = {종류: iingcombolo.decode() for 종류, iingcombolo in untanga_ixabiso.수신됨.items()}
                처음 = len(ilog_umqolo)
                thumela('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', i_TCP_iphothi), timeout=5) as untanga_ixabiso:
                    untanga_ixabiso.sendall(b'A')
                    assert untanga_ixabiso.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as untanga_ixabiso:
                    untanga_ixabiso.settimeout(5)
                    untanga_ixabiso.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert untanga_ixabiso.recvfrom(64)[0] == b'UDP-IN'
                Umbhalo = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Umbhalo and 'exit 0' in Umbhalo, Umbhalo
                ingxelo_ixabiso_ddf2aaf3['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in isiniki_myalelo('terminal')
                isiniki_myalelo('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(ilog_umqolo)
                thumela('java 창예제\n'.encode())
                받기('GUI 예제 lungisa: 창예제\r\n'.encode(), 처음)
                처음 = len(ilog_umqolo)
                thumela(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ingxelo_ixabiso_ddf2aaf3['suspended_java_ps'] = isiniki_myalelo('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ingxelo_ixabiso_ddf2aaf3['suspended_java_ps']), ingxelo_ixabiso_ddf2aaf3['suspended_java_ps']
                ingxelo_ixabiso_ddf2aaf3['top'] = isiniki_myalelo('top -n 1')
                assert 'java 창예제' in ingxelo_ixabiso_ddf2aaf3['top'] and 'kernel/shell' in ingxelo_ixabiso_ddf2aaf3['top']
                ingxelo_ixabiso_ddf2aaf3['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ingxelo_ixabiso_ddf2aaf3['network_trace'] = ibhulorho_ixabiso.ithreyisi_ilog
                assert not ibhulorho_ixabiso.Impazamo, ibhulorho_ixabiso.Impazamo
                thumela(b'poweroff\n')
                assert Inkqubo_ixabiso.wait(timeout=15) == 0
                ingxelo_ixabiso_ddf2aaf3['passed'] = True
            khetha_into.close()
    except Exception as Impazamo:
        ingxelo_ixabiso_ddf2aaf3['error'] = str(Impazamo)
        raise
    finally:
        if Inkqubo_ixabiso is not None and Inkqubo_ixabiso.poll() is None:
            Inkqubo_ixabiso.terminate()
            try:
                Inkqubo_ixabiso.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Inkqubo_ixabiso.kill()
                Inkqubo_ixabiso.wait()
        (출력 / 'serial.log').write_bytes(ilog_umqolo)
        (출력 / 'report.json').write_text(json.dumps(ingxelo_ixabiso_ddf2aaf3, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({iqhosha_ixabiso: ingxelo_ixabiso_ddf2aaf3[iqhosha_ixabiso] for iqhosha_ixabiso in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Phumeza()
