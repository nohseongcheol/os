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
from نفاذ_کریں_حکم import عکس_ڈالنا_روٹ, حکم
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def چلائیں():
    پیمائش_کوائف = عکس_ڈالنا_روٹ / 'build/verification/ftp'; پیمائش_کوائف.mkdir(parents=True, exist_ok=True)
    توثیق_رپورٹ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((عکس_ڈالنا_روٹ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = پیمائش_کوائف / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] دلائل) throws Exception { اردو.اپنا.اخراج_کا_مقام.لکھیں_لائن("JAR نفاذ_کریں_حکم: " + دلائل[0]); اردو.اپنا.فائل_کا_نام.لکھیں("jar.txt", "اپنا کرنیل_قدر فائل_کا_نام"); اردو.اپنا.اخراج_کا_مقام.لکھیں_لائن(اردو.اپنا.فائل_کا_نام.پڑھیں("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(عکس_ڈالنا_روٹ/'build/java-library/classes'), '-d', str(پیمائش_کوائف), str(자바원문)])
    محفوظ = io.BytesIO()
    with zipfile.ZipFile(محفوظ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(پیمائش_کوائف/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); دہانہ_نمبر = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); سرور_بہاؤ_پورٹ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with نیٹ_ورک_برج(دہانہ_نمبر, ['tcp:{}:9300'.format(سرور_بہاؤ_پورٹ), 'udp:{}:9301'.format(서버전문접속번호)], کیپچر_کریں=True) as برج:
        عمل_کاری = subprocess.Popen(حکم() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + برج.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        منتخب_کنندہ = selectors.DefaultSelector(); منتخب_کنندہ.register(عمل_کاری.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            کوائف = bytearray(); اختتام_آفسٹ = time.monotonic() + 시간제한
            while 확인표시 not in کوائف:
                if time.monotonic() > اختتام_آفسٹ or عمل_کاری.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + کوائف.decode('utf-8', 'replace'))
                for 누름값, _ in منتخب_کنندہ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: کوائف.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in کوائف or b'FAIL ' in کوائف: raise AssertionError(کوائف)
            return کوائف.decode('utf-8', 'replace').replace('\r\n', '\n')
        def شیل(اندراج_کی_سطر):
            عمل_کاری.stdin.write(اندراج_کی_سطر.encode() + b'\n'); عمل_کاری.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in شیل('ftpd start')
            فائل_منتقلی_رابطہ = ftplib.FTP(); فائل_منتقلی_رابطہ.encoding = 'utf-8'; فائل_منتقلی_رابطہ.connect('127.0.0.1', دہانہ_نمبر, timeout=20); فائل_منتقلی_رابطہ.login()
            پے_لوڈ_کوائف = bytes(range(256)) * 32
            فائل_منتقلی_رابطہ.storbinary('STOR binary.dat', io.BytesIO(پے_لوڈ_کوائف))
            پیمائش = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR binary.dat', پیمائش.extend)
            assert پیمائش == پے_لوڈ_کوائف; assert فائل_منتقلی_رابطہ.size('binary.dat') == len(پے_لوڈ_کوائف)
            توثیق_رپورٹ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            فائل_منتقلی_رابطہ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in شیل('cat 한글.txt')
            assert '한글.txt' in فائل_منتقلی_رابطہ.nlst()
            assert dict(فائل_منتقلی_رابطہ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            توثیق_رپورٹ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: فائل_منتقلی_رابطہ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            پیمائش = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR binary.dat', پیمائش.extend); assert پیمائش == پے_لوڈ_کوائف
            توثیق_رپورٹ['checks'].append('oversized replacement rejected; previous file preserved')
            with فائل_منتقلی_رابطہ.transfercmd('STOR pending.txt') as اپ_لوڈ_کريں_فائلیں:
                # A control command must not change the active upload's destination.
                assert فائل_منتقلی_رابطہ.size('binary.dat') == len(پے_لوڈ_کوائف)
                اپ_لوڈ_کريں_فائلیں.sendall(b'UPLOAD TARGET PRESERVED')
            assert فائل_منتقلی_رابطہ.voidresp().startswith('226')
            پیمائش = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR pending.txt', پیمائش.extend)
            assert پیمائش == b'UPLOAD TARGET PRESERVED'
            پیمائش = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR binary.dat', پیمائش.extend)
            assert پیمائش == پے_لوڈ_کوائف
            فائل_منتقلی_رابطہ.delete('pending.txt')
            توثیق_رپورٹ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            فائل_منتقلی_رابطہ.storbinary('STOR 인사.jar', io.BytesIO(محفوظ.getvalue()))
            متن = شیل('java -jar 인사.jar 누리')
            assert 'JAR نفاذ_کریں_حکم: 누리' in متن and 'اپنا کرنیل_قدر فائل_کا_نام' in متن and 'exit 0' in متن, متن
            متن = شیل('./인사.jar 세상')
            assert 'JAR نفاذ_کریں_حکم: 세상' in متن and 'exit 0' in متن, متن
            توثیق_رپورٹ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct کوائف { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct کوائف قدر = {합(10), 1.25}; if (قدر.수 != 55 || قدر.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = بنائیں_فائل("cc.txt", مطالعہ_تحریری | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; لکھیں_فائل_کوائف(문서, 인사, sizeof(인사)-1); بند_فائل(문서); لکھیں_فائل_کوائف(1, 인사, sizeof(인사)-1); return 0; }\n'
            فائل_منتقلی_رابطہ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            متن = شیل('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = شیل('run 한글.elf'); assert 'CC NATIVE PASS' in متن and 'exit 0' in متن, متن
            assert 'CC NATIVE PASS' in شیل('cat cc.txt')
            실행파일 = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            فائل_منتقلی_رابطہ.storbinary('STOR نقل_قدر.elf', io.BytesIO(실행파일)); متن = شیل('run نقل_قدر.elf'); assert 'CC NATIVE PASS' in متن and 'exit 0' in متن, متن
            فائل_منتقلی_رابطہ.storbinary('STOR نفاذ_کریں_حکم', io.BytesIO(실행파일)); متن=شیل('./نفاذ_کریں_حکم');assert 'CC NATIVE PASS' in متن and 'exit 0' in متن,متن
            فائل_منتقلی_رابطہ.storbinary('STOR نام.txt', io.BytesIO(실행파일)); متن=شیل('./نام.txt');assert 'CC NATIVE PASS' in متن and 'exit 0' in متن,متن
            شیل('rm نفاذ_کریں_حکم نام.txt')
            توثیق_رپورٹ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            شیل('rm binary.dat 한글.txt 한글.c 한글.elf نقل_قدر.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(پیمائش_کوائف/'linux-reference')
            فائل_منتقلی_رابطہ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            متن=شیل('./리눅스인사');assert 'exit -8' in متن,متن
            متن=شیل('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in متن,متن
            assert 'LINUX ELF FILE IO' in شیل('cat linux.txt')
            فائل_منتقلی_رابطہ.delete('리눅스인사');فائل_منتقلی_رابطہ.delete('linux.txt')
            فائل_منتقلی_رابطہ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in شیل('./거짓.elf');فائل_منتقلی_رابطہ.delete('거짓.elf')
            توثیق_رپورٹ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = پیمائش_کوائف/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket متصل_ہوں = اردو.اپنا.연결통신.متصل_ہوں("10.0.2.2", Integer.parseInt(args[0]));
 متصل_ہوں.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ماخذ_فائل = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ماخذ_فائل.length;i++) if (متصل_ہوں.getInputStream().read() != (ماخذ_فائل[i]&255)) throw new RuntimeException("TCP mismatch");
 متصل_ہوں.close();
 DatagramSocket 종단 = اردو.اپنا.통신.کھولیں(0); اردو.اپنا.통신.ٹائم_آؤٹ(종단, 500);
 اردو.اپنا.통신.بھیجیں(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!اردو.اپنا.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(عکس_ڈالنا_روٹ/'build/java-library/classes'),'-d',str(پیمائش_کوائف),str(통신원문)])
                فائل_منتقلی_رابطہ.storbinary('STOR 바깥통신.class', io.BytesIO((پیمائش_کوائف/'바깥통신.class').read_bytes()))
                متن = شیل('java 바깥통신 {} {}'.format(되돌림서버항목.ٹرانسمشن_کنٹرول_پروٹوکول_پورٹ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in متن and '10.0.2.2' in متن and 'exit 0' in متن, متن
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            توثیق_رپورٹ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            فائل_منتقلی_رابطہ.delete('바깥통신.class')
            سرور_ماخذ=پیمائش_کوائف/'서버시험.java'
            سرور_ماخذ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket سرور_قدر = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket مہمان_قدر = سرور_قدر.accept();
  مہمان_قدر.getOutputStream().write(مہمان_قدر.getInputStream().read()+1); مہمان_قدر.close(); سرور_قدر.close();
  byte[] مشمول_قدر = new byte[8]; DatagramPacket 전문 = new DatagramPacket(مشمول_قدر, مشمول_قدر.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(پیمائش_کوائف),str(سرور_ماخذ)])
            فائل_منتقلی_رابطہ.storbinary('STOR 서버시험.class',io.BytesIO((پیمائش_کوائف/'서버시험.class').read_bytes()))
            عمل_کاری.stdin.write('java 서버시험\n'.encode());عمل_کاری.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',سرور_بہاؤ_پورٹ),timeout=5) as ساتھی_قدر:
                ساتھی_قدر.sendall(b'A');assert ساتھی_قدر.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ساتھی_قدر:
                ساتھی_قدر.settimeout(5);ساتھی_قدر.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ساتھی_قدر.recvfrom(512)[0]==b'UDP-IN'
            متن=수신하기();assert 'INBOUND TCP UDP PASS' in متن and 'exit 0' in متن,متن
            توثیق_رپورٹ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            فائل_منتقلی_رابطہ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] دلائل) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } اردو.اپنا.اخراج_کا_مقام.수쓰기(합); اردو.اپنا.فائل_کا_نام.لکھیں("aot.txt", "한글 AOT فائل_کا_نام 😀"); اردو.اپنا.اخراج_کا_مقام.لکھیں_لائن(اردو.اپنا.فائل_کا_نام.پڑھیں("aot.txt")); } }'
            فائل_منتقلی_رابطہ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            متن = شیل('javac 빛.java'); assert 'exit 0' in متن and 'Compiled:' in متن, متن
            متن = شیل('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = شیل('run 빛.elf'); assert '\n55\n' in متن and '한글 AOT فائل_کا_نام 😀' in متن and 'exit 0' in متن, متن
            자체실행파일 = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            متن = شیل('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in متن and 'unsupported' in متن, متن
            보존자료 = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); فائل_منتقلی_رابطہ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            فائل_منتقلی_رابطہ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            متن = شیل('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = شیل('run 빛.elf'); assert '\n55\n' in متن and '한글 AOT فائل_کا_نام 😀' in متن and 'exit 0' in متن, متن
            توثیق_رپورٹ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            توثیق_رپورٹ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            جامد_ماخذ=پیمائش_کوائف/'정적시험.java'
            جامد_ماخذ.write_text('''public class 정적시험 {
 static int عکس_ڈالنا_روٹ = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] دلائل) {
  int[] قدر = new int[] {عکس_ڈالنا_روٹ, 합(10)};
  System.out.println(قدر[0] + قدر[1]); System.out.println(دلائل[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(پیمائش_کوائف),str(جامد_ماخذ)])
            فائل_منتقلی_رابطہ.storbinary('STOR 정적시험.class',io.BytesIO((پیمائش_کوائف/'정적시험.class').read_bytes()))
            متن=شیل('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in متن,متن
            متن=شیل('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in متن,متن
            فائل_منتقلی_رابطہ.delete('정적시험.class');فائل_منتقلی_رابطہ.delete('정적시험.elf')
            توثیق_رپورٹ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(محفوظ.getvalue());손상자료[14]^=1
            فائل_منتقلی_رابطہ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            متن=شیل('java -jar 인사.jar');assert 'Main-Class\nexit 1' in متن,متن
            توثیق_رپورٹ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            فائل_منتقلی_رابطہ.quit(); assert 'FTP stopped' in شیل('ftpd stop')
            assert not برج.غلطی, برج.غلطی
            توثیق_رپورٹ.update(passed=True, frames_to_guest=برج.커널수신틀수, frames_from_guest=برج.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in منتخب_کنندہ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            برج.توقف_ایونٹ.set()
            عمل_کاری.terminate()
            try: عمل_کاری.wait(timeout=5)
            except subprocess.TimeoutExpired: عمل_کاری.kill(); عمل_کاری.wait()
            منتخب_کنندہ.close(); عمل_کاری.stdin.close(); عمل_کاری.stdout.close()
            توثیق_رپورٹ['bridge_error'] = برج.غلطی
            توثیق_رپورٹ['frames_to_guest'] = برج.커널수신틀수; توثیق_رپورٹ['frames_from_guest'] = برج.커널발신틀수
            (پیمائش_کوائف/'packets.json').write_text(json.dumps(برج.ٹریس_لاگ,indent=2)+'\n')
            (پیمائش_کوائف / 'serial.log').write_bytes(대화기록)
            (پیمائش_کوائف / 'report.json').write_text(json.dumps(توثیق_رپورٹ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': چلائیں()
