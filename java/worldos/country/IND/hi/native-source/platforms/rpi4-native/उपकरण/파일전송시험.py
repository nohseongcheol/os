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
from ब्रिज_3de4fe3a import ब्रिज_3de4fe3a
from निष्पादित_करें_आदेश import प्रोजेक्ट_करें_मूल, आदेश
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def चलाएँ():
    परिणाम_डेटा = प्रोजेक्ट_करें_मूल / 'build/verification/ftp'; परिणाम_डेटा.mkdir(parents=True, exist_ok=True)
    प्रमाणीकरण_रिपोर्ट = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((प्रोजेक्ट_करें_मूल / 'build/kernel8.img').read_bytes()).hexdigest()}
    बोला_गया_पाठ = bytearray()
    자바원문 = परिणाम_डेटा / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] तर्क) throws Exception { हिंदी.निज.निर्गम.लिखना_लाइन("JAR निष्पादित_करें_आदेश: " + तर्क[0]); हिंदी.निज.संचिका.लिखें("jar.txt", "निज कर्नेल_मान संचिका"); हिंदी.निज.निर्गम.लिखना_लाइन(हिंदी.निज.संचिका.पढ़ें("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(प्रोजेक्ट_करें_मूल/'build/java-library/classes'), '-d', str(परिणाम_डेटा), str(자바원문)])
    संग्रह = io.BytesIO()
    with zipfile.ZipFile(संग्रह, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(परिणाम_डेटा/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); पोर्ट_संख्या = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버연결접속번호 = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with ब्रिज_3de4fe3a(पोर्ट_संख्या, ['tcp:{}:9300'.format(서버연결접속번호), 'udp:{}:9301'.format(서버전문접속번호)], कैप्चर_करें=True) as ब्रिज:
        प्रक्रिया = subprocess.Popen(आदेश() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ब्रिज.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        सिलेक्टर = selectors.DefaultSelector(); सिलेक्टर.register(प्रक्रिया.stdout, selectors.EVENT_READ)
        def 수신하기(मार्कर=b'jkoros-native> ', 시간제한=60):
            आँकड़े = bytearray(); समाप्त_करें_ऑफ़सेट = time.monotonic() + 시간제한
            while मार्कर not in आँकड़े:
                if time.monotonic() > समाप्त_करें_ऑफ़सेट or प्रक्रिया.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + आँकड़े.decode('utf-8', 'replace'))
                for 누름값, _ in सिलेक्टर.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: आँकड़े.extend(조각); बोला_गया_पाठ.extend(조각)
                if b'PANIC:' in आँकड़े or b'FAIL ' in आँकड़े: raise AssertionError(आँकड़े)
            return आँकड़े.decode('utf-8', 'replace').replace('\r\n', '\n')
        def शेल(पंक्ति):
            प्रक्रिया.stdin.write(पंक्ति.encode() + b'\n'); प्रक्रिया.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in शेल('ftpd start')
            फ़ाइल_स्थानांतरण_कनेक्शन = ftplib.FTP(); फ़ाइल_स्थानांतरण_कनेक्शन.encoding = 'utf-8'; फ़ाइल_स्थानांतरण_कनेक्शन.connect('127.0.0.1', पोर्ट_संख्या, timeout=20); फ़ाइल_स्थानांतरण_कनेक्शन.login()
            पेलोड_डेटा = bytes(range(256)) * 32
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR binary.dat', io.BytesIO(पेलोड_डेटा))
            परिणाम = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR binary.dat', परिणाम.extend)
            assert परिणाम == पेलोड_डेटा; assert फ़ाइल_स्थानांतरण_कनेक्शन.size('binary.dat') == len(पेलोड_डेटा)
            प्रमाणीकरण_रिपोर्ट['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in शेल('cat 한글.txt')
            assert '한글.txt' in फ़ाइल_स्थानांतरण_कनेक्शन.nlst()
            assert dict(फ़ाइल_स्थानांतरण_कनेक्शन.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            प्रमाणीकरण_रिपोर्ट['checks'].append('UTF-8 filename and content visible in guest shell')
            try: फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            परिणाम = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR binary.dat', परिणाम.extend); assert परिणाम == पेलोड_डेटा
            प्रमाणीकरण_रिपोर्ट['checks'].append('oversized replacement rejected; previous file preserved')
            with फ़ाइल_स्थानांतरण_कनेक्शन.transfercmd('STOR pending.txt') as अपलोड_फ़ाइलें:
                # A control command must not change the active upload's destination.
                assert फ़ाइल_स्थानांतरण_कनेक्शन.size('binary.dat') == len(पेलोड_डेटा)
                अपलोड_फ़ाइलें.sendall(b'UPLOAD TARGET PRESERVED')
            assert फ़ाइल_स्थानांतरण_कनेक्शन.voidresp().startswith('226')
            परिणाम = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR pending.txt', परिणाम.extend)
            assert परिणाम == b'UPLOAD TARGET PRESERVED'
            परिणाम = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR binary.dat', परिणाम.extend)
            assert परिणाम == पेलोड_डेटा
            फ़ाइल_स्थानांतरण_कनेक्शन.delete('pending.txt')
            प्रमाणीकरण_रिपोर्ट['checks'].append('interleaved SIZE cannot change the active STOR destination')
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR अभिनन्दन_ae353e94.jar', io.BytesIO(संग्रह.getvalue()))
            पाठ = शेल('java -jar अभिनन्दन_ae353e94.jar 누리')
            assert 'JAR निष्पादित_करें_आदेश: 누리' in पाठ and 'निज कर्नेल_मान संचिका' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('./अभिनन्दन_ae353e94.jar 세상')
            assert 'JAR निष्पादित_करें_आदेश: 세상' in पाठ and 'exit 0' in पाठ, पाठ
            प्रमाणीकरण_रिपोर्ट['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct आँकड़े { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct आँकड़े मान = {합(10), 1.25}; if (मान.수 != 55 || मान.비율 * 2 != 2.5) return 3; const char अभिनन्दन_ae353e94[] = "CC NATIVE PASS\\n"; int 문서 = जारी_फ़ाइल("cc.txt", पठन_लेखन | 없으면만들기 | कम_करें_सामग्री, 0600); if (문서 < 0) return 1; लिखना_फ़ाइल_डेटा(문서, अभिनन्दन_ae353e94, sizeof(अभिनन्दन_ae353e94)-1); बंद_फ़ाइल(문서); लिखना_फ़ाइल_डेटा(1, अभिनन्दन_ae353e94, sizeof(अभिनन्दन_ae353e94)-1); return 0; }\n'
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            पाठ = शेल('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('run 한글.elf'); assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ, पाठ
            assert 'CC NATIVE PASS' in शेल('cat cc.txt')
            निष्पादन_योग्य_फ़ाइल = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR 한글.elf', निष्पादन_योग्य_फ़ाइल.extend)
            assert निष्पादन_योग्य_फ़ाइल[:4] == b'\x7fELF' and निष्पादन_योग्य_फ़ाइल[18:20] == b'\xb7\x00'
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR आवृत्ति_मान.elf', io.BytesIO(निष्पादन_योग्य_फ़ाइल)); पाठ = शेल('run आवृत्ति_मान.elf'); assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ, पाठ
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR निष्पादित_करें_आदेश', io.BytesIO(निष्पादन_योग्य_फ़ाइल)); पाठ=शेल('./निष्पादित_करें_आदेश');assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ,पाठ
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR नाम.txt', io.BytesIO(निष्पादन_योग्य_फ़ाइल)); पाठ=शेल('./नाम.txt');assert 'CC NATIVE PASS' in पाठ and 'exit 0' in पाठ,पाठ
            शेल('rm निष्पादित_करें_आदेश नाम.txt')
            प्रमाणीकरण_रिपोर्ट['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            शेल('rm binary.dat 한글.txt 한글.c 한글.elf आवृत्ति_मान.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(परिणाम_डेटा/'linux-reference')
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            पाठ=शेल('./리눅스인사');assert 'exit -8' in पाठ,पाठ
            पाठ=शेल('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in पाठ,पाठ
            assert 'LINUX ELF FILE IO' in शेल('cat linux.txt')
            फ़ाइल_स्थानांतरण_कनेक्शन.delete('리눅스인사');फ़ाइल_स्थानांतरण_कनेक्शन.delete('linux.txt')
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in शेल('./거짓.elf');फ़ाइल_स्थानांतरण_कनेक्शन.delete('거짓.elf')
            प्रमाणीकरण_रिपोर्ट['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = परिणाम_डेटा/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket जोड़ना = हिंदी.निज.연결통신.जोड़ना("10.0.2.2", Integer.parseInt(args[0]));
 जोड़ना.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] स्रोत = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<स्रोत.length;i++) if (जोड़ना.getInputStream().read() != (स्रोत[i]&255)) throw new RuntimeException("TCP mismatch");
 जोड़ना.close();
 DatagramSocket एंडपॉइंट = हिंदी.निज.통신.खोलें(0); हिंदी.निज.통신.대기시간(एंडपॉइंट, 500);
 हिंदी.निज.통신.भेजें(एंडपॉइंट, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!हिंदी.निज.통신.받기(एंडपॉइंट).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 एंडपॉइंट.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(प्रोजेक्ट_करें_मूल/'build/java-library/classes'),'-d',str(परिणाम_डेटा),str(통신원문)])
                फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 바깥통신.class', io.BytesIO((परिणाम_डेटा/'바깥통신.class').read_bytes()))
                पाठ = शेल('java 바깥통신 {} {}'.format(되돌림서버항목.연결접속번호, 되돌림서버항목.यूज़र_डेटाग्राम_प्रॉटोकॉल_पोर्ट))
                assert 'EXTERNAL TCP UDP PASS' in पाठ and '10.0.2.2' in पाठ and 'exit 0' in पाठ, पाठ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            प्रमाणीकरण_रिपोर्ट['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            फ़ाइल_स्थानांतरण_कनेक्शन.delete('바깥통신.class')
            서버원문=परिणाम_डेटा/'서버시험.java'
            서버원문.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket 서버 = new ServerSocket(9300); DatagramSocket एंडपॉइंट = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket अतिथि_मान = 서버.accept();
  अतिथि_मान.getOutputStream().write(अतिथि_मान.getInputStream().read()+1); अतिथि_मान.close(); 서버.close();
  byte[] सामग्री_मान = new byte[8]; DatagramPacket स्वतंत्रसंदेश = new DatagramPacket(सामग्री_मान, सामग्री_मान.length); एंडपॉइंट.receive(स्वतंत्रसंदेश);
  एंडपॉइंट.send(स्वतंत्रसंदेश); एंडपॉइंट.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(परिणाम_डेटा),str(서버원문)])
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 서버시험.class',io.BytesIO((परिणाम_डेटा/'서버시험.class').read_bytes()))
            प्रक्रिया.stdin.write('java 서버시험\n'.encode());प्रक्रिया.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',서버연결접속번호),timeout=5) as पीअर_मान:
                पीअर_मान.sendall(b'A');assert पीअर_मान.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as पीअर_मान:
                पीअर_मान.settimeout(5);पीअर_मान.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert पीअर_मान.recvfrom(512)[0]==b'UDP-IN'
            पाठ=수신하기();assert 'INBOUND TCP UDP PASS' in पाठ and 'exit 0' in पाठ,पाठ
            प्रमाणीकरण_रिपोर्ट['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            फ़ाइल_स्थानांतरण_कनेक्शन.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] तर्क) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } हिंदी.निज.निर्गम.수쓰기(합); हिंदी.निज.संचिका.लिखें("aot.txt", "한글 AOT संचिका 😀"); हिंदी.निज.निर्गम.लिखना_लाइन(हिंदी.निज.संचिका.पढ़ें("aot.txt")); } }'
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            पाठ = शेल('javac 빛.java'); assert 'exit 0' in पाठ and 'Compiled:' in पाठ, पाठ
            पाठ = शेल('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('run 빛.elf'); assert '\n55\n' in पाठ and '한글 AOT संचिका 😀' in पाठ and 'exit 0' in पाठ, पाठ
            자체실행파일 = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            पाठ = शेल('jaot अभिनन्दन_ae353e94.jar -o 빛.elf'); assert 'exit 1' in पाठ and 'unsupported' in पाठ, पाठ
            보존자료 = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); फ़ाइल_स्थानांतरण_कनेक्शन.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            पाठ = शेल('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in पाठ and 'exit 0' in पाठ, पाठ
            पाठ = शेल('run 빛.elf'); assert '\n55\n' in पाठ and '한글 AOT संचिका 😀' in पाठ and 'exit 0' in पाठ, पाठ
            प्रमाणीकरण_रिपोर्ट['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            प्रमाणीकरण_रिपोर्ट['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            정적원문=परिणाम_डेटा/'정적시험.java'
            정적원문.write_text('''public class 정적시험 {
 static int प्रोजेक्ट_करें_मूल = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] तर्क) {
  int[] मान = new int[] {प्रोजेक्ट_करें_मूल, 합(10)};
  System.out.println(मान[0] + मान[1]); System.out.println(तर्क[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(परिणाम_डेटा),str(정적원문)])
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR 정적시험.class',io.BytesIO((परिणाम_डेटा/'정적시험.class').read_bytes()))
            पाठ=शेल('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in पाठ,पाठ
            पाठ=शेल('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in पाठ,पाठ
            फ़ाइल_स्थानांतरण_कनेक्शन.delete('정적시험.class');फ़ाइल_स्थानांतरण_कनेक्शन.delete('정적시험.elf')
            प्रमाणीकरण_रिपोर्ट['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(संग्रह.getvalue());손상자료[14]^=1
            फ़ाइल_स्थानांतरण_कनेक्शन.storbinary('STOR अभिनन्दन_ae353e94.jar',io.BytesIO(손상자료))
            पाठ=शेल('java -jar अभिनन्दन_ae353e94.jar');assert 'Main-Class\nexit 1' in पाठ,पाठ
            प्रमाणीकरण_रिपोर्ट['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            फ़ाइल_स्थानांतरण_कनेक्शन.quit(); assert 'FTP stopped' in शेल('ftpd stop')
            assert not ब्रिज.त्रुटि, ब्रिज.त्रुटि
            प्रमाणीकरण_रिपोर्ट.update(passed=True, frames_to_guest=ब्रिज.커널수신틀수, frames_from_guest=ब्रिज.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in सिलेक्टर.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: बोला_गया_पाठ.extend(조각)
            ब्रिज.रोकें_घटना.set()
            प्रक्रिया.terminate()
            try: प्रक्रिया.wait(timeout=5)
            except subprocess.TimeoutExpired: प्रक्रिया.kill(); प्रक्रिया.wait()
            सिलेक्टर.close(); प्रक्रिया.stdin.close(); प्रक्रिया.stdout.close()
            प्रमाणीकरण_रिपोर्ट['bridge_error'] = ब्रिज.त्रुटि
            प्रमाणीकरण_रिपोर्ट['frames_to_guest'] = ब्रिज.커널수신틀수; प्रमाणीकरण_रिपोर्ट['frames_from_guest'] = ब्रिज.커널발신틀수
            (परिणाम_डेटा/'packets.json').write_text(json.dumps(ब्रिज.ट्रेस_लॉग,indent=2)+'\n')
            (परिणाम_डेटा / 'serial.log').write_bytes(बोला_गया_पाठ)
            (परिणाम_डेटा / 'report.json').write_text(json.dumps(प्रमाणीकरण_रिपोर्ट, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': चलाएँ()
