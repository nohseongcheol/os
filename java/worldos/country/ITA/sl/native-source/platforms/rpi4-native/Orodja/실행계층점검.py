#!/usr/bin/env python3
"""QEMU의 dejanski_podatki CPU dovoljenje_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Izvedi_ukaz import pobuda_koren, Ukaz
from most_3de4fe3a import most_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Zaženi():
    Izpis = pobuda_koren / 'build/verification/execution-network-review'
    Izpis.mkdir(parents=True, exist_ok=True)
    prijavi_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((pobuda_koren / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    vir_Datoteke = {
        'pravica_preveriti': '''public class pravica_preveriti {
 public static void main(String[] Argumenti) {
  System.out.println("EL0_PROBE_READY");
  int 수 = 0; while (true) { 수++; }
 }
}''',
        'mreža_preveriti': '''import java.net.*;
public class mreža_preveriti {
 public static void main(String[] Argumenti) throws Exception {
  Socket Poveži = new Socket("10.0.2.2", Integer.parseInt(Argumenti[0]));
  Poveži.setSoTimeout(3000);
  byte[] Besedilo = "TCP 한글\\n".getBytes("UTF-8");
  Poveži.getOutputStream().write(Besedilo);
  for (int kazalec_mesta = 0; kazalec_mesta < Besedilo.length; kazalec_mesta++)
   if (Poveži.getInputStream().read() != (Besedilo[kazalec_mesta] & 255)) throw new RuntimeException("TCP mismatch");
  Poveži.close();
  DatagramSocket končna_točka = new DatagramSocket(); končna_točka.setSoTimeout(3000);
  Besedilo = "UDP 한글".getBytes("UTF-8");
  končna_točka.send(new DatagramPacket(Besedilo, Besedilo.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumenti[1])));
  byte[] odgovor = new byte[64]; DatagramPacket datagram = new DatagramPacket(odgovor, odgovor.length);
  končna_točka.receive(datagram);
  if (datagram.getLength() != Besedilo.length) throw new RuntimeException("UDP length");
  for (int kazalec_mesta = 0; kazalec_mesta < Besedilo.length; kazalec_mesta++)
   if (odgovor[kazalec_mesta] != Besedilo[kazalec_mesta]) throw new RuntimeException("UDP mismatch");
  končna_točka.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'sprejeti_sprejemati_prejeti_prejemati_preveriti': '''import java.net.*;
public class sprejeti_sprejemati_prejeti_prejemati_preveriti {
 public static void main(String[] Argumenti) throws Exception {
  ServerSocket strežnik_VALUE = new ServerSocket(9300); strežnik_VALUE.setSoTimeout(5000);
  DatagramSocket končna_točka = new DatagramSocket(9301); končna_točka.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Poveži = strežnik_VALUE.accept(); Poveži.setSoTimeout(5000);
  Poveži.getOutputStream().write(Poveži.getInputStream().read() + 1);
  Poveži.close(); strežnik_VALUE.close();
  byte[] podatki = new byte[64]; DatagramPacket datagram = new DatagramPacket(podatki, podatki.length);
  končna_točka.receive(datagram); končna_točka.send(datagram); končna_točka.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Ime, VIR in vir_Datoteke.items():
        (Izpis / (Ime + '.java')).write_text(VIR, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Izpis)] +
                          [str(Izpis / (Ime + '.java')) for Ime in vir_Datoteke])
    LOG_zapis = bytearray()
    def prazen_številka_vrat(Tip_območje=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, Tip_območje) as Išči_VALUE:
            Išči_VALUE.bind(('127.0.0.4', 0))
            return Išči_VALUE.getsockname()[1]
    Datoteka_številka_vrat, TCP_vrata, UDP_vrata = prazen_številka_vrat(), prazen_številka_vrat(), prazen_številka_vrat(socket.SOCK_DGRAM)
    Proces_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, most_3de4fe3a(
                Datoteka_številka_vrat, ['tcp:{}:9300'.format(TCP_vrata), 'udp:{}:9301'.format(UDP_vrata)],
                snemati=True, gostiti_naslov='127.0.0.4') as most_VALUE:
            nadzor_pot = Path(임시) / 'qmp.sock'
            Proces_VALUE = subprocess.Popen(Ukaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(nadzor_pot)] + most_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_element = selectors.DefaultSelector()
            CHOOSE_element.register(Proces_VALUE.stdout, selectors.EVENT_READ)
            def sprejeti_sprejemati_prejeti_prejemati(oddaja_VALUE_487749b8=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while oddaja_VALUE_487749b8 not in LOG_zapis[처음:]:
                    if time.monotonic() > 끝 or Proces_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(oddaja_VALUE_487749b8) + '\n' + LOG_zapis[처음:].decode('utf-8', 'replace'))
                    for Ključ_VALUE, _ in CHOOSE_element.select(.05):
                        조각 = Ključ_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_zapis.extend(조각)
                return LOG_zapis[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def poslati(podatki):
                Proces_VALUE.stdin.write(podatki)
                Proces_VALUE.stdin.flush()
            def lupina(Besedilo):
                print(Besedilo, flush=True)
                처음 = len(LOG_zapis)
                poslati((Besedilo + '\n').encode())
                return sprejeti_sprejemati_prejeti_prejemati(처음=처음)
            sprejeti_sprejemati_prejeti_prejemati()
            with socket.socket(socket.AF_UNIX) as nadzor_VALUE:
                nadzor_VALUE.settimeout(10)
                nadzor_VALUE.connect(str(nadzor_pot))
                tok_VALUE = nadzor_VALUE.makefile('rwb')
                json.loads(tok_VALUE.readline())
                def zahteva(navodilo_VALUE, Argumenti=None):
                    podatki = {'execute': navodilo_VALUE}
                    if Argumenti is not None:
                        podatki['arguments'] = Argumenti
                    tok_VALUE.write((json.dumps(podatki) + '\n').encode())
                    tok_VALUE.flush()
                    while True:
                        odgovor = json.loads(tok_VALUE.readline())
                        if 'error' in odgovor:
                            raise AssertionError(odgovor)
                        if 'return' in odgovor:
                            return odgovor['return']
                zahteva('qmp_capabilities')
                def 권한읽기():
                    zahteva('stop')
                    try:
                        return zahteva('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        zahteva('cont')
                prijavi_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in prijavi_VALUE['shell_cpu'], prijavi_VALUE['shell_cpu']
                prijavi_VALUE['initial_ps'] = lupina('ps')
                assert 'kernel/shell' in prijavi_VALUE['initial_ps']
                prijavi_VALUE['ipconfig'] = lupina('ipconfig')
                assert 'inet 10.0.2.15' in prijavi_VALUE['ipconfig']
                prijavi_VALUE['gateway_ping'] = lupina('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in prijavi_VALUE['gateway_ping']
                assert 'FTP listening' in lupina('ftpd start')
                with ftplib.FTP() as Prenos_VALUE:
                    Prenos_VALUE.encoding = 'utf-8'
                    Prenos_VALUE.connect('127.0.0.4', Datoteka_številka_vrat, timeout=20)
                    Prenos_VALUE.login()
                    for Ime in vir_Datoteke:
                        Prenos_VALUE.storbinary('STOR ' + Ime + '.class', io.BytesIO((Izpis / (Ime + '.class')).read_bytes()))
                처음 = len(LOG_zapis)
                poslati('java pravica_preveriti\n'.encode())
                sprejeti_sprejemati_prejeti_prejemati(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    prijavi_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in prijavi_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in prijavi_VALUE['java_cpu'], prijavi_VALUE['java_cpu']
                sprejeti_sprejemati_prejeti_prejemati(처음=처음)
                prijavi_VALUE['after_exit_ps'] = lupina('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', prijavi_VALUE['after_exit_ps'])
                prijavi_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as enakovreden_VALUE:
                    Besedilo = lupina('java mreža_preveriti {} {}'.format(enakovreden_VALUE.TCP_vrata, enakovreden_VALUE.UDP_vrata))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Besedilo and 'exit 0' in Besedilo, Besedilo
                    assert enakovreden_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, enakovreden_VALUE.수신됨
                    assert not enakovreden_VALUE.오류들, enakovreden_VALUE.오류들
                    prijavi_VALUE['outbound_peers'] = {종류: podatki.decode() for 종류, podatki in enakovreden_VALUE.수신됨.items()}
                처음 = len(LOG_zapis)
                poslati('java sprejeti_sprejemati_prejeti_prejemati_preveriti\n'.encode())
                sprejeti_sprejemati_prejeti_prejemati(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_vrata), timeout=5) as enakovreden_VALUE:
                    enakovreden_VALUE.sendall(b'A')
                    assert enakovreden_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as enakovreden_VALUE:
                    enakovreden_VALUE.settimeout(5)
                    enakovreden_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_vrata))
                    assert enakovreden_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Besedilo = sprejeti_sprejemati_prejeti_prejemati(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Besedilo and 'exit 0' in Besedilo, Besedilo
                prijavi_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in lupina('terminal')
                lupina('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_zapis)
                poslati('java PrimerOkna\n'.encode())
                sprejeti_sprejemati_prejeti_prejemati('GUI 예제 Pripravi: PrimerOkna\r\n'.encode(), 처음)
                처음 = len(LOG_zapis)
                poslati(bytes([30, 2, 1, 0, 0, 0, 0]))
                sprejeti_sprejemati_prejeti_prejemati(처음=처음)
                prijavi_VALUE['suspended_java_ps'] = lupina('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java PrimerOkna', prijavi_VALUE['suspended_java_ps']), prijavi_VALUE['suspended_java_ps']
                prijavi_VALUE['top'] = lupina('top -n 1')
                assert 'java PrimerOkna' in prijavi_VALUE['top'] and 'kernel/shell' in prijavi_VALUE['top']
                prijavi_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                prijavi_VALUE['network_trace'] = most_VALUE.dnevnik_sledenja
                assert not most_VALUE.NAPAKA, most_VALUE.NAPAKA
                poslati(b'poweroff\n')
                assert Proces_VALUE.wait(timeout=15) == 0
                prijavi_VALUE['passed'] = True
            CHOOSE_element.close()
    except Exception as NAPAKA:
        prijavi_VALUE['error'] = str(NAPAKA)
        raise
    finally:
        if Proces_VALUE is not None and Proces_VALUE.poll() is None:
            Proces_VALUE.terminate()
            try:
                Proces_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_VALUE.kill()
                Proces_VALUE.wait()
        (Izpis / 'serial.log').write_bytes(LOG_zapis)
        (Izpis / 'report.json').write_text(json.dumps(prijavi_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Ključ_VALUE: prijavi_VALUE[Ključ_VALUE] for Ključ_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Zaženi()
