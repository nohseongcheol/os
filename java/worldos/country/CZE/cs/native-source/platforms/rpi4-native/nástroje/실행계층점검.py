#!/usr/bin/env python3
"""QEMU의 skutečný_data CPU oprávnění_HODNOTA, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Provést_příkaz import akce_kořen, příkaz
from most_3de4fe3a import most_3de4fe3a
from zobrazení_výsledků_testovací_přípravek import zobrazení_výsledků_testovací_přípravek


def Spustit_2():
    výstupní_pozice = akce_kořen / 'build/verification/execution-network-review'
    výstupní_pozice.mkdir(parents=True, exist_ok=True)
    Zpráva_HODNOTA = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((akce_kořen / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    zdroj_Files = {
        'oprávnění_šek': '''public class oprávnění_šek {
 public static void main(String[] argumenty) {
  System.out.println("EL0_PROBE_READY");
  int číslo = 0; while (true) { číslo++; }
 }
}''',
        'síť_šek': '''import java.net.*;
public class síť_šek {
 public static void main(String[] argumenty) throws Exception {
  Socket Připojit = new Socket("10.0.2.2", Integer.parseInt(argumenty[0]));
  Připojit.setSoTimeout(3000);
  byte[] text = "TCP 한글\\n".getBytes("UTF-8");
  Připojit.getOutputStream().write(text);
  for (int poziční_index = 0; poziční_index < text.length; poziční_index++)
   if (Připojit.getInputStream().read() != (text[poziční_index] & 255)) throw new RuntimeException("TCP mismatch");
  Připojit.close();
  DatagramSocket účastník = new DatagramSocket(); účastník.setSoTimeout(3000);
  text = "UDP 한글".getBytes("UTF-8");
  účastník.send(new DatagramPacket(text, text.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumenty[1])));
  byte[] odezva = new byte[64]; DatagramPacket datagram = new DatagramPacket(odezva, odezva.length);
  účastník.receive(datagram);
  if (datagram.getLength() != text.length) throw new RuntimeException("UDP length");
  for (int poziční_index = 0; poziční_index < text.length; poziční_index++)
   if (odezva[poziční_index] != text[poziční_index]) throw new RuntimeException("UDP mismatch");
  účastník.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'dostat_šek': '''import java.net.*;
public class dostat_šek {
 public static void main(String[] argumenty) throws Exception {
  ServerSocket server_HODNOTA = new ServerSocket(9300); server_HODNOTA.setSoTimeout(5000);
  DatagramSocket účastník = new DatagramSocket(9301); účastník.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Připojit = server_HODNOTA.accept(); Připojit.setSoTimeout(5000);
  Připojit.getOutputStream().write(Připojit.getInputStream().read() + 1);
  Připojit.close(); server_HODNOTA.close();
  byte[] data = new byte[64]; DatagramPacket datagram = new DatagramPacket(data, data.length);
  účastník.receive(datagram); účastník.send(datagram); účastník.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Název, zdrojový_soubor in zdroj_Files.items():
        (výstupní_pozice / (Název + '.java')).write_text(zdrojový_soubor, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(výstupní_pozice)] +
                          [str(výstupní_pozice / (Název + '.java')) for Název in zdroj_Files])
    LOGZ_ZÁZNAM = bytearray()
    def 빈접속번호(TYP_oblast=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYP_oblast) as HLEDAT_HODNOTA:
            HLEDAT_HODNOTA.bind(('127.0.0.4', 0))
            return HLEDAT_HODNOTA.getsockname()[1]
    souborový_port_číslo, port_TCP, protokol_UDP_port = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Proces_HODNOTA = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, most_3de4fe3a(
                souborový_port_číslo, ['tcp:{}:9300'.format(port_TCP), 'udp:{}:9301'.format(protokol_UDP_port)],
                čerpat=True, hostit_ODKAZ='127.0.0.4') as most_HODNOTA:
            řízení_cesta = Path(임시) / 'qmp.sock'
            Proces_HODNOTA = subprocess.Popen(příkaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(řízení_cesta)] + most_HODNOTA.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            ZVOLIT_zboží = selectors.DefaultSelector()
            ZVOLIT_zboží.register(Proces_HODNOTA.stdout, selectors.EVENT_READ)
            def dostat(zobrazit_HODNOTA=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while zobrazit_HODNOTA not in LOGZ_ZÁZNAM[처음:]:
                    if time.monotonic() > 끝 or Proces_HODNOTA.poll() is not None:
                        raise AssertionError('Missing ' + repr(zobrazit_HODNOTA) + '\n' + LOGZ_ZÁZNAM[처음:].decode('utf-8', 'replace'))
                    for Klíč_HODNOTA, _ in ZVOLIT_zboží.select(.05):
                        조각 = Klíč_HODNOTA.fileobj.read(65536)
                        if 조각:
                            LOGZ_ZÁZNAM.extend(조각)
                return LOGZ_ZÁZNAM[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def poslat(data):
                Proces_HODNOTA.stdin.write(data)
                Proces_HODNOTA.stdin.flush()
            def prostředí(text):
                print(text, flush=True)
                처음 = len(LOGZ_ZÁZNAM)
                poslat((text + '\n').encode())
                return dostat(처음=처음)
            dostat()
            with socket.socket(socket.AF_UNIX) as řízení_HODNOTA:
                řízení_HODNOTA.settimeout(10)
                řízení_HODNOTA.connect(str(řízení_cesta))
                tok_HODNOTA = řízení_HODNOTA.makefile('rwb')
                json.loads(tok_HODNOTA.readline())
                def žádost(명령어, argumenty=None):
                    data = {'execute': 명령어}
                    if argumenty is not None:
                        data['arguments'] = argumenty
                    tok_HODNOTA.write((json.dumps(data) + '\n').encode())
                    tok_HODNOTA.flush()
                    while True:
                        odezva = json.loads(tok_HODNOTA.readline())
                        if 'error' in odezva:
                            raise AssertionError(odezva)
                        if 'return' in odezva:
                            return odezva['return']
                žádost('qmp_capabilities')
                def oprávnění_ke_čtení():
                    žádost('stop')
                    try:
                        return žádost('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        žádost('cont')
                Zpráva_HODNOTA['shell_cpu'] = oprávnění_ke_čtení()
                assert 'EL1h' in Zpráva_HODNOTA['shell_cpu'], Zpráva_HODNOTA['shell_cpu']
                Zpráva_HODNOTA['initial_ps'] = prostředí('ps')
                assert 'kernel/shell' in Zpráva_HODNOTA['initial_ps']
                Zpráva_HODNOTA['ipconfig'] = prostředí('ipconfig')
                assert 'inet 10.0.2.15' in Zpráva_HODNOTA['ipconfig']
                Zpráva_HODNOTA['gateway_ping'] = prostředí('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in Zpráva_HODNOTA['gateway_ping']
                assert 'FTP listening' in prostředí('ftpd start')
                with ftplib.FTP() as přenos_HODNOTA:
                    přenos_HODNOTA.encoding = 'utf-8'
                    přenos_HODNOTA.connect('127.0.0.4', souborový_port_číslo, timeout=20)
                    přenos_HODNOTA.login()
                    for Název in zdroj_Files:
                        přenos_HODNOTA.storbinary('STOR ' + Název + '.class', io.BytesIO((výstupní_pozice / (Název + '.class')).read_bytes()))
                처음 = len(LOGZ_ZÁZNAM)
                poslat('java oprávnění_šek\n'.encode())
                dostat(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    Zpráva_HODNOTA['java_cpu'] = oprávnění_ke_čtení()
                    if 'EL0t' in Zpráva_HODNOTA['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in Zpráva_HODNOTA['java_cpu'], Zpráva_HODNOTA['java_cpu']
                dostat(처음=처음)
                Zpráva_HODNOTA['after_exit_ps'] = prostředí('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', Zpráva_HODNOTA['after_exit_ps'])
                Zpráva_HODNOTA['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with zobrazení_výsledků_testovací_přípravek() as partner_HODNOTA:
                    text = prostředí('java síť_šek {} {}'.format(partner_HODNOTA.port_TCP, partner_HODNOTA.protokol_UDP_port))
                    assert 'OUTBOUND_TCP_UDP_PASS' in text and 'exit 0' in text, text
                    assert partner_HODNOTA.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, partner_HODNOTA.수신됨
                    assert not partner_HODNOTA.오류들, partner_HODNOTA.오류들
                    Zpráva_HODNOTA['outbound_peers'] = {Druh_HODNOTA: data.decode() for Druh_HODNOTA, data in partner_HODNOTA.수신됨.items()}
                처음 = len(LOGZ_ZÁZNAM)
                poslat('java dostat_šek\n'.encode())
                dostat(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', port_TCP), timeout=5) as partner_HODNOTA:
                    partner_HODNOTA.sendall(b'A')
                    assert partner_HODNOTA.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as partner_HODNOTA:
                    partner_HODNOTA.settimeout(5)
                    partner_HODNOTA.sendto(b'UDP-IN', ('127.0.0.4', protokol_UDP_port))
                    assert partner_HODNOTA.recvfrom(64)[0] == b'UDP-IN'
                text = dostat(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in text and 'exit 0' in text, text
                Zpráva_HODNOTA['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in prostředí('terminal')
                prostředí('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOGZ_ZÁZNAM)
                poslat('java UkázkaOkna\n'.encode())
                dostat('GUI 예제 Připravit: UkázkaOkna\r\n'.encode(), 처음)
                처음 = len(LOGZ_ZÁZNAM)
                poslat(bytes([30, 2, 1, 0, 0, 0, 0]))
                dostat(처음=처음)
                Zpráva_HODNOTA['suspended_java_ps'] = prostředí('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java UkázkaOkna', Zpráva_HODNOTA['suspended_java_ps']), Zpráva_HODNOTA['suspended_java_ps']
                Zpráva_HODNOTA['top'] = prostředí('top -n 1')
                assert 'java UkázkaOkna' in Zpráva_HODNOTA['top'] and 'kernel/shell' in Zpráva_HODNOTA['top']
                Zpráva_HODNOTA['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                Zpráva_HODNOTA['network_trace'] = most_HODNOTA.protokol_trasování
                assert not most_HODNOTA.chyba, most_HODNOTA.chyba
                poslat(b'poweroff\n')
                assert Proces_HODNOTA.wait(timeout=15) == 0
                Zpráva_HODNOTA['passed'] = True
            ZVOLIT_zboží.close()
    except Exception as chyba:
        Zpráva_HODNOTA['error'] = str(chyba)
        raise
    finally:
        if Proces_HODNOTA is not None and Proces_HODNOTA.poll() is None:
            Proces_HODNOTA.terminate()
            try:
                Proces_HODNOTA.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Proces_HODNOTA.kill()
                Proces_HODNOTA.wait()
        (výstupní_pozice / 'serial.log').write_bytes(LOGZ_ZÁZNAM)
        (výstupní_pozice / 'report.json').write_text(json.dumps(Zpráva_HODNOTA, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Klíč_HODNOTA: Zpráva_HODNOTA[Klíč_HODNOTA] for Klíč_HODNOTA in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Spustit_2()
