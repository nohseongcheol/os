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
from Network_bridge import Network_bridge
from Mag_execute_utos import Project_root, utos
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def run():
    sukat_data = Project_root / 'build/verification/ftp'; sukat_data.mkdir(parents=True, exist_ok=True)
    pagpapatibay_ulat = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((Project_root / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = sukat_data / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.sumulat_linya("JAR Mag_execute_utos: " + 인수[0]); 한국어.자체.file.sumulat("jar.txt", "자체 kernel_VALUE file"); 한국어.자체.출력.sumulat_linya(한국어.자체.file.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(Project_root/'build/java-library/classes'), '-d', str(sukat_data), str(자바원문)])
    Archive = io.BytesIO()
    with zipfile.ZipFile(Archive, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(sukat_data/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); numero_ng_port = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); server_Stream_port = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with Network_bridge(numero_ng_port, ['tcp:{}:9300'.format(server_Stream_port), 'udp:{}:9301'.format(서버전문접속번호)], mag_capture=True) as bridge:
        Proseso = subprocess.Popen(utos() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + bridge.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        tagapili = selectors.DefaultSelector(); tagapili.register(Proseso.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            data = bytearray(); tapusin_OFFSET = time.monotonic() + 시간제한
            while 확인표시 not in data:
                if time.monotonic() > tapusin_OFFSET or Proseso.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + data.decode('utf-8', 'replace'))
                for 누름값, _ in tagapili.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: data.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in data or b'FAIL ' in data: raise AssertionError(data)
            return data.decode('utf-8', 'replace').replace('\r\n', '\n')
        def shell(linya):
            Proseso.stdin.write(linya.encode() + b'\n'); Proseso.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in shell('ftpd start')
            file_lipat_koneksyon = ftplib.FTP(); file_lipat_koneksyon.encoding = 'utf-8'; file_lipat_koneksyon.connect('127.0.0.1', numero_ng_port, timeout=20); file_lipat_koneksyon.login()
            payload_data = bytes(range(256)) * 32
            file_lipat_koneksyon.storbinary('STOR binary.dat', io.BytesIO(payload_data))
            sukat = bytearray(); file_lipat_koneksyon.retrbinary('RETR binary.dat', sukat.extend)
            assert sukat == payload_data; assert file_lipat_koneksyon.size('binary.dat') == len(payload_data)
            pagpapatibay_ulat['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            file_lipat_koneksyon.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in shell('cat 한글.txt')
            assert '한글.txt' in file_lipat_koneksyon.nlst()
            assert dict(file_lipat_koneksyon.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            pagpapatibay_ulat['checks'].append('UTF-8 filename and content visible in guest shell')
            try: file_lipat_koneksyon.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            sukat = bytearray(); file_lipat_koneksyon.retrbinary('RETR binary.dat', sukat.extend); assert sukat == payload_data
            pagpapatibay_ulat['checks'].append('oversized replacement rejected; previous file preserved')
            with file_lipat_koneksyon.transfercmd('STOR pending.txt') as upload_Mga_File:
                # A control command must not change the active upload's destination.
                assert file_lipat_koneksyon.size('binary.dat') == len(payload_data)
                upload_Mga_File.sendall(b'UPLOAD TARGET PRESERVED')
            assert file_lipat_koneksyon.voidresp().startswith('226')
            sukat = bytearray(); file_lipat_koneksyon.retrbinary('RETR pending.txt', sukat.extend)
            assert sukat == b'UPLOAD TARGET PRESERVED'
            sukat = bytearray(); file_lipat_koneksyon.retrbinary('RETR binary.dat', sukat.extend)
            assert sukat == payload_data
            file_lipat_koneksyon.delete('pending.txt')
            pagpapatibay_ulat['checks'].append('interleaved SIZE cannot change the active STOR destination')
            file_lipat_koneksyon.storbinary('STOR 인사.jar', io.BytesIO(Archive.getvalue()))
            SMS = shell('java -jar 인사.jar 누리')
            assert 'JAR Mag_execute_utos: 누리' in SMS and '자체 kernel_VALUE file' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('./인사.jar 세상')
            assert 'JAR Mag_execute_utos: 세상' in SMS and 'exit 0' in SMS, SMS
            pagpapatibay_ulat['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct data { int 수; double 비율; };\nint SUM_VALUE(int n) { return n ? n + SUM_VALUE(n-1) : 0; }\nint main(void) { struct data VALUE = {SUM_VALUE(10), 1.25}; if (VALUE.수 != 55 || VALUE.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = buksan_file("cc.txt", nababasa_nasusulatan | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; sumulat_file_data(문서, 인사, sizeof(인사)-1); isara_file(문서); sumulat_file_data(1, 인사, sizeof(인사)-1); return 0; }\n'
            file_lipat_koneksyon.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            SMS = shell('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 한글.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            assert 'CC NATIVE PASS' in shell('cat cc.txt')
            실행파일 = bytearray(); file_lipat_koneksyon.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            file_lipat_koneksyon.storbinary('STOR gumawa_ng_kopya_VALUE.elf', io.BytesIO(실행파일)); SMS = shell('run gumawa_ng_kopya_VALUE.elf'); assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS, SMS
            file_lipat_koneksyon.storbinary('STOR Mag_execute_utos', io.BytesIO(실행파일)); SMS=shell('./Mag_execute_utos');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            file_lipat_koneksyon.storbinary('STOR pangalan.txt', io.BytesIO(실행파일)); SMS=shell('./pangalan.txt');assert 'CC NATIVE PASS' in SMS and 'exit 0' in SMS,SMS
            shell('rm Mag_execute_utos pangalan.txt')
            pagpapatibay_ulat['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            shell('rm binary.dat 한글.txt 한글.c 한글.elf gumawa_ng_kopya_VALUE.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(sukat_data/'linux-reference')
            file_lipat_koneksyon.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            SMS=shell('./리눅스인사');assert 'exit -8' in SMS,SMS
            SMS=shell('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in SMS,SMS
            assert 'LINUX ELF FILE IO' in shell('cat linux.txt')
            file_lipat_koneksyon.delete('리눅스인사');file_lipat_koneksyon.delete('linux.txt')
            file_lipat_koneksyon.storbinary('STOR FALSE_VALUE.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in shell('./FALSE_VALUE.elf');file_lipat_koneksyon.delete('FALSE_VALUE.elf')
            pagpapatibay_ulat['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = sukat_data/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket CONNECT = 한국어.자체.연결통신.CONNECT("10.0.2.2", Integer.parseInt(args[0]));
 CONNECT.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] pinagmulan = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<pinagmulan.length;i++) if (CONNECT.getInputStream().read() != (pinagmulan[i]&255)) throw new RuntimeException("TCP mismatch");
 CONNECT.close();
 DatagramSocket 종단 = 한국어.자체.통신.buksan(0); 한국어.자체.통신.TIMEOUT(종단, 500);
 한국어.자체.통신.i_email(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(Project_root/'build/java-library/classes'),'-d',str(sukat_data),str(통신원문)])
                file_lipat_koneksyon.storbinary('STOR 바깥통신.class', io.BytesIO((sukat_data/'바깥통신.class').read_bytes()))
                SMS = shell('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_port, 되돌림서버항목.UDP_port))
                assert 'EXTERNAL TCP UDP PASS' in SMS and '10.0.2.2' in SMS and 'exit 0' in SMS, SMS
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            pagpapatibay_ulat['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            file_lipat_koneksyon.delete('바깥통신.class')
            server_pinagmulan=sukat_data/'서버시험.java'
            server_pinagmulan.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket server_VALUE = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket bisita_VALUE = server_VALUE.accept();
  bisita_VALUE.getOutputStream().write(bisita_VALUE.getInputStream().read()+1); bisita_VALUE.close(); server_VALUE.close();
  byte[] Nilalaman_VALUE = new byte[8]; DatagramPacket 전문 = new DatagramPacket(Nilalaman_VALUE, Nilalaman_VALUE.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(sukat_data),str(server_pinagmulan)])
            file_lipat_koneksyon.storbinary('STOR 서버시험.class',io.BytesIO((sukat_data/'서버시험.class').read_bytes()))
            Proseso.stdin.write('java 서버시험\n'.encode());Proseso.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',server_Stream_port),timeout=5) as peer_VALUE:
                peer_VALUE.sendall(b'A');assert peer_VALUE.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as peer_VALUE:
                peer_VALUE.settimeout(5);peer_VALUE.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert peer_VALUE.recvfrom(512)[0]==b'UDP-IN'
            SMS=수신하기();assert 'INBOUND TCP UDP PASS' in SMS and 'exit 0' in SMS,SMS
            pagpapatibay_ulat['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            file_lipat_koneksyon.delete('서버시험.class')
            instruksiyon_SEQUENCE = 'public class 빛 { public static void main(String[] 인수) throws Exception { int SUM_VALUE = 0; int 수 = 1; while (수 <= 10) { SUM_VALUE = SUM_VALUE + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(SUM_VALUE); 한국어.자체.file.sumulat("aot.txt", "한글 AOT file 😀"); 한국어.자체.출력.sumulat_linya(한국어.자체.file.읽기("aot.txt")); } }'
            file_lipat_koneksyon.storbinary('STOR 빛.java', io.BytesIO(instruksiyon_SEQUENCE.encode()))
            SMS = shell('javac 빛.java'); assert 'exit 0' in SMS and 'Compiled:' in SMS, SMS
            SMS = shell('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT file 😀' in SMS and 'exit 0' in SMS, SMS
            자체실행파일 = bytearray(); file_lipat_koneksyon.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            SMS = shell('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in SMS and 'unsupported' in SMS, SMS
            보존자료 = bytearray(); file_lipat_koneksyon.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); file_lipat_koneksyon.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            file_lipat_koneksyon.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            SMS = shell('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in SMS and 'exit 0' in SMS, SMS
            SMS = shell('run 빛.elf'); assert '\n55\n' in SMS and '한글 AOT file 😀' in SMS and 'exit 0' in SMS, SMS
            pagpapatibay_ulat['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            pagpapatibay_ulat['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            hindi_nababago_pinagmulan=sukat_data/'정적시험.java'
            hindi_nababago_pinagmulan.write_text('''public class 정적시험 {
 static int Project_root = 3;
 static int SUM_VALUE(int n) { return n == 0 ? 0 : n + SUM_VALUE(n-1); }
 public static void main(String[] 인수) {
  int[] VALUE = new int[] {Project_root, SUM_VALUE(10)};
  System.out.println(VALUE[0] + VALUE[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(sukat_data),str(hindi_nababago_pinagmulan)])
            file_lipat_koneksyon.storbinary('STOR 정적시험.class',io.BytesIO((sukat_data/'정적시험.class').read_bytes()))
            SMS=shell('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in SMS,SMS
            SMS=shell('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in SMS,SMS
            file_lipat_koneksyon.delete('정적시험.class');file_lipat_koneksyon.delete('정적시험.elf')
            pagpapatibay_ulat['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(Archive.getvalue());손상자료[14]^=1
            file_lipat_koneksyon.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            SMS=shell('java -jar 인사.jar');assert 'Main-Class\nexit 1' in SMS,SMS
            pagpapatibay_ulat['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            file_lipat_koneksyon.quit(); assert 'FTP stopped' in shell('ftpd stop')
            assert not bridge.error, bridge.error
            pagpapatibay_ulat.update(passed=True, frames_to_guest=bridge.커널수신틀수, frames_from_guest=bridge.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in tagapili.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            bridge.panadaliang_ihinto_kaganapan.set()
            Proseso.terminate()
            try: Proseso.wait(timeout=5)
            except subprocess.TimeoutExpired: Proseso.kill(); Proseso.wait()
            tagapili.close(); Proseso.stdin.close(); Proseso.stdout.close()
            pagpapatibay_ulat['bridge_error'] = bridge.error
            pagpapatibay_ulat['frames_to_guest'] = bridge.커널수신틀수; pagpapatibay_ulat['frames_from_guest'] = bridge.커널발신틀수
            (sukat_data/'packets.json').write_text(json.dumps(bridge.trace_LOG,indent=2)+'\n')
            (sukat_data / 'serial.log').write_bytes(대화기록)
            (sukat_data / 'report.json').write_text(json.dumps(pagpapatibay_ulat, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': run()
