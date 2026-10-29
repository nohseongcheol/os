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
from شبکه_پل import شبکه_پل
from اجرا_فرمان import نمایش_دادن_جذر, فرمان
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def اجرا_2():
    سنجش_داده_ها = نمایش_دادن_جذر / 'build/verification/ftp'; سنجش_داده_ها.mkdir(parents=True, exist_ok=True)
    اعتبارسنجی_گزارش = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((نمایش_دادن_جذر / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = سنجش_داده_ها / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] نشانوندها) throws Exception { فارسی.بومی.خروجی.نوشتن_خط("JAR اجرا_فرمان: " + نشانوندها[0]); فارسی.بومی.پرونده.نوشتن("jar.txt", "بومی هسته_مقدار پرونده"); فارسی.بومی.خروجی.نوشتن_خط(فارسی.بومی.پرونده.خواندن("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(نمایش_دادن_جذر/'build/java-library/classes'), '-d', str(سنجش_داده_ها), str(자바원문)])
    آرشیو = io.BytesIO()
    with zipfile.ZipFile(آرشیو, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(سنجش_داده_ها/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); شماره_درگاه = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); سرور_جریان_تبدیل = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with شبکه_پل(شماره_درگاه, ['tcp:{}:9300'.format(سرور_جریان_تبدیل), 'udp:{}:9301'.format(서버전문접속번호)], ضبط_کردن=True) as پل:
        فرآیند = subprocess.Popen(فرمان() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + پل.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        انتخاب_کننده = selectors.DefaultSelector(); انتخاب_کننده.register(فرآیند.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            داده_ها = bytearray(); پایان_دادن_جابجایی_لایه_ای = time.monotonic() + 시간제한
            while 확인표시 not in داده_ها:
                if time.monotonic() > پایان_دادن_جابجایی_لایه_ای or فرآیند.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + داده_ها.decode('utf-8', 'replace'))
                for 누름값, _ in انتخاب_کننده.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: داده_ها.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in داده_ها or b'FAIL ' in داده_ها: raise AssertionError(داده_ها)
            return داده_ها.decode('utf-8', 'replace').replace('\r\n', '\n')
        def واسط(خط):
            فرآیند.stdin.write(خط.encode() + b'\n'); فرآیند.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in واسط('ftpd start')
            فایل_انتقال_اتصال = ftplib.FTP(); فایل_انتقال_اتصال.encoding = 'utf-8'; فایل_انتقال_اتصال.connect('127.0.0.1', شماره_درگاه, timeout=20); فایل_انتقال_اتصال.login()
            داده_های_ضروری_داده_ها = bytes(range(256)) * 32
            فایل_انتقال_اتصال.storbinary('STOR binary.dat', io.BytesIO(داده_های_ضروری_داده_ها))
            سنجش = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR binary.dat', سنجش.extend)
            assert سنجش == داده_های_ضروری_داده_ها; assert فایل_انتقال_اتصال.size('binary.dat') == len(داده_های_ضروری_داده_ها)
            اعتبارسنجی_گزارش['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            فایل_انتقال_اتصال.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in واسط('cat 한글.txt')
            assert '한글.txt' in فایل_انتقال_اتصال.nlst()
            assert dict(فایل_انتقال_اتصال.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            اعتبارسنجی_گزارش['checks'].append('UTF-8 filename and content visible in guest shell')
            try: فایل_انتقال_اتصال.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            سنجش = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR binary.dat', سنجش.extend); assert سنجش == داده_های_ضروری_داده_ها
            اعتبارسنجی_گزارش['checks'].append('oversized replacement rejected; previous file preserved')
            with فایل_انتقال_اتصال.transfercmd('STOR pending.txt') as آپلود_فایل:
                # A control command must not change the active upload's destination.
                assert فایل_انتقال_اتصال.size('binary.dat') == len(داده_های_ضروری_داده_ها)
                آپلود_فایل.sendall(b'UPLOAD TARGET PRESERVED')
            assert فایل_انتقال_اتصال.voidresp().startswith('226')
            سنجش = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR pending.txt', سنجش.extend)
            assert سنجش == b'UPLOAD TARGET PRESERVED'
            سنجش = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR binary.dat', سنجش.extend)
            assert سنجش == داده_های_ضروری_داده_ها
            فایل_انتقال_اتصال.delete('pending.txt')
            اعتبارسنجی_گزارش['checks'].append('interleaved SIZE cannot change the active STOR destination')
            فایل_انتقال_اتصال.storbinary('STOR 인사.jar', io.BytesIO(آرشیو.getvalue()))
            متن = واسط('java -jar 인사.jar 누리')
            assert 'JAR اجرا_فرمان: 누리' in متن and 'بومی هسته_مقدار پرونده' in متن and 'exit 0' in متن, متن
            متن = واسط('./인사.jar 세상')
            assert 'JAR اجرا_فرمان: 세상' in متن and 'exit 0' in متن, متن
            اعتبارسنجی_گزارش['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct داده_ها { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct داده_ها مقدار = {합(10), 1.25}; if (مقدار.수 != 55 || مقدار.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ایجاد_فایل("cc.txt", خواندن_نوشتن | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; نوشتن_فایل_داده_ها(문서, 인사, sizeof(인사)-1); بستن_فایل(문서); نوشتن_فایل_داده_ها(1, 인사, sizeof(인사)-1); return 0; }\n'
            فایل_انتقال_اتصال.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            متن = واسط('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = واسط('run 한글.elf'); assert 'CC NATIVE PASS' in متن and 'exit 0' in متن, متن
            assert 'CC NATIVE PASS' in واسط('cat cc.txt')
            실행파일 = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            فایل_انتقال_اتصال.storbinary('STOR کپی_مقدار.elf', io.BytesIO(실행파일)); متن = واسط('run کپی_مقدار.elf'); assert 'CC NATIVE PASS' in متن and 'exit 0' in متن, متن
            فایل_انتقال_اتصال.storbinary('STOR اجرا_فرمان', io.BytesIO(실행파일)); متن=واسط('./اجرا_فرمان');assert 'CC NATIVE PASS' in متن and 'exit 0' in متن,متن
            فایل_انتقال_اتصال.storbinary('STOR نام.txt', io.BytesIO(실행파일)); متن=واسط('./نام.txt');assert 'CC NATIVE PASS' in متن and 'exit 0' in متن,متن
            واسط('rm اجرا_فرمان نام.txt')
            اعتبارسنجی_گزارش['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            واسط('rm binary.dat 한글.txt 한글.c 한글.elf کپی_مقدار.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(سنجش_داده_ها/'linux-reference')
            فایل_انتقال_اتصال.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            متن=واسط('./리눅스인사');assert 'exit -8' in متن,متن
            متن=واسط('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in متن,متن
            assert 'LINUX ELF FILE IO' in واسط('cat linux.txt')
            فایل_انتقال_اتصال.delete('리눅스인사');فایل_انتقال_اتصال.delete('linux.txt')
            فایل_انتقال_اتصال.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in واسط('./거짓.elf');فایل_انتقال_اتصال.delete('거짓.elf')
            اعتبارسنجی_گزارش['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = سنجش_داده_ها/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket اتصال = فارسی.بومی.연결통신.اتصال("10.0.2.2", Integer.parseInt(args[0]));
 اتصال.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] مبداء = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<مبداء.length;i++) if (اتصال.getInputStream().read() != (مبداء[i]&255)) throw new RuntimeException("TCP mismatch");
 اتصال.close();
 DatagramSocket 종단 = فارسی.بومی.통신.باز_کردن(0); فارسی.بومی.통신.پایان_مهلت_زمانی(종단, 500);
 فارسی.بومی.통신.ارسال(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!فارسی.بومی.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(نمایش_دادن_جذر/'build/java-library/classes'),'-d',str(سنجش_داده_ها),str(통신원문)])
                فایل_انتقال_اتصال.storbinary('STOR 바깥통신.class', io.BytesIO((سنجش_داده_ها/'바깥통신.class').read_bytes()))
                متن = واسط('java 바깥통신 {} {}'.format(되돌림서버항목.پروتکل_کنترل_مخابره_تبدیل, 되돌림서버항목.پروتکل_داده_نگار_کاربر_تبدیل))
                assert 'EXTERNAL TCP UDP PASS' in متن and '10.0.2.2' in متن and 'exit 0' in متن, متن
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            اعتبارسنجی_گزارش['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            فایل_انتقال_اتصال.delete('바깥통신.class')
            سرور_منبع=سنجش_داده_ها/'서버시험.java'
            سرور_منبع.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket سرور_مقدار = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket مهمان_مقدار = سرور_مقدار.accept();
  مهمان_مقدار.getOutputStream().write(مهمان_مقدار.getInputStream().read()+1); مهمان_مقدار.close(); سرور_مقدار.close();
  byte[] محتوا_مقدار = new byte[8]; DatagramPacket 전문 = new DatagramPacket(محتوا_مقدار, محتوا_مقدار.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(سنجش_داده_ها),str(سرور_منبع)])
            فایل_انتقال_اتصال.storbinary('STOR 서버시험.class',io.BytesIO((سنجش_داده_ها/'서버시험.class').read_bytes()))
            فرآیند.stdin.write('java 서버시험\n'.encode());فرآیند.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',سرور_جریان_تبدیل),timeout=5) as مشابه_مقدار:
                مشابه_مقدار.sendall(b'A');assert مشابه_مقدار.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as مشابه_مقدار:
                مشابه_مقدار.settimeout(5);مشابه_مقدار.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert مشابه_مقدار.recvfrom(512)[0]==b'UDP-IN'
            متن=수신하기();assert 'INBOUND TCP UDP PASS' in متن and 'exit 0' in متن,متن
            اعتبارسنجی_گزارش['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            فایل_انتقال_اتصال.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] نشانوندها) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } فارسی.بومی.خروجی.수쓰기(합); فارسی.بومی.پرونده.نوشتن("aot.txt", "한글 AOT پرونده 😀"); فارسی.بومی.خروجی.نوشتن_خط(فارسی.بومی.پرونده.خواندن("aot.txt")); } }'
            فایل_انتقال_اتصال.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            متن = واسط('javac 빛.java'); assert 'exit 0' in متن and 'Compiled:' in متن, متن
            متن = واسط('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = واسط('run 빛.elf'); assert '\n55\n' in متن and '한글 AOT پرونده 😀' in متن and 'exit 0' in متن, متن
            자체실행파일 = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            متن = واسط('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in متن and 'unsupported' in متن, متن
            보존자료 = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); فایل_انتقال_اتصال.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            فایل_انتقال_اتصال.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            متن = واسط('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in متن and 'exit 0' in متن, متن
            متن = واسط('run 빛.elf'); assert '\n55\n' in متن and '한글 AOT پرونده 😀' in متن and 'exit 0' in متن, متن
            اعتبارسنجی_گزارش['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            اعتبارسنجی_گزارش['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ایستا_منبع=سنجش_داده_ها/'정적시험.java'
            ایستا_منبع.write_text('''public class 정적시험 {
 static int نمایش_دادن_جذر = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] نشانوندها) {
  int[] مقدار = new int[] {نمایش_دادن_جذر, 합(10)};
  System.out.println(مقدار[0] + مقدار[1]); System.out.println(نشانوندها[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(سنجش_داده_ها),str(ایستا_منبع)])
            فایل_انتقال_اتصال.storbinary('STOR 정적시험.class',io.BytesIO((سنجش_داده_ها/'정적시험.class').read_bytes()))
            متن=واسط('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in متن,متن
            متن=واسط('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in متن,متن
            فایل_انتقال_اتصال.delete('정적시험.class');فایل_انتقال_اتصال.delete('정적시험.elf')
            اعتبارسنجی_گزارش['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(آرشیو.getvalue());손상자료[14]^=1
            فایل_انتقال_اتصال.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            متن=واسط('java -jar 인사.jar');assert 'Main-Class\nexit 1' in متن,متن
            اعتبارسنجی_گزارش['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            فایل_انتقال_اتصال.quit(); assert 'FTP stopped' in واسط('ftpd stop')
            assert not پل.خطا, پل.خطا
            اعتبارسنجی_گزارش.update(passed=True, frames_to_guest=پل.커널수신틀수, frames_from_guest=پل.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in انتخاب_کننده.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            پل.مکث_کردن_رویداد.set()
            فرآیند.terminate()
            try: فرآیند.wait(timeout=5)
            except subprocess.TimeoutExpired: فرآیند.kill(); فرآیند.wait()
            انتخاب_کننده.close(); فرآیند.stdin.close(); فرآیند.stdout.close()
            اعتبارسنجی_گزارش['bridge_error'] = پل.خطا
            اعتبارسنجی_گزارش['frames_to_guest'] = پل.커널수신틀수; اعتبارسنجی_گزارش['frames_from_guest'] = پل.커널발신틀수
            (سنجش_داده_ها/'packets.json').write_text(json.dumps(پل.اثر_ماتریس_واقعه_نگار,indent=2)+'\n')
            (سنجش_داده_ها / 'serial.log').write_bytes(대화기록)
            (سنجش_داده_ها / 'report.json').write_text(json.dumps(اعتبارسنجی_گزارش, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': اجرا_2()
