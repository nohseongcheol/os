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
from ජාලය_පාලම import ජාලය_පාලම
from ක්_රියාත්මක_කරන්න_විධානය import 기준, විධානය
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ක්_රියාත්මක_කරන්න_2():
    결과자료 = 기준 / 'build/verification/ftp'; 결과자료.mkdir(parents=True, exist_ok=True)
    වලංගුකරණය_වාර්තාව = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((기준 / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = 결과자료 / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] විස්තාරක) throws Exception { 한국어.자체.출력.ලියන්න_පේළිය("JAR ක්_රියාත්මක_කරන්න_විධානය: " + විස්තාරක[0]); 한국어.자체.ගොනු.ලිවීම("jar.txt", "자체 කර්නලය_අගය ගොනු"); 한국어.자체.출력.ලියන්න_පේළිය(한국어.자체.ගොනු.කියවීම("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(기준/'build/java-library/classes'), '-d', str(결과자료), str(자바원문)])
    සංරක්ෂිතය = io.BytesIO()
    with zipfile.ZipFile(සංරක්ෂිතය, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(결과자료/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 접속번호 = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); සේවාදායකය_දහර_තොට = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with ජාලය_පාලම(접속번호, ['tcp:{}:9300'.format(සේවාදායකය_දහර_තොට), 'udp:{}:9301'.format(서버전문접속번호)], ග්_රහණය=True) as පාලම:
        සැකසුම = subprocess.Popen(විධානය() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + පාලම.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        වරකය = selectors.DefaultSelector(); වරකය.register(සැකසුම.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            දත්ත = bytearray(); නිමා_කරන්න_ඕෆ්සෙට් = time.monotonic() + 시간제한
            while 확인표시 not in දත්ත:
                if time.monotonic() > නිමා_කරන්න_ඕෆ්සෙට් or සැකසුම.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + දත්ත.decode('utf-8', 'replace'))
                for 누름값, _ in වරකය.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: දත්ත.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in දත්ත or b'FAIL ' in දත්ත: raise AssertionError(දත්ත)
            return දත්ත.decode('utf-8', 'replace').replace('\r\n', '\n')
        def කවචය(පේළිය):
            සැකසුම.stdin.write(පේළිය.encode() + b'\n'); සැකසුම.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in කවචය('ftpd start')
            ගොනුව_මාරුව_සබැඳුම = ftplib.FTP(); ගොනුව_මාරුව_සබැඳුම.encoding = 'utf-8'; ගොනුව_මාරුව_සබැඳුම.connect('127.0.0.1', 접속번호, timeout=20); ගොනුව_මාරුව_සබැඳුම.login()
            ගෙවීම්_භාරය_දත්ත = bytes(range(256)) * 32
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR binary.dat', io.BytesIO(ගෙවීම්_භාරය_දත්ත))
            결과 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ගෙවීම්_භාරය_දත්ත; assert ගොනුව_මාරුව_සබැඳුම.size('binary.dat') == len(ගෙවීම්_භාරය_දත්ත)
            වලංගුකරණය_වාර්තාව['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in කවචය('cat 한글.txt')
            assert '한글.txt' in ගොනුව_මාරුව_සබැඳුම.nlst()
            assert dict(ගොනුව_මාරුව_සබැඳුම.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            වලංගුකරණය_වාර්තාව['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ගොනුව_මාරුව_සබැඳුම.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            결과 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR binary.dat', 결과.extend); assert 결과 == ගෙවීම්_භාරය_දත්ත
            වලංගුකරණය_වාර්තාව['checks'].append('oversized replacement rejected; previous file preserved')
            with ගොනුව_මාරුව_සබැඳුම.transfercmd('STOR pending.txt') as උඩුගත_කරන්න_ගොනු:
                # A control command must not change the active upload's destination.
                assert ගොනුව_මාරුව_සබැඳුම.size('binary.dat') == len(ගෙවීම්_භාරය_දත්ත)
                උඩුගත_කරන්න_ගොනු.sendall(b'UPLOAD TARGET PRESERVED')
            assert ගොනුව_මාරුව_සබැඳුම.voidresp().startswith('226')
            결과 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR pending.txt', 결과.extend)
            assert 결과 == b'UPLOAD TARGET PRESERVED'
            결과 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR binary.dat', 결과.extend)
            assert 결과 == ගෙවීම්_භාරය_දත්ත
            ගොනුව_මාරුව_සබැඳුම.delete('pending.txt')
            වලංගුකරණය_වාර්තාව['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 인사.jar', io.BytesIO(සංරක්ෂිතය.getvalue()))
            පෙළ = කවචය('java -jar 인사.jar 누리')
            assert 'JAR ක්_රියාත්මක_කරන්න_විධානය: 누리' in පෙළ and '자체 කර්නලය_අගය ගොනු' in පෙළ and 'exit 0' in පෙළ, පෙළ
            පෙළ = කවචය('./인사.jar 세상')
            assert 'JAR ක්_රියාත්මක_කරන්න_විධානය: 세상' in පෙළ and 'exit 0' in පෙළ, පෙළ
            වලංගුකරණය_වාර්තාව['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct දත්ත { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct දත්ත අගය = {합(10), 1.25}; if (අගය.수 != 55 || අගය.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = සාදන්න_ගොනුව("cc.txt", කියවීම්_ලිවීම් | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ලියන්න_ගොනුව_දත්ත(문서, 인사, sizeof(인사)-1); වසන්න_ගොනුව(문서); ලියන්න_ගොනුව_දත්ත(1, 인사, sizeof(인사)-1); return 0; }\n'
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            පෙළ = කවචය('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in පෙළ and 'exit 0' in පෙළ, පෙළ
            පෙළ = කවචය('run 한글.elf'); assert 'CC NATIVE PASS' in පෙළ and 'exit 0' in පෙළ, පෙළ
            assert 'CC NATIVE PASS' in කවචය('cat cc.txt')
            실행파일 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR ප්_රස්තාව_අගය.elf', io.BytesIO(실행파일)); පෙළ = කවචය('run ප්_රස්තාව_අගය.elf'); assert 'CC NATIVE PASS' in පෙළ and 'exit 0' in පෙළ, පෙළ
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR ක්_රියාත්මක_කරන්න_විධානය', io.BytesIO(실행파일)); පෙළ=කවචය('./ක්_රියාත්මක_කරන්න_විධානය');assert 'CC NATIVE PASS' in පෙළ and 'exit 0' in පෙළ,පෙළ
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR නම.txt', io.BytesIO(실행파일)); පෙළ=කවචය('./නම.txt');assert 'CC NATIVE PASS' in පෙළ and 'exit 0' in පෙළ,පෙළ
            කවචය('rm ක්_රියාත්මක_කරන්න_විධානය නම.txt')
            වලංගුකරණය_වාර්තාව['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            කවචය('rm binary.dat 한글.txt 한글.c 한글.elf ප්_රස්තාව_අගය.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(결과자료/'linux-reference')
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            පෙළ=කවචය('./리눅스인사');assert 'exit -8' in පෙළ,පෙළ
            පෙළ=කවචය('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in පෙළ,පෙළ
            assert 'LINUX ELF FILE IO' in කවචය('cat linux.txt')
            ගොනුව_මාරුව_සබැඳුම.delete('리눅스인사');ගොනුව_මාරුව_සබැඳුම.delete('linux.txt')
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in කවචය('./거짓.elf');ගොනුව_මාරුව_සබැඳුම.delete('거짓.elf')
            වලංගුකරණය_වාර්තාව['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = 결과자료/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket සම්බන්ද_වන්න = 한국어.자체.연결통신.සම්බන්ද_වන්න("10.0.2.2", Integer.parseInt(args[0]));
 සම්බන්ද_වන්න.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] මූලය = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<මූලය.length;i++) if (සම්බන්ද_වන්න.getInputStream().read() != (මූලය[i]&255)) throw new RuntimeException("TCP mismatch");
 සම්බන්ද_වන්න.close();
 DatagramSocket 종단 = 한국어.자체.통신.විවෘත_කරන්න(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.ඊමේල්(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(기준/'build/java-library/classes'),'-d',str(결과자료),str(통신원문)])
                ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 바깥통신.class', io.BytesIO((결과자료/'바깥통신.class').read_bytes()))
                පෙළ = කවචය('java 바깥통신 {} {}'.format(되돌림서버항목.සම්ප්_රේෂණ_පාලන_ප්_රොටොකෝලය_තොට, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in පෙළ and '10.0.2.2' in පෙළ and 'exit 0' in පෙළ, පෙළ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            වලංගුකරණය_වාර්තාව['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ගොනුව_මාරුව_සබැඳුම.delete('바깥통신.class')
            සේවාදායකය_මූලය=결과자료/'서버시험.java'
            සේවාදායකය_මූලය.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket සේවාදායකය_අගය = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket අමුත්තා_අගය = සේවාදායකය_අගය.accept();
  අමුත්තා_අගය.getOutputStream().write(අමුත්තා_අගය.getInputStream().read()+1); අමුත්තා_අගය.close(); සේවාදායකය_අගය.close();
  byte[] අන්තර්ගතය_අගය = new byte[8]; DatagramPacket 전문 = new DatagramPacket(අන්තර්ගතය_අගය, අන්තර්ගතය_අගය.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(සේවාදායකය_මූලය)])
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 서버시험.class',io.BytesIO((결과자료/'서버시험.class').read_bytes()))
            සැකසුම.stdin.write('java 서버시험\n'.encode());සැකසුම.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',සේවාදායකය_දහර_තොට),timeout=5) as සමානයා_අගය:
                සමානයා_අගය.sendall(b'A');assert සමානයා_අගය.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as සමානයා_අගය:
                සමානයා_අගය.settimeout(5);සමානයා_අගය.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert සමානයා_අගය.recvfrom(512)[0]==b'UDP-IN'
            පෙළ=수신하기();assert 'INBOUND TCP UDP PASS' in පෙළ and 'exit 0' in පෙළ,පෙළ
            වලංගුකරණය_වාර්තාව['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ගොනුව_මාරුව_සබැඳුම.delete('서버시험.class')
            උපදෙස_අනුක්_රමය = 'public class 빛 { public static void main(String[] විස්තාරක) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.출력.수쓰기(합); 한국어.자체.ගොනු.ලිවීම("aot.txt", "한글 AOT ගොනු 😀"); 한국어.자체.출력.ලියන්න_පේළිය(한국어.자체.ගොනු.කියවීම("aot.txt")); } }'
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 빛.java', io.BytesIO(උපදෙස_අනුක්_රමය.encode()))
            පෙළ = කවචය('javac 빛.java'); assert 'exit 0' in පෙළ and 'Compiled:' in පෙළ, පෙළ
            පෙළ = කවචය('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in පෙළ and 'exit 0' in පෙළ, පෙළ
            පෙළ = කවචය('run 빛.elf'); assert '\n55\n' in පෙළ and '한글 AOT ගොනු 😀' in පෙළ and 'exit 0' in පෙළ, පෙළ
            자체실행파일 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            පෙළ = කවචය('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in පෙළ and 'unsupported' in පෙළ, පෙළ
            보존자료 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ගොනුව_මාරුව_සබැඳුම.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            පෙළ = කවචය('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in පෙළ and 'exit 0' in පෙළ, පෙළ
            පෙළ = කවචය('run 빛.elf'); assert '\n55\n' in පෙළ and '한글 AOT ගොනු 😀' in පෙළ and 'exit 0' in පෙළ, පෙළ
            වලංගුකරණය_වාර්තාව['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            වලංගුකරණය_වාර්තාව['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ස්ථිතික_මූලය=결과자료/'정적시험.java'
            ස්ථිතික_මූලය.write_text('''public class 정적시험 {
 static int 기준 = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] විස්තාරක) {
  int[] අගය = new int[] {기준, 합(10)};
  System.out.println(අගය[0] + අගය[1]); System.out.println(විස්තාරක[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(결과자료),str(ස්ථිතික_මූලය)])
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 정적시험.class',io.BytesIO((결과자료/'정적시험.class').read_bytes()))
            පෙළ=කවචය('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in පෙළ,පෙළ
            පෙළ=කවචය('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in පෙළ,පෙළ
            ගොනුව_මාරුව_සබැඳුම.delete('정적시험.class');ගොනුව_මාරුව_සබැඳුම.delete('정적시험.elf')
            වලංගුකරණය_වාර්තාව['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(සංරක්ෂිතය.getvalue());손상자료[14]^=1
            ගොනුව_මාරුව_සබැඳුම.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            පෙළ=කවචය('java -jar 인사.jar');assert 'Main-Class\nexit 1' in පෙළ,පෙළ
            වලංගුකරණය_වාර්තාව['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ගොනුව_මාරුව_සබැඳුම.quit(); assert 'FTP stopped' in කවචය('ftpd stop')
            assert not පාලම.දෝෂය, පාලම.දෝෂය
            වලංගුකරණය_වාර්තාව.update(passed=True, frames_to_guest=පාලම.커널수신틀수, frames_from_guest=පාලම.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in වරකය.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            පාලම.විරාම_කරන්න_සිද්ධිය.set()
            සැකසුම.terminate()
            try: සැකසුම.wait(timeout=5)
            except subprocess.TimeoutExpired: සැකසුම.kill(); සැකසුම.wait()
            වරකය.close(); සැකසුම.stdin.close(); සැකසුම.stdout.close()
            වලංගුකරණය_වාර්තාව['bridge_error'] = පාලම.දෝෂය
            වලංගුකරණය_වාර්තාව['frames_to_guest'] = පාලම.커널수신틀수; වලංගුකරණය_වාර්තාව['frames_from_guest'] = පාලම.커널발신틀수
            (결과자료/'packets.json').write_text(json.dumps(පාලම.추적기록,indent=2)+'\n')
            (결과자료 / 'serial.log').write_bytes(대화기록)
            (결과자료 / 'report.json').write_text(json.dumps(වලංගුකරණය_වාර්තාව, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ක්_රියාත්මක_කරන්න_2()
