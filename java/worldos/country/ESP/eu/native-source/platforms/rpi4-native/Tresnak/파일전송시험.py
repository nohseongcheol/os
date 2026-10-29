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
from sare_zubi import sare_zubi
from exekutatu_komando import Project_erro, Komandoa
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Exekutatu_2():
    neurria_datuak = Project_erro / 'build/verification/ftp'; neurria_datuak.mkdir(parents=True, exist_ok=True)
    balidazio_txosten = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_erro / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = neurria_datuak / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argumentuak) throws Exception { Euskara.자체.Irteera.idatzi_lerro("JAR exekutatu_komando: " + Argumentuak[0]); Euskara.자체.Fitxategia.Idatzi("jar.txt", "자체 nukleo_balio Fitxategia"); Euskara.자체.Irteera.idatzi_lerro(Euskara.자체.Fitxategia.Irakurri("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_erro/'build/java-library/classes'), '-d', str(neurria_datuak), str(자바원문)])
    artxibo = io.BytesIO()
    with zipfile.ZipFile(artxibo, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(neurria_datuak/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ataka_zenbaki = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); zerbitzari_Stream_ataka = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with sare_zubi(ataka_zenbaki, ['tcp:{}:9300'.format(zerbitzari_Stream_ataka), 'udp:{}:9301'.format(서버전문접속번호)], atera_ba7b8054=True) as zubi:
        Prozesua = subprocess.Popen(Komandoa() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + zubi.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(Prozesua.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            datuak = bytearray(); amaitu_Geruzak = time.monotonic() + 시간제한
            while 확인표시 not in datuak:
                if time.monotonic() > amaitu_Geruzak or Prozesua.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + datuak.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: datuak.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in datuak or b'FAIL ' in datuak: raise AssertionError(datuak)
            return datuak.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(Marra):
            Prozesua.stdin.write(Marra.encode() + b'\n'); Prozesua.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in shell('ftpd start')
            fitxategi_transferitu_konexio = ftplib.FTP(); fitxategi_transferitu_konexio.encoding = 'utf-8'; fitxategi_transferitu_konexio.connect('127.0.0.1', ataka_zenbaki, timeout=20); fitxategi_transferitu_konexio.login()
            karga_datuak = bytes(range(256)) * 32
            fitxategi_transferitu_konexio.storbinary('STOR binary.dat', io.BytesIO(karga_datuak))
            EMAITZA = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR binary.dat', EMAITZA.extend)
            assert EMAITZA == karga_datuak; assert fitxategi_transferitu_konexio.size('binary.dat') == len(karga_datuak)
            balidazio_txosten['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fitxategi_transferitu_konexio.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in fitxategi_transferitu_konexio.nlst()
            assert dict(fitxategi_transferitu_konexio.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            balidazio_txosten['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fitxategi_transferitu_konexio.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            EMAITZA = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR binary.dat', EMAITZA.extend); assert EMAITZA == karga_datuak
            balidazio_txosten['checks'].append('oversized replacement rejected; previous file preserved')
            with fitxategi_transferitu_konexio.transfercmd('STOR pending.txt') as Upload_Fitxategiak:
                # A control command must not change the active upload's destination.
                assert fitxategi_transferitu_konexio.size('binary.dat') == len(karga_datuak)
                Upload_Fitxategiak.sendall(b'UPLOAD TARGET PRESERVED')
            assert fitxategi_transferitu_konexio.voidresp().startswith('226')
            EMAITZA = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR pending.txt', EMAITZA.extend)
            assert EMAITZA == b'UPLOAD TARGET PRESERVED'
            EMAITZA = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR binary.dat', EMAITZA.extend)
            assert EMAITZA == karga_datuak
            fitxategi_transferitu_konexio.delete('pending.txt')
            balidazio_txosten['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fitxategi_transferitu_konexio.storbinary('STOR 인사.jar', io.BytesIO(artxibo.getvalue()))
            Testua = shell('java -jar 인사.jar 누리')
            assert 'JAR exekutatu_komando: 누리' in Testua and '자체 nukleo_balio Fitxategia' in Testua and 'exit 0' in Testua, Testua
            Testua = shell('./인사.jar 세상')
            assert 'JAR exekutatu_komando: 세상' in Testua and 'exit 0' in Testua, Testua
            balidazio_txosten['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct datuak { int 수; double 비율; };\nint BATU_balio(int n) { return n ? n + BATU_balio(n-1) : 0; }\nint main(void) { struct datuak balio = {BATU_balio(10), 1.25}; if (balio.수 != 55 || balio.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ireki_fitxategi("cc.txt", irakurri_idatzi | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; idatzi_fitxategi_datuak(문서, 인사, sizeof(인사)-1); itxi_fitxategi(문서); idatzi_fitxategi_datuak(1, 인사, sizeof(인사)-1); return 0; }\n'
            fitxategi_transferitu_konexio.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Testua = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Testua and 'exit 0' in Testua, Testua
            Testua = shell('run 한글.elf'); assert 'CC NATIVE PASS' in Testua and 'exit 0' in Testua, Testua
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            실행파일 = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fitxategi_transferitu_konexio.storbinary('STOR kopiatu_balio.elf', io.BytesIO(실행파일)); Testua = shell('run kopiatu_balio.elf'); assert 'CC NATIVE PASS' in Testua and 'exit 0' in Testua, Testua
            fitxategi_transferitu_konexio.storbinary('STOR exekutatu_komando', io.BytesIO(실행파일)); Testua=shell('./exekutatu_komando');assert 'CC NATIVE PASS' in Testua and 'exit 0' in Testua,Testua
            fitxategi_transferitu_konexio.storbinary('STOR Izena.txt', io.BytesIO(실행파일)); Testua=shell('./Izena.txt');assert 'CC NATIVE PASS' in Testua and 'exit 0' in Testua,Testua
            shell('rm exekutatu_komando Izena.txt')
            balidazio_txosten['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf kopiatu_balio.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(neurria_datuak/'linux-reference')
            fitxategi_transferitu_konexio.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Testua=shell('./리눅스인사');assert 'exit -8' in Testua,Testua
            Testua=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Testua,Testua
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            fitxategi_transferitu_konexio.delete('리눅스인사');fitxategi_transferitu_konexio.delete('linux.txt')
            fitxategi_transferitu_konexio.storbinary('STOR FALTSUA_balio.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in shell('./FALTSUA_balio.elf');fitxategi_transferitu_konexio.delete('FALTSUA_balio.elf')
            balidazio_txosten['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as atzeko_planoko_eguneratze_zerbitzari_sarrera:
                통신원문 = neurria_datuak/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Konektatu = Euskara.자체.연결통신.Konektatu("10.0.2.2", Integer.parseInt(args[0]));
 Konektatu.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ITURBURUA = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ITURBURUA.length;i++) if (Konektatu.getInputStream().read() != (ITURBURUA[i]&255)) throw new RuntimeException("TCP mismatch");
 Konektatu.close();
 DatagramSocket amaiera_puntu = Euskara.자체.통신.Ireki(0); Euskara.자체.통신.DENBORA_MUGA(amaiera_puntu, 500);
 Euskara.자체.통신.bidali(amaiera_puntu, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!Euskara.자체.통신.받기(amaiera_puntu).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 amaiera_puntu.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_erro/'build/java-library/classes'),'-d',str(neurria_datuak),str(통신원문)])
                fitxategi_transferitu_konexio.storbinary('STOR 바깥통신.class', io.BytesIO((neurria_datuak/'바깥통신.class').read_bytes()))
                Testua = shell('java 바깥통신 {} {}'.format(atzeko_planoko_eguneratze_zerbitzari_sarrera.TCP_ataka, atzeko_planoko_eguneratze_zerbitzari_sarrera.UDP_ataka))
                assert 'EXTERNAL TCP UDP PASS' in Testua and '10.0.2.2' in Testua and 'exit 0' in Testua, Testua
                assert atzeko_planoko_eguneratze_zerbitzari_sarrera.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, atzeko_planoko_eguneratze_zerbitzari_sarrera.수신됨
                assert not atzeko_planoko_eguneratze_zerbitzari_sarrera.오류들, atzeko_planoko_eguneratze_zerbitzari_sarrera.오류들
            balidazio_txosten['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fitxategi_transferitu_konexio.delete('바깥통신.class')
            zerbitzari_iturburu=neurria_datuak/'서버시험.java'
            zerbitzari_iturburu.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket zerbitzari_balio = new ServerSocket(9300); DatagramSocket amaiera_puntu = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gonbidatu_balio = zerbitzari_balio.accept();
  gonbidatu_balio.getOutputStream().write(gonbidatu_balio.getInputStream().read()+1); gonbidatu_balio.close(); zerbitzari_balio.close();
  byte[] eduki_balio = new byte[8]; DatagramPacket 전문 = new DatagramPacket(eduki_balio, eduki_balio.length); amaiera_puntu.receive(전문);
  amaiera_puntu.send(전문); amaiera_puntu.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(neurria_datuak),str(zerbitzari_iturburu)])
            fitxategi_transferitu_konexio.storbinary('STOR 서버시험.class',io.BytesIO((neurria_datuak/'서버시험.class').read_bytes()))
            Prozesua.stdin.write('java 서버시험\n'.encode());Prozesua.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',zerbitzari_Stream_ataka),timeout=5) as pareko_balio:
                pareko_balio.sendall(b'A');assert pareko_balio.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as pareko_balio:
                pareko_balio.settimeout(5);pareko_balio.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert pareko_balio.recvfrom(512)[0]==b'UDP-IN'
            Testua=수신하기();assert 'INBOUND TCP UDP PASS' in Testua and 'exit 0' in Testua,Testua
            balidazio_txosten['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fitxategi_transferitu_konexio.delete('서버시험.class')
            instrukzio_SEKUENTZIA = 'public class 빛 { public static void main(String[] Argumentuak) throws Exception { int BATU_balio = 0; int 수 = 1; while (수 <= 10) { BATU_balio = BATU_balio + 수; 수 = 수 + 1; } Euskara.자체.Irteera.수쓰기(BATU_balio); Euskara.자체.Fitxategia.Idatzi("aot.txt", "한글 AOT Fitxategia 😀"); Euskara.자체.Irteera.idatzi_lerro(Euskara.자체.Fitxategia.Irakurri("aot.txt")); } }'
            fitxategi_transferitu_konexio.storbinary('STOR 빛.java', io.BytesIO(instrukzio_SEKUENTZIA.encode()))
            Testua = shell('javac 빛.java'); assert 'exit 0' in Testua and 'Compiled:' in Testua, Testua
            Testua = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Testua and 'exit 0' in Testua, Testua
            Testua = shell('run 빛.elf'); assert '\n55\n' in Testua and '한글 AOT Fitxategia 😀' in Testua and 'exit 0' in Testua, Testua
            자체실행파일 = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Testua = shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Testua and 'unsupported' in Testua, Testua
            보존자료 = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fitxategi_transferitu_konexio.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fitxategi_transferitu_konexio.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Testua = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Testua and 'exit 0' in Testua, Testua
            Testua = shell('run 빛.elf'); assert '\n55\n' in Testua and '한글 AOT Fitxategia 😀' in Testua and 'exit 0' in Testua, Testua
            balidazio_txosten['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            balidazio_txosten['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            estatiko_iturburu=neurria_datuak/'정적시험.java'
            estatiko_iturburu.write_text('''public class 정적시험 {
 static int Project_erro = 3;
 static int BATU_balio(int n) { return n == 0 ? 0 : n + BATU_balio(n-1); }
 public static void main(String[] Argumentuak) {
  int[] balio = new int[] {Project_erro, BATU_balio(10)};
  System.out.println(balio[0] + balio[1]); System.out.println(Argumentuak[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(neurria_datuak),str(estatiko_iturburu)])
            fitxategi_transferitu_konexio.storbinary('STOR 정적시험.class',io.BytesIO((neurria_datuak/'정적시험.class').read_bytes()))
            Testua=shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Testua,Testua
            Testua=shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Testua,Testua
            fitxategi_transferitu_konexio.delete('정적시험.class');fitxategi_transferitu_konexio.delete('정적시험.elf')
            balidazio_txosten['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(artxibo.getvalue());손상자료[14]^=1
            fitxategi_transferitu_konexio.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Testua=shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Testua,Testua
            balidazio_txosten['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fitxategi_transferitu_konexio.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not zubi.errorea, zubi.errorea
            balidazio_txosten.update(passed=True, frames_to_guest=zubi.커널수신틀수, frames_from_guest=zubi.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            zubi.pausatu_gertaera.set()
            Prozesua.terminate()
            try: Prozesua.wait(timeout=5)
            except subprocess.TimeoutExpired: Prozesua.kill(); Prozesua.wait()
            준비선택기.close(); Prozesua.stdin.close(); Prozesua.stdout.close()
            balidazio_txosten['bridge_error'] = zubi.errorea
            balidazio_txosten['frames_to_guest'] = zubi.커널수신틀수; balidazio_txosten['frames_from_guest'] = zubi.커널발신틀수
            (neurria_datuak/'packets.json').write_text(json.dumps(zubi.balio_diagonalen_batura_LOG,indent=2)+'\n')
            (neurria_datuak / 'serial.log').write_bytes(대화기록)
            (neurria_datuak / 'report.json').write_text(json.dumps(balidazio_txosten, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Exekutatu_2()
