#!/usr/bin/env python3
"""Real host TCP client -> SLIP -> bare-metal lwIP -> FTP -> Java VFS."""
import ftplib
import hashlib
import io
import json
import selectors
import socket
import subprocess
import time
import zipfile
from netzwerkBrücke import netzwerkBrücke
from befehlAusführen import projektWurzel, befehl
from WiedergebenPrüfaufbau import WiedergebenPrüfaufbau
from eLFPrüfung import linuxBeispiel


def ausführenVorgang():
    ergebnisDaten = projektWurzel / 'build/verification/ftp'; ergebnisDaten.mkdir(parents=True, exist_ok=True)
    validierungBericht = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((projektWurzel / 'build/kernel8.img').read_bytes()).hexdigest()}
    ablaufprotokoll = bytearray()
    javaQuelltext = ergebnisDaten / 'bündelPrüfung.java'
    javaQuelltext.write_text('public class bündelPrüfung { public static void main(String[] argumente) throws Exception { Deutsch.eigen.Ausgabe.zeileSchreiben("JAR befehlAusführen: " + argumente[0]); Deutsch.eigen.Datei.schreiben("jar.txt", "eigen betriebskernWert Datei"); Deutsch.eigen.Ausgabe.zeileSchreiben(Deutsch.eigen.Datei.lesen("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projektWurzel/'build/java-library/classes'), '-d', str(ergebnisDaten), str(javaQuelltext)])
    archiv = io.BytesIO()
    with zipfile.ZipFile(archiv, 'w', zipfile.ZIP_DEFLATED) as javaBündel:
        javaBündel.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: bündelPrüfung\r\n\r\n')
        javaBündel.write(str(ergebnisDaten/'bündelPrüfung.class'), 'bündelPrüfung.class')
    with socket.socket() as vorläufig:
        vorläufig.bind(('127.0.0.1', 0)); portNummer = vorläufig.getsockname()[1]
    with socket.socket() as vorläufig:
        vorläufig.bind(('127.0.0.1', 0)); dienstanbieterDatenstromPort = vorläufig.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as vorläufig:
        vorläufig.bind(('127.0.0.1', 0)); dienstanbieterDatagrammPort = vorläufig.getsockname()[1]
    with netzwerkBrücke(portNummer, ['tcp:{}:9300'.format(dienstanbieterDatenstromPort), 'udp:{}:9301'.format(dienstanbieterDatagrammPort)], erfassen=True) as brücke:
        prozess = subprocess.Popen(befehl() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + brücke.weitergeleitetArgument(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        auswähler = selectors.DefaultSelector(); auswähler.register(prozess.stdout, selectors.EVENT_READ)
        def nachrichtEmpfangen(markierung=b'jkoros-native> ', ausführungZeitüberschreitung=60):
            Daten = bytearray(); endeVersatzwert = time.monotonic() + ausführungZeitüberschreitung
            while markierung not in Daten:
                if time.monotonic() > endeVersatzwert or prozess.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + Daten.decode('utf-8', 'replace'))
                for gedrücktWert, _ in auswähler.select(.1):
                    fragmentWert = gedrücktWert.fileobj.read(4096)
                    if fragmentWert: Daten.extend(fragmentWert); ablaufprotokoll.extend(fragmentWert)
                if b'PANIC:' in Daten or b'FAIL ' in Daten: raise AssertionError(Daten)
            return Daten.decode('utf-8', 'replace').replace('\r\n', '\n')
        def befehlshülle(zeile):
            prozess.stdin.write(zeile.encode() + b'\n'); prozess.stdin.flush(); return nachrichtEmpfangen()
        try:
            nachrichtEmpfangen(); assert 'FTP listening' in befehlshülle('ftpd start')
            dateiÜbertragungVerbindung = ftplib.FTP(); dateiÜbertragungVerbindung.encoding = 'utf-8'; dateiÜbertragungVerbindung.connect('127.0.0.1', portNummer, timeout=20); dateiÜbertragungVerbindung.login()
            nutzdatenDaten = bytes(range(256)) * 32
            dateiÜbertragungVerbindung.storbinary('STOR binary.dat', io.BytesIO(nutzdatenDaten))
            ergebnis = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR binary.dat', ergebnis.extend)
            assert ergebnis == nutzdatenDaten; assert dateiÜbertragungVerbindung.size('binary.dat') == len(nutzdatenDaten)
            validierungBericht['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            dateiÜbertragungVerbindung.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in befehlshülle('cat 한글.txt')
            assert '한글.txt' in dateiÜbertragungVerbindung.nlst()
            assert dict(dateiÜbertragungVerbindung.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validierungBericht['checks'].append('UTF-8 filename and content visible in guest shell')
            try: dateiÜbertragungVerbindung.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as hilfsEintrag: assert str(hilfsEintrag).startswith('552'), str(hilfsEintrag)
            else: raise AssertionError('oversized upload accepted')
            ergebnis = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR binary.dat', ergebnis.extend); assert ergebnis == nutzdatenDaten
            validierungBericht['checks'].append('oversized replacement rejected; previous file preserved')
            with dateiÜbertragungVerbindung.transfercmd('STOR pending.txt') as hochladenDateien:
                # A control command must not change the active upload's destination.
                assert dateiÜbertragungVerbindung.size('binary.dat') == len(nutzdatenDaten)
                hochladenDateien.sendall(b'UPLOAD TARGET PRESERVED')
            assert dateiÜbertragungVerbindung.voidresp().startswith('226')
            ergebnis = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR pending.txt', ergebnis.extend)
            assert ergebnis == b'UPLOAD TARGET PRESERVED'
            ergebnis = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR binary.dat', ergebnis.extend)
            assert ergebnis == nutzdatenDaten
            dateiÜbertragungVerbindung.delete('pending.txt')
            validierungBericht['checks'].append('interleaved SIZE cannot change the active STOR destination')
            dateiÜbertragungVerbindung.storbinary('STOR Gruß.jar', io.BytesIO(archiv.getvalue()))
            Text = befehlshülle('java -jar Gruß.jar 누리')
            assert 'JAR befehlAusführen: 누리' in Text and 'eigen betriebskernWert Datei' in Text and 'exit 0' in Text, Text
            Text = befehlshülle('./Gruß.jar 세상')
            assert 'JAR befehlAusführen: 세상' in Text and 'exit 0' in Text, Text
            validierungBericht['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            ursprünglichDaten = '#include <DateiABI.h>\nstruct Daten { int Zahl; double 비율; };\nint summeWert(int n) { return n ? n + summeWert(n-1) : 0; }\nint main(void) { struct Daten Wert = {summeWert(10), 1.25}; if (Wert.Zahl != 55 || Wert.비율 * 2 != 2.5) return 3; const char Gruß[] = "CC NATIVE PASS\\n"; int Dokumentation = dateiÖffnen("cc.txt", LesenSchreiben | ErstellenFallsFehlend | KürzenInhalt, 0600); if (Dokumentation < 0) return 1; dateiDatenSchreiben(Dokumentation, Gruß, sizeof(Gruß)-1); dateiSchließen(Dokumentation); dateiDatenSchreiben(1, Gruß, sizeof(Gruß)-1); return 0; }\n'
            dateiÜbertragungVerbindung.storbinary('STOR HangulText.c', io.BytesIO(ursprünglichDaten.encode()))
            Text = befehlshülle('cc HangulText.c -o HangulText.elf'); assert 'Compiled native ARM64 ELF:' in Text and 'exit 0' in Text, Text
            Text = befehlshülle('run HangulText.elf'); assert 'CC NATIVE PASS' in Text and 'exit 0' in Text, Text
            assert 'CC NATIVE PASS' in befehlshülle('cat cc.txt')
            ausführdateiDatei = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR HangulText.elf', ausführdateiDatei.extend)
            assert ausführdateiDatei[:4] == b'\x7fELF' and ausführdateiDatei[18:20] == b'\xb7\x00'
            dateiÜbertragungVerbindung.storbinary('STOR wertKopieren.elf', io.BytesIO(ausführdateiDatei)); Text = befehlshülle('run wertKopieren.elf'); assert 'CC NATIVE PASS' in Text and 'exit 0' in Text, Text
            dateiÜbertragungVerbindung.storbinary('STOR befehlAusführen', io.BytesIO(ausführdateiDatei)); Text=befehlshülle('./befehlAusführen');assert 'CC NATIVE PASS' in Text and 'exit 0' in Text,Text
            dateiÜbertragungVerbindung.storbinary('STOR Name.txt', io.BytesIO(ausführdateiDatei)); Text=befehlshülle('./Name.txt');assert 'CC NATIVE PASS' in Text and 'exit 0' in Text,Text
            befehlshülle('rm befehlAusführen Name.txt')
            validierungBericht['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            befehlshülle('rm binary.dat HangulText.txt HangulText.c HangulText.elf wertKopieren.elf cc.txt jar.txt')
            linuxDatei,erwartet=linuxBeispiel(ergebnisDaten/'linux-reference')
            dateiÜbertragungVerbindung.storbinary('STOR 리눅스인사',io.BytesIO(linuxDatei.read_bytes()))
            Text=befehlshülle('./리눅스인사');assert 'exit -8' in Text,Text
            Text=befehlshülle('run --linux 리눅스인사 한글인수');assert erwartet+'exit 0' in Text,Text
            assert 'LINUX ELF FILE IO' in befehlshülle('cat linux.txt')
            dateiÜbertragungVerbindung.delete('리눅스인사');dateiÜbertragungVerbindung.delete('linux.txt')
            dateiÜbertragungVerbindung.storbinary('STOR falschWert.elf',io.BytesIO(b'plain text'))
            assert '실행할 Zahl 없습니다:' in befehlshülle('./falschWert.elf');dateiÜbertragungVerbindung.delete('falschWert.elf')
            validierungBericht['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with WiedergebenPrüfaufbau() as wiedergebenDienstanbieterEintrag:
                netzQuelltext = ergebnisDaten/'ExternKommunikation.java'
                netzQuelltext.write_text('''import java.net.*; import java.io.*;
public class ExternKommunikation { public static void main(String[] args) throws Exception {
 Socket verbinden = Deutsch.eigen.verbindungBeförderung.verbinden("10.0.2.2", Integer.parseInt(args[0]));
 verbinden.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Quelltext = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Quelltext.length;i++) if (verbinden.getInputStream().read() != (Quelltext[i]&255)) throw new RuntimeException("TCP mismatch");
 verbinden.close();
 DatagramSocket endpunkt = Deutsch.eigen.Kommunikation.öffnen(0); Deutsch.eigen.Kommunikation.zeitüberschreitung(endpunkt, 500);
 Deutsch.eigen.Kommunikation.senden(endpunkt, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Deutsch.eigen.Kommunikation.empfangen(endpunkt).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 endpunkt.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projektWurzel/'build/java-library/classes'),'-d',str(ergebnisDaten),str(netzQuelltext)])
                dateiÜbertragungVerbindung.storbinary('STOR ExternKommunikation.class', io.BytesIO((ergebnisDaten/'ExternKommunikation.class').read_bytes()))
                Text = befehlshülle('java ExternKommunikation {} {}'.format(wiedergebenDienstanbieterEintrag.tCPPort, wiedergebenDienstanbieterEintrag.uDPPort))
                assert 'EXTERNAL TCP UDP PASS' in Text and '10.0.2.2' in Text and 'exit 0' in Text, Text
                assert wiedergebenDienstanbieterEintrag.hatEmpfangenWert == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, wiedergebenDienstanbieterEintrag.hatEmpfangenWert
                assert not wiedergebenDienstanbieterEintrag.fehlerliste, wiedergebenDienstanbieterEintrag.fehlerliste
            validierungBericht['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            dateiÜbertragungVerbindung.delete('ExternKommunikation.class')
            dienstanbieterQuelltext=ergebnisDaten/'DienstanbieterPrüfung.java'
            dienstanbieterQuelltext.write_text('''import java.net.*; public class DienstanbieterPrüfung {
 public static void main(String[] args) throws Exception {
  ServerSocket dienstanbieterWert = new ServerSocket(9300); DatagramSocket endpunkt = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gastWert = dienstanbieterWert.accept();
  gastWert.getOutputStream().write(gastWert.getInputStream().read()+1); gastWert.close(); dienstanbieterWert.close();
  byte[] inhaltswertWert = new byte[8]; DatagramPacket datagramm = new DatagramPacket(inhaltswertWert, inhaltswertWert.length); endpunkt.receive(datagramm);
  endpunkt.send(datagramm); endpunkt.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ergebnisDaten),str(dienstanbieterQuelltext)])
            dateiÜbertragungVerbindung.storbinary('STOR DienstanbieterPrüfung.class',io.BytesIO((ergebnisDaten/'DienstanbieterPrüfung.class').read_bytes()))
            prozess.stdin.write('java DienstanbieterPrüfung\n'.encode());prozess.stdin.flush();nachrichtEmpfangen(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',dienstanbieterDatenstromPort),timeout=5) as gegenstelleWert:
                gegenstelleWert.sendall(b'A');assert gegenstelleWert.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as gegenstelleWert:
                gegenstelleWert.settimeout(5);gegenstelleWert.sendto(b'UDP-IN',('127.0.0.1',dienstanbieterDatagrammPort));assert gegenstelleWert.recvfrom(512)[0]==b'UDP-IN'
            Text=nachrichtEmpfangen();assert 'INBOUND TCP UDP PASS' in Text and 'exit 0' in Text,Text
            validierungBericht['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            dateiÜbertragungVerbindung.delete('DienstanbieterPrüfung.class')
            befehlswortFolge = 'public class Farbe { public static void main(String[] argumente) throws Exception { int summeWert = 0; int Zahl = 1; while (Zahl <= 10) { summeWert = summeWert + Zahl; Zahl = Zahl + 1; } Deutsch.eigen.Ausgabe.nummerSchreiben(summeWert); Deutsch.eigen.Datei.schreiben("aot.txt", "한글 AOT Datei 😀"); Deutsch.eigen.Ausgabe.zeileSchreiben(Deutsch.eigen.Datei.lesen("aot.txt")); } }'
            dateiÜbertragungVerbindung.storbinary('STOR Farbe.java', io.BytesIO(befehlswortFolge.encode()))
            Text = befehlshülle('javac Farbe.java'); assert 'exit 0' in Text and 'Compiled:' in Text, Text
            Text = befehlshülle('jaot Farbe.class -o Farbe.elf'); assert 'AOT compiled native ARM64 ELF:' in Text and 'exit 0' in Text, Text
            Text = befehlshülle('run Farbe.elf'); assert '\n55\n' in Text and '한글 AOT Datei 😀' in Text and 'exit 0' in Text, Text
            systemnah = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR Farbe.elf', systemnah.extend)
            Text = befehlshülle('jaot Gruß.jar -o Farbe.elf'); assert 'exit 1' in Text and 'unsupported' in Text, Text
            bewahrtDaten = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR Farbe.elf', bewahrtDaten.extend); assert systemnah == bewahrtDaten
            bytecode = bytearray(); dateiÜbertragungVerbindung.retrbinary('RETR Farbe.class', bytecode.extend)
            gepackt = io.BytesIO()
            with zipfile.ZipFile(gepackt, 'w', zipfile.ZIP_DEFLATED) as javaBündel:
                javaBündel.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: Farbe\r\n\r\n')
                javaBündel.writestr('Farbe.class', bytecode)
            dateiÜbertragungVerbindung.storbinary('STOR Farbe.jar', io.BytesIO(gepackt.getvalue()))
            Text = befehlshülle('jaot Farbe.jar -o Farbe.elf'); assert 'AOT compiled native ARM64 ELF:' in Text and 'exit 0' in Text, Text
            Text = befehlshülle('run Farbe.elf'); assert '\n55\n' in Text and '한글 AOT Datei 😀' in Text and 'exit 0' in Text, Text
            validierungBericht['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validierungBericht['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statischQuelltext=ergebnisDaten/'StatischPrüfung.java'
            statischQuelltext.write_text('''public class StatischPrüfung {
 static int projektWurzel = 3;
 static int summeWert(int n) { return n == 0 ? 0 : n + summeWert(n-1); }
 public static void main(String[] argumente) {
  int[] Wert = new int[] {projektWurzel, summeWert(10)};
  System.out.println(Wert[0] + Wert[1]); System.out.println(argumente[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ergebnisDaten),str(statischQuelltext)])
            dateiÜbertragungVerbindung.storbinary('STOR StatischPrüfung.class',io.BytesIO((ergebnisDaten/'StatischPrüfung.class').read_bytes()))
            Text=befehlshülle('jaot StatischPrüfung.class -o StatischPrüfung.elf');assert 'exit 0' in Text,Text
            Text=befehlshülle('run StatischPrüfung.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Text,Text
            dateiÜbertragungVerbindung.delete('StatischPrüfung.class');dateiÜbertragungVerbindung.delete('StatischPrüfung.elf')
            validierungBericht['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            beschädigt=bytearray(archiv.getvalue());beschädigt[14]^=1
            dateiÜbertragungVerbindung.storbinary('STOR Gruß.jar',io.BytesIO(beschädigt))
            Text=befehlshülle('java -jar Gruß.jar');assert 'Main-Class\nexit 1' in Text,Text
            validierungBericht['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            dateiÜbertragungVerbindung.quit(); assert 'FTP stopped' in befehlshülle('ftpd stop')
            assert not brücke.fehler, brücke.fehler
            validierungBericht.update(passed=True, frames_to_guest=brücke.rahmenlisteNachGast, frames_from_guest=brücke.rahmenlisteVonGast)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for gedrücktWert,_ in auswähler.select(0):
                fragmentWert=gedrücktWert.fileobj.read(65536)
                if fragmentWert: ablaufprotokoll.extend(fragmentWert)
            brücke.pausierenEreignis.set()
            prozess.terminate()
            try: prozess.wait(timeout=5)
            except subprocess.TimeoutExpired: prozess.kill(); prozess.wait()
            auswähler.close(); prozess.stdin.close(); prozess.stdout.close()
            validierungBericht['bridge_error'] = brücke.fehler
            validierungBericht['frames_to_guest'] = brücke.rahmenlisteNachGast; validierungBericht['frames_from_guest'] = brücke.rahmenlisteVonGast
            (ergebnisDaten/'packets.json').write_text(json.dumps(brücke.spurProtokolldatei,indent=2)+'\n')
            (ergebnisDaten / 'serial.log').write_bytes(ablaufprotokoll)
            (ergebnisDaten / 'report.json').write_text(json.dumps(validierungBericht, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ausführenVorgang()
