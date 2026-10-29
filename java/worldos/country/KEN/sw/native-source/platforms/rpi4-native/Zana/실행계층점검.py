#!/usr/bin/env python3
"""QEMU의 halisi_data CPU kibali_thamani, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from tekeleza_amri import 기준, amri
from Mtandao_daraja import Mtandao_daraja
from 되돌림시험서버 import 되돌림시험서버


def endesha():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    ripoti_thamani = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    chanzo_Faili = {
        'kibali_hundi': '''public class kibali_hundi {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Mtandao_hundi': '''import java.net.*;
public class Mtandao_hundi {
 public static void main(String[] 인수) throws Exception {
  Socket UNGANISHA = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  UNGANISHA.setSoTimeout(3000);
  byte[] SMS = "TCP 한글\\n".getBytes("UTF-8");
  UNGANISHA.getOutputStream().write(SMS);
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (UNGANISHA.getInputStream().read() != (SMS[자리] & 255)) throw new RuntimeException("TCP mismatch");
  UNGANISHA.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  SMS = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(SMS, SMS.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] jibu = new byte[64]; DatagramPacket 전문 = new DatagramPacket(jibu, jibu.length);
  종단.receive(전문);
  if (전문.getLength() != SMS.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < SMS.length; 자리++)
   if (jibu[자리] != SMS[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket seva_thamani = new ServerSocket(9300); seva_thamani.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket UNGANISHA = seva_thamani.accept(); UNGANISHA.setSoTimeout(5000);
  UNGANISHA.getOutputStream().write(UNGANISHA.getInputStream().read() + 1);
  UNGANISHA.close(); seva_thamani.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Jina, chanzo in chanzo_Faili.items():
        (출력 / (Jina + '.java')).write_text(chanzo, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Jina + '.java')) for Jina in chanzo_Faili])
    batli_REKODI = bytearray()
    def tupu_namba_ya_kituo(aina_kategoria=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, aina_kategoria) as Duhusi_thamani:
            Duhusi_thamani.bind(('127.0.0.4', 0))
            return Duhusi_thamani.getsockname()[1]
    faili_namba_ya_kituo, TCP_kituo, 전문접속번호 = tupu_namba_ya_kituo(), tupu_namba_ya_kituo(), tupu_namba_ya_kituo(socket.SOCK_DGRAM)
    Mchakato_thamani = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Mtandao_daraja(
                faili_namba_ya_kituo, ['tcp:{}:9300'.format(TCP_kituo), 'udp:{}:9301'.format(전문접속번호)],
                unasaji=True, mwenyeji_anwani='127.0.0.4') as daraja_thamani:
            udhibiti_njia = Path(임시) / 'qmp.sock'
            Mchakato_thamani = subprocess.Popen(amri() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(udhibiti_njia)] + daraja_thamani.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            chagua_kipengee = selectors.DefaultSelector()
            chagua_kipengee.register(Mchakato_thamani.stdout, selectors.EVENT_READ)
            def 받기(onyesha_thamani=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while onyesha_thamani not in batli_REKODI[처음:]:
                    if time.monotonic() > 끝 or Mchakato_thamani.poll() is not None:
                        raise AssertionError('Missing ' + repr(onyesha_thamani) + '\n' + batli_REKODI[처음:].decode('utf-8', 'replace'))
                    for Kitufe_thamani, _ in chagua_kipengee.select(.05):
                        조각 = Kitufe_thamani.fileobj.read(65536)
                        if 조각:
                            batli_REKODI.extend(조각)
                return batli_REKODI[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def tuma(data):
                Mchakato_thamani.stdin.write(data)
                Mchakato_thamani.stdin.flush()
            def sheli(SMS):
                print(SMS, flush=True)
                처음 = len(batli_REKODI)
                tuma((SMS + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as udhibiti_thamani:
                udhibiti_thamani.settimeout(10)
                udhibiti_thamani.connect(str(udhibiti_njia))
                Stream_thamani = udhibiti_thamani.makefile('rwb')
                json.loads(Stream_thamani.readline())
                def 요청(agizo_thamani, 인수=None):
                    data = {'execute': agizo_thamani}
                    if 인수 is not None:
                        data['arguments'] = 인수
                    Stream_thamani.write((json.dumps(data) + '\n').encode())
                    Stream_thamani.flush()
                    while True:
                        jibu = json.loads(Stream_thamani.readline())
                        if 'error' in jibu:
                            raise AssertionError(jibu)
                        if 'return' in jibu:
                            return jibu['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                ripoti_thamani['shell_cpu'] = 권한읽기()
                assert 'EL1h' in ripoti_thamani['shell_cpu'], ripoti_thamani['shell_cpu']
                ripoti_thamani['initial_ps'] = sheli('ps')
                assert 'kernel/shell' in ripoti_thamani['initial_ps']
                ripoti_thamani['ipconfig'] = sheli('ipconfig')
                assert 'inet 10.0.2.15' in ripoti_thamani['ipconfig']
                ripoti_thamani['gateway_ping'] = sheli('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in ripoti_thamani['gateway_ping']
                assert 'FTP listening' in sheli('ftpd start')
                with ftplib.FTP() as hamisha_thamani_630ba093:
                    hamisha_thamani_630ba093.encoding = 'utf-8'
                    hamisha_thamani_630ba093.connect('127.0.0.4', faili_namba_ya_kituo, timeout=20)
                    hamisha_thamani_630ba093.login()
                    for Jina in chanzo_Faili:
                        hamisha_thamani_630ba093.storbinary('STOR ' + Jina + '.class', io.BytesIO((출력 / (Jina + '.class')).read_bytes()))
                처음 = len(batli_REKODI)
                tuma('java kibali_hundi\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    ripoti_thamani['java_cpu'] = 권한읽기()
                    if 'EL0t' in ripoti_thamani['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in ripoti_thamani['java_cpu'], ripoti_thamani['java_cpu']
                받기(처음=처음)
                ripoti_thamani['after_exit_ps'] = sheli('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', ripoti_thamani['after_exit_ps'])
                ripoti_thamani['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as kompyuta_rika_thamani:
                    SMS = sheli('java Mtandao_hundi {} {}'.format(kompyuta_rika_thamani.TCP_kituo, kompyuta_rika_thamani.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                    assert kompyuta_rika_thamani.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, kompyuta_rika_thamani.수신됨
                    assert not kompyuta_rika_thamani.오류들, kompyuta_rika_thamani.오류들
                    ripoti_thamani['outbound_peers'] = {종류: data.decode() for 종류, data in kompyuta_rika_thamani.수신됨.items()}
                처음 = len(batli_REKODI)
                tuma('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_kituo), timeout=5) as kompyuta_rika_thamani:
                    kompyuta_rika_thamani.sendall(b'A')
                    assert kompyuta_rika_thamani.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as kompyuta_rika_thamani:
                    kompyuta_rika_thamani.settimeout(5)
                    kompyuta_rika_thamani.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert kompyuta_rika_thamani.recvfrom(64)[0] == b'UDP-IN'
                SMS = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in SMS and 'exit 0' in SMS, SMS
                ripoti_thamani['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in sheli('terminal')
                sheli('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(batli_REKODI)
                tuma('java 창예제\n'.encode())
                받기('GUI 예제 Andaa: 창예제\r\n'.encode(), 처음)
                처음 = len(batli_REKODI)
                tuma(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                ripoti_thamani['suspended_java_ps'] = sheli('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', ripoti_thamani['suspended_java_ps']), ripoti_thamani['suspended_java_ps']
                ripoti_thamani['top'] = sheli('top -n 1')
                assert 'java 창예제' in ripoti_thamani['top'] and 'kernel/shell' in ripoti_thamani['top']
                ripoti_thamani['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                ripoti_thamani['network_trace'] = daraja_thamani.idadi_ya_maingizo_mlalo_batli
                assert not daraja_thamani.kosa, daraja_thamani.kosa
                tuma(b'poweroff\n')
                assert Mchakato_thamani.wait(timeout=15) == 0
                ripoti_thamani['passed'] = True
            chagua_kipengee.close()
    except Exception as kosa:
        ripoti_thamani['error'] = str(kosa)
        raise
    finally:
        if Mchakato_thamani is not None and Mchakato_thamani.poll() is None:
            Mchakato_thamani.terminate()
            try:
                Mchakato_thamani.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Mchakato_thamani.kill()
                Mchakato_thamani.wait()
        (출력 / 'serial.log').write_bytes(batli_REKODI)
        (출력 / 'report.json').write_text(json.dumps(ripoti_thamani, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Kitufe_thamani: ripoti_thamani[Kitufe_thamani] for Kitufe_thamani in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    endesha()
