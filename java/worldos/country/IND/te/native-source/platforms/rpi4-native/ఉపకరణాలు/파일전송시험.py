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
from నెట్_వర్క్_బ్రిడ్జ్ import నెట్_వర్క్_బ్రిడ్జ్
from అమలు_చేయి_ఆదేశం import ప్రొజెక్ట్_మూలం, ఆదేశము
from 되돌림시험서버 import 되돌림시험서버
from 실행파일시험 import 리눅스예제


def నడుపుము():
    ప్రమాణం_డేటా = ప్రొజెక్ట్_మూలం / 'build/verification/ftp'; ప్రమాణం_డేటా.mkdir(parents=True, exist_ok=True)
    నిర్ధారణ_నివేదిక = {'passed': False, 'linux_loaded': False, 'checks': [],
              'kernel_sha256': hashlib.sha256((ప్రొజెక్ట్_మూలం / 'build/kernel8.img').read_bytes()).hexdigest()}
    대화기록 = bytearray()
    자바원문 = ప్రమాణం_డేటా / '꾸러미시험.java'
    자바원문.write_text('public class 꾸러미시험 { public static void main(String[] 인수) throws Exception { 한국어.자체.అవుట్పుట్.వ్రాయి_పంక్తి("JAR అమలు_చేయి_ఆదేశం: " + 인수[0]); 한국어.자체.దస్త్రం.వ్రాయుము("jar.txt", "자체 కెర్నల్_మూల్యం దస్త్రం"); 한국어.자체.అవుట్పుట్.వ్రాయి_పంక్తి(한국어.자체.దస్త్రం.చదువు("jar.txt")); } }', encoding='utf-8')
    subprocess.check_call(['javac', '--release', '8', '-encoding', 'UTF-8', '-cp', str(ప్రొజెక్ట్_మూలం/'build/java-library/classes'), '-d', str(ప్రమాణం_డేటా), str(자바원문)])
    ఆర్కైవ్ = io.BytesIO()
    with zipfile.ZipFile(ఆర్కైవ్, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
        자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 꾸러미시험\r\n\r\n')
        자바꾸러미.write(str(ప్రమాణం_డేటా/'꾸러미시험.class'), '꾸러미시험.class')
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); పోర్ట్_సంఖ్య = 임시자원.getsockname()[1]
    with socket.socket() as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); సర్వర్_ధార_పోర్టు = 임시자원.getsockname()[1]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as 임시자원:
        임시자원.bind(('127.0.0.1', 0)); 서버전문접속번호 = 임시자원.getsockname()[1]
    with నెట్_వర్క్_బ్రిడ్జ్(పోర్ట్_సంఖ్య, ['tcp:{}:9300'.format(సర్వర్_ధార_పోర్టు), 'udp:{}:9301'.format(서버전문접속번호)], సంగ్రహణ=True) as బ్రిడ్జ్:
        క్రమణం = subprocess.Popen(ఆదేశము() + ['-display', 'none', '-monitor', 'none', '-serial', 'stdio'] + బ్రిడ్జ్.전달인수(),
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=0)
        సెలక్టర్ = selectors.DefaultSelector(); సెలక్టర్.register(క్రమణం.stdout, selectors.EVENT_READ)
        def 수신하기(확인표시=b'jkoros-native> ', 시간제한=60):
            డేటా = bytearray(); ముగించు_ఆఫ్_సెట్ = time.monotonic() + 시간제한
            while 확인표시 not in డేటా:
                if time.monotonic() > ముగించు_ఆఫ్_సెట్ or క్రమణం.poll() is not None:
                    raise AssertionError('UART timeout/exit: ' + డేటా.decode('utf-8', 'replace'))
                for 누름값, _ in సెలక్టర్.select(.1):
                    조각 = 누름값.fileobj.read(4096)
                    if 조각: డేటా.extend(조각); 대화기록.extend(조각)
                if b'PANIC:' in డేటా or b'FAIL ' in డేటా: raise AssertionError(డేటా)
            return డేటా.decode('utf-8', 'replace').replace('\r\n', '\n')
        def షెల్(పంక్తి):
            క్రమణం.stdin.write(పంక్తి.encode() + b'\n'); క్రమణం.stdin.flush(); return 수신하기()
        try:
            수신하기(); assert 'FTP listening' in షెల్('ftpd start')
            ఫైలు_బదిలీ_కనెక్షన్ = ftplib.FTP(); ఫైలు_బదిలీ_కనెక్షన్.encoding = 'utf-8'; ఫైలు_బదిలీ_కనెక్షన్.connect('127.0.0.1', పోర్ట్_సంఖ్య, timeout=20); ఫైలు_బదిలీ_కనెక్షన్.login()
            చెల్లింపుభారం_డేటా = bytes(range(256)) * 32
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR binary.dat', io.BytesIO(చెల్లింపుభారం_డేటా))
            ప్రమాణం = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR binary.dat', ప్రమాణం.extend)
            assert ప్రమాణం == చెల్లింపుభారం_డేటా; assert ఫైలు_బదిలీ_కనెక్షన్.size('binary.dat') == len(చెల్లింపుభారం_డేటా)
            నిర్ధారణ_నివేదిక['checks'].append('real TCP PASV binary STOR/RETR and SIZE, 8192 bytes including SLIP escapes')
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 한글.txt', io.BytesIO('안녕하세요 😀\n'.encode()))
            assert '안녕하세요 😀' in షెల్('cat 한글.txt')
            assert '한글.txt' in ఫైలు_బదిలీ_కనెక్షన్.nlst()
            assert dict(ఫైలు_బదిలీ_కనెక్షన్.mlsd())['한글.txt']['size'] == str(len('안녕하세요 😀\n'.encode()))
            నిర్ధారణ_నివేదిక['checks'].append('UTF-8 filename and content visible in guest shell')
            try: ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR binary.dat', io.BytesIO(b'x' * 16385))
            except ftplib.error_perm as 보조항목: assert str(보조항목).startswith('552'), str(보조항목)
            else: raise AssertionError('oversized upload accepted')
            ప్రమాణం = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR binary.dat', ప్రమాణం.extend); assert ప్రమాణం == చెల్లింపుభారం_డేటా
            నిర్ధారణ_నివేదిక['checks'].append('oversized replacement rejected; previous file preserved')
            with ఫైలు_బదిలీ_కనెక్షన్.transfercmd('STOR pending.txt') as అప్_లోడ్_ఫైల్_లు:
                # A control command must not change the active upload's destination.
                assert ఫైలు_బదిలీ_కనెక్షన్.size('binary.dat') == len(చెల్లింపుభారం_డేటా)
                అప్_లోడ్_ఫైల్_లు.sendall(b'UPLOAD TARGET PRESERVED')
            assert ఫైలు_బదిలీ_కనెక్షన్.voidresp().startswith('226')
            ప్రమాణం = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR pending.txt', ప్రమాణం.extend)
            assert ప్రమాణం == b'UPLOAD TARGET PRESERVED'
            ప్రమాణం = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR binary.dat', ప్రమాణం.extend)
            assert ప్రమాణం == చెల్లింపుభారం_డేటా
            ఫైలు_బదిలీ_కనెక్షన్.delete('pending.txt')
            నిర్ధారణ_నివేదిక['checks'].append('interleaved SIZE cannot change the active STOR destination')
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 인사.jar', io.BytesIO(ఆర్కైవ్.getvalue()))
            పాఠ్యము = షెల్('java -jar 인사.jar 누리')
            assert 'JAR అమలు_చేయి_ఆదేశం: 누리' in పాఠ్యము and '자체 కెర్నల్_మూల్యం దస్త్రం' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            పాఠ్యము = షెల్('./인사.jar 세상')
            assert 'JAR అమలు_చేయి_ఆదేశం: 세상' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            నిర్ధారణ_నివేదిక['checks'].append('DEFLATE JAR upload, Main-Class, Korean API/file I/O, arguments, java -jar and direct shell execution')
            원본자료 = '#include <파일규약.h>\nstruct డేటా { int 수; double 비율; };\nint 합(int n) { return n ? n + 합(n-1) : 0; }\nint main(void) { struct డేటా మూల్యం = {합(10), 1.25}; if (మూల్యం.수 != 55 || మూల్యం.비율 * 2 != 2.5) return 3; const char 인사[] = "CC NATIVE PASS\\n"; int 문서 = తెరువు_ఫైలు("cc.txt", పఠన_లేఖన | 없으면만들기 | 내용비우기, 0600); if (문서 < 0) return 1; వ్రాయి_ఫైలు_డేటా(문서, 인사, sizeof(인사)-1); మూసివేయి_ఫైలు(문서); వ్రాయి_ఫైలు_డేటా(1, 인사, sizeof(인사)-1); return 0; }\n'
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 한글.c', io.BytesIO(원본자료.encode()))
            పాఠ్యము = షెల్('cc 한글.c -o 한글.elf'); assert 'Compiled native ARM64 ELF:' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            పాఠ్యము = షెల్('run 한글.elf'); assert 'CC NATIVE PASS' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            assert 'CC NATIVE PASS' in షెల్('cat cc.txt')
            실행파일 = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR 한글.elf', 실행파일.extend)
            assert 실행파일[:4] == b'\x7fELF' and 실행파일[18:20] == b'\xb7\x00'
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR కాపీ_మూల్యం.elf', io.BytesIO(실행파일)); పాఠ్యము = షెల్('run కాపీ_మూల్యం.elf'); assert 'CC NATIVE PASS' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR అమలు_చేయి_ఆదేశం', io.BytesIO(실행파일)); పాఠ్యము=షెల్('./అమలు_చేయి_ఆదేశం');assert 'CC NATIVE PASS' in పాఠ్యము and 'exit 0' in పాఠ్యము,పాఠ్యము
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR పేరు.txt', io.BytesIO(실행파일)); పాఠ్యము=షెల్('./పేరు.txt');assert 'CC NATIVE PASS' in పాఠ్యము and 'exit 0' in పాఠ్యము,పాఠ్యము
            షెల్('rm అమలు_చేయి_ఆదేశం పేరు.txt')
            నిర్ధారణ_నివేదిక['checks'].append('guest TinyCC compiles UTF-8 C with recursion/struct/double and Korean POSIX; ELF64 download, re-upload and EL0 execution')
            షెల్('rm binary.dat 한글.txt 한글.c 한글.elf కాపీ_మూల్యం.elf cc.txt jar.txt')
            리눅스파일,예상결과=리눅스예제(ప్రమాణం_డేటా/'linux-reference')
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 리눅스인사',io.BytesIO(리눅스파일.read_bytes()))
            పాఠ్యము=షెల్('./리눅스인사');assert 'exit -8' in పాఠ్యము,పాఠ్యము
            పాఠ్యము=షెల్('run --linux 리눅스인사 한글인수');assert 예상결과+'exit 0' in పాఠ్యము,పాఠ్యము
            assert 'LINUX ELF FILE IO' in షెల్('cat linux.txt')
            ఫైలు_బదిలీ_కనెక్షన్.delete('리눅스인사');ఫైలు_బదిలీ_కనెక్షన్.delete('linux.txt')
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 거짓.elf',io.BytesIO(b'plain text'))
            assert '실행할 수 없습니다:' in షెల్('./거짓.elf');ఫైలు_బదిలీ_కనెక్షన్.delete('거짓.elf')
            నిర్ధారణ_నివేదిక['checks'].append('ELF header detection independent of suffix, extensionless and .txt native binaries; same extensionless Linux ARM64 ELF uploaded and run through explicit Linux ABI')
            with 되돌림시험서버() as 되돌림서버항목:
                통신원문 = ప్రమాణం_డేటా/'바깥통신.java'
                통신원문.write_text('''import java.net.*; import java.io.*;
public class 바깥통신 { public static void main(String[] args) throws Exception {
 Socket కనెక్టుచేయి = 한국어.자체.연결통신.కనెక్టుచేయి("10.0.2.2", Integer.parseInt(args[0]));
 కనెక్టుచేయి.getOutputStream().write("TCP 한글\\n".getBytes("UTF-8"));
 byte[] వనరు = "TCP 한글\\n".getBytes("UTF-8");
 for (int i=0;i<వనరు.length;i++) if (కనెక్టుచేయి.getInputStream().read() != (వనరు[i]&255)) throw new RuntimeException("TCP mismatch");
 కనెక్టుచేయి.close();
 DatagramSocket 종단 = 한국어.자체.통신.తెరువు(0); 한국어.자체.통신.대기시간(종단, 500);
 한국어.자체.통신.పంపు(종단, "10.0.2.2", Integer.parseInt(args[1]), "UDP 한글");
 if (!한국어.자체.통신.받기(종단).equals("UDP 한글")) throw new RuntimeException("UDP mismatch");
 종단.close(); System.out.println(InetAddress.getByName("10.0.2.2").getHostAddress()); System.out.println("EXTERNAL TCP UDP PASS");
} }''', encoding='utf-8')
                subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-cp',str(ప్రొజెక్ట్_మూలం/'build/java-library/classes'),'-d',str(ప్రమాణం_డేటా),str(통신원문)])
                ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 바깥통신.class', io.BytesIO((ప్రమాణం_డేటా/'바깥통신.class').read_bytes()))
                పాఠ్యము = షెల్('java 바깥통신 {} {}'.format(되돌림서버항목.ట్రాన్స్_మిషన్_కంట్రోల్_ప్రోటోకాల్_పోర్టు, 되돌림서버항목.전문접속번호))
                assert 'EXTERNAL TCP UDP PASS' in పాఠ్యము and '10.0.2.2' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
                assert 되돌림서버항목.수신됨 == {'tcp':'TCP 한글\n'.encode(), 'udp':'UDP 한글'.encode()}, 되돌림서버항목.수신됨
                assert not 되돌림서버항목.오류들, 되돌림서버항목.오류들
            నిర్ధారణ_నివేదిక['checks'].append('guest Java/Korean Socket and DatagramSocket send real IPv4 TCP/UDP to independent host peers')
            ఫైలు_బదిలీ_కనెక్షన్.delete('바깥통신.class')
            సర్వర్_మూలం=ప్రమాణం_డేటా/'서버시험.java'
            సర్వర్_మూలం.write_text('''import java.net.*; public class 서버시험 {
 public static void main(String[] args) throws Exception {
  ServerSocket సర్వర్_మూల్యం = new ServerSocket(9300); DatagramSocket 종단 = new DatagramSocket(9301);
  System.out.println("SERVER READY"); Socket అతిథి_మూల్యం = సర్వర్_మూల్యం.accept();
  అతిథి_మూల్యం.getOutputStream().write(అతిథి_మూల్యం.getInputStream().read()+1); అతిథి_మూల్యం.close(); సర్వర్_మూల్యం.close();
  byte[] విషయం_మూల్యం = new byte[8]; DatagramPacket 전문 = new DatagramPacket(విషయం_మూల్యం, విషయం_మూల్యం.length); 종단.receive(전문);
  종단.send(전문); 종단.close(); System.out.println("INBOUND TCP UDP PASS");
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ప్రమాణం_డేటా),str(సర్వర్_మూలం)])
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 서버시험.class',io.BytesIO((ప్రమాణం_డేటా/'서버시험.class').read_bytes()))
            క్రమణం.stdin.write('java 서버시험\n'.encode());క్రమణం.stdin.flush();수신하기(b'SERVER READY\r\n')
            with socket.create_connection(('127.0.0.1',సర్వర్_ధార_పోర్టు),timeout=5) as పియర్_మూల్యం:
                పియర్_మూల్యం.sendall(b'A');assert పియర్_మూల్యం.recv(1)==b'B'
            with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as పియర్_మూల్యం:
                పియర్_మూల్యం.settimeout(5);పియర్_మూల్యం.sendto(b'UDP-IN',('127.0.0.1',서버전문접속번호));assert పియర్_మూల్యం.recvfrom(512)[0]==b'UDP-IN'
            పాఠ్యము=수신하기();assert 'INBOUND TCP UDP PASS' in పాఠ్యము and 'exit 0' in పాఠ్యము,పాఠ్యము
            నిర్ధారణ_నివేదిక['checks'].append('host initiates TCP/UDP to guest ServerSocket/DatagramSocket through explicit port forwards')
            ఫైలు_బదిలీ_కనెక్షన్.delete('서버시험.class')
            명령열 = 'public class 빛 { public static void main(String[] 인수) throws Exception { int 합 = 0; int 수 = 1; while (수 <= 10) { 합 = 합 + 수; 수 = 수 + 1; } 한국어.자체.అవుట్పుట్.수쓰기(합); 한국어.자체.దస్త్రం.వ్రాయుము("aot.txt", "한글 AOT దస్త్రం 😀"); 한국어.자체.అవుట్పుట్.వ్రాయి_పంక్తి(한국어.자체.దస్త్రం.చదువు("aot.txt")); } }'
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 빛.java', io.BytesIO(명령열.encode()))
            పాఠ్యము = షెల్('javac 빛.java'); assert 'exit 0' in పాఠ్యము and 'Compiled:' in పాఠ్యము, పాఠ్యము
            పాఠ్యము = షెల్('jaot 빛.class -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            పాఠ్యము = షెల్('run 빛.elf'); assert '\n55\n' in పాఠ్యము and '한글 AOT దస్త్రం 😀' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            자체실행파일 = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR 빛.elf', 자체실행파일.extend)
            పాఠ్యము = షెల్('jaot 인사.jar -o 빛.elf'); assert 'exit 1' in పాఠ్యము and 'unsupported' in పాఠ్యము, పాఠ్యము
            보존자료 = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR 빛.elf', 보존자료.extend); assert 자체실행파일 == 보존자료
            바이트코드 = bytearray(); ఫైలు_బదిలీ_కనెక్షన్.retrbinary('RETR 빛.class', 바이트코드.extend)
            묶인자료 = io.BytesIO()
            with zipfile.ZipFile(묶인자료, 'w', zipfile.ZIP_DEFLATED) as 자바꾸러미:
                자바꾸러미.writestr('META-INF/MANIFEST.MF', 'Manifest-Version: 1.0\r\nMain-Class: 빛\r\n\r\n')
                자바꾸러미.writestr('빛.class', 바이트코드)
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 빛.jar', io.BytesIO(묶인자료.getvalue()))
            పాఠ్యము = షెల్('jaot 빛.jar -o 빛.elf'); assert 'AOT compiled native ARM64 ELF:' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            పాఠ్యము = షెల్('run 빛.elf'); assert '\n55\n' in పాఠ్యము and '한글 AOT దస్త్రం 😀' in పాఠ్యము and 'exit 0' in పాఠ్యము, పాఠ్యము
            నిర్ధారణ_నివేదిక['checks'].append('guest javac -> guest jaot -> native ARM64 ELF executes arithmetic and Korean file/print intrinsics')
            నిర్ధారణ_నివేదిక['checks'].append('guest JAR -> native AOT ELF; unsupported bytecode rejected without overwriting previous ELF; MUTF-8 emoji')
            నిశ్చల_మూలం=ప్రమాణం_డేటా/'정적시험.java'
            నిశ్చల_మూలం.write_text('''public class 정적시험 {
 static int ప్రొజెక్ట్_మూలం = 3;
 static int 합(int n) { return n == 0 ? 0 : n + 합(n-1); }
 public static void main(String[] 인수) {
  int[] మూల్యం = new int[] {ప్రొజెక్ట్_మూలం, 합(10)};
  System.out.println(మూల్యం[0] + మూల్యం[1]); System.out.println(인수[0]);
 }
}''',encoding='utf-8')
            subprocess.check_call(['javac','--release','8','-encoding','UTF-8','-d',str(ప్రమాణం_డేటా),str(నిశ్చల_మూలం)])
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 정적시험.class',io.BytesIO((ప్రమాణం_డేటా/'정적시험.class').read_bytes()))
            పాఠ్యము=షెల్('jaot 정적시험.class -o 정적시험.elf');assert 'exit 0' in పాఠ్యము,పాఠ్యము
            పాఠ్యము=షెల్('run 정적시험.elf 한글인수');assert '\n58\n한글인수\nexit 0' in పాఠ్యము,పాఠ్యము
            ఫైలు_బదిలీ_కనెక్షన్.delete('정적시험.class');ఫైలు_బదిలీ_కనెక్షన్.delete('정적시험.elf')
            నిర్ధారణ_నివేదిక['checks'].append('native AOT static initialization, recursion, arrays and Unicode arguments')
            손상자료=bytearray(ఆర్కైవ్.getvalue());손상자료[14]^=1
            ఫైలు_బదిలీ_కనెక్షన్.storbinary('STOR 인사.jar',io.BytesIO(손상자료))
            పాఠ్యము=షెల్('java -jar 인사.jar');assert 'Main-Class\nexit 1' in పాఠ్యము,పాఠ్యము
            నిర్ధారణ_నివేదిక['checks'].append('tampered ZIP metadata rejected by guest JAR loader')
            ఫైలు_బదిలీ_కనెక్షన్.quit(); assert 'FTP stopped' in షెల్('ftpd stop')
            assert not బ్రిడ్జ్.దోషం, బ్రిడ్జ్.దోషం
            నిర్ధారణ_నివేదిక.update(passed=True, frames_to_guest=బ్రిడ్జ్.커널수신틀수, frames_from_guest=బ్రిడ్జ్.커널발신틀수)
            print('PASS native ARM64 TCP/FTP upload, download, Unicode, failed overwrite preservation')
        finally:
            for 누름값,_ in సెలక్టర్.select(0):
                조각=누름값.fileobj.read(65536)
                if 조각: 대화기록.extend(조각)
            బ్రిడ్జ్.నిలుపు_ఈవెంట్.set()
            క్రమణం.terminate()
            try: క్రమణం.wait(timeout=5)
            except subprocess.TimeoutExpired: క్రమణం.kill(); క్రమణం.wait()
            సెలక్టర్.close(); క్రమణం.stdin.close(); క్రమణం.stdout.close()
            నిర్ధారణ_నివేదిక['bridge_error'] = బ్రిడ్జ్.దోషం
            నిర్ధారణ_నివేదిక['frames_to_guest'] = బ్రిడ్జ్.커널수신틀수; నిర్ధారణ_నివేదిక['frames_from_guest'] = బ్రిడ్జ్.커널발신틀수
            (ప్రమాణం_డేటా/'packets.json').write_text(json.dumps(బ్రిడ్జ్.జాడ_లాగ్,indent=2)+'\n')
            (ప్రమాణం_డేటా / 'serial.log').write_bytes(대화기록)
            (ప్రమాణం_డేటా / 'report.json').write_text(json.dumps(నిర్ధారణ_నివేదిక, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__': నడుపుము()
