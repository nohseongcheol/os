#!/usr/bin/env python3
"""QEMU의 hakyky_maglumat CPU rugsat_baha, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from ýerine_ýetir_buýruk import 기준, buýruk
from 통신다리 import 통신다리
from 되돌림시험서버 import 되돌림시험서버


def Bitir():
    출력 = 기준 / 'build/verification/execution-network-review'
    출력.mkdir(parents=True, exist_ok=True)
    hasabat_baha = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    gor_Faýllar = {
        'rugsat_derňe': '''public class rugsat_derňe {
 public static void main(String[] 인수) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'Tor_derňe': '''import java.net.*;
public class Tor_derňe {
 public static void main(String[] 인수) throws Exception {
  Socket Birikme = new Socket("10.0.2.2", Integer.parseInt(인수[0]));
  Birikme.setSoTimeout(3000);
  byte[] Metin = "TCP 한글\\n".getBytes("UTF-8");
  Birikme.getOutputStream().write(Metin);
  for (int 자리 = 0; 자리 < Metin.length; 자리++)
   if (Birikme.getInputStream().read() != (Metin[자리] & 255)) throw new RuntimeException("TCP mismatch");
  Birikme.close();
  DatagramSocket 종단 = new DatagramSocket(); 종단.setSoTimeout(3000);
  Metin = "UDP 한글".getBytes("UTF-8");
  종단.send(new DatagramPacket(Metin, Metin.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(인수[1])));
  byte[] jogap_bermek = new byte[64]; DatagramPacket 전문 = new DatagramPacket(jogap_bermek, jogap_bermek.length);
  종단.receive(전문);
  if (전문.getLength() != Metin.length) throw new RuntimeException("UDP length");
  for (int 자리 = 0; 자리 < Metin.length; 자리++)
   if (jogap_bermek[자리] != Metin[자리]) throw new RuntimeException("UDP mismatch");
  종단.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] 인수) throws Exception {
  ServerSocket serwer_baha = new ServerSocket(9300); serwer_baha.setSoTimeout(5000);
  DatagramSocket 종단 = new DatagramSocket(9301); 종단.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Birikme = serwer_baha.accept(); Birikme.setSoTimeout(5000);
  Birikme.getOutputStream().write(Birikme.getInputStream().read() + 1);
  Birikme.close(); serwer_baha.close();
  byte[] maglumat = new byte[64]; DatagramPacket 전문 = new DatagramPacket(maglumat, maglumat.length);
  종단.receive(전문); 종단.send(전문); 종단.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ad, Çeşme in gor_Faýllar.items():
        (출력 / (Ad + '.java')).write_text(Çeşme, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(출력)] +
                          [str(출력 / (Ad + '.java')) for Ad in gor_Faýllar])
    hasaba_alyş_setir = bytearray()
    def 빈접속번호(ýaz_kategoriýa=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, ýaz_kategoriýa) as gözle_baha:
            gözle_baha.bind(('127.0.0.4', 0))
            return gözle_baha.getsockname()[1]
    파일접속번호, TCP_port, 전문접속번호 = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proses_baha = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, 통신다리(
                파일접속번호, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(전문접속번호)],
                düşüriş=True, esasy_salgy='127.0.0.4') as 다리:
            dolandyryş_ýol = Path(임시) / 'qmp.sock'
            Proses_baha = subprocess.Popen(buýruk() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(dolandyryş_ýol)] + 다리.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            saýlap_al_element = selectors.DefaultSelector()
            saýlap_al_element.register(Proses_baha.stdout, selectors.EVENT_READ)
            def 받기(görkez_baha_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while görkez_baha_487749b8 not in hasaba_alyş_setir[처음:]:
                    if time.monotonic() > 끝 or Proses_baha.poll() is not None:
                        raise AssertionError('Missing ' + repr(görkez_baha_487749b8) + '\n' + hasaba_alyş_setir[처음:].decode('utf-8', 'replace'))
                    for açar_baha, _ in saýlap_al_element.select(.05):
                        조각 = açar_baha.fileobj.read(65536)
                        if 조각:
                            hasaba_alyş_setir.extend(조각)
                return hasaba_alyş_setir[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def iber(maglumat):
                Proses_baha.stdin.write(maglumat)
                Proses_baha.stdin.flush()
            def gabyjak(Metin):
                print(Metin, flush=True)
                처음 = len(hasaba_alyş_setir)
                iber((Metin + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as dolandyryş_baha:
                dolandyryş_baha.settimeout(10)
                dolandyryş_baha.connect(str(dolandyryş_ýol))
                Stream_baha = dolandyryş_baha.makefile('rwb')
                json.loads(Stream_baha.readline())
                def 요청(instruksiýa_baha, 인수=None):
                    maglumat = {'execute': instruksiýa_baha}
                    if 인수 is not None:
                        maglumat['arguments'] = 인수
                    Stream_baha.write((json.dumps(maglumat) + '\n').encode())
                    Stream_baha.flush()
                    while True:
                        jogap_bermek = json.loads(Stream_baha.readline())
                        if 'error' in jogap_bermek:
                            raise AssertionError(jogap_bermek)
                        if 'return' in jogap_bermek:
                            return jogap_bermek['return']
                요청('qmp_capabilities')
                def 권한읽기():
                    요청('stop')
                    try:
                        return 요청('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        요청('cont')
                hasabat_baha['shell_cpu'] = 권한읽기()
                assert 'EL1h' in hasabat_baha['shell_cpu'], hasabat_baha['shell_cpu']
                hasabat_baha['initial_ps'] = gabyjak('ps')
                assert 'kernel/shell' in hasabat_baha['initial_ps']
                hasabat_baha['ipconfig'] = gabyjak('ipconfig')
                assert 'inet 10.0.2.15' in hasabat_baha['ipconfig']
                hasabat_baha['gateway_ping'] = gabyjak('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in hasabat_baha['gateway_ping']
                assert 'FTP listening' in gabyjak('ftpd start')
                with ftplib.FTP() as geçir_baha:
                    geçir_baha.encoding = 'utf-8'
                    geçir_baha.connect('127.0.0.4', 파일접속번호, timeout=20)
                    geçir_baha.login()
                    for Ad in gor_Faýllar:
                        geçir_baha.storbinary('STOR ' + Ad + '.class', io.BytesIO((출력 / (Ad + '.class')).read_bytes()))
                처음 = len(hasaba_alyş_setir)
                iber('java rugsat_derňe\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    hasabat_baha['java_cpu'] = 권한읽기()
                    if 'EL0t' in hasabat_baha['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in hasabat_baha['java_cpu'], hasabat_baha['java_cpu']
                받기(처음=처음)
                hasabat_baha['after_exit_ps'] = gabyjak('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', hasabat_baha['after_exit_ps'])
                hasabat_baha['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as deň_derejeli_düwün_baha:
                    Metin = gabyjak('java Tor_derňe {} {}'.format(deň_derejeli_düwün_baha.TCP_port, deň_derejeli_düwün_baha.전문접속번호))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Metin and 'exit 0' in Metin, Metin
                    assert deň_derejeli_düwün_baha.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, deň_derejeli_düwün_baha.수신됨
                    assert not deň_derejeli_düwün_baha.오류들, deň_derejeli_düwün_baha.오류들
                    hasabat_baha['outbound_peers'] = {종류: maglumat.decode() for 종류, maglumat in deň_derejeli_düwün_baha.수신됨.items()}
                처음 = len(hasaba_alyş_setir)
                iber('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as deň_derejeli_düwün_baha:
                    deň_derejeli_düwün_baha.sendall(b'A')
                    assert deň_derejeli_düwün_baha.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as deň_derejeli_düwün_baha:
                    deň_derejeli_düwün_baha.settimeout(5)
                    deň_derejeli_düwün_baha.sendto(b'UDP-IN', ('127.0.0.4', 전문접속번호))
                    assert deň_derejeli_düwün_baha.recvfrom(64)[0] == b'UDP-IN'
                Metin = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Metin and 'exit 0' in Metin, Metin
                hasabat_baha['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in gabyjak('terminal')
                gabyjak('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(hasaba_alyş_setir)
                iber('java 창예제\n'.encode())
                받기('GUI 예제 Taýýarla: 창예제\r\n'.encode(), 처음)
                처음 = len(hasaba_alyş_setir)
                iber(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                hasabat_baha['suspended_java_ps'] = gabyjak('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', hasabat_baha['suspended_java_ps']), hasabat_baha['suspended_java_ps']
                hasabat_baha['top'] = gabyjak('top -n 1')
                assert 'java 창예제' in hasabat_baha['top'] and 'kernel/shell' in hasabat_baha['top']
                hasabat_baha['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                hasabat_baha['network_trace'] = 다리.추적기록
                assert not 다리.Hata, 다리.Hata
                iber(b'poweroff\n')
                assert Proses_baha.wait(timeout=15) == 0
                hasabat_baha['passed'] = True
            saýlap_al_element.close()
    except Exception as Hata:
        hasabat_baha['error'] = str(Hata)
        raise
    finally:
        if Proses_baha is not None and Proses_baha.poll() is None:
            Proses_baha.terminate()
            try:
                Proses_baha.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proses_baha.kill()
                Proses_baha.wait()
        (출력 / 'serial.log').write_bytes(hasaba_alyş_setir)
        (출력 / 'report.json').write_text(json.dumps(hasabat_baha, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({açar_baha: hasabat_baha[açar_baha] for açar_baha in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Bitir()
