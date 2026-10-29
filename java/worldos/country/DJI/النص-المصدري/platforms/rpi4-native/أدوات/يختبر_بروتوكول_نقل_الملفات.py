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
from جسر_3de4fe3a import جسر_3de4fe3a
from ينفذ_أمر import يعرض_جذر, أمر
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def تشغيل():
    مقياس_بيانات = يعرض_جذر / 'build/verification/ftp'; مقياس_بيانات.mkdir(parents=True, exist_ok=True)
    التحقق_من_صحة_إبلاغ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((يعرض_جذر / 'build/kernel8.img').read_bytes()).hexdigest()}
    نسخة_مكتوبة = bytearray()
    자바원문 = مقياس_بيانات / 'يختبر_يُجمع.java'
    자바원문.write_text('public class يختبر_يُجمع { public static void main(String[] وسائط) throws Exception { العربية.ذاتي.مخرجات.كتابة_خط("JAR ينفذ_أمر: " + وسائط[0]); العربية.ذاتي.ملف.كتابة("jar.txt", "ذاتي نواة_قيمة ملف"); العربية.ذاتي.مخرجات.كتابة_خط(العربية.ذاتي.ملف.قراءة("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(يعرض_جذر/'build/java-library/classes'), '-d', str(مقياس_بيانات), str(자바원문)])
    أرشيف = io.BytesIO()
    with zipfile.ZipFile(أرشيف, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: يختبر_يُجمع\r\n\r\n')
        자바꾸러미.write(str(مقياس_بيانات/'يختبر_يُجمع.class'), 'يختبر_يُجمع.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); رقم_المنفذ = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); خادم_بث_منفذ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); خادم_مخطط_بيانات_منفذ = 임시자원.getsockname()[1]
    with جسر_3de4fe3a(رقم_المنفذ, ['tcp:{}:9300'.format(خادم_بث_منفذ), 'udp:{}:9301'.format(خادم_مخطط_بيانات_منفذ)], يسجل=True) as جسر:
        عملية = subprocess.Popen(أمر() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + جسر.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        محدد = selectors.DefaultSelector(); محدد.register(عملية.stdout, selectors.EVENT_READ)
        def يستلم_رسالة(علامة=b'jkoros-native> ', 시간제한=60):
            بيانات = bytearray(); إنهاء_مكالمة_إزاحة = time.monotonic() + 시간제한
            while علامة not in بيانات:
                if time.monotonic() > إنهاء_مكالمة_إزاحة or عملية.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + بيانات.decode('utf-8', 'replace'))
                for 누름값, _ in محدد.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: بيانات.extend(조각); نسخة_مكتوبة.extend(조각)
                if b'PANIC:' in بيانات or b'FAIL ' in بيانات: raise AssertionError(بيانات)
            return بيانات.decode('utf-8', 'replace').replace('\r\n', '\n')
        def 셸(سطر):
            عملية.stdin.write(سطر.encode() + b'\n'); عملية.stdin.flush(); return يستلم_رسالة()
        try:
            يستلم_رسالة(); assert 'FTP listening' in 셸('ftpd start')
            نقل_الملفات_صديق = ftplib.FTP(); نقل_الملفات_صديق.encoding = 'utf-8'; نقل_الملفات_صديق.connect('127.0.0.1', رقم_المنفذ, timeout=20); نقل_الملفات_صديق.login()
            حمولة_بيانات = bytes(range(256)) * 32
            نقل_الملفات_صديق.storbinary('STOR binary.dat', io.BytesIO(حمولة_بيانات))
            نتيجة = bytearray(); نقل_الملفات_صديق.retrbinary('RETR binary.dat', نتيجة.extend)
            assert نتيجة == حمولة_بيانات; assert نقل_الملفات_صديق.size('binary.dat') == len(حمولة_بيانات)
            التحقق_من_صحة_إبلاغ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            نقل_الملفات_صديق.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in 셸('cat 한글.txt')
            assert '한글.txt' in نقل_الملفات_صديق.nlst()
            assert dict(نقل_الملفات_صديق.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            التحقق_من_صحة_إبلاغ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: نقل_الملفات_صديق.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            نتيجة = bytearray(); نقل_الملفات_صديق.retrbinary('RETR binary.dat', نتيجة.extend); assert نتيجة == حمولة_بيانات
            التحقق_من_صحة_إبلاغ['checks'].append('oversized replacement rejected; previous file preserved')
            with نقل_الملفات_صديق.transfercmd('STOR pending.txt') as تحميل_الملفات:
                # A control command must not change the active upload's destination.
                assert نقل_الملفات_صديق.size('binary.dat') == len(حمولة_بيانات)
                تحميل_الملفات.sendall(b'UPLOAD TARGET PRESERVED')
            assert نقل_الملفات_صديق.voidresp().startswith('226')
            نتيجة = bytearray(); نقل_الملفات_صديق.retrbinary('RETR pending.txt', نتيجة.extend)
            assert نتيجة == b'UPLOAD TARGET PRESERVED'
            نتيجة = bytearray(); نقل_الملفات_صديق.retrbinary('RETR binary.dat', نتيجة.extend)
            assert نتيجة == حمولة_بيانات
            نقل_الملفات_صديق.delete('pending.txt')
            التحقق_من_صحة_إبلاغ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            نقل_الملفات_صديق.storbinary('STOR 인사.jar', io.BytesIO(أرشيف.getvalue()))
            نص = 셸('java -jar 인사.jar 누리')
            assert 'JAR ينفذ_أمر: 누리' in نص and 'ذاتي نواة_قيمة ملف' in نص and 'exit 0' in نص, نص
            نص = 셸('./인사.jar 세상')
            assert 'JAR ينفذ_أمر: 세상' in نص and 'exit 0' in نص, نص
            التحقق_من_صحة_إبلاغ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct بيانات { int رقم; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct بيانات قيمة = {합(10), 1.25}; if (قيمة.رقم != 55 || قيمة.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = فتح_ملف("cc.txt", مقروء_مكتوب | 없으면만들기 | يقتطع_المحتويات, 0600); if (문서 < 0) return 1; كتابة_ملف_بيانات(문서, 인사, sizeof(인사)-1); يغلق_ملف(문서); كتابة_ملف_بيانات(1, 인사, sizeof(인사)-1); return 0; }\n'
            نقل_الملفات_صديق.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            نص = 셸('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in نص and 'exit 0' in نص, نص
            نص = 셸('run 한글.elf'); assert 'CC NATIVE PASS' in نص and 'exit 0' in نص, نص
            assert 'CC NATIVE PASS' in 셸('cat cc.txt')
            실행파일 = bytearray(); نقل_الملفات_صديق.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            نقل_الملفات_صديق.storbinary('STOR مثيل_قيمة.elf', io.BytesIO(실행파일)); نص = 셸('run مثيل_قيمة.elf'); assert 'CC NATIVE PASS' in نص and 'exit 0' in نص, نص
            نقل_الملفات_صديق.storbinary('STOR ينفذ_أمر', io.BytesIO(실행파일)); نص=셸('./ينفذ_أمر');assert 'CC NATIVE PASS' in نص and 'exit 0' in نص,نص
            نقل_الملفات_صديق.storbinary('STOR اسم.txt', io.BytesIO(실행파일)); نص=셸('./اسم.txt');assert 'CC NATIVE PASS' in نص and 'exit 0' in نص,نص
            셸('rm ينفذ_أمر اسم.txt')
            التحقق_من_صحة_إبلاغ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            셸('rm binary.dat 한글.txt 한글.c 한글.elf مثيل_قيمة.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(مقياس_بيانات/'linux-reference')
            نقل_الملفات_صديق.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            نص=셸('./리눅스인사');assert 'exit -8' in نص,نص
            نص=셸('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in نص,نص
            assert 'LINUX ELF FILE IO' in 셸('cat linux.txt')
            نقل_الملفات_صديق.delete('리눅스인사');نقل_الملفات_صديق.delete('linux.txt')
            نقل_الملفات_صديق.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 رقم 없습니다:' in 셸('./거짓.elf');نقل_الملفات_صديق.delete('거짓.elf')
            التحقق_من_صحة_إبلاغ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as ارتداد_خادم_إدخال:
                صافي_مصدر = مقياس_بيانات/'바깥통신.java'
                صافي_مصدر.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket اتصال = العربية.ذاتي.صديق_نقل.اتصال("10.0.2.2", Integer.parseInt(args[0]));
 اتصال.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] مصدر = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<مصدر.length;i++) if (اتصال.getInputStream().read() != (مصدر[i]&255)) throw new RuntimeException("TCP mismatch");
 اتصال.close();
 DatagramSocket المشارك = العربية.ذاتي.통신.فتح(0); العربية.ذاتي.통신.대기시간(المشارك, 500);
 العربية.ذاتي.통신.يرسل(المشارك, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!العربية.ذاتي.통신.يستلم(المشارك).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 المشارك.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(يعرض_جذر/'build/java-library/classes'),'-d',str(مقياس_بيانات),str(صافي_مصدر)])
                نقل_الملفات_صديق.storbinary('STOR 바깥통신.class', io.BytesIO((مقياس_بيانات/'바깥통신.class').read_bytes()))
                نص = 셸('java 바깥통신 {} {}'.format(ارتداد_خادم_إدخال.TCP_منفذ, ارتداد_خادم_إدخال.بروتوكول_مخطط_بيانات_المستخدم_منفذ))
                assert 'EXTERNAL TCP UDP PASS' in نص and '10.0.2.2' in نص and 'exit 0' in نص, نص
                assert ارتداد_خادم_إدخال.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, ارتداد_خادم_إدخال.수신됨
                assert not ارتداد_خادم_إدخال.오류들, ارتداد_خادم_إدخال.오류들
            التحقق_من_صحة_إبلاغ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            نقل_الملفات_صديق.delete('바깥통신.class')
            خادم_مصدر=مقياس_بيانات/'خادم_يختبر.java'
            خادم_مصدر.write_text('''import java.net.*; public class خادم_يختبر {
 public static void main(String[] args) throws Exception {
  ServerSocket خادم_قيمة = new ServerSocket(9300); DatagramSocket المشارك = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ضيف_قيمة = خادم_قيمة.accept();
  ضيف_قيمة.getOutputStream().write(ضيف_قيمة.getInputStream().read()+1); ضيف_قيمة.close(); خادم_قيمة.close();
  byte[] محتوى_قيمة = new byte[8]; DatagramPacket رزمةمستقلة = new DatagramPacket(محتوى_قيمة, محتوى_قيمة.length); المشارك.receive(رزمةمستقلة);
  المشارك.send(رزمةمستقلة); المشارك.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(مقياس_بيانات),str(خادم_مصدر)])
            نقل_الملفات_صديق.storbinary('STOR خادم_يختبر.class',io.BytesIO((مقياس_بيانات/'خادم_يختبر.class').read_bytes()))
            عملية.stdin.write('java خادم_يختبر\n'.encode());عملية.stdin.flush();يستلم_رسالة(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',خادم_بث_منفذ),timeout=5) as نظير_قيمة:
                نظير_قيمة.sendall(b'A');assert نظير_قيمة.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as نظير_قيمة:
                نظير_قيمة.settimeout(5);نظير_قيمة.sendto(b'UDP-IN',('127.0.0.1',خادم_مخطط_بيانات_منفذ));assert نظير_قيمة.recvfrom(512)[0]==b'UDP-IN'
            نص=يستلم_رسالة();assert 'INBOUND TCP UDP PASS' in نص and 'exit 0' in نص,نص
            التحقق_من_صحة_إبلاغ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            نقل_الملفات_صديق.delete('خادم_يختبر.class')
            تعليمة_تسلسل = 'public class 빛 { public static void main(String[] وسائط) throws Exception { int 합 = 0; int رقم = 1; while (رقم <= 10) { 합 = 합 + رقم; رقم = رقم + 1; } العربية.ذاتي.مخرجات.كتابة_رقم(합); العربية.ذاتي.ملف.كتابة("aot.txt", "한글 AOT ملف 😀"); العربية.ذاتي.مخرجات.كتابة_خط(العربية.ذاتي.ملف.قراءة("aot.txt")); } }'
            نقل_الملفات_صديق.storbinary('STOR 빛.java', io.BytesIO(تعليمة_تسلسل.encode()))
            نص = 셸('javac 빛.java'); assert 'exit 0' in نص and 'Compiled:' in نص, نص
            نص = 셸('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in نص and 'exit 0' in نص, نص
            نص = 셸('run 빛.elf'); assert '\n55\n' in نص and '한글 AOT ملف 😀' in نص and 'exit 0' in نص, نص
            أصلي = bytearray(); نقل_الملفات_صديق.retrbinary('RETR 빛.elf', أصلي.extend)
            نص = 셸('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in نص and 'unsupported' in نص, نص
            보존자료 = bytearray(); نقل_الملفات_صديق.retrbinary('RETR 빛.elf', 보존자료.extend); assert أصلي == 보존자료
            바이트코드 = bytearray(); نقل_الملفات_صديق.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            نقل_الملفات_صديق.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            نص = 셸('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in نص and 'exit 0' in نص, نص
            نص = 셸('run 빛.elf'); assert '\n55\n' in نص and '한글 AOT ملف 😀' in نص and 'exit 0' in نص, نص
            التحقق_من_صحة_إبلاغ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            التحقق_من_صحة_إبلاغ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ثابت_مصدر=مقياس_بيانات/'ثابت_يختبر.java'
            ثابت_مصدر.write_text('''public class ثابت_يختبر {
 static int يعرض_جذر = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] وسائط) {
  int[] قيمة = new int[] {يعرض_جذر, 합(10)};
  System.out.println(قيمة[0] + قيمة[1]); System.out.println(وسائط[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(مقياس_بيانات),str(ثابت_مصدر)])
            نقل_الملفات_صديق.storbinary('STOR ثابت_يختبر.class',io.BytesIO((مقياس_بيانات/'ثابت_يختبر.class').read_bytes()))
            نص=셸('jaot ثابت_يختبر.class -o ثابت_يختبر.elf');assert 'exit 0' in نص,نص
            نص=셸('run ثابت_يختبر.elf 한글인수');assert '\n58\n한글인수\nexit 0' in نص,نص
            نقل_الملفات_صديق.delete('ثابت_يختبر.class');نقل_الملفات_صديق.delete('ثابت_يختبر.elf')
            التحقق_من_صحة_إبلاغ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(أرشيف.getvalue());손상자료[14]^=1
            نقل_الملفات_صديق.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            نص=셸('java -jar 인사.jar');assert 'Main-Class\nexit 1' in نص,نص
            التحقق_من_صحة_إبلاغ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            نقل_الملفات_صديق.quit(); assert 'FTP stopped' in 셸('ftpd stop')
            assert not جسر.خطأ, جسر.خطأ
            التحقق_من_صحة_إبلاغ.update(passed=True, frames_to_guest=جسر.커널수신틀수, frames_from_guest=جسر.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in محدد.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: نسخة_مكتوبة.extend(조각)
            جسر.إيقاف_مؤقت_حدث.set()
            عملية.terminate()
            try: عملية.wait(timeout=5)
            except subprocess.TimeoutExpired: عملية.kill(); عملية.wait()
            محدد.close(); عملية.stdin.close(); عملية.stdout.close()
            التحقق_من_صحة_إبلاغ['bridge_error'] = جسر.خطأ
            التحقق_من_صحة_إبلاغ['frames_to_guest'] = جسر.커널수신틀수; التحقق_من_صحة_إبلاغ['frames_from_guest'] = جسر.커널발신틀수
            (مقياس_بيانات/'packets.json').write_text(json.dumps(جسر.سجل_التتبّع,indent=2)+'\n')
            (مقياس_بيانات / 'serial.log').write_bytes(نسخة_مكتوبة)
            (مقياس_بيانات / 'report.json').write_text(json.dumps(التحقق_من_صحة_إبلاغ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': تشغيل()
