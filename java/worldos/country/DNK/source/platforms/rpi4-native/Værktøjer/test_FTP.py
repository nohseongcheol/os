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
from Udfør_kommando import To_do_rod, Kommando
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Kør_2():
    KR_data = To_do_rod / 'build/verification/ftp'; KR_data.mkdir(parents=True, exist_ok=True)
    validering_rapport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((To_do_rod / 'build/kernel8.img').read_bytes()).hexdigest()}
    afskrift = bytearray()
    자바원문 = KR_data / 'test_bundt.java'
    자바원문.write_text('public class test_bundt { public static void main(String[] Argumenter) throws Exception { Dansk.eget.Udgang.skrive_linje("JAR Udfør_kommando: " + Argumenter[0]); Dansk.eget.Fil.Skrive("jar.txt", "eget kerne_VÆRDI Fil"); Dansk.eget.Udgang.skrive_linje(Dansk.eget.Fil.Læse("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(To_do_rod/'build/java-library/classes'), '-d', str(KR_data), str(자바원문)])
    Arkiv = io.BytesIO()
    with zipfile.ZipFile(Arkiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_bundt\r\n\r\n')
        자바꾸러미.write(str(KR_data/'test_bundt.class'), 'test_bundt.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); portnummer = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_strøm_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagram_port = 임시자원.getsockname()[1]
    with bro_3de4fe3a(portnummer, ['tcp:{}:9300'.format(server_strøm_port), 'udp:{}:9301'.format(server_datagram_port)], optage=True) as bro:
        Proces = subprocess.Popen(Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + bro.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
        def modtage_mail(mærke=b'jkoros-native> ', udførelse_TIMEOUT=60):
            data = bytearray(); afslutte_et_opkald_FORSKYDNING = time.monotonic() + udførelse_TIMEOUT
            while mærke not in data:
                if time.monotonic() > afslutte_et_opkald_FORSKYDNING or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in selektor.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); afskrift.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Shell(Linje):
            Proces.stdin.write(Linje.encode() + b'\n'); Proces.stdin.flush(); return modtage_mail()
        try:
            modtage_mail(); assert 'FTP listening' in Shell('ftpd start')
            filoverførsel_forbindelse = ftplib.FTP(); filoverførsel_forbindelse.encoding = 'utf-8'; filoverførsel_forbindelse.connect('127.0.0.1', portnummer, timeout=20); filoverførsel_forbindelse.login()
            nyttedata_data = bytes(range(256)) * 32
            filoverførsel_forbindelse.storbinary('STOR binary.dat', io.BytesIO(nyttedata_data))
            KR = bytearray(); filoverførsel_forbindelse.retrbinary('RETR binary.dat', KR.extend)
            assert KR == nyttedata_data; assert filoverførsel_forbindelse.size('binary.dat') == len(nyttedata_data)
            validering_rapport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            filoverførsel_forbindelse.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Shell('cat 한글.txt')
            assert '한글.txt' in filoverførsel_forbindelse.nlst()
            assert dict(filoverførsel_forbindelse.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validering_rapport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: filoverførsel_forbindelse.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            KR = bytearray(); filoverførsel_forbindelse.retrbinary('RETR binary.dat', KR.extend); assert KR == nyttedata_data
            validering_rapport['checks'].append('oversized replacement rejected; previous file preserved')
            with filoverførsel_forbindelse.transfercmd('STOR pending.txt') as Upload_Filer:
                # A control command must not change the active upload's destination.
                assert filoverførsel_forbindelse.size('binary.dat') == len(nyttedata_data)
                Upload_Filer.sendall(b'UPLOAD TARGET PRESERVED')
            assert filoverførsel_forbindelse.voidresp().startswith('226')
            KR = bytearray(); filoverførsel_forbindelse.retrbinary('RETR pending.txt', KR.extend)
            assert KR == b'UPLOAD TARGET PRESERVED'
            KR = bytearray(); filoverførsel_forbindelse.retrbinary('RETR binary.dat', KR.extend)
            assert KR == nyttedata_data
            filoverførsel_forbindelse.delete('pending.txt')
            validering_rapport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            filoverførsel_forbindelse.storbinary('STOR 인사.jar', io.BytesIO(Arkiv.getvalue()))
            Tekst = Shell('java -jar 인사.jar 누리')
            assert 'JAR Udfør_kommando: 누리' in Tekst and 'eget kerne_VÆRDI Fil' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('./인사.jar 세상')
            assert 'JAR Udfør_kommando: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            validering_rapport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int tal; double 비율; };\nint SUM_VÆRDI(int n) { return n ? n + SUM_VÆRDI(n-1) : 0; }\nint main(void) { struct data VÆRDI = {SUM_VÆRDI(10), 1.25}; if (VÆRDI.tal != 55 || VÆRDI.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = åben_fil("cc.txt", læse_skrive | 없으면만들기 | afkorte_Indhold, 0600); if (문서 < 0) return 1; skrive_fil_data(문서, 인사, sizeof(인사)-1); Luk_fil(문서); skrive_fil_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            filoverførsel_forbindelse.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = Shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in Shell('cat cc.txt')
            eksekverbar_fil = bytearray(); filoverførsel_forbindelse.retrbinary('RETR 한글.elf', eksekverbar_fil.extend)
            assert eksekverbar_fil[:4] == b'\x7fELF' and eksekverbar_fil[18:20] == b'\xb7\x00'
            filoverførsel_forbindelse.storbinary('STOR kopiere_VÆRDI.elf', io.BytesIO(eksekverbar_fil)); Tekst = Shell('run kopiere_VÆRDI.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            filoverførsel_forbindelse.storbinary('STOR Udfør_kommando', io.BytesIO(eksekverbar_fil)); Tekst=Shell('./Udfør_kommando');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            filoverførsel_forbindelse.storbinary('STOR Navn.txt', io.BytesIO(eksekverbar_fil)); Tekst=Shell('./Navn.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            Shell('rm Udfør_kommando Navn.txt')
            validering_rapport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Shell('rm binary.dat 한글.txt 한글.c 한글.elf kopiere_VÆRDI.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_data/'linux-reference')
            filoverførsel_forbindelse.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=Shell('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=Shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in Shell('cat linux.txt')
            filoverførsel_forbindelse.delete('리눅스인사');filoverførsel_forbindelse.delete('linux.txt')
            filoverførsel_forbindelse.storbinary('STOR FALSK_VÆRDI.elf',io.BytesIO(b'plain text'))
            assert '실행할 tal 없습니다:' in Shell('./FALSK_VÆRDI.elf');filoverførsel_forbindelse.delete('FALSK_VÆRDI.elf')
            validering_rapport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as ekko_server_post:
                NET_kilde = KR_data/'바깥통신.java'
                NET_kilde.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Tilslut = Dansk.eget.forbindelse_transport.Tilslut("10.0.2.2", Integer.parseInt(args[0]));
 Tilslut.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] KILDE = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<KILDE.length;i++) if (Tilslut.getInputStream().read() != (KILDE[i]&255)) throw new RuntimeException("TCP mismatch");
 Tilslut.close();
 DatagramSocket slutpunkt = Dansk.eget.통신.Åbn(0); Dansk.eget.통신.TIMEOUT(slutpunkt, 500);
 Dansk.eget.통신.maile(slutpunkt, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Dansk.eget.통신.modtage(slutpunkt).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 slutpunkt.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(To_do_rod/'build/java-library/classes'),'-d',str(KR_data),str(NET_kilde)])
                filoverførsel_forbindelse.storbinary('STOR 바깥통신.class', io.BytesIO((KR_data/'바깥통신.class').read_bytes()))
                Tekst = Shell('java 바깥통신 {} {}'.format(ekko_server_post.TCP_port, ekko_server_post.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert ekko_server_post.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, ekko_server_post.수신됨
                assert not ekko_server_post.오류들, ekko_server_post.오류들
            validering_rapport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            filoverførsel_forbindelse.delete('바깥통신.class')
            server_kilde=KR_data/'server_test.java'
            server_kilde.write_text('''import java.net.*; public class server_test {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VÆRDI = new ServerSocket(9300); DatagramSocket slutpunkt = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gæst_VÆRDI = server_VÆRDI.accept();
  gæst_VÆRDI.getOutputStream().write(gæst_VÆRDI.getInputStream().read()+1); gæst_VÆRDI.close(); server_VÆRDI.close();
  byte[] Indhold_VÆRDI = new byte[8]; DatagramPacket datagram = new DatagramPacket(Indhold_VÆRDI, Indhold_VÆRDI.length); slutpunkt.receive(datagram);
  slutpunkt.send(datagram); slutpunkt.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(server_kilde)])
            filoverførsel_forbindelse.storbinary('STOR server_test.class',io.BytesIO((KR_data/'server_test.class').read_bytes()))
            Proces.stdin.write('java server_test\n'.encode());Proces.stdin.flush();modtage_mail(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_strøm_port),timeout=5) as peer_VÆRDI:
                peer_VÆRDI.sendall(b'A');assert peer_VÆRDI.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_VÆRDI:
                peer_VÆRDI.settimeout(5);peer_VÆRDI.sendto(b'UDP-IN',('127.0.0.1',server_datagram_port));assert peer_VÆRDI.recvfrom(512)[0]==b'UDP-IN'
            Tekst=modtage_mail();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            validering_rapport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            filoverførsel_forbindelse.delete('server_test.class')
            명령열 = 'public class 빛 { public static void main(String[] Argumenter) throws Exception { int SUM_VÆRDI = 0; int tal = 1; while (tal <= 10) { SUM_VÆRDI = SUM_VÆRDI + tal; tal = tal + 1; } Dansk.eget.Udgang.skrive_tal(SUM_VÆRDI); Dansk.eget.Fil.Skrive("aot.txt", "한글 AOT Fil 😀"); Dansk.eget.Udgang.skrive_linje(Dansk.eget.Fil.Læse("aot.txt")); } }'
            filoverførsel_forbindelse.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Tekst = Shell('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = Shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fil 😀' in Tekst and 'exit 0' in Tekst, Tekst
            oprindelig = bytearray(); filoverførsel_forbindelse.retrbinary('RETR 빛.elf', oprindelig.extend)
            Tekst = Shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); filoverførsel_forbindelse.retrbinary('RETR 빛.elf', 보존자료.extend); assert oprindelig == 보존자료
            바이트코드 = bytearray(); filoverførsel_forbindelse.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            filoverførsel_forbindelse.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = Shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = Shell('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fil 😀' in Tekst and 'exit 0' in Tekst, Tekst
            validering_rapport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validering_rapport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statisk_kilde=KR_data/'statisk_test.java'
            statisk_kilde.write_text('''public class statisk_test {
 static int To_do_rod = 3;
 static int SUM_VÆRDI(int n) { return n == 0 ? 0 : n + SUM_VÆRDI(n-1); }
 public static void main(String[] Argumenter) {
  int[] VÆRDI = new int[] {To_do_rod, SUM_VÆRDI(10)};
  System.out.println(VÆRDI[0] + VÆRDI[1]); System.out.println(Argumenter[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_data),str(statisk_kilde)])
            filoverførsel_forbindelse.storbinary('STOR statisk_test.class',io.BytesIO((KR_data/'statisk_test.class').read_bytes()))
            Tekst=Shell('jaot statisk_test.class -o statisk_test.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=Shell('run statisk_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            filoverførsel_forbindelse.delete('statisk_test.class');filoverførsel_forbindelse.delete('statisk_test.elf')
            validering_rapport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arkiv.getvalue());손상자료[14]^=1
            filoverførsel_forbindelse.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=Shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            validering_rapport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            filoverførsel_forbindelse.quit(); assert 'FTP stopped' in Shell('ftpd stop')
            assert not bro.fejl, bro.fejl
            validering_rapport.update(passed=True, frames_to_guest=bro.커널수신틀수, frames_from_guest=bro.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selektor.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: afskrift.extend(조각)
            bro.Afbryd_midlertidigt_hændelse.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            selektor.close(); Proces.stdin.close(); Proces.stdout.close()
            validering_rapport['bridge_error'] = bro.fejl
            validering_rapport['frames_to_guest'] = bro.커널수신틀수; validering_rapport['frames_from_guest'] = bro.커널발신틀수
            (KR_data/'packets.json').write_text(json.dumps(bro.sporingslogfil,indent=2)+'\n')
            (KR_data / 'serial.log').write_bytes(afskrift)
            (KR_data / 'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Kør_2()
