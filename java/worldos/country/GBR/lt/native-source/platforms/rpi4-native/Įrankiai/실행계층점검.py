#!/usr/bin/env python3
"""QEMU의 faktinis_duomenys CPU teisė_VALUE, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from Vykdyti_komanda import Project_šaknis, Komanda
from tiltas_3de4fe3a import tiltas_3de4fe3a
from 되돌림시험서버 import 되돌림시험서버


def Paleisti():
    Išvestis = Project_šaknis / 'build/verification/execution-network-review'
    Išvestis.mkdir(parents=True, exist_ok=True)
    pranešti_VALUE = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((Project_šaknis / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    šaltinis_Failai = {
        'teisė_čekis': '''public class teisė_čekis {
 public static void main(String[] Argumentai) {
  System.out.println("EL0_PROBE_READY");
  int numeris = 0; while (true) { numeris++; }
 }
}''',
        'tinklas_čekis': '''import java.net.*;
public class tinklas_čekis {
 public static void main(String[] Argumentai) throws Exception {
  Socket Prisijungti = new Socket("10.0.2.2", Integer.parseInt(Argumentai[0]));
  Prisijungti.setSoTimeout(3000);
  byte[] Tekstas = "TCP 한글\\n".getBytes("UTF-8");
  Prisijungti.getOutputStream().write(Tekstas);
  for (int vietos_rodyklė = 0; vietos_rodyklė < Tekstas.length; vietos_rodyklė++)
   if (Prisijungti.getInputStream().read() != (Tekstas[vietos_rodyklė] & 255)) throw new RuntimeException("TCP mismatch");
  Prisijungti.close();
  DatagramSocket dalyvis = new DatagramSocket(); dalyvis.setSoTimeout(3000);
  Tekstas = "UDP 한글".getBytes("UTF-8");
  dalyvis.send(new DatagramPacket(Tekstas, Tekstas.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(Argumentai[1])));
  byte[] atsakyti = new byte[64]; DatagramPacket paketų_kelio_schema = new DatagramPacket(atsakyti, atsakyti.length);
  dalyvis.receive(paketų_kelio_schema);
  if (paketų_kelio_schema.getLength() != Tekstas.length) throw new RuntimeException("UDP length");
  for (int vietos_rodyklė = 0; vietos_rodyklė < Tekstas.length; vietos_rodyklė++)
   if (atsakyti[vietos_rodyklė] != Tekstas[vietos_rodyklė]) throw new RuntimeException("UDP mismatch");
  dalyvis.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'gauti_čekis': '''import java.net.*;
public class gauti_čekis {
 public static void main(String[] Argumentai) throws Exception {
  ServerSocket serveris_VALUE = new ServerSocket(9300); serveris_VALUE.setSoTimeout(5000);
  DatagramSocket dalyvis = new DatagramSocket(9301); dalyvis.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket Prisijungti = serveris_VALUE.accept(); Prisijungti.setSoTimeout(5000);
  Prisijungti.getOutputStream().write(Prisijungti.getInputStream().read() + 1);
  Prisijungti.close(); serveris_VALUE.close();
  byte[] duomenys = new byte[64]; DatagramPacket paketų_kelio_schema = new DatagramPacket(duomenys, duomenys.length);
  dalyvis.receive(paketų_kelio_schema); dalyvis.send(paketų_kelio_schema); dalyvis.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Pavadinimas_2, ŠALTINIS in šaltinis_Failai.items():
        (Išvestis / (Pavadinimas_2 + '.java')).write_text(ŠALTINIS, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Išvestis)] +
                          [str(Išvestis / (Pavadinimas_2 + '.java')) for Pavadinimas_2 in šaltinis_Failai])
    LOG_RECORD = bytearray()
    def 빈접속번호(TYPE_sritis=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, TYPE_sritis) as Ieška_VALUE:
            Ieška_VALUE.bind(('127.0.0.4', 0))
            return Ieška_VALUE.getsockname()[1]
    Failas_prievado_numeris, TCP_jungtis, UDP_jungtis = 빈접속번호(), 빈접속번호(), 빈접속번호(socket.SOCK_DGRAM)
    Procesas_VALUE = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as 임시, tiltas_3de4fe3a(
                Failas_prievado_numeris, ['tcp:{}:9300'.format(TCP_jungtis), 'udp:{}:9301'.format(UDP_jungtis)],
                įrašyti=True, organizuoti_ADDRESS='127.0.0.4') as tiltas_VALUE:
            valdymas_kelias = Path(임시) / 'qmp.sock'
            Procesas_VALUE = subprocess.Popen(Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(valdymas_kelias)] + tiltas_VALUE.전달인수(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            CHOOSE_prekė = selectors.DefaultSelector()
            CHOOSE_prekė.register(Procesas_VALUE.stdout, selectors.EVENT_READ)
            def gauti(laida_VALUE=b'jkoros-native> ', 처음=0, 제한=60):
                끝 = time.monotonic() + 제한
                while laida_VALUE not in LOG_RECORD[처음:]:
                    if time.monotonic() > 끝 or Procesas_VALUE.poll() is not None:
                        raise AssertionError('Missing ' + repr(laida_VALUE) + '\n' + LOG_RECORD[처음:].decode('utf-8', 'replace'))
                    for Raktas_VALUE, _ in CHOOSE_prekė.select(.05):
                        조각 = Raktas_VALUE.fileobj.read(65536)
                        if 조각:
                            LOG_RECORD.extend(조각)
                return LOG_RECORD[처음:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def siųsti(duomenys):
                Procesas_VALUE.stdin.write(duomenys)
                Procesas_VALUE.stdin.flush()
            def apvalkalas(Tekstas):
                print(Tekstas, flush=True)
                처음 = len(LOG_RECORD)
                siųsti((Tekstas + '\n').encode())
                return gauti(처음=처음)
            gauti()
            with socket.socket(socket.AF_UNIX) as valdymas_VALUE:
                valdymas_VALUE.settimeout(10)
                valdymas_VALUE.connect(str(valdymas_kelias))
                Stream_VALUE = valdymas_VALUE.makefile('rwb')
                json.loads(Stream_VALUE.readline())
                def užklausa(명령어, Argumentai=None):
                    duomenys = {'execute': 명령어}
                    if Argumentai is not None:
                        duomenys['arguments'] = Argumentai
                    Stream_VALUE.write((json.dumps(duomenys) + '\n').encode())
                    Stream_VALUE.flush()
                    while True:
                        atsakyti = json.loads(Stream_VALUE.readline())
                        if 'error' in atsakyti:
                            raise AssertionError(atsakyti)
                        if 'return' in atsakyti:
                            return atsakyti['return']
                užklausa('qmp_capabilities')
                def 권한읽기():
                    užklausa('stop')
                    try:
                        return užklausa('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        užklausa('cont')
                pranešti_VALUE['shell_cpu'] = 권한읽기()
                assert 'EL1h' in pranešti_VALUE['shell_cpu'], pranešti_VALUE['shell_cpu']
                pranešti_VALUE['initial_ps'] = apvalkalas('ps')
                assert 'kernel/shell' in pranešti_VALUE['initial_ps']
                pranešti_VALUE['ipconfig'] = apvalkalas('ipconfig')
                assert 'inet 10.0.2.15' in pranešti_VALUE['ipconfig']
                pranešti_VALUE['gateway_ping'] = apvalkalas('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in pranešti_VALUE['gateway_ping']
                assert 'FTP listening' in apvalkalas('ftpd start')
                with ftplib.FTP() as perduoti_VALUE_630ba093:
                    perduoti_VALUE_630ba093.encoding = 'utf-8'
                    perduoti_VALUE_630ba093.connect('127.0.0.4', Failas_prievado_numeris, timeout=20)
                    perduoti_VALUE_630ba093.login()
                    for Pavadinimas_2 in šaltinis_Failai:
                        perduoti_VALUE_630ba093.storbinary('STOR ' + Pavadinimas_2 + '.class', io.BytesIO((Išvestis / (Pavadinimas_2 + '.class')).read_bytes()))
                처음 = len(LOG_RECORD)
                siųsti('java teisė_čekis\n'.encode())
                gauti(b'EL0_PROBE_READY\r\n', 처음)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    pranešti_VALUE['java_cpu'] = 권한읽기()
                    if 'EL0t' in pranešti_VALUE['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in pranešti_VALUE['java_cpu'], pranešti_VALUE['java_cpu']
                gauti(처음=처음)
                pranešti_VALUE['after_exit_ps'] = apvalkalas('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', pranešti_VALUE['after_exit_ps'])
                pranešti_VALUE['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with 되돌림시험서버() as lygiavertis_mazgas_VALUE:
                    Tekstas = apvalkalas('java tinklas_čekis {} {}'.format(lygiavertis_mazgas_VALUE.TCP_jungtis, lygiavertis_mazgas_VALUE.UDP_jungtis))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Tekstas and 'exit 0' in Tekstas, Tekstas
                    assert lygiavertis_mazgas_VALUE.수신됨 == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, lygiavertis_mazgas_VALUE.수신됨
                    assert not lygiavertis_mazgas_VALUE.오류들, lygiavertis_mazgas_VALUE.오류들
                    pranešti_VALUE['outbound_peers'] = {종류: duomenys.decode() for 종류, duomenys in lygiavertis_mazgas_VALUE.수신됨.items()}
                처음 = len(LOG_RECORD)
                siųsti('java gauti_čekis\n'.encode())
                gauti(b'INBOUND_READY\r\n', 처음)
                with socket.create_connection(('127.0.0.4', TCP_jungtis), timeout=5) as lygiavertis_mazgas_VALUE:
                    lygiavertis_mazgas_VALUE.sendall(b'A')
                    assert lygiavertis_mazgas_VALUE.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as lygiavertis_mazgas_VALUE:
                    lygiavertis_mazgas_VALUE.settimeout(5)
                    lygiavertis_mazgas_VALUE.sendto(b'UDP-IN', ('127.0.0.4', UDP_jungtis))
                    assert lygiavertis_mazgas_VALUE.recvfrom(64)[0] == b'UDP-IN'
                Tekstas = gauti(처음=처음)
                assert 'INBOUND_TCP_UDP_PASS' in Tekstas and 'exit 0' in Tekstas, Tekstas
                pranešti_VALUE['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in apvalkalas('terminal')
                apvalkalas('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                처음 = len(LOG_RECORD)
                siųsti('java LangoPavyzdys\n'.encode())
                gauti('GUI 예제 Parengti: LangoPavyzdys\r\n'.encode(), 처음)
                처음 = len(LOG_RECORD)
                siųsti(bytes([30, 2, 1, 0, 0, 0, 0]))
                gauti(처음=처음)
                pranešti_VALUE['suspended_java_ps'] = apvalkalas('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java LangoPavyzdys', pranešti_VALUE['suspended_java_ps']), pranešti_VALUE['suspended_java_ps']
                pranešti_VALUE['top'] = apvalkalas('top -n 1')
                assert 'java LangoPavyzdys' in pranešti_VALUE['top'] and 'kernel/shell' in pranešti_VALUE['top']
                pranešti_VALUE['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                pranešti_VALUE['network_trace'] = tiltas_VALUE.sekimo_žurnalas
                assert not tiltas_VALUE.KLAIDA, tiltas_VALUE.KLAIDA
                siųsti(b'poweroff\n')
                assert Procesas_VALUE.wait(timeout=15) == 0
                pranešti_VALUE['passed'] = True
            CHOOSE_prekė.close()
    except Exception as KLAIDA:
        pranešti_VALUE['error'] = str(KLAIDA)
        raise
    finally:
        if Procesas_VALUE is not None and Procesas_VALUE.poll() is None:
            Procesas_VALUE.terminate()
            try:
                Procesas_VALUE.wait(timeout=10)
            except subprocess.TimeoutExpired:
                Procesas_VALUE.kill()
                Procesas_VALUE.wait()
        (Išvestis / 'serial.log').write_bytes(LOG_RECORD)
        (Išvestis / 'report.json').write_text(json.dumps(pranešti_VALUE, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({Raktas_VALUE: pranešti_VALUE[Raktas_VALUE] for Raktas_VALUE in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    Paleisti()
