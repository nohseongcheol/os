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
from អនុវត្ត_ពាក្យបញ្ជា import បញ្ចាំង_ឬស, ពាក្យ_បញ្ជា
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def រត់():
    ការវាស់វែង_ទិន្នន័យ = បញ្ចាំង_ឬស / 'build/verification/ftp'; ការវាស់វែង_ទិន្នន័យ.mkdir(parents=True, exist_ok=True)
    សុពលភាព_រាយការណ៍ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((បញ្ចាំង_ឬស / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ការវាស់វែង_ទិន្នន័យ / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] អាគុយម៉ង់) throws Exception { 한국어.자체.លទ្ធផល.សរសេរ_បណ្ដាញ("JAR អនុវត្ត_ពាក្យបញ្ជា: " + អាគុយម៉ង់[0]); 한국어.자체.ឯកសារ.សរសេរ("jar.txt", "자체 ខឺណេល_តំលៃ ឯកសារ"); 한국어.자체.លទ្ធផល.សរសេរ_បណ្ដាញ(한국어.자체.ឯកសារ.អាន("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(បញ្ចាំង_ឬស/'build/java-library/classes'), '-d', str(ការវាស់វែង_ទិន្នន័យ), str(자바원문)])
    ប័ណ្ណសារ = io.BytesIO()
    with zipfile.ZipFile(ប័ណ្ណសារ, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ការវាស់វែង_ទិន្នន័យ/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); លេខរន្ធ = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ម៉ាស៊ីនមេ_ស្ទ្រីម_ច្រក = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with 통신다리(លេខរន្ធ, ['tcp:{}:9300'.format(ម៉ាស៊ីនមេ_ស្ទ្រីម_ច្រក), 'udp:{}:9301'.format(서버전문접속번호)], ថត=True) as 연결다리:
        ដំណើរការ = subprocess.Popen(ពាក្យ_បញ្ជា() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + 연결다리.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        អ្នកជ្រើសរើស = selectors.DefaultSelector(); អ្នកជ្រើសរើស.register(ដំណើរការ.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ទិន្នន័យ = bytearray(); បញ្ចប់_ការបែង_ភាគ = time.monotonic() + 시간제한
            while 확인표시 not in ទិន្នន័យ:
                if time.monotonic() > បញ្ចប់_ការបែង_ភាគ or ដំណើរការ.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ទិន្នន័យ.decode('utf-8', 'replace'))
                for 누름값, _ in អ្នកជ្រើសរើស.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ទិន្នន័យ.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ទិន្នន័យ or b'FAIL ' in ទិន្នន័យ: raise AssertionError(ទិន្នន័យ)
            return ទិន្នន័យ.decode('utf-8', 'replace').replace('\r\n', '\n')
        def 셸(បន្ទាត់):
            ដំណើរការ.stdin.write(បន្ទាត់.encode() + b'\n'); ដំណើរការ.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in 셸('ftpd start')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់ = ftplib.FTP(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.encoding = 'utf-8'; ឯកសារ_ផ្ទេរ_ការភ្ជាប់.connect('127.0.0.1', លេខរន្ធ, timeout=20); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.login()
            ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ = bytes(range(256)) * 32
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR binary.dat', io.BytesIO(ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ))
            ការវាស់វែង = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR binary.dat', ការវាស់វែង.extend)
            assert ការវាស់វែង == ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ; assert ឯកសារ_ផ្ទេរ_ការភ្ជាប់.size('binary.dat') == len(ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ)
            សុពលភាព_រាយការណ៍['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in 셸('cat 한글.txt')
            assert '한글.txt' in ឯកសារ_ផ្ទេរ_ការភ្ជាប់.nlst()
            assert dict(ឯកសារ_ផ្ទេរ_ការភ្ជាប់.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            សុពលភាព_រាយការណ៍['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ការវាស់វែង = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR binary.dat', ការវាស់វែង.extend); assert ការវាស់វែង == ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ
            សុពលភាព_រាយការណ៍['checks'].append('oversized replacement rejected; previous file preserved')
            with ឯកសារ_ផ្ទេរ_ការភ្ជាប់.transfercmd('STOR pending.txt') as បង្ហោះ_ឯកសារ:
                # A control command must not change the active upload's destination.
                assert ឯកសារ_ផ្ទេរ_ការភ្ជាប់.size('binary.dat') == len(ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ)
                បង្ហោះ_ឯកសារ.sendall(b'UPLOAD TARGET PRESERVED')
            assert ឯកសារ_ផ្ទេរ_ការភ្ជាប់.voidresp().startswith('226')
            ការវាស់វែង = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR pending.txt', ការវាស់វែង.extend)
            assert ការវាស់វែង == b'UPLOAD TARGET PRESERVED'
            ការវាស់វែង = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR binary.dat', ការវាស់វែង.extend)
            assert ការវាស់វែង == ទិន្នន័យដែលផ្ទុក_ទិន្នន័យ
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('pending.txt')
            សុពលភាព_រាយការណ៍['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 인사.jar', io.BytesIO(ប័ណ្ណសារ.getvalue()))
            អត្ថបទ = 셸('java -jar 인사.jar 누리')
            assert 'JAR អនុវត្ត_ពាក្យបញ្ជា: 누리' in អត្ថបទ and '자체 ខឺណេល_តំលៃ ឯកសារ' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            អត្ថបទ = 셸('./인사.jar 세상')
            assert 'JAR អនុវត្ត_ពាក្យបញ្ជា: 세상' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            សុពលភាព_រាយការណ៍['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ទិន្នន័យ { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ទិន្នន័យ តំលៃ = {합(10), 1.25}; if (តំលៃ.수 != 55 || តំលៃ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = បើក_ឯកសារ("cc.txt", អាន_សរសេរ | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; សរសេរ_ឯកសារ_ទិន្នន័យ(문서, 인사, sizeof(인사)-1); បិទ_ឯកសារ(문서); សរសេរ_ឯកសារ_ទិន្នន័យ(1, 인사, sizeof(인사)-1); return 0; }\n'
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            អត្ថបទ = 셸('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            អត្ថបទ = 셸('run 한글.elf'); assert 'CC NATIVE PASS' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            assert 'CC NATIVE PASS' in 셸('cat cc.txt')
            실행파일 = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR ចំលង_តំលៃ.elf', io.BytesIO(실행파일)); អត្ថបទ = 셸('run ចំលង_តំលៃ.elf'); assert 'CC NATIVE PASS' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR អនុវត្ត_ពាក្យបញ្ជា', io.BytesIO(실행파일)); អត្ថបទ=셸('./អនុវត្ត_ពាក្យបញ្ជា');assert 'CC NATIVE PASS' in អត្ថបទ and 'exit 0' in អត្ថបទ,អត្ថបទ
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR ឈ្មោះ.txt', io.BytesIO(실행파일)); អត្ថបទ=셸('./ឈ្មោះ.txt');assert 'CC NATIVE PASS' in អត្ថបទ and 'exit 0' in អត្ថបទ,អត្ថបទ
            셸('rm អនុវត្ត_ពាក្យបញ្ជា ឈ្មោះ.txt')
            សុពលភាព_រាយការណ៍['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            셸('rm binary.dat 한글.txt 한글.c 한글.elf ចំលង_តំលៃ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ការវាស់វែង_ទិន្នន័យ/'linux-reference')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            អត្ថបទ=셸('./리눅스인사');assert 'exit -8' in អត្ថបទ,អត្ថបទ
            អត្ថបទ=셸('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in អត្ថបទ,អត្ថបទ
            assert 'LINUX ELF FILE IO' in 셸('cat linux.txt')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('리눅스인사');ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('linux.txt')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in 셸('./거짓.elf');ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('거짓.elf')
            សុពលភាព_រាយការណ៍['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ការវាស់វែង_ទិន្នន័យ/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ភ្ជាប់ = 한국어.자체.연결통신.ភ្ជាប់("10.0.2.2", Integer.parseInt(args[0]));
 ភ្ជាប់.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ប្រភព = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ប្រភព.length;i++) if (ភ្ជាប់.getInputStream().read() != (ប្រភព[i]&255)) throw new RuntimeException("TCP mismatch");
 ភ្ជាប់.close();
 DatagramSocket 종단 = 한국어.자체.통신.បើក(0); 한국어.자체.통신.អស់ម៉ោង(종단, 500);
 한국어.자체.통신.ផ្ញើ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(បញ្ចាំង_ឬស/'build/java-library/classes'),'-d',str(ការវាស់វែង_ទិន្នន័យ),str(통신원문)])
                ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 바깥통신.class', io.BytesIO((ការវាស់វែង_ទិន្នន័យ/'바깥통신.class').read_bytes()))
                អត្ថបទ = 셸('java 바깥통신 {} {}'.format(되돌림서버항목.ប្រូតូកូលត្រូតពិនិត្យការបញ្ជូន_ច្រក, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in អត្ថបទ and '10.0.2.2' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            សុពលភាព_រាយការណ៍['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('바깥통신.class')
            ម៉ាស៊ីនមេ_ប្រភព=ការវាស់វែង_ទិន្នន័យ/'서버시험.java'
            ម៉ាស៊ីនមេ_ប្រភព.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ម៉ាស៊ីនមេ_តំលៃ = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ភ្ញៀវ_តំលៃ = ម៉ាស៊ីនមេ_តំលៃ.accept();
  ភ្ញៀវ_តំលៃ.getOutputStream().write(ភ្ញៀវ_តំលៃ.getInputStream().read()+1); ភ្ញៀវ_តំលៃ.close(); ម៉ាស៊ីនមេ_តំលៃ.close();
  byte[] មាតិកា_តំលៃ = new byte[8]; DatagramPacket 전문 = new DatagramPacket(មាតិកា_តំលៃ, មាតិកា_តំលៃ.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ការវាស់វែង_ទិន្នន័យ),str(ម៉ាស៊ីនមេ_ប្រភព)])
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 서버시험.class',io.BytesIO((ការវាស់វែង_ទិន្នន័យ/'서버시험.class').read_bytes()))
            ដំណើរការ.stdin.write('java 서버시험\n'.encode());ដំណើរការ.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ម៉ាស៊ីនមេ_ស្ទ្រីម_ច្រក),timeout=5) as សិទ្ធស្មើ_តំលៃ:
                សិទ្ធស្មើ_តំលៃ.sendall(b'A');assert សិទ្ធស្មើ_តំលៃ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as សិទ្ធស្មើ_តំលៃ:
                សិទ្ធស្មើ_តំលៃ.settimeout(5);សិទ្ធស្មើ_តំលៃ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert សិទ្ធស្មើ_តំលៃ.recvfrom(512)[0]==b'UDP-IN'
            អត្ថបទ=수신하기();assert 'INBOUND TCP UDP PASS' in អត្ថបទ and 'exit 0' in អត្ថបទ,អត្ថបទ
            សុពលភាព_រាយការណ៍['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] អាគុយម៉ង់) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.លទ្ធផល.수쓰기(합); 한국어.자체.ឯកសារ.សរសេរ("aot.txt", "한글 AOT ឯកសារ 😀"); 한국어.자체.លទ្ធផល.សរសេរ_បណ្ដាញ(한국어.자체.ឯកសារ.អាន("aot.txt")); } }'
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            អត្ថបទ = 셸('javac 빛.java'); assert 'exit 0' in អត្ថបទ and 'Compiled:' in អត្ថបទ, អត្ថបទ
            អត្ថបទ = 셸('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            អត្ថបទ = 셸('run 빛.elf'); assert '\n55\n' in អត្ថបទ and '한글 AOT ឯកសារ 😀' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            자체실행파일 = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            អត្ថបទ = 셸('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in អត្ថបទ and 'unsupported' in អត្ថបទ, អត្ថបទ
            보존자료 = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ឯកសារ_ផ្ទេរ_ការភ្ជាប់.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            អត្ថបទ = 셸('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            អត្ថបទ = 셸('run 빛.elf'); assert '\n55\n' in អត្ថបទ and '한글 AOT ឯកសារ 😀' in អត្ថបទ and 'exit 0' in អត្ថបទ, អត្ថបទ
            សុពលភាព_រាយការណ៍['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            សុពលភាព_រាយការណ៍['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            នឹង_ប្រភព=ការវាស់វែង_ទិន្នន័យ/'정적시험.java'
            នឹង_ប្រភព.write_text('''public class 정적시험 {
 static int បញ្ចាំង_ឬស = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] អាគុយម៉ង់) {
  int[] តំលៃ = new int[] {បញ្ចាំង_ឬស, 합(10)};
  System.out.println(តំលៃ[0] + តំលៃ[1]); System.out.println(អាគុយម៉ង់[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ការវាស់វែង_ទិន្នន័យ),str(នឹង_ប្រភព)])
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 정적시험.class',io.BytesIO((ការវាស់វែង_ទិន្នន័យ/'정적시험.class').read_bytes()))
            អត្ថបទ=셸('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in អត្ថបទ,អត្ថបទ
            អត្ថបទ=셸('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in អត្ថបទ,អត្ថបទ
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('정적시험.class');ឯកសារ_ផ្ទេរ_ការភ្ជាប់.delete('정적시험.elf')
            សុពលភាព_រាយការណ៍['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ប័ណ្ណសារ.getvalue());손상자료[14]^=1
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            អត្ថបទ=셸('java -jar 인사.jar');assert 'Main-Class\nexit 1' in អត្ថបទ,អត្ថបទ
            សុពលភាព_រាយការណ៍['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ឯកសារ_ផ្ទេរ_ការភ្ជាប់.quit(); assert 'FTP stopped' in 셸('ftpd stop')
            assert not 연결다리.កំហុស, 연결다리.កំហុស
            សុពលភាព_រាយការណ៍.update(passed=True, frames_to_guest=연결다리.커널수신틀수, frames_from_guest=연결다리.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in អ្នកជ្រើសរើស.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            연결다리.ផ្អាក_ព្រឹត្តិការណ៍.set()
            ដំណើរការ.terminate()
            try: ដំណើរការ.wait(timeout=5)
            except subprocess.TimeoutExpired: ដំណើរការ.kill(); ដំណើរការ.wait()
            អ្នកជ្រើសរើស.close(); ដំណើរការ.stdin.close(); ដំណើរការ.stdout.close()
            សុពលភាព_រាយការណ៍['bridge_error'] = 연결다리.កំហុស
            សុពលភាព_រាយការណ៍['frames_to_guest'] = 연결다리.커널수신틀수; សុពលភាព_រាយការណ៍['frames_from_guest'] = 연결다리.커널발신틀수
            (ការវាស់វែង_ទិន្នន័យ/'packets.json').write_text(json.dumps(연결다리.ត្រេស_កំណត់_ហេតុ,indent=2)+'\n')
            (ការវាស់វែង_ទិន្នន័យ / 'serial.log').write_bytes(대화기록)
            (ការវាស់វែង_ទិន្នន័យ / 'report.json').write_text(json.dumps(សុពលភាព_រាយការណ៍, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': រត់()
