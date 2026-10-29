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
from tilts_3de4fe3a import tilts_3de4fe3a
from Izpildīt_komanda import Project_sakne, Komanda
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Palaist():
    mērs_dati = Project_sakne / 'build/verification/ftp'; mērs_dati.mkdir(parents=True, exist_ok=True)
    validācija_ziņot = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_sakne / 'build/kernel8.img').read_bytes()).hexdigest()}
    transkripcija = bytearray()
    자바원문 = mērs_dati / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Parametri) throws Exception { Latviešu.savs.Izvade.rakstīšana_līnija("JAR Izpildīt_komanda: " + Parametri[0]); Latviešu.savs.Fails.Rakstīt("jar.txt", "savs kodols_VALUE Fails"); Latviešu.savs.Izvade.rakstīšana_līnija(Latviešu.savs.Fails.Lasīt("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_sakne/'build/java-library/classes'), '-d', str(mērs_dati), str(자바원문)])
    Arhīvs = io.BytesIO()
    with zipfile.ZipFile(Arhīvs, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(mērs_dati/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); porta_numurs = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); serveris_Stream_ports = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); serveris_datogramma_ports = 임시자원.getsockname()[1]
    with tilts_3de4fe3a(porta_numurs, ['tcp:{}:9300'.format(serveris_Stream_ports), 'udp:{}:9301'.format(serveris_datogramma_ports)], tvert=True) as tilts:
        Process = subprocess.Popen(Komanda() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + tilts.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        atlasītājs = selectors.DefaultSelector(); atlasītājs.register(Process.stdout, selectors.EVENT_READ)
        def saņemt_ziņa(marķieris=b'jkoros-native> ', 시간제한=60):
            dati = bytearray(); beigt_zvanu_Nobīde = time.monotonic() + 시간제한
            while marķieris not in dati:
                if time.monotonic() > beigt_zvanu_Nobīde or Process.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + dati.decode('utf-8', 'replace'))
                for 누름값, _ in atlasītājs.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: dati.extend(조각); transkripcija.extend(조각)
                if b'PANIC:' in dati or b'FAIL ' in dati: raise AssertionError(dati)
            return dati.decode('utf-8', 'replace').replace('\r\n', '\n')
        def čaula(Līniju):
            Process.stdin.write(Līniju.encode() + b'\n'); Process.stdin.flush(); return saņemt_ziņa()
        try:
            saņemt_ziņa(); assert 'FTP listening' in čaula('ftpd start')
            faila_pārsūtīšana_paziņa = ftplib.FTP(); faila_pārsūtīšana_paziņa.encoding = 'utf-8'; faila_pārsūtīšana_paziņa.connect('127.0.0.1', porta_numurs, timeout=20); faila_pārsūtīšana_paziņa.login()
            vērtums_dati = bytes(range(256)) * 32
            faila_pārsūtīšana_paziņa.storbinary('STOR binary.dat', io.BytesIO(vērtums_dati))
            mērs = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR binary.dat', mērs.extend)
            assert mērs == vērtums_dati; assert faila_pārsūtīšana_paziņa.size('binary.dat') == len(vērtums_dati)
            validācija_ziņot['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            faila_pārsūtīšana_paziņa.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in čaula('cat 한글.txt')
            assert '한글.txt' in faila_pārsūtīšana_paziņa.nlst()
            assert dict(faila_pārsūtīšana_paziņa.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validācija_ziņot['checks'].append('UTF-8 filename and content visible in guest shell')
            try: faila_pārsūtīšana_paziņa.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            mērs = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR binary.dat', mērs.extend); assert mērs == vērtums_dati
            validācija_ziņot['checks'].append('oversized replacement rejected; previous file preserved')
            with faila_pārsūtīšana_paziņa.transfercmd('STOR pending.txt') as Upload_Faili:
                # A control command must not change the active upload's destination.
                assert faila_pārsūtīšana_paziņa.size('binary.dat') == len(vērtums_dati)
                Upload_Faili.sendall(b'UPLOAD TARGET PRESERVED')
            assert faila_pārsūtīšana_paziņa.voidresp().startswith('226')
            mērs = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR pending.txt', mērs.extend)
            assert mērs == b'UPLOAD TARGET PRESERVED'
            mērs = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR binary.dat', mērs.extend)
            assert mērs == vērtums_dati
            faila_pārsūtīšana_paziņa.delete('pending.txt')
            validācija_ziņot['checks'].append('interleaved SIZE cannot change the active STOR destination')
            faila_pārsūtīšana_paziņa.storbinary('STOR 인사.jar', io.BytesIO(Arhīvs.getvalue()))
            Teksts = čaula('java -jar 인사.jar 누리')
            assert 'JAR Izpildīt_komanda: 누리' in Teksts and 'savs kodols_VALUE Fails' in Teksts and 'exit 0' in Teksts, Teksts
            Teksts = čaula('./인사.jar 세상')
            assert 'JAR Izpildīt_komanda: 세상' in Teksts and 'exit 0' in Teksts, Teksts
            validācija_ziņot['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct dati { int numurs; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct dati VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.numurs != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = atvērt_Fails("cc.txt", 읽고쓰기 | 없으면만들기 | apraut_Satura_rādītājs, 0600); if (문서 < 0) return 1; rakstīšana_Fails_dati(문서, 인사, sizeof(인사)-1); Aizvērt_Fails(문서); rakstīšana_Fails_dati(1, 인사, sizeof(인사)-1); return 0; }\n'
            faila_pārsūtīšana_paziņa.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Teksts = čaula('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Teksts and 'exit 0' in Teksts, Teksts
            Teksts = čaula('run 한글.elf'); assert 'CC NATIVE PASS' in Teksts and 'exit 0' in Teksts, Teksts
            assert 'CC NATIVE PASS' in čaula('cat cc.txt')
            izpildāms_fails = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR 한글.elf', izpildāms_fails.extend)
            assert izpildāms_fails[:4] == b'\x7fELF' and izpildāms_fails[18:20] == b'\xb7\x00'
            faila_pārsūtīšana_paziņa.storbinary('STOR kopēt_VALUE.elf', io.BytesIO(izpildāms_fails)); Teksts = čaula('run kopēt_VALUE.elf'); assert 'CC NATIVE PASS' in Teksts and 'exit 0' in Teksts, Teksts
            faila_pārsūtīšana_paziņa.storbinary('STOR Izpildīt_komanda', io.BytesIO(izpildāms_fails)); Teksts=čaula('./Izpildīt_komanda');assert 'CC NATIVE PASS' in Teksts and 'exit 0' in Teksts,Teksts
            faila_pārsūtīšana_paziņa.storbinary('STOR Nosaukums.txt', io.BytesIO(izpildāms_fails)); Teksts=čaula('./Nosaukums.txt');assert 'CC NATIVE PASS' in Teksts and 'exit 0' in Teksts,Teksts
            čaula('rm Izpildīt_komanda Nosaukums.txt')
            validācija_ziņot['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            čaula('rm binary.dat 한글.txt 한글.c 한글.elf kopēt_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(mērs_dati/'linux-reference')
            faila_pārsūtīšana_paziņa.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Teksts=čaula('./리눅스인사');assert 'exit -8' in Teksts,Teksts
            Teksts=čaula('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Teksts,Teksts
            assert 'LINUX ELF FILE IO' in čaula('cat linux.txt')
            faila_pārsūtīšana_paziņa.delete('리눅스인사');faila_pārsūtīšana_paziņa.delete('linux.txt')
            faila_pārsūtīšana_paziņa.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 numurs 없습니다:' in čaula('./FALSE_VALUE.elf');faila_pārsūtīšana_paziņa.delete('FALSE_VALUE.elf')
            validācija_ziņot['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as atbalss_serveris_ievade:
                NET_avots = mērs_dati/'바깥통신.java'
                NET_avots.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Savienoties = Latviešu.savs.paziņa_transportēšana.Savienoties("10.0.2.2", Integer.parseInt(args[0]));
 Savienoties.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] AVOTS = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<AVOTS.length;i++) if (Savienoties.getInputStream().read() != (AVOTS[i]&255)) throw new RuntimeException("TCP mismatch");
 Savienoties.close();
 DatagramSocket dalībnieks = Latviešu.savs.통신.Atvērt(0); Latviešu.savs.통신.NOILGUMS(dalībnieks, 500);
 Latviešu.savs.통신.sūtīt(dalībnieks, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Latviešu.savs.통신.saņemt(dalībnieks).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 dalībnieks.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_sakne/'build/java-library/classes'),'-d',str(mērs_dati),str(NET_avots)])
                faila_pārsūtīšana_paziņa.storbinary('STOR 바깥통신.class', io.BytesIO((mērs_dati/'바깥통신.class').read_bytes()))
                Teksts = čaula('java 바깥통신 {} {}'.format(atbalss_serveris_ievade.TCP_ports, atbalss_serveris_ievade.UDP_ports))
                assert 'EXTERNAL TCP UDP PASS' in Teksts and '10.0.2.2' in Teksts and 'exit 0' in Teksts, Teksts
                assert atbalss_serveris_ievade.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, atbalss_serveris_ievade.수신됨
                assert not atbalss_serveris_ievade.오류들, atbalss_serveris_ievade.오류들
            validācija_ziņot['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            faila_pārsūtīšana_paziņa.delete('바깥통신.class')
            serveris_avots=mērs_dati/'서버시험.java'
            serveris_avots.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket serveris_VALUE = new ServerSocket(9300); DatagramSocket dalībnieks = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket viesis_VALUE = serveris_VALUE.accept();
  viesis_VALUE.getOutputStream().write(viesis_VALUE.getInputStream().read()+1); viesis_VALUE.close(); serveris_VALUE.close();
  byte[] Saturs_VALUE = new byte[8]; DatagramPacket datogramma = new DatagramPacket(Saturs_VALUE, Saturs_VALUE.length); dalībnieks.receive(datogramma);
  dalībnieks.send(datogramma); dalībnieks.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mērs_dati),str(serveris_avots)])
            faila_pārsūtīšana_paziņa.storbinary('STOR 서버시험.class',io.BytesIO((mērs_dati/'서버시험.class').read_bytes()))
            Process.stdin.write('java 서버시험\n'.encode());Process.stdin.flush();saņemt_ziņa(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',serveris_Stream_ports),timeout=5) as vienranga_VALUE:
                vienranga_VALUE.sendall(b'A');assert vienranga_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as vienranga_VALUE:
                vienranga_VALUE.settimeout(5);vienranga_VALUE.sendto(b'UDP-IN',('127.0.0.1',serveris_datogramma_ports));assert vienranga_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Teksts=saņemt_ziņa();assert 'INBOUND TCP UDP PASS' in Teksts and 'exit 0' in Teksts,Teksts
            validācija_ziņot['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            faila_pārsūtīšana_paziņa.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Parametri) throws Exception { int SUM_VALUE = 0; int numurs = 1; while (numurs <= 10) { SUM_VALUE = SUM_VALUE + numurs; numurs = numurs + 1; } Latviešu.savs.Izvade.rakstīšana_numurs(SUM_VALUE); Latviešu.savs.Fails.Rakstīt("aot.txt", "한글 AOT Fails 😀"); Latviešu.savs.Izvade.rakstīšana_līnija(Latviešu.savs.Fails.Lasīt("aot.txt")); } }'
            faila_pārsūtīšana_paziņa.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Teksts = čaula('javac 빛.java'); assert 'exit 0' in Teksts and 'Compiled:' in Teksts, Teksts
            Teksts = čaula('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teksts and 'exit 0' in Teksts, Teksts
            Teksts = čaula('run 빛.elf'); assert '\n55\n' in Teksts and '한글 AOT Fails 😀' in Teksts and 'exit 0' in Teksts, Teksts
            자체실행파일 = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Teksts = čaula('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Teksts and 'unsupported' in Teksts, Teksts
            보존자료 = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); faila_pārsūtīšana_paziņa.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            faila_pārsūtīšana_paziņa.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Teksts = čaula('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teksts and 'exit 0' in Teksts, Teksts
            Teksts = čaula('run 빛.elf'); assert '\n55\n' in Teksts and '한글 AOT Fails 😀' in Teksts and 'exit 0' in Teksts, Teksts
            validācija_ziņot['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validācija_ziņot['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=mērs_dati/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int Project_sakne = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Parametri) {
  int[] VALUE = new int[] {Project_sakne, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Parametri[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(mērs_dati),str(정적원문)])
            faila_pārsūtīšana_paziņa.storbinary('STOR 정적시험.class',io.BytesIO((mērs_dati/'정적시험.class').read_bytes()))
            Teksts=čaula('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Teksts,Teksts
            Teksts=čaula('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Teksts,Teksts
            faila_pārsūtīšana_paziņa.delete('정적시험.class');faila_pārsūtīšana_paziņa.delete('정적시험.elf')
            validācija_ziņot['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arhīvs.getvalue());손상자료[14]^=1
            faila_pārsūtīšana_paziņa.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Teksts=čaula('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Teksts,Teksts
            validācija_ziņot['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            faila_pārsūtīšana_paziņa.quit(); assert 'FTP stopped' in čaula('ftpd stop')
            assert not tilts.Kļūda, tilts.Kļūda
            validācija_ziņot.update(passed=True, frames_to_guest=tilts.커널수신틀수, frames_from_guest=tilts.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in atlasītājs.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: transkripcija.extend(조각)
            tilts.Pauze_notikums.set()
            Process.terminate()
            try: Process.wait(timeout=5)
            except subprocess.TimeoutExpired: Process.kill(); Process.wait()
            atlasītājs.close(); Process.stdin.close(); Process.stdout.close()
            validācija_ziņot['bridge_error'] = tilts.Kļūda
            validācija_ziņot['frames_to_guest'] = tilts.커널수신틀수; validācija_ziņot['frames_from_guest'] = tilts.커널발신틀수
            (mērs_dati/'packets.json').write_text(json.dumps(tilts.trasēšanas_žurnāls,indent=2)+'\n')
            (mērs_dati / 'serial.log').write_bytes(transkripcija)
            (mērs_dati / 'report.json').write_text(json.dumps(validācija_ziņot, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Palaist()
