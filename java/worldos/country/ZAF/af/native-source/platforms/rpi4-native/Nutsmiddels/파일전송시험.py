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
from Netwerk_brug import Netwerk_brug
from uitvoer_bevel import Project_wortel, Opdrag
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Loop():
    maatreël_data = Project_wortel / 'build/verification/ftp'; maatreël_data.mkdir(parents=True, exist_ok=True)
    validering_verslag = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_wortel / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = maatreël_data / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.Afvoer.skryf_lyn("JAR uitvoer_bevel: " + 인수[0]); 한국어.자체.Lêer.Skryf("jar.txt", "자체 kern_VALUE Lêer"); 한국어.자체.Afvoer.skryf_lyn(한국어.자체.Lêer.Lees("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_wortel/'build/java-library/classes'), '-d', str(maatreël_data), str(자바원문)])
    Argief = io.BytesIO()
    with zipfile.ZipFile(Argief, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(maatreël_data/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); bediener_Stream_ombou = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Netwerk_brug(접속번호, ['tcp:{}:9300'.format(bediener_Stream_ombou), 'udp:{}:9301'.format(서버전문접속번호)], lê_vas=True) as brug:
        Proses = subprocess.Popen(Opdrag() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + brug.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        selekteerder = selectors.DefaultSelector(); selekteerder.register(Proses.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); beëindig_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > beëindig_OFFSET or Proses.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in selekteerder.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def dop(lyn):
            Proses.stdin.write(lyn.encode() + b'\n'); Proses.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in dop('ftpd start')
            lêer_oordra_verbinding = ftplib.FTP(); lêer_oordra_verbinding.encoding = 'utf-8'; lêer_oordra_verbinding.connect('127.0.0.1', 접속번호, timeout=20); lêer_oordra_verbinding.login()
            lading_data = bytes(range(256)) * 32
            lêer_oordra_verbinding.storbinary('STOR binary.dat', io.BytesIO(lading_data))
            maatreël = bytearray(); lêer_oordra_verbinding.retrbinary('RETR binary.dat', maatreël.extend)
            assert maatreël == lading_data; assert lêer_oordra_verbinding.size('binary.dat') == len(lading_data)
            validering_verslag['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            lêer_oordra_verbinding.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in dop('cat 한글.txt')
            assert '한글.txt' in lêer_oordra_verbinding.nlst()
            assert dict(lêer_oordra_verbinding.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            validering_verslag['checks'].append('UTF-8 filename and content visible in guest shell')
            try: lêer_oordra_verbinding.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            maatreël = bytearray(); lêer_oordra_verbinding.retrbinary('RETR binary.dat', maatreël.extend); assert maatreël == lading_data
            validering_verslag['checks'].append('oversized replacement rejected; previous file preserved')
            with lêer_oordra_verbinding.transfercmd('STOR pending.txt') as oplaai_Lêers:
                # A control command must not change the active upload's destination.
                assert lêer_oordra_verbinding.size('binary.dat') == len(lading_data)
                oplaai_Lêers.sendall(b'UPLOAD TARGET PRESERVED')
            assert lêer_oordra_verbinding.voidresp().startswith('226')
            maatreël = bytearray(); lêer_oordra_verbinding.retrbinary('RETR pending.txt', maatreël.extend)
            assert maatreël == b'UPLOAD TARGET PRESERVED'
            maatreël = bytearray(); lêer_oordra_verbinding.retrbinary('RETR binary.dat', maatreël.extend)
            assert maatreël == lading_data
            lêer_oordra_verbinding.delete('pending.txt')
            validering_verslag['checks'].append('interleaved SIZE cannot change the active STOR destination')
            lêer_oordra_verbinding.storbinary('STOR 인사.jar', io.BytesIO(Argief.getvalue()))
            Teks = dop('java -jar 인사.jar 누리')
            assert 'JAR uitvoer_bevel: 누리' in Teks and '자체 kern_VALUE Lêer' in Teks and 'exit 0' in Teks, Teks
            Teks = dop('./인사.jar 세상')
            assert 'JAR uitvoer_bevel: 세상' in Teks and 'exit 0' in Teks, Teks
            validering_verslag['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct data VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = skep_lêer("cc.txt", lees_skryf | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; skryf_lêer_data(문서, 인사, sizeof(인사)-1); sluit_lêer(문서); skryf_lêer_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            lêer_oordra_verbinding.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Teks = dop('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Teks and 'exit 0' in Teks, Teks
            Teks = dop('run 한글.elf'); assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks, Teks
            assert 'CC NATIVE PASS' in dop('cat cc.txt')
            실행파일 = bytearray(); lêer_oordra_verbinding.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            lêer_oordra_verbinding.storbinary('STOR geval_VALUE.elf', io.BytesIO(실행파일)); Teks = dop('run geval_VALUE.elf'); assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks, Teks
            lêer_oordra_verbinding.storbinary('STOR uitvoer_bevel', io.BytesIO(실행파일)); Teks=dop('./uitvoer_bevel');assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks,Teks
            lêer_oordra_verbinding.storbinary('STOR Naam.txt', io.BytesIO(실행파일)); Teks=dop('./Naam.txt');assert 'CC NATIVE PASS' in Teks and 'exit 0' in Teks,Teks
            dop('rm uitvoer_bevel Naam.txt')
            validering_verslag['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            dop('rm binary.dat 한글.txt 한글.c 한글.elf geval_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(maatreël_data/'linux-reference')
            lêer_oordra_verbinding.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Teks=dop('./리눅스인사');assert 'exit -8' in Teks,Teks
            Teks=dop('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Teks,Teks
            assert 'LINUX ELF FILE IO' in dop('cat linux.txt')
            lêer_oordra_verbinding.delete('리눅스인사');lêer_oordra_verbinding.delete('linux.txt')
            lêer_oordra_verbinding.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in dop('./FALSE_VALUE.elf');lêer_oordra_verbinding.delete('FALSE_VALUE.elf')
            validering_verslag['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = maatreël_data/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket Koppel = 한국어.자체.연결통신.Koppel("10.0.2.2", Integer.parseInt(args[0]));
 Koppel.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] Bron = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<Bron.length;i++) if (Koppel.getInputStream().read() != (Bron[i]&255)) throw new RuntimeException("TCP mismatch");
 Koppel.close();
 DatagramSocket 종단 = 한국어.자체.통신.skep(0); 한국어.자체.통신.UITTELLING(종단, 500);
 한국어.자체.통신.e_pos(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_wortel/'build/java-library/classes'),'-d',str(maatreël_data),str(통신원문)])
                lêer_oordra_verbinding.storbinary('STOR 바깥통신.class', io.BytesIO((maatreël_data/'바깥통신.class').read_bytes()))
                Teks = dop('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_ombou, 되돌림서버항목.GDP_Gebruikersdatagramprotokol_ombou))
                assert 'EXTERNAL TCP UDP PASS' in Teks and '10.0.2.2' in Teks and 'exit 0' in Teks, Teks
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            validering_verslag['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            lêer_oordra_verbinding.delete('바깥통신.class')
            bediener_bron=maatreël_data/'서버시험.java'
            bediener_bron.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket bediener_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket gas_VALUE = bediener_VALUE.accept();
  gas_VALUE.getOutputStream().write(gas_VALUE.getInputStream().read()+1); gas_VALUE.close(); bediener_VALUE.close();
  byte[] Inhoud_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Inhoud_VALUE, Inhoud_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(maatreël_data),str(bediener_bron)])
            lêer_oordra_verbinding.storbinary('STOR 서버시험.class',io.BytesIO((maatreël_data/'서버시험.class').read_bytes()))
            Proses.stdin.write('java 서버시험\n'.encode());Proses.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',bediener_Stream_ombou),timeout=5) as portuur_VALUE:
                portuur_VALUE.sendall(b'A');assert portuur_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as portuur_VALUE:
                portuur_VALUE.settimeout(5);portuur_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert portuur_VALUE.recvfrom(512)[0]==b'UDP-IN'
            Teks=수신하기();assert 'INBOUND TCP UDP PASS' in Teks and 'exit 0' in Teks,Teks
            validering_verslag['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            lêer_oordra_verbinding.delete('서버시험.class')
            instruksie_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.Afvoer.수쓰기(SUM_VALUE); 한국어.자체.Lêer.Skryf("aot.txt", "한글 AOT Lêer 😀"); 한국어.자체.Afvoer.skryf_lyn(한국어.자체.Lêer.Lees("aot.txt")); } }'
            lêer_oordra_verbinding.storbinary('STOR 빛.java', io.BytesIO(instruksie_SEQUENCE.encode()))
            Teks = dop('javac 빛.java'); assert 'exit 0' in Teks and 'Compiled:' in Teks, Teks
            Teks = dop('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teks and 'exit 0' in Teks, Teks
            Teks = dop('run 빛.elf'); assert '\n55\n' in Teks and '한글 AOT Lêer 😀' in Teks and 'exit 0' in Teks, Teks
            자체실행파일 = bytearray(); lêer_oordra_verbinding.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Teks = dop('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Teks and 'unsupported' in Teks, Teks
            보존자료 = bytearray(); lêer_oordra_verbinding.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); lêer_oordra_verbinding.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            lêer_oordra_verbinding.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Teks = dop('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Teks and 'exit 0' in Teks, Teks
            Teks = dop('run 빛.elf'); assert '\n55\n' in Teks and '한글 AOT Lêer 😀' in Teks and 'exit 0' in Teks, Teks
            validering_verslag['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            validering_verslag['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            staties_bron=maatreël_data/'정적시험.java'
            staties_bron.write_text('''public class 정적시험 {
 static int Project_wortel = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {Project_wortel, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(maatreël_data),str(staties_bron)])
            lêer_oordra_verbinding.storbinary('STOR 정적시험.class',io.BytesIO((maatreël_data/'정적시험.class').read_bytes()))
            Teks=dop('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Teks,Teks
            Teks=dop('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Teks,Teks
            lêer_oordra_verbinding.delete('정적시험.class');lêer_oordra_verbinding.delete('정적시험.elf')
            validering_verslag['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Argief.getvalue());손상자료[14]^=1
            lêer_oordra_verbinding.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Teks=dop('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Teks,Teks
            validering_verslag['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            lêer_oordra_verbinding.quit(); assert 'FTP stopped' in dop('ftpd stop')
            assert not brug.Fout, brug.Fout
            validering_verslag.update(passed=True, frames_to_guest=brug.커널수신틀수, frames_from_guest=brug.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in selekteerder.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            brug.pouseer_gebeurtenis.set()
            Proses.terminate()
            try: Proses.wait(timeout=5)
            except subprocess.TimeoutExpired: Proses.kill(); Proses.wait()
            selekteerder.close(); Proses.stdin.close(); Proses.stdout.close()
            validering_verslag['bridge_error'] = brug.Fout
            validering_verslag['frames_to_guest'] = brug.커널수신틀수; validering_verslag['frames_from_guest'] = brug.커널발신틀수
            (maatreël_data/'packets.json').write_text(json.dumps(brug.spoor_LOG,indent=2)+'\n')
            (maatreël_data / 'serial.log').write_bytes(대화기록)
            (maatreël_data / 'report.json').write_text(json.dumps(validering_verslag, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Loop()
