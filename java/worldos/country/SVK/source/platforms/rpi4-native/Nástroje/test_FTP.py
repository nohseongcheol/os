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
from sieťový_most import sieťový_most
from Vykonať_príkaz import akcia_koreň, Príkaz
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Spustiť_2():
    KR_údaje = akcia_koreň / 'build/verification/ftp'; KR_údaje.mkdir(parents=True, exist_ok=True)
    overenie_správa = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((akcia_koreň / 'build/kernel8.img').read_bytes()).hexdigest()}
    prepis = bytearray()
    자바원문 = KR_údaje / 'test_zväzok.java'
    자바원문.write_text('public class test_zväzok { public static void main(String[] Argumenty) throws Exception { Slovenský.vlastné.Výstup.zapísať_linka("JAR Vykonať_príkaz: " + Argumenty[0]); Slovenský.vlastné.Súbor.Zápis("jar.txt", "vlastné jadro_VALUE Súbor"); Slovenský.vlastné.Výstup.zapísať_linka(Slovenský.vlastné.Súbor.Čítanie("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akcia_koreň/'build/java-library/classes'), '-d', str(KR_údaje), str(자바원문)])
    Archív = io.BytesIO()
    with zipfile.ZipFile(Archív, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_zväzok\r\n\r\n')
        자바꾸러미.write(str(KR_údaje/'test_zväzok.class'), 'test_zväzok.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); číslo_portu = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagram_port = 임시자원.getsockname()[1]
    with sieťový_most(číslo_portu, ['tcp:{}:9300'.format(server_Stream_port), 'udp:{}:9301'.format(server_datagram_port)], snímať=True) as most:
        Proces = subprocess.Popen(Príkaz() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + most.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
        def dostať_e_mail(fixka=b'jkoros-native> ', 시간제한=60):
            údaje = bytearray(); ukončiť_hovor_Posun = time.monotonic() + 시간제한
            while fixka not in údaje:
                if time.monotonic() > ukončiť_hovor_Posun or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + údaje.decode('utf-8', 'replace'))
                for 누름값, _ in selektor.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: údaje.extend(조각); prepis.extend(조각)
                if b'PANIC:' in údaje or b'FAIL ' in údaje: raise AssertionError(údaje)
            return údaje.decode('utf-8', 'replace').replace('\r\n', '\n')
        def 셸(riadok):
            Proces.stdin.write(riadok.encode() + b'\n'); Proces.stdin.flush(); return dostať_e_mail()
        try:
            dostať_e_mail(); assert 'FTP listening' in 셸('ftpd start')
            prenos_súborov_kontakt = ftplib.FTP(); prenos_súborov_kontakt.encoding = 'utf-8'; prenos_súborov_kontakt.connect('127.0.0.1', číslo_portu, timeout=20); prenos_súborov_kontakt.login()
            údajová_časť_údaje = bytes(range(256)) * 32
            prenos_súborov_kontakt.storbinary('STOR binary.dat', io.BytesIO(údajová_časť_údaje))
            KR = bytearray(); prenos_súborov_kontakt.retrbinary('RETR binary.dat', KR.extend)
            assert KR == údajová_časť_údaje; assert prenos_súborov_kontakt.size('binary.dat') == len(údajová_časť_údaje)
            overenie_správa['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            prenos_súborov_kontakt.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in 셸('cat 한글.txt')
            assert '한글.txt' in prenos_súborov_kontakt.nlst()
            assert dict(prenos_súborov_kontakt.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            overenie_správa['checks'].append('UTF-8 filename and content visible in guest shell')
            try: prenos_súborov_kontakt.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            KR = bytearray(); prenos_súborov_kontakt.retrbinary('RETR binary.dat', KR.extend); assert KR == údajová_časť_údaje
            overenie_správa['checks'].append('oversized replacement rejected; previous file preserved')
            with prenos_súborov_kontakt.transfercmd('STOR pending.txt') as nahrať_Súbory:
                # A control command must not change the active upload's destination.
                assert prenos_súborov_kontakt.size('binary.dat') == len(údajová_časť_údaje)
                nahrať_Súbory.sendall(b'UPLOAD TARGET PRESERVED')
            assert prenos_súborov_kontakt.voidresp().startswith('226')
            KR = bytearray(); prenos_súborov_kontakt.retrbinary('RETR pending.txt', KR.extend)
            assert KR == b'UPLOAD TARGET PRESERVED'
            KR = bytearray(); prenos_súborov_kontakt.retrbinary('RETR binary.dat', KR.extend)
            assert KR == údajová_časť_údaje
            prenos_súborov_kontakt.delete('pending.txt')
            overenie_správa['checks'].append('interleaved SIZE cannot change the active STOR destination')
            prenos_súborov_kontakt.storbinary('STOR 인사.jar', io.BytesIO(Archív.getvalue()))
            Spracovanie_textu = 셸('java -jar 인사.jar 누리')
            assert 'JAR Vykonať_príkaz: 누리' in Spracovanie_textu and 'vlastné jadro_VALUE Súbor' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            Spracovanie_textu = 셸('./인사.jar 세상')
            assert 'JAR Vykonať_príkaz: 세상' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            overenie_správa['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct údaje { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct údaje VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = otvoriť_Súbor("cc.txt", na_čítanie_a_zapisovanie | 없으면만들기 | skrátiť_Obsah, 0600); if (문서 < 0) return 1; zapísať_Súbor_údaje(문서, 인사, sizeof(인사)-1); Zavrieť_Súbor(문서); zapísať_Súbor_údaje(1, 인사, sizeof(인사)-1); return 0; }\n'
            prenos_súborov_kontakt.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Spracovanie_textu = 셸('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            Spracovanie_textu = 셸('run 한글.elf'); assert 'CC NATIVE PASS' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            assert 'CC NATIVE PASS' in 셸('cat cc.txt')
            spustiteľný_súbor = bytearray(); prenos_súborov_kontakt.retrbinary('RETR 한글.elf', spustiteľný_súbor.extend)
            assert spustiteľný_súbor[:4] == b'\x7fELF' and spustiteľný_súbor[18:20] == b'\xb7\x00'
            prenos_súborov_kontakt.storbinary('STOR inštancia_VALUE.elf', io.BytesIO(spustiteľný_súbor)); Spracovanie_textu = 셸('run inštancia_VALUE.elf'); assert 'CC NATIVE PASS' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            prenos_súborov_kontakt.storbinary('STOR Vykonať_príkaz', io.BytesIO(spustiteľný_súbor)); Spracovanie_textu=셸('./Vykonať_príkaz');assert 'CC NATIVE PASS' in Spracovanie_textu and 'exit 0' in Spracovanie_textu,Spracovanie_textu
            prenos_súborov_kontakt.storbinary('STOR Názov.txt', io.BytesIO(spustiteľný_súbor)); Spracovanie_textu=셸('./Názov.txt');assert 'CC NATIVE PASS' in Spracovanie_textu and 'exit 0' in Spracovanie_textu,Spracovanie_textu
            셸('rm Vykonať_príkaz Názov.txt')
            overenie_správa['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            셸('rm binary.dat 한글.txt 한글.c 한글.elf inštancia_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_údaje/'linux-reference')
            prenos_súborov_kontakt.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Spracovanie_textu=셸('./리눅스인사');assert 'exit -8' in Spracovanie_textu,Spracovanie_textu
            Spracovanie_textu=셸('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Spracovanie_textu,Spracovanie_textu
            assert 'LINUX ELF FILE IO' in 셸('cat linux.txt')
            prenos_súborov_kontakt.delete('리눅스인사');prenos_súborov_kontakt.delete('linux.txt')
            prenos_súborov_kontakt.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in 셸('./FALSE_VALUE.elf');prenos_súborov_kontakt.delete('FALSE_VALUE.elf')
            overenie_správa['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as ozvena_server_položka:
                NET_zdroj = KR_údaje/'바깥통신.java'
                NET_zdroj.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Pripojiť = Slovenský.vlastné.연결통신.Pripojiť("10.0.2.2", Integer.parseInt(args[0]));
 Pripojiť.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ZDROJ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ZDROJ.length;i++) if (Pripojiť.getInputStream().read() != (ZDROJ[i]&255)) throw new RuntimeException("TCP mismatch");
 Pripojiť.close();
 DatagramSocket účastník = Slovenský.vlastné.통신.Otvoriť(0); Slovenský.vlastné.통신.TIMEOUT(účastník, 500);
 Slovenský.vlastné.통신.odoslať(účastník, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Slovenský.vlastné.통신.dostať(účastník).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 účastník.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(akcia_koreň/'build/java-library/classes'),'-d',str(KR_údaje),str(NET_zdroj)])
                prenos_súborov_kontakt.storbinary('STOR 바깥통신.class', io.BytesIO((KR_údaje/'바깥통신.class').read_bytes()))
                Spracovanie_textu = 셸('java 바깥통신 {} {}'.format(ozvena_server_položka.TCP_port, ozvena_server_položka.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Spracovanie_textu and '10.0.2.2' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
                assert ozvena_server_položka.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, ozvena_server_položka.수신됨
                assert not ozvena_server_položka.오류들, ozvena_server_položka.오류들
            overenie_správa['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            prenos_súborov_kontakt.delete('바깥통신.class')
            server_zdroj=KR_údaje/'server_test.java'
            server_zdroj.write_text('''import java.net.*; public class server_test {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket účastník = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket hosť_VALUE = server_VALUE.accept();
  hosť_VALUE.getOutputStream().write(hosť_VALUE.getInputStream().read()+1); hosť_VALUE.close(); server_VALUE.close();
  byte[] obsah_VALUE = new byte[8]; DatagramPacket datagram = new DatagramPacket(obsah_VALUE, obsah_VALUE.length); účastník.receive(datagram);
  účastník.send(datagram); účastník.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_údaje),str(server_zdroj)])
            prenos_súborov_kontakt.storbinary('STOR server_test.class',io.BytesIO((KR_údaje/'server_test.class').read_bytes()))
            Proces.stdin.write('java server_test\n'.encode());Proces.stdin.flush();dostať_e_mail(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_Stream_port),timeout=5) as partnerský_uzol_VALUE:
                partnerský_uzol_VALUE.sendall(b'A');assert partnerský_uzol_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as partnerský_uzol_VALUE:
                partnerský_uzol_VALUE.settimeout(5);partnerský_uzol_VALUE.sendto(b'UDP-IN',('127.0.0.1',server_datagram_port));assert partnerský_uzol_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Spracovanie_textu=dostať_e_mail();assert 'INBOUND TCP UDP PASS' in Spracovanie_textu and 'exit 0' in Spracovanie_textu,Spracovanie_textu
            overenie_správa['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            prenos_súborov_kontakt.delete('server_test.class')
            inštrukcia_SEQUENCE = 'public class 빛 { public static void main(String[] Argumenty) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } Slovenský.vlastné.Výstup.수쓰기(SUM_VALUE); Slovenský.vlastné.Súbor.Zápis("aot.txt", "한글 AOT Súbor 😀"); Slovenský.vlastné.Výstup.zapísať_linka(Slovenský.vlastné.Súbor.Čítanie("aot.txt")); } }'
            prenos_súborov_kontakt.storbinary('STOR 빛.java', io.BytesIO(inštrukcia_SEQUENCE.encode()))
            Spracovanie_textu = 셸('javac 빛.java'); assert 'exit 0' in Spracovanie_textu and 'Compiled:' in Spracovanie_textu, Spracovanie_textu
            Spracovanie_textu = 셸('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            Spracovanie_textu = 셸('run 빛.elf'); assert '\n55\n' in Spracovanie_textu and '한글 AOT Súbor 😀' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            자체실행파일 = bytearray(); prenos_súborov_kontakt.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Spracovanie_textu = 셸('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Spracovanie_textu and 'unsupported' in Spracovanie_textu, Spracovanie_textu
            보존자료 = bytearray(); prenos_súborov_kontakt.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); prenos_súborov_kontakt.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            prenos_súborov_kontakt.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Spracovanie_textu = 셸('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            Spracovanie_textu = 셸('run 빛.elf'); assert '\n55\n' in Spracovanie_textu and '한글 AOT Súbor 😀' in Spracovanie_textu and 'exit 0' in Spracovanie_textu, Spracovanie_textu
            overenie_správa['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            overenie_správa['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=KR_údaje/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int akcia_koreň = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumenty) {
  int[] VALUE = new int[] {akcia_koreň, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumenty[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_údaje),str(정적원문)])
            prenos_súborov_kontakt.storbinary('STOR 정적시험.class',io.BytesIO((KR_údaje/'정적시험.class').read_bytes()))
            Spracovanie_textu=셸('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Spracovanie_textu,Spracovanie_textu
            Spracovanie_textu=셸('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Spracovanie_textu,Spracovanie_textu
            prenos_súborov_kontakt.delete('정적시험.class');prenos_súborov_kontakt.delete('정적시험.elf')
            overenie_správa['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archív.getvalue());손상자료[14]^=1
            prenos_súborov_kontakt.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Spracovanie_textu=셸('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Spracovanie_textu,Spracovanie_textu
            overenie_správa['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            prenos_súborov_kontakt.quit(); assert 'FTP stopped' in 셸('ftpd stop')
            assert not most.chyba, most.chyba
            overenie_správa.update(passed=True, frames_to_guest=most.커널수신틀수, frames_from_guest=most.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selektor.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: prepis.extend(조각)
            most.Pozastaviť_udalosť.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            selektor.close(); Proces.stdin.close(); Proces.stdout.close()
            overenie_správa['bridge_error'] = most.chyba
            overenie_správa['frames_to_guest'] = most.커널수신틀수; overenie_správa['frames_from_guest'] = most.커널발신틀수
            (KR_údaje/'packets.json').write_text(json.dumps(most.denník_sledovania,indent=2)+'\n')
            (KR_údaje / 'serial.log').write_bytes(prepis)
            (KR_údaje / 'report.json').write_text(json.dumps(overenie_správa, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Spustiť_2()
