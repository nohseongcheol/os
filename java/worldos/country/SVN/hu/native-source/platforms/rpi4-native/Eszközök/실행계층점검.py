#!/usr/bin/env python3
"""QEMU의 tényleges_adat CPU engedély_ÉRTÉK, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from végrehajt_parancs import teendő_gyök, Parancs
from híd_3de4fe3a import híd_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Futtatás():
    Kimenet = teendő_gyök / 'build/verification/execution-network-review'
    Kimenet.mkdir(parents=True, exist_ok=True)
    jelent_ÉRTÉK = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((teendő_gyök / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    forrás_Files = {
        'jog_csekk': '''public class jog_csekk {
 public static void main(String[] Argumentumok) {
  System.out.println("EL0_PROBE_READY");
  int szám = 0; while (true) { szám++; }
 }
}''',
        'hálózat_csekk': '''import java.net.*;
public class hálózat_csekk {
 public static void main(String[] Argumentumok) throws Exception {
  Socket Kapcsolódás = new Socket("10.0.2.2", Integer.parseInt(Argumentumok[0]));
  Kapcsolódás.setSoTimeout(3000);
  byte[] Szöveg = "TCP 한글\\n".getBytes("UTF-8");
  Kapcsolódás.getOutputStream().write(Szöveg);
  for (int helyzetindex = 0; helyzetindex < Szöveg.length; helyzetindex++)
   if (Kapcsolódás.getInputStream().read() != (Szöveg[helyzetindex] & 255)) throw new RuntimeException("TCP mismatch");
  Kapcsolódás.close();
  DatagramSocket végpont = new DatagramSocket(); végpont.setSoTimeout(3000);
  Szöveg = "UDP 한글".getBytes("UTF-8");
  végpont.send(new DatagramPacket(Szöveg, Szöveg.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumentumok[1])));
  byte[] válasz = new byte[64]; DatagramPacket datagram = new DatagramPacket(válasz, válasz.length);
  végpont.receive(datagram);
  if (datagram.getLength() != Szöveg.length) throw new RuntimeException("UDP length");
  for (int helyzetindex = 0; helyzetindex < Szöveg.length; helyzetindex++)
   if (válasz[helyzetindex] != Szöveg[helyzetindex]) throw new RuntimeException("UDP mismatch");
  végpont.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'fogad_csekk': '''import java.net.*;
public class fogad_csekk {
 public static void main(String[] Argumentumok) throws Exception {
  ServerSocket kiszolgáló_ÉRTÉK = new ServerSocket(9300); kiszolgáló_ÉRTÉK.setSoTimeout(5000);
  DatagramSocket végpont = new DatagramSocket(9301); végpont.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Kapcsolódás = kiszolgáló_ÉRTÉK.accept(); Kapcsolódás.setSoTimeout(5000);
  Kapcsolódás.getOutputStream().write(Kapcsolódás.getInputStream().read() + 1);
  Kapcsolódás.close(); kiszolgáló_ÉRTÉK.close();
  byte[] adat = new byte[64]; DatagramPacket datagram = new DatagramPacket(adat, adat.length);
  végpont.receive(datagram); végpont.send(datagram); végpont.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Név, FORRÁS in forrás_Files.items():
        (Kimenet / (Név + '.java')).write_text(FORRÁS, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Kimenet)] +
                          [str(Kimenet / (Név + '.java')) for Név in forrás_Files])
    LOG_REKORD = bytearray()
    def üres_portszám(beír_terület=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, beír_terület) as keres_ÉRTÉK:
            keres_ÉRTÉK.bind(('127.0.0.4', 0))
            return keres_ÉRTÉK.getsockname()[1]
    fájlport_szám, TCP_port, UDP_port = üres_portszám(), üres_portszám(), üres_portszám(socket.SOCK_DGRAM)
    folyamat_ÉRTÉK = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, híd_3de4fe3a(
                fájlport_szám, ['tcp:{}:9300'.format(TCP_port), 'udp:{}:9301'.format(UDP_port)],
                kioszt=True, gazda_CÍM='127.0.0.4') as híd_ÉRTÉK:
            vezérlő_útvonal = Path(임시) / 'qmp.sock'
            folyamat_ÉRTÉK = subprocess.Popen(Parancs() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(vezérlő_útvonal)] + híd_ÉRTÉK.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            VÁLASZT_cikk = selectors.DefaultSelector()
            VÁLASZT_cikk.register(folyamat_ÉRTÉK.stdout, selectors.EVENT_READ)
            def fogad(bemutató_ÉRTÉK=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while bemutató_ÉRTÉK not in LOG_REKORD[처음:]:
                    if time.monotonic() > 끝 or folyamat_ÉRTÉK.poll() is not None:
                        raise AssertionError('Missing ' + repr(bemutató_ÉRTÉK) + '\n' + LOG_REKORD[처음:].decode('utf-8', 'replace'))
                    for Kulcs_ÉRTÉK, _ in VÁLASZT_cikk.select(.05):
                        조각 = Kulcs_ÉRTÉK.fileobj.read(65536)
                        if 조각:
                            LOG_REKORD.extend(조각)
                return LOG_REKORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def küld(adat):
                folyamat_ÉRTÉK.stdin.write(adat)
                folyamat_ÉRTÉK.stdin.flush()
            def felület(Szöveg):
                print(Szöveg, flush=True)
                처음 = len(LOG_REKORD)
                küld((Szöveg + '\n').encode())
                return fogad(처음=처음)
            fogad()
            with socket.socket(socket.AF_UNIX) as vezérlő_ÉRTÉK:
                vezérlő_ÉRTÉK.settimeout(10)
                vezérlő_ÉRTÉK.connect(str(vezérlő_útvonal))
                Stream_ÉRTÉK = vezérlő_ÉRTÉK.makefile('rwb')
                json.loads(Stream_ÉRTÉK.readline())
                def kérés(명령어, Argumentumok=None):
                    adat = {'execute': 명령어}
                    if Argumentumok is not None:
                        adat['arguments'] = Argumentumok
                    Stream_ÉRTÉK.write((json.dumps(adat) + '\n').encode())
                    Stream_ÉRTÉK.flush()
                    while True:
                        válasz = json.loads(Stream_ÉRTÉK.readline())
                        if 'error' in válasz:
                            raise AssertionError(válasz)
                        if 'return' in válasz:
                            return válasz['return']
                kérés('qmp_capabilities')
                def 권한읽기():
                    kérés('stop')
                    try:
                        return kérés('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        kérés('cont')
                jelent_ÉRTÉK['shell_cpu'] = 권한읽기()
                assert 'EL1h' in jelent_ÉRTÉK['shell_cpu'], jelent_ÉRTÉK['shell_cpu']
                jelent_ÉRTÉK['initial_ps'] = felület('ps')
                assert 'kernel/shell' in jelent_ÉRTÉK['initial_ps']
                jelent_ÉRTÉK['ipconfig'] = felület('ipconfig')
                assert 'inet 10.0.2.15' in jelent_ÉRTÉK['ipconfig']
                jelent_ÉRTÉK['gateway_ping'] = felület('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in jelent_ÉRTÉK['gateway_ping']
                assert 'FTP listening' in felület('ftpd start')
                with ftplib.FTP() as átvisz_ÉRTÉK:
                    átvisz_ÉRTÉK.encoding = 'utf-8'
                    átvisz_ÉRTÉK.connect('127.0.0.4', fájlport_szám, timeout=20)
                    átvisz_ÉRTÉK.login()
                    for Név in forrás_Files:
                        átvisz_ÉRTÉK.storbinary('STOR ' + Név + '.class', io.BytesIO((Kimenet / (Név + '.class')).read_bytes()))
                처음 = len(LOG_REKORD)
                küld('java jog_csekk\n'.encode())
                fogad(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    jelent_ÉRTÉK['java_cpu'] = 권한읽기()
                    if 'EL0t' in jelent_ÉRTÉK['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in jelent_ÉRTÉK['java_cpu'], jelent_ÉRTÉK['java_cpu']
                fogad(처음=처음)
                jelent_ÉRTÉK['after_exit_ps'] = felület('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', jelent_ÉRTÉK['after_exit_ps'])
                jelent_ÉRTÉK['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as társ_ÉRTÉK:
                    Szöveg = felület('java hálózat_csekk {} {}'.format(társ_ÉRTÉK.TCP_port, társ_ÉRTÉK.UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Szöveg and 'exit 0' in Szöveg, Szöveg
                    assert társ_ÉRTÉK.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, társ_ÉRTÉK.수신됨
                    assert not társ_ÉRTÉK.오류들, társ_ÉRTÉK.오류들
                    jelent_ÉRTÉK['outbound_peers'] = {Altípus_ÉRTÉK: adat.decode() for Altípus_ÉRTÉK, adat in társ_ÉRTÉK.수신됨.items()}
                처음 = len(LOG_REKORD)
                küld('java fogad_csekk\n'.encode())
                fogad(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_port), timeout=5) as társ_ÉRTÉK:
                    társ_ÉRTÉK.sendall(b'A')
                    assert társ_ÉRTÉK.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as társ_ÉRTÉK:
                    társ_ÉRTÉK.settimeout(5)
                    társ_ÉRTÉK.sendto(b'UDP-IN', ('127.0.0.4', UDP_port))
                    assert társ_ÉRTÉK.recvfrom(64)[0] == b'UDP-IN'
                Szöveg = fogad(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Szöveg and 'exit 0' in Szöveg, Szöveg
                jelent_ÉRTÉK['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in felület('terminal')
                felület('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_REKORD)
                küld('java AblakPélda\n'.encode())
                fogad('GUI 예제 Előkészítés: AblakPélda\r\n'.encode(), 처음)
                처음 = len(LOG_REKORD)
                küld(bytes([30, 2, 1, 0, 0, 0, 0]))
                fogad(처음=처음)
                jelent_ÉRTÉK['suspended_java_ps'] = felület('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java AblakPélda', jelent_ÉRTÉK['suspended_java_ps']), jelent_ÉRTÉK['suspended_java_ps']
                jelent_ÉRTÉK['top'] = felület('top -n 1')
                assert 'java AblakPélda' in jelent_ÉRTÉK['top'] and 'kernel/shell' in jelent_ÉRTÉK['top']
                jelent_ÉRTÉK['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                jelent_ÉRTÉK['network_trace'] = híd_ÉRTÉK.nyomkövetési_napló
                assert not híd_ÉRTÉK.HIBA, híd_ÉRTÉK.HIBA
                küld(b'poweroff\n')
                assert folyamat_ÉRTÉK.wait(timeout=15) == 0
                jelent_ÉRTÉK['passed'] = True
            VÁLASZT_cikk.close()
    except Exception as HIBA:
        jelent_ÉRTÉK['error'] = str(HIBA)
        raise
    finally:
        if folyamat_ÉRTÉK is not None and folyamat_ÉRTÉK.poll() is None:
            folyamat_ÉRTÉK.terminate()
            try:
                folyamat_ÉRTÉK.wait(timeout=10)
            except subprocess.TimeoutExpired:
                folyamat_ÉRTÉK.kill()
                folyamat_ÉRTÉK.wait()
        (Kimenet / 'serial.log').write_bytes(LOG_REKORD)
        (Kimenet / 'report.json').write_text(json.dumps(jelent_ÉRTÉK, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Kulcs_ÉRTÉK: jelent_ÉRTÉK[Kulcs_ÉRTÉK] for Kulcs_ÉRTÉK in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Futtatás()
