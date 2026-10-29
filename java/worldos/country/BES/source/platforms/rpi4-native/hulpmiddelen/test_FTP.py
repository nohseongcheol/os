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
from brug_3de4fe3a import brug_3de4fe3a
from Uitvoeren_opdracht import Taken_wortel, opdracht
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def starten():
    HR_gegevens = Taken_wortel / 'build/verification/ftp'; HR_gegevens.mkdir(parents=True, exist_ok=True)
    validatie_Rapport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Taken_wortel / 'build/kernel8.img').read_bytes()).hexdigest()}
    transcriptie = bytearray()
    자바원문 = HR_gegevens / 'test_bundel.java'
    자바원문.write_text('public class test_bundel { public static void main(String[] argumenten) throws Exception { Nederlands.Eigen.tekstuitvoer.schrijven_lijn("JAR Uitvoeren_opdracht: " + argumenten[0]); Nederlands.Eigen.bestand.Schrijven("jar.txt", "Eigen kernel_WAARDE bestand"); Nederlands.Eigen.tekstuitvoer.schrijven_lijn(Nederlands.Eigen.bestand.Lezen("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Taken_wortel/'build/java-library/classes'), '-d', str(HR_gegevens), str(자바원문)])
    Archief = io.BytesIO()
    with zipfile.ZipFile(Archief, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_bundel\r\n\r\n')
        자바꾸러미.write(str(HR_gegevens/'test_bundel.class'), 'test_bundel.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); poortnummer = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_Stream_poort = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagram_poort = 임시자원.getsockname()[1]
    with brug_3de4fe3a(poortnummer, ['tcp:{}:9300'.format(server_Stream_poort), 'udp:{}:9301'.format(server_datagram_poort)], Capture=True) as brug:
        Proces = subprocess.Popen(opdracht() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + brug.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selector = selectors.DefaultSelector(); selector.register(Proces.stdout, selectors.EVENT_READ)
        def ontvangen_e_mail(markering=b'jkoros-native> ', uitvoerbewerking_TIMEOUT=60):
            gegevens = bytearray(); beëindigen_VERSCHUIVING = time.monotonic() + uitvoerbewerking_TIMEOUT
            while markering not in gegevens:
                if time.monotonic() > beëindigen_VERSCHUIVING or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + gegevens.decode('utf-8', 'replace'))
                for 누름값, _ in selector.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: gegevens.extend(조각); transcriptie.extend(조각)
                if b'PANIC:' in gegevens or b'FAIL ' in gegevens: raise AssertionError(gegevens)
            return gegevens.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Shell(invoerregel):
            Proces.stdin.write(invoerregel.encode() + b'\n'); Proces.stdin.flush(); return ontvangen_e_mail()
        try:
            ontvangen_e_mail(); assert 'FTP listening' in Shell('ftpd start')
            bestandsoverdracht_verbinding = ftplib.FTP(); bestandsoverdracht_verbinding.encoding = 'utf-8'; bestandsoverdracht_verbinding.connect('127.0.0.1', poortnummer, timeout=20); bestandsoverdracht_verbinding.login()
            payload_gegevens = bytes(range(256)) * 32
            bestandsoverdracht_verbinding.storbinary('STOR binary.dat', io.BytesIO(payload_gegevens))
            resultaat = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR binary.dat', resultaat.extend)
            assert resultaat == payload_gegevens; assert bestandsoverdracht_verbinding.size('binary.dat') == len(payload_gegevens)
            validatie_Rapport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            bestandsoverdracht_verbinding.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Shell('cat 한글.txt')
            assert '한글.txt' in bestandsoverdracht_verbinding.nlst()
            assert dict(bestandsoverdracht_verbinding.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validatie_Rapport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: bestandsoverdracht_verbinding.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            resultaat = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR binary.dat', resultaat.extend); assert resultaat == payload_gegevens
            validatie_Rapport['checks'].append('oversized replacement rejected; previous file preserved')
            with bestandsoverdracht_verbinding.transfercmd('STOR pending.txt') as Upload_Files:
                # A control command must not change the active upload's destination.
                assert bestandsoverdracht_verbinding.size('binary.dat') == len(payload_gegevens)
                Upload_Files.sendall(b'UPLOAD TARGET PRESERVED')
            assert bestandsoverdracht_verbinding.voidresp().startswith('226')
            resultaat = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR pending.txt', resultaat.extend)
            assert resultaat == b'UPLOAD TARGET PRESERVED'
            resultaat = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR binary.dat', resultaat.extend)
            assert resultaat == payload_gegevens
            bestandsoverdracht_verbinding.delete('pending.txt')
            validatie_Rapport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            bestandsoverdracht_verbinding.storbinary('STOR 인사.jar', io.BytesIO(Archief.getvalue()))
            tekst = Shell('java -jar 인사.jar 누리')
            assert 'JAR Uitvoeren_opdracht: 누리' in tekst and 'Eigen kernel_WAARDE bestand' in tekst and 'exit 0' in tekst, tekst
            tekst = Shell('./인사.jar 세상')
            assert 'JAR Uitvoeren_opdracht: 세상' in tekst and 'exit 0' in tekst, tekst
            validatie_Rapport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct gegevens { int nummer; double 비율; };\nint SOM_WAARDE(int n) { return n ? n + SOM_WAARDE(n-1) : 0; }\nint main(void) { struct gegevens WAARDE = {SOM_WAARDE(10), 1.25}; if (WAARDE.nummer != 55 || WAARDE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int Guides = open_Bestand("cc.txt", lezen_schrijven | 없으면만들기 | afkappen_Inhoud, 0600); if (Guides < 0) return 1; schrijven_Bestand_gegevens(Guides, 인사, sizeof(인사)-1); Sluiten_Bestand(Guides); schrijven_Bestand_gegevens(1, 인사, sizeof(인사)-1); return 0; }\n'
            bestandsoverdracht_verbinding.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            tekst = Shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in tekst and 'exit 0' in tekst, tekst
            tekst = Shell('run 한글.elf'); assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst, tekst
            assert 'CC NATIVE PASS' in Shell('cat cc.txt')
            uitvoerbaar_bestand = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR 한글.elf', uitvoerbaar_bestand.extend)
            assert uitvoerbaar_bestand[:4] == b'\x7fELF' and uitvoerbaar_bestand[18:20] == b'\xb7\x00'
            bestandsoverdracht_verbinding.storbinary('STOR kopiëren_WAARDE.elf', io.BytesIO(uitvoerbaar_bestand)); tekst = Shell('run kopiëren_WAARDE.elf'); assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst, tekst
            bestandsoverdracht_verbinding.storbinary('STOR Uitvoeren_opdracht', io.BytesIO(uitvoerbaar_bestand)); tekst=Shell('./Uitvoeren_opdracht');assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst,tekst
            bestandsoverdracht_verbinding.storbinary('STOR Naam.txt', io.BytesIO(uitvoerbaar_bestand)); tekst=Shell('./Naam.txt');assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst,tekst
            Shell('rm Uitvoeren_opdracht Naam.txt')
            validatie_Rapport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Shell('rm binary.dat 한글.txt 한글.c 한글.elf kopiëren_WAARDE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(HR_gegevens/'linux-reference')
            bestandsoverdracht_verbinding.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            tekst=Shell('./리눅스인사');assert 'exit -8' in tekst,tekst
            tekst=Shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in tekst,tekst
            assert 'LINUX ELF FILE IO' in Shell('cat linux.txt')
            bestandsoverdracht_verbinding.delete('리눅스인사');bestandsoverdracht_verbinding.delete('linux.txt')
            bestandsoverdracht_verbinding.storbinary('STOR ONWAAR_WAARDE.elf',io.BytesIO(b'plain text'))
            assert '실행할 nummer 없습니다:' in Shell('./ONWAAR_WAARDE.elf');bestandsoverdracht_verbinding.delete('ONWAAR_WAARDE.elf')
            validatie_Rapport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as echo_server_invoer:
                NET_bron = HR_gegevens/'extern_communicatie.java'
                NET_bron.write_text('''import java.net.*; import java.io.*;
public class extern_communicatie { public static void main(String[] args) throws Exception {
 Socket Verbinden = Nederlands.Eigen.verbinding_transport.Verbinden("10.0.2.2", Integer.parseInt(args[0]));
 Verbinden.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] broncode = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<broncode.length;i++) if (Verbinden.getInputStream().read() != (broncode[i]&255)) throw new RuntimeException("TCP mismatch");
 Verbinden.close();
 DatagramSocket eindpunt = Nederlands.Eigen.communicatie.Openen(0); Nederlands.Eigen.communicatie.TIMEOUT(eindpunt, 500);
 Nederlands.Eigen.communicatie.e_mailen(eindpunt, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Nederlands.Eigen.communicatie.ontvangen(eindpunt).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 eindpunt.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Taken_wortel/'build/java-library/classes'),'-d',str(HR_gegevens),str(NET_bron)])
                bestandsoverdracht_verbinding.storbinary('STOR extern_communicatie.class', io.BytesIO((HR_gegevens/'extern_communicatie.class').read_bytes()))
                tekst = Shell('java extern_communicatie {} {}'.format(echo_server_invoer.TCP_poort, echo_server_invoer.UDP_poort))
                assert 'EXTERNAL TCP UDP PASS' in tekst and '10.0.2.2' in tekst and 'exit 0' in tekst, tekst
                assert echo_server_invoer.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, echo_server_invoer.수신됨
                assert not echo_server_invoer.오류들, echo_server_invoer.오류들
            validatie_Rapport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            bestandsoverdracht_verbinding.delete('extern_communicatie.class')
            server_bron=HR_gegevens/'server_test.java'
            server_bron.write_text('''import java.net.*; public class server_test {
 public static void main(String[] args) throws Exception {
  ServerSocket server_WAARDE = new ServerSocket(9300); DatagramSocket eindpunt = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gast_WAARDE = server_WAARDE.accept();
  gast_WAARDE.getOutputStream().write(gast_WAARDE.getInputStream().read()+1); gast_WAARDE.close(); server_WAARDE.close();
  byte[] Inhoud_WAARDE = new byte[8]; DatagramPacket datagram = new DatagramPacket(Inhoud_WAARDE, Inhoud_WAARDE.length); eindpunt.receive(datagram);
  eindpunt.send(datagram); eindpunt.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(HR_gegevens),str(server_bron)])
            bestandsoverdracht_verbinding.storbinary('STOR server_test.class',io.BytesIO((HR_gegevens/'server_test.class').read_bytes()))
            Proces.stdin.write('java server_test\n'.encode());Proces.stdin.flush();ontvangen_e_mail(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_Stream_poort),timeout=5) as peer_WAARDE:
                peer_WAARDE.sendall(b'A');assert peer_WAARDE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_WAARDE:
                peer_WAARDE.settimeout(5);peer_WAARDE.sendto(b'UDP-IN',('127.0.0.1',server_datagram_poort));assert peer_WAARDE.recvfrom(512)[0]==b'UDP-IN'
            tekst=ontvangen_e_mail();assert 'INBOUND TCP UDP PASS' in tekst and 'exit 0' in tekst,tekst
            validatie_Rapport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            bestandsoverdracht_verbinding.delete('server_test.class')
            instructie_REEKS = 'public class 빛 { public static void main(String[] argumenten) throws Exception { int SOM_WAARDE = 0; int nummer = 1; while (nummer <= 10) { SOM_WAARDE = SOM_WAARDE + nummer; nummer = nummer + 1; } Nederlands.Eigen.tekstuitvoer.schrijven_nummer(SOM_WAARDE); Nederlands.Eigen.bestand.Schrijven("aot.txt", "한글 AOT bestand 😀"); Nederlands.Eigen.tekstuitvoer.schrijven_lijn(Nederlands.Eigen.bestand.Lezen("aot.txt")); } }'
            bestandsoverdracht_verbinding.storbinary('STOR 빛.java', io.BytesIO(instructie_REEKS.encode()))
            tekst = Shell('javac 빛.java'); assert 'exit 0' in tekst and 'Compiled:' in tekst, tekst
            tekst = Shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in tekst and 'exit 0' in tekst, tekst
            tekst = Shell('run 빛.elf'); assert '\n55\n' in tekst and '한글 AOT bestand 😀' in tekst and 'exit 0' in tekst, tekst
            systeemeigen = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR 빛.elf', systeemeigen.extend)
            tekst = Shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in tekst and 'unsupported' in tekst, tekst
            보존자료 = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR 빛.elf', 보존자료.extend); assert systeemeigen == 보존자료
            바이트코드 = bytearray(); bestandsoverdracht_verbinding.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            bestandsoverdracht_verbinding.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            tekst = Shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in tekst and 'exit 0' in tekst, tekst
            tekst = Shell('run 빛.elf'); assert '\n55\n' in tekst and '한글 AOT bestand 😀' in tekst and 'exit 0' in tekst, tekst
            validatie_Rapport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validatie_Rapport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statisch_bron=HR_gegevens/'statisch_test.java'
            statisch_bron.write_text('''public class statisch_test {
 static int Taken_wortel = 3;
 static int SOM_WAARDE(int n) { return n == 0 ? 0 : n + SOM_WAARDE(n-1); }
 public static void main(String[] argumenten) {
  int[] WAARDE = new int[] {Taken_wortel, SOM_WAARDE(10)};
  System.out.println(WAARDE[0] + WAARDE[1]); System.out.println(argumenten[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(HR_gegevens),str(statisch_bron)])
            bestandsoverdracht_verbinding.storbinary('STOR statisch_test.class',io.BytesIO((HR_gegevens/'statisch_test.class').read_bytes()))
            tekst=Shell('jaot statisch_test.class -o statisch_test.elf');assert 'exit 0' in tekst,tekst
            tekst=Shell('run statisch_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in tekst,tekst
            bestandsoverdracht_verbinding.delete('statisch_test.class');bestandsoverdracht_verbinding.delete('statisch_test.elf')
            validatie_Rapport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archief.getvalue());손상자료[14]^=1
            bestandsoverdracht_verbinding.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            tekst=Shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in tekst,tekst
            validatie_Rapport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            bestandsoverdracht_verbinding.quit(); assert 'FTP stopped' in Shell('ftpd stop')
            assert not brug.fout, brug.fout
            validatie_Rapport.update(passed=True, frames_to_guest=brug.커널수신틀수, frames_from_guest=brug.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selector.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transcriptie.extend(조각)
            brug.Onderbreken_gebeurtenis.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            selector.close(); Proces.stdin.close(); Proces.stdout.close()
            validatie_Rapport['bridge_error'] = brug.fout
            validatie_Rapport['frames_to_guest'] = brug.커널수신틀수; validatie_Rapport['frames_from_guest'] = brug.커널발신틀수
            (HR_gegevens/'packets.json').write_text(json.dumps(brug.traceerlogboek,indent=2)+'\n')
            (HR_gegevens / 'serial.log').write_bytes(transcriptie)
            (HR_gegevens / 'report.json').write_text(json.dumps(validatie_Rapport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': starten()
