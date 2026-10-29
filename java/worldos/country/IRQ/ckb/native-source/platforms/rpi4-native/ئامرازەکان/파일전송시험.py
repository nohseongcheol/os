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
from جێبەجێکردن_فەرمان import 기준, فەرمان
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ڕادان():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    ڕەواکردن_ڕاپۆرت = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.ڕایت_کردن_دێڕ("JAR جێبەجێکردن_فەرمان: " + 인수[0]); 한국어.자체.فایل.ڕایت_کردن("jar.txt", "자체 کوورەک_نرخ فایل"); 한국어.자체.출력.ڕایت_کردن_دێڕ(한국어.자체.فایل.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    ئەرشیف = io.BytesIO()
    with zipfile.ZipFile(ئەرشیف, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ڕاژەکار_Stream_دەرگا = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(접속번호, ['tcp:{}:9300'.format(ڕاژەکار_Stream_دەرگا), 'udp:{}:9301'.format(서버전문접속번호)], تۆمارکردن=True) as 연결다리:
        پرۆسە = subprocess.Popen(فەرمان() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        هەڵبژێرەر = selectors.DefaultSelector(); هەڵبژێرەر.register(پرۆسە.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            دەیتا = bytearray(); دوایی_کردن_ئۆفسێت = time.monotonic() + 시간제한
            while 확인표시 not in دەیتا:
                if time.monotonic() > دوایی_کردن_ئۆفسێت or پرۆسە.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + دەیتا.decode('utf-8', 'replace'))
                for 누름값, _ in هەڵبژێرەر.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: دەیتا.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in دەیتا or b'FAIL ' in دەیتا: raise AssertionError(دەیتا)
            return دەیتا.decode('utf-8', 'replace').replace('\r\n', '\n')
        def توێکڵ(دێڕ):
            پرۆسە.stdin.write(دێڕ.encode() + b'\n'); پرۆسە.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in توێکڵ('ftpd start')
            فایل_گواستنەوە_گرێدان = ftplib.FTP(); فایل_گواستنەوە_گرێدان.encoding = 'utf-8'; فایل_گواستنەوە_گرێدان.connect('127.0.0.1', 접속번호, timeout=20); فایل_گواستنەوە_گرێدان.login()
            بارگەى_كرێ_دەیتا = bytes(range(256)) * 32
            فایل_گواستنەوە_گرێدان.storbinary('STOR binary.dat', io.BytesIO(بارگەى_كرێ_دەیتا))
            결과 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == بارگەى_كرێ_دەیتا; assert فایل_گواستنەوە_گرێدان.size('binary.dat') == len(بارگەى_كرێ_دەیتا)
            ڕەواکردن_ڕاپۆرت['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            فایل_گواستنەوە_گرێدان.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in توێکڵ('cat 한글.txt')
            assert '한글.txt' in فایل_گواستنەوە_گرێدان.nlst()
            assert dict(فایل_گواستنەوە_گرێدان.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ڕەواکردن_ڕاپۆرت['checks'].append('UTF-8 filename and content visible in guest shell')
            try: فایل_گواستنەوە_گرێدان.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == بارگەى_كرێ_دەیتا
            ڕەواکردن_ڕاپۆرت['checks'].append('oversized replacement rejected; previous file preserved')
            with فایل_گواستنەوە_گرێدان.transfercmd('STOR pending.txt') as بار_کردن_فایله_کان:
                # A control command must not change the active upload's destination.
                assert فایل_گواستنەوە_گرێدان.size('binary.dat') == len(بارگەى_كرێ_دەیتا)
                بار_کردن_فایله_کان.sendall(b'UPLOAD TARGET PRESERVED')
            assert فایل_گواستنەوە_گرێدان.voidresp().startswith('226')
            결과 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == بارگەى_كرێ_دەیتا
            فایل_گواستنەوە_گرێدان.delete('pending.txt')
            ڕەواکردن_ڕاپۆرت['checks'].append('interleaved SIZE cannot change the active STOR destination')
            فایل_گواستنەوە_گرێدان.storbinary('STOR 인사.jar', io.BytesIO(ئەرشیف.getvalue()))
            دەق = توێکڵ('java -jar 인사.jar 누리')
            assert 'JAR جێبەجێکردن_فەرمان: 누리' in دەق and '자체 کوورەک_نرخ فایل' in دەق and 'exit 0' in دەق, دەق
            دەق = توێکڵ('./인사.jar 세상')
            assert 'JAR جێبەجێکردن_فەرمان: 세상' in دەق and 'exit 0' in دەق, دەق
            ڕەواکردن_ڕاپۆرت['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct دەیتا { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct دەیتا نرخ = {합(10), 1.25}; if (نرخ.수 != 55 || نرخ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = کردنەوە_فایل("cc.txt", خوێندن_نووسین | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ڕایت_کردن_فایل_دەیتا(문서, 인사, sizeof(인사)-1); داخستن_فایل(문서); ڕایت_کردن_فایل_دەیتا(1, 인사, sizeof(인사)-1); return 0; }\n'
            فایل_گواستنەوە_گرێدان.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            دەق = توێکڵ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in دەق and 'exit 0' in دەق, دەق
            دەق = توێکڵ('run 한글.elf'); assert 'CC NATIVE PASS' in دەق and 'exit 0' in دەق, دەق
            assert 'CC NATIVE PASS' in توێکڵ('cat cc.txt')
            실행파일 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            فایل_گواستنەوە_گرێدان.storbinary('STOR کۆپی_نرخ.elf', io.BytesIO(실행파일)); دەق = توێکڵ('run کۆپی_نرخ.elf'); assert 'CC NATIVE PASS' in دەق and 'exit 0' in دەق, دەق
            فایل_گواستنەوە_گرێدان.storbinary('STOR جێبەجێکردن_فەرمان', io.BytesIO(실행파일)); دەق=توێکڵ('./جێبەجێکردن_فەرمان');assert 'CC NATIVE PASS' in دەق and 'exit 0' in دەق,دەق
            فایل_گواستنەوە_گرێدان.storbinary('STOR ناو.txt', io.BytesIO(실행파일)); دەق=توێکڵ('./ناو.txt');assert 'CC NATIVE PASS' in دەق and 'exit 0' in دەق,دەق
            توێکڵ('rm جێبەجێکردن_فەرمان ناو.txt')
            ڕەواکردن_ڕاپۆرت['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            توێکڵ('rm binary.dat 한글.txt 한글.c 한글.elf کۆپی_نرخ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            فایل_گواستنەوە_گرێدان.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            دەق=توێکڵ('./리눅스인사');assert 'exit -8' in دەق,دەق
            دەق=توێکڵ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in دەق,دەق
            assert 'LINUX ELF FILE IO' in توێکڵ('cat linux.txt')
            فایل_گواستنەوە_گرێدان.delete('리눅스인사');فایل_گواستنەوە_گرێدان.delete('linux.txt')
            فایل_گواستنەوە_گرێدان.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in توێکڵ('./거짓.elf');فایل_گواستنەوە_گرێدان.delete('거짓.elf')
            ڕەواکردن_ڕاپۆرت['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket لكاندن = 한국어.자체.연결통신.لكاندن("10.0.2.2", Integer.parseInt(args[0]));
 لكاندن.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ژێدەر = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ژێدەر.length;i++) if (لكاندن.getInputStream().read() != (ژێدەر[i]&255)) throw new RuntimeException("TCP mismatch");
 لكاندن.close();
 DatagramSocket 종단 = 한국어.자체.통신.کردنەوە(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.ناردن(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                فایل_گواستنەوە_گرێدان.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                دەق = توێکڵ('java 바깥통신 {} {}'.format(되돌림서버항목.TCP_دەرگا, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in دەق and '10.0.2.2' in دەق and 'exit 0' in دەق, دەق
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ڕەواکردن_ڕاپۆرت['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            فایل_گواستنەوە_گرێدان.delete('바깥통신.class')
            ڕاژەکار_ژێدەر=결과자료/'서버시험.java'
            ڕاژەکار_ژێدەر.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ڕاژەکار_نرخ = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket 손님 = ڕاژەکار_نرخ.accept();
  손님.getOutputStream().write(손님.getInputStream().read()+1); 손님.close(); ڕاژەکار_نرخ.close();
  byte[] ناوەرۆک_نرخ = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ناوەرۆک_نرخ, ناوەرۆک_نرخ.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ڕاژەکار_ژێدەر)])
            فایل_گواستنەوە_گرێدان.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            پرۆسە.stdin.write('java 서버시험\n'.encode());پرۆسە.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ڕاژەکار_Stream_دەرگا),timeout=5) as هاوتا_نرخ:
                هاوتا_نرخ.sendall(b'A');assert هاوتا_نرخ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as هاوتا_نرخ:
                هاوتا_نرخ.settimeout(5);هاوتا_نرخ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert هاوتا_نرخ.recvfrom(512)[0]==b'UDP-IN'
            دەق=수신하기();assert 'INBOUND TCP UDP PASS' in دەق and 'exit 0' in دەق,دەق
            ڕەواکردن_ڕاپۆرت['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            فایل_گواستنەوە_گرێدان.delete('서버시험.class')
            ڕێنمایی_زنجیره = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.فایل.ڕایت_کردن("aot.txt", "한글 AOT فایل 😀"); 한국어.자체.출력.ڕایت_کردن_دێڕ(한국어.자체.فایل.읽기("aot.txt")); } }'
            فایل_گواستنەوە_گرێدان.storbinary('STOR 빛.java', io.BytesIO(ڕێنمایی_زنجیره.encode()))
            دەق = توێکڵ('javac 빛.java'); assert 'exit 0' in دەق and 'Compiled:' in دەق, دەق
            دەق = توێکڵ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in دەق and 'exit 0' in دەق, دەق
            دەق = توێکڵ('run 빛.elf'); assert '\n55\n' in دەق and '한글 AOT فایل 😀' in دەق and 'exit 0' in دەق, دەق
            자체실행파일 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            دەق = توێکڵ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in دەق and 'unsupported' in دەق, دەق
            보존자료 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); فایل_گواستنەوە_گرێدان.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            فایل_گواستنەوە_گرێدان.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            دەق = توێکڵ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in دەق and 'exit 0' in دەق, دەق
            دەق = توێکڵ('run 빛.elf'); assert '\n55\n' in دەق and '한글 AOT فایل 😀' in دەق and 'exit 0' in دەق, دەق
            ڕەواکردن_ڕاپۆرت['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ڕەواکردن_ڕاپۆرت['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ستاتیک_ژێدەر=결과자료/'정적시험.java'
            ستاتیک_ژێدەر.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] نرخ = new int[] {기준, 합(10)};
  System.out.println(نرخ[0] + نرخ[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ستاتیک_ژێدەر)])
            فایل_گواستنەوە_گرێدان.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            دەق=توێکڵ('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in دەق,دەق
            دەق=توێکڵ('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in دەق,دەق
            فایل_گواستنەوە_گرێدان.delete('정적시험.class');فایل_گواستنەوە_گرێدان.delete('정적시험.elf')
            ڕەواکردن_ڕاپۆرت['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ئەرشیف.getvalue());손상자료[14]^=1
            فایل_گواستنەوە_گرێدان.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            دەق=توێکڵ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in دەق,دەق
            ڕەواکردن_ڕاپۆرت['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            فایل_گواستنەوە_گرێدان.quit(); assert 'FTP stopped' in توێکڵ('ftpd stop')
            assert not 연결다리.هەڵە, 연결다리.هەڵە
            ڕەواکردن_ڕاپۆرت.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in هەڵبژێرەر.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.ڕاگرتن_پێشهات.set()
            پرۆسە.terminate()
            try: پرۆسە.wait(timeout=5)
            except subprocess.TimeoutExpired: پرۆسە.kill(); پرۆسە.wait()
            هەڵبژێرەر.close(); پرۆسە.stdin.close(); پرۆسە.stdout.close()
            ڕەواکردن_ڕاپۆرت['bridge_error'] = 연결다리.هەڵە
            ڕەواکردن_ڕاپۆرت['frames_to_guest'] = 연결다리.커널수신틀수; ڕەواکردن_ڕاپۆرت['frames_from_guest'] = 연결다리.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(연결다리.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(ڕەواکردن_ڕاپۆرت, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ڕادان()
