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
from Reseau_Bréck import Reseau_Bréck
from ausféieren_Befeel import projezéieren_Racinn, Befeel
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Laf():
    Mooss_Daten = projezéieren_Racinn / 'build/verification/ftp'; Mooss_Daten.mkdir(parents=True, exist_ok=True)
    Validatioun_mellen = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((projezéieren_Racinn / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = Mooss_Daten / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.schreiwen_Zeil("JAR ausféieren_Befeel: " + 인수[0]); 한국어.자체.Fichier.schreiwen("jar.txt", "자체 Kernel_VALUE Fichier"); 한국어.자체.출력.schreiwen_Zeil(한국어.자체.Fichier.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(projezéieren_Racinn/'build/java-library/classes'), '-d', str(Mooss_Daten), str(자바원문)])
    Archiv = io.BytesIO()
    with zipfile.ZipFile(Archiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(Mooss_Daten/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); Server_Stream_Port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Reseau_Bréck(접속번호, ['tcp:{}:9300'.format(Server_Stream_Port), 'udp:{}:9301'.format(서버전문접속번호)], ophuelen=True) as Bréck:
        Prozess = subprocess.Popen(Befeel() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + Bréck.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        Selekteur = selectors.DefaultSelector(); Selekteur.register(Prozess.stdout, selectors.EVENT_READ)
        def 수신하기(Markéierung=b'jkoros-native> ', 시간제한=60):
            Daten = bytearray(); bëennegen_OFFSET = time.monotonic() + 시간제한
            while Markéierung not in Daten:
                if time.monotonic() > bëennegen_OFFSET or Prozess.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + Daten.decode('utf-8', 'replace'))
                for 누름값, _ in Selekteur.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: Daten.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in Daten or b'FAIL ' in Daten: raise AssertionError(Daten)
            return Daten.decode('utf-8', 'replace').replace('\r\n', '\n')
        def Shell(Zeil):
            Prozess.stdin.write(Zeil.encode() + b'\n'); Prozess.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in Shell('ftpd start')
            Fichier_Transfer_Verbindung = ftplib.FTP(); Fichier_Transfer_Verbindung.encoding = 'utf-8'; Fichier_Transfer_Verbindung.connect('127.0.0.1', 접속번호, timeout=20); Fichier_Transfer_Verbindung.login()
            nëtzlech_Charge_Daten = bytes(range(256)) * 32
            Fichier_Transfer_Verbindung.storbinary('STOR binary.dat', io.BytesIO(nëtzlech_Charge_Daten))
            Mooss = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR binary.dat', Mooss.extend)
            assert Mooss == nëtzlech_Charge_Daten; assert Fichier_Transfer_Verbindung.size('binary.dat') == len(nëtzlech_Charge_Daten)
            Validatioun_mellen['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            Fichier_Transfer_Verbindung.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in Shell('cat 한글.txt')
            assert '한글.txt' in Fichier_Transfer_Verbindung.nlst()
            assert dict(Fichier_Transfer_Verbindung.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            Validatioun_mellen['checks'].append('UTF-8 filename and content visible in guest shell')
            try: Fichier_Transfer_Verbindung.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            Mooss = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR binary.dat', Mooss.extend); assert Mooss == nëtzlech_Charge_Daten
            Validatioun_mellen['checks'].append('oversized replacement rejected; previous file preserved')
            with Fichier_Transfer_Verbindung.transfercmd('STOR pending.txt') as eroplueden_Fichieren:
                # A control command must not change the active upload's destination.
                assert Fichier_Transfer_Verbindung.size('binary.dat') == len(nëtzlech_Charge_Daten)
                eroplueden_Fichieren.sendall(b'UPLOAD TARGET PRESERVED')
            assert Fichier_Transfer_Verbindung.voidresp().startswith('226')
            Mooss = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR pending.txt', Mooss.extend)
            assert Mooss == b'UPLOAD TARGET PRESERVED'
            Mooss = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR binary.dat', Mooss.extend)
            assert Mooss == nëtzlech_Charge_Daten
            Fichier_Transfer_Verbindung.delete('pending.txt')
            Validatioun_mellen['checks'].append('interleaved SIZE cannot change the active STOR destination')
            Fichier_Transfer_Verbindung.storbinary('STOR 인사.jar', io.BytesIO(Archiv.getvalue()))
            SMS = Shell('java -jar 인사.jar 누리')
            assert 'JAR ausféieren_Befeel: 누리' in SMS and '자체 Kernel_VALUE Fichier' in SMS and 'exit 0' in SMS, SMS
            SMS = Shell('./인사.jar 세상')
            assert 'JAR ausféieren_Befeel: 세상' in SMS and 'exit 0' in SMS, SMS
            Validatioun_mellen['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct Daten { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct Daten VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ariichten_Fichier("cc.txt", lies_schreiffäeg | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; schreiwen_Fichier_Daten(문서, 인사, sizeof(인사)-1); Clôture_Fichier(문서); schreiwen_Fichier_Daten(1, 인사, sizeof(인사)-1); return 0; }\n'
            Fichier_Transfer_Verbindung.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = Shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = Shell('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in Shell('cat cc.txt')
            실행파일 = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            Fichier_Transfer_Verbindung.storbinary('STOR Instanz_VALUE.elf', io.BytesIO(실행파일)); SMS = Shell('run Instanz_VALUE.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            Fichier_Transfer_Verbindung.storbinary('STOR ausféieren_Befeel', io.BytesIO(실행파일)); SMS=Shell('./ausféieren_Befeel');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            Fichier_Transfer_Verbindung.storbinary('STOR Numm.txt', io.BytesIO(실행파일)); SMS=Shell('./Numm.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            Shell('rm ausféieren_Befeel Numm.txt')
            Validatioun_mellen['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            Shell('rm binary.dat 한글.txt 한글.c 한글.elf Instanz_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(Mooss_Daten/'linux-reference')
            Fichier_Transfer_Verbindung.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=Shell('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=Shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in Shell('cat linux.txt')
            Fichier_Transfer_Verbindung.delete('리눅스인사');Fichier_Transfer_Verbindung.delete('linux.txt')
            Fichier_Transfer_Verbindung.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in Shell('./FALSE_VALUE.elf');Fichier_Transfer_Verbindung.delete('FALSE_VALUE.elf')
            Validatioun_mellen['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = Mooss_Daten/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Verbannen = 한국어.자체.연결통신.Verbannen("10.0.2.2", Integer.parseInt(args[0]));
 Verbannen.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Quell = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Quell.length;i++) if (Verbannen.getInputStream().read() != (Quell[i]&255)) throw new RuntimeException("TCP mismatch");
 Verbannen.close();
 DatagramSocket 종단 = 한국어.자체.통신.ariichten(0); 한국어.자체.통신.TIMEOUT(종단, 500);
 한국어.자체.통신.mailen(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(projezéieren_Racinn/'build/java-library/classes'),'-d',str(Mooss_Daten),str(통신원문)])
                Fichier_Transfer_Verbindung.storbinary('STOR 바깥통신.class', io.BytesIO((Mooss_Daten/'바깥통신.class').read_bytes()))
                SMS = Shell('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_Port, 되돌림서버항목.UDP_Port))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            Validatioun_mellen['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            Fichier_Transfer_Verbindung.delete('바깥통신.class')
            Server_Quell=Mooss_Daten/'서버시험.java'
            Server_Quell.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket Server_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket Gaascht_VALUE = Server_VALUE.accept();
  Gaascht_VALUE.getOutputStream().write(Gaascht_VALUE.getInputStream().read()+1); Gaascht_VALUE.close(); Server_VALUE.close();
  byte[] Inhalt_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Inhalt_VALUE, Inhalt_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(Mooss_Daten),str(Server_Quell)])
            Fichier_Transfer_Verbindung.storbinary('STOR 서버시험.class',io.BytesIO((Mooss_Daten/'서버시험.class').read_bytes()))
            Prozess.stdin.write('java 서버시험\n'.encode());Prozess.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',Server_Stream_Port),timeout=5) as Peer_VALUE:
                Peer_VALUE.sendall(b'A');assert Peer_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as Peer_VALUE:
                Peer_VALUE.settimeout(5);Peer_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert Peer_VALUE.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            Validatioun_mellen['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            Fichier_Transfer_Verbindung.delete('서버시험.class')
            Instruktioun_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_VALUE); 한국어.자체.Fichier.schreiwen("aot.txt", "한글 AOT Fichier 😀"); 한국어.자체.출력.schreiwen_Zeil(한국어.자체.Fichier.읽기("aot.txt")); } }'
            Fichier_Transfer_Verbindung.storbinary('STOR 빛.java', io.BytesIO(Instruktioun_SEQUENCE.encode()))
            SMS = Shell('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = Shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = Shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fichier 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = Shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); Fichier_Transfer_Verbindung.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            Fichier_Transfer_Verbindung.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = Shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = Shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT Fichier 😀' in SMS and 'exit 0' in SMS, SMS
            Validatioun_mellen['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            Validatioun_mellen['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statesch_Quell=Mooss_Daten/'정적시험.java'
            statesch_Quell.write_text('''public class 정적시험 {
 static int projezéieren_Racinn = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {projezéieren_Racinn, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(Mooss_Daten),str(statesch_Quell)])
            Fichier_Transfer_Verbindung.storbinary('STOR 정적시험.class',io.BytesIO((Mooss_Daten/'정적시험.class').read_bytes()))
            SMS=Shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=Shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            Fichier_Transfer_Verbindung.delete('정적시험.class');Fichier_Transfer_Verbindung.delete('정적시험.elf')
            Validatioun_mellen['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archiv.getvalue());손상자료[14]^=1
            Fichier_Transfer_Verbindung.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=Shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            Validatioun_mellen['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            Fichier_Transfer_Verbindung.quit(); assert 'FTP stopped' in Shell('ftpd stop')
            assert not Bréck.Feeler, Bréck.Feeler
            Validatioun_mellen.update(passed=True, frames_to_guest=Bréck.커널수신틀수, frames_from_guest=Bréck.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in Selekteur.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            Bréck.pausen_Evenement.set()
            Prozess.terminate()
            try: Prozess.wait(timeout=5)
            except subprocess.TimeoutExpired: Prozess.kill(); Prozess.wait()
            Selekteur.close(); Prozess.stdin.close(); Prozess.stdout.close()
            Validatioun_mellen['bridge_error'] = Bréck.Feeler
            Validatioun_mellen['frames_to_guest'] = Bréck.커널수신틀수; Validatioun_mellen['frames_from_guest'] = Bréck.커널발신틀수
            (Mooss_Daten/'packets.json').write_text(json.dumps(Bréck.추적기록,indent=2)+'\n')
            (Mooss_Daten / 'serial.log').write_bytes(대화기록)
            (Mooss_Daten / 'report.json').write_text(json.dumps(Validatioun_mellen, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Laf()
