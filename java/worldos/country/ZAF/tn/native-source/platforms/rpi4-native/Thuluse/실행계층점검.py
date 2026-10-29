#!/usr/bin/env python3
"""QEMU의 tota_tshedimosetso CPU tetla_Boleng, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from diragatsa_Taelo import 기준, Taelo
from Neteweke_leborogo import Neteweke_leborogo
from 되돌림시험서버 import 되돌림시험서버


def dirisa():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    pego_Boleng = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    Motswedi_Difaele = {
        'tetla_tlhola': '''public class tetla_tlhola {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Neteweke_tlhola': '''import java.net.*;
public class Neteweke_tlhola {
 public static void main(String[] 인수) throws Exception {
  Socket Golaganya = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Golaganya.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  Golaganya.getOutputStream().write(SMS);
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (Golaganya.getInputStream().read() != (SMS[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Golaganya.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] araba = new byte[64]; DatagramPacket 전문 = new DatagramPacket(araba, araba.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (araba[자리] != SMS[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket sefara_Boleng = new ServerSocket(9300); sefara_Boleng.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Golaganya = sefara_Boleng.accept(); Golaganya.setSoTimeout(5000);
  Golaganya.getOutputStream().write(Golaganya.getInputStream().read() + 1);
  Golaganya.close(); sefara_Boleng.close();
  byte[] tshedimosetso = new byte[64]; DatagramPacket 전문 = new DatagramPacket(tshedimosetso, tshedimosetso.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for leina, Motswedi in Motswedi_Difaele.items():
        (출력 / (leina + '.java')).write_text(Motswedi, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (leina + '.java')) for leina in Motswedi_Difaele])
    rekota_mola = bytearray()
    def 빈접속번호(tlanya_setlhopha=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, tlanya_setlhopha) as batla_Boleng:
            batla_Boleng.bind(('127.0.0.4', 0))
            return batla_Boleng.getsockname()[1]
    파일접속번호, TCP_gorogisetsa, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Thulaganyo_Boleng = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Neteweke_leborogo(
                파일접속번호, ['tcp:{}:9300'.format(TCP_gorogisetsa), 'udp:{}:9301'.format(전문접속번호)],
                tshwara=True, pinagare_aterese='127.0.0.4') as leborogo_Boleng:
            taolo_tsela = Path(임시) / 'qmp.sock'
            Thulaganyo_Boleng = subprocess.Popen(Taelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(taolo_tsela)] + leborogo_Boleng.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            tlhopha_selwana = selectors.DefaultSelector()
            tlhopha_selwana.register(Thulaganyo_Boleng.stdout, selectors.EVENT_READ)
            def 받기(bontsha_Boleng=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while bontsha_Boleng not in rekota_mola[처음:]:
                    if time.monotonic() > 끝 or Thulaganyo_Boleng.poll() is not None:
                        raise AssertionError('Missing ' + repr(bontsha_Boleng) + '\n' + rekota_mola[처음:].decode('utf-8', 'replace'))
                    for taetsi_Boleng, _ in tlhopha_selwana.select(.05):
                        조각 = taetsi_Boleng.fileobj.read(65536)
                        if 조각:
                            rekota_mola.extend(조각)
                return rekota_mola[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def romela(tshedimosetso):
                Thulaganyo_Boleng.stdin.write(tshedimosetso)
                Thulaganyo_Boleng.stdin.flush()
            def setlhalosataelo(SMS):
                print(SMS, flush=True)
                처음 = len(rekota_mola)
                romela((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as taolo_Boleng:
                taolo_Boleng.settimeout(10)
                taolo_Boleng.connect(str(taolo_tsela))
                moela_Boleng = taolo_Boleng.makefile('rwb')
                json.loads(moela_Boleng.readline())
                def 요청(taelo_Boleng, 인수=None):
                    tshedimosetso = {'execute': taelo_Boleng}
                    if 인수 is not None:
                        tshedimosetso['arguments'] = 인수
                    moela_Boleng.write((json.dumps(tshedimosetso) + '\n').encode())
                    moela_Boleng.flush()
                    while True:
                        araba = json.loads(moela_Boleng.readline())
                        if 'error' in araba:
                            raise AssertionError(araba)
                        if 'return' in araba:
                            return araba['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                pego_Boleng['shell_cpu'] = 권한읽기()
                assert 'EL1h' in pego_Boleng['shell_cpu'], pego_Boleng['shell_cpu']
                pego_Boleng['initial_ps'] = setlhalosataelo('ps')
                assert 'kernel/shell' in pego_Boleng['initial_ps']
                pego_Boleng['ipconfig'] = setlhalosataelo('ipconfig')
                assert 'inet 10.0.2.15' in pego_Boleng['ipconfig']
                pego_Boleng['gateway_ping'] = setlhalosataelo('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in pego_Boleng['gateway_ping']
                assert 'FTP listening' in setlhalosataelo('ftpd start')
                with ftplib.FTP() as fudusa_Boleng:
                    fudusa_Boleng.encoding = 'utf-8'
                    fudusa_Boleng.connect('127.0.0.4', 파일접속번호, timeout=20)
                    fudusa_Boleng.login()
                    for leina in Motswedi_Difaele:
                        fudusa_Boleng.storbinary('STOR ' + leina + '.class', io.BytesIO((출력 / (leina + '.class')).read_bytes()))
                처음 = len(rekota_mola)
                romela('java tetla_tlhola\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    pego_Boleng['java_cpu'] = 권한읽기()
                    if 'EL0t' in pego_Boleng['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in pego_Boleng['java_cpu'], pego_Boleng['java_cpu']
                받기(처음=처음)
                pego_Boleng['after_exit_ps'] = setlhalosataelo('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', pego_Boleng['after_exit_ps'])
                pego_Boleng['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as semphato_Boleng:
                    SMS = setlhalosataelo('java Neteweke_tlhola {} {}'.format(semphato_Boleng.TCP_gorogisetsa, semphato_Boleng.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert semphato_Boleng.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, semphato_Boleng.수신됨
                    assert not semphato_Boleng.오류들, semphato_Boleng.오류들
                    pego_Boleng['outbound_peers'] = {종류: tshedimosetso.decode() for 종류, tshedimosetso in semphato_Boleng.수신됨.items()}
                처음 = len(rekota_mola)
                romela('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_gorogisetsa), timeout=5) as semphato_Boleng:
                    semphato_Boleng.sendall(b'A')
                    assert semphato_Boleng.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as semphato_Boleng:
                    semphato_Boleng.settimeout(5)
                    semphato_Boleng.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert semphato_Boleng.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                pego_Boleng['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in setlhalosataelo('terminal')
                setlhalosataelo('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(rekota_mola)
                romela('java 창예제\n'.encode())
                받기('GUI 예제 Baakanya: 창예제\r\n'.encode(), 처음)
                처음 = len(rekota_mola)
                romela(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                pego_Boleng['suspended_java_ps'] = setlhalosataelo('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', pego_Boleng['suspended_java_ps']), pego_Boleng['suspended_java_ps']
                pego_Boleng['top'] = setlhalosataelo('top -n 1')
                assert 'java 창예제' in pego_Boleng['top'] and 'kernel/shell' in pego_Boleng['top']
                pego_Boleng['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                pego_Boleng['network_trace'] = leborogo_Boleng.palo_tlhakanyo_rekota
                assert not leborogo_Boleng.phoso, leborogo_Boleng.phoso
                romela(b'poweroff\n')
                assert Thulaganyo_Boleng.wait(timeout=15) == 0
                pego_Boleng['passed'] = True
            tlhopha_selwana.close()
    except Exception as phoso:
        pego_Boleng['error'] = str(phoso)
        raise
    finally:
        if Thulaganyo_Boleng is not None and Thulaganyo_Boleng.poll() is None:
            Thulaganyo_Boleng.terminate()
            try:
                Thulaganyo_Boleng.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Thulaganyo_Boleng.kill()
                Thulaganyo_Boleng.wait()
        (출력 / 'serial.log').write_bytes(rekota_mola)
        (출력 / 'report.json').write_text(json.dumps(pego_Boleng, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({taetsi_Boleng: pego_Boleng[taetsi_Boleng] for taetsi_Boleng in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    dirisa()
