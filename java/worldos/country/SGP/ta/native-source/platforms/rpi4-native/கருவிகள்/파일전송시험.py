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
from பிணையம்_பிரிட்ஜ் import பிணையம்_பிரிட்ஜ்
from இயக்கு_கட்டளை import திட்டப்பணி_மூலம், கட்டளை
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def செயல்படுத்துக():
    அளவிடக்கூடியது_தரவு = திட்டப்பணி_மூலம் / 'build/verification/ftp'; அளவிடக்கூடியது_தரவு.mkdir(parents=True, exist_ok=True)
    செல்லுபடியாக்கம்_அறிக்கை = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((திட்டப்பணி_மூலம் / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = அளவிடக்கூடியது_தரவு / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] செயலுருபுகள்) throws Exception { தமிழ்.자체.வெளியீட்டு_இடம்.எழுது_வரி("JAR இயக்கு_கட்டளை: " + செயலுருபுகள்[0]); தமிழ்.자체.கோப்பின்_பெயர்.எழுது("jar.txt", "자체 கரு_மதிப்பு கோப்பின்_பெயர்"); தமிழ்.자체.வெளியீட்டு_இடம்.எழுது_வரி(தமிழ்.자체.கோப்பின்_பெயர்.படி("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(திட்டப்பணி_மூலம்/'build/java-library/classes'), '-d', str(அளவிடக்கூடியது_தரவு), str(자바원문)])
    காப்பகம் = io.BytesIO()
    with zipfile.ZipFile(காப்பகம், 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(அளவிடக்கூடியது_தரவு/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); முனைய_எண் = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); சேவையகம்_தொடரோடி_முணையம் = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with பிணையம்_பிரிட்ஜ்(முனைய_எண், ['tcp:{}:9300'.format(சேவையகம்_தொடரோடி_முணையம்), 'udp:{}:9301'.format(서버전문접속번호)], பிடிப்பு=True) as பிரிட்ஜ்:
        செயல்பாடு = subprocess.Popen(கட்டளை() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + பிரிட்ஜ்.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        தேர்வி = selectors.DefaultSelector(); தேர்வி.register(செயல்பாடு.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            தரவு = bytearray(); முடி_ஆஃப்செட் = time.monotonic() + 시간제한
            while 확인표시 not in தரவு:
                if time.monotonic() > முடி_ஆஃப்செட் or செயல்பாடு.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + தரவு.decode('utf-8', 'replace'))
                for 누름값, _ in தேர்வி.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: தரவு.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in தரவு or b'FAIL ' in தரவு: raise AssertionError(தரவு)
            return தரவு.decode('utf-8', 'replace').replace('\r\n', '\n')
        def கூடு(உள்ளீட்டு_வரி):
            செயல்பாடு.stdin.write(உள்ளீட்டு_வரி.encode() + b'\n'); செயல்பாடு.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in கூடு('ftpd start')
            கோப்பு_இடமாற்று_இணைப்பு = ftplib.FTP(); கோப்பு_இடமாற்று_இணைப்பு.encoding = 'utf-8'; கோப்பு_இடமாற்று_இணைப்பு.connect('127.0.0.1', முனைய_எண், timeout=20); கோப்பு_இடமாற்று_இணைப்பு.login()
            பேலோட்_தரவு = bytes(range(256)) * 32
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR binary.dat', io.BytesIO(பேலோட்_தரவு))
            அளவிடக்கூடியது = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR binary.dat', அளவிடக்கூடியது.extend)
            assert அளவிடக்கூடியது == பேலோட்_தரவு; assert கோப்பு_இடமாற்று_இணைப்பு.size('binary.dat') == len(பேலோட்_தரவு)
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in கூடு('cat 한글.txt')
            assert '한글.txt' in கோப்பு_இடமாற்று_இணைப்பு.nlst()
            assert dict(கோப்பு_இடமாற்று_இணைப்பு.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('UTF-8 filename and content visible in guest shell')
            try: கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            அளவிடக்கூடியது = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR binary.dat', அளவிடக்கூடியது.extend); assert அளவிடக்கூடியது == பேலோட்_தரவு
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('oversized replacement rejected; previous file preserved')
            with கோப்பு_இடமாற்று_இணைப்பு.transfercmd('STOR pending.txt') as பதிவேற்று_கோப்புகள்:
                # A control command must not change the active upload's destination.
                assert கோப்பு_இடமாற்று_இணைப்பு.size('binary.dat') == len(பேலோட்_தரவு)
                பதிவேற்று_கோப்புகள்.sendall(b'UPLOAD TARGET PRESERVED')
            assert கோப்பு_இடமாற்று_இணைப்பு.voidresp().startswith('226')
            அளவிடக்கூடியது = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR pending.txt', அளவிடக்கூடியது.extend)
            assert அளவிடக்கூடியது == b'UPLOAD TARGET PRESERVED'
            அளவிடக்கூடியது = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR binary.dat', அளவிடக்கூடியது.extend)
            assert அளவிடக்கூடியது == பேலோட்_தரவு
            கோப்பு_இடமாற்று_இணைப்பு.delete('pending.txt')
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('interleaved SIZE cannot change the active STOR destination')
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 인사.jar', io.BytesIO(காப்பகம்.getvalue()))
            உரை = கூடு('java -jar 인사.jar 누리')
            assert 'JAR இயக்கு_கட்டளை: 누리' in உரை and '자체 கரு_மதிப்பு கோப்பின்_பெயர்' in உரை and 'exit 0' in உரை, உரை
            உரை = கூடு('./인사.jar 세상')
            assert 'JAR இயக்கு_கட்டளை: 세상' in உரை and 'exit 0' in உரை, உரை
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct தரவு { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct தரவு மதிப்பு = {합(10), 1.25}; if (மதிப்பு.수 != 55 || மதிப்பு.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = திற_கோப்பு("cc.txt", படிக்க_எழுத | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; எழுது_கோப்பு_தரவு(문서, 인사, sizeof(인사)-1); மூடு_கோப்பு(문서); எழுது_கோப்பு_தரவு(1, 인사, sizeof(인사)-1); return 0; }\n'
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            உரை = கூடு('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in உரை and 'exit 0' in உரை, உரை
            உரை = கூடு('run 한글.elf'); assert 'CC NATIVE PASS' in உரை and 'exit 0' in உரை, உரை
            assert 'CC NATIVE PASS' in கூடு('cat cc.txt')
            செயல்படுத்தக்கூடிய_கோப்பு = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR 한글.elf', செயல்படுத்தக்கூடிய_கோப்பு.extend)
            assert செயல்படுத்தக்கூடிய_கோப்பு[:4] == b'\x7fELF' and செயல்படுத்தக்கூடிய_கோப்பு[18:20] == b'\xb7\x00'
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR நகலெடு_மதிப்பு.elf', io.BytesIO(செயல்படுத்தக்கூடிய_கோப்பு)); உரை = கூடு('run நகலெடு_மதிப்பு.elf'); assert 'CC NATIVE PASS' in உரை and 'exit 0' in உரை, உரை
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR இயக்கு_கட்டளை', io.BytesIO(செயல்படுத்தக்கூடிய_கோப்பு)); உரை=கூடு('./இயக்கு_கட்டளை');assert 'CC NATIVE PASS' in உரை and 'exit 0' in உரை,உரை
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR பெயர்.txt', io.BytesIO(செயல்படுத்தக்கூடிய_கோப்பு)); உரை=கூடு('./பெயர்.txt');assert 'CC NATIVE PASS' in உரை and 'exit 0' in உரை,உரை
            கூடு('rm இயக்கு_கட்டளை பெயர்.txt')
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            கூடு('rm binary.dat 한글.txt 한글.c 한글.elf நகலெடு_மதிப்பு.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(அளவிடக்கூடியது_தரவு/'linux-reference')
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            உரை=கூடு('./리눅스인사');assert 'exit -8' in உரை,உரை
            உரை=கூடு('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in உரை,உரை
            assert 'LINUX ELF FILE IO' in கூடு('cat linux.txt')
            கோப்பு_இடமாற்று_இணைப்பு.delete('리눅스인사');கோப்பு_இடமாற்று_இணைப்பு.delete('linux.txt')
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in கூடு('./거짓.elf');கோப்பு_இடமாற்று_இணைப்பு.delete('거짓.elf')
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = அளவிடக்கூடியது_தரவு/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket இணைக்க = தமிழ்.자체.연결통신.இணைக்க("10.0.2.2", Integer.parseInt(args[0]));
 இணைக்க.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] மூலக்_கோப்பு = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<மூலக்_கோப்பு.length;i++) if (இணைக்க.getInputStream().read() != (மூலக்_கோப்பு[i]&255)) throw new RuntimeException("TCP mismatch");
 இணைக்க.close();
 DatagramSocket முடிவுப்_புள்ளி = தமிழ்.자체.통신.திற(0); தமிழ்.자체.통신.대기시간(முடிவுப்_புள்ளி, 500);
 தமிழ்.자체.통신.அனுப்பு(முடிவுப்_புள்ளி, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!தமிழ்.자체.통신.받기(முடிவுப்_புள்ளி).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 முடிவுப்_புள்ளி.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(திட்டப்பணி_மூலம்/'build/java-library/classes'),'-d',str(அளவிடக்கூடியது_தரவு),str(통신원문)])
                கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 바깥통신.class', io.BytesIO((அளவிடக்கூடியது_தரவு/'바깥통신.class').read_bytes()))
                உரை = கூடு('java 바깥통신 {} {}'.format(되돌림서버항목.டிரான்ஸ்மிஷன்_கண்ட்ரோல்_புரோட்டோகால்_முணையம், 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in உரை and '10.0.2.2' in உரை and 'exit 0' in உரை, உரை
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            கோப்பு_இடமாற்று_இணைப்பு.delete('바깥통신.class')
            சேவையகம்_மூலம்=அளவிடக்கூடியது_தரவு/'서버시험.java'
            சேவையகம்_மூலம்.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket சேவையகம்_மதிப்பு = new ServerSocket(9300); DatagramSocket முடிவுப்_புள்ளி = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket விருந்தினர்_மதிப்பு = சேவையகம்_மதிப்பு.accept();
  விருந்தினர்_மதிப்பு.getOutputStream().write(விருந்தினர்_மதிப்பு.getInputStream().read()+1); விருந்தினர்_மதிப்பு.close(); சேவையகம்_மதிப்பு.close();
  byte[] உள்ளடக்கம்_மதிப்பு = new byte[8]; DatagramPacket 전문 = new DatagramPacket(உள்ளடக்கம்_மதிப்பு, உள்ளடக்கம்_மதிப்பு.length); முடிவுப்_புள்ளி.receive(전문);
  முடிவுப்_புள்ளி.send(전문); முடிவுப்_புள்ளி.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(அளவிடக்கூடியது_தரவு),str(சேவையகம்_மூலம்)])
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 서버시험.class',io.BytesIO((அளவிடக்கூடியது_தரவு/'서버시험.class').read_bytes()))
            செயல்பாடு.stdin.write('java 서버시험\n'.encode());செயல்பாடு.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',சேவையகம்_தொடரோடி_முணையம்),timeout=5) as பியர்_மதிப்பு:
                பியர்_மதிப்பு.sendall(b'A');assert பியர்_மதிப்பு.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as பியர்_மதிப்பு:
                பியர்_மதிப்பு.settimeout(5);பியர்_மதிப்பு.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert பியர்_மதிப்பு.recvfrom(512)[0]==b'UDP-IN'
            உரை=수신하기();assert 'INBOUND TCP UDP PASS' in உரை and 'exit 0' in உரை,உரை
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            கோப்பு_இடமாற்று_இணைப்பு.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] செயலுருபுகள்) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } தமிழ்.자체.வெளியீட்டு_இடம்.수쓰기(합); தமிழ்.자체.கோப்பின்_பெயர்.எழுது("aot.txt", "한글 AOT கோப்பின்_பெயர் 😀"); தமிழ்.자체.வெளியீட்டு_இடம்.எழுது_வரி(தமிழ்.자체.கோப்பின்_பெயர்.படி("aot.txt")); } }'
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            உரை = கூடு('javac 빛.java'); assert 'exit 0' in உரை and 'Compiled:' in உரை, உரை
            உரை = கூடு('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in உரை and 'exit 0' in உரை, உரை
            உரை = கூடு('run 빛.elf'); assert '\n55\n' in உரை and '한글 AOT கோப்பின்_பெயர் 😀' in உரை and 'exit 0' in உரை, உரை
            자체실행파일 = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            உரை = கூடு('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in உரை and 'unsupported' in உரை, உரை
            보존자료 = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); கோப்பு_இடமாற்று_இணைப்பு.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            உரை = கூடு('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in உரை and 'exit 0' in உரை, உரை
            உரை = கூடு('run 빛.elf'); assert '\n55\n' in உரை and '한글 AOT கோப்பின்_பெயர் 😀' in உரை and 'exit 0' in உரை, உரை
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            மாறா_மூலம்=அளவிடக்கூடியது_தரவு/'정적시험.java'
            மாறா_மூலம்.write_text('''public class 정적시험 {
 static int திட்டப்பணி_மூலம் = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] செயலுருபுகள்) {
  int[] மதிப்பு = new int[] {திட்டப்பணி_மூலம், 합(10)};
  System.out.println(மதிப்பு[0] + மதிப்பு[1]); System.out.println(செயலுருபுகள்[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(அளவிடக்கூடியது_தரவு),str(மாறா_மூலம்)])
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 정적시험.class',io.BytesIO((அளவிடக்கூடியது_தரவு/'정적시험.class').read_bytes()))
            உரை=கூடு('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in உரை,உரை
            உரை=கூடு('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in உரை,உரை
            கோப்பு_இடமாற்று_இணைப்பு.delete('정적시험.class');கோப்பு_இடமாற்று_இணைப்பு.delete('정적시험.elf')
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(காப்பகம்.getvalue());손상자료[14]^=1
            கோப்பு_இடமாற்று_இணைப்பு.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            உரை=கூடு('java -jar 인사.jar');assert 'Main-Class\nexit 1' in உரை,உரை
            செல்லுபடியாக்கம்_அறிக்கை['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            கோப்பு_இடமாற்று_இணைப்பு.quit(); assert 'FTP stopped' in கூடு('ftpd stop')
            assert not பிரிட்ஜ்.பிழை, பிரிட்ஜ்.பிழை
            செல்லுபடியாக்கம்_அறிக்கை.update(passed=True, frames_to_guest=பிரிட்ஜ்.커널수신틀수, frames_from_guest=பிரிட்ஜ்.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in தேர்வி.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            பிரிட்ஜ்.நிற்க_நிகழ்வு.set()
            செயல்பாடு.terminate()
            try: செயல்பாடு.wait(timeout=5)
            except subprocess.TimeoutExpired: செயல்பாடு.kill(); செயல்பாடு.wait()
            தேர்வி.close(); செயல்பாடு.stdin.close(); செயல்பாடு.stdout.close()
            செல்லுபடியாக்கம்_அறிக்கை['bridge_error'] = பிரிட்ஜ்.பிழை
            செல்லுபடியாக்கம்_அறிக்கை['frames_to_guest'] = பிரிட்ஜ்.커널수신틀수; செல்லுபடியாக்கம்_அறிக்கை['frames_from_guest'] = பிரிட்ஜ்.커널발신틀수
            (அளவிடக்கூடியது_தரவு/'packets.json').write_text(json.dumps(பிரிட்ஜ்.சுவடு_பதிவு,indent=2)+'\n')
            (அளவிடக்கூடியது_தரவு / 'serial.log').write_bytes(대화기록)
            (அளவிடக்கூடியது_தரவு / 'report.json').write_text(json.dumps(செல்லுபடியாக்கம்_அறிக்கை, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': செயல்படுத்துக()
