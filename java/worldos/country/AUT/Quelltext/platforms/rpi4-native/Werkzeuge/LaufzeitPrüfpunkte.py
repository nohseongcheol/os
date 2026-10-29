#!/usr/bin/env python3
"""QEMU의 tatsächlichDaten CPU erlaubnisWert, Java 세션 표시와 VM 경계의 TCP/UDP를 점검한다."""
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

from befehlAusführen import projektWurzel, befehl
from netzwerkBrücke import netzwerkBrücke
from WiedergebenPrüfaufbau import WiedergebenPrüfaufbau


def ausführenVorgang():
    Ausgabe = projektWurzel / 'build/verification/execution-network-review'
    Ausgabe.mkdir(parents=True, exist_ok=True)
    berichtWert = {'passed': False, 'linux_loaded': False, 'checks': [],
          'kernel_sha256': hashlib.sha256((projektWurzel / 'build/kernel8.img').read_bytes()).hexdigest(),
          'network_scope': 'QEMU guest <-> independent host TCP/UDP peers; not a public Internet or remote LAN test'}
    quelltextDateien = {
        'VorrechtPrüfen': '''public class VorrechtPrüfen {
 public static void main(String[] argumente) {
  System.out.println("EL0_PROBE_READY");
  int Zahl = 0; while (true) { Zahl++; }
 }
}''',
        'NetzwerkPrüfen': '''import java.net.*;
public class NetzwerkPrüfen {
 public static void main(String[] argumente) throws Exception {
  Socket verbinden = new Socket("10.0.2.2", Integer.parseInt(argumente[0]));
  verbinden.setSoTimeout(3000);
  byte[] Text = "TCP 한글\\n".getBytes("UTF-8");
  verbinden.getOutputStream().write(Text);
  for (int positionIndex = 0; positionIndex < Text.length; positionIndex++)
   if (verbinden.getInputStream().read() != (Text[positionIndex] & 255)) throw new RuntimeException("TCP mismatch");
  verbinden.close();
  DatagramSocket endpunkt = new DatagramSocket(); endpunkt.setSoTimeout(3000);
  Text = "UDP 한글".getBytes("UTF-8");
  endpunkt.send(new DatagramPacket(Text, Text.length, InetAddress.getByName("10.0.2.2"), Integer.parseInt(argumente[1])));
  byte[] antwort = new byte[64]; DatagramPacket datagramm = new DatagramPacket(antwort, antwort.length);
  endpunkt.receive(datagramm);
  if (datagramm.getLength() != Text.length) throw new RuntimeException("UDP length");
  for (int positionIndex = 0; positionIndex < Text.length; positionIndex++)
   if (antwort[positionIndex] != Text[positionIndex]) throw new RuntimeException("UDP mismatch");
  endpunkt.close(); System.out.println("OUTBOUND_TCP_UDP_PASS");
 }
}''',
        'EmpfangenPrüfen': '''import java.net.*;
public class EmpfangenPrüfen {
 public static void main(String[] argumente) throws Exception {
  ServerSocket dienstanbieterWert = new ServerSocket(9300); dienstanbieterWert.setSoTimeout(5000);
  DatagramSocket endpunkt = new DatagramSocket(9301); endpunkt.setSoTimeout(5000);
  System.out.println("INBOUND_READY");
  Socket verbinden = dienstanbieterWert.accept(); verbinden.setSoTimeout(5000);
  verbinden.getOutputStream().write(verbinden.getInputStream().read() + 1);
  verbinden.close(); dienstanbieterWert.close();
  byte[] Daten = new byte[64]; DatagramPacket datagramm = new DatagramPacket(Daten, Daten.length);
  endpunkt.receive(datagramm); endpunkt.send(datagramm); endpunkt.close();
  System.out.println("INBOUND_TCP_UDP_PASS");
 }
}''',
    }
    for Name, Quelltext in quelltextDateien.items():
        (Ausgabe / (Name + '.java')).write_text(Quelltext, encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-d', str(Ausgabe)] +
                          [str(Ausgabe / (Name + '.java')) for Name in quelltextDateien])
    protokolldateiAufzeichnung = bytearray()
    def leerwertPortNummer(typKategorie=socket.SOCK_STREAM):
        with socket.socket(socket.AF_INET, typKategorie) as wertSuchen:
            wertSuchen.bind(('127.0.0.4', 0))
            return wertSuchen.getsockname()[1]
    dateiPortNummer, tCPPort, uDPPort = leerwertPortNummer(), leerwertPortNummer(), leerwertPortNummer(socket.SOCK_DGRAM)
    prozessWert = None
    try:
        with tempfile.TemporaryDirectory(prefix='jkoros-layer-') as vorläufigWert, netzwerkBrücke(
                dateiPortNummer, ['tcp:{}:9300'.format(tCPPort), 'udp:{}:9301'.format(uDPPort)],
                erfassen=True, wirtssystemAdresse='127.0.0.4') as brückeWert:
            steuerungPfad = Path(vorläufigWert) / 'qmp.sock'
            prozessWert = subprocess.Popen(befehl() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio',
                        '-qmp', 'unix:{},server=on,wait=off'.format(steuerungPfad)] + brückeWert.weitergeleitetArgument(),
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
            auswählenElementeintrag = selectors.DefaultSelector()
            auswählenElementeintrag.register(prozessWert.stdout, selectors.EVENT_READ)
            def empfangen(wertAnzeigen=b'jkoros-native> ', anfänglichElementeintrag=0, grenzwertWert=60):
                endung = time.monotonic() + grenzwertWert
                while wertAnzeigen not in protokolldateiAufzeichnung[anfänglichElementeintrag:]:
                    if time.monotonic() > endung or prozessWert.poll() is not None:
                        raise AssertionError('Missing ' + repr(wertAnzeigen) + '\n' + protokolldateiAufzeichnung[anfänglichElementeintrag:].decode('utf-8', 'replace'))
                    for tasteWert, _ in auswählenElementeintrag.select(.05):
                        fragmentWert = tasteWert.fileobj.read(65536)
                        if fragmentWert:
                            protokolldateiAufzeichnung.extend(fragmentWert)
                return protokolldateiAufzeichnung[anfänglichElementeintrag:].decode('utf-8', 'replace').replace('\r\n', '\n')
            def senden(Daten):
                prozessWert.stdin.write(Daten)
                prozessWert.stdin.flush()
            def befehlshülle(Text):
                print(Text, flush=True)
                anfänglichElementeintrag = len(protokolldateiAufzeichnung)
                senden((Text + '\n').encode())
                return empfangen(anfänglichElementeintrag=anfänglichElementeintrag)
            empfangen()
            with socket.socket(socket.AF_UNIX) as steuerungWert:
                steuerungWert.settimeout(10)
                steuerungWert.connect(str(steuerungPfad))
                datenstromWert = steuerungWert.makefile('rwb')
                json.loads(datenstromWert.readline())
                def anfrage(befehlswortWert, argumente=None):
                    Daten = {'execute': befehlswortWert}
                    if argumente is not None:
                        Daten['arguments'] = argumente
                    datenstromWert.write((json.dumps(Daten) + '\n').encode())
                    datenstromWert.flush()
                    while True:
                        antwort = json.loads(datenstromWert.readline())
                        if 'error' in antwort:
                            raise AssertionError(antwort)
                        if 'return' in antwort:
                            return antwort['return']
                anfrage('qmp_capabilities')
                def erlaubnisLesen():
                    anfrage('stop')
                    try:
                        return anfrage('human-monitor-command', {'command-line': 'info registers'})
                    finally:
                        anfrage('cont')
                berichtWert['shell_cpu'] = erlaubnisLesen()
                assert 'EL1h' in berichtWert['shell_cpu'], berichtWert['shell_cpu']
                berichtWert['initial_ps'] = befehlshülle('ps')
                assert 'kernel/shell' in berichtWert['initial_ps']
                berichtWert['ipconfig'] = befehlshülle('ipconfig')
                assert 'inet 10.0.2.15' in berichtWert['ipconfig']
                berichtWert['gateway_ping'] = befehlshülle('ping -c 2 10.0.2.2')
                assert '2 transmitted, 2 received' in berichtWert['gateway_ping']
                assert 'FTP listening' in befehlshülle('ftpd start')
                with ftplib.FTP() as übertragungWert:
                    übertragungWert.encoding = 'utf-8'
                    übertragungWert.connect('127.0.0.4', dateiPortNummer, timeout=20)
                    übertragungWert.login()
                    for Name in quelltextDateien:
                        übertragungWert.storbinary('STOR ' + Name + '.class', io.BytesIO((Ausgabe / (Name + '.class')).read_bytes()))
                anfänglichElementeintrag = len(protokolldateiAufzeichnung)
                senden('java VorrechtPrüfen\n'.encode())
                empfangen(b'EL0_PROBE_READY\r\n', anfänglichElementeintrag)
                # The output syscall may still be finishing: inspect until CPU 0 is in EL0.
                for _ in range(30):
                    berichtWert['java_cpu'] = erlaubnisLesen()
                    if 'EL0t' in berichtWert['java_cpu']:
                        break
                    time.sleep(.01)
                assert 'EL0t' in berichtWert['java_cpu'], berichtWert['java_cpu']
                empfangen(anfänglichElementeintrag=anfänglichElementeintrag)
                berichtWert['after_exit_ps'] = befehlshülle('ps')
                assert not re.search(r'\n\d+ \d+ .*java ', berichtWert['after_exit_ps'])
                berichtWert['checks'].append('QMP CPU 0: shell EL1h; Java bytecode VM EL0t; terminated Java omitted from ps')
                with WiedergebenPrüfaufbau() as gegenstelleWert:
                    Text = befehlshülle('java NetzwerkPrüfen {} {}'.format(gegenstelleWert.tCPPort, gegenstelleWert.uDPPort))
                    assert 'OUTBOUND_TCP_UDP_PASS' in Text and 'exit 0' in Text, Text
                    assert gegenstelleWert.hatEmpfangenWert == {'tcp': 'TCP 한글\n'.encode(), 'udp': 'UDP 한글'.encode()}, gegenstelleWert.hatEmpfangenWert
                    assert not gegenstelleWert.fehlerliste, gegenstelleWert.fehlerliste
                    berichtWert['outbound_peers'] = {artWert: Daten.decode() for artWert, Daten in gegenstelleWert.hatEmpfangenWert.items()}
                anfänglichElementeintrag = len(protokolldateiAufzeichnung)
                senden('java EmpfangenPrüfen\n'.encode())
                empfangen(b'INBOUND_READY\r\n', anfänglichElementeintrag)
                with socket.create_connection(('127.0.0.4', tCPPort), timeout=5) as gegenstelleWert:
                    gegenstelleWert.sendall(b'A')
                    assert gegenstelleWert.recv(1) == b'B'
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as gegenstelleWert:
                    gegenstelleWert.settimeout(5)
                    gegenstelleWert.sendto(b'UDP-IN', ('127.0.0.4', uDPPort))
                    assert gegenstelleWert.recvfrom(64)[0] == b'UDP-IN'
                Text = empfangen(anfänglichElementeintrag=anfänglichElementeintrag)
                assert 'INBOUND_TCP_UDP_PASS' in Text and 'exit 0' in Text, Text
                berichtWert['checks'].append('Independent host peers: outbound TCP/UDP payloads, inbound TCP/UDP forwarding, FTP class upload')
                assert 'TERMINAL READY' in befehlshülle('terminal')
                befehlshülle('cd /example/java')
                # This GUI source exceeds the guest compiler subset; use the class
                # compiled by the normal image build and installed alongside it.
                anfänglichElementeintrag = len(protokolldateiAufzeichnung)
                senden('java Fensterbeispiel\n'.encode())
                empfangen('GUI Beispiele vorbereiten: Fensterbeispiel\r\n'.encode(), anfänglichElementeintrag)
                anfänglichElementeintrag = len(protokolldateiAufzeichnung)
                senden(bytes([30, 2, 1, 0, 0, 0, 0]))
                empfangen(anfänglichElementeintrag=anfänglichElementeintrag)
                berichtWert['suspended_java_ps'] = befehlshülle('ps')
                assert re.search(r'\n\d+ 0 SUSPENDED \d+ \d+ \d+ java Fensterbeispiel', berichtWert['suspended_java_ps']), berichtWert['suspended_java_ps']
                berichtWert['top'] = befehlshülle('top -n 1')
                assert 'java Fensterbeispiel' in berichtWert['top'] and 'kernel/shell' in berichtWert['top']
                berichtWert['checks'].append('Bundled Java GUI parked on terminal switch; separate Java PID visible in ps and top')
                berichtWert['network_trace'] = brückeWert.spurProtokolldatei
                assert not brückeWert.fehler, brückeWert.fehler
                senden(b'poweroff\n')
                assert prozessWert.wait(timeout=15) == 0
                berichtWert['passed'] = True
            auswählenElementeintrag.close()
    except Exception as fehler:
        berichtWert['error'] = str(fehler)
        raise
    finally:
        if prozessWert is not None and prozessWert.poll() is None:
            prozessWert.terminate()
            try:
                prozessWert.wait(timeout=10)
            except subprocess.TimeoutExpired:
                prozessWert.kill()
                prozessWert.wait()
        (Ausgabe / 'serial.log').write_bytes(protokolldateiAufzeichnung)
        (Ausgabe / 'report.json').write_text(json.dumps(berichtWert, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({tasteWert: berichtWert[tasteWert] for tasteWert in ('passed', 'checks', 'network_scope')}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    ausführenVorgang()
