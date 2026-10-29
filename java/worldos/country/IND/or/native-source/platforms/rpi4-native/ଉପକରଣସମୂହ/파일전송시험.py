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
from ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍ import ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍
from ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ import ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, ନିର୍ଦ୍ଦେଶ
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def ଚଳାନ୍ତୁ():
    ମାପ_ଡାଟା = ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/verification/ftp'; ମାପ_ଡାଟା.mkdir(parents=True, exist_ok=True)
    ବୈଧକରଣ_ରିପୋର୍ଟ = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ମାପ_ଡାଟା / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.ନିର୍ଗମ.ଲିଖନ_ରେଖା("JAR ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ: " + 인수[0]); 한국어.자체.ଫାଇଲ.ଲେଖନ୍ତୁ("jar.txt", "자체 କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ ଫାଇଲ"); 한국어.자체.ନିର୍ଗମ.ଲିଖନ_ରେଖା(한국어.자체.ଫାଇଲ.ପଢନ୍ତୁ("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/java-library/classes'), '-d', str(ମାପ_ଡାଟା), str(자바원문)])
    ଅଭିଲେଖାଗାର = io.BytesIO()
    with zipfile.ZipFile(ଅଭିଲେଖାଗାର, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ମାପ_ଡାଟା/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ପୋର୍ଟ୍_ନମ୍ଵର୍ = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); ସର୍ଭର୍_ଷ୍ଟ୍ରିମ୍_ପୋର୍ଟ = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with ନେଟ୍_ୱାର୍କ୍_ବ୍ରିଜ୍(ପୋର୍ଟ୍_ନମ୍ଵର୍, ['tcp:{}:9300'.format(ସର୍ଭର୍_ଷ୍ଟ୍ରିମ୍_ପୋର୍ଟ), 'udp:{}:9301'.format(서버전문접속번호)], କ୍ୟାପଚର୍_କରିବା=True) as ବ୍ରିଜ୍:
        ପ୍ରକ୍ରିୟା = subprocess.Popen(ନିର୍ଦ୍ଦେଶ() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + ବ୍ରିଜ୍.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        ଚୟନକାରୀ = selectors.DefaultSelector(); ଚୟନକାରୀ.register(ପ୍ରକ୍ରିୟା.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            ଡାଟା = bytearray(); ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍ = time.monotonic() + 시간제한
            while 확인표시 not in ଡାଟା:
                if time.monotonic() > ଶେଷ_କରନ୍ତୁ_ଅଫ୍_ସେଟ୍ or ପ୍ରକ୍ରିୟା.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + ଡାଟା.decode('utf-8', 'replace'))
                for 누름값, _ in ଚୟନକାରୀ.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: ଡାଟା.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in ଡାଟା or b'FAIL ' in ଡାଟା: raise AssertionError(ଡାଟା)
            return ଡାଟା.decode('utf-8', 'replace').replace('\r\n', '\n')
        def ଖୋଳ(ରେଖା):
            ପ୍ରକ୍ରିୟା.stdin.write(ରେଖା.encode() + b'\n'); ପ୍ରକ୍ରିୟା.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in ଖୋଳ('ftpd start')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ = ftplib.FTP(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.encoding = 'utf-8'; ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.connect('127.0.0.1', ପୋର୍ଟ୍_ନମ୍ଵର୍, timeout=20); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.login()
            ପେଲୋଡ୍_ଡାଟା = bytes(range(256)) * 32
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR binary.dat', io.BytesIO(ପେଲୋଡ୍_ଡାଟା))
            ମାପ = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR binary.dat', ମାପ.extend)
            assert ମାପ == ପେଲୋଡ୍_ଡାଟା; assert ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.size('binary.dat') == len(ପେଲୋଡ୍_ଡାଟା)
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in ଖୋଳ('cat 한글.txt')
            assert '한글.txt' in ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.nlst()
            assert dict(ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ମାପ = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR binary.dat', ମାପ.extend); assert ମାପ == ପେଲୋଡ୍_ଡାଟା
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('oversized replacement rejected; previous file preserved')
            with ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.transfercmd('STOR pending.txt') as ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ:
                # A control command must not change the active upload's destination.
                assert ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.size('binary.dat') == len(ପେଲୋଡ୍_ଡାଟା)
                ଅପଲୋଡ୍_ଫାଇଲ୍_ଗୁଡିକ.sendall(b'UPLOAD TARGET PRESERVED')
            assert ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.voidresp().startswith('226')
            ମାପ = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR pending.txt', ମାପ.extend)
            assert ମାପ == b'UPLOAD TARGET PRESERVED'
            ମାପ = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR binary.dat', ମାପ.extend)
            assert ମାପ == ପେଲୋଡ୍_ଡାଟା
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('pending.txt')
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 인사.jar', io.BytesIO(ଅଭିଲେଖାଗାର.getvalue()))
            ପାଠ୍ଯ = ଖୋଳ('java -jar 인사.jar 누리')
            assert 'JAR ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ: 누리' in ପାଠ୍ଯ and '자체 କେନ୍ଦ୍ରିକ_ମୂଲ୍ୟ ଫାଇଲ' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ପାଠ୍ଯ = ଖୋଳ('./인사.jar 세상')
            assert 'JAR ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ: 세상' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct ଡାଟା { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct ଡାଟା ମୂଲ୍ୟ = {합(10), 1.25}; if (ମୂଲ୍ୟ.수 != 55 || ମୂଲ୍ୟ.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = ଖୋଲିବା_ଫାଇଲ୍("cc.txt", ପଢିବା_ଲେଖିବା | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; ଲିଖନ_ଫାଇଲ୍_ଡାଟା(문서, 인사, sizeof(인사)-1); ବନ୍ଦ_ଫାଇଲ୍(문서); ଲିଖନ_ଫାଇଲ୍_ଡାଟା(1, 인사, sizeof(인사)-1); return 0; }\n'
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            ପାଠ୍ଯ = ଖୋଳ('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ପାଠ୍ଯ = ଖୋଳ('run 한글.elf'); assert 'CC NATIVE PASS' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            assert 'CC NATIVE PASS' in ଖୋଳ('cat cc.txt')
            실행파일 = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR କପି_ମୂଲ୍ୟ.elf', io.BytesIO(실행파일)); ପାଠ୍ଯ = ଖୋଳ('run କପି_ମୂଲ୍ୟ.elf'); assert 'CC NATIVE PASS' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ', io.BytesIO(실행파일)); ପାଠ୍ଯ=ଖୋଳ('./ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ');assert 'CC NATIVE PASS' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ,ପାଠ୍ଯ
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR ନାମ.txt', io.BytesIO(실행파일)); ପାଠ୍ଯ=ଖୋଳ('./ନାମ.txt');assert 'CC NATIVE PASS' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ,ପାଠ୍ଯ
            ଖୋଳ('rm ନିର୍ବାହ_କରିବା_ନିର୍ଦ୍ଦେଶ ନାମ.txt')
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            ଖୋଳ('rm binary.dat 한글.txt 한글.c 한글.elf କପି_ମୂଲ୍ୟ.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ମାପ_ଡାଟା/'linux-reference')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            ପାଠ୍ଯ=ଖୋଳ('./리눅스인사');assert 'exit -8' in ପାଠ୍ଯ,ପାଠ୍ଯ
            ପାଠ୍ଯ=ଖୋଳ('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in ପାଠ୍ଯ,ପାଠ୍ଯ
            assert 'LINUX ELF FILE IO' in ଖୋଳ('cat linux.txt')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('리눅스인사');ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('linux.txt')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in ଖୋଳ('./거짓.elf');ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('거짓.elf')
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ମାପ_ଡାଟା/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket ସଂଯୋଗ_କରନ୍ତୁ = 한국어.자체.연결통신.ସଂଯୋଗ_କରନ୍ତୁ("10.0.2.2", Integer.parseInt(args[0]));
 ସଂଯୋଗ_କରନ୍ତୁ.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] ଉତ୍ସ = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<ଉତ୍ସ.length;i++) if (ସଂଯୋଗ_କରନ୍ତୁ.getInputStream().read() != (ଉତ୍ସ[i]&255)) throw new RuntimeException("TCP mismatch");
 ସଂଯୋଗ_କରନ୍ତୁ.close();
 DatagramSocket 종단 = 한국어.자체.통신.ଖୋଲନ୍ତୁ(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.ପଠାନ୍ତୁ(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍/'build/java-library/classes'),'-d',str(ମାପ_ଡାଟା),str(통신원문)])
                ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 바깥통신.class', io.BytesIO((ମାପ_ଡାଟା/'바깥통신.class').read_bytes()))
                ପାଠ୍ଯ = ଖୋଳ('java 바깥통신 {} {}'.format(되돌림서버항목.ପ୍ରେରଣ_ନିୟନ୍ତ୍ରଣ_ପ୍ରୋଟୋକଲ୍_ପୋର୍ଟ, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in ପାଠ୍ଯ and '10.0.2.2' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('바깥통신.class')
            ସର୍ଭର୍_ଉତ୍ସ=ମାପ_ଡାଟା/'서버시험.java'
            ସର୍ଭର୍_ଉତ୍ସ.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket ସର୍ଭର୍_ମୂଲ୍ୟ = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket ଅତିଥି_ମୂଲ୍ୟ = ସର୍ଭର୍_ମୂଲ୍ୟ.accept();
  ଅତିଥି_ମୂଲ୍ୟ.getOutputStream().write(ଅତିଥି_ମୂଲ୍ୟ.getInputStream().read()+1); ଅତିଥି_ମୂଲ୍ୟ.close(); ସର୍ଭର୍_ମୂଲ୍ୟ.close();
  byte[] ବିଷୟ_ମୂଲ୍ୟ = new byte[8]; DatagramPacket 전문 = new DatagramPacket(ବିଷୟ_ମୂଲ୍ୟ, ବିଷୟ_ମୂଲ୍ୟ.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ମାପ_ଡାଟା),str(ସର୍ଭର୍_ଉତ୍ସ)])
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 서버시험.class',io.BytesIO((ମାପ_ଡାଟା/'서버시험.class').read_bytes()))
            ପ୍ରକ୍ରିୟା.stdin.write('java 서버시험\n'.encode());ପ୍ରକ୍ରିୟା.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',ସର୍ଭର୍_ଷ୍ଟ୍ରିମ୍_ପୋର୍ଟ),timeout=5) as ସମକକ୍ଷ_ମୂଲ୍ୟ:
                ସମକକ୍ଷ_ମୂଲ୍ୟ.sendall(b'A');assert ସମକକ୍ଷ_ମୂଲ୍ୟ.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as ସମକକ୍ଷ_ମୂଲ୍ୟ:
                ସମକକ୍ଷ_ମୂଲ୍ୟ.settimeout(5);ସମକକ୍ଷ_ମୂଲ୍ୟ.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert ସମକକ୍ଷ_ମୂଲ୍ୟ.recvfrom(512)[0]==b'UDP-IN'
            ପାଠ୍ଯ=수신하기();assert 'INBOUND TCP UDP PASS' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ,ପାଠ୍ଯ
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.ନିର୍ଗମ.수쓰기(합); 한국어.자체.ଫାଇଲ.ଲେଖନ୍ତୁ("aot.txt", "한글 AOT ଫାଇଲ 😀"); 한국어.자체.ନିର୍ଗମ.ଲିଖନ_ରେଖା(한국어.자체.ଫାଇଲ.ପଢନ୍ତୁ("aot.txt")); } }'
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            ପାଠ୍ଯ = ଖୋଳ('javac 빛.java'); assert 'exit 0' in ପାଠ୍ଯ and 'Compiled:' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ପାଠ୍ଯ = ଖୋଳ('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ପାଠ୍ଯ = ଖୋଳ('run 빛.elf'); assert '\n55\n' in ପାଠ୍ଯ and '한글 AOT ଫାଇଲ 😀' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            자체실행파일 = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            ପାଠ୍ଯ = ଖୋଳ('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in ପାଠ୍ଯ and 'unsupported' in ପାଠ୍ଯ, ପାଠ୍ଯ
            보존자료 = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            ପାଠ୍ଯ = ଖୋଳ('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ପାଠ୍ଯ = ଖୋଳ('run 빛.elf'); assert '\n55\n' in ପାଠ୍ଯ and '한글 AOT ଫାଇଲ 😀' in ପାଠ୍ଯ and 'exit 0' in ପାଠ୍ଯ, ପାଠ୍ଯ
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            ସ୍ଥିର_ଉତ୍ସ=ମାପ_ଡାଟା/'정적시험.java'
            ସ୍ଥିର_ଉତ୍ସ.write_text('''public class 정적시험 {
 static int ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍ = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] ମୂଲ୍ୟ = new int[] {ପ୍ରୋଜେକ୍ଟ୍_ରୁଟ୍, 합(10)};
  System.out.println(ମୂଲ୍ୟ[0] + ମୂଲ୍ୟ[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ମାପ_ଡାଟା),str(ସ୍ଥିର_ଉତ୍ସ)])
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 정적시험.class',io.BytesIO((ମାପ_ଡାଟା/'정적시험.class').read_bytes()))
            ପାଠ୍ଯ=ଖୋଳ('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in ପାଠ୍ଯ,ପାଠ୍ଯ
            ପାଠ୍ଯ=ଖୋଳ('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in ପାଠ୍ଯ,ପାଠ୍ଯ
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('정적시험.class');ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.delete('정적시험.elf')
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ଅଭିଲେଖାଗାର.getvalue());손상자료[14]^=1
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            ପାଠ୍ଯ=ଖୋଳ('java -jar 인사.jar');assert 'Main-Class\nexit 1' in ପାଠ୍ଯ,ପାଠ୍ଯ
            ବୈଧକରଣ_ରିପୋର୍ଟ['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ଫାଇଲ୍_ସ୍ଥାନାନ୍ତର_ସଂଯୋଗ.quit(); assert 'FTP stopped' in ଖୋଳ('ftpd stop')
            assert not ବ୍ରିଜ୍.ତ୍ରୁଟି, ବ୍ରିଜ୍.ତ୍ରୁଟି
            ବୈଧକରଣ_ରିପୋର୍ଟ.update(passed=True, frames_to_guest=ବ୍ରିଜ୍.커널수신틀수, frames_from_guest=ବ୍ରିଜ୍.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in ଚୟନକାରୀ.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            ବ୍ରିଜ୍.ବିରାମ_ଘଟଣା.set()
            ପ୍ରକ୍ରିୟା.terminate()
            try: ପ୍ରକ୍ରିୟା.wait(timeout=5)
            except subprocess.TimeoutExpired: ପ୍ରକ୍ରିୟା.kill(); ପ୍ରକ୍ରିୟା.wait()
            ଚୟନକାରୀ.close(); ପ୍ରକ୍ରିୟା.stdin.close(); ପ୍ରକ୍ରିୟା.stdout.close()
            ବୈଧକରଣ_ରିପୋର୍ଟ['bridge_error'] = ବ୍ରିଜ୍.ତ୍ରୁଟି
            ବୈଧକରଣ_ରିପୋର୍ଟ['frames_to_guest'] = ବ୍ରିଜ୍.커널수신틀수; ବୈଧକରଣ_ରିପୋର୍ଟ['frames_from_guest'] = ବ୍ରିଜ୍.커널발신틀수
            (ମାପ_ଡାଟା/'packets.json').write_text(json.dumps(ବ୍ରିଜ୍.ଚିହ୍ନଟ_ଲଗ୍,indent=2)+'\n')
            (ମାପ_ଡାଟା / 'serial.log').write_bytes(대화기록)
            (ମାପ_ଡାଟା / 'report.json').write_text(json.dumps(ବୈଧକରଣ_ରିପୋର୍ଟ, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': ଚଳାନ୍ତୁ()
