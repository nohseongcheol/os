#!/usr/bin/env python3
"""QEMU의 kgonthe_data CPU tumelelo_boleng, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from phethagatša_taelo import 기준, Taelo
from Netweke_kgokaganyo import Netweke_kgokaganyo
from 되돌림시험서버 import 되돌림시험서버


def Diriša():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    pego_boleng = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    mohlodi_Difaele = {
        'tumelelo_lekola': '''public class tumelelo_lekola {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Netweke_lekola': '''import java.net.*;
public class Netweke_lekola {
 public static void main(String[] 인수) throws Exception {
  Socket Ikgokaganye = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Ikgokaganye.setSoTimeout(3000);
  byte[] Sengwalwa = "TCP 한글\\n".getBytes("UTF-8");
  Ikgokaganye.getOutputStream().write(Sengwalwa);
  for (int 자리 = 0; 자리 < Sengwalwa.length; 자리++)
   if (Ikgokaganye.getInputStream().read() != (Sengwalwa[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Ikgokaganye.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Sengwalwa = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Sengwalwa, Sengwalwa.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] fetola = new byte[64]; DatagramPacket 전문 = new DatagramPacket(fetola, fetola.length);
  종단.receive(전문);
  if (전문.getLength() != Sengwalwa.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Sengwalwa.length; 자리++)
   if (fetola[자리] != Sengwalwa[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket seba_boleng = new ServerSocket(9300); seba_boleng.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Ikgokaganye = seba_boleng.accept(); Ikgokaganye.setSoTimeout(5000);
  Ikgokaganye.getOutputStream().write(Ikgokaganye.getInputStream().read() + 1);
  Ikgokaganye.close(); seba_boleng.close();
  byte[] data = new byte[64]; DatagramPacket 전문 = new DatagramPacket(data, data.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Leina, mohlodi in mohlodi_Difaele.items():
        (출력 / (Leina + '.java')).write_text(mohlodi, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Leina + '.java')) for Leina in mohlodi_Difaele])
    pego_rei = bytearray()
    def 빈접속번호(thaepa_legoro=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, thaepa_legoro) as Nyaka_boleng:
            Nyaka_boleng.bind(('127.0.0.4', 0))
            return Nyaka_boleng.getsockname()[1]
    파일접속번호, TCP_phote, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    tiragalo_boleng = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, Netweke_kgokaganyo(
                파일접속번호, ['tcp:{}:9300'.format(TCP_phote), 'udp:{}:9301'.format(전문접속번호)],
                tšea=True, go_nea_ditirelo_atrese='127.0.0.4') as kgokaganyo_boleng_982037b1:
            taolo_tsela = Path(임시) / 'qmp.sock'
            tiragalo_boleng = subprocess.Popen(Taelo() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(taolo_tsela)] + kgokaganyo_boleng_982037b1.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            kgetha_aetheme = selectors.DefaultSelector()
            kgetha_aetheme.register(tiragalo_boleng.stdout, selectors.EVENT_READ)
            def 받기(bontšha_boleng=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while bontšha_boleng not in pego_rei[처음:]:
                    if time.monotonic() > 끝 or tiragalo_boleng.poll() is not None:
                        raise AssertionError('Missing ' + repr(bontšha_boleng) + '\n' + pego_rei[처음:].decode('utf-8', 'replace'))
                    for khii_boleng, _ in kgetha_aetheme.select(.05):
                        조각 = khii_boleng.fileobj.read(65536)
                        if 조각:
                            pego_rei.extend(조각)
                return pego_rei[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def Romela(data):
                tiragalo_boleng.stdin.write(data)
                tiragalo_boleng.stdin.flush()
            def šele(Sengwalwa):
                print(Sengwalwa, flush=True)
                처음 = len(pego_rei)
                Romela((Sengwalwa + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as taolo_boleng:
                taolo_boleng.settimeout(10)
                taolo_boleng.connect(str(taolo_tsela))
                Stream_boleng = taolo_boleng.makefile('rwb')
                json.loads(Stream_boleng.readline())
                def 요청(taelo_boleng, 인수=None):
                    data = {'execute': taelo_boleng}
                    if 인수 is not None:
                        data['arguments'] = 인수
                    Stream_boleng.write((json.dumps(data) + '\n').encode())
                    Stream_boleng.flush()
                    while True:
                        fetola = json.loads(Stream_boleng.readline())
                        if 'error' in fetola:
                            raise AssertionError(fetola)
                        if 'return' in fetola:
                            return fetola['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                pego_boleng['shell_cpu'] = 권한읽기()
                assert 'EL1h' in pego_boleng['shell_cpu'], pego_boleng['shell_cpu']
                pego_boleng['initial_ps'] = šele('ps')
                assert 'kernel/shell' in pego_boleng['initial_ps']
                pego_boleng['ipconfig'] = šele('ipconfig')
                assert 'inet 10.0.2.15' in pego_boleng['ipconfig']
                pego_boleng['gateway_ping'] = šele('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in pego_boleng['gateway_ping']
                assert 'FTP listening' in šele('ftpd start')
                with ftplib.FTP() as fetišetša_boleng:
                    fetišetša_boleng.encoding = 'utf-8'
                    fetišetša_boleng.connect('127.0.0.4', 파일접속번호, timeout=20)
                    fetišetša_boleng.login()
                    for Leina in mohlodi_Difaele:
                        fetišetša_boleng.storbinary('STOR ' + Leina + '.class', io.BytesIO((출력 / (Leina + '.class')).read_bytes()))
                처음 = len(pego_rei)
                Romela('java tumelelo_lekola\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    pego_boleng['java_cpu'] = 권한읽기()
                    if 'EL0t' in pego_boleng['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in pego_boleng['java_cpu'], pego_boleng['java_cpu']
                받기(처음=처음)
                pego_boleng['after_exit_ps'] = šele('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', pego_boleng['after_exit_ps'])
                pego_boleng['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as sedirišwa_sa_legoro_le_tee_boleng:
                    Sengwalwa = šele('java Netweke_lekola {} {}'.format(sedirišwa_sa_legoro_le_tee_boleng.TCP_phote, sedirišwa_sa_legoro_le_tee_boleng.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
                    assert sedirišwa_sa_legoro_le_tee_boleng.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, sedirišwa_sa_legoro_le_tee_boleng.수신됨
                    assert not sedirišwa_sa_legoro_le_tee_boleng.오류들, sedirišwa_sa_legoro_le_tee_boleng.오류들
                    pego_boleng['outbound_peers'] = {종류: data.decode() for 종류, data in sedirišwa_sa_legoro_le_tee_boleng.수신됨.items()}
                처음 = len(pego_rei)
                Romela('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_phote), timeout=5) as sedirišwa_sa_legoro_le_tee_boleng:
                    sedirišwa_sa_legoro_le_tee_boleng.sendall(b'A')
                    assert sedirišwa_sa_legoro_le_tee_boleng.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sedirišwa_sa_legoro_le_tee_boleng:
                    sedirišwa_sa_legoro_le_tee_boleng.settimeout(5)
                    sedirišwa_sa_legoro_le_tee_boleng.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert sedirišwa_sa_legoro_le_tee_boleng.recvfrom(64)[0] == b'UDP-IN'
                Sengwalwa = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Sengwalwa and 'exit 0' in Sengwalwa, Sengwalwa
                pego_boleng['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in šele('terminal')
                šele('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(pego_rei)
                Romela('java 창예제\n'.encode())
                받기('GUI 예제 Lokišetša: 창예제\r\n'.encode(), 처음)
                처음 = len(pego_rei)
                Romela(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                pego_boleng['suspended_java_ps'] = šele('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', pego_boleng['suspended_java_ps']), pego_boleng['suspended_java_ps']
                pego_boleng['top'] = šele('top -n 1')
                assert 'java 창예제' in pego_boleng['top'] and 'kernel/shell' in pego_boleng['top']
                pego_boleng['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                pego_boleng['network_trace'] = kgokaganyo_boleng_982037b1.latišiša_pego
                assert not kgokaganyo_boleng_982037b1.Phošo, kgokaganyo_boleng_982037b1.Phošo
                Romela(b'poweroff\n')
                assert tiragalo_boleng.wait(timeout=15) == 0
                pego_boleng['passed'] = True
            kgetha_aetheme.close()
    except Exception as Phošo:
        pego_boleng['error'] = str(Phošo)
        raise
    finally:
        if tiragalo_boleng is not None and tiragalo_boleng.poll() is None:
            tiragalo_boleng.terminate()
            try:
                tiragalo_boleng.wait(timeout=10)
            except subprocess.TimeoutExpired:
                tiragalo_boleng.kill()
                tiragalo_boleng.wait()
        (출력 / 'serial.log').write_bytes(pego_rei)
        (출력 / 'report.json').write_text(json.dumps(pego_boleng, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({khii_boleng: pego_boleng[khii_boleng] for khii_boleng in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Diriša()
