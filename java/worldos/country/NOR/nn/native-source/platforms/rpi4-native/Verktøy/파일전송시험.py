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
from Nettverk_bru import Nettverk_bru
from Utfør_kommando import spegle_rot, Kommando
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Køyr_2():
    forretningsmål_data = spegle_rot / 'build/verification/ftp'; forretningsmål_data.mkdir(parents=True, exist_ok=True)
    validering_rapport = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((spegle_rot / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = forretningsmål_data / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Argument) throws Exception { 한국어.자체.Utdata.skrive_line("JAR Utfør_kommando: " + Argument[0]); 한국어.자체.Fil.Skriv("jar.txt", "자체 kjerne_VALUE Fil"); 한국어.자체.Utdata.skrive_line(한국어.자체.Fil.Les("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(spegle_rot/'build/java-library/classes'), '-d', str(forretningsmål_data), str(자바원문)])
    Arkiv = io.BytesIO()
    with zipfile.ZipFile(Arkiv, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(forretningsmål_data/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); portnummer = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); tenar_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Nettverk_bru(portnummer, ['tcp:{}:9300'.format(tenar_Stream_port), 'udp:{}:9301'.format(서버전문접속번호)], ta_opp=True) as bru:
        Prosess = subprocess.Popen(Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + bru.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        veljar = selectors.DefaultSelector(); veljar.register(Prosess.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); avslutte_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > avslutte_OFFSET or Prosess.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in veljar.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def grensesnitt(linje):
            Prosess.stdin.write(linje.encode() + b'\n'); Prosess.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in grensesnitt('ftpd start')
            fil_Overfør_kontakt = ftplib.FTP(); fil_Overfør_kontakt.encoding = 'utf-8'; fil_Overfør_kontakt.connect('127.0.0.1', portnummer, timeout=20); fil_Overfør_kontakt.login()
            nyttelast_data = bytes(range(256)) * 32
            fil_Overfør_kontakt.storbinary('STOR binary.dat', io.BytesIO(nyttelast_data))
            forretningsmål = bytearray(); fil_Overfør_kontakt.retrbinary('RETR binary.dat', forretningsmål.extend)
            assert forretningsmål == nyttelast_data; assert fil_Overfør_kontakt.size('binary.dat') == len(nyttelast_data)
            validering_rapport['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            fil_Overfør_kontakt.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in grensesnitt('cat 한글.txt')
            assert '한글.txt' in fil_Overfør_kontakt.nlst()
            assert dict(fil_Overfør_kontakt.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validering_rapport['checks'].append('UTF-8 filename and content visible in guest shell')
            try: fil_Overfør_kontakt.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            forretningsmål = bytearray(); fil_Overfør_kontakt.retrbinary('RETR binary.dat', forretningsmål.extend); assert forretningsmål == nyttelast_data
            validering_rapport['checks'].append('oversized replacement rejected; previous file preserved')
            with fil_Overfør_kontakt.transfercmd('STOR pending.txt') as Upload_Filer:
                # A control command must not change the active upload's destination.
                assert fil_Overfør_kontakt.size('binary.dat') == len(nyttelast_data)
                Upload_Filer.sendall(b'UPLOAD TARGET PRESERVED')
            assert fil_Overfør_kontakt.voidresp().startswith('226')
            forretningsmål = bytearray(); fil_Overfør_kontakt.retrbinary('RETR pending.txt', forretningsmål.extend)
            assert forretningsmål == b'UPLOAD TARGET PRESERVED'
            forretningsmål = bytearray(); fil_Overfør_kontakt.retrbinary('RETR binary.dat', forretningsmål.extend)
            assert forretningsmål == nyttelast_data
            fil_Overfør_kontakt.delete('pending.txt')
            validering_rapport['checks'].append('interleaved SIZE cannot change the active STOR destination')
            fil_Overfør_kontakt.storbinary('STOR 인사.jar', io.BytesIO(Arkiv.getvalue()))
            Tekst = grensesnitt('java -jar 인사.jar 누리')
            assert 'JAR Utfør_kommando: 누리' in Tekst and '자체 kjerne_VALUE Fil' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = grensesnitt('./인사.jar 세상')
            assert 'JAR Utfør_kommando: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            validering_rapport['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct data VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = opne_fil("cc.txt", lese_og_skrivetilgang | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; skrive_fil_data(문서, 인사, sizeof(인사)-1); Lukk_fil(문서); skrive_fil_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            fil_Overfør_kontakt.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = grensesnitt('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = grensesnitt('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in grensesnitt('cat cc.txt')
            실행파일 = bytearray(); fil_Overfør_kontakt.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            fil_Overfør_kontakt.storbinary('STOR kopiere_VALUE.elf', io.BytesIO(실행파일)); Tekst = grensesnitt('run kopiere_VALUE.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            fil_Overfør_kontakt.storbinary('STOR Utfør_kommando', io.BytesIO(실행파일)); Tekst=grensesnitt('./Utfør_kommando');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            fil_Overfør_kontakt.storbinary('STOR Namn.txt', io.BytesIO(실행파일)); Tekst=grensesnitt('./Namn.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            grensesnitt('rm Utfør_kommando Namn.txt')
            validering_rapport['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            grensesnitt('rm binary.dat 한글.txt 한글.c 한글.elf kopiere_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(forretningsmål_data/'linux-reference')
            fil_Overfør_kontakt.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=grensesnitt('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=grensesnitt('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in grensesnitt('cat linux.txt')
            fil_Overfør_kontakt.delete('리눅스인사');fil_Overfør_kontakt.delete('linux.txt')
            fil_Overfør_kontakt.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in grensesnitt('./FALSE_VALUE.elf');fil_Overfør_kontakt.delete('FALSE_VALUE.elf')
            validering_rapport['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = forretningsmål_data/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Kopla_til = 한국어.자체.연결통신.Kopla_til("10.0.2.2", Integer.parseInt(args[0]));
 Kopla_til.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] KJELDE = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<KJELDE.length;i++) if (Kopla_til.getInputStream().read() != (KJELDE[i]&255)) throw new RuntimeException("TCP mismatch");
 Kopla_til.close();
 DatagramSocket endepunkt = 한국어.자체.통신.Opna(0); 한국어.자체.통신.TIMEOUT(endepunkt, 500);
 한국어.자체.통신.sende(endepunkt, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(endepunkt).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 endepunkt.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(spegle_rot/'build/java-library/classes'),'-d',str(forretningsmål_data),str(통신원문)])
                fil_Overfør_kontakt.storbinary('STOR 바깥통신.class', io.BytesIO((forretningsmål_data/'바깥통신.class').read_bytes()))
                Tekst = grensesnitt('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            validering_rapport['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            fil_Overfør_kontakt.delete('바깥통신.class')
            tenar_kjelde=forretningsmål_data/'서버시험.java'
            tenar_kjelde.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket tenar_VALUE = new ServerSocket(9300); DatagramSocket endepunkt = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gjest_VALUE = tenar_VALUE.accept();
  gjest_VALUE.getOutputStream().write(gjest_VALUE.getInputStream().read()+1); gjest_VALUE.close(); tenar_VALUE.close();
  byte[] Innhald_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Innhald_VALUE, Innhald_VALUE.length); endepunkt.receive(전문);
  endepunkt.send(전문); endepunkt.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(forretningsmål_data),str(tenar_kjelde)])
            fil_Overfør_kontakt.storbinary('STOR 서버시험.class',io.BytesIO((forretningsmål_data/'서버시험.class').read_bytes()))
            Prosess.stdin.write('java 서버시험\n'.encode());Prosess.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',tenar_Stream_port),timeout=5) as node_VALUE_6a3b6fa7:
                node_VALUE_6a3b6fa7.sendall(b'A');assert node_VALUE_6a3b6fa7.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as node_VALUE_6a3b6fa7:
                node_VALUE_6a3b6fa7.settimeout(5);node_VALUE_6a3b6fa7.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert node_VALUE_6a3b6fa7.recvfrom(512)[0]==b'UDP-IN'
            Tekst=수신하기();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            validering_rapport['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            fil_Overfør_kontakt.delete('서버시험.class')
            instruksjon_SEQUENCE = 'public class 빛 { public static void main(String[] Argument) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.Utdata.수쓰기(SUM_VALUE); 한국어.자체.Fil.Skriv("aot.txt", "한글 AOT Fil 😀"); 한국어.자체.Utdata.skrive_line(한국어.자체.Fil.Les("aot.txt")); } }'
            fil_Overfør_kontakt.storbinary('STOR 빛.java', io.BytesIO(instruksjon_SEQUENCE.encode()))
            Tekst = grensesnitt('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = grensesnitt('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = grensesnitt('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fil 😀' in Tekst and 'exit 0' in Tekst, Tekst
            자체실행파일 = bytearray(); fil_Overfør_kontakt.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Tekst = grensesnitt('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); fil_Overfør_kontakt.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); fil_Overfør_kontakt.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            fil_Overfør_kontakt.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = grensesnitt('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = grensesnitt('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Fil 😀' in Tekst and 'exit 0' in Tekst, Tekst
            validering_rapport['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validering_rapport['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            statisk_kjelde=forretningsmål_data/'정적시험.java'
            statisk_kjelde.write_text('''public class 정적시험 {
 static int spegle_rot = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] Argument) {
  int[] VALUE = new int[] {spegle_rot, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(Argument[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(forretningsmål_data),str(statisk_kjelde)])
            fil_Overfør_kontakt.storbinary('STOR 정적시험.class',io.BytesIO((forretningsmål_data/'정적시험.class').read_bytes()))
            Tekst=grensesnitt('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=grensesnitt('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            fil_Overfør_kontakt.delete('정적시험.class');fil_Overfør_kontakt.delete('정적시험.elf')
            validering_rapport['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Arkiv.getvalue());손상자료[14]^=1
            fil_Overfør_kontakt.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=grensesnitt('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            validering_rapport['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            fil_Overfør_kontakt.quit(); assert 'FTP stopped' in grensesnitt('ftpd stop')
            assert not bru.FEIL, bru.FEIL
            validering_rapport.update(passed=True, frames_to_guest=bru.커널수신틀수, frames_from_guest=bru.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in veljar.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            bru.Pause_hending.set()
            Prosess.terminate()
            try: Prosess.wait(timeout=5)
            except subprocess.TimeoutExpired: Prosess.kill(); Prosess.wait()
            veljar.close(); Prosess.stdin.close(); Prosess.stdout.close()
            validering_rapport['bridge_error'] = bru.FEIL
            validering_rapport['frames_to_guest'] = bru.커널수신틀수; validering_rapport['frames_from_guest'] = bru.커널발신틀수
            (forretningsmål_data/'packets.json').write_text(json.dumps(bru.spor_LOG,indent=2)+'\n')
            (forretningsmål_data / 'serial.log').write_bytes(대화기록)
            (forretningsmål_data / 'report.json').write_text(json.dumps(validering_rapport, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Køyr_2()
