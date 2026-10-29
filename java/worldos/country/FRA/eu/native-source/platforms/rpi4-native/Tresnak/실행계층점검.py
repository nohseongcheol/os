#!/usr/bin/env python3
"""QEMU의 benetako_datuak CPU baimen_balio, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from exekutatu_komando import Project_erro, Komandoa
from sare_zubi import sare_zubi
from 되돌림시험서버 import 되돌림시험서버


def Exekutatu_2():
    Irteera = Project_erro / 'build/verification/execution-network-review'
    Irteera.mkdir(parents=True, exist_ok=True)
    txosten_balio = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_erro / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    iturburu_Fitxategiak = {
        'baimen_txeke': '''public class baimen_txeke {
 public static void main(String[] Argumentuak) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'sare_txeke': '''import java.net.*;
public class sare_txeke {
 public static void main(String[] Argumentuak) throws Exception {
  Socket Konektatu = new Socket("10.0.2.2", Integer.parseInt(Argumentuak[0]));
  Konektatu.setSoTimeout(3000);
  byte[] Testua = "TCP 한글\\n".getBytes("UTF-8");
  Konektatu.getOutputStream().write(Testua);
  for (int kargu_INDIZE = 0; kargu_INDIZE < Testua.length; kargu_INDIZE++)
   if (Konektatu.getInputStream().read() != (Testua[kargu_INDIZE] & 255)) throw new RuntimeException("TCP mismatch");
  Konektatu.close();
  DatagramSocket amaiera_puntu = new DatagramSocket(); amaiera_puntu.setSoTimeout(3000);
  Testua = "UDP 한글".getBytes("UTF-8");
  amaiera_puntu.send(new DatagramPacket(Testua, Testua.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumentuak[1])));
  byte[] erantzun = new byte[64]; DatagramPacket 전문 = new DatagramPacket(erantzun, erantzun.length);
  amaiera_puntu.receive(전문);
  if (전문.getLength() != Testua.length) throw new RuntimeException("UDP length");
  for (int kargu_INDIZE = 0; kargu_INDIZE < Testua.length; kargu_INDIZE++)
   if (erantzun[kargu_INDIZE] != Testua[kargu_INDIZE]) throw new RuntimeException("UDP mismatch");
  amaiera_puntu.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        '수신점검': '''import java.net.*;
public class 수신점검 {
 public static void main(String[] Argumentuak) throws Exception {
  ServerSocket zerbitzari_balio = new ServerSocket(9300); zerbitzari_balio.setSoTimeout(5000);
  DatagramSocket amaiera_puntu = new DatagramSocket(9301); amaiera_puntu.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Konektatu = zerbitzari_balio.accept(); Konektatu.setSoTimeout(5000);
  Konektatu.getOutputStream().write(Konektatu.getInputStream().read() + 1);
  Konektatu.close(); zerbitzari_balio.close();
  byte[] datuak = new byte[64]; DatagramPacket 전문 = new DatagramPacket(datuak, datuak.length);
  amaiera_puntu.receive(전문); amaiera_puntu.send(전문); amaiera_puntu.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Izena, ITURBURUA in iturburu_Fitxategiak.items():
        (Irteera / (Izena + '.java')).write_text(ITURBURUA, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Irteera)] +
                          [str(Irteera / (Izena + '.java')) for Izena in iturburu_Fitxategiak])
    LOG_marka = bytearray()
    def 빈접속번호(MOTA_Kategoria=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, MOTA_Kategoria) as BILATU_balio:
            BILATU_balio.bind(('127.0.0.4', 0))
            return BILATU_balio.getsockname()[1]
    fitxategi_ataka_zenbaki, TCP_ataka, UDP_ataka = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    prozesu_balio = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, sare_zubi(
                fitxategi_ataka_zenbaki, ['tcp:{}:9300'.format(TCP_ataka), 'udp:{}:9301'.format(UDP_ataka)],
                atera_ba7b8054=True, Ostalari_helbide='127.0.0.4') as zubi_balio:
            kontrol_bide_izen = Path(임시) / 'qmp.sock'
            prozesu_balio = subprocess.Popen(Komandoa() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(kontrol_bide_izen)] + zubi_balio.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            AUKERATU_elementu = selectors.DefaultSelector()
            AUKERATU_elementu.register(prozesu_balio.stdout, selectors.EVENT_READ)
            def 받기(erakutsi_balio=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while erakutsi_balio not in LOG_marka[처음:]:
                    if time.monotonic() > 끝 or prozesu_balio.poll() is not None:
                        raise AssertionError('Missing ' + repr(erakutsi_balio) + '\n' + LOG_marka[처음:].decode('utf-8', 'replace'))
                    for gako_balio, _ in AUKERATU_elementu.select(.05):
                        조각 = gako_balio.fileobj.read(65536)
                        if 조각:
                            LOG_marka.extend(조각)
                return LOG_marka[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def bidali(datuak):
                prozesu_balio.stdin.write(datuak)
                prozesu_balio.stdin.flush()
            def shell(Testua):
                print(Testua, flush=True)
                처음 = len(LOG_marka)
                bidali((Testua + '\n').encode())
                return 받기(처음=처음)
            받기()
            with socket.socket(socket.AF_UNIX) as kontrol_balio:
                kontrol_balio.settimeout(10)
                kontrol_balio.connect(str(kontrol_bide_izen))
                Stream_balio = kontrol_balio.makefile('rwb')
                json.loads(Stream_balio.readline())
                def eskaera(instrukzio_balio_4c26ea1b, Argumentuak=None):
                    datuak = {'execute': instrukzio_balio_4c26ea1b}
                    if Argumentuak is not None:
                        datuak['arguments'] = Argumentuak
                    Stream_balio.write((json.dumps(datuak) + '\n').encode())
                    Stream_balio.flush()
                    while True:
                        erantzun = json.loads(Stream_balio.readline())
                        if 'error' in erantzun:
                            raise AssertionError(erantzun)
                        if 'return' in erantzun:
                            return erantzun['return']
                eskaera('qmp_capabilities')
                def 권한읽기():
                    eskaera('stop')
                    try:
                        return eskaera('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        eskaera('cont')
                txosten_balio['shell_cpu'] = 권한읽기()
                assert 'EL1h' in txosten_balio['shell_cpu'], txosten_balio['shell_cpu']
                txosten_balio['initial_ps'] = shell('ps')
                assert 'kernel/shell' in txosten_balio['initial_ps']
                txosten_balio['ipconfig'] = shell('ipconfig')
                assert 'inet 10.0.2.15' in txosten_balio['ipconfig']
                txosten_balio['gateway_ping'] = shell('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in txosten_balio['gateway_ping']
                assert 'FTP listening' in shell('ftpd start')
                with ftplib.FTP() as transferitu_balio:
                    transferitu_balio.encoding = 'utf-8'
                    transferitu_balio.connect('127.0.0.4', fitxategi_ataka_zenbaki, timeout=20)
                    transferitu_balio.login()
                    for Izena in iturburu_Fitxategiak:
                        transferitu_balio.storbinary('STOR ' + Izena + '.class', io.BytesIO((Irteera / (Izena + '.class')).read_bytes()))
                처음 = len(LOG_marka)
                bidali('java baimen_txeke\n'.encode())
                받기(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    txosten_balio['java_cpu'] = 권한읽기()
                    if 'EL0t' in txosten_balio['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in txosten_balio['java_cpu'], txosten_balio['java_cpu']
                받기(처음=처음)
                txosten_balio['after_exit_ps'] = shell('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', txosten_balio['after_exit_ps'])
                txosten_balio['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as pareko_balio:
                    Testua = shell('java sare_txeke {} {}'.format(pareko_balio.TCP_ataka, pareko_balio.UDP_ataka))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Testua and 'exit 0' in Testua, Testua
                    assert pareko_balio.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, pareko_balio.수신됨
                    assert not pareko_balio.오류들, pareko_balio.오류들
                    txosten_balio['outbound_peers'] = {종류: datuak.decode() for 종류, datuak in pareko_balio.수신됨.items()}
                처음 = len(LOG_marka)
                bidali('java 수신점검\n'.encode())
                받기(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_ataka), timeout=5) as pareko_balio:
                    pareko_balio.sendall(b'A')
                    assert pareko_balio.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as pareko_balio:
                    pareko_balio.settimeout(5)
                    pareko_balio.sendto(b'UDP-IN', ('127.0.0.4', UDP_ataka))
                    assert pareko_balio.recvfrom(64)[0] == b'UDP-IN'
                Testua = 받기(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Testua and 'exit 0' in Testua, Testua
                txosten_balio['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in shell('terminal')
                shell('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_marka)
                bidali('java 창예제\n'.encode())
                받기('GUI 예제 준비: 창예제\r\n'.encode(), 처음)
                처음 = len(LOG_marka)
                bidali(bytes([30, 2, 1, 0, 0, 0, 0]))
                받기(처음=처음)
                txosten_balio['suspended_java_ps'] = shell('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java 창예제', txosten_balio['suspended_java_ps']), txosten_balio['suspended_java_ps']
                txosten_balio['top'] = shell('top -n 1')
                assert 'java 창예제' in txosten_balio['top'] and 'kernel/shell' in txosten_balio['top']
                txosten_balio['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                txosten_balio['network_trace'] = zubi_balio.balio_diagonalen_batura_LOG
                assert not zubi_balio.errorea, zubi_balio.errorea
                bidali(b'poweroff\n')
                assert prozesu_balio.wait(timeout=15) == 0
                txosten_balio['passed'] = True
            AUKERATU_elementu.close()
    except Exception as errorea:
        txosten_balio['error'] = str(errorea)
        raise
    finally:
        if prozesu_balio is not None and prozesu_balio.poll() is None:
            prozesu_balio.terminate()
            try:
                prozesu_balio.wait(timeout=10)
            except subprocess.TimeoutExpired:
                prozesu_balio.kill()
                prozesu_balio.wait()
        (Irteera / 'serial.log').write_bytes(LOG_marka)
        (Irteera / 'report.json').write_text(json.dumps(txosten_balio, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({gako_balio: txosten_balio[gako_balio] for gako_balio in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Exekutatu_2()
