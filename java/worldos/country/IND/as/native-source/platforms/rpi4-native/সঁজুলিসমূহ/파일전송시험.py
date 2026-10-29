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
from নেটৱৰ্ক_ব্ৰীজ import নেটৱৰ্ক_ব্ৰীজ
from নিষ্পাদন_আদেশ import 기준, কমান্ড
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def সঞ্চালন():
    পৰিমাপ_ডাটা = 기준 / 'build/verification/ftp'; পৰিমাপ_ডাটা.mkdir(parents=True, exist_ok=True)
    বৈধতা_ৰিপ_ৰ্ট = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = পৰিমাপ_ডাটা / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.নিৰ্গম.লিখক_লাইন("JAR নিষ্পাদন_আদেশ: " + 인수[0]); 한국어.자체.নথিপত্ৰ.লিখা("jar.txt", "자체 কাৰ্ণেল_মান নথিপত্ৰ"); 한국어.자체.নিৰ্গম.লিখক_লাইন(한국어.자체.নথিপত্ৰ.পড়া("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(পৰিমাপ_ডাটা), str(자바원문)])
    অভিলেখাগাৰ = io.BytesIO()
    with zipfile.ZipFile(অভিলেখাগাৰ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(পৰিমাপ_ডাটা/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ছাৰ্ভাৰ_ষ্ট্ৰিম_পৰ্ট = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with নেটৱৰ্ক_ব্ৰীজ(접속번호, ['tcp:{}:9300'.format(ছাৰ্ভাৰ_ষ্ট্ৰিম_পৰ্ট), 'udp:{}:9301'.format(서버전문접속번호)], কেপচাৰ=True) as ব্ৰীজ:
        প্ৰসেস = subprocess.Popen(কমান্ড() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ব্ৰীজ.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        চয়নকাৰী = selectors.DefaultSelector(); চয়নকাৰী.register(প্ৰসেস.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ডাটা = bytearray(); অন্ত_কৰক_অফছেট = time.monotonic() + 시간제한
            while 확인표시 not in ডাটা:
                if time.monotonic() > অন্ত_কৰক_অফছেট or প্ৰসেস.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ডাটা.decode('utf-8', 'replace'))
                for 누름값, _ in চয়নকাৰী.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ডাটা.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ডাটা or b'FAIL ' in ডাটা: raise AssertionError(ডাটা)
            return ডাটা.decode('utf-8', 'replace').replace('\r\n', '\n')
        def শ্বেল(লাইন):
            প্ৰসেস.stdin.write(লাইন.encode() + b'\n'); প্ৰসেস.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in শ্বেল('ftpd start')
            ফাইল_স্থানান্তৰণ_সংযোগ = ftplib.FTP(); ফাইল_স্থানান্তৰণ_সংযোগ.encoding = 'utf-8'; ফাইল_স্থানান্তৰণ_সংযোগ.connect('127.0.0.1', 접속번호, timeout=20); ফাইল_স্থানান্তৰণ_সংযোগ.login()
            প্লেল_ড_ডাটা = bytes(range(256)) * 32
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR binary.dat', io.BytesIO(প্লেল_ড_ডাটা))
            পৰিমাপ = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR binary.dat', পৰিমাপ.extend)
            assert পৰিমাপ == প্লেল_ড_ডাটা; assert ফাইল_স্থানান্তৰণ_সংযোগ.size('binary.dat') == len(প্লেল_ড_ডাটা)
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in শ্বেল('cat 한글.txt')
            assert '한글.txt' in ফাইল_স্থানান্তৰণ_সংযোগ.nlst()
            assert dict(ফাইল_স্থানান্তৰণ_সংযোগ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            পৰিমাপ = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR binary.dat', পৰিমাপ.extend); assert পৰিমাপ == প্লেল_ড_ডাটা
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('oversized replacement rejected; previous file preserved')
            with ফাইল_স্থানান্তৰণ_সংযোগ.transfercmd('STOR pending.txt') as আপল_ড_কৰক_ফাইলসমূহ:
                # A control command must not change the active upload's destination.
                assert ফাইল_স্থানান্তৰণ_সংযোগ.size('binary.dat') == len(প্লেল_ড_ডাটা)
                আপল_ড_কৰক_ফাইলসমূহ.sendall(b'UPLOAD TARGET PRESERVED')
            assert ফাইল_স্থানান্তৰণ_সংযোগ.voidresp().startswith('226')
            পৰিমাপ = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR pending.txt', পৰিমাপ.extend)
            assert পৰিমাপ == b'UPLOAD TARGET PRESERVED'
            পৰিমাপ = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR binary.dat', পৰিমাপ.extend)
            assert পৰিমাপ == প্লেল_ড_ডাটা
            ফাইল_স্থানান্তৰণ_সংযোগ.delete('pending.txt')
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 인사.jar', io.BytesIO(অভিলেখাগাৰ.getvalue()))
            টেক্সট = শ্বেল('java -jar 인사.jar 누리')
            assert 'JAR নিষ্পাদন_আদেশ: 누리' in টেক্সট and '자체 কাৰ্ণেল_মান নথিপত্ৰ' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            টেক্সট = শ্বেল('./인사.jar 세상')
            assert 'JAR নিষ্পাদন_আদেশ: 세상' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ডাটা { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ডাটা মান = {합(10), 1.25}; if (মান.수 != 55 || মান.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = খোলক_ফাইল("cc.txt", পঢ়িব_লিখিব_পৰা | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; লিখক_ফাইল_ডাটা(문서, 인사, sizeof(인사)-1); বন্ধ_কৰক_ফাইল(문서); লিখক_ফাইল_ডাটা(1, 인사, sizeof(인사)-1); return 0; }\n'
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            টেক্সট = শ্বেল('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            টেক্সট = শ্বেল('run 한글.elf'); assert 'CC NATIVE PASS' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            assert 'CC NATIVE PASS' in শ্বেল('cat cc.txt')
            실행파일 = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR নজিৰ_মান.elf', io.BytesIO(실행파일)); টেক্সট = শ্বেল('run নজিৰ_মান.elf'); assert 'CC NATIVE PASS' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR নিষ্পাদন_আদেশ', io.BytesIO(실행파일)); টেক্সট=শ্বেল('./নিষ্পাদন_আদেশ');assert 'CC NATIVE PASS' in টেক্সট and 'exit 0' in টেক্সট,টেক্সট
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR নাম.txt', io.BytesIO(실행파일)); টেক্সট=শ্বেল('./নাম.txt');assert 'CC NATIVE PASS' in টেক্সট and 'exit 0' in টেক্সট,টেক্সট
            শ্বেল('rm নিষ্পাদন_আদেশ নাম.txt')
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            শ্বেল('rm binary.dat 한글.txt 한글.c 한글.elf নজিৰ_মান.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(পৰিমাপ_ডাটা/'linux-reference')
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            টেক্সট=শ্বেল('./리눅스인사');assert 'exit -8' in টেক্সট,টেক্সট
            টেক্সট=শ্বেল('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in টেক্সট,টেক্সট
            assert 'LINUX ELF FILE IO' in শ্বেল('cat linux.txt')
            ফাইল_স্থানান্তৰণ_সংযোগ.delete('리눅스인사');ফাইল_স্থানান্তৰণ_সংযোগ.delete('linux.txt')
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in শ্বেল('./거짓.elf');ফাইল_স্থানান্তৰণ_সংযোগ.delete('거짓.elf')
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = পৰিমাপ_ডাটা/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket সংযোগ_স্থাপনা = 한국어.자체.연결통신.সংযোগ_স্থাপনা("10.0.2.2", Integer.parseInt(args[0]));
 সংযোগ_স্থাপনা.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] উৎস = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<উৎস.length;i++) if (সংযোগ_স্থাপনা.getInputStream().read() != (উৎস[i]&255)) throw new RuntimeException("TCP mismatch");
 সংযোগ_স্থাপনা.close();
 DatagramSocket 종단 = 한국어.자체.통신.খোলো(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.ই_মেইল_কৰক(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(পৰিমাপ_ডাটা),str(통신원문)])
                ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 바깥통신.class', io.BytesIO((পৰিমাপ_ডাটা/'바깥통신.class').read_bytes()))
                টেক্সট = শ্বেল('java 바깥통신 {} {}'.format(되돌림서버항목.প্রচাৰণ_নিয়ন্ত্রণ_প্ৰ_ট_ক_ল_পৰ্ট, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in টেক্সট and '10.0.2.2' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ফাইল_স্থানান্তৰণ_সংযোগ.delete('바깥통신.class')
            ছাৰ্ভাৰ_উৎস=পৰিমাপ_ডাটা/'서버시험.java'
            ছাৰ্ভাৰ_উৎস.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ছাৰ্ভাৰ_মান = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket অতিথি_মান = ছাৰ্ভাৰ_মান.accept();
  অতিথি_মান.getOutputStream().write(অতিথি_মান.getInputStream().read()+1); অতিথি_মান.close(); ছাৰ্ভাৰ_মান.close();
  byte[] সামগ্ৰী_মান = new byte[8]; DatagramPacket 전문 = new DatagramPacket(সামগ্ৰী_মান, সামগ্ৰী_মান.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(পৰিমাপ_ডাটা),str(ছাৰ্ভাৰ_উৎস)])
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 서버시험.class',io.BytesIO((পৰিমাপ_ডাটা/'서버시험.class').read_bytes()))
            প্ৰসেস.stdin.write('java 서버시험\n'.encode());প্ৰসেস.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ছাৰ্ভাৰ_ষ্ট্ৰিম_পৰ্ট),timeout=5) as পীয়েৰ_মান:
                পীয়েৰ_মান.sendall(b'A');assert পীয়েৰ_মান.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as পীয়েৰ_মান:
                পীয়েৰ_মান.settimeout(5);পীয়েৰ_মান.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert পীয়েৰ_মান.recvfrom(512)[0]==b'UDP-IN'
            টেক্সট=수신하기();assert 'INBOUND TCP UDP PASS' in টেক্সট and 'exit 0' in টেক্সট,টেক্সট
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ফাইল_স্থানান্তৰণ_সংযোগ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.নিৰ্গম.수쓰기(합); 한국어.자체.নথিপত্ৰ.লিখা("aot.txt", "한글 AOT নথিপত্ৰ 😀"); 한국어.자체.নিৰ্গম.লিখক_লাইন(한국어.자체.নথিপত্ৰ.পড়া("aot.txt")); } }'
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            টেক্সট = শ্বেল('javac 빛.java'); assert 'exit 0' in টেক্সট and 'Compiled:' in টেক্সট, টেক্সট
            টেক্সট = শ্বেল('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            টেক্সট = শ্বেল('run 빛.elf'); assert '\n55\n' in টেক্সট and '한글 AOT নথিপত্ৰ 😀' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            자체실행파일 = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            টেক্সট = শ্বেল('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in টেক্সট and 'unsupported' in টেক্সট, টেক্সট
            보존자료 = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ফাইল_স্থানান্তৰণ_সংযোগ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            টেক্সট = শ্বেল('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            টেক্সট = শ্বেল('run 빛.elf'); assert '\n55\n' in টেক্সট and '한글 AOT নথিপত্ৰ 😀' in টেক্সট and 'exit 0' in টেক্সট, টেক্সট
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            স্থিৰ_উৎস=পৰিমাপ_ডাটা/'정적시험.java'
            স্থিৰ_উৎস.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] মান = new int[] {기준, 합(10)};
  System.out.println(মান[0] + মান[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(পৰিমাপ_ডাটা),str(স্থিৰ_উৎস)])
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 정적시험.class',io.BytesIO((পৰিমাপ_ডাটা/'정적시험.class').read_bytes()))
            টেক্সট=শ্বেল('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in টেক্সট,টেক্সট
            টেক্সট=শ্বেল('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in টেক্সট,টেক্সট
            ফাইল_স্থানান্তৰণ_সংযোগ.delete('정적시험.class');ফাইল_স্থানান্তৰণ_সংযোগ.delete('정적시험.elf')
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(অভিলেখাগাৰ.getvalue());손상자료[14]^=1
            ফাইল_স্থানান্তৰণ_সংযোগ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            টেক্সট=শ্বেল('java -jar 인사.jar');assert 'Main-Class\nexit 1' in টেক্সট,টেক্সট
            বৈধতা_ৰিপ_ৰ্ট['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ফাইল_স্থানান্তৰণ_সংযোগ.quit(); assert 'FTP stopped' in শ্বেল('ftpd stop')
            assert not ব্ৰীজ.ত্ৰুটি, ব্ৰীজ.ত্ৰুটি
            বৈধতা_ৰিপ_ৰ্ট.update(passed=True, frames_to_guest=ব্ৰীজ.커널수신틀수, frames_from_guest=ব্ৰীজ.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in চয়নকাৰী.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ব্ৰীজ.বিৰাম_কৰক_ইভেণ্ট.set()
            প্ৰসেস.terminate()
            try: প্ৰসেস.wait(timeout=5)
            except subprocess.TimeoutExpired: প্ৰসেস.kill(); প্ৰসেস.wait()
            চয়নকাৰী.close(); প্ৰসেস.stdin.close(); প্ৰসেস.stdout.close()
            বৈধতা_ৰিপ_ৰ্ট['bridge_error'] = ব্ৰীজ.ত্ৰুটি
            বৈধতা_ৰিপ_ৰ্ট['frames_to_guest'] = ব্ৰীজ.커널수신틀수; বৈধতা_ৰিপ_ৰ্ট['frames_from_guest'] = ব্ৰীজ.커널발신틀수
            (পৰিমাপ_ডাটা/'packets.json').write_text(json.dumps(ব্ৰীজ.ট্ৰেচ_লগ,indent=2)+'\n')
            (পৰিমাপ_ডাটা / 'serial.log').write_bytes(대화기록)
            (পৰিমাপ_ডাটা / 'report.json').write_text(json.dumps(বৈধতা_ৰিপ_ৰ্ট, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': সঞ্চালন()
