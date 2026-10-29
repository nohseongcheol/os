#!/usr/bin/env python3
"""QEMU의 Na_hakika_Tarin_bayani CPU izini_Daraja, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from gudanar_Umarni import 기준, Umarni
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def Tafiyar_da():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    Rahoto_Daraja = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    tushe_Fayiloli = {
        'izini_Bincika': '''public class izini_Bincika {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Hanyar_sadarwa_Bincika': '''import java.net.*;
public class Hanyar_sadarwa_Bincika {
 public static void main(String[] 인수) throws Exception {
  Socket Haɗi = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Haɗi.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  Haɗi.getOutputStream().write(SMS);
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (Haɗi.getInputStream().read() != (SMS[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Haɗi.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] mayar_da_martani = new byte[64]; DatagramPacket 전문 = new DatagramPacket(mayar_da_martani, mayar_da_martani.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (mayar_da_martani[자리] != SMS[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket Saba_Daraja = new ServerSocket(9300); Saba_Daraja.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Haɗi = Saba_Daraja.accept(); Haɗi.setSoTimeout(5000);
  Haɗi.getOutputStream().write(Haɗi.getInputStream().read() + 1);
  Haɗi.close(); Saba_Daraja.close();
  byte[] Tarin_bayani = new byte[64]; DatagramPacket 전문 = new DatagramPacket(Tarin_bayani, Tarin_bayani.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Suna, tushe in tushe_Fayiloli.items():
        (출력 / (Suna + '.java')).write_text(tushe, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Suna + '.java')) for Suna in tushe_Fayiloli])
    logu_naɗa = bytearray()
    def holoko_lambar_kafa(rubuta_ɓangare=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, rubuta_ɓangare) as Leko_Daraja:
            Leko_Daraja.bind(('127.0.0.4', 0))
            return Leko_Daraja.getsockname()[1]
    Fayil_lambar_kafa, TCP_fot, 전문접속번호 = holoko_lambar_kafa(), holoko_lambar_kafa(), holoko_lambar_kafa(socket.SOCK_DGRAM)
    haryar_aikin_na_ura_Daraja = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                Fayil_lambar_kafa, ['tcp:{}:9300'.format(TCP_fot), 'udp:{}:9301'.format(전문접속번호)],
                ɗauka=True, sauka_imel='127.0.0.4') as 다리:
            masarrafa_Hanyar_shiga = Path(임시) / 'qmp.sock'
            haryar_aikin_na_ura_Daraja = subprocess.Popen(Umarni() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(masarrafa_Hanyar_shiga)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            bayyana_ra_ayinka_abu = selectors.DefaultSelector()
            bayyana_ra_ayinka_abu.register(haryar_aikin_na_ura_Daraja.stdout, selectors.EVENT_READ)
            def 받기(Nuna_Daraja=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while Nuna_Daraja not in logu_naɗa[처음:]:
                    if time.monotonic() > 끝 or haryar_aikin_na_ura_Daraja.poll() is not None:
                        raise AssertionError('Missing ' + repr(Nuna_Daraja) + '\n' + logu_naɗa[처음:].decode('utf-8', 'replace'))
                    for Makulli_Daraja, _ in bayyana_ra_ayinka_abu.select(.05):
                        조각 = Makulli_Daraja.fileobj.read(65536)
                        if 조각:
                            logu_naɗa.extend(조각)
                return logu_naɗa[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def Aika(Tarin_bayani):
                haryar_aikin_na_ura_Daraja.stdin.write(Tarin_bayani)
                haryar_aikin_na_ura_Daraja.stdin.flush()
            def Mai_fayyace_umani(SMS):
                print(SMS, flush=True)
                처음 = len(logu_naɗa)
                Aika((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as masarrafa_Daraja:
                masarrafa_Daraja.settimeout(10)
                masarrafa_Daraja.connect(str(masarrafa_Hanyar_shiga))
                watsuwa_Daraja = masarrafa_Daraja.makefile('rwb')
                json.loads(watsuwa_Daraja.readline())
                def 요청(Sharadi_Daraja, 인수=None):
                    Tarin_bayani = {'execute': Sharadi_Daraja}
                    if 인수 is not None:
                        Tarin_bayani['arguments'] = 인수
                    watsuwa_Daraja.write((json.dumps(Tarin_bayani) + '\n').encode())
                    watsuwa_Daraja.flush()
                    while True:
                        mayar_da_martani = json.loads(watsuwa_Daraja.readline())
                        if 'error' in mayar_da_martani:
                            raise AssertionError(mayar_da_martani)
                        if 'return' in mayar_da_martani:
                            return mayar_da_martani['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                Rahoto_Daraja['shell_cpu'] = 권한읽기()
                assert 'EL1h' in Rahoto_Daraja['shell_cpu'], Rahoto_Daraja['shell_cpu']
                Rahoto_Daraja['initial_ps'] = Mai_fayyace_umani('ps')
                assert 'kernel/shell' in Rahoto_Daraja['initial_ps']
                Rahoto_Daraja['ipconfig'] = Mai_fayyace_umani('ipconfig')
                assert 'inet 10.0.2.15' in Rahoto_Daraja['ipconfig']
                Rahoto_Daraja['gateway_ping'] = Mai_fayyace_umani('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Rahoto_Daraja['gateway_ping']
                assert 'FTP listening' in Mai_fayyace_umani('ftpd start')
                with ftplib.FTP() as Gusar_da_Daraja:
                    Gusar_da_Daraja.encoding = 'utf-8'
                    Gusar_da_Daraja.connect('127.0.0.4', Fayil_lambar_kafa, timeout=20)
                    Gusar_da_Daraja.login()
                    for Suna in tushe_Fayiloli:
                        Gusar_da_Daraja.storbinary('STOR ' + Suna + '.class', io.BytesIO((출력 / (Suna + '.class')).read_bytes()))
                처음 = len(logu_naɗa)
                Aika('java izini_Bincika\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Rahoto_Daraja['java_cpu'] = 권한읽기()
                    if 'EL0t' in Rahoto_Daraja['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Rahoto_Daraja['java_cpu'], Rahoto_Daraja['java_cpu']
                받기(처음=처음)
                Rahoto_Daraja['after_exit_ps'] = Mai_fayyace_umani('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Rahoto_Daraja['after_exit_ps'])
                Rahoto_Daraja['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as Fiya_Daraja:
                    SMS = Mai_fayyace_umani('java Hanyar_sadarwa_Bincika {} {}'.format(Fiya_Daraja.TCP_fot, Fiya_Daraja.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert Fiya_Daraja.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, Fiya_Daraja.수신됨
                    assert not Fiya_Daraja.오류들, Fiya_Daraja.오류들
                    Rahoto_Daraja['outbound_peers'] = {종류: Tarin_bayani.decode() for 종류, Tarin_bayani in Fiya_Daraja.수신됨.items()}
                처음 = len(logu_naɗa)
                Aika('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_fot), timeout=5) as Fiya_Daraja:
                    Fiya_Daraja.sendall(b'A')
                    assert Fiya_Daraja.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as Fiya_Daraja:
                    Fiya_Daraja.settimeout(5)
                    Fiya_Daraja.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert Fiya_Daraja.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                Rahoto_Daraja['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in Mai_fayyace_umani('terminal')
                Mai_fayyace_umani('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(logu_naɗa)
                Aika('java 창예제\n'.encode())
                받기('GUI 예제 Shirya: 창예제\r\n'.encode(), 처음)
                처음 = len(logu_naɗa)
                Aika(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                Rahoto_Daraja['suspended_java_ps'] = Mai_fayyace_umani('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', Rahoto_Daraja['suspended_java_ps']), Rahoto_Daraja['suspended_java_ps']
                Rahoto_Daraja['top'] = Mai_fayyace_umani('top -n 1')
                assert 'java 창예제' in Rahoto_Daraja['top'] and 'kernel/shell' in Rahoto_Daraja['top']
                Rahoto_Daraja['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Rahoto_Daraja['network_trace'] = 다리.추적기록
                assert not 다리.Kuskure, 다리.Kuskure
                Aika(b'poweroff\n')
                assert haryar_aikin_na_ura_Daraja.wait(timeout=15) == 0
                Rahoto_Daraja['passed'] = True
            bayyana_ra_ayinka_abu.close()
    except Exception as Kuskure:
        Rahoto_Daraja['error'] = str(Kuskure)
        raise
    finally:
        if haryar_aikin_na_ura_Daraja is not None and haryar_aikin_na_ura_Daraja.poll() is None:
            haryar_aikin_na_ura_Daraja.terminate()
            try:
                haryar_aikin_na_ura_Daraja.wait(timeout=10)
            except subprocess.TimeoutExpired:
                haryar_aikin_na_ura_Daraja.kill()
                haryar_aikin_na_ura_Daraja.wait()
        (출력 / 'serial.log').write_bytes(logu_naɗa)
        (출력 / 'report.json').write_text(json.dumps(Rahoto_Daraja, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Makulli_Daraja: Rahoto_Daraja[Makulli_Daraja] for Makulli_Daraja in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Tafiyar_da()
