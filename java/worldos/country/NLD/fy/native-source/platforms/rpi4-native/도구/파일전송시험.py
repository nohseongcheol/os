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
from 통신다리 import 통신다리
from 실행 import 기준, Kommando
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def Start():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    검증기록 = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] Arguminten) throws Exception { 한국어.자체.출력.줄쓰기("JAR 실행: " + Arguminten[0]); 한국어.자체.Bestân.Skriuwe("jar.txt", "자체 커널 Bestân"); 한국어.자체.출력.줄쓰기(한국어.자체.Bestân.Lêze("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    압축꾸러미 = io.BytesIO()
    with zipfile.ZipFile(압축꾸러미, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버연결접속번호 = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(서버연결접속번호), 'udp:{}:9301'.format(서버전문접속번호)], 포착여부=True) as 연결다리:
        실행과정 = subprocess.Popen(Kommando() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        준비선택기 = selectors.DefaultSelector(); 준비선택기.register(실행과정.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            자료 = bytearray(); 끝위치 = time.monotonic() + 시간제한
            while 확인표시 not in 자료:
                if time.monotonic() > 끝위치 or 실행과정.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + 자료.decode('utf-8', 'replace'))
                for 누름값, _ in 준비선택기.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: 자료.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in 자료 or b'FAIL ' in 자료: raise AssertionError(자료)
            return 자료.decode('utf-8', 'replace').replace('\r\n', '\n')
        def 셸(줄):
            실행과정.stdin.write(줄.encode() + b'\n'); 실행과정.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in 셸('ftpd start')
            파일전송접속 = ftplib.FTP(); 파일전송접속.encoding = 'utf-8'; 파일전송접속.connect('127.0.0.1', 접속번호, timeout=20); 파일전송접속.login()
            내용자료 = bytes(range(256)) * 32
            파일전송접속.storbinary('STOR binary.dat', io.BytesIO(내용자료))
            결과 = bytearray(); 파일전송접속.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료; assert 파일전송접속.size('binary.dat') == len(내용자료)
            검증기록['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            파일전송접속.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in 셸('cat 한글.txt')
            assert '한글.txt' in 파일전송접속.nlst()
            assert dict(파일전송접속.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            검증기록['checks'].append('UTF-8 filename and content visible in guest shell')
            try: 파일전송접속.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); 파일전송접속.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == 내용자료
            검증기록['checks'].append('oversized replacement rejected; previous file preserved')
            with 파일전송접속.transfercmd('STOR pending.txt') as 올리기:
                # A control command must not change the active upload's destination.
                assert 파일전송접속.size('binary.dat') == len(내용자료)
                올리기.sendall(b'UPLOAD TARGET PRESERVED')
            assert 파일전송접속.voidresp().startswith('226')
            결과 = bytearray(); 파일전송접속.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); 파일전송접속.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == 내용자료
            파일전송접속.delete('pending.txt')
            검증기록['checks'].append('interleaved SIZE cannot change the active STOR destination')
            파일전송접속.storbinary('STOR 인사.jar', io.BytesIO(압축꾸러미.getvalue()))
            Tekst = 셸('java -jar 인사.jar 누리')
            assert 'JAR 실행: 누리' in Tekst and '자체 커널 Bestân' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = 셸('./인사.jar 세상')
            assert 'JAR 실행: 세상' in Tekst and 'exit 0' in Tekst, Tekst
            검증기록['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct 자료 { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct 자료 값 = {합(10), 1.25}; if (값.수 != 55 || 값.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = 파일열기("cc.txt", 읽고쓰기 | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; 파일자료쓰기(문서, 인사, sizeof(인사)-1); 파일닫기(문서); 파일자료쓰기(1, 인사, sizeof(인사)-1); return 0; }\n'
            파일전송접속.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            Tekst = 셸('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = 셸('run 한글.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            assert 'CC NATIVE PASS' in 셸('cat cc.txt')
            실행파일 = bytearray(); 파일전송접속.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            파일전송접속.storbinary('STOR 복사.elf', io.BytesIO(실행파일)); Tekst = 셸('run 복사.elf'); assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst, Tekst
            파일전송접속.storbinary('STOR 실행', io.BytesIO(실행파일)); Tekst=셸('./실행');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            파일전송접속.storbinary('STOR Namme.txt', io.BytesIO(실행파일)); Tekst=셸('./Namme.txt');assert 'CC NATIVE PASS' in Tekst and 'exit 0' in Tekst,Tekst
            셸('rm 실행 Namme.txt')
            검증기록['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            셸('rm binary.dat 한글.txt 한글.c 한글.elf 복사.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            파일전송접속.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            Tekst=셸('./리눅스인사');assert 'exit -8' in Tekst,Tekst
            Tekst=셸('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in Tekst,Tekst
            assert 'LINUX ELF FILE IO' in 셸('cat linux.txt')
            파일전송접속.delete('리눅스인사');파일전송접속.delete('linux.txt')
            파일전송접속.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in 셸('./거짓.elf');파일전송접속.delete('거짓.elf')
            검증기록['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket 연결 = 한국어.자체.연결통신.연결("10.0.2.2", Integer.parseInt(args[0]));
 연결.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] 원문 = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<원문.length;i++) if (연결.getInputStream().read() != (원문[i]&255)) throw new RuntimeException("TCP mismatch");
 연결.close();
 DatagramSocket 종단 = 한국어.자체.통신.Iepenje(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.보내기(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                파일전송접속.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                Tekst = 셸('java 바깥통신 {} {}'.format(되돌림서버항목.연결접속번호, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in Tekst and '10.0.2.2' in Tekst and 'exit 0' in Tekst, Tekst
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            검증기록['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            파일전송접속.delete('바깥통신.class')
            서버원문=결과자료/'서버시험.java'
            서버원문.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = 서버.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); 서버.close();
  byte[] 내용 = new byte[8]; DatagramPacket 전문 = new DatagramPacket(내용, 내용.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(서버원문)])
            파일전송접속.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            실행과정.stdin.write('java 서버시험\n'.encode());실행과정.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',서버연결접속번호),timeout=5) as 상대:
                상대.sendall(b'A');assert 상대.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as 상대:
                상대.settimeout(5);상대.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert 상대.recvfrom(512)[0]==b'UDP-IN'
            Tekst=수신하기();assert 'INBOUND TCP UDP PASS' in Tekst and 'exit 0' in Tekst,Tekst
            검증기록['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            파일전송접속.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] Arguminten) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.Bestân.Skriuwe("aot.txt", "한글 AOT Bestân 😀"); 한국어.자체.출력.줄쓰기(한국어.자체.Bestân.Lêze("aot.txt")); } }'
            파일전송접속.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            Tekst = 셸('javac 빛.java'); assert 'exit 0' in Tekst and 'Compiled:' in Tekst, Tekst
            Tekst = 셸('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = 셸('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Bestân 😀' in Tekst and 'exit 0' in Tekst, Tekst
            자체실행파일 = bytearray(); 파일전송접속.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            Tekst = 셸('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in Tekst and 'unsupported' in Tekst, Tekst
            보존자료 = bytearray(); 파일전송접속.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); 파일전송접속.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            파일전송접속.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            Tekst = 셸('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in Tekst and 'exit 0' in Tekst, Tekst
            Tekst = 셸('run 빛.elf'); assert '\n55\n' in Tekst and '한글 AOT Bestân 😀' in Tekst and 'exit 0' in Tekst, Tekst
            검증기록['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            검증기록['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=결과자료/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] Arguminten) {
  int[] 값 = new int[] {기준, 합(10)};
  System.out.println(값[0] + 값[1]); System.out.println(Arguminten[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(정적원문)])
            파일전송접속.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            Tekst=셸('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in Tekst,Tekst
            Tekst=셸('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in Tekst,Tekst
            파일전송접속.delete('정적시험.class');파일전송접속.delete('정적시험.elf')
            검증기록['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(압축꾸러미.getvalue());손상자료[14]^=1
            파일전송접속.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            Tekst=셸('java -jar 인사.jar');assert 'Main-Class\nexit 1' in Tekst,Tekst
            검증기록['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            파일전송접속.quit(); assert 'FTP stopped' in 셸('ftpd stop')
            assert not 연결다리.Flater, 연결다리.Flater
            검증기록.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in 준비선택기.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.멈춤사건.set()
            실행과정.terminate()
            try: 실행과정.wait(timeout=5)
            except subprocess.TimeoutExpired: 실행과정.kill(); 실행과정.wait()
            준비선택기.close(); 실행과정.stdin.close(); 실행과정.stdout.close()
            검증기록['bridge_error'] = 연결다리.Flater
            검증기록['frames_to_guest'] = 연결다리.커널수신틀수; 검증기록['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(검증기록, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': Start()
