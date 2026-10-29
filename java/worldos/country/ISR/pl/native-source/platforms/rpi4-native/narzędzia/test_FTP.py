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
from mostek_3de4fe3a import mostek_3de4fe3a
from Wykonaj_polecenie import Project_korzeń, polecenie
from echo_warunki_początkowe import echo_warunki_początkowe
from 실행파일시험 import 리눅스예제


def Uruchom_2():
    KR_dane = Project_korzeń / 'build/verification/ftp'; KR_dane.mkdir(parents=True, exist_ok=True)
    walidacja_Raport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_korzeń / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkrypcja = bytearray()
    자바원문 = KR_dane / 'test_pakiet.java'
    자바원문.write_text('public class test_pakiet { public static void main(String[] argumenty) throws Exception { polski.własny.pozycja_wyjścia.zapis_linia("JAR Wykonaj_polecenie: " + argumenty[0]); polski.własny.nazwa_pliku.Zapis("jar.txt", "własny jądro_WARTOŚĆ nazwa_pliku"); polski.własny.pozycja_wyjścia.zapis_linia(polski.własny.nazwa_pliku.Odczyt("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_korzeń/'build/java-library/classes'), '-d', str(KR_dane), str(자바원문)])
    Archiwum = io.BytesIO()
    with zipfile.ZipFile(Archiwum, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: test_pakiet\r\n\r\n')
        자바꾸러미.write(str(KR_dane/'test_pakiet.class'), 'test_pakiet.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); numer_portu = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); serwer_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); serwer_datagram_port = 임시자원.getsockname()[1]
    with mostek_3de4fe3a(numer_portu, ['tcp:{}:9300'.format(serwer_Stream_port), 'udp:{}:9301'.format(serwer_datagram_port)], Capture=True) as mostek:
        Proces = subprocess.Popen(polecenie() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + mostek.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selektor = selectors.DefaultSelector(); selektor.register(Proces.stdout, selectors.EVENT_READ)
        def odbierać_e_mail(pisak=b'jkoros-native> ', wykonanie_TIMEOUT=60):
            dane = bytearray(); Koniec_przesunąć = time.monotonic() + wykonanie_TIMEOUT
            while pisak not in dane:
                if time.monotonic() > Koniec_przesunąć or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + dane.decode('utf-8', 'replace'))
                for 누름값, _ in selektor.select(.1):
                    fragment_WARTOŚĆ_652d4b53 = 누름값.fileobj.read(4096)
                    if fragment_WARTOŚĆ_652d4b53: dane.extend(fragment_WARTOŚĆ_652d4b53); transkrypcja.extend(fragment_WARTOŚĆ_652d4b53)
                if b'PANIC:' in dane or b'FAIL ' in dane: raise AssertionError(dane)
            return dane.decode('utf-8', 'replace').replace('\r\n', '\n')
        def powłoka(wiersz_wejścia):
            Proces.stdin.write(wiersz_wejścia.encode() + b'\n'); Proces.stdin.flush(); return odbierać_e_mail()
        try:
            odbierać_e_mail(); assert 'FTP listening' in powłoka('ftpd start')
            transfer_plików_połączenie = ftplib.FTP(); transfer_plików_połączenie.encoding = 'utf-8'; transfer_plików_połączenie.connect('127.0.0.1', numer_portu, timeout=20); transfer_plików_połączenie.login()
            ładunek_dane = bytes(range(256)) * 32
            transfer_plików_połączenie.storbinary('STOR binary.dat', io.BytesIO(ładunek_dane))
            WYNIK = bytearray(); transfer_plików_połączenie.retrbinary('RETR binary.dat', WYNIK.extend)
            assert WYNIK == ładunek_dane; assert transfer_plików_połączenie.size('binary.dat') == len(ładunek_dane)
            walidacja_Raport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            transfer_plików_połączenie.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in powłoka('cat 한글.txt')
            assert '한글.txt' in transfer_plików_połączenie.nlst()
            assert dict(transfer_plików_połączenie.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            walidacja_Raport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: transfer_plików_połączenie.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            WYNIK = bytearray(); transfer_plików_połączenie.retrbinary('RETR binary.dat', WYNIK.extend); assert WYNIK == ładunek_dane
            walidacja_Raport['checks'].append('oversized replacement rejected; previous file preserved')
            with transfer_plików_połączenie.transfercmd('STOR pending.txt') as Upload_Files:
                # A control command must not change the active upload's destination.
                assert transfer_plików_połączenie.size('binary.dat') == len(ładunek_dane)
                Upload_Files.sendall(b'UPLOAD TARGET PRESERVED')
            assert transfer_plików_połączenie.voidresp().startswith('226')
            WYNIK = bytearray(); transfer_plików_połączenie.retrbinary('RETR pending.txt', WYNIK.extend)
            assert WYNIK == b'UPLOAD TARGET PRESERVED'
            WYNIK = bytearray(); transfer_plików_połączenie.retrbinary('RETR binary.dat', WYNIK.extend)
            assert WYNIK == ładunek_dane
            transfer_plików_połączenie.delete('pending.txt')
            walidacja_Raport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            transfer_plików_połączenie.storbinary('STOR 인사.jar', io.BytesIO(Archiwum.getvalue()))
            tekst = powłoka('java -jar 인사.jar 누리')
            assert 'JAR Wykonaj_polecenie: 누리' in tekst and 'własny jądro_WARTOŚĆ nazwa_pliku' in tekst and 'exit 0' in tekst, tekst
            tekst = powłoka('./인사.jar 세상')
            assert 'JAR Wykonaj_polecenie: 세상' in tekst and 'exit 0' in tekst, tekst
            walidacja_Raport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <Plik_ABI.h>\nstruct dane { int identyfikator; double 비율; };\nint SUMA_WARTOŚĆ(int n) { return n ? n + SUMA_WARTOŚĆ(n-1) : 0; }\nint main(void) { struct dane WARTOŚĆ = {SUMA_WARTOŚĆ(10), 1.25}; if (WARTOŚĆ.identyfikator != 55 || WARTOŚĆ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = otwarty_Plik("cc.txt", R_W | 없으면만들기 | obcinać_Spis_treści, 0600); if (문서 < 0) return 1; zapis_Plik_dane(문서, 인사, sizeof(인사)-1); Zamknij_Plik(문서); zapis_Plik_dane(1, 인사, sizeof(인사)-1); return 0; }\n'
            transfer_plików_połączenie.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            tekst = powłoka('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in tekst and 'exit 0' in tekst, tekst
            tekst = powłoka('run 한글.elf'); assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst, tekst
            assert 'CC NATIVE PASS' in powłoka('cat cc.txt')
            plik_wykonywalny = bytearray(); transfer_plików_połączenie.retrbinary('RETR 한글.elf', plik_wykonywalny.extend)
            assert plik_wykonywalny[:4] == b'\x7fELF' and plik_wykonywalny[18:20] == b'\xb7\x00'
            transfer_plików_połączenie.storbinary('STOR kopiować_WARTOŚĆ.elf', io.BytesIO(plik_wykonywalny)); tekst = powłoka('run kopiować_WARTOŚĆ.elf'); assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst, tekst
            transfer_plików_połączenie.storbinary('STOR Wykonaj_polecenie', io.BytesIO(plik_wykonywalny)); tekst=powłoka('./Wykonaj_polecenie');assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst,tekst
            transfer_plików_połączenie.storbinary('STOR Nazwa.txt', io.BytesIO(plik_wykonywalny)); tekst=powłoka('./Nazwa.txt');assert 'CC NATIVE PASS' in tekst and 'exit 0' in tekst,tekst
            powłoka('rm Wykonaj_polecenie Nazwa.txt')
            walidacja_Raport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            powłoka('rm binary.dat 한글.txt 한글.c 한글.elf kopiować_WARTOŚĆ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_dane/'linux-reference')
            transfer_plików_połączenie.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            tekst=powłoka('./리눅스인사');assert 'exit -8' in tekst,tekst
            tekst=powłoka('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in tekst,tekst
            assert 'LINUX ELF FILE IO' in powłoka('cat linux.txt')
            transfer_plików_połączenie.delete('리눅스인사');transfer_plików_połączenie.delete('linux.txt')
            transfer_plików_połączenie.storbinary('STOR FAŁSZ_WARTOŚĆ.elf',io.BytesIO(b'plain text'))
            assert '실행할 identyfikator 없습니다:' in powłoka('./FAŁSZ_WARTOŚĆ.elf');transfer_plików_połączenie.delete('FAŁSZ_WARTOŚĆ.elf')
            walidacja_Raport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with echo_warunki_początkowe() as echo_serwer_wpis:
                NET_źródło = KR_dane/'zewnętrzny_komunikacja.java'
                NET_źródło.write_text('''import java.net.*; import java.io.*;
public class zewnętrzny_komunikacja { public static void main(String[] args) throws Exception {
 Socket Połącz = polski.własny.połączenie_transport.Połącz("10.0.2.2", Integer.parseInt(args[0]));
 Połącz.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] plik_źródłowy = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<plik_źródłowy.length;i++) if (Połącz.getInputStream().read() != (plik_źródłowy[i]&255)) throw new RuntimeException("TCP mismatch");
 Połącz.close();
 DatagramSocket uczestnik = polski.własny.komunikacja.Otwórz(0); polski.własny.komunikacja.TIMEOUT(uczestnik, 500);
 polski.własny.komunikacja.wysłać(uczestnik, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!polski.własny.komunikacja.odbierać(uczestnik).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 uczestnik.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_korzeń/'build/java-library/classes'),'-d',str(KR_dane),str(NET_źródło)])
                transfer_plików_połączenie.storbinary('STOR zewnętrzny_komunikacja.class', io.BytesIO((KR_dane/'zewnętrzny_komunikacja.class').read_bytes()))
                tekst = powłoka('java zewnętrzny_komunikacja {} {}'.format(echo_serwer_wpis.port_TCP, echo_serwer_wpis.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in tekst and '10.0.2.2' in tekst and 'exit 0' in tekst, tekst
                assert echo_serwer_wpis.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, echo_serwer_wpis.수신됨
                assert not echo_serwer_wpis.오류들, echo_serwer_wpis.오류들
            walidacja_Raport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            transfer_plików_połączenie.delete('zewnętrzny_komunikacja.class')
            serwer_źródło=KR_dane/'serwer_test.java'
            serwer_źródło.write_text('''import java.net.*; public class serwer_test {
 public static void main(String[] args) throws Exception {
  ServerSocket serwer_WARTOŚĆ = new ServerSocket(9300); DatagramSocket uczestnik = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gość_WARTOŚĆ = serwer_WARTOŚĆ.accept();
  gość_WARTOŚĆ.getOutputStream().write(gość_WARTOŚĆ.getInputStream().read()+1); gość_WARTOŚĆ.close(); serwer_WARTOŚĆ.close();
  byte[] treść_WARTOŚĆ_cb0f2404 = new byte[8]; DatagramPacket datagram = new DatagramPacket(treść_WARTOŚĆ_cb0f2404, treść_WARTOŚĆ_cb0f2404.length); uczestnik.receive(datagram);
  uczestnik.send(datagram); uczestnik.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_dane),str(serwer_źródło)])
            transfer_plików_połączenie.storbinary('STOR serwer_test.class',io.BytesIO((KR_dane/'serwer_test.class').read_bytes()))
            Proces.stdin.write('java serwer_test\n'.encode());Proces.stdin.flush();odbierać_e_mail(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',serwer_Stream_port),timeout=5) as węzeł_równorzędny_WARTOŚĆ:
                węzeł_równorzędny_WARTOŚĆ.sendall(b'A');assert węzeł_równorzędny_WARTOŚĆ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as węzeł_równorzędny_WARTOŚĆ:
                węzeł_równorzędny_WARTOŚĆ.settimeout(5);węzeł_równorzędny_WARTOŚĆ.sendto(b'UDP-IN',('127.0.0.1',serwer_datagram_port));assert węzeł_równorzędny_WARTOŚĆ.recvfrom(512)[0]==b'UDP-IN'
            tekst=odbierać_e_mail();assert 'INBOUND TCP UDP PASS' in tekst and 'exit 0' in tekst,tekst
            walidacja_Raport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            transfer_plików_połączenie.delete('serwer_test.class')
            instrukcja_SEKWENCJA = 'public class 빛 { public static void main(String[] argumenty) throws Exception { int SUMA_WARTOŚĆ = 0; int identyfikator = 1; while (identyfikator <= 10) { SUMA_WARTOŚĆ = SUMA_WARTOŚĆ + identyfikator; identyfikator = identyfikator + 1; } polski.własny.pozycja_wyjścia.zapis_identyfikator(SUMA_WARTOŚĆ); polski.własny.nazwa_pliku.Zapis("aot.txt", "한글 AOT nazwa_pliku 😀"); polski.własny.pozycja_wyjścia.zapis_linia(polski.własny.nazwa_pliku.Odczyt("aot.txt")); } }'
            transfer_plików_połączenie.storbinary('STOR 빛.java', io.BytesIO(instrukcja_SEKWENCJA.encode()))
            tekst = powłoka('javac 빛.java'); assert 'exit 0' in tekst and 'Compiled:' in tekst, tekst
            tekst = powłoka('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in tekst and 'exit 0' in tekst, tekst
            tekst = powłoka('run 빛.elf'); assert '\n55\n' in tekst and '한글 AOT nazwa_pliku 😀' in tekst and 'exit 0' in tekst, tekst
            natywny = bytearray(); transfer_plików_połączenie.retrbinary('RETR 빛.elf', natywny.extend)
            tekst = powłoka('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in tekst and 'unsupported' in tekst, tekst
            보존자료 = bytearray(); transfer_plików_połączenie.retrbinary('RETR 빛.elf', 보존자료.extend); assert natywny == 보존자료
            바이트코드 = bytearray(); transfer_plików_połączenie.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            transfer_plików_połączenie.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            tekst = powłoka('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in tekst and 'exit 0' in tekst, tekst
            tekst = powłoka('run 빛.elf'); assert '\n55\n' in tekst and '한글 AOT nazwa_pliku 😀' in tekst and 'exit 0' in tekst, tekst
            walidacja_Raport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            walidacja_Raport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statyczny_źródło=KR_dane/'statyczny_test.java'
            statyczny_źródło.write_text('''public class statyczny_test {
 static int Project_korzeń = 3;
 static int SUMA_WARTOŚĆ(int n) { return n == 0 ? 0 : n + SUMA_WARTOŚĆ(n-1); }
 public static void main(String[] argumenty) {
  int[] WARTOŚĆ = new int[] {Project_korzeń, SUMA_WARTOŚĆ(10)};
  System.out.println(WARTOŚĆ[0] + WARTOŚĆ[1]); System.out.println(argumenty[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_dane),str(statyczny_źródło)])
            transfer_plików_połączenie.storbinary('STOR statyczny_test.class',io.BytesIO((KR_dane/'statyczny_test.class').read_bytes()))
            tekst=powłoka('jaot statyczny_test.class -o statyczny_test.elf');assert 'exit 0' in tekst,tekst
            tekst=powłoka('run statyczny_test.elf 한글인수');assert '\n58\n한글인수\nexit 0' in tekst,tekst
            transfer_plików_połączenie.delete('statyczny_test.class');transfer_plików_połączenie.delete('statyczny_test.elf')
            walidacja_Raport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archiwum.getvalue());손상자료[14]^=1
            transfer_plików_połączenie.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            tekst=powłoka('java -jar 인사.jar');assert 'Main-Class\nexit 1' in tekst,tekst
            walidacja_Raport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            transfer_plików_połączenie.quit(); assert 'FTP stopped' in powłoka('ftpd stop')
            assert not mostek.błąd, mostek.błąd
            walidacja_Raport.update(passed=True, frames_to_guest=mostek.커널수신틀수, frames_from_guest=mostek.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selektor.select(0):
                fragment_WARTOŚĆ_652d4b53=누름값.fileobj.read(65536)
                if fragment_WARTOŚĆ_652d4b53: transkrypcja.extend(fragment_WARTOŚĆ_652d4b53)
            mostek.Wstrzymaj_konkurs.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            selektor.close(); Proces.stdin.close(); Proces.stdout.close()
            walidacja_Raport['bridge_error'] = mostek.błąd
            walidacja_Raport['frames_to_guest'] = mostek.커널수신틀수; walidacja_Raport['frames_from_guest'] = mostek.커널발신틀수
            (KR_dane/'packets.json').write_text(json.dumps(mostek.dziennik_śledzenia,indent=2)+'\n')
            (KR_dane / 'serial.log').write_bytes(transkrypcja)
            (KR_dane / 'report.json').write_text(json.dumps(walidacja_Raport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Uruchom_2()
