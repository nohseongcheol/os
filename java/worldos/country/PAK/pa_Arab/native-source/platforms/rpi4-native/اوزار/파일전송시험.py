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
from نیٹ_ورک_برج import نیٹ_ورک_برج
from نفاذ_کرو_حکم import 기준, حکم
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def چلاؤ():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    جواز_دہی_رپورٹ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.출력.لکھو_لائن("JAR نفاذ_کرو_حکم: " + 인수[0]); 한국어.자체.فائل.لکھو("jar.txt", "자체 کرنل_قدر فائل"); 한국어.자체.출력.لکھو_لائن(한국어.자체.فائل.읽기("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    محفوظہ = io.BytesIO()
    with zipfile.ZipFile(محفوظہ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); سرور_سٹریم_دہانہ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with نیٹ_ورک_برج(접속번호, ['tcp:{}:9300'.format(سرور_سٹریم_دہانہ), 'udp:{}:9301'.format(서버전문접속번호)], کھیچو=True) as برج:
        عمل = subprocess.Popen(حکم() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + برج.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        منتخب_کرنڑ_آلا = selectors.DefaultSelector(); منتخب_کرنڑ_آلا.register(عمل.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            کوائف = bytearray(); ختم_کرو_آف_سیٹ = time.monotonic() + 시간제한
            while 확인표시 not in کوائف:
                if time.monotonic() > ختم_کرو_آف_سیٹ or عمل.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + کوائف.decode('utf-8', 'replace'))
                for 누름값, _ in منتخب_کرنڑ_آلا.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: کوائف.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in کوائف or b'FAIL ' in کوائف: raise AssertionError(کوائف)
            return کوائف.decode('utf-8', 'replace').replace('\r\n', '\n')
        def شیل(لائن):
            عمل.stdin.write(لائن.encode() + b'\n'); عمل.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in شیل('ftpd start')
            فائل_منتقلی_کنکشن = ftplib.FTP(); فائل_منتقلی_کنکشن.encoding = 'utf-8'; فائل_منتقلی_کنکشن.connect('127.0.0.1', 접속번호, timeout=20); فائل_منتقلی_کنکشن.login()
            پے_لوڈ_کوائف = bytes(range(256)) * 32
            فائل_منتقلی_کنکشن.storbinary('STOR binary.dat', io.BytesIO(پے_لوڈ_کوائف))
            결과 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == پے_لوڈ_کوائف; assert فائل_منتقلی_کنکشن.size('binary.dat') == len(پے_لوڈ_کوائف)
            جواز_دہی_رپورٹ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            فائل_منتقلی_کنکشن.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in شیل('cat 한글.txt')
            assert '한글.txt' in فائل_منتقلی_کنکشن.nlst()
            assert dict(فائل_منتقلی_کنکشن.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            جواز_دہی_رپورٹ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: فائل_منتقلی_کنکشن.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == پے_لوڈ_کوائف
            جواز_دہی_رپورٹ['checks'].append('oversized replacement rejected; previous file preserved')
            with فائل_منتقلی_کنکشن.transfercmd('STOR pending.txt') as اپ_لوڈ_کرو_فائلاں:
                # A control command must not change the active upload's destination.
                assert فائل_منتقلی_کنکشن.size('binary.dat') == len(پے_لوڈ_کوائف)
                اپ_لوڈ_کرو_فائلاں.sendall(b'UPLOAD TARGET PRESERVED')
            assert فائل_منتقلی_کنکشن.voidresp().startswith('226')
            결과 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == پے_لوڈ_کوائف
            فائل_منتقلی_کنکشن.delete('pending.txt')
            جواز_دہی_رپورٹ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            فائل_منتقلی_کنکشن.storbinary('STOR 인사.jar', io.BytesIO(محفوظہ.getvalue()))
            متن = شیل('java -jar 인사.jar 누리')
            assert 'JAR نفاذ_کرو_حکم: 누리' in متن and '자체 کرنل_قدر فائل' in متن and 'exit 0' in متن, متن
            متن = شیل('./인사.jar 세상')
            assert 'JAR نفاذ_کرو_حکم: 세상' in متن and 'exit 0' in متن, متن
            جواز_دہی_رپورٹ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct کوائف { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct کوائف قدر = {합(10), 1.25}; if (قدر.수 != 55 || قدر.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = بنڑاؤ_فائل("cc.txt", پڑھو_لکھو | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; لکھو_فائل_کوائف(문서, 인사, sizeof(인사)-1); بند_کرو_فائل(문서); لکھو_فائل_کوائف(1, 인사, sizeof(인사)-1); return 0; }\n'
            فائل_منتقلی_کنکشن.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            متن = شیل('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = شیل('run 한글.elf'); assert 'CC NATIVE PASS' in متن and 'exit 0' in متن, متن
            assert 'CC NATIVE PASS' in شیل('cat cc.txt')
            실행파일 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            فائل_منتقلی_کنکشن.storbinary('STOR نقل_قدر.elf', io.BytesIO(실행파일)); متن = شیل('run نقل_قدر.elf'); assert 'CC NATIVE PASS' in متن and 'exit 0' in متن, متن
            فائل_منتقلی_کنکشن.storbinary('STOR نفاذ_کرو_حکم', io.BytesIO(실행파일)); متن=شیل('./نفاذ_کرو_حکم');assert 'CC NATIVE PASS' in متن and 'exit 0' in متن,متن
            فائل_منتقلی_کنکشن.storbinary('STOR ناں.txt', io.BytesIO(실행파일)); متن=شیل('./ناں.txt');assert 'CC NATIVE PASS' in متن and 'exit 0' in متن,متن
            شیل('rm نفاذ_کرو_حکم ناں.txt')
            جواز_دہی_رپورٹ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            شیل('rm binary.dat 한글.txt 한글.c 한글.elf نقل_قدر.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            فائل_منتقلی_کنکشن.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            متن=شیل('./리눅스인사');assert 'exit -8' in متن,متن
            متن=شیل('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in متن,متن
            assert 'LINUX ELF FILE IO' in شیل('cat linux.txt')
            فائل_منتقلی_کنکشن.delete('리눅스인사');فائل_منتقلی_کنکشن.delete('linux.txt')
            فائل_منتقلی_کنکشن.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in شیل('./거짓.elf');فائل_منتقلی_کنکشن.delete('거짓.elf')
            جواز_دہی_رپورٹ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket جڑو = 한국어.자체.연결통신.جڑو("10.0.2.2", Integer.parseInt(args[0]));
 جڑو.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ماخذ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ماخذ.length;i++) if (جڑو.getInputStream().read() != (ماخذ[i]&255)) throw new RuntimeException("TCP mismatch");
 جڑو.close();
 DatagramSocket 종단 = 한국어.자체.통신.بنڑاؤ(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.بھیجو(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                فائل_منتقلی_کنکشن.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                متن = شیل('java 바깥통신 {} {}'.format(되돌림서버항목.ٹرانسمشن_کنٹرول_پروٹوکول_دہانہ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in متن and '10.0.2.2' in متن and 'exit 0' in متن, متن
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            جواز_دہی_رپورٹ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            فائل_منتقلی_کنکشن.delete('바깥통신.class')
            سرور_ماخذ=결과자료/'서버시험.java'
            سرور_ماخذ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket سرور_قدر = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket مہمان_قدر = سرور_قدر.accept();
  مہمان_قدر.getOutputStream().write(مہمان_قدر.getInputStream().read()+1); مہمان_قدر.close(); سرور_قدر.close();
  byte[] اجزاء_قدر = new byte[8]; DatagramPacket 전문 = new DatagramPacket(اجزاء_قدر, اجزاء_قدر.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(سرور_ماخذ)])
            فائل_منتقلی_کنکشن.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            عمل.stdin.write('java 서버시험\n'.encode());عمل.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',سرور_سٹریم_دہانہ),timeout=5) as ہم_سر_قدر:
                ہم_سر_قدر.sendall(b'A');assert ہم_سر_قدر.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ہم_سر_قدر:
                ہم_سر_قدر.settimeout(5);ہم_سر_قدر.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ہم_سر_قدر.recvfrom(512)[0]==b'UDP-IN'
            متن=수신하기();assert 'INBOUND TCP UDP PASS' in متن and 'exit 0' in متن,متن
            جواز_دہی_رپورٹ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            فائل_منتقلی_کنکشن.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.فائل.لکھو("aot.txt", "한글 AOT فائل 😀"); 한국어.자체.출력.لکھو_لائن(한국어.자체.فائل.읽기("aot.txt")); } }'
            فائل_منتقلی_کنکشن.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            متن = شیل('javac 빛.java'); assert 'exit 0' in متن and 'Compiled:' in متن, متن
            متن = شیل('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = شیل('run 빛.elf'); assert '\n55\n' in متن and '한글 AOT فائل 😀' in متن and 'exit 0' in متن, متن
            자체실행파일 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            متن = شیل('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in متن and 'unsupported' in متن, متن
            보존자료 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); فائل_منتقلی_کنکشن.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            فائل_منتقلی_کنکشن.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            متن = شیل('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = شیل('run 빛.elf'); assert '\n55\n' in متن and '한글 AOT فائل 😀' in متن and 'exit 0' in متن, متن
            جواز_دہی_رپورٹ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            جواز_دہی_رپورٹ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ساقط_ماخذ=결과자료/'정적시험.java'
            ساقط_ماخذ.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] قدر = new int[] {기준, 합(10)};
  System.out.println(قدر[0] + قدر[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ساقط_ماخذ)])
            فائل_منتقلی_کنکشن.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            متن=شیل('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in متن,متن
            متن=شیل('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in متن,متن
            فائل_منتقلی_کنکشن.delete('정적시험.class');فائل_منتقلی_کنکشن.delete('정적시험.elf')
            جواز_دہی_رپورٹ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(محفوظہ.getvalue());손상자료[14]^=1
            فائل_منتقلی_کنکشن.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            متن=شیل('java -jar 인사.jar');assert 'Main-Class\nexit 1' in متن,متن
            جواز_دہی_رپورٹ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            فائل_منتقلی_کنکشن.quit(); assert 'FTP stopped' in شیل('ftpd stop')
            assert not برج.نقص, برج.نقص
            جواز_دہی_رپورٹ.update(passed=True, frames_to_guest=برج.커널수신틀수, frames_from_guest=برج.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in منتخب_کرنڑ_آلا.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            برج.توقف_کرو_واقعہ.set()
            عمل.terminate()
            try: عمل.wait(timeout=5)
            except subprocess.TimeoutExpired: عمل.kill(); عمل.wait()
            منتخب_کرنڑ_آلا.close(); عمل.stdin.close(); عمل.stdout.close()
            جواز_دہی_رپورٹ['bridge_error'] = برج.نقص
            جواز_دہی_رپورٹ['frames_to_guest'] = برج.커널수신틀수; جواز_دہی_رپورٹ['frames_from_guest'] = برج.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(برج.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(جواز_دہی_رپورٹ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': چلاؤ()
