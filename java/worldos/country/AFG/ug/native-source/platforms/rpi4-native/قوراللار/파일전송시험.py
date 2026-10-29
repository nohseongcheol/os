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
from تور_كۆۋرۈك import تور_كۆۋرۈك
from ئىجرا_قىلىش_بۇيرۇق import كۆرسىتىش_يىلتىز, بۇيرۇق
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ئىجرا_قىل_2():
    ئۆلچەم_مەلۇمات = كۆرسىتىش_يىلتىز / 'build/verification/ftp'; ئۆلچەم_مەلۇمات.mkdir(parents=True, exist_ok=True)
    دەلىللەش_خەۋەر = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((كۆرسىتىش_يىلتىز / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ئۆلچەم_مەلۇمات / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception { 한국어.자체.چىقار.يازماق_قۇر("JAR ئىجرا_قىلىش_بۇيرۇق: " + ئۆزگەرگۈچىلەر[0]); 한국어.자체.ھۆججەت.ياز("jar.txt", "자체 يادرو_قىممىتى ھۆججەت"); 한국어.자체.چىقار.يازماق_قۇر(한국어.자체.ھۆججەت.ئوقۇ("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(كۆرسىتىش_يىلتىز/'build/java-library/classes'), '-d', str(ئۆلچەم_مەلۇمات), str(자바원문)])
    ئارخىپ = io.BytesIO()
    with zipfile.ZipFile(ئارخىپ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ئۆلچەم_مەلۇمات/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); مۇلازىمىتېر_ئېقىم_ئېغىز = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with تور_كۆۋرۈك(접속번호, ['tcp:{}:9300'.format(مۇلازىمىتېر_ئېقىم_ئېغىز), 'udp:{}:9301'.format(서버전문접속번호)], تۇتۇش=True) as كۆۋرۈك:
        جەريان = subprocess.Popen(بۇيرۇق() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + كۆۋرۈك.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        تاللىغۇچ = selectors.DefaultSelector(); تاللىغۇچ.register(جەريان.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            مەلۇمات = bytearray(); تاماملىماق_ئاغما = time.monotonic() + 시간제한
            while 확인표시 not in مەلۇمات:
                if time.monotonic() > تاماملىماق_ئاغما or جەريان.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + مەلۇمات.decode('utf-8', 'replace'))
                for 누름값, _ in تاللىغۇچ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: مەلۇمات.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in مەلۇمات or b'FAIL ' in مەلۇمات: raise AssertionError(مەلۇمات)
            return مەلۇمات.decode('utf-8', 'replace').replace('\r\n', '\n')
        def قاپ(قۇر):
            جەريان.stdin.write(قۇر.encode() + b'\n'); جەريان.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in قاپ('ftpd start')
            ھۆججەت_يوللاش_ئۇلىنىش = ftplib.FTP(); ھۆججەت_يوللاش_ئۇلىنىش.encoding = 'utf-8'; ھۆججەت_يوللاش_ئۇلىنىش.connect('127.0.0.1', 접속번호, timeout=20); ھۆججەت_يوللاش_ئۇلىنىش.login()
            يۈك_مەلۇمات = bytes(range(256)) * 32
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR binary.dat', io.BytesIO(يۈك_مەلۇمات))
            ئۆلچەم = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR binary.dat', ئۆلچەم.extend)
            assert ئۆلچەم == يۈك_مەلۇمات; assert ھۆججەت_يوللاش_ئۇلىنىش.size('binary.dat') == len(يۈك_مەلۇمات)
            دەلىللەش_خەۋەر['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in قاپ('cat 한글.txt')
            assert '한글.txt' in ھۆججەت_يوللاش_ئۇلىنىش.nlst()
            assert dict(ھۆججەت_يوللاش_ئۇلىنىش.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            دەلىللەش_خەۋەر['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ئۆلچەم = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR binary.dat', ئۆلچەم.extend); assert ئۆلچەم == يۈك_مەلۇمات
            دەلىللەش_خەۋەر['checks'].append('oversized replacement rejected; previous file preserved')
            with ھۆججەت_يوللاش_ئۇلىنىش.transfercmd('STOR pending.txt') as يۈكلىمەك_ھۆججەت:
                # A control command must not change the active upload's destination.
                assert ھۆججەت_يوللاش_ئۇلىنىش.size('binary.dat') == len(يۈك_مەلۇمات)
                يۈكلىمەك_ھۆججەت.sendall(b'UPLOAD TARGET PRESERVED')
            assert ھۆججەت_يوللاش_ئۇلىنىش.voidresp().startswith('226')
            ئۆلچەم = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR pending.txt', ئۆلچەم.extend)
            assert ئۆلچەم == b'UPLOAD TARGET PRESERVED'
            ئۆلچەم = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR binary.dat', ئۆلچەم.extend)
            assert ئۆلچەم == يۈك_مەلۇمات
            ھۆججەت_يوللاش_ئۇلىنىش.delete('pending.txt')
            دەلىللەش_خەۋەر['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 인사.jar', io.BytesIO(ئارخىپ.getvalue()))
            تېكىست = قاپ('java -jar 인사.jar 누리')
            assert 'JAR ئىجرا_قىلىش_بۇيرۇق: 누리' in تېكىست and '자체 يادرو_قىممىتى ھۆججەت' in تېكىست and 'exit 0' in تېكىست, تېكىست
            تېكىست = قاپ('./인사.jar 세상')
            assert 'JAR ئىجرا_قىلىش_بۇيرۇق: 세상' in تېكىست and 'exit 0' in تېكىست, تېكىست
            دەلىللەش_خەۋەر['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct مەلۇمات { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct مەلۇمات قىممىتى = {합(10), 1.25}; if (قىممىتى.수 != 55 || قىممىتى.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = قۇرۇش_ھۆججەت("cc.txt", ئوقۇش_يېزىش | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; يازماق_ھۆججەت_مەلۇمات(문서, 인사, sizeof(인사)-1); ئاياغ_ھۆججەت(문서); يازماق_ھۆججەت_مەلۇمات(1, 인사, sizeof(인사)-1); return 0; }\n'
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            تېكىست = قاپ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in تېكىست and 'exit 0' in تېكىست, تېكىست
            تېكىست = قاپ('run 한글.elf'); assert 'CC NATIVE PASS' in تېكىست and 'exit 0' in تېكىست, تېكىست
            assert 'CC NATIVE PASS' in قاپ('cat cc.txt')
            실행파일 = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR مىسال_قىممىتى.elf', io.BytesIO(실행파일)); تېكىست = قاپ('run مىسال_قىممىتى.elf'); assert 'CC NATIVE PASS' in تېكىست and 'exit 0' in تېكىست, تېكىست
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR ئىجرا_قىلىش_بۇيرۇق', io.BytesIO(실행파일)); تېكىست=قاپ('./ئىجرا_قىلىش_بۇيرۇق');assert 'CC NATIVE PASS' in تېكىست and 'exit 0' in تېكىست,تېكىست
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR ئاتى.txt', io.BytesIO(실행파일)); تېكىست=قاپ('./ئاتى.txt');assert 'CC NATIVE PASS' in تېكىست and 'exit 0' in تېكىست,تېكىست
            قاپ('rm ئىجرا_قىلىش_بۇيرۇق ئاتى.txt')
            دەلىللەش_خەۋەر['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            قاپ('rm binary.dat 한글.txt 한글.c 한글.elf مىسال_قىممىتى.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ئۆلچەم_مەلۇمات/'linux-reference')
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            تېكىست=قاپ('./리눅스인사');assert 'exit -8' in تېكىست,تېكىست
            تېكىست=قاپ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in تېكىست,تېكىست
            assert 'LINUX ELF FILE IO' in قاپ('cat linux.txt')
            ھۆججەت_يوللاش_ئۇلىنىش.delete('리눅스인사');ھۆججەت_يوللاش_ئۇلىنىش.delete('linux.txt')
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in قاپ('./거짓.elf');ھۆججەت_يوللاش_ئۇلىنىش.delete('거짓.elf')
            دەلىللەش_خەۋەر['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ئۆلچەم_مەلۇمات/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ئۇلا = 한국어.자체.연결통신.ئۇلا("10.0.2.2", Integer.parseInt(args[0]));
 ئۇلا.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] مەنبە = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<مەنبە.length;i++) if (ئۇلا.getInputStream().read() != (مەنبە[i]&255)) throw new RuntimeException("TCP mismatch");
 ئۇلا.close();
 DatagramSocket 종단 = 한국어.자체.통신.ئاچ(0); 한국어.자체.통신.ۋاقىت_ئاشتى(종단, 500);
 한국어.자체.통신.ئەۋەتمەك(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(كۆرسىتىش_يىلتىز/'build/java-library/classes'),'-d',str(ئۆلچەم_مەلۇمات),str(통신원문)])
                ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 바깥통신.class', io.BytesIO((ئۆلچەم_مەلۇمات/'바깥통신.class').read_bytes()))
                تېكىست = قاپ('java 바깥통신 {} {}'.format(되돌림서버항목.يەتكۈزۈش_كونترول_كېلىشىمى_ئېغىز, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in تېكىست and '10.0.2.2' in تېكىست and 'exit 0' in تېكىست, تېكىست
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            دەلىللەش_خەۋەر['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ھۆججەت_يوللاش_ئۇلىنىش.delete('바깥통신.class')
            مۇلازىمىتېر_مەنبە=ئۆلچەم_مەلۇمات/'서버시험.java'
            مۇلازىمىتېر_مەنبە.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket مۇلازىمىتېر_قىممىتى = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket مېھمان_قىممىتى = مۇلازىمىتېر_قىممىتى.accept();
  مېھمان_قىممىتى.getOutputStream().write(مېھمان_قىممىتى.getInputStream().read()+1); مېھمان_قىممىتى.close(); مۇلازىمىتېر_قىممىتى.close();
  byte[] مەزمۇن_قىممىتى = new byte[8]; DatagramPacket 전문 = new DatagramPacket(مەزمۇن_قىممىتى, مەزمۇن_قىممىتى.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ئۆلچەم_مەلۇمات),str(مۇلازىمىتېر_مەنبە)])
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 서버시험.class',io.BytesIO((ئۆلچەم_مەلۇمات/'서버시험.class').read_bytes()))
            جەريان.stdin.write('java 서버시험\n'.encode());جەريان.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',مۇلازىمىتېر_ئېقىم_ئېغىز),timeout=5) as باراۋەرلىك_قىممىتى:
                باراۋەرلىك_قىممىتى.sendall(b'A');assert باراۋەرلىك_قىممىتى.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as باراۋەرلىك_قىممىتى:
                باراۋەرلىك_قىممىتى.settimeout(5);باراۋەرلىك_قىممىتى.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert باراۋەرلىك_قىممىتى.recvfrom(512)[0]==b'UDP-IN'
            تېكىست=수신하기();assert 'INBOUND TCP UDP PASS' in تېكىست and 'exit 0' in تېكىست,تېكىست
            دەلىللەش_خەۋەر['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ھۆججەت_يوللاش_ئۇلىنىش.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] ئۆزگەرگۈچىلەر) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.چىقار.수쓰기(합); 한국어.자체.ھۆججەت.ياز("aot.txt", "한글 AOT ھۆججەت 😀"); 한국어.자체.چىقار.يازماق_قۇر(한국어.자체.ھۆججەت.ئوقۇ("aot.txt")); } }'
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            تېكىست = قاپ('javac 빛.java'); assert 'exit 0' in تېكىست and 'Compiled:' in تېكىست, تېكىست
            تېكىست = قاپ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in تېكىست and 'exit 0' in تېكىست, تېكىست
            تېكىست = قاپ('run 빛.elf'); assert '\n55\n' in تېكىست and '한글 AOT ھۆججەت 😀' in تېكىست and 'exit 0' in تېكىست, تېكىست
            자체실행파일 = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            تېكىست = قاپ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in تېكىست and 'unsupported' in تېكىست, تېكىست
            보존자료 = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ھۆججەت_يوللاش_ئۇلىنىش.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            تېكىست = قاپ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in تېكىست and 'exit 0' in تېكىست, تېكىست
            تېكىست = قاپ('run 빛.elf'); assert '\n55\n' in تېكىست and '한글 AOT ھۆججەت 😀' in تېكىست and 'exit 0' in تېكىست, تېكىست
            دەلىللەش_خەۋەر['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            دەلىللەش_خەۋەر['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ئىستاتىك_مەنبە=ئۆلچەم_مەلۇمات/'정적시험.java'
            ئىستاتىك_مەنبە.write_text('''public class 정적시험 {
 static int كۆرسىتىش_يىلتىز = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] ئۆزگەرگۈچىلەر) {
  int[] قىممىتى = new int[] {كۆرسىتىش_يىلتىز, 합(10)};
  System.out.println(قىممىتى[0] + قىممىتى[1]); System.out.println(ئۆزگەرگۈچىلەر[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ئۆلچەم_مەلۇمات),str(ئىستاتىك_مەنبە)])
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 정적시험.class',io.BytesIO((ئۆلچەم_مەلۇمات/'정적시험.class').read_bytes()))
            تېكىست=قاپ('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in تېكىست,تېكىست
            تېكىست=قاپ('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in تېكىست,تېكىست
            ھۆججەت_يوللاش_ئۇلىنىش.delete('정적시험.class');ھۆججەت_يوللاش_ئۇلىنىش.delete('정적시험.elf')
            دەلىللەش_خەۋەر['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ئارخىپ.getvalue());손상자료[14]^=1
            ھۆججەت_يوللاش_ئۇلىنىش.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            تېكىست=قاپ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in تېكىست,تېكىست
            دەلىللەش_خەۋەر['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ھۆججەت_يوللاش_ئۇلىنىش.quit(); assert 'FTP stopped' in قاپ('ftpd stop')
            assert not كۆۋرۈك.خاتالىق, كۆۋرۈك.خاتالىق
            دەلىللەش_خەۋەر.update(passed=True, frames_to_guest=كۆۋرۈك.커널수신틀수, frames_from_guest=كۆۋرۈك.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in تاللىغۇچ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            كۆۋرۈك.تورمۇزلىماق_ھادىسە.set()
            جەريان.terminate()
            try: جەريان.wait(timeout=5)
            except subprocess.TimeoutExpired: جەريان.kill(); جەريان.wait()
            تاللىغۇچ.close(); جەريان.stdin.close(); جەريان.stdout.close()
            دەلىللەش_خەۋەر['bridge_error'] = كۆۋرۈك.خاتالىق
            دەلىللەش_خەۋەر['frames_to_guest'] = كۆۋرۈك.커널수신틀수; دەلىللەش_خەۋەر['frames_from_guest'] = كۆۋرۈك.커널발신틀수
            (ئۆلچەم_مەلۇمات/'packets.json').write_text(json.dumps(كۆۋرۈك.추적기록,indent=2)+'\n')
            (ئۆلچەم_مەلۇمات / 'serial.log').write_bytes(대화기록)
            (ئۆلچەم_مەلۇمات / 'report.json').write_text(json.dumps(دەلىللەش_خەۋەر, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ئىجرا_قىل_2()
