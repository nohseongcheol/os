#!/usr/bin/env python3
"""QEMU의 skutočný_údaje CPU povolenie_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Vykonať_príkaz import akcia_koreň, Príkaz
from sieťový_most import sieťový_most
from 되돌림시험서버 import 되돌림시험서버


def Spustiť_2():
    Výstup = akcia_koreň / 'build/verification/execution-network-review'
    Výstup.mkdir(parents=True, exist_ok=True)
    správa_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((akcia_koreň / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    zdroj_Súbory = {
        'povolenie_skontrolovať': '''public class povolenie_skontrolovať {
 public static void main(String[] Argumenty) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'sieť_skontrolovať': '''import java.net.*;
public class sieť_skontrolovať {
 public static void main(String[] Argumenty) throws Exception {
  Socket Pripojiť = new Socket("10.0.2.2", Integer.parseInt(Argumenty[0]));
  Pripojiť.setSoTimeout(3000);
  byte[] Spracovanie_textu = "TCP 한글\\n".getBytes("UTF-8");
  Pripojiť.getOutputStream().write(Spracovanie_textu);
  for (int pozičný_index = 0; pozičný_index < Spracovanie_textu.length; pozičný_index++)
   if (Pripojiť.getInputStream().read() != (Spracovanie_textu[pozičný_index] & 255)) throw new RuntimeException("TCP mismatch");
  Pripojiť.close();
  DatagramSocket účastník = new DatagramSocket(); účastník.setSoTimeout(3000);
  Spracovanie_textu = "UDP 한글".getBytes("UTF-8");
  účastník.send(new DatagramPacket(Spracovanie_textu, Spracovanie_textu.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumenty[1])));
  byte[] odozva = new byte[64]; DatagramPacket datagram = new DatagramPacket(odozva, odozva.length);
  účastník.receive(datagram);
  if (datagram.getLength() != Spracovanie_textu.length) throw new RuntimeException("UDP length");
  for (int pozičný_index = 0; pozičný_index < Spracovanie_textu.length; pozičný_index++)
   if (odozva[pozičný_index] != Spracovanie_textu[pozičný_index]) throw new RuntimeException("UDP mismatch");
  účastník.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'dostať_skontrolovať': '''import java.net.*;
public class dostať_skontrolovať {
 public static void main(String[] Argumenty) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); server_VALUE.setSoTimeout(5000);
  DatagramSocket účastník = new DatagramSocket(9301); účastník.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Pripojiť = server_VALUE.accept(); Pripojiť.setSoTimeout(5000);
  Pripojiť.getOutputStream().write(Pripojiť.getInputStream().read() + 1);
  Pripojiť.close(); server_VALUE.close();
  byte[] údaje = new byte[64]; DatagramPacket datagram = new DatagramPacket(údaje, údaje.length);
  účastník.receive(datagram); účastník.send(datagram); účastník.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Názov, ZDROJ in zdroj_Súbory.items():
        (Výstup / (Názov + '.java')).write_text(ZDROJ, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Výstup)] +
                          [str(Výstup / (Názov + '.java')) for Názov in zdroj_Súbory])
    LOG_RECORD = bytearray()
    def prázdny_číslo_portu(Typ_oblasť=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Typ_oblasť) as Hľadať_VALUE:
            Hľadať_VALUE.bind(('127.0.0.4', 0))
            return Hľadať_VALUE.getsockname()[1]
    Súbor_číslo_portu, TCP_port, UDP_port = prázdny_číslo_portu(), prázdny_číslo_portu(), prázdny_číslo_portu(socket.SOCK_DGRAM)
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, sieťový_most(
                Súbor_číslo_portu, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                snímať=True, hostiteľ_adresa='127.0.0.4') as most_VALUE:
            riadenie_cesta = Path(임시) / 'qmp.sock'
            Proces_VALUE = subprocess.Popen(Príkaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(riadenie_cesta)] + most_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_položka = selectors.DefaultSelector()
            CHOOSE_položka.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def dostať(zobraziť_VALUE_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while zobraziť_VALUE_487749b8 not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(zobraziť_VALUE_487749b8) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for Kľúč_VALUE, _ in CHOOSE_položka.select(.05):
                        조각 = Kľúč_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def odoslať(údaje):
                Proces_VALUE.stdin.write(údaje)
                Proces_VALUE.stdin.flush()
            def 셸(Spracovanie_textu):
                print(Spracovanie_textu, flush=True)
                처음 = len(LOG_RECORD)
                odoslať((Spracovanie_textu + '\n').encode())
                return dostať(처음=처음)
            dostať()
            with socket.socket(socket.AF_UNIX) as riadenie_VALUE:
                riadenie_VALUE.settimeout(10)
                riadenie_VALUE.connect(str(riadenie_cesta))
                Stream_VALUE = riadenie_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def požiadavka(inštrukcia_VALUE, Argumenty=None):
                    údaje = {'execute': inštrukcia_VALUE}
                    if Argumenty is not None:
                        údaje['arguments'] = Argumenty
                    Stream_VALUE.write((json.dumps(údaje) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        odozva = json.loads(Stream_VALUE.readline())
                        if 'error' in odozva:
                            raise AssertionError(odozva)
                        if 'return' in odozva:
                            return odozva['return']
                požiadavka('qmp_capabilities')
                def 권한읽기():
                    požiadavka('stop')
                    try:
                        return požiadavka('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        požiadavka('cont')
                správa_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in správa_VALUE['shell_cpu'], správa_VALUE['shell_cpu']
                správa_VALUE['initial_ps'] = 셸('ps')
                assert 'kernel/shell' in správa_VALUE['initial_ps']
                správa_VALUE['ipconfig'] = 셸('ipconfig')
                assert 'inet 10.0.2.15' in správa_VALUE['ipconfig']
                správa_VALUE['gateway_ping'] = 셸('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in správa_VALUE['gateway_ping']
                assert 'FTP listening' in 셸('ftpd start')
                with ftplib.FTP() as prenos_VALUE:
                    prenos_VALUE.encoding = 'utf-8'
                    prenos_VALUE.connect('127.0.0.4', Súbor_číslo_portu, timeout=20)
                    prenos_VALUE.login()
                    for Názov in zdroj_Súbory:
                        prenos_VALUE.storbinary('STOR ' + Názov + '.class', io.BytesIO((Výstup / (Názov + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                odoslať('java povolenie_skontrolovať\n'.encode())
                dostať(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    správa_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in správa_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in správa_VALUE['java_cpu'], správa_VALUE['java_cpu']
                dostať(처음=처음)
                správa_VALUE['after_exit_ps'] = 셸('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', správa_VALUE['after_exit_ps'])
                správa_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as partnerský_uzol_VALUE:
                    Spracovanie_textu = 셸('java sieť_skontrolovať {} {}'.format(partnerský_uzol_VALUE.TCP_port, partnerský_uzol_VALUE.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
                    assert partnerský_uzol_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, partnerský_uzol_VALUE.수신됨
                    assert not partnerský_uzol_VALUE.오류들, partnerský_uzol_VALUE.오류들
                    správa_VALUE['outbound_peers'] = {종류: údaje.decode() for 종류, údaje in partnerský_uzol_VALUE.수신됨.items()}
                처음 = len(LOG_RECORD)
                odoslať('java dostať_skontrolovať\n'.encode())
                dostať(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as partnerský_uzol_VALUE:
                    partnerský_uzol_VALUE.sendall(b'A')
                    assert partnerský_uzol_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as partnerský_uzol_VALUE:
                    partnerský_uzol_VALUE.settimeout(5)
                    partnerský_uzol_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert partnerský_uzol_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Spracovanie_textu = dostať(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
                správa_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in 셸('terminal')
                셸('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                odoslať('java UkážkaOkna\n'.encode())
                dostať('GUI 예제 Pripraviť: UkážkaOkna\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                odoslať(bytes([30, 2, 1, 0, 0, 0, 0]))
                dostať(처음=처음)
                správa_VALUE['suspended_java_ps'] = 셸('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java UkážkaOkna', správa_VALUE['suspended_java_ps']), správa_VALUE['suspended_java_ps']
                správa_VALUE['top'] = 셸('top -n 1')
                assert 'java UkážkaOkna' in správa_VALUE['top'] and 'kernel/shell' in správa_VALUE['top']
                správa_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                správa_VALUE['network_trace'] = most_VALUE.denník_sledovania
                assert not most_VALUE.chyba, most_VALUE.chyba
                odoslať(b'poweroff\n')
                assert Proces_VALUE.wait(timeout=15) == 0
                správa_VALUE['passed'] = True
            CHOOSE_položka.close()
    except Exception as chyba:
        správa_VALUE['error'] = str(chyba)
        raise
    finally:
        if Proces_VALUE is not None and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:
                Proces_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_VALUE.kill()
                Proces_VALUE.wait()
        (Výstup / 'serial.log').write_bytes(LOG_RECORD)
        (Výstup / 'report.json').write_text(json.dumps(správa_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Kľúč_VALUE: správa_VALUE[Kľúč_VALUE] for Kľúč_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Spustiť_2()
