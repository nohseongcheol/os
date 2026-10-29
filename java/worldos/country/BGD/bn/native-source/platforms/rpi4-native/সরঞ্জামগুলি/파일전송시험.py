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
from নেটওয়ার্ক_ব্রিজ import নেটওয়ার্ক_ব্রিজ
from কার্যকর_করুন_আদেশ import প্রকল্প_মূল, আদেশ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def চালনা():
    পরিমাপ_ডাটা = প্রকল্প_মূল / 'build/verification/ftp'; পরিমাপ_ডাটা.mkdir(parents=True, exist_ok=True)
    বৈধকরণ_রিপোর্ট = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((প্রকল্প_মূল / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = পরিমাপ_ডাটা / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception { বাংলা.নিজ.নির্গম.লেখা_লাইন("JAR কার্যকর_করুন_আদেশ: " + আর্গুমেন্ট_তালিকা[0]); বাংলা.নিজ.নথির_নাম.লেখা("jar.txt", "নিজ কারনেল_মান নথির_নাম"); বাংলা.নিজ.নির্গম.লেখা_লাইন(বাংলা.নিজ.নথির_নাম.পড়া("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(প্রকল্প_মূল/'build/java-library/classes'), '-d', str(পরিমাপ_ডাটা), str(자바원문)])
    সংগ্রহ_করা = io.BytesIO()
    with zipfile.ZipFile(সংগ্রহ_করা, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(পরিমাপ_ডাটা/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); পোর্ট_নম্বর = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); সার্ভার_প্রবাহ_পোর্ট = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with নেটওয়ার্ক_ব্রিজ(পোর্ট_নম্বর, ['tcp:{}:9300'.format(সার্ভার_প্রবাহ_পোর্ট), 'udp:{}:9301'.format(서버전문접속번호)], ক্যাপচার=True) as ব্রিজ:
        প্রসেস = subprocess.Popen(আদেশ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ব্রিজ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        নির্বাচক = selectors.DefaultSelector(); নির্বাচক.register(প্রসেস.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ডাটা = bytearray(); শেষ_করা_অফসেট = time.monotonic() + 시간제한
            while 확인표시 not in ডাটা:
                if time.monotonic() > শেষ_করা_অফসেট or প্রসেস.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ডাটা.decode('utf-8', 'replace'))
                for 누름값, _ in নির্বাচক.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ডাটা.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ডাটা or b'FAIL ' in ডাটা: raise AssertionError(ডাটা)
            return ডাটা.decode('utf-8', 'replace').replace('\r\n', '\n')
        def শেল(নিবেশের_পঙ্_ক্তি):
            প্রসেস.stdin.write(নিবেশের_পঙ্_ক্তি.encode() + b'\n'); প্রসেস.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in শেল('ftpd start')
            ফাইল_স্থানান্তর_সংযোগ = ftplib.FTP(); ফাইল_স্থানান্তর_সংযোগ.encoding = 'utf-8'; ফাইল_স্থানান্তর_সংযোগ.connect('127.0.0.1', পোর্ট_নম্বর, timeout=20); ফাইল_স্থানান্তর_সংযোগ.login()
            পেলোড_ডাটা = bytes(range(256)) * 32
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR binary.dat', io.BytesIO(পেলোড_ডাটা))
            পরিমাপ = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR binary.dat', পরিমাপ.extend)
            assert পরিমাপ == পেলোড_ডাটা; assert ফাইল_স্থানান্তর_সংযোগ.size('binary.dat') == len(পেলোড_ডাটা)
            বৈধকরণ_রিপোর্ট['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in শেল('cat 한글.txt')
            assert '한글.txt' in ফাইল_স্থানান্তর_সংযোগ.nlst()
            assert dict(ফাইল_স্থানান্তর_সংযোগ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            বৈধকরণ_রিপোর্ট['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            পরিমাপ = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR binary.dat', পরিমাপ.extend); assert পরিমাপ == পেলোড_ডাটা
            বৈধকরণ_রিপোর্ট['checks'].append('oversized replacement rejected; previous file preserved')
            with ফাইল_স্থানান্তর_সংযোগ.transfercmd('STOR pending.txt') as আপলোড_ফাইলগুলি:
                # A control command must not change the active upload's destination.
                assert ফাইল_স্থানান্তর_সংযোগ.size('binary.dat') == len(পেলোড_ডাটা)
                আপলোড_ফাইলগুলি.sendall(b'UPLOAD TARGET PRESERVED')
            assert ফাইল_স্থানান্তর_সংযোগ.voidresp().startswith('226')
            পরিমাপ = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR pending.txt', পরিমাপ.extend)
            assert পরিমাপ == b'UPLOAD TARGET PRESERVED'
            পরিমাপ = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR binary.dat', পরিমাপ.extend)
            assert পরিমাপ == পেলোড_ডাটা
            ফাইল_স্থানান্তর_সংযোগ.delete('pending.txt')
            বৈধকরণ_রিপোর্ট['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 인사.jar', io.BytesIO(সংগ্রহ_করা.getvalue()))
            পাঠ = শেল('java -jar 인사.jar 누리')
            assert 'JAR কার্যকর_করুন_আদেশ: 누리' in পাঠ and 'নিজ কারনেল_মান নথির_নাম' in পাঠ and 'exit 0' in পাঠ, পাঠ
            পাঠ = শেল('./인사.jar 세상')
            assert 'JAR কার্যকর_করুন_আদেশ: 세상' in পাঠ and 'exit 0' in পাঠ, পাঠ
            বৈধকরণ_রিপোর্ট['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ডাটা { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ডাটা মান = {합(10), 1.25}; if (মান.수 != 55 || মান.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = খোলা_ফাইল("cc.txt", পঠন_লিখন | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; লেখা_ফাইল_ডাটা(문서, 인사, sizeof(인사)-1); বন্ধ_ফাইল(문서); লেখা_ফাইল_ডাটা(1, 인사, sizeof(인사)-1); return 0; }\n'
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            পাঠ = শেল('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in পাঠ and 'exit 0' in পাঠ, পাঠ
            পাঠ = শেল('run 한글.elf'); assert 'CC NATIVE PASS' in পাঠ and 'exit 0' in পাঠ, পাঠ
            assert 'CC NATIVE PASS' in শেল('cat cc.txt')
            실행파일 = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR নজির_মান.elf', io.BytesIO(실행파일)); পাঠ = শেল('run নজির_মান.elf'); assert 'CC NATIVE PASS' in পাঠ and 'exit 0' in পাঠ, পাঠ
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR কার্যকর_করুন_আদেশ', io.BytesIO(실행파일)); পাঠ=শেল('./কার্যকর_করুন_আদেশ');assert 'CC NATIVE PASS' in পাঠ and 'exit 0' in পাঠ,পাঠ
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR নাম.txt', io.BytesIO(실행파일)); পাঠ=শেল('./নাম.txt');assert 'CC NATIVE PASS' in পাঠ and 'exit 0' in পাঠ,পাঠ
            শেল('rm কার্যকর_করুন_আদেশ নাম.txt')
            বৈধকরণ_রিপোর্ট['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            শেল('rm binary.dat 한글.txt 한글.c 한글.elf নজির_মান.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(পরিমাপ_ডাটা/'linux-reference')
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            পাঠ=শেল('./리눅스인사');assert 'exit -8' in পাঠ,পাঠ
            পাঠ=শেল('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in পাঠ,পাঠ
            assert 'LINUX ELF FILE IO' in শেল('cat linux.txt')
            ফাইল_স্থানান্তর_সংযোগ.delete('리눅스인사');ফাইল_স্থানান্তর_সংযোগ.delete('linux.txt')
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in শেল('./거짓.elf');ফাইল_স্থানান্তর_সংযোগ.delete('거짓.elf')
            বৈধকরণ_রিপোর্ট['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = পরিমাপ_ডাটা/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket সংযোগ_স্থাপনা = বাংলা.নিজ.연결통신.সংযোগ_স্থাপনা("10.0.2.2", Integer.parseInt(args[0]));
 সংযোগ_স্থাপনা.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] উৎস_নথি = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<উৎস_নথি.length;i++) if (সংযোগ_স্থাপনা.getInputStream().read() != (উৎস_নথি[i]&255)) throw new RuntimeException("TCP mismatch");
 সংযোগ_স্থাপনা.close();
 DatagramSocket 종단 = বাংলা.নিজ.통신.খুলুন(0); বাংলা.নিজ.통신.টাইমআউট(종단, 500);
 বাংলা.নিজ.통신.পাঠান(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!বাংলা.নিজ.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(প্রকল্প_মূল/'build/java-library/classes'),'-d',str(পরিমাপ_ডাটা),str(통신원문)])
                ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 바깥통신.class', io.BytesIO((পরিমাপ_ডাটা/'바깥통신.class').read_bytes()))
                পাঠ = শেল('java 바깥통신 {} {}'.format(되돌림서버항목.ট্রান্সমিশন_কন্ট্রোল_প্রটোকল_পোর্ট, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in পাঠ and '10.0.2.2' in পাঠ and 'exit 0' in পাঠ, পাঠ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            বৈধকরণ_রিপোর্ট['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ফাইল_স্থানান্তর_সংযোগ.delete('바깥통신.class')
            সার্ভার_উত্স=পরিমাপ_ডাটা/'서버시험.java'
            সার্ভার_উত্স.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket সার্ভার_মান = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket অতিথি_মান = সার্ভার_মান.accept();
  অতিথি_মান.getOutputStream().write(অতিথি_মান.getInputStream().read()+1); অতিথি_মান.close(); সার্ভার_মান.close();
  byte[] সামগ্রি_মান = new byte[8]; DatagramPacket 전문 = new DatagramPacket(সামগ্রি_মান, সামগ্রি_মান.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(পরিমাপ_ডাটা),str(সার্ভার_উত্স)])
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 서버시험.class',io.BytesIO((পরিমাপ_ডাটা/'서버시험.class').read_bytes()))
            প্রসেস.stdin.write('java 서버시험\n'.encode());প্রসেস.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',সার্ভার_প্রবাহ_পোর্ট),timeout=5) as পিয়ার_মান:
                পিয়ার_মান.sendall(b'A');assert পিয়ার_মান.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as পিয়ার_মান:
                পিয়ার_মান.settimeout(5);পিয়ার_মান.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert পিয়ার_মান.recvfrom(512)[0]==b'UDP-IN'
            পাঠ=수신하기();assert 'INBOUND TCP UDP PASS' in পাঠ and 'exit 0' in পাঠ,পাঠ
            বৈধকরণ_রিপোর্ট['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ফাইল_স্থানান্তর_সংযোগ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] আর্গুমেন্ট_তালিকা) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } বাংলা.নিজ.নির্গম.수쓰기(합); বাংলা.নিজ.নথির_নাম.লেখা("aot.txt", "한글 AOT নথির_নাম 😀"); বাংলা.নিজ.নির্গম.লেখা_লাইন(বাংলা.নিজ.নথির_নাম.পড়া("aot.txt")); } }'
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            পাঠ = শেল('javac 빛.java'); assert 'exit 0' in পাঠ and 'Compiled:' in পাঠ, পাঠ
            পাঠ = শেল('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in পাঠ and 'exit 0' in পাঠ, পাঠ
            পাঠ = শেল('run 빛.elf'); assert '\n55\n' in পাঠ and '한글 AOT নথির_নাম 😀' in পাঠ and 'exit 0' in পাঠ, পাঠ
            자체실행파일 = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            পাঠ = শেল('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in পাঠ and 'unsupported' in পাঠ, পাঠ
            보존자료 = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ফাইল_স্থানান্তর_সংযোগ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            পাঠ = শেল('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in পাঠ and 'exit 0' in পাঠ, পাঠ
            পাঠ = শেল('run 빛.elf'); assert '\n55\n' in পাঠ and '한글 AOT নথির_নাম 😀' in পাঠ and 'exit 0' in পাঠ, পাঠ
            বৈধকরণ_রিপোর্ট['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            বৈধকরণ_রিপোর্ট['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            স্থির_উত্স=পরিমাপ_ডাটা/'정적시험.java'
            স্থির_উত্স.write_text('''public class 정적시험 {
 static int প্রকল্প_মূল = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] আর্গুমেন্ট_তালিকা) {
  int[] মান = new int[] {প্রকল্প_মূল, 합(10)};
  System.out.println(মান[0] + মান[1]); System.out.println(আর্গুমেন্ট_তালিকা[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(পরিমাপ_ডাটা),str(স্থির_উত্স)])
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 정적시험.class',io.BytesIO((পরিমাপ_ডাটা/'정적시험.class').read_bytes()))
            পাঠ=শেল('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in পাঠ,পাঠ
            পাঠ=শেল('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in পাঠ,পাঠ
            ফাইল_স্থানান্তর_সংযোগ.delete('정적시험.class');ফাইল_স্থানান্তর_সংযোগ.delete('정적시험.elf')
            বৈধকরণ_রিপোর্ট['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(সংগ্রহ_করা.getvalue());손상자료[14]^=1
            ফাইল_স্থানান্তর_সংযোগ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            পাঠ=শেল('java -jar 인사.jar');assert 'Main-Class\nexit 1' in পাঠ,পাঠ
            বৈধকরণ_রিপোর্ট['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ফাইল_স্থানান্তর_সংযোগ.quit(); assert 'FTP stopped' in শেল('ftpd stop')
            assert not ব্রিজ.ত্রুটি, ব্রিজ.ত্রুটি
            বৈধকরণ_রিপোর্ট.update(passed=True, frames_to_guest=ব্রিজ.커널수신틀수, frames_from_guest=ব্রিজ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in নির্বাচক.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ব্রিজ.বিরতি_ঘটনা.set()
            প্রসেস.terminate()
            try: প্রসেস.wait(timeout=5)
            except subprocess.TimeoutExpired: প্রসেস.kill(); প্রসেস.wait()
            নির্বাচক.close(); প্রসেস.stdin.close(); প্রসেস.stdout.close()
            বৈধকরণ_রিপোর্ট['bridge_error'] = ব্রিজ.ত্রুটি
            বৈধকরণ_রিপোর্ট['frames_to_guest'] = ব্রিজ.커널수신틀수; বৈধকরণ_রিপোর্ট['frames_from_guest'] = ব্রিজ.커널발신틀수
            (পরিমাপ_ডাটা/'packets.json').write_text(json.dumps(ব্রিজ.ট্রেস_লগ,indent=2)+'\n')
            (পরিমাপ_ডাটা / 'serial.log').write_bytes(대화기록)
            (পরিমাপ_ডাটা / 'report.json').write_text(json.dumps(বৈধকরণ_রিপোর্ট, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': চালনা()
