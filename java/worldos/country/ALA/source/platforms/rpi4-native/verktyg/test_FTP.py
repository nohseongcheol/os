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
from brygga_3de4fe3a import brygga_3de4fe3a
from köra_kommando import åtgärd_rot, kommando
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Kör():
    KR_data = åtgärd_rot / 'build/verification/ftp'; KR_data.mkdir(parents=True, exist_ok=True)
    validering_Rapport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((åtgärd_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    avskrift = bytearray()
    자바원문 = KR_data / 'test_bunt.java'
    자바원문.write_text('public class test_bunt { public static void main(String[] argument) throws Exception { Svenska.eget.utmatningsposition.skriva_rad("JAR köra_kommando: " + argument[0]); Svenska.eget.filnamn.Skriv("jar.txt", "eget kärna_värde filnamn"); Svenska.eget.utmatningsposition.skriva_rad(Svenska.eget.filnamn.Läs("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(åtgärd_rot/'build/java-library/classes'), '-d', str(KR_data), str(자바원문)])
    Arkiv = io.BytesIO()
    with zipfile.ZipFile(Arkiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_bunt\r\n\r\n')
        자바꾸러미.write(str(KR_data/'test_bunt.class'), 'test_bunt.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); portnummer = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_flöde_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagram_port = 임시자원.getsockname()[1]
    with brygga_3de4fe3a(portnummer, ['tcp:{}:9300'.format(server_flöde_port), 'udp:{}:9301'.format(server_datagram_port)], Capture=True) as brygga:
        Process = subprocess.Popen(kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + brygga.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        väljare = selectors.DefaultSelector(); väljare.register(Process.stdout, selectors.EVENT_READ)
        def få_dokument(markör_8b722c5f=b'jkoros-native> ', körning_TIMEOUT=60):
            data = bytearray(); avsluta_FÖRSKJUTNING = time.monotonic() + körning_TIMEOUT
            while markör_8b722c5f not in data:
                if time.monotonic() > avsluta_FÖRSKJUTNING or Process.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in väljare.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); avskrift.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Shell(inmatningsrad):
            Process.stdin.write(inmatningsrad.encode() + b'\n'); Process.stdin.flush(); return få_dokument()
        try:
            få_dokument(); assert 'FTP listening' in Shell('ftpd start')
            filöverföring_kontakt = ftplib.FTP(); filöverföring_kontakt.encoding = 'utf-8'; filöverföring_kontakt.connect('127.0.0.1', portnummer, timeout=20); filöverföring_kontakt.login()
            nyttolast_data = bytes(range(256)) * 32
            filöverföring_kontakt.storbinary('STOR binary.dat', io.BytesIO(nyttolast_data))
            RESULTAT = bytearray(); filöverföring_kontakt.retrbinary('RETR binary.dat', RESULTAT.extend)
            assert RESULTAT == nyttolast_data; assert filöverföring_kontakt.size('binary.dat') == len(nyttolast_data)
            validering_Rapport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            filöverföring_kontakt.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Shell('cat 한글.txt')
            assert '한글.txt' in filöverföring_kontakt.nlst()
            assert dict(filöverföring_kontakt.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validering_Rapport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: filöverföring_kontakt.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            RESULTAT = bytearray(); filöverföring_kontakt.retrbinary('RETR binary.dat', RESULTAT.extend); assert RESULTAT == nyttolast_data
            validering_Rapport['checks'].append('oversized replacement rejected; previous file preserved')
            with filöverföring_kontakt.transfercmd('STOR pending.txt') as Upload_Filer:
                # A control command must not change the active upload's destination.
                assert filöverföring_kontakt.size('binary.dat') == len(nyttolast_data)
                Upload_Filer.sendall(b'UPLOAD TARGET PRESERVED')
            assert filöverföring_kontakt.voidresp().startswith('226')
            RESULTAT = bytearray(); filöverföring_kontakt.retrbinary('RETR pending.txt', RESULTAT.extend)
            assert RESULTAT == b'UPLOAD TARGET PRESERVED'
            RESULTAT = bytearray(); filöverföring_kontakt.retrbinary('RETR binary.dat', RESULTAT.extend)
            assert RESULTAT == nyttolast_data
            filöverföring_kontakt.delete('pending.txt')
            validering_Rapport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            filöverföring_kontakt.storbinary('STOR 인사.jar', io.BytesIO(Arkiv.getvalue()))
            text = Shell('java -jar 인사.jar 누리')
            assert 'JAR köra_kommando: 누리' in text and 'eget kärna_värde filnamn' in text and 'exit 0' in text, text
            text = Shell('./인사.jar 세상')
            assert 'JAR köra_kommando: 세상' in text and 'exit 0' in text, text
            validering_Rapport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int nummer; double 비율; };\nint SUM_värde(int n) { return n ? n + SUM_värde(n-1) : 0; }\nint main(void) { struct data värde = {SUM_värde(10), 1.25}; if (värde.nummer != 55 || värde.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = skapa_fil("cc.txt", läsa_skriva | 없으면만들기 | trimma_Innehåll, 0600); if (문서 < 0) return 1; skriva_fil_data(문서, 인사, sizeof(인사)-1); Stäng_fil(문서); skriva_fil_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            filöverföring_kontakt.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            text = Shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = Shell('run 한글.elf'); assert 'CC NATIVE PASS' in text and 'exit 0' in text, text
            assert 'CC NATIVE PASS' in Shell('cat cc.txt')
            körbar_fil_fil = bytearray(); filöverföring_kontakt.retrbinary('RETR 한글.elf', körbar_fil_fil.extend)
            assert körbar_fil_fil[:4] == b'\x7fELF' and körbar_fil_fil[18:20] == b'\xb7\x00'
            filöverföring_kontakt.storbinary('STOR kopia_värde.elf', io.BytesIO(körbar_fil_fil)); text = Shell('run kopia_värde.elf'); assert 'CC NATIVE PASS' in text and 'exit 0' in text, text
            filöverföring_kontakt.storbinary('STOR köra_kommando', io.BytesIO(körbar_fil_fil)); text=Shell('./köra_kommando');assert 'CC NATIVE PASS' in text and 'exit 0' in text,text
            filöverföring_kontakt.storbinary('STOR Namn.txt', io.BytesIO(körbar_fil_fil)); text=Shell('./Namn.txt');assert 'CC NATIVE PASS' in text and 'exit 0' in text,text
            Shell('rm köra_kommando Namn.txt')
            validering_Rapport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Shell('rm binary.dat 한글.txt 한글.c 한글.elf kopia_värde.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_data/'linux-reference')
            filöverföring_kontakt.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            text=Shell('./리눅스인사');assert 'exit -8' in text,text
            text=Shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in text,text
            assert 'LINUX ELF FILE IO' in Shell('cat linux.txt')
            filöverföring_kontakt.delete('리눅스인사');filöverföring_kontakt.delete('linux.txt')
            filöverföring_kontakt.storbinary('STOR FALSKT_värde.elf',io.BytesIO(b'plain text'))
            assert '실행할 nummer 없습니다:' in Shell('./FALSKT_värde.elf');filöverföring_kontakt.delete('FALSKT_värde.elf')
            validering_Rapport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as UppdateraSkärm_server_post:
                NET_källa = KR_data/'extern_kommunikation.java'
                NET_källa.write_text('''import java.net.*; import java.io.*;
public class extern_kommunikation { public static void main(String[] args) throws Exception {
 Socket Anslut = Svenska.eget.kontakt_transport.Anslut("10.0.2.2", Integer.parseInt(args[0]));
 Anslut.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] källfil = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<källfil.length;i++) if (Anslut.getInputStream().read() != (källfil[i]&255)) throw new RuntimeException("TCP mismatch");
 Anslut.close();
 DatagramSocket deltagare = Svenska.eget.kommunikation.Öppna(0); Svenska.eget.kommunikation.TIMEOUT(deltagare, 500);
 Svenska.eget.kommunikation.skicka(deltagare, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Svenska.eget.kommunikation.få(deltagare).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 deltagare.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(åtgärd_rot/'build/java-library/classes'),'-d',str(KR_data),str(NET_källa)])
                filöverföring_kontakt.storbinary('STOR extern_kommunikation.class', io.BytesIO((KR_data/'extern_kommunikation.class').read_bytes()))
                text = Shell('java extern_kommunikation {} {}'.format(UppdateraSkärm_server_post.TCP_port, UppdateraSkärm_server_post.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in text and '10.0.2.2' in text and 'exit 0' in text, text
                assert UppdateraSkärm_server_post.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, UppdateraSkärm_server_post.수신됨
                assert not UppdateraSkärm_server_post.오류들, UppdateraSkärm_server_post.오류들
            validering_Rapport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            filöverföring_kontakt.delete('extern_kommunikation.class')
            server_källa=KR_data/'server_test.java'
            server_källa.write_text('''import java.net.*; public class server_test {
 public static void main(String[] args) throws Exception {
  ServerSocket server_värde = new ServerSocket(9300); DatagramSocket deltagare = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gäst_värde = server_värde.accept();
  gäst_värde.getOutputStream().write(gäst_värde.getInputStream().read()+1); gäst_värde.close(); server_värde.close();
  byte[] Innehåll_värde = new byte[8]; DatagramPacket datagram = new DatagramPacket(Innehåll_värde, Innehåll_värde.length); deltagare.receive(datagram);
  deltagare.send(datagram); deltagare.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(server_källa)])
            filöverföring_kontakt.storbinary('STOR server_test.class',io.BytesIO((KR_data/'server_test.class').read_bytes()))
            Process.stdin.write('java server_test\n'.encode());Process.stdin.flush();få_dokument(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_flöde_port),timeout=5) as peer_värde:
                peer_värde.sendall(b'A');assert peer_värde.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_värde:
                peer_värde.settimeout(5);peer_värde.sendto(b'UDP-IN',('127.0.0.1',server_datagram_port));assert peer_värde.recvfrom(512)[0]==b'UDP-IN'
            text=få_dokument();assert 'INBOUND TCP UDP PASS' in text and 'exit 0' in text,text
            validering_Rapport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            filöverföring_kontakt.delete('server_test.class')
            instruktion_SEKVENS = 'public class 빛 { public static void main(String[] argument) throws Exception { int SUM_värde = 0; int nummer = 1; while (nummer <= 10) { SUM_värde = SUM_värde + nummer; nummer = nummer + 1; } Svenska.eget.utmatningsposition.skriva_nummer(SUM_värde); Svenska.eget.filnamn.Skriv("aot.txt", "한글 AOT filnamn 😀"); Svenska.eget.utmatningsposition.skriva_rad(Svenska.eget.filnamn.Läs("aot.txt")); } }'
            filöverföring_kontakt.storbinary('STOR 빛.java', io.BytesIO(instruktion_SEKVENS.encode()))
            text = Shell('javac 빛.java'); assert 'exit 0' in text and 'Compiled:' in text, text
            text = Shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = Shell('run 빛.elf'); assert '\n55\n' in text and '한글 AOT filnamn 😀' in text and 'exit 0' in text, text
            ursprunglig = bytearray(); filöverföring_kontakt.retrbinary('RETR 빛.elf', ursprunglig.extend)
            text = Shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in text and 'unsupported' in text, text
            보존자료 = bytearray(); filöverföring_kontakt.retrbinary('RETR 빛.elf', 보존자료.extend); assert ursprunglig == 보존자료
            바이트코드 = bytearray(); filöverföring_kontakt.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            filöverföring_kontakt.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            text = Shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in text and 'exit 0' in text, text
            text = Shell('run 빛.elf'); assert '\n55\n' in text and '한글 AOT filnamn 😀' in text and 'exit 0' in text, text
            validering_Rapport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validering_Rapport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statisk_källa=KR_data/'statisk_test.java'
            statisk_källa.write_text('''public class statisk_test {
 static int åtgärd_rot = 3;
 static int SUM_värde(int n) { return n == 0 ? 0 : n + SUM_värde(n-1); }
 public static void main(String[] argument) {
  int[] värde = new int[] {åtgärd_rot, SUM_värde(10)};
  System.out.println(värde[0] + värde[1]); System.out.println(argument[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(statisk_källa)])
            filöverföring_kontakt.storbinary('STOR statisk_test.class',io.BytesIO((KR_data/'statisk_test.class').read_bytes()))
            text=Shell('jaot statisk_test.class -o statisk_test.elf');assert 'exit 0' in text,text
            text=Shell('run statisk_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in text,text
            filöverföring_kontakt.delete('statisk_test.class');filöverföring_kontakt.delete('statisk_test.elf')
            validering_Rapport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arkiv.getvalue());손상자료[14]^=1
            filöverföring_kontakt.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            text=Shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in text,text
            validering_Rapport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            filöverföring_kontakt.quit(); assert 'FTP stopped' in Shell('ftpd stop')
            assert not brygga.fel, brygga.fel
            validering_Rapport.update(passed=True, frames_to_guest=brygga.커널수신틀수, frames_from_guest=brygga.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in väljare.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: avskrift.extend(조각)
            brygga.Pausa_händelse.set()
            Process.terminate()
            try: Process.wait(timeout=5)
            except subprocess.TimeoutExpired: Process.kill(); Process.wait()
            väljare.close(); Process.stdin.close(); Process.stdout.close()
            validering_Rapport['bridge_error'] = brygga.fel
            validering_Rapport['frames_to_guest'] = brygga.커널수신틀수; validering_Rapport['frames_from_guest'] = brygga.커널발신틀수
            (KR_data/'packets.json').write_text(json.dumps(brygga.spårningslogg,indent=2)+'\n')
            (KR_data / 'serial.log').write_bytes(avskrift)
            (KR_data / 'report.json').write_text(json.dumps(validering_Rapport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Kör()
