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
from sild_3de4fe3a import sild_3de4fe3a
from Täida_käsk import Project_juur, Käsk
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Käivita_2():
    näitaja_andmed = Project_juur / 'build/verification/ftp'; näitaja_andmed.mkdir(parents=True, exist_ok=True)
    kinnitamine_aruanne = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_juur / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkriptsioon = bytearray()
    자바원문 = näitaja_andmed / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumendid) throws Exception { Eesti.oma.Väljund.kirjutamine_liin("JAR Täida_käsk: " + Argumendid[0]); Eesti.oma.Fail.Kirjutamine("jar.txt", "oma tuum_VALUE Fail"); Eesti.oma.Väljund.kirjutamine_liin(Eesti.oma.Fail.Lugemine("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_juur/'build/java-library/classes'), '-d', str(näitaja_andmed), str(자바원문)])
    Arhiiv = io.BytesIO()
    with zipfile.ZipFile(Arhiiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(näitaja_andmed/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); pordinumber = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_voog_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_datagramm_port = 임시자원.getsockname()[1]
    with sild_3de4fe3a(pordinumber, ['tcp:{}:9300'.format(server_voog_port), 'udp:{}:9301'.format(server_datagramm_port)], hõivama=True) as sild:
        Protsess = subprocess.Popen(Käsk() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + sild.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        valija = selectors.DefaultSelector(); valija.register(Protsess.stdout, selectors.EVENT_READ)
        def saama_meil(marker=b'jkoros-native> ', 시간제한=60):
            andmed = bytearray(); lõpeta_kõne_nihe = time.monotonic() + 시간제한
            while marker not in andmed:
                if time.monotonic() > lõpeta_kõne_nihe or Protsess.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + andmed.decode('utf-8', 'replace'))
                for 누름값, _ in valija.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: andmed.extend(조각); transkriptsioon.extend(조각)
                if b'PANIC:' in andmed or b'FAIL ' in andmed: raise AssertionError(andmed)
            return andmed.decode('utf-8', 'replace').replace('\r\n', '\n')
        def kest(Joon):
            Protsess.stdin.write(Joon.encode() + b'\n'); Protsess.stdin.flush(); return saama_meil()
        try:
            saama_meil(); assert 'FTP listening' in kest('ftpd start')
            failiedastus_ühendus = ftplib.FTP(); failiedastus_ühendus.encoding = 'utf-8'; failiedastus_ühendus.connect('127.0.0.1', pordinumber, timeout=20); failiedastus_ühendus.login()
            last_andmed = bytes(range(256)) * 32
            failiedastus_ühendus.storbinary('STOR binary.dat', io.BytesIO(last_andmed))
            TULEMUS = bytearray(); failiedastus_ühendus.retrbinary('RETR binary.dat', TULEMUS.extend)
            assert TULEMUS == last_andmed; assert failiedastus_ühendus.size('binary.dat') == len(last_andmed)
            kinnitamine_aruanne['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            failiedastus_ühendus.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in kest('cat 한글.txt')
            assert '한글.txt' in failiedastus_ühendus.nlst()
            assert dict(failiedastus_ühendus.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            kinnitamine_aruanne['checks'].append('UTF-8 filename and content visible in guest shell')
            try: failiedastus_ühendus.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            TULEMUS = bytearray(); failiedastus_ühendus.retrbinary('RETR binary.dat', TULEMUS.extend); assert TULEMUS == last_andmed
            kinnitamine_aruanne['checks'].append('oversized replacement rejected; previous file preserved')
            with failiedastus_ühendus.transfercmd('STOR pending.txt') as Upload_Failid:
                # A control command must not change the active upload's destination.
                assert failiedastus_ühendus.size('binary.dat') == len(last_andmed)
                Upload_Failid.sendall(b'UPLOAD TARGET PRESERVED')
            assert failiedastus_ühendus.voidresp().startswith('226')
            TULEMUS = bytearray(); failiedastus_ühendus.retrbinary('RETR pending.txt', TULEMUS.extend)
            assert TULEMUS == b'UPLOAD TARGET PRESERVED'
            TULEMUS = bytearray(); failiedastus_ühendus.retrbinary('RETR binary.dat', TULEMUS.extend)
            assert TULEMUS == last_andmed
            failiedastus_ühendus.delete('pending.txt')
            kinnitamine_aruanne['checks'].append('interleaved SIZE cannot change the active STOR destination')
            failiedastus_ühendus.storbinary('STOR 인사.jar', io.BytesIO(Arhiiv.getvalue()))
            Tekst = kest('java -jar 인사.jar 누리')
            assert 'JAR Täida_käsk: 누리' in Tekst and 'oma tuum_VALUE Fail' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = kest('./인사.jar 세상')
            assert 'JAR Täida_käsk: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            kinnitamine_aruanne['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct andmed { int number; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct andmed VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.number != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = avama_Fail("cc.txt", 읽고쓰기 | 없으면만들기 | lühendama_Sisu, 0600); if (문서 < 0) return 1; kirjutamine_Fail_andmed(문서, 인사, sizeof(인사)-1); Sule_Fail(문서); kirjutamine_Fail_andmed(1, 인사, sizeof(인사)-1); return 0; }\n'
            failiedastus_ühendus.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = kest('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = kest('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in kest('cat cc.txt')
            실행파일 = bytearray(); failiedastus_ühendus.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            failiedastus_ühendus.storbinary('STOR eksemplar_VALUE.elf', io.BytesIO(실행파일)); Tekst = kest('run eksemplar_VALUE.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            failiedastus_ühendus.storbinary('STOR Täida_käsk', io.BytesIO(실행파일)); Tekst=kest('./Täida_käsk');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            failiedastus_ühendus.storbinary('STOR Nimi_2.txt', io.BytesIO(실행파일)); Tekst=kest('./Nimi_2.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            kest('rm Täida_käsk Nimi_2.txt')
            kinnitamine_aruanne['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            kest('rm binary.dat 한글.txt 한글.c 한글.elf eksemplar_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(näitaja_andmed/'linux-reference')
            failiedastus_ühendus.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=kest('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=kest('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in kest('cat linux.txt')
            failiedastus_ühendus.delete('리눅스인사');failiedastus_ühendus.delete('linux.txt')
            failiedastus_ühendus.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 number 없습니다:' in kest('./FALSE_VALUE.elf');failiedastus_ühendus.delete('FALSE_VALUE.elf')
            kinnitamine_aruanne['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as kaja_server_kirje:
                NET_lähe = näitaja_andmed/'바깥통신.java'
                NET_lähe.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Ühendu = Eesti.oma.ühendus_transport.Ühendu("10.0.2.2", Integer.parseInt(args[0]));
 Ühendu.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ALLIKAS = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ALLIKAS.length;i++) if (Ühendu.getInputStream().read() != (ALLIKAS[i]&255)) throw new RuntimeException("TCP mismatch");
 Ühendu.close();
 DatagramSocket osaleja = Eesti.oma.통신.Ava(0); Eesti.oma.통신.TIMEOUT(osaleja, 500);
 Eesti.oma.통신.saatma(osaleja, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Eesti.oma.통신.saama(osaleja).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 osaleja.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_juur/'build/java-library/classes'),'-d',str(näitaja_andmed),str(NET_lähe)])
                failiedastus_ühendus.storbinary('STOR 바깥통신.class', io.BytesIO((näitaja_andmed/'바깥통신.class').read_bytes()))
                Tekst = kest('java 바깥통신 {} {}'.format(kaja_server_kirje.TCP_port, kaja_server_kirje.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert kaja_server_kirje.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, kaja_server_kirje.수신됨
                assert not kaja_server_kirje.오류들, kaja_server_kirje.오류들
            kinnitamine_aruanne['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            failiedastus_ühendus.delete('바깥통신.class')
            server_lähe=näitaja_andmed/'서버시험.java'
            server_lähe.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket osaleja = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket külaline_VALUE = server_VALUE.accept();
  külaline_VALUE.getOutputStream().write(külaline_VALUE.getInputStream().read()+1); külaline_VALUE.close(); server_VALUE.close();
  byte[] Sisu_VALUE = new byte[8]; DatagramPacket datagramm = new DatagramPacket(Sisu_VALUE, Sisu_VALUE.length); osaleja.receive(datagramm);
  osaleja.send(datagramm); osaleja.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(näitaja_andmed),str(server_lähe)])
            failiedastus_ühendus.storbinary('STOR 서버시험.class',io.BytesIO((näitaja_andmed/'서버시험.class').read_bytes()))
            Protsess.stdin.write('java 서버시험\n'.encode());Protsess.stdin.flush();saama_meil(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_voog_port),timeout=5) as partner_VALUE:
                partner_VALUE.sendall(b'A');assert partner_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as partner_VALUE:
                partner_VALUE.settimeout(5);partner_VALUE.sendto(b'UDP-IN',('127.0.0.1',server_datagramm_port));assert partner_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Tekst=saama_meil();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            kinnitamine_aruanne['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            failiedastus_ühendus.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Argumendid) throws Exception { int SUM_VALUE = 0; int number = 1; while (number <= 10) { SUM_VALUE = SUM_VALUE + number; number = number + 1; } Eesti.oma.Väljund.kirjutamine_number(SUM_VALUE); Eesti.oma.Fail.Kirjutamine("aot.txt", "한글 AOT Fail 😀"); Eesti.oma.Väljund.kirjutamine_liin(Eesti.oma.Fail.Lugemine("aot.txt")); } }'
            failiedastus_ühendus.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Tekst = kest('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = kest('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = kest('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fail 😀' in Tekst and 'exit 0' in Tekst, Tekst
            자체실행파일 = bytearray(); failiedastus_ühendus.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Tekst = kest('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); failiedastus_ühendus.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); failiedastus_ühendus.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            failiedastus_ühendus.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = kest('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = kest('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fail 😀' in Tekst and 'exit 0' in Tekst, Tekst
            kinnitamine_aruanne['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            kinnitamine_aruanne['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=näitaja_andmed/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int Project_juur = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argumendid) {
  int[] VALUE = new int[] {Project_juur, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argumendid[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(näitaja_andmed),str(정적원문)])
            failiedastus_ühendus.storbinary('STOR 정적시험.class',io.BytesIO((näitaja_andmed/'정적시험.class').read_bytes()))
            Tekst=kest('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=kest('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            failiedastus_ühendus.delete('정적시험.class');failiedastus_ühendus.delete('정적시험.elf')
            kinnitamine_aruanne['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhiiv.getvalue());손상자료[14]^=1
            failiedastus_ühendus.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=kest('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            kinnitamine_aruanne['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            failiedastus_ühendus.quit(); assert 'FTP stopped' in kest('ftpd stop')
            assert not sild.VIGA, sild.VIGA
            kinnitamine_aruanne.update(passed=True, frames_to_guest=sild.커널수신틀수, frames_from_guest=sild.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in valija.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transkriptsioon.extend(조각)
            sild.Peata_sündmus.set()
            Protsess.terminate()
            try: Protsess.wait(timeout=5)
            except subprocess.TimeoutExpired: Protsess.kill(); Protsess.wait()
            valija.close(); Protsess.stdin.close(); Protsess.stdout.close()
            kinnitamine_aruanne['bridge_error'] = sild.VIGA
            kinnitamine_aruanne['frames_to_guest'] = sild.커널수신틀수; kinnitamine_aruanne['frames_from_guest'] = sild.커널발신틀수
            (näitaja_andmed/'packets.json').write_text(json.dumps(sild.jälituslogi,indent=2)+'\n')
            (näitaja_andmed / 'serial.log').write_bytes(transkriptsioon)
            (näitaja_andmed / 'report.json').write_text(json.dumps(kinnitamine_aruanne, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Käivita_2()
