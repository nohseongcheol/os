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
from bro_3de4fe3a import bro_3de4fe3a
from Utfør_kommando import speile_rot, Kommando
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Kjør_2():
    KR_data = speile_rot / 'build/verification/ftp'; KR_data.mkdir(parents=True, exist_ok=True)
    validering_rapport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((speile_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    utskrift = bytearray()
    자바원문 = KR_data / 'test_bunt.java'
    자바원문.write_text('public class test_bunt { public static void main(String[] Argumenter) throws Exception { norsk.eget.Utgang.skrive_linje("JAR Utfør_kommando: " + Argumenter[0]); norsk.eget.Fil.Skriv("jar.txt", "eget kjerne_VERDI Fil"); norsk.eget.Utgang.skrive_linje(norsk.eget.Fil.Les("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(speile_rot/'build/java-library/classes'), '-d', str(KR_data), str(자바원문)])
    Arkiv = io.BytesIO()
    with zipfile.ZipFile(Arkiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_bunt\r\n\r\n')
        자바꾸러미.write(str(KR_data/'test_bunt.class'), 'test_bunt.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); portnummer = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_strøm_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagram_port = 임시자원.getsockname()[1]
    with bro_3de4fe3a(portnummer, ['tcp:{}:9300'.format(server_strøm_port), 'udp:{}:9301'.format(server_datagram_port)], hente=True) as bro:
        Prosess = subprocess.Popen(Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + bro.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        velger = selectors.DefaultSelector(); velger.register(Prosess.stdout, selectors.EVENT_READ)
        def motta_e_post(tusj=b'jkoros-native> ', kjøring_TIMEOUT=60):
            data = bytearray(); avslutte_en_samtale_FORSKYVNING = time.monotonic() + kjøring_TIMEOUT
            while tusj not in data:
                if time.monotonic() > avslutte_en_samtale_FORSKYVNING or Prosess.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in velger.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); utskrift.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Shell(Linje):
            Prosess.stdin.write(Linje.encode() + b'\n'); Prosess.stdin.flush(); return motta_e_post()
        try:
            motta_e_post(); assert 'FTP listening' in Shell('ftpd start')
            filoverføring_kontakt = ftplib.FTP(); filoverføring_kontakt.encoding = 'utf-8'; filoverføring_kontakt.connect('127.0.0.1', portnummer, timeout=20); filoverføring_kontakt.login()
            nyttelast_data = bytes(range(256)) * 32
            filoverføring_kontakt.storbinary('STOR binary.dat', io.BytesIO(nyttelast_data))
            KR = bytearray(); filoverføring_kontakt.retrbinary('RETR binary.dat', KR.extend)
            assert KR == nyttelast_data; assert filoverføring_kontakt.size('binary.dat') == len(nyttelast_data)
            validering_rapport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            filoverføring_kontakt.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Shell('cat 한글.txt')
            assert '한글.txt' in filoverføring_kontakt.nlst()
            assert dict(filoverføring_kontakt.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validering_rapport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: filoverføring_kontakt.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            KR = bytearray(); filoverføring_kontakt.retrbinary('RETR binary.dat', KR.extend); assert KR == nyttelast_data
            validering_rapport['checks'].append('oversized replacement rejected; previous file preserved')
            with filoverføring_kontakt.transfercmd('STOR pending.txt') as Upload_Filer:
                # A control command must not change the active upload's destination.
                assert filoverføring_kontakt.size('binary.dat') == len(nyttelast_data)
                Upload_Filer.sendall(b'UPLOAD TARGET PRESERVED')
            assert filoverføring_kontakt.voidresp().startswith('226')
            KR = bytearray(); filoverføring_kontakt.retrbinary('RETR pending.txt', KR.extend)
            assert KR == b'UPLOAD TARGET PRESERVED'
            KR = bytearray(); filoverføring_kontakt.retrbinary('RETR binary.dat', KR.extend)
            assert KR == nyttelast_data
            filoverføring_kontakt.delete('pending.txt')
            validering_rapport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            filoverføring_kontakt.storbinary('STOR 인사.jar', io.BytesIO(Arkiv.getvalue()))
            Tekst = Shell('java -jar 인사.jar 누리')
            assert 'JAR Utfør_kommando: 누리' in Tekst and 'eget kjerne_VERDI Fil' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('./인사.jar 세상')
            assert 'JAR Utfør_kommando: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            validering_rapport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int nummer; double 비율; };\nint SUMMER_VERDI(int n) { return n ? n + SUMMER_VERDI(n-1) : 0; }\nint main(void) { struct data VERDI = {SUMMER_VERDI(10), 1.25}; if (VERDI.nummer != 55 || VERDI.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = åpen_Fil("cc.txt", lese_og_skrive | 없으면만들기 | avkorte_Innhold, 0600); if (문서 < 0) return 1; skrive_Fil_data(문서, 인사, sizeof(인사)-1); Lukk_Fil(문서); skrive_Fil_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            filoverføring_kontakt.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = Shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in Shell('cat cc.txt')
            kjørbar_fil = bytearray(); filoverføring_kontakt.retrbinary('RETR 한글.elf', kjørbar_fil.extend)
            assert kjørbar_fil[:4] == b'\x7fELF' and kjørbar_fil[18:20] == b'\xb7\x00'
            filoverføring_kontakt.storbinary('STOR kopiere_VERDI.elf', io.BytesIO(kjørbar_fil)); Tekst = Shell('run kopiere_VERDI.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            filoverføring_kontakt.storbinary('STOR Utfør_kommando', io.BytesIO(kjørbar_fil)); Tekst=Shell('./Utfør_kommando');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            filoverføring_kontakt.storbinary('STOR Navn.txt', io.BytesIO(kjørbar_fil)); Tekst=Shell('./Navn.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            Shell('rm Utfør_kommando Navn.txt')
            validering_rapport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Shell('rm binary.dat 한글.txt 한글.c 한글.elf kopiere_VERDI.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_data/'linux-reference')
            filoverføring_kontakt.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=Shell('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=Shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in Shell('cat linux.txt')
            filoverføring_kontakt.delete('리눅스인사');filoverføring_kontakt.delete('linux.txt')
            filoverføring_kontakt.storbinary('STOR USANN_VERDI.elf',io.BytesIO(b'plain text'))
            assert '실행할 nummer 없습니다:' in Shell('./USANN_VERDI.elf');filoverføring_kontakt.delete('USANN_VERDI.elf')
            validering_rapport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as oppdatere_skjerm_server_oppføring:
                netto_kilde = KR_data/'바깥통신.java'
                netto_kilde.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Koble_til = norsk.eget.kontakt_transport.Koble_til("10.0.2.2", Integer.parseInt(args[0]));
 Koble_til.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] KILDE = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<KILDE.length;i++) if (Koble_til.getInputStream().read() != (KILDE[i]&255)) throw new RuntimeException("TCP mismatch");
 Koble_til.close();
 DatagramSocket deltaker = norsk.eget.통신.Åpne(0); norsk.eget.통신.TIMEOUT(deltaker, 500);
 norsk.eget.통신.sende(deltaker, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!norsk.eget.통신.motta(deltaker).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 deltaker.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(speile_rot/'build/java-library/classes'),'-d',str(KR_data),str(netto_kilde)])
                filoverføring_kontakt.storbinary('STOR 바깥통신.class', io.BytesIO((KR_data/'바깥통신.class').read_bytes()))
                Tekst = Shell('java 바깥통신 {} {}'.format(oppdatere_skjerm_server_oppføring.TCP_port, oppdatere_skjerm_server_oppføring.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert oppdatere_skjerm_server_oppføring.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, oppdatere_skjerm_server_oppføring.수신됨
                assert not oppdatere_skjerm_server_oppføring.오류들, oppdatere_skjerm_server_oppføring.오류들
            validering_rapport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            filoverføring_kontakt.delete('바깥통신.class')
            server_kilde=KR_data/'server_test.java'
            server_kilde.write_text('''import java.net.*; public class server_test {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VERDI = new ServerSocket(9300); DatagramSocket deltaker = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gjest_VERDI = server_VERDI.accept();
  gjest_VERDI.getOutputStream().write(gjest_VERDI.getInputStream().read()+1); gjest_VERDI.close(); server_VERDI.close();
  byte[] Innhold_VERDI = new byte[8]; DatagramPacket datagram = new DatagramPacket(Innhold_VERDI, Innhold_VERDI.length); deltaker.receive(datagram);
  deltaker.send(datagram); deltaker.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(server_kilde)])
            filoverføring_kontakt.storbinary('STOR server_test.class',io.BytesIO((KR_data/'server_test.class').read_bytes()))
            Prosess.stdin.write('java server_test\n'.encode());Prosess.stdin.flush();motta_e_post(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_strøm_port),timeout=5) as node_VERDI_6a3b6fa7:
                node_VERDI_6a3b6fa7.sendall(b'A');assert node_VERDI_6a3b6fa7.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as node_VERDI_6a3b6fa7:
                node_VERDI_6a3b6fa7.settimeout(5);node_VERDI_6a3b6fa7.sendto(b'UDP-IN',('127.0.0.1',server_datagram_port));assert node_VERDI_6a3b6fa7.recvfrom(512)[0]==b'UDP-IN'
            Tekst=motta_e_post();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            validering_rapport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            filoverføring_kontakt.delete('server_test.class')
            명령열 = 'public class 빛 { public static void main(String[] Argumenter) throws Exception { int SUMMER_VERDI = 0; int nummer = 1; while (nummer <= 10) { SUMMER_VERDI = SUMMER_VERDI + nummer; nummer = nummer + 1; } norsk.eget.Utgang.skrive_nummer(SUMMER_VERDI); norsk.eget.Fil.Skriv("aot.txt", "한글 AOT Fil 😀"); norsk.eget.Utgang.skrive_linje(norsk.eget.Fil.Les("aot.txt")); } }'
            filoverføring_kontakt.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Tekst = Shell('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = Shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fil 😀' in Tekst and 'exit 0' in Tekst, Tekst
            opprinnelig = bytearray(); filoverføring_kontakt.retrbinary('RETR 빛.elf', opprinnelig.extend)
            Tekst = Shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); filoverføring_kontakt.retrbinary('RETR 빛.elf', 보존자료.extend); assert opprinnelig == 보존자료
            바이트코드 = bytearray(); filoverføring_kontakt.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            filoverføring_kontakt.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = Shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fil 😀' in Tekst and 'exit 0' in Tekst, Tekst
            validering_rapport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validering_rapport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statisk_kilde=KR_data/'statisk_test.java'
            statisk_kilde.write_text('''public class statisk_test {
 static int speile_rot = 3;
 static int SUMMER_VERDI(int n) { return n == 0 ? 0 : n + SUMMER_VERDI(n-1); }
 public static void main(String[] Argumenter) {
  int[] VERDI = new int[] {speile_rot, SUMMER_VERDI(10)};
  System.out.println(VERDI[0] + VERDI[1]); System.out.println(Argumenter[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(statisk_kilde)])
            filoverføring_kontakt.storbinary('STOR statisk_test.class',io.BytesIO((KR_data/'statisk_test.class').read_bytes()))
            Tekst=Shell('jaot statisk_test.class -o statisk_test.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=Shell('run statisk_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            filoverføring_kontakt.delete('statisk_test.class');filoverføring_kontakt.delete('statisk_test.elf')
            validering_rapport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arkiv.getvalue());손상자료[14]^=1
            filoverføring_kontakt.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=Shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            validering_rapport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            filoverføring_kontakt.quit(); assert 'FTP stopped' in Shell('ftpd stop')
            assert not bro.feil, bro.feil
            validering_rapport.update(passed=True, frames_to_guest=bro.커널수신틀수, frames_from_guest=bro.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in velger.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: utskrift.extend(조각)
            bro.Pause_hendelse.set()
            Prosess.terminate()
            try: Prosess.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosess.kill(); Prosess.wait()
            velger.close(); Prosess.stdin.close(); Prosess.stdout.close()
            validering_rapport['bridge_error'] = bro.feil
            validering_rapport['frames_to_guest'] = bro.커널수신틀수; validering_rapport['frames_from_guest'] = bro.커널발신틀수
            (KR_data/'packets.json').write_text(json.dumps(bro.sporingslogg,indent=2)+'\n')
            (KR_data / 'serial.log').write_bytes(utskrift)
            (KR_data / 'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Kjør_2()
