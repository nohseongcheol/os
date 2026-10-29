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
from mrežni_most import mrežni_most
from Izvrši_komanda import radnja_koren, komanda
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def koristiti():
    KR_podaci = radnja_koren / 'build/verification/ftp'; KR_podaci.mkdir(parents=True, exist_ok=True)
    provera_valjanosti_izveštaj = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((radnja_koren / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkript = bytearray()
    자바원문 = KR_podaci / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.줄쓰기("JAR Izvrši_komanda: " + 인수[0]); 한국어.자체.Datoteka.쓰기("jar.txt", "자체 jezgro_VALUE Datoteka"); 한국어.자체.출력.줄쓰기(한국어.자체.Datoteka.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(radnja_koren/'build/java-library/classes'), '-d', str(KR_podaci), str(자바원문)])
    Arhiva = io.BytesIO()
    with zipfile.ZipFile(Arhiva, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(KR_podaci/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); broj_porta = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_tok_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagram_port = 임시자원.getsockname()[1]
    with mrežni_most(broj_porta, ['tcp:{}:9300'.format(server_tok_port), 'udp:{}:9301'.format(server_datagram_port)], uhvatiti=True) as most:
        Proces = subprocess.Popen(komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + most.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        birač = selectors.DefaultSelector(); birač.register(Proces.stdout, selectors.EVENT_READ)
        def primiti_poruka(označivač=b'jkoros-native> ', 시간제한=60):
            podaci = bytearray(); završiti_razgovor_Pomak = time.monotonic() + 시간제한
            while označivač not in podaci:
                if time.monotonic() > završiti_razgovor_Pomak or Proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + podaci.decode('utf-8', 'replace'))
                for 누름값, _ in birač.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: podaci.extend(조각); transkript.extend(조각)
                if b'PANIC:' in podaci or b'FAIL ' in podaci: raise AssertionError(podaci)
            return podaci.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ljuska(red):
            Proces.stdin.write(red.encode() + b'\n'); Proces.stdin.flush(); return primiti_poruka()
        try:
            primiti_poruka(); assert 'FTP listening' in ljuska('ftpd start')
            prenos_datoteka_veza = ftplib.FTP(); prenos_datoteka_veza.encoding = 'utf-8'; prenos_datoteka_veza.connect('127.0.0.1', broj_porta, timeout=20); prenos_datoteka_veza.login()
            korisni_podaci_podaci = bytes(range(256)) * 32
            prenos_datoteka_veza.storbinary('STOR binary.dat', io.BytesIO(korisni_podaci_podaci))
            KR = bytearray(); prenos_datoteka_veza.retrbinary('RETR binary.dat', KR.extend)
            assert KR == korisni_podaci_podaci; assert prenos_datoteka_veza.size('binary.dat') == len(korisni_podaci_podaci)
            provera_valjanosti_izveštaj['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            prenos_datoteka_veza.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ljuska('cat 한글.txt')
            assert '한글.txt' in prenos_datoteka_veza.nlst()
            assert dict(prenos_datoteka_veza.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            provera_valjanosti_izveštaj['checks'].append('UTF-8 filename and content visible in guest shell')
            try: prenos_datoteka_veza.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            KR = bytearray(); prenos_datoteka_veza.retrbinary('RETR binary.dat', KR.extend); assert KR == korisni_podaci_podaci
            provera_valjanosti_izveštaj['checks'].append('oversized replacement rejected; previous file preserved')
            with prenos_datoteka_veza.transfercmd('STOR pending.txt') as Otprema_Datoteke:
                # A control command must not change the active upload's destination.
                assert prenos_datoteka_veza.size('binary.dat') == len(korisni_podaci_podaci)
                Otprema_Datoteke.sendall(b'UPLOAD TARGET PRESERVED')
            assert prenos_datoteka_veza.voidresp().startswith('226')
            KR = bytearray(); prenos_datoteka_veza.retrbinary('RETR pending.txt', KR.extend)
            assert KR == b'UPLOAD TARGET PRESERVED'
            KR = bytearray(); prenos_datoteka_veza.retrbinary('RETR binary.dat', KR.extend)
            assert KR == korisni_podaci_podaci
            prenos_datoteka_veza.delete('pending.txt')
            provera_valjanosti_izveštaj['checks'].append('interleaved SIZE cannot change the active STOR destination')
            prenos_datoteka_veza.storbinary('STOR 인사.jar', io.BytesIO(Arhiva.getvalue()))
            SMS = ljuska('java -jar 인사.jar 누리')
            assert 'JAR Izvrši_komanda: 누리' in SMS and '자체 jezgro_VALUE Datoteka' in SMS and 'exit 0' in SMS, SMS
            SMS = ljuska('./인사.jar 세상')
            assert 'JAR Izvrši_komanda: 세상' in SMS and 'exit 0' in SMS, SMS
            provera_valjanosti_izveštaj['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct podaci { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct podaci VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = otvoren_Datoteka("cc.txt", za_čitanje_pisanje | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; 파일자료쓰기(문서, 인사, sizeof(인사)-1); Zatvori_Datoteka(문서); 파일자료쓰기(1, 인사, sizeof(인사)-1); return 0; }\n'
            prenos_datoteka_veza.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = ljuska('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = ljuska('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in ljuska('cat cc.txt')
            실행파일 = bytearray(); prenos_datoteka_veza.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            prenos_datoteka_veza.storbinary('STOR instanca_VALUE.elf', io.BytesIO(실행파일)); SMS = ljuska('run instanca_VALUE.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            prenos_datoteka_veza.storbinary('STOR Izvrši_komanda', io.BytesIO(실행파일)); SMS=ljuska('./Izvrši_komanda');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            prenos_datoteka_veza.storbinary('STOR ime.txt', io.BytesIO(실행파일)); SMS=ljuska('./ime.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            ljuska('rm Izvrši_komanda ime.txt')
            provera_valjanosti_izveštaj['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ljuska('rm binary.dat 한글.txt 한글.c 한글.elf instanca_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(KR_podaci/'linux-reference')
            prenos_datoteka_veza.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=ljuska('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=ljuska('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in ljuska('cat linux.txt')
            prenos_datoteka_veza.delete('리눅스인사');prenos_datoteka_veza.delete('linux.txt')
            prenos_datoteka_veza.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ljuska('./FALSE_VALUE.elf');prenos_datoteka_veza.delete('FALSE_VALUE.elf')
            provera_valjanosti_izveštaj['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as eho_server_stavka:
                NET_izvor = KR_podaci/'바깥통신.java'
                NET_izvor.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket veze = 한국어.자체.연결통신.veze("10.0.2.2", Integer.parseInt(args[0]));
 veze.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] izvor = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<izvor.length;i++) if (veze.getInputStream().read() != (izvor[i]&255)) throw new RuntimeException("TCP mismatch");
 veze.close();
 DatagramSocket učesnik = 한국어.자체.통신.otvoren(0); 한국어.자체.통신.TIMEOUT(učesnik, 500);
 한국어.자체.통신.poslati(učesnik, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.primiti(učesnik).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 učesnik.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(radnja_koren/'build/java-library/classes'),'-d',str(KR_podaci),str(NET_izvor)])
                prenos_datoteka_veza.storbinary('STOR 바깥통신.class', io.BytesIO((KR_podaci/'바깥통신.class').read_bytes()))
                SMS = ljuska('java 바깥통신 {} {}'.format(eho_server_stavka.TCP_port, eho_server_stavka.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert eho_server_stavka.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, eho_server_stavka.수신됨
                assert not eho_server_stavka.오류들, eho_server_stavka.오류들
            provera_valjanosti_izveštaj['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            prenos_datoteka_veza.delete('바깥통신.class')
            server_izvor=KR_podaci/'서버시험.java'
            server_izvor.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket učesnik = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gost_VALUE = server_VALUE.accept();
  gost_VALUE.getOutputStream().write(gost_VALUE.getInputStream().read()+1); gost_VALUE.close(); server_VALUE.close();
  byte[] Sadržaj_VALUE = new byte[8]; DatagramPacket datagram = new DatagramPacket(Sadržaj_VALUE, Sadržaj_VALUE.length); učesnik.receive(datagram);
  učesnik.send(datagram); učesnik.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_podaci),str(server_izvor)])
            prenos_datoteka_veza.storbinary('STOR 서버시험.class',io.BytesIO((KR_podaci/'서버시험.class').read_bytes()))
            Proces.stdin.write('java 서버시험\n'.encode());Proces.stdin.flush();primiti_poruka(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_tok_port),timeout=5) as ravnopravni_uređaj_VALUE:
                ravnopravni_uređaj_VALUE.sendall(b'A');assert ravnopravni_uređaj_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ravnopravni_uređaj_VALUE:
                ravnopravni_uređaj_VALUE.settimeout(5);ravnopravni_uređaj_VALUE.sendto(b'UDP-IN',('127.0.0.1',server_datagram_port));assert ravnopravni_uređaj_VALUE.recvfrom(512)[0]==b'UDP-IN'
            SMS=primiti_poruka();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            provera_valjanosti_izveštaj['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            prenos_datoteka_veza.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_VALUE); 한국어.자체.Datoteka.쓰기("aot.txt", "한글 AOT Datoteka 😀"); 한국어.자체.출력.줄쓰기(한국어.자체.Datoteka.읽기("aot.txt")); } }'
            prenos_datoteka_veza.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            SMS = ljuska('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = ljuska('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = ljuska('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Datoteka 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); prenos_datoteka_veza.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = ljuska('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); prenos_datoteka_veza.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); prenos_datoteka_veza.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            prenos_datoteka_veza.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = ljuska('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = ljuska('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Datoteka 😀' in SMS and 'exit 0' in SMS, SMS
            provera_valjanosti_izveštaj['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            provera_valjanosti_izveštaj['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=KR_podaci/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int radnja_koren = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {radnja_koren, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(KR_podaci),str(정적원문)])
            prenos_datoteka_veza.storbinary('STOR 정적시험.class',io.BytesIO((KR_podaci/'정적시험.class').read_bytes()))
            SMS=ljuska('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=ljuska('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            prenos_datoteka_veza.delete('정적시험.class');prenos_datoteka_veza.delete('정적시험.elf')
            provera_valjanosti_izveštaj['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhiva.getvalue());손상자료[14]^=1
            prenos_datoteka_veza.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=ljuska('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            provera_valjanosti_izveštaj['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            prenos_datoteka_veza.quit(); assert 'FTP stopped' in ljuska('ftpd stop')
            assert not most.greška, most.greška
            provera_valjanosti_izveštaj.update(passed=True, frames_to_guest=most.커널수신틀수, frames_from_guest=most.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in birač.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transkript.extend(조각)
            most.Pauziraj_događaj.set()
            Proces.terminate()
            try: Proces.wait(timeout=5)
            except subprocess.TimeoutExpired: Proces.kill(); Proces.wait()
            birač.close(); Proces.stdin.close(); Proces.stdout.close()
            provera_valjanosti_izveštaj['bridge_error'] = most.greška
            provera_valjanosti_izveštaj['frames_to_guest'] = most.커널수신틀수; provera_valjanosti_izveštaj['frames_from_guest'] = most.커널발신틀수
            (KR_podaci/'packets.json').write_text(json.dumps(most.evidencija_praćenja,indent=2)+'\n')
            (KR_podaci / 'serial.log').write_bytes(transkript)
            (KR_podaci / 'report.json').write_text(json.dumps(provera_valjanosti_izveštaj, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': koristiti()
