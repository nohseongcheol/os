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
from most_3de4fe3a import most_3de4fe3a
from Izvrši_naredba import akcija_korijen, Naredba
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Pokreni():
    KR_podaci = akcija_korijen / 'build/verification/ftp'; KR_podaci.mkdir(parents=True, exist_ok=True)
    provjera_izvješće = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((akcija_korijen / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkript = bytearray()
    자바원문 = KR_podaci / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumenti) throws Exception { hrvatski.vlastiti.Izlaz.zapisivanje_red("JAR Izvrši_naredba: " + Argumenti[0]); hrvatski.vlastiti.Datoteka.Zapisuj("jar.txt", "vlastiti jezgra_sustava_VALUE Datoteka"); hrvatski.vlastiti.Izlaz.zapisivanje_red(hrvatski.vlastiti.Datoteka.Čitaj("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(akcija_korijen/'build/java-library/classes'), '-d', str(KR_podaci), str(자바원문)])
    Arhiva = io.BytesIO()
    with zipfile.ZipFile(Arhiva, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(KR_podaci/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); broj_priključka = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_tok_prebaciti = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datogram_prebaciti = 임시자원.getsockname()[1]
    with most_3de4fe3a(broj_priključka, ['tcp:{}:9300'.format(server_tok_prebaciti), 'udp:{}:9301'.format(server_datogram_prebaciti)], snimiti=True) as most:
        Proces = subprocess.Popen(Naredba() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + most.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        odabirač = selectors.DefaultSelector(); odabirač.register(Proces.stdout, selectors.EVENT_READ)
        def primiti_poruka(marker=b'jkoros-native> ', 시간제한=60):
            podaci = bytearray(); završiti_razgovor_pomak = time.monotonic() + 시간제한
            while marker not in podaci:
                if time.monotonic() > završiti_razgovor_pomak or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + podaci.decode('utf-8', 'replace'))
                for 누름값, _ in odabirač.select(.1):
                    fragment_VALUE = 누름값.fileobj.read(4096)
                    if fragment_VALUE: podaci.extend(fragment_VALUE); transkript.extend(fragment_VALUE)
                if b'PANIC:' in podaci or b'FAIL ' in podaci: raise AssertionError(podaci)
            return podaci.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ljuska(red):
            Proces.stdin.write(red.encode() + b'\n'); Proces.stdin.flush(); return primiti_poruka()
        try:
            primiti_poruka(); assert 'FTP listening' in ljuska('ftpd start')
            prijenos_datoteka_veza = ftplib.FTP(); prijenos_datoteka_veza.encoding = 'utf-8'; prijenos_datoteka_veza.connect('127.0.0.1', broj_priključka, timeout=20); prijenos_datoteka_veza.login()
            korisni_podaci_podaci = bytes(range(256)) * 32
            prijenos_datoteka_veza.storbinary('STOR binary.dat', io.BytesIO(korisni_podaci_podaci))
            REZULTAT = bytearray(); prijenos_datoteka_veza.retrbinary('RETR binary.dat', REZULTAT.extend)
            assert REZULTAT == korisni_podaci_podaci; assert prijenos_datoteka_veza.size('binary.dat') == len(korisni_podaci_podaci)
            provjera_izvješće['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            prijenos_datoteka_veza.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ljuska('cat 한글.txt')
            assert '한글.txt' in prijenos_datoteka_veza.nlst()
            assert dict(prijenos_datoteka_veza.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            provjera_izvješće['checks'].append('UTF-8 filename and content visible in guest shell')
            try: prijenos_datoteka_veza.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            REZULTAT = bytearray(); prijenos_datoteka_veza.retrbinary('RETR binary.dat', REZULTAT.extend); assert REZULTAT == korisni_podaci_podaci
            provjera_izvješće['checks'].append('oversized replacement rejected; previous file preserved')
            with prijenos_datoteka_veza.transfercmd('STOR pending.txt') as Prijenos_Datoteke:
                # A control command must not change the active upload's destination.
                assert prijenos_datoteka_veza.size('binary.dat') == len(korisni_podaci_podaci)
                Prijenos_Datoteke.sendall(b'UPLOAD TARGET PRESERVED')
            assert prijenos_datoteka_veza.voidresp().startswith('226')
            REZULTAT = bytearray(); prijenos_datoteka_veza.retrbinary('RETR pending.txt', REZULTAT.extend)
            assert REZULTAT == b'UPLOAD TARGET PRESERVED'
            REZULTAT = bytearray(); prijenos_datoteka_veza.retrbinary('RETR binary.dat', REZULTAT.extend)
            assert REZULTAT == korisni_podaci_podaci
            prijenos_datoteka_veza.delete('pending.txt')
            provjera_izvješće['checks'].append('interleaved SIZE cannot change the active STOR destination')
            prijenos_datoteka_veza.storbinary('STOR 인사.jar', io.BytesIO(Arhiva.getvalue()))
            Tekst = ljuska('java -jar 인사.jar 누리')
            assert 'JAR Izvrši_naredba: 누리' in Tekst and 'vlastiti jezgra_sustava_VALUE Datoteka' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('./인사.jar 세상')
            assert 'JAR Izvrši_naredba: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            provjera_izvješće['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct podaci { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct podaci VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = otvoreno_Datoteka("cc.txt", 읽고쓰기 | 없으면만들기 | skratiti_Sadržaj, 0600); if (문서 < 0) return 1; zapisivanje_Datoteka_podaci(문서, 인사, sizeof(인사)-1); Zatvori_Datoteka(문서); zapisivanje_Datoteka_podaci(1, 인사, sizeof(인사)-1); return 0; }\n'
            prijenos_datoteka_veza.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = ljuska('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in ljuska('cat cc.txt')
            실행파일 = bytearray(); prijenos_datoteka_veza.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            prijenos_datoteka_veza.storbinary('STOR instanca_VALUE.elf', io.BytesIO(실행파일)); Tekst = ljuska('run instanca_VALUE.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            prijenos_datoteka_veza.storbinary('STOR Izvrši_naredba', io.BytesIO(실행파일)); Tekst=ljuska('./Izvrši_naredba');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            prijenos_datoteka_veza.storbinary('STOR Ime.txt', io.BytesIO(실행파일)); Tekst=ljuska('./Ime.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            ljuska('rm Izvrši_naredba Ime.txt')
            provjera_izvješće['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ljuska('rm binary.dat 한글.txt 한글.c 한글.elf instanca_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_podaci/'linux-reference')
            prijenos_datoteka_veza.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=ljuska('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=ljuska('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in ljuska('cat linux.txt')
            prijenos_datoteka_veza.delete('리눅스인사');prijenos_datoteka_veza.delete('linux.txt')
            prijenos_datoteka_veza.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ljuska('./FALSE_VALUE.elf');prijenos_datoteka_veza.delete('FALSE_VALUE.elf')
            provjera_izvješće['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as eho_server_unos:
                NET_izvor = KR_podaci/'바깥통신.java'
                NET_izvor.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Spoji_se = hrvatski.vlastiti.연결통신.Spoji_se("10.0.2.2", Integer.parseInt(args[0]));
 Spoji_se.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] IZVOR = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<IZVOR.length;i++) if (Spoji_se.getInputStream().read() != (IZVOR[i]&255)) throw new RuntimeException("TCP mismatch");
 Spoji_se.close();
 DatagramSocket sudionik = hrvatski.vlastiti.통신.Otvori(0); hrvatski.vlastiti.통신.TIMEOUT(sudionik, 500);
 hrvatski.vlastiti.통신.slati(sudionik, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!hrvatski.vlastiti.통신.primiti(sudionik).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 sudionik.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(akcija_korijen/'build/java-library/classes'),'-d',str(KR_podaci),str(NET_izvor)])
                prijenos_datoteka_veza.storbinary('STOR 바깥통신.class', io.BytesIO((KR_podaci/'바깥통신.class').read_bytes()))
                Tekst = ljuska('java 바깥통신 {} {}'.format(eho_server_unos.TCP_prebaciti, eho_server_unos.UDP_prebaciti))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert eho_server_unos.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, eho_server_unos.수신됨
                assert not eho_server_unos.오류들, eho_server_unos.오류들
            provjera_izvješće['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            prijenos_datoteka_veza.delete('바깥통신.class')
            server_izvor=KR_podaci/'서버시험.java'
            server_izvor.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket sudionik = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gost_VALUE = server_VALUE.accept();
  gost_VALUE.getOutputStream().write(gost_VALUE.getInputStream().read()+1); gost_VALUE.close(); server_VALUE.close();
  byte[] Sadržaj_VALUE = new byte[8]; DatagramPacket datogram = new DatagramPacket(Sadržaj_VALUE, Sadržaj_VALUE.length); sudionik.receive(datogram);
  sudionik.send(datogram); sudionik.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_podaci),str(server_izvor)])
            prijenos_datoteka_veza.storbinary('STOR 서버시험.class',io.BytesIO((KR_podaci/'서버시험.class').read_bytes()))
            Proces.stdin.write('java 서버시험\n'.encode());Proces.stdin.flush();primiti_poruka(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_tok_prebaciti),timeout=5) as ravnopravan_član_VALUE:
                ravnopravan_član_VALUE.sendall(b'A');assert ravnopravan_član_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ravnopravan_član_VALUE:
                ravnopravan_član_VALUE.settimeout(5);ravnopravan_član_VALUE.sendto(b'UDP-IN',('127.0.0.1',server_datogram_prebaciti));assert ravnopravan_član_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Tekst=primiti_poruka();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            provjera_izvješće['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            prijenos_datoteka_veza.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Argumenti) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } hrvatski.vlastiti.Izlaz.수쓰기(SUM_VALUE); hrvatski.vlastiti.Datoteka.Zapisuj("aot.txt", "한글 AOT Datoteka 😀"); hrvatski.vlastiti.Izlaz.zapisivanje_red(hrvatski.vlastiti.Datoteka.Čitaj("aot.txt")); } }'
            prijenos_datoteka_veza.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Tekst = ljuska('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = ljuska('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Datoteka 😀' in Tekst and 'exit 0' in Tekst, Tekst
            자체실행파일 = bytearray(); prijenos_datoteka_veza.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Tekst = ljuska('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); prijenos_datoteka_veza.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); prijenos_datoteka_veza.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            prijenos_datoteka_veza.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = ljuska('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Datoteka 😀' in Tekst and 'exit 0' in Tekst, Tekst
            provjera_izvješće['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            provjera_izvješće['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=KR_podaci/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int akcija_korijen = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumenti) {
  int[] VALUE = new int[] {akcija_korijen, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumenti[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_podaci),str(정적원문)])
            prijenos_datoteka_veza.storbinary('STOR 정적시험.class',io.BytesIO((KR_podaci/'정적시험.class').read_bytes()))
            Tekst=ljuska('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=ljuska('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            prijenos_datoteka_veza.delete('정적시험.class');prijenos_datoteka_veza.delete('정적시험.elf')
            provjera_izvješće['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhiva.getvalue());손상자료[14]^=1
            prijenos_datoteka_veza.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=ljuska('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            provjera_izvješće['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            prijenos_datoteka_veza.quit(); assert 'FTP stopped' in ljuska('ftpd stop')
            assert not most.GREŠKA, most.GREŠKA
            provjera_izvješće.update(passed=True, frames_to_guest=most.커널수신틀수, frames_from_guest=most.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in odabirač.select(0):
                fragment_VALUE=누름값.fileobj.read(65536)
                if fragment_VALUE: transkript.extend(fragment_VALUE)
            most.Pauziraj_događaj.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            odabirač.close(); Proces.stdin.close(); Proces.stdout.close()
            provjera_izvješće['bridge_error'] = most.GREŠKA
            provjera_izvješće['frames_to_guest'] = most.커널수신틀수; provjera_izvješće['frames_from_guest'] = most.커널발신틀수
            (KR_podaci/'packets.json').write_text(json.dumps(most.zapis_praćenja,indent=2)+'\n')
            (KR_podaci / 'serial.log').write_bytes(transkript)
            (KR_podaci / 'report.json').write_text(json.dumps(provjera_izvješće, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Pokreni()
