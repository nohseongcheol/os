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
from Mreža_most import Mreža_most
from Izvrši_komanda import projicirati_koijen, Naredba
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Pokreni():
    mjera_podaci = projicirati_koijen / 'build/verification/ftp'; mjera_podaci.mkdir(parents=True, exist_ok=True)
    provjera_izvještaj = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((projicirati_koijen / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = mjera_podaci / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumenti) throws Exception { 한국어.자체.Ispis.pisati_redak("JAR Izvrši_komanda: " + Argumenti[0]); 한국어.자체.Fajl.Piši("jar.txt", "자체 jezgro_VALUE Fajl"); 한국어.자체.Ispis.pisati_redak(한국어.자체.Fajl.Čitaj("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projicirati_koijen/'build/java-library/classes'), '-d', str(mjera_podaci), str(자바원문)])
    Arhiva = io.BytesIO()
    with zipfile.ZipFile(Arhiva, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(mjera_podaci/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); broj_priključka = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_tok_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Mreža_most(broj_priključka, ['tcp:{}:9300'.format(server_tok_port), 'udp:{}:9301'.format(서버전문접속번호)], snimiti=True) as most:
        proces = subprocess.Popen(Naredba() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + most.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        birač = selectors.DefaultSelector(); birač.register(proces.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            podaci = bytearray(); završiti_Pomak = time.monotonic() + 시간제한
            while 확인표시 not in podaci:
                if time.monotonic() > završiti_Pomak or proces.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + podaci.decode('utf-8', 'replace'))
                for 누름값, _ in birač.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: podaci.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in podaci or b'FAIL ' in podaci: raise AssertionError(podaci)
            return podaci.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ljuska(Linija):
            proces.stdin.write(Linija.encode() + b'\n'); proces.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ljuska('ftpd start')
            fajl_prijenos_veza = ftplib.FTP(); fajl_prijenos_veza.encoding = 'utf-8'; fajl_prijenos_veza.connect('127.0.0.1', broj_priključka, timeout=20); fajl_prijenos_veza.login()
            korisni_sadržaj_podaci = bytes(range(256)) * 32
            fajl_prijenos_veza.storbinary('STOR binary.dat', io.BytesIO(korisni_sadržaj_podaci))
            mjera = bytearray(); fajl_prijenos_veza.retrbinary('RETR binary.dat', mjera.extend)
            assert mjera == korisni_sadržaj_podaci; assert fajl_prijenos_veza.size('binary.dat') == len(korisni_sadržaj_podaci)
            provjera_izvještaj['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fajl_prijenos_veza.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ljuska('cat 한글.txt')
            assert '한글.txt' in fajl_prijenos_veza.nlst()
            assert dict(fajl_prijenos_veza.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            provjera_izvještaj['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fajl_prijenos_veza.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            mjera = bytearray(); fajl_prijenos_veza.retrbinary('RETR binary.dat', mjera.extend); assert mjera == korisni_sadržaj_podaci
            provjera_izvještaj['checks'].append('oversized replacement rejected; previous file preserved')
            with fajl_prijenos_veza.transfercmd('STOR pending.txt') as Upload_Fajlovi:
                # A control command must not change the active upload's destination.
                assert fajl_prijenos_veza.size('binary.dat') == len(korisni_sadržaj_podaci)
                Upload_Fajlovi.sendall(b'UPLOAD TARGET PRESERVED')
            assert fajl_prijenos_veza.voidresp().startswith('226')
            mjera = bytearray(); fajl_prijenos_veza.retrbinary('RETR pending.txt', mjera.extend)
            assert mjera == b'UPLOAD TARGET PRESERVED'
            mjera = bytearray(); fajl_prijenos_veza.retrbinary('RETR binary.dat', mjera.extend)
            assert mjera == korisni_sadržaj_podaci
            fajl_prijenos_veza.delete('pending.txt')
            provjera_izvještaj['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fajl_prijenos_veza.storbinary('STOR 인사.jar', io.BytesIO(Arhiva.getvalue()))
            Tekst = ljuska('java -jar 인사.jar 누리')
            assert 'JAR Izvrši_komanda: 누리' in Tekst and '자체 jezgro_VALUE Fajl' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('./인사.jar 세상')
            assert 'JAR Izvrši_komanda: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            provjera_izvještaj['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct podaci { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct podaci VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = kreirati_fajl("cc.txt", i_za_čitanje_i_za_pisanje | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; pisati_fajl_podaci(문서, 인사, sizeof(인사)-1); zatvoriti_fajl(문서); pisati_fajl_podaci(1, 인사, sizeof(인사)-1); return 0; }\n'
            fajl_prijenos_veza.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = ljuska('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in ljuska('cat cc.txt')
            실행파일 = bytearray(); fajl_prijenos_veza.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fajl_prijenos_veza.storbinary('STOR instanca_VALUE.elf', io.BytesIO(실행파일)); Tekst = ljuska('run instanca_VALUE.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            fajl_prijenos_veza.storbinary('STOR Izvrši_komanda', io.BytesIO(실행파일)); Tekst=ljuska('./Izvrši_komanda');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            fajl_prijenos_veza.storbinary('STOR Naziv.txt', io.BytesIO(실행파일)); Tekst=ljuska('./Naziv.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            ljuska('rm Izvrši_komanda Naziv.txt')
            provjera_izvještaj['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ljuska('rm binary.dat 한글.txt 한글.c 한글.elf instanca_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(mjera_podaci/'linux-reference')
            fajl_prijenos_veza.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=ljuska('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=ljuska('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in ljuska('cat linux.txt')
            fajl_prijenos_veza.delete('리눅스인사');fajl_prijenos_veza.delete('linux.txt')
            fajl_prijenos_veza.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ljuska('./FALSE_VALUE.elf');fajl_prijenos_veza.delete('FALSE_VALUE.elf')
            provjera_izvještaj['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = mjera_podaci/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Spoji_se = 한국어.자체.연결통신.Spoji_se("10.0.2.2", Integer.parseInt(args[0]));
 Spoji_se.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] IZVOR = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<IZVOR.length;i++) if (Spoji_se.getInputStream().read() != (IZVOR[i]&255)) throw new RuntimeException("TCP mismatch");
 Spoji_se.close();
 DatagramSocket završna_tačka = 한국어.자체.통신.Otvori(0); 한국어.자체.통신.TIMEOUT(završna_tačka, 500);
 한국어.자체.통신.poslati(završna_tačka, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(završna_tačka).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 završna_tačka.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projicirati_koijen/'build/java-library/classes'),'-d',str(mjera_podaci),str(통신원문)])
                fajl_prijenos_veza.storbinary('STOR 바깥통신.class', io.BytesIO((mjera_podaci/'바깥통신.class').read_bytes()))
                Tekst = ljuska('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            provjera_izvještaj['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fajl_prijenos_veza.delete('바깥통신.class')
            server_izvor=mjera_podaci/'서버시험.java'
            server_izvor.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket završna_tačka = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gost_VALUE = server_VALUE.accept();
  gost_VALUE.getOutputStream().write(gost_VALUE.getInputStream().read()+1); gost_VALUE.close(); server_VALUE.close();
  byte[] Sadržaj_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Sadržaj_VALUE, Sadržaj_VALUE.length); završna_tačka.receive(전문);
  završna_tačka.send(전문); završna_tačka.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mjera_podaci),str(server_izvor)])
            fajl_prijenos_veza.storbinary('STOR 서버시험.class',io.BytesIO((mjera_podaci/'서버시험.class').read_bytes()))
            proces.stdin.write('java 서버시험\n'.encode());proces.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_tok_port),timeout=5) as peer_VALUE:
                peer_VALUE.sendall(b'A');assert peer_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_VALUE:
                peer_VALUE.settimeout(5);peer_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert peer_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Tekst=수신하기();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            provjera_izvještaj['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fajl_prijenos_veza.delete('서버시험.class')
            programska_naredba_SEQUENCE = 'public class 빛 { public static void main(String[] Argumenti) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.Ispis.수쓰기(SUM_VALUE); 한국어.자체.Fajl.Piši("aot.txt", "한글 AOT Fajl 😀"); 한국어.자체.Ispis.pisati_redak(한국어.자체.Fajl.Čitaj("aot.txt")); } }'
            fajl_prijenos_veza.storbinary('STOR 빛.java', io.BytesIO(programska_naredba_SEQUENCE.encode()))
            Tekst = ljuska('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = ljuska('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fajl 😀' in Tekst and 'exit 0' in Tekst, Tekst
            자체실행파일 = bytearray(); fajl_prijenos_veza.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Tekst = ljuska('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); fajl_prijenos_veza.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fajl_prijenos_veza.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fajl_prijenos_veza.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = ljuska('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = ljuska('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fajl 😀' in Tekst and 'exit 0' in Tekst, Tekst
            provjera_izvještaj['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            provjera_izvještaj['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statični_izvor=mjera_podaci/'정적시험.java'
            statični_izvor.write_text('''public class 정적시험 {
 static int projicirati_koijen = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumenti) {
  int[] VALUE = new int[] {projicirati_koijen, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumenti[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mjera_podaci),str(statični_izvor)])
            fajl_prijenos_veza.storbinary('STOR 정적시험.class',io.BytesIO((mjera_podaci/'정적시험.class').read_bytes()))
            Tekst=ljuska('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=ljuska('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            fajl_prijenos_veza.delete('정적시험.class');fajl_prijenos_veza.delete('정적시험.elf')
            provjera_izvještaj['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhiva.getvalue());손상자료[14]^=1
            fajl_prijenos_veza.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=ljuska('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            provjera_izvještaj['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fajl_prijenos_veza.quit(); assert 'FTP stopped' in ljuska('ftpd stop')
            assert not most.GRESKA, most.GRESKA
            provjera_izvještaj.update(passed=True, frames_to_guest=most.커널수신틀수, frames_from_guest=most.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in birač.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            most.pauza_događaj.set()
            proces.terminate()
            try: proces.wait(timeout=5)
            except subprocess.TimeoutExpired: proces.kill(); proces.wait()
            birač.close(); proces.stdin.close(); proces.stdout.close()
            provjera_izvještaj['bridge_error'] = most.GRESKA
            provjera_izvještaj['frames_to_guest'] = most.커널수신틀수; provjera_izvještaj['frames_from_guest'] = most.커널발신틀수
            (mjera_podaci/'packets.json').write_text(json.dumps(most.trag_LOG,indent=2)+'\n')
            (mjera_podaci / 'serial.log').write_bytes(대화기록)
            (mjera_podaci / 'report.json').write_text(json.dumps(provjera_izvještaj, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Pokreni()
